# The shell `hello-tauri` of uwui's flake: Node.js and npm, which run Tauri's CLI; Rust's toolchain;
# and the GTK 3 and WebKitGTK libraries that Tauri builds against and loads at run time.
pkgs: {
  packages = [
    pkgs.nodejs
    pkgs.cargo
    pkgs.rustc
    pkgs.pkg-config
  ];
  buildInputs = [
    pkgs.webkitgtk_4_1
    pkgs.gtk3
    pkgs.libsoup_3
  ];
  # GSettings schemas (GTK's and the desktop's, which glib's setup hook gathers in
  # GSETTINGS_SCHEMAS_PATH), as nixpkgs' wrapGAppsHook gives GTK programs. Without any schema,
  # WebKitGTK draws the page at three quarters of its size, without the button's rounded corners.
  shellHook = ''
    export XDG_DATA_DIRS="$GSETTINGS_SCHEMAS_PATH''${XDG_DATA_DIRS:+:$XDG_DATA_DIRS}"
  '';
}
