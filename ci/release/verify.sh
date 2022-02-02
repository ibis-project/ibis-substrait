#!/usr/bin/env nix-shell
#!nix-shell --pure --keep POETRY_PYPI_TOKEN_PYPI -p poetry -p git -i bash
# shellcheck shell=bash

set -euo pipefail

# verify TOML is sane
poetry check

# verify that the lock file is up to date
# we set PYTHONHASHSEED=some_constant here
# to avoid reordering of poetry extras
# see https://github.com/python-poetry/poetry/issues/5125
PYTHONHASHSEED=0 poetry lock --no-update
git diff --exit-code poetry.lock

# verify that we have a token available to push to pypi using set -u
: "${POETRY_PYPI_TOKEN_PYPI}"
