#!/usr/bin/env bash

set -e

echo "Running tests..."
echo ""
pytest --cov pycondor

echo "Running flake8..."
echo ""
flake8 pycondor

echo "Moving coverage report to 'shared' volume"
echo ""
mv .coverage /shared
