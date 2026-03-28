# Phase 5 — Master Lexicon Bootstrap

Phase 5 takes the parsed source data from `../fcn_ingest/` and assembles the first unified FCN master lexicon database.

## What this phase does

- Imports Siméon 1885 parsed entries, Kaikki/Wiktionary lexical rows, and UD treebank data
- Assigns FCN entry IDs (`FCN-LEX-000001` format)
- Creates initial register and variety classifications
- Deduplicates candidate entries and flags them for review
- Produces the first unified SQLite database

## Key files

| File | Description |
|---|---|
| `fcn_phase5_import.py` | Main import script (40.8 KB) |
| `fcn_master_lexicon.sqlite` | Output database (~104 MB) |
| `fcn_phase4_master_lexicon_schema.sql` | Database schema definition |
| `duplicate_candidates.csv` | Entries flagged for deduplication review (372 KB) |
| `PHASE5_IMPORT_README.md` | Detailed import documentation |
| `run_phase5_import.sh` | Shell runner |

## Output scale

The Phase 5 database contains the initial unified lexicon that is carried forward and expanded through Phases 6–8. The schema established here (distinct columns for EHN spoken form, MSN headword, MSN poetic form, classical citation form) is the foundation of the entire FCN register separation model.

## Input

- `../fcn_ingest/simeon_parsed.json` — 28,709 Siméon entries
- `../fcn_ingest/nahuatl_kaikki_unified.json` — 8,465 Kaikki lexical rows
- `../fcn_ingest/out_ud/` — UD treebank grammar evidence

## Next phase

Phase 6 (`../phase6/`) applies orthographic normalization to this database.
