#!/usr/bin/env bash

set -e

echo "Building documentation..."
cd docs
make clean
make html
cd ../
echo "Successfully built the documentation!"
