#!/usr/bin/env bash
set -euo pipefail

RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
TEMP="$(mktemp -d)"
trap 'rm -rf -- "$TEMP"' EXIT
# Los archivos descargados como ZIP pueden perder el bit ejecutable.
chmod +x "$RAIZ"/tests/mocks/*
MEDIOS="$TEMP/medios de prueba"
mkdir -p -- "$MEDIOS/subcarpeta"
touch -- "$MEDIOS/video uno.MP4" "$MEDIOS/subcarpeta/video dos.mp4" "$MEDIOS/subcarpeta/video dos.mov"

export MOCK_MEDIA_DIR="$MEDIOS"
export MOCK_FFMPEG_LOG="$TEMP/ffmpeg.log"
export MOCK_PROGRESS_LOG="$TEMP/progreso.log"
export MOCK_DIALOG_LOG="$TEMP/dialogos.log"
PATH="$RAIZ/tests/mocks:$PATH" bash "$RAIZ/convertir_medios.sh"

[[ -f "$MEDIOS/video uno.mov" ]]
[[ "$(wc -l < "$MOCK_FFMPEG_LOG")" -eq 1 ]]
grep -q -- '-map 0 -c copy' "$MOCK_FFMPEG_LOG"
grep -q '100' "$MOCK_PROGRESS_LOG"
grep -q 'Convertidos: 1' "$MOCK_DIALOG_LOG"
grep -q 'Omitidos: 1' "$MOCK_DIALOG_LOG"

rm -f -- "$MEDIOS/video uno.mov"
: > "$MOCK_DIALOG_LOG"
if MOCK_FFMPEG_FAIL=1 PATH="$RAIZ/tests/mocks:$PATH" bash "$RAIZ/convertir_medios.sh"; then
    printf 'Se esperaba un estado de error.\n' >&2
    exit 1
fi
[[ ! -e "$MEDIOS/video uno.mov" ]]
grep -q 'Fallidos: 1' "$MOCK_DIALOG_LOG"
grep -q 'incompleto o dañado' "$MOCK_DIALOG_LOG"

printf 'Pruebas de la v2 superadas.\n'
