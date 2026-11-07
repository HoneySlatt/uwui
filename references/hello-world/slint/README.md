# Slint: "Hello, World!"

The screen of reference written with [Slint](https://slint.dev), from its official Rust template.

## Documentation followed

Read on 2026-11-06:

- Slint's "Getting started", Rust tab:
  <https://docs.slint.dev/latest/docs/slint/guide/getting-started/>. Without VS Code, it says to
  take the Rust template and run it with Cargo.
- The template, `slint-rust-template`, at commit `b93312d04648f2cdc6f14b8b8839d68a8e1272d2`:
  <https://github.com/slint-ui/slint-rust-template>.
- The `Button` of `std-widgets.slint`, for `primary`:
  <https://docs.slint.dev/latest/docs/slint/reference/std-widgets/basic-widgets/button/>.

## Versions

- slint and slint-build 1.18.1, with their default features (winit 0.30, FemtoVG on OpenGL); every
  crate in `Cargo.lock`. The widget style is Fluent, the default when Slint is built without its
  Qt backend, which its default features leave out.
- rustc and cargo 1.98.1, from the nixpkgs of uwui's `flake.lock`.

## Changes from the template

The template's files are copied as they are at that commit: `Cargo.toml` (with its own release
profile, `lto = true` and `codegen-units = 1`), `build.rs`, `.cargo/config.toml` (Windows only)
and `.gitignore`. They were written from the repository's sources rather than its ZIP archive.
The package keeps the template's name, `slint-rust-template`, which names the binary.

- `ui/app-window.slint`: the counter becomes a `Text` "Hello, World!" above a `Button`
  "Let's Go!" with `primary: true`, the docs' primary accent colour. The template's
  `VerticalBox` gets `alignment: center` and the text `horizontal-alignment: center`. A
  `VerticalBox` stretches its children across, so the button sits in a `HorizontalLayout` with
  `alignment: center`.
- `src/main.rs`: the callback `clicked` prints `Clicked!`.

## Build

`build.sh <out>` runs `cargo build --release`, as the docs say, with two additions that do not
change the program: `CARGO_TARGET_DIR=<out>/target`, so that the source folder stays clean, and
`--locked`, so that the build fails rather than move off `Cargo.lock`. The build needs pkg-config
and fontconfig, which `shell.nix` lists: the crate `yeslogic-fontconfig-sys` links fontconfig.

## What `ship/` holds

The release binary `slint-rust-template` alone: Cargo has no packaging step. It links glibc,
libgcc_s and fontconfig, with FreeType. At run time it loads the libraries that `shell.nix` puts
on `LD_LIBRARY_PATH`. In a headless sway it loaded libwayland-client, libwayland-egl, libEGL with
the system's Mesa drivers, and libX11. It also tries the D-Bus session bus for the desktop's
settings, and prints an error when there is none.

## Reload

`reload.sh <out>` prepares the live preview that `scripts/reloads.sh` times, as Slint's
documentation runs it ("Live Preview in Your Application", read on 2026-11-07,
<https://github.com/slint-ui/slint/blob/master/docs/astro/src/content/docs/guide/tooling/live-preview.mdx>):
a debug build with the feature `slint/live-preview` and `SLINT_LIVE_PREVIEW=1`, run by `cargo run`.
The interpreter reads `ui/app-window.slint` again; no Rust is compiled. How each save is written,
and why, is in [`docs/measurements.md`](../../../docs/measurements.md#the-rivals-reloads-2026-11-07).
