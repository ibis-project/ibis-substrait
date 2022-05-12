{ pkgs, ... }:
self: super:
{
  protobuf = super.protobuf.overridePythonAttrs (
    old: {
      nativeBuildInputs = old.nativeBuildInputs or [ ] ++ [ self.pyext ];
      propagatedNativeBuildInputs = old.propagatedNativeBuildInputs or [ ] ++ [
        pkgs.buildPackages.protobuf
      ];
      buildInputs = old.buildInputs or [ ] ++ [ pkgs.buildPackages.protobuf ];
      preConfigure = ''
        export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
        export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=2
      '';

      preBuild = ''
        ${self.python.pythonForBuild.interpreter} setup.py build
        ${self.python.pythonForBuild.interpreter} setup.py build_ext --cpp_implementation
      '';

      installFlags = "--install-option='--cpp_implementation'";
      postInstall = ''
        cp -v $(find build -name "_message*") $out/${self.python.sitePackages}/google/protobuf/pyext
      '';
    }
  );

  ibis-framework = super.ibis-framework.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.poetry-core ];
  });

  protoletariat = super.protoletariat.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.poetry-core ];
  });

  traitlets = super.traitlets.overridePythonAttrs (attrs: {
    nativeBuildInputs = attrs.nativeBuildInputs or [ ] ++ [ self.flit-core ];
  });

  pandas = super.pandas.overridePythonAttrs (_: {
    format = "setuptools";
    enableParallelBuilding = true;
  });

  pydantic = super.pydantic.overridePythonAttrs (_: {
    format = "setuptools";
    enableParallelBuilding = true;
  });
}
