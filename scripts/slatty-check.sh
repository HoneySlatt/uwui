#!/usr/bin/env bash
# Checks scripts/measure.py against Slatty's probe, which times Slatty's frames from inside
# (docs/measurements.md, "The method checked against Slatty's probe"): Slatty's build with its
# probe runs under scripts/measure.py, both reading the same runs, and
# scripts/compare-with-probe.py prints how far apart they are.
#
#     scripts/slatty-check.sh <slatty> <profile> <folder>
#
# <slatty> is a clone of SlattyLauncher whose `slatty-measure` built the probe's build
# (`cargo run --release -p slatty-measure -- headless <profile>` once, inside it, which also makes
# <profile>, its fake library of 10,000 games); <folder> where the figures go. Run it inside
# Slatty's development shell, which has sway: `nix develop <slatty> -c scripts/slatty-check.sh ...`.
#
# Two series: 10 starts, then the memory and 60 s at rest, under Wayland and Xwayland; then one
# start whose probe scrolls the library 16 logical pixels a frame for 1,200 frames. Slatty runs
# with nothing of the user's, as `slatty-measure` runs it: its home and XDG folders in the profile,
# no session bus, every request through a closed port.
set -euo pipefail
slatty=$(realpath "$1") profile=$(realpath "$2")
mkdir -p "$3"
folder=$(realpath "$3")
here=$(cd "$(dirname "$0")" && pwd)
program=$slatty/target/probe/release/slatty-gui
[ -x "$program" ] || {
    echo "no probe's build in $program: run slatty-measure once" >&2
    exit 1
}

# Slatty, its probe's log named after its pid, which exec keeps.
cat >"$folder/slatty.sh" <<EOF
#!/usr/bin/env bash
exec env -i PATH="\$PATH" LD_LIBRARY_PATH="\${LD_LIBRARY_PATH:-}" LANG="\${LANG:-}" \\
    HOME="$profile/home" XDG_CONFIG_HOME="$profile/home/.config" \\
    XDG_DATA_HOME="$profile/home/.local/share" XDG_CACHE_HOME="$profile/home/.cache" \\
    XDG_STATE_HOME="$profile/home/.local/state" XDG_RUNTIME_DIR="\$XDG_RUNTIME_DIR" \\
    \${WAYLAND_DISPLAY:+WAYLAND_DISPLAY=\$WAYLAND_DISPLAY} DISPLAY="\$DISPLAY" \\
    DBUS_SESSION_BUS_ADDRESS=unix:path=/nonexistent HTTPS_PROXY=http://127.0.0.1:9 \\
    HTTP_PROXY=http://127.0.0.1:9 ALL_PROXY=http://127.0.0.1:9 https_proxy=http://127.0.0.1:9 \\
    http_proxy=http://127.0.0.1:9 all_proxy=http://127.0.0.1:9 \\
    SLATTY_PROBE="\$SLATTY_PROBE_LOGS/probe-\$\$.log" SLATTY_PROBE_STEP="\${SLATTY_PROBE_STEP:-}" \\
    "$program"
EOF
chmod +x "$folder/slatty.sh"

echo "starts, memory and rest"
SLATTY_PROBE_LOGS=$folder/start python3 -I "$here/measure.py" --xwayland "$folder/start" -- "$folder/slatty.sh"
echo "scrolling"
printf 'measure whole 20\n' >"$folder/scroll.steps"
SLATTY_PROBE_LOGS=$folder/scroll SLATTY_PROBE_STEP=scroll python3 -I "$here/measure.py" --runs 0 \
    --steps "$folder/scroll.steps" "$folder/scroll" -- "$folder/slatty.sh"
python3 -I "$here/compare-with-probe.py" "$folder/start" "$folder/scroll"
