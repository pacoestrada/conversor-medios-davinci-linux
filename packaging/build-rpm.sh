#!/usr/bin/env bash
set -euo pipefail

RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
VERSION="${VERSION:-2.1.0}"
NOMBRE="conversor-mp4-mov-$VERSION"

if ! command -v rpmbuild >/dev/null 2>&1; then
    printf 'No se encuentra rpmbuild. Instala las herramientas de construcción RPM.\n' >&2
    exit 1
fi

TEMPORAL="$(mktemp -d)"
trap 'rm -rf -- "$TEMPORAL"' EXIT
mkdir -p "$TEMPORAL"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS,tmp,rpmdb} "$TEMPORAL/$NOMBRE"

install -Dm755 "$RAIZ/src/conversor-medios" "$TEMPORAL/$NOMBRE/src/conversor-medios"
install -Dm644 "$RAIZ/data/com.pacoestrada.ConversorMp4Mov.desktop" \
    "$TEMPORAL/$NOMBRE/data/com.pacoestrada.ConversorMp4Mov.desktop"
for tamano in 48 64 128 256 512; do
    install -Dm644 \
        "$RAIZ/data/icons/${tamano}x${tamano}/com.pacoestrada.ConversorMp4Mov.png" \
        "$TEMPORAL/$NOMBRE/data/icons/${tamano}x${tamano}/com.pacoestrada.ConversorMp4Mov.png"
done
install -Dm644 "$RAIZ/LICENSE" "$TEMPORAL/$NOMBRE/LICENSE"

tar -C "$TEMPORAL" -czf "$TEMPORAL/SOURCES/$NOMBRE.tar.gz" "$NOMBRE"
sed "s/^Version:.*/Version:        $VERSION/" \
    "$RAIZ/packaging/rpm/conversor-mp4-mov.spec" > "$TEMPORAL/SPECS/conversor-mp4-mov.spec"

rpmbuild \
    --define "_topdir $TEMPORAL" \
    --define "_tmppath $TEMPORAL/tmp" \
    --define "_dbpath $TEMPORAL/rpmdb" \
    -ba "$TEMPORAL/SPECS/conversor-mp4-mov.spec"
mkdir -p "$RAIZ/dist"
find "$TEMPORAL/RPMS" -type f -name '*.rpm' -exec install -m644 {} "$RAIZ/dist/" \;
printf 'Paquete RPM creado en: %s/dist\n' "$RAIZ"
