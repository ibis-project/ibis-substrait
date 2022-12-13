{ pkgs, ... }:
let
  inherit (pkgs) lib stdenv;
  parallelizeSetuptoolsBuild = drv: drv.overridePythonAttrs (attrs: {
    format = "setuptools";
    enableParallelBuilding = true;
    setupPyBuildFlags = attrs.setupPyBuildFlags or [ ] ++ [ "--parallel" "$NIX_BUILD_CORES" ];
  });
in
self: super:
{
  protobuf = super.protobuf.overridePythonAttrs (
    attrs: {
      format = "setuptools";
      setupPyBuildFlags = attrs.setupPyBuildFlags or [ ] ++ [ "--cpp_implementation" ];

      propagatedNativeBuildInputs = attrs.propagatedNativeBuildInputs or [ ] ++ [
        pkgs.buildPackages.protobuf3_20
      ];
      buildInputs = attrs.buildInputs or [ ] ++ [ pkgs.buildPackages.protobuf3_20 ];
      preConfigure = ''
        export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
        export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=2
      '';

      installFlags = "--install-option='--cpp_implementation'";
      postInstall = ''
        cp -v $(find build -name "_message*") $out/${self.python.sitePackages}/google/protobuf/pyext
      '';
    }
  );

  duckdb = super.duckdb.overridePythonAttrs (
    _: {
      prePatch = ''
        substituteInPlace setup.py --replace "multiprocessing.cpu_count()" "int(os.getenv('NIX_BUILD_CORES', multiprocessing.cpu_count()))"

      '';
    }
  );

  protoletariat = super.protoletariat.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.poetry-core ];
  });

  traitlets = super.traitlets.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.flit-core ];
  });

  jdot = super.jdot.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.setuptools ];
  });

  pydantic = (parallelizeSetuptoolsBuild super.pydantic).overridePythonAttrs (attrs: {
    buildInputs = attrs.buildInputs or [ ] ++ lib.optionals (self.pythonOlder "3.9") [ pkgs.libxcrypt ];
  });

  pandas = parallelizeSetuptoolsBuild super.pandas;
  substrait-validator = super.substrait-validator.override {
    preferWheel = true;
  };
}
