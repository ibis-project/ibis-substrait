let
  sources = import ./sources.nix;
in
args: import sources.nixpkgs ({
  overlays = [
    (pkgs: _: {
      poetry2nix = import sources.poetry2nix {
        inherit pkgs;
        inherit (pkgs) poetry;
      };

      substrait = pkgs.fetchFromGitHub {
        owner = "substrait-io";
        repo = "substrait";
        rev = "1a23f3bebdf6b273c2032b9906c77441a176da68";
        sha256 = "sha256:9l7hztGn7PJSs10oePvtkFuZ6EZOz4zC/GTy+zHwc4c=";
      };

      mkPoetryEnv = python: pkgs.poetry2nix.mkPoetryEnv {
        inherit python;
        projectDir = ../.;
        editablePackageSources = {
          ibis_substrait = ../ibis_substrait;
        };
        groups = [ "dev" "types" "test" ];
        preferWheels = true;
        overrides = [
          (import ../poetry-overrides.nix)
          pkgs.poetry2nix.defaultPoetryOverrides
        ];

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
} // args)
