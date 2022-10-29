#!/usr/bin/env nix-shell
#!nix-shell -I nixpkgs=./nix --pure --keep POETRY_PYPI_TOKEN_PYPI -p git poetry -i bash
# shellcheck shell=bash

set -euo pipefail

# verify TOML is sane
poetry check

# verify lock file is consistent with pyproject.toml
poetry lock --check

# verify that we have a token available to push to pypi using set -u
: "${POETRY_PYPI_TOKEN_PYPI}"
