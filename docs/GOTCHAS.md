# Gotchas

Cosas que rompen el pipeline en silencio. Todas encontradas corriendo material
real, no leyendo documentación.

---

## 1. Los tiempos de palabra de whisper.cpp son interpolados

Con `-ml 1`, whisper.cpp devuelve una palabra por segmento, pero **el `fin` de
una palabra es exactamente el `inicio` de la siguiente**. No hay huecos. Son
tiempos repartidos por el alineador, no bordes acústicos reales.

```
00:01:53.560 --> 00:01:54.300   ita
00:01:54.300 --> 00:01:54.800   ,
00:01:54.800 --> 00:01:55.310   ya
```

**Consecuencia:** no se puede detectar silencio desde la transcripción. Un
detector de frases basado en huecos encuentra cero. Pasó: sobre 473 palabras
detectó **4 frases** y 0,07 s de aire.

> **El silencio sale del audio, siempre.** La transcripción sirve para saber
> QUÉ se dijo y aproximadamente cuándo. Para saber DÓNDE cortar hay que medir
> la señal. (`REGLAS.md` 2.1 y 2.2.)

---

## 1 bis. `-ml 1` da TOKENS, no palabras, y en español parte palabras

El mismo flag que parece dar "una palabra por segmento" en realidad da **un
token**. En español los tokens de whisper parten palabras por la mitad:

```
hic + imos   ->  subtitulo: "HIC IMOS"
env + ío     ->  subtitulo: "ENV ÍO"
conect + ada ->  subtitulo: "CONECT ADA"
interval + o ->  subtitulo: "INTERVAL O"
```

Pasó de verdad y llegó hasta el video renderizado. Lo cazó la revisión de
fotogramas, no el código.

**La pista para volver a pegarlas:** el token que **abre** palabra trae un
espacio delante en el campo `text`; el que **continúa** no lo trae. Si se hace
`.strip()` al leer, esa información se pierde para siempre.

```python
abre = bruto.startswith(" ")      # antes de cualquier strip()
if abre: nueva_palabra(txt)
else:    pegar_al_anterior(txt)
```

Resultado: de 102 grupos rotos a 80 bien formados.

> **No se hace `strip()` antes de decidir si el token abre palabra.**

---

## 2. Las grabaciones de pantalla de macOS son de tasa variable

```
r_frame_rate   = 60/1          <- lo que dice
avg_frame_rate = 32496/701     <- 46,36 fps, lo que es
```

`setpts=N/FRAME_RATE/TB` toma el 60 declarado, no el 46,36 real, y escribe
marcas de tiempo imposibles. El codificador falla con `-22 Invalid argument` y
`Nothing was written into output file`, que no dice nada del problema real.

> **Se normaliza a CFR antes de cualquier `select` o `setpts`:**
> `fps=30` primero en la cadena, y después `setpts=N/30/TB`.

---

## 3. `overlay` explota si las entradas traen bases de tiempo distintas

Una pista hecha con el demuxer `concat` no comparte base de tiempo con el
material. `overlay` falla con el mismo `-22` inútil.

> **Las dos entradas se igualan antes de componer:**
> ```
> [0:v]...,settb=AVTB,setpts=PTS-STARTPTS[v];
> [1:v]fps=30,format=rgba,settb=AVTB,setpts=PTS-STARTPTS[ov];
> [v][ov]overlay=...
> ```

---

## 4. El nombre de los archivos de macOS trae un espacio que no es un espacio

`Screen Recording 2026-10-22 at 2.39.54 PM.mov` lleva **U+202F** (espacio
estrecho sin salto) antes de `PM`, no un espacio normal:

```
...322e33392e3534 e280af 504d2e6d6f76
                  ^^^^^^ U+202F
```

Escribir el nombre a mano da `No such file or directory` aunque `find` lo
liste. Rompe scripts, rutas y llamadas a herramientas.

> **Se copia el material a un nombre limpio antes de trabajar**, o se accede
> siempre por glob, nunca escribiendo el nombre.

---

## 5. El ffmpeg de Homebrew no trae `drawtext` ni `subtitles`

Este Mac tiene ffmpeg 8.1 con 481 filtros, pero **sin libass y sin
libfreetype**. No hay forma de quemar texto directamente.

| Filtro | Está |
|---|---|
| `overlay`, `drawbox`, `scale`, `pad`, `select` | sí |
| `drawtext`, `subtitles` | **no** |

