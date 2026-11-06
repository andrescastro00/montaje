#!/usr/bin/env bash
# Montaje · instala y comprueba todo lo que hace falta para editar video aqui.
#
#   ./instalar.sh              comprueba e instala lo que falte
#   ./instalar.sh --revisar    solo comprueba, no instala nada
#   ./instalar.sh --completo   agrega lo pesado y opcional (modelo de voz generativo)
#
# Idempotente: correrlo dos veces no rompe nada y la segunda tarda segundos.
# Nunca usa sudo. Nunca toca el python del sistema (ver docs/GOTCHAS.md).

set -o pipefail   # sin -u: en bash 3.2 de macOS un arreglo vacio con -u aborta el script
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="$PWD"

MODO="instalar"; COMPLETO=0
for a in "$@"; do
  case "$a" in
    --revisar|-r)  MODO="revisar" ;;
    --completo|-c) COMPLETO=1 ;;
    --ayuda|-h)    sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "No conozco la opcion $a. Usa --revisar, --completo o --ayuda."; exit 2 ;;
  esac
done

V=$'\033[32m'; R=$'\033[31m'; A=$'\033[33m'; N=$'\033[0m'; B=$'\033[1m'
[ -t 1 ] || { V=""; R=""; A=""; N=""; B=""; }

FILAS=(); PENDIENTES=(); FALLAS=0
anotar() { FILAS+=("$1|$2|$3"); }
ok()     { anotar "$1" "${V}listo${N}" "$2"; }
arreglado() { anotar "$1" "${V}instalado${N}" "$2"; }
falta()  { anotar "$1" "${R}FALTA${N}" "$2"; FALLAS=$((FALLAS+1)); }
aviso()  { anotar "$1" "${A}opcional${N}" "$2"; }
pendiente() { PENDIENTES+=("$1"); }
hay()    { command -v "$1" >/dev/null 2>&1; }
paso()   { printf "  %s…\n" "$1"; }

echo
echo "${B}Montaje${N} · $( [ "$MODO" = revisar ] && echo "revisando" || echo "instalando" ) en $RAIZ"
echo

# ─────────────────────────────────────────────────────────────── 0. el equipo
SO="$(uname -s)"
case "$SO" in
  Darwin) ok "sistema" "macOS $(sw_vers -productVersion 2>/dev/null)" ;;
  Linux)  aviso "sistema" "Linux: instala a mano ffmpeg, nodejs, yt-dlp, whisper.cpp, tesseract" ;;
  *)      falta "sistema" "$SO no esta probado" ;;
esac

if hay git; then ok "git" "$(git --version | awk '{print $3}')"; else falta "git" "sin git no hay repo"; fi

# exFAT rompe npm (GOTCHAS). Y un render largo necesita disco.
FS="$(df -T 2>/dev/null | awk 'NR>1{print $2}' | head -1)"
[ "$SO" = Darwin ] && FS="$(diskutil info . 2>/dev/null | awk -F': *' '/Type \(Bundle\)/{print $2}' | head -1)"
case "${FS:-}" in
  exfat|ExFAT|exFAT) falta "disco" "esta carpeta esta en exFAT y npm se rompe ahi. Muevela a un disco APFS" ;;
  *) LIBRE="$(df -h . | awk 'NR==2{print $4}')"; ok "disco" "$LIBRE libres${FS:+, $FS}" ;;
esac

# ───────────────────────────────────────────────── 1. gestor de paquetes
BREW=""
if hay brew; then
  BREW="brew"; ok "homebrew" "$(brew --version | head -1 | awk '{print $2}')"
elif [ "$SO" = Darwin ]; then
  falta "homebrew" 'instalalo con: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/brew/HEAD/install.sh)"'
fi

instalar_formula() {   # instalar_formula <comando> <formula> <para que> [opcional]
  local cmd="$1" formula="$2" para="$3" opc="${4:-}"
  if hay "$cmd"; then ok "$cmd" "$para"; return 0; fi
  if [ "$MODO" = revisar ] || [ -z "$BREW" ]; then
    [ -n "$opc" ] && aviso "$cmd" "falta. $para · brew install $formula" || falta "$cmd" "$para · brew install $formula"
    return 1
  fi
  paso "instalando $formula"
  if brew install "$formula" >/tmp/montaje-brew.log 2>&1 && hay "$cmd"; then
    arreglado "$cmd" "$para"
  else
    [ -n "$opc" ] && aviso "$cmd" "no se pudo instalar. Mira /tmp/montaje-brew.log" \
                  || falta "$cmd" "no se pudo instalar. Mira /tmp/montaje-brew.log"
    return 1
  fi
}

