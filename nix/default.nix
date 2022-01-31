let
  sources = import ./sources.nix;
in
import sources.nixpkgs {
  overlays = [
    (pkgs: _: {
      poetry2nix = import sources.poetry2nix {
        inherit pkgs;
        inherit (pkgs) poetry;
      };

      substrait = pkgs.fetchFromGitHub {
        owner = "substrait-io";
        repo = "substrait";
        rev = "50e56f24fa9939b7f38e873570e44ceb13a97a14";
        sha256 = "sha256-19HzCXcWT1/YlStHu276moa+H4O2SxGv0gTH9UxqsI4=";
      };
      # substrait = ../../substrait;

      mkPoetryEnv = python: pkgs.poetry2nix.mkPoetryEnv {
        inherit python;
        projectDir = ../.;
        editablePackageSources = {
          ibis_substrait = ../ibis_substrait;
        };
        overrides = pkgs.poetry2nix.overrides.withDefaults (
          import ../poetry-overrides.nix {
            inherit pkgs;
            inherit (pkgs) lib stdenv;
          }
        );
      };

      ibisSubstraitDevEnv37 = pkgs.mkPoetryEnv pkgs.python37;
      ibisSubstraitDevEnv38 = pkgs.mkPoetryEnv pkgs.python38;
      ibisSubstraitDevEnv39 = pkgs.mkPoetryEnv pkgs.python39;
      ibisSubstraitDevEnv310 = pkgs.mkPoetryEnv pkgs.python310;

      prettierTOML = pkgs.writeShellScriptBin "prettier" ''
        ${pkgs.nodePackages.prettier}/bin/prettier \
        --plugin-search-dir "${pkgs.nodePackages.prettier-plugin-toml}/lib" \
        "$@"
      '';
    })
  ];
}
