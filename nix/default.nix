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
        rev = "4e70145508133988967db1f3dc96a45ce555867f";
        sha256 = "sha256:1c4d6asdghbp00qr8zrirxqwqhnhkjk8qy1phy1cmq2fvyzggqp3";
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
