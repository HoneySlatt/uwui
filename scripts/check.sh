#!/usr/bin/env bash
# Every automated check of this repository, which CI runs unchanged: the links between Markdown
# files, anchors included. External links are not checked: they fail for reasons unrelated to the
# change being checked. Run it inside `nix develop`.
set -euo pipefail
cd "$(dirname "$0")/.."

mapfile -t markdown < <(git ls-files --cached --others --exclude-standard '*.md')
lychee --offline --include-fragments --no-progress "${markdown[@]}"
