#!/usr/bin/env bash
# Builds the release program with Cargo's default release profile, all build files under <out>.
# Usage, inside `nix develop <uwui>#hello-gpui-kit`: build.sh <out>
# CARGO_TARGET_DIR, when set, is honoured, so that several Rust references share one target folder.
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <out>" >&2
  exit 2
fi
mkdir -p "$1"
out=$(cd "$1" && pwd)
source_dir=$(cd "$(dirname "$0")" && pwd)
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$out/target}"

start=$(date +%s.%N)
cargo build --release --manifest-path "$source_dir/Cargo.toml"
end=$(date +%s.%N)

rm -rf "$out/ship"
mkdir -p "$out/ship"
cp "$CARGO_TARGET_DIR/release/hello-gpui-kit" "$out/ship/"

cat > "$out/run" <<RUN
#!/usr/bin/env bash
exec "$out/ship/hello-gpui-kit" "\$@"
RUN
chmod +x "$out/run"

awk -v s="$start" -v e="$end" 'BEGIN { printf "build wall time: %.1f s\n", e - s }'
