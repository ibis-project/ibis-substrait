{ python ? "3.10" }:
let
  pkgs = import ./nix { };
  drv =
    { poetry2nix
    , python
    , lib
    }: poetry2nix.mkPoetryApplication {
      inherit python;

      projectDir = ./.;
      src = lib.cleanSource ./.;

      overrides = pkgs.poetry2nix.overrides.withDefaults (
        import ./poetry-overrides.nix {
          inherit pkgs;
          inherit (pkgs) lib stdenv;
        }
      );

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
