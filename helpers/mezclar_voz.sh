#!/bin/bash
# Mezcla locucion + cama (ambiente real y/o musica), con la cama DUCKEADA.
#
#   mezclar_voz.sh voz.wav cama.wav salida.wav [LUFS]
#
# La voz se despega ~8 dB de la cama (REGLAS 9.8). Para comprobar que se
# entiende, transcribir la SALIDA con whisper: si lee palabra por palabra,
# se entiende; si se come palabras, la cama esta muy arriba.
#
# El loudnorm va en una pasada APARTE: dentro de un filter_complex grande
# falla (GOTCHAS 6).
set -e
VOZ=$1; CAMA=$2; OUT=$3; I=${4:--14}
TMP="$(mktemp -t mezcla).wav"
ffmpeg -y -v error -i "$CAMA" -i "$VOZ" \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.030:ratio=7:attack=15:release=340:level_sc=1.6[d];\
[d][1:a]amix=inputs=2:duration=longest:normalize=0[out]" \
  -map "[out]" -ac 2 -ar 48000 -c:a pcm_s16le "$TMP"
ffmpeg -y -v error -i "$TMP" -af "loudnorm=I=${I}:TP=-1.0:LRA=11" -ar 48000 -c:a pcm_s16le "$OUT"
rm -f "$TMP"
ffmpeg -hide_banner -i "$OUT" -af ebur128 -f null - 2>&1 | grep -A8 Summary | grep -E "I:|LRA:"
