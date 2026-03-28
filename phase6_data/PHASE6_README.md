# FCN Phase 6 README

This directory contains the completed Phase 6 deliverables for Flor y Canto Nahuatl.

## Files

- `fcn_phase6_orthography_manual.md` — Orthography Manual (Deliverable 6)
- `fcn_phase6_style_manual.md` — Style Manual (Deliverable 7)
- `fcn_phase6_normalize.py` — orthography normalization and search-fallback utility
- `run_phase6_exports.sh` — batch export script for EHN → MSN candidate mappings

## Run the orthography export

```bash
cd /mnt/data/amoxcalli-nahuatl-project-main/phase6
./run_phase6_exports.sh /mnt/data/fcn_master_lexicon.sqlite /mnt/data/phase6_reports
```

## Output files

The batch run writes:

- `/mnt/data/phase6_reports/ehn_to_msn_candidates.csv`
- `/mnt/data/phase6_reports/orthography_candidate_summary.json`

## One-off normalization example

```bash
python3 fcn_phase6_normalize.py normalize cihuatl
python3 fcn_phase6_normalize.py normalize cuahuitl
python3 fcn_phase6_normalize.py normalize oztotl
```

These commands are review tools. They do **not** write changes back into the canonical database.


## Review database

A review copy of the lexicon database was created at:

- `/mnt/data/fcn_master_lexicon_phase6_review.sqlite`

This copy adds:
- `phase6_msn_candidates`
- `v_phase6_ehn_review`

In DB Browser, open the review DB and browse `v_phase6_ehn_review` to inspect current vs proposed `MSN` headwords for EHN rows.
