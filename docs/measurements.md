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

## Three models beside the control, on M6d.1b's bench (2026-11-07)

Signals, views that say they changed, and messages, prototyped on the bench of SlimeEngine's
milestone M6d.1b3a from [their ideal code](ideal-code/README.md), and the control measured again
beside them on the same bench
([ADR-0202](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0202-how-m6d1-compares-ways-of-writing-an-application.md)).
The prototypes are on the branch
[`m6d1b-bench`](https://github.com/HoneySlatt/SlimeEngine/tree/m6d1b-bench/benches/src/prototypes),
thrown away once M6d.1b ends. The bench measures as
[the control's section](#how-the-bench-measures) says, with the additions below. From them, and
from what Opium, Pluto and the DAW ask of uwui, the owner chose signals, with live values
([ADR-0205](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0205-signals-change-uwuis-interface.md)). Slatty's list, written
after, checked the choice: no need of its left uncovered ([ADR-0206](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0206-slatty-ported-again-the-daw-later.md)).

- Machine: AMD Ryzen 7 5800X, 32 GB, Linux 7.3; the bench pinned to one core, the machine at
  rest.
- Build: release, SlimeEngine's branch `m6d1b-bench`. The control and the signals' times at
  `efdad6d`; the signals' counts at `fcc9acb`, which marks a selection changed alone as
  `Ui::describe` does, without drawing its list again, and counts the same at `ae40506`; the views
  and messages at `ae40506`, which takes out of them allocations of the prototypes' own: a `Vec`
  for each row of a view's processor, and a closure for each handler of `view`, whose message is
  now kept by value, as Iced keeps it. A run of the signals at `ae40506` was some 10 % slower
  throughout, in the theme's styles too, which their code does not touch: the machine's noise, not
  kept.
- Command: `taskset -c 6 target/release/slime-benches --prototypes`, after
  `cargo build --locked --release -p slime-benches`. A model and a screen may be named:
  `control signals views messages`, `hello library songs document mistakes`.
- Each time: the median of 21 runs. Each count: taken once, and the same on a second run, for
  every screen of every model.

### What the bench added for the three models

On the branch, beside what the four share since M6d.1b2:

- **Elements nested as tuples**, an array, a `Vec` or an `Option`, which the three models write
  and the control does not.
- **A description matched with the tree's by keys**, for views and messages: an element without a
  key takes the key of its place among its siblings.
- **Events found up the tree:** a handler is looked for from the element that an action names up
  to the root; a command or a cancel that none takes there goes to any handler of it.
- **Scripts that find their elements by class**, not by the control's paths, so that the four
  models play the same script; the search runs outside the spans measured.
- **The delay ended by the model's own pending work too:** a frame ends it only when no builder is
  asked to run and the model has no work left for the next frame, a message queued, a binding
  queued, a view notified and not rendered. In the four models, none was left: a screen's first
  rows show one frame after it opens, and every other interaction in the frame of its input, as
  in the control.
- **On uwui's tree:** `Ui::describe`, which gives an element a new description outside its
  builder; `Ui::change`, which changes one part of it, a text, an image, a class, a selection, a
  list's rows or a wave, marking what `describe` would for that part, without the rest given
  again; `Children::keep`, which keeps a child and its subtree as they are; `Ui::parent`;
  `Ui::asks_build`; `Ui::forget_builds`, which makes each builder run again whatever its
  revision; and the children that a build removes freed in the order of their places.
- **Exact counts:** the tree's removal in a fixed order, and the bench's maps hashed with fixed
  keys. Before, the places that new elements took, and the moment a map that takes and gives back
  entries grew, changed from one run to the next, which the second run's check showed. The
  control is measured again on this bench: it pays one allocation more for each build that removes
  children.

What each model's runtime is, on the branch:

- **Signals**, written by hand, no library added
  ([ADR-0204](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0204-signals-written-by-hand-for-the-prototypes.md)): one thread;
  signals, memos and bindings in an arena, each owned by a scope; values in a `RefCell`, so that a
  value borrowed twice panics, as Floem's; a memo tells what reads it only when its value
  changed. A closure given where a value would be becomes a binding that changes that part of its
  element through `Ui::change`. A list mounts the rows that come in scopes of their own and
  disposes those that leave; `dyn_view` mounts its view again in a new scope. A new interface is
  built from the same state by running the view's function again in a new runtime, the root
  scope's signals taking their values in the order that they are made. Two ways in which it may
  cost less than Floem: its bindings wait in a queue until the frame's build, so that a handler
  that sets two signals runs a binding that reads both once; and `set` tells no one of a value
  equal to the one held, as the ideal code has it.
- **Views that say they changed:** each view a value in the application, rendered again when it
  calls `notify`, its root element kept in its parent's place; a view within a view renders apart:
  a view not notified is kept as it is when its parent renders, as GPUI's `Entity::cached` keeps
  it, not as GPUI's plain views, which render with their parent. A list's processor runs when its
  view rendered or the list shows other rows. A view is released, its value dropped, at the end
  of the frame after its last handle goes. The figures are views' best case.
- **Messages:** `update` for each message of the frame, then `view` whole, `lazy` keeping a part
  whose value is equal, by its place in the description. A shortcut of the prototype, not of the
  model: the description borrows the state, which the application owns beside it, so it is not
  kept between messages. When a list shows other rows, `view` runs again, only that list's
  closure and the `lazy` parts on its way used, and the closure runs for every row that shows.
  Iced keeps its tree of widgets, which own their data, between messages; the ideal code's grid
  ran its closure for the cells that come alone.

"Code run" counts, in each model, the units of the application's code that the model calls:

| Model | A unit |
|---|---|
| Control | a builder |
| Signals | a memo worked out, a binding run again, a row's, a cell's or the root's view made |
| Views | a `render`, a processor |
| Messages | a `view`, a `lazy` part's closure, a row's or a cell's closure for each row or cell that shows |

The units are not of one size: a builder or a `render` describes many elements, a binding changes
one part of one. The times compare; the units count what each model runs. Each model's runtime
keeps its own books in the application's phase, counted there: the signals' arena of nodes, the
views' processors in `Rc`, the messages' `lazy` values in `Rc` and their places in the description
as `Vec`s.

### The four models side by side

In each cell: the processor time of the whole interaction, in ms, the median of 21 runs; the
allocations of the application's phase; and the units of code run, as the table above counts
them. The other phases' counts, and every range, are in the full figures below.

#### "Hello, World!"

| Interaction | Control | Signals | Views | Messages |
|---|---|---|---|---|
| opened | 0.357; 18; 1 | 0.341; 19; 1 | 0.348; 22; 1 | 0.335; 21; 1 |
| its button pressed | 0.095; 0; 0 | 0.093; 0; 0 | 0.094; 0; 0 | 0.098; 18; 1 |
| A frame where nothing changed | 0.001; 0; 0 | 0.002; 0; 0 | 0.002; 0; 0 | 0.001; 0; 0 |

Memory held, in MB: open and still; after the script and the screen closed:

| Control | Signals | Views | Messages |
|---|---|---|---|
| 0.07; 0.06 | 0.07; 0.06 | 0.07; 0.06 | 0.07; 0.06 |

#### Slatty's library

| Interaction | Control | Signals | Views | Messages |
|---|---|---|---|---|
| opened | 2.331; 1107; 3 | 2.697; 12125; 107 | 2.393; 1231; 3 | 2.306; 1242; 107 |
| scrolled, 16 logical pixels a frame | 174.985; 189227; 181 | 153.830; 31742; 1365 | 182.406; 211046; 181 | 171.565; 213037; 20551 |
| the filter focused by Tab | 0.030; 0; 0 | 0.029; 0; 0 | 0.030; 0; 0 | 0.028; 0; 0 |
| a filter typed, a character a frame | 6.334; 43645; 9 | 6.600; 46712; 352 | 6.415; 44053; 9 | 6.076; 44073; 345 |
| the grid focused by Tab | 0.026; 0; 0 | 0.026; 0; 0 | 0.028; 0; 0 | 0.026; 0; 0 |
| the selection moved by the arrows | 1.481; 1146; 4 | 1.541; 2044; 108 | 1.879; 3440; 6 | 1.731; 3443; 318 |
| a game's page opened, its key art fading in | 1.011; 40; 1 | 0.969; 35; 1 | 1.188; 1126; 2 | 1.105; 1126; 106 |
| the page closed | 0.072; 22; 1 | 0.067; 8; 1 | 0.246; 1109; 2 | 0.217; 1110; 106 |
| the theme changed | 5.842; 1; 0 | 5.937; 4; 1 | 5.895; 1109; 2 | 5.695; 1110; 106 |
| A frame where nothing changed | 0.014; 0; 0 | 0.014; 0; 0 | 0.015; 0; 0 | 0.014; 0; 0 |

Memory held, in MB: open and still; after the script and the screen closed:

| Control | Signals | Views | Messages |
|---|---|---|---|
| 2.59; 6.43 | 2.94; 6.43 | 2.61; 6.43 | 2.61; 6.43 |

#### Opium's songs

| Interaction | Control | Signals | Views | Messages |
|---|---|---|---|---|
| opened | 2.615; 1105; 4 | 2.693; 2683; 28 | 2.621; 1015; 4 | 2.574; 1041; 30 |
| scrolled from end to end, 16 logical pixels a frame | 4978.913; 16922580; 16948 | 3638.214; 1186364; 8474 | 5598.537; 15159988; 16948 | 5224.382; 15532844; 483018 |
| a column sorted by a click on its header | 2.656; 1011; 2 | 2.718; 315; 161 | 2.888; 914; 2 | 2.747; 926; 28 |
| the table focused by Tab, from the header | 0.040; 0; 0 | 0.039; 0; 0 | 0.040; 0; 0 | 0.038; 0; 0 |
| the selection moved by the arrows | 1.876; 1168; 4 | 2.070; 2603; 29 | 2.233; 2827; 6 | 2.111; 2863; 84 |
| the theme changed | 8.536; 1; 0 | 8.413; 4; 1 | 8.437; 912; 2 | 8.250; 41; 1 |
| a song played by Enter | 0.607; 1194; 38 | 0.509; 173; 64 | 0.689; 1251; 39 | 0.797; 2479; 64 |
| each frame while a song plays, its wave moving | 2.187; 1200; 240 | 2.043; 720; 240 | 2.385; 2160; 240 | 3.274; 10320; 240 |
| A frame where nothing changed | 0.011; 0; 0 | 0.011; 0; 0 | 0.011; 0; 0 | 0.011; 0; 0 |

Memory held, in MB: open and still; after the script and the screen closed:

| Control | Signals | Views | Messages |
|---|---|---|---|
| 2.61; 38.79 | 2.70; 38.79 | 2.61; 38.79 | 2.61; 38.79 |

#### A document of 100,000 lines

| Interaction | Control | Signals | Views | Messages |
|---|---|---|---|---|
| opened | 1.513; 320; 3 | 1.610; 1190; 73 | 1.512; 324; 3 | 1.504; 327; 74 |
| a line that shows changed | 0.055; 237; 1 | 0.028; 7; 1 | 0.075; 247; 2 | 0.064; 248; 73 |
| a line that does not show changed | 0.029; 236; 1 | 0.004; 1; 0 | 0.045; 246; 2 | 0.037; 247; 73 |
| A frame where nothing changed | 0.005; 0; 0 | 0.006; 0; 0 | 0.005; 0; 0 | 0.005; 0; 0 |

Memory held, in MB: open and still; after the script and the screen closed:

| Control | Signals | Views | Messages |
|---|---|---|---|
| 11.73; 0.92 | 38.03; 0.92 | 11.73; 0.92 | 11.73; 0.92 |

### Wrong renders and panics

Each mistake of [the ideal code's list](ideal-code/README.md#mistakes-that-the-compiler-lets-through),
shown by a small case that compiles; the small cases' figures are in the tables below.

| Model | Mistake | What shows |
|---|---|---|
| The four | A key forgotten: covers keyed by their places | The focus passes to another game when one before it is removed: in each model, the second cover focused, then the first removed, the focus is on "Game 2", not "Game 1". The comparison with a new interface does not see it: it takes the focus by path, which follows the keys |
| Control | A revision not moved | A wrong render: 2 items of 49 |
| Control | An id kept after its builder ran again | Nothing: the id's generation moved, and it names no new element |
| Signals | A signal read outside a closure that the view tracks | A wrong render: 1 item of 50 |
| Signals | A signal of a scope disposed, read | A panic: a page's signal, its handle kept outside the page, read by a bar below it once the page closed and the selection moved |
| Signals | A value borrowed twice | A panic: `update` inside a closure that `with` runs |
| Views | A `notify` forgotten | A wrong render: 2 items of 49 |
| Views | A view within a view changed without its own `notify` | A wrong render: 1 item of 50 |
| Views | A view updated while it is updated, found by the prototype | A panic: a view within a view tells the view around it, which updates the view within, as GPUI's entities panic |
| Messages | A `lazy` part whose value leaves out what it reads | A wrong render: 1 item of 49 |
| Messages | A subscription to frames not given up | At rest, `update` and `view` run at each frame: 46 units of code a frame where nothing changes |
| Messages | A `lazy` part kept by its place, found by the review and not shown by a case | Two `lazy` parts of equal values that change places, or a sibling that comes before one, keep the wrong content, as Iced's `lazy` by place does |

Compile errors met writing the prototypes from the ideal code, an indication that depends on who
writes: in views, five errors of the borrow checker, without codes, in two functions: Rust 2024
captures every lifetime of an `impl Trait` that a method returns, so that `cover` and `song_row`,
called in a processor's closure, return `impl IntoElement + use<>`. In messages, two lints: an
element turned into itself by `.into()`, which the prototype answers with a widget type that turns
into `El`, as Iced's do; a private type in `Message`. In signals, none in the screens' code.

The concepts that the ideal code's README counts hold, but for one in views: on the library and
the songs, `use<>`, a function's result that captures no lifetime, is a ninth concept of the
model's. A widget that turns into `El` is the `.into()` that messages' ideal code wrote already;
`Clone` derived is the bench's, for a new interface, not the author's.

### The reloads, and a task cancelled with its component

Answered on Slatty's library, its grid scrolled, a filter typed, the selection moved and a game's
page open, without `subsecond` or `serde`: a function's body swapped through a table of entry
points, as `subsecond` does; a type's state through a form by its fields' names, written by hand.
The time that a reload takes is M6d.1c's.

| Model | A function's body | A type's state migrated | A task cancelled with its component |
|---|---|---|---|
| Control | Shows once the tree forgets its builders' revisions, which the prototype adds to the tree: no revision moved, no builder runs the new body. State kept | Through a form; the revisions and ids, the program's state too, start again, and the builders are forgotten. State kept | No: the page's elements go and nothing tells the program, which keeps the task unless it drops it by hand |
| Signals | The view's function runs again in a new runtime, its signals replayed in the order that they are made, mounted over the tree, whose elements keep their state by their keys; the view before disposed, its cleanups run, so that its tasks are cancelled and the new view starts its own. State kept | Not kept: a changed type that adds a signal before the others shifts the order, the new signal taking the selection's value, the selection the page's, which its type refuses: the selection and the page are lost. Signals would need names | Yes: in `on_cleanup`, with the page's scope |
| Views | Every view renders again through a table of bodies by type. State kept | Each view's value through a form. State kept | Yes: the page a view of its own, which holds the task, released with its last handle |
| Messages | `view` runs again. State kept | The state through a form. State kept | Yes for a subscription, given up once the state no longer asks for it; a task started once would need its handle kept by hand, not prototyped |

### The lines that the prototypes forced to change

Counted by [`scripts/count_code.py`](../scripts/count_code.py), against the ideal code at
`1f501f2`, each file's two lines that declare its module of tests left out. In each, `main` is gone, 3
to 9 lines, no host running it yet, and `uwui::prelude` is `super::prelude`, the same names.

| Model | Screen | Ideal | Prototype | What changed, and why |
|---|---|---|---|---|
| Signals | `hello.rs` | 13 | 10 | `hello` made public, for the bench to call it |
| Signals | `library.rs` | 63 | 61 | `Clone` derived on `Game`, for a new interface's signals replayed |
| Signals | `songs.rs` | 140 | 138 | `Clone` derived on `Song` |
| Signals | `document.rs` | 28 | 25 | Nothing |
| Views | `hello.rs` | 16 | 14 | `Clone` derived, a view cloned for a new interface; `Hello` made public |
| Views | `library.rs` | 101 | 100 | `Clone` on 2 types; `cover` returns `impl IntoElement + use<>` |
| Views | `songs.rs` | 172 | 172 | `Clone` on 3 types; `song_row` returns `impl IntoElement + use<>` |
| Views | `document.rs` | 28 | 25 | `Clone`; `lines` made public, for the bench to make the document |
| Messages | `hello.rs` | 21 | 18 | `Message`, `update` and `view` made public |
| Messages | `library.rs` | 98 | 94 | `Clone` on 2 types, a state cloned for a new interface |
| Messages | `songs.rs` | 168 | 163 | `Clone` on 2 types; `Column` made public, `Message` holding it |
| Messages | `document.rs` | 31 | 24 | `Clone`; `lines` made public |

The style sheets are the control's, unchanged.

### What moving the editor and *Hunna Wood* would cost

The places in their code that would change, counted on SlimeEngine's `main` at `65bbb57`, the
code under test left out. The editor is `crates/slime-editor/src`; *Hunna Wood* builds with uwui
its overlay of development alone, `games/hunnawood/src/overlay.rs`, behind its feature
`development`; both build panels of `crates/slime-devui`, counted once, apart.

| Place | Editor | *Hunna Wood* | `slime-devui` |
|---|---|---|---|
| Builders, `Ui::build` | 10 | 1 | 4 |
| Elements described in them, `add` and `add_slot` | 39 | 7 | 29 |
| Actions read: `take_actions` | 1 | 1 | 1 |
| Actions read: arms on `ActionKind` | 14 | 2 | 7 |
| Ids kept to read actions, fields | 23 | 3 | 7 |
| Revisions kept by hand: fields | 6 | 1 | 3 |
| Revisions kept by hand: places that move them | 15 | 1 | 3 |
| The tree's state read back: `focus`, `state` | 5 | 0 | 3 |

What each place becomes in each model:

| Place | Control | Signals | Views | Messages |
|---|---|---|---|---|
| A builder | stays | a view's function, run once; what it reads of the program's state becomes signals | a view's `render`, or a processor for a list's rows | a part of `view`, `lazy` where a revision guarded it |
| An element described | stays | an element in a tuple; each value that changes, a closure | an element in a tuple, keyed where it was | an element in a tuple, keyed where it was |
| An action read, an arm | stays | a handler on its element | a listener on its element | a message, its variant and its arm in `update` |
| An id kept | stays | gone | gone | gone |
| A revision kept, a field | stays | gone, its state in signals | gone | gone, or a `lazy` part's value |
| A place that moves a revision | stays | gone | a `notify` | gone |
| The tree's state read back | stays | stays | stays | stays |

In the editor, 10 builders, 14 arms, 23 ids, 6 revisions and 15 places that move them would
change in each of the three models; in *Hunna Wood*'s overlay, 1, 2, 3, 1 and 1. The models differ
in what the code becomes, not in how many places change. Not counted: the editor's dock, built
by uwui's `Dock::build`, its viewports, drawn by the renderer into surfaces, and one box of the
marquee added to the display list by hand.

### What they say

- On the tree's phases, styles, layout and the display list, the four models do the same work:
  the counts of elements styled, laid out and drawn again, and of items changed, are the same in
  each, but for Opium's bar, which holds in the control one row more around its wave. The models
  differ in the application's phase, and in what they hold.
- Signals cost least where a list scrolls: they keep the rows that stay, and make only those that
  come. Opium's table scrolled from end to end, 3.6 s of processor against 5.0 to 5.6 s, and
  1.2 million allocations in the application against 15.2 to 16.9 million; Slatty's grid, 154 ms
  against 172 to 182 ms. A line of the document that does not show costs them 4 µs and 1
  allocation, against 29 to 45 µs and 236 to 247.
- Signals cost most to open and to hold: the library opens with 12,100 allocations in the
  application against 1,100 to 1,250; a document of 100,000 lines, a signal each, holds 38.0 MB
  against 11.7 MB. A sort runs again each row's closures that read the order, 161 units of code, against 2 renders
  or builders, and 28 closures of `view` and its rows in messages.
- Views and messages describe a whole screen again for a change of one part: a page closed or a
  theme changed in the library takes some 1,100 allocations in the application, against 22 and 1
  for the control, and 8 and 4 for signals. Their scrolls cost as the control's, which builds the
  rows again too, the views' some 5 to 12 % more.
- Messages run `view` at each frame of the wave, the table kept by `lazy`: 3.3 ms and 10,300
  allocations over 240 frames, against 2.0 to 2.4 ms and 720 to 2,200 for the other three.
- A frame where nothing changed runs no code of the application and allocates nothing in it, in
  the four models; only a subscription to frames not given up breaks that, in messages.
- In each model, a screen's first rows show one frame after it opens, the list laid out first,
  and every other interaction in the frame of its input: none left work of its own for the next
  frame.
- The memory held after a screen closed is the tree's, the same in the four.
- Signals' reload keeps the state for a new body, but not for a changed type unless its signals
  are named; the three others keep it for both. The control is the only one told nothing when a
  part goes, so that a task bound to it is cancelled by hand.
- Each model shows its own mistakes; none shows fewer than two. The control's id kept after its
  builder ran again is no mistake on uwui's tree, the id's generation keeping it from naming
  another element. A key forgotten passes element
  state to another item in all four, and the bench's comparison does not see it.

Not measured: the owner's laptop, which the owner may measure with the command above; a start,
the memory that the system sees, power, and the GPU, which a window's host measures from M6d.7.

### The figures, in full

<details>
<summary>The control</summary>

#### "Hello, World!"

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 1 | 1, 0.357 (0.321–0.478) | 1 | 4 | 1 | 4 | 4 / 4 (100.0 %) | 0 of 4 |
| its button pressed | 1 | 1, 0.095 (0.089–0.125) | 0 | 1 | 0 | 1 | 0 / 4 (0.0 %) | 0 of 4 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 4 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.003 (0.003–0.012) | 0.255 (0.230–0.286) | 0.091 (0.086–0.221) | 0.003 (0.002–0.003) | 0.357 (0.321–0.478) |
| its button pressed | 0.002 (0.002–0.006) | 0.008 (0.007–0.022) | 0.084 (0.077–0.113) | 0.000 (0.000–0.000) | 0.002 (0.002–0.003) | 0.095 (0.089–0.125) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.005) | 0.000 (0.000–0.000) | 0.001 (0.000–0.001) | 0.001 (0.001–0.007) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 18, 16.6 | 4501, 242.3 | 408, 87.1 | 34, 3.1 |
| its button pressed | 3, 0.2 | 0, 0.0 | 1408, 68.6 | 1, 0.0 | 18, 1.8 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 6, 0.7 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.07 MB; after the script and the screen closed, 0.06 MB.

#### Slatty's library

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.331 (2.257–3.454) | 3 | 320 | 2 | 320 | 218 / 225 (96.9 %) | 0 of 218 |
| scrolled, 16 logical pixels a frame | 1200 | 1, 0.100 (0.096–0.166) | 181 | 4276 | 181 | 412560 | 275340 / 283453 (97.1 %) | 0 of 247 |
| the filter focused by Tab | 1 | 1, 0.030 (0.028–0.036) | 0 | 1 | 0 | 1 | 1 / 248 (0.4 %) | 0 of 248 |
| a filter typed, a character a frame | 5 | 1, 2.023 (1.894–2.651) | 9 | 1020 | 5 | 1028 | 692 / 720 (96.1 %) | 0 of 208 |
| the grid focused by Tab | 1 | 1, 0.026 (0.025–0.044) | 0 | 3 | 0 | 2 | 0 / 207 (0.0 %) | 0 of 207 |
| the selection moved by the arrows | 39 | 1, 0.881 (0.845–1.468) | 4 | 320 | 3 | 427 | 248 / 8500 (2.9 %) | 0 of 218 |
| a game's page opened, its key art fading in | 45 | 1, 0.456 (0.425–0.747) | 1 | 5 | 1 | 48 | 49 / 10035 (0.5 %) | 0 of 223 |
| the page closed | 1 | 1, 0.072 (0.069–0.110) | 1 | 1 | 1 | 0 | 0 / 218 (0.0 %) | 0 of 218 |
| the theme changed | 37 | 1, 0.727 (0.703–1.184) | 0 | 320 | 0 | 11840 | 3924 / 8066 (48.6 %) | 0 of 218 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 218 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.153 (0.145–0.720) | 0.562 (0.551–0.734) | 1.495 (1.443–1.800) | 0.119 (0.113–0.200) | 2.331 (2.257–3.454) |
| scrolled, 16 logical pixels a frame | 3.454 (3.389–3.943) | 21.916 (21.471–26.568) | 3.064 (2.982–3.584) | 35.767 (35.227–43.142) | 110.990 (108.265–130.120) | 174.985 (171.527–207.357) |
| the filter focused by Tab | 0.005 (0.005–0.008) | 0.000 (0.000–0.000) | 0.003 (0.002–0.008) | 0.000 (0.000–0.000) | 0.021 (0.020–0.023) | 0.030 (0.028–0.036) |
| a filter typed, a character a frame | 0.050 (0.048–0.060) | 3.032 (2.911–3.617) | 0.358 (0.284–0.391) | 2.532 (2.463–3.074) | 0.315 (0.306–0.419) | 6.334 (6.059–6.948) |
| the grid focused by Tab | 0.006 (0.005–0.009) | 0.000 (0.000–0.000) | 0.004 (0.004–0.007) | 0.000 (0.000–0.000) | 0.016 (0.016–0.028) | 0.026 (0.025–0.044) |
| the selection moved by the arrows | 0.003 (0.003–0.005) | 0.192 (0.178–0.295) | 0.121 (0.113–0.200) | 0.610 (0.589–1.066) | 0.548 (0.516–0.946) | 1.481 (1.417–2.511) |
| a game's page opened, its key art fading in | 0.002 (0.002–0.003) | 0.009 (0.008–0.016) | 0.306 (0.288–0.507) | 0.144 (0.136–0.243) | 0.549 (0.519–0.979) | 1.011 (0.974–1.748) |
| the page closed | 0.001 (0.001–0.001) | 0.006 (0.005–0.008) | 0.002 (0.002–0.004) | 0.049 (0.047–0.077) | 0.013 (0.013–0.020) | 0.072 (0.069–0.110) |
| the theme changed | 0.002 (0.002–0.003) | 0.003 (0.003–0.008) | 2.539 (2.479–3.604) | 0.003 (0.003–0.006) | 3.288 (3.195–4.889) | 5.842 (5.682–8.511) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.013 (0.013–0.023) | 0.014 (0.014–0.024) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1107, 2653.7 | 8756, 471.6 | 8470, 915.6 | 1723, 257.1 |
| scrolled, 16 logical pixels a frame | 1201, 38.4 | 189227, 14438.2 | 4614, 236.4 | 161883, 43431.6 | 2106546, 291652.8 |
| the filter focused by Tab | 14, 5.0 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 53, 87.5 |
| a filter typed, a character a frame | 207, 23.6 | 43645, 4063.8 | 1023, 19.0 | 19512, 1399.7 | 5345, 731.6 |
| the grid focused by Tab | 18, 4.8 | 0, 0.0 | 4, 0.1 | 1, 0.0 | 48, 79.0 |
| the selection moved by the arrows | 6, 0.8 | 1146, 261.2 | 700, 85.8 | 6084, 374.7 | 2587, 3178.4 |
| a game's page opened, its key art fading in | 3, 0.3 | 40, 4.1 | 4554, 271.5 | 506, 56.0 | 971, 3503.6 |
| the page closed | 5, 0.3 | 22, 1.0 | 2, 0.0 | 183, 31.8 | 18, 77.2 |
| the theme changed | 8, 0.3 | 1, 0.0 | 44003, 8717.5 | 37, 0.3 | 61010, 8512.0 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 18, 77.2 |

Memory held, against before the screen opened: its data alone, 0.65 MB; open and still, 2.59 MB; after the script and the screen closed, 6.43 MB.

#### Opium's songs

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.615 (2.551–2.770) | 4 | 219 | 2 | 219 | 169 / 181 (93.4 %) | 0 of 169 |
| scrolled from end to end, 16 logical pixels a frame | 27625 | 1, 0.274 (0.260–0.311) | 16948 | 67792 | 16948 | 5881272 | 4412940 / 4755405 (92.8 %) | 0 of 168 |
| a column sorted by a click on its header | 37 | 1, 2.321 (2.245–2.734) | 2 | 1 | 1 | 193 | 171 / 6216 (2.8 %) | 0 of 168 |
| the table focused by Tab, from the header | 3 | 1, 0.016 (0.015–0.024) | 0 | 6 | 0 | 3 | 0 / 504 (0.0 %) | 0 of 168 |
| the selection moved by the arrows | 39 | 1, 1.529 (1.462–1.710) | 4 | 212 | 1 | 320 | 265 / 6661 (4.0 %) | 0 of 169 |
| the theme changed | 37 | 1, 1.223 (1.185–1.301) | 0 | 219 | 0 | 8103 | 5076 / 6253 (81.2 %) | 0 of 169 |
| a song played by Enter | 37 | 1, 0.258 (0.243–0.300) | 38 | 8 | 1 | 76 | 39 / 6253 (0.6 %) | 0 of 169 |
| each frame while a song plays, its wave moving | 240 | 1, 0.009 (0.009–0.018) | 240 | 0 | 0 | 240 | 11 / 40671 (0.0 %) | 0 of 170 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 169 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.159 (0.142–0.194) | 0.895 (0.869–0.988) | 1.425 (1.397–1.495) | 0.133 (0.129–0.149) | 2.615 (2.551–2.770) |
| scrolled from end to end, 16 logical pixels a frame | 46.636 (44.612–55.053) | 1446.591 (1405.060–1532.823) | 56.741 (54.330–61.468) | 958.713 (919.650–1032.312) | 2469.768 (2396.362–2622.122) | 4978.913 (4820.014–5303.777) |
| a column sorted by a click on its header | 0.015 (0.014–0.016) | 1.169 (1.134–1.435) | 0.142 (0.135–0.160) | 0.812 (0.781–0.900) | 0.514 (0.483–0.566) | 2.656 (2.554–3.062) |
| the table focused by Tab, from the header | 0.009 (0.008–0.011) | 0.000 (0.000–0.001) | 0.004 (0.004–0.005) | 0.000 (0.000–0.000) | 0.027 (0.025–0.038) | 0.040 (0.038–0.056) |
| the selection moved by the arrows | 0.003 (0.003–0.004) | 0.229 (0.216–0.289) | 0.094 (0.090–0.143) | 1.050 (1.005–1.126) | 0.499 (0.483–0.601) | 1.876 (1.805–2.078) |
| the theme changed | 0.002 (0.002–0.003) | 0.004 (0.003–0.005) | 2.434 (2.370–2.609) | 0.003 (0.003–0.004) | 6.094 (5.909–6.417) | 8.536 (8.290–9.037) |
| a song played by Enter | 0.002 (0.002–0.003) | 0.115 (0.112–0.133) | 0.098 (0.093–0.123) | 0.069 (0.065–0.088) | 0.320 (0.300–0.397) | 0.607 (0.585–0.723) |
| each frame while a song plays, its wave moving | 0.006 (0.006–0.007) | 0.146 (0.135–0.224) | 0.024 (0.022–0.044) | 0.012 (0.010–0.018) | 1.999 (1.852–2.577) | 2.187 (2.026–2.870) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.010 (0.009–0.017) | 0.011 (0.010–0.019) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1105, 1381.6 | 16969, 929.0 | 9679, 976.9 | 1807, 270.1 |
| scrolled from end to end, 16 logical pixels a frame | 27542, 881.3 | 16922580, 950694.7 | 84740, 4677.6 | 5552861, 724808.4 | 43962991, 5669253.5 |
| a column sorted by a click on its header | 3, 0.2 | 1011, 190.1 | 1384, 91.6 | 6324, 429.6 | 3439, 2944.8 |
| the table focused by Tab, from the header | 30, 2.7 | 0, 0.0 | 6, 0.1 | 3, 0.0 | 83, 217.5 |
| the selection moved by the arrows | 6, 0.8 | 1168, 1387.0 | 589, 81.5 | 8050, 619.0 | 3699, 3101.5 |
| the theme changed | 8, 0.3 | 1, 0.0 | 42405, 6578.4 | 37, 0.3 | 98488, 12293.3 |
| a song played by Enter | 3, 0.3 | 1194, 63.8 | 1386, 89.1 | 290, 26.2 | 1011, 2710.3 |
| each frame while a song plays, its wave moving | 0, 0.0 | 1200, 63.4 | 0, 0.0 | 240, 1.9 | 5520, 17438.6 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 19, 71.7 |

Memory held, against before the screen opened: its data alone, 1.39 MB; open and still, 2.61 MB; after the script and the screen closed, 38.79 MB.

#### A document of 100,000 lines

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 1.513 (1.428–1.670) | 3 | 74 | 2 | 74 | 75 / 78 (96.2 %) | 0 of 75 |
| a line that shows changed | 1 | 1, 0.055 (0.053–0.061) | 1 | 0 | 1 | 1 | 1 / 75 (1.3 %) | 0 of 75 |
| a line that does not show changed | 1 | 1, 0.029 (0.028–0.042) | 1 | 0 | 0 | 0 | 0 / 75 (0.0 %) | 0 of 75 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 75 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.001) | 0.060 (0.043–0.084) | 0.224 (0.202–0.266) | 1.184 (1.128–1.265) | 0.051 (0.046–0.057) | 1.513 (1.428–1.670) |
| a line that shows changed | 0.000 (0.000–0.000) | 0.028 (0.027–0.031) | 0.000 (0.000–0.000) | 0.021 (0.021–0.024) | 0.005 (0.004–0.006) | 0.055 (0.053–0.061) |
| a line that does not show changed | 0.000 (0.000–0.000) | 0.026 (0.025–0.035) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.003 (0.003–0.006) | 0.029 (0.028–0.042) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.004 (0.003–0.012) | 0.005 (0.004–0.014) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 320, 663.2 | 3205, 174.7 | 3127, 753.5 | 754, 107.1 |
| a line that shows changed | 0, 0.0 | 237, 24.7 | 0, 0.0 | 119, 11.7 | 23, 37.1 |
| a line that does not show changed | 0, 0.0 | 236, 24.6 | 0, 0.0 | 1, 0.0 | 13, 36.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 13, 36.4 |

Memory held, against before the screen opened: its data alone, 10.75 MB; open and still, 11.73 MB; after the script and the screen closed, 0.92 MB.

#### A revision not moved

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 0.646 (0.638–0.661) | 3 | 47 | 2 | 47 | 49 / 52 (94.2 %) | 0 of 49 |
| the list focused by Tab | 1 | 1, 0.005 (0.005–0.009) | 0 | 1 | 0 | 1 | 0 / 49 (0.0 %) | 0 of 49 |
| the selection moved by an arrow | 1 | 1, 0.003 (0.003–0.008) | 0 | 0 | 0 | 0 | 0 / 49 (0.0 %) | 2 of 49 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 49 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.028 (0.027–0.036) | 0.250 (0.244–0.259) | 0.338 (0.334–0.351) | 0.027 (0.026–0.028) | 0.646 (0.638–0.661) |
| the list focused by Tab | 0.001 (0.001–0.003) | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.002 (0.002–0.004) | 0.005 (0.005–0.009) |
| the selection moved by an arrow | 0.001 (0.001–0.002) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.002 (0.002–0.005) | 0.003 (0.003–0.008) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.003 (0.003–0.003) | 0.004 (0.003–0.004) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 210, 334.8 | 4198, 231.2 | 1852, 295.9 | 481, 55.3 |
| the list focused by Tab | 7, 0.5 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 14, 18.4 |
| the selection moved by an arrow | 2, 0.3 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 12, 18.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 12, 18.4 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.43 MB; after the script and the screen closed, 0.39 MB.

Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!
Clicked!

</details>

<details>
<summary>Signals</summary>

#### "Hello, World!"

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 1 | 1, 0.341 (0.335–0.364) | 1 | 4 | 1 | 4 | 4 / 4 (100.0 %) | 0 of 4 |
| its button pressed | 1 | 1, 0.093 (0.091–0.103) | 0 | 1 | 0 | 1 | 0 / 4 (0.0 %) | 0 of 4 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 4 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.004 (0.004–0.014) | 0.246 (0.241–0.256) | 0.087 (0.086–0.096) | 0.002 (0.002–0.003) | 0.341 (0.335–0.364) |
| its button pressed | 0.002 (0.002–0.003) | 0.008 (0.008–0.014) | 0.082 (0.080–0.091) | 0.000 (0.000–0.000) | 0.002 (0.002–0.002) | 0.093 (0.091–0.103) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.002 (0.002–0.002) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 19, 16.9 | 4501, 242.3 | 408, 87.1 | 34, 3.1 |
| its button pressed | 3, 0.2 | 0, 0.0 | 1408, 68.6 | 1, 0.0 | 18, 1.8 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 6, 0.7 |

Memory held, against before the screen opened: its data alone, 0.01 MB; open and still, 0.07 MB; after the script and the screen closed, 0.06 MB.

#### Slatty's library

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.697 (2.585–2.929) | 107 | 320 | 2 | 320 | 218 / 225 (96.9 %) | 0 of 218 |
| scrolled, 16 logical pixels a frame | 1200 | 1, 0.094 (0.092–0.101) | 1365 | 4276 | 181 | 412560 | 275340 / 283453 (97.1 %) | 0 of 247 |
| the filter focused by Tab | 1 | 1, 0.029 (0.027–0.039) | 0 | 1 | 0 | 1 | 1 / 248 (0.4 %) | 0 of 248 |
| a filter typed, a character a frame | 5 | 1, 2.178 (1.996–2.290) | 352 | 1020 | 5 | 1028 | 692 / 720 (96.1 %) | 0 of 208 |
| the grid focused by Tab | 1 | 1, 0.026 (0.025–0.034) | 0 | 3 | 0 | 2 | 0 / 207 (0.0 %) | 0 of 207 |
| the selection moved by the arrows | 39 | 1, 0.979 (0.942–1.009) | 108 | 320 | 3 | 427 | 248 / 8500 (2.9 %) | 0 of 218 |
| a game's page opened, its key art fading in | 45 | 1, 0.438 (0.426–0.464) | 1 | 5 | 1 | 48 | 49 / 10035 (0.5 %) | 0 of 223 |
| the page closed | 1 | 1, 0.067 (0.065–0.086) | 1 | 1 | 1 | 0 | 0 / 218 (0.0 %) | 0 of 218 |
| the theme changed | 37 | 1, 0.692 (0.661–0.743) | 1 | 320 | 0 | 11840 | 3924 / 8066 (48.6 %) | 0 of 218 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 218 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.615 (0.557–0.677) | 0.545 (0.523–0.602) | 1.415 (1.376–1.532) | 0.113 (0.107–0.123) | 2.697 (2.585–2.929) |
| scrolled, 16 logical pixels a frame | 3.259 (3.179–3.675) | 8.881 (8.760–9.231) | 2.852 (2.795–2.966) | 34.010 (33.278–35.164) | 104.834 (103.278–107.966) | 153.830 (151.290–159.002) |
| the filter focused by Tab | 0.005 (0.005–0.012) | 0.000 (0.000–0.001) | 0.002 (0.002–0.005) | 0.000 (0.000–0.000) | 0.021 (0.020–0.028) | 0.029 (0.027–0.039) |
| a filter typed, a character a frame | 0.048 (0.047–0.053) | 3.470 (3.300–3.620) | 0.357 (0.259–0.376) | 2.401 (2.298–2.473) | 0.306 (0.293–0.315) | 6.600 (6.200–6.826) |
| the grid focused by Tab | 0.005 (0.005–0.008) | 0.001 (0.001–0.001) | 0.004 (0.003–0.004) | 0.000 (0.000–0.000) | 0.016 (0.015–0.020) | 0.026 (0.025–0.034) |
| the selection moved by the arrows | 0.003 (0.003–0.004) | 0.323 (0.297–0.336) | 0.120 (0.114–0.128) | 0.580 (0.566–0.617) | 0.513 (0.488–0.583) | 1.541 (1.489–1.630) |
| a game's page opened, its key art fading in | 0.002 (0.002–0.002) | 0.015 (0.014–0.023) | 0.298 (0.290–0.316) | 0.136 (0.132–0.145) | 0.515 (0.493–0.593) | 0.969 (0.935–1.059) |
| the page closed | 0.001 (0.001–0.001) | 0.005 (0.005–0.012) | 0.002 (0.002–0.004) | 0.046 (0.044–0.059) | 0.013 (0.012–0.020) | 0.067 (0.065–0.086) |
| the theme changed | 0.002 (0.002–0.002) | 0.008 (0.008–0.016) | 2.405 (2.361–2.764) | 0.003 (0.002–0.003) | 3.508 (3.376–3.637) | 5.937 (5.776–6.236) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.013 (0.012–0.027) | 0.014 (0.013–0.029) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 12125, 4223.4 | 8756, 471.6 | 8470, 915.6 | 1723, 257.1 |
| scrolled, 16 logical pixels a frame | 1201, 38.4 | 31742, 19717.1 | 4614, 236.4 | 161883, 43431.6 | 2106546, 291652.8 |
| the filter focused by Tab | 14, 5.0 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 53, 87.5 |
| a filter typed, a character a frame | 207, 23.6 | 46712, 7164.9 | 1023, 19.0 | 19512, 1399.7 | 5345, 731.6 |
| the grid focused by Tab | 18, 4.8 | 0, 0.0 | 4, 0.1 | 1, 0.0 | 48, 79.0 |
| the selection moved by the arrows | 6, 0.8 | 2044, 1133.1 | 700, 85.8 | 6084, 374.7 | 2587, 3178.4 |
| a game's page opened, its key art fading in | 3, 0.3 | 35, 12.9 | 4554, 271.5 | 506, 56.0 | 971, 3503.6 |
| the page closed | 5, 0.3 | 8, 0.5 | 2, 0.0 | 183, 31.8 | 18, 77.2 |
| the theme changed | 8, 0.3 | 4, 0.2 | 44003, 8717.5 | 37, 0.3 | 61010, 8512.0 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 18, 77.2 |

Memory held, against before the screen opened: its data alone, 0.58 MB; open and still, 2.94 MB; after the script and the screen closed, 6.43 MB.

#### Opium's songs

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.693 (2.597–2.833) | 28 | 218 | 2 | 218 | 169 / 181 (93.4 %) | 0 of 169 |
| scrolled from end to end, 16 logical pixels a frame | 27625 | 1, 0.202 (0.191–0.232) | 8474 | 67792 | 16948 | 5881272 | 4412940 / 4755405 (92.8 %) | 0 of 168 |
| a column sorted by a click on its header | 37 | 1, 2.398 (2.173–2.545) | 161 | 1 | 1 | 193 | 171 / 6216 (2.8 %) | 0 of 168 |
| the table focused by Tab, from the header | 3 | 1, 0.015 (0.015–0.025) | 0 | 6 | 0 | 3 | 0 / 504 (0.0 %) | 0 of 168 |
| the selection moved by the arrows | 39 | 1, 1.725 (1.629–1.894) | 29 | 212 | 1 | 320 | 265 / 6661 (4.0 %) | 0 of 169 |
| the theme changed | 37 | 1, 1.269 (1.220–1.355) | 1 | 218 | 0 | 8066 | 5076 / 6253 (81.2 %) | 0 of 169 |
| a song played by Enter | 37 | 1, 0.180 (0.169–0.220) | 64 | 8 | 1 | 75 | 39 / 6253 (0.6 %) | 0 of 169 |
| each frame while a song plays, its wave moving | 240 | 1, 0.009 (0.008–0.016) | 240 | 0 | 0 | 240 | 11 / 40671 (0.0 %) | 0 of 170 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 169 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.294 (0.281–0.309) | 0.885 (0.850–0.971) | 1.392 (1.328–1.474) | 0.130 (0.124–0.169) | 2.693 (2.597–2.833) |
| scrolled from end to end, 16 logical pixels a frame | 45.457 (44.520–52.216) | 219.472 (216.065–234.821) | 54.150 (52.588–58.195) | 934.684 (921.012–989.296) | 2384.638 (2361.304–2459.081) | 3638.214 (3602.678–3790.860) |
| a column sorted by a click on its header | 0.014 (0.013–0.017) | 1.272 (1.079–1.368) | 0.138 (0.124–0.152) | 0.793 (0.769–0.860) | 0.509 (0.480–0.552) | 2.718 (2.492–2.899) |
| the table focused by Tab, from the header | 0.009 (0.008–0.010) | 0.001 (0.000–0.001) | 0.004 (0.004–0.010) | 0.000 (0.000–0.000) | 0.026 (0.025–0.038) | 0.039 (0.037–0.054) |
| the selection moved by the arrows | 0.003 (0.003–0.004) | 0.401 (0.376–0.570) | 0.117 (0.094–0.140) | 1.040 (1.009–1.112) | 0.500 (0.476–0.578) | 2.070 (1.972–2.326) |
| the theme changed | 0.002 (0.002–0.003) | 0.010 (0.009–0.016) | 2.392 (2.325–2.592) | 0.003 (0.002–0.003) | 6.002 (5.903–6.270) | 8.413 (8.251–8.879) |
| a song played by Enter | 0.002 (0.002–0.003) | 0.026 (0.024–0.044) | 0.102 (0.098–0.128) | 0.067 (0.063–0.078) | 0.312 (0.295–0.391) | 0.509 (0.489–0.643) |
| each frame while a song plays, its wave moving | 0.006 (0.006–0.007) | 0.084 (0.075–0.131) | 0.024 (0.022–0.039) | 0.013 (0.010–0.017) | 1.918 (1.837–2.537) | 2.043 (1.955–2.730) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.010 (0.009–0.022) | 0.011 (0.010–0.023) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 2683, 2113.6 | 16968, 929.0 | 9662, 969.0 | 1805, 270.1 |
| scrolled from end to end, 16 logical pixels a frame | 27542, 881.3 | 1186364, 329464.2 | 84740, 4677.6 | 5552861, 724808.4 | 43962991, 5669253.5 |
| a column sorted by a click on its header | 3, 0.2 | 315, 168.4 | 1383, 91.4 | 6323, 429.6 | 3439, 2944.8 |
| the table focused by Tab, from the header | 30, 2.7 | 0, 0.0 | 6, 0.1 | 3, 0.0 | 83, 217.5 |
| the selection moved by the arrows | 6, 0.8 | 2603, 2050.1 | 589, 81.5 | 8050, 619.0 | 3699, 3101.5 |
| the theme changed | 8, 0.3 | 4, 0.2 | 42295, 6553.6 | 37, 0.3 | 98414, 12292.2 |
| a song played by Enter | 3, 0.3 | 173, 11.1 | 1385, 88.9 | 287, 25.2 | 1009, 2710.3 |
| each frame while a song plays, its wave moving | 0, 0.0 | 720, 48.0 | 0, 0.0 | 240, 1.9 | 5520, 17438.6 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 19, 71.7 |

Memory held, against before the screen opened: its data alone, 1.34 MB; open and still, 2.70 MB; after the script and the screen closed, 38.79 MB.

#### A document of 100,000 lines

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 1.610 (1.530–1.699) | 73 | 74 | 2 | 74 | 75 / 78 (96.2 %) | 0 of 75 |
| a line that shows changed | 1 | 1, 0.028 (0.027–0.058) | 1 | 0 | 1 | 1 | 1 / 75 (1.3 %) | 0 of 75 |
| a line that does not show changed | 1 | 1, 0.004 (0.004–0.037) | 0 | 0 | 0 | 0 | 0 / 75 (0.0 %) | 0 of 75 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 75 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.119 (0.106–0.144) | 0.242 (0.206–0.276) | 1.191 (1.147–1.248) | 0.054 (0.049–0.062) | 1.610 (1.530–1.699) |
| a line that shows changed | 0.000 (0.000–0.000) | 0.002 (0.002–0.005) | 0.000 (0.000–0.000) | 0.020 (0.020–0.048) | 0.005 (0.005–0.007) | 0.028 (0.027–0.058) |
| a line that does not show changed | 0.000 (0.000–0.000) | 0.001 (0.001–0.005) | 0.000 (0.000–0.001) | 0.000 (0.000–0.001) | 0.003 (0.003–0.030) | 0.004 (0.004–0.037) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.001 (0.001–0.002) | 0.000 (0.000–0.001) | 0.000 (0.000–0.001) | 0.004 (0.004–0.024) | 0.006 (0.005–0.028) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1190, 984.7 | 3205, 174.7 | 3127, 753.5 | 754, 107.1 |
| a line that shows changed | 0, 0.0 | 7, 0.3 | 0, 0.0 | 119, 11.7 | 23, 37.1 |
| a line that does not show changed | 0, 0.0 | 1, 0.0 | 0, 0.0 | 1, 0.0 | 13, 36.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 13, 36.4 |

Memory held, against before the screen opened: its data alone, 37.02 MB; open and still, 38.03 MB; after the script and the screen closed, 0.92 MB.

#### A signal read outside a closure that the view tracks

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 0.738 (0.725–0.800) | 46 | 49 | 2 | 49 | 50 / 54 (92.6 %) | 0 of 50 |
| the list focused by Tab | 1 | 1, 0.005 (0.005–0.006) | 0 | 1 | 0 | 1 | 0 / 50 (0.0 %) | 0 of 50 |
| the selection moved by an arrow | 37 | 1, 0.008 (0.008–0.017) | 1 | 2 | 0 | 74 | 71 / 1885 (3.8 %) | 1 of 50 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 50 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.050 (0.047–0.063) | 0.294 (0.291–0.317) | 0.365 (0.357–0.392) | 0.027 (0.026–0.029) | 0.738 (0.725–0.800) |
| the list focused by Tab | 0.001 (0.001–0.002) | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.002 (0.002–0.003) | 0.005 (0.005–0.006) |
| the selection moved by an arrow | 0.002 (0.002–0.009) | 0.005 (0.005–0.007) | 0.018 (0.017–0.023) | 0.002 (0.002–0.002) | 0.120 (0.118–0.151) | 0.146 (0.144–0.185) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.001 (0.000–0.001) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.003 (0.003–0.007) | 0.004 (0.004–0.008) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 332, 539.1 | 5188, 285.4 | 1993, 307.0 | 497, 56.2 |
| the list focused by Tab | 8, 0.5 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 16, 18.5 |
| the selection moved by an arrow | 2, 0.3 | 5, 0.3 | 258, 51.2 | 37, 0.3 | 1402, 768.1 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 14, 18.5 |

Memory held, against before the screen opened: its data alone, 0.01 MB; open and still, 0.45 MB; after the script and the screen closed, 0.40 MB.

</details>

<details>
<summary>Views that say they changed</summary>

#### "Hello, World!"

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 1 | 1, 0.348 (0.326–0.470) | 1 | 4 | 1 | 4 | 4 / 4 (100.0 %) | 0 of 4 |
| its button pressed | 1 | 1, 0.094 (0.089–0.114) | 0 | 1 | 0 | 1 | 0 / 4 (0.0 %) | 0 of 4 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 4 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.005 (0.005–0.026) | 0.248 (0.235–0.285) | 0.089 (0.084–0.193) | 0.002 (0.002–0.003) | 0.348 (0.326–0.470) |
| its button pressed | 0.002 (0.002–0.005) | 0.008 (0.007–0.027) | 0.083 (0.078–0.094) | 0.000 (0.000–0.000) | 0.002 (0.002–0.002) | 0.094 (0.089–0.114) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.001 (0.000–0.005) | 0.000 (0.000–0.000) | 0.001 (0.000–0.001) | 0.002 (0.001–0.006) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 22, 24.6 | 4501, 242.3 | 408, 87.1 | 34, 3.1 |
| its button pressed | 3, 0.2 | 0, 0.0 | 1408, 68.6 | 1, 0.0 | 18, 1.8 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 6, 0.7 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.07 MB; after the script and the screen closed, 0.06 MB.

#### Slatty's library

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.393 (2.308–3.221) | 3 | 320 | 2 | 320 | 218 / 225 (96.9 %) | 0 of 218 |
| scrolled, 16 logical pixels a frame | 1200 | 1, 0.096 (0.092–0.110) | 181 | 4276 | 181 | 412560 | 275340 / 283453 (97.1 %) | 0 of 247 |
| the filter focused by Tab | 1 | 1, 0.030 (0.029–0.039) | 0 | 1 | 0 | 1 | 1 / 248 (0.4 %) | 0 of 248 |
| a filter typed, a character a frame | 5 | 1, 2.067 (2.006–2.796) | 9 | 1020 | 5 | 1028 | 692 / 720 (96.1 %) | 0 of 208 |
| the grid focused by Tab | 1 | 1, 0.028 (0.027–0.036) | 0 | 3 | 0 | 2 | 0 / 207 (0.0 %) | 0 of 207 |
| the selection moved by the arrows | 39 | 1, 0.920 (0.892–1.031) | 6 | 320 | 3 | 427 | 248 / 8500 (2.9 %) | 0 of 218 |
| a game's page opened, its key art fading in | 45 | 1, 0.620 (0.607–0.704) | 2 | 5 | 1 | 48 | 49 / 10035 (0.5 %) | 0 of 223 |
| the page closed | 1 | 1, 0.246 (0.236–0.314) | 2 | 1 | 1 | 0 | 0 / 218 (0.0 %) | 0 of 218 |
| the theme changed | 37 | 1, 0.881 (0.864–0.972) | 2 | 320 | 0 | 11840 | 3924 / 8066 (48.6 %) | 0 of 218 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 218 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.265 (0.220–0.966) | 0.564 (0.545–0.615) | 1.456 (1.419–1.599) | 0.117 (0.110–0.145) | 2.393 (2.308–3.221) |
| scrolled, 16 logical pixels a frame | 3.468 (3.431–3.968) | 34.912 (34.257–37.187) | 3.086 (3.010–3.228) | 35.062 (34.415–36.939) | 106.145 (104.298–109.592) | 182.406 (179.413–190.425) |
| the filter focused by Tab | 0.005 (0.005–0.009) | 0.000 (0.000–0.000) | 0.003 (0.002–0.004) | 0.000 (0.000–0.000) | 0.022 (0.021–0.030) | 0.030 (0.029–0.039) |
| a filter typed, a character a frame | 0.051 (0.049–0.056) | 3.224 (3.161–3.970) | 0.355 (0.327–0.408) | 2.451 (2.414–2.622) | 0.313 (0.293–0.363) | 6.415 (6.297–7.252) |
| the grid focused by Tab | 0.006 (0.005–0.007) | 0.001 (0.001–0.001) | 0.004 (0.003–0.005) | 0.000 (0.000–0.000) | 0.017 (0.016–0.023) | 0.028 (0.027–0.036) |
| the selection moved by the arrows | 0.003 (0.003–0.005) | 0.606 (0.580–0.746) | 0.123 (0.117–0.146) | 0.589 (0.579–0.634) | 0.550 (0.524–0.615) | 1.879 (1.807–2.146) |
| a game's page opened, its key art fading in | 0.002 (0.002–0.003) | 0.183 (0.175–0.241) | 0.302 (0.285–0.373) | 0.142 (0.138–0.159) | 0.558 (0.523–0.724) | 1.188 (1.138–1.374) |
| the page closed | 0.001 (0.001–0.001) | 0.180 (0.172–0.235) | 0.003 (0.003–0.004) | 0.048 (0.046–0.060) | 0.014 (0.013–0.016) | 0.246 (0.236–0.314) |
| the theme changed | 0.002 (0.002–0.011) | 0.181 (0.175–0.213) | 2.398 (2.340–2.923) | 0.003 (0.002–0.004) | 3.310 (3.094–4.637) | 5.895 (5.657–7.759) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.001 (0.000–0.001) | 0.000 (0.000–0.000) | 0.014 (0.013–0.020) | 0.015 (0.014–0.022) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1231, 3283.0 | 8756, 471.6 | 8470, 915.6 | 1723, 257.1 |
| scrolled, 16 logical pixels a frame | 1201, 38.4 | 211046, 133283.5 | 4614, 236.4 | 161883, 43431.6 | 2106546, 291652.8 |
| the filter focused by Tab | 14, 5.0 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 53, 87.5 |
| a filter typed, a character a frame | 207, 23.6 | 44053, 6095.1 | 1023, 19.0 | 19512, 1399.7 | 5345, 731.6 |
| the grid focused by Tab | 18, 4.8 | 0, 0.0 | 4, 0.1 | 1, 0.0 | 48, 79.0 |
| the selection moved by the arrows | 6, 0.8 | 3440, 2248.2 | 702, 87.5 | 6084, 374.7 | 2587, 3178.4 |
| a game's page opened, its key art fading in | 3, 0.3 | 1126, 689.2 | 4555, 272.3 | 506, 56.0 | 971, 3503.6 |
| the page closed | 5, 0.3 | 1109, 682.2 | 3, 0.9 | 183, 31.8 | 18, 77.2 |
| the theme changed | 8, 0.3 | 1109, 682.2 | 44004, 8718.4 | 37, 0.3 | 61010, 8512.0 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 18, 77.2 |

Memory held, against before the screen opened: its data alone, 0.65 MB; open and still, 2.61 MB; after the script and the screen closed, 6.43 MB.

#### Opium's songs

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.621 (2.554–2.842) | 4 | 218 | 2 | 218 | 169 / 181 (93.4 %) | 0 of 169 |
| scrolled from end to end, 16 logical pixels a frame | 27625 | 1, 0.330 (0.313–0.383) | 16948 | 67792 | 16948 | 5881272 | 4412940 / 4755405 (92.8 %) | 0 of 168 |
| a column sorted by a click on its header | 37 | 1, 2.539 (2.280–3.501) | 2 | 1 | 1 | 193 | 171 / 6216 (2.8 %) | 0 of 168 |
| the table focused by Tab, from the header | 3 | 1, 0.015 (0.015–0.026) | 0 | 6 | 0 | 3 | 0 / 504 (0.0 %) | 0 of 168 |
| the selection moved by the arrows | 39 | 1, 1.597 (1.497–2.299) | 6 | 212 | 1 | 320 | 265 / 6661 (4.0 %) | 0 of 169 |
| the theme changed | 37 | 1, 1.336 (1.291–1.496) | 2 | 218 | 0 | 8066 | 5076 / 6253 (81.2 %) | 0 of 169 |
| a song played by Enter | 37 | 1, 0.302 (0.289–0.364) | 39 | 8 | 1 | 75 | 39 / 6253 (0.6 %) | 0 of 169 |
| each frame while a song plays, its wave moving | 240 | 1, 0.010 (0.010–0.042) | 240 | 0 | 0 | 240 | 11 / 40671 (0.0 %) | 0 of 170 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 169 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.223 (0.202–0.328) | 0.886 (0.848–0.970) | 1.379 (1.339–1.495) | 0.132 (0.126–0.138) | 2.621 (2.554–2.842) |
| scrolled from end to end, 16 logical pixels a frame | 46.988 (45.524–55.949) | 2112.932 (2062.650–2253.293) | 60.259 (58.280–66.547) | 976.332 (957.462–1058.192) | 2396.983 (2354.497–2525.537) | 5598.537 (5480.185–5959.518) |
| a column sorted by a click on its header | 0.014 (0.014–0.021) | 1.390 (1.162–2.273) | 0.140 (0.136–0.158) | 0.803 (0.782–0.895) | 0.530 (0.506–0.589) | 2.888 (2.617–3.847) |
| the table focused by Tab, from the header | 0.008 (0.008–0.016) | 0.000 (0.000–0.001) | 0.004 (0.004–0.005) | 0.000 (0.000–0.000) | 0.027 (0.026–0.041) | 0.040 (0.039–0.057) |
| the selection moved by the arrows | 0.003 (0.003–0.004) | 0.535 (0.502–1.174) | 0.117 (0.096–0.134) | 1.040 (0.999–1.159) | 0.528 (0.506–0.590) | 2.233 (2.114–2.989) |
| the theme changed | 0.002 (0.002–0.003) | 0.129 (0.125–0.155) | 2.334 (2.257–2.666) | 0.003 (0.002–0.005) | 5.968 (5.723–6.759) | 8.437 (8.110–9.563) |
| a song played by Enter | 0.002 (0.002–0.003) | 0.194 (0.187–0.249) | 0.099 (0.095–0.119) | 0.067 (0.065–0.086) | 0.323 (0.298–0.395) | 0.689 (0.652–0.828) |
| each frame while a song plays, its wave moving | 0.006 (0.006–0.007) | 0.350 (0.328–0.533) | 0.023 (0.021–0.040) | 0.012 (0.011–0.022) | 1.994 (1.869–2.550) | 2.385 (2.236–3.151) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.001 (0.000–0.001) | 0.000 (0.000–0.000) | 0.010 (0.010–0.018) | 0.011 (0.011–0.019) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1015, 1838.6 | 16968, 929.0 | 9662, 969.0 | 1805, 270.1 |
| scrolled from end to end, 16 logical pixels a frame | 27542, 881.3 | 15159988, 8503130.3 | 84740, 4677.6 | 5552861, 724808.4 | 43962991, 5669253.5 |
| a column sorted by a click on its header | 3, 0.2 | 914, 639.3 | 1384, 91.6 | 6323, 429.6 | 3439, 2944.8 |
| the table focused by Tab, from the header | 30, 2.7 | 0, 0.0 | 6, 0.1 | 3, 0.0 | 83, 217.5 |
| the selection moved by the arrows | 6, 0.8 | 2827, 2839.8 | 591, 81.9 | 8050, 619.0 | 3699, 3101.5 |
| the theme changed | 8, 0.3 | 912, 503.3 | 42296, 6553.8 | 37, 0.3 | 98414, 12292.2 |
| a song played by Enter | 3, 0.3 | 1251, 796.5 | 1386, 89.1 | 287, 25.2 | 1009, 2710.3 |
| each frame while a song plays, its wave moving | 0, 0.0 | 2160, 1900.3 | 0, 0.0 | 240, 1.9 | 5520, 17438.6 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 19, 71.7 |

Memory held, against before the screen opened: its data alone, 1.39 MB; open and still, 2.61 MB; after the script and the screen closed, 38.79 MB.

#### A document of 100,000 lines

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 1.512 (1.426–1.607) | 3 | 74 | 2 | 74 | 75 / 78 (96.2 %) | 0 of 75 |
| a line that shows changed | 1 | 1, 0.075 (0.070–0.082) | 2 | 0 | 1 | 1 | 1 / 75 (1.3 %) | 0 of 75 |
| a line that does not show changed | 1 | 1, 0.045 (0.044–0.066) | 2 | 0 | 0 | 0 | 0 / 75 (0.0 %) | 0 of 75 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 75 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.001) | 0.077 (0.062–0.087) | 0.221 (0.197–0.249) | 1.162 (1.118–1.279) | 0.049 (0.045–0.052) | 1.512 (1.426–1.607) |
| a line that shows changed | 0.000 (0.000–0.000) | 0.047 (0.043–0.052) | 0.000 (0.000–0.000) | 0.021 (0.021–0.025) | 0.005 (0.005–0.006) | 0.075 (0.070–0.082) |
| a line that does not show changed | 0.000 (0.000–0.000) | 0.041 (0.040–0.060) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.004 (0.004–0.007) | 0.045 (0.044–0.066) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.004 (0.003–0.014) | 0.005 (0.004–0.016) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 324, 803.0 | 3205, 174.7 | 3127, 753.5 | 754, 107.1 |
| a line that shows changed | 0, 0.0 | 247, 164.7 | 0, 0.0 | 119, 11.7 | 23, 37.1 |
| a line that does not show changed | 0, 0.0 | 246, 164.7 | 0, 0.0 | 1, 0.0 | 13, 36.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 13, 36.4 |