> **Los subtítulos se dibujan aparte** (PIL, HyperFrames o canvas) y se
> componen con `overlay`. Que además es mejor: así llevan la tipografía y los
> colores de la marca de verdad, no los que acepte libass.

---

## 6. `loudnorm` dentro de un `filter_complex` grande falla

Combinado con `aselect` de expresión larga, el codificador AAC muere con `-22`.
Por separado funciona perfecto.

> **El audio se procesa en su propio paso** y se multiplexa al final.

---

## 7. PIL no vive en el Python aislado

`python3 -I` ignora los site-packages del usuario, que es donde está Pillow.
Para scripts propios que dibujan, se corre sin `-I`.

---

## 8. El umbral de silencio no se adivina, se mide

`silencedetect=noise=-34dB:d=0.35` encontró **cero** silencios en material que
sí los tiene, porque la grabación de pantalla captura el sistema y el piso de
ruido queda alto.

Lo que hay que hacer es medir la distribución primero:

| percentil | dB |
|---|---|
| 1 | −39,8 |
| 20 | −33,7 |
| 50 | −27,6 |
| 90 | −19,1 |

Y sacar el umbral de ahí. En este material, −33 dB con mínimo 0,30 s.

> **Un umbral en dB copiado de un tutorial es una adivinanza.** El mismo número
> que funciona en una grabación a cámara da cero en una captura de pantalla.

---

## 9. Animar el `.clip` pelea con HyperFrames

En una composición de HyperFrames, el div con `class="clip"` lo controla el
motor: él decide cuándo se ve y cuándo no. Si además se le anima la opacidad
desde GSAP, el subtítulo **se queda pegado en pantalla después de su tiempo**.

Pasó de verdad: "vidrio, cuero," seguía puesto a los 16,0 s cuando su bloque
terminaba a los 15,02 s. El `lint` lo avisó como `overlapping_gsap_tweens` sobre
`__unresolved__` y no le hice caso.

```html
<div id="s8" class="clip marco">        <!-- esto lo maneja HyperFrames -->
  <div class="sub" id="t8">vidrio, cuero,</div>   <!-- esto se anima -->
</div>
```

> **La animación va en el div de adentro, siempre.**
> Y cuando el `lint` dice `__unresolved__`, es que no pudo resolver el objetivo:
> mirar qué se está animando antes de renderizar 107 segundos.

---

## 10. `-t` no garantiza fotogramas: `-frames:v` sí

Pedir `-t 2.11` a 30 fps deja 64 fotogramas donde la cuenta son 63. Por sí solo
no importa; sumado en diez tramos, la imagen termina **5 fotogramas detrás de la
voz**, y los subtítulos, que sí están puestos en segundos exactos, se desfasan.

Se redondea la línea de tiempo **una sola vez**, entera, y cada tramo se corta
al número que le toca:

```bash
CORTES=(0 4.12 7.49 9.60 ... 31.50)
MARCAS=(); for c in "${CORTES[@]}"; do MARCAS+=( "$(python3 -c "print(round($c*30))")" ); done
N=$(( MARCAS[i+1] - MARCAS[i] ))
ffmpeg ... -t "$(python3 -c "print($d+0.3)")" ... -frames:v "$N" ...
```

Se pide un poco de más con `-t` y se recorta exacto con `-frames:v`.

---

## 11. whisper alucina sobre audio sin voz

El audio de la máquina, sin una sola palabra, devolvió:

```
[00:00:00.000 --> 00:00:29.980]   ¡Suscríbete al canal!
[00:00:30.000 --> 00:00:31.380]   Gracias por ver el video.
```

Se entrenó con subtítulos de YouTube y, cuando no hay nada que transcribir,
rellena con lo que más vio. **Un bloque de 30 segundos de corrido es la señal**:
el habla real se parte en segmentos cortos.

> Para preguntar "¿hay voces aquí?", lo que cuenta no es que devuelva texto,
> sino que devuelva texto **segmentado como habla**.

---

## 12. El `python3` de Homebrew no trae numpy

`which python3` → `/opt/homebrew/bin/python3` (3.15), sin numpy.
`/usr/bin/python3` (el del sistema) sí lo trae (2.0.2).

Los scripts que miden audio llevan `/usr/bin/python3` explícito en el shebang.
Un `brew upgrade` puede cambiar esto en mitad de una sesión: a mí se me cayó
entre un script y el siguiente.
