# MSN Word Inventory — Workspace Copy

This directory is a **local working copy** of the Kaikki/Wiktionary and Siméon source data. It duplicates files that are canonically stored in `../fcn_ingest/`.

## Contents

| File | Canonical location |
|---|---|
| `kaikki_nci.jsonl` (Classical Nahuatl) | `../fcn_ingest/kaikki_nci.jsonl` |
| `kaikki_nhn.jsonl` (Central Nahuatl) | `../fcn_ingest/kaikki_nhn.jsonl` |
| `kaikki_nch.jsonl` (Central Huasteca) | `../fcn_ingest/kaikki_nch.jsonl` |
| `kaikki_nhe.jsonl` (Eastern Huasteca) | `../fcn_ingest/kaikki_nhe.jsonl` |
| `nahuatl_kaikki_raw.jsonl` | `../fcn_ingest/nahuatl_kaikki_raw.jsonl` |
| `nahuatl_kaikki_unified.json` | `../fcn_ingest/nahuatl_kaikki_unified.json` |
| `simeon_parsed.json` | `../fcn_ingest/simeon_parsed.json` |
| `simeon_1885_ocr_raw.txt` | `../fcn_ingest/simeon_1885_ocr_raw.txt` |
| `simeon_wordlist.txt` | `../fcn_ingest/simeon_wordlist.txt` |
| `simeon_parser.py` | `../fcn_ingest/simeon_parser.py` |

## Use

Use this directory as a scratch workspace for MSN word inventory work. Do not treat these files as more authoritative than their canonical counterparts in `../fcn_ingest/`. If the two copies diverge, `../fcn_ingest/` wins.
