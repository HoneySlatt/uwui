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

- The base of every interface of its owner's: applications, the owner's desktop shell, and the
  editor and games of SlimeEngine, which depends on uwui, never the reverse.
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

### Machines

- The high tier: the class of an RX 6900 XT, 8 cores, 32 GB, a display at 3840 × 2160 and 240 Hz:
  4.17 ms a frame. Frames follow the display, 60 to 240 a second and beyond.
- The desktop's lowest: a Raspberry Pi 5, or an old computer without a Vulkan GPU, drawn by a light
  renderer on the CPU, its effects reduced. The owner's very modest laptop is measured first.
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
| How an application's state changes its interface | signals, views that say they changed as in GPUI, messages as in Elm, measured on the screens of reference | SlimeEngine's M6d.1 |
| The format of layouts | the engine's notation laid out as scene files, a markup of its own, a subset of HTML and CSS | SlimeEngine's M6d.1 |
| Rust's code reloaded, its state kept | to survey | SlimeEngine's M6d.1 |
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
  themes, one dependency for an application; chosen from the needs of the music player and the
  launcher, tables among them; every component held to the same bar.
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
- Four programs, outside this repository, ported before the API is declared stable, each with a
  checkpoint where the owner uses it, their figures with their present frameworks measured first:
  the music player on the desktop, the launcher Slatty, the music player's Android prototype
  measured against Jetpack Compose, and a media application.

**Exit.** The four programs run on uwui at least as well as on their present frameworks, on each
of the figures measured first; uwui's API is declared stable, after the trials' reports; writing
an application beats GPUI with gpui-kit across the whole framework, every component and every
program ported; every need that the music player marks as indispensable exists, shown by an
example and its tests; nothing is drawn at rest, under Wayland, under Xwayland, on Android and on
the web; the power that the GPU and the CPU draw is measured for each effect, at rest and in
motion.

### Then, to its 1.0

- What the four programs did not need: the rest of the library of components, the editor of code,
  rich text, Markdown, the terminal, PDF, the map, the web view, charts and conversations with AIs,
  each a crate of its own.
- The system's integrations in a crate of their own; hosts for the owner's shell, its login and
  lock screens, and its compositor; whole Android applications without Kotlin; web applications
  installed and offline, and uwui embedded in a page.
- Video decoded by the GPU, HDR, AVIF, JPEG XL, HEIC and Lottie; the renderer on the CPU, measured
  on the lowest machines.
- Extensions in WebAssembly; settings, the window's state and undo for applications; translation
  through Fluent.
- `uwui new`, `run`, `dev`, `bundle` and `doctor`; packages for Linux, Windows, Android and the
  web; signed updates; a book, a site whose demonstrations run in the browser, and small
  applications finished.
- WCAG 2.2 at level AA, checked; the same small application, whole, written with each rival and
  with uwui, measured on the owner's machines.

**Exit.** uwui 1.0, announced and published on crates.io with a site, outside contributions
opened: every requirement of ADR-0190 met or recorded as debt; the application measured against
the rivals better than each as a whole, on lines, start, memory, frames and power; semantic
versioning kept from then on.

The cut and the order of these stages are designed in SlimeEngine's milestone M6d.10, with the
owner.
