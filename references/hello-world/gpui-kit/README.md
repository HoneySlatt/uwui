# Hello, World! in gpui-kit

gpui-kit's "Basic Example", word for word.

## Documentation followed

- gpui-kit's `README.md` at revision `b2aaa3e5f9a387dea74981586bfca33e7e08420d`, read 2026-11-06:
  <https://github.com/longbridge/gpui-kit/blob/b2aaa3e5f9a387dea74981586bfca33e7e08420d/README.md>.
  - "Usage": the dependency, `gpui-kit = "0.7"`, default features.
  - "Basic Example": `src/main.rs`, copied unchanged.
- The project is `cargo new`'s template (edition 2024) with that dependency.
- The release build is `cargo build --release` with Cargo's default release profile.

## Versions

- gpui-kit 0.7.3, the newest 0.7 on 2026-11-06 (0.9.0 is the newest overall).
- It pins GPUI as the `gpui-pre-*` crates 0.3.9, with wgpu 29.0.4.
- `Cargo.lock` freezes every crate.
- rustc 1.98.1 and cargo 1.98.0, from uwui's nixpkgs.

## Deviations

None. The README's code builds as it stands: no edition, feature or extra code was needed.

## Building and running

```sh
nix develop <uwui>#hello-gpui-kit --command references/hello-world/gpui-kit/build.sh <out>
<out>/run
```

- All of Cargo's output goes to `<out>/target`, or to `CARGO_TARGET_DIR` when set.
- By default it runs natively on Wayland (xdg-shell), not through Xwayland.
- At run time it opens no internet socket. It tries D-Bus's session and system buses.

## What `ship/` holds

- `hello-gpui-kit`, the release binary (about 49 MB; symbols kept, no debug information).
- Rust's packaging is the binary.
- gpui-kit's default features embed its icons in the binary.
- It needs from the system: libxcb, libxkbcommon, libxkbcommon-x11, freetype and their own
  dependencies (linked); wayland-client, wayland-egl, libEGL and the Vulkan loader with a Vulkan
  driver (opened at run time); the system's fonts.
