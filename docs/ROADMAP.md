# uwui's roadmap

uwui's direction: what it is, the quality bar it is held to, the decisions still open, and its
stages. Its code still lives in [SlimeEngine](https://github.com/HoneySlatt/SlimeEngine), in
`crates/uwui` and `crates/uwui-render`, until SlimeEngine's Stage 6d moves it here
([ADR-0194](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0194-stage-6d-uwui-leaving-the-engine.md)).
Until then, uwui's decisions are SlimeEngine's ADRs, linked below by their numbers.

Update this file when a stage is reshaped, a budget changes, or an open decision is taken.

## 1. What uwui is

A UI framework in Rust, GPU-rendered, for the desktop, Linux, Windows and macOS, Android phones
and televisions, and the web; iOS once a project of the owner's is accepted by Apple, tvOS after a
trial; under MIT OR Apache-2.0
([ADR-0181](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0181-uwuis-scope.md),
[ADR-0190](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0190-uwuis-requirements.md),
[ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).

- The base of its owner's applications, and of the editor and games of SlimeEngine, which
  depends on uwui, never the reverse; not of the owner's desktop, its shell, its login and lock
  screens nor its compositor ([ADR-0199](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0199-uwuis-targets-tools-and-references-narrowed.md)).
- Embedded in a host that calls it: its core never owns the event loop, and runs without a window
  or a GPU.
- Drawn with its host's wgpu device: `uwui-render` takes the device, its queue, an encoder that
  the host submits and a target, and never sets a callback or a handler on a device that it is
  lent; SlimeEngine lends its own through a guarded door, from its milestone M6d.4b1b
  ([ADR-0244](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0244-the-engine-lends-its-device-through-a-guarded-door.md)).
- The same look on every platform, from themes in files; the behaviours that each platform's users
  expect. Its core ships one sober look, a start; Glass, Material 3 Expressive and Pro are official
  themes, each a crate of its own; nothing is chosen in silence ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md), [ADR-0215](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0215-the-engine-measured-against-the-market.md)).
- An application ports with no line written for one platform ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- Read and driven by agents, through one core for agents and its MCP server; a user's own agents
  use a finished application through the actions that it declares once ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md), [ADR-0218](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0218-one-core-for-agents-in-uwui.md)).
- Paid for by its patrons, through GitHub Sponsors or Open Collective, from its 1.0; no other paid
  offer ([ADR-0214](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0214-the-engine-under-a-licence-of-its-own-with-a-royalty.md)).
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
- Porting: more easily than with Electron or GPUI, to Linux, Windows, macOS and the web, then iOS
  and Android as far as phones allow ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- Agents: they succeed with uwui at least as often as with the best rival, on fewer tokens
  ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- Measured as SlimeEngine is: the light sensor, blind tests by people, compiling's budgets and
  hours without a crash ([ADR-0215](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0215-the-engine-measured-against-the-market.md)).

### Screens of reference

Four screens, chosen with the owner on 2026-11-06 before any work on them, measure uwui
([ADR-0198](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0198-screens-of-reference-and-the-rivals-measured.md)).
They are never changed to suit a benchmark: a change is the owner's decision, in an ADR. Each has
two figures, in [`measurements.md`](measurements.md): the owner's program, the floor that a port
must not fall under; and its rivals, the bar to beat, the best of them criterion by criterion.

