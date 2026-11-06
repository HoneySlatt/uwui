{
  description = "uwui: its development shells";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells.${system} = {
        # Every tool that scripts/check.sh runs: lychee, which checks the links between Markdown
        # files, and Python for the scripts' tests. The toolchain arrives with uwui's code.
        default = pkgs.mkShell {
          packages = [ pkgs.lychee pkgs.python3 ];
        };
      };
    };
}
