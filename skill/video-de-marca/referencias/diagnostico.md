# Diagnosticar la pieza antes de abrirla

Un TikTok de 10 segundos y el institucional de una fundación respetada no son la misma pieza con
distinta duración. Son **gramáticas distintas**. Este archivo es cómo se decide cuál es cuál.

Se diagnostica. No se interroga. El agente contesta estas siete por su cuenta con lo que tiene
(el pedido, la carpeta del cliente, su manual de marca, el material) y solo pregunta lo que no
puede inferir y sería caro equivocar.

---

## Las siete preguntas

**1. Dónde se publica.** Define la relación de aspecto, la duración útil y las zonas muertas.
No es lo mismo "para redes" que "para el feed de Instagram": si quien pide dice "redes", el agente
elige y lo dice, no pregunta.

**2. Qué tiene que pasar después de verlo.** Que paren (gancho), que entiendan (explicación), que
confíen (prueba), que escriban (CTA). Una pieza hace **una** de esas cosas bien. Si el pedido trae
dos, se dice cuál queda de protagonista.

**3. Quién es la marca y en qué nicho juega.** Una agencia de IA puede ser veloz y jugar. Una
fundación con cincuenta años no. Un taller de grabado láser necesita que se vea el material, no el
motion. Esto se mira en el manual de marca del cliente, no se improvisa.

**4. Qué material hay de verdad.** Antes de diseñar: hay cara a cámara, hay producto, hay pantallas,
hay fotos, o no hay nada y toca dibujarlo. Se abre la carpeta y se mira. Un plan que pide material
que no existe es un plan que no se puede ejecutar.

**5. En qué estado lo va a ver quien lo mire.** En el feed, en mudo, con el pulgar listo para
subir. O sentado en una sala de juntas con el proyector. Esto decide si el texto es obligatorio.

**6. Quién edita después.** Si el editor pone sus propios subtítulos, el agente no los pone. Si el
editor ya quemó su gancho y su fecha en el bruto, no se pone nada encima. Esto va en el
`AGENTS.md` de cada quien.

**7. Cuánto se puede gastar.** Voz de pago, modelos generativos y avatares cuestan. Si cuesta, se
pregunta una vez, con el número, antes de gastar.

---

## La ficha, en cinco líneas

El resultado del diagnóstico se escribe y se dice. No se guarda en la cabeza.

```
Pieza:      <qué es>            Red:      <dónde se publica>
Formato:    <relación> <dur>    Gancho:   <segundo en que tiene que haber pasado algo>
Ritmo:      <cortes por minuto> Texto:    <palabras por pantalla>
Sonido:     <voz / música / mudo>         Subtítulos: <sí quemados / no, los pone el editor>
Registro:   <cómo habla esta marca>       Prohibido: <lo que esta marca no hace>
```

---

## Los arquetipos, con números

Los números son puntos de partida medidos en piezas reales, no leyes. Si el diagnóstico pide otra
cosa, manda el diagnóstico, y se dice por qué.

| Pieza | Relación | Duración | Gancho antes de | Cortes/min | Texto por pantalla | Sonido |
|---|---|---|---|---|---|---|
| Gancho de TikTok o Reel | 9:16 | 7 a 15 s | 1,5 s | 20 a 40 | 3 a 6 palabras | mudo + subtítulo quemado |
| Reel explicativo | 9:16 | 30 a 60 s | 2 s | 12 a 20 | 4 a 8 palabras | voz del bruto |
| Short de YouTube | 9:16 | 15 a 50 s | 2 s | 15 a 25 | 4 a 8 palabras | voz, con música baja |
| YouTube largo | 16:9 | 6 a 20 min | 30 s | 4 a 10 | una frase | voz + ambiente |
| Institucional de una organización seria | 16:9 | 60 a 120 s | no hay gancho, hay apertura | 3 a 6 | una frase, poco | voz grave + música sobria |
| Hero de una web, en bucle | 16:9 o 21:9 | 6 a 12 s | n/a | 2 a 4 | ninguno o dos palabras | **mudo siempre** |
| Pauta en Meta | 9:16 y 1:1 | 15 a 30 s | 3 s | 10 a 20 | 3 a 6 palabras | mudo + subtítulo |
| Demo de producto | 16:9 | 45 a 90 s | 5 s | 6 a 12 | etiquetas cortas | voz |
| Sting de logo o separador | la del destino | 3 a 6 s | n/a | 1 | el nombre | un golpe, o mudo |
| Intro de caso de éxito | la de la serie | fija, la que pida el editor | n/a | 1 a 3 | el nombre | **sin pista de audio** |

Tres reglas que salen de esa tabla y se olvidan seguido:

- **El hero de una web va mudo y en bucle.** Un hero con voz es un anuncio que nadie pidió. Y tiene
  que poder cortarse en cualquier cuadro sin que se note.
- **La intro de una serie sale sin pista de audio** y con la duración exacta que pida el editor. Un
  clip más corto que el hueco de su línea de tiempo se lo rechazan.
- **La pauta se entrega en 9:16 y en 1:1.** Entregar una sola relación es entregar media pauta.

---

## El eje de la seriedad

