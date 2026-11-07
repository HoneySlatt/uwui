#!/usr/bin/env python3
"""Tests of scripts/measure.py's arithmetic, which scripts/check.sh runs: the figures of frames, the
sizes that the kernel writes, and the `save` step's change, its file, its region and its first frame.

    python3 -I scripts/test_measure.py
"""

import os
import stat
import sys
import tempfile
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


class FirstChange(unittest.TestCase):
    FRAMES = [(10, "a"), (20, "a"), (30, "b"), (40, "c")]

    def test_the_first_frame_that_differs_after_the_save(self):
        self.assertEqual(measure.first_change(self.FRAMES, 15, "a"), (30, "b"))

    def test_a_frame_before_the_save_does_not_count(self):
        self.assertEqual(measure.first_change(self.FRAMES, 30, "a"), (40, "c"))

    def test_frames_that_show_the_same_image_are_not_a_change(self):
        self.assertIsNone(measure.first_change([(10, "a"), (20, "a")], 5, "a"))


class ReplaceOnce(unittest.TestCase):
    def test_the_text_replaced(self):
        self.assertEqual(measure.replace_once('text("Hello, World!")', '"Hello, World!"', '"Hi"'), 'text("Hi")')

    def test_a_text_absent_is_refused(self):
        with self.assertRaises(ValueError):
            measure.replace_once("nothing here", "World", "Reload")

    def test_a_text_there_twice_is_refused(self):
        with self.assertRaises(ValueError):
            measure.replace_once("World, World", "World", "Reload")


class SaveAsAnEditor(unittest.TestCase):
    def test_the_file_is_replaced_whole_and_keeps_its_mode(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "main.rs")
            with open(path, "w", encoding="utf-8") as file:
                file.write("old")
            os.chmod(path, 0o640)
            inode = os.stat(path).st_ino
            measure.save_as_an_editor(path, "new")
            with open(path, encoding="utf-8") as file:
                self.assertEqual(file.read(), "new")
            self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), 0o640)
            self.assertNotEqual(os.stat(path).st_ino, inode, "renamed over, not written in place")
            self.assertEqual(os.listdir(folder), ["main.rs"])


class SaveInPlace(unittest.TestCase):
    def test_the_same_file_written_over_and_shortened(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "main.rs")
            with open(path, "w", encoding="utf-8") as file:
                file.write("a longer text")
            inode = os.stat(path).st_ino
            measure.save_in_place(path, "short")
            with open(path, encoding="utf-8") as file:
                self.assertEqual(file.read(), "short")
            self.assertEqual(os.stat(path).st_ino, inode)


class Saves(unittest.TestCase):
    def file(self, folder, text):
        path = os.path.join(folder, "main.rs")
        with open(path, "w", encoding="utf-8", newline="") as file:
            file.write(text)
        return path

    def test_each_save_returns_its_time_and_keeps_line_endings(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.file(folder, "a\r\nb\r\n")
            for save in (measure.save_as_an_editor, measure.save_in_place):
                before = measure.now_ns()
                saved = save(path, "c\r\nd\r\n")
                self.assertTrue(before <= saved <= measure.now_ns())
                self.assertEqual(measure.read_text(path), "c\r\nd\r\n")

    def test_restore_saves_back_a_changed_file_the_steps_way(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.file(folder, "changed")
            inode = os.stat(path).st_ino
            measure.restore(path, "original", in_place=True)
            self.assertEqual(measure.read_text(path), "original")
            self.assertEqual(os.stat(path).st_ino, inode, "written in place, as the step saved")

    def test_restore_leaves_a_file_already_as_it_was(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.file(folder, "original")
            inode = os.stat(path).st_ino
            measure.restore(path, "original", in_place=False)
            self.assertEqual(os.stat(path).st_ino, inode, "not renamed over")


class RegionInLayout(unittest.TestCase):
    def test_moved_by_the_windows_origin(self):
        self.assertEqual(measure.region_in_layout("10,20,300,40", (100, 50)), "110,70,300,40")


class Views(unittest.TestCase):
    class Sway:
        def ipc(self, *_):
            return {"type": "root", "nodes": [
                {"type": "output", "nodes": [{"type": "workspace", "nodes": [
                    {"type": "con", "id": 7, "pid": 42, "nodes": []},
                    {"type": "con", "id": 5, "pid": None, "nodes": [{"type": "con", "id": 9, "pid": 43}]},
                ], "floating_nodes": [{"type": "floating_con", "id": 11, "pid": 44}]}]}]}

    def test_every_window_with_a_process_found(self):
        self.assertEqual(measure.views(self.Sway()), [(7, 42), (9, 43), (11, 44)])

    def test_a_display_not_sways_has_none(self):
        self.assertIsNone(measure.views(object()))


class CheckSaveSteps(unittest.TestCase):
    def test_a_text_not_in_the_file_stops_before_the_program_starts(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "main.rs")
            with open(path, "w", encoding="utf-8") as file:
                file.write("Hello")
            measure.check_save_steps([f"save body 1 {path} Hello Bye", "still"])
            with self.assertRaises(SystemExit):
                measure.check_save_steps([f"save body 1 {path} World Bye"])

    def test_a_missing_file_stops_it(self):
        with self.assertRaises(SystemExit):
            measure.check_save_steps(["save body 1 /nonexistent/main.rs a b"])

    def test_a_negative_pause_stops_it(self):
        with self.assertRaises(SystemExit):
            measure.save_step("save body 1 main.rs a b --pause -1")


class SaveStep(unittest.TestCase):
    def test_words_in_quotes_and_options(self):
        step = measure.save_step("save body 21 src/main.rs '\"Hello, World!\"' '\"Hello, Reload!\"' "
                                 "--region 0,0,100,50 --in-place --then 'kill -USR1 1' --pause 2 --limit 30")
        self.assertEqual((step.label, step.runs, step.file), ("body", 21, "src/main.rs"))
        self.assertEqual((step.text, step.replacement), ('"Hello, World!"', '"Hello, Reload!"'))
        self.assertEqual((step.region, step.in_place, step.then, step.pause, step.limit),
                         ("0,0,100,50", True, "kill -USR1 1", 2, 30))

    def test_a_region_that_is_not_four_numbers_is_refused(self):
        with self.assertRaises(SystemExit):
            measure.save_step("save body 21 main.rs a b --region 0,0,100")

    def test_a_replacement_that_changes_nothing_is_refused(self):
        with self.assertRaises(SystemExit):
            measure.save_step("save body 21 main.rs same same")

    def test_a_missing_word_is_refused(self):
        with self.assertRaises(SystemExit):
            measure.save_step("save body 21 main.rs only-the-text")


if __name__ == "__main__":
    unittest.main()
