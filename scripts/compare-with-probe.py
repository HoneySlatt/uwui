#!/usr/bin/env python3
"""Compares what scripts/measure.py read from outside Slatty with what Slatty's probe logged from
inside, in the same runs: scripts/slatty-check.sh runs both, then this.

usage: scripts/compare-with-probe.py <start folder> <scroll folder>

The probe's times are of frames drawn, before the compositor shows them; measure.py's, of frames
shown. A start compares the first frame shown with the probe's first frame drawn, and the first
still frame with the probe's `covers`, the first frame drawn with every cover; the rest, the frames
counted by each; the scroll, the intervals between frames by each, over the probe's own scroll.
"""

import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from measure import frame_figures


def probe(folder, pid, offset):
    """The probe's events of a run, in ns of CLOCK_MONOTONIC: name -> list of times."""
    events = {}
    with open(os.path.join(folder, f"probe-{pid}.log"), encoding="utf-8") as file:
        for line in file:
            stamp, name, *_ = line.split()
            events.setdefault(name, []).append(int(stamp) - offset)
    return events


def spread(values):
    return f"{statistics.median(values):.1f} ({min(values):.1f} to {max(values):.1f})"


def main():
    start_folder, scroll_folder = sys.argv[1], sys.argv[2]
    with open(os.path.join(start_folder, "results.json"), encoding="utf-8") as file:
        results = json.load(file)
    offset = results["realtime_minus_monotonic_ns"]
    first, still = [], []
    print("start, ms after the launch: shown from outside / drawn by the probe")
    for run in results["starts"]:
        events = probe(start_folder, run["pid"], offset)
        drawn_first = (events["frame"][0] - run["launched_ns"]) / 1e6
        drawn_covers = (events["covers"][0] - run["launched_ns"]) / 1e6
        print(f"  first frame {run['first_ms']} / {drawn_first:.1f}; still {run['still_ms']} / covers {drawn_covers:.1f}")
        first.append(run["first_ms"] - drawn_first)
        if run["still_ms"] is not None:
            still.append(run["still_ms"] - drawn_covers)
    print(f"outside minus probe, first frame: {spread(first)} ms; still minus covers: {spread(still)} ms")
    for name in ("steps", "xwayland"):
        rest = results[name]["rest"]
        events = probe(start_folder, results[name]["pid"], offset)
        drawn = sum(rest["start_ns"] <= stamp <= rest["end_ns"] for stamp in events.get("frame", []))
        print(f"rest, {name}: frames {rest['frames']} from outside / {drawn} by the probe")
    with open(os.path.join(scroll_folder, "results.json"), encoding="utf-8") as file:
        scroll = json.load(file)
    events = probe(scroll_folder, scroll["steps"]["pid"], scroll["realtime_minus_monotonic_ns"])
    begin, end = events["begin"][0], events["end"][0]
    with open(os.path.join(scroll_folder, "steps-frames.txt"), encoding="utf-8") as file:
        shown = [int(line) for line in file]
    keys = ("frames", "p50_ms", "p95_ms", "p99_ms", "max_ms", "over_4_17", "over_6_25", "over_16_7", "missed")
    outside = frame_figures(shown, begin, end)
    inside = frame_figures(events["frame"], begin, end)
    print("scroll, 1,200 frames: from outside / by the probe")
    for key in keys:
        print(f"  {key}: {outside.get(key)} / {inside.get(key)}")


if __name__ == "__main__":
    main()
