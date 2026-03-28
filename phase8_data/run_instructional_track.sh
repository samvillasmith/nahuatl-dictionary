#!/usr/bin/env bash
set -euo pipefail

DB_IN="${1:-./fcn_master_lexicon_phase8_2_units.sqlite}"

python fcn_phase8_3_lesson_export.py   --db "$DB_IN"   --out-db ./fcn_master_lexicon_phase8_3.sqlite   --report-dir ./phase8_3_reports

python fcn_phase8_4_assessment_layer.py   --db ./fcn_master_lexicon_phase8_3.sqlite   --out-db ./fcn_master_lexicon_phase8_4.sqlite   --report-dir ./phase8_4_reports

python fcn_phase8_5_product_bundles.py   --db ./fcn_master_lexicon_phase8_4.sqlite   --out-db ./fcn_master_lexicon_phase8_5.sqlite   --report-dir ./phase8_5_reports

python fcn_phase8_6_primer_foundation.py   --db ./fcn_master_lexicon_phase8_5.sqlite   --out-db ./fcn_master_lexicon_phase8_6.sqlite   --report-dir ./phase8_6_reports

echo "Instructional track 8.3–8.6 complete."
