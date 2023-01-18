{ self, pre-commit-hooks, ... }:

system:

with self.nixpkgs.${system};
let
  protoExcludePattern = "ibis_substrait/proto/.+\\.py";
in
{
  pre-commit-check = pre-commit-hooks.lib.${system}.run {
    src = ./.;
    hooks = {
      actionlint.enable = true;
      deadnix.enable = true;
      shellcheck.enable = true;
      statix.enable = true;
      nixpkgs-fmt.enable = true;

      ruff = {
        enable = true;
        entry = "ruff --force-exclude";
        types = [ "python" ];
        excludes = [ protoExcludePattern ];
      };

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
          "((tests|docs)/.+|build)\\.py"
        ];
      };

      shfmt = {
        enable = true;
        entry = lib.mkForce "${pkgs.shfmt}/bin/shfmt -i 2 -sr -d -s -l";
      };
    };
  };
}

