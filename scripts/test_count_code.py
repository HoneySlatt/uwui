#!/usr/bin/env python3
"""Tests of scripts/count_code.py, which scripts/check.sh runs: the lines and the concepts that it
counts.

    python3 -I scripts/test_count_code.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True
import count_code  # noqa: E402

RUST = """//! A screen.
//!
//! The model's concepts:
//! - `View`, what a view's function gives
//! - the rule: a view's function runs once; a closure that reads a signal runs again when it
//!   changes
//!
//! Shared by the four models:
//! - `label`

use uwui::prelude::*;

/// A comment, not counted.
fn hello() -> impl View {
    // Nor this one.

    label("Hello, World!")
}
"""


class Count(unittest.TestCase):
    def test_lines_leave_out_blank_lines_and_comments(self):
        self.assertEqual(count_code.count(RUST, "//")[0], 4)

    def test_each_bullet_is_one_concept_whatever_its_lines(self):
        self.assertEqual(count_code.count(RUST, "//")[1:], (2, 1))

    def test_a_style_sheet_s_comments_start_with_a_hash(self):
        sheet = "# A rule.\n\n[centered]\nselect = {}\n"
        self.assertEqual(count_code.count(sheet, "#"), (2, 0, 0))


if __name__ == "__main__":
    unittest.main()
