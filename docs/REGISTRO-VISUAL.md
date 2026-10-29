# Registro visual

> Cómo se decide **cómo se tiene que ver** una pieza, antes de dibujar nada.
>
> Esto no es una galería de estilos. Una galería te da 86 looks y ninguna razón
> para escoger. Esto da la razón. El look se construye después, y se construye
> solo.

---

## 1. Por qué no sirve una librería de prompts

Copiar un prompt bonito produce una pieza bonita que no es de nadie. Y pasa lo
peor: la pieza se ve bien y está mal, porque el estilo contradice lo que el
contenido necesita que la gente sienta.

Un video de historia con estética de caricatura infantil le dice al espectador
"esto es un cuento". Un video de matemáticas con collage psicodélico le dice
"esto es opinión". El estilo no decora: **el estilo es un argumento sobre qué
tan en serio hay que tomarse lo que se está diciendo.**

Entonces la skill no necesita 86 prompts. Necesita responder tres preguntas y
derivar el look de ahí.

---

## 2. Las tres preguntas

### 2.1 · ¿Qué tipo de verdad es esto?

Es la que más manda y casi nadie la hace.

| El contenido es… | Entonces la imagen tiene que… | Y NO puede… |
|---|---|---|
| **Un hecho verificable** (una cifra, un anuncio, una ley) | Mostrar la fuente real, capturada | Ilustrarse. Una ilustración de un dato lo vuelve opinión |
| **Una explicación** (cómo funciona algo) | Construirse paso a paso, una pieza a la vez | Aparecer terminada. Si aparece armada, no explicó |
| **Una historia** (algo que pasó) | Tener textura, tiempo y lugar | Ser genérica. Lo genérico mata el "esto pasó de verdad" |
| **Una opinión o una venta** | Mostrar la cara de quien lo dice | Esconderse detrás de gráficos. Gráficos vendiendo = desconfianza |

### 2.2 · ¿Qué tiene que sentir quien mira?

No "qué tiene que entender". Qué tiene que **sentir**.

Rigor · Curiosidad · Urgencia · Calma · Asombro · Cercanía · Autoridad

Una sola. Si son dos, la pieza está haciendo dos trabajos y hay que partirla.

### 2.3 · ¿Qué permite la marca?

La marca **vetan** antes de que el estilo proponga. Si RegiaVía es espresso,
crema y naranja, entonces el neón cian está vetado aunque le quede perfecto al
tema. Ver `REGLAS.md` 0.1.

---

## 3. El mapa

De tipo de contenido a dirección de arte. **Con la razón al lado**, porque la
razón es lo que permite resolver un caso que no esté en la tabla.

| Contenido | Dirección | Por qué |
|---|---|---|
| **Histórico** | Cartografía: mapas de época, líneas de tiempo, grano de papel, tinta sepia, rotulación a mano | El mapa antiguo es el objeto que la cultura asocia con "esto es un registro, no un invento". Da autoridad sin solemnidad |
| **Matemático / técnico** | Gráficos construidos: ejes que se dibujan, curvas que se trazan, geometría limpia sobre fondo oscuro | En matemáticas **el dibujo ES la demostración**. Se construye en pantalla porque ver construirse es entender |
| **Para niños** | Animación de formas: colores saturados, formas redondas, rebote en el movimiento, caras | La forma redonda y el rebote leen como "seguro, amable". Un niño no lee el texto, lee el movimiento |
| **Producto / lanzamiento** | El producto real, en 3/4, con luz dura y fondo limpio. Nada de ilustrarlo | La gente compra lo que ve. Un producto ilustrado parece que no existe todavía |
| **Dato o noticia** | Captura real de la fuente, recortada y resaltada | Ver `REGLAS.md` 4.1. La prueba, no el dibujo de la prueba |
| **Proceso / tutorial** | Pantalla real con zoom y señalamiento | Quien sigue un tutorial necesita reconocer su propia pantalla |
| **Testimonio / marca** | Persona a cuadro, gráficos mínimos, tipografía de la marca | La cara es el argumento. Lo demás estorba |
| **Concepto abstracto** (confianza, riesgo, tiempo) | Metáfora física: objetos, peso, equilibrio, distancia | Lo abstracto solo se entiende cuando se vuelve cosa que se puede tocar |

