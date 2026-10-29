# El encargo

> Qué hacer cuando llega material y nadie dijo exactamente qué hacer con él.
>
> Este documento existe por una falla concreta: llegó una grabación, se le
> pusieron subtítulos y nada más, y a nadie se le explicó **por qué solo eso**.
> El problema no fue la decisión. Fue que la decisión era invisible.
>
> **Una decisión que no se dice no se puede corregir.**

---

## 1. Los tres cajones

Todo lo que pasa en un encargo cae en uno de tres. Nada se queda sin cajón.

### Cajón 1 · Hazlo

Cosas que están bien **siempre**. No se preguntan, no se anuncian antes, se
hacen y se reportan en una línea al final.

- Limpiar el ruido de fondo. Un audio sucio no se entrega nunca.
- Normalizar la sonoridad al destino.
- Quitar aire muerto y arranques fallidos.
- Revisar el color. Revisarlo no es cambiarlo: si ya está bien, se dice "el
  color está bien" y se deja.
- Respetar la zona segura de la plataforma.
- Poner subtítulos si hay voz. En redes se mira en mudo.
- Medir todo lo que se reporta.
- Mirar fotogramas del archivo final antes de entregarlo.

### Cajón 2 · Pregunta, una sola vez

Cosas que **cambian la pieza entera** y no se pueden deducir del material.
Van todas juntas, en un mensaje, máximo cuatro, **cada una con mi
recomendación de primera**. Nunca de a una, nunca a mitad del trabajo.

- Para quién es y qué tiene que hacer quien lo vea.
- Dónde se publica (define formato, duración y ritmo).
- Si lleva voz, y de quién.
- Cuando el material contradice lo que se pidió.

### Cajón 3 · Dilo

Todo juicio que tomé solo se escribe, **en una línea, con su razón**.

> "Le puse subtítulos y nada más porque es una demo de pantalla: los gráficos
> encima taparían justo lo que hay que ver. Si quieres, le meto zooms a los
> clics."

Eso es lo que faltó. No el efecto: la frase.

---

## 2. Qué tengo que saber antes de empezar

Si el encargo no contesta estas cinco, **no se arranca a editar**. Se pregunta.

| | Pregunta | Si no está, se deduce de |
|---|---|---|
| 1 | Para qué plataforma | El formato del material (vertical = redes) |
| 2 | Qué tiene que hacer quien lo vea | **No se deduce. Se pregunta.** |
| 3 | De qué marca es | La carpeta donde está |
| 4 | Cuánto tiene que durar | La plataforma |
| 5 | Lleva voz, música, o va mudo | **No se deduce. Se pregunta.** |

Las dos que no se deducen son las dos que definen la pieza. Adivinarlas es lo
que produce un video correcto que no sirve para nada.

---

## 3. Levantar la mano

**No se entrega algo mediocre por no preguntar.** Tampoco se para todo por una
duda que se resuelve sola.

La regla: **si la duda cambia más de un tercio de la pieza, se pregunta antes
de construir. Si cambia menos, se decide, se construye, y se dice qué se
decidió.**

Y cuando no se sabe algo del tema (qué hace el cliente, qué es un grabado
láser, cómo se llama una pieza): **no se inventa y no se pregunta todavía.**
Primero se busca: en la carpeta del cliente, en su manual de marca, en su sitio,
en internet. Preguntar lo que está escrito en la carpeta de al lado es hacerle
perder el tiempo a quien pidió el trabajo.

Se pregunta cuando la respuesta **no existe en ningún lado** porque está
solamente en la cabeza de quien pidió.

---

## 4. Recetas por tipo de material

El default cuando llega una carpeta y no dice nada más.

### 4.1 · Carpeta de clips verticales sin voz

Lo más común. Material de celular, grabado el mismo día, sin audio útil.

1. **Inventariar y ordenar.** Duración, resolución, orientación, si tiene audio
   servible. Los clips se agrupan por tema, no por nombre de archivo.
2. **Descartar lo inservible:** desenfocado, movido, subexpuesto, duplicado.
   Se dice cuántos se cayeron y por qué.
3. **Elegir el orden.** Una historia, no un collage: qué se ve primero, qué
   entiende quien mira, con qué se queda.
4. **Color.** Corrección pareja entre clips (vienen de luces distintas aunque
   sea el mismo día), y un grado suave. Nunca exagerado.
5. **Voz.** Si la pieza necesita que alguien explique, se escribe el guion
   primero y se aprueba antes de generarla.
6. **Música y efectos**, debajo de la voz.
7. **Subtítulos** siempre, aunque haya voz.
8. **Ritmo.** Algo cambia cada 2 a 3 segundos.
9. **Cierre con una sola acción.**

### 4.2 · Una grabación larga hablando

Transcribir, cortar silencios y repeticiones, subtítulos, limpiar audio,
revisar color. Gráficos solo donde haya una idea que el video no muestra.

### 4.3 · Captura de pantalla

Igual que la anterior, **pero los gráficos tapan justo lo que hay que ver.**
En vez de gráficos: zooms a donde está pasando la acción, y resaltado del
clic. Y se revisa qué más sale en pantalla antes de publicar.

---

## 5. Sonido: el piso mínimo

Un audio con ruido de fondo no se entrega, aunque nadie lo haya pedido.

Cadena base, en este orden:

```
highpass=f=80          quita el retumbo del cuarto y el manejo del equipo
afftdn=nf=-25          resta el ruido estacionario (ventilador, aire, nevera)
anlmdn=s=0.0004        limpia lo que queda, sin volver la voz metalica
deesser                baja las eses que quedan filosas despues de limpiar
acompressor            empareja distancia a la boca
speechnorm             levanta lo bajito sin aplastar lo fuerte
loudnorm               al destino
```

**El límite:** si se oye que el audio fue procesado, se pasó. Mejor un poco de
ruido que una voz de robot. Se comparan los dos antes de decidir.

---

## 6. Color: revisar siempre, cambiar a veces

Revisar es obligatorio (cajón 1). Cambiar es un juicio que se dice (cajón 3).

Qué se mira: clips del mismo día con luces distintas, blancos virados,
negros levantados o aplastados, piel con color raro.

Qué se hace: **primero emparejar** los clips entre sí, y solo después un grado
suave. Emparejar es técnico y casi siempre hace falta. El grado es estilo y
casi siempre debe ser menos de lo que uno quiere.

**Nunca:** saturación alta, contraste duro, virados de moda, piel naranja.

---

## 7. Lo que se entrega con la pieza

Siempre, en el mensaje, no en un archivo aparte:

1. **El archivo**, con su enlace.
2. **Lo medido:** duración, formato, sonoridad. Con la herramienta que lo midió.
3. **Los juicios que tomé solo**, uno por línea, con su razón.
4. **Lo que no hice y por qué**, si fue una decisión y no un olvido.
5. **Lo que haría distinto** si me dice que sí.

El punto 4 es el que faltaba.
