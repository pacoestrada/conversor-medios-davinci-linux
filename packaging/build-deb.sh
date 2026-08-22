#!/usr/bin/env bash
set -euo pipefail

RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
VERSION="${VERSION:-2.0.1}"
ARQUITECTURA="all"
NOMBRE="conversor-mp4-mov_${VERSION}_${ARQUITECTURA}"
CONSTRUCCION="$RAIZ/build/$NOMBRE"

rm -rf -- "$CONSTRUCCION"
install -Dm755 "$RAIZ/src/conversor-medios" "$CONSTRUCCION/usr/bin/conversor-medios"
install -Dm644 "$RAIZ/data/com.pacoestrada.ConversorMp4Mov.desktop" "$CONSTRUCCION/usr/share/applications/com.pacoestrada.ConversorMp4Mov.desktop"

for tamano in 48 64 128 256 512; do
    install -Dm644 \
        "$RAIZ/data/icons/${tamano}x${tamano}/com.pacoestrada.ConversorMp4Mov.png" \
        "$CONSTRUCCION/usr/share/icons/hicolor/${tamano}x${tamano}/apps/com.pacoestrada.ConversorMp4Mov.png"
done

install -Dm644 "$RAIZ/LICENSE" "$CONSTRUCCION/usr/share/doc/conversor-mp4-mov/copyright"
install -Dm644 "$RAIZ/packaging/debian/control" "$CONSTRUCCION/DEBIAN/control"
sed -i "s/^Version:.*/Version: $VERSION/" "$CONSTRUCCION/DEBIAN/control"
mkdir -p -- "$RAIZ/dist"
dpkg-deb --root-owner-group --build "$CONSTRUCCION" "$RAIZ/dist/$NOMBRE.deb"
printf 'Paquete creado: %s\n' "$RAIZ/dist/$NOMBRE.deb"
