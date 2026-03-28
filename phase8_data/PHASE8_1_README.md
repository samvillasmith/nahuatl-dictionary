# Phase 8.1 — Nahuatlahtolli cleanup and canonical lesson normalization

This step cleans the raw Phase 8 crawl output into a canonical instructional layer.

## What it does

- keeps only `Tlamachtiliztli N` lesson pages as lesson content
- drops site/navigation pages such as `Language`, `Funding`, `Resources`, `Units`, `Introduction`, `Contact`
- keeps the earliest canonical page for each `(lesson_number, locale)` pair
- preserves bilingual pairing (`en` and `es`) by lesson number
- drops later duplicate mirror pages within the same `(lesson_number, locale)` pair
- creates views for bilingual and English-only curriculum exports
- writes CSV reports and a summary JSON

## Inputs

- a successful Phase 8 SQLite database, such as `fcn_master_lexicon_phase8_open_only.sqlite`

## Outputs

The cleanup writes:

- a new SQLite DB with Phase 8.1 tables/views
- `phase81_summary.json`
- `phase81_canonical_lessons.csv`
- `phase81_english_core_lessons.csv`
- `phase81_spanish_parallel_lessons.csv`
- `phase81_duplicate_pages.csv`
- `phase81_noise_pages.csv`
- `phase81_lesson_counts.csv`

## Usage

```bash
python fcn_phase8_1_cleanup.py \
  --db ./fcn_master_lexicon_phase8_open_only.sqlite \
  --out-db ./fcn_master_lexicon_phase8_1_clean.sqlite \
  --report-dir ./phase8_1_reports
```

## Useful views in DB Browser

- `v_phase81_canonical_lesson_pages`
- `v_phase81_english_core_lessons`
- `v_phase81_spanish_parallel_lessons`
- `v_phase81_canonical_lessons`
- `v_phase81_vocab_bilingual`
- `v_phase81_vocab_english`
- `v_phase81_dialogues_bilingual`
- `v_phase81_dialogues_english`
- `v_phase81_constructions_bilingual`
- `v_phase81_constructions_english`
- `v_phase81_lesson_counts`
