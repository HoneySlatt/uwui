#!/usr/bin/env bash
# Prepares the program's reload as Iced runs it, every file under <out>: `cargo hot` 0.1.1 installed
# in <out>/tools, a copy of the project in <out>/project built once in debug with Iced's feature
# `hot`, and <out>/reload, which runs it under `cargo hot` and becomes it. scripts/reloads.sh runs
# it, then reload.steps.
# Usage, inside `nix develop <uwui>#hello-iced`: reload.sh <out>
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <out>" >&2
  exit 2
fi
mkdir -p "$1"
out=$(cd "$1" && pwd)
source_dir=$(cd "$(dirname "$0")" && pwd)

if [ ! -x "$out/tools/bin/cargo-hot" ]; then
  CARGO_TARGET_DIR="$out/tools/target" cargo install cargo-hot --version 0.1.1 --locked --root "$out/tools"
fi

rm -rf "$out/project"
mkdir -p "$out/project"
cp -r "$source_dir/." "$out/project/"
# The feature `hot` adds `cargo hot`'s protocol to Cargo.lock, in the copy only.
(cd "$out/project" && cargo build --features iced/hot)

# measure.py runs the program with a $HOME of its own and behind a closed proxy: Cargo keeps the
# home and the crates that this build fetched, and stays offline.
cat > "$out/reload" <<RUN
#!/usr/bin/env bash
export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}" CARGO_NET_OFFLINE=true PATH="$out/tools/bin:\$PATH"
cd "$out/project"
exec cargo hot --features iced/hot
RUN
chmod +x "$out/reload"
