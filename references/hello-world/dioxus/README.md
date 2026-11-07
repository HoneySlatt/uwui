# Dioxus: "Hello, World!"

The screen of reference written with [Dioxus](https://dioxuslabs.com) for the desktop, from the
example of its README.

## Documentation followed

Read on 2026-11-07:

- Dioxus's README at 0.7.10, its first example, a counter in `rsx!`:
  <https://github.com/DioxusLabs/dioxus/blob/v0.7.10/README.md>.
- "Getting started", for the desktop's system libraries on Linux (WebKitGTK 4.1, libxdo):
  <https://dioxuslabs.com/learn/0.7/getting_started/>.
- "Hot-Reloading", for what `dx serve` reloads without compiling and what `--hotpatch` patches:
  <https://dioxuslabs.com/learn/0.7/essentials/ui/hotreload/>.

## Versions

- dioxus 0.7.10 with its feature `desktop` (wry on WebKitGTK 4.1); every crate in `Cargo.lock`.
- `dx` 0.7.10, rustc and cargo 1.98.1, from the nixpkgs of uwui's `flake.lock`.

## Changes from the docs

- The counter becomes the screen: no state, the text "Hello, World!" above a button "Let's Go!",
  whose `onclick` prints `Clicked!`.
- Dioxus draws HTML: a `div` with an inline style lays the two out in a column, centred in the
  window, 12 pixels apart. The button keeps WebKitGTK's default look; nothing else is styled.
- The README installs `dx` by a script and makes the project with `dx new`, which fetches a
  template: here `dx` comes from nixpkgs, and `Cargo.toml` is what `cargo new` and
  `cargo add dioxus --features desktop` write, with `edition = "2024"`.

## Build

`build.sh <out>` copies the project to `<out>/project`, since `dx` writes its `target/` there, and
runs `dx build --release --platform desktop --locked`.

## What `ship/` holds

The folder that `dx` assembles for Linux: the release binary `hello-dioxus`, about 7 MB, and an
empty `assets/`. It draws through WebKitGTK 4.1 and GTK 3, which it loads from the system.

## Reload

`reload.sh <out>` prepares the reloads that `scripts/reloads.sh` times: a copy in `<out>/project`,
built once in debug, and `<out>/reload`, which runs `dx serve --platform desktop --hotpatch`.

- `dx serve` reloads a change of `rsx!`'s literals without compiling: the button's label is timed
  so.
- A change of a function's body needs a patch (`--hotpatch`, by `subsecond`). In the copy, the
  text moves into a function `greeting()`, called from `rsx!`, whose body `dx` patches: timed so.
  A string literal in braces, `{"Hello, World!"}`, would not do: RSX's reload takes it as a
  literal, without a patch.
- `dx` shows a notice at the window's top right after each reload: `reload.steps` compares only
  the region of the text and the button.

## License

Dioxus and its README's example are MIT OR Apache-2.0.
