# Flor y Canto Nahuatl — Deliverable 4
## Master Lexicon Schema (v0.1 draft)

### Canonical storage choice
Use a **SQLite relational database** as the canonical authoring store:
- filename: `fcn_master_lexicon.sqlite`
- text encoding: UTF-8
- normalization target: Unicode NFC
- canonical export view: `v_lexicon_flat_export`
- interchange exports: CSV, JSONL, Parquet

### Row grain
One row in `lexicon_entries` represents **one curated lexical sense**, not one raw source row and not one orthographic token.

### Required main-table fields
- `entry_id`
- `project_name`
- `ehn_spoken_form`
- `msn_headword`
- `msn_poetic_form`
- `classical_citation_form`
- `part_of_speech`
- `register`
- `variety`
- `gloss_en`
- `gloss_es`
- `root_family`
- `source_file`
- `source_reference`
- `source_confidence`
- `speaker_validation_status`
- `editorial_status`
- `notes_internal`
- `notes_public`

### Supporting tables
- `sources`
- `entry_sources`
- `variants`
- `roots_families`
- `examples`
- `validation`
- `literary_notes`

### ID format
- `FCN-LEX-000001` — lexical sense entry
- `FCN-SRC-000001` — source record
- `FCN-ESR-000001` — entry-source link
- `FCN-VAR-000001` — variant
- `FCN-ROOT-000001` — root family
- `FCN-EX-000001` — example
- `FCN-VAL-000001` — validation record
- `FCN-LIT-000001` — literary note

### Core rule
Do not collapse EHN, MSN neutral, MSN poetic, and Classical citation into a single undifferentiated form field. The main table stores the **preferred publication-facing form set** for one sense. All additional forms and attestations live in supporting tables.
