#!/usr/bin/env bash
# Trae un video a una carpeta de trabajo y lo deja medido.
#
#   ./helpers/traer.sh <enlace o ruta> [nombre]
#   ./helpers/traer.sh https://youtu.be/XXXX clase-de-octubre
#   ./helpers/traer.sh "~/Downloads/IMG_5704.MOV" taller
#   ./helpers/traer.sh https://www.instagram.com/reel/XXXX/ referencia --solo-traer
#
# Deja: trabajos/<fecha>-<nombre>/ con bruto/, datos/, vista/, obra/, salida/ y PIEZA.md
# y al terminar llama a mirar.sh, que es lo que te deja VER el video.
#
# Solo para material propio o con permiso. Un reel ajeno es referencia, no material.

set -o pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; RAIZ="$(dirname "$AQUI")"
V=$'\033[32m'; R=$'\033[31m'; N=$'\033[0m'; B=$'\033[1m'; [ -t 1 ] || { V=""; R=""; N=""; B=""; }
muere() { echo "${R}$1${N}" >&2; exit 1; }

ORIGEN="${1:-}"; NOMBRE="${2:-}"; SOLO_TRAER=0
for a in "$@"; do [ "$a" = "--solo-traer" ] && SOLO_TRAER=1; done
[ -z "$ORIGEN" ] && { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
[ "$NOMBRE" = "--solo-traer" ] && NOMBRE=""
command -v ffprobe >/dev/null || muere "Falta ffmpeg. Corre ./instalar.sh"

slug() { echo "$1" | tr '[:upper:]' '[:lower:]' \
  | sed 's/[áàä]/a/g;s/[éèë]/e/g;s/[íìï]/i/g;s/[óòö]/o/g;s/[úùü]/u/g;s/ñ/n/g' \
  | sed 's/[^a-z0-9]\+/-/g;s/^-//;s/-$//' | cut -c1-48; }

ES_ENLACE=0; [[ "$ORIGEN" =~ ^https?:// ]] && ES_ENLACE=1
ORIGEN_LOCAL="${ORIGEN/#\~/$HOME}"

# ── el nombre de la carpeta
if [ -z "$NOMBRE" ]; then
  if [ "$ES_ENLACE" = 1 ]; then
    command -v yt-dlp >/dev/null || muere "Falta yt-dlp para bajar enlaces. Corre ./instalar.sh"
    TITULO="$(yt-dlp --no-warnings --skip-download --print "%(title)s" "$ORIGEN" 2>/dev/null | head -1)"
    NOMBRE="$(slug "${TITULO:-video}")"
  else
    NOMBRE="$(slug "$(basename "${ORIGEN_LOCAL%.*}")")"
  fi
fi
[ -z "$NOMBRE" ] && NOMBRE="video"

CARPETA="$RAIZ/trabajos/$(date +%Y-%m-%d)-$NOMBRE"
n=2; while [ -e "$CARPETA" ]; do CARPETA="$RAIZ/trabajos/$(date +%Y-%m-%d)-$NOMBRE-$n"; n=$((n+1)); done
mkdir -p "$CARPETA"/{bruto,datos,vista,obra,salida}
echo "${B}Carpeta:${N} ${CARPETA#$RAIZ/}"

# ── el material
if [ "$ES_ENLACE" = 1 ]; then
  command -v yt-dlp >/dev/null || muere "Falta yt-dlp. Corre ./instalar.sh"
  echo "  bajando con yt-dlp…"
  yt-dlp --no-warnings --no-playlist \
         -f "bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b" --merge-output-format mp4 \
         --write-info-json --write-thumbnail \
         -o "$CARPETA/bruto/base.%(ext)s" "$ORIGEN" || muere "yt-dlp no pudo bajarlo. Si es privado o pide sesion, bajalo a mano y pasame la ruta del archivo."
  echo "$ORIGEN" > "$CARPETA/datos/origen.txt"
else
  [ -f "$ORIGEN_LOCAL" ] || muere "No existe el archivo: $ORIGEN_LOCAL"
  EXT="${ORIGEN_LOCAL##*.}"
  ln "$ORIGEN_LOCAL" "$CARPETA/bruto/base.$EXT" 2>/dev/null \
    || cp "$ORIGEN_LOCAL" "$CARPETA/bruto/base.$EXT" \
    || muere "No pude copiar el archivo"
  echo "$ORIGEN_LOCAL" > "$CARPETA/datos/origen.txt"
  echo "  material copiado a bruto/"
fi
chmod -w "$CARPETA"/bruto/base.* 2>/dev/null   # bruto es de solo lectura. Nunca se sobrescribe.

BASE="$(ls "$CARPETA"/bruto/base.* 2>/dev/null | grep -viE '\.(json|jpg|png|webp)$' | head -1)"
[ -z "$BASE" ] && muere "No quedo ningun archivo de video en bruto/"

# ── la ficha tecnica: por FLUJO, no del contenedor (docs/GOTCHAS.md)
{
  echo "# Ficha tecnica · $(basename "$BASE")"
  echo "# Medido con ffprobe el $(date '+%Y-%m-%d %H:%M'). Los numeros del contenedor mienten:"
  echo "# estos son por flujo."
  echo
  ffprobe -v error -show_entries stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames,duration,sample_rate,channels,bit_rate \
          -show_entries format=duration,size,bit_rate,format_name -of default=noprint_wrappers=0 "$BASE"
} > "$CARPETA/datos/ficha-tecnica.txt" 2>&1

leer() { ffprobe -v error -select_streams "$1" -show_entries stream="$2" -of csv=p=0 "$BASE" 2>/dev/null | head -1; }
ANCHO="$(leer v:0 width)"; ALTO="$(leer v:0 height)"; DUR="$(leer v:0 duration)"
[ -z "$DUR" ] || [ "$DUR" = "N/A" ] && DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$BASE")"
FPS="$(leer v:0 r_frame_rate)"; AUDIO="$(leer a:0 codec_name)"

# ── PIEZA.md: la ficha que se llena ANTES de abrir el motor
RELACION="vertical 9:16"; [ "${ANCHO:-0}" -gt "${ALTO:-1}" ] && RELACION="horizontal 16:9"
[ "${ANCHO:-0}" = "${ALTO:-1}" ] && RELACION="cuadrado 1:1"
cat > "$CARPETA/PIEZA.md" <<MD
# $(basename "$CARPETA")

Origen: \`$(cat "$CARPETA/datos/origen.txt")\`
Traido: $(date '+%Y-%m-%d %H:%M')

## Lo medido (no se toca: esto es un hecho)

| | |
|---|---|
| Resolucion | ${ANCHO:-?} x ${ALTO:-?} ($RELACION) |
| Duracion | ${DUR:-?} s |
| Fotogramas por segundo | ${FPS:-?} |
| Audio | ${AUDIO:-sin pista de audio} |

Lo demas esta en \`datos/ficha-tecnica.txt\`, \`datos/cortes.txt\` y \`datos/palabras.txt\`.
Para mirarlo: \`vista/vista.html\` (y \`docs/VER-VIDEO.md\` si no sabes como).

## La ficha de la pieza (se llena ANTES de abrir el motor)

Se diagnostica con \`skill/video-de-marca/referencias/diagnostico.md\`. No se pregunta lo que se
puede deducir de la marca, el nicho, el objetivo y la red donde se publica.

\`\`\`
Pieza:      <que es>              Red:      <donde se publica>
Formato:    <relacion> <dur>      Gancho:   <segundo en que tiene que haber pasado algo>
Ritmo:      <cortes por minuto>   Texto:    <palabras por pantalla>
Sonido:     <voz / musica / mudo>           Subtitulos: <quemados / no>
Registro:   <como habla esta marca>         Prohibido: <lo que esta marca no hace>
\`\`\`

## Si hay un reel de referencia

Lo que se saca de mirarlo son numeros, no adjetivos:

| | Referencia | Lo nuestro |
|---|---|---|
| Cortes por minuto | | |
| Segundo del gancho | | |
| Palabras por pantalla | | |
| De donde entra el texto | | |
| Musica: que tan fuerte | | |
| Donde pone la cara | | |

## El plan, por tramos

| Tramo (s) | Que se ve | Que se oye | Por que |
|---|---|---|---|

## Notas de quien aprueba

Cada nota que llegue se copia aqui tal cual, y la regla que de ahi sale se escribe en \`mi/AGENTS.md\`.
MD

echo "  ${V}ficha tecnica y PIEZA.md listos${N}"
if [ "$SOLO_TRAER" = 1 ]; then
  echo
  echo "Siguiente: ${B}./helpers/mirar.sh ${CARPETA#$RAIZ/}${N}"
else
  exec "$AQUI/mirar.sh" "$CARPETA"
fi
