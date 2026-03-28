#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="$BASE_DIR/fcn_master_lexicon.sqlite"
QA_DIR="$BASE_DIR/phase5_reports"

python3 "$BASE_DIR/fcn_phase5_import.py" \
  --repo "$BASE_DIR" \
  --schema "$BASE_DIR/fcn_phase4_master_lexicon_schema.sql" \
  --db "$DB_PATH" \
  --qa-dir "$QA_DIR" \
  --replace-db

python3 - <<'PY'
import json
from pathlib import Path
base = Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
summary_path = base / 'phase5_reports' / 'import_run_summary.json'
if summary_path.exists():
    print('\nSaved summary:')
    print(summary_path)
    print(summary_path.read_text(encoding='utf-8'))
PY
