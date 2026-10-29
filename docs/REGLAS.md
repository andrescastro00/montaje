# Reglas

> El criterio. Esto es lo único que no se puede bajar de ningún repo.
>
> **Cómo crece este archivo:** cada vez que Santiago o Diego dicen "esto está
> mal", no se arregla el video y ya. Se busca **cuál regla debió haberlo
> evitado**, y se escribe o se corrige. Una nota que no termina en una línea
> de este archivo es una nota que se va a volver a necesitar.
>
> Cada regla lleva de dónde salió. Las que dicen `[Santiago]` o `[Diego]` mandan
> sobre todas las demás.

---

## 0. Las que mandan sobre todo

**0.1 · La marca manda sobre el efecto.** `[Santiago · 28-oct-2026]`
Un sting de RegiaVía es **un gesto**, no una pila de efectos. Antes de poner un
solo sonido o un solo gráfico, se resuelve en qué registro habla la marca. Si la
marca es cálida y calmada, no se le monta lenguaje de tráiler encima.

*De dónde salió:* se le pusieron tres whooshes, un riser, un sparkle y dos
impactos a una pieza de 6 s de una marca espresso y crema. Veredicto textual:
"los sonidos más AI slop forzados, puestos encima, que he visto jamás".

**0.2 · Silencio no es lo mismo que sin voz.** `[Santiago · 28-oct-2026]`
"Sin locución" nunca quiere decir "sin audio". Una pieza muda se siente rota.
Toda pieza sale con sonido, aunque sea aire a −38 dB.

**0.3 · Una librería de stock siempre suena a stock.**
Para sonido de marca se **diseña** (síntesis, notas, envolventes), no se pega.
Los efectos de catálogo sirven para acentos funcionales (un clic de interfaz en
un tutorial), no para la identidad.

*Confirmación externa:* el banco de 86 estilos más citado genera **también sus
efectos de sonido en código**, por la misma razón. El sonido sintetizado se
versiona, se ajusta al milisegundo y no arrastra licencias.

---

**0.4 · Una referencia de estilo es CÓDIGO, no un video.**
Si se le pasa un MP4 como referencia, el modelo no lo ve: toma unas capturas y
adivina el resto. Se pierde el timing, las curvas de aceleración, el orden de
las capas, todo.

Si la referencia es **el código que produjo esa pieza**, el modelo no reinventa:
**modifica**. Y ahí pasan dos cosas buenas a la vez: sale consistente, y el
modelo barato rinde igual que el caro, porque ya no tiene que inventar la
estructura, solo cambiarle los datos.

> Corolario económico: **un buen banco de estilos en código vale más que un
> modelo más caro.** Esta es la razón de ser de `estilos/`.

---

**0.5 · Todo juicio que tomé solo se dice, en una línea, con su razón.**
`[Santiago · 28-oct-2026]`
No basta con decidir bien. Si la decisión no se dice, no se puede corregir, y
quien recibe el trabajo no sabe si fue criterio o descuido.

*De dónde salió:* se entregó una grabación con subtítulos y nada más. La
decisión era defendible (los gráficos taparían la pantalla que hay que ver),
pero nunca se dijo. Veredicto textual: **"¿Cuál fue el juicio? No me lo
preguntó."** El reclamo no era por el efecto que faltaba: era por la frase que
faltaba. Ver `ENCARGO.md` §1, cajón 3.

**0.6 · Un audio con ruido no se entrega, aunque nadie lo pida.**
`[Santiago · 28-oct-2026]`
Limpiar el ruido de fondo está en el cajón de "hazlo", no en el de "pregunta".
Cadena base en `ENCARGO.md` §5. El límite: si se **oye** que el audio fue
procesado, se pasó.

**0.7 · El color se revisa siempre. Cambiarlo es otra cosa.**
`[Santiago · 28-oct-2026]`
Revisar es obligatorio. Cambiar es un juicio que se dice. Y cuando se cambia,
**menos de lo que uno quiere**: emparejar los clips entre sí es casi siempre
necesario; el grado casi siempre sobra.

---

## 1. Antes de tocar nada

