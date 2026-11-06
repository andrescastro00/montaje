<!--
  PLANTILLA. Esto no es un archivo que se usa tal cual: es un molde que cada persona llena.

  POR QUÉ EXISTE
  La skill trae el oficio: cómo se diagnostica una pieza, cómo se mide un bruto, qué niveles de
  sonido funcionan, cómo se verifica. Lo que la skill NO puede traer es el gusto de la persona
  concreta con la que se trabaja, ni las rutas de su disco, ni qué le gustó y qué le pareció feo.
  Eso cambia por persona, por marca y por mes. Va aquí.

  CÓMO SE USA
  1. Trabajando desde el repo `montaje`, va en `mi/AGENTS.md`, y `./instalar.sh` ya lo copió ahí.
     Trabajando sin el repo, se copia a la raíz de la carpeta de trabajo con el nombre AGENTS.md
     (y duplicado idéntico como CLAUDE.md y GEMINI.md si se usa más de un agente; idénticos de
     verdad, se comprueba con `md5 -q AGENTS.md CLAUDE.md GEMINI.md`).
  2. Se llena con lo de cada quien. Lo que no aplique se borra, no se deja en blanco.
  3. No hay que llenarlo de una sentada, y NADIE debe ser interrogado para llenarlo: el agente lo
     va llenando con cada nota que recibe.
  4. Cada vez que llega una nota sobre una entrega, se escribe aquí la REGLA que habría evitado el
     error, no la anécdota. Eso es lo que hace que la pieza veinte salga mejor que la uno.

  ESTE ARCHIVO ES DE CADA QUIEN y NO SE SUBE. `mi/` está en el .gitignore del repo. No hay un
  AGENTS.md común: dos personas que trabajen con editores distintos tienen archivos distintos, y
  está bien. El oficio se comparte, el gusto no.

  Borrar este comentario al llenarlo.
-->

# Cerebro de motion · <MARCA>

> Lo que se aprendió editando con <QUIÉN>, desde <FECHA>. Su gusto, el flujo que funciona y las
> trampas que ya costaron horas.
>
> **Para el agente que lee esto:**
> 1. Léelo completo antes de tocar un video.
> 2. Las reglas de la sección 2 no se discuten: salen de rechazos reales.
> 3. Las recetas apuntan a proyectos que ya existen. Se copia de ahí, no se empieza de cero.
> 4. El oficio general está en la skill `video-de-marca`. Esto es solo lo que es de esta marca y
>    de esta persona.

---

## 1. Contexto en treinta segundos

- **<MARCA>** hace <qué> para <quién>.
- **<QUIÉN PIDE>** es quien pide el motion y quien aprueba. <Cómo manda los pedidos: por voz, por
  escrito, con transcripciones que llegan con errores. Si llegan transcritas, interpretar la
  intención y no la letra.>
- **Quién sale en cámara:** <nombres y qué rol tiene cada uno>.
- **Cuentas oficiales:** <red: @cuenta>. <Ojo con las cuentas homónimas, si las hay.>

**Paleta**

| Color | Hex |
|---|---|
| <nombre> | `#______` |

**Tipografía**

- Títulos: <familia y peso>
- Interfaz y texto: <familia>
- <Dónde están embebidas, para no volver a buscarlas.>

**Personaje o mascota de marca:** <cuál es exactamente, y cuál NO es>.

---

## 2. El gusto de <QUIÉN> (reglas duras)

Cada regla aquí salió de un rechazo concreto o de un "me encantó". Si una regla no tiene origen,
no es una regla: es una opinión mía y no va en esta sección.

### Lo que pide

1. <Regla.> <Origen: qué rechazó o qué aprobó.>
2.
3.

### Lo que no quiere

1. <Regla.> <Origen.>
2.

### Formato por formato

- **Vertical (reels, TikTok):** <zonas, duración, si lleva subtítulos>
- **Horizontal (YouTube, web):** <estilo, cada cuántas escenas cambia algo, transiciones>
- **<otro formato>:**

### Sonido

- <Qué le gusta y qué le pareció feo, con el nombre del efecto.>
- <Si pone sus propios efectos y subtítulos en edición, el agente no pone ninguno.>

### Forma de trabajar

- **Cuando dice "ya sabes qué hacer":** hacerlo. Sin preguntas.
- **Cuándo sí preguntar:** <los casos caros de esta relación>.
- **Entregas:** <nombre del archivo, dónde se deja, si se abre en el Finder, si se conserva la
  versión anterior>.
- **Nunca:** <lo que no se toca ni se borra nunca>.

---

## 3. Rutas

| Qué | Dónde |
|---|---|
| Material en bruto | |
| Proyectos de trabajo | |
| Copia o respaldo | |
| Entregables | |
| Modelos locales (transcripción, etc.) | |
| Librería de efectos | |

<Avisos del entorno: discos con formato que rompe cosas, carpetas con espacios al final del
nombre, rutas que no se pueden mover porque algo las busca ahí.>

---

## 4. Proyectos de referencia

De cuál se copia qué. Esta tabla vale más que cualquier explicación.

| Proyecto | Copiar de aquí |
|---|---|
| | |

---

## 5. Lo que no se puede afirmar en esta marca

<Cifras que hay que medir antes de ponerlas. Nombres que necesitan permiso. Afirmaciones
prohibidas. Qué se verifica y contra qué fuente.>

---

## 6. Registro de aprendizajes

Uno por línea, con fecha. Lo que se escribe es la regla, no la historia.

- **<AAAA-MM-DD>** <La regla.> <En una línea, por qué.>

---

*Última actualización: <AAAA-MM-DD>. Si se aprende algo nuevo, se agrega aquí y se replica en
CLAUDE.md y GEMINI.md, que deben quedar idénticos.*
