#!/usr/bin/env bash
# Builds the "Hello, World!" of references/hello-world, then measures each by scripts/measure.py
# (docs/measurements.md): 10 starts, the memory and 60 s at rest under Wayland, the same under
# Xwayland, and the GPU's power with sway alone before and after.
#
#     scripts/hello-world.sh <builds> <figures> [<name>...]
#
# <name> is a folder of references/hello-world, all of them by default. Each is built by its
# `build.sh` inside its shell, `nix develop .#hello-<name>`, into <builds>/<name>, unless
# <builds>/<name>/run exists; its figures go to <figures>/<name>. Run it on a machine at rest.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p "$1" "$2"
builds=$(realpath "$1") figures=$(realpath "$2")
shift 2
names=("$@")
[ ${#names[@]} -gt 0 ] || mapfile -t names < <(find references/hello-world -mindepth 1 -maxdepth 1 -type d -printf "%f\n" | sort)
for name in "${names[@]}"; do
    if [ ! -x "$builds/$name/run" ]; then
        echo "== $name: build"
        nix develop ".#hello-$name" -c "references/hello-world/$name/build.sh" "$builds/$name"
    fi
    echo "== $name: measure"
    nix develop ".#hello-$name" -c python3 -I scripts/measure.py --xwayland --power \
        --steps scripts/hello-world.steps "$figures/$name" -- "$builds/$name/run"
done
