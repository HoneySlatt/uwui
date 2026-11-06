# egui: "Hello, World!"

The screen of reference written with [egui](https://www.egui.rs) and eframe, its framework
crate, as eframe's documentation shows.

## Documentation followed

Read on 2026-11-06:

- eframe's crate documentation (0.37.0), section "Usage, native":
  <https://docs.rs/eframe/0.37.0/eframe/>. It is the only complete, self-contained native program
  the docs give.
  The alternatives were set aside: `examples/hello_world` of egui's repository uses the workspace's
  dependencies and sets a 320 × 240 window, an image loader and a logger; `eframe_template`
  targets the web and native, with state persistence.
- egui's README, section "Layout", and the issue it links (emilk/egui#4378), for centring.

## Versions

- eframe and egui 0.37.0, with eframe's default features (wgpu 30, winit 0.30, AccessKit, system
  fonts); every crate in `Cargo.lock`.
- rustc and cargo 1.98.1, from the nixpkgs of uwui's `flake.lock`.

## Changes from the docs

- The panel's `ui.heading("Hello World!")` becomes `ui.label("Hello, World!")` and
  `ui.button("Let's Go!")`, which prints `Clicked!` when clicked.
- Centring: egui lays out in one pass and cannot centre a group vertically by itself (README,
  "Layout"). `ui.vertical_centered` centres each widget across; the group is pushed down by half
  the height it leaves, computed from egui's own text height, button padding and spacing.
- egui has no primary button style: the button is egui's default. The theme is egui's default.
- The snippet compiles with three warnings (unused `cc`, unused `frame`, unused `Result`):
  kept, to stay word for word.
- `Cargo.toml` is what `cargo new` and `cargo add eframe` write, with `edition = "2024"`.

## Build

`build.sh <out>` runs `cargo build --release`, as the docs say, with two additions that do not
change the program: `CARGO_TARGET_DIR=<out>/target`, so that the source folder stays clean, and
`--locked`, so that the build fails rather than move off `Cargo.lock`.

## What `ship/` holds

The release binary `hello-egui` alone: Cargo has no packaging step. It links only glibc and
libgcc_s. At run time it loads the libraries that `shell.nix` puts on `LD_LIBRARY_PATH`. In a
headless sway it loaded libwayland-client, libEGL, the Vulkan loader with the system's Mesa
drivers, fontconfig and FreeType (for the system fonts), and libX11. libxkbcommon was not loaded,
the headless output having no keyboard.
