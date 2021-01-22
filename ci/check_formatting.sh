#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

. $LOCAL_DIR/../.env

black --check $PACKAGE
isort --check --profile black $PACKAGE
