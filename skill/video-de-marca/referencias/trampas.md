# Trampas

Lo que rompe el proceso **sin dar error**. Cada una costó horas una vez.

---

## zsh y ffmpeg

- **`$n:algo` en zsh se lee como un modificador.** `$ms:all` se interpreta como `$ms` con el
  modificador `:a`, y el filtro de ffmpeg sale roto sin ningún aviso. Siempre `${n}` antes de los
  dos puntos.
- **`vstack` y `hstack` con más de dos entradas** necesitan `=inputs=N` explícito.
- **`colorkey` pone alfa 255 a todo lo que no coincide.** Para recortar una zona, `drawbox` con
  `replace=1`.
- **`tblend` marca un corte un cuadro tarde.** Para ubicar cortes, `select='between(n,a,b)'` con
  `tile` y mirar.
- **Chroma key con verde puro**: cero fundidos y ningún verde propio en la pieza. Cualquier
  opacidad intermedia queda turbia.
- **Para unir sin recodificar, `-c copy`.** Pero no se pega un tramo recodificado con el resto
  copiado si el códec tiene fotogramas clave espaciados: el corte se ve.
- **`concat`: el filtro, no el demuxer.** El demuxer se detuvo en el quinto segmento y entregó 384
  cuadros de 811 sin decir nada. El filtro decodifica todo y no depende de las marcas de tiempo del
  contenedor.
- **Para cortar por número de cuadros, `-frames:v N`, no `-t`.** Con fuente a cuadro variable,
  `-t` entrega un número distinto de cuadros cada vez.
- **Material de celular va a cuadro variable**: `fps=30` como primer filtro de la cadena, antes de
  cualquier otra cosa.

---

## HyperFrames y GSAP

- Un `fromTo` con opacidad 1 en el "from" se pinta desde el cuadro cero por `immediateRender`.
  Lleva `immediateRender: false`. Y las coordenadas se miden **después** de la entrada, nunca en
  t = 0.
- `radial-gradient(circle at X% Y%, ... 34%)` se corta en cuadrado. Hay que darle radio en píxeles:
  `circle 250px at ...`.
- Los overlays de pantalla completa visibles desde el inicio disparan el lint. O entran con un
  tween desde `opacity: 0`, o van dentro de un contenedor más chico.
- Los `<audio>` tienen que ser estáticos dentro de la raíz, con `id` y su propia pista. Si el
  contenido se genera por script, `insertAdjacentHTML`, no `innerHTML =`.
- Con identificadores generados en un bucle, prefijo único por bloque: el `check` no detecta
  identificadores duplicados.
- **`power2` es cúbica.** Para sincronizar dos tweens hay que usar la misma curva y su inversa
  exacta, no una parecida.
- **`onUpdate` no corre en `seek()`.** Para una trayectoria, `keyframes` con `ease: "none"`.
- `remove-background` del motor sirve para **personas**. Para objetos, la API de Vision del sistema
  (`VNGenerateForegroundInstanceMaskRequest`).

---

## "Se ve pixelado"

Casi siempre es la vista previa, no el export. Se comprueba con un render borrador y cuadros a
resolución completa antes de tocar nada.

Y dos cosas que sí pixelan de verdad: `filter: blur` o `drop-shadow` sobre elementos que se animan,
y `will-change` en capas que hacen algo más que trasladarse.

---

## Barridos de onda que se parten

- La cresta no puede ir a más de unos 1.500 px por segundo.
- Tiene que salir **completa** del cuadro.
- Nada de la escena siguiente puede verse antes de que la ola lo cubra.

Y para un trazo que escribe: **una onda larga y continua**, no un zigzag por letra. Fluido quiere
decir curvas largas y velocidad constante.

---

## Entorno

- **Un disco exFAT rompe `npm install` y los `init`** con `ENOTSUP ... link`, y llena todo de
  archivos `._*`. Se trabaja en el disco interno y se copia al externo solo el código y los
  renders.
- **Antes de un render largo, `df -h`.** El render escribe cada cuadro en el directorio temporal.
  Con 1,5 GB libres dio `ENOSPC` a mitad de camino. En videos enormes se renderiza por bloques y
  se unen con `concat -c copy`.
- **El directorio temporal se vacía de un día para otro.** Los scripts de medición viven en el
  proyecto, no en el temporal.
- **No se cuelga un render en primer plano.** Se lanza en segundo plano y se espera con un bucle.
- **Un archivo de audio grande dentro del proyecto cuelga el bundle.** Un `.wav` de 190 MB lo dejó
  seis minutos. Con un `.gitignore` que excluya `out/`, `build/`, audio y video, baja a un segundo.
- **Un script con el nombre de un módulo de Python lo tapa.** Un archivo `re.py` en el directorio
  de trabajo rompe `import re` desde dentro de numpy, con un error que no nombra el archivo.
- **No se instalan modelos en el python del sistema.** Un `pip install` degradó numpy y rompió
  opencv. Cada modelo en su propio entorno virtual.
- **`open -R "<archivo>"`** lo muestra seleccionado en el Finder.
- **Si el archivo "no carga"** después de entregarlo: lo más probable es que se haya sobrescrito
  mientras el reproductor lo tenía abierto. Se cierra el reproductor antes de copiar, y se entrega
  con nombre nuevo cuando corrige algo ya entregado.

---

## Medir contra una métrica mala

La trampa más cara y la más difícil de ver: **cuando una medida sale distinta cada vez que se
cambia la ventana, no se usa para decidir.** Pasó con una medición de reverberación que dio 0,76,
0,92, 1,27, 1,50 y 1,55 según la ventana, y llevó a optimizar la cadena contra un número que no
medía nada.

Lo mismo con cualquier métrica que se compare entre dos señales que no son comparables: medir
"cuánto eco quedó" antes y después de una ecualización no dice nada, porque la ecualización cambió
el balance.

Cuando pase: se imprime la curva cruda, se mira, y si no se sostiene, se dice y se para.
