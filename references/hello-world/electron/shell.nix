# The shell `hello-electron` of uwui's flake: Node.js and npm, which build the app, and the libraries
# that Electron loads at run time. Electron itself comes from npm: upstream's generic Linux build,
# which NixOS starts through nix-ld (`programs.nix-ld.enable`), with these libraries.
pkgs: {
  packages = [ pkgs.nodejs ];
  NIX_LD = pkgs.lib.fileContents "${pkgs.stdenv.cc}/nix-support/dynamic-linker";
  NIX_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.alsa-lib
    pkgs.at-spi2-atk
    pkgs.at-spi2-core
    pkgs.cairo
    pkgs.cups
    pkgs.dbus
    pkgs.expat
    pkgs.glib
    pkgs.gtk3
    pkgs.libgbm
    pkgs.libGL
    pkgs.libx11
    pkgs.libxcb
    pkgs.libxcomposite
    pkgs.libxdamage
    pkgs.libxext
    pkgs.libxfixes
    pkgs.libxkbcommon
    pkgs.libxrandr
    pkgs.nspr
    pkgs.nss
    pkgs.pango
    pkgs.systemd
  ];
}
