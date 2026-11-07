# The shell `hello-compose` of uwui's flake: the JDK 21 from nixpkgs, which runs Gradle (through the
# wrapper, which fetches the Gradle version that the project pins) and packages the app with its own
# runtime image (jpackage); and the libraries that the app loads from the system at run time
# (Skiko, Compose's renderer, links libGL). Compose Hot Reload runs the app on the JetBrains Runtime,
# from nixpkgs too, which COMPOSE_RELOAD_JBR names for reload.sh (in its home, beside its `release`
# file, which Compose Hot Reload reads).
pkgs:
let
  runtimeLibraries = [ pkgs.libGL ];
in
{
  packages = [ pkgs.jdk21 ];
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath runtimeLibraries;
  COMPOSE_RELOAD_JBR = "${pkgs.jetbrains.jdk}/lib/openjdk/bin/java";
}
