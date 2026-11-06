# The shell `hello-iced` of uwui's flake: the Rust toolchain that builds the program, and the
# libraries that winit and Iced's default renderers (wgpu on Vulkan or OpenGL, tiny-skia as a
# fallback) load at run time.
pkgs: {
  packages = [ pkgs.cargo pkgs.rustc ];
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.vulkan-loader
    pkgs.libGL
    pkgs.fontconfig
    pkgs.libx11
    pkgs.libxcursor
    pkgs.libxi
    pkgs.libxrandr
  ];
}
