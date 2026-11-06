# Cómo mira un video un agente que no ve

Un modelo de lenguaje **no ve ni oye un video**. Esa es la única dificultad real de editar con
agentes; todo lo demás es ffmpeg. Y la falla típica no es que el agente diga "no puedo ver": es que
**describe el video sin haberlo mirado**, con mucha seguridad, a partir del título y del nombre del
archivo. Sale un plan precioso de una pieza que no existe.

Se resuelve convirtiendo el video en cosas que un agente **sí** puede consumir. Con el repo
`montaje` es un comando; sin el repo, son los mismos `ffmpeg` y `whisper` escritos a mano
(`referencias/medir.md` los trae uno por uno):

```bash
./helpers/mirar.sh https://www.instagram.com/reel/XXXXXXXX/ referencia
```

Eso deja, en `trabajos/<fecha>-referencia/`:

| Qué | Dónde | Para qué |
|---|---|---|
| El video | `bruto/base.mp4` | reproducirlo, o mandarlo a un modelo que acepte video |
| La página | `vista/vista.html` | **mirarlo**: reproductor, rejilla de fotogramas, onda, palabras |
| Todo en una imagen | `vista/hoja-de-contacto.jpg` | el video entero de un vistazo, en **una** imagen |
| Fotograma por fotograma | `vista/fotogramas/s0007,50.jpg` | el segundo exacto, con el segundo en el nombre |
| Las palabras | `datos/palabras.txt` | qué se dice y en qué milisegundo |
| Los cortes | `datos/cortes.txt` | dónde cambia el plano, medido, y cuántos por minuto |
| La onda | `vista/onda.png` | dónde hay voz, dónde hay silencio, dónde pega la música |

---

## Los cuatro caminos, según lo que sepas hacer

Escoge **el primero que puedas**, de arriba hacia abajo. No hace falta preguntarle a nadie: pruébalo.

### 1. Si manejas un navegador

Claude in Chrome, Playwright, Puppeteer, Chrome headless, cualquiera.

```
abrir   file:///ruta/absoluta/trabajos/<fecha>-<pieza>/vista/vista.html
```

La página es autocontenida y funciona sin internet. Dentro: el reproductor con el video real, una
rejilla de fotogramas en la que **un clic lleva al segundo exacto**, la onda con su aguja, las
palabras resaltándose a medida que suenan, y en vertical un interruptor que **pinta encima las
zonas que tapa la interfaz de Reel y TikTok**. Es la forma más rica de mirar, porque puedes volver.

Dos cosas que hay que saber:

- Una extensión de navegador puede necesitar permiso para `file://`. Si no abre, copia la carpeta
  `vista/` a donde la extensión sí llegue, o sirve la carpeta: `python3 -m http.server 8731`
  y entra a `http://localhost:8731/vista/vista.html`. Lo segundo funciona siempre.
- Chrome headless en Mac **no baja de 500 px de ancho de ventana**: una captura pedida a 390 sale
  recortada y parece un desborde de CSS que no existe (gotcha conocido de Chrome en Mac).

Captura directa, sin extensión:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --window-size=1400,2200 --screenshot=/tmp/vista.png \
  "file://$PWD/trabajos/<fecha>-<pieza>/vista/vista.html"
