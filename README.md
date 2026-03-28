# Flor y Canto Nahuatl (FCN)

The first machine-readable Nahuatl language infrastructure: a 37,000-entry lexicon, a complete CEFR A1–B1 instructional curriculum, a multi-register orthographic standard, and four production-ready reference manuals — all built from primary historical and contemporary sources and released open.

---

## Scale at a glance

| Resource | Count |
|---|---|
| Siméon 1885 parsed entries | 28,709 |
| Wiktionary/Kaikki lexical rows | 8,465 (4 varieties) |
| UD treebank sentences | 2,169 |
| UD treebank tokens | 19,549 |
| Classical example bank (text blocks) | 60,663 |
| **Master lexicon entries** | **37,146** |
| **Lexicon variants** | **44,900** |
| Lesson units | 100 |
| Core curriculum units | 32 |
| Primer vocabulary items (A1–B1) | 1,008 |
| Primer constructions | 278 |
| Unit exports (4 formats × 32 units) | 128 files |
| Assessment items | 160 |

---

## What this is

**Flor y Canto Nahuatl** treats Nahuatl as a teachable, writable, publishable living language — not a museum artifact. It builds three distinct production registers with their own orthographic standards, pedagogical materials, and governance rules:

| Register | Label | Description |
|---|---|---|
| Spoken standard | EHN | Eastern Huasteca Nahuatl — spoken-first, primer foundation |
| Written standard | MSN neutral | Modern written norm — education and publishing |
| Literary elevated | MSN-P | Elevated literary register — song, ceremony, public address |

Nahuatl is spoken by approximately 1.7 million people today — the most widely spoken indigenous language family in North America. The major historical dictionaries have been locked inside scanned page images and physical books. This project makes that foundation machine-readable, register-distinguished, and source-tracked.

---

## Project pipeline

```
fcn_ingest/    Parse raw sources → lexical rows, classical examples, UD grammar evidence
    ↓
phase5/        Import and unify → first master lexicon SQLite
    ↓
phase6/        Normalize orthography → FCN conventions (k/s/w/ts/h/macrons)
    ↓
phase7/        Curate core vocabulary → core_ehn_250, core_ehn_500, example bank
    ↓
phase8/        Instructional pipeline → 37K-entry database, 32 units, 1,008 primer items
    ↓
phase9/        Poetic inventory → 21-item MSN-P seed (diction, vocatives, formulas)
phase10/       Register conversion → rules and examples for all 4 conversion directions
phase11/       Editorial QA → 6-level QA scale, validation status taxonomy
    ↓
phase12/       Final products → 4 reference manuals (D15–D18)
```

**The production database is `phase8/fcn_master_lexicon_phase8_6_primer.sqlite`.**

---

## Directory guide

| Directory | What it contains |
|---|---|
| `fcn_ingest/` | Source parser pipeline: Kaikki, UD, Siméon, COERLL; raw data; processed outputs |
| `phase5/` | Master lexicon bootstrap: first unified SQLite from all sources |
| `phase6/` | Orthographic normalization: FCN conventions, style manual |
| `phase7/` | Core vocabulary curation: 250/500-item lists, verb list, example bank |
| `phase8/` | **Main database and curriculum** (37K entries, 100 lessons, 128 unit exports) |
| `phase9/` | Poetic register inventory: elevated diction, vocatives, refrain particles, formulas |
| `phase10/` | Register conversion guide: EHN↔MSN↔MSN-P↔Classical rules and examples |
| `phase11/` | Editorial QA and validation: QA-0 through QA-5 scale, publication blockers |
| `phase12/` | Reference manuals: Spoken Primer (D15), MSN Manual (D16), Poetic Manual (D17), Dictionary Manual (D18) |
| `master_source_book/` | Deliverable 14: Master Sourcebook compiling all project principles |
| `docs/` | Founding charter, register charter, mission statements, internal premises |
| `msn_word_inventory/` | Workspace copy of Kaikki and Siméon data (canonical in `fcn_ingest/`) |

### Root-level data files

