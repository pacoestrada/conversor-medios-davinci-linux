#!/usr/bin/env bash
set -euo pipefail

RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
VERSION="${VERSION:-2.0.0}"
ARQUITECTURA="all"
NOMBRE="conversor-mp4-mov_${VERSION}_${ARQUITECTURA}"
CONSTRUCCION="$RAIZ/build/$NOMBRE"

rm -rf -- "$CONSTRUCCION"
install -Dm755 "$RAIZ/src/conversor-medios" "$CONSTRUCCION/usr/bin/conversor-medios"
install -Dm644 "$RAIZ/data/com.pacoestrada.ConversorMp4Mov.desktop" "$CONSTRUCCION/usr/share/applications/com.pacoestrada.ConversorMp4Mov.desktop"

ICONO_PNG="$RAIZ/conversor_mp4_a_mov_en_linux.png"
if [[ -f "$ICONO_PNG" ]]; then
    install -Dm644 "$ICONO_PNG" "$CONSTRUCCION/usr/share/icons/hicolor/512x512/apps/com.pacoestrada.ConversorMp4Mov.png"
else
    install -Dm644 "$RAIZ/data/com.pacoestrada.ConversorMp4Mov.svg" "$CONSTRUCCION/usr/share/icons/hicolor/scalable/apps/com.pacoestrada.ConversorMp4Mov.svg"
fi

install -Dm644 "$RAIZ/LICENSE" "$CONSTRUCCION/usr/share/doc/conversor-mp4-mov/copyright"
install -Dm644 "$RAIZ/packaging/debian/control" "$CONSTRUCCION/DEBIAN/control"
sed -i "s/^Version:.*/Version: $VERSION/" "$CONSTRUCCION/DEBIAN/control"
mkdir -p -- "$RAIZ/dist"
dpkg-deb --root-owner-group --build "$CONSTRUCCION" "$RAIZ/dist/$NOMBRE.deb"
printf 'Paquete creado: %s\n' "$RAIZ/dist/$NOMBRE.deb"
