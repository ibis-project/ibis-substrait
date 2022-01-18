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
        rev = "e1b4c04a1b518912f4c4065b16a1b2c0ac8e14cf";
        sha256 = "sha256-56FSjDngsROSHLjMv+OYAIYqphEu3GzgIMHbgh/ZQw0=";
      };

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
