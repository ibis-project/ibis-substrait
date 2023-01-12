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
    rev = "1a23f3bebdf6b273c2032b9906c77441a176da68";
    sha256 = "9l7hztGn7PJSs10oePvtkFuZ6EZOz4zC/GTy+zHwc4c=";
  };

  ibisSubstraitDevEnv38 = mkPoetryEnv final.python38;
  ibisSubstraitDevEnv39 = mkPoetryEnv final.python39;
  ibisSubstraitDevEnv310 = mkPoetryEnv final.python310;

  ibisSubstrait38 = mkIbisSubstrait final.python38;
  ibisSubstrait39 = mkIbisSubstrait final.python39;
  ibisSubstrait310 = mkIbisSubstrait final.python310;

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
