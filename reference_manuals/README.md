# reference_manuals/ — Final Deliverables (D14–D18)

## IMPORTANT: These are editorial documents, not the database

The files in this directory are **reference manuals and editorial interfaces**. They are written documentation of the FCN data model — they are not the data itself.

**The production database lives in `../curriculum/`.**

| If you want | Go to |
|---|---|
| The lexicon (37,146 entries, 44,900 variants) | `../curriculum/fcn_master_lexicon_phase8_6_primer.sqlite` |
| The full primer vocabulary (1,008 items) | `../curriculum/phase8_6_reports/phase86_primer_units.csv` |
| All 32 unit exports in 4 formats | `../curriculum/phase8_3_reports/unit_exports/` |
| The constructions bank (278 primer items) | `../curriculum/phase8_2_reports/` |
| The assessment layer (160 items) | `../curriculum/phase8_4_reports/` |
| Lesson dialogues (22 primer / 215 total) | `../curriculum/phase8_3_reports/` |
| Poetic register inventory CSVs | `../poetic_register/` |
| Register conversion examples | `../register_conversion/` |

---

## What is in this directory

| File | Deliverable | What it is |
|---|---|---|
| `fcn_deliverable14_master_sourcebook.md` | D14 | Master Sourcebook: compiles all project principles, source governance, and register model decisions in one document |
| `fcn_deliverable15_spoken_ehn_primer.md` | D15 | Spoken EHN Primer: pedagogy model, 4 worked sample units, primer glossary seed, drill types, contamination screening |
| `fcn_deliverable16_msn_manual.md` | D16 | MSN Manual: orthographic reference, model prose sentences, paradigms, register conversion rules |
| `fcn_deliverable17_poetic_nahuatl_manual.md` | D17 | Poetic Nahuatl Manual: MSN-P register inventory, annotated examples, songwriting exercises, governance |
| `fcn_deliverable18_dictionary_manual.md` | D18 | Dictionary Manual: 18-field schema, 46-entry seed set, 4 publication format renderings |
| `dictionary_test_sample.csv` | — | 4-entry CSV sample for schema format testing |

---

## What each document actually is

**D14 (Master Sourcebook)** is the constitutional document for the project. It compiles all source governance decisions, register model principles, and authority hierarchy rules. Read this before working with any other document.

**D15 (Spoken EHN Primer)** documents the pedagogy model and editorial principles for the 23-unit, 1,008-item primer in `../curriculum/`. The 4 worked units in D15 are illustrative samples. The full 23 units, all vocabulary, all assessments, and all product bundles are in `../curriculum/`.

**D16 (MSN Manual)** documents the orthographic and register conventions established in `../orthography/` and applied through `../curriculum/`. The model sentences and paradigms illustrate the conventions; the canonical lexicon is in `../curriculum/`.

**D17 (Poetic Manual)** documents the MSN-P register using the Phase A seed inventory (21 items) from `../poetic_register/`. The conversion examples are from `../register_conversion/`.

**D18 (Dictionary Manual)** documents the 18-field entry schema with 46 seed entries illustrating the format. The full 37,146-entry lexicon is in `../curriculum/fcn_master_lexicon_phase8_6_primer.sqlite`, table `lexicon_entries`.

---

## Pipeline context

```
source_data/ → lexicon_bootstrap/ → orthography/ → core_vocabulary/ → curriculum/
                                                                           ↓
                                           poetic_register/ register_conversion/ editorial_qa/
                                                                           ↓
                                                               reference_manuals/  ← you are here
```
