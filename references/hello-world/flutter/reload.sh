#!/usr/bin/env bash
# Prepares the program's hot reload as Flutter's documentation runs it, every file under <out>: a
# copy of the project in <out>/project built once in debug (`flutter build linux --debug`, which
# also fetches the pub packages into <out>/pub-cache), and <out>/reload, which runs it with
# `flutter run` and becomes the tool. `flutter run` does not watch the files: an editor asks it to
# reload on each save, which reload.steps does by the signal that the tool documents (SIGUSR1, to
# the pid that it writes to <out>/flutter.pid). scripts/reloads.sh runs it, then reload.steps.
# Usage, inside `nix develop <uwui>#hello-flutter`: reload.sh <out>
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <out>" >&2
  exit 2
fi
mkdir -p "$1"
out=$(cd "$1" && pwd)
source_dir=$(cd "$(dirname "$0")" && pwd)
export PUB_CACHE="$out/pub-cache"
export HOME="$out/home"
mkdir -p "$HOME"

rm -rf "$out/project"
mkdir -p "$out/project"
cp -r "$source_dir/." "$out/project/"
# Flutter's and Dart's telemetry, which their first run announces, stay off.
flutter --disable-analytics
dart --disable-analytics
(cd "$out/project" && flutter build linux --debug)

# measure.py runs the program with a $HOME of its own and behind a closed proxy: the pub packages
# stay those of this build, and `flutter run` fetches nothing (--no-pub). The tool keeps the home
# whose settings turned its telemetry off. It speaks to the program's VM service on the loopback,
# which the closed proxy must not take.
cat > "$out/reload" <<RUN
#!/usr/bin/env bash
export PUB_CACHE="$out/pub-cache" HOME="$out/home" NO_PROXY=localhost,127.0.0.1 no_proxy=localhost,127.0.0.1
cd "$out/project"
rm -f "$out/flutter.pid"
exec flutter run -d linux --debug --no-pub --pid-file "$out/flutter.pid"
RUN
chmod +x "$out/reload"