# ──────────────────────────────────────────────────────── 2. lo que no se negocia
instalar_formula ffmpeg  ffmpeg      "cortar, pegar, renderizar y medir"
instalar_formula ffprobe ffmpeg      "leer los datos reales de un archivo"
instalar_formula node    node        "el motor de video corre en node$(hay node && echo " (v$(node -p process.versions.node))")"
instalar_formula yt-dlp  yt-dlp      "traer un video o un reel desde un enlace"

if hay ffmpeg; then
  FILTROS="$(ffmpeg -hide_banner -filters 2>/dev/null)"
  TIENE=""
  grep -q " drawtext " <<<"$FILTROS" && TIENE="drawtext "
  grep -q " subtitles " <<<"$FILTROS" && TIENE="${TIENE}libass"
  if [ -n "$TIENE" ]; then ok "subtitulos de ffmpeg" "$TIENE disponible"
  else aviso "subtitulos de ffmpeg" "sin drawtext ni libass: los subtitulos se dibujan con helpers/subtitulos.py (es mejor)"; fi
fi

if hay node; then
  MAYOR="$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)"
  [ "${MAYOR:-0}" -ge 20 ] || falta "version de node" "v$(node -p 'process.versions.node' 2>/dev/null) es muy viejo, hace falta 20 o mas"
fi

# ───────────────────────────────────────────────────── 3. oir el video (whisper)
MODELOS="$RAIZ/modelos"
instalar_formula whisper-cli whisper-cpp "transcribir palabra por palabra, en local y gratis"
if hay whisper-cli; then
  mkdir -p "$MODELOS"
  MODELO="$(ls -S "$MODELOS"/ggml-*.bin 2>/dev/null | head -1)"
  if [ -z "$MODELO" ]; then
    # Si ya hay modelos en el equipo, se reusan en vez de bajar 1,6 GB otra vez.
    AJENO="$(ls -S "$HOME"/Proyectos/_modelos/whisper/ggml-*.bin "$HOME"/.cache/whisper/ggml-*.bin 2>/dev/null | head -1)"
    if [ -n "$AJENO" ] && [ "$MODO" = revisar ]; then
      aviso "modelo de whisper" "hay uno en el equipo ($(basename "$AJENO")). Corre ./instalar.sh y lo enlazo"
    elif [ -n "$AJENO" ]; then
      ln -sf "$AJENO" "$MODELOS/$(basename "$AJENO")"; MODELO="$MODELOS/$(basename "$AJENO")"
      arreglado "modelo de whisper" "enlazado el que ya tenias: $(basename "$AJENO")"
    elif [ "$MODO" = revisar ]; then
      falta "modelo de whisper" "sin modelo no hay transcripcion. Corre ./instalar.sh"
    else
      paso "bajando ggml-large-v3-turbo.bin (1,6 GB, una sola vez)"
      URL=https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
      if curl -fL --retry 3 -o "$MODELOS/.parcial" "$URL" 2>/dev/null; then
        mv "$MODELOS/.parcial" "$MODELOS/ggml-large-v3-turbo.bin"
        MODELO="$MODELOS/ggml-large-v3-turbo.bin"
        arreglado "modelo de whisper" "large-v3-turbo, 1,6 GB"
      else
        rm -f "$MODELOS/.parcial"
        falta "modelo de whisper" "no se pudo bajar. Bajalo a mano a modelos/ desde huggingface.co/ggerganov/whisper.cpp"
      fi
    fi
  else
    ok "modelo de whisper" "$(basename "$MODELO") ($(du -hL "$MODELO" 2>/dev/null | cut -f1))"
  fi
fi

# ──────────────────────────────────────────────── 4. medir y dibujar (python)
VENV="$RAIZ/.venv"
PAQUETES=(numpy scipy pillow soundfile nara_wpe)
if [ -x "$VENV/bin/python" ] && "$VENV/bin/python" -c "import numpy,scipy,PIL,soundfile,nara_wpe" 2>/dev/null; then
  ok "python del proyecto" ".venv con $("$VENV/bin/python" -V | awk '{print $2}')"
elif [ "$MODO" = revisar ]; then
  falta "python del proyecto" "falta .venv con ${PAQUETES[*]}. Corre ./instalar.sh"
