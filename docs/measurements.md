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

## "Hello, World!" in ten frameworks (2026-11-06)

The bar of the screen "Hello, World!", for SlimeEngine's milestone M6d.0b: each framework's program
of [`references/hello-world/`](../references/hello-world/README.md), measured by
[`scripts/hello-world.sh`](../scripts/hello-world.sh).

- Machine: AMD Ryzen 7 5800X, 32 GB, Radeon RX 6900 XT on RADV, NVMe, Linux 7.3.
- sway 1.12 without a screen, one output of 3840 × 2160 at 240 Hz, scale 1.5, the window alone on
  it; drawn by sway's GL renderer on the GPU. Each program's release build; warm starts.
- Each figure: the median of 10 runs and their range, or one run.
- The desktop's own session shared the GPU, a video playing in a browser on another output: the
  GPU's power varied by 3 W over the series, more than any program changed it.

| Program | First frame shown | Still | Resident, its main process / PSS of all its processes / video memory (processes) | Size of what ships |
|---|---|---|---|---|
| GPUI with gpui-kit | 142 (139–145) ms | the same | 104.1 / 57.0 / 334.4 MB (1) | 49.0 MB |
| GPUI alone | 140 (137–143) ms | the same | 98.6 / 51.6 / 337.1 MB (1) | 35.8 MB |
| Flutter | 295 (292–298) ms | the same | 151.6 / 86.7 / 575.5 MB (1) | 21.8 MB |
| Compose for the desktop | 944 (920–973) ms | 974 (950–1002) ms | 279.3 / 214.4 / 19.1 MB (1) | 148.8 MB, with its Java runtime |
| Electron | 263 (251–273) ms | 266 (254–275) ms | 198.4 / 258.3 / 197.7 MB (7) | 287.3 MB |
| Tauri | 208 (204–215) ms | 375 (368–395) ms | 174.4 / 224.9 / 616.9 MB (3) | 6.2 MB, and the system's WebKitGTK |
| Qt Quick | 110 (108–116) ms | 132 (131–140) ms | 149.4 / 85.2 / 114.8 MB (1) | 0.05 MB, and the system's Qt, some 64 MiB |
| Slint | 71 (69–77) ms | the same | 99.3 / 39.8 / 98.2 MB (1) | 19.0 MB |
| Iced | 93 (91–97) ms | the same | 91.6 / 44.3 / 152.3 MB (1) | 21.9 MB |
| egui | 78 (76–81) ms | the same | 102.3 / 52.8 / 349.3 MB (1) | 27.4 MB |

At rest, 60 s, 10 s after the program stands still: frames / processor ticks / wake-ups, of every
thread of every process it started.

| Program | Wayland | Xwayland |
|---|---|---|
| GPUI with gpui-kit | 0 / 0 / 120 | 0 / 14 / 14,553 |
| GPUI alone | 0 / 0 / 242 | 0 / 15 / 14,681 |
| Flutter | 0 / 0 / 0 | 0 / 0 / 0 |
| Compose for the desktop | X11 only | 0 / 1 / 1,731 |
| Electron | 0 / 0 / 69 | 0 / 0 / 70 |
| Tauri | 0 / 2 / 41 | 0 / 0 / 43 |
| Qt Quick | 0 / 0 / 0 | 0 / 0 / 0 |
| Slint | 0 / 0 / 121 | 0 / 0 / 120 |
| Iced | 0 / 0 / 240 | 0 / 0 / 240 |
| egui | 0 / 0 / 120 | 0 / 0 / 120 |

What they say:

- Slint, egui and Iced show their window within 100 ms, uwui's budget of a start; GPUI, with or
  without gpui-kit, and Qt Quick within 150 ms; Compose takes nearly a second, its Java runtime
  started first.
- gpui-kit's program starts 2 ms later than GPUI's alone, holds 5 MB more and ships 13 MB more; but
  gpui-kit 0.7 runs a snapshot of GPUI (`gpui-pre` 0.3.9, wgpu 29), and GPUI alone is Zed's of the
  day (wgpu 30): the gap mixes gpui-kit with two versions of GPUI.
- Tauri's and Qt Quick's first frames are not their last: Tauri shows its window some 170 ms before
  its page, Qt Quick some 20 ms before its controls.
- Video memory varies some thirtyfold, from Compose's 19 MB, which draws through Xwayland in a window it
  keeps at 790 × 570, to Tauri's 617 MB.
- No program draws at rest. Flutter and Qt Quick do not wake at all; GPUI under Xwayland wakes
  some 240 times a second, the display's rate, and uses processor time for it.
- The GPU's power at rest did not change with any program, within the 3 W of drift.

Not measured, and why:

- Compose's window stays at its default 790 × 570 logical pixels inside sway's tile: it draws
  fewer pixels than the others, which its figures favour.
- Electron reaches the network at its first start, for its spell checker's dictionary; the
  measured starts run behind a closed proxy.
