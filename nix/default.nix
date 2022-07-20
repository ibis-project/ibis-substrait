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
        rev = "b8fb06a52397463bfe9cffc2c89fe71eba56b2ca";
        sha256 = "sha256:1irbmicarxiv8dmq6pgnwb94mwbj6x92r2fm0b14xc0hp73d4j6n";
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
