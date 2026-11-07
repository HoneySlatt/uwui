#!/usr/bin/env bash
# Prepares the program's reloads as Dioxus's docs run them, every file under <out>: a copy of the
# project in <out>/project, built once in debug by `dx build`, and <out>/reload, which serves it
# with `dx serve --hotpatch` and becomes `dx`. scripts/reloads.sh runs it, then reload.steps.
# Usage, inside `nix develop <uwui>#hello-dioxus`: reload.sh <out>
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
# The text moves into a function of its own, called from `rsx!`: its change is a function's body,
# which only a patch of subsecond's applies, not RSX's reload. The button's label stays a literal of
# `rsx!`, which RSX's reload applies without compiling.
sed -i 's/^\( *\)"Hello, World!"$/\1{greeting()}/' "$out/project/src/main.rs"
grep -q '{greeting()}' "$out/project/src/main.rs"
printf '\nfn greeting() -> String {\n    "Hello, World!".to_string()\n}\n' >> "$out/project/src/main.rs"

(cd "$out/project" && dx build --platform desktop --locked)

# measure.py runs the program with a $HOME of its own and behind a closed proxy: Cargo keeps the
# home and the crates that this build fetched, and stays offline.
cat > "$out/reload" <<RUN
#!/usr/bin/env bash
export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}" CARGO_NET_OFFLINE=true
cd "$out/project"
exec dx serve --platform desktop --hotpatch --interactive false
RUN
chmod +x "$out/reload"
