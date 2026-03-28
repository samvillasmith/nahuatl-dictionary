# Phase 8 — Open-only Nāhuatlahtolli Expansion

This phase executes the open-only plan for getting FCN to a real conversational EHN track without touching restricted sources.

## What this phase adds

- `fcn_phase8_schema.sql`
  - lesson tables
  - dialogue tables
  - lesson vocabulary alignment table
  - pedagogical units table
  - construction bank table

- `fcn_phase8_open_sources.json`
  - open-only source config
  - Nāhuatlahtolli as the modern lesson backbone
  - existing FCN open sources retained for lexical, grammar, and reference support

- `fcn_phase8_open_only.py`
  - copies an existing FCN SQLite DB
  - applies the Phase 8 schema extension
  - registers open sources in `sources`
  - ingests lesson data from either:
    1. existing `nahuatlahtolli-to-bank` outputs, or
    2. direct crawl of open lesson pages
  - derives dialogue rows, lesson vocab, pedagogical units, and construction candidates

- `run_phase8_open_only.sh`
  - convenience runner

## Inputs

### Option A — preferred if you already have lesson-bank output

Use an existing parser output directory containing:

- `lessons_index.csv`
- `lesson_blocks.jsonl`

Example:

```bash
cd /mnt/data/amoxcalli-nahuatl-project-main/phase8
./run_phase8_open_only.sh \
  /mnt/data/fcn_master_lexicon.sqlite \
  /mnt/data/fcn_master_lexicon_phase8_open_only.sqlite \
  /mnt/data/phase8_reports \
  /path/to/out_nahuatlahtolli
```

### Option B — crawl the open lesson site directly

This requires network access on the machine where you run it.

```bash
cd /mnt/data/amoxcalli-nahuatl-project-main/phase8
./run_phase8_open_only.sh \
  /mnt/data/fcn_master_lexicon.sqlite \
  /mnt/data/fcn_master_lexicon_phase8_open_only.sqlite \
  /mnt/data/phase8_reports
```

## Outputs

The Phase 8 output DB will contain new tables:

- `lesson_units`
- `lesson_blocks`
- `lesson_dialogues`
- `lesson_vocab`
- `pedagogical_units`
- `construction_bank`

Useful views:

- `v_phase8_dialogue_export`
- `v_phase8_vocab_alignment`

Reports written to the report directory:

- `phase8_summary.json`
- `phase8_lessons.csv`
- `phase8_constructions.csv`

## Recommended follow-up after first run

1. inspect `lesson_units`
2. inspect `lesson_dialogues`
3. inspect `v_phase8_vocab_alignment`
4. review unmatched lesson vocabulary
5. promote the best constructions into curated A1–B1 teaching units
6. draft the first 12 pedagogical units from the imported lesson material

## Important boundary

This is an **open-only** phase.

Do not feed restricted or permission-needed sources into this pipeline.
