#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DB_IN="${1:-/mnt/data/fcn_master_lexicon.sqlite}"
OUT_DB="${2:-/mnt/data/fcn_master_lexicon_phase8_open_only.sqlite}"
REPORT_DIR="${3:-/mnt/data/phase8_reports}"
LESSON_BANK_DIR="${4:-}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
SCHEMA="$REPO_DIR/phase8/fcn_phase8_schema.sql"
CONFIG="$REPO_DIR/phase8/fcn_phase8_open_sources.json"
SCRIPT="$REPO_DIR/phase8/fcn_phase8_open_only.py"

if [[ -n "$LESSON_BANK_DIR" ]]; then
  "$PYTHON_BIN" "$SCRIPT" \
    --db "$DB_IN" \
    --schema "$SCHEMA" \
    --config "$CONFIG" \
    --out-db "$OUT_DB" \
    --report-dir "$REPORT_DIR" \
    --lesson-bank-dir "$LESSON_BANK_DIR"
else
  "$PYTHON_BIN" "$SCRIPT" \
    --db "$DB_IN" \
    --schema "$SCHEMA" \
    --config "$CONFIG" \
    --out-db "$OUT_DB" \
    --report-dir "$REPORT_DIR" \
    --crawl
fi
