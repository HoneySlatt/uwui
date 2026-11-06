#!/usr/bin/env bash
# Builds the app as Electron's tutorial does (Electron Forge, `npm run package`, the step that
# `npm run make` runs first), in a copy of this folder under <out>, then writes <out>/run and
# <out>/ship/. Run it inside `nix develop <uwui>#hello-electron`.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: build.sh <out>" >&2
  exit 2
fi
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$1"
out=$(cd "$1" && pwd)

# npm's cache and Electron's download (which @electron/get keeps in $XDG_CACHE_HOME/electron) stay
# under <out>, like every other build file.
export npm_config_cache="$out/cache/npm"
export XDG_CACHE_HOME="$out/cache"
export npm_config_update_notifier=false

start=$(date +%s%N)
rm -rf "$out/app"
mkdir "$out/app"
cp "$here"/{package.json,package-lock.json,forge.config.js,main.js,preload.js,renderer.js,index.html,styles.css} "$out/app/"
cd "$out/app"
# `npm ci` installs exactly what package-lock.json freezes.
npm ci
npm run package
end=$(date +%s%N)

# What a user receives: Forge's packaged app folder (Electron, its libraries and the app's asar).
rm -rf "$out/ship"
cp -a "$out/app/out/my-electron-app-linux-x64" "$out/ship"

cat > "$out/run" <<RUN
#!/bin/sh
exec "$out/ship/my-electron-app" "\$@"
RUN
chmod +x "$out/run"

elapsed_ms=$(( (end - start) / 1000000 ))
printf 'build wall time: %d.%03d s\n' $((elapsed_ms / 1000)) $((elapsed_ms % 1000))
