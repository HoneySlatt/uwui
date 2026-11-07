# The shell `hello-dioxus` of uwui's flake: Rust's toolchain and Dioxus's CLI, `dx`, which builds
# and serves the program; and the GTK 3 and WebKitGTK libraries that Dioxus's desktop renderer
# (wry) builds against and loads at run time, with libxdo, which its global shortcuts link.
pkgs: {
  packages = [
    pkgs.cargo
    pkgs.rustc
    pkgs.pkg-config
    pkgs.dioxus-cli
  ];
  buildInputs = [
    pkgs.webkitgtk_4_1
    pkgs.gtk3
    pkgs.libsoup_3
    pkgs.xdotool
    pkgs.openssl
  ];
  # GSettings schemas, as Tauri's shell gives them: WebKitGTK draws the page wrong without any.
  shellHook = ''
    export XDG_DATA_DIRS="$GSETTINGS_SCHEMAS_PATH''${XDG_DATA_DIRS:+:$XDG_DATA_DIRS}"
  '';
}
