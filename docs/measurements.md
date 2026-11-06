# Measurements

What the programs of uwui's pilots and their rivals measured, on the
[screens of reference](ROADMAP.md#screens-of-reference): one section per measurement, newest last.
A section names the machine, the program's version, the command, and the figures with their
spread. Sizes are in MB of 10⁶ bytes, the unit of uwui's budgets. A figure compares with another only on the same machine, screen and data.

The programs run on test data and test profiles, built from clones of their repositories: nothing
of their users' is read or written, but on the owner's accounts where a section says so.

Update this file when a program or a rival is measured.

## Slatty's library, with Iced (2026-11-06)

The floor of the screen "Slatty's library": Slatty with its interface on Iced 0.14, measured again
by its own `slatty-measure`, as on 2026-11-05, for SlimeEngine's milestone M6d.0a. How it measures
is in [Slatty's `testing.md`](https://github.com/HoneySlatt/SlattyLauncher/blob/main/docs/testing.md#the-application-at-10000-games).

- Machine: AMD Ryzen 7 5800X, 32 GB, Radeon RX 6900 XT on RADV, NVMe, Linux 7.3.
- Build: release, Slatty at `4463d00`, from a clone.
- Command: `slatty-measure headless`, then `slatty-measure desktop`, 10 runs a series.
- Each figure: the median of the runs, and their range.

In sway 1.12 without a screen, one output of 3840 × 2160 at 240 Hz, scale 1.5, the window tiled at
2556 × 1413 (3834 × 2120 pixels):

| | Median (range) |
|---|---|
| Start, warm: library in the state / shown / every cover shown | 68 (65–73) / 527 (515–534) / 666 (648–677) ms |
| Start, cold: the same | 148 (144–164) / 606 (599–628) / 731 (724–757) ms |
| Memory, every cover shown: resident / video | 154 (154–155) / 301 (301–301) MB |
| Memory after scrolling the whole grid: resident / video | 155 (155–156) / 443 (443–443) MB |
| Memory after 200 game pages with key art: resident / video | 224 (220–225) / 387 (387–388) MB |
| At rest 60 s, Wayland: frames / CPU ticks / wake-ups | 0 (0–0) / 0 (0–1) / 120 (120–120) |
| At rest 60 s, Xwayland: the same | 0 (0–0) / 0 (0–1) / 120 (120–122) |

On the owner's display, under Umbriel, 3840 × 2160 at 240 Hz, scale 1.5, variable refresh rate
on, the window tiled beside others at 1280 × 1410 (1920 × 2115 pixels), not alone on the output as
the screen asks: `slatty-measure desktop` opens it where the compositor places it.

| | Median (range) |
|---|---|
| Start, warm: library in the state / shown / every cover shown | 76 (71–82) / 393 (386–417) / 436 (432–460) ms |
| Scrolling, 1,200 frames: time between frames, p50 / p99 / max | 4.16 (4.16–4.17) / 16.47 (15.59–19.65) / 18.36 (17.38–23.62) ms |
| Frames over 4.17 / 6.25 / 16.7 ms, of 1,200 | 572 (556–600) / 114 (99–210) / 11 (1–86) |
| `view` while scrolling, p50 / p99 | 0.423 (0.418–0.443) / 0.573 (0.529–0.754) ms |
| The card's power at rest: without / with Slatty / without | 37.0 (35.0–40.0) / 37.5 (36.0–41.0) / 37.0 (36.0–40.0) W |

What they say:

- In sway, start, memory and rest match the measure of 2026-11-05 on Slatty's tree of then, within
  its ranges, but for the video memory after the whole grid, 443 MB against 452 MB.
- The first frame shows some 460 ms after the library is in the state, in sway; on 2026-11-05,
  about 230 ms of that gap was sway's answer to the first frame, seen in its Wayland traffic.
- Scrolling holds 240 Hz at the median, but not throughout: about 114 frames in 1,200 past 6.25 ms;
  on 2026-11-05, the slow frames came as each row of covers came into view. Then, in a window of
  nearly the same size, the median was 5.1 ms and the 99th percentile 37 to 51 ms; why it differs is
  not established: the interface's code is the same but for one message, Umbriel may not be.
- At rest: no frame and no work, but 120 wake-ups a minute, all of one thread of zbus, the D-Bus
  library, every 500 ms.
- The card's power at rest does not rise with Slatty, within the sensor's noise.

## Opium's songs, with egui (2026-11-06)

The floor of the screen "Opium's songs": Opium, the owner's music player, with its window on
eframe and egui 0.37 over wgpu, for SlimeEngine's milestone M6d.0a. Its start had never been
measured.

- Machine: AMD Ryzen 7 5800X, 32 GB, Radeon RX 6900 XT on RADV, NVMe, Linux 7.3.
- Build: release (thin LTO, one codegen unit), Opium at `72d99e4`, from a clone; the binary,
  76.4 MB.
- Data: [`scripts/fake-music-library.py`](../scripts/fake-music-library.py)'s library, 8,500 songs
  of 2,900 albums by 1,150 artists, 595 MB; Opium in its M3E theme, its services off, muted.
- Command: [`scripts/opium-measure.sh`](../scripts/opium-measure.sh) as it was before M6d.0b,
  which ran Opium's own `scripts/measure/startup.py`, then its screenshot mode for the memory, in
  sway 1.12 without a screen, one output of 3840 × 2160 at 240 Hz, scale 1.5, the window alone on
  it; without a network or a session bus.

| | Median (range) |
|---|---|
| Start, warm, to the first frame saved, 10 runs | 181.1 (179.5–190.3) ms |
| Memory 30 s after the table of songs opens, 5 runs: resident / video | 257.8 (254.8–258.9) / 349.3 (349.3–349.3) MB |

What they say, and what is not measured:

- The first frame saved is an upper bound of the first frame: it adds egui's read-back of the
  image and its encoding as PNG. It is not the first useful frame: drawn at the window's size
  before sway gave it its tile, the library not yet in. Opium logs no moment when the table is
  drawn whole.
- The memory is taken with the table opened by Opium's screenshot mode, the only way to open a
  page at start, which repaints five times a second while it waits.
- Not measured here: the table at rest, scrolled, and its wave moving, nor the GPU's power. Each
  needs the table opened by a person's input, without the screenshot mode: the pointer of
  `wlrctl` moved and clicked in sway without a screen did not reach Opium's window, and Opium has
  no shortcut to the page. On its home page, the services off, a sign of loading turns without
  end: Opium is never at rest there. SlimeEngine's M6d.0b gives input from outside, and measures
  them.

## The method checked against Slatty's probe (2026-11-06)

[`scripts/measure.py`](../scripts/measure.py) reads any program from outside, through its
compositor and the kernel
([ADR-0200](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0200-applications-measured-from-outside.md)).
For SlimeEngine's milestone M6d.0b, it ran on Slatty's build with its probe, which logs from inside
when each frame is drawn, both reading the same runs:
[`scripts/slatty-check.sh`](../scripts/slatty-check.sh), then
[`scripts/compare-with-probe.py`](../scripts/compare-with-probe.py).

- Machine: AMD Ryzen 7 5800X, 32 GB, Radeon RX 6900 XT on RADV, NVMe, Linux 7.3.
- Slatty at `4463d00`, its probe's release build, on the fake profile of 10,000 games.
- sway 1.12 without a screen, one output of 3840 × 2160 at 240 Hz, scale 1.5, the window alone on
  it at 2560 × 1440; 10 starts after one not counted.

| | From outside | The probe | Apart |
|---|---|---|---|
| First frame, ms after the launch: shown / drawn | 261.5 (260.3–263.7) | 58.6 (57.8–60.5) | 202.9 (202.5–203.2) |
| Still frame / `covers`, the first frame drawn with every cover | 712.5 (698.0–718.2) | 714.2 (688.2–736.2) | −4.1 (−22.0 to +21.7) |
| At rest 60 s, Wayland / Xwayland: frames | 0 / 0 | 0 / 0 | 0 |
| Scrolling 1,200 frames: frames | 1,200 | 1,200 | 0 |
| The same: time between frames, p50 / p95 / p99 / longest | 4.11 / 30.91 / 31.70 / 32.28 ms | 4.30 / 31.64 / 32.29 / 34.90 ms | at most 0.7 ms, 2.6 ms for the longest |
| The same: frames over 6.25 / 16.7 ms | 336 / 91 | 327 / 91 | 9 / 0 |

The margin, from these runs:

- A frame in motion is timed within 1 ms of the probe at the median and the high percentiles,
  and the frames over 6.25 and 16.7 ms are counted within 3 %. Frames over 4.17 ms are not
  compared: drawn frames jitter around 4.17 ms, while the frames shown follow sway's schedule.
- The still frame lies within 22 ms, some five frames, of the probe's `covers`, before or after:
  the probe logs `covers` when the last cover is made at its size, not when the image last
  changes.
- The first frame shown comes 203 ms after the first frame drawn, within a millisecond, every
  run: Slatty draws it at 1440 × 900, before sway gives the window its tile, and sway shows it
  once its transaction, which waits for windows to answer their new size, times out, after 200 ms
  by default. With that timeout at 50 ms (`sway -D txn-timeout=50`), the first frame came at
  112 ms instead of 261, in 3 runs. The method counts what a person sees, sway's wait included; a
  program that answers sway at once does not pay it.

What else they say:

- sway's output without a screen refreshes at 243 Hz, not 240: 4.11 ms between frames.
- In sway, Slatty's scroll misses more frames than the probe's own runs on the owner's display:
  91 frames over 16.7 ms here, 11 there at the median (above).

## Opium's songs, from outside (2026-11-06)

The floor of the screen "Opium's songs", completed for SlimeEngine's milestone M6d.0b: what the
section of M6d.0a above left, now that a person's input reaches the window
([ADR-0200](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0200-applications-measured-from-outside.md)).

- Machine, build, data and output as above: Opium at `72d99e4`, the fake library of 8,500 songs,
  sway 1.12 without a screen at 3840 × 2160, 240 Hz, scale 1.5, the window alone on it.
- Command: [`scripts/opium-measure.sh`](../scripts/opium-measure.sh), whose second part runs
  [`scripts/measure.py`](../scripts/measure.py) with the steps of
  [`scripts/opium-songs.steps`](../scripts/opium-songs.steps), in this order: the table opened by
  a click, at rest 60 s; a song played 60 s, then paused; the table scrolled 16 logical pixels a
  frame from the first song to the last; the table closed. One run of the steps; 10 starts.
- The song plays through the session's PipeWire, muted; the library's songs are silence.

| | Figure |
|---|---|
| Start, warm, to the first frame shown, from outside / to the first frame saved, Opium's own | 109.1 (106.4–122.4) / 178.6 (173.5–187.1) ms |
| Memory, the table open: resident / proportional / video | 247.6 / 193.4 / 349.3 MB |
| The same after a song played 60 s | 261.0 / 204.3 / 349.3 MB |
| The same after the table is scrolled from end to end | 293.1 / 236.4 / 349.4 MB |
| The same 10 s after the table is closed | 293.1 / 236.4 / 349.4 MB |
| At rest 60 s, the table open: frames / processor / wake-ups a second | 0 / 0.8 % of a core / 42.9 |
| A song playing 60 s: frames a second, the time between them | 4.0, 250.1 ms (249.4–251.5) |
| The same: the processor, Opium's / the compositor's; wake-ups a second | 1.5 % / 0.2 %; 206.9 |
| Scrolled from end to end, 130 s: frames a second, p50 / p95 / p99 / longest | 243.4, 4.11 / 4.13 / 4.15 / 8.17 ms |
| The same: refreshes missed | 1 in 31,636 frames |
| The same: the processor, Opium's / the compositor's | 28.0 % / 7.2 % of a core |
| The same: the GPU's load, its power / sway alone | 12.1 %, 45.4 W / 36.8 W |

The method's own copies cost the compositor during a scroll: in 20 s of the same scroll, sway used
7.1 % of a core and the GPU was 14.4 % busy with them, 4.3 % and 9.0 % without them; Opium's
processor, 28.4 % and 28.5 %, and the GPU's power, 45.5 W both, did not change.

What they say:

- Scrolling holds the display's rate from the first song to the last, one refresh missed in 130 s,
  for about a quarter of a core, nearly all in Opium's main thread; its clipboard's thread
  (`smithay-clipboard`) wakes some 1,000 times a second meanwhile, more than the main thread.
- Memory does not come back: scrolling the table end to end adds 32 MB resident, and closing it
  gives none of it back; a song played 60 s added 13 MB before.
- Opium is never quite at rest: its thread `connect`, which looks for devices to play on, makes
  39 of its 43 wake-ups a second, the network closed as here.
- Its wave of progress moves 4 times a second while a song plays, and costs little.
- The first frame shown comes some 70 ms before the first frame that Opium saves, which adds its
  read-back and its encoding; neither is the table drawn: Opium opens on its home page.

Not measured: a frame of the table opened from a still home page, which never stands still, its
services off; the processor's power, which only root reads.
