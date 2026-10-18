#!/usr/bin/env bash
set -euo pipefail

RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
VERSION="${VERSION:-2.3.1}"
TOPDIR="$(mktemp -d)"
trap 'rm -rf -- "$TOPDIR"' EXIT

for directorio in BUILD BUILDROOT RPMS SOURCES SPECS SRPMS tmp rpmdb; do
    mkdir -p -- "$TOPDIR/$directorio"
done

FUENTE="conversor-mp4-mov-$VERSION"
tar --exclude='./build' --exclude='./dist' --exclude='./.git' \
    --transform="s,^\.,$FUENTE," \
    -czf "$TOPDIR/SOURCES/$FUENTE.tar.gz" -C "$RAIZ" .

sed "s/^Version:.*/Version:        $VERSION/" \
    "$RAIZ/packaging/rpm/conversor-mp4-mov.spec" > "$TOPDIR/SPECS/conversor-mp4-mov.spec"

rpmbuild -ba "$TOPDIR/SPECS/conversor-mp4-mov.spec" \
    --define "_topdir $TOPDIR" \
    --define "_tmppath $TOPDIR/tmp" \
    --define "_dbpath $TOPDIR/rpmdb"

mkdir -p -- "$RAIZ/dist"
find "$TOPDIR/RPMS" -type f -name '*.rpm' -exec cp -f -- {} "$RAIZ/dist/" \;
printf 'Paquete RPM creado en: %s\n' "$RAIZ/dist"
