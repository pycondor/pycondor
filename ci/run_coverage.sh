#!/usr/bin/env bash

set -e

echo "Running code coverage..."
pip install codecov
codecov
