#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

. $LOCAL_DIR/../.env

mypy \
    --disallow-untyped-defs \
    --disallow-incomplete-defs \
    --show-column-numbers \
    -p $PACKAGE
