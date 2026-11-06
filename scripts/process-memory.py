#!/usr/bin/env python3
"""Prints a process's memory now: its resident size (VmRSS), and the video memory that the
kernel's DRM says it asked for (drm-total-vram), summed over the GPU files that it opened, each
client of a device once; none where the driver gives no figure.

usage: scripts/process-memory.py <pid>

One line: `resident_mb=<n> video_mb=<n or ->`, in megabytes of 10^6 bytes, as uwui's budgets are
written. The kernel writes sizes in bytes, KiB, MiB or GiB.
"""

import os
import sys

UNITS = {"": 1 / 1024, "KiB": 1, "kB": 1, "MiB": 1024, "GiB": 1024 * 1024}


def kib(value):
    figure, _, unit = value.strip().partition(" ")
    return int(figure) * UNITS[unit.strip()]


def field(text, name):
    for line in text.splitlines():
        if line.startswith(name + ":"):
            return line.split(":", 1)[1].strip()
    return None


def main():
    pid = sys.argv[1]
    with open(f"/proc/{pid}/status", encoding="utf-8") as status:
        resident = kib(field(status.read(), "VmRSS"))
    clients = {}
    for fd in os.listdir(f"/proc/{pid}/fd"):
        try:
            if not os.readlink(f"/proc/{pid}/fd/{fd}").startswith("/dev/dri"):
                continue
            with open(f"/proc/{pid}/fdinfo/{fd}", encoding="utf-8") as info:
                text = info.read()
        except OSError:
            continue
        client, video = field(text, "drm-client-id"), field(text, "drm-total-vram")
        if client is not None and video is not None:
            clients[(field(text, "drm-pdev"), client)] = kib(video)
    video = f"{sum(clients.values()) * 1024 / 1e6:.1f}" if clients else "-"
    print(f"resident_mb={resident * 1024 / 1e6:.1f} video_mb={video}")


if __name__ == "__main__":
    main()
