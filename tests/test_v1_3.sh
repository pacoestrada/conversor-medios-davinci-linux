#!/usr/bin/env bash

set -euo pipefail

RAIZ_PROYECTO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
DIRECTORIO_TEMPORAL="$(mktemp -d)"
MOCKS="$RAIZ_PROYECTO/tests/mocks"

limpiar() {
    rm -rf -- "$DIRECTORIO_TEMPORAL"
}
trap limpiar EXIT

CARPETA_MEDIOS="$DIRECTORIO_TEMPORAL/medios de prueba"
mkdir -p -- "$CARPETA_MEDIOS/subcarpeta"
touch -- "$CARPETA_MEDIOS/video uno.MP4"
touch -- "$CARPETA_MEDIOS/subcarpeta/video dos.mp4"
touch -- "$CARPETA_MEDIOS/subcarpeta/video dos.mov"

export MOCK_MEDIA_DIR="$CARPETA_MEDIOS"
export MOCK_FFMPEG_LOG="$DIRECTORIO_TEMPORAL/ffmpeg.log"
export MOCK_PROGRESS_LOG="$DIRECTORIO_TEMPORAL/progreso.log"
export MOCK_DIALOG_LOG="$DIRECTORIO_TEMPORAL/dialogos.log"

PATH="$MOCKS:$PATH" "$RAIZ_PROYECTO/convertir_medios.sh"

[[ -f "$CARPETA_MEDIOS/video uno.mov" ]]
[[ -f "$CARPETA_MEDIOS/subcarpeta/video dos.mov" ]]
[[ "$(wc -l < "$MOCK_FFMPEG_LOG")" -eq 1 ]]
grep -q '100' "$MOCK_PROGRESS_LOG"
grep -q 'Convertidos: 1' "$MOCK_DIALOG_LOG"
grep -q 'Omitidos porque ya existían: 1' "$MOCK_DIALOG_LOG"

rm -f -- "$CARPETA_MEDIOS/video uno.mov"
: > "$MOCK_FFMPEG_LOG"

MOCK_ZENITY_CANCEL=1 PATH="$MOCKS:$PATH" "$RAIZ_PROYECTO/convertir_medios.sh"

[[ ! -e "$CARPETA_MEDIOS/video uno.mov" ]]
[[ ! -s "$MOCK_FFMPEG_LOG" ]]

printf 'Pruebas de la v1.3 superadas.\n'
