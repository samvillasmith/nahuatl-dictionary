# Phase 5 import instructions

This is the concrete next step after Phase 4.

## What this does

`fcn_phase5_import.py` will:

1. create the SQLite database from `fcn_phase4_master_lexicon_schema.sql`
2. register the source inventory in `sources`
3. import `out_kaikki/fcn_lexical_rows.jsonl` into:
   - `lexicon_entries`
   - `entry_sources`
   - `variants`
   - `entry_payloads`
4. import `simeon_parsed.json` into the classical/reference layer
5. stage `out_classical` into:
   - `classical_examples_staging`
   - `classical_blocks_staging`
6. link any conservative exact classical example matches into `examples`
7. flag duplicate candidates
8. write QA outputs to `phase5_reports/`

## Files created

- `fcn_master_lexicon.sqlite`
- `phase5_reports/summary.json`
- `phase5_reports/import_run_summary.json`
- `phase5_reports/register_counts.csv`
- `phase5_reports/variety_counts.csv`
- `phase5_reports/source_counts.csv`
- `phase5_reports/variant_distribution.csv`
- `phase5_reports/duplicate_candidates.csv`

## Run it

From inside `fcn_ingest/`:

```bash
chmod +x run_phase5_import.sh
./run_phase5_import.sh
```

Or directly:

```bash
python3 fcn_phase5_import.py \
  --repo . \
  --schema ./fcn_phase4_master_lexicon_schema.sql \
  --db ./fcn_master_lexicon.sqlite \
  --qa-dir ./phase5_reports \
  --replace-db
```

## Inspect the database with Python

Count entries by register:

```bash
python3 - <<'PY'
import sqlite3
conn = sqlite3.connect('fcn_master_lexicon.sqlite')
for row in conn.execute('SELECT register, COUNT(*) FROM lexicon_entries GROUP BY register ORDER BY COUNT(*) DESC'):
    print(row)
conn.close()
PY
```

Show a few EHN entries:

```bash
python3 - <<'PY'
import sqlite3
conn = sqlite3.connect('fcn_master_lexicon.sqlite')
for row in conn.execute("""
    SELECT entry_id, ehn_spoken_form, msn_headword, gloss_en, part_of_speech
    FROM lexicon_entries
    WHERE register = 'EHN_colloquial'
    ORDER BY msn_headword
    LIMIT 20
"""):
    print(row)
conn.close()
PY
```

Show flagged duplicate candidates:

```bash
python3 - <<'PY'
import sqlite3
conn = sqlite3.connect('fcn_master_lexicon.sqlite')
for row in conn.execute("""
    SELECT entry_id, COALESCE(ehn_spoken_form, msn_headword, classical_citation_form), part_of_speech, variety
    FROM lexicon_entries
    WHERE editorial_status = 'Flagged'
    LIMIT 50
"""):
    print(row)
conn.close()
PY
```

## What to do immediately after the import

1. inspect `phase5_reports/summary.json`
2. inspect `phase5_reports/duplicate_candidates.csv`
3. spot-check 20 EHN rows
4. spot-check 20 Siméon classical rows
5. only then move into Phase 6 orthography decisions

## Notes

- Siméon definitions are preserved in `entry_payloads.payload_json` and summarized in `notes_internal`.
- Raw OCR is **not** imported as canonical lexical rows.
- `out_classical` is staged conservatively because OCR headword linkage is noisy.