El registro no es solo cómo habla el copy. Es cómo **se mueve** la pieza. Un mismo contenido, tres
velocidades:

| | Institucional serio | Marca de producto | Creador / agencia de IA |
|---|---|---|---|
| Entrada del texto | fundido de 0,4 s | desplazamiento con freno | pop con rebote corto |
| Curva | `power1` o lineal | `power2.out` | `back.out` suave |
| Corte entre escenas | fundido a negro o a blanco | corte seco | barrido con sonido |
| Tiempo quieto en pantalla | largo, deja respirar | medio | mínimo, siempre pasa algo |
| Color | la paleta, plana | la paleta + un acento | acentos y degradados |
| Chiste | no | si la marca lo tiene | sí |
| Mascota, emoji, caricatura | **nunca** | solo si está en el manual | sí |

Y lo que no cambia en ninguna columna: **nada de texto con trazo ni bordes** (`WebkitTextStroke`).
Para separar texto de un fondo se usa un degradado detrás o una sombra suave. El contorno se ve
barato en las tres.

---

## Las zonas de peligro, por red

Un gráfico bien hecho debajo de la interfaz de la app es un gráfico que nadie ve. Medidas sobre un
lienzo de 1080 x 1920.

**Instagram Reels y TikTok**
- Arriba: los primeros **270 px** se los come la interfaz.
- Abajo: la descripción y el nombre tapan de **y ≈ 1480** para abajo.
- Derecha: la columna de botones ocupa de **x ≈ 960** para la derecha.
- Lo útil queda entre y 270 y 1480, y hasta x 960. Se compone **simétrico respecto al centro**
  (x = 540), no corrido para esquivar la cara.

**Shorts de YouTube**: igual arriba, pero el título puede subir más desde abajo. Se deja y < 1420.

**Feed cuadrado y pauta**: se compone dentro del 90% central y el texto clave dentro del 80%. El
motor dibuja esas guías solo; no se dibujan a mano.

**Y la regla que no se negocia en vertical: nunca se le corta la cabeza al presentador.** La gorra
o el pelo quedan a **30 px o más** de cualquier borde de panel o tarjeta, en **todos** los cuadros,
no en el que se miró. Se mide, no se calcula a ojo: `referencias/medir.md`, sección de caras.

---

## Reglas de oficio que valen para casi toda pieza

Salieron de rechazos reales, no de teoría.

1. **Visuales, no texto.** Una pieza que es solo texto moviéndose es una pieza mala, salvo que el
   encargo sea justamente tipografía cinética. El texto que haya va sincronizado con lo que se dice.
2. **Interfaces y productos reales.** Si se habla de Gmail, de WhatsApp o de Claude, se recrea la
   interfaz **de hoy**: se abre la app, se leen los textos exactos, el orden, los grises, los
   radios y los altos de fila, y se redibuja. Nada genérico y nada de memoria, que cambian seguido.
   Las capturas con datos de alguien no se usan tal cual: se redibujan.
3. **Solo se titula lo que se anuncia.** Si nadie dijo "caso número uno", el uno no lleva título.
4. **Un gráfico de calificación se mueve una vez**, en la palabra del veredicto, y se queda quieto
   hasta el siguiente. Una barra que tiembla todo el tiempo no se lee.
5. **Si algo ya está quemado en el bruto** (el gancho del editor, una fecha, un "gratis"), se mide
   cuándo entra y cuándo sale y no se pone nada encima.
6. **Simetría respecto al centro.** Los gráficos no se corren para esquivar una cara: se busca una
   franja libre.
7. **Pantalla partida solo para demos.** El resto del tiempo el presentador va completo y las
   tarjetas van en las franjas libres: la pared sobre la cabeza y la zona de las piernas.

---

## Copiar un video de referencia

Cuando llega un video y el pedido es "hazlo igualito":

1. La herramienta es **`/reverse-any-video`**, que lo vuelve un proyecto editable y compara el
   render contra el original cuadro por cuadro. Es función de pago: si lo rechaza, se dice y se
   para, no se improvisa un sustituto.
2. Si no hay plan, se hace a mano: hojas de contacto a 8 o 10 cuadros por segundo y cada escena
   anotada en segundos y en píxeles.
3. **Se traduce la mecánica, no los assets**: qué objeto se transforma en qué, cómo entra y cómo
   sale cada cosa. Los gráficos siguen lo que dice **nuestro** guion, no el de la referencia.
4. Solo se copian videos sobre los que quien pide tiene derechos.

Si lo que se quiere es un episodio nuevo en un estilo probado, y no copiar una pieza concreta, eso
es `/style-sampling`.

---

## Cuándo sí se pregunta

Tres casos, y se pregunta **una vez**, con opciones concretas y con el segundo exacto de cada
escena de la que se hable:

- **Tono nuevo** que la marca no ha usado. Se muestran dos o tres cuadros antes de renderizar todo.
- **Algo que cuesta plata**: voz de pago, modelos generativos, avatares. Con el número.
- **Algo que obliga a volver a grabar** o a reencuadrar todo el material.

Fuera de esos tres, el agente decide, lo dice en una línea con su razón, y sigue.
