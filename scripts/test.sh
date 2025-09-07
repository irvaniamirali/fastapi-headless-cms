#!/usr/bin/env bash
set -euo pipefail

pytest --maxfail=1 --disable-warnings -q --cov=app --cov-report=term-missing
