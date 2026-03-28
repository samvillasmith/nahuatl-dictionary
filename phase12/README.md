# Phase 12 — Final Products (Deliverables 15–18)

## IMPORTANT: These are editorial documents, not the database

The four files in this directory are **reference manuals and editorial interfaces**. They are written documentation of the FCN data model — they are not the data itself.

The production database lives in **`../phase8/`**.

| If you want | Go to |
|---|---|
| The lexicon (37,146 entries, 44,900 variants) | `../phase8/fcn_master_lexicon_phase8_6_primer.sqlite` |
| The full primer vocabulary (1,008 items) | `../phase8/phase8_6_reports/phase86_primer_units.csv` |
| All 32 unit exports in 4 formats | `../phase8/phase8_3_reports/unit_exports/` |
| The constructions bank (278 primer items) | `../phase8/phase8_2_reports/` |
| The assessment layer (160 items) | `../phase8/phase8_4_reports/` |
| Lesson dialogues (22 primer / 215 total) | `../phase8/phase8_3_reports/` |

---

## What is in this directory

| File | Deliverable | What it is |
|---|---|---|
| `fcn_deliverable15_spoken_ehn_primer.md` | D15 | Spoken EHN Primer: pedagogy model, 4 worked sample units, primer glossary seed, drill types, contamination screening |
| `fcn_deliverable16_msn_manual.md` | D16 | MSN Manual: orthographic reference, model prose sentences, paradigms, register conversion rules |
| `fcn_deliverable17_poetic_nahuatl_manual.md` | D17 | Poetic Nahuatl Manual: MSN-P register inventory, annotated examples, songwriting exercises, governance |
| `fcn_deliverable18_dictionary_manual.md` | D18 | Dictionary Manual: 18-field schema, 46-entry seed set, 4 publication format renderings |
| `dictionary_test_sample.csv` | — | 4-entry CSV sample for format testing |

---

## Relationship to the full database

**D15 (Primer)** documents the pedagogy model and editorial principles for the 23-unit, 1,008-item primer that Phase 8 assembled. The 4 worked units in D15 are illustrative samples drawn from Phase 8 lesson exports. The full 23 units, all vocabulary, all assessments, and all product bundles are in `../phase8/`.

**D16 (MSN Manual)** documents the orthographic and register conventions that govern Phase 6–8 normalization. The model sentences and paradigms illustrate the conventions; the canonical lexicon is in `../phase8/`.

**D17 (Poetic Manual)** documents the MSN-P register using the Phase 9 seed inventory (21 items). Phase 9 source CSVs are in `../phase9/`.

**D18 (Dictionary Manual)** documents the 18-field entry schema with 46 seed entries. The full 37K-entry lexicon is in `../phase8/fcn_master_lexicon_phase8_6_primer.sqlite`, table `lexicon_entries`.

---

## Phase context

Phase 12 is the final editorial layer. The build order is:

```
fcn_ingest/ → phase5/ → phase6/ → phase7/ → phase8/
                                              ↓
                              phase9/ phase10/ phase11/
                                              ↓
                                          phase12/  ← you are here
```
