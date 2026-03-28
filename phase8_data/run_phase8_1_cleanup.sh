#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 INPUT_DB OUTPUT_DB REPORT_DIR" >&2
  exit 1
fi

python fcn_phase8_1_cleanup.py --db "$1" --out-db "$2" --report-dir "$3"
