# Phase 6 — Orthography and Style Normalization

Phase 6 applies FCN orthographic conventions to the master lexicon and establishes the style manual that governs all subsequent production.

## What this phase does

- Normalizes headwords and spoken forms to FCN orthography (k, s, w, ts, h, macrons for vowel length)
- Flags entries with unresolved orthographic conflicts for review
- Produces EHN→MSN candidate mappings for register-boundary work
- Establishes the FCN style manual as a governance document

## FCN orthographic conventions (established here)

| Classical / variant | FCN convention | Example |
|---|---|---|
| c / qu before e/i | k | *quetza* → *quētza* → **kētza** |
| z / ç | s | *cihuatl* → **siwatl** |
| hu / uh | w | *huatl* → **watl** |
| tz | ts | *tzintli* → **tsintli** |
| glottal stop | h | *tlahtoa* → **tlahtoa** |
| vowel length | macron (ā ē ī ō) | *nahuatl* → **nāhuatl** |

## Key files

| File | Description |
|---|---|
| `fcn_phase6_normalize.py` | Normalization script (10 KB) |
| `fcn_master_lexicon_phase6_review.sqlite` | Output database (~104 MB) |
| `fcn_phase6_orthography_manual.md` | FCN orthography reference (12.8 KB) |
| `fcn_phase6_style_manual.md` | FCN style manual (11 KB) |
| `ehn_to_msn_candidates.csv` | EHN→MSN normalization candidates (123 KB) |
| `PHASE6_README.md` | Phase documentation |

## Next phase

Phase 7 (`../phase7/`) builds the core lexicon and example bank from the normalized database.