Memory held, against before the screen opened: its data alone, 10.75 MB; open and still, 11.73 MB; after the script and the screen closed, 0.92 MB.

#### A notify forgotten

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 0.629 (0.619–0.667) | 3 | 47 | 2 | 47 | 49 / 52 (94.2 %) | 0 of 49 |
| the list focused by Tab | 1 | 1, 0.005 (0.005–0.010) | 0 | 1 | 0 | 1 | 0 / 49 (0.0 %) | 0 of 49 |
| the selection moved by an arrow | 1 | 1, 0.004 (0.004–0.010) | 0 | 0 | 0 | 0 | 0 / 49 (0.0 %) | 2 of 49 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 49 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.036 (0.036–0.051) | 0.241 (0.236–0.250) | 0.323 (0.317–0.345) | 0.026 (0.025–0.027) | 0.629 (0.619–0.667) |
| the list focused by Tab | 0.001 (0.001–0.002) | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.002 (0.002–0.006) | 0.005 (0.005–0.010) |
| the selection moved by an arrow | 0.001 (0.001–0.002) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.002 (0.002–0.005) | 0.004 (0.004–0.010) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.003 (0.002–0.004) | 0.004 (0.003–0.005) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 219, 424.3 | 4198, 231.2 | 1852, 295.9 | 481, 55.3 |
| the list focused by Tab | 7, 0.5 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 14, 18.4 |
| the selection moved by an arrow | 2, 0.3 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 12, 18.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 12, 18.4 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.43 MB; after the script and the screen closed, 0.39 MB.

