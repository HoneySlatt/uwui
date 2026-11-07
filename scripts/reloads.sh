#!/usr/bin/env bash
# Times the reloads of the "Hello, World!" of references/hello-world that can reload, each by
# scripts/measure.py's step `save`, from a change saved to the first frame that shows it
# (docs/measurements.md, "The rivals' reloads").
#
#     scripts/reloads.sh <work> <figures> [<name>...]
#
# <name> is a folder of references/hello-world that holds a `reload.sh`, all of them by default.
# Its `reload.sh`, inside its shell `nix develop .#hello-<name>`, copies it to <work>/<name>/project,
# builds it once in debug and writes <work>/<name>/reload, the command that starts its reload's
# tool. measure.py then runs that command in the copy and plays its `reload.steps`, whose files
# are the copy's; its figures go to <figures>/<name>. A tool whose daemons outlive the program
# (Gradle's) leaves <work>/<name>/stop, run last. Run it on a machine at rest.
set -euo pipefail
cd "$(dirname "$0")/.."
here=$(pwd)
mkdir -p "$1" "$2"
work=$(realpath "$1") figures=$(realpath "$2")
shift 2
names=("$@")
[ ${#names[@]} -gt 0 ] || mapfile -t names < <(find references/hello-world -mindepth 2 -maxdepth 2 -name reload.sh -printf "%h\n" | xargs -n1 basename | sort)
# A tool's daemons stopped even when the series is interrupted.
stop_tool() {
    if [ -n "${current:-}" ] && [ -x "$work/$current/stop" ]; then
        nix develop ".#hello-$current" -c "$work/$current/stop" || true
    fi
}
trap 'stop_tool; exit 130' INT TERM
for name in "${names[@]}"; do
    current=$name
    echo "== $name: prepare"
    if ! nix develop ".#hello-$name" -c "references/hello-world/$name/reload.sh" "$work/$name"; then
        echo "== $name: the preparation failed"
        continue
    fi
    echo "== $name: reload"
    (cd "$work/$name/project" && nix develop "$here#hello-$name" -c python3 -I "$here/scripts/measure.py" \
        --runs 0 --no-warm-up --steps "$here/references/hello-world/$name/reload.steps" "$figures/$name" \
        -- "$work/$name/reload") || echo "== $name: the measure failed"
    stop_tool
    current=
done
