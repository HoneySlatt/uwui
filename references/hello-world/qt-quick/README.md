# Qt Quick: "Hello, World!"

The reference screen in Qt Quick: "Hello, World!" above a primary button "Let's Go!", centred in
the window; the button logs `Clicked!` through `console.log`.

## Docs followed (read 2026-11-06)

- `CMakeLists.txt` and `main.cpp` are Qt Creator's "Qt Quick Application" template with its
  default choices (minimum Qt 6.10, Figma content support on, no virtual keyboard), from
  `share/qtcreator/templates/wizards/projects/qtquickapplication` in Qt Creator's repository, and
  `.gitignore` is the one that wizard writes.
- `Main.qml` is the `Window` of [First steps with QML](https://doc.qt.io/qt-6.11/qmlfirststeps.html),
  with the template's title, holding a `Column` with a `Text` and a `Button` from `QtQuick.Controls`.
- The build is CMake's release build as Qt Creator configures it: the Ninja generator and
  `CMAKE_BUILD_TYPE=Release`. Qt's CMake docs give no command line of their own.

## Versions

- Qt 6.11.2 (qtbase, qtdeclarative) from nixpkgs (uwui's `flake.lock`); CMake 4.4.3, Ninja 1.13.2,
  GCC 16.2.
- The Qt version is the lock: the program links to the shell's Qt.

## Deviations from the docs

- Qt Creator's current template writes an `ApplicationWindow` with `QtQuick.Controls.Basic`, a
  two-pane layout and a light/dark toggle. `Main.qml` uses the plain `Window` of Qt's first steps
  instead, so that the controls take their default style (Fusion on Linux), with only the screen
  inside.
- `highlighted: true` gives the button its primary look in the default style.
- The template's `importedcontent/README.md` (a note for Figma exports) is left out; the
  `CMakeLists.txt` block that reads that folder is kept, and does nothing without it.
- `shell.nix` sets `QT_PLUGIN_PATH`, `QML_IMPORT_PATH` and `QML2_IMPORT_PATH` to the shell's Qt and
  empties `QT_QPA_PLATFORMTHEME` and `QT_STYLE_OVERRIDE`, so that the program loads this Qt's
  plugins and shows Qt's default look, whatever the user's session sets. The program is unchanged.

## Build and run

```sh
nix develop <uwui>#hello-qt-quick --command references/hello-world/qt-quick/build.sh <out>
<out>/run
```

`build.sh` configures and builds in `<out>/build` and times both steps.

## Where `Clicked!` goes

`console.log` goes through Qt's logging, as `qml: Clicked!`. Qt from nixpkgs is built with journald
support, so it writes to standard error only when standard error is a terminal; otherwise the
message goes to the systemd journal. `QT_FORCE_STDERR_LOGGING=1` sends it to standard error always.

## What `ship/` holds

The release binary `apphello` alone (the QML is compiled into it). It loads Qt from the system:
Qt Core, Gui, DBus, Network, OpenGL, Wayland Client (qtbase), Qml, QmlMeta, QmlModels,
QmlWorkerScript, Quick, Quick Controls 2 with its Basic and Fusion styles, Quick Templates 2
(qtdeclarative), and the plugins for Wayland (platform, xdg-shell, EGL). These 25 files weigh
about 64 MiB; Qt Core also loads ICU, and the rest of the stack (EGL, Mesa, fontconfig, FreeType,
HarfBuzz, xkbcommon) comes from the system too. It runs natively on Wayland.
