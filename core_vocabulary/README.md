# core_vocabulary/ — Curated EHN Vocabulary Sets and Example Bank

This directory contains the editorially curated core vocabulary sets that define what EHN speakers need to know at each level. These lists are the direct input to the instructional curriculum in `../curriculum/`.

## What this phase does

- Selects a prioritized core EHN vocabulary (250-item and 500-item sets)
- Compiles 100 essential verbs
- Builds an everyday example bank from attested and editorially normalized sentences
- Compiles function word and social interaction inventories
- Produces the database that feeds directly into `../curriculum/`

## Key files

| File | Description |
|---|---|
| `fcn_phase7_build_core_lexicon.py` | Main build script (29.2 KB) |
| `fcn_master_lexicon_phase7_review.sqlite` | Output database (~105 MB) — direct input to `../curriculum/` |
| `core_ehn_250.csv` | Top 250 EHN everyday words (76.3 KB) |
| `core_ehn_500.csv` | Top 500 EHN everyday words (150 KB) |
| `core_verbs_100.csv` | 100 essential verbs (29.6 KB) |
| `everyday_example_bank.csv` | Example sentences (16.5 KB) |
| `function_words.csv` | Function word inventory (26.1 KB) |
| `social_interaction.csv` | Social interaction vocabulary (15.9 KB) |
| `fcn_phase7_core_lexicon.md` | Phase documentation |

## Why these files matter

The `core_ehn_250.csv` and `core_ehn_500.csv` lists are the editorial curation of the most pedagogically important EHN spoken vocabulary. They seed the 1,008-item primer vocabulary assembled in `../curriculum/`. The `everyday_example_bank.csv` is the precursor to the 215 lesson dialogues in the curriculum database.

## Next step

`../curriculum/` takes `fcn_master_lexicon_phase7_review.sqlite` as its lexical input and runs the full instructional pipeline on top of it.