#### A view within a view changed without its own notify

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 0.735 (0.722–0.760) | 4 | 50 | 2 | 50 | 50 / 54 (92.6 %) | 0 of 50 |
| the list focused by Tab | 1 | 1, 0.005 (0.005–0.006) | 0 | 1 | 0 | 1 | 0 / 50 (0.0 %) | 0 of 50 |
| the row selected played by Enter | 1 | 1, 0.004 (0.004–0.012) | 0 | 0 | 0 | 0 | 0 / 50 (0.0 %) | 1 of 50 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 50 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.041 (0.040–0.048) | 0.299 (0.295–0.314) | 0.364 (0.357–0.381) | 0.028 (0.027–0.034) | 0.735 (0.722–0.760) |
| the list focused by Tab | 0.001 (0.001–0.002) | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.003 (0.002–0.003) | 0.005 (0.005–0.006) |
| the row selected played by Enter | 0.001 (0.001–0.002) | 0.001 (0.001–0.002) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.002 (0.002–0.010) | 0.004 (0.004–0.012) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.003 (0.003–0.007) | 0.004 (0.004–0.008) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 231, 437.9 | 5189, 285.4 | 2010, 313.2 | 496, 56.2 |
| the list focused by Tab | 8, 0.5 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 16, 18.5 |
| the row selected played by Enter | 3, 0.3 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 14, 18.5 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 14, 18.5 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.44 MB; after the script and the screen closed, 0.40 MB.

