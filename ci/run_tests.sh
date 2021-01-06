#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

source $LOCAL_DIR/../.env

python -m unittest discover -v -s $PYTHONPATH -p "*_test.py"
