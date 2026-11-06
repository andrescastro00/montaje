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

---

## 9. Locución propia

**9.1 · Si hay voz del dueño, gana.**
Una voz de biblioteca, aunque sea colombiana, suena a banco de voces. La del
dueño del taller suena a taller. Antes de pagar locución, preguntar si graba.

**9.2 · El guion se entrega con instrucciones de grabación, no solo con texto.**
Lo que decide la calidad es el cuarto, la distancia y el silencio de cabeza,
no la redacción. Se piden: cuarto con cosas blandas, el celular a un palmo y de
lado, **cinco segundos de silencio al principio** (es la huella del ruido),
dos segundos entre tomas, y el archivo original, nunca por WhatsApp (recomprime
a 16 kHz mono y lo que llegue ya no se arregla).

**9.3 · Se mide la grabación antes de decidir cuánto limpiarla.**
Separación p95−p5 medida: 49,1 dB en la toma de Santiago. Con eso, la cadena
`normal` (afftdn nf=−20 + anlmdn) dejó el piso en −110 dB, que es silencio
digital: se oye procesado. La `suave` (highpass + afftdn nf=−28) dio +9 dB y
sonido de persona. **Cuanto más limpia llega, menos se le mete.**

**9.4 · Los silencios no se dejan en cero.**
Un bloque de voz rodeado de nada suena pegado con cinta. Los huecos se rellenan
con tono de sala del mismo archivo (el rabo, donde no habla), con cruce de
0,03 s. La costura deja de oírse.

**9.5 · Las fronteras salen de `silencedetect`, nunca de whisper.**
whisper.cpp interpola y entrega bloques pegados sin huecos (GOTCHAS 1). Para
saber qué dice cada bloque, se corta por energía y se transcribe cada bloque
por separado.

**9.6 · Lo cortado se vuelve a leer.**
Después de montar la voz se transcribe el resultado y se compara con lo que se
quería dejar. Es la única forma de saber que no se partió una palabra.

**9.7 · Con voz, el texto en pantalla es subtítulo, no titular.**
Un titular grande que repite lo que se está oyendo es ruido. El texto pasa a
servirle a quien mira en silencio: dice exactamente lo que se dice, en caja
baja (se lee más rápido que la versalita de marca) y con la palabra que pesa en
el color de acento.

**9.8 · La voz se despega 8 dB de la cama, y se comprueba transcribiendo la
mezcla.**
Si whisper lee la mezcla final palabra por palabra, se entiende. Si se come
palabras, la cama está muy arriba. Es la única prueba de inteligibilidad que
puede correr un agente que no oye.

**9.9 · Una grabación tiene tres defectos distintos, y quitar ruido solo toca
uno.**
Se confunden todo el tiempo y se arreglan con herramientas distintas:

| Defecto | Qué es | Qué suena | Con qué se quita |
|---|---|---|---|
| Ruido | fondo constante que no depende de la voz | zumbido, aire | `afftdn` (`sonido_limpio.py`) |
| Eco | la propia voz rebotando con retardo | hueco, lejano | WPE (`realzar_voz.py`) |
| Tono | el micrófono oyó mal el reparto de graves y agudos | apagado, sin calidad | EQ medida (`realzar_voz.py`) |

El tercero es el que más se siente y el que yo me salté: entregué la locución
de Santiago con +9 dB de separación voz-ruido y él la oyó mal igual, porque el
problema no era el ruido. Medido en su toma: **2,5 kHz estaba 22 dB por debajo
del pico de 200 Hz**, cuando en locución eso son 12. Una voz así suena
retumbada y lejana, y eso es lo que un oído sin entrenar llama "eco".

**9.10 · El tono se corrige midiendo, no de oído y nunca con una receta.**
Se saca el espectro promedio de los cuadros CON voz, se compara banda por banda
(tercios de octava) contra una curva de locución, y la diferencia es la
corrección. Tres frenos que son parte de la regla:

- **Techo de ±10 dB.** Más que eso no es ecualizar, es inventar lo que el
  micrófono no capturó.
- **Repartir entre cortar y realzar**, no solo realzar: bajar el retumbe de
  200 Hz suena igual que subir la presencia y no sube el ruido con ella.