| Screen | What it is | Rivals |
|---|---|---|
| "Hello, World!" | gpui-kit's "Basic Example", word for word, from its README at [`b2aaa3e`](https://github.com/longbridge/gpui-kit/blob/b2aaa3e5f9a387dea74981586bfca33e7e08420d/README.md#basic-example): "Hello, World!" above a primary button, "Let's Go!", that prints "Clicked!" | The same with GPUI and gpui-kit, with GPUI alone, Flutter, Compose for the desktop, Electron, Tauri, Qt Quick, Slint, Iced and egui, each as its own documentation writes it ([`references/hello-world/`](../references/hello-world/README.md)) |
| Slatty's library | The grid of covers of Slatty, the owner's launcher, on the fake profile of 10,000 games that its `slatty-measure` makes; it scrolls 16 logical pixels a frame for 1,200 frames; a game's page opens, its key art fading in | Steam, on the owner's account; Nautilus and gThumb, on the same 10,000 covers |
| Opium's songs | The table of songs of Opium, the owner's music player, in its M3E theme, on a fake library of 8,500 local songs; it scrolls from end to end; a song plays, its wave of progress moving | Spotify and Cider, on the owner's accounts |
| Zed's file | Zed, scrolling a file of 100,000 lines made by [`scripts/long-file.py`](../scripts/long-file.py) | Zed itself: uwui has no editor of code before its 1.0 |

Every screen is measured on the same output: 3840 × 2160 at 240 Hz, at a scale of 1.5, its window
alone on it, in a headless sway, from outside, by [`scripts/measure.py`](../scripts/measure.py)
([ADR-0200](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0200-applications-measured-from-outside.md));
frames in motion are checked once on the owner's display. The rivals on the owner's accounts run on libraries of other sizes, written
beside their figures, and change with their versions: each figure names its version and its date.
The rivals were narrowed on 2026-11-06 to those that aim at what uwui aims at
([ADR-0201](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0201-the-rivals-narrowed.md)).

A fifth screen, rich in effects, comes in the first stage beside uwui's first material of glass:
glass over moving content, a background blurred, shapes that morph, a transition on springs from
one screen to the next. The owner chooses it before any work on it; the proposal is Opium's screen of
the song playing, in its Glass theme. Its rivals are those that can draw it: Flutter, Compose,
Electron, and SwiftUI with Apple's glass on macOS; beside it, a table of what each rival can draw.
Before 1.0, a *gallery*: mock-ups of the market chosen with the owner, which uwui reproduces, each
judged image against mock-up, with its frame's cost ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).

#### The bar of each screen

The best rival on each criterion, measured on 2026-11-06, from
[`measurements.md`](measurements.md); memory is the proportional size of all a program's
processes, then its video memory. A program on uwui must beat each line, at the least; the floor,
the owner's program, is in `measurements.md` beside it. Its lead is a budget of its own, below.

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
- Televisions: a Xiaomi TV Box S of the third generation (Amlogic, 2 GB, a Mali-G310, Google TV),
  the lowest box supported, not yet at hand; the owner's Apple TV 4K of 2022 (A15) for tvOS
  ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).
- Apple's: a Mac with Apple's chips checks macOS and builds for iOS and tvOS; none is at hand, and
  macOS's checks by hand are debt until one is ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).

### Budgets

A budget missed is debt until it is met. No application runs on uwui yet: none is measured.

