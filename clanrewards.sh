#!/bin/bash

SCRIPT_DIR=$(cd $(dirname "$0") && pwd);

if test -f "$SCRIPT_DIR/.venv/bin/python"; then
    "$SCRIPT_DIR/.venv/bin/python" $SCRIPT_DIR/src/__init__.py $*
else
    echo "Failed to load python executable."
    exit 1
fi
