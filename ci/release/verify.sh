#!/usr/bin/env nix-shell
#!nix-shell -I nixpkgs=channel:nixos-unstable-small --pure --keep POETRY_PYPI_TOKEN_PYPI -p dyff git poetry yj -i bash
# shellcheck shell=bash

set -euo pipefail

# verify TOML is sane
poetry check

# verify lock file is up to date
bash ./dev/lockfile_diff.sh

# verify that we have a token available to push to pypi using set -u
: "${POETRY_PYPI_TOKEN_PYPI}"
