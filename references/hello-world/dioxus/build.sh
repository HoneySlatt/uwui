#!/usr/bin/env bash
# Builds the release program as Dioxus's CLI does (`dx build --release --platform desktop`), every
# build file under <out>, then writes <out>/run and <out>/ship/. Run it inside
# `nix develop <uwui>#hello-dioxus`.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: build.sh <out>" >&2
  exit 2
fi
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$1"
out=$(cd "$1" && pwd)

# `dx` writes into the project's target/ folder: the project is built from a copy under <out>.
rm -rf "$out/project"
mkdir -p "$out/project"
cp -r "$here/." "$out/project/"
start=$(date +%s%N)
(cd "$out/project" && dx build --release --platform desktop --locked)
end=$(date +%s%N)

# What a user receives: the application folder that `dx` assembles, its binary and its assets.
rm -rf "$out/ship"
cp -r "$out/project/target/dx/hello-dioxus/release/linux/app" "$out/ship"

cat > "$out/run" <<RUN
#!/bin/sh
exec "$out/ship/hello-dioxus" "\$@"
RUN
chmod +x "$out/run"

elapsed_ms=$(( (end - start) / 1000000 ))
printf 'build wall time: %d.%03d s\n' $((elapsed_ms / 1000)) $((elapsed_ms % 1000))