**1.1 · Cada archivo que entra tiene UN trabajo.**
Si se da una referencia, se dice exactamente qué tomar de ella: "de este, el
ritmo del corte"; "de este, la paleta"; "de este, cómo entra el texto". Una
referencia sin instrucción es una invitación a copiar lo que no se quería.

**1.2 · El mapa de beats va antes que cualquier gráfico.**
Lista de cada idea del guion y qué se ve mientras se dice. Se aprueba el mapa
antes de construir. Cambiar una línea de texto cuesta cero; cambiar un gráfico
terminado cuesta horas.

**1.3 · Láminas fijas antes de cualquier MP4.**
Cinco imágenes quietas, lado a lado con la referencia si la hay. Si el color
está plano, si la cara queda tapada, si el encuadre está mal, se ve ahí, gratis.

---

## 2. El corte

**2.1 · Se corta en frontera de frase, no de palabra.**
Los tiempos de palabra traen ~120 ms de error: cuatro fotogramas a 30 fps.
Cortar ahí se come sílabas.

**2.2 · El silencio se respeta cuando es pausa, se quita cuando es error.**
Un umbral de decibeles no sabe la diferencia. Esto es criterio: una pausa antes
de un remate se queda; un "emmm" de tres segundos buscando la idea se va.

**2.3 · Se queda la última toma limpia de cada línea.**
Y se reporta qué se quitó, con su segundo.

**2.4 · Fundido de 30 ms en cada corte de audio.** Sin esto suenan clics.

**2.5 · Los primeros dos segundos deciden todo lo demás.**
Se trabajan aparte y se piden **tres versiones**. Se juzgan **en mudo**: si
engancha sin sonido, engancha.

---

## 3. Gráficos y movimiento

**3.1 · Una idea, un gráfico.** Y se queda el tiempo suficiente para leerse.
No un gráfico por frase.

*De dónde salió:* un editor con 15 años de oficio puso un gráfico por frase
durante meses; los comentarios de su propia audiencia le dijeron que era
demasiado. Cambió la regla.

**3.2 · Se mueve una cosa a la vez.**

**3.3 · Nada de texto dentro de una imagen generada por IA.** Deforma las
letras. El texto se pone en código, siempre.

**3.4 · Los gráficos van del lado contrario a la persona**, y nunca encima de
la cara.

**3.5 · Todo dentro de la zona segura** de la plataforma. Nada de texto en el
20 % inferior en vertical.

**3.8 · El aire de una caja de texto se mide, no se calcula de memoria.**
`[Santiago · 28-oct-2026]`
Arriba y abajo tienen que dar **el mismo número**. Y el aire no se mide contra
el alto de la línea: se mide contra el **alto real del glifo**, que es lo que
el ojo ve.

*De dónde salió:* la cápsula de subtítulos tenía 20 px arriba y 24 abajo. Nadie
lo midió; salió de un `alto = alto_fila * filas + 44` escrito de memoria. Se
nota, y lo notó él.

**3.6 · Ritmo: algo cambia cada 2 a 3 segundos.** Pero cambiar por cambiar
satura. Si todo se mueve, nada resalta.

**3.7 · Cuando algo salga mal, se agregan REGLAS, no EFECTOS.**
La reacción natural cuando una pieza se ve pobre es echarle grano, glow y
cortes. Eso la empeora. Se para, se escriben prohibiciones concretas
("sin recortes, sin grano, la cara siempre natural"), y se vuelve a láminas.

---

## 4. Imágenes de afuera

**4.1 · Si el guion afirma un hecho, sale la prueba real.**
Captura del anuncio real, del sitio real, del post real. No una recreación.

**4.2 · Nada de fotos de internet para decorar.** Si la imagen no prueba nada
ni muestra nada que las palabras no digan, estorba.

**4.3 · Ninguna captura sin revisar qué más sale en ella.** Las barras
laterales traen listas de clientes y nombres. Se recorta antes.

**4.4 · Caras reales solo desde fotos reales y con permiso.**

---

## 5. Sonido

**5.1 · Primero se decide el registro de la marca, después se busca el sonido.**
Ver 0.1.

