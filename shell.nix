{ python ? "3.10" }:
let
  pkgs = import ./nix;
  inherit (pkgs) lib;

  devDeps = with pkgs; [
    buf
    cacert
    cachix
    git
    jq
    niv
    nix-linter
    nixpkgs-fmt
    poetry
    prettierTOML
    protobuf
    sd
    shellcheck
    shfmt
    yj
  ];

  pythonShortVersion = builtins.replaceStrings [ "." ] [ "" ] python;
  ibisSubstraitDevEnv = pkgs."ibisSubstraitDevEnv${pythonShortVersion}";
  genProtos = pkgs.writeShellApplication {
    name = "gen-protos";
    runtimeInputs = with pkgs; [ buf ];
    text = ''
      proto_dir=./proto
      mkdir -p "$proto_dir"
      chmod u+rwx "$proto_dir"
      rm -rf "$proto_dir"
      cp -fr ${pkgs.substrait}/proto "$proto_dir"
      find "$proto_dir" -type d -exec chmod u+rwx {} +
      find "$proto_dir" -type f -exec chmod u+rw {} +
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

  PYTHONPATH = builtins.toPath ./.;
}
