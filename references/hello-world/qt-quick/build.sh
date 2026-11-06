#!/usr/bin/env bash
# Builds the release program with CMake as Qt's docs and Qt Creator do (Ninja, CMAKE_BUILD_TYPE
# Release), all build files under <out>.
# Usage, inside `nix develop <uwui>#hello-qt-quick`: build.sh <out>
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <out>" >&2
  exit 2
fi
mkdir -p "$1"
out=$(cd "$1" && pwd)
source_dir=$(cd "$(dirname "$0")" && pwd)

start=$(date +%s.%N)
cmake -S "$source_dir" -B "$out/build" -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build "$out/build"
end=$(date +%s.%N)

rm -rf "$out/ship"
mkdir -p "$out/ship"
cp "$out/build/apphello" "$out/ship/"

cat > "$out/run" <<RUN
#!/usr/bin/env bash
exec "$out/ship/apphello" "\$@"
RUN
chmod +x "$out/run"

awk -v s="$start" -v e="$end" 'BEGIN { printf "build wall time: %.1f s\n", e - s }'
