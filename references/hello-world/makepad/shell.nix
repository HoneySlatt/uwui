# The shell `hello-makepad` of uwui's flake: the Rust toolchain that builds the program, and the
# libraries that Makepad's own platform layer links or loads at run time (Wayland or X11, Vulkan,
# EGL and OpenGL, libdrm, xkbcommon for the keyboard, ALSA and PulseAudio for its audio, OpenSSL
# for its network layer).
pkgs:
let
  libraries = [
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.libGL
    pkgs.vulkan-loader
    pkgs.libx11
    pkgs.libxcursor
    pkgs.libxi
    pkgs.libxrandr
    pkgs.alsa-lib
    pkgs.libpulseaudio
    pkgs.libdrm
    pkgs.openssl
  ];
in
{
  packages = [ pkgs.cargo pkgs.rustc pkgs.pkg-config ] ++ libraries;
  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath libraries;
}
