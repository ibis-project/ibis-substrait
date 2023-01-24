#!/usr/bin/env bash

set -eo pipefail

substrait_protos="${1:-${PROTO_DIR}}"

set -u

proto_dir=./proto
extension_dir=./ibis_substrait/extensions

mkdir -p "$proto_dir"
mkdir -p "$extension_dir"
chmod u+rwx "$proto_dir"
chmod u+rwx "$extension_dir"
rm -r "$proto_dir"
rm -r "$extension_dir"

cp -fr "$substrait_protos" "$proto_dir"
cp -fr "$substrait_protos/../extensions" "$extension_dir"

find "$proto_dir" -type d -exec chmod u+rwx {} +
find "$proto_dir" -type f -exec chmod u+rw {} +
find "$extension_dir" -type d -exec chmod u+rwx {} +
find "$extension_dir" -type f -exec chmod u+rw {} +

rm -rf ./ibis_substrait/proto

python proto_prefix.py "$proto_dir"/tmp substrait.ibis "$proto_dir"/substrait

mv "$proto_dir"/substrait substrait.bak
mv "$proto_dir"/tmp/substrait "$proto_dir"

buf generate
protol --in-place --create-package --python-out "./ibis_substrait/proto" buf

rm -rf "$proto_dir"/tmp
rm -rf "$proto_dir"/substrait
mv substrait.bak "$proto_dir"/substrait