The Siméon files at the root (`simeon_parsed.json`, `simeon_1885_ocr_raw.txt`, `simeon_parser.py`, `simeon_wordlist.txt`) are copies of the canonical versions in `fcn_ingest/`. The `fcn_ingest/` versions are authoritative.

---

## Phase 12 manuals — important note

The files in `phase12/` are **editorial reference documents**. They are not the production data. They document the schema, pedagogy, and register conventions that govern the database in `phase8/`. See `phase12/README.md` for the full explanation of what each document is and where the underlying data lives.

---

## Sources

| Source | Date | License |
|---|---|---|
| Rémi Siméon, *Dictionnaire de la langue nahuatl ou mexicaine* | 1885 | Public domain |
| Alonso de Molina, *Vocabulario en lengua castellana y mexicana* | 1571 | Public domain |
| Bernardino de Sahagún, *Florentine Codex* | 1577 | Public domain |
| English Wiktionary (via Wiktextract/Kaikki) | 2026 | CC BY-SA 3.0 / GFDL |
| COERLL Nāhuatlahtolli course | 2026 | Open educational resource |
| UD Western Sierra Puebla Nahuatl (ITML) | 2026 | See treebank license |
| UD Highland Puebla Nahuatl (ITML) | 2026 | See treebank license |

OCR sources: [Siméon on archive.org](https://archive.org/details/dictionnairedela00sime) · [Molina on archive.org](https://archive.org/details/vocabulariodela00platgoog)

---

## Quick start — lexicon data

```python
import json

with open("fcn_ingest/simeon_parsed.json") as f:
    data = json.load(f)

# Search for a word
for entry in data["entries"]:
    if entry["headword"] == "XOCHITL":
        print(entry)
        break

# Find every word built from a root
cuica_words = [e for e in data["entries"] if "cuica" in e.get("roots", [])]
for e in cuica_words:
    print(f"  {e['headword']}: {e['definition_fr'][:80]}")
```

## Quick start — production database

```python
import sqlite3

conn = sqlite3.connect("phase8/fcn_master_lexicon_phase8_6_primer.sqlite")
cur = conn.cursor()

# How many entries?
cur.execute("SELECT COUNT(*) FROM lexicon_entries")
print(cur.fetchone())  # (37146,)

# Browse primer vocabulary
cur.execute("SELECT surface_form, gloss_en, part_of_speech FROM primer_vocab LIMIT 20")
for row in cur.fetchall():
    print(row)

# Get a full unit export
cur.execute("SELECT lesson_number, theme_en, target_band FROM phase82_unit_plan ORDER BY lesson_number")
for row in cur.fetchall():
    print(row)
```

---

## Siméon entry format

```json
{
  "headword": "TONALLI",
  "definition_fr": "Ardeur, chaleur du soleil, été; au fig. âme, esprit, signe de nativité...",
  "pos": "noun",
  "roots": ["tona"]
}
```

- **headword** — Nahuatl word (colonial orthography)
- **definition_fr** — Definition in French (Siméon's original language)
- **pos** — Part of speech
- **roots** — Morphological roots as identified by Siméon

---

## FCN orthographic conventions

FCN uses a consistent modern orthography distinct from colonial spelling conventions:

| Feature | FCN convention | Classical variant |
|---|---|---|
| Velar stop | k | c / qu |
| Sibilant | s | z / ç |
| Labio-velar | w | hu / uh |
| Affricate | ts | tz |
| Saltillo / glottal | h | h / ʼ / unmarked |
| Vowel length | macron (ā ē ī ō) | unmarked |

---

## Data breakdown

### Siméon Dictionary

| | Count |
|---|---|
| Total entries | 28,709 |
| Unique headwords | 26,806 |
| Nouns (including derived) | 9,765 |
| Verbs | 5,888 |
| Adjectives (including derived) | 3,355 |
| Adverbs | 917 |
| Entries with root morphology | 19,150 |

### Wiktionary (Kaikki)

| Variety | Rows |
|---|---|
| Classical Nahuatl (nci) | 5,132 |
| Central Nahuatl (nhn) | 1,855 |
| Central Huasteca Nahuatl (nch) | 795 |
| Eastern Huasteca Nahuatl (nhe) | 683 |
| **Total** | **8,465** |

### Universal Dependencies

| | Count |
|---|---|
| Sentences | 2,169 |
| Tokens | 19,549 |
| Unique grammatical features | 61 |

---

## S3 hosting

All files are publicly hosted on Amazon S3:

```
https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/
```

### Core data files

| File | Link |
|---|---|
| `simeon_parsed.json` (6.2 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/simeon_parsed.json) |
| `simeon_1885_ocr_raw.txt` (3.2 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/simeon_1885_ocr_raw.txt) |
| `simeon_wordlist.txt` | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/simeon_wordlist.txt) |
| `simeon_parser.py` | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/simeon_parser.py) |
| `download_all_nahuatl.py` | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/download_all_nahuatl.py) |

