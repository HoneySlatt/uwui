#!/usr/bin/env bash
# Measures a rival of the screens of reference (docs/ROADMAP.md), those that SlimeEngine's ADR-0201
# kept, by scripts/measure.py, with the steps of scripts/market/<application>.steps: 10 starts, then
# its screen opened, at rest, scrolled and closed (docs/measurements.md).
#
#     scripts/market.sh <application> <folder> [<data>]
#
# <application>, and the <data> it needs:
#
#     zed                          the file of scripts/long-file.py, made here
#     nautilus, gthumb             <data>: a folder of images, Slatty's 10,000 covers, whose
#                                  thumbnails scripts/thumbnails.py makes
#     spotify, cider, steam        the owner's own profile, copied once into <folder>
#
# Each application is built from uwui's flake.lock (`nix build .#market.<package>`), at the version
# its figures name. Its profile is <folder>/home, kept from one run to the next. Run it from
# anywhere, on a machine at rest, with python3 on the PATH; it takes sway and grim from the nixpkgs
# that uwui's flake.lock pins.
#
# Every application gets a session bus of its own, which some refuse to start without, with no
# service to start; the bus and what it started stop at the end. Steam runs under
# scripts/subreaper.py, which keeps its client, that leaves its launcher's tree, among the
# processes measured. The open applications run without a network, as measure.py has it; the
# closed ones reach theirs, behind no proxy. Spotify, Cider and Steam run on a copy of the owner's
# profile, made once: logged in, but never on the owner's files; Steam's copy has no game and no
# library but its own. Spotify and Cider play a song, muted in the player, through the session's
# sound server, which they reach though their runtime folder is sway's.
set -euo pipefail
[ $# -ge 2 ] || {
    sed -n '2,/^set -e/p' "$0" | sed '$d; s/^# \{0,1\}//' >&2
    exit 2
}
application=$1
mkdir -p "$2"
folder=$(realpath "$2")
data=${3:+$(realpath "$3")}
here=$(cd "$(dirname "$0")" && pwd)
home=$folder/home

# A rival's package, built from flake.lock's input `market`: assigned to a variable, so that a
# failed build stops the script.
market() { nix build --quiet --no-link --print-out-paths "$here/..#market.$1^out"; }
tools=$(nix build --no-link --print-out-paths --inputs-from "$here/.." nixpkgs#sway nixpkgs#grim |
    sed 's|$|/bin|' | paste -sd:)
export PATH=$tools:$PATH

# The XDG folders of a user: gThumb shows nothing without them.
mkdir -p "$home/.config" "$home/.cache" "$home/.local/share" "$home/.local/state" "$home/Pictures"
if [ ! -e "$home/.config/user-dirs.dirs" ]; then
    for name in DESKTOP DOWNLOAD DOCUMENTS MUSIC PICTURES VIDEOS PUBLICSHARE TEMPLATES; do
        echo "XDG_${name}_DIR=\"\$HOME/Pictures\""
    done >"$home/.config/user-dirs.dirs"
fi
profile=(HOME="$home" XDG_CONFIG_HOME="$home/.config" XDG_CACHE_HOME="$home/.cache"
    XDG_DATA_HOME="$home/.local/share" XDG_STATE_HOME="$home/.local/state")
network=(-u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy)
sound=PULSE_SERVER="unix:${XDG_RUNTIME_DIR:-/nonexistent}/pulse/native"

# The session bus, started with the profile and no display. Its configuration is its own: the
# system's would let it start every service the system lists, a keyring among them, for which
# Chromium waits 25 s; this one starts none.
cat >"$folder/bus.conf" <<END
<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-Bus Bus Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">
<busconfig>
  <type>session</type>
  <listen>unix:tmpdir=/tmp</listen>
  <auth>EXTERNAL</auth>
  <policy context="default">
    <allow send_destination="*" eavesdrop="true"/>
    <allow eavesdrop="true"/>
    <allow own="*"/>
  </policy>
</busconfig>
END
dbus=$(market dbus)
bus_output=$(env -u WAYLAND_DISPLAY -u DISPLAY -u DBUS_SESSION_BUS_ADDRESS "${profile[@]}" \
    "$dbus/bin/dbus-daemon" --config-file="$folder/bus.conf" --fork --print-address=1 \
    --print-pid=1)
bus=$(sed -n 1p <<<"$bus_output")
bus_pid=$(sed -n 2p <<<"$bus_output")
stop_bus() {
    # What the bus started holds its address in its environment.
    for environ in /proc/[0-9]*/environ; do
        if grep -qzxF "DBUS_SESSION_BUS_ADDRESS=$bus" "$environ" 2>/dev/null; then
            pid=${environ#/proc/}
            kill -TERM "${pid%/environ}" 2>/dev/null || true
        fi
    done
    # The bus leads a session of its own, which holds the helpers it forked.
    kill -TERM -- "-$bus_pid" 2>/dev/null || true
}
trap stop_bus EXIT
run=(env "${profile[@]}" DBUS_SESSION_BUS_ADDRESS="$bus")

measure() {
    python3 -I "$here/measure.py" --steps "$here/market/$application.steps" "$@"
}
# Copies the owner's folder <from> to <to> in the profile, once, whole or not at all.
copy_once() {
    if [ ! -e "$2" ]; then
        mkdir -p "$(dirname "$2")"
        rm -rf "$2.part"
        cp -a "$1" "$2.part"
        mv "$2.part" "$2"
    fi
}

case $application in
zed)
    app=$(market zed-editor)
    file=$(mktemp -d)
    trap 'stop_bus; rm -rf "$file"' EXIT
    python3 -I "$here/long-file.py" "$file/long.rs"
    mkdir -p "$home/.config/zed"
    # No language server, which would be fetched from the network; no telemetry, no update; the
    # file's folder trusted, else a dialog stands over the file.
    cat >"$home/.config/zed/settings.json" <<EOF
{
  "telemetry": { "diagnostics": false, "metrics": false },
  "auto_update": false,
  "enable_language_server": false,
  "session": { "trust_all_worktrees": true }
}
EOF
    # The application itself, not `zeditor`, the command line that starts it as another process.
    # A start waits 5 s at most for stillness, not 60: Zed stands still within 1.3 s, and an
    # editor whose caret blinked never would.
    measure --still-limit 5 "$folder/figures" -- "${run[@]}" "$app/libexec/zed-editor" "$file/long.rs"
    ;;
