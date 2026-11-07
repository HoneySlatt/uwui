#!/usr/bin/env bash
# Prepares the program's hot reload as Compose Hot Reload's documentation runs it from the command
# line, every file under <out>: a copy of the project in <out>/project, compiled once, Gradle's
# caches in <out>/gradle-home, and <out>/reload, which runs `./gradlew :desktopApp:hotRun --auto`
# on the JetBrains Runtime and becomes Gradle. In that mode Gradle builds continuously and the app
# reloads each change it compiles. <out>/stop stops the Gradle daemons that the reload left.
# scripts/reloads.sh runs it, then reload.steps, then <out>/stop.
# Usage, inside `nix develop <uwui>#hello-compose`: reload.sh <out>
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "usage: $0 <out>" >&2
  exit 2
fi
mkdir -p "$1"
out=$(cd "$1" && pwd)
source_dir=$(cd "$(dirname "$0")" && pwd)
export GRADLE_USER_HOME="$out/gradle-home"
export HOME="$out/home"
mkdir -p "$HOME"

rm -rf "$out/project"
mkdir -p "$out/project"
cp -r "$source_dir/." "$out/project/"
# Compose Multiplatform bundles the plugin of Compose Hot Reload since 1.10.0: the project is
# unchanged. The hot run started once without a display, so that Gradle compiles the app and
# fetches all that the run needs, the agent of Compose Hot Reload included; the app then stops, as
# it finds no display, and so does the run, which is expected to fail.
(cd "$out/project" && env -u DISPLAY -u WAYLAND_DISPLAY timeout 900 ./gradlew :desktopApp:hotRun \
  -Pcompose.reload.jbr.binary="$COMPOSE_RELOAD_JBR" || true; ./gradlew --stop)

# measure.py runs the program with a $HOME of its own and behind a closed proxy: Gradle keeps the
# caches and the home of this build, and stays offline. The tools' window of Compose Hot Reload
# runs headless: sway would float it over the app's text, and it draws without end.
cat > "$out/reload" <<RUN
#!/usr/bin/env bash
export GRADLE_USER_HOME="$out/gradle-home" HOME="$out/home"
cd "$out/project"
exec ./gradlew --offline :desktopApp:hotRun --auto -Pcompose.reload.jbr.binary="$COMPOSE_RELOAD_JBR" \
  -Pcompose.reload.devToolsHeadless=true
RUN
cat > "$out/stop" <<RUN
#!/usr/bin/env bash
export GRADLE_USER_HOME="$out/gradle-home" HOME="$out/home"
cd "$out/project" && ./gradlew --stop
RUN
chmod +x "$out/reload" "$out/stop"