- **No tocar lo que un filtro propio dejó vacío** (GOTCHAS 14).

En la toma de Santiago salieron −6 dB en 200 Hz y +5 dB en 3,15 kHz: una
inclinación de +7,3 dB hacia la presencia. El error medio contra la curva de
locución bajó de 4,5 a 2,4 dB.

**9.11 · Primero el eco, después el tono, y el de-esser al final.**
El orden no es decorativo. Realzar la presencia antes de quitar el eco realza
el eco; y realzar la presencia siempre sube el siseo de las eses, así que el
de-esser va **después** del EQ, nunca antes. Orden completo:

```
highpass 85  →  WPE (eco)  →  EQ medida (tono)  →  afftdn (ruido)
             →  de-esser  →  compresor  →  loudnorm en pasada aparte
```

**9.12 · El eco de un cuarto chico solo lo quita un modelo GENERATIVO.**
Esto se probó con el oído de Santiago de por medio: después de arreglarle el
tono, seguía oyendo el cuarto. Se midió y se probó todo lo que hay:

| Herramienta | Qué hace | Qué quitó |
|---|---|---|
| `afftdn` y compañía | quitan ruido | nada de eco, no es su trabajo |
| WPE (`nara_wpe`) | resta la cola tardía | RT60 0,37 → 0,29 s, y en reflexiones tempranas un 9 % dañando la voz |
| 7 modelos de UVR | restan la reverb | **nada**: −28 a −59 dB de energía, SRMR sin moverse |
| Resemble Enhance | **resintetiza la voz** | RT60 1,27 → **0,14 s** |

Los siete de UVR (DeEcho-DeReverb, De-Echo-Normal, De-Echo-Aggressive,
aufr33-jarredou y tres MelBand Roformer, uno con SDR 19,17) están entrenados
con voces de **música** y reverb artificial de plancha o sala. No se activan
con una voz real grabada con celular en un cuarto de verdad.

**La línea que separa lo que sirve de lo que no es restar contra generar.**
Un cuarto chico no agrega una cola larga: agrega reflexiones a 3 y 5 ms que se
suman a la voz misma y la peinan. Eso no se puede restar, porque está dentro
del sonido directo. Solo se arregla volviendo a generar la voz.

**9.13 · Con un modelo generativo, `tau = 0` y se comprueba transcribiendo.**
Con los valores por omisión, Resemble Enhance inventa. Medido en la misma toma:

```
tau=0,5  nfe=64    "calcomanía"              ->  "pescomanía"
                   "Escríbanos por WhatsApp" ->  "Estriba nuestro WhatsApp"
tau=0,0  nfe=128   idéntico a la toma cruda, palabra por palabra
```

`tau` es la temperatura. En 0 el modelo deja de muestrear al azar, así que
además de no inventar **es determinista**, y el montaje se puede repetir
(REGLAS 1.2). Y aun así se comprueba: `quitar_eco.py` transcribe entrada y
salida y compara. Un modelo que reescribe la onda puede reescribir la palabra;
la transcripción no es un lujo, es la condición para usarlo.

**Mezclar el modelo con el original no sirve.** Probado en 40, 60, 75 y 90 %:
el RT60 se queda en 1,27 s hasta el 100 %. El eco está en el original y
cualquier dosis lo devuelve entero.

**9.14 · Después de un modelo generativo, las fronteras se mueven, y NO se
reajustan a ciegas.**
La duración se conserva al milisegundo, pero los finales de palabra caen hasta
47 ms más tarde. Ajustar cada frontera buscando energía en el archivo nuevo
parece lo obvio y está mal: metía de vuelta "o el material que usted se
imagina" y "al alcance de todos ustedes", las dos frases que se habían cortado
a propósito. Lo correcto: **se mantienen los tiempos del EDL**, se amplía el
margen de salida, y el margen se topa contra las zonas que se botaron.
El corte editorial manda sobre el detector.

**9.15 · Lo que sigue sin poder hacerse.**
Resemble Enhance no es magia: reconstruye la voz a partir de lo que el
micrófono capturó. Si el micrófono no capturó una banda, no aparece. Y lo que
de verdad arregla un cuarto chico sigue siendo **grabar cerca**: el sonido
directo cae con la distancia y las reflexiones no, así que acercarse de 40 a
10 cm sube la relación directo/cuarto unos 12 dB. Eso es más de lo que logra
cualquier modelo, y es gratis.

