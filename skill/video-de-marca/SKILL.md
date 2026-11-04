---
name: video-de-marca
description: Capa de criterio y de marca para CUALQUIER video: lanzamientos, promos, demos, pauta, clases, reels, TikToks, institucionales, intros, logos animados. Se lee ANTES de hyperframes, no en su lugar. Resuelve lo que el motor no sabe. Primero DIAGNOSTICA qué pieza es (red social, objetivo, nicho, marca, material disponible) y de ahí salen la relación de aspecto, la duración, el ritmo, la densidad de texto, el sonido y las zonas prohibidas. Después pone la voz de la marca (Aztec, RegiaVía o cliente), lo que se puede afirmar y lo que no, si lleva locución, cómo se mide el material antes de diseñar, cómo se verifica antes de entregar, y dónde queda el archivo. Activar cuando se pida hacer, editar, mejorar, copiar o "hacer igualito" un video, un motion, un reel, un short, un corto de pauta, un hero de una web, una intro o una animación; cuando se comparta un guion, un bruto o una URL para volverla video; o cuando alguien diga "hazme un video de X". Si hay duda, activar.
---

# Video de marca

Esto NO es un motor de video. El motor es HyperFrames y ya está instalado. Esto es la capa fina
que el motor no puede traer: **qué pieza es**, con qué voz se escribe, qué se puede afirmar, cómo
se mide el material antes de diseñar, cómo se verifica antes de entregar y dónde queda el archivo.

El orden importa. Primero se decide **qué** se está haciendo. Después se abre el motor.

| Paso | Dónde está |
|---|---|
| 1. Diagnosticar la pieza y escribir su ficha | `referencias/diagnostico.md` |
| 2. Poner la voz de la marca | sección 2 de este archivo |
| 3. Medir el material antes de diseñar nada | `referencias/medir.md` |
| 4. Construir con el motor | `/hyperframes` y su tabla de tipos |
| 5. Sonorizar | `referencias/sonido.md` |
| 6. Verificar con números, no a ojo | `referencias/verificar.md` |
| 7. Entregar | sección 6 de este archivo |

Lo que rompe el proceso en silencio: `referencias/trampas.md`.
El criterio del editor con el que se trabaja: `plantillas/AGENTS.md`, que **cada persona llena con
el suyo**. No hay uno común y no se sube uno común.

---

## 0. Antes de nada: diagnosticar, no preguntar

Un TikTok de 10 segundos, un video de YouTube de 14 minutos y el institucional de una fundación
respetada **no son la misma pieza con distinta duración**. Son gramáticas distintas: cambian la
relación de aspecto, dónde cae el gancho, cuántos cortes por minuto, cuánto texto cabe en pantalla,
si hay voz, si hay música, si lleva subtítulos quemados y hasta si se puede hacer un chiste.

El agente **decide**. No llena a nadie de preguntas. Lee `referencias/diagnostico.md`, escribe la
ficha de la pieza en cinco líneas, la dice y sigue. Solo pregunta cuando dos lecturas producen
trabajo materialmente distinto y caro de rehacer: un tono nuevo, una voz que cuesta plata, un
reencuadre que obliga a volver a grabar.

La ficha, siempre, antes de abrir el motor:

```
Pieza:      <qué es>            Red:      <dónde se publica>
Formato:    <relación> <dur>    Gancho:   <segundo en que tiene que haber pasado algo>
Ritmo:      <cortes por minuto> Texto:    <palabras por pantalla>
Sonido:     <voz / música / mudo>         Subtítulos: <sí quemados / no, los pone el editor>
Registro:   <cómo habla esta marca>       Prohibido: <lo que esta marca no hace>
```

---

## 1. Qué skill hace esto (la tabla cambió en noviembre de 2026)

HyperFrames consolidó su catálogo. **Ya no hay trece skills de video.** Hay nueve, y el enrutador
es `/hyperframes`, que lee un archivo de tipo según lo que se pida.

