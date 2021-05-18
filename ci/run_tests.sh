#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

. $LOCAL_DIR/../.env

python -Wd -m unittest discover -v -s $PACKAGE -p "*_test.py"
