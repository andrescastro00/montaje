# Montaje

**Un editor de video que es un agente, y trabaja en tu equipo.**

Clonas esta carpeta, abres ahí tu agente (Claude Code, Codex, Gemini CLI, Cursor), le pasas un
enlace de YouTube o un archivo, y edita. No hay que configurar nada: el repo trae las instrucciones
que el agente lee solo, el instalador que pone las herramientas, y el criterio que separa un video
que se ve profesional de uno que se ve hecho por una máquina.

El motor es [HyperFrames](https://www.npmjs.com/package/hyperframes) y software libre
(`ffmpeg`, `whisper.cpp`, `yt-dlp`). Esto es la capa que al motor le falta: **qué pieza es, para
quién, con qué ritmo, y cómo se comprueba que quedó bien.**

---

## Empezar

```bash
git clone https://github.com/andrescastro00/montaje.git
cd montaje
./instalar.sh
```

`instalar.sh` comprueba e instala lo que falte (`ffmpeg`, `node`, `yt-dlp`, `whisper.cpp` con su
modelo, Python con sus paquetes, `tesseract`, las nueve skills de HyperFrames) y termina con una
tabla de qué quedó listo y qué tienes que hacer tú. Es idempotente: se puede correr siempre.

Después abres tu agente en esa carpeta y le dices qué video quieres editar. Él ya sabe el resto:
lee `AGENTS.md` al entrar.

```
Tú:      edítame este reel → https://youtu.be/XXXXXXXXXXX
Agente:  (lo trae, lo mide, lo mira, escribe la ficha, propone el plan por tramos, edita, verifica)
```

Requiere macOS con [Homebrew](https://brew.sh). En Linux funciona instalando a mano las mismas
herramientas; en Windows, con WSL.

---

## Qué hace distinto

**1. Mira el video antes de opinar.** Un modelo de lenguaje no ve ni oye. La falla típica no es que
diga "no puedo ver": es que **describe el video sin haberlo mirado** y propone un plan precioso de
una pieza que no existe. Aquí un comando convierte cualquier video en cosas que un agente sí
consume: fotogramas numerados por segundo, una hoja de contacto con el video entero en una imagen,
la onda, los cortes medidos, las palabras con su milisegundo, y una página HTML para mirarlo en el
navegador o por computer use. Los cuatro caminos están en [`docs/VER-VIDEO.md`](docs/VER-VIDEO.md).

```bash
./helpers/mirar.sh https://www.instagram.com/reel/XXXXXXXX/ referencia
```

**2. Diagnostica qué pieza es, en vez de preguntar.** Un TikTok de 10 segundos, un YouTube de 14
minutos y el institucional de una fundación no son la misma pieza con distinta duración: son
gramáticas distintas. Cambian la relación de aspecto, dónde cae el gancho, los cortes por minuto,
las palabras por pantalla, el sonido, y hasta si cabe un chiste. El agente deduce todo eso de la
marca, el nicho, el objetivo y la red donde se publica, lo escribe en cinco líneas y sigue. Solo
pregunta cuando equivocarse sale caro. Diez arquetipos con números reales, en
[`skill/video-de-marca/referencias/diagnostico.md`](skill/video-de-marca/referencias/diagnostico.md).

**3. Mide, no estima.** Dónde está la cabeza en cada cuadro, qué tapa la interfaz de Instagram,
cuántos decibelios por debajo va la música, si el audio quedó sincronizado. Todo con números, antes
de diseñar y antes de entregar.

**4. Aprende tu gusto, y no se lo cuenta a nadie.** El oficio está en el repo y se comparte. El
gusto de cada quien (tu marca, qué apruebas, qué te molesta) vive en `mi/AGENTS.md`, que es local y
**nunca se sube**. Cada nota que le das reescribe una regla ahí. Por eso la pieza veinte sale mejor
que la uno, y por eso dos personas pueden usar el mismo repo sin pisarse.

---

## Por dónde se lee

| Archivo | Qué contesta |
|---|---|
| **`AGENTS.md`** = `CLAUDE.md` = `GEMINI.md` | Lo que el agente lee al entrar. El lazo de trabajo completo |
| **`docs/VER-VIDEO.md`** | Cómo mira un video un agente que no ve. Los cuatro caminos |
| **`docs/REGLAS.md`** | El criterio. Si solo vas a leer una cosa, esta |
| **`docs/ARQUITECTURA.md`** | Por qué está hecho así. Las tres trampas medidas |
| **`docs/GOTCHAS.md`** | Lo que rompe el proceso en silencio. Todo encontrado con material real |
| **`docs/HERRAMIENTAS.md`** | Qué se usa, con qué licencia, y qué reemplaza a lo de pago |
| **`docs/ENCARGO.md`** | Qué hacer cuando llega material y nadie dijo qué hacer |
| **`docs/REGISTRO-VISUAL.md`** | Cómo se decide cómo se tiene que ver algo, antes de dibujar |
| **`skill/video-de-marca/`** | El oficio empaquetado como skill. Se instala suelta, sin el repo |
| **`helpers/`** | Los comandos: traer, mirar, cortar por silencio, subtitular, limpiar voz, mezclar |
| **`piezas/regiavia-demo/`** | Una pieza terminada con su mapa de beats, para ver cómo se ve un plan |

---

## La skill, sin el repo

`skill/video-de-marca/` funciona sola. Si ya tienes tu flujo y solo quieres el criterio:

```bash
ln -s "$PWD/skill/video-de-marca" ~/.claude/skills/video-de-marca
```

Trae el diagnóstico de la pieza, cómo se mide un bruto antes de diseñar, los niveles de sonido que
funcionan, las seis comprobaciones antes de entregar y las trampas que rompen el proceso sin dar
error. Lo que **no** trae, a propósito, es el gusto de una persona concreta.

---

## Lo que esto no es

No es una copia de ningún producto. El motor es software libre con licencia permisiva, invocado por
línea de comandos, sin obra derivada (`docs/HERRAMIENTAS.md`). El criterio está escrito desde cero y
calibrado contra notas reales de ediciones que se rechazaron y se volvieron a hacer.

Tampoco es un botón mágico. Es un oficio escrito para que lo ejecute un agente, con las mediciones
que hacen falta para que no invente. Las primeras piezas se corrigen; eso es parte del diseño.

---

## Estado

Funciona y está en uso. Primera corrida extremo a extremo sobre material real: 116,6 s de grabación
con voz, transcritos en 11,4 s, 25 cortes, 10,28 s de aire muerto quitado, 80 grupos de subtítulo en
la marca. Veintiún gotchas documentados, todos encontrados editando de verdad.

La voz quedó resuelta: el eco de un cuarto pequeño son reflexiones tempranas y **solo lo quita un
modelo generativo**. Medido, de 1,27 s de RT60 a 0,14 s, con la transcripción intacta palabra por
palabra.

**Siguiente:** formalizar el esquema de `montaje.json` y mover el pipeline a scripts estables en
`helpers/`.

---

MIT. Úsalo, cámbialo, véndelo. Si encuentras una trampa nueva, un PR a `docs/GOTCHAS.md` le sirve a
todo el mundo.
