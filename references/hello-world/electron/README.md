# Electron: "Hello, World!"

The screen written as Electron's own tutorial writes an app, then packaged with Electron Forge as
the tutorial packages it.

## Documentation followed

Read on 2026-11-06, the docs of Electron 45.2.3 ("latest"):

- [Building your First App](https://www.electronjs.org/docs/latest/tutorial/tutorial-first-app):
  `npm init`, `npm install electron --save-dev`, `main.js`, `index.html`.
- [Using Preload Scripts](https://www.electronjs.org/docs/latest/tutorial/tutorial-preload),
  "Communicating between processes": a preload script that calls `ipcRenderer.invoke`, a handler
  in the main process.
- [Packaging Your Application](https://www.electronjs.org/docs/latest/tutorial/tutorial-packaging):
  `npx create-electron-app@latest import`, then `npm run make`.

## Versions

- Electron 45.2.3, from npm: upstream's Linux x64 build.
- Electron Forge 8.0.1 (`@electron/packager` 20.3.0, `@electron/fuses` 2.1.3).
- Node.js 24.21.0 and npm 11.19.0, from uwui's nixpkgs.
- `package-lock.json` freezes every npm package.

## Deviations from the docs

- The page holds the screen instead of the tutorial's heading, emoji and version list: the text
  "Hello, World!" above a `<button>` "Let's Go!". `styles.css` centres both, 0.5rem apart. It is a
  file because the tutorial's Content-Security-Policy refuses inline styles.
- The button keeps the browser's default look: HTML has no "primary" button, and the tutorial has no
  stylesheet.
- "Clicked!" goes through the tutorial's IPC pattern: `preload.js` exposes `electronAPI.clicked()`,
  which invokes the channel `clicked`; its handler in `main.js` calls `console.log`. A
  `console.log` in the renderer would go to the DevTools console, not to standard output.
- `package.json` has the fields the tutorial shows for `npm init` (author "Jane Doe", MIT).
  Forge's import added its scripts, its packages, `electron-squirrel-startup` and `forge.config.js`.
- `build.sh` runs `npm ci` rather than `npm install`: it installs exactly what the lockfile freezes.
- `build.sh` runs `npm run package` rather than `npm run make`. `make` runs `package`, then wraps
  its folder in a .deb and an .rpm. Those makers need dpkg, fakeroot and rpmbuild, and rpmbuild
  fails on NixOS: it finds no RPM database in `/var/lib/rpm`. Their sizes are not measured.
- npm's cache and Electron's download (`$XDG_CACHE_HOME/electron`) are kept under `<out>`.

## What `ship/` holds

Forge's packaged app folder, `my-electron-app-linux-x64/`: Electron's binary renamed
`my-electron-app`, Chromium's resources (`.pak` files, ICU data, V8 snapshots, locales), its own
`libffmpeg.so`, SwiftShader and a Vulkan loader, `chrome-sandbox`, `chrome_crashpad_handler`, and
the app in `resources/app.asar`.

It relies on the system for GTK 3, GLib, NSS and NSPR, ATK and AT-SPI, CUPS, D-Bus, expat, GBM,
OpenGL (libglvnd), X11 and xcb, xkbcommon, Pango, Cairo, ALSA and udev.

## Running it on NixOS

Upstream's binary expects a standard Linux loader. NixOS starts it through nix-ld, which the system
must enable (`programs.nix-ld.enable`). `shell.nix` sets `NIX_LD` and `NIX_LD_LIBRARY_PATH` to the
libraries above.

Electron 45 picks Wayland when `XDG_SESSION_TYPE=wayland`, as a Wayland login session sets it.
Otherwise it uses X11, through Xwayland.

At its first start, Electron's default spell checker downloads the en-US dictionary from Google's
servers. The app writes its profile in `$XDG_CONFIG_HOME/my-electron-app`.
