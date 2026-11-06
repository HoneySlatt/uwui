# Flutter: "Hello, World!"

The reference screen in Flutter for the Linux desktop: "Hello, World!" above a primary button
"Let's Go!", centred in the window; the button prints `Clicked!` on standard output.

## Docs followed (read 2026-11-06)

- The project is `flutter create --platforms=linux hello`: Flutter's default template
  ([Create a new app](https://docs.flutter.dev/reference/create-new-app)).
- `lib/main.dart` takes the shape of Flutter's minimal app, `flutter create --empty`'s template
  (`MaterialApp` > `Scaffold` > `Center`; [Building user interfaces](https://docs.flutter.dev/ui)),
  with a `Column` holding a `Text` and a `FilledButton`.
- The release build is `flutter build linux --release`, and the bundle is what a user gets
  ([Build and release a Linux app](https://docs.flutter.dev/deployment/linux)).

## Versions

- Flutter 3.47.4, Dart 3.13.3, from nixpkgs (uwui's `flake.lock`). Material 3, Flutter's default.
- Pub packages: `pubspec.lock`, as `flutter create` resolved them (`cupertino_icons`, `flutter_lints`).
- The `linux/` runner is the template's, unchanged (GTK 3).

## Deviations from the docs

- `--platforms=linux`: the template's other platform folders are left out; this reference only
  builds for Linux.
- `lib/main.dart` replaces the template's counter demo. The primary button is `FilledButton`,
  Material 3's high-emphasis (primary) button.
- `onPressed` uses `print`, which writes to standard output in a release build too. The template's
  lints flag `print` (`avoid_print`, an info that does not stop the build).
- `test/widget_test.dart`, the template's test of the counter demo, is left out: it tests the demo
  that the screen replaces.
- `build.sh` points `HOME` and `PUB_CACHE` under `<out>` during the build. Flutter writes its
  settings and telemetry files into the home folder, and pub its cache, so the home folder stays
  clean and the sizes show. Neither changes the program.

## Build and run

```sh
nix develop <uwui>#hello-flutter --command references/hello-world/flutter/build.sh <out>
<out>/run
```

`build.sh` copies the project to `<out>/project` (Flutter writes `.dart_tool/` and `build/` into
it) and times `flutter build linux --release`, which also fetches the pub packages.

## What `ship/` holds

The release bundle: the `hello` runner, `lib/libflutter_linux_gtk.so` (the engine),
`lib/libapp.so` (the app's AOT code), and `data/`: ICU data and Flutter's assets, with the
Material icons font (tree-shaken to about 1 KB) and the Cupertino icons font (about 250 KB, whole),
which the template's `cupertino_icons` dependency adds.

From the system it loads GTK 3 and its stack (GLib, Pango, Cairo, HarfBuzz, ATK, gdk-pixbuf),
libepoxy and EGL/OpenGL ES (libglvnd and the Mesa driver). The runner's RUNPATH points to these
libraries in the Nix store. It runs natively on Wayland, through GTK, and draws with Impeller on
OpenGL ES.
