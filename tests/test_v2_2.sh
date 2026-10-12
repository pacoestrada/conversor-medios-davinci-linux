#!/usr/bin/env bash
set -euo pipefail
RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
TEMP="$(mktemp -d)"
trap 'rm -rf -- "$TEMP"' EXIT
mkdir -p "$TEMP/bin" "$TEMP/medios/subcarpeta"
cp "$RAIZ/tests/mocks/zenity" "$TEMP/bin/zenity"
chmod +x "$TEMP/bin/zenity"
export MOCK_MEDIA_DIR="$TEMP/medios" MOCK_DIALOG_LOG="$TEMP/dialogos" MOCK_PROGRESS_LOG="$TEMP/progreso"
export MOCK_DIRECTION='Preparar para publicación (MOV → MP4)'
export PATH="$TEMP/bin:$PATH"
ffmpeg -v error -f lavfi -i testsrc2=s=64x64:r=10:d=1 -f lavfi -i sine=frequency=440:duration=1 -c:v libx264 -c:a pcm_s24le -ar 48000 -shortest "$MOCK_MEDIA_DIR/video uno.MOV"
ffmpeg -v error -i "$MOCK_MEDIA_DIR/video uno.MOV" -map 0:v -c copy "$MOCK_MEDIA_DIR/sin audio.mov"
ffmpeg -v error -i "$MOCK_MEDIA_DIR/video uno.MOV" -map 0:v -map 0:a -map 0:a -c copy "$MOCK_MEDIA_DIR/dos pistas.mov"
ffmpeg -v error -f lavfi -i testsrc2=s=64x64:r=10:d=1 -f lavfi -i sine=duration=1 -ac 2 -c:v libx264 -c:a pcm_s24le -ar 48000 -shortest "$MOCK_MEDIA_DIR/estereo.mov"
touch "$MOCK_MEDIA_DIR/subcarpeta/omitido.mov" "$MOCK_MEDIA_DIR/subcarpeta/omitido.mp4"
bash "$RAIZ/convertir_medios.sh"
grep -q "foreground='#16803c'" "$MOCK_DIALOG_LOG"
grep -q 'Convertidos: 4' "$MOCK_DIALOG_LOG"
grep -q 'Omitidos: 1' "$MOCK_DIALOG_LOG"
[[ "$(ffprobe -v error -select_streams a -show_entries stream=codec_name,sample_rate -of csv=p=0 "$MOCK_MEDIA_DIR/video uno.mp4")" == 'aac,48000' ]]
[[ "$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$MOCK_MEDIA_DIR/dos pistas.mp4" | wc -l)" == 2 ]]
[[ "$(ffprobe -v error -select_streams a -show_entries stream=channels -of csv=p=0 "$MOCK_MEDIA_DIR/estereo.mp4")" == 2 ]]
[[ -z "$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$MOCK_MEDIA_DIR/sin audio.mp4")" ]]
for base in 'video uno' 'dos pistas' 'sin audio' 'estereo'; do
 entrada="$MOCK_MEDIA_DIR/$base.mov"; [[ -e "$entrada" ]] || entrada="$MOCK_MEDIA_DIR/$base.MOV"
 [[ "$(ffmpeg -v error -i "$entrada" -map 0:v -c copy -f hash -)" == "$(ffmpeg -v error -i "$MOCK_MEDIA_DIR/$base.mp4" -map 0:v -c copy -f hash -)" ]]
done
# Una salida existente permanece intacta.
huella="$(sha256sum "$MOCK_MEDIA_DIR/video uno.mp4")"
bash "$RAIZ/convertir_medios.sh"
[[ "$huella" == "$(sha256sum "$MOCK_MEDIA_DIR/video uno.mp4")" ]]
# ProRes no admite copia a MP4: informar y eliminar el temporal.
ffmpeg -v error -f lavfi -i testsrc2=s=64x64:r=10:d=1 -c:v prores_ks -threads 1 "$MOCK_MEDIA_DIR/prores.mov"
: > "$MOCK_DIALOG_LOG"
if bash "$RAIZ/convertir_medios.sh"; then echo 'Se esperaba rechazo del vídeo incompatible' >&2; exit 1; fi
grep -q 'Este vídeo no se puede copiar a MP4' "$MOCK_DIALOG_LOG"
[[ ! -e "$MOCK_MEDIA_DIR/prores.mp4" ]]
rm "$MOCK_MEDIA_DIR/prores.mov"
printf 'archivo dañado' > "$MOCK_MEDIA_DIR/roto.mov"
: > "$MOCK_DIALOG_LOG"
if bash "$RAIZ/convertir_medios.sh"; then echo 'Se esperaba error' >&2; exit 1; fi
grep -q "foreground='#c62828'" "$MOCK_DIALOG_LOG"
[[ ! -e "$MOCK_MEDIA_DIR/roto.mp4" ]]
rm "$MOCK_MEDIA_DIR/roto.mov" "$MOCK_MEDIA_DIR/video uno.mp4"
printf '#!/usr/bin/env bash\nexit 1\n' > "$TEMP/bin/ffprobe"
chmod +x "$TEMP/bin/ffprobe"
: > "$MOCK_DIALOG_LOG"
if bash "$RAIZ/convertir_medios.sh"; then echo 'Se esperaba fallo de verificación' >&2; exit 1; fi
grep -q "foreground='#c62828'" "$MOCK_DIALOG_LOG"
[[ ! -e "$MOCK_MEDIA_DIR/video uno.mp4" ]]
[[ -z "$(find "$MOCK_MEDIA_DIR" -name '.conversor-*' -print)" ]]
printf 'Pruebas MOV a MP4 con medios reales superadas.\n'