| Budget | Figure | Measured by |
|---|---|---|
| At rest | 0 frames and 0 own wake-ups a second; a caret that blinks stops after 10 s without input | every thread's context switches over 10 s, on each compositor of the series ([ADR-0185](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0185-rest-checked-in-ci.md), [ADR-0195](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0195-a-series-of-headless-compositors.md)) |
| Input to present | at the 99th percentile, 1 frame, 4.17 ms on the high tier ([ADR-0189](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0189-first-measures-of-time.md)) | a person's input given through the compositor, `input to present` in a trace |
| Start | a typical application on the high tier, warm, to its first useful frame, 100 ms; cold, 500 ms ([ADR-0190](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0190-uwuis-requirements.md), [ADR-0192](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0192-the-budget-of-a-cold-start.md)) | the log's times, and the launch timed by `hyperfine` |
| Size and changes | a typical application on the high tier: at most 100 MB resident at rest, a binary of at most 20 MB, a change of its interface seen within 2 s ([ADR-0190](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0190-uwuis-requirements.md)) | the four programs of the first stage, and the application measured against the rivals |
| The package for the web | at most 1 MB of WebAssembly compressed with brotli, fonts apart; provisional until the web's trial ([ADR-0181](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0181-uwuis-scope.md)) | the web's trial |
| Power | each effect at rest and in motion, the GPU's and the CPU's, on the owner's machine and on a modest one ([ADR-0171](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0171-effects-of-the-interface.md)); its figure from the lead, below | decided with the effects |
| The lead | on each machine and screen, a program's *own cost*, what it adds above a *blank window* that only clears and presents, is at most a third of the best rival's: memory, the start, the processor, power, a frame's time and the package's size; at rest and from input to present, the blank window's figure ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)) | the blank window measured beside each screen, from SlimeEngine's M6d.7 |
| Porting | an application on uwui's APIs alone runs on Linux, Windows, macOS and the web with no line written for one platform; on Android and iOS, only its package's configuration and permissions differ; a couch screen's lines counted apart, as a form factor's ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)); provisional until the trials of Android, the web and iOS ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)) | the small application of 1.0 on each platform: its lines for that platform, the steps from `uwui new` to a package installed, the package's size, against Electron, Tauri, Flutter, GPUI and Compose Multiplatform |
| Input to photon | timed by a light sensor on the screen, so that the rivals compare from outside ([ADR-0215](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0215-the-engine-measured-against-the-market.md)) | the light sensor's bench, from SlimeEngine's Stage 6e |
| Compiling | SlimeEngine's budgets of compiling, applied to an application on uwui; their figures for an application weighed at SlimeEngine's M6d.10 ([ADR-0215](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0215-the-engine-measured-against-the-market.md), [ADR-0220](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0220-the-roadmap-reshaped-by-the-market.md)) | at each milestone, on the high tier |
| Hours without a crash | at least 99.9 % of an application's hours of use without a crash, no work lost after one ([ADR-0215](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0215-the-engine-measured-against-the-market.md)) | the hours and crashes counted on the machine |
| Agents | an *agent bench*: a screen from a mock-up, a feature added, a bug fixed, a port to the web, given to the same agents in the same words with uwui and with GPUI and gpui-kit, Flutter, Compose, Electron, Tauri and Slint; at least the best rival's success, on fewer tokens; provisional ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)) | success, tries, tokens and time, with the models, their versions and the date, at each release |

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
- macOS aimed at for 1.0, as Linux and Windows: built and tested in CI on Apple's chips, checked by
  hand on a Mac with Apple's chips, never in a virtual machine; the documentation names the last
  check by hand and its date, or says that none was made
  ([ADR-0173](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0173-the-platforms-of-applications.md),
  [ADR-0196](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0196-checks-by-hand-on-macos.md),
  [ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md),
  [ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).
- iOS a target of 1.0 once a minimal build of Aerith passes Apple's review for TestFlight; until
  then, a trial on Xcode's simulator. iOS 17 at least; frame times, power, touch and VoiceOver on an
  iPhone before 1.0; iPadOS's stylus, pointer and windows debt ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).
- Android TV aimed at for 1.0, Google's quality checklist for TV apps met: the D-pad, Back and the
  media keys, the screen kept on while a video plays, TalkBack driven by the D-pad, 32-bit builds,
  the memory of low-memory boxes ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).
- tvOS built in CI from the move; a trial after the first stage decides whether it is a target of
  1.0 or after ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).
- Colour: one way to blend, in sRGB's encoding, on every target; SDR white at 1.0, the display's
  headroom applied at the end; a colour description on every surface, image and plane; floats
  only while content asks ([ADR-0234](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0234-uwuis-colour-model-before-its-api-is-stable.md)).
- Blind tests by people: an application's captures compared with its rivals' without knowing which
  is which ([ADR-0215](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0215-the-engine-measured-against-the-market.md)).