</details>

<details>
<summary>Messages</summary>

#### "Hello, World!"

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 1 | 1, 0.335 (0.317–0.436) | 1 | 4 | 1 | 4 | 4 / 4 (100.0 %) | 0 of 4 |
| its button pressed | 1 | 1, 0.098 (0.093–0.148) | 1 | 1 | 0 | 1 | 0 / 4 (0.0 %) | 0 of 4 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 4 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.005 (0.005–0.023) | 0.240 (0.226–0.272) | 0.086 (0.083–0.176) | 0.002 (0.002–0.003) | 0.335 (0.317–0.436) |
| its button pressed | 0.002 (0.002–0.004) | 0.012 (0.012–0.023) | 0.082 (0.077–0.131) | 0.000 (0.000–0.000) | 0.002 (0.002–0.002) | 0.098 (0.093–0.148) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.004) | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.001 (0.001–0.006) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 21, 20.9 | 4501, 242.3 | 408, 87.1 | 34, 3.1 |
| its button pressed | 3, 0.2 | 18, 4.8 | 1408, 68.6 | 1, 0.0 | 18, 1.8 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 6, 0.7 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.07 MB; after the script and the screen closed, 0.06 MB.

#### Slatty's library

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.306 (2.241–3.154) | 107 | 320 | 2 | 320 | 218 / 225 (96.9 %) | 0 of 218 |
| scrolled, 16 logical pixels a frame | 1200 | 1, 0.092 (0.089–0.116) | 20551 | 4276 | 181 | 412560 | 275340 / 283453 (97.1 %) | 0 of 247 |
| the filter focused by Tab | 1 | 1, 0.028 (0.027–0.049) | 0 | 1 | 0 | 1 | 1 / 248 (0.4 %) | 0 of 248 |
| a filter typed, a character a frame | 5 | 1, 2.011 (1.879–2.971) | 345 | 1020 | 5 | 1028 | 692 / 720 (96.1 %) | 0 of 208 |
| the grid focused by Tab | 1 | 1, 0.026 (0.025–0.057) | 0 | 3 | 0 | 2 | 0 / 207 (0.0 %) | 0 of 207 |
| the selection moved by the arrows | 39 | 1, 0.877 (0.857–1.335) | 318 | 320 | 3 | 427 | 248 / 8500 (2.9 %) | 0 of 218 |
| a game's page opened, its key art fading in | 45 | 1, 0.579 (0.560–0.701) | 106 | 5 | 1 | 48 | 49 / 10035 (0.5 %) | 0 of 223 |
| the page closed | 1 | 1, 0.217 (0.209–0.295) | 106 | 1 | 1 | 0 | 0 / 218 (0.0 %) | 0 of 218 |
| the theme changed | 37 | 1, 0.845 (0.826–0.944) | 106 | 320 | 0 | 11840 | 3924 / 8066 (48.6 %) | 0 of 218 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 218 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.244 (0.213–0.728) | 0.543 (0.525–0.609) | 1.407 (1.379–1.640) | 0.112 (0.108–0.177) | 2.306 (2.241–3.154) |
| scrolled, 16 logical pixels a frame | 3.303 (3.243–3.692) | 30.132 (29.646–31.097) | 2.861 (2.812–2.980) | 33.489 (33.003–34.938) | 101.767 (99.954–105.363) | 171.565 (168.686–178.069) |
| the filter focused by Tab | 0.005 (0.005–0.009) | 0.000 (0.000–0.001) | 0.003 (0.002–0.005) | 0.000 (0.000–0.000) | 0.021 (0.020–0.035) | 0.028 (0.027–0.049) |
| a filter typed, a character a frame | 0.049 (0.047–0.061) | 3.001 (2.929–3.904) | 0.346 (0.263–0.416) | 2.380 (2.312–2.545) | 0.296 (0.287–0.350) | 6.076 (5.843–7.051) |
| the grid focused by Tab | 0.006 (0.005–0.015) | 0.001 (0.001–0.002) | 0.004 (0.003–0.007) | 0.000 (0.000–0.000) | 0.016 (0.015–0.033) | 0.026 (0.025–0.057) |
| the selection moved by the arrows | 0.003 (0.003–0.006) | 0.534 (0.517–0.804) | 0.120 (0.115–0.255) | 0.567 (0.551–0.675) | 0.510 (0.485–0.552) | 1.731 (1.696–2.292) |
| a game's page opened, its key art fading in | 0.002 (0.002–0.004) | 0.156 (0.149–0.247) | 0.295 (0.285–0.309) | 0.135 (0.130–0.163) | 0.514 (0.491–0.581) | 1.105 (1.068–1.278) |
| the page closed | 0.001 (0.001–0.002) | 0.153 (0.148–0.216) | 0.003 (0.003–0.009) | 0.045 (0.044–0.057) | 0.013 (0.013–0.022) | 0.217 (0.209–0.295) |
| the theme changed | 0.002 (0.002–0.003) | 0.153 (0.146–0.193) | 2.342 (2.289–2.653) | 0.003 (0.003–0.004) | 3.194 (3.118–3.535) | 5.695 (5.616–6.386) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.013 (0.013–0.029) | 0.014 (0.014–0.031) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1242, 3097.6 | 8756, 471.6 | 8470, 915.6 | 1723, 257.1 |
| scrolled, 16 logical pixels a frame | 1201, 38.4 | 213037, 97842.9 | 4614, 236.4 | 161883, 43431.6 | 2106546, 291652.8 |
| the filter focused by Tab | 14, 5.0 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 53, 87.5 |
| a filter typed, a character a frame | 207, 23.6 | 44073, 5474.0 | 1023, 19.0 | 19512, 1399.7 | 5345, 731.6 |
| the grid focused by Tab | 18, 4.8 | 0, 0.0 | 4, 0.1 | 1, 0.0 | 48, 79.0 |
| the selection moved by the arrows | 6, 0.8 | 3443, 1667.0 | 702, 87.5 | 6084, 374.7 | 2587, 3178.4 |
| a game's page opened, its key art fading in | 3, 0.3 | 1126, 495.5 | 4555, 272.3 | 506, 56.0 | 971, 3503.6 |
| the page closed | 5, 0.3 | 1110, 488.4 | 3, 0.9 | 183, 31.8 | 18, 77.2 |
| the theme changed | 8, 0.3 | 1110, 488.4 | 44004, 8718.4 | 37, 0.3 | 61010, 8512.0 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 18, 77.2 |

