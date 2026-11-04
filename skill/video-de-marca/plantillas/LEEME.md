# Las plantillas

## `AGENTS.md`

El molde del criterio **local**. La skill trae el oficio; este archivo trae el gusto de la persona
concreta con la que se trabaja, sus rutas y sus rechazos.

Por qué separado y por qué local: el flujo que de verdad funciona es agéntico. El agente abre la
carpeta del trabajo, encuentra ahí un archivo que dice cómo trabaja ese editor, y ya no hay que
explicárselo cada vez. La skill no puede traer eso porque cambia por persona.

```bash
cp ~/.claude/skills/video-de-marca/plantillas/AGENTS.md <carpeta del trabajo>/AGENTS.md
# y si se usa más de un agente:
cd <carpeta del trabajo> && cp AGENTS.md CLAUDE.md && cp AGENTS.md GEMINI.md
md5 -q AGENTS.md CLAUDE.md GEMINI.md   # los tres iguales
```

**Es de cada quien.** No hay un `AGENTS.md` común y no se sube uno común a un repo compartido. Dos
personas con editores distintos tienen archivos distintos.

## Cómo se llena bien

La sección 2 es la que importa. Una regla solo entra ahí si tiene **origen**: un rechazo concreto
o un "me encantó". Una regla sin origen es una opinión del agente disfrazada de criterio, y esas
son las que llevan a rehacer piezas.

La forma que funciona para cada entrada:

```
N. <La regla, en imperativo.> <Qué pasó: qué se entregó y qué dijo.>
```

Y cuando llega una nota sobre una entrega, lo que se escribe no es la anécdota: es **la regla que
habría evitado el error**.
