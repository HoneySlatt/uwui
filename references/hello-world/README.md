# "Hello, World!" in twelve frameworks

The screen of reference "Hello, World!" ([`docs/ROADMAP.md`](../../docs/ROADMAP.md#screens-of-reference)),
written in each framework as its own documentation shows, and frozen: each folder holds its
sources and every lock of its versions. They are measured by
[`scripts/hello-world.sh`](../../scripts/hello-world.sh), and their reloads timed by
[`scripts/reloads.sh`](../../scripts/reloads.sh); their figures are in
[`docs/measurements.md`](../../docs/measurements.md). Dioxus's and Makepad's, added for the
reloads, have no figures of their start yet. CI does not build them.

Each folder's `README.md` names the pages followed, the versions, every change from the docs and
why, and what its program needs from the system. Each holds:

- `shell.nix`: the toolchain and libraries that `flake.nix` makes the shell `hello-<folder>`;
- `build.sh <out>`: the release build into `<out>`, which writes `<out>/run`, a script that
  becomes the program, and `<out>/ship/`, what the framework's packaging gives a user.

A folder whose framework reloads a change while its program runs also holds:

- `reload.sh <out>`: a copy of the project in `<out>/project`, built once in debug, as an author
  runs it while writing, and `<out>/reload`, a script that starts the framework's tool of reload
  and becomes it;
- `reload.steps`: the steps of `scripts/measure.py` that change a file of the copy and time the
  first frame that shows it.

| Folder | Framework | Started from | That source's license |
|---|---|---|---|
| `gpui-kit` | gpui-kit 0.7.3 | its README's "Basic Example", word for word | Apache-2.0 |
| `gpui` | GPUI, Zed at `145bcfc` | GPUI's README and examples | Apache-2.0 |
| `flutter` | Flutter 3.47.4 | `flutter create` | BSD-3-Clause |
| `compose` | Compose Multiplatform 1.12.2 | the Kotlin Multiplatform wizard's output | Apache-2.0 |
| `electron` | Electron 45.2.3 | Electron's tutorial | MIT |
| `tauri` | Tauri 2.12.5 | `create-tauri-app`, Vanilla | MIT OR Apache-2.0 |
| `qt-quick` | Qt 6.11.2 | Qt Creator's "Qt Quick Application" | Qt Creator's output, which The Qt Company GPL Exception 1.0 leaves to the user's terms |
| `slint` | Slint 1.18.1 | `slint-rust-template` | MIT |
| `iced` | Iced 0.14.0 | its README's example | MIT |
| `egui` | eframe 0.37.0 | eframe's documentation | MIT OR Apache-2.0 |
| `dioxus` | Dioxus 0.7.10 | its README's example | MIT OR Apache-2.0 |
| `makepad` | Makepad at `506ec05` | its `counter` example | MIT OR Apache-2.0 |

Updated when a reference is added, or frozen again at newer versions.
