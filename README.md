# Nahuatl Dictionary Project

**The first machine-readable dataset of Classical Nahuatl — 28,709 dictionary entries, 8,465 Wiktionary lexical rows, two parsed treebanks, and a growing classical example bank. Open and free.**

---

## What This Is

A structured, machine-readable collection of Classical and Modern Nahuatl language data, built from the major historical and contemporary sources:

- **Rémi Siméon's *Dictionnaire de la langue nahuatl ou mexicaine*** (1885) — 28,709 parsed entries with definitions, parts of speech, and root morphology. Siméon compiled his dictionary from Fray Alonso de Molina's *Vocabulario* (1571), Sahagún's *Florentine Codex*, and other colonial-era manuscripts recorded directly from native speakers.
- **English Wiktionary** (via Wiktextract/Kaikki) — 8,465 lexical rows spanning Classical Nahuatl, Central Nahuatl, Central Huasteca, and Eastern Huasteca varieties.
- **Universal Dependencies treebanks** — 2,169 sentences and 19,549 tokens of grammatically annotated modern Nahuatl (Western Sierra Puebla and Highland Puebla).
- **Molina's *Vocabulario en lengua castellana y mexicana*** (1571) — Raw OCR text, awaiting structured parsing (~23,000 potential additional entries).

All source material is **public domain** or **CC BY-SA**. The parsed data is released under **CC BY-SA 4.0**.

## Why This Exists

There are 1.7 million speakers of Nahuatl varieties alive today — the most widely spoken indigenous language family in North America. Until now, the major historical dictionaries have been locked inside scanned page images and physical books, inaccessible to the communities who actually speak the language.

Classical Nahuatl is the shared root of every modern variety, the language of the surviving poetry and philosophy, and the natural foundation for a living literary standard. This project makes that foundation available to anyone with a computer.

## Repository Structure

```
├── README.md                    # This file
├── simeon_parsed.json           # Full parsed Siméon dictionary (28,709 entries)
├── simeon_wordlist.txt          # Plain headword list (26,806 words)
├── simeon_1885_ocr_raw.txt      # Raw OCR of Siméon 1885
├── simeon_parser.py             # Parser — reproduce or improve the extraction
├── download_all_nahuatl.py      # Source downloader script
│
├── fcn_ingest/                  # FCN source parser pipeline
│   ├── fcn_source_parsers.py    # Multi-source parser (Wiktionary, UD, IA, Nahuatlahtolli)
│   ├── fcn_legal_ingest.py      # Source downloader with provenance tracking
│   ├── fcn_sources_demo.json    # Demo configuration for ingest pipeline
│   ├── FCN_SOURCE_PARSERS_README.md  # Parser documentation
│   ├── README_SOURCES.txt       # Source provenance memo
│   │
│   │  # Wiktionary source files
│   ├── nahuatl_kaikki_unified.json   # Unified Wiktionary data (all varieties)
│   ├── nahuatl_kaikki_raw.jsonl      # Raw Wiktionary extract
│   ├── kaikki_nci.jsonl         # Classical Nahuatl (Wiktionary)
│   ├── kaikki_nhn.jsonl         # Central Nahuatl (Wiktionary)
│   ├── kaikki_nch.jsonl         # Central Huasteca Nahuatl (Wiktionary)
│   ├── kaikki_nhe.jsonl         # Eastern Huasteca Nahuatl (Wiktionary)
│   │
│   │  # Siméon source files (pipeline copies)
│   ├── simeon_parsed.json
│   ├── simeon_1885_ocr_raw.txt
│   ├── simeon_parser.py
│   ├── simeon_wordlist.txt
│   │
│   │  # Parsed outputs
│   ├── out_kaikki/              # Wiktionary → FCN lexical rows
│   │   ├── fcn_lexical_rows.csv       # 8,465 rows (3.1 MB)
│   │   ├── fcn_lexical_rows.jsonl     # Same data, JSONL format (6.9 MB)
│   │   └── summary.json
│   │
│   ├── out_classical/           # Siméon → classical example bank
│   │   ├── classical_blocks.jsonl     # 60,663 text blocks (16.4 MB)
│   │   ├── classical_examples.jsonl   # 55,904 examples (11.6 MB)
│   │   ├── headword_candidates.csv    # 63 candidates (2.9 KB)
│   │   └── summary.json
│   │
│   ├── out_ud/                  # UD treebanks → grammar evidence tables
│   │   ├── sentences.jsonl            # 2,169 sentences (1.0 MB)
│   │   ├── tokens.csv                 # 19,549 tokens
│   │   ├── lemma_feature_counts.csv   # Lemma × feature matrix (182.4 KB)
│   │   ├── dependency_counts.csv      # Dependency relation counts (9.6 KB)
│   │   ├── feature_counts.csv         # Grammatical feature counts (2.7 KB)
│   │   ├── grammar_evidence_examples.jsonl  # Example sentences per pattern (18.5 KB)
│   │   └── summary.json
│   │
│   └── data/                    # Raw ingested sources with provenance
│       ├── ledger/
│       │   └── provenance.csv         # Legal provenance ledger for all sources
│       ├── wikimedia/
│       │   └── enwiktionary-pages-articles/
│       │       └── enwiktionary-latest-pages-articles.xml.bz2  # Full Wiktionary dump
│       ├── internet_archive/
│       │   └── vocabularioenlen00moli_0/
│       │       └── metadata.json      # Molina 1571 archive metadata
│       └── github/
│           ├── ud-western-sierra-puebla/
│           │   └── nhi_itml-ud-test.conllu   # Western Sierra Puebla treebank
│           ├── ud-western-sierra-puebla-readme/
│           │   └── README.md
│           └── ud-highland-puebla/
│               └── azz_itml-ud-test.conllu   # Highland Puebla treebank
│
└── msn_word_inventory/          # Modern Standard Nahuatl word inventory workspace
    ├── nahuatl_kaikki_unified.json
    ├── nahuatl_kaikki_raw.jsonl
    ├── kaikki_nci.jsonl
    ├── kaikki_nch.jsonl
    ├── kaikki_nhe.jsonl
    ├── kaikki_nhn.jsonl
    ├── README_SOURCES.txt
    ├── simeon_parsed.json
    ├── simeon_1885_ocr_raw.txt
    ├── simeon_parser.py
    └── simeon_wordlist.txt
```

