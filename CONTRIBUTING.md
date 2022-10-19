# Set up dev environment

1. Install [nix](https://nixos.org/download.html)

2. Fork and clone the repository

```sh
gh repo fork --clone --remote ibis-project/ibis-substrait
```

3. Set up public `ibis-substrait` Cachix cache to pull pre-built dependencies:

```sh
nix-shell -p cachix --run 'cachix use ibis-substrait'
```

4. Run `nix-shell` in the checkout directory

```sh
cd ibis-substrait
nix-shell
```

# Updating the bundled proto files

1. Open `nix/default.nix` and look for this block:

```
      substrait = pkgs.fetchFromGitHub {
        owner = "substrait-io";
        repo = "substrait";
        rev = "4e70145508133988967db1f3dc96a45ce555867f";
        sha256 = "sha256:1c4d6asdghbp00qr8zrirxqwqhnhkjk8qy1phy1cmq2fvyzggqp3";
      };
```

2. Update the `rev` to the release of `substrait` you want to use and zero out
   the `sha256` hash:

```diff
       substrait = pkgs.fetchFromGitHub {
         owner = "substrait-io";
         repo = "substrait";
-        rev = "4e70145508133988967db1f3dc96a45ce555867f";
-        sha256 = "sha256:1c4d6asdghbp00qr8zrirxqwqhnhkjk8qy1phy1cmq2fvyzggqp3";
+        rev = "f3f6bdc947e689e800279666ff33f118e42d2146";
+        sha256 = "sha256:0000000000000000000000000000000000000000000000000000";
       };
```

3. Run `nix-shell` again to trigger a rebuild. This will error and will report
   the new `sha256` hash to use:

```sh
...
unpacking source archive /build/f3f6bdc947e689e800279666ff33f118e42d2146.tar.gz
hash mismatch in fixed-output derivation '/nix/store/0gncgfv4fwjs93alhpkskmmxk65qsn3q-source':
  wanted: sha256:0000000000000000000000000000000000000000000000000000
  got:    sha256:156rg46g9z7rcq5bkksvmfxdlj9djxx03zlahgfqb5h2b1h794cy
cannot build derivation '/nix/store/jqfylm2prkxqf33qjv8w5d3nlkivp0qq-gen-protos.drv': 1 dependencies couldn't be built
error: build of '/nix/store/jqfylm2prkxqf33qjv8w5d3nlkivp0qq-gen-protos.drv' failed
```

4. Update `nix/default.nix` with the new hash:

```diff
       substrait = pkgs.fetchFromGitHub {
         owner = "substrait-io";
         repo = "substrait";
-        rev = "4e70145508133988967db1f3dc96a45ce555867f";
-        sha256 = "sha256:1c4d6asdghbp00qr8zrirxqwqhnhkjk8qy1phy1cmq2fvyzggqp3";
+        rev = "f3f6bdc947e689e800279666ff33f118e42d2146";
+        sha256 = "sha256:156rg46g9z7rcq5bkksvmfxdlj9djxx03zlahgfqb5h2b1h794cy";
       };
```

5. Run `nix-shell` once more to load the new substrait `proto` files.  If this
   completes without error, run `gen-protos` inside of `nix-shell` to update the
   generated protobuf stub files.

```sh
$ gen-protos
proto_prefix.py: wrote 8 file(s), 0 up-to-date, 0 not in src prefix
Writing mypy to substrait/ibis/extensions/extensions_pb2.pyi
Writing mypy to substrait/ibis/type_pb2.pyi
Writing mypy to substrait/ibis/algebra_pb2.pyi
Writing mypy to substrait/ibis/capabilities_pb2.pyi
Writing mypy to substrait/ibis/parameterized_types_pb2.pyi
Writing mypy to substrait/ibis/type_expressions_pb2.pyi
Writing mypy to substrait/ibis/function_pb2.pyi
Writing mypy to substrait/ibis/plan_pb2.pyi
```
