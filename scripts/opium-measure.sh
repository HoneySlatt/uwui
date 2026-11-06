#!/usr/bin/env bash
# Measures the floor of the screen of reference "Opium's songs" (docs/ROADMAP.md), with Opium's own
# scripts where it has them: its start to the first frame that it saves, and its memory with the
# table of songs open.
#
#     scripts/opium-measure.sh <opium> <library> <folder>
#
# <opium> is a clone of Opium, its release build made (`nix develop -c cargo build --release -p
# app-desktop` inside it); <library> the fake library of `scripts/fake-music-library.py`; <folder>
# where the profile and the figures go, made if missing. Run it inside Opium's development shell,
# from anywhere: `nix develop <opium> -c scripts/opium-measure.sh ...`. It needs sway and grim,
# which it takes from nixpkgs.
#
# Opium runs in a sway of its own without a screen, one output of 3840 x 2160 at 240 Hz and a scale
# of 1.5, as the screen asks; in the M3E theme, its services off, muted, on a profile in <folder>,
# without a session bus and without a network (`unshare --net`): nothing of the user's is read or
# written. Each run is ended by its own pid. The first start, not counted, indexes the library.
set -euo pipefail
opium=$(realpath "$1") library=$(realpath "$2")
mkdir -p "$3"
folder=$(realpath "$3")
profile=$folder/profile
here=$(cd "$(dirname "$0")" && pwd)

if pgrep -ax opium; then
    echo "an Opium already runs: whose?" >&2
    exit 1
fi
mkdir -p "$profile/config/opium" "$profile/cache" "$profile/data"
cat >"$profile/config/opium/settings.toml" <<EOF
theme = "m3e"
appearance = "stock"
local_folders = ["$library"]
services_off = ["AppleMusic", "SoundCloud", "Navidrome"]
muted = true
EOF
# The screenshot mode opens a page once a playlist exists.
printf '%s\n' '{"lists":{"p1":{"name":{"at":{"at":1,"device":"x"},"value":"T"}}}}' \
    >"$profile/config/opium/playlists.json"

work=$(mktemp -d)
sway_pid=
app_pid=
trap 'for pid in $app_pid $sway_pid; do kill -TERM "$pid" 2>/dev/null || true; done; rm -rf "$work"' EXIT
mkdir -m 700 "$work/runtime"
printf 'output HEADLESS-1 mode --custom 3840x2160@240Hz scale 1.5\ndefault_border none\nxwayland disable\n' \
    >"$work/sway.config"
tools=$(nix build --no-link --print-out-paths nixpkgs#sway nixpkgs#grim | sed 's|$|/bin|' | paste -sd:)
export PATH=$tools:$PATH
env -u WAYLAND_DISPLAY -u DISPLAY -u DBUS_SESSION_BUS_ADDRESS XDG_RUNTIME_DIR="$work/runtime" \
    WLR_BACKENDS=headless WLR_LIBINPUT_NO_DEVICES=1 WLR_RENDERER=gles2 \
    sway -c "$work/sway.config" >"$work/sway.log" 2>&1 &
sway_pid=$!
for _ in $(seq 100); do
    [ -S "$work/runtime/wayland-1" ] && break
    sleep 0.1
done
[ -S "$work/runtime/wayland-1" ] || {
    cat "$work/sway.log" >&2
    exit 1
}
export XDG_RUNTIME_DIR=$work/runtime WAYLAND_DISPLAY=wayland-1
offline=(unshare --user --map-current-user --net)

cd "$opium"
echo "first start, not counted: the library indexed"
"${offline[@]}" scripts/measure/run.sh "$profile" >"$folder/first.log" 2>&1 &
app_pid=$!
for _ in $(seq 300); do
    [ -s "$profile/cache/opium/local/index.json" ] && break
    sleep 1
done
sleep 20
kill -TERM "$app_pid"
wait "$app_pid" || true
app_pid=

echo "start, warm, to the first frame saved, 10 runs"
"${offline[@]}" python3 -I scripts/measure/startup.py "$profile" 10 "$folder/startup.json" | tail -1

echo "memory 30 s after the table of songs opens, 5 runs"
for run in 1 2 3 4 5; do
    "${offline[@]}" scripts/measure/run.sh "$profile" OPIUM_SCREENSHOT="$work/never.png" \
        OPIUM_SCREENSHOT_AFTER=100000 OPIUM_SCREENSHOT_PAGE=page:songs >"$folder/memory-$run.log" 2>&1 &
    app_pid=$!
    sleep 30
    [ "$run" = 1 ] && grim -s 0.33 "$folder/songs.png"
    python3 -I "$here/process-memory.py" "$app_pid" | tee -a "$folder/memory.txt"
    kill -TERM "$app_pid"
    wait "$app_pid" || true
    app_pid=
    sleep 2
done
echo "the table of songs as drawn: $folder/songs.png"
