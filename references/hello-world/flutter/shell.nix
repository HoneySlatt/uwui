# The shell `hello-flutter` of uwui's flake: Flutter from nixpkgs, which carries the Linux desktop
# toolchain (clang, CMake, Ninja, pkg-config, GTK 3), and the libraries the program loads at run time.
pkgs: {
  packages = [ pkgs.flutter ];
}
