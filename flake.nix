{
  description = "uwui: its development shell";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      # Every tool that scripts/check.sh runs: lychee, which checks the links between Markdown
      # files. The toolchain arrives with uwui's code.
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pkgs.lychee ];
      };
    };
}
