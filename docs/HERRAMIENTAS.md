# Herramientas

Licencias verificadas contra la **API de GitHub**, no contra blogs. Los blogs
se contradicen entre sí en casi todas (sobre todo en auto-editor y whisperX).
Fecha de verificación: **28 de octubre de 2026**.

## Motor (todo permisivo, cero GPL/AGPL)

| Proyecto | Licencia | ⭐ | Para qué |
|---|---|---|---|
| `openai/whisper` | MIT | 111k | Transcripción, multilingüe |
| `ggml-org/whisper.cpp` | MIT | 55k | Lo mismo, rápido en chip Apple |
| `google-ai-edge/mediapipe` | Apache-2.0 | 37k | Caras, encuadre, reframe |
| `browser-use/video-use` | **MIT** | **30k** | **El más cercano a lo que queremos. Ver abajo** |
| `SYSTRAN/faster-whisper` | MIT | 26k | Transcripción con VAD integrado |
| `m-bain/whisperX` | BSD-2 | 25k | Palabra por palabra + quién habla |
| `Zulko/moviepy` | MIT | 15k | Montaje por código |
| `pyannote/pyannote-audio` | MIT | 11k | Quién habla |
| `snakers4/silero-vad` | MIT | 11k | Voz contra silencio |
| `WyattBlue/auto-editor` | Unlicense | 5,6k | Cortar silencios |
| `Breakthrough/PySceneDetect` | BSD-3 | 5,3k | Cambios de plano |
| `adefossez/demucs` | MIT | 3,5k | Separar voz de ruido |
| `AcademySoftwareFoundation/OpenTimelineIO` | Apache-2.0 | 2k | Entregar a Premiere/Resolve/FCP |
| `haidrrrry/claude-remotion-skill` | MIT | 694 | Skill de referencia (Remotion) |

**Ninguna de estas obliga a nada**, porque se invocan por línea de comandos.
No hay obra derivada. Ver `ARQUITECTURA.md` §3.

---

## `browser-use/video-use` — lo más parecido que existe

MIT, 30k estrellas, movido hace semanas. **Hay que leerlo antes de escribir una
línea nuestra.** Lo que ya resolvió:

- Empaca todas las tomas en **un archivo de ~12 KB** que es la vista principal
  del agente.
- `timeline_view`: PNG bajo demanda con **tira de fotogramas + onda + palabras**.
  Es la respuesta a "cómo ve el agente". Lo compara contra volcar fotogramas:
  ~45 M de tokens contra ~12 KB más unas imágenes.
- Lazo de autorrevisión en cada frontera de corte, **tope 3 intentos**.
- Un subagente por animación.
- Quita muletillas y aire muerto, colorea, funde 30 ms en los cortes, quema
  subtítulos, guarda notas de sesión en `project.md`.

**Diferencia con lo nuestro:** transcribe con **ElevenLabs Scribe**, que es de
pago y por API. Nosotros lo cambiamos por Whisper o Parakeet local. Y su
registro es gringo; el nuestro es RegiaVía en español.

---

## Transcripción: Whisper o Parakeet

| | Whisper | Parakeet (NVIDIA) |
|---|---|---|
| Licencia | **MIT** | **CC-BY-4.0** (revisar antes de uso comercial) |
| Velocidad | base | ~40-50× más rápido en throughput |
| Idiomas | multilingüe | **fuerte en inglés** |
| Mac Intel | sí | **no** |
| Palabra por palabra | sí | sí |

**Para nosotros gana Whisper**, y no por poco: trabajamos **en español**, y
Parakeet está optimizado para inglés. Los videos gringos recomiendan Parakeet
porque graban en inglés. Es la clase de consejo que no se copia sin pensar.

Parakeet entra solo si algún día se edita material en inglés.

---

## Tres carriles para dibujar, no uno

No todo gráfico necesita un framework. Se escoge por pieza:

| Carril | Cuándo | Costo |
|---|---|---|
| **HyperFrames** | Lo ya montado en `~/Proyectos/video-studio`, con 13 skills y bloques listos. **El default.** | gratis |
| **Canvas en JavaScript puro** | Piezas de estilo muy propio, donde el framework estorba más de lo que ayuda. Claude escribe JS que dibuja cada fotograma. Sin instalar nada. | gratis |
| **Remotion** | Muchas versiones por dato, control al fotograma, o el video va dentro de una app React | gratis |

El carril de **canvas puro** es el que no teníamos. Vale justamente porque el
ejemplar en código es el formato de referencia (ver `REGLAS.md` 0.4): un archivo
JS autocontenido es la unidad más fácil de guardar, versionar y modificar.

---

## De pago, opcional, y qué reemplaza a cada uno

Ninguno es necesario para arrancar.

| Herramienta | Para qué | Costo | Alternativa gratis |
|---|---|---|---|
| **Higgsfield** (MCP oficial, `mcp.higgsfield.ai`) | Generar imagen y video con 30+ modelos (Veo, Sora, Kling) | créditos | No hay equivalente real |
| **ElevenLabs** (vía Composio) | Voz | plan pagado para voces en español | Sin voz, escrito para leerse en mudo |
| **Epidemic Sound** | Música y efectos con licencia | ~10 USD/mes | Openverse (CC) + los 21 efectos de `media-use` + síntesis |
| **Tella** (MCP) | Grabar cara y pantalla a la vez | ~13 USD/mes | Grabación normal + edición |
| **ElevenLabs Scribe** | Transcripción (lo que usa `video-use`) | por API | Whisper local, gratis |

**Ojo con ElevenLabs:** comprobado que el plan gratis devuelve
`402 paid_plan_required` para las voces en español. Las gratis son premade en
inglés y hablan español con acento gringo. En una pieza de una agencia
colombiana eso es peor que el silencio.

**Salida por probar para la voz en español: Gemini Flash TTS**, desde Google AI
Studio. Tiene catálogo de voces, control de estilo y etiquetas de respiración y
risa dentro del guion. Es la alternativa más clara al muro de pago de
ElevenLabs. **Falta probar cómo suena en español colombiano** antes de
adoptarla.

---

## Referencias

- `prompt-motion.com` (con guion, no `promptmotion.com`): galería de motion
  graphics hechos con Claude, **cada uno con el prompt exacto**. ~83 piezas.
  Sirve de banco de arranque, no de estilo: el estilo sale de la marca.
- La crítica de `cutback.video` sobre lo que se rompe. **Es el blog de Selects,
  que vende la solución**, así que su recomendación tira para su lado. Pero sus
  mediciones de falla son reales y están recogidas en `ARQUITECTURA.md` §5.

---

## Lo que NO vamos a usar

**Un producto de pago que nos recomendaron.** Es comercial, con licencia personal a
nombre de un tercero que prohíbe compartirlo, sublicenciarlo, incluirlo en un
producto propio y quitarle los avisos de autoría. No entra aquí, ni entero ni
en partes, ni con los créditos cambiados.

No hace falta: usa Whisper y ffmpeg igual que nosotros. Lo que vendía era el
criterio, y el criterio está en `REGLAS.md`, escrito desde cero y calibrado
con las notas de Santiago.