**Lo que no está en la tabla se resuelve así:** se pregunta de qué objeto del
mundo real la gente ya saca esa sensación, y se construye el look desde ese
objeto. El mapa antiguo para lo histórico es exactamente eso.

---

## 4. Cómo se arma el prompt

Lo que pediste: que la skill sepa **construirlo**, no copiarlo. Un prompt de
estilo que funciona tiene seis partes, siempre en este orden.

```
1. SUSTRATO      sobre qué está hecho. Papel prensado, pantalla
                 de fósforo, cartón, vidrio, tela. Esto manda sobre
                 todo lo demás: define textura, borde y luz.

2. PALETA        tres a cinco colores con su trabajo asignado
                 (fondo, tinta, acento, sombra). De la marca si hay.

3. TRAZO         cómo se dibuja un borde. Línea de pincel, corte
                 limpio de vinilo, lápiz de cera, trazo de plumilla.

4. LUZ           de dónde viene y qué tan dura. Es lo que separa
                 "plano" de "con cuerpo".

5. LETRA         la tipografía Y cómo se comporta: rotulada a mano,
                 compuesta en plomo, renderizada en pantalla.

6. MOVIMIENTO    la física del mundo. ¿Las cosas caen, flotan,
                 se desvanecen, se dibujan solas? Una sola física
                 por pieza.
```

Y tres prohibiciones que valen para cualquier estilo:

- **Una física a la vez.** Si unas cosas caen y otras flotan, el mundo es falso.
- **El sustrato manda.** Si es papel, nada puede brillar como pantalla.
- **La letra pertenece al mundo.** Tipografía de pantalla sobre papel acuarelado
  delata todo.

### Ejemplo, con el mismo contenido en dos registros

Tema: *cómo se calcula una herencia*.

> **Histórico-cartográfico** — Sustrato: papel de mapa prensado, grano visible,
> bordes gastados. Paleta: sepia de fondo, tinta ferrogálica, un solo rojo de
> lacre para el acento. Trazo: plumilla, grosor variable. Luz: lateral suave,
> como vela. Letra: rotulada a mano, cursiva inglesa para los nombres.
> Movimiento: las líneas se dibujan solas, de izquierda a derecha.

> **Técnico-construido** — Sustrato: pantalla, fondo espresso plano. Paleta:
> crema para la tinta, naranja para el acento, nada más. Trazo: corte limpio,
> cápsulas completas. Luz: ninguna, plano. Letra: Outfit para los datos,
> Archivo 800 para las cifras. Movimiento: cada rama aparece cuando se
> nombra, y se queda.

Mismo tema, dos argumentos distintos sobre qué es una herencia: un documento
que viene de lejos, o un cálculo que se puede verificar. **Esa es la decisión,
y es anterior al color.**

---

## 5. Cómo aprende esto

El banco de estilos de `estilos/` no guarda prompts. Guarda **el código que
produjo una pieza que quedó buena**, con sus seis partes ya resueltas. Se
modifica, no se reescribe. Ver `REGLAS.md` 0.4.

Cada vez que una pieza queda bien, se le anota arriba qué respondió a las tres
preguntas de §2. Así la siguiente no empieza de cero: empieza por buscar un
caso con las mismas respuestas.

---

## 6. Referencias

- **The AI Style Atlas** (futurepedia.io): 86 looks en 14 categorías. Nombres
  útiles como vocabulario: *Flat-Vector Science, Watercolor Wash, Shadow Puppet
  Theatre, Whiteboard Explainer, Manim-Style Math, Illuminated Manuscript,
  Papercraft Models, Halftone Pop Panel, Isometric Pastel, 1940s Film Noir,
  Bioluminescent Deep Sea, Editorial Essay Collage*.
  **Se usa como diccionario, no como catálogo para copiar.** Los textos de sus
  prompts están detrás de un POST con parámetros y no se pudieron extraer; da
  igual, porque lo que vale es el eje de §3, no el texto.
- `prompt-motion.com`: ~83 piezas con su prompt exacto.
