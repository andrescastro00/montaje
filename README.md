# Montaje

Sistema de edición de video con agentes, para RegiaVía.

De una carpeta con material en bruto a un video terminado: transcribir, cortar
silencios y repeticiones, animar, buscar la prueba real de lo que se afirma,
sonorizar, revisar y entregar. En español, con la marca de quien pide.

**Privado. Santiago y Diego.**

---

## Por dónde se empieza a leer

| Archivo | Qué contesta |
|---|---|
| **`docs/ARQUITECTURA.md`** | Cómo ve un video un agente que no puede ver. Las tres trampas medidas |
| **`docs/REGLAS.md`** | El criterio. Lo único que no se baja de ningún repo |
| **`docs/REGISTRO-VISUAL.md`** | Cómo se decide cómo se tiene que ver algo, antes de dibujar |
| **`docs/HERRAMIENTAS.md`** | Qué se usa, con qué licencia, y qué reemplaza a lo de pago |
| **`docs/ENCARGO.md`** | Qué hacer cuando llega material y nadie dijo qué hacer. Los tres cajones |
| **`docs/GOTCHAS.md`** | Lo que rompe el pipeline en silencio. Todo encontrado con material real |
| **`skill/video-de-marca/`** | La skill que instala cualquiera. El criterio, vuelto herramienta |

Si solo vas a leer una cosa: `REGLAS.md`. Lo demás es cómo se ejecutan esas
reglas. Si vas a recibir un encargo: `ENCARGO.md` primero.

---

## La idea en cinco líneas

1. Un agente de lenguaje no ve ni oye un video. Todo lo demás es fácil.
2. Se le da a leer **un archivo de texto** con cada palabra y su milisegundo.
3. Y en los puntos de decisión, **una imagen compuesta**: tira de fotogramas +
   forma de onda + palabras. Mira donde hay que decidir, no el video entero.
4. Decide en serie. Renderiza en paralelo, máximo cuatro.
5. Cada nota de Santiago o Diego **reescribe la regla que debió evitar el
   error**. Eso es lo que hace que la pieza veinte salga mejor que la uno.

---

## Lo que esto NO es

No es una copia de ningún producto de nadie. El motor es software libre con
licencia permisiva (`docs/HERRAMIENTAS.md`), invocado por línea de comandos, sin
obra derivada. El criterio está escrito desde cero y calibrado con notas reales.

---

## La skill

`skill/video-de-marca/` es este criterio empaquetado como skill de agente. Se instala en un Mac
con un enlace:

```bash
ln -s "$PWD/skill/video-de-marca" ~/.claude/skills/video-de-marca
```

Trae el oficio: cómo se diagnostica qué pieza es (red, objetivo, nicho, marca), cómo se mide un
bruto antes de diseñar, los niveles de sonido que funcionan, las seis comprobaciones antes de
entregar y las trampas que rompen el proceso en silencio.

Lo que **no** trae, a propósito, es el gusto de una persona concreta. Eso va en un `AGENTS.md`
local que cada quien llena con el suyo, a partir de `skill/video-de-marca/plantillas/AGENTS.md`.
No hay un `AGENTS.md` común y no se sube uno común aquí.

---

## Estado

Arrancando. Documentación de arquitectura y criterio escrita; falta el código.

Primera corrida extremo a extremo hecha sobre material real: 116,6 s de
grabación con voz, transcritos en 11,4 s, 25 cortes, 10,28 s de aire quitado,
80 grupos de subtítulo en la marca. Ocho gotchas documentados.

Voz resuelta: el eco de un cuarto chico es reflexiones tempranas y solo lo quita un modelo
generativo. Medido, 1,27 s de RT60 a 0,14 s, con la transcripción intacta.

**Siguiente:** formalizar el esquema de `montaje.json` y meter el pipeline en
scripts estables dentro de `helpers/`.
