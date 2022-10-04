poetry shell

# Clean existing protos
proto_dir=./proto
rm -r "$proto_dir"

# Copy proto from substrait repo
cp -fr ../substrait/proto ./

# Changes permissions
find "$proto_dir" -type d -exec chmod u+rwx {} +
find "$proto_dir" -type f -exec chmod u+rw {} +

# Clean compiled Python proto definitions
rm -rf ./ibis_substrait/proto

# Map the namespaces for the protos
python proto_prefix.py "$proto_dir"/tmp substrait.ibis "$proto_dir"/substrait
mv "$proto_dir"/substrait substrait.bak
mv "$proto_dir"/tmp/substrait "$proto_dir"

# Bring in the proto
curl \
  --header "Accept: application/vnd.github.VERSION.raw" \
  https://api.github.com/repos/westonpace/arrow/contents/cpp/proto/substrait/extension_rels.proto\?ref\=feature/bamboo-demo \
  --output "$proto_dir"/extension_rels.proto

# Modify asof Substrait namespace references to use substrait.ibis
sed -i '' 's/substrait\//substrait\/ibis\//g' "$proto_dir"/extension_rels.proto
sed -i '' 's/\.substrait\./.substrait.ibis./g' "$proto_dir"/extension_rels.proto

# Generate protobufs
buf generate
protol --in-place --create-package --python-out "./ibis_substrait/proto" buf
rm -rf "$proto_dir"/tmp
rm -rf "$proto_dir"/substrait
mv substrait.bak "$proto_dir"/substrait