#!/usr/bin/env python3
"""Writes the file of the screen of reference "Zed's file" (docs/ROADMAP.md): 100,000 lines of
Rust, for Zed to scroll; the same bytes at every run of one version of Python, whose random
numbers a later version may draw otherwise (docs/measurements.md names the file's SHA-256).

    scripts/long-file.py <file> [<lines>]

The file is made of modules of plausible code, a struct, its methods and their comments, so that
its lines vary in length and in what a highlighter colours, as a real source does; it is not meant
to compile. Its lines end with `\\n`; the last line is a closing brace.
"""

import random
import sys

WORDS = ["frame", "glyph", "layout", "cache", "atlas", "scroll", "theme", "style", "node", "tree",
         "event", "pointer", "window", "surface", "buffer", "texture", "shader", "font", "line", "row",
         "column", "cell", "list", "item", "range", "offset", "size", "width", "height", "color"]
TYPES = ["u32", "f32", "usize", "bool", "String", "Vec<u8>", "Option<f32>", "Rect", "Point"]


def module(chance, number):
    """One module: a struct of a few fields and an impl of a few methods."""
    name = "".join(word.capitalize() for word in chance.sample(WORDS, 2))
    fields = chance.sample(WORDS, chance.randint(3, 7))
    lines = [f"/// The {' '.join(chance.sample(WORDS, 3))} of module {number}, kept between frames.",
             "#[derive(Debug, Clone, Default)]", f"pub struct {name}{number} {{"]
    lines += [f"    pub {field}: {chance.choice(TYPES)}," for field in fields]
    lines += ["}", "", f"impl {name}{number} {{"]
    for method in chance.sample(WORDS, chance.randint(3, 6)):
        lines.append(f"    // Each {chance.choice(WORDS)} is {chance.choice(['measured', 'drawn', 'kept', 'freed'])}"
                     f" once per {chance.choice(WORDS)}, never twice.")
        lines.append(f"    pub fn {method}_{chance.choice(WORDS)}(&mut self, {chance.choice(WORDS)}: "
                     f"{chance.choice(TYPES)}) -> usize {{")
        for _ in range(chance.randint(2, 8)):
            left, right = chance.sample(fields, 2) if len(fields) > 1 else (fields[0], fields[0])
            lines.append(chance.choice([
                f"        let {chance.choice(WORDS)} = self.{left}.clone();",
                f"        if self.{left} == self.{right} {{ return {chance.randint(0, 4096)}; }}",
                f"        let total = {chance.randint(1, 999)} * {chance.randint(1, 999)} + 0x{chance.randint(0, 65535):04x};",
                f"        println!(\"{{}} {chance.choice(WORDS)} at {{:?}}\", \"{chance.choice(WORDS)}\", self.{left});",
                f"        for index in 0..{chance.randint(2, 64)} {{ let _ = index; }}",
            ]))
        lines.append(f"        {chance.randint(0, 1 << 20)}")
        lines.append("    }")
    lines += ["}", ""]
    return lines


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    wanted = int(sys.argv[2]) if len(sys.argv) == 3 else 100_000
    chance = random.Random(2026_11_06)
    lines = []
    number = 0
    while len(lines) < wanted - 1:
        lines += module(chance, number)
        number += 1
    lines = lines[:wanted - 1] + ["}"]
    with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as file:
        file.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