| Lo que pide | A dónde ir |
|---|---|
| Cualquier video, sin saber cuál | `/hyperframes` (manda, y enruta solo) |
| Lanzamiento, promo, demo de producto | `/hyperframes` → `references/types/launch.md` |
| Explicador, tutorial, clase | `/hyperframes` → `references/types/explainer.md` |
| Reel, TikTok, Short, cualquier vertical | `/hyperframes` → `references/types/vertical.md` |
| Cifras, gráficos, dashboards animados | `/hyperframes` → `references/types/data.md` |
| Video con música de protagonista | `/hyperframes` → `references/types/music.md` |
| 3D, simulación, generativo | `/hyperframes` → `references/types/3d.md` |
| Personaje, mascota, corto con historia | `/hyperframes` → `references/types/character.md` |
| Mapa, lugar real, un sitio web vuelto video, un PR, tipografía cinética | `/hyperframes` → `references/film.md` |
| Subtítulos; tarjetas sobre alguien hablando | `/hyperframes` → `references/captions.md`, `overlays.md` |
| **Copiar un video que mandaron ("hazlo igualito")** | `/reverse-any-video` |
| **Un episodio en un estilo probado** | `/style-sampling` |
| Presentación para exponer | `/slideshow` |
| Traer algo hecho en Remotion | `/remotion-to-hyperframes` |
| Música, efectos, voz, imágenes, logos, recortes, color | `/media-use` |
| Diseño que viene de Figma | `/figma` |

Las nueve vivas: `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` (el juego
base) más `figma`, `slideshow`, `remotion-to-hyperframes`, `reverse-any-video` y `style-sampling`
(se instalan a pedido). Se comprueba con `npx hyperframes skills check` y se actualizan con
`npx hyperframes skills update`, que es un comando **de la persona**, no del agente.

### Skills huérfanas: no las uses

Si en el Mac todavía aparecen `general-video`, `motion-graphics`, `product-launch-video`,
`website-to-video`, `faceless-explainer`, `pr-to-video`, `talking-head-recut`, `music-to-video`,
`embedded-captions` o cualquier `hyperframes-animation / -audio / -core / -creative / -keyframes /
-media / -studio`, son **restos congelados**. HyperFrames las retiró y las fundió en `/hyperframes`.
`skills update` no las toca y `skills check` no las cuenta: se quedan ahí, viejas, compitiendo con
las vivas y describiendo un motor que ya cambió. No se leen, no se citan y conviene sacarlas de la
carpeta de skills. Lo que decían está hoy en `references/types/` de `/hyperframes`.

### Lo que no existe

- **REALSFX no es una skill.** Verificado el 28 de octubre de 2026. Lo parecido es "Unrealsfx",
  una categoría de efectos de la biblioteca de pago Artlist. Decirlo en vez de buscar media hora.
- **`/brag` sí existe** (github.com/latent-spaces/brag, MIT) pero no está instalado y no hace falta:
  escribe la historia y delega el render a HyperFrames, que es lo que ya hace el tipo `launch`.

---

## 2. La voz: de quién es la pieza

Antes de escribir una línea del guion, resolver de quién es.

**Aztec** manda `~/.claude/AZTEC.md` y el repo `~/Proyectos/aztec-copy`. Leer `CLAUDE.md`,
`alma/SOUL-aztec.md` y el alma del canal. No se negocia: cero invención de cifras, toda cifra con
dueño visible, prohibido "no es X, es Y", em-dash, emojis, signos de apertura, "descubre",
"desbloquea". El resultado antes que la herramienta. Una idea por pieza.

**RegiaVía o Calzada**: registro **usted**, igual que regiavia.com. Sin hype. La firma es
"Venda más. Gaste menos." El producto se llama **Calzada** y la agencia **RegiaVía**: en el login y
en la app la marca grande es RegiaVía; en la página pública, Calzada.

**Un cliente**: leer su `00-INDICE.md` y su `01 Contexto y marca/`. Si tiene skill propia
(`mecatronisis-brand`, `con-cuentas-claras-copy`, `aztec-brand`), esa manda sobre esta.

**En todos los casos**, las reglas de cualquier texto de Santiago: sin em-dashes, sin emojis, sin
signos de apertura. Frases cortas. Nada de autoayuda.

