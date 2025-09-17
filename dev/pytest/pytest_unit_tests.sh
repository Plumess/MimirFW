#!/bin/bash
set -x

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
cd "$SCRIPT_DIR/../.."

# run unit tests
uv run --directory api --dev pytest api/tests/unit_tests