- The processor's power: only root reads its sensor (RAPL).

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

## The applications of the market (2026-11-06)

The rivals of three screens, for SlimeEngine's milestone M6d.0c, each measured from outside by
[`scripts/market.sh`](../scripts/market.sh), which runs [`scripts/measure.py`](../scripts/measure.py)
with the steps of [`scripts/market/`](../scripts/market). The bar that they set, the best of them
criterion by criterion, is in [`ROADMAP.md`](ROADMAP.md#the-bar-of-each-screen). Strawberry,
Elisa, GNOME Music and Heroic were set aside by the owner on the same day
([ADR-0201](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0201-the-rivals-narrowed.md)).

- Machine: AMD Ryzen 7 5800X, 32 GB, Radeon RX 6900 XT on RADV, NVMe, Linux 7.3.
- sway 1.12 without a screen, one output of 3840 × 2160 at 240 Hz, scale 1.5, each window alone on
  it at 2560 × 1440 logical pixels.
- Versions: one revision of nixpkgs for all, `31ecbac` of 2026-10-27, the owner's system's, pinned
  in [`flake.lock`](../flake.lock) as the input `market`. Steam's client updates itself: its
  package `1792618285`, of 2026-10-21.
- Each start: 10 warm runs after one not counted, the median and the range; "still" as
  [ADR-0200](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0200-applications-measured-from-outside.md)
  defines it, or "never" when the program did not stand still within 60 s, 5 s for Zed. The steps:
  one run.
- Memory: the proportional size (PSS) summed over all the program's processes, and its video
  memory, in MB.
- "In motion": the frames of a scroll from its first frame to its last, so that a list that
  reaches its end early is not charged for the seconds after.
- Each application has a session bus of its own; the open ones run without a network, the closed
  ones with theirs. Spotify, Cider and Steam ran on copies of the owner's profiles, logged in to
  the owner's accounts: their figures are not reproducible from this repository.

### Slatty's library

Steam on the owner's collection "Main", 281 games, opened from the view of collections; Nautilus
50.2.2 and gThumb 4.0 on the folder of Slatty's 10,000 covers, their thumbnails made beforehand by
[`scripts/thumbnails.py`](../scripts/thumbnails.py) with the thumbnailer they call, as after a
first visit. Each grid scrolled 16 logical pixels a frame for 1,200 frames, then closed; Steam
also opened a game's page.

| | Steam | Nautilus | gThumb |
|---|---|---|---|
| Start: first frame shown, ms | 7,624 (7,426–7,918) | 286 (273–311) | 316 (301–332) |
| Start: still, ms | 15,098 (11,190–15,572), 5 runs of 10; never in the others | 911 (842–1,001) | 1,313 (1,271–1,341) |
| Memory, the grid open | 1,493.2 / 354.0 | 460.3 / 333.5 | 229.7 / 153.8 |
| Memory, the grid scrolled | 1,521.9 / 305.9 | 736.1 / 1,089.3 | 404.0 / 149.9 |
| Memory, a game's page opened | 1,547.0 / 406.3 | – | – |
| Memory, the grid closed | 1,517.7 / 296.8 | 735.5 / 1,075.7 | 397.1 / 154.1 |
| At rest 60 s: frames / processor / wake-ups a second | 7,471 / 18.6 % / 3,136 | 0 / 0.0 % / 1.2 | 0 / 0.0 % / 12.1 |
| In motion: frames a second | 125.1 | 15.0 | 242.1 |
| In motion: p50 / p95 / p99 / longest, ms | 4.10 / 4.14 / 8.18 / 1,019 | 58.7 / 116.8 / 127.9 / 127.9 | 4.11 / 4.14 / 4.19 / 8.28 |
| In motion: refreshes missed / pauses of 100 ms or more | 10 / 4 | 850 / 10 | 6 / 0 |
| Scrolled: processor, the program's / the compositor's | 50.4 % / 4.0 % | 673 % / 2.0 % | 169 % / 7.8 % |
| Scrolled: the GPU's load, its power | 6.2 %, 43.6 W | 23.6 %, 47.8 W | 17.9 %, 43.1 W |

What they say:

- gThumb holds the display's rate, 6 refreshes missed in 1,209 frames, for 1.7 cores; Nautilus
  reads its thumbnails as the grid moves, on nearly seven cores, and shows 15 frames a second.
- Steam's first frame comes after 7.6 s, its launcher, its update check, its client and its web
  view started in turn. Its grid draws some 125 frames a second at rest, the pointer resting on a
  cover, whose card shows; why it draws is not established. It scrolls at that rate, with pauses
  of up to 1 s.
- No grid gives memory back when it closes. Nautilus's video memory triples while it scrolls,
  334 to 1,089 MB, and stays.

### Opium's songs

Spotify 1.2.95.453 on the owner's account, started on the public playlist "Top 10,000 Songs of
All Time", 9,998 songs: the owner's own playlists hold 13 songs at most. Cider 4.0.17 on the
owner's Apple Music library, 8,500 songs as Cider counts them while it synchronizes, its view
"Songs". Each table rested, then a song played
60 s, muted in the player, through the session's sound server; then each table scrolled 16
logical pixels at each of the display's frames, from its first song to its last, and closed.

| | Spotify | Cider |
|---|---|---|
| Start: first frame shown, ms | 448 (397–488) | 1,424 (1,407–1,442) |
| Start: still, ms | 4,409 (4,134–4,420) | 6,037 (5,190–6,732) |
| Memory, the table open | 1,076.9 / 441.9 | 945.2 / 636.7 |
| Memory, a song played 60 s | 1,046.9 / 367.4 | 886.3 / 576.1 |
| Memory, the table scrolled | 1,110.6 / 402.5 | 848.4 / 521.0 |
| Memory, the table closed, the home page open | 1,376.6 / 499.8 | 888.1 / 845.0 |
| At rest 60 s: frames / processor / wake-ups a second | 0 / 2.2 % / 315 | 38 / 3.6 % / 305 |
| A song playing 60 s: frames a second, their interval at the median | 38.4, 19.3 ms | 4.6, 250 ms |
| The same: processor / wake-ups a second / the GPU's power | 17.4 % / 2,650 / 38.7 W | 13.1 % / 1,056 / 37.8 W |
| Scrolled: seconds in motion | 13.4 | 88.4 |
| In motion: frames a second | 55.2 | 4.9 |
| In motion: p50 / p95 / p99 / longest, ms | 16.7 / 23.1 / 24.9 / 476 | 17.1 / 52.6 / 144 / 58,058 |
| In motion: refreshes missed / pauses of 100 ms or more | 2,294 / 2 | 1,423 / 15 |
| Scrolled: processor, the program's / the compositor's | 21.2 % / 0.9 % | 30.4 % / 0.9 % |
| Scrolled: the GPU's load, its power | 1.2 %, 37.9 W | 2.0 %, 38.0 W |

What they say:

- Both draw their tables at 60 frames a second at most on a display of 240 Hz, as Chromium does
  here; Opium holds 240 (above, and on the owner's display below).
- The same touchpad's scroll moves Chromium's tables much further than the pixels given: Spotify
  crossed its 9,998 songs in 13.4 s. Cider's table stops for long: 58 s without a frame in this
  run, 27 s six seconds in in an earlier one, before it moves on.
- A song playing costs Spotify 17 % of a core and 38 frames a second, its whole window redrawn;
  Cider 13 % and 4.6 frames a second; Opium 1.5 % and 4.0 (above).
- Each holds about 1 GB in its processes, and gives little or none of it back when the table
  closes; Spotify's home page takes 300 MB more.

### Zed's file

Zed 1.25.3 on the file of [`scripts/long-file.py`](../scripts/long-file.py): 100,000 lines of
Rust, 3.7 MB, SHA-256 `31d1c250…82d15c8`, written by Python 3.14; its language server off, as
nothing could fetch one. It scrolled 16 logical pixels a frame for 210 s, reaching the file's
end, then closed it.

| | Zed |
|---|---|
| Start: first frame shown / still, ms | 246 (238–263) / 1,284 (1,271–1,304) |
| Memory: the file open / scrolled / closed | 424.1 / 438.3 / 438.6, video 337.1 throughout |
| At rest 60 s: frames / processor / wake-ups a second | 0 / 0.1 % / 81.8 |
| In motion, 209 s: frames a second | 195.2 |
| In motion: p50 / p95 / p99 / longest, ms | 4.12 / 8.20 / 8.27 / 13.57 |
| In motion: refreshes missed | 10,108 in 40,860 frames |
| Scrolled: processor, Zed's / the compositor's | 92.3 % / 6.6 % |
| Scrolled: the GPU's load, its power | 12.7 %, 47.5 W |

What they say: one frame in four takes two refreshes, its main thread nearly a whole core busy;
an earlier run of the same steps, the bus of the system's services then open to Zed, held 223.6
frames a second, the spread between two runs. Zed's caret stops blinking, and Zed stands still.

### What changed in the method

- A program's stillness counted the processor's ticks of the threads alive at each reading: when
  a busy thread ended, the total fell, and the program seemed quiet. `measure.py` counts each
  thread's growth since its last reading
  ([`scripts/test_measure.py`](../scripts/test_measure.py)). The starts of this section are
  measured with it; the earlier sections' were not. Electron's and Tauri's "Hello, World!", whose
  processes start and end threads while they start, measured again with it: 264 / 266 ms and
  218 / 394 ms, against 263 / 266 and 208 / 375 above, the earlier figures standing.
- A program that leaves its launcher's tree, Steam, runs under
  [`scripts/subreaper.py`](../scripts/subreaper.py), which adopts what it leaves and ends it.
- The session bus of `market.sh` has a configuration of its own: the system's let it start a
  keyring, for which Chromium waited 25 s at each start.

## Opium's songs, on the owner's display (2026-11-06)

The frames in motion of the screen "Opium's songs", once, on the owner's display, as
[ADR-0200](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0200-applications-measured-from-outside.md)
asks: Opium at `72d99e4` on the fake library, alone on an empty workspace of the owner's display,
3840 × 2160 at 240 Hz, scale 1.5, under Umbriel, the owner's compositor, given its full width,
2560 × 1410; the steps of [`scripts/opium-display.steps`](../scripts/opium-display.steps) run by
`scripts/measure.py --display`. One run, the owner away from the machine's input; images taken
during the run showed the table open, then at its last song.

| | Figure |
|---|---|
| Scrolled 130 s: frames a second | 240.0 |
| p50 / p95 / p99 / longest, ms | 4.17 / 4.21 / 4.28 / 8.33 |
| Refreshes missed | 2 in 31,200 frames |
| The processor, Opium's / the compositor's | 26.0 % / 13.3 % |
| The GPU's load, its power | 15.1 %, 47.7 W |

What they say: Opium scrolls as smoothly on the owner's display as in sway
([above](#opiums-songs-from-outside-2026-11-06)); Umbriel, which copies the frames as sway does,
spends nearly twice sway's processor on them, 13.3 % of a core against 7.2 %. The output's other
changes, its bar's, count among the frames: they did not raise the rate above the display's.

## The control, on M6d.1b's bench (2026-11-06)

The bench of SlimeEngine's milestone M6d.1b2, checked on the control, today's rebuild by keys,
before the three other state models are compared on it
([ADR-0202](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0202-how-m6d1-compares-ways-of-writing-an-application.md)).
Each screen's [ideal code](ideal-code/control/) runs on uwui's tree in SlimeEngine, with what the
four models share added to it on the branch
[`m6d1b-bench`](https://github.com/HoneySlatt/SlimeEngine/tree/m6d1b-bench/benches/src/prototypes),
thrown away once M6d.1b ends. There is no window: the bench is the host, and moves its clock a frame
of 240 Hz at a time. These figures do not compare with those measured from outside above.

- Machine: AMD Ryzen 7 5800X, 32 GB, Linux 7.3; the bench pinned to one core.
- Build: release, SlimeEngine's branch `m6d1b-bench`: the counts at `4969314`, the times at
  `ffa6e09`, the machine at rest. A run at `4969314` while the owner played on the machine was some
  30 % slower, and is not kept. Between the two commits, the interface's clock moved from the
  application's column to the input's, a few nanoseconds a frame, and a text counts as changed by
  what it lays out rather than by its layout's place in memory, which changed one count: the
  songs' theme, 5,076 items changed in place of 5,128.
- Command: `taskset -c 6 target/release/slime-benches --prototypes`, after
  `cargo build --locked --release -p slime-benches`, in SlimeEngine's `nix develop`.
- Each time: the median of 21 runs, and their range, in ms of the processor. Each count: taken once,
  and the same on a second run, for every screen; a second measure in another process counted the
  same too.
- The screen: 3840 × 2160 pixels at a scale of 1.5, which each screen fills. The data are made in
  the program, the same at every run: 10,000 games, 8,500 songs and 100,000 lines; images are keys,
  decoded nowhere.

### How the bench measures

- **A frame** gives the interface and the program the frame's time, then handles its input, gives
  the actions to the program and runs its builders, then styles, lays out and gathers the display
  list. Its five parts are timed and their allocations counted apart, on the bench's thread:
  *input*, the interface taking the frame's time and its input; *application*, the program's
  `advance`, `act` and `build`;
  *styles*; *layout*; *display list*, what changed drawn again and the list gathered.
- **An interaction** is its inputs, frame by frame, then the frames that run until nothing moves
  and no builder is asked to run again: a transition's, a fade's.
- **Delay**: from the frame that takes the interaction's first input to the first frame after which
  no builder must run again, in frames of 4.17 ms, and the processor time of those frames. It ends
  when nothing is left pending in the control's way, a builder asked; a model that defers its work
  otherwise, to the next frame, adds its own pending work to it at M6d.1b3.
- **Items changed**: the items of a frame's display list that the list before did not hold, what a
  renderer that kept the list before would draw anew, a text the same where it lays out the same
  text in the same style and box; out of all the items, over the interaction's frames.
- **Items wrong**: once an interaction settled, its display list compared, item by item, with that
  of a new interface built from the same state, the program cloned and built on a new interface,
  given the first one's scrolls, focus, pointer and theme, both still. Any item that differs is a
  wrong render.
- **A frame where nothing changed**: one frame without input, once the screen opened and settled.
- **Memory**: the bytes taken less those given back on the bench's thread, against what it held
  before the screen opened, its interface already made with its fonts and themes: the screen's
  data alone; the screen open and still; and after the whole script, its root removed and its
  program dropped. The bench's own records are left out.

### For the owner's laptop

The owner, and only the owner, may run the same on the lowest machine: no agent measures there.
From a clone of SlimeEngine, plugged in, other programs closed:

```sh
git switch m6d1b-bench
nix develop -c cargo build --locked --release -p slime-benches
nix develop -c taskset -c 1 target/release/slime-benches --prototypes > control.md
```

It took 98 s here. The press of "Hello, World!" prints `Clicked!` before the tables, once a run;
`--runs 5` gives a quicker look; screens may be named:
`hello library songs document mistake`. The build compiles the engine's benchmarks, wgpu among
them: its length on the laptop is not known.

### The figures

#### "Hello, World!"

| Interaction | Frames | Delay: frames, CPU ms | Builders run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 1 | 1, 0.294 (0.279–0.481) | 1 | 4 | 1 | 4 | 4 / 4 (100.0 %) | 0 of 4 |
| its button pressed | 1 | 1, 0.076 (0.071–0.091) | 0 | 1 | 0 | 1 | 0 / 4 (0.0 %) | 0 of 4 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 4 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.003 (0.002–0.014) | 0.214 (0.203–0.253) | 0.074 (0.072–0.211) | 0.002 (0.002–0.009) | 0.294 (0.279–0.481) |
| its button pressed | 0.001 (0.001–0.004) | 0.003 (0.002–0.003) | 0.070 (0.066–0.083) | 0.000 (0.000–0.000) | 0.001 (0.001–0.002) | 0.076 (0.071–0.091) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.007) | 0.000 (0.000–0.004) | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.001 (0.001–0.009) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 18, 16.6 | 4501, 242.3 | 408, 87.1 | 34, 3.1 |
| its button pressed | 3, 0.2 | 0, 0.0 | 1408, 68.6 | 1, 0.0 | 18, 1.8 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 6, 0.7 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.07 MB; after the script and the screen closed, 0.06 MB.

#### Slatty's library

| Interaction | Frames | Delay: frames, CPU ms | Builders run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 1.984 (1.933–2.739) | 3 | 320 | 2 | 320 | 218 / 225 (96.9 %) | 0 of 218 |
| scrolled, 16 logical pixels a frame | 1200 | 1, 0.081 (0.080–0.097) | 181 | 4276 | 181 | 412560 | 275340 / 283453 (97.1 %) | 0 of 247 |
| the filter focused by Tab | 1 | 1, 0.026 (0.024–0.032) | 0 | 1 | 0 | 1 | 1 / 248 (0.4 %) | 0 of 248 |
| a filter typed, a character a frame | 5 | 1, 1.764 (1.619–2.514) | 9 | 1020 | 5 | 1028 | 692 / 720 (96.1 %) | 0 of 208 |
| the grid focused by Tab | 1 | 1, 0.024 (0.023–0.034) | 0 | 3 | 0 | 2 | 0 / 207 (0.0 %) | 0 of 207 |
| the selection moved by the arrows | 39 | 1, 0.731 (0.706–0.762) | 4 | 320 | 3 | 427 | 248 / 8500 (2.9 %) | 0 of 218 |
| a game's page opened, its key art fading in | 45 | 1, 0.387 (0.378–0.428) | 1 | 5 | 1 | 48 | 49 / 10035 (0.5 %) | 0 of 223 |
| the page closed | 1 | 1, 0.061 (0.059–0.074) | 1 | 1 | 1 | 0 | 0 / 218 (0.0 %) | 0 of 218 |
| the theme changed | 37 | 1, 0.618 (0.600–0.650) | 0 | 320 | 0 | 11840 | 3924 / 8066 (48.6 %) | 0 of 218 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 218 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.150 (0.129–0.594) | 0.478 (0.466–0.525) | 1.255 (1.227–1.446) | 0.101 (0.097–0.174) | 1.984 (1.933–2.739) |
| scrolled, 16 logical pixels a frame | 2.840 (2.752–2.985) | 17.438 (17.249–17.726) | 2.527 (2.487–2.624) | 28.667 (28.196–29.018) | 92.162 (90.819–93.240) | 143.583 (141.756–145.169) |
| the filter focused by Tab | 0.005 (0.004–0.008) | 0.000 (0.000–0.000) | 0.002 (0.002–0.003) | 0.000 (0.000–0.000) | 0.019 (0.017–0.021) | 0.026 (0.024–0.032) |
| a filter typed, a character a frame | 0.042 (0.041–0.044) | 2.583 (2.490–3.316) | 0.324 (0.247–0.342) | 2.125 (2.068–2.202) | 0.268 (0.259–0.290) | 5.359 (5.108–6.078) |
| the grid focused by Tab | 0.005 (0.005–0.014) | 0.000 (0.000–0.000) | 0.003 (0.003–0.004) | 0.000 (0.000–0.000) | 0.015 (0.015–0.017) | 0.024 (0.023–0.034) |
| the selection moved by the arrows | 0.003 (0.003–0.003) | 0.161 (0.151–0.171) | 0.105 (0.102–0.111) | 0.503 (0.493–0.527) | 0.484 (0.463–0.520) | 1.261 (1.225–1.302) |
| a game's page opened, its key art fading in | 0.001 (0.001–0.002) | 0.008 (0.007–0.010) | 0.263 (0.257–0.301) | 0.120 (0.116–0.130) | 0.483 (0.468–0.516) | 0.877 (0.862–0.932) |
| the page closed | 0.001 (0.001–0.001) | 0.004 (0.004–0.006) | 0.002 (0.002–0.003) | 0.041 (0.040–0.050) | 0.013 (0.012–0.019) | 0.061 (0.059–0.074) |
| the theme changed | 0.002 (0.002–0.002) | 0.003 (0.003–0.004) | 2.191 (2.155–2.415) | 0.002 (0.002–0.003) | 2.749 (2.692–3.236) | 4.944 (4.870–5.660) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.012 (0.011–0.016) | 0.013 (0.012–0.017) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1107, 2653.7 | 8756, 471.6 | 8470, 915.6 | 1723, 257.1 |
| scrolled, 16 logical pixels a frame | 1201, 38.4 | 189137, 14427.4 | 4614, 236.4 | 161883, 43431.6 | 2106546, 291652.8 |
| the filter focused by Tab | 14, 5.0 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 53, 87.5 |
| a filter typed, a character a frame | 207, 23.6 | 43642, 4060.9 | 1023, 19.0 | 19512, 1399.7 | 5345, 731.6 |
| the grid focused by Tab | 18, 4.8 | 0, 0.0 | 4, 0.1 | 1, 0.0 | 48, 79.0 |
| the selection moved by the arrows | 6, 0.8 | 1145, 260.4 | 700, 85.8 | 6084, 374.7 | 2587, 3178.4 |
| a game's page opened, its key art fading in | 3, 0.3 | 40, 4.1 | 4554, 271.5 | 506, 56.0 | 971, 3503.6 |
| the page closed | 5, 0.3 | 21, 1.0 | 2, 0.0 | 183, 31.8 | 18, 77.2 |
| the theme changed | 8, 0.3 | 1, 0.0 | 44003, 8717.5 | 37, 0.3 | 61010, 8512.0 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 18, 77.2 |

Memory held, against before the screen opened: its data alone, 0.65 MB; open and still, 2.59 MB; after the script and the screen closed, 6.43 MB.

#### Opium's songs

| Interaction | Frames | Delay: frames, CPU ms | Builders run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.406 (2.322–2.621) | 4 | 219 | 2 | 219 | 169 / 181 (93.4 %) | 0 of 169 |
| scrolled from end to end, 16 logical pixels a frame | 27625 | 1, 0.238 (0.234–0.253) | 16948 | 67792 | 16948 | 5881272 | 4412940 / 4755405 (92.8 %) | 0 of 168 |
| a column sorted by a click on its header | 37 | 1, 2.240 (2.041–2.586) | 2 | 1 | 1 | 193 | 171 / 6216 (2.8 %) | 0 of 168 |
| the table focused by Tab, from the header | 3 | 1, 0.014 (0.013–0.027) | 0 | 6 | 0 | 3 | 0 / 504 (0.0 %) | 0 of 168 |
| the selection moved by the arrows | 39 | 1, 1.397 (1.323–1.850) | 4 | 212 | 1 | 320 | 265 / 6661 (4.0 %) | 0 of 169 |
| the theme changed | 37 | 1, 1.092 (1.057–1.176) | 0 | 219 | 0 | 8103 | 5076 / 6253 (81.2 %) | 0 of 169 |
| a song played by Enter | 37 | 1, 0.225 (0.216–0.259) | 38 | 8 | 1 | 76 | 39 / 6253 (0.6 %) | 0 of 169 |
| each frame while a song plays, its wave moving | 240 | 1, 0.008 (0.008–0.015) | 240 | 0 | 0 | 240 | 11 / 40671 (0.0 %) | 0 of 170 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 169 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.155 (0.123–0.178) | 0.825 (0.817–0.978) | 1.308 (1.241–1.343) | 0.120 (0.117–0.133) | 2.406 (2.322–2.621) |
| scrolled from end to end, 16 logical pixels a frame | 41.606 (40.718–45.594) | 1221.629 (1209.744–1269.231) | 50.842 (50.148–55.178) | 816.810 (807.748–876.962) | 2106.246 (2094.659–2214.732) | 4237.489 (4206.418–4461.697) |
| a column sorted by a click on its header | 0.014 (0.013–0.020) | 1.225 (1.028–1.463) | 0.134 (0.116–0.142) | 0.720 (0.697–0.786) | 0.460 (0.444–0.495) | 2.545 (2.326–2.887) |
| the table focused by Tab, from the header | 0.008 (0.007–0.012) | 0.000 (0.000–0.001) | 0.004 (0.004–0.005) | 0.000 (0.000–0.000) | 0.024 (0.022–0.036) | 0.036 (0.034–0.052) |
| the selection moved by the arrows | 0.002 (0.002–0.003) | 0.221 (0.202–0.593) | 0.094 (0.080–0.118) | 0.933 (0.904–1.018) | 0.450 (0.434–0.490) | 1.712 (1.632–2.172) |
| the theme changed | 0.002 (0.002–0.002) | 0.004 (0.004–0.005) | 2.186 (2.136–2.312) | 0.003 (0.002–0.003) | 5.405 (5.330–5.670) | 7.620 (7.492–7.971) |
| a song played by Enter | 0.002 (0.002–0.003) | 0.100 (0.093–0.110) | 0.087 (0.083–0.107) | 0.061 (0.058–0.069) | 0.283 (0.274–0.300) | 0.533 (0.518–0.572) |
| each frame while a song plays, its wave moving | 0.005 (0.005–0.005) | 0.117 (0.109–0.134) | 0.020 (0.017–0.024) | 0.009 (0.008–0.012) | 1.757 (1.686–1.945) | 1.905 (1.828–2.108) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.009 (0.009–0.014) | 0.010 (0.010–0.015) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1105, 1381.6 | 16969, 929.0 | 9679, 976.9 | 1807, 270.1 |
| scrolled from end to end, 16 logical pixels a frame | 27542, 881.3 | 16914106, 950423.6 | 84740, 4677.6 | 5552861, 724808.4 | 43962991, 5669253.5 |
| a column sorted by a click on its header | 3, 0.2 | 1011, 190.1 | 1384, 91.6 | 6324, 429.6 | 3439, 2944.8 |
| the table focused by Tab, from the header | 30, 2.7 | 0, 0.0 | 6, 0.1 | 3, 0.0 | 83, 217.5 |
| the selection moved by the arrows | 6, 0.8 | 1167, 1386.8 | 589, 81.5 | 8050, 619.0 | 3699, 3101.5 |
| the theme changed | 8, 0.3 | 1, 0.0 | 42405, 6578.4 | 37, 0.3 | 98488, 12293.3 |
| a song played by Enter | 3, 0.3 | 1194, 63.8 | 1386, 89.1 | 290, 26.2 | 1011, 2710.3 |
| each frame while a song plays, its wave moving | 0, 0.0 | 1200, 63.4 | 0, 0.0 | 240, 1.9 | 5520, 17438.6 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 19, 71.7 |

Memory held, against before the screen opened: its data alone, 1.39 MB; open and still, 2.61 MB; after the script and the screen closed, 38.79 MB.

#### A document of 100,000 lines

| Interaction | Frames | Delay: frames, CPU ms | Builders run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 1.443 (1.341–1.669) | 3 | 74 | 2 | 74 | 75 / 78 (96.2 %) | 0 of 75 |
| a line that shows changed | 1 | 1, 0.051 (0.048–0.062) | 1 | 0 | 1 | 1 | 1 / 75 (1.3 %) | 0 of 75 |
| a line that does not show changed | 1 | 1, 0.026 (0.025–0.037) | 1 | 0 | 0 | 0 | 0 / 75 (0.0 %) | 0 of 75 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 75 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.060 (0.043–0.069) | 0.217 (0.188–0.236) | 1.120 (1.059–1.350) | 0.047 (0.043–0.054) | 1.443 (1.341–1.669) |
| a line that shows changed | 0.000 (0.000–0.000) | 0.026 (0.024–0.029) | 0.000 (0.000–0.000) | 0.020 (0.019–0.026) | 0.005 (0.004–0.006) | 0.051 (0.048–0.062) |
| a line that does not show changed | 0.000 (0.000–0.000) | 0.023 (0.022–0.031) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.003 (0.003–0.005) | 0.026 (0.025–0.037) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.004 (0.003–0.012) | 0.004 (0.004–0.013) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 320, 663.2 | 3205, 174.7 | 3127, 753.5 | 754, 107.1 |
| a line that shows changed | 0, 0.0 | 237, 24.7 | 0, 0.0 | 119, 11.7 | 23, 37.1 |
| a line that does not show changed | 0, 0.0 | 236, 24.6 | 0, 0.0 | 1, 0.0 | 13, 36.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 13, 36.4 |

Memory held, against before the screen opened: its data alone, 10.75 MB; open and still, 11.74 MB; after the script and the screen closed, 0.92 MB.

#### The control's mistake, a revision not moved

| Interaction | Frames | Delay: frames, CPU ms | Builders run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 0.576 (0.563–0.711) | 3 | 47 | 2 | 47 | 49 / 52 (94.2 %) | 0 of 49 |
| the list focused by Tab | 1 | 1, 0.005 (0.004–0.006) | 0 | 1 | 0 | 1 | 0 / 49 (0.0 %) | 0 of 49 |
| the selection moved by an arrow | 1 | 1, 0.003 (0.003–0.008) | 0 | 0 | 0 | 0 | 0 / 49 (0.0 %) | 2 of 49 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 49 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.025 (0.024–0.040) | 0.220 (0.216–0.296) | 0.307 (0.298–0.417) | 0.023 (0.023–0.025) | 0.576 (0.563–0.711) |
| the list focused by Tab | 0.001 (0.001–0.002) | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.002 (0.002–0.003) | 0.005 (0.004–0.006) |
| the selection moved by an arrow | 0.001 (0.001–0.002) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.002 (0.002–0.005) | 0.003 (0.003–0.008) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.002 (0.002–0.006) | 0.003 (0.003–0.007) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 210, 334.8 | 4198, 231.2 | 1852, 295.9 | 481, 55.3 |
| the list focused by Tab | 7, 0.5 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 14, 18.4 |
| the selection moved by an arrow | 2, 0.3 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 12, 18.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 12, 18.4 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.43 MB; after the script and the screen closed, 0.39 MB.

### The lines that the prototype forced to change

Counted by [`scripts/count_code.py`](../scripts/count_code.py), against the ideal code at
`1f501f2`:

| File | Ideal | Prototype | What changed, and why |
|---|---|---|---|
| `hello.rs` | 25 | 22 | `Clone` derived, for the bench's new interface; `Hello` made public, for the bench to make it; `main` gone, 3 lines: no host runs it yet |
| `library.rs` | 140 | 139 | `Clone` derived on 3 types; `main` gone, 3 lines |
| `songs.rs` | 203 | 202 | `Clone` derived on 3 types; `main` gone, 3 lines |
| `document.rs` | 41 | 39 | `Clone` derived; `main` gone, 3 lines |
| `library.style` | 21 | 24 | The key art's size in uwui's format, and a height, since an image has no size of its own: 1 line; the cover's image given the cell's room: a rule of 3 lines |
| `songs.style` | 37 | 37 | 7 sizes in uwui's format, `{ Pixels = 36 }` and `"Auto"`, and `text.align`, which uwui calls `text.style.alignment`: 8 lines |

No compile error met in the screens' code. Three errors met reading the style sheets, each a
document error at the start: `"100%"`, no dimension of uwui's; `text.align`; and
`enter.opacity`, first an option, which a style sheet writes as a list: `enter` became a share of
the style's opacity, so that the ideal line holds.

What the parts that the four models share chose, on the branch, for each model alike: a screen's
root is a grid of one cell, which the screen fills; `pressable` lays its children out in a column;
the wave is 480 by 24 logical pixels; the screens' data are made by the bench, in place of the
ideal code's `uwui::sample`, whose types the screens' files define; a grid places its cells in
the order that its builder adds them; a row or a cell selected is in the state `Selected`; each
theme's rules are made when the themes are given, so that a change of theme costs only its
styling. They are tested through the bench alone, not apart: none is kept.

### What they say

- Every interaction shows in the frame of its input. A list's or a grid's first rows show one frame
  after the screen opens: the first frame lays the list out, the second builds its rows.
- A frame where nothing changed runs no builder, styles and lays out nothing, and draws nothing
  again, in 1 to 13 µs. It still allocates, 7 to 20 times and 0.7 to 77 kB: once in the
  layout's phase, the rest in the display list's, which gathers its list anew.
- Scrolling draws again every element that shows, its place being in its items: 93 to 97 % of the
  items change at each frame. The display list is the costliest phase, two thirds of the library's
  scroll and half of the songs', with 1,590 to 1,760 allocations a frame.
- Styling allocates much: a button styled again, "Hello"'s press, takes 1,408 allocations and
  69 kB; a theme changed, the library's 320 elements over 37 frames of transition, 44,000 and
  8.7 MB in its styles alone.
- The control's own cost shows in the application's phase: the filter runs 9 builders over 4
  characters and allocates 4 MB, every title lowered in case at each character; a line of the
  document that does not show runs the lines' builder again, 236 allocations, and draws nothing.
- While a song plays, its wave's builder runs alone at each frame, 5 allocations; its items seldom
  change: snapped to whole pixels, the wave moves less than a pixel a frame.
- Once a screen closed, the interface keeps what it laid out: 38.8 MB after Opium's songs scrolled
  from end to end, near the text cache's budget of 32 MiB; 6.4 MB after the library; 0.9 MB after
  the document; 0.06 MB after "Hello". The bench does not tell apart the text cache, the arena of
  elements, which never shrinks, the cache of styles, and the fonts' data read at their first use.
- The bench shows the control's own mistake, a revision not moved, as a wrong render: 2 items of
  49 after the arrow, the list still showing the row selected before. Every screen renders as a new
  interface would: 0 items wrong after each interaction.

Not measured: the owner's laptop, which the owner may measure with the command above; a start,
the memory that the system sees, power, and the GPU, which a window's host measures from M6d.7.
