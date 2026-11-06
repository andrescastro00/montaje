#!/usr/bin/env bash
# Convierte un video en algo que un agente de lenguaje SI puede mirar.
#
#   ./helpers/mirar.sh trabajos/2026-11-06-reel        # una carpeta ya traida
#   ./helpers/mirar.sh https://www.instagram.com/reel/XXXX/ referencia   # lo trae y lo mira
#   ./helpers/mirar.sh ~/Downloads/bruto.mp4
#
#   --cada 0.5    un fotograma cada medio segundo (por omision: ~60 en total)
#   --hasta 30    solo los primeros 30 segundos
#   --sin-voz     no transcribir
#
# Deja en vista/: fotogramas numerados, hoja-de-contacto.jpg, onda.png y vista.html
# Como mirarlo segun lo que sepas hacer: docs/VER-VIDEO.md

set -o pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; RAIZ="$(dirname "$AQUI")"
V=$'\033[32m'; R=$'\033[31m'; N=$'\033[0m'; B=$'\033[1m'; [ -t 1 ] || { V=""; R=""; N=""; B=""; }
muere() { echo "${R}$1${N}" >&2; exit 1; }

ARG="${1:-}"; [ -z "$ARG" ] && { sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
shift || true
CADA=""; HASTA=""; CON_VOZ=1; NOMBRE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --cada)  CADA="$2"; shift 2 ;;
    --hasta) HASTA="$2"; shift 2 ;;
    --sin-voz) CON_VOZ=0; shift ;;
    *) NOMBRE="$1"; shift ;;
  esac
done

# Si lo que llega es un enlace o un archivo, primero se trae.
ARG_LOCAL="${ARG/#\~/$HOME}"
if [[ "$ARG" =~ ^https?:// ]] || { [ -f "$ARG_LOCAL" ] && [ ! -d "$ARG_LOCAL" ]; }; then
  exec "$AQUI/traer.sh" "$ARG" ${NOMBRE:+"$NOMBRE"}
fi

CARPETA="$(cd "$ARG_LOCAL" 2>/dev/null && pwd)" || muere "No existe la carpeta $ARG"
BASE="$(ls "$CARPETA"/bruto/base.* 2>/dev/null | grep -viE '\.(json|jpg|png|webp|txt)$' | head -1)"
[ -z "$BASE" ] && muere "No hay bruto/base.* en $CARPETA. Traelo con ./helpers/traer.sh"
command -v ffmpeg >/dev/null || muere "Falta ffmpeg. Corre ./instalar.sh"
mkdir -p "$CARPETA"/{vista/fotogramas,datos}

DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$BASE" | cut -d. -f1)"
DUR="${DUR:-0}"; [ -n "$HASTA" ] && [ "$HASTA" -lt "$DUR" ] && DUR="$HASTA"
ANCHO="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$BASE" | head -1)"
ALTO="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$BASE" | head -1)"

# ── 1. fotogramas, uno por cada paso, con el milisegundo en el nombre
# Sesenta fotogramas alcanzan para leer el ritmo de casi cualquier pieza sin
# ahogar al agente en imagenes. Un reel de 15 s sale a cuatro por segundo.
if [ -z "$CADA" ]; then
  CADA="$(awk -v d="$DUR" 'BEGIN{p=d/60; if(p<0.25)p=0.25; printf "%.2f", p}')"
