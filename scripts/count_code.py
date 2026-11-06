#!/usr/bin/env python3
"""Counts what an author writes and learns in each file that it is given: its lines, without blank
lines and comments; and, in a file of Rust, the concepts that its header lists, one bullet each,
under "The model's concepts:" and "Shared by the four models:" (docs/ideal-code/README.md). A
style sheet's comments start with `#`. It reads the files as they are: run `rustfmt --check` on
those of Rust first.

    python3 -I scripts/count_code.py docs/ideal-code/*/*.rs docs/ideal-code/sheets/*.style

Prints one line for each file: its path, its lines, the model's concepts, the shared concepts.
"""

import sys

MODEL = "The model's concepts:"
SHARED = "Shared by the four models:"


def count(text, comment):
    """The lines of code in `text`, whose comments start with `comment`, and the bullets under
    each heading of its header."""
    lines = 0
    bullets = {MODEL: 0, SHARED: 0}
    heading = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("//!"):
            words = stripped[3:].strip()
            if words in bullets:
                heading = words
            elif words.startswith("- ") and heading:
                bullets[heading] += 1
            elif not words:
                heading = None
            continue
        if stripped and not stripped.startswith(comment):
            lines += 1
    return lines, bullets[MODEL], bullets[SHARED]


def main(paths):
    if not paths:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    for path in paths:
        with open(path, encoding="utf-8") as file:
            comment = "#" if path.endswith(".style") else "//"
            lines, model, shared = count(file.read(), comment)
        print(f"{path}\t{lines}\t{model}\t{shared}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