El registro también es una decisión de **diseño**, no solo de copy. Una fundación respetada y una
agencia de IA no mueven el texto a la misma velocidad ni usan la misma curva. Eso está en
`referencias/diagnostico.md`, sección "el eje de la seriedad".

---

## 3. Lo que no se puede afirmar

Un video se comparte y se queda. Una cifra inventada ahí dura más que en un correo.

- **Ningún número sin medirlo primero.** Si sale de una base, consultarla en el momento y poner la
  fecha de la medición en el video o en el pie. Pasó de verdad: el video de Calzada decía "76% de
  las tareas las crea una IA", de una medición vieja; al volver a contar daba otra cosa.
- **Si el presentador se equivoca al hablar, en pantalla va lo que quiso decir**, no lo que dijo.
  Y si dice una cifra que no se puede sostener, en pantalla no va ninguna.
- **Nunca "mejor que <competidor>".** Es la frase que un escéptico tumba primero. Lo que diferencia
  se muestra. Se puede nombrar a la competencia para decir qué hacen bien y qué problema distinto
  resuelve lo nuestro.
- **Las noticias se verifican en la fuente primaria** (la keynote, la página oficial), no en prensa.
- **Nada de nombres de clientes reales** en una pieza pública sin permiso escrito. Para demos, un
  proyecto ficticio.
- **Ningún pantallazo sin revisar qué más sale.** Las barras laterales traen listas de clientes y
  nombres de grupos. Recortar antes de publicar. Lo que quede legible se tapa y se vuelve a
  renderizar: se comprueba con OCR sobre el video ya editado, no a ojo (`referencias/verificar.md`).
- **El nombre propio de una persona en pantalla lo confirma quien lo pidió**, contra una fuente
  (la etiqueta de la reunión, su LinkedIn), antes de renderizar.

---

## 4. Locución: qué cambió y qué sigue igual

**Lo nuevo (noviembre de 2026).** Entrar con `npx hyperframes auth login` es **gratis** y abre, en
el plan Free: catálogo de más de 10.000 pistas de música, efectos de sonido, búsqueda de más de
75.000 imágenes y 3 minutos al mes de Voice Turbo. Eso cambia el cálculo de la música y de los
efectos: ya no hay que rebuscar en bancos con atribución para una pista de fondo.

Sobre la voz, tres caminos y ninguno es automático:

| Camino | Qué da | Cuándo |
|---|---|---|
| `npx hyperframes auth login` → Voice Turbo | 3 min al mes gratis | piezas cortas, probar un guion |
| `npx hyperframes tts` (Kokoro, en el equipo) | ilimitado, sin cuenta | borradores y medir tiempos |
| ElevenLabs vía Composio | voz colombiana de verdad | cuando la pieza la va a ver un cliente |

**La voz de una pieza que se publica se escucha antes de aprobarla.** Kokoro y las voces premade
en inglés hablan español con acento gringo; en una pieza de una agencia colombiana eso es peor que
el silencio. Eso no se asume: se genera una frase, se oye y se decide.

**ElevenLabs funciona vía Composio, no con una llave local.** Las voces de biblioteca en español
**no las deja el plan gratis por API**: devuelven `402 paid_plan_required`. Son 5 dólares de
crédito. Las dos que sirven:

| voice_id | Quién | Para qué |
|---|---|---|
| `86V9x9hrQds83qf7zaGn` | Marcela, colombiana | piezas para Colombia, cercanía |
| `1u9q7vX1Lcx74yAcFPt7` | Luisa, narradora latinoamericana | narración, explicadores |

Ajustes que funcionan: `stability: 0.62`, `similarity_boost: 0.8`, `style: 0`. Y se genera **una
pista por escena**, no una sola corrida: así cada frase cae donde debe con `adelay` de ffmpeg, en
vez de rezar para que calce.

**Por defecto, y salvo que el diagnóstico diga otra cosa, la pieza se escribe para leerse en
mudo.** Es como se miran los videos en un feed y en una landing. La voz se agrega cuando el
diagnóstico la pide, no por costumbre.

**Nunca se gastan los créditos de nadie sin preguntar.**

---

