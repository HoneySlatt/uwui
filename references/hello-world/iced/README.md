# Iced: "Hello, World!"

The screen of reference written with [Iced](https://iced.rs), as its README shows.

## Documentation followed

Read on 2026-11-06:

- Iced's README at tag 0.14.0, section "Overview":
  <https://github.com/iced-rs/iced/blob/0.14.0/README.md#overview>.
  Its counter is the first route Iced shows; the book follows the same shape.
- The rustdoc of `iced::widget::center` (0.14.0), for centring:
  <https://docs.rs/iced/0.14.0/iced/widget/fn.center.html>.

## Versions

- iced 0.14.0, with its default features (wgpu 27, tiny-skia, winit 0.30); every crate in
  `Cargo.lock`.
- rustc and cargo 1.98.1, from the nixpkgs of uwui's `flake.lock`.

## Changes from the docs

- The counter becomes the screen: no state, one message `Clicked`, and `update` prints
  `Clicked!`.
- `view` puts the column in `center(...)` and aligns it with `.align_x(Center)`, so that the text
  and the button sit in the middle of the window. It returns that `Container` instead of a
  `Column`.
- The column keeps the README's default spacing (none); nothing else is styled. The button's
  default style is Iced's `button::primary`; the theme is Iced's default.
- `Cargo.toml` is what `cargo new` and `cargo add iced` write, with `edition = "2024"`.

## Build

`build.sh <out>` runs `cargo build --release`, as the docs say, with two additions that do not
change the program: `CARGO_TARGET_DIR=<out>/target`, so that the source folder stays clean, and
`--locked`, so that the build fails rather than move off `Cargo.lock`.

## What `ship/` holds

The release binary `hello-iced` alone: Cargo has no packaging step. It links only glibc and
libgcc_s. At run time it loads the libraries that `shell.nix` puts on `LD_LIBRARY_PATH`. In a
headless sway it loaded libwayland-client, libwayland-egl, libEGL, the Vulkan loader with the
system's Mesa drivers, and libX11 and libxcb (linked by the graphics stack). libxkbcommon was
not loaded, the headless output having no keyboard; nor was fontconfig.

## Reload

`reload.sh <out>` prepares the reload that `scripts/reloads.sh` times, read on 2026-11-07 in
Iced's pull request that added it (<https://github.com/iced-rs/iced/pull/3000>): Iced's feature
`hot` and `cargo hot` 0.1.1, which `reload.sh` installs by cargo into `<out>/tools`. A copy in
`<out>/project` is built once in debug, and `<out>/reload` runs `cargo hot --features iced/hot`.
`view` is patched through `subsecond`. How each save is written, and why, is in
[`docs/measurements.md`](../../../docs/measurements.md#the-rivals-reloads-2026-11-07).
