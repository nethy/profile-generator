#!/usr/bin/env -S bash -e

LOCAL_DIR="$(dirname "${BASH_SOURCE[0]}")"

echo "Checking typing"
$LOCAL_DIR/check_typing.sh
echo

echo "Checking linting"
$LOCAL_DIR/check_linting.sh
echo

echo "Running tests"
$LOCAL_DIR/run_tests.sh
echo

echo "Checking formatting"
$LOCAL_DIR/check_formatting.sh
echo
