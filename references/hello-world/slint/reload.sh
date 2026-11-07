#!/usr/bin/env bash
# Prepares the program's live preview as Slint's documentation runs it, every file under <out>: a
# copy of the project in <out>/project built once in debug with the feature `live-preview` and
# SLINT_LIVE_PREVIEW=1, and <out>/reload, which runs it so through `cargo run` and becomes cargo.
# scripts/reloads.sh runs it, then reload.steps.
# Usage, inside `nix develop <uwui>#hello-slint`: reload.sh <out>
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <out>" >&2
  exit 2
fi
mkdir -p "$1"
out=$(cd "$1" && pwd)
source_dir=$(cd "$(dirname "$0")" && pwd)

rm -rf "$out/project"
mkdir -p "$out/project"
cp -r "$source_dir/." "$out/project/"
# The feature adds Slint's interpreter to Cargo.lock, in the copy only.
(cd "$out/project" && SLINT_LIVE_PREVIEW=1 cargo build --features slint/live-preview)

# measure.py runs the program with a $HOME of its own and behind a closed proxy: Cargo keeps the
# home and the crates that this build fetched, and stays offline.
cat > "$out/reload" <<RUN
#!/usr/bin/env bash
export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}" CARGO_NET_OFFLINE=true SLINT_LIVE_PREVIEW=1
cd "$out/project"
exec cargo run --features slint/live-preview
RUN
chmod +x "$out/reload"
