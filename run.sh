#!/usr/bin/env -S bash -e

PYTHONPATH=profile_generator
PYTHONPATH=$PYTHONPATH python -m $PYTHONPATH "$@"