else
  INTERPRETE=""
  for c in python3.12 python3.11 python3.13 python3; do hay "$c" && { INTERPRETE="$c"; break; }; done
  if [ -z "$INTERPRETE" ]; then
    falta "python del proyecto" "no hay python3. brew install python@3.12"
  else
    paso "creando .venv con $INTERPRETE e instalando ${PAQUETES[*]}"
    [ -x "$VENV/bin/python" ] || "$INTERPRETE" -m venv "$VENV" >/dev/null 2>&1
    "$VENV/bin/pip" install -q --upgrade pip >/dev/null 2>&1
    if "$VENV/bin/pip" install -q "${PAQUETES[@]}" >/tmp/montaje-pip.log 2>&1 \
       && "$VENV/bin/python" -c "import numpy,scipy,PIL,soundfile,nara_wpe" 2>/dev/null; then
      arreglado "python del proyecto" ".venv con $("$VENV/bin/python" -V | awk '{print $2}')"
    else
      falta "python del proyecto" "fallo la instalacion. Mira /tmp/montaje-pip.log"
    fi
  fi
fi

instalar_formula tesseract tesseract "leer el texto que quedo quemado en el video (verificacion)" opcional

# ────────────────────────────────────────────── 5. el motor: HyperFrames
if hay node && hay npx; then
  hf_estado() {   # imprime "<al dia> <atrasadas>"
    local s; s="$(npx --yes hyperframes@latest skills check 2>&1)"
    echo "$(grep -oE '[0-9]+ current' <<<"$s" | grep -oE '^[0-9]+' | head -1):$(grep -oE '[0-9]+ (outdated|missing)' <<<"$s" | grep -oE '^[0-9]+' | paste -sd+ - | bc 2>/dev/null)"
  }
  IFS=: read -r AL_DIA ATRASADAS <<<"$(hf_estado)"
  AL_DIA="${AL_DIA:-0}"; ATRASADAS="${ATRASADAS:-0}"
  if [ "$ATRASADAS" = 0 ] && [ "$AL_DIA" -ge 9 ]; then
    ok "skills de HyperFrames" "$AL_DIA al dia"
  elif [ "$MODO" = revisar ]; then
    falta "skills de HyperFrames" "$AL_DIA al dia y $ATRASADAS atrasadas o sin instalar. Corre ./instalar.sh"
  else
    # El comando es "de la persona", no del agente: lo corre este script, que lo corre la persona.
    paso "actualizando las skills de HyperFrames ($ATRASADAS atrasadas o sin instalar)"
    npx --yes hyperframes@latest skills update >/tmp/montaje-hf.log 2>&1
    npx --yes hyperframes@latest skills        >>/tmp/montaje-hf.log 2>&1
    IFS=: read -r AL_DIA ATRASADAS <<<"$(hf_estado)"
    AL_DIA="${AL_DIA:-0}"; ATRASADAS="${ATRASADAS:-0}"
    if [ "${ATRASADAS:-0}" = 0 ] && [ "${AL_DIA:-0}" -ge 9 ]; then
      arreglado "skills de HyperFrames" "$AL_DIA al dia"
    else
      falta "skills de HyperFrames" "quedaron $AL_DIA al dia y $ATRASADAS atrasadas. Mira /tmp/montaje-hf.log"
    fi
  fi

  # Las huerfanas no se borran solas y describen un motor que ya cambio.
  HUERFANAS=0
  for s in general-video motion-graphics product-launch-video website-to-video faceless-explainer \
           pr-to-video talking-head-recut music-to-video embedded-captions \
           hyperframes-animation hyperframes-audio hyperframes-core hyperframes-creative \
           hyperframes-keyframes hyperframes-media hyperframes-studio; do
    [ -e "$HOME/.claude/skills/$s" ] && HUERFANAS=$((HUERFANAS+1))
  done
  [ "$HUERFANAS" -gt 0 ] && aviso "skills huerfanas" "$HUERFANAS retiradas siguen en ~/.claude/skills. No las leas (docs/GOTCHAS.md 20)"

  CUENTA="$(npx --yes hyperframes@latest auth status 2>&1 | head -3 | tr '\n' ' ')"
  if grep -qiE "not signed in|no session|sign in" <<<"$CUENTA"; then
    aviso "cuenta de HyperFrames" "sin sesion. Es GRATIS y abre 10.000+ pistas, efectos y 75.000+ imagenes"
    pendiente "npx hyperframes auth login   (gratis, lo corre la persona en su terminal, no el agente)"
  elif grep -qiE "signed in|logged in|plan" <<<"$CUENTA"; then
    ok "cuenta de HyperFrames" "con sesion: musica, efectos e imagenes disponibles"
  else
    aviso "cuenta de HyperFrames" "no pude leer el estado de la sesion"
  fi
fi

