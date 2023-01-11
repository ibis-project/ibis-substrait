let
  pkgs = import ./nix { };
  inherit (pkgs) lib;
  sources = import ./nix/sources.nix;
  pre-commit-hooks = import sources.pre-commit-hooks;
  protoExcludePattern = "ibis_substrait/proto/.+\\.py";
  nixSourcesPattern = "nix/sources\\.nix";
in
{
  pre-commit-check = pre-commit-hooks.run {
    src = ./.;
    hooks = {
      ruff = {
        enable = true;
        entry = "ruff --force-exclude";
        types = [ "python" ];
      };
      shellcheck.enable = true;

      black = {
        enable = true;
        excludes = [ protoExcludePattern ];
      };

      mypy = {
        enable = true;
        entry = "mypy";
        types = [ "python" ];
        excludes = [
          protoExcludePattern
          "tests/.+\\.py"
          "docs/.+\\.py"
        ];
      };

      deadnix = {
        enable = true;
        excludes = [ nixSourcesPattern ];
      };

      statix = {
        enable = true;
        entry = lib.mkForce "${pkgs.statix}/bin/statix fix";
      };

      nixpkgs-fmt = {
        enable = true;
        entry = lib.mkForce "${pkgs.nixpkgs-fmt}/bin/nixpkgs-fmt";
        excludes = [ nixSourcesPattern ];
      };

      shfmt = {
        enable = true;
        entry = lib.mkForce "${pkgs.shfmt}/bin/shfmt -i 2 -sr -d -s -l";
      };
    };
  };
}
