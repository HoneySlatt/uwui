#!/usr/bin/env bash
# Builds the release bundle as Flutter's docs say (`flutter build linux --release`), all build files
# under <out>.
# Usage, inside `nix develop <uwui>#hello-flutter`: build.sh <out>
# Flutter writes .dart_tool/ and build/ into the project, so the project is built from a copy under
# <out>. Pub's cache and the tool's settings and telemetry files, which Flutter writes into the home
# folder, go to <out> too.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <out>" >&2
  exit 2
fi
mkdir -p "$1"
out=$(cd "$1" && pwd)
source_dir=$(cd "$(dirname "$0")" && pwd)
export PUB_CACHE="$out/pub-cache"
export HOME="$out/home"
mkdir -p "$HOME"

rm -rf "$out/project"
mkdir -p "$out/project"
cp -r "$source_dir/." "$out/project/"

start=$(date +%s.%N)
(cd "$out/project" && flutter build linux --release)
end=$(date +%s.%N)

rm -rf "$out/ship"
cp -r "$out/project/build/linux/x64/release/bundle" "$out/ship"

cat > "$out/run" <<RUN
#!/usr/bin/env bash
exec "$out/ship/hello" "\$@"
RUN
chmod +x "$out/run"

awk -v s="$start" -v e="$end" 'BEGIN { printf "build wall time: %.1f s\n", e - s }'
