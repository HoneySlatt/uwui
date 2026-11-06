# Compose Multiplatform: "Hello, World!"

The reference screen in Compose Multiplatform for the desktop: "Hello, World!" above a primary
button "Let's Go!", centred in the window; the button prints `Clicked!` on standard output.

## Docs followed (read 2026-11-06)

- JetBrains' getting-started,
  [Create your Compose Multiplatform app](https://kotlinlang.org/docs/multiplatform/compose-multiplatform-new-project.html),
  makes the project with the Kotlin Multiplatform wizard. Its desktop-only template
  (`compose-multiplatform-desktop-template`) says it is obsolete and points to the wizard.
- The project is the wizard's output as JetBrains publishes it in
  [Kotlin/kmp-wizard](https://github.com/Kotlin/kmp-wizard), branch `all-frontends-shared-gradle`
  at `e6d2dea580964e4529413ca29ec78919b2182286` (2026-10-27), cut to its desktop target:
  `desktopApp/` (the entry point) and `shared/` (the UI, in `App.kt`).
- The release build is `./gradlew :desktopApp:createDistributable`, Compose's app image with its
  own Java runtime
  ([Native distributions](https://kotlinlang.org/docs/multiplatform/compose-native-distribution.html)).

## Versions

- Kotlin 2.4.21, Compose Multiplatform 1.12.2, Compose Material 3 1.12.0-alpha03, kotlinx-coroutines
  1.11.0, as the wizard pins them in `gradle/libs.versions.toml`.
- Gradle 9.5.1 through the wrapper (`gradle/wrapper/`, with the distribution's SHA-256). `gradlew`,
  `gradlew.bat` and `gradle-wrapper.jar` are byte for byte the wizard's.
- JDK 21.0.12.1 (OpenJDK) from nixpkgs runs Gradle and makes the runtime image.
- Gradle writes no lockfile by default; the versions above, all fixed, are the lock.

## Deviations from the docs

- The wizard's zip is not downloaded: its files are rewritten from the published branch, keeping
  only the desktop target. Android, iOS and web modules, targets, plugins and versions are removed
  from `settings.gradle.kts`, `build.gradle.kts`, `shared/build.gradle.kts`, `gradle.properties`
  and `libs.versions.toml`. A desktop-only choice in the wizard may lay the modules out otherwise.
- `gradle/gradle-daemon-jvm.properties` loses its `toolchainVendor=AZUL` line. With it, Gradle
  would download Azul's JDK 21 to run its daemon; without it, it uses nixpkgs' JDK 21.
- `App.kt` keeps the template's `MaterialTheme` and `Column` (its background and padding) and
  holds the screen: `Text` and a Material 3 `Button` (the filled, primary button), centred with
  `Arrangement.spacedBy(8.dp, Alignment.CenterVertically)`. The wizard's sample code that the
  screen no longer uses (`Greeting`, `Platform`, the logo resource) is removed.
- `main.kt` is the template's: `Window(onCloseRequest = ::exitApplication, title = ...)`.
- `build.sh` points `GRADLE_USER_HOME` and `HOME` under `<out>` during the build, so that Gradle's
  caches, the Gradle distribution and what the Gradle and Kotlin daemons write stay out of the home
  folder and the sizes show. It stops the Gradle daemon after the build. Neither changes the program.

## Build and run

```sh
nix develop <uwui>#hello-compose --command references/hello-world/compose/build.sh <out>
<out>/run
```

`build.sh` copies the project to `<out>/project` (Gradle writes `.gradle/`, `.kotlin/` and
`build/` into it) and times `./gradlew :desktopApp:createDistributable`, which also downloads
Gradle and the Maven dependencies on a clean `<out>`.

## What `ship/` holds

The app image `org.example.project/`: the launcher `bin/org.example.project`, `lib/app/` (the
app's and Compose's jars, and Skiko's native library `libskiko-linux-x64.so`) and `lib/runtime/`
(a Java 21 runtime made by jlink from nixpkgs' JDK).

From the system it loads libGL (Skiko links it; `shell.nix` puts libglvnd on `LD_LIBRARY_PATH`)
and the Mesa driver, X11 and its extensions, GTK 3 (which AWT loads), fontconfig, FreeType and
HarfBuzz; the runtime's own libraries reach the last ones through nixpkgs' JDK. The window is an
X11 window: it runs through Xwayland, not natively on Wayland.
