#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

source $LOCAL_DIR/../.env

black --check $PYTHONPATH
isort --check --profile black $PYTHONPATH
