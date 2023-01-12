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

      genProtos = pkgs.writeShellApplication {
        name = "gen-protos";
        runtimeInputs = [ pkgs.buf ];
        text = ''
          proto_dir=./proto
          mkdir -p "$proto_dir"
          chmod u+rwx "$proto_dir"
          rm -r "$proto_dir"
          cp -fr ${pkgs.substrait}/proto "$proto_dir"
          find "$proto_dir" -type d -exec chmod u+rwx {} +
          find "$proto_dir" -type f -exec chmod u+rw {} +
          rm -rf ./ibis_substrait/proto
          python proto_prefix.py "$proto_dir"/tmp substrait.ibis "$proto_dir"/substrait
          mv "$proto_dir"/substrait substrait.bak
          mv "$proto_dir"/tmp/substrait "$proto_dir"
          buf generate
          protol --in-place --create-package --python-out "./ibis_substrait/proto" buf
          rm -rf "$proto_dir"/tmp
          rm -rf "$proto_dir"/substrait
          mv substrait.bak "$proto_dir"/substrait
        '';
      };

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
            buf
            cacert
            cachix
            genProtos
            jq
            nixpkgs-fmt
            poetry
            protobuf3_20
            sd
            yj
          ])
          ++ [ pkgs."ibisSubstraitDevEnv${shortPythonVersion}" ]
          ++ preCommitDeps;

          inherit (self.checks.${system}.pre-commit-check) shellHook;
        };
    in
    rec {
      packages = {
        inherit (pkgs) ibisSubstrait38 ibisSubstrait39 ibisSubstrait310;

        default = pkgs.ibisSubstrait310;
      };

      checks = import ./nix/checks.nix inputs system;
      nixpkgs = pkgs;

      devShells = rec {
        ibisSubstrait38 = mkDevShell pkgs.ibisSubstraitDevEnv38;
        ibisSubstrait39 = mkDevShell pkgs.ibisSubstraitDevEnv39;
        ibisSubstrait310 = mkDevShell pkgs.ibisSubstraitDevEnv310;

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

        default = ibisSubstrait310;
      };
    }
  );
}