fi
rm -f "$CARPETA"/vista/fotogramas/*.jpg
echo "  un fotograma cada ${CADA} s de ${DUR} s…"
ANCHO_MIN=360
ffmpeg -nostdin -v error -i "$BASE" ${HASTA:+-t "$HASTA"} \
       -vf "fps=1/$CADA,scale=$ANCHO_MIN:-2" -q:v 4 \
       "$CARPETA/vista/fotogramas/f%04d.jpg" 2>/dev/null
# El nombre lleva el segundo real: asi el agente cita "el fotograma del segundo 7,5".
i=0
for f in "$CARPETA"/vista/fotogramas/f*.jpg; do
  [ -e "$f" ] || break
  T="$(awk -v i="$i" -v c="$CADA" 'BEGIN{printf "%07.2f", i*c}' | tr '.' ',')"
  mv "$f" "$CARPETA/vista/fotogramas/s${T}.jpg"; i=$((i+1))
done
CUANTOS="$(ls "$CARPETA"/vista/fotogramas/*.jpg 2>/dev/null | wc -l | tr -d ' ')"

# ── 2. la hoja de contacto: el video entero en UNA imagen
COLS=6; FILAS=$(( (CUANTOS + COLS - 1) / COLS )); [ "$FILAS" -lt 1 ] && FILAS=1
ffmpeg -nostdin -v error -i "$BASE" ${HASTA:+-t "$HASTA"} \
       -vf "fps=1/$CADA,scale=216:-2,tile=${COLS}x${FILAS}:padding=4:color=0x111111" \
       -frames:v 1 -q:v 3 -y "$CARPETA/vista/hoja-de-contacto.jpg" 2>/dev/null

# ── 3. la onda: donde hay voz, donde hay silencio, donde pega la musica
TIENE_AUDIO="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$BASE" | head -1)"
if [ -n "$TIENE_AUDIO" ]; then
  ffmpeg -nostdin -v error -i "$BASE" ${HASTA:+-t "$HASTA"} \
         -filter_complex "showwavespic=s=1600x240:colors=0xff6a2b|0x7a7a7a:split_channels=0" \
         -frames:v 1 -y "$CARPETA/vista/onda.png" 2>/dev/null
fi

# ── 4. los cortes: donde cambia el plano, medido
{
  echo "# Cortes detectados (cambio de plano > 0,30). Segundo del PRIMER cuadro nuevo."
  # OJO: showinfo escribe en nivel "info". Con -v error no imprime NADA y el
  # conteo sale en cero sin dar error. Es el mismo gotcha del psnr.
  ffmpeg -nostdin -v info -i "$BASE" ${HASTA:+-t "$HASTA"} \
         -filter:v "select='gt(scene,0.30)',showinfo" -f null - 2>&1 \
    | grep -oE 'pts_time:[0-9.]+' | cut -d: -f2 | awk '{printf "%.2f\n", $1}'
} > "$CARPETA/datos/cortes.txt" 2>/dev/null
NCORTES="$(grep -cE '^[0-9]' "$CARPETA/datos/cortes.txt" 2>/dev/null)"; NCORTES="${NCORTES:-0}"
CPM="$(awk -v n="$NCORTES" -v d="$DUR" 'BEGIN{ if(d>0) printf "%.0f", n*60/d; else print 0 }')"

# ── 5. las palabras, con su milisegundo
MODELO="$(ls -S "$RAIZ"/modelos/ggml-*.bin 2>/dev/null | head -1)"
if [ "$CON_VOZ" = 1 ] && [ -n "$TIENE_AUDIO" ] && [ -n "$MODELO" ] && command -v whisper-cli >/dev/null; then
  echo "  transcribiendo palabra por palabra…"
  ffmpeg -nostdin -v error -i "$BASE" ${HASTA:+-t "$HASTA"} -ar 16000 -ac 1 -c:a pcm_s16le \
         -y "$CARPETA/datos/voz16k.wav" 2>/dev/null
  # -ml 1 -sow da un token por linea con su tiempo. Ojo: son TOKENS, no palabras;
  # vista.py los vuelve a pegar con la regla de GOTCHAS 1 bis.
  whisper-cli -m "$MODELO" -f "$CARPETA/datos/voz16k.wav" -l es -ml 1 -sow -ojf \
              -of "$CARPETA/datos/palabras" >/dev/null 2>&1
  rm -f "$CARPETA/datos/voz16k.wav"
elif [ "$CON_VOZ" = 1 ] && [ -n "$TIENE_AUDIO" ]; then
  echo "  (sin transcribir: falta whisper-cli o el modelo. Corre ./instalar.sh)"
fi

# ── 6. la pagina para mirarlo
PY="$RAIZ/.venv/bin/python"; [ -x "$PY" ] || PY="python3"
"$PY" "$AQUI/vista.py" "$CARPETA" --cada "$CADA" ${HASTA:+--hasta "$HASTA"} || muere "vista.py fallo"

REL="${CARPETA#$RAIZ/}"
echo
echo "${V}${B}Listo.${N} ${CUANTOS} fotogramas · ${NCORTES} cortes (~${CPM} por minuto) · ${ANCHO}x${ALTO} · ${DUR} s"
echo
echo "${B}Ahora MIRALO.${N} Tres caminos, segun lo que sepas hacer (docs/VER-VIDEO.md):"
echo "  1. Navegador:     abre  file://$CARPETA/vista/vista.html"
echo "  2. Computer use:  open \"$CARPETA/vista/vista.html\"  y toma capturas"
echo "  3. Solo archivos: lee  $REL/vista/hoja-de-contacto.jpg  (el video entero en una imagen)"
EJEMPLO="$(ls "$CARPETA"/vista/fotogramas/*.jpg 2>/dev/null | sed -n "$(( (CUANTOS/3) + 1 ))p")"
echo "                    y    $REL/vista/fotogramas/$(basename "${EJEMPLO:-s0000,00.jpg}")  (el segundo exacto)"
echo
echo "Los numeros estan en $REL/datos/ y la ficha en $REL/PIEZA.md"
