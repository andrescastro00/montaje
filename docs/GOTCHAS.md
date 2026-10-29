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

---

## 13. El RT60 no se mide con una recta sobre la envolvente

Medí el eco de un cuarto normal y me dio **1,5 s**, que es una iglesia. Lo
volví a medir con otra ventana y me dio 0,76. Con otra, 0,92. Ninguna servía
para decidir nada.

La causa, mirando la caída de verdad (dB respecto a la palabra que acaba):

```
ms tras la palabra    0    40    80   120   160   200   240   280
dB                  -13   -19   -26   -32   -36   -37   -32   -30
                                               ^ aquí ya es el piso de ruido
```

A los ~180 ms la curva **toca el piso de ruido y se aplana**. Un tramo plano
ajustado a una recta extrapola a un RT60 enorme, y cuanto más larga la ventana,
más absurdo el número.

**Lo que sí funciona:** promediar la caída de todas las pausas reales, tirar la
parte que ya está a menos de 8 dB del piso, ajustar entre −10 y −30 dB (T20) y
extrapolar por tres. En esa toma: **0,37 s**, que es un cuarto sin tratar, y
coincide con lo que se ve en la tabla.

Y la regla de arriba: **cuando una medida sale distinta cada vez que se cambia
la ventana, no se usa para decidir. Se imprime la curva cruda y se mira.** Me
costó tres barridos de parámetros guiados por un número que no significaba nada.

---

## 14. No se "corrige" la banda que uno mismo vació

El corrector de tono pedía **+10 dB en 80 Hz**. Normal: el paso anterior era un
`highpass=f=85`, así que esa banda medía −217 dB. El corrector veía un hueco
enorme y quería rellenarlo, o sea devolver el retumbe que se acababa de quitar.

Dos topes, los dos por el mismo motivo:

- **Por debajo del filtro de graves, corrección = 0.** El hueco está ahí a
  propósito.
- **Por encima de 12,5 kHz, solo cortar, nunca realzar.** Un AAC de 64 kbps
  (lo que graba Notas de Voz) no guardó nada allá arriba: realzar sube el ruido
  del propio codec. En esa toma, 16 kHz estaba a −48 dB y el corrector pedía
  +3,3.

> Si una banda está vacía, primero hay que preguntarse si la vació uno mismo.

---

## 15. No se instalan modelos en el python del sistema

`pip install deepfilternet` en `/usr/bin/python3` **degradó numpy de 2.0.2 a
1.26.4** (el paquete exige `numpy<2`) y de paso rompió `opencv-python-headless`,
que pide `numpy>=2`. Y después no sirvió: necesita `torchaudio`, que no estaba.

`/usr/bin/python3` es el único que tiene numpy y scipy (GOTCHAS 12), o sea que
es el que usa todo lo que mide audio aquí. Degradarlo rompe cosas que no tienen
nada que ver con lo que se estaba haciendo.

**Regla:** un modelo va en su propio entorno o no va. Y antes de instalar algo
que arrastre numpy, torch o scipy, se mira qué versión pide. Si pide un pin
viejo, se descarta.

Lo que sí se puede instalar sin romper nada, y es lo que resolvió el problema:
`nara_wpe` (puro numpy/scipy, desreverberación WPE).

---

## 16. `loudnorm` en una pasada se come la ecualización

Se calculó una corrección de tono medida, se aplicó, y el error contra la
curva de locución quedó en **0,9 dB**. Al final de la cadena, **2,4 dB**.
Nadie había tocado el EQ.

Era `loudnorm`. En una sola pasada no es una ganancia: va comprimiendo
mientras avanza, y eso cambia el balance espectral. Medido por etapas:

```
EQ aplicado                      0,9 dB
+ de-esser i=0.45                2,1 dB   <- se come 1,2
+ compresor                      1,8 dB
+ loudnorm una pasada            2,4 dB   <- se come 1,5
```

**Dos pasadas:** medir con `print_format=json`, y aplicar con `linear=true` y
los `measured_*`. Así es una ganancia pareja y no toca el espectro.

Y el de-esser: en 0,45 estaba deshaciendo el realce de presencia que se acababa
de calcular. Bajó a 0,20, donde no cuesta nada medible.

---

## 17. Comparar dos transcripciones con `zip` miente

El verificador del modelo generativo dijo **7 de 88 palabras iguales, 8 %**, y
pintaba que el modelo había destrozado la locución. Las dos transcripciones
eran idénticas salvo **una palabra insertada**: "grabado láser" contra
"grabado a láser".

Comparar por posición desalinea todo lo que viene después de la primera
inserción. Con `difflib.SequenceMatcher`: **87 de 88, 99 %**, y la salida dice
exactamente cuál fue el cambio.

> Un verificador que da falsos positivos se desactiva solo: a la tercera, nadie
> lo lee. Vale más que diga QUÉ cambió que cuánto.

---

## 18. Un script llamado `re.py` tapa el módulo `re` de Python

Se guardó un script de prueba como `re.py` en la carpeta de trabajo. El
siguiente `python3` corrido ahí reventó dentro de `numpy`, con un error que no
nombra el archivo:

```
AttributeError: partially initialized module 're' has no attribute 'compile'
(most likely due to a circular import)
```

Python busca primero en el directorio actual. Aplica igual a `json.py`,
`io.py`, `types.py`, `select.py`, `copy.py`. Los scripts de trabajo llevan
nombre largo (`resemble_correr.py`), nunca el de un módulo de la biblioteca.

---

## 19. SRMR no sirve para comparar antes y después de ecualizar

SRMR mide reverberación dividiendo la energía de modulación lenta (el habla)
por la rápida (lo que agrega el cuarto). Realzar la presencia en 2-5 kHz sube
las **consonantes**, que son modulación rápida, así que el número baja aunque
no haya más eco. Midió −2,4 dB por una ecualización que mejoró la grabación.

Sirve para comparar versiones **con el mismo balance espectral** (por ejemplo,
siete desreverberadores sobre el mismo archivo, que fue para lo que se usó).
Para comparar a través de un EQ hay que usar el RT60.

> Toda métrica tiene una variable que la confunde. Antes de decidir con un
> número, hay que preguntarse qué más lo mueve.
