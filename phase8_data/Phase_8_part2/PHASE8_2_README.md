# Phase 8.2 — Unit Assembly and Proficiency Mapping

This stage consumes a cleaned Phase 8.1 SQLite database and produces a canonical pedagogical unit plan, band packs, prioritized vocabulary/construction exports, dialogue samples, and a Phase 8.2 output database.

## Inputs
- `fcn_master_lexicon_phase8_1_clean.sqlite`

## Outputs
- `fcn_master_lexicon_phase8_2_units.sqlite`
- `phase8_2_reports/phase82_summary.json`
- `phase8_2_reports/phase82_unit_plan.csv`
- `phase8_2_reports/phase82_band_packs.csv`
- `phase8_2_reports/phase82_vocab_priority_top500.csv`
- `phase8_2_reports/phase82_construction_priority_top300.csv`
- `phase8_2_reports/phase82_dialogue_samples.csv`

## What Phase 8.2 does
1. Reads the canonical lesson pairings from Phase 8.1 (`v_phase81_canonical_lessons`).
2. Creates one pedagogical unit per unique lesson number.
3. Populates `pedagogical_units` with generated FCN unit rows.
4. Builds band packs for A1, A2, B1, and a B2 bridge built from the densest B1 lessons.
5. Prioritizes lesson-attested English vocabulary and constructions by recurrence and lesson spread.
6. Exports two dialogue samples per English lesson for quick review and curriculum drafting.

## Run
```bash
python fcn_phase8_2_unit_assembly.py \
  --db ./fcn_master_lexicon_phase8_1_clean.sqlite \
  --out-db ./fcn_master_lexicon_phase8_2_units.sqlite \
  --report-dir ./phase8_2_reports
```

## Inspect in DB Browser
Open `fcn_master_lexicon_phase8_2_units.sqlite` and inspect:
- `v_phase82_unit_plan`
- `v_phase82_a1_units`
- `v_phase82_a2_units`
- `v_phase82_b1_units`
- `v_phase82_b2_bridge_units`
- `v_phase82_vocab_priority`
- `v_phase82_construction_priority`
- `v_phase82_dialogue_samples`
- `v_phase82_band_pack`

## Notes
The B2 bridge is intentionally conservative. It does not claim that the source course itself is B2; it identifies the strongest B1 lessons to reuse for extended controlled speaking and writing tasks.
