# The shell `hello-compose` of uwui's flake: the JDK 21 from nixpkgs, which runs Gradle (through the
# wrapper, which fetches the Gradle version that the project pins) and packages the app with its own
# runtime image (jpackage); and the libraries that the app loads from the system at run time
# (Skiko, Compose's renderer, links libGL).
pkgs:
let
  runtimeLibraries = [ pkgs.libGL ];
in
{
  packages = [ pkgs.jdk21 ];
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath runtimeLibraries;
}
