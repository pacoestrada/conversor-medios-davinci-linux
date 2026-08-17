#!/usr/bin/env bash

# Permite elegir gráficamente una carpeta y convierte a MOV todos los MP4
# que encuentre en ella y en sus subcarpetas.

set -u

TITULO="Conversión de archivos multimedia"
CARPETA_SCRIPT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

mostrar_error_sin_zenity() {
    local mensaje="$1"

    if command -v xmessage >/dev/null 2>&1; then
        xmessage -center "$mensaje"
    elif command -v notify-send >/dev/null 2>&1; then
        notify-send -u critical "$TITULO" "$mensaje"
    else
        echo "$mensaje" >&2
    fi
}

if ! command -v zenity >/dev/null 2>&1; then
    mostrar_error_sin_zenity "No se encuentra Zenity. Instálalo con: sudo apt install zenity"
    exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
    mensaje=$'No se encuentra FFmpeg.\n\nInstálalo con: sudo apt install ffmpeg'
    zenity --error --title="$TITULO" --width=430 --text="$mensaje"
    exit 1
fi

CARPETA_SELECCIONADA="$(
    zenity --file-selection \
        --directory \
        --title="Selecciona la carpeta que contiene los vídeos" \
        --filename="$CARPETA_SCRIPT/"
)" || exit 0

if [[ ! -d "$CARPETA_SELECCIONADA" || ! -r "$CARPETA_SELECCIONADA" ]]; then
    zenity --error \
        --title="$TITULO" \
        --width=450 \
        --text="No se puede leer la carpeta seleccionada."
    exit 1
fi

# Normaliza la ruta elegida y elimina posibles barras finales.
CARPETA_ORIGEN="$(cd -- "$CARPETA_SELECCIONADA" && pwd -P)"

# Obtiene los nombres de forma segura, incluso si contienen espacios.
mapfile -d '' ARCHIVOS_MP4 < <(
    find "$CARPETA_ORIGEN" -type f -iname '*.mp4' -print0
)

if (( ${#ARCHIVOS_MP4[@]} == 0 )); then
    printf -v mensaje 'No se han encontrado archivos MP4 en:\n%s' "$CARPETA_ORIGEN"
    zenity --info --title="$TITULO" --width=430 --text="$mensaje"
    exit 0
fi

PENDIENTES=()
OMITIDOS=0

for video in "${ARCHIVOS_MP4[@]}"; do
    salida="${video%.*}.mov"

    if [[ -f "$salida" ]]; then
        ((OMITIDOS += 1))
    else
        PENDIENTES+=("$video")
    fi
done

TOTAL=${#PENDIENTES[@]}

if (( TOTAL == 0 )); then
    printf -v mensaje 'No hay nada pendiente.\n\nLos %d archivos MP4 ya tienen su correspondiente MOV.' "$OMITIDOS"
    zenity --info --title="$TITULO" --width=450 --text="$mensaje"
    exit 0
fi

TEMPORAL="$(mktemp -d)"
ARCHIVO_RESULTADO="$TEMPORAL/resultado"
ARCHIVO_ERRORES="$TEMPORAL/errores"

limpiar() {
    rm -rf -- "$TEMPORAL"
}
trap limpiar EXIT

(
    correctos=0
    errores=0
    indice=0

    echo "0"

    for video in "${PENDIENTES[@]}"; do
        salida="${video%.*}.mov"
        nombre_relativo="${video#"$CARPETA_ORIGEN"/}"
        # Zenity interpreta las líneas que empiezan por # como mensajes.
        nombre_mostrado="${nombre_relativo//$'\n'/ }"

        porcentaje=$((indice * 100 / TOTAL))
        echo "$porcentaje"
        printf '# Convirtiendo %d de %d: %s\n' "$((indice + 1))" "$TOTAL" "$nombre_mostrado"

        if ffmpeg -nostdin -y -loglevel error -i "$video" -c:v copy -c:a pcm_s24le "$salida"; then
            ((correctos += 1))
        else
            ((errores += 1))
            printf '%s\n' "$nombre_relativo" >> "$ARCHIVO_ERRORES"
            # Un archivo incompleto no debe impedir un nuevo intento posterior.
            rm -f -- "$salida"
        fi

        ((indice += 1))
        echo "$((indice * 100 / TOTAL))"
    done

    printf '%s %s\n' "$correctos" "$errores" > "$ARCHIVO_RESULTADO"
) | zenity --progress --title="$TITULO" --width=520 --text="Preparando la conversión…" --percentage=0 --auto-close --no-cancel

if [[ ! -s "$ARCHIVO_RESULTADO" ]]; then
    zenity --error --title="$TITULO" --width=450 --text="La conversión se interrumpió inesperadamente."
    exit 1
fi

read -r CORRECTOS ERRORES < "$ARCHIVO_RESULTADO"

if (( ERRORES == 0 )); then
    printf -v mensaje 'Conversión completada.\n\nConvertidos: %d' "$CORRECTOS"
    if (( OMITIDOS > 0 )); then
        printf -v mensaje '%s\nOmitidos porque ya existían: %d' "$mensaje" "$OMITIDOS"
    fi

    zenity --info --title="$TITULO" --width=450 --text="$mensaje"
else
    lista_errores="$(sed 's/^/• /' "$ARCHIVO_ERRORES")"
    printf -v mensaje 'Conversión terminada con incidencias.\n\nConvertidos: %d\nCon error: %d\nOmitidos: %d\n\nArchivos con error:\n%s' "$CORRECTOS" "$ERRORES" "$OMITIDOS" "$lista_errores"
    zenity --warning --title="$TITULO" --width=560 --text="$mensaje"
    exit 1
fi
