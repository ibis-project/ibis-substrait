{
  description = "Ibis Substrait compiler.";

  inputs = {
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };

    flake-utils.url = "github:numtide/flake-utils";

    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";

    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-utils.follows = "flake-utils";
      };
    };
    pre-commit-hooks = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-utils.follows = "flake-utils";
      };
    };
  };

  outputs = { self, flake-utils, gitignore, nixpkgs, poetry2nix, ... }@inputs: {
    overlays.default = nixpkgs.lib.composeManyExtensions [
      gitignore.overlay
      poetry2nix.overlay
      (import ./nix/overlay.nix)
    ];
  } // flake-utils.lib.eachDefaultSystem (
    system:
    let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [ self.overlays.default ];
      };
      inherit (pkgs) lib;

      preCommitDeps = with pkgs; [
        actionlint
        git
        just
        nixpkgs-fmt
        pre-commit
        prettierTOML
        shellcheck
        shfmt
        statix
      ];

      mkDevShell = env:
        let
          pythonVersion = env.python.version;
          shortPythonVersion = lib.concatStrings (lib.take 2 (lib.splitVersion env.python.version));
        in
        pkgs.mkShell {

          name = "ibis-substrait-${pythonVersion}";
          nativeBuildInputs = (with pkgs; [
            cacert
            cachix
            nixpkgs-fmt
            poetry
          ])
          ++ [ pkgs."ibisSubstraitDevEnv${shortPythonVersion}" ]
          ++ preCommitDeps;

          inherit (self.checks.${system}.pre-commit-check) shellHook;
        };
    in
    rec {
      packages = {
        inherit (pkgs) ibisSubstrait39 ibisSubstrait310 ibisSubstrait311;

        default = pkgs.ibisSubstrait311;
      };

      checks = import ./nix/checks.nix inputs system;
      nixpkgs = pkgs;

      devShells = rec {
        ibisSubstrait39 = mkDevShell pkgs.ibisSubstraitDevEnv39;
        ibisSubstrait310 = mkDevShell pkgs.ibisSubstraitDevEnv310;
        ibisSubstrait311 = mkDevShell pkgs.ibisSubstraitDevEnv311;

        release = pkgs.mkShell {
          name = "release";
          nativeBuildInputs = with pkgs; [
            git
            poetry
            nodejs
            unzip
            gnugrep
          ];
        };

        default = ibisSubstrait311;
      };
    }
  );
}
