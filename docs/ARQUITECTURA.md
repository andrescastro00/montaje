# Arquitectura

> Qué hace cada pieza, por qué está, y las tres decisiones que casi todo el mundo
> toma mal. Si solo vas a leer una sección, lee **§2 Cómo ve el agente** y
> **§5 Las tres trampas**.

---

## 1. El problema real

Un agente de lenguaje no puede ver ni oír un video. Esa es toda la dificultad.
Todo lo demás (cortar, animar, colorear, mezclar) son herramientas que existen
hace veinte años y funcionan bien.

Entonces el trabajo de verdad es: **convertir un video en algo que un agente
pueda leer, decidir sobre eso, y después verificar que lo que salió es lo que
quería.**

Las tres etapas son leer, decidir y verificar. No "editar".

---

## 2. Cómo ve el agente (la decisión más importante)

Hay tres formas y dos son malas.

| Vía | Costo | Problema |
|---|---|---|
| Volcar fotogramas al modelo | ~45 M de tokens por video | Inviable y además no sirve: ver 10.000 imágenes sueltas no es ver una película |
| Solo el texto transcrito | ~12 KB | Barato, pero el agente queda ciego: no sabe si hay un salto de imagen, si se le ve la cara tapada, si el corte quedó feo |
| **Texto siempre + una imagen compuesta bajo demanda** | ~12 KB + unas pocas imágenes | **Esta.** |

La tercera es la que usa `browser-use/video-use` (MIT, 30k estrellas) y es
claramente correcta:

- **Capa de lectura permanente:** todas las tomas empacadas en UN archivo de
  texto (~12 KB) con cada palabra y su milisegundo, más quién habla.
- **Capa visual bajo demanda:** una función `vista_linea(desde, hasta)` que
  devuelve **un PNG** que junta tres cosas en una sola imagen: tira de
  fotogramas + forma de onda + las palabras alineadas debajo.

El agente mira esa imagen **solo en los puntos de decisión**: una pausa
ambigua, dos tomas que compiten, un corte que hay que confirmar. No mira el
video entero. Mira donde tiene que decidir, igual que un editor humano hace
scrub en la zona dudosa.

**Esta es la pieza que no teníamos y es la que separa un editor de un
generador de cortes a ciegas.**

---

## 3. El documento único

Todas las herramientas escriben sobre el mismo papel, indexado por **segundo
del clip original**. El segundo es la llave que une todo. Ninguna herramienta
sabe que las otras existen; son procesos que reciben una ruta y devuelven JSON.

```
material/
   ├─ ffprobe          → fps, resolución, canales, duración REAL
   ├─ transcripción    → cada palabra con su milisegundo + quién habla
   ├─ VAD              → dónde hay voz y dónde no
   ├─ escenas          → dónde cambia el plano
   ├─ caras            → dónde está la cara en cada momento
   └─ separación       → voz por un lado, ruido por otro
                ↓
          montaje.json          ← UN archivo. Todo en segundos.
                ↓
        [ el criterio decide ]  ← docs/REGLAS.md
                ↓
             EDL (la lista de cortes)
                ↓
    ffmpeg corta · HyperFrames dibuja · se mezcla el sonido
                ↓
        AUTOREVISIÓN  ← vuelve a §2, mira cada corte
                ↓
   MP4  ·  o OTIO/FCPXML para Premiere, Resolve, Final Cut
                ·  o capas MOV con alfa para CapCut
```

**Beneficio de licencia:** las herramientas se invocan por línea de comandos,
nunca se mezcla su código con el nuestro. No hay obra derivada. El repo no
hereda MIT, ni BSD, ni Apache, ni CC-BY. Son programas que esto *invoca*, no
código que esto *contiene*. Por eso se pueden juntar doce proyectos de cinco
licencias distintas sin un solo problema.

---

## 4. Los siete oficios

Un video lo hace un equipo. Cada oficio es una pieza distinta y se contrata
aparte. Tratar de que una sola cosa haga todo es el error de origen.

