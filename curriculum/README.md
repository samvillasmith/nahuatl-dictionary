# curriculum/ — Instructional Pipeline and Production Database

This is the largest and most important directory in the FCN project. **The production database lives here.**

## Scale at a glance

| | Count |
|---|---|
| Lexicon entries | 37,146 |
| Variants | 44,900 |
| Lesson units (total) | 100 |
| Core curriculum units | 32 |
| Primer units (A1–B1) | 23 |
| Primer vocabulary items | 1,008 |
| Primer constructions | 278 |
| Primer dialogues | 22 |
| Lesson vocabulary items | 4,491 |
| Lesson dialogues | 215 |
| Construction bank entries | 350 |
| Assessment items | 160 (5 types × 32 units) |
| Unit exports | 128 (32 units × 4 formats) |
| Contamination hits (primer) | 0 |

---

## Pipeline

Phase 8 runs as a 6-step pipeline. Each step produces a new SQLite database (~100 MB each):

| Step | Script | Output DB | What it does |
|---|---|---|---|
| 8.1 | `fcn_phase8_1_cleanup.py` | `fcn_master_lexicon_phase8_1_clean.sqlite` | Cleans COERLL lesson HTML; deduplicates; categorizes by locale and proficiency |
| 8.2 | `fcn_phase8_2_unit_assembly.py` | `fcn_master_lexicon_phase8_2_units.sqlite` | Assembles 32 pedagogical units with themes, CEFR bands, vocab/construction priority |
| 8.3 | `fcn_phase8_3_lesson_export.py` | `fcn_master_lexicon_phase8_3_exports.sqlite` | Exports all units in 4 formats (JSON, Markdown, CSV, Printable) |
| 8.4 | `fcn_phase8_4_assessment_layer.py` | `fcn_master_lexicon_phase8_4_assessment.sqlite` | Creates 5 assessment item types per unit (160 total) |
| 8.5 | `fcn_phase8_5_product_bundles.py` | `fcn_master_lexicon_phase8_5_products.sqlite` | Organizes into 4 product bundles: app, textbook, flashcard, teacher |
| 8.6 | `fcn_phase8_6_primer_foundation_fixed.py` | `fcn_master_lexicon_phase8_6_primer.sqlite` | Filters to A1–B1 primer foundation (23 units, 1,008 vocab, 0 contamination) |

**The canonical production database is `fcn_master_lexicon_phase8_6_primer.sqlite`.**

To run the full pipeline from the `core_vocabulary/` database:
```bash
bash run_instructional_track.sh
```

---

## Key tables (Phase 8.6 database)

| Table | Rows | Description |
|---|---|---|
| `lexicon_entries` | 37,146 | Master lexicon with EHN, MSN, and Classical forms |
| `variants` | 44,900 | Orthographic and morphological variants |
| `lesson_units` | 100 | All lessons from the COERLL Nahuatlahtolli corpus |
| `lesson_vocab` | 4,491 | Vocabulary indexed to lessons |
| `lesson_dialogues` | 215 | Dialogue exchanges with speaker labels and translations |
| `construction_bank` | 350 | Grammatical constructions with patterns and explanations |
| `pedagogical_units` | 100 | Full instructional units with goals and grammar focus |
| `phase82_unit_plan` | 32 | Core 32-unit curriculum |
| `phase82_vocab_priority` | 1,334 | Vocabulary ranked by pedagogical priority |
| `primer_units` | 23 | A1–B1 foundational subset |
| `primer_vocab` | 1,008 | Primer vocabulary set |
| `primer_constructions` | 278 | Primer constructions |
| `primer_dialogues` | 22 | Primer dialogues |
| `unit_assessment_manifest` | 160 | Assessment items |
| `unit_export_manifest` | 128 | Export tracking |

---

## Reports and exports

```
phase8_1_reports/        Lesson cleanup CSVs (canonical lessons, duplicates, noise)
phase8_2_reports/        Unit plan, vocab priority, construction priority, dialogue samples
phase8_3_reports/
  unit_exports/
    csv/                 Vocab CSV for each of 32 units
    json/                Full structured unit data (JSON)
    markdown/            Human-readable unit documents
    printable/           Student/teacher packets
phase8_4_reports/        Assessment item summary
phase8_5_reports/
  app_bundle/            App implementation manifests
  textbook_bundle/       Markdown chapters
  flashcard_bundle/      Spaced-repetition CSV decks
  teacher_bundle/        Teacher-facing materials
phase8_6_reports/        Primer summary JSON, primer_units.csv, contamination_hits.csv
```

---

## Relationship to other phases

- **Input:** `../core_vocabulary/fcn_master_lexicon_phase7_review.sqlite` as lexical foundation; COERLL Nahuatlahtolli HTML as instructional source
- **Output feeds:** `../poetic_register/`, `../register_conversion/`, `../editorial_qa/`, and `../reference_manuals/` all draw vocabulary, constructions, and examples from this database
- **Reference manuals note:** The deliverables in `../reference_manuals/` are editorial documents built on top of this database. See `../reference_manuals/README.md`.

---

## Source material

The lesson corpus comes from **COERLL Nahuatlahtolli** (`coerll_nahuatl_materials.html`) — an open educational resource for Huasteca Nahuatl. The lexicon integrates Siméon 1885, Kaikki/Wiktionary, and UD treebank data assembled in Phases 5–7.
