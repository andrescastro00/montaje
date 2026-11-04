# Medir el material antes de diseñar nada

Un agente de lenguaje **no ve ni oye un video**. Todo lo demás del oficio es fácil comparado con
eso. Un plan hecho sin medir es un plan inventado: pone una tarjeta encima de una cara, titula algo
que el presentador nunca dijo o tapa el texto que el editor ya había quemado.

Medir cuesta minutos. Rehacer cuesta horas. Se mide siempre.

---

## 1. Lo primero, los hechos del archivo

```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,duration \
  -show_entries format=duration,size -of default=nw=1 BASE.mp4
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames \
  -of csv=p=0 BASE.mp4
```

El número de **cuadros reales** no es la duración por los fps: el material de celular viene a
cuadro variable. Todo lo que se construya encima se escribe en segundos del bruto.

---

## 2. Hoja de contacto del bruto completo

Un cuadro cada tres segundos, en mosaico. Sirve para ver el encuadre, los cortes y lo que el editor
ya dejó quemado, de un vistazo.

```bash
ffmpeg -i BASE.mp4 -vf "fps=1/3,scale=216:384,tile=11x6" -frames:v 1 hoja.jpg
```

Para mirar un momento concreto con detalle, diez cuadros por segundo y recortado:

```bash
ffmpeg -ss 172.6 -i BASE.mp4 -t 1.6 -vf "fps=10,crop=1080:700:0:200,scale=216:140,tile=4x4" \
  -frames:v 1 detalle.jpg
```

Así se sabe el cuadro **exacto** en que entra y sale lo que ya está quemado, y nada se le pone
encima.

---

## 3. Transcripción con tiempos por palabra

Es el insumo central: con cada palabra y su milisegundo, el agente puede decidir qué dispara qué.

```bash
npx hyperframes transcribe BASE.mp4            # Parakeet o whisper, del propio motor
```

O con whisper.cpp local, que da control fino:

```bash
ffmpeg -i BASE.mp4 -ac 1 -ar 16000 audio/voz16k.wav
nohup whisper-cli -m "<ruta al modelo>" -l es -f audio/voz16k.wav -ml 1 -sow -ojf -of audio/words \
  > audio/whisper.log 2>&1 &
```

- `-ml 1 -sow` da **una palabra por segmento**. El JSON queda en `transcription[].offsets.from`, en
  milisegundos.
- Con GPU va a unas diez veces tiempo real. Dentro de un entorno sin GPU hay que usar `-ng` y es
  del orden de veinte veces más lento: se lanza con `nohup` y se espera.
- Audios largos: cortar en ventanas de unos 9 segundos **por el punto de menor energía**, no por
  tiempo fijo, y transcribir ventana por ventana. Los tiempos salen limpios.

**Trampas medidas:**
- `--prompt` desplaza los tiempos.
- Más de 22 segundos seguidos y los tiempos salen redondeados al segundo.
- `-dtw` junto con `-ng` devuelve todo en cero.
- Whisper oye mal los nombres propios y las marcas: "Cloud" por Claude, "plan E" por planear. Se
  corrige en el plan, **no** en pantalla. Y si alucina una frase al final sobre silencio
  ("suscríbete al canal"), se verifica esa línea transcribiendo solo su ventana.

---

## 4. Dónde está la cabeza del presentador, en cada cuadro

Esta es la medición que evita el error que no se perdona: cortarle la cabeza a alguien.

```bash
ffmpeg -i BASE.mp4 -vf "fps=5,scale=540:960" cuadros/f%05d.png
```

Y sobre esos cuadros, detección de caras con la API de Vision del sistema
(`VNDetectFaceRectanglesRequest`, revisión 3), que es gratis, local y rápida. En un Mac se llama
desde un binario de Swift: el `python3` del sistema no trae pyobjc.

Devuelve `[x, y_arriba, ancho, alto, confianza]` normalizados. De ahí:

- **Tope de la cabeza ≈ y_cara − 0,45 × alto.** Es conservador incluso con gorra.
- Se toma el **mínimo** del tope y el **máximo** de la barbilla en ventanas de diez segundos. Con
  eso se calcula cuánto baja el video en una pantalla partida y dónde termina la franja libre de
  arriba.
- **Se mide en todos los cuadros, no en uno.** Cuando alguien se estira, la cabeza sube unos 60 px.

Si no hay Vision a mano, el sustituto honesto es muestrear cuadros cada 0,2 s y mirarlos en
mosaico con líneas guía dibujadas (`drawbox`) en los límites de las zonas de peligro. Lo que no
vale es calcular a ojo sobre un solo cuadro.

---

## 5. Pantallas negras y tramos, en videos largos

Para un video de horas, decodificar todo es inviable. Se decodifican **solo los fotogramas clave**:

```bash
ffmpeg -skip_frame nokey -i BASE.mp4 -vf "scale=96:54,format=gray" -f rawvideo - | <script>
```

Un fotograma clave con luminancia media por debajo de 20 (en una zona sin burbuja de cámara) es
negro. Dos horas y media se resuelven en unos dos minutos y medio. Después se afina cuadro a cuadro
solo en los bordes de cada tramo, y los límites se guardan en un JSON, en cuadros.

Alternativa sin script: `signalstats` y leer `YAVG` por segundo.

---

## 6. La burbuja de cámara no está quieta

Si el material trae una burbuja de cámara encima de una grabación de pantalla, **no es fija**: salta
y hace zooms lentos. Si el motion le abre un hueco en una posición fija, en algún momento se verá
mal.

- Se guarda su caja en **cada** cuadro: píxeles por encima de 30 a media resolución, multiplicado
  por dos. Seis mil cuadros se resuelven en segundos.
- **Radio de la esquina**: se lee la primera columna clara de cada fila. Medido: una burbuja típica
  tiene radio de 0,13 veces su lado menor; un reel insertado, 0,075 veces su ancho.
- Si el bruto anima la burbuja, el hueco se abre **cuando ya está quieta**, no mientras crece.

---

## 7. Cuando vuelven a exportar el bruto

Pasa seguido y casi nunca hay que rehacer todo.

1. Antes de tocar nada, se comparan los dos brutos: a dos cuadros por segundo en general, y cuadro
   a cuadro en los bordes de cada tramo.
2. **Si todo quedó corrido un número exacto de cuadros**, se reutiliza el motion con un desfase: se
   corren las escenas y los rangos de render; las mediciones hechas sobre el bruto viejo siguen
   sirviendo en sus propias coordenadas.
3. Si solo cambió algo fuera de los tramos con motion, los overlays sirven tal cual y basta volver
   a montar con el audio del bruto nuevo.
4. **El audio del bruto nuevo puede venir unos 48 ms corrido.** Se usa siempre el del nuevo, nunca
   el viejo pegado al video nuevo.

---

## 8. Lo que hay que haber medido antes de escribir el plan

Una lista corta. Si falta una, el plan todavía no se puede escribir.

- [ ] Resolución, fps reales, duración y número de cuadros.
- [ ] Hoja de contacto del bruto completo, mirada de verdad.
- [ ] Transcripción con tiempo por palabra.
- [ ] Tope de la cabeza y barbilla por ventanas, si hay alguien en cámara.
- [ ] Entrada y salida de todo lo que el editor ya quemó.
- [ ] Tramos de pantalla negra o de grabación de pantalla, si los hay.
- [ ] Qué productos o interfaces reales aparecen nombrados, para ir a buscarlos.
