# Sonido

El catálogo de música y efectos de HyperFrames entra con `npx hyperframes auth login`, que es
gratis: más de 10.000 pistas y efectos de sonido en el plan Free. Esa es la primera opción y
reemplaza a rebuscar en bancos con atribución. Fuera de ahí, Openverse (de la WordPress Foundation)
tiene material Creative Commons, pero **casi toda licencia CC exige atribución**, y en un video eso
significa un crédito en pantalla o en la descripción: hay que verificar la licencia de cada pieza.

---

## La regla de fondo

**Casi imperceptible, elegante y moderno.** Lo que suena a plantilla: el "tling", el ping de
notificación, el brillo de hada, el sonido de aprobación. Nada de eso.

Y una pieza de calma no se sonoriza con ruido filtrado haciendo de oleaje: suena a que alguien
sopla en el micrófono. Ahí se entrega en silencio o con un fondo generado de verdad.

**Ante la duda, mudo.** Un efecto que nadie pidió es un efecto que molesta. Si quien edita pone sus
propios efectos y subtítulos, el agente no pone ninguno.

---

## Niveles que funcionan

Picos, sobre una voz entre −14 y −19 LUFS. Son puntos de partida medidos, no leyes.

| Uso | Nivel |
|---|---|
| Clic suave de un cursor (pasa-altos 500, pasa-bajos 7000) | −21 dBFS, con ±2,5 aleatorio |
| Barrido entre escenas (pasa-altos 220, pasa-bajos 7500, con fundido) | −35 dBFS |
| Golpe grave bajo un título (seno que cae de 95 a 48 Hz) | −37 dBFS |
| Contador de una barra que sube (un tic cada vez que el número pasa un entero) | unos 13 LU bajo la voz |
| Pieza con muchos efectos: golpe / sello / barrido / pop / clic / teclas | −18 / −22 / −27 / −29 / −31 / −35 |

Dos detalles que se notan: el barrido tiene su energía máxima **a mitad del barrido**, no al
empezar, y el barrido solo va donde de verdad cambia algo grande. Un barrido en cada corte
convierte la pieza en una máquina tragamonedas.

---

## La voz no se toca

**Se mezcla aparte y se une copiando.** Mezclar los efectos en el mismo `filter_complex` que los
overlays cortó una pista de audio a las dos horas y media sin dar ningún error.

```
[0:a]aformat=sample_rates=44100:channel_layouts=stereo[voz];
[1:a]aformat=sample_rates=44100:channel_layouts=stereo[fx];
[voz][fx]amix=inputs=2:normalize=0:duration=first[out]
```

`normalize=0` es obligatorio: sin eso, `amix` baja la voz para hacerle sitio a los efectos.

Y después:

```bash
ffmpeg -i video-sin-audio.mp4 -i mezcla.m4a -map 0:v -map 1:a -c copy -movflags +faststart final.mp4
```

**El audio no va dentro del render del motor.** Renderizar con el códec de audio incorporado dejó
la voz 43 ms atrasada. Se renderiza mudo y el audio se pone con ffmpeg.

---

## Una voz opaca se arregla con ecualización, no con denoise

Para una voz que suena apagada y lejana (que es distinto de una voz con ruido):

- pasa-altos a 75 Hz
- −3 dB en 300 Hz, que es donde se embarra
- +2,5 dB en 3,2 kHz, que es la presencia
- realce de 1,5 dB desde 6,5 kHz
- compresor 2,5 a 1
- `loudnorm` **en dos pasadas** a −14 LUFS

**Sin denoise.** Un denoise sobre una voz que no tiene ruido solo mete artefactos.

Hay tres defectos distintos y cada uno tiene su herramienta: **ruido** (un piso constante, se quita
con un denoise), **eco** (la voz rebotando en el cuarto) y **tono** (el micrófono capturó un
balance malo, se arregla con ecualización medida). Un denoise solo toca el primero.

**El eco de un cuarto chico no se resta, se regenera.** Son reflexiones tempranas, a 3 y 5
milisegundos, que se suman al sonido directo: no hay una cola que quitar. Los modelos de de-reverb
entrenados con voces de música no quitan nada ahí. Lo que funciona es un modelo generativo que
resintetiza la voz, con su temperatura en cero para que no invente palabras, y verificando después
que la transcripción de la salida sea igual a la de la toma cruda.

Y el arreglo gratis que le gana a cualquier modelo: **grabar más cerca**. Pasar de 40 a 10 cm sube
la relación voz contra cuarto unos 12 dB.

---

## Dos trampas de normalización

- **`loudnorm` de una sola pasada aplana los contrastes.** Si la pieza va de una oficina ruidosa a
  una calma, una pasada se lleva justo el contraste que se buscaba. En piezas de contraste se mide
  el LUFS y se aplica una ganancia fija. Y una pasada también se come la ecualización que se acaba
  de aplicar: va en dos pasadas con los valores medidos.
- **El limitador sube el nivel solo.** Para limitar sin subir, hay que desactivar su ganancia
  automática.

---

## ElevenLabs, plan gratis

- **Sí deja**: voces premade con etiquetas, y la generación de efectos y fondos.
- **No deja**: voces de biblioteca por API (devuelve 402), diseño de voz (403), música (402).
- **No se gastan los créditos de nadie sin preguntar.**
