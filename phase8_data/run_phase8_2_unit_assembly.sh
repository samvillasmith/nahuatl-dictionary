#!/usr/bin/env bash
set -euo pipefail
python fcn_phase8_2_unit_assembly.py \
  --db ./fcn_master_lexicon_phase8_1_clean.sqlite \
  --out-db ./fcn_master_lexicon_phase8_2_units.sqlite \
  --report-dir ./phase8_2_reports
