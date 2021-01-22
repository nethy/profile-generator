#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

. $LOCAL_DIR/../.env

echo "Formatting code"
black $PACKAGE
echo

echo "Sorting imports"
isort --profile=black $PACKAGE
echo
