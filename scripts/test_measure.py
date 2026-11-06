#!/usr/bin/env python3
"""Tests of scripts/measure.py's arithmetic, which scripts/check.sh runs: the figures of frames and
the sizes that the kernel writes.

    python3 -I scripts/test_measure.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True
import measure  # noqa: E402

MS = 1_000_000


class FrameFigures(unittest.TestCase):
    def test_steady_frames_miss_nothing(self):
        stamps = [round(index * 4.1667 * MS) for index in range(241)]
        figures = measure.frame_figures(stamps, 0, stamps[-1])
        self.assertEqual(figures["frames"], 241)
        self.assertEqual(figures["missed"], 0)
        self.assertEqual(figures["p99_ms"], 4.17)

    def test_an_interval_of_three_refreshes_misses_two(self):
        stamps = [0, round(4.1667 * MS), round(4 * 4.1667 * MS)]
        figures = measure.frame_figures(stamps, 0, stamps[-1])
        self.assertEqual(figures["missed"], 2)
        self.assertEqual(figures["max_ms"], 12.5)

    def test_a_long_interval_is_a_pause(self):
        figures = measure.frame_figures([0, 500 * MS], 0, 500 * MS)
        self.assertEqual((figures["missed"], figures["pauses"]), (0, 1))

    def test_frames_outside_the_window_are_left_out(self):
        figures = measure.frame_figures([0, 10 * MS, 20 * MS, 30 * MS], 5 * MS, 25 * MS)
        self.assertEqual(figures["frames"], 2)

    def test_nearest_rank(self):
        self.assertEqual(measure.nearest_rank([1, 2, 3, 4], 50), 2)
        self.assertEqual(measure.nearest_rank([1, 2, 3, 4], 99), 4)
        self.assertEqual(measure.nearest_rank([7], 95), 7)


class TicksSince(unittest.TestCase):
    def test_a_thread_that_ends_does_not_take_work_away(self):
        before = {(1, 1): ("main", 100, 0), (1, 2): ("worker", 500, 0)}
        after = {(1, 1): ("main", 103, 0)}
        self.assertEqual(measure.ticks_since(before, after), 3)

    def test_a_new_thread_counts_whole(self):
        before = {(1, 1): ("main", 100, 0)}
        after = {(1, 1): ("main", 100, 0), (2, 2): ("helper", 7, 0)}
        self.assertEqual(measure.ticks_since(before, after), 7)

    def test_a_number_taken_again_is_a_new_thread(self):
        before = {(1, 9): ("old", 400, 0)}
        after = {(1, 9): ("new", 5, 0)}
        self.assertEqual(measure.ticks_since(before, after), 5)


class Kilobytes(unittest.TestCase):
    def test_units(self):
        text = "VmRSS:\t  2048 kB\ndrm-total-vram:\t3 MiB\ndrm-total-gtt:\t4096\n"
        self.assertEqual(measure.kilobytes(text, "VmRSS"), 2048)
        self.assertEqual(measure.kilobytes(text, "drm-total-vram"), 3072)
        self.assertEqual(measure.kilobytes(text, "drm-total-gtt"), 4)

    def test_a_value_without_a_unit_does_not_take_the_next_line(self):
        self.assertEqual(measure.kilobytes("a:\t1024\nb:\t5 kB\n", "a"), 1)

    def test_a_missing_field(self):
        self.assertIsNone(measure.kilobytes("VmRSS:\t1 kB\n", "VmHWM"))


if __name__ == "__main__":
    unittest.main()
