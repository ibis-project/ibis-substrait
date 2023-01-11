{ python ? "3.10" }:
let
  pkgs = import ./nix { };

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
    protobuf3_20
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
      python proto_prefix.py "$proto_dir"/tmp substrait.ibis "$proto_dir"/substrait
      mv "$proto_dir"/substrait substrait.bak
      mv "$proto_dir"/tmp/substrait "$proto_dir"
      buf generate
      protol --in-place --create-package --python-out "./ibis_substrait/proto" buf
      rm -rf "$proto_dir"/tmp
      rm -rf "$proto_dir"/substrait
      mv substrait.bak "$proto_dir"/substrait
    '';
  };
in
pkgs.mkShell {
  name = "ibis-substrait-${pythonShortVersion}";

  shellHook = ''
    ${(import ./pre-commit.nix).pre-commit-check.shellHook}
  '';

  nativeBuildInputs = devDeps ++ [ ibisSubstraitDevEnv genProtos ];
}
