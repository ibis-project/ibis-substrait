{ python ? "3.10" }:
let
  pkgs = import ./nix;
  inherit (pkgs) lib;

  ibisSubstraitDevEnv = pkgs."ibisSubstraitDevEnv${pythonShortVersion}";

  devDeps = with pkgs; [
    buf
    cacert
    cachix
    git
    jq
    niv
    nix-linter
    nixpkgs-fmt
    prettierTOML
    protobuf
    sd
    shellcheck
    shfmt
    yj
    ibisSubstraitDevEnv.pkgs.poetry
  ];

  pythonShortVersion = builtins.replaceStrings [ "." ] [ "" ] python;
  genProtos = pkgs.writeShellApplication {
    name = "gen-protos";
    runtimeInputs = with pkgs; [ buf ];
    text = ''
      proto_dir=./proto
      mkdir -p "$proto_dir"
      chmod u+rwx "$proto_dir"
      rm -r "$proto_dir"
      cp -fr ${pkgs.substrait}/proto "$proto_dir"
      find "$proto_dir" -type d -exec chmod u+rwx {} +
      find "$proto_dir" -type f -exec chmod u+rw {} +
      rm -rf ./ibis_substrait/proto
      buf generate
      protol --in-place --create-package --python-out "./ibis_substrait/proto" buf
    '';
  };
in
pkgs.mkShell {
  name = "ibis-substrait-${pythonShortVersion}";

  shellHook = ''
    ${(import ./pre-commit.nix).pre-commit-check.shellHook}
  '';

  buildInputs = devDeps ++ [ ibisSubstraitDevEnv genProtos ];

  PYTHONHASHSEED = 0;

  PYTHONPATH = builtins.toPath ./.;
}
