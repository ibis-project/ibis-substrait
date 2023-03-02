final: _:
let
  overrides = [
    (import ../poetry-overrides.nix)
    final.poetry2nix.defaultPoetryOverrides
  ];

  mkPoetryEnv = python: final.poetry2nix.mkPoetryEnv {
    inherit python overrides;
    projectDir = ../.;
    editablePackageSources = {
      ibis_substrait = ../ibis_substrait;
    };
    groups = [ "dev" "types" "test" ];
    preferWheels = true;
  };

  mkIbisSubstrait =
    python:
    let
      drv = { poetry2nix, python, lib }: poetry2nix.mkPoetryApplication {
        inherit python overrides;

        projectDir = ../.;
        src = lib.cleanSource ../.;

        checkGroups = [ "test" ];
        preferWheels = true;

        # remove the build/ folder generated by `build.py`
        preCheck = ''
          rm -r build
        '';

        checkPhase = ''
          runHook preCheck
          pytest
          runHook postCheck
        '';

        pythonImportsCheck = [ "ibis_substrait" ];
      };
    in
    final.callPackage drv { inherit python; };
in
{
  substrait = final.fetchFromGitHub {
    owner = "substrait-io";
    repo = "substrait";
    rev = "335a4dc74ccb3ef88769878d36c35e511e47ef70";
    sha256 = "q4kZBObYCgPSoxOAJAHuPrKcm0T+rWqRqUibHidtfPs=";
  };

  ibisSubstraitDevEnv38 = mkPoetryEnv final.python38;
  ibisSubstraitDevEnv39 = mkPoetryEnv final.python39;
  ibisSubstraitDevEnv310 = mkPoetryEnv final.python310;
  ibisSubstraitDevEnv311 = mkPoetryEnv final.python311;

  ibisSubstrait38 = mkIbisSubstrait final.python38;
  ibisSubstrait39 = mkIbisSubstrait final.python39;
  ibisSubstrait310 = mkIbisSubstrait final.python310;
  ibisSubstrait311 = mkIbisSubstrait final.python311;

  prettierTOML =
    let
      inherit (final) nodePackages;
    in
    final.writeShellScriptBin "prettier" ''
      ${nodePackages.prettier}/bin/prettier \
      --plugin-search-dir "${nodePackages.prettier-plugin-toml}/lib" \
      "$@"
    '';
}
