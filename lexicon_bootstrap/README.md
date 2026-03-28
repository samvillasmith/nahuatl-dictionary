# lexicon_bootstrap/ — First Unified Lexicon Assembly

This directory assembles all parsed source data from `../source_data/` into the first unified FCN master lexicon database. The database schema and register separation model are established here.

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
| `fcn_phase4_master_lexicon_schema.sql` | Database schema — defines all tables, views, and indexes |
| `fcn_phase4_master_lexicon_schema.md` | Human-readable schema documentation |
| `duplicate_candidates.csv` | Entries flagged for deduplication review (372 KB) |
| `PHASE5_IMPORT_README.md` | Detailed import documentation |
| `run_phase5_import.sh` | Shell runner |

## Output scale

The database established here carries forward through the entire pipeline. The schema's core architectural decision — **separate columns for EHN spoken form, MSN headword, MSN poetic form, and classical citation form** — enforces register separation at the data model level. Registers cannot be accidentally collapsed.

## Input

- `../source_data/simeon_parsed.json` — 28,709 Siméon entries
- `../source_data/nahuatl_kaikki_unified.json` — 8,465 Kaikki lexical rows
- `../source_data/out_ud/` — UD treebank grammar evidence

## Running

```bash
bash run_phase5_import.sh
# or
python fcn_phase5_import.py
```

## Next step

`../orthography/` applies FCN orthographic normalization to this database.
