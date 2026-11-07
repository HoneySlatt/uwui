#!/usr/bin/env bash
# Prepares the program's reload as Makepad runs it, every file under <out>: a copy of the project in
# <out>/project built once in debug, and <out>/reload, which runs it with `--hot` through
# `cargo run` and becomes cargo. With `--hot`, Makepad watches the files of its `script_mod!`
# blocks and evaluates a changed block again, without compiling. scripts/reloads.sh runs it, then
# reload.steps.
# Usage, inside `nix develop <uwui>#hello-makepad`: reload.sh <out>
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
(cd "$out/project" && cargo build --locked)

# measure.py runs the program with a $HOME of its own and behind a closed proxy: Cargo keeps the
# home and the crates that this build fetched, and stays offline.
cat > "$out/reload" <<RUN
#!/usr/bin/env bash
export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}" CARGO_NET_OFFLINE=true
cd "$out/project"
exec cargo run --locked -- --hot
RUN
chmod +x "$out/reload"