## 10. Primero se diagnostica la pieza, después se abre el motor

**10.1.** Un TikTok de 10 segundos, un video de YouTube de 14 minutos y el institucional de una
fundación respetada no son la misma pieza con distinta duración. Son gramáticas distintas: cambian
la relación de aspecto, dónde cae el gancho, los cortes por minuto, cuánto texto cabe, si hay voz,
si lleva subtítulos quemados y hasta si se puede hacer un chiste.

**10.2.** Antes de abrir el motor se escribe la **ficha de la pieza** y se dice: qué es, dónde se
publica, formato y duración, en qué segundo tiene que haber pasado algo, ritmo, palabras por
pantalla, sonido, subtítulos, registro y lo prohibido para esa marca. Cinco líneas.

**10.3.** El agente **decide**. No interroga. Solo pregunta cuando dos lecturas producen trabajo
materialmente distinto y caro de rehacer: un tono nuevo, algo que cuesta plata, algo que obliga a
volver a grabar. Se pregunta una vez, con opciones concretas y con el segundo exacto de cada
escena de la que se hable.

**10.4.** El registro de una marca no es solo cómo habla el copy: es **cómo se mueve** la pieza. La
curva, el tiempo quieto en pantalla, si hay barrido o fundido y si cabe un chiste salen del mismo
eje. Está en `skill/video-de-marca/referencias/diagnostico.md`.

**10.5.** Las zonas de peligro de cada red se respetan siempre, y la cabeza de quien sale en cámara
queda a 30 px o más de cualquier borde de panel, **en todos los cuadros**, no en el que se miró.
Eso se mide, no se calcula a ojo.

**10.6.** El gusto del editor con el que se trabaja **no va en la skill**: va en un `AGENTS.md`
local, que cada persona llena con el suyo. No hay uno común. El molde está en
`skill/video-de-marca/plantillas/AGENTS.md`.

---

## 11. Se mira antes de decidir, y se trabaja en local

**11.1 Un agente de lenguaje no ve ni oye un video.** La falla no suena a "no puedo ver": suena a
un plan precioso, detallado y seguro, de una pieza que no existe, escrito a partir del título y del
nombre del archivo. Antes de proponer un tramo, se mira: hoja de contacto, fotogramas del punto de
decisión, cortes medidos, palabras con su milisegundo. Cómo, según lo que el agente sepa hacer,
está en `VER-VIDEO.md`.

**11.2 Mirar es salir con números, no con adjetivos.** Cortes por minuto, segundo del gancho,
palabras por pantalla, de dónde entra el texto, dónde está la cara, qué tan fuerte va la música.
Si una referencia no se puede volver números, no se miró.

**11.3 "Mire este reel" es la mejor información que va a llegar.** Casi nadie sabe describir el
video que quiere, y casi todos saben señalar uno que les gusta. Un reel de referencia se trae, se
mide y se convierte en la columna de la izquierda de una tabla de dos columnas. Lo ajeno es
referencia, no material: se aprende su ritmo, no se reusan sus planos, su música ni su locución.

**11.4 El trabajo es local.** El repo es el cerebro y se comparte; el material, los renders y la
voz no salen del equipo. Al repo no se sube ni un bruto, ni un render, ni un fotograma. Si hay que
forzar un `git add`, se está haciendo algo mal.

**11.5 El oficio se comparte, el gusto no.** Lo que le sirve a cualquiera (una trampa de `ffmpeg`,
un nivel que funciona, una medición) va a `GOTCHAS.md` o aquí. Lo que es de una persona o de una
marca va a su `mi/AGENTS.md`, que es local y de cada quien. Esa separación es lo que permite que
dos personas usen el mismo repo sin pisarse, y lo que lo hace útil para alguien de afuera.

**11.6 Las herramientas se comprueban antes de prometer.** `./instalar.sh` corre al abrir. Prometer
un video y fallar a los veinte minutos porque faltaba `ffmpeg` es peor que decirlo en el primer
mensaje.