## 5. Sonido, medición y verificación

Están en sus archivos porque son largos y se consultan, no se leen de corrido:

- **`referencias/medir.md`**: cómo un agente que no ve ni oye llega a saber qué hay en el bruto.
  Transcripción con tiempos por palabra, hoja de contacto, dónde está la cabeza del presentador en
  cada cuadro, qué quemó el editor y dónde están las pantallas negras.
- **`referencias/sonido.md`**: la tabla de niveles que funciona, qué suena a barato, cómo se mezcla
  sin dañar la voz y por qué el audio nunca va dentro del render.
- **`referencias/verificar.md`**: las seis comprobaciones antes de entregar. Ninguna es a ojo.
- **`referencias/trampas.md`**: lo que rompe el proceso sin dar error.

---

## 6. Dónde queda el archivo

Según MAPA, y nunca en el home ni en el repo:

- Video de pauta: `~/Downloads/Trabajo/<Cliente>/03 Pauta/Videos de pauta/<AAAA-MM Campaña>/`
- Video orgánico, clase, reel: `~/Downloads/Trabajo/<Cliente>/04 Contenido/Videos/`
- Video de un producto propio que vive en una web: junto a la web
  (real: `pm-regiavia/public/landing/lanzamiento.mp4`)
- Proyecto propio: `~/Downloads/Mis proyectos/<Proyecto>/04 Contenido/Videos/`

Reglas de entrega:

1. **Un entregable, un formato.** Se entrega el mp4 y nada más.
2. **Nombre nuevo si corrige algo ya entregado.** Los editores cachean por ruta: un archivo con el
   mismo nombre puede no recargarse nunca. Y nunca se sobrescribe la base de nadie.
3. **Se abre el archivo** con `open` (o `open -R` para mostrarlo en el Finder) y en la respuesta va
   como enlace `file://` con los espacios en `%20`.
4. **El mensaje final dice**: qué tiene el video por tramos con sus segundos, qué se respetó, cómo
   se verificó y qué se puede quitar fácil. Corto y sin jerga.
5. **Si algo no se pudo hacer o no está verificado, se dice.**

---

## 7. El plan B: cuando HyperFrames es demasiado

Para una pieza chica y muy a la medida (una composición propia con pantallazos reales y texto) hay
un camino probado que no necesita framework, en `~/Proyectos/pm-regiavia/video/`:

- `escena.html` es la composición entera y expone `window.pintar(t)`, que deja la escena exacta en
  el milisegundo `t`. **Regla que no se rompe: ninguna animación ni transición de CSS.** Esas
  tienen su propio reloj y al renderizar se saltan fotogramas. Todo movimiento sale de `pintar`.
- `render.mjs` abre Chrome headless por CDP, llama a `pintar` por cada fotograma, captura y junta
  con ffmpeg. `--fps 12` para un borrador; `--en 14.2` para mirar un solo segundo.
- Toda capa arranca en `opacity: 0`: si `pintar` revienta se ve negro, que es un error evidente, en
  vez de todas las escenas encimadas, que parece un diseño malo. Y el renderizador falla ruidoso.

**Cuándo usarlo:** composición muy a medida, o HyperFrames no disponible.
**Cuándo no:** cualquier cosa que el motor ya haga. No se reconstruye un motor.

---

## 8. El reproductor, si el video va en una web

En `~/Proyectos/pm-regiavia/src/components/landing/reproductor.tsx` hay uno con un efecto que vale
la pena reusar: **la barra avanza rápido y va frenando** (1,6 veces la velocidad real al empezar,
0,4 al terminar). Una barra pareja le dice a quien mira "te faltan treinta segundos" en el primer
segundo y ahí se va.

**El límite es parte de la receta:** la barra es ritmo, los números no se tocan. La duración que se
muestra es la de verdad. Un contador que diga "quedan 8" cuando faltan veinte no es un efecto, es
una mentira.

Y el `<video>` se pinta siempre, también en el servidor: decidir entre `<img>` y `<video>` con
`matchMedia` hace que el HTML llegue con una imagen y el video aparezca al hidratar, cambiando la
página delante de quien mira.
