#!/usr/bin/env bash
# Format project codebase using black, isort, and ruff.

set -euo pipefail

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
TARGETS=("app" "scripts" "tests")

echo "Running isort..."
isort "${TARGETS[@]}"

echo "Running black..."
black "${TARGETS[@]}"

echo "Running ruff..."
ruff check --fix "${TARGETS[@]}"

echo "Code formatted successfully!"