```

### 2. Si manejas la pantalla (computer use)

```bash
open "trabajos/<fecha>-<pieza>/vista/vista.html"
```

Y de ahí capturas. Sirve también para mirar el video en QuickTime y moverse con las flechas, que es
lo más parecido a ver de verdad. Pero cuidado: en una terminal, computer use **no escribe bien**; lo
que se teclea en una ventana de terminal se pierde o se mezcla. Para la terminal usa el shell.

### 3. Si solo puedes leer archivos (es el caso más común)

Los fotogramas son `.jpg` normales y los lees como imágenes. **El orden importa, porque las imágenes
cuestan:**

1. **`vista/hoja-de-contacto.jpg` primero, siempre.** Es el video entero en una sola imagen, en
   rejilla, en orden. De ahí sale el ritmo, la paleta, dónde está la cara y cuántos planos hay.
2. Después, **entre cuatro y ocho fotogramas sueltos**, y solo de los puntos donde hay que decidir:
   el primer segundo, cada corte de `datos/cortes.txt` que importe, el cuadro donde entra el texto,
   el último. El nombre lleva el segundo: `s0007,50.jpg` es el segundo 7,50.
3. Lo que se dice está en texto (`datos/palabras.txt`): eso no gasta imágenes. Leelo completo.

**Lo que no se hace:** volcar los sesenta fotogramas al modelo, y menos todos los cuadros del video.
Está medido en la arquitectura del repo: un video entero cuadro por cuadro son unos 45 millones de
tokens, y además no sirve, porque ver diez mil imágenes sueltas no es ver una película.

### 4. Si tu modelo acepta video de verdad

Algunos sí: Gemini recibe un archivo de video por su File API y lo procesa entero. Si es tu caso,
manda `bruto/base.mp4` directo y pregúntale por segundos concretos. La mayoría **no** acepta video
(Claude y GPT reciben imágenes, no video), y ahí el camino es el 3. Si no estás seguro de lo que
acepta tu modelo, no lo adivines: usa el camino 3, que funciona en todos.

---

## Traer videos de internet

`yt-dlp` resuelve YouTube, TikTok, Instagram, X, Vimeo, Facebook y bastantes más. Ya lo instala
`./instalar.sh` y ya lo usa `traer.sh`, así que casi nunca hay que llamarlo a mano.

```bash
./helpers/traer.sh https://youtu.be/XXXXXXXXXXX clase-de-octubre
./helpers/traer.sh https://www.tiktok.com/@alguien/video/123456 referencia
```

Cuando falla, casi siempre es una de estas tres, y ninguna se arregla insistiendo:

| Falla | Qué es | Qué se hace |
|---|---|---|
| Pide sesión o sale 403 | el video es privado o la red bloquea | `yt-dlp --cookies-from-browser chrome <url>`, y si no, se pide el archivo |
| Baja un video de 10 s cuando el real dura 3 min | era una vista previa | se pide el enlace del original o el archivo |
| Un enlace de Drive o Dropbox | no es una página de video | se pide el enlace de descarga directa, o el archivo |

**Un archivo que manda la persona siempre es mejor que un enlace**: trae la resolución real, sin
recomprimir. Pedirlo no es pereza, es calidad. Y lo que llegue por WhatsApp viene recomprimido a
16 kHz mono si tiene voz: para locución no sirve, se pide por AirDrop o Drive.

**Lo ajeno es referencia, no material.** El reel de otra persona se mira para aprender su ritmo. No
se reusan sus planos, su música ni su locución en una pieza propia, ni se vuelve a publicar.

---

## Qué se saca de mirar

Mirar no es "ya lo vi, se ve bien". Mirar es salir con **números**, y esos números van a `PIEZA.md`
antes de abrir el motor. Si una referencia no se puede volver números, no se miró.

| Lo que se mide | Cómo se saca | Por qué importa |
|---|---|---|
| Cortes por minuto | `datos/cortes.txt`, ya contado | es el ritmo, y es lo que más delata una pieza fuera de tono |
| El segundo del gancho | el primer fotograma donde ya pasó algo | en vertical, si pasa después de 1,5 s, no hay pieza |
| Palabras por pantalla | se cuentan en los fotogramas | tres a seis en vertical; una frase en horizontal |
| De dónde entra el texto | dos fotogramas seguidos en un corte | la dirección y la curva son la mitad del registro |
| Dónde está la cara | la rejilla, mirando los bordes | en vertical, la cabeza a 30 px de cualquier borde, **en todos los cuadros** |
| Qué deja vacío | la hoja de contacto | el aire es decisión, no sobra |
| Música: qué tan fuerte | `vista/onda.png` contra las palabras | si tapa la voz se nota en la onda antes de oírlo |

Y lo que no se puede medir se dice que no se midió. Un plan honesto con tres huecos vale más que un
plan completo inventado.
