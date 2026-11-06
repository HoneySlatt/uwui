#!/usr/bin/env bash
# Builds the release program as the docs say (`cargo build --release`), every build file under
# <out>, then writes <out>/run and <out>/ship/. Run it inside `nix develop <uwui>#hello-egui`.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: build.sh <out>" >&2
  exit 2
fi
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$1"
out=$(cd "$1" && pwd)

# --locked only refuses to build if Cargo.lock would change: it keeps the frozen versions.
start=$(date +%s%N)
CARGO_TARGET_DIR="$out/target" cargo build --release --locked --manifest-path "$here/Cargo.toml"
end=$(date +%s%N)

# What a user receives: the release binary alone (Cargo has no packaging step of its own).
rm -rf "$out/ship"
mkdir "$out/ship"
cp "$out/target/release/hello-egui" "$out/ship/"

cat > "$out/run" <<RUN
#!/bin/sh
exec "$out/ship/hello-egui" "\$@"
RUN
chmod +x "$out/run"

elapsed_ms=$(( (end - start) / 1000000 ))
printf 'build wall time: %d.%03d s\n' $((elapsed_ms / 1000)) $((elapsed_ms % 1000))