## S3 Hosting

All files are publicly hosted on Amazon S3. The base URL is:

```
https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/
```

### Core Data Files

| File | Size | Link |
|------|------|------|
| `simeon_parsed.json` | 6.2 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/simeon_parsed.json) |
| `simeon_1885_ocr_raw.txt` | 3.2 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/simeon_1885_ocr_raw.txt) |
| `simeon_wordlist.txt` | 359.6 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/simeon_wordlist.txt) |
| `simeon_parser.py` | 13.2 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/simeon_parser.py) |
| `download_all_nahuatl.py` | 14.2 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/download_all_nahuatl.py) |

### Wiktionary / Kaikki Data

| File | Size | Link |
|------|------|------|
| `nahuatl_kaikki_unified.json` | 3.9 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/nahuatl_kaikki_unified.json) |
| `nahuatl_kaikki_raw.jsonl` | 9.3 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/nahuatl_kaikki_raw.jsonl) |
| `kaikki_nci.jsonl` (Classical) | 6.2 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/kaikki_nci.jsonl) |
| `kaikki_nhn.jsonl` (Central) | 1.6 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/kaikki_nhn.jsonl) |
| `kaikki_nch.jsonl` (Central Huasteca) | 601.5 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/kaikki_nch.jsonl) |
| `kaikki_nhe.jsonl` (Eastern Huasteca) | 484.4 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/kaikki_nhe.jsonl) |
| `enwiktionary-latest-pages-articles.xml.bz2` (full dump) | ~1.5 GB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/data/wikimedia/enwiktionary-pages-articles/enwiktionary-latest-pages-articles.xml.bz2) |

> The Wiktionary dump is also available directly from [Wikimedia](https://dumps.wikimedia.org/enwiktionary/latest/).

### Parsed Outputs

| File | Size | Link |
|------|------|------|
| `out_kaikki/fcn_lexical_rows.csv` | 3.1 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_kaikki/fcn_lexical_rows.csv) |
| `out_kaikki/fcn_lexical_rows.jsonl` | 6.9 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_kaikki/fcn_lexical_rows.jsonl) |
| `out_classical/classical_blocks.jsonl` | 16.4 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_classical/classical_blocks.jsonl) |
| `out_classical/classical_examples.jsonl` | 11.6 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_classical/classical_examples.jsonl) |
| `out_classical/headword_candidates.csv` | 2.9 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_classical/headword_candidates.csv) |
| `out_ud/sentences.jsonl` | 1.0 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_ud/sentences.jsonl) |
| `out_ud/tokens.csv` | — | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_ud/tokens.csv) |
| `out_ud/lemma_feature_counts.csv` | 182.4 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_ud/lemma_feature_counts.csv) |
| `out_ud/dependency_counts.csv` | 9.6 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_ud/dependency_counts.csv) |
| `out_ud/feature_counts.csv` | 2.7 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_ud/feature_counts.csv) |
| `out_ud/grammar_evidence_examples.jsonl` | 18.5 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/out_ud/grammar_evidence_examples.jsonl) |

### Universal Dependencies Treebanks

| File | Size | Link |
|------|------|------|
| `nhi_itml-ud-test.conllu` (Western Sierra Puebla) | 1.3 MB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/data/github/ud-western-sierra-puebla/nhi_itml-ud-test.conllu) |
| `azz_itml-ud-test.conllu` (Highland Puebla) | — | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/data/github/ud-highland-puebla/azz_itml-ud-test.conllu) |

### FCN Pipeline Scripts

