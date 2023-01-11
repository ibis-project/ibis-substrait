{ python ? "3.10" }:
let
  pkgs = import ./nix { };
  drv = { poetry2nix, python, lib }: poetry2nix.mkPoetryApplication {
    inherit python;

    projectDir = ./.;
    src = lib.cleanSource ./.;

    checkGroups = [ "test" ];
    preferWheels = true;
    overrides = [
      (import ./poetry-overrides.nix)
      pkgs.poetry2nix.defaultPoetryOverrides
    ];

    checkPhase = ''
      runHook preCheck

      pytest

      runHook postCheck
    '';

    pythonImportsCheck = [ "ibis_substrait" ];
  };
in
pkgs.callPackage drv {
  python = pkgs."python${builtins.replaceStrings [ "." ] [ "" ] python}";
}
