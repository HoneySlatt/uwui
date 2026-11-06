#!/usr/bin/env bash
# Measures the floor of the screen of reference "Opium's songs" (docs/ROADMAP.md): its start to the
# first frame that it saves, with Opium's own script; then from outside, by scripts/measure.py, its
# start to its first frame shown, and the steps of scripts/opium-songs.steps: the table of songs
# opened by a click, its memory, its rest, scrolled from end to end, closed, and a song playing.
#
#     scripts/opium-measure.sh <opium> <library> <folder>
#
# <opium> is a clone of Opium, its release build made (`nix develop -c cargo build --release -p
# app-desktop` inside it); <library> the fake library of `scripts/fake-music-library.py`; <folder>
# where the profile and the figures go, made if missing. Run it inside Opium's development shell,
# from anywhere: `nix develop <opium> -c scripts/opium-measure.sh ...`. It needs sway and grim,
# which it takes from the nixpkgs that uwui's flake.lock pins.
#
# Opium runs in a sway of its own without a screen, one output of 3840 x 2160 at 240 Hz and a scale
# of 1.5, as the screen asks; in the M3E theme, its services off, muted, on a profile in <folder>,
# without a session bus and without a network (`unshare --net`): nothing of the user's is read or
# written. Its player reaches the session's PipeWire, if one runs, to play a song: muted, and the
# fake library's songs are silence. Each run is ended by its own pid. The first start, not
# counted, indexes the library. GPU figures need a machine at rest: no game, no video playing.
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
# sway runs in a process group of its own: nixpkgs' sway is a wrapper that starts it under
# dbus-run-session, and both must stop with it.
trap '[ -n "$app_pid" ] && kill -TERM "$app_pid" 2>/dev/null; [ -n "$sway_pid" ] && kill -TERM -- "-$sway_pid" 2>/dev/null; rm -rf "$work"' EXIT
mkdir -m 700 "$work/runtime"
printf 'output HEADLESS-1 mode --custom 3840x2160@240Hz scale 1.5\ndefault_border none\nxwayland disable\n' \
    >"$work/sway.config"
pipewire=${XDG_RUNTIME_DIR:-/nonexistent}/pipewire-0
tools=$(nix build --no-link --print-out-paths --inputs-from "$here/.." nixpkgs#sway nixpkgs#grim |
    sed 's|$|/bin|' | paste -sd:)
export PATH=$tools:$PATH
env -u WAYLAND_DISPLAY -u DISPLAY -u DBUS_SESSION_BUS_ADDRESS XDG_RUNTIME_DIR="$work/runtime" \
    WLR_BACKENDS=headless WLR_LIBINPUT_NO_DEVICES=1 WLR_RENDERER=gles2 \
    setsid sway -c "$work/sway.config" >"$work/sway.log" 2>&1 &
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

echo "from outside: start to the first frame shown, 10 runs; then the table's steps"
python3 -I "$here/measure.py" --runs 10 --still-limit 3 --power --steps "$here/opium-songs.steps" \
    "$folder/outside" -- env PIPEWIRE_REMOTE="$pipewire" "${offline[@]}" \
    "$opium/scripts/measure/run.sh" "$profile"
