# The shell `hello-<folder>` of uwui's flake: Rust's toolchain, the libraries that GPUI's crates
# build against (found through pkg-config), and those that GPUI opens at run time (wayland, EGL,
# Vulkan).
pkgs:
let
  libraries = [
    pkgs.fontconfig
    pkgs.freetype
    pkgs.libxcb
    pkgs.libxkbcommon
    pkgs.wayland
    pkgs.libGL
    pkgs.vulkan-loader
  ];
in
{
  packages = [
    pkgs.rustc
    pkgs.cargo
    pkgs.pkg-config
  ] ++ libraries;
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath libraries;
}
