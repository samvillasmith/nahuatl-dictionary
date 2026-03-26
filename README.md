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
├── simeon_parsed.json          # Full parsed Siméon dictionary (28,709 entries)
├── simeon_wordlist.txt          # Plain headword list (26,806 words)
├── simeon_parser.py             # Parser — reproduce or improve the extraction
├── amoxtli_glossary.json        # Curated philosophical/theological glossary (44 entries)
│
├── fcn_ingest/                  # FCN source parser pipeline
│   ├── fcn_source_parsers.py    # Multi-source parser (Wiktionary, UD, IA, Nahuatlahtolli)
│   ├── fcn_legal_ingest.py      # Source downloader with provenance tracking
│   ├── out_kaikki/              # Parsed Wiktionary lexical rows (8,465 rows)
│   ├── out_ud/                  # Parsed UD grammar evidence tables
│   ├── out_classical/           # Classical example bank (55,904 examples)
│   └── data/ledger/             # Provenance ledger for all ingested sources
│
└── msn_word_inventory/          # Modern Standard Nahuatl word inventory workspace
```

## Large Files (S3)

Some source files exceed GitHub's 100 MB limit and are hosted publicly on S3:

| File | Size | Link |
|------|------|------|
| `enwiktionary-latest-pages-articles.xml.bz2` | ~1.5 GB | [Download from S3](https://YOUR-BUCKET-NAME.s3.amazonaws.com/enwiktionary-latest-pages-articles.xml.bz2) |
| `molina_1571_ocr_raw.txt` | — | [Download from S3](https://YOUR-BUCKET-NAME.s3.amazonaws.com/molina_1571_ocr_raw.txt) |
| `simeon_1885_ocr_raw.txt` | — | [Download from S3](https://YOUR-BUCKET-NAME.s3.amazonaws.com/simeon_1885_ocr_raw.txt) |

> **Note:** Replace the S3 links above with your actual bucket URLs. The Wiktionary dump is also available directly from [Wikimedia](https://dumps.wikimedia.org/enwiktionary/latest/).

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
