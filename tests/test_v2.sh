#!/usr/bin/env bash
set -euo pipefail
RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
TEMP="$(mktemp -d)"
trap 'rm -rf -- "$TEMP"' EXIT
mkdir -p "$TEMP/bin" "$TEMP/medios/subcarpeta"
cp "$RAIZ/tests/mocks/zenity" "$TEMP/bin/zenity"
chmod +x "$TEMP/bin/zenity"
export MOCK_MEDIA_DIR="$TEMP/medios" MOCK_DIALOG_LOG="$TEMP/dialogos" MOCK_PROGRESS_LOG="$TEMP/progreso"
export PATH="$TEMP/bin:$PATH"
ffmpeg -v error -f lavfi -i testsrc2=s=64x64:r=10:d=1 -f lavfi -i sine=frequency=440:duration=1 -c:v mpeg4 -c:a aac -shortest "$MOCK_MEDIA_DIR/video uno.MP4"
ffmpeg -v error -i "$MOCK_MEDIA_DIR/video uno.MP4" -map 0:v -c copy "$MOCK_MEDIA_DIR/sin audio.mp4"
ffmpeg -v error -i "$MOCK_MEDIA_DIR/video uno.MP4" -map 0:v -map 0:a -map 0:a -c copy "$MOCK_MEDIA_DIR/dos pistas.mp4"
touch "$MOCK_MEDIA_DIR/subcarpeta/omitido.mp4" "$MOCK_MEDIA_DIR/subcarpeta/omitido.mov"
bash "$RAIZ/convertir_medios.sh"
grep -q "foreground='#16803c'" "$MOCK_DIALOG_LOG"
grep -q 'Convertidos: 3' "$MOCK_DIALOG_LOG"
grep -q 'Omitidos: 1' "$MOCK_DIALOG_LOG"
[[ "$(ffprobe -v error -select_streams a -show_entries stream=codec_name,sample_rate -of csv=p=0 "$MOCK_MEDIA_DIR/video uno.mov")" == 'pcm_s24le,48000' ]]
[[ "$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$MOCK_MEDIA_DIR/dos pistas.mov" | wc -l)" == 2 ]]
[[ -z "$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$MOCK_MEDIA_DIR/sin audio.mov")" ]]
for base in 'video uno' 'dos pistas' 'sin audio'; do
    entrada="$MOCK_MEDIA_DIR/$base.mp4"; [[ -e "$entrada" ]] || entrada="$MOCK_MEDIA_DIR/$base.MP4"
    [[ "$(ffmpeg -v error -i "$entrada" -map 0:v -c copy -f hash -)" == "$(ffmpeg -v error -i "$MOCK_MEDIA_DIR/$base.mov" -map 0:v -c copy -f hash -)" ]]
done
# Un archivo dañado debe dar rojo y no dejar un MOV.
printf 'archivo dañado' > "$MOCK_MEDIA_DIR/roto.mp4"
: > "$MOCK_DIALOG_LOG"
if bash "$RAIZ/convertir_medios.sh"; then echo 'Se esperaba error' >&2; exit 1; fi
grep -q "foreground='#c62828'" "$MOCK_DIALOG_LOG"
grep -q 'Fallidos: 1' "$MOCK_DIALOG_LOG"
[[ ! -e "$MOCK_MEDIA_DIR/roto.mov" ]]
rm "$MOCK_MEDIA_DIR/roto.mp4" "$MOCK_MEDIA_DIR/video uno.mov"
# Una conversión terminada pero una comprobación fallida tampoco da verde.
printf '#!/usr/bin/env bash\nexit 1\n' > "$TEMP/bin/ffprobe"
chmod +x "$TEMP/bin/ffprobe"
: > "$MOCK_DIALOG_LOG"
if bash "$RAIZ/convertir_medios.sh"; then echo 'Se esperaba fallo de verificación' >&2; exit 1; fi
grep -q "foreground='#c62828'" "$MOCK_DIALOG_LOG"
[[ ! -e "$MOCK_MEDIA_DIR/video uno.mov" ]]
[[ -z "$(find "$MOCK_MEDIA_DIR" -name '.conversor-*' -print)" ]]
printf 'Pruebas con medios reales superadas.\n'
