#!/usr/bin/env bash

# Lanzador compatible con las versiones anteriores.
set -euo pipefail
RAIZ="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec bash "$RAIZ/src/conversor-medios" "$@"
