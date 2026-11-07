# Hello, World! in GPUI

The screen of gpui-kit's "Basic Example", written with GPUI alone.

## Documentation followed

Read 2026-11-06, at Zed's commit `145bcfc1bc3a9c6963a13c634df0fa4efc6b522e`:

- GPUI's `README.md`, "Getting Started":
  <https://github.com/zed-industries/zed/blob/145bcfc1bc3a9c6963a13c634df0fa4efc6b522e/crates/gpui/README.md>.
  It gives the dependencies `gpui` and `gpui_platform` (features `font-kit`, `wayland`, `x11`)
  and starts the program with `gpui_platform::application().run(...)`.
- Its `hello_world` example, the one GPUI's examples list says to start from:
  `crates/gpui/examples/hello_world.rs`.
- The button: the `button` helper of GPUI's `window` example, `crates/gpui/examples/window.rs`,
  copied unchanged (a `div` with an `id`, a style and `on_click`).
- The project is `cargo new`'s template (edition 2024).
- The release build is `cargo build --release` with Cargo's default release profile.

## Versions

- GPUI from Zed's Git repository at commit `145bcfc1bc3a9c6963a13c634df0fa4efc6b522e`
  (gpui 0.2.2 and gpui_platform 0.1.0 in that tree), with wgpu 30.0.0 from Git.
- `Cargo.lock` freezes every crate, the Git commits included.
- rustc 1.98.1 and cargo 1.98.0, from uwui's nixpkgs. Zed's own toolchain file names 1.98.1 too.

## Deviations

- **Git, not crates.io.** The README writes `version = "*"` for both crates.
  `gpui_platform` is not on crates.io, so Cargo cannot resolve it.
  The `gpui` on crates.io, 0.2.2 of 2025-10-22, predates `gpui_platform` and has another API.
  (gpui.rs still shows that older API, with `Application::new()`.)
  So both crates come from Zed's repository, with the README's names and features.
- **Zed's patches do not apply.** Zed's workspace patches some crates (`[patch.crates-io]`);
  Cargo ignores a dependency's patches, so those crates come from crates.io. It builds and runs.
- **Zed's release profile does not apply.** Zed builds its release with thin LTO and one codegen
  unit; a program that depends on GPUI gets Cargo's default profile.
- **Window options.** `WindowOptions::default()`, as the screen asks. `hello_world` sets
  500 × 500 bounds.
- **Root view.** From `hello_world`: `flex`, `flex_col`, `gap_3`, `justify_center`,
  `items_center` and `text_xl` are kept.
  - `size_full()` replaces `size(px(500.0))`, to fill and centre in the window.
  - The background is white, as in the `window` example's root, without a text colour.
    `hello_world`'s grey background and white text would leave the button's label, white on
    light grey, unreadable.
  - Its shadow and blue border, which framed the 500 px box, are dropped.
  - "Hello, World!" is written out, not formatted from a field.
  - The row of coloured squares is replaced by the button.
- **Fonts and the web.** `hello_world` calls `example_support::load_fonts`, which loads fonts only
  on the web and does nothing natively, and has a WebAssembly entry point. Both are left out.
- `cx.activate(true)` is kept from `hello_world`.

## Building and running

```sh
nix develop <uwui>#hello-gpui --command references/hello-world/gpui/build.sh <out>
<out>/run
```

- All of Cargo's output goes to `<out>/target`, or to `CARGO_TARGET_DIR` when set.
- Cargo clones Zed's repository into its own cache (about 0.5 GB), outside `<out>`.
- By default it runs natively on Wayland (xdg-shell), not through Xwayland.
- At run time it opens no internet socket. It tries D-Bus's session and system buses.

## What `ship/` holds

- `hello-gpui`, the release binary (about 36 MB; symbols kept, no debug information).
- Rust's packaging is the binary.
- It needs from the system: libxcb, libxkbcommon, libxkbcommon-x11, freetype and their own
  dependencies (linked); wayland-client, wayland-egl, libEGL and the Vulkan loader with a Vulkan
  driver (opened at run time); the system's fonts.

## Reload

`reload.sh <out>` prepares the reload that `scripts/reloads.sh` times, as the pull request that
added it to GPUI runs it (<https://github.com/zed-industries/zed/pull/65738>, read on 2026-11-07):
the feature `gpui/hot-reload` of the same commit, in a debug build served by
`dx serve --platform linux --hot-patch`. `dx` 0.7.10 comes from uwui's nixpkgs, in this folder's
shell. The view's `render` is patched through `subsecond`.
