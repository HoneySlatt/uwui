# uwui's roadmap

uwui's direction: what it is, the quality bar it is held to, the decisions still open, and its
stages. Its code still lives in [SlimeEngine](https://github.com/HoneySlatt/SlimeEngine), in
`crates/uwui` and `crates/uwui-render`, until SlimeEngine's Stage 6d moves it here
([ADR-0194](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0194-stage-6d-uwui-leaving-the-engine.md)).
Until then, uwui's decisions are SlimeEngine's ADRs, linked below by their numbers.

Update this file when a stage is reshaped, a budget changes, or an open decision is taken.

## 1. What uwui is

A UI framework in Rust, GPU-rendered, for the desktop, Android phones and the web, under MIT OR
Apache-2.0
([ADR-0181](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0181-uwuis-scope.md),
[ADR-0190](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0190-uwuis-requirements.md)).

- The base of its owner's applications, and of the editor and games of SlimeEngine, which
  depends on uwui, never the reverse; not of the owner's desktop, its shell, its login and lock
  screens nor its compositor ([ADR-0199](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0199-uwuis-targets-tools-and-references-narrowed.md)).
- Embedded in a host that calls it: its core never owns the event loop, and runs without a window
  or a GPU.
- The same look on every platform, from themes in files; the behaviours that each platform's users
  expect.
- Read and driven by agents, through a channel and an MCP server of its own.
- Public and adopted widely at its 1.0, judged as a whole against GPUI with gpui-kit, Flutter and
  Jetpack Compose, SwiftUI, Electron and Tauri, Qt and Slint.

## 2. Quality bar

### References

- The most refined interfaces of the time: in motion, materials such as glass and shapes that
  morph, type, and responsiveness
  ([ADR-0170](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0170-applications-on-the-ui-framework.md),
  [ADR-0171](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0171-effects-of-the-interface.md)).
- Writing an application: no longer, and with no more concepts to learn, than with GPUI and
  gpui-kit, and better on what they lack: a change of the look or of the layout seen without
  compiling again, the start, memory, power at rest and in motion, Android and the web, agents.
  Judged on whole programs, and on screens of reference chosen before the work and never tuned for.

### Screens of reference

Four screens, chosen with the owner on 2026-11-06 before any work on them, measure uwui
([ADR-0198](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0198-screens-of-reference-and-the-rivals-measured.md)).
They are never changed to suit a benchmark: a change is the owner's decision, in an ADR. Each has
two figures, in [`measurements.md`](measurements.md): the owner's program, the floor that a port
must not fall under; and its rivals, the bar to beat, the best of them criterion by criterion.

| Screen | What it is | Rivals |
|---|---|---|
| "Hello, World!" | gpui-kit's "Basic Example", word for word, from its README at [`b2aaa3e`](https://github.com/longbridge/gpui-kit/blob/b2aaa3e5f9a387dea74981586bfca33e7e08420d/README.md#basic-example): "Hello, World!" above a primary button, "Let's Go!", that prints "Clicked!" | The same with GPUI and gpui-kit, with GPUI alone, Flutter, Compose for the desktop, Electron, Tauri, Qt Quick, Slint, Iced and egui, each as its own documentation writes it ([`references/hello-world/`](../references/hello-world/README.md)) |
| Slatty's library | The grid of covers of Slatty, the owner's launcher, no longer developed and rebuilt on uwui as this screen alone ([ADR-0203](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0203-pilots-replaced-pluto-and-a-daw.md)), on the fake profile of 10,000 games that its `slatty-measure` makes; it scrolls 16 logical pixels a frame for 1,200 frames; a game's page opens, its key art fading in | Steam, on the owner's account; Nautilus and gThumb, on the same 10,000 covers |
| Opium's songs | The table of songs of Opium, the owner's music player, in its M3E theme, on a fake library of 8,500 local songs; it scrolls from end to end; a song plays, its wave of progress moving | Spotify and Cider, on the owner's accounts |
| Zed's file | Zed, scrolling a file of 100,000 lines made by [`scripts/long-file.py`](../scripts/long-file.py) | Zed itself: uwui has no editor of code before its 1.0 |

Every screen is measured on the same output: 3840 × 2160 at 240 Hz, at a scale of 1.5, its window
alone on it, in a headless sway, from outside, by [`scripts/measure.py`](../scripts/measure.py)
([ADR-0200](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0200-applications-measured-from-outside.md));
frames in motion are checked once on the owner's display. The rivals on the owner's accounts run on libraries of other sizes, written
beside their figures, and change with their versions: each figure names its version and its date.
The rivals were narrowed on 2026-11-06 to those that aim at what uwui aims at
([ADR-0201](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0201-the-rivals-narrowed.md)).

#### The bar of each screen

The best rival on each criterion, measured on 2026-11-06, from
[`measurements.md`](measurements.md); memory is the proportional size of all a program's
processes, then its video memory. A program on uwui beats a screen's bar when it beats each line;
the floor, the owner's program, is in `measurements.md` beside it.

"Hello, World!":

| Criterion | The bar | Held by |
|---|---|---|
| First frame shown / still | 71 / 71 ms | Slint |
| Memory | 39.8 / 98.2 MB | Slint; Compose's 19.1 MB of video memory set aside, its window smaller than the others' |
| At rest, under Wayland and Xwayland | 0 frames, 0 ticks, 0 wake-ups | Flutter, Qt Quick |
| What ships, all it needs within | 19.0 MB | Slint |

Slatty's library:

| Criterion | The bar | Held by |
|---|---|---|
| First frame shown / still | 286 / 911 ms | Nautilus |
| Memory, the grid open / scrolled / closed | 229.7 / 153.8; 404.0 / 149.9; 397.1 / 154.1 MB | gThumb |
| Memory, a game's page open | 1,547.0 / 406.3 MB | Steam, alone to have one |
| At rest | 0 frames, 0.0 % of a core, 1.2 wake-ups a second | Nautilus |
| Scrolled: frames a second, p99, longest | 242.1, 4.19 ms, 8.28 ms | gThumb |
| Scrolled: the processor | 169 % of a core at the display's rate; 50.4 % at 125 frames a second | gThumb; Steam |
| Scrolled: the GPU's power | 43.1 W | gThumb |

Opium's songs; Opium itself, the floor, is better than this bar on its start, its memory, its
rest, a song playing and its frames:

| Criterion | The bar | Held by |
|---|---|---|
| First frame shown / still | 448 / 4,409 ms | Spotify |
| Memory, the table open / a song played / scrolled / closed | 945.2 / 441.9; 886.3 / 367.4; 848.4 / 402.5; 888.1 / 499.8 MB | Cider; Spotify for video memory |
| At rest | 0 frames, 2.2 % of a core, 305 wake-ups a second | Spotify; Cider for wake-ups |
| A song playing: frames a second, the processor, the GPU's power | 4.6, 13.1 % of a core, 37.8 W | Cider |
| Scrolled: frames a second, p99 | 55.2, 24.9 ms | Spotify |
| Scrolled: the processor, the GPU's power | 21.2 % of a core, 37.9 W, at 55 frames a second | Spotify |

Zed's file, Zed itself:

| Criterion | The bar |
|---|---|
| First frame shown / still | 246 / 1,284 ms |
| Memory, the file open / scrolled / closed | 424.1 / 438.3 / 438.6 MB, 337.1 MB of video memory |
| At rest | 0 frames, 0.1 % of a core, 81.8 wake-ups a second |
| Scrolled: frames a second, p99, refreshes missed | 195.2, 8.27 ms, one frame in four |
| Scrolled: the processor, the GPU's power | 92.3 % of a core, 47.5 W |

### Machines

- The high tier: the class of an RX 6900 XT, 8 cores, 32 GB, a display at 3840 × 2160 and 240 Hz:
  4.17 ms a frame. Frames follow the display, 60 to 240 a second and beyond.
- The desktop's lowest: a Raspberry Pi 5, or an old computer without a Vulkan GPU, drawn by a light
  renderer on the CPU, its effects reduced. The owner's very modest laptop is measured first: an
  HP Laptop 17-ca2xxx, an AMD Athlon Silver 3050U (Zen, 2 cores at 1.4 to 3.2 GHz, 1 MiB of L2
  and 4 MiB of L3 cache) and its integrated Radeon (Vega) on amdgpu, 4 GiB of DDR4 on one module,
  a single channel at 2,400 MT/s, its second slot empty, 3.25 GiB of it left to programs; Ethernet,
  Wi-Fi and an ELAN touchpad; NixOS 26.11, Linux 7.1.5, the compositor niri. Its display's size and
  rate, its storage and its Vulkan driver are not yet known.
- Phones: an entry-level Android 14 phone, of the class of a Helio G99, 4 GB, a screen at 90 Hz,
  not measured; the owner's Pixel measures phones.
- The web: both of them in a browser, Chrome and Firefox on the laptop, Chrome on the phone, the
  first load over Chrome's "slow 4G" profile.
- The handheld tier: the owner's Steam Deck.

### Budgets

A budget missed is debt until it is met. No application runs on uwui yet: none is measured.

| Budget | Figure | Measured by |
|---|---|---|
| At rest | 0 frames and 0 own wake-ups a second; a caret that blinks stops after 10 s without input | every thread's context switches over 10 s, on each compositor of the series ([ADR-0185](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0185-rest-checked-in-ci.md), [ADR-0195](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0195-a-series-of-headless-compositors.md)) |
| Input to present | at the 99th percentile, 1 frame, 4.17 ms on the high tier ([ADR-0189](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0189-first-measures-of-time.md)) | a person's input given through the compositor, `input to present` in a trace |
| Start | a typical application on the high tier, warm, to its first useful frame, 100 ms; cold, 500 ms ([ADR-0190](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0190-uwuis-requirements.md), [ADR-0192](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0192-the-budget-of-a-cold-start.md)) | the log's times, and the launch timed by `hyperfine` |
| Size and changes | a typical application on the high tier: at most 100 MB resident at rest, a binary of at most 20 MB, a change of its interface seen within 2 s ([ADR-0190](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0190-uwuis-requirements.md)) | the four programs of the first stage, and the application measured against the rivals |
| The package for the web | at most 1 MB of WebAssembly compressed with brotli, fonts apart; provisional until the web's trial ([ADR-0181](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0181-uwuis-scope.md)) | the web's trial |
| Power | each effect at rest and in motion, the GPU's and the CPU's, on the owner's machine and on a modest one ([ADR-0171](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0171-effects-of-the-interface.md)) | decided with the effects |

The interface's GPU time and a list's frame, which SlimeEngine's editor shares, stay in
[SlimeEngine's quality bar](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/ROADMAP.md#4-quality-bar)
until its milestone M6d.10 decides their home.

### Without a figure

- WCAG 2.2 at level AA, checked: screen readers on every platform, the whole application by the
  keyboard, contrasts checked in CI, touch targets of 48 dp at least.
- Reduced motion and reduced transparency; effects lightened on modest hardware and on battery.
- Every writing system, layouts mirrored for right-to-left.
- The same tests on a series of headless compositors, Weston, sway, KWin, Mutter and X11 through
  Xvfb, and on Windows by hand
  ([ADR-0195](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0195-a-series-of-headless-compositors.md)).
- Variable refresh rates, checked by hand: no headless compositor emulates them.
- macOS built and tested in CI, and checked by hand on macOS 26, Intel with an AMD GPU; supported
  once a Mac with Apple's chips checks it
  ([ADR-0173](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0173-the-platforms-of-applications.md),
  [ADR-0196](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0196-checks-by-hand-on-macos.md)).
- Content from outside read within limits of size, memory and time, fuzzed, and never crashing.
- No telemetry: uwui sends nothing over the network of its own accord.

## 3. Open decisions

| Topic | Candidates | Decided at |
|---|---|---|
| How an application's state changes its interface | signals, views that say they changed as in GPUI, messages as in Elm, beside today's rebuild by keys as the control, compared as [ADR-0202](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0202-how-m6d1-compares-ways-of-writing-an-application.md) says; [the survey](survey-writing-an-application.md#1-how-state-changes-the-interface); [each screen's ideal code](ideal-code/README.md); [the four measured](measurements.md#three-models-beside-the-control-on-m6d1bs-bench-2026-11-07) | SlimeEngine's M6d.1b3b, once Opium, Pluto's client and the DAW have each said what they ask of uwui ([ADR-0203](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0203-pilots-replaced-pluto-and-a-daw.md)) |
| The format of layouts | the engine's notation laid out as scene files, a markup of its own, a subset of HTML and CSS; [the survey](survey-writing-an-application.md#2-the-format-of-layouts) | SlimeEngine's M6d.1d |
| Rust's code reloaded, its state kept | a function's body through `subsecond`, as Iced, GPUI and Rune do; a type's state through a form that does not depend on its layout, or a restart; [the survey](survey-writing-an-application.md#3-the-three-reloads) | SlimeEngine's M6d.1c |
| Games' interfaces, HUD, inventories, dialogues and interfaces within the world | uwui whole; a host and layers of their own over uwui's core; a framework of their own, weighed from what *Hunna Wood*'s interface costs the game | SlimeEngine's M6d.10 |
| How vector shapes are drawn | by measurement: tessellated on the CPU, distance fields, or stencil then cover | the first stage's drawing |

## 4. Stages

### Now: uwui leaves SlimeEngine

SlimeEngine's Stage 6d: the figures before, how an application is written decided, uwui
decoupled from the engine, its desktop host on a series of compositors, its channel for agents,
then its code moved here
([SlimeEngine's plan](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/PLAN.md)).

### The first stage: the foundations and four programs

**Goal.** uwui runs applications on the desktop, on Android phones and on the web as well as the
frameworks that they leave, with looks as refined as current interfaces have, at the lowest draw
of power.

- Writing an application more easily than with GPUI and gpui-kit, across the whole framework: an
  application started in one call, its components drawn from their state, events handled by
  closures on the elements, styles written in code beside the themes' files, layouts and Rust's
  code reloaded at once, the state kept.
- A library of components in layers, as gpui-kit's: behaviour and state in uwui, the look in
  themes, one dependency for an application; chosen from the needs of the first stage's programs,
  tables among them; every component held to the same bar.
- The platforms' behaviours, the same look everywhere: a scroll's physics, predictive back, a
  selection's handles and the long press, haptics, the conventions of shortcuts; one model of
  focus for the keyboard, accessibility and gamepads.
- Fonts given as bytes and loaded when a text first needs them, with a fallback for each writing
  system, for Android and the web.
- Two bounded trials, thrown away, before the API is declared stable: Android, in a Kotlin
  activity, and the web, in a canvas, each with its report.
- Images read from files and the network, decoded away from the interface's thread, in a cache
  bounded by memory that frees the GPU's; cropped to cover, cross-faded, textures updated at each
  frame.
- Drawing: groups drawn apart into images of their own, kept while they do not change; what lies
  behind an element blurred, bent, tinted and lit, for glass; transforms, several shadows,
  gradients of several stops and radial ones, dithered; vector shapes that morph; a first material
  of glass.
- Motion: transforms animated, curves and springs, delays in cascade, animations driven by
  scrolling and by gestures, interrupted without a jump, an element that becomes another, variable
  fonts whose axes move; a rate capped for each animation, effects stopped while the window has
  lost the focus, nothing drawn at rest.
- Text styled by ranges, masked fields, double clicks, the pointer's shapes, smooth and sideways
  scrolling, virtual lists that scroll sideways, a table's header that stays; gamepads.
- Four programs, outside this repository, before the API is declared stable, each with a
  checkpoint where the owner uses it: two ported, their figures with their present frameworks
  measured first, the music player on the desktop and its Android prototype, measured against
  Jetpack Compose; the native client of Pluto, the owner's harness of agents, today on egui; and a
  digital audio workstation of the class of FL Studio and Pro Tools, which hosts VST3 and CLAP
  plugins, a new project. The last two each take their bar from their interview and the market
  when they are designed. Beside them, Slatty's library, rebuilt alone as its screen of reference
  ([ADR-0198](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0198-screens-of-reference-and-the-rivals-measured.md),
  [ADR-0203](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0203-pilots-replaced-pluto-and-a-daw.md)).

**Exit.** The two programs ported run on uwui at least as well as on their present frameworks, on
each of the figures measured first, and so does Slatty's library against Slatty on Iced; Pluto's
client and the DAW run, each at the bar set when it was designed; uwui's API is declared stable,
after the trials' reports; writing an application beats GPUI with gpui-kit across the whole
framework, every component and every program ported; every need that the music player marks as
indispensable exists, shown by an example and its tests; nothing is drawn at rest, under Wayland,
under Xwayland, on Android and on the web; the power that the GPU and the CPU draw is measured for
each effect, at rest and in motion.

### Then, to its 1.0

- What the four programs did not need: the rest of the library of components, the editor of code,
  rich text, Markdown, the terminal, PDF, the map, the web view, charts and conversations with AIs,
  each a crate of its own.
- The system's integrations in a crate of their own; whole Android applications without Kotlin;
  web applications installed and offline, and uwui embedded in a page.
- Video decoded by the GPU, HDR, AVIF, JPEG XL, HEIC and Lottie; the renderer on the CPU, measured
  on the lowest machines.
- Extensions in WebAssembly; settings, the window's state and undo for applications; translation
  through Fluent.
- `uwui new`, `run`, `dev`, `bundle` and `doctor`, `bundle` delegating to the tools that make
  each package; packages for Linux, Windows, Android and the web; updates installed by an
  application evaluated, at most an optional crate for Windows and macOS ([ADR-0199](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0199-uwuis-targets-tools-and-references-narrowed.md)); a book, a site whose demonstrations run in the browser, and small
  applications finished.
- WCAG 2.2 at level AA, checked; the same small application, whole, written with each rival and
  with uwui, measured on the owner's machines.

**Exit.** uwui 1.0, announced and published on crates.io with a site, outside contributions
opened: every requirement of ADR-0190 met or recorded as debt; the application measured against
the rivals better than each as a whole, on lines, start, memory, frames and power; semantic
versioning kept from then on.

The cut and the order of these stages are designed in SlimeEngine's milestone M6d.10, with the
owner.