Memory held, against before the screen opened: its data alone, 0.65 MB; open and still, 2.61 MB; after the script and the screen closed, 6.43 MB.

#### Opium's songs

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 2.574 (2.464–2.675) | 30 | 218 | 2 | 218 | 169 / 181 (93.4 %) | 0 of 169 |
| scrolled from end to end, 16 logical pixels a frame | 27625 | 1, 0.288 (0.270–0.325) | 483018 | 67792 | 16948 | 5881272 | 4412940 / 4755405 (92.8 %) | 0 of 168 |
| a column sorted by a click on its header | 37 | 1, 2.436 (2.206–2.573) | 28 | 1 | 1 | 193 | 171 / 6216 (2.8 %) | 0 of 168 |
| the table focused by Tab, from the header | 3 | 1, 0.015 (0.014–0.025) | 0 | 6 | 0 | 3 | 0 / 504 (0.0 %) | 0 of 168 |
| the selection moved by the arrows | 39 | 1, 1.546 (1.466–1.646) | 84 | 212 | 1 | 320 | 265 / 6661 (4.0 %) | 0 of 169 |
| the theme changed | 37 | 1, 1.212 (1.172–1.270) | 1 | 218 | 0 | 8066 | 5076 / 6253 (81.2 %) | 0 of 169 |
| a song played by Enter | 37 | 1, 0.284 (0.271–0.323) | 64 | 8 | 1 | 75 | 39 / 6253 (0.6 %) | 0 of 169 |
| each frame while a song plays, its wave moving | 240 | 1, 0.014 (0.013–0.026) | 240 | 0 | 0 | 240 | 11 / 40671 (0.0 %) | 0 of 170 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 169 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.001) | 0.218 (0.192–0.266) | 0.863 (0.829–0.925) | 1.362 (1.295–1.431) | 0.128 (0.124–0.139) | 2.574 (2.464–2.675) |
| scrolled from end to end, 16 logical pixels a frame | 45.387 (44.241–52.907) | 1874.705 (1859.498–1946.747) | 56.285 (54.858–60.105) | 937.780 (922.345–1005.262) | 2307.635 (2281.710–2415.539) | 5224.382 (5172.208–5480.559) |
| a column sorted by a click on its header | 0.014 (0.013–0.016) | 1.336 (1.139–1.430) | 0.136 (0.133–0.162) | 0.777 (0.734–0.820) | 0.498 (0.486–0.556) | 2.747 (2.518–2.907) |
| the table focused by Tab, from the header | 0.008 (0.008–0.010) | 0.000 (0.000–0.001) | 0.004 (0.004–0.006) | 0.000 (0.000–0.000) | 0.025 (0.024–0.037) | 0.038 (0.036–0.054) |
| the selection moved by the arrows | 0.003 (0.003–0.004) | 0.497 (0.471–0.532) | 0.111 (0.091–0.136) | 1.004 (0.972–1.063) | 0.497 (0.482–0.580) | 2.111 (2.021–2.240) |
| the theme changed | 0.002 (0.002–0.002) | 0.012 (0.011–0.022) | 2.329 (2.272–2.503) | 0.003 (0.003–0.003) | 5.902 (5.737–6.033) | 8.250 (8.028–8.564) |
| a song played by Enter | 0.002 (0.002–0.003) | 0.311 (0.295–0.360) | 0.101 (0.093–0.121) | 0.065 (0.064–0.088) | 0.324 (0.308–0.386) | 0.797 (0.774–0.933) |
| each frame while a song plays, its wave moving | 0.006 (0.006–0.007) | 1.229 (1.166–1.434) | 0.026 (0.022–0.042) | 0.010 (0.010–0.015) | 1.995 (1.905–2.444) | 3.274 (3.148–3.942) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.007) | 0.000 (0.000–0.000) | 0.010 (0.009–0.015) | 0.011 (0.010–0.018) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 1041, 1802.2 | 16968, 929.0 | 9662, 969.0 | 1805, 270.1 |
| scrolled from end to end, 16 logical pixels a frame | 27542, 881.3 | 15532844, 7988487.3 | 84740, 4677.6 | 5552861, 724808.4 | 43962991, 5669253.5 |
| a column sorted by a click on its header | 3, 0.2 | 926, 597.8 | 1384, 91.6 | 6323, 429.6 | 3439, 2944.8 |
| the table focused by Tab, from the header | 30, 2.7 | 0, 0.0 | 6, 0.1 | 3, 0.0 | 83, 217.5 |
| the selection moved by the arrows | 6, 0.8 | 2863, 2715.4 | 591, 81.9 | 8050, 619.0 | 3699, 3101.5 |
| the theme changed | 8, 0.3 | 41, 13.9 | 42295, 6553.6 | 37, 0.3 | 98414, 12292.2 |
| a song played by Enter | 3, 0.3 | 2479, 963.7 | 1386, 89.1 | 287, 25.2 | 1009, 2710.3 |
| each frame while a song plays, its wave moving | 0, 0.0 | 10320, 3344.4 | 0, 0.0 | 240, 1.9 | 5520, 17438.6 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 19, 71.7 |

