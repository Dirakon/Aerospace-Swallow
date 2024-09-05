{
  description = "Terminal-swallowing script for Aerospace";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    nixpkgs,
    flake-utils,
    ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
        swallowApp = 
          pkgs.stdenv.mkDerivation {
            name = "aerospace-swallow";
            propagatedBuildInputs = [
              (pkgs.python3.withPackages (pythonPackages: []))
            ];
            dontUnpack = true;
            installPhase = "install -Dm755 ${./main.py} $out/bin/aerospace-swallow";
          };

      in {
        devShells = {
          default = pkgs.mkShell {
            buildInputs = [pkgs.python3 swallowApp];
          };
        };
        default = swallowApp;
      }
    );
}
