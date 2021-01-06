#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

source $LOCAL_DIR/../.env

MYPYPATH=$PYTHONPATH mypy \
    --disallow-untyped-defs \
    --disallow-incomplete-defs \
    --show-column-numbers \
    -p $PYTHONPATH
