{ pkgs, ... }:
let
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

      nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.pyext ];
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

  protoletariat = super.protoletariat.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.poetry-core ];
  });

  traitlets = super.traitlets.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.flit-core ];
  });

  jdot = super.jdot.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.setuptools ];
  });

  pandas = parallelizeSetuptoolsBuild super.pandas;
  pydantic = parallelizeSetuptoolsBuild super.pydantic;
  substrait-validator = super.substrait-validator.override {
    preferWheel = true;
  };
}