Memory held, against before the screen opened: its data alone, 1.39 MB; open and still, 2.61 MB; after the script and the screen closed, 38.79 MB.

#### A document of 100,000 lines

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 1.504 (1.424–1.657) | 74 | 74 | 2 | 74 | 75 / 78 (96.2 %) | 0 of 75 |
| a line that shows changed | 1 | 1, 0.064 (0.061–0.080) | 73 | 0 | 1 | 1 | 1 / 75 (1.3 %) | 0 of 75 |
| a line that does not show changed | 1 | 1, 0.037 (0.036–0.058) | 73 | 0 | 0 | 0 | 0 / 75 (0.0 %) | 0 of 75 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 75 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.071 (0.057–0.085) | 0.216 (0.199–0.244) | 1.165 (1.114–1.289) | 0.049 (0.046–0.055) | 1.504 (1.424–1.657) |
| a line that shows changed | 0.000 (0.000–0.001) | 0.038 (0.035–0.046) | 0.000 (0.000–0.000) | 0.021 (0.020–0.027) | 0.005 (0.005–0.006) | 0.064 (0.061–0.080) |
| a line that does not show changed | 0.000 (0.000–0.000) | 0.033 (0.032–0.052) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.004 (0.003–0.006) | 0.037 (0.036–0.058) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.004 (0.003–0.014) | 0.005 (0.004–0.016) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 327, 663.9 | 3205, 174.7 | 3127, 753.5 | 754, 107.1 |
| a line that shows changed | 0, 0.0 | 248, 25.6 | 0, 0.0 | 119, 11.7 | 23, 37.1 |
| a line that does not show changed | 0, 0.0 | 247, 25.5 | 0, 0.0 | 1, 0.0 | 13, 36.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 13, 36.4 |

Memory held, against before the screen opened: its data alone, 10.75 MB; open and still, 11.73 MB; after the script and the screen closed, 0.92 MB.

#### A lazy value that leaves out the row playing

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 0.631 (0.619–0.689) | 49 | 47 | 2 | 47 | 49 / 52 (94.2 %) | 0 of 49 |
| the list focused by Tab | 1 | 1, 0.005 (0.005–0.007) | 0 | 1 | 0 | 1 | 0 / 49 (0.0 %) | 0 of 49 |
| the row selected played by Enter | 1 | 1, 0.006 (0.006–0.013) | 1 | 0 | 0 | 0 | 0 / 49 (0.0 %) | 1 of 49 |
| A frame where nothing changed | 1 | — | 0 | 0 | 0 | 0 | 0 / 49 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.037 (0.035–0.048) | 0.239 (0.233–0.255) | 0.325 (0.321–0.369) | 0.025 (0.025–0.030) | 0.631 (0.619–0.689) |
| the list focused by Tab | 0.001 (0.001–0.003) | 0.000 (0.000–0.000) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.002 (0.002–0.003) | 0.005 (0.005–0.007) |
| the row selected played by Enter | 0.001 (0.001–0.002) | 0.003 (0.003–0.004) | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.002 (0.002–0.006) | 0.006 (0.006–0.013) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.000 (0.000–0.000) | 0.000 (0.000–0.001) | 0.000 (0.000–0.000) | 0.003 (0.002–0.003) | 0.004 (0.003–0.005) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 227, 336.5 | 4198, 231.2 | 1852, 295.9 | 481, 55.3 |
| the list focused by Tab | 7, 0.5 | 0, 0.0 | 1, 0.0 | 1, 0.0 | 14, 18.4 |
| the row selected played by Enter | 3, 0.3 | 9, 0.6 | 0, 0.0 | 1, 0.0 | 12, 18.4 |
| A frame where nothing changed | 0, 0.0 | 0, 0.0 | 0, 0.0 | 1, 0.0 | 12, 18.4 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.43 MB; after the script and the screen closed, 0.39 MB.

#### Frames not given up

| Interaction | Frames | Delay: frames, CPU ms | Code run | Elements styled | Layouts | Elements drawn again | Items changed / all | Items wrong |
|---|---|---|---|---|---|---|---|---|
| opened | 2 | 2, 0.641 (0.629–0.679) | 47 | 47 | 2 | 47 | 49 / 52 (94.2 %) | 0 of 49 |
| the list focused by Tab | 1 | 1, 0.026 (0.026–0.035) | 46 | 1 | 0 | 1 | 0 / 49 (0.0 %) | 0 of 49 |
| the selection moved by an arrow | 37 | 1, 0.028 (0.028–0.035) | 1702 | 2 | 0 | 74 | 71 / 1848 (3.8 %) | 0 of 49 |
| A frame where nothing changed | 1 | — | 46 | 0 | 0 | 0 | 0 / 49 | — |

Processor time of each phase, in ms, the median of 21 runs (range):

| Interaction | input | application | styles | layout | display list | Whole |
|---|---|---|---|---|---|---|
| opened | 0.000 (0.000–0.000) | 0.036 (0.035–0.044) | 0.243 (0.234–0.282) | 0.333 (0.328–0.347) | 0.026 (0.025–0.027) | 0.641 (0.629–0.679) |
| the list focused by Tab | 0.001 (0.001–0.002) | 0.021 (0.021–0.030) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.003 (0.003–0.003) | 0.026 (0.026–0.035) |
| the selection moved by an arrow | 0.002 (0.002–0.002) | 0.758 (0.743–0.780) | 0.025 (0.024–0.027) | 0.002 (0.002–0.003) | 0.123 (0.119–0.147) | 0.910 (0.892–0.942) |
| A frame where nothing changed | 0.000 (0.000–0.000) | 0.025 (0.024–0.030) | 0.001 (0.001–0.001) | 0.000 (0.000–0.000) | 0.003 (0.003–0.011) | 0.028 (0.028–0.039) |

Allocations of each phase, and the kB that they took:

| Interaction | input | application | styles | layout | display list |
|---|---|---|---|---|---|
| opened | 0, 0.0 | 233, 337.1 | 4198, 231.2 | 1852, 295.9 | 481, 55.3 |
| the list focused by Tab | 7, 0.5 | 166, 12.6 | 2, 0.4 | 1, 0.0 | 14, 18.4 |
| the selection moved by an arrow | 2, 0.3 | 6142, 467.8 | 295, 64.5 | 37, 0.3 | 1328, 763.9 |
| A frame where nothing changed | 0, 0.0 | 166, 12.6 | 1, 0.4 | 1, 0.0 | 12, 18.4 |

Memory held, against before the screen opened: its data alone, 0.00 MB; open and still, 0.43 MB; after the script and the screen closed, 0.39 MB.

</details>

## Signals named across a reload (2026-11-07)