# ─────────────────────────────────────── 6. la skill, visible para el agente
if [ -d "$HOME/.claude/skills" ] || mkdir -p "$HOME/.claude/skills" 2>/dev/null; then
  DESTINO="$HOME/.claude/skills/video-de-marca"
  ORIGEN="$RAIZ/skill/video-de-marca"
  if [ "$(readlink "$DESTINO" 2>/dev/null)" = "$ORIGEN" ]; then
    ok "skill video-de-marca" "enlazada en ~/.claude/skills"
  elif [ -e "$DESTINO" ]; then
    aviso "skill video-de-marca" "ya hay algo en ~/.claude/skills/video-de-marca y no lo piso. Borralo y vuelve a correr"
  elif [ "$MODO" = revisar ]; then
    falta "skill video-de-marca" "sin enlazar. Corre ./instalar.sh"
  else
    ln -s "$ORIGEN" "$DESTINO" && arreglado "skill video-de-marca" "enlazada en ~/.claude/skills" \
      || falta "skill video-de-marca" "no se pudo enlazar"
  fi
fi

# ──────────────────────────────────────────── 7. las carpetas de esta persona
mkdir -p "$RAIZ/trabajos" "$RAIZ/mi"
if [ -f "$RAIZ/mi/AGENTS.md" ]; then
  REGLAS="$(grep -cE '^[0-9]+\. ' "$RAIZ/mi/AGENTS.md" 2>/dev/null || echo 0)"
  ok "mi/AGENTS.md" "tu gusto, con $REGLAS reglas aprendidas"
elif [ "$MODO" = revisar ]; then
  falta "mi/AGENTS.md" "sin el, el agente edita con gusto de nadie. Corre ./instalar.sh"
else
  cp "$RAIZ/skill/video-de-marca/plantillas/AGENTS.md" "$RAIZ/mi/AGENTS.md"
  arreglado "mi/AGENTS.md" "creado desde la plantilla. Es tuyo y no se sube"
  pendiente "Llena mi/AGENTS.md con tu marca (o deja que el agente lo llene con cada nota tuya)"
fi

# ─────────────────────────────────────── 8. lo pesado, solo con --completo
QUITAECO="$HOME/Proyectos/_modelos/resemble"
if [ -x "$QUITAECO/.venv/bin/python" ]; then
  ok "quitar eco (generativo)" "resemble-enhance instalado"
elif [ "$COMPLETO" = 1 ] && [ "$MODO" != revisar ]; then
  if hay python3.11; then
    paso "instalando resemble-enhance (pesado: torch, ~2 GB)"
    mkdir -p "$QUITAECO" && python3.11 -m venv "$QUITAECO/.venv" >/dev/null 2>&1
    if "$QUITAECO/.venv/bin/pip" install -q resemble-enhance >/tmp/montaje-eco.log 2>&1; then
      arreglado "quitar eco (generativo)" "listo. Se usa con helpers/quitar_eco.py"
    else
      aviso "quitar eco (generativo)" "fallo. Mira /tmp/montaje-eco.log. No es necesario para editar"
    fi
  else
    aviso "quitar eco (generativo)" "necesita python 3.11: brew install python@3.11"
  fi
else
  aviso "quitar eco (generativo)" "no instalado. Solo hace falta si grabas voz en un cuarto con eco: ./instalar.sh --completo"
fi

# ───────────────────────────────────────────────────────────── el resumen
echo
printf "${B}%-26s %-12s %s${N}\n" "CAPACIDAD" "ESTADO" "QUE SIGNIFICA"
printf '%s\n' "────────────────────────────────────────────────────────────────────────────────"
for f in "${FILAS[@]}"; do
  IFS='|' read -r c e q <<<"$f"
  printf "%-26s %-21s %s\n" "$c" "$e" "$q"
done
echo

if [ ${#PENDIENTES[@]} -gt 0 ]; then
  echo "${B}Lo que tienes que hacer tu${N} (el agente no lo puede hacer por ti):"
  for p in "${PENDIENTES[@]}"; do echo "  · $p"; done
  echo
fi

if [ "$FALLAS" -gt 0 ]; then
  echo "${R}${B}Falta algo que si es necesario.${N} Arreglalo antes de prometer un video."
  exit 1
fi
echo "${V}${B}Todo listo.${N} El siguiente paso es traer un video:"
echo "  ./helpers/traer.sh <enlace de YouTube, TikTok, Instagram o ruta del archivo> <nombre>"
echo "  ./helpers/mirar.sh trabajos/<la carpeta que salio>      # para MIRARLO"
echo
