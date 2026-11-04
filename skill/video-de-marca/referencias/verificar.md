# Verificar antes de entregar

Ninguna de estas se hace a ojo. Un video se publica y se queda: el costo de un error es mayor que
el de comprobarlo.

Se verifica **el entregable**, no el proyecto. El archivo que se va a enviar.

---

## 1. Duración y cuadros de cada pista

No solo del video: también del audio. Un archivo con el video de 31,5 s y el audio de 29,8 s se ve
bien y se oye mal al final.

```bash
ffprobe -v error -show_entries stream=codec_type,duration,nb_frames -of compact=p=0 FINAL.mp4
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames \
  -of csv=p=0 FINAL.mp4
```

El número de cuadros tiene que ser el esperado, no "parecido".

---

## 2. Sincronía del audio contra el bruto

Tiene que dar cero. Se correlacionan ocho segundos de audio a 8 kHz en tres puntos distintos del
video (principio, mitad, final):

```python
c = np.correlate(final[400:-400], base, "valid")
lag_ms = (np.argmax(c) - 400) / 8
```

Si da distinto de cero en algún punto, hay un desfase que crece y se oye.

---

## 3. Lo que no se tocó sigue igual

Fuera de los tramos con motion, el video entregado tiene que ser el bruto. Se comprueba con PSNR:
por encima de unos 42 dB está intacto.

```bash
ffmpeg -hide_banner -ss 0 -to 4.5 -i FINAL.mp4 -ss 0 -to 4.5 -i BASE.mp4 \
  -lavfi "[0:v][1:v]psnr" -f null - 2>&1 | grep average
```

No se usa `-v error` para esto: `psnr` y `ebur128` imprimen a nivel info y con `-v error` no sale
nada y parece que no corrió.

---

## 4. El volumen de la voz quedó como en el bruto

```bash
ffmpeg -hide_banner -i FINAL.mp4 -map 0:a -af ebur128 -f null - 2>&1 | grep -E "^\s+I:"
```

---

## 5. Cuadros del entregable en los momentos clave, en mosaico

Y se miran. Cuatro preguntas:

- La cabeza completa en todas las pantallas partidas.
- Nada dentro de las zonas de peligro de la red a la que va.
- Nada encima de lo que el editor ya había quemado.
- Las tarjetas caben: el borde inferior por encima del límite de la descripción.

Ayuda dibujar las guías encima con `drawbox` en los límites de la red: y = 270, y = 1480, x = 960
para un vertical de 1080 x 1920.

---

## 6. Qué quedó legible que no debería

OCR sobre **todos** los cuadros del video ya editado, no del proyecto. Lo que siga legible se tapa
con cajas y se vuelve a renderizar.

Lo que se escapa siempre: los zooms con desenfoque parcial y los dígitos sueltos grandes. Y lo que
hay que buscar: nombres de clientes, números de teléfono, correos, nombres de grupos de WhatsApp,
cifras de gasto, barras laterales con listas.

---

## 7. Lo que se dice al entregar

- Qué tiene el video, **por tramos con sus segundos**.
- Qué se respetó: lo que ya estaba hecho, las zonas, la marca.
- **Cómo se verificó**, con los números: sincronía, cabeza, PSNR, LUFS.
- Qué se puede quitar fácil si no gusta.
- Lo que no se pudo hacer o no está verificado, dicho claro.

Corto y en lenguaje de quien lo lee. Nada de jerga que no haga falta.
