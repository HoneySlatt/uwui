{
  description = "uwui: its development shells";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  # The applications of the market that scripts/market.sh measures, at the versions their figures
  # name: one revision of nixpkgs for all, the owner's system's when they were measured, moved only
  # to measure them again.
  inputs.market.url = "github:NixOS/nixpkgs/31ecbaca1bdefa45dffc409f0250bd8039ea0010";

  outputs = { nixpkgs, market, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      # Spotify, Cider and Steam are not free software.
      marketPkgs = import market { inherit system; config.allowUnfree = true; };
      references = ./references/hello-world;
      # The tools of scripts/measure.py: a headless sway, grim for its images, Python.
      measuring = [ pkgs.sway pkgs.grim pkgs.python3 ];
      # One shell for each "Hello, World!" of references/hello-world, named `hello-<folder>`: the
      # toolchain that builds it and the libraries that it loads, which its `shell.nix` lists, and
      # the tools that measure it.
      helloWorlds = builtins.listToAttrs (map (name: {
        name = "hello-${name}";
        value = let shell = import (references + "/${name}/shell.nix") pkgs;
        in pkgs.mkShell (shell // { packages = (shell.packages or [ ]) ++ measuring; });
      }) (builtins.attrNames (pkgs.lib.filterAttrs (_: type: type == "directory")
        (builtins.readDir references))));
    in {
      # scripts/market.sh builds each rival from here: `nix build .#market.<package>`.
      legacyPackages.${system}.market = marketPkgs;

      devShells.${system} = helloWorlds // {
        # Every tool that scripts/check.sh runs: lychee, which checks the links between Markdown
        # files, and Python for the scripts' tests. The toolchain arrives with uwui's code.
        default = pkgs.mkShell {
          packages = [ pkgs.lychee pkgs.python3 ];
        };
      };
    };
}
