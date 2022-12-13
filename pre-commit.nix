let
  inherit (import ./nix { }) lib;
  sources = import ./nix/sources.nix;
  pre-commit-hooks = import sources.pre-commit-hooks;
  protoExcludePattern = "ibis_substrait/proto/.+\\.py";
  nixSourcesPattern = "nix/sources\\.nix";
in
{
  pre-commit-check = pre-commit-hooks.run {
    src = ./.;
    hooks = {
      black = {
        enable = true;
        entry = lib.mkForce "black --check";
        types = [ "python" ];
        excludes = [ protoExcludePattern ];
      };

      flake8 = {
        enable = true;
        language = "python";
        entry = lib.mkForce "flake8";
        types = [ "python" ];
        excludes = [ protoExcludePattern ];
      };

      isort = {
        enable = true;
        language = "python";
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

      nix-linter = {
        enable = true;
        entry = lib.mkForce "nix-linter";
        excludes = [ nixSourcesPattern ];
      };

      nixpkgs-fmt = {
        enable = true;
        entry = lib.mkForce "nixpkgs-fmt --check";
        excludes = [ nixSourcesPattern ];
      };

      pyupgrade = {
        enable = true;
        entry = "pyupgrade --py38-plus";
        types = [ "python" ];
        excludes = [ protoExcludePattern ];
      };

      shellcheck = {
        enable = true;
        entry = lib.mkForce "shellcheck";
        files = "\\.sh$";
        types_or = lib.mkForce [ ];
      };

      shfmt = {
        enable = true;
        entry = lib.mkForce "shfmt -i 2 -sr -d -s -l";
        files = "\\.sh$";
      };
    };
  };
}
