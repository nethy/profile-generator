#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

source $LOCAL_DIR/../.env

echo "Formatting code"
black $PYTHONPATH
echo

echo "Sorting imports"
isort --profile=black $PYTHONPATH
echo
