# Phase 8.3 — Lesson Export and Productization

## Purpose
Convert the assembled instructional database into lesson-ready exports for app, textbook, drills, and printable packets.

## Inputs
- `fcn_master_lexicon_phase8_2_units.sqlite`
- `v_phase82_unit_plan`
- `v_phase82_vocab_priority`
- `v_phase82_construction_priority`
- `v_phase82_dialogue_samples`
- `v_phase82_band_pack`

## Outputs per unit
1. lesson overview
2. target vocab
3. target constructions
4. dialogue set
5. exercises
6. quiz/review items
7. app/textbook export formats

## Deliverables
- `unit_exports/markdown/`
- `unit_exports/json/`
- `unit_exports/csv/`
- `unit_exports/printable/`
- manifest files for app/textbook use

## Rules
- Use only canonical English units for core export packets
- Keep bilingual fields where available, but do not require Spanish for export completeness
- Preserve proficiency band tags
- Preserve lesson number
- Preserve source-aware notes if present

## Exit criteria
All 32 canonical units export successfully in:
- markdown
- json
- csv

And at least one printable packet is generated per unit.
