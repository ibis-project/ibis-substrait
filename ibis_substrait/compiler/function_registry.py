import importlib
import itertools
from collections import defaultdict
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any, Optional, Union

import yaml

from .mapping import normalize_substrait_type_names


class FunctionEntry:
    def __init__(self, name: str) -> None:
        self.name = name
        self.options: Mapping[str, Any] = {}
        self.arg_names: list = []
        self.inputs: list = []
        self.normalized_inputs: list = []
        self.uri: str = ""

    def parse(self, impl: Mapping[str, Any]) -> None:
        self.rtn = impl["return"]
        self.nullability = impl.get("nullability", False)
        self.variadic = impl.get("variadic", False)
        if input_args := impl.get("args", []):
            for val in input_args:
                if typ := val.get("value"):
                    self.inputs.append(typ.strip("?"))
                    self.normalized_inputs.append(normalize_substrait_type_names(typ))
                elif arg_name := val.get("name", None):
                    self.arg_names.append(arg_name)

        if options_args := impl.get("options", []):
            for val in options_args:
                self.options[val] = options_args[val]["values"]  # type: ignore

    def __repr__(self) -> str:
        return f"{self.name}:{'_'.join(self.normalized_inputs)}"

    def castable(self) -> None:
        raise NotImplementedError

    def satisfies_signature(self, signature: tuple) -> Optional[str]:
        import re

        def is_any_variable(txt: str) -> bool:
            return txt.startswith("any") and txt[-1].isnumeric()

        # TODO come up with better way parse variables
        def is_variable(txt: str) -> bool:
            return txt.startswith("P") or txt.startswith("S")

        def to_tuple_type(txt: str) -> tuple:
            return tuple([i for i in re.split(r"\W+", txt) if i != ""])

        def to_string_type(tp: tuple) -> str:
            return tp[0] + (f"<{','.join(tp[1:])}>" if len(tp) > 1 else "")

        if self.variadic:
            min_args_allowed = self.variadic.get("min", 0)
            if len(signature) < min_args_allowed:
                return None
            inputs = [self.inputs[0]] * len(signature)
        else:
            inputs = self.inputs

        if len(inputs) != len(signature):
            return None

        signature_tuple = [to_tuple_type(arg) for arg in signature]
        inputs = [to_tuple_type(arg) for arg in inputs]
        rtn = to_tuple_type(self.rtn)

        zipped_args = list(zip(inputs, signature_tuple))

        var_mapping = {}

        for x, y in zipped_args:
            for i, j in zip(x, y):
                if is_any_variable(i) and i not in var_mapping:
                    var_mapping[i] = to_string_type(y)
                elif is_variable(i) and i not in var_mapping:
                    var_mapping[i] = j

            if is_any_variable(x[0]):
                x_str = var_mapping.get(x[0])
            else:
                x_str = to_string_type(
                    tuple([var_mapping.get(i, i).lower() for i in x])
                )

            y_str = to_string_type(y)

            compatible = x_str == y_str or x_str == "any"

            if not compatible:
                return None

        rtn = tuple([var_mapping.get(i, i) for i in rtn])
        return to_string_type(rtn)


def _parse_func(entry: Mapping[str, Any]) -> Iterator[FunctionEntry]:
    for impl in entry.get("impls", []):
        sf = FunctionEntry(entry["name"])
        sf.parse(impl)

        yield sf


class FunctionRegistry:
    def __init__(self) -> None:
        self._extension_mapping: dict = defaultdict(dict)
        self.id_generator = itertools.count(1)

        self.uri_aliases = {}

        for fpath in importlib.resources.files("substrait.extensions").glob(  # type: ignore
            "functions*.yaml"
        ):
            self.uri_aliases[fpath.name] = (
                f"https://github.com/substrait-io/substrait/blob/main/extensions/{fpath.name}"
            )
            self.register_extension_yaml(fpath)

    def register_extension_yaml(
        self,
        fname: Union[str, Path],
        prefix: Optional[str] = None,
        uri: Optional[str] = None,
    ) -> None:
        """Add a substrait extension YAML file to the ibis substrait compiler.

        Parameters
        ----------
        fname
            The filename of the extension yaml to register.
        prefix
            Custom prefix to use when constructing Substrait extension URI
        uri
            A custom URI to use for all functions defined within `fname`.
            If passed, this value overrides `prefix`.


        """
        fname = Path(fname)
        with open(fname) as f:  # type: ignore
            extension_definitions = yaml.safe_load(f)

        prefix = (
            prefix.strip("/")
            if prefix is not None
            else "https://github.com/substrait-io/substrait/blob/main/extensions"
        )

        uri = uri or f"{prefix}/{fname.name}"

        self.register_extension_dict(extension_definitions, uri)

    def register_extension_dict(self, definitions: dict, uri: str) -> None:
        for named_functions in definitions.values():
            for function in named_functions:
                for func in _parse_func(function):
                    func.uri = uri
                    if (
                        func.uri in self._extension_mapping
                        and function["name"] in self._extension_mapping[func.uri]
                    ):
                        self._extension_mapping[func.uri][function["name"]].append(func)
                    else:
                        self._extension_mapping[func.uri][function["name"]] = [func]

    # TODO add an optional return type check
    def lookup_function(
        self, uri: str, function_name: str, signature: tuple
    ) -> Optional[tuple[FunctionEntry, str]]:
        uri = self.uri_aliases.get(uri, uri)
        if (
            uri not in self._extension_mapping
            or function_name not in self._extension_mapping[uri]
        ):
            return None
        functions = self._extension_mapping[uri][function_name]
        for f in functions:
            assert isinstance(f, FunctionEntry)
            rtn = f.satisfies_signature(signature)
            if rtn is not None:
                return (f, rtn)

        return None
