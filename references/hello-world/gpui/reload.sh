#!/usr/bin/env bash
# Prepares the program's reload as GPUI's documentation runs it, every file under <out>: a copy of
# the project in <out>/project built once in debug with GPUI's feature `hot-reload`, and
# <out>/reload, which serves it with `dx serve --hot-patch` and becomes `dx`. scripts/reloads.sh
# runs it, then reload.steps.
# Usage, inside `nix develop <uwui>#hello-gpui`: reload.sh <out>
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
# The feature only switches on code of the same commit of GPUI: Cargo.lock adds its crates.
(cd "$out/project" && dx build --platform linux --features gpui/hot-reload)

# measure.py runs the program with a $HOME of its own and behind a closed proxy: Cargo keeps the
# home and the crates that this build fetched, and stays offline.
cat > "$out/reload" <<RUN
#!/usr/bin/env bash
export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}" CARGO_NET_OFFLINE=true
cd "$out/project"
exec dx serve --platform linux --hot-patch --interactive false --features gpui/hot-reload
RUN
chmod +x "$out/reload"