### Wiktionary / Kaikki data

| File | Link |
|---|---|
| `nahuatl_kaikki_unified.json` (3.9 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/nahuatl_kaikki_unified.json) |
| `nahuatl_kaikki_raw.jsonl` (9.3 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/nahuatl_kaikki_raw.jsonl) |
| `kaikki_nci.jsonl` Classical (6.2 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/kaikki_nci.jsonl) |
| `kaikki_nhn.jsonl` Central (1.6 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/kaikki_nhn.jsonl) |
| `kaikki_nch.jsonl` Central Huasteca | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/kaikki_nch.jsonl) |
| `kaikki_nhe.jsonl` Eastern Huasteca | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/kaikki_nhe.jsonl) |

### Parsed outputs

| File | Link |
|---|---|
| `out_kaikki/fcn_lexical_rows.csv` (3.1 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_kaikki/fcn_lexical_rows.csv) |
| `out_kaikki/fcn_lexical_rows.jsonl` (6.9 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_kaikki/fcn_lexical_rows.jsonl) |
| `out_classical/classical_blocks.jsonl` (16.4 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_classical/classical_blocks.jsonl) |
| `out_classical/classical_examples.jsonl` (11.6 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_classical/classical_examples.jsonl) |
| `out_ud/sentences.jsonl` (1.0 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_ud/sentences.jsonl) |
| `out_ud/tokens.csv` | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_ud/tokens.csv) |

### Universal Dependencies treebanks

| File | Link |
|---|---|
| `nhi_itml-ud-test.conllu` Western Sierra Puebla (1.3 MB) | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/data/github/ud-western-sierra-puebla/nhi_itml-ud-test.conllu) |
| `azz_itml-ud-test.conllu` Highland Puebla | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/data/github/ud-highland-puebla/azz_itml-ud-test.conllu) |

---

## Limitations

**Siméon definitions are in French.** English and Spanish translations are on the roadmap.

**OCR source material.** Siméon and Molina texts were auto-OCR'd from 19th-century scans on archive.org. They contain errors. Use with judgment; corrections are welcome as pull requests.

**Colonial orthography in source data.** Siméon headwords use 16th/17th-century spelling without macrons or glottal-stop marking. FCN orthographic normalization is applied from Phase 6 onward.

---

## Roadmap

- [ ] English translations of Siméon definitions
- [ ] Spanish translations of Siméon definitions
- [ ] Parse Molina 1571 *Vocabulario* (~23,000 additional entries)
- [ ] OCR error corrections in Siméon source
- [ ] Cross-variety lemma alignment (Classical ↔ Central ↔ Huasteca)
- [ ] Searchable dictionary website
- [ ] Publish primer-ready exports from Phase 8 instructional track
- [ ] Phase B/C expansion of MSN-P poetic inventory (phase9/)
- [ ] Community validation pipeline for proposed literary-modern items
- [ ] App and textbook bundle production from Phase 8.5 outputs

---

## License

The parsed data in this repository is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Source material is public domain. Wiktionary-derived data inherits CC BY-SA 3.0 / GFDL.

## Citation

```
Sam Itzli, "Flor y Canto Nahuatl," GitHub, 2026.
https://github.com/samvillasmith/nahuatl-dictionary

Parsed from: Rémi Siméon, Dictionnaire de la langue nahuatl ou mexicaine,
Paris: Imprimerie Nationale, 1885.
```