- No look imposed: `uwui new` asks which look, uwui's own, Plain, Glass, Material 3 Expressive or
  Pro; each root is given its look, never by default
  ([ADR-0226](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0226-an-application-started-in-one-call-each-root-given-its-look.md)); a test of signature checks that applications on uwui are not recognised by their look
  ([ADR-0215](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0215-the-engine-measured-against-the-market.md)).
- The official themes' images of reference run in uwui's CI: a change that breaks one is refused
  ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- A user's agents: consent agent by agent, each action through the interface's own commands, undone
  and logged, no secret given ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- Content from outside read within limits of size, memory and time, fuzzed, and never crashing.
- No telemetry: uwui sends nothing over the network of its own accord.

## 3. Open decisions

| Topic | Candidates | Decided at |
|---|---|---|
| Games' interfaces, HUD, inventories, dialogues and interfaces within the world | uwui's core with a layer of the engine's, the direction that [SlimeEngine's ADR-0209](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0209-platforms-the-editor-and-agents.md) takes, confirmed by a measure of *Hunna Wood*'s HUD and a menu driven by a gamepad, [as the engine proposes it](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/uwui-needs.md#for-m6d10); a framework of their own if it fails | SlimeEngine's M6d.10 |
| How vector shapes are drawn | by measurement: tessellated on the CPU, distance fields, or stencil then cover | the first stage's drawing |
| iOS a target of 1.0 | yes, if a minimal build of Aerith passes Apple's review for TestFlight; a trial alone otherwise ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)) | Aerith's review |
| tvOS a target of 1.0, or after it | its focus mirrored to the system's focus engine; App Review's verdict on an interface drawn by the application ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)) | the tvOS trial's report, after the first stage |
| Glass over a plane that uwui cannot read on Apple's platforms | the system's glass as one step of the fallback, taken by the owner; the steps' order with uwui's own ([ADR-0235](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0235-content-from-outside-the-tree.md)) | the whole element, after the first stage |

## 4. Stages

### Now: uwui leaves SlimeEngine