| Oficio | Qué hace | Con qué |
|---|---|---|
| **Director** | Decide. Es el único que no se automatiza del todo | El criterio + Santiago |
| **Transcriptor** | Oye y escribe con milisegundos | Whisper / Parakeet |
| **Montajista** | Corta, quita silencios y repeticiones | ffmpeg, auto-editor |
| **Animador** | Títulos, gráficos, subtítulos | HyperFrames |
| **Investigador** | Busca la prueba real de lo que se afirma | Chrome |
| **Sonidista** | Música, efectos, mezcla, sonoridad | media-use + síntesis |
| **Finalizador** | Revisa antes de que nadie vea | ffmpeg + §2 |

El **investigador** es el que casi nadie tiene y el que más cambia el
resultado: cuando el guion dice "OpenAI anunció X", sale el anuncio **real**,
capturado del sitio real, no una recreación. Eso no es B-roll decorativo, es
prueba. Y es gratis: es un navegador.

---

## 5. Las tres trampas

Medidas, no opinadas. Las tres vienen de fallas documentadas.

### 5.1 El modelo miente con los números

Caso medido: se le pidió un corte de **300 s**. Entregó **578,24 s** mientras
reportaba **299,32 s**. No mintió a propósito: sumó mal y creyó su suma.

> **Regla: ninguna duración, ningún conteo y ninguna suma se reporta sin
> medirla con `ffprobe` sobre el archivo final.** Lo que diga el agente sobre
> cuánto dura algo no es un dato, es una hipótesis.

### 5.2 Los tiempos de palabra no son tiempos de corte

El borde de una palabra en una transcripción tiene ~120 ms de error. A 30 fps
son **cuatro fotogramas**. Cortar ahí produce cortes que se comen la primera
sílaba o dejan un pedazo de la siguiente.

Caso medido: 11 de 11 cortes cayeron a mitad de frase. Video inservible.

> **Regla: se corta en frontera de frase, no de palabra, y con colchón.**
> El silencio se respeta cuando es pausa dramática y se quita cuando es error.
> Distinguirlos es criterio, no umbral de decibeles.

### 5.3 El paralelismo multiplica los errores, no los arregla

Aquí mis fuentes se contradicen y hay que resolverlo.

- Un editor con 15 años de oficio dice: *un subagente por sección*.
- Una medición dice: con 6 cortes, en paralelo tarda **28,6 s** contra
  **19,4 s** en serie. Más lento. Y los 6 cortes siguieron mal en ambos modos.

No se contradicen: **hablan de cosas distintas.**

> **Regla: el paralelismo es para RENDERIZAR, nunca para DECIDIR.**
> Renderizar es trabajo de CPU, verificable y sin criterio: paralelo, y con
> **tope de 4 a la vez** (nueve a la vez tumbaron una máquina y los trabajos
> se cancelaron entre sí). Decidir es criterio: en serie, con todo el contexto
> a la vista. Repartir las decisiones entre nueve copias no da nueve opiniones
> buenas, da nueve versiones del mismo error.

La fuente que midió esto vende la solución, así que su recomendación hay que
leerla con pinzas. Pero los números de falla son reproducibles y son contra
lo que hay que diseñar.

---

## 6. El orden que ahorra plata

De más barato a más caro de cambiar. Nunca se salta un escalón.

```
1. mapa de beats    cambiar una línea de texto      ~0
2. láminas fijas    cambiar un PNG                  segundos
3. borrador a 1/2   cambiar un MP4 chico            minutos
4. render final     cambiar todo                    horas
```

Cambiar un plan no cuesta nada. Cambiar un gráfico terminado cuesta mucho.
Por eso **el mapa de beats va antes que cualquier gráfico**: una lista de cada
idea del guion y qué se ve en pantalla mientras se dice.

Y durante las notas, **todo se renderiza a media resolución**. Calidad plena
solo cuando el corte ya está aprobado.

Corolario: **mostrar solo lo que cambió.** Volver a renderizar la pieza
completa para que se vea un ajuste de dos segundos es quemar tiempo y tokens.

---

## 7. Qué construimos nosotros

Casi todo ya está escrito. Lo nuestro son tres cosas:

1. **El esquema de `montaje.json`** — el papel donde todos escriben.
2. **`docs/REGLAS.md`** — el criterio. Esto no se copia de ningún repo: sale
   de las notas de Santiago y de Diego, una por una.
3. **El lazo de aprendizaje** — cada nota no arregla un video, **reescribe la
   regla que debió haberlo evitado**. Es lo único que hace que la pieza número
   veinte salga mejor que la número uno.

Lo demás es pegamento.
