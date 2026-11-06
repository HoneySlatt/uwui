#!/usr/bin/env bash
# Builds the desktop app's distributable (`./gradlew :desktopApp:createDistributable`, Compose's
# own packaging: the app image, with a Java runtime), all build files under <out>.
# Usage, inside `nix develop <uwui>#hello-compose`: build.sh <out>
# Gradle writes .gradle/, .kotlin/ and build/ into the project, so the project is built from a copy
# under <out>. Gradle's caches (GRADLE_USER_HOME) and what the Gradle and Kotlin daemons write into
# the home folder go to <out> too.
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

start=$(date +%s.%N)
(cd "$out/project" && ./gradlew :desktopApp:createDistributable)
end=$(date +%s.%N)
# The daemons outlive the build otherwise.
(cd "$out/project" && ./gradlew --stop)

rm -rf "$out/ship"
cp -r "$out/project/desktopApp/build/compose/binaries/main/app/org.example.project" "$out/ship"

cat > "$out/run" <<RUN
#!/usr/bin/env bash
exec "$out/ship/bin/org.example.project" "\$@"
RUN
chmod +x "$out/run"

awk -v s="$start" -v e="$end" 'BEGIN { printf "build wall time: %.1f s\n", e - s }'
