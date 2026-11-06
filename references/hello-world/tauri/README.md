# Tauri: "Hello, World!"

The screen written from Tauri 2's own project template, built for release as its docs build it.

## Documentation followed

Read on 2026-11-06 (pages last updated on 2026-11-05):

- [Create a Project](https://v2.tauri.app/start/create-project/): `create-tauri-app` with
  `npm create tauri-app@latest`. Answers: TypeScript / JavaScript, npm, Vanilla, JavaScript.
- [Prerequisites](https://v2.tauri.app/start/prerequisites/): WebKitGTK 4.1 and its companions,
  here from nixpkgs.
- [Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/): the template's
  command, which the button calls.
- [Distribute](https://v2.tauri.app/distribute/): `npm run tauri build`.

## Versions

- Tauri CLI 2.12.4 (`@tauri-apps/cli`, from npm, as the npm route uses; nixpkgs' `cargo-tauri` is
  not used), `create-tauri-app` 4.7.5.
- Crates: `tauri` 2.12.5, `wry` 0.57.1, `tao` 0.37.2, `webkit2gtk` 2.0.2.
- Rust 1.98.1, Node.js 24.21.0 and npm 11.19.0, WebKitGTK 2.54.1 (ABI 4.1), GTK 3.24.52 and
  libsoup 3.6.6, from uwui's nixpkgs.
- `package-lock.json` and `src-tauri/Cargo.lock` freeze every package.

## Deviations from the docs

- The docs show a shell script first (`sh <(curl https://create.tauri.app/sh)`). It downloads and
  runs a program from the web outside a package manager, so the npm route was taken.
- The docs recommend pnpm and TypeScript. npm comes with nixpkgs' Node.js. JavaScript needs no
  build step for a vanilla page.
- `identifier` is `com.tauri-app.app`, the value the docs show: the template derives it from the
  local user's name.
- The template's logos, its README and its `.vscode/` are removed.
- The page holds the screen instead of the template's greeting form: "Hello, World!" above a button
  "Let's Go!". `main.js` invokes the command `clicked` instead of `greet`; in `lib.rs`, `clicked`
  prints "Clicked!" with `println!`.
- `styles.css` keeps the template's page and button rules, and drops those of the removed elements.
  Its container fills the window (`height: 100%`) and centres the text and the button, 0.5rem apart.
- `build.sh` runs `npm ci` rather than `npm install`: it installs exactly what the lockfile freezes.
  It passes `--locked` to Cargo, which refuses to change `Cargo.lock`.
- `build.sh` builds the .deb and .rpm bundles but not the AppImage
  (`npm run tauri build -- --bundles deb,rpm`). For it, Tauri downloads `linuxdeploy` and its
  plugins from GitHub at build time, and `linuxdeploy` fails to run on NixOS.
- The copy built under `<out>` gets an empty `[workspace]` table in `Cargo.toml`: `<out>` may lie
  inside another Cargo workspace, which Cargo would otherwise attach the app to.
- npm's cache and Cargo's target folder are kept under `<out>`.
- The template's release profile (LTO, one codegen unit, `panic = "abort"`, stripped) is its own,
  kept as is.

## What `ship/` holds

What the .deb package installs: `usr/bin/tauri-app`, the release binary with the page embedded;
`usr/share/applications/tauri-app.desktop`; and three icons in `usr/share/icons/hicolor/`.

It relies on the system for WebKitGTK 4.1, GTK 3, libsoup 3 and GLib, and for GSettings schemas.
Built in uwui's shell, the binary finds these libraries in the Nix store.

## Running it on NixOS

`shell.nix` puts GTK's and the desktop's GSettings schemas in `XDG_DATA_DIRS`, as nixpkgs'
`wrapGAppsHook` does for GTK programs. Without any schema, WebKitGTK draws the page at three
quarters of its size, without the button's rounded corners.

GTK picks Wayland whenever `WAYLAND_DISPLAY` is set.
