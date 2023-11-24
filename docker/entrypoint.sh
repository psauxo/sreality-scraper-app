#!/bin/sh

set -e

# activate our virtual environment here
. /usr/app/src/.venv/bin/activate

# Evaluating passed command:
exec "$@"
