# How an application is written: a survey

What the field does on each question of SlimeEngine's milestone M6d.1, which decides how an
application on uwui is written
([ADR-0194](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0194-stage-6d-uwui-leaving-the-engine.md),
[ADR-0202](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0202-how-m6d1-compares-ways-of-writing-an-application.md)).
Written for M6d.1a on 2026-11-06. Each later part of M6d.1 reads the sections it decides from.

Each reference is read for what it brings, not on a full grid
([ADR-0199](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0199-uwuis-targets-tools-and-references-narrowed.md)).
Every fact was read on 2026-11-06 in the reference's current documentation or source, unless its
section gives another date, and names its version. A fact that could not be checked in a primary source says so. Nothing here was built,
run or measured: the figures quoted are the references' authors'.

Update this file only to correct a fact, or to add a question that a later part of M6d.1 reads,
with the date it was read. A newer version of a reference is read again at the milestone that
needs it.

## The references

| Reference | Read for | Version read |
|---|---|---|
| uwui today | the control: a tree rebuilt by keys | SlimeEngine [`10a3e73`](https://github.com/HoneySlatt/SlimeEngine/blob/10a3e738e75107df4c9228d29ebe95a3753e44dd/crates/uwui/README.md), 2026-11-06 |
| [Floem](https://github.com/lapce/floem) | fine-grained signals | 0.2.0, 2024-11-15; `main` at `1351ffb`, 2026-09-24 |
| [GPUI](https://github.com/zed-industries/zed/tree/main/crates/gpui) with [gpui-kit](https://github.com/longbridge/gpui-kit) | views that say they changed; its executor | Zed `main` at `1253dde`, 2026-11-06; `gpui` 0.2.2 on crates.io; gpui-kit 0.9.0, 2026-11-02, on `gpui-pre` 0.3.11 (Zed `f816e1f`, 2026-11-01) |
| [Iced](https://github.com/iced-rs/iced) | messages, as in Elm | 0.14.0, 2025-12-07; `master` 0.15.0-dev at `8ff48c4`, 2026-11-01 |
| [Makepad](https://github.com/makepad/makepad) | a format of layouts reloaded | `main`, crate version 2.0.0, tag `release-2026-11-06.5` |
| [Slint](https://github.com/slint-ui/slint) | a format of layouts reloaded | 1.18.1, 2026-09-21 |
| [Dioxus](https://github.com/DioxusLabs/dioxus) and [`subsecond`](https://docs.rs/subsecond/0.7.10/subsecond/) | Rust's code reloaded | 0.7.10, 2026-07-30 |
| [Flutter](https://docs.flutter.dev/tools/hot-reload) | code reloaded, the state kept | the documentation of 3.47, read on 2026-11-06; web reload as of 3.35 |
| Jetpack Compose: [Live Edit](https://developer.android.com/develop/ui/compose/tooling/iterative-development) and [Compose Hot Reload](https://github.com/JetBrains/compose-hot-reload) | code reloaded, the state kept | Live Edit's page of 2026-11-06; Compose Hot Reload 1.2.0, 2026-07-23 |
| [Rune](https://github.com/anomalyco/rune) | motion that runs no view again | `dev` at `ddf1414`, 2026-11-06; 0.0.1, no release |
| [SwiftUI](https://developer.apple.com/documentation/swiftui/) | read only, without a Mac to measure it | Apple's documentation of 2026-11-06, which names Xcode 27 |

Two facts weigh on every section:

- **Maturity.** Floem's last release is 0.2.0, of 2024-11-15, and its `main` depends on crates from
  git, so it cannot be published ([issue #1050](https://github.com/lapce/floem/issues/1050)). Rune
  was created on 2026-10-22, has no release and takes no outside pull requests
  ([README](https://github.com/anomalyco/rune/blob/ddf14140253bd1b963993895e3fa025d1ec58537/README.md)).
  Iced calls itself experimental (`src/lib.rs`, 0.14.0). GPUI warns of breaking changes between
  versions, and gpui-kit pins its snapshot of GPUI exactly for that reason (gpui-kit's
  `Cargo.toml`, 0.9.0).
- **Licences.** All are under MIT or Apache-2.0 but Slint: GPLv3, a royalty-free licence that
  requires its "About Slint" widget shown and forbids embedded systems, or a commercial licence
  ([`LICENSES/`](https://github.com/slint-ui/slint/tree/master/LICENSES), 1.18.1).

## 1. How state changes the interface

**uwui today, the control.** The program keeps its state. `Ui::build` runs a builder when the
revision that it reads moved, and matches the elements it adds with those before by their keys,
so that their state and scroll survive. `Ui::frame` styles again the elements that changed, lays
out the roots where something changed, draws again what changed, and counts each of these in
`FrameStats`. Lists build only the rows that show. A person's input becomes `Action`s, which the
program reads from a queue (`Ui::take_actions`). The revision is moved by hand: forgetting it
leaves the interface as it was
([`crates/uwui/README.md`](https://github.com/HoneySlatt/SlimeEngine/blob/10a3e738e75107df4c9228d29ebe95a3753e44dd/crates/uwui/README.md)).

**Signals: Floem.** The view function runs once; the README says so ("the view tree is constructed
only once", `main`).

- A signal is a `Copy` handle to a value kept in a thread's runtime. A closure that reads it,
  a style or a label, runs again when it changes, and nothing else does
  (`reactive/src/runtime.rs`, `src/views/decorator.rs`, `main`).
- Each signal, effect and memo belongs to a `Scope`. Disposing the scope frees them. A signal made
  in a scope that is never disposed lives until the runtime ends.
- A list, `dyn_stack`, runs its items' function again when its signals change, hashes every key
  and compares the set with the one before: a change costs O(n) in keys, and every row stays a live
  view. `virtual_stack` compares the rows that show alone (`src/views/dyn_stack.rs`,
  `src/views/virtual_stack.rs`, `main`).
- What an author learns: signals, effects, memos, scopes, "a read tracks, a write notifies", and two
  panics: a value borrowed twice, and a handle whose scope was disposed (`reactive/src/`, `main`).

Slint's properties and SwiftUI's `@Observable` work the same way, by tracking reads. A Slint
binding records each property it reads and is evaluated again lazily when one changes
([reactivity](https://github.com/slint-ui/slint/blob/master/docs/astro/src/content/docs/guide/language/concepts/reactivity.mdx),
1.18.1). SwiftUI runs a view's `body` again only when an observable property that `body` read
directly changes (iOS 17, macOS 14;
[migrating to `@Observable`](https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro)).

**Views that say they changed: GPUI.**

- The `App` owns every entity. An `Entity<T>` is a counted handle, read only through the `App`. A
  view is an entity that implements `Render`. It calls `cx.notify()` when it changed; others
  `observe` it or `subscribe` to its typed events (`_ownership_and_data_flow.rs`, Zed `1253dde`).
- Each frame of a window that changed calls `render` from the root view down, and lays out the
  element tree it gives. `Entity::cached` keeps a view's elements until it notifies, but it needs a
  size of its own, not measured from its content (`view.rs`, `window.rs`, `1253dde`).
- A view tree rendered incrementally was proposed and closed unmerged on 2026-09-24. Its
  description calls the frame a walk of the whole tree, and measured one row changed in Zed going
  from 765 µs to 285 µs with it
  ([PR #63800](https://github.com/zed-industries/zed/pull/63800)).
- `uniform_list` lays out only the rows that show, all of one height; `list` takes rows of any
  height through a `ListState` that the view keeps (`elements/uniform_list.rs`,
  `elements/list.rs`).
- What an author learns: `App`, `Window`, `Context<T>`, `Entity` and `WeakEntity`, `Render` and
  `RenderOnce`, `notify` and `emit`, element identifiers. A view that changes its state without
  `notify` stays as it was; a cached view that does not notify goes stale.

**Messages: Iced.**

- `update(&mut State, Message) -> Task<Message>` changes the state; `view(&State) ->
  Element<Message>` describes the interface (`src/lib.rs`, 0.14.0).
- After each batch of messages, the runtime calls `update`, then `view` for every window, compares
  the new elements with its tree of widgets, and lays out from the root
  (`winit/src/lib.rs`, `runtime/src/user_interface.rs`, 0.14.0). Since 0.14, a frame is drawn only
  after an update or when a widget asks
  ([PR #2662](https://github.com/iced-rs/iced/pull/2662)).
- `keyed::column` keeps state with the right item when items move; its documentation says "the
  whole widget tree is rebuilt during every `view` call" (`widget/src/keyed.rs`, 0.14.0). `lazy`
  builds its content again only when the hash of what it depends on changes.
- Iced has no list that builds only its rows that show: "we don't have a `list` widget"
  ([issue #3429](https://github.com/iced-rs/iced/issues/3429), closed 2026-08). 0.14 adds a
  `table` and a `grid`.
- What an author learns: the state, `Message`, `update`, `view`, `Element`, `Task`,
  `Subscription`, `Theme` ([the book's architecture](https://book.iced.rs/architecture.html)).

**Retained widgets: Makepad.** Widgets are kept and handle events (`handle_event`, `draw_walk`),
and emit actions that the application reads. Nothing tracks what a value is read by: "array
changes do NOT re-render" ([`docs/agents/splash.md`](https://github.com/makepad/makepad/blob/main/docs/agents/splash.md),
`main`).

**A view run again, then motion apart: Rune.** An application is `fn view(&State, &mut Cx) -> El`.
Its handlers change the state between frames; then the view runs again and a comparison retargets
the properties' tracks. Elements are named by keys (`examples/hello/src/main.rs`,
`crates/rune/README.md`, `ddf1414`). It is today's uwui with the comparison done by the
framework, and its motion apart, as section 5 says.

What it tells M6d.1b:

- No framework read lets the cost of its model be measured apart from the rest of it: GPUI walks
  its whole tree, Iced lays out from its root. M6d.1b measures the models on uwui's own tree
  ([ADR-0202](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0202-how-m6d1-compares-ways-of-writing-an-application.md)).
- Each model has a mistake that the compiler lets through: a revision not moved (uwui), a
  `notify` forgotten (GPUI), a key forgotten (Iced, Rune), a value read outside a tracking scope
  (signals).

## 2. The format of layouts

Of the references, only Makepad and Slint write layouts outside Rust. Floem, GPUI, Iced, Rune and
SwiftUI write them in code; Dioxus writes them in a macro of Rust, RSX.

**Makepad: Splash.** A dynamic language, written inside Rust's files in a `script_mod!` macro. The
compiled text is kept, and the same text is read again from the file and run in a virtual machine
when it changes (`platform/src/live_reload.rs`, `main`).

```text
main_view := View{ flow: Down spacing: 12 align: Center
  Label{ text: "Count: " + state.counter } }
```

- Its errors show at run time, and its own guide for agents lists silent failures: `height: Fit`
  needed on every container, `for` loops drawn only when built
  ([`docs/agents/splash.md`](https://github.com/makepad/makepad/blob/main/docs/agents/splash.md)).
- Rust binds to it through structures derived with `#[derive(Script)]`, values placed with
  `#(...)`, and `script_eval!`. Its shaders are written in it too.
- Its tools: Studio, and a "tweaker" that edits the `script_mod!` blocks in the source. No language
  server and no formatter were found.
- The archived `live_design!` that preceded it "is not the reference for current APIs": the format
  changed wholly between 1.0 (crates.io, 2025-05-13) and `main`.

**Slint: `.slint`.** A typed language, with properties `in`, `out` and `in-out`, callbacks and
global singletons, read at compile time by a macro or `build.rs`, or at run time by
`slint-interpreter` (`api/rs/slint/lib.rs`, 1.18.1).

```text
export component HelloWorld inherits Window {
    Text { text: "hello world"; color: green; }
}
```

- Rust calls generated functions: `set_<property>`, `on_<callback>`, `global::<T>()`.
- Its tools: a language server with a formatter, extensions for several editors, a viewer and an
  online editor, a tree-sitter grammar.
- Its FAQ defends a language of its own for "strictly typed binding expressions"
  ([`FAQ.md`](https://github.com/slint-ui/slint/blob/master/FAQ.md)).

**Dioxus: RSX.** Markup, text attributes and literal properties change without compiling; new
Rust expressions, logic outside RSX and a component's signature need a build or a patch
([hot reload guide](https://dioxuslabs.com/learn/0.7/essentials/ui/hotreload/), 0.7).

### Notations for trees, and code that reaches a file's elements

Read on 2026-11-09 for SlimeEngine's M6d.1d2a, which chose the notation of layouts.

- **KDL 2.0**, a document language of nodes with arguments, properties and children, final since
  2024-12-22 ([kdl.dev](https://kdl.dev)). Its Rust reader `kdl` 6.7.1 (2026-05-31, Apache-2.0)
  reads KDL 2, keeps a document's formatting and comments when it is changed and written back,
  and has a `serde` that its changelog calls experimental; it depends on `miette`, `num-traits`
  and `winnow` 0.7. tree-sitter-kdl 2.0.0 (2026-09-09) reads KDL 1 and 2; Neovim's pins it;
  Helix's and Zed's grammars predate KDL 2; VS Code's `kdl-org.kdl` 2.1.3 reads KDL 2; `kdl-lsp`
  gives diagnostics alone; `kdlfmt` formats. niri, through `knuffel`, and Zellij, through `kdl`
  4.5, are on KDL 1. KDL 1 and 2 differ on keywords, `true` against `#true`, and on raw strings.
  M6d.1d2a's prototype found that `kdl` 6.7.1 reads by recursion without a bound
  ([measured](measurements.md#a-layouts-change-seen-2026-11-09)).
- **TOML 1.1**, released on 2025-12-18, lets an inline table span lines with a trailing comma.
  `toml` parses it from 0.9.10, `toml_edit` from 0.24.0. taplo's last release is 0.10.0
  (2025-05-23); its author left the project in 2024, and an issue asking for TOML 1.1 was answered
  "No" in 2026-01. tombi reads TOML 1.1 behind its `toml-version` option, 1.0 by default. TOML's
  specification says that a table's pairs are "not guaranteed to be in any specific order".
- **How code reaches a file's elements.** Android's View Binding generates a class for each
  layout, its mismatches failing "at compile time rather than at runtime"; XAML's `x:Name` becomes
  a field generated when the program is built; GTK's Blueprint compiles to GtkBuilder's XML, which
  its README calls verbose, and gtk-rs's `#[template_child]` matches a template's ids by name;
  Unity's UXML is XML, its elements found by `Q("name")` while the program runs; Qt's `.ui` files
  become a structure of pointers through `uic`, and `findChild` finds a name while it runs; Slint
  generates setters and callbacks for a component's top-level properties alone; Makepad finds
  elements by `ids!` while it runs.

## 3. The three reloads

A reload is three questions, answered apart
([ADR-0199](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0199-uwuis-targets-tools-and-references-narrowed.md)).

### A style or a layout

- **Makepad**, desktop: started with `--hot`, a watcher hands the changed `script_mod!` blocks to
  the virtual machine. An edit that changes the number of blocks or of `#(...)` values is refused
  with a message; an edit is checked before it is installed. The application's data, the widgets'
  identities and the text being edited survive
  ([`widgets/themes/README.md`](https://github.com/makepad/makepad/blob/main/widgets/themes/README.md)).
  On the web, a development server sends changes over a WebSocket (`platform/src/os/web/`); that
  path was read in the code, not tried. On Android: not found.
- **Slint**, since 1.13.0 (2025-09-03): built with `SLINT_LIVE_PREVIEW=1` and the feature
  `live-preview`, the interpreter reads `.slint` files again when they change. The properties,
  callbacks and models that Rust set are kept; a syntax error keeps the previous version shown. A
  property renamed, or a new one that Rust uses, needs a build. Not for release builds
  ([live preview](https://github.com/slint-ui/slint/blob/master/docs/astro/src/content/docs/guide/tooling/live-preview.mdx)).
  Documented for Rust, C++ and Node.js; on the web and Android: not documented.
- **uwui today**: `Ui::set_style` takes new style sheets and themes while the interface runs, and
  styles it again; no program of SlimeEngine reads them again when their files change.
- **gpui-kit**: its themes are JSON files that `ThemeRegistry::watch_dir` reads again when they
  change, except on the web (`crates/component/src/theme/registry.rs`, 0.9.0).
- **Dioxus**: RSX, as above, on every platform it runs on.
- No reference gives the latency of this reload.

### A function's body

The reloads of Dioxus, Iced, GPUI, Slint, Flutter and Compose were timed on their "Hello, World!",
from a change saved to the frame that shows it, and Makepad's tried:
[`measurements.md`](measurements.md#the-rivals-reloads-2026-11-07).

- **`subsecond`**, Dioxus 0.7.10
  ([docs.rs](https://docs.rs/subsecond/0.7.10/subsecond/)): calls made through `subsecond::call`
  go through a table of the latest functions' addresses. A tool outside the program, `dx`, compiles
  the change, links it against the running program's addresses, and sends the new table; on a
  patch, the stack unwinds to the nearest `call` and runs again.
  - Which crates are patched: docs.rs still says only the crate that holds `main`; `dx` patches
    every crate of a workspace since Dioxus 0.7.4, 2026-03-28
    ([PR #5291](https://github.com/DioxusLabs/dioxus/pull/5291)), which GPUI's integration relies
    on ([PR #65738](https://github.com/zed-industries/zed/pull/65738)). A dependency outside the
    workspace is not patched.
  - Statics' initialisers are not run again; thread-locals of the patched crate seem to reset.
  - Active only with `debug_assertions`.
  - Platforms: Linux, macOS, Windows, Android (arm64 and armv7), iOS's simulator alone, and
    wasm32.
  - Its author gave some 130 ms from a save to the patch on an M4 Mac, for 0.7's first alphas
    ([comment](https://news.ycombinator.com/item?id=44371543), 2025-06-24).
- **Iced 0.14**, feature `hot`, "very, very experimental": `update`, `view`, `title` and
  `subscription` called through `subsecond`, run by `cargo hot`. A patch runs `view` again; the
  state is kept and no message is replayed. Only the root crate is reloaded. Not on wasm; on
  Android, not documented ([PR #3000](https://github.com/iced-rs/iced/pull/3000);
  `src/hot.rs` on `master`).
- **GPUI**, `main` since 2026-10-17, feature `hot-reload`, through `subsecond` and `dx serve
  --hot-patch`: "every view and component render (and any code those renders call)", the state
  kept. The phases of a custom element are not patched. Not on the web yet, listed as to follow
  ([PR #65738](https://github.com/zed-industries/zed/pull/65738)). `gpui` 0.2.2 on crates.io does
  not have it; gpui-kit does not use it.
- **Rune**, feature `hot`, through Dioxus's CLI 0.7.10: function bodies patched; "scroll offsets,
  app state and spring tracks stay in the runtime"; a patched view that panics falls back to the
  original. Its own figure: "median save-to-GPU time is about 8 s for Settings, short of the
  one-second target" (`crates/rune/README.md`, `ddf1414`).
- **Makepad**: Relax, a compiler of Rust to its own runtime, added on 2026-10-31, applies function
  bodies and some initialisers in one transaction; a change of signature or layout restarts in
  place (`libs/relax/compiler/src/reload.rs`, `main`). Its maturity was not checked.
- **Flutter**: the Dart virtual machine loads the changed libraries; "methods are the atoms" of a
  reload; no code runs again, then the framework builds, lays out and paints every widget again.
  `main()` and `initState()` do not run again. One figure, an example: "Reloaded 1 of 448 libraries
  in 978ms" ([hot reload](https://docs.flutter.dev/tools/hot-reload);
  [the VM's design](https://github.com/dart-lang/sdk/blob/main/runtime/docs/hot-reload.md)). Android
  and iOS; the web by default since 3.35
  ([web building](https://docs.flutter.dev/platform-integration/web/building)). In debug builds
  only.
- **Jetpack Compose**: Live Edit, on Android only, "only supports editing a function body"; it
  resets the state at the first change of a file
  ([iterative development](https://developer.android.com/develop/ui/compose/tooling/iterative-development)).
  Compose Hot Reload, on the desktop only, redefines classes in the JetBrains Runtime; `remember`ed
  state survives unless its scope is invalidated
  ([README](https://github.com/JetBrains/compose-hot-reload),
  [Kotlin's documentation](https://kotlinlang.org/docs/multiplatform/compose-hot-reload.html)).
- **SwiftUI**: Xcode's previews stay "up to date as you change the view's code"
  ([previews](https://developer.apple.com/documentation/swiftui/previews-in-xcode)); whether state
  survives is not documented. A reload of a running application is a third party's, InjectionIII.

### A type whose state migrates

No reference migrates a value whose type changed.

- `subsecond` "does not support hot-reloading of structs"; a changed layout used by new code on
  old values can crash. The framework must discard or rebuild its state; Dioxus rebuilds it
  ([docs.rs](https://docs.rs/subsecond/0.7.10/subsecond/)).
- Iced asks for a cold start when `State` or `Message` change: "Types have changed. Restart to
  re-enable hotpatching" (`devtools/src/lib.rs`, 0.14.0).
- Rune restarts on a change of state's types, signatures or `setup`, and migrates nothing.
- Flutter accepts fields added and removed, keeping the others' values; a renamed field loses its
  value; a class turned into an enum, or a change in the number of type arguments, is refused at
  once, and the program goes on unchanged
  ([the VM's design](https://github.com/dart-lang/sdk/blob/main/runtime/docs/hot-reload.md)).
- Compose Hot Reload keeps old instances when fields are added, the new ones at the JVM's
  defaults; read in its author's post of the prototype, December 2024
  ([post](https://blog.sellmair.io/say-hello-to-compose-hot-reload-firework)), not in its current
  documentation.

What it tells M6d.1c: in Rust, a type's state survives a change of the type only through a form
that does not depend on its layout, written before the patch and read after it, as `serde` would
write it. The framework must own the state it keeps, so that it can rebuild it.

## 4. The executor and its waker

- **GPUI.** A foreground executor runs futures that are not `Send` on the main thread; a
  background one runs the others. `cx.spawn` hands its closure a weak handle to its entity.
  Dropping a `Task` cancels it; `detach` lets it run. Dropping the entity does not cancel its
  tasks: they fail when they next reach it (`scheduler/src/executor.rs`, `app/context.rs`,
  `1253dde`).
  - The waker: on Linux, a `calloop` ping, a pool of threads and one thread of timers; on Windows,
    `PostMessageW`; on macOS and iOS, Grand Central Dispatch; on the web, workers and `setTimeout`.
  - Tests: a `TestScheduler` with a seed, `run_until_parked`, and simulated time,
    `advance_clock` (`crates/scheduler`, `app/test_context.rs`).
- **Iced.** An `Executor` trait, its back end chosen by a feature, `tokio`, `smol` or a pool of
  threads; `wasm_bindgen` on the web. `Task::abortable` gives a handle that cancels; a
  `Subscription` is started and stopped as `subscription(&State)` changes. The waker sends through
  winit's `EventLoopProxy` (`futures/src/`, `runtime/src/task.rs`, `winit/src/proxy.rs`, 0.14.0).
  Its test emulator runs tasks; a simulated clock was not found (`test/src/emulator.rs`).
- **Floem.** A future runs in an effect of the current scope, on the event loop; its waker queues a
  trigger and sends an idle event to winit's proxy. Disposing the scope drops the future
  (`src/receiver_signal/common/executors.rs`, `src/ext_event.rs`, `main`). Its headless harness
  has no clock to move (`src/headless.rs`).
- **Slint.** `spawn_local` runs a future on the event loop, from the main thread;
  `invoke_from_event_loop` carries a closure from another thread (`api/rs/slint/lib.rs`, 1.18.1).
- **Makepad.** `Cx::post_action` from any thread, `UiRunner` for a closure on the interface's
  thread (`platform/src/action.rs`, `platform/src/ui_runner.rs`).
- **Rune.** No asynchronous runtime: `rune::Latest` runs the newest request on up to four shared
  threads, and its answer reaches the state on the interface's thread; `spawn_local` on the web
  (`crates/rune/README.md`).
- **SwiftUI.** `.task` starts work with a view and cancels it "if the task hasn't finished when
  SwiftUI removes the view or the view changes identity"; `task(id:)` starts it again when the
  value changes ([`task`](https://developer.apple.com/documentation/swiftui/view/task(priority:_:)),
  iOS 15, macOS 12).

What it tells M6d.1c: SwiftUI and Floem bind a task to the life of its view or its scope; GPUI and
Rune bind it to a value that the code keeps, a `Task` or a `Latest`. GPUI alone runs tests on
simulated time, which
[ADR-0190](https://github.com/HoneySlatt/SlimeEngine/blob/main/docs/adr/0190-uwuis-requirements.md)
asks of uwui's executor.

## 5. The time that motion reads, and motion that runs no view

- **Rune.** "Animation samples tracks at frame time; it never re-runs view functions"
  (`crates/rune/src/runtime.rs`, `ddf1414`).
  - A frame advances the scene's time and gets the nodes whose values changed: rectangle,
    opacity, transform, blur, radius, fill, mask. Layout runs once, at the target state, when the
    state changes; animated rectangles are interpolated (`crates/rune/src/runtime/frame.rs`,
    `crates/rune-motion/README.md`).
  - Scrolling, hover and press move tracks and run no view; starting or retargeting an animation
    needs the view run once, since the comparison makes the track.
  - The time: "use the timestamp the frame will be shown at, not the current time". On macOS, a
    `CVDisplayLink`'s target; on Linux and Windows, `Instant::now()` for now
    (`crates/rune/src/window/draw.rs`). A late frame charges motion the real gap, up to 0.25 s; a
    headless run uses a clock moved by hand, its traces identical to the bit.
  - Springs keep position and speed when retargeted, checked by tests. Its author's figures, on
    Apple's chips: 17 ns to sample a spring, 0.76 ms a frame for 10,000 rectangles moving, nothing
    allocated in a steady frame.
  - Reduced motion: travel, scale, shape and blur change at once, opacity and colour fade briefly.
- **SwiftUI.** Built-in effects, as `scaleEffect`, animate "off the main thread and without calling
  into any of your view code"; a custom `Animatable` view runs `body` and layout at every frame
  ([WWDC23, "Explore SwiftUI animation"](https://developer.apple.com/videos/play/wwdc2023/10156/)).
  Springs keep their speed when another replaces them
  ([`Animation`](https://developer.apple.com/documentation/swiftui/animation)). Where the time comes
  from is not documented.
- **GPUI.** `with_animation` reads `cx.background_executor().now()` during layout, which tests can
  move. While it runs, it asks for the next frame, which notifies the view: the view's `render` runs
  at every frame (`elements/animation.rs`, `window.rs`, `1253dde`). It honours `reduce_motion`.
- **Iced.** `Animation<T>` takes the time it is given, an `Instant`; `window::frames()` gives one per
  frame. Each frame is a message: `update`, then `view`, run again (`core/src/animation.rs`,
  `runtime/src/window.rs`, 0.14.0). `master` adds a `FrameClock` that steadies frames' gaps
  ([PR #3527](https://github.com/iced-rs/iced/pull/3527)).
- **Floem.** A style pass reads one `Instant::now()` for all its views; transitions step with it.
  No code of a view runs, by reading of the code (`src/window/handle.rs`,
  `src/style/transition.rs`, `main`).
- **Slint.** `animate` plays when a property changes; the time is the platform's monotonic clock
  (`internal/core/animations.rs`, 1.18.1).
- **Makepad.** An `Animator`, driven by `Event::NextFrame`, writes values into shaders' instances
  (`widgets/core/src/animator.rs`).
- **uwui today.** `Ui::advance` takes the time that the program gives each frame; transitions move
  colours, opacity and a section's height without running a builder
  ([`crates/uwui/README.md`](https://github.com/HoneySlatt/SlimeEngine/blob/10a3e738e75107df4c9228d29ebe95a3753e44dd/crates/uwui/README.md)).

What it tells M6d.1d: Rune and SwiftUI's built-in effects keep motion out of the views; GPUI and
Iced run views at every frame of an animation. Only Rune reads the time a frame will be shown, and
only on macOS.

### What platforms give of a frame's time

Read on 2026-11-09 for SlimeEngine's M6d.1d2b: what each platform tells a program of when a frame
shows, and of when an input happened, in each one's current documentation. Nothing was run.

| Platform | A frame's time of presentation | Input's times | Comparable |
|---|---|---|---|
| Wayland | past: `wp_presentation`'s `presented`, the time the content "turned into light the first time", in the clock that `clock_id` names, with `refresh`, the next refresh predicted, and `seq` ([`presentation-time.xml`](https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/stable/presentation-time/presentation-time.xml), stable, version 3); a time asked "not before", `wp_commit_timing_v1` (staging); `wl_surface.frame`'s `done` is "the current time, in milliseconds, with an undefined base" | milliseconds "with an undefined base"; nanoseconds through `zwp_input_timestamps_v1` (unstable), in the same domain | not promised: `clock_id` "implies nothing about" input's times |
| macOS 14 and later, iOS | future: `CADisplayLink.targetTimestamp`, "when the next frame displays"; past: `timestamp` ([Apple](https://developer.apple.com/documentation/quartzcore/cadisplaylink/targettimestamp)); `CVDisplayLink`'s functions deprecated in macOS 15 | `NSEvent`'s and `UIEvent`'s `timestamp`, seconds since the system started | likely, not stated |
| Android | future, from API 33: `FrameTimeline.getExpectedPresentationTimeNanos()`, "expected to be presented", in `System.nanoTime()`; before, `doFrame(frameTimeNanos)`, the frame's start, whose use for animations "causes animations to skip forward after late frames" ([Choreographer](https://developer.android.com/reference/android/view/Choreographer.FrameData)) | `getEventTimeNanos()` (API 34) and `getEventTime()`, in `uptimeMillis()`'s base | yes, documented |
| Windows | past: `DXGI_FRAME_STATISTICS.SyncQPCTime`, in flip model or full screen only, "not reliable in many multiple monitor scenarios"; `DWM_TIMING_INFO`'s `qpcVBlank` and `qpcRefreshPeriod`, for the whole desktop; a time asked, `IPresentationManager`'s `SetTargetTime`, from build 22000 ([DXGI](https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiswapchain-getframestatistics)) | `GetMessageTime`, milliseconds of the tick count, which wraps; `POINTER_INFO.PerformanceCount`, the performance counter | `PerformanceCount` with DXGI's and DWM's times, yes; the tick count no; the presentation manager's interrupt time and the performance counter are two clocks, their conversion not documented |
| The web | none: `requestAnimationFrame`'s argument is the event loop's "last render opportunity time", in milliseconds since the time origin, coarsened to 100 µs, 5 µs when cross-origin isolated ([HTML](https://html.spec.whatwg.org/multipage/webappapis.html#event-loop-processing-model)) | `Event.timeStamp`, from the same origin | yes |
| winit 0.30.13 | none; Wayland's frame callback's time dropped (`wayland/state.rs`); `MonitorHandle::refresh_rate_millihertz()` gives the mode's rate | none: `KeyEvent` and `Touch` carry no time | — |
| wgpu 30.0.1 | none: `Adapter::get_presentation_timestamp()` reads the current time in the presentation's clock; `VK_GOOGLE_display_timing` only through `as_hal` | — | — |

`std::time::Instant::now()` panics on `wasm32-unknown-unknown`, "time not implemented on this
platform" (std's `sys/time/unsupported.rs`, read on Rust's `master`); on WASI it reads
`CLOCK_MONOTONIC`. The crate `web-time` gives an `Instant` on `performance.now()`, and winit uses
it on the web.

What it tells M6d.1d2b: a future time of presentation exists on Apple and on Android from API 33,
a past one on Wayland and Windows, none on the web. Neither winit nor wgpu passes any on,
so uwui's hosts read them with code of their own.

### More of a frame's time, of power and of clocks

Read on 2026-11-09 for SlimeEngine's M6d.1d2b2, in each platform's current documentation or, where
said, its code. Nothing was run.

- **X11's Present extension.** `PresentCompleteNotify` gives `ust` and `msc`, "the frame count and
  system time when the presentation actually occurred": a past time
  ([`presentproto.txt`](https://gitlab.freedesktop.org/xorg/proto/xorgproto/-/raw/master/presentproto.txt),
  version 1.4). A future time is asked, never given: `PresentPixmap`'s `target-msc`, `divisor` and
  `remainder`; its option of a time in `ust`, Mesa says, "xserver does not implement it at all".
  - `ust`'s clock and unit are not in the protocol. In the X server's and Mesa's code they are
    microseconds of `CLOCK_MONOTONIC`.
  - Xwayland implements Present without Wayland's `wp_presentation`: at each frame callback it adds
    one to `msc` and sets `ust` to the time now (`xwayland-present.c`), so its `ust` is when the
    callback came, not when the image showed.
  - Input: the core protocol's times are milliseconds that "wrap around (after about 49.7 days)";
    XInput2's too. The X server reads them from `CLOCK_MONOTONIC` (its code); no text ties them to
    `ust`.
- **Android.** No method `getAnimationTimeNanos` exists: `FrameData.getFrameTimeNanos`'s page links
  to one that the API lacks
  ([`FrameData`](https://developer.android.com/reference/android/view/Choreographer.FrameData)).
  `FrameTimeline` (API 33) gives `getDeadlineNanos()`, "which this frame needs to be ready by",
  beside the expected presentation time. A past presentation exists from API 35:
  `SurfaceControl.TransactionStats.getPresentFence()`, a fence whose `getSignalTime()` is in
  `CLOCK_MONOTONIC`; the NDK's `ASurfaceTransactionStats_getPresentFenceFd` from API 29. A time is
  asked through `setDesiredPresentTimeNanos` (API 35; the NDK's from 29). A surface asks for a rate
  through `Surface.setFrameRate` (API 30), which "won't introduce frame rate throttling", and a view
  through `View.setRequestedFrameRate` (API 35); with the adaptive refresh rate of Android 15 QPR1,
  the rate is "the highest vote".
- **Windows' presentation manager** (`presentation.h`, build 22000). Its statistics are of three
  kinds: a present's status (queued, skipped, cancelled) and a composition frame's, with no time;
  and an independent flip's, `GetDisplayedTime()` and `GetPresentDuration()`, in the system's
  interrupt time, 100 ns since the start. `SetTargetTime` asks: "The system will attempt to display
  the present as close to the specified time as possible." How interrupt time converts to the
  performance counter is not documented. DXGI's `SetMaximumFrameLatency`, on a swap chain made with its waitable object, sets the frames
  queued, 1 by default; no count of frames in flight is given.
- **Apple's rate.** `CADisplayLink.preferredFrameRateRange`, iOS 15 and macOS 14, "a range of
  frequencies your app allows", best effort; "the system disables faster refresh rates in low power
  mode or if a device gets hot".

| Platform | Saving power | On battery | Its change |
|---|---|---|---|
| Windows | `PowerManager.EnergySaverStatus` (10240); effective power mode notifications (1809) | `SYSTEM_POWER_STATUS.ACLineStatus` | `EnergySaverStatusChanged`; `GUID_POWER_SAVING_STATUS` |
| macOS, iOS | `ProcessInfo.isLowPowerModeEnabled` (iOS 9, macOS 12) | IOKit's power sources on macOS; `UIDevice`'s battery state on iOS | `NSProcessInfoPowerStateDidChange` |
| Android | `PowerManager.isPowerSaveMode()` (API 21) | `BatteryManager.isCharging()` (API 23) | `ACTION_POWER_SAVE_MODE_CHANGED`, to receivers registered |
| Linux | the portal's `PowerProfileMonitor`, `power-saver-enabled` (portal 1.10.0) | UPower's `OnBattery` | not named on the pages read |
| The web | none | `getBattery()`: Chrome; Firefox only from 43 to 52; Safari none | — |

WebKit halves `requestAnimationFrame` to 30 a second in Low Power Mode, by its code
(`AnimationFrameRate.cpp`), not its documentation.

| Clock | Counts a suspend |
|---|---|
| Linux's `CLOCK_MONOTONIC` / `CLOCK_BOOTTIME` ([`clock_gettime(2)`](https://man7.org/linux/man-pages/man2/clock_gettime.2.html)) | no / yes |
| Windows' performance counter / unbiased interrupt time | yes / no |
| Apple's `mach_absolute_time` / `mach_continuous_time` | no / yes |
| Android's `uptimeMillis()` / `elapsedRealtime()` | no / yes |
| The web's `performance.now()` | not specified; Windows' browsers only, by MDN |
| Rust's `std::time::Instant` | not specified: `CLOCK_MONOTONIC` on Linux and `CLOCK_UPTIME_RAW` on macOS, no; the performance counter on Windows, yes |

Civil time: `std::time::SystemTime::now()`, as `Instant::now()`, panics on
`wasm32-unknown-unknown`. The system tells a program that its clock changed on Windows
(`WM_TIMECHANGE`), Linux (`timerfd` with `TFD_TIMER_CANCEL_ON_SET`, which systemd's `timedate1`
names for it), Apple (`NSSystemClockDidChange`) and Android (`ACTION_TIME_CHANGED`); that its zone
changed on Linux (`timedate1`'s `Timezone`), Apple (`NSSystemTimeZoneDidChange`) and Android
(`ACTION_TIMEZONE_CHANGED`), not documented on Windows; the web has no such event, and reads its
zone from `Intl.DateTimeFormat().resolvedOptions().timeZone`.

What it tells M6d.1d2b2: X11 gives a past presentation's time as Wayland and Windows do, Xwayland
none; Android adds a past one from API 35. The clocks that platforms give for frames and input stop
during a suspend, except Windows'. A power-saving state exists everywhere but the web.

## 6. An application started in one call

| Reference | Its start |
|---|---|
| uwui today | none: the program makes a `Ui`, adds its roots and calls each frame from its own loop, as SlimeEngine's `slime-app` does for the editor |
| Floem | `floem::launch(\|\| "Hello, World!")` (`src/app/mod.rs`, `main`) |
| GPUI | `gpui_platform::application().run(\|cx\| …)`, then `cx.open_window` with a root view (`crates/gpui/README.md`) |
| gpui-kit | `gpui_kit::init(cx)` first, then `gpui_kit::open_window(…)`, which wraps the view in its `Root` (`crates/kit/src/lib.rs`, 0.9.0) |
| Iced | `iced::run(update, view)` (`src/lib.rs`, 0.14.0) |
| Slint | `HelloWorld::new().unwrap().run().unwrap()` (`api/rs/slint/lib.rs`, 1.18.1) |
| Makepad | `app_main!(App);` (`examples/counter/src/main.rs`, `main`) |
| Dioxus | `dioxus::launch(app)`, on the renderer that its features choose (`examples/01-app-demos/hello_world.rs`, 0.7.10) |
| Rune | `rune::run(AppSpec::new("Hello", (320.0, 200.0), State::default, view))` (`examples/hello/src/main.rs`) |
| SwiftUI | `@main struct MyApp: App { var body: some Scene { WindowGroup { … } } }` ([`App`](https://developer.apple.com/documentation/swiftui/app)) |

The ten "Hello, World!" of [`references/hello-world/`](../references/hello-world/README.md) hold
the whole programs.

## 7. Styles written in code, beside themes

- **gpui-kit**: themes in JSON files with a schema, 21 shipped; styles in code through GPUI's
  methods, `.v_flex().gap_2()`, and states, `hover`, `active`, `focus`
  ([`docs/STYLING-AND-MOTION.md`](https://github.com/longbridge/gpui-kit/blob/main/docs/STYLING-AND-MOTION.md)).
- **Iced**: each widget's `.style(|theme, status| …)`; a `Catalog` trait for each widget, which a
  theme implements; built-in themes and `Theme::custom`; palettes made in OKLCH since 0.14
  (`widget/src/button.rs`, 0.14.0).
- **Floem**: `.style(|s| …)` with typed properties, classes declared by `style_class!` that a
  parent's style may target, a default design system in `src/style/theme.rs` (`main`).
- **Slint**: styles chosen at build time, `fluent`, `material`, `cupertino`, `cosmic`, `qt`, each
  light and dark; shared values in global singletons
  ([style](https://github.com/slint-ui/slint/blob/master/docs/astro/src/content/docs/reference/std-widgets/style.mdx)).
- **Makepad**: themes are Splash sheets read again when chosen, each two files: `theme.splash`,
  the tokens that widgets read, and `widgets.splash`, assignments on widgets' kinds, a face's
  shader among them (`widgets/sheets/themes/<id>/`, 39 themes, commit `506ec05`, read on
  2026-11-09).
- **Rune**: tokens in Rust values, colours in OKLCH, a motion palette; a crate maps another design's
  `theme.json` onto its kit (`themes/opencode`).
- **SwiftUI**: styles are code, `ButtonStyle` and modifiers passed down the environment; no theme
  file.
- **uwui today**: style sheets and themes read from files, the element's own style over the
  rules, colours computed in OKLCH.

## 8. Reloads on the web and on Android

What each model's reload of a function's body does on the two platforms besides the desktop; a
style's or a layout's reload, and a type's migration, are in [section 3](#3-the-three-reloads).
"Not documented" means that no source read says either way.

| Reference | Model | Web | Android |
|---|---|---|---|
| uwui today | rebuild by keys | not built; through `subsecond`, as any model of Rust | not built; through `subsecond`, as any model of Rust |
| `subsecond` (Dioxus) | signals | a function's body: yes | a function's body: yes |
| Iced, `hot` | messages | no (compiled out on wasm32) | not documented |
| GPUI, `hot-reload` | views that say they changed | no, to follow | GPUI has no Android port in Zed's repository |
| Rune, `hot` | a view run again | no: "desktop development" only (`crates/rune/README.md`) | Android is not among Rune's platforms |
| Makepad | retained widgets | Splash, over a WebSocket, read in the code | not documented |
| Slint, live preview | properties | not documented | not documented |
| Flutter | widgets built again | yes, by default since 3.35 | yes |
| Compose | composition | no (Hot Reload is for the desktop) | Live Edit, function bodies only |

What it tells M6d.1c: `subsecond` is the only tool for Rust's code that covers the web and Android;
a model that owns its views' entry points can call through it on each.

## 9. Themes that change a component's structure

Read on 2026-11-09 for SlimeEngine's M6d.1d1: what a theme holds, and whether it may change the
tree of parts that a component draws, as a switch drawn as a box with a tick in one theme and as
a pill with a thumb in another. Each reference was read in its documentation and source at the
version named.

| Reference | Values | Rules that select | The parts' tree changed by a theme |
|---|---|---|---|
| Qt Quick Controls 6.12.0 | a typed `palette`; an attached `Material` or `Universal` | none: one QML file per control | yes: a style is "a set of QML files within a single directory", each control's file rooted in its behaviour's type from `QtQuick.Templates`, its parts `background`, `contentItem`, `indicator` ([customizing](https://doc.qt.io/qt-6/qtquickcontrols-customize.html)) |
| WPF, WinUI 3 | typed resources by key; WinUI's `ThemeResource` for light, dark and high contrast | `Style` by type or key, with triggers | yes: a `ControlTemplate` replaces the control's tree whole, under the parts that `TemplatePartAttribute` names, `PART_EditableTextBox` for one ([WPF](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/creating-a-control-that-has-a-customizable-appearance)) |
| Slint 1.18.1 | typed globals, `Palette` and `StyleMetrics` | none | yes, as each style re-implements each widget whole, behaviour and accessibility included (`internal/compiler/widgets/*/switch.slint`); styles chosen at build time, `fluent` by default |
| Flutter 3.47.9 | typed `ThemeData`, `ThemeExtension` | none: each widget merges its theme's layers | no: another structure is another widget, `Switch.adaptive` choosing Material's or Cupertino's; both now packages of their own, `material_ui` and `cupertino_ui` |
| Jetpack Compose, `androidx-main` | typed `CompositionLocal`s | none | no: a design system is a library of components; slots, as `Switch`'s `thumbContent`, are the one structural hook ([custom design systems](https://developer.android.com/develop/ui/compose/designsystems/custom)) |
| gpui-kit 0.9.0 | JSON themes read into typed colours, 21 shipped | none: tokens applied by code | no from a JSON theme; a look of another shape is another layer over `gpui-base`, which "owns reusable behavior and the geometry required to implement it" (`docs/ARCHITECTURE.md`) |
| Iced 0.14.0 | a typed `Palette` | a `Catalog` trait per widget: a class and a status give a `Style` | no: the widget's `draw` is fixed |
| Floem, `1351ffb` | a typed `DesignSystem` | one `Style` that targets classes of `style_class!` | no: views paint themselves |
| Makepad, `506ec05` | `theme.splash`'s tokens | assignments on widgets' kinds in `widgets.splash` | partly: a sheet rewrites a widget's face, its shader, over the tree that exists; no sheet read adds or removes parts |
| Radix Primitives, React Aria | none | the application's CSS, on `data-state` and default classes | the application writes the tree out of the library's parts; the library keeps roles, focus and keys |

What they hold for the contract between a component and the parts that a theme gives it:

- Behaviour and accessibility stay with the control, not its parts: Qt's role is the template's
  (`QQuickAbstractButton::accessibleRole`), WinUI's and WPF's the control's automation peer,
  Radix's the root's `role="switch"`.
- A part left out must not break the control: WPF's rule is "Your control should not throw an
  exception or report an error if a FrameworkElement, VisualState, or VisualStateGroup is missing
  from the ControlTemplate"; Qt's template tests each part, `if (indicator)`. Radix leaves it to
  the author: "it is your responsibility to ensure it remains accessible and functional".
- A control made of others needs each of them styled: Qt asks a style for both `ScrollBar.qml`
  and `ScrollView.qml`; WPF's parts may be controls, `PART_EditableTextBox` a `TextBox`.
- A style that owns the whole widget repeats its behaviour: Slint declares the switch's
  accessible role once in each style's file.
- Themes drift from their framework's versions: Flutter moved Material and Cupertino out into
  packages of their own, `material_ui` asking Flutter 3.47.0 at least.

What it tells M6d.1d1: themes change a component's structure only where the parts' tree is data
or code that the theme owns, under a contract of named parts that keeps behaviour and meaning on
the control (Qt, WPF); elsewhere, another look is another library of components.

## 10. The system's preferences

Read on 2026-11-09 for SlimeEngine's M6d.1d2b: which of the system's preferences each platform
gives a program, in each one's current documentation.

| Platform | Light or dark | Contrast | Less motion | Less transparency | Size of text |
|---|---|---|---|---|---|
| Linux, the desktop's portal ([`org.freedesktop.portal.Settings`](https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.Settings.html), version 2) | `color-scheme`, 0 none, 1 dark, 2 light (portal 1.12.0) | `contrast`, 0 normal, 1 higher (1.19.0, by its tags) | `reduced-motion` (1.21.0, 2026-01-21) | none | none among its keys |
| GNOME, through the portal's own namespaces | as above | `org.gnome.desktop.a11y.interface high-contrast` | `org.gnome.desktop.a11y.interface reduced-motion`; `org.gnome.desktop.interface enable-animations` | none found | `org.gnome.desktop.interface text-scaling-factor`, 0.5 to 3.0 |
| KDE, through the portal | as above | none | from `AnimationDurationFactor` at 0 | none found | its fonts in `org.kde.kdeglobals.<group>`; its DPI not found |
| Windows | through `UISettings`' colours | `SPI_GETHIGHCONTRAST` | `UISettings.AnimationsEnabled` | `UISettings.AdvancedEffectsEnabled` | `UISettings.TextScaleFactor` |
| macOS | `effectiveAppearance` | `accessibilityDisplayShouldIncreaseContrast` | `…ShouldReduceMotion` | `…ShouldReduceTransparency` | none found |
| iOS | trait collection | `isDarkerSystemColorsEnabled` | `isReduceMotionEnabled` | `isReduceTransparencyEnabled` | Dynamic Type, `preferredContentSizeCategory` |
| Android | `Configuration.uiMode` | high-contrast text (API 36) | `ValueAnimator.areAnimatorsEnabled()` (API 26) | not searched | `fontScale`, "no longer used as a direct multiplier" from API 34 |
| The web ([Media Queries 5](https://drafts.csswg.org/mediaqueries-5/)) | `prefers-color-scheme` | `prefers-contrast`, `forced-colors` | `prefers-reduced-motion` | `prefers-reduced-transparency`: Chrome 118, Firefox behind a flag, Safari none | none |
| winit 0.30.13 | `Window::theme()` and `ThemeChanged` on Windows, macOS and the web; on Wayland "only returns theme overrides", on X11 none | none | none | none | none |

The portal sends `SettingChanged` when a setting changes. winit's decorations on Wayland read
`color-scheme` through `dbus-send` for themselves, and give it to no program.

What it tells M6d.1d2b: winit gives light or dark on three platforms, and nothing else. Each
platform gives the others by its own means, with gaps: Linux's portal holds neither the size of
text nor less transparency, KDE's no contrast, macOS and the web no size of text, Safari no less
transparency; Android's less transparency was not searched.

Saving power and running on battery, read for M6d.1d2b2, are in
["More of a frame's time, of power and of clocks"](#more-of-a-frames-time-of-power-and-of-clocks).

## What stays open

- Not checked in a primary source: whether Apple's `CADisplayLink.timestamp` and
  `NSEvent.timestamp` share a clock; the clock of X11's `ust`, read only in code; how Xwayland times
  X11's input; how Windows' interrupt time converts to its performance counter; where KDE keeps its
  fonts' DPI; whether Windows and Android cap the display's rate while saving power.
- Floem's WebGPU support is "highly experimental" (`examples/webgpu/README.md`, `main`); it has no
  Android port, its maintainer citing no time for one
  ([issue #619](https://github.com/lapce/floem/issues/619), open).
- No reference publishes the latency of a style's or a layout's reload; M6d.1d measures uwui's
  against [its budget of a change seen](ROADMAP.md#budgets).
- Not checked in a primary source: Flutter 3.35's date; Compose Hot Reload's changes supported in
  its current version; how GPUI's reload handles a changed type; whether SwiftUI's previews keep
  state; how Dioxus's signals behave across a patch.
