#!/usr/bin/env bash
# Builds the release app as Tauri's docs do (`npm run tauri build`) in a copy of this folder under
# <out>, then writes <out>/run and <out>/ship/. Run it inside `nix develop <uwui>#hello-tauri`.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: build.sh <out>" >&2
  exit 2
fi
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$1"
out=$(cd "$1" && pwd)

# npm's cache and Cargo's build files stay under <out>, like every other build file.
export npm_config_cache="$out/cache/npm"
export npm_config_update_notifier=false
export CARGO_TARGET_DIR="$out/target"

start=$(date +%s%N)
rm -rf "$out/app"
mkdir "$out/app"
cp -a "$here"/{package.json,package-lock.json,src,src-tauri} "$out/app/"
# <out> may lie inside another Cargo workspace: an empty [workspace] table keeps Cargo from
# attaching the copy to it. It changes nothing else.
printf '\n[workspace]\n' >> "$out/app/src-tauri/Cargo.toml"
cd "$out/app"
# `npm ci` installs exactly what package-lock.json freezes; `--locked` makes Cargo refuse to
# change Cargo.lock. The AppImage bundle is left out: Tauri downloads linuxdeploy for it, which
# cannot run on NixOS. The .deb and .rpm bundles are built as by default.
npm ci
npm run tauri build -- --bundles deb,rpm -- --locked
end=$(date +%s%N)

# What a user receives: what the .deb package installs (the binary, its .desktop file and icons).
rm -rf "$out/ship"
cp -a "$CARGO_TARGET_DIR"/release/bundle/deb/tauri-app_*_amd64/data "$out/ship"

cat > "$out/run" <<RUN
#!/bin/sh
exec "$out/ship/usr/bin/tauri-app" "\$@"
RUN
chmod +x "$out/run"

elapsed_ms=$(( (end - start) / 1000000 ))
printf 'build wall time: %d.%03d s\n' $((elapsed_ms / 1000)) $((elapsed_ms % 1000))