nautilus | gthumb)
    [ -d "$data" ] || { echo "a folder of images is needed" >&2; exit 2; }
    if [ "$application" = nautilus ]; then
        app=$(market nautilus)
        command=("${run[@]}" "$app/bin/nautilus" --new-window "$data")
    else
        app=$(market gthumb)
        command=("${run[@]}" "$app/bin/gthumb" "$data")
    fi
    # Its thumbnails, made beforehand by the thumbnailer it calls, at the size it asks at its
    # default zoom, as after a user's first visit to the folder.
    size=x-large
    [ "$application" = gthumb ] && size=large
    gdk_pixbuf=$(market gdk-pixbuf)
    python3 -I "$here/thumbnails.py" "$gdk_pixbuf/bin/gdk-pixbuf-thumbnailer" "$size" "$data" \
        "$home/.cache"
    measure "$folder/figures" -- "${command[@]}"
    ;;
spotify)
    app=$(market spotify)
    copy_once ~/.config/spotify "$home/.config/spotify"
    copy_once ~/.cache/spotify "$home/.cache/spotify"
    # The copy's storage, not the owner's.
    sed -i "s|^storage.last-location=.*|storage.last-location=\"$home/.cache/spotify/Storage\"|" \
        "$home/.config/spotify/prefs"
    # Spotify starts on a public playlist of 9,998 songs: the owner's are of 13 at most.
    measure "$folder/figures" -- env "${network[@]}" "${run[@]}" "$sound" NIXOS_OZONE_WL=1 \
        "$app/bin/spotify" --uri=spotify:playlist:1G8IpkZKobrIlXcVPoSIuf
    ;;
cider)
    app=$(market cider-2)
    copy_once ~/.config/sh.cider.genten "$home/.config/sh.cider.genten"
    widevine=$home/.config/sh.cider.genten/WidevineCdm/latest-component-updated-widevine-cdm
    [ -e "$widevine" ] && sed -i "s|$HOME/.config/|$home/.config/|g" "$widevine"
    measure "$folder/figures" -- env "${network[@]}" "${run[@]}" "$sound" NIXOS_OZONE_WL=1 \
        "$app/bin/cider-2"
    ;;
steam)
    app=$(market steam)
    steam=$home/.local/share/Steam
    # The copy is marked made only once whole: one left half made, whose paths may still lead to
    # the owner's folders, is made again.
    if [ ! -e "$home/.steam-copied" ]; then
        rm -rf "$steam" "$home/.steam"
        # The client and the owner's login, without the games, their tools and the logs.
        mkdir -p "$home/.local/share" "$home/.steam"
        tar -C ~/.local/share --exclude=Steam/steamapps --exclude=Steam/compatibilitytools.d \
            --exclude=Steam/logs --exclude=Steam/millennium -cf - Steam | tar -C "$home/.local/share" -xf -
        mkdir -p "$steam/steamapps"
        # One library, the copy's own, empty: Steam never reaches the owner's games.
        printf '"libraryfolders"\n{\n\t"0"\n\t{\n\t\t"path"\t\t"%s"\n\t\t"label"\t\t""\n\t\t"contentid"\t\t"0"\n\t\t"totalsize"\t\t"0"\n\t\t"apps"\n\t\t{\n\t\t}\n\t}\n}\n' \
            "$steam" | tee "$steam/config/libraryfolders.vdf" >"$steam/steamapps/libraryfolders.vdf"
        sed -i "s|$HOME/.local/share/|$home/.local/share/|g" "$steam/config/htmlcache/Default/Preferences"
        sed -i 's|"/[^"]*"|""|g' "$steam/config/DialogConfig.vdf"
        cp ~/.steam/registry.vdf "$home/.steam/"
        sed -i "s|$HOME/.local/share/Steam|$steam|g" "$home/.steam/registry.vdf"
        for link in bin32:ubuntu12_32 bin64:ubuntu12_64 root: steam: sdk32:linux32 sdk64:linux64; do
            ln -sfn "$steam/${link#*:}" "$home/.steam/${link%%:*}"
        done
        ln -sfn bin32 "$home/.steam/bin"
        : >"$home/.steam-copied"
    fi
    measure "$folder/figures" -- env "${network[@]}" "${run[@]}" python3 -I "$here/subreaper.py" \
        "$app/bin/steam"
    ;;
*)
    echo "unknown application: $application" >&2
    exit 2
    ;;
esac
