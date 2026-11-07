# Makepad: "Hello, World!"

The screen of reference written with [Makepad](https://github.com/makepad/makepad), from its
`counter` example, at a commit of its `main` branch.

## Documentation followed

Read on 2026-11-07, at Makepad's commit `506ec05105b9adb08d1d21f9879df181b5244ea7` (2026-10-31),
the head of `main`:

- Makepad's README, "Examples", which runs them with `cargo run -p <example>`:
  <https://github.com/makepad/makepad/blob/506ec05105b9adb08d1d21f9879df181b5244ea7/README.md>.
- The `counter` example, the smallest with a label and a button:
  `examples/counter/src/main.rs`.
- `platform/src/live_reload.rs`, for the reload: a program started with `--hot` watches the files
  of its `script_mod!` blocks and evaluates a changed block again.

## Versions

- makepad-widgets 2.0.0 from Makepad's Git repository at that commit, without its default
  features, as the examples take it; every crate in `Cargo.lock`, the commit included. The
  last makepad-widgets on crates.io, 1.0.0 of May 2025, has another API (`live_design!`) and no
  `--hot`.
- rustc and cargo 1.98.1, from the nixpkgs of uwui's `flake.lock`.

## Changes from the example

- The counter becomes the screen: a `Label` "Hello, World!" above a `Button` "Let's Go!", which
  prints `Clicked!` when clicked; the counter's state, its `on_render` and its icon are left out.
- The window keeps Makepad's default size, without the example's `inner_size`, and the safe
  area's padding, which only mobile systems need, is left out. The column keeps the example's
  `align: Center` and spacing of 12.
- The example's feature `tweaker`, Makepad's design overlay, is left out.
- A crate of its own, outside Makepad's workspace: `makepad-widgets` comes from Git, not by path.

## Build

`build.sh <out>` runs `cargo build --release`, as the README runs the examples, with
`CARGO_TARGET_DIR=<out>/target` and `--locked`, which change nothing in the program. Cargo clones
Makepad's repository into its own cache, outside `<out>`.

## What `ship/` holds

The release binary `hello-makepad` alone, about 32 MB: Makepad's desktop builds have no packaging
step. It draws with its own renderer, on Vulkan or, without a Vulkan loader, on OpenGL ES.

## Reload

`reload.sh <out>` prepares the reload that `scripts/reloads.sh` times: a copy in `<out>/project`,
built once in debug, and `<out>/reload`, which runs it with `cargo run -- --hot`. The text is in a
`script_mod!` block, Makepad's own language, evaluated again without compiling: it is not a Rust
function's body.

## License

The `counter` example's crate is MIT OR Apache-2.0, as is makepad-widgets; the repository's
`LICENSE` file gives MIT.
