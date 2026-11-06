# The shell `hello-slint` of uwui's flake: the Rust toolchain that builds the program, fontconfig
# that Slint links (found through pkg-config), and the libraries that winit and Slint's default
# renderer (FemtoVG on OpenGL) load at run time.
pkgs: {
  packages = [ pkgs.cargo pkgs.rustc pkgs.pkg-config pkgs.fontconfig ];
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.libGL
    pkgs.vulkan-loader
    pkgs.fontconfig
    pkgs.libx11
    pkgs.libxcursor
    pkgs.libxi
    pkgs.libxrandr
  ];
}