**5.2 · Los efectos van debajo de la voz y de la música**, no peleando.

**5.3 · El sonido marca dónde está el corte, no al revés.**
Quien decide el corte es el mismo que decide el golpe.

**5.4 · Sonoridad medida, nunca estimada.**
Pieza calmada: −16 a −17 LUFS. Pieza para redes con voz: −14 LUFS.
Pico real por debajo de −1,5 dBTP. Se mide con `ebur128`, no se calcula a ojo.

**5.5 · Un efecto por evento, y solo si el evento importa.**
Tres elementos entrando no son tres efectos. Probablemente es uno, o ninguno.

---

## 6. Antes de que nadie lo vea

**6.1 · Ninguna duración se reporta sin medirla con `ffprobe`.**
El modelo suma mal y cree su propia suma. Caso medido: pidió 300 s, entregó
578 s, reportó 299 s.

**6.2 · Se revisa cada frontera de corte** con la vista compuesta
(tira de fotogramas + onda + palabras), buscando seis cosas:

1. una animación que corre dos veces
2. un gráfico que parpadea y no alcanza a leerse
3. texto que entra tarde para lo que dura
4. un gráfico encima de la cara
5. una palabra dicha dos veces seguidas
6. labios que se despegan de la voz

**6.2 bis · Se lee el texto mirando la imagen.** `[28-oct-2026]`
Antes de dar por buena una escena que lleva texto, se lee el texto **mirando la
lámina**. Si la imagen no demuestra lo que el texto afirma, la escena está mal
aunque se vea bonita.

*De dónde salió:* una escena decía "lo que sirve se junta" y mostraba cuatro
trozos separados, porque al encoger las barras muertas los huecos del `gap`
sobrevivían. Se veía bien y decía exactamente lo contrario.

**6.3 · Máximo tres intentos de arreglo automático.** Al cuarto, se para y se
cuenta qué pasa. Un agente dando vueltas sobre el mismo error quema tiempo.

**6.4 · Se entrega con hoja de decisiones:** qué se cortó, qué se dejó, qué se
decidió sin preguntar y por qué. Eso es lo que permite dar notas precisas.

---

## 7. Cómo se trabaja

**7.1 · Se muestra solo lo que cambió.** No se vuelve a renderizar la pieza
entera para enseñar un ajuste de dos segundos.

**7.2 · Borradores a media resolución.** Calidad plena solo con el corte ya
aprobado.

**7.3 · Renderizar en paralelo: tope de 4.** Más que eso tumba la máquina y los
trabajos se cancelan entre sí.

**7.4 · Decidir nunca va en paralelo.** Repartir decisiones entre varias copias
no da varias opiniones buenas: da varias versiones del mismo error. Medido:
con 6 cortes, en paralelo tardó 28,6 s contra 19,4 s en serie, y los 6 cortes
salieron igual de mal.

**7.5 · Forma de dar notas:** veredicto, arreglos, lo que se queda, y qué
mostrar. Cada arreglo con su segundo y cuánto ("un pelín", "mucho").

**7.6 · Modelo caro para pensar, barato para construir.**
El criterio y la dirección de arte van en el modelo fuerte. Armar los gráficos
uno por uno va en el rápido.
**Matiz importante:** si hay un ejemplar en código (0.4), el modelo barato
también sirve para construir con estilo. El modelo caro se reserva para cuando
hay que inventar la estructura, no para repetirla.

**7.7 · Cuando una pieza quede buena, se vuelve skill.**
No se vuelve a la galería ni al prompt largo. Se guarda el código, se
parametriza lo que cambia, y queda como formato repetible en `estilos/`.

---

## 8. Pendientes

Cosas que todavía no son regla porque no se han probado:

- Qué tan seco o con cuánta cola quiere Santiago el sonido de marca.
  *Falta una referencia suya para medirla.*
- Si el bed instrumental va o no va en piezas cortas de marca.
- Paleta y tipografía de subtítulos para RegiaVía en vertical.
- Reglas propias de Diego (todavía no ha dado ninguna nota).
