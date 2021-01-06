#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

source $LOCAL_DIR/../.env

PYTHONPATH=$PYTHONPATH pylint --rcfile=$LOCAL_DIR/pylintrc $PYTHONPATH
