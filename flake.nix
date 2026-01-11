{
  description = "Claude Arena - Python Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
      };
    in {
      devShell = pkgs.mkShell {
        packages = [
          pkgs.python311
          pkgs.uv
          pkgs.sqlite
          pkgs.git
          pkgs.just
        ];
      };
    });
}
