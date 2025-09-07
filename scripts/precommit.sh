#!/usr/bin/env bash
set -euo pipefail

./scripts/format.sh
./scripts/lint.sh
./scripts/test.sh
