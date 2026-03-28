#!/usr/bin/env bash
set -euo pipefail
DB_PATH="${1:-/mnt/data/fcn_master_lexicon_phase6_review.sqlite}"
OUT_DIR="${2:-/mnt/data/phase7_reports}"
REVIEW_DB="${3:-/mnt/data/fcn_master_lexicon_phase7_review.sqlite}"
cd /mnt/data/amoxcalli-nahuatl-project-main/phase7
python3 fcn_phase7_build_core_lexicon.py --db "$DB_PATH" --out-dir "$OUT_DIR" --review-db "$REVIEW_DB"
