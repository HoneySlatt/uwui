# The shell `hello-qt-quick` of uwui's flake: CMake, Ninja and Qt 6 from nixpkgs. The program links
# to this Qt; the variables below make it load this Qt's plugins and QML modules, and Qt's own
# default look, whatever the user's session sets (other Qt versions' paths, a platform theme).
pkgs:
let
  qt = pkgs.qt6;
in
{
  packages = [
    pkgs.cmake
    pkgs.ninja
    qt.qtbase
    qt.qtdeclarative
  ];
  QT_PLUGIN_PATH = "${qt.qtbase}/${qt.qtbase.qtPluginPrefix}";
  QML_IMPORT_PATH = "${qt.qtdeclarative}/${qt.qtbase.qtQmlPrefix}";
  QML2_IMPORT_PATH = "${qt.qtdeclarative}/${qt.qtbase.qtQmlPrefix}";
  QT_QPA_PLATFORMTHEME = "";
  QT_STYLE_OVERRIDE = "";
}
