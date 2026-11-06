{
  description = "uwui: its development shells";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
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
      devShells.${system} = helloWorlds // {
        # Every tool that scripts/check.sh runs: lychee, which checks the links between Markdown
        # files, and Python for the scripts' tests. The toolchain arrives with uwui's code.
        default = pkgs.mkShell {
          packages = [ pkgs.lychee pkgs.python3 ];
        };
      };
    };
}
