#!/usr/bin/env bash
# Every automated check of this repository, which CI runs unchanged: the links between Markdown
# files, anchors included; the scripts' syntax; the tests of scripts/measure.py's arithmetic. External links are not checked: they fail for reasons unrelated to the
# change being checked. Run it inside `nix develop`.
set -euo pipefail
cd "$(dirname "$0")/.."

mapfile -t markdown < <(git ls-files --cached --others --exclude-standard '*.md')
lychee --offline --include-fragments --no-progress "${markdown[@]}"

for script in scripts/*.sh; do
    bash -n "$script"
done
python3 -I -c 'import ast, sys; [ast.parse(open(f).read(), f) for f in sys.argv[1:]]' scripts/*.py
python3 -I scripts/test_measure.py