SlimeEngine's Stage 6d: the figures before, how an application is written decided, uwui
decoupled from the engine, its desktop host on a series of compositors, one core for agents and
its MCP server, the actions declared once, then its code moved here
([SlimeEngine's plan](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/PLAN.md)).

### The first stage: the foundations and four programs

**Goal.** uwui runs applications on the desktop, on Android phones and on the web as well as the
frameworks that they leave, with looks as refined as current interfaces have, at the lowest draw
of power.

- Writing an application more easily than with GPUI and gpui-kit, across the whole framework: an
  application started in one call, its components drawn from their state, events handled by
  closures on the elements, styles written in code beside the themes' files, layouts and Rust's
  code reloaded at once, the state kept.
- An application started in one call, `uwui::run`, which names its look, under an attribute that
  writes each platform's entry, from the one crate that an application in the core's look names,
  its *facade*; another look is a crate beside it; the engine and libraries of components name
  the core. Each root given its target and its look,
  replaced while it runs with its state kept; the application's themes, sheets and parts stacked
  over it, a component's parts replaced whole; one macro, `files!`, for an application's files,
  embedded in every build ([ADR-0226](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0226-an-application-started-in-one-call-each-root-given-its-look.md)).
- State that changes the interface through signals, and the frame's values through live values,
  cells that any thread writes and an element reads as it is drawn
  ([ADR-0205](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0205-signals-change-uwuis-interface.md),
  chosen from [the four models measured](measurements.md#three-models-beside-the-control-on-m6d1bs-bench-2026-11-07)):
  a list fed by its changes by key, signals fed by a state outside uwui in batches, and a timer
  at the granularity that it shows.
- The interface's tasks on an executor of uwui's own, each owned by the scope that started it and
  cancelled with it, its timers on their root's clock, whose next deadline the host waits for and
  meets at a wake that runs tasks and draws nothing, a task woken outside a frame too, so that a
  hidden window's timers end
  ([ADR-0227](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0227-the-time-that-motion-reads.md)): no thread of uwui's for them. Other threads change signals through a channel that a task of the
  view receives, a burst taken whole in the next frame; a channel made outside the view outlives
  a reload
  ([ADR-0211](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0211-the-executor-and-other-threads-through-channels.md),
  [measured](measurements.md#the-interfaces-executor-and-other-threads-2026-11-07)). The adapter
  for tokio apart.
- Rust's code reloaded while the application runs: a function's body through `subsecond`, its
  patches compiled and sent by `dx` and applied by the host between two frames, `uwui dev`
  compiling with line tables alone
  ([ADR-0212](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0212-a-functions-body-reloaded-through-subsecond-and-dx.md),
  [measured](measurements.md#a-functions-body-reloaded-through-subsecond-2026-11-07), beside
  [the rivals' reloads](measurements.md#the-rivals-reloads-2026-11-07)); a type's state through
  signals named by their authors, kept through `serde`
  ([ADR-0210](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0210-signals-named-for-a-reload.md),
  [measured](measurements.md#signals-named-across-a-reload-2026-11-07)).
- A library of components in layers: behaviour, state, focus and meaning in uwui's components,
  the look in the themes' parts, written as data, reached through the facade; chosen from
  the needs of the first stage's programs, tables among them; every component held to the same
  bar. A theme holds values, rules and, for any component it chooses, its parts: states reach them
  through rules, values that move as shares read when drawn, the application's content through
  slots; a component without parts in its theme takes the core's; a test kit renders each theme's
  components in each state, density and direction, and checks their contracts ([ADR-0222](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0222-what-a-theme-is.md)).
  Rules typed for each of a component's parts, and the part of a style that a theme adds, read by
  Glass or Material 3 Expressive and attached to the look of each root
  ([ADR-0229](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0229-styles-typed-as-declarations.md)).
- Styles written in code: an element's own style, typed, with its states, naming the themes'
  values by tokens; over the rules' bases, under their states and the user's size of text;
  density and contrast reaching them by the themes' names alone, a number written in code staying
  the author's
  ([ADR-0223](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0223-styles-written-in-code-through-tokens.md),
  [ADR-0237](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0237-the-users-text-size-and-less-motion-density-and-contrast-by-names.md)).
  Built in the engine before the move: the declarations that code writes, with their states, in
  the mask order, a rule's state over a base written in code, a hover or a press that never
  changes the box, the place of each call kept
  ([ADR-0231](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0231-an-elements-own-style-written-in-code.md));
  transitions that move every colour that a style holds, from the derive's list, elements that
  move alike sharing the style shown, the frame after a change of theme and each frame of its
  transition within targets of allocations
  ([ADR-0232](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0232-transitions-read-the-derives-colours-and-share-what-they-show.md));
  the user's size of text, a curve of stops, over every text but icons and a list's rows, given
  with less motion as the user's preferences, the frame after its change within a target of
  allocations ([ADR-0237](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0237-the-users-text-size-and-less-motion-density-and-contrast-by-names.md));
  tokens, the themes' values named in code by four kinds, a colour, a length, a duration and a
  number, each crate's list declared to the interface, which reads each token in its kind when it
  takes its themes, the core's roles among them
  ([ADR-0238](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0238-tokens-typed-named-in-code-declared-by-each-crate.md)). Built here: the look's own tokens, its spacings, radii, sizes of text,
  durations and colours, declared by the look as a value; under forced colours, which leaves of a
  rule named a role, recorded as the sheets are read; less transparency through a set of values
  by their names, as contrast; a style's reload through `uwui dev` timed again, a token that it
  adds read at the next taking of the themes ([ADR-0238](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0238-tokens-typed-named-in-code-declared-by-each-crate.md)). A token and less motion read when a component, a knob or a meter, is drawn, with live values, a component their first reader, so that a change of theme or of the preferences draws again without running a view ([ADR-0242](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0242-the-canvas-moved-in-three-steps-tokens-read-when-drawn-later.md)). A theme's or a style sheet's file changed is sent by `uwui dev` over its one connection,
  which relays `dx`'s patches, after an interval of 50 ms and a few milliseconds of the program's ([ADR-0224](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0224-a-files-change-reaches-the-application-through-the-development-tool.md),
  [measured](measurements.md#a-style-sheets-change-seen-2026-11-09)).
- Layouts written as data in KDL 2.0: a screen's elements, their names, classes and literal texts,
  the commands that a press runs and slots that code fills, no expression and no style; a named
  element bound by the view's code through methods that a macro generates, the compiler checking
  its names; a name keying its element, so that its state and its kept signals stay when an element
  comes before it; a kind of component from another crate named by its prefix and registered by
  that crate; a theme's parts written the same way, in a file of their own. A layout's change
  sent by `uwui dev`, the view's function not run again
  ([ADR-0225](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0225-layouts-written-in-kdl-reached-from-code-by-their-names.md),
  [measured](measurements.md#a-layouts-change-seen-2026-11-09)). Every document of uwui in KDL,
  layouts, a theme's parts, values and rules, shortcuts and docks' layouts, read by uwui's own
  reader, which its Stage 6d builds: without recursion, its size, depth and count of items bounded,
  checked against KDL's official tests, its errors at their line and column; a theme's values in
  groups of their kinds; a table of shortcuts a node for each scope, `scope global { Primary+Z
  edit.undo }`, its chords naming `Primary`, Ctrl or ⌘ after the platform, a value, and shown as
  the platform writes them, `Ctrl+Shift+Z` or `⇧⌘Z`; the cooked form a document's text
  ([ADR-0241](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0241-every-document-of-uwui-in-kdl-read-by-its-own-reader.md)).
  Built here: the reader fuzzed under guidance of coverage in CI; a document written back with
  its order, formatting and comments kept, by edits at its spans; colours outside sRGB, as
  functions; a token of text once something reads one.
- The core's own look, light, dark and of high contrast, in three densities, and its variant
  *Plain*, the core's parts in forced colours' roles, a designer's start; the system's preferences
  followed, light or dark, contrast and forced colours, less motion and transparency, the size of
  text and saving power, read by a crate of uwui's that the engine's platform layer calls too
  ([ADR-0226](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0226-an-application-started-in-one-call-each-root-given-its-look.md));
  the look a value whose sets, high contrast in light and in dark among them, the interface
  chooses from the user's preferences, which gain light or dark, contrast, forced colours and less
  transparency; under forced colours, the colours that code writes giving way by property, each
  to the role that pairs with it, with an opt-out for content that the elements below inherit; the
  couch density scaling the root, a theme giving its named values; the themes' test kit rendering
  every look at 200 % text ([ADR-0237](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0237-the-users-text-size-and-less-motion-density-and-contrast-by-names.md));
  the roles that Plain and forced colours add, `canvas`, `button_text`, `link_text` and a color of
  selected text, beside the seven that the components' defaults read, and the defaults of the
  layers that the core's look styles by class today, the tooltip, the palette, the notifications
  and the colour picker, once written as parts
  ([ADR-0230](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0230-the-cores-roles-and-each-kinds-defaults.md)); the official themes
  Glass, Material 3 Expressive and Pro, each a crate of its own in this repository with its own
  version, which the core never depends on ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- What differs between platforms and an application needs, in uwui: files and settings, the network,
  long work ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- The platforms' behaviours, the same look everywhere: a scroll's physics, predictive back, a
  selection's handles and the long press, haptics, the conventions of shortcuts; one model of
  focus for the keyboard, accessibility and gamepads.
- Fonts given as bytes and loaded when a text first needs them, with a fallback for each writing
  system, for Android and the web; on the web, the dictionaries of words of the scripts written
  without spaces loaded the same way, which the budget of the web's package then leaves out as it
  leaves fonts out: 1.93 MB of the core's 2.35 MB compressed, the core 0.42 MB without them
  ([measurements](measurements.md#the-package-for-the-web-measured-again-2026-11-11)).
- Four bounded trials, thrown away, before the API is declared stable, each with its report:
  Android, in a Kotlin activity, with a third milestone on the television box; the web, in a
  canvas; right after the first material of glass, content from outside the tree, shared by Aerith
  and Magnolia: a child process's surface on Linux with its input and focus, an HDR plane under an
  SDR interface on KWin or Mutter, Media3 in a `SurfaceView` on the Pixel, Aerith's player screen
  measured against mpv, Stremio, Jellyfin's desktop client and Kodi ([ADR-0236](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0236-one-trial-of-content-from-outside-for-aerith-and-magnolia.md)); then iOS, in two
  milestones, through uwui's own UIKit host on a Mac with Apple's chips, bought before it starts:
  the surface lost and made again, rotation, the system's keyboard with composition, iOS's
  scrolling, suspend and resume, a first try of VoiceOver through `accesskit_ios`, and on paper how
  uwui's focus maps onto tvOS's focus engine ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md), [ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).
- The colour model, before the API is declared stable: the interface blending in sRGB's encoding on
  every target, floats included; 1.0 as SDR white, the display's headroom read live and applied
  once at the end; an extensible colour description, on Wayland's model, on every surface, image
  and plane; the output's description from the host where wgpu gives none; a window in floats only
  while it shows content beyond SDR; the themes' colours and tagged images in wide gamuts; glass
  over HDR content brought down to SDR white ([ADR-0234](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0234-uwuis-colour-model-before-its-api-is-stable.md)).
- The foundations of content from outside the tree: a transparent surface over a plane, layers of
  the platform in the host's API, their colour descriptions ([ADR-0235](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0235-content-from-outside-the-tree.md)).
- Images read from files and the network, decoded away from the interface's thread, in a cache
  bounded by memory that frees the GPU's; cropped to cover, cross-faded, textures updated at each
  frame.
- Drawing: groups drawn apart into images of their own, kept while they do not change; what lies
  behind an element blurred, bent, tinted and lit, for glass; transforms, several shadows,
  gradients of several stops and radial ones, dithered; vector shapes that morph; a first material
  of glass, and the fifth screen of reference. The canvas reads its items by their index, from a
  storage buffer or, on WebGL2, OpenGL ES and WebGPU's mode of compatibility, a texture, through
  one shader, and draws groups, glass's blur and its copy to the window in passes; it keeps its
  items across frames and writes what changed. Its prototype's glass, four panels, kept 0.5 ms
  at 3840 × 2160 on what it adds to the frame; its boundaries between passes alone pass the
  handheld tier's 50 µs, judged once a boundary's cost on the Deck is known
  ([ADR-0245](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0245-the-interfaces-gpu-budget-counts-what-it-adds-to-the-frame.md)): measured again here
  ([ADR-0243](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0243-the-canvas-reads-its-items-by-index-from-a-buffer-or-a-texture.md),
  [measured](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/measurements.md#m6d4a-the-canvass-prototype)).
- Motion: transforms animated, curves and springs, delays in cascade, animations driven by
  scrolling and by gestures, interrupted without a jump, an element that becomes another, variable
  fonts whose axes move; a rate capped for each animation, effects stopped while the window has
  lost the focus, nothing drawn at rest.
- The time that motion reads ([ADR-0227](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0227-the-time-that-motion-reads.md)): each window's frame read at when it shows, given,
  predicted, asked, ready under a variable refresh, on the display's grid or simulated, never back; motion placed by its formula,
  no cap after a late frame; one clock of the host's that counts a suspend, and two types,
  `Instant` and `RootTime`; each root's time and speed, the application's motion and timers
  following it, hover, press, focus and uwui's own timings on the host's clock, a pause menu a root of its own; input's events in the
  host's clock, a fling starting at its input, a transition at its first frame; a motion asking for
  a frame when its drawing changes visibly, under a cap of one frame in n refreshes, halved for
  lasting motion while saving power; `now`, `shown_at` and `next_frame` in place of a signal of the
  frame's time; the civil time, its zone and offset, through the timer at a granularity.
- Text styled by ranges, masked fields, double clicks, the pointer's shapes, smooth and sideways
  scrolling, virtual lists that scroll sideways, a table's header that stays; gamepads.
- Four programs, outside this repository, before the API is declared stable, each with a
  checkpoint where the owner uses it: three ported, their figures with their present frameworks
  measured first, the music player on the desktop and its Android prototype, measured against
  Jetpack Compose, and the launcher Slatty; and the native client of Pluto, the owner's harness of
  agents, today on egui, its bar taken from its interview and the market when it is designed. The
  DAW, Magnolia, and the media client, Aerith, come later, clients of uwui after this stage, their
  needs checked by the choices meanwhile and by the trial of content from outside
  ([ADR-0198](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0198-screens-of-reference-and-the-rivals-measured.md),
  [ADR-0206](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0206-slatty-ported-again-the-daw-later.md)).

**Exit.** The three programs ported run on uwui at least as well as on their present frameworks,
on each of the figures measured first; Pluto's client runs at the bar set when it was designed; uwui's API is declared stable,
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
- The element for content from outside the tree: a plane by default, composed by uwui while an
  effect needs its frames, in step with the interface where the platform allows it, input, focus
  and accessibility forwarded, a budget of live planes, its API experimental until Aerith or
  Magnolia ships on it; frames decoded by the GPU shown without a copy, the player staying the
  application's ([ADR-0235](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0235-content-from-outside-the-tree.md)). HDR images, gain maps applied at the live headroom ([ADR-0234](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0234-uwuis-colour-model-before-its-api-is-stable.md)); AVIF, JPEG
  XL, HEIC and Lottie; the renderer on the CPU, measured on the lowest machines.
- The tvOS trial, two milestones on the owner's Apple TV, if Aerith passes Apple's review for tvOS
  ([ADR-0233](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0233-uwuis-platforms-apples-chips-ios-and-the-tvs.md)).
- Extensions in WebAssembly; settings, the window's state and undo for applications; translation
  through Fluent.
- `uwui new`, `run`, `dev`, `bundle` and `doctor`, `bundle` delegating to the tools that make
  each package; packages for Linux, Windows, Android and the web; updates installed by an
  application evaluated, at most an optional crate for Windows and macOS ([ADR-0199](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0199-uwuis-targets-tools-and-references-narrowed.md)); a book, a site whose demonstrations run in the browser, and small
  applications finished.
- macOS's host and integrations, the menu bar, ⌘ as the primary modifier checked on a Mac, a
  text field's keys of Control as macOS gives them, notifications, Now
  Playing and the Dock; `uwui bundle` makes an application bundle and a disk image, signed and
  notarized, under an Apple developer account ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- WCAG 2.2 at level AA, checked; the same small application, whole, written with each rival and
  with uwui, measured on the owner's machines, built and run on Linux, Windows, macOS, the web,
  Android and iOS's simulator; CI building uwui's examples for every target at each push, Apple's
  each night
  ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).
- The gallery of the market's mock-ups.
- The agent bench at each release; documentation written for agents, a compact reference and a
  skill, and an `AGENTS.md` written by `uwui new`.
- A local MCP server through which the user's assistant calls an application's actions on the
  desktop; each system's adapter when a pilot needs it and the system offers it ([ADR-0213](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0213-uwuis-reach-its-lead-its-themes-and-agents.md)).

**Exit.** uwui 1.0, announced and published on crates.io with a site, outside contributions
opened: every requirement of ADR-0190 met or recorded as debt; the application measured against
the rivals better than each as a whole, on lines, start, memory, frames and power; semantic
versioning kept from then on; patronage opened.

The cut and the order of these stages are designed in SlimeEngine's milestone M6d.10, with the
owner.