Signals' state kept across a reload of its type, on the bench of SlimeEngine's milestone M6d.1c1
([ADR-0210](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0210-signals-named-for-a-reload.md)).
On [M6d.1b's bench](#the-reloads-and-a-task-cancelled-with-its-component), signals replayed in the
order that they were made lost the selection and the page when a signal was added before the
others. Now an author names the signals whose state a reload keeps,
`RwSignal::kept("selected", || 0)`. Each kept value is written through `serde` into a
`serde_json::Value` by its scope's path and its name. The signal of that name then reads it into
its type as the new code has it. A signal not named starts again.

A scope's path is the keys, from the window's root, of the element that made it. Only rows and
dynamic views make scopes; the root's holds the rest. A grid's cells are keyed by their items, a
list's rows and an element's children by their places.

The prototype goes on from M6d.1b's, on the branch
[`m6d1c-bench`](https://github.com/HoneySlatt/SlimeEngine/tree/m6d1c-bench/benches/src/prototypes),
thrown away once M6d.1 ends. The bench's comparison with a new interface still replays the root
scope's signals in their order: it runs the same function again, a tool of the bench and not the
model's reload. It copies a value that holds signals with their handles, which name the same
signals in the new interface only when both made them in the same places of their arenas.

- Machine: AMD Ryzen 7 5800X, 32 GB, Linux 7.3; the bench pinned to one core, the machine at
  rest.
- Build: release, SlimeEngine's branch `m6d1c-bench` at `72ca87e`.
- Command: `taskset -c 6 target/release/slime-benches --prototypes --reloads`, after
  `cargo build --locked --release -p slime-benches`.
- Each time: the median of 21 runs, with their range. Each count: the same in all 21 runs.
- The runtime notes what a reload could not keep: the tests read the notes, and `--reloads`
  fails on any.

### The state kept

Each case is a test on the branch: `signals/library/reload.rs` on Slatty's library, its grid
scrolled, a filter typed, the selection moved and a game's page open; `signals/kept.rs` apart.

| Change reloaded | What is kept | What the reload says |
|---|---|---|
| A body: the field's placeholder changed | All: scroll, selection, the field's text, the filter, the page | Nothing |
| A signal added before the others, which lost the state on M6d.1b's bench | All | Nothing |
| A signal renamed, `selected` to `cursor` | All but the selection, which starts again | `` `selected` at [] taken by no signal `` |
| The page's type changed, a place to a title | All but the page, which starts again: closed | `` `page` started again: invalid type: integer `…`, expected a string `` |
| A kept struct gains a field, `#[serde(default)]` | Its other fields; the new one at its default | Nothing |
| A grid's cells reordered, each cell's own kept signal | Each cell's value, by its item | Nothing |
| A document's lines, a kept value that holds 100,000 signals, one edited | The edit | Nothing |
| A map keyed by pairs, which the form cannot write | Nothing: it starts again | `` `cells` not kept: key must be a string `` |
| A kept value that holds a signal, its other field's type changed | Nothing: it starts again; the signal that the failed read made is disposed | `` `panel` started again: … `` |
| An element added before two dynamic views, each keeping `open` | Each view takes the value that the one before it held at its place, without a word | `` `open` at [Index(0), Index(0)] taken by no signal ``: the value left where no scope is now |
| Two signals named alike in one scope | A panic at the first run: `` two signals named `page` in one scope `` | — |
| A part that keeps a signal, used twice in one scope | The same panic, `` two signals named `count` in one scope ``: the part is no scope of its own | — |

### The reload's time

From the reload's call to the frame that shows it, settled, in the program, without a window. Not
the compiler's part: `subsecond`'s, which M6d.1c3 times. The call writes the kept values, disposes
the view before, runs the new one, and reads the kept values back. The frames mount the view over
the tree, whose elements keep their state by their keys, then style, lay out and draw.

| Screen | Kept | The call: ms, allocations, kB | Frames until still | Their phases: ms, allocations, kB | Whole: ms |
|---|---|---|---|---|---|
| Slatty's library, its page open | 4 signals | 0.139 (0.135–0.200), 51, 17.1 | 1 | 0.765 (0.741–0.777), 12,064, 1,259.2 | 0.903 (0.877–0.946) |
| A document of 100,000 lines, one edited | 1 value of 100,000 signals | 13.087 (12.666–28.865), 200,081, 61,771.0 | 1 | 0.133 (0.110–0.245), 1,134, 395.4 | 13.219 (12.800–29.073) |

The library's games are made before the reload, as a program's data loaded at its start, which a
reload does not load again. The document's lines are the kept value itself: each line is written,
read and made a signal again, some 130 ns and 2 allocations a line. A first timing, before the
review's changes at `09dd69d`, gave 0.881 ms and 14.983 ms, the same counts.

### What names cost the bench's screens

The signals' counts at `72ca87e` against `ae40506`, M6d.1b's, on every screen of the bench, two
runs each. The library's four signals and the document's lines are now kept; the songs' signals
are not named. The other phases, styles, layout and the display list, count the same.

| Screen | Interaction | The application's allocations, kB: before, after |
|---|---|---|
| Slatty's library | opened | 12,125, 4,223.4; 12,137, 4,236.2 |
| Slatty's library | scrolled | 31,742, 19,717.1; 31,743, 19,729.7 |
| Slatty's library | a filter typed | 46,712, 7,164.9; 46,713, 7,190.0 |
| Opium's songs | opened | 2,683, 2,113.6; 2,690, 2,116.7 |
| Opium's songs | scrolled from end to end | 1,186,364, 329,464.2; 1,186,365, 329,467.4 |
| A document of 100,000 lines | opened | 1,190, 984.7; 1,198, 997.2 |
| A signal read outside a closure that the view tracks | opened | 332, 539.1; 340, 545.4 |

The memory held while a screen is open is the same within 0.01 MB: the document's 38.04 MB against
38.03 MB, the small case's 0.46 MB against 0.45 MB. A first version kept each name and each scope's place in the graph's nodes: the document
held 2.1 MB more, some 21 bytes a signal. They now live in two maps beside the nodes, which only
named signals and scopes fill. The allocations more are those maps growing, a list's path and a
dynamic view's.

### What they say

- Names keep the state across every change that the bench makes but a rename, a type that no
  longer reads and a value that cannot be written, and the runtime notes those three.
- A scope's path follows the elements' keys, as the tree's own state does: an element added
  before a dynamic view, or a list's rows reordered, gives a kept value to another scope; only a
  value left where no scope is now is noted. A part used twice in one scope names its signals twice. Keys that views give, and a
  scope for each part that keeps state, would answer both: uwui's first stage decides them.
- The framework's part of a reload on Slatty's library is under 1 ms: the call 0.14 ms, the frame
  that shows it 0.77 ms. The time from a change saved to its frame is the compiler's, M6d.1c3's.
- A large kept value costs by its size: the 100,000 lines, 13 ms. Kept state that holds a
  program's data, rather than the interface's, is better loaded again by the program.
- A signal not named holds no more memory. Each list and dynamic view mounted, and each scope,
  costs a few allocations more as a screen opens, their path and the maps' growth, whether or not
  a signal is named: 7 to 12 on the bench's screens, and 1 over a whole scroll.

Not measured: the compiler's part of a reload; the owner's laptop; a reload on the web and on
Android, which M6d.1c3 weighs.

## The interface's executor, and other threads (2026-11-07)

The interface's tasks, and other threads' changes to signals, on the bench of SlimeEngine's
milestone M6d.1c2
([ADR-0211](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0211-the-executor-and-other-threads-through-channels.md)).
A task runs on the interface's thread, owned by the scope that started it and cancelled with it.
Its timers follow the frame's clock, and the host waits for the first one's deadline: no thread
of uwui's sleeps for them. Other threads hold a channel's sender, never a signal: a task of the
view receives and sets the signals. The application makes the channel before its view, so that a
reload's new view reads the same receiver.

The screen is Slatty's downloads: a list of 10,000 games, a signal for each game's progress, and a
label that counts the updates received. The core's thread sends one game's progress, or many
games' at once in a batch. The executor and the channel are written by hand on the standard
library, on the branch
[`m6d1c-bench`](https://github.com/HoneySlatt/SlimeEngine/tree/m6d1c-bench/benches/src/prototypes),
thrown away once M6d.1 ends.

- Machine: AMD Ryzen 7 5800X, 32 GB, Linux 7.3; the bench pinned to one core, the core's thread
  on the same core, the machine at rest.
- Build: release, SlimeEngine's branch `m6d1c-bench` at `ffe4aa5`.
- Command: `taskset -c 6 target/release/slime-benches --prototypes --threads`, after
  `cargo build --locked --release -p slime-benches`.
- Each time: the median of 21 runs, with their range. Each count: the same in all 21 runs, or
  the bench fails.
- The host waits as a window's loop would, on a condition variable that the executor's waker
  notifies. A real window adds its own wake, winit's proxy and the compositor's frame: M6d.7's.

### What the tests show

Each case is a test on the branch, in `signals/threads.rs` and `tasks.rs`.

| Case | What happens |
|---|---|
| A page that starts a task waiting an hour, closed | The task is dropped with the page's scope, and its timer forgotten: no deadline left |
| A task that sleeps 5 s | No frame runs while it waits; the host runs one frame at its deadline, which shows its change |
| A frame at rest while 1,000 tasks wait, on timers and channels | No task polled, no binding run, nothing allocated by the application, no wake of the host |
| 10,000 messages from another thread, sent before the frame | One wake of the host; all shown in the next frame |
| A batch of three games, one far below the rows that show | The batch's poll, the count's label and the two rows that show run; the third game's row is not mounted |
| Four threads sending 20,000 messages while frames run | All received, no wake lost, in 50 runs of 50 in a release build |
| More values waiting than a poll's budget of 16,384 | One budget a frame, the rest in the frames after |
| A reload, one message sent before it and one during it | Both received by the new view's task, the count kept by its name, the sender still valid |
| The last sender dropped during a reload | The new task receives what was sent, then ends |
| A channel made within a view, then the view reloaded | The old sender's send fails with `Closed` |
| A task that wakes itself at each poll | Polled once a frame, each frame asking the next |
| A task that cancels itself in its own poll | Dropped once its poll ends |
| A waker kept from a cancelled task, its place taken by a new task | Wakes nothing |
| The application closed while a task waits on a timer | The task is dropped |

### A change from another thread, to the frame that shows it

| Change | Frames until still | From the send to the frame: ms | The frame's phases: ms, allocations, kB | Code run | Host's wakes |
|---|---|---|---|---|---|
| One game's progress, the host waiting | 1 | 0.105 (0.098–0.134) | 0.080 (0.069–0.096), 247, 47.2 | 3 | 1 |
| 10,000 games' progress, as 10,000 messages | 1 | — | 0.715 (0.698–0.742), 2,435, 345.5 | 47 | 1 |
| 10,000 games' progress, as one batch | 1 | — | 0.480 (0.473–0.495), 2,433, 345.0 | 47 | 1 |

- *From the send to the frame*: from the core's send to the end of the frame's display list, the
  host woken from its wait. A run whose host did not wait yet as the change was sent is run
  again. The bursts are sent whole before the frame, so they have no such delay.
- *Code run*: the task's polls and the bindings run again. One change runs the task, the count's
  label and the game's row. A burst runs the task once, the count once, and each of the 46 rows
  that show but the first, whose progress stays 0.
- The frame's allocations are the tree's: styles, layout and the display list for the labels that
  changed. The batch takes 0.24 ms less than the 10,000 messages, each of which is received,
  applied and counted on its own.

### A frame at rest while tasks wait

| Tasks waiting | The frame: ms, allocations, kB | The application's part: ms, allocations | Code run | Host's wakes | Next deadline |
|---|---|---|---|---|---|
| None | 0.001 (0.001–0.001), 5, 0.6 | 0.001 (0.001–0.001), 0 | 0 | 0 | none |
| 500 on timers, 500 on channels | 0.001 (0.001–0.001), 5, 0.6 | 0.001 (0.001–0.001), 0 | 0 | 0 | 3,600 s |

A frame at rest runs only when something else asks for one: no task asks it. The 5 allocations
are the tree's own at a still frame, as on the bench's other screens. The application's part
allocates nothing, with or without tasks waiting. The host learns the first timer's deadline, an
hour away, and runs no frame before it.

### What tasks cost outside the frames

Counted once, in a test:

- the executor, made with the application: 5 allocations, 0.9 kB;
- a task spawned: 5 allocations, 0.3 kB, its future's box among them, and the cleanup that its
  scope runs;
- a task cancelled: 1 allocation, the free list growing.

The signals' runtime also changed: a change no longer clones the list of what reads the signal.
On the bench's screens, the application's allocations fell by 1 to 8 an interaction; nothing else
moved. Without it, the 10,000 messages cost some 10,000 allocations more.

### What they say

- A change from another thread shows in the next frame, its wake included, 0.1 ms after its
  send on this machine. A burst of 10,000 is taken whole in one frame, under 1 ms.
- Tasks that wait cost a frame nothing: no poll, no allocation, no wake.
- The core never holds a signal: what it sends is its own message, a batch or a key.
- The budget a poll and an unbounded channel are the prototype's: uwui's first stage sets both.
  Unbounded, what the core sends while no frame runs waits in memory.

Not measured: the owner's laptop; a real window's wake; tokio's channels, which the bench does
not depend on; a timer's frame against a real display's.

## A function's body reloaded through subsecond (2026-11-07)

Rust's code reloaded while the program runs, its state kept, on the bench of SlimeEngine's
milestone M6d.1c3a
([ADR-0212](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0212-a-functions-body-reloaded-through-subsecond-and-dx.md)).
The bench runs under `dx serve --hot-patch` and plays Slatty's library to a game's page: its grid
scrolled, a filter typed, the selection moved. Then, at each run, it changes its search field's
placeholder in the view's source file and saves it, as an editor writes a file and renames it.
`dx` compiles the change, links it against the running program's addresses and sends the new
table of the functions' addresses over its websocket. A thread of the bench receives it and wakes
the host, which applies it between two frames and runs the view again through `subsecond`'s
table. Each kept signal takes its value back by its name
([as on M6d.1c1's bench](#signals-named-across-a-reload-2026-11-07)).

The prototype goes on from M6d.1c2's, on the branch
[`m6d1c-bench`](https://github.com/HoneySlatt/SlimeEngine/tree/m6d1c-bench/benches/src/prototypes),
thrown away once M6d.1 ends.

- Machine: AMD Ryzen 7 5800X, 32 GB, Linux 7.3; at rest, but for other sessions' light work, a
  load average of 1.0 to 1.6.
- Build: `dx`'s profile `desktop-dev`, which inherits `dev`: without optimisation and with debug
  assertions, which `subsecond` needs. SlimeEngine's branch `m6d1c-bench` at `52bdb71`; the
  review's changes after it, at `8f19ef0`, touch no timed path. rustc 1.99.0, `dx` and
  `subsecond` 0.7.10. Not pinned to a core: the compiler and the linker use all of them, as on an author's
  machine.
- Command, inside SlimeEngine's `nix develop`: `dx serve --hot-patch --interactive false -p
  slime-benches --features hot --args="--prototypes --hot --runs 21"`;
  `CARGO_PROFILE_DEV_DEBUG=line-tables-only` for line tables alone; `SLIME_HOT_SCREENS=0` for the
  bench's own size.
- Size: Slatty's interface, its crate `gui`, holds 21,140 lines of code, counted by
  [`scripts/count_code.py`](../scripts/count_code.py) on its files as they are. The bench's crate
  holds 12,988; its `build.rs` adds 146 views of the library's shape, 8,177 lines once formatted,
  for 21,165. Its program links SlimeEngine's crates, from its `crates/` and `games/`, 126,477
  lines; Slatty's links its other crates, 57,477 lines, and Iced.
- Each time: the median of 21 runs, with their range, in milliseconds; a session's first patch
  apart. Each run checks that its frame shows the new placeholder with the scroll, the selection,
  the field's text, the filter and the page kept, and that the reload noted nothing: all 21 did,
  in each series.

### From a change saved to the frame that shows it

| The crate that changed | Debug information | Whole | The patch arrived | `dx`'s own count | Applied | The reload's call | Its frame | A session's first |
|---|---|---|---|---|---|---|---|---|
| Slatty's size, 21,165 lines | full, the `dev` profile's | 2,041 (1,900–2,457) | 2,022 (1,881–2,436) | 1,233 (1,153–1,444) | 7.9 (7.7–10.0) | 1.1 (1.1–1.3) | 4.8 (4.7–5.8) | 1,987 |
| Slatty's size, 21,165 lines | line tables alone | 1,684 (1,636–2,379) | 1,666 (1,617–2,360) | 1,126 (1,098–1,523) | 8.2 (7.5–11.6) | 1.1 (1.0–1.4) | 4.6 (4.4–5.3) | 1,644 |
| The bench's own, 12,988 lines | full | 1,149 (1,112–2,079) | 1,137 (1,100–2,067) | 670 (650–1,096) | 3.4 (3.1–3.8) | 1.0 (1.0–1.2) | 4.8 (4.6–5.5) | 1,296 |

- *Whole*: from the save, once the file is renamed, to the end of the frame's display list.
- *The patch arrived*: from the save to the patch read on the bench's thread. `dx` heard of the
  change some 2 ms after the save, in every series.
- *`dx`'s own count*: the time that `dx` gives in its message, from the start of its build of the
  patch to the patch built (`serve/runner.rs` of dioxus-cli 0.7.10). The rest of the patch's
  arrival, some 0.8 s at Slatty's size and 0.5 s at the bench's, comes after that count; the
  table that maps the patch's functions onto the running program's, which `dx` makes from both
  binaries, is part of it, not timed apart.
- *Applied*: `subsecond::apply_patch`, the patch's library loaded and its table installed.
- *The reload's call* and *its frame*: as on M6d.1c1's bench, here without optimisation.
- The parts leave out 2 to 5 ms of each whole: the patch handed from the bench's thread, where it
  arrives, to the host, which it wakes.

The same change, built again by cargo without a reload, at Slatty's size with full debug
information: 2,181 ms (2,157–2,389), by `benches/hot-rebuild.sh`. A first series overlapped
another build running on the machine, 3,238 ms; it was run again once that ended.

### What they say

- A body changed shows within the budget of a change seen, 2 s, at Slatty's size with line
  tables alone: 1.68 s. With full debug information, it misses it by 0.04 s. `uwui dev` compiles
  with line tables, in a folder of its own: cargo's builds keep full debug information.
- Nearly all the time is `dx`'s: the patch built, some 1.2 s at Slatty's size, then some 0.8 s
  after its count, the patch's table among it. The program's own part, the patch
  applied, the view run again and its frame, is some 14 ms without optimisation, and a few more to
  hand the patch to the host.
- `dx` links the whole crate that changed into the patch: its count and what follows it both grow
  with that crate's size, 1.15 s at 13,000 lines, 2.04 s at 21,200. An interface cut into smaller
  crates reloads faster.
- The reload saves little of the compiler's time over cargo's own build, 2.04 s against 2.18 s. It
  saves the program's start, its data loaded again, and the state found again by hand.
- The state is kept by the signals' names across every run.
- On Linux, a thread-local defined in the crate that a patch links does not link at all, and one
  reached by code compiled there, a generic function or one inlined, becomes the patch's own empty
  copy. The bench's thread-locals moved to a crate of their own, reached through functions neither
  generic nor inlined; uwui's will follow the same rule. This costs the bench's signals a call out
  of line, and each lookup of the runtime a downcast: M6d.1c1's and M6d.1c2's figures on this
  branch were taken before it.

Not measured: the web and Android, which have no host yet, weighed in the ADR from
[the survey](survey-writing-an-application.md#8-reloads-on-the-web-and-on-android); Windows and
macOS; a window's frame; the owner's laptop. The rivals' reloads are
[timed apart](#the-rivals-reloads-2026-11-07).

## The rivals' reloads (2026-11-07)

How fast the rivals show a change of their code, beside
[uwui's reload through `subsecond`](#a-functions-body-reloaded-through-subsecond-2026-11-07), for
SlimeEngine's milestone M6d.1c3b. Each runs its own reload as an author runs it, in a debug build,
on its "Hello, World!" of [`references/hello-world/`](../references/hello-world/README.md): the
program started by its tool, the text "Hello, World!" changed to "Hello, Reload!" in its source and
back, 21 times. [`scripts/reloads.sh`](../scripts/reloads.sh) prepares each and plays its
`reload.steps` through the step `save` of [`scripts/measure.py`](../scripts/measure.py): the file
saved, then the first frame that the compositor shows whose pixels differ, compared by their
CRC-32. No probe runs in the programs.

- Machine: AMD Ryzen 7 5800X, 32 GB, Radeon RX 6900 XT on RADV, NVMe, Linux 7.3.1; sway 1.12
  without a screen, one output of 3840 × 2160 at 240 Hz, scale 1.5, the window alone on it. At
  rest, Steam's client open without a game; a load average under 1 before the series, each
  program's build apart from its reloads.
- Each time: the median of 21 reloads, with their range, in milliseconds, from just before the file
  changes on disk to the first frame shown changed; a session's first reload apart. Each reload
  waited for the program to stand still, as `still` waits, but Compose's, which never stands still
  under its reload: 5 s apart. In every series, all 21 showed their change; each first frame
  changed was the image that the program settled on, never one between; the program settled on
  the same two images, the change's and the original's, and kept its process and its window, as
  sway lists them.
- Versions: `dx` 0.7.10, rustc 1.98.1, from uwui's nixpkgs; Dioxus 0.7.10; Iced 0.14.0 with
  `cargo hot` 0.1.1; GPUI at Zed's `145bcfc`; Slint 1.18.1; Flutter 3.47.4 and Dart 3.13.3;
  Compose Multiplatform 1.12.2 with its Compose Hot Reload 1.2.0, on the JetBrains Runtime
  25.0.3-b508.4, Gradle 9.5.1; Makepad at `506ec05`. The Rust programs build with the `dev`
  profile's full debug information.
- Command, in uwui's repository: `scripts/reloads.sh <work> <figures>`. A first series, before the
  step noted its first frame's image and stamped the save before the file's sync, gave the same
  figures within 15 ms, Makepad's absence included.

### From a change saved to the frame that shows it

| Framework | What changed, and how it reloads | Whole | The tool's own count | A session's first | Memory while reloading |
|---|---|---|---|---|---|
| Flutter | the widget's `build` method: the Dart VM loads the changed library, on the signal that an editor sends | 154 (147–171) | 112 (109–124), "Reloaded 1 of 754 libraries" | 219 | 948 MB |
| Dioxus, RSX | a literal of `rsx!`, the button's label: read again, not compiled | 38.6 (37.7–39.4) | | 51 | 822 MB |
| Dioxus, a function's body | `greeting()`, called from `rsx!`: patched through `subsecond` by `dx` | 648 (641–655) | 604 (598–612) | 958 | the same |
| GPUI | the view's `render`: patched through `subsecond` by `dx` | 618 (610–625) | 613 (604–620) | 942 | 996 MB |
| Iced | `view`: patched through `subsecond` by `cargo hot` | 1,303 (1,286–1,323) | 1,190 (1,170–1,210), cargo's | 2,035 | 686 MB |
| Slint | the `.slint` file: read again by its interpreter, not compiled | 307 (305–314) | | 308 | 134 MB, the program alone |
| Compose | the composable `App`: compiled by Gradle, its class redefined by the JetBrains Runtime | 460 (432–510) | | 619 | 2,200 MB, Gradle's daemons with the program |
| Makepad | the `script_mod!` block, under `--hot` | not shown | | not shown | |

- *The tool's own count*: what the tool writes in its log for each reload. `dx`'s log line counts
  from the start of its build of the patch to the patch's table made (`build/builder.rs` of
  dioxus-cli 0.7.10); the time in its message to the program, which uwui's bench reads, stops
  before that table. Flutter's counts its compile, its reload and the widgets built again;
  `cargo hot`'s, its cargo build of the patch.
- *Memory*: once the series ends, the proportional size (PSS) of the processes that the command
  started: the program with its tool, `dx`, `cargo`, Flutter's tool or Gradle, as an author runs
  them.

### What they show

- Rust reloaded through `dx`, on a crate of a few lines: 0.65 s for Dioxus, 0.62 s for GPUI, nearly
  all of it inside `dx`'s log count, 44 ms and 5 ms outside it. uwui's bench, under the same `dx`,
  takes 1.15 s at 13,000 lines with full debug information and 1.68 s at Slatty's size with line
  tables alone; its time ends at its display list, not at a frame shown, and it ran on rustc
  1.99.0. `dx`'s message counts 0.67 s and 1.13 s of it; the rest, some 0.5 and 0.6 s, comes after
  that count. It holds the table made from both binaries, larger for the bench's program, which
  links SlimeEngine's crates, than for a "Hello, World!"; it was not timed apart.
- Iced's `cargo hot`, on the same `subsecond`, takes twice as long as `dx` on the same size: its
  cargo build of the patch alone is 1.19 s.
- What does not compile Rust is faster: Flutter's VM, 0.15 s; Slint's interpreter, which reads its
  markup again, 0.31 s; Dioxus's RSX, read again, 0.04 s. Compose compiles Kotlin through Gradle's
  daemon in 0.46 s. A layout's or a style's reload without compiling, which SlimeEngine's M6d.1d
  designs, is the change that can come in under 0.1 s.
- Of the rivals timed, none reloads a Rust function's body faster than `dx` allows: ADR-0212's
  choice stands. Makepad's own reload of Rust, through its compiler Relax under `makepad run`, was
  not built.
- The state: every program kept its process and its window across each reload; none started
  again. What each keeps inside, its widgets' state and its own, is read in
  [the survey](survey-writing-an-application.md#a-functions-body), not measured: a "Hello, World!"
  holds no state to check.
- How a save must be written: `cargo hot` 0.1.1 and Slint 1.18.1 reload only a file written over
  itself. A file saved by a rename, as many editors save, is not reloaded, which their steps show
  once each; their series write the file in place. Under `dx`, only saves by a rename were timed.
  `flutter run` watches no file: an editor asks it to reload, here by the signal SIGUSR1 that its
  tool documents.
- Compose under its reload never rests: it draws some 63 frames a second without end, the same
  pixels; its processes, Gradle's daemons with the program, use 10 % of a core and wake 4,282
  times a second.
- Makepad: here, each change is logged as detected, saved either way, and never shown; no frame
  changed, drawn on Vulkan as on OpenGL ES, even after the pointer moved over the window, and
  nothing in its log says why. Its code drops a change without a word when it finds no compiled
  block for the file, and this reference is a crate outside Makepad's workspace, which may be the
  cause; Makepad's own examples, inside it, need its repository cloned, and were not tried. Not
  timed; the cause not found.

Not measured: the rivals on the web, Android and the owner's laptop; their reloads at Slatty's size;
a change of a type's state, which [the survey](survey-writing-an-application.md#a-type-whose-state-migrates)
reads.

## A style sheet's change seen (2026-11-09)

A style sheet's change, from its save to the frame that shows it, the state kept, on the bench of
SlimeEngine's milestone M6d.1d1
([ADR-0224](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0224-a-files-change-reaches-the-application-through-the-development-tool.md)).
Slatty's library on signals is played to a game's page: its grid scrolled, a filter typed, the
selection moved. Then, at each run, the bench saves the screen's style sheet with its title's size
changed, 52 then 44 then 52, as an editor writes a new file and renames it over the old one. A
thread of the bench looks at the file's time of change each millisecond, standing for the
development tool's watcher. Once it changed, the thread reads the text, hands it to the host and
wakes it. The host styles the interface again with it (`Ui::set_themes`, the theme shown kept), and
runs the frame that shows it.

The prototype goes on from M6d.1c's, on the branch
[`m6d1c-bench`](https://github.com/HoneySlatt/SlimeEngine/tree/m6d1c-bench/benches/src/prototypes),
in `style_reload.rs`, thrown away once M6d.1 ends.

- Machine: AMD Ryzen 7 5800X, 32 GB, Linux 7.3.1; at rest, but for other sessions' light work, a
  load average over one minute of 1.95 to 2.30.
- Build: SlimeEngine's branch `m6d1c-bench` at `dbf86fc`, rustc 1.99.0. Release, and the `dev`
  profile, without optimisation, as an author runs an application. The review's changes after it,
  at `9e6cfa4`, add checks and touch no timed path.
- Command, inside SlimeEngine's `nix develop`: `cargo build --release -p slime-benches`, then
  `../target/release/slime-benches --prototypes --style --runs 21` from `benches/`, and the same in
  the `dev` profile.
- Each time: the median of 21 runs, with their range, in milliseconds; a session's first change
  apart. Each run checks that its frame shows the new size with the scroll, the selection, the
  field's text, the filter and the page kept: all 21 did, in each series. From `9e6cfa4`, each run
  checks too that its frame ran no code of the application, and a test that the theme shown is
  kept.

### From a change saved to the frame that shows it

| Build | Noticed | Read | Rules made again | Its frame | Whole | A session's first |
|---|---|---|---|---|---|---|
| Release | 0.44 (0.20–1.00) | 0.46 (0.21–1.01) | 1.44 (1.26–1.70) | 0.97 (0.86–1.30) | 2.94 (2.43–3.67) | 2.86 |
| Debug | 0.60 (0.02–0.91) | 0.62 (0.04–0.93) | 8.29 (7.90–10.27) | 4.73 (4.55–6.21) | 13.58 (12.90–16.30) | 16.39 |

- *Noticed* and *Read*: from the save to the watcher's sight of the change, then to the file read.
  They hang on the watcher's look each millisecond; a tool told by the system, inotify,
  `ReadDirectoryChangesW` or FSEvents, has another delay, measured when it is built.
- *Rules made again*: the screen's two style sheets and the two themes, dark and light, read and
  their rules made, once for each theme.
- *Its frame*: every element styled again, laid out and drawn into the display list.
- *Whole*: from the save, once the file is renamed, to the end of the frame's display list.

### What they say

- The program's part of a style's change is far within the budget of a change seen, 2 s: some
  3 ms in a release build, 14 ms in an author's debug build, to the display list. The whole adds
  the development tool's watcher, its interval of 50 ms and its connection, and a frame presented
  ([ADR-0224](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0224-a-files-change-reaches-the-application-through-the-development-tool.md)),
  measured when the tool is built. The rivals' figures, Slint's interpreter 0.31 s and Dioxus's RSX
  0.04 s ([the rivals](#the-rivals-reloads-2026-11-07)), run from a save to a frame on the screen
  through their own watchers: they compare with that whole, not with this part.
- The program's part is the rules made again for each theme, then a frame that styles every element:
  the cost grows with the themes given and the elements shown.
- The state is kept: a style's change runs no view.

Not measured: the tool's watcher and its connection, which do not exist yet; the web and Android;
Windows and macOS; a window's frame; the owner's laptop.

## A layout's change seen (2026-11-09)

A layout's change, from its save to the frame that shows it, the state kept, on the bench of
SlimeEngine's milestone M6d.1d2a
([ADR-0225](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0225-layouts-written-in-kdl-reached-from-code-by-their-names.md)).
Slatty's library is written as layouts in KDL 2.0, its search field, its grid of covers, a cover
and a game's page; the view's code binds each named element by its name, and fills the page's
slot. It is played to a game's page: its grid scrolled, a filter typed, the selection moved. Then,
at each run, the bench saves the layouts' file with a label added before the grid, or taken away
again, as an editor writes a new file and renames it over the old one. The same watcher as the
style sheet's, a thread that looks at the file's time of change each millisecond, reads it and
wakes the host. The application reads the text into layouts and sets their signal; the frame
makes the library's top layout again with its bindings, the covers of the cells that show and the
page, and mounts them over the tree, whose elements keep their state by their names.

The prototype goes on from M6d.1d1's, on the branch
[`m6d1c-bench`](https://github.com/HoneySlatt/SlimeEngine/tree/m6d1c-bench/benches/src/prototypes),
in `layout_reload.rs`, `signals/layout.rs` and `signals/laid.rs`, thrown away once M6d.1 ends. It
reads KDL through the crate `kdl` 6.7.1, which uwui does not take: its own reader comes with its
first stage.

- Machine: AMD Ryzen 7 5800X, 32 GB, Linux 7.3.1; at rest but for a browser in use, a load
  average over one minute of 2.4 to 3.7.
- Build: SlimeEngine's branch `m6d1c-bench` at `a66f364`, rustc 1.99.0. Release, and the `dev`
  profile, without optimisation, as an author runs an application. The review's change after it,
  at `68769b7`, refuses more inputs in the look that the text gets before `kdl` reads it, a few
  hundred bytes scanned once more, and touches nothing else that is timed.
- Command, inside SlimeEngine's `nix develop`: `cargo build --release -p slime-benches`, then
  `../target/release/slime-benches --prototypes --layout --runs 21` from `benches/`, and the same in
  the `dev` profile.
- Each time: the median of 21 runs, with their range, in milliseconds; a session's first change
  apart. Each run checks that its frame shows the label added or taken away with the scroll, the
  selection, the field's text, the filter and the page kept, and that the application noted no
  binding left unused: all 21 did, in each series. Tests check that the view's function does not
  run again.

### From a change saved to the frame that shows it

| Build | Noticed | Read | Relaid | Its frame | Whole | A session's first | Code run |
|---|---|---|---|---|---|---|---|
| Release | 0.53 (0.30–0.99) | 0.55 (0.32–1.01) | 0.40 (0.36–0.51) | 0.78 (0.74–1.13) | 1.78 (1.51–2.66) | 1.71 | 106 |
| Debug | 0.64 (0.00–1.04) | 0.66 (0.02–1.06) | 3.98 (3.26–4.50) | 4.64 (4.38–5.96) | 9.32 (8.09–11.17) | 10.56 | 106 |

- *Noticed* and *Read*: as the style sheet's, hanging on the watcher's look each millisecond.
- *Relaid*: the text checked, read by `kdl` into layouts, compared with the last ones and their
  signal set.
- *Its frame*: the library's top layout made again with its bindings, the cells' covers and the
  page made again, mounted over the tree, styled, laid out and drawn into the display list.
- *Whole*: from the save, once the file is renamed, to the end of the frame's display list.
- *Code run*: the units of the application's code that the frame counted, as a reload's are
  counted: the top layout's view run again and the 105 covers of the cells that show. The bindings
  made anew and the page's view, which run as they are made, are not counted; the view's function
  does not run.

### What they say

- The program's part of a layout's change is far within the budget of a change seen, 2 s: some
  2 ms in a release build, 9 ms in an author's debug build, to the display list. As for a style,
  the whole adds the development tool's watcher, its interval and its connection, and a frame
  presented, measured when the tool is built.
- A layout's change costs about what a style sheet's does, but its cost differs: it runs code, the
  covers of the cells that show made again, where a style runs none; it styles again only what it
  made. It grows with the elements below the layout that changed, not with the themes.
- The state is kept by the elements' names: a label added before the grid moves the grid's place
  among its siblings, and its scroll and selection stay.
- `kdl` 6.7.1 reads by recursion without a bound: in a debug build, a hundred `/-` in a row, or a
  thousand `a )`, overflow a 2 MiB stack and abort the program. The prototype looks at the text
  before it reads and refuses the cases that its reviews found; the look is partial, and other
  inputs may still abort it. uwui's own reader bounds its depth.

Not measured: the tool's watcher and its connection; what `dx` does when a file that a macro
reads changes; the web and Android; Windows and macOS; a window's frame; the owner's laptop.

## The notations of layouts, counted (2026-11-09)

The same screens written in each notation that SlimeEngine's milestone M6d.1d2a weighed for
layouts
([ADR-0225](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0225-layouts-written-in-kdl-reached-from-code-by-their-names.md)):
Slatty's library, its cover and a game's page, "Hello, World!", and the parts of a switch and of a
check box. The lead of the milestone wrote one sample in each notation; the review of its design
rewrote the KDL and the TOML at their best: the KDL with its names and texts apart
(`label title`, `label text="Hello, World!"`), the TOML with its own shorthands, and with
positional arrays. The XML and the flat TOML are the first samples. The KDL counted names the rows'
layout of its grid (`row=cover`) and no command.

No tokenizer of a model was used. Three counts stand for one: *words*, each run of letters,
digits and `_` and each other symbol; *runs*, the same with each run of symbols counted once, as a
tokenizer merges them; *unquoted*, the words without the double quotes.

| Notation | Bytes | Lines | Words | Runs | Unquoted |
|---|---|---|---|---|---|
| KDL 2.0, names and texts apart | 756 | 40 | 157 | 151 | 151 |
| KDL 2.0, the first sample | 743 | 40 | 153 | 149 | 145 |
| TOML, positional arrays | 823 | 23 | 314 | 242 | 238 |
| TOML, its own shorthands, lines broken within arrays | 926 | 31 | 304 | 277 | 258 |
| TOML, the first sample, nested inline tables | 955 | 34 | 313 | 287 | 267 |
| TOML, flat as scene files | 1,180 | 86 | 365 | 363 | 273 |
| A subset of XML | 1,047 | 42 | 342 | 257 | 290 |

- Every TOML sample but the first reads as TOML 1.0, which lets an array span lines but not an
  inline table; the first spreads inline tables over several lines, which only TOML 1.1 reads.
- KDL takes the fewest tokens by every count: the best TOML takes 1.6 to 1.9 times as many, the
  XML 1.7 to 2.2.
- A file's tokens are not an agent's: whether agents write a notation well, at once and in few
  tries, is the agent bench's to measure.

## The package for the web, a first probe (2026-11-11)

A probe of SlimeEngine's M6d.3b1, before the reader of themes moved to KDL: uwui's core built for
`wasm32-unknown-unknown`, a label and a button laid out and drawn, nothing read, then the same with
a style sheet and a theme read through reflection. A release build, `opt-level = "z"`, fat LTO, one
unit of code, `panic = "abort"`, stripped, without `wasm-opt`; built with nixpkgs' rustc 1.99.0 and
the development shell's linker, not the project's toolchain, which lacks the target. Sizes in bytes:

| Module | Raw | gzip -9 | zstd -19 | xz -9e |
|---|---|---|---|---|
| `uwui-kdl` alone, every entry walked | 73 335 | 37 556 | 35 471 | 33 744 |
| uwui's core, nothing read | 4 559 559 | 2 757 208 | 2 516 902 | 2 322 144 |
| the same, a sheet and a theme read | 4 816 073 | 2 849 324 | 2 593 018 | 2 391 008 |

- uwui's core alone is some 2.3 MB compressed by xz, against the [budget](ROADMAP.md) of 1 MB
  compressed by brotli, fonts apart, before any document is read: 3.4 MB of its 4.6 MB is data,
  its crate not found, the scripts of `parley` the first suspect.
- Brotli was not available: xz stands in for it. SlimeEngine's M6d.3b2 measures again with the
  project's toolchain and brotli; the web's trial confirms or corrects the budget.