| File | Size | Link |
|------|------|------|
| `fcn_source_parsers.py` | 39.1 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/fcn_source_parsers.py) |
| `fcn_legal_ingest.py` | 10.6 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/fcn_legal_ingest.py) |
| `FCN_SOURCE_PARSERS_README.md` | 2.2 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/FCN_SOURCE_PARSERS_README.md) |
| `README_SOURCES.txt` | 2.2 KB | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/README_SOURCES.txt) |
| `provenance.csv` | — | [Download](https://nahuatl-language.s3.us-east-1.amazonaws.com/molina/fcn_ingest/data/ledger/provenance.csv) |

## Data at a Glance

### Siméon Dictionary

| | Count |
|---|------:|
| Total entries | 28,709 |
| Unique headwords | 26,806 |
| Nouns (including derived) | 9,765 |
| Verbs | 5,888 |
| Adjectives (including derived) | 3,355 |
| Adverbs | 917 |
| Entries with root morphology | 19,150 |
| Entries with conjugation patterns | 3,885 |

### Wiktionary (Kaikki)

| Variety | Rows |
|---|------:|
| Classical Nahuatl | 5,132 |
| Central Nahuatl | 1,855 |
| Central Huasteca Nahuatl | 795 |
| Eastern Huasteca Nahuatl | 683 |
| **Total** | **8,465** |

### Universal Dependencies

| | Count |
|---|------:|
| Sentences | 2,169 |
| Tokens | 19,549 |
| Unique grammatical features | 61 |

### Classical Example Bank

| | Count |
|---|------:|
| Text blocks | 60,663 |
| Extracted examples | 55,904 |
| Headword candidates | 63 |

## Entry Format (Siméon)

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
- **pos** — Part of speech (noun, verb, adjective, adverb, etc.)
- **roots** — Morphological roots as identified by Siméon
- **alternates** — Variant spellings, when present
- **calendar** — Tonalpohualli information, when present

## Quick Start

```python
import json

with open("simeon_parsed.json") as f:
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

## FCN Source Parsers

The `fcn_ingest/` pipeline converts raw sources into structured, FCN-ready data with full provenance tracking. Supported sources:

- **Wiktionary** (Kaikki/Wiktextract JSON, JSONL, or raw XML dumps) → lexical rows
- **Universal Dependencies** (CoNLL-U) → grammar evidence tables
- **Internet Archive** (OCR text, PDFs, parsed JSON) → classical example bank
- **Nahuatlahtolli** (HTML lessons) → modern Huasteca grammar/example bank

See [`fcn_ingest/FCN_SOURCE_PARSERS_README.md`](fcn_ingest/FCN_SOURCE_PARSERS_README.md) for usage details.

## Limitations

**Siméon definitions are in French.** Translating to English and Spanish is on the roadmap.

**OCR source material.** The Siméon and Molina texts were auto-OCR'd from 19th-century scans hosted on archive.org. They contain errors — garbled characters, misread letters, broken line joins. Use with judgment. Corrections are welcome as pull requests.

**Colonial orthography.** Headwords use 16th/17th-century spelling. No macrons (vowel length), no glottal stops. For phonological detail, cross-reference with Karttunen's *Analytical Dictionary of Nahuatl*.

## Sources

| Source | Date | License |
|--------|------|---------|
| Rémi Siméon, *Dictionnaire de la langue nahuatl ou mexicaine* | 1885 | Public domain |
| Alonso de Molina, *Vocabulario en lengua castellana y mexicana* | 1571 | Public domain |
| Bernardino de Sahagún, *Florentine Codex* | 1577 | Public domain |
| English Wiktionary (via Wiktextract/Kaikki) | 2026 | CC BY-SA 3.0 / GFDL |
| UD Western Sierra Puebla Nahuatl (ITML) | 2026 | See treebank license |
| UD Highland Puebla Nahuatl (ITML) | 2026 | See treebank license |

OCR sources: [Siméon on archive.org](https://archive.org/details/dictionnairedela00sime) · [Molina on archive.org](https://archive.org/details/vocabulariodela00platgoog)

## Citation

```
Sam Itzli, "Nahuatl Dictionary Project," GitHub, 2026.
https://github.com/samvillasmith/nahuatl-dictionary

Parsed from: Rémi Siméon, Dictionnaire de la langue nahuatl ou mexicaine,
Paris: Imprimerie Nationale, 1885.
```

## Roadmap

- [ ] Searchable dictionary website
- [ ] English translations of definitions
- [ ] Spanish translations of definitions
- [ ] Orthographic normalization to modern conventions
- [ ] Vowel length and glottal stop annotation (via Karttunen cross-reference)
- [ ] OCR error corrections
- [ ] Parse Molina's 1571 *Vocabulario* directly (~23,000 additional entries)
- [ ] Integrate Nahuatlahtolli modern grammar examples
- [ ] Cross-variety lemma alignment (Classical ↔ Central ↔ Huasteca)

## License

The parsed data in this repository is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The source material is public domain. Wiktionary-derived data inherits CC BY-SA 3.0 / GFDL.
>>>>>>> a6244d3 (added governance documents)
