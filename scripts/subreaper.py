#!/usr/bin/env python3
"""Runs a program that leaves its own process tree, Steam's client, so that scripts/measure.py
still counts all of it, and ends all of it (scripts/market.sh).

    scripts/subreaper.py <command> [<argument>...]

measure.py counts the processes descended from the one it starts, and ends that one's process
group. Steam's launcher starts its client and exits, and the client, orphaned, joins whichever
ancestor the kernel names to adopt orphans: outside the tree, its processor and memory uncounted;
its helpers lead process groups of their own, which outlive the run and meet the next one. This
process declares itself that ancestor (PR_SET_CHILD_SUBREAPER), runs the command as its child and
adopts whatever the command leaves. Sent SIGTERM, it ends every process below it, SIGKILL after
3 s for those that remain, then itself, before measure.py ends the group itself. Its own memory,
some 10 MB, is counted with theirs.
"""

import ctypes
import os
import signal
import subprocess
import sys
import time

PR_SET_CHILD_SUBREAPER = 36


def descendants():
    """Every process below this one, now."""
    children = {}
    for entry in os.listdir("/proc"):
        if entry.isdigit():
            try:
                with open(f"/proc/{entry}/stat", encoding="utf-8") as file:
                    parent = int(file.read().rsplit(")", 1)[1].split()[1])
            except OSError:
                continue
            children.setdefault(parent, []).append(int(entry))
    found, queue = [], list(children.get(os.getpid(), []))
    while queue:
        pid = queue.pop()
        found.append(pid)
        queue.extend(children.get(pid, []))
    return found


def end_all(*_):
    for sent in (signal.SIGTERM, signal.SIGKILL):
        for pid in descendants():
            try:
                os.kill(pid, sent)
            except ProcessLookupError:
                pass
        deadline = time.monotonic() + 3
        while descendants() and time.monotonic() < deadline:
            reap()
            time.sleep(0.1)
    sys.exit(0)


def reap():
    try:
        while os.waitpid(-1, os.WNOHANG)[0]:
            pass
    except ChildProcessError:
        pass


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if ctypes.CDLL(None, use_errno=True).prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0) != 0:
        sys.exit(f"prctl: {os.strerror(ctypes.get_errno())}")
    signal.signal(signal.SIGTERM, end_all)
    subprocess.Popen(sys.argv[1:])
    # Every descendant that the command leaves becomes a child of this process, reaped here.
    while True:
        try:
            os.wait()
        except ChildProcessError:
            return


if __name__ == "__main__":
    main()
