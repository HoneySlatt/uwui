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
- Command: [`scripts/opium-measure.sh`](../scripts/opium-measure.sh), which runs Opium's own
  `scripts/measure/startup.py`, in sway 1.12 without a screen, one output of 3840 × 2160 at
  240 Hz, scale 1.5, the window alone on it; without a network or a session bus.

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
