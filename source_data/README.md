# source_data/ — Raw Sources and Ingest Pipeline

This directory contains all raw source data and the scripts that parse it into FCN-ready formats. Everything downstream in the pipeline depends on what this directory produces.

## What lives here

### Raw source data

| File | Size | Description |
|---|---|---|
| `simeon_parsed.json` | 6.5 MB | 28,709 parsed Siméon 1885 entries |
| `simeon_1885_ocr_raw.txt` | 3.4 MB | Raw OCR of Siméon dictionary |
| `simeon_wordlist.txt` | 368 KB | Plain headword list |
| `nahuatl_kaikki_unified.json` | 4.1 MB | Unified Wiktionary/Kaikki data |
| `nahuatl_kaikki_raw.jsonl` | 9.7 MB | Raw Kaikki extract |
| `kaikki_nci.jsonl` | 6.5 MB | Classical Nahuatl (5,132 rows) |
| `kaikki_nhn.jsonl` | 1.7 MB | Central Nahuatl (1,855 rows) |
| `kaikki_nch.jsonl` | 616 KB | Central Huasteca Nahuatl (795 rows) |
| `kaikki_nhe.jsonl` | 496 KB | Eastern Huasteca Nahuatl (683 rows) |

### Parser and downloader scripts

| File | Description |
|---|---|
| `fcn_source_parsers.py` | Multi-source parser: Wiktionary/Kaikki, UD treebanks, Internet Archive OCR, COERLL HTML → FCN tables |
| `fcn_legal_ingest.py` | Source downloader with provenance tracking |
| `simeon_parser.py` | Siméon 1885 dictionary parser |
| `download_all_nahuatl.py` | Multi-source downloader (Siméon, Kaikki, UD, COERLL) |

### Processed outputs

| Directory | Contents |
|---|---|
| `out_kaikki/` | `fcn_lexical_rows.jsonl` (7.2 MB), `fcn_lexical_rows.csv` (3.2 MB) |
| `out_classical/` | `classical_blocks.jsonl` (17.2 MB), `classical_examples.jsonl` (12.2 MB) |
| `out_ud/` | `sentences.jsonl`, `tokens.csv`, `lemma_feature_counts.csv`, `grammar_evidence_examples.jsonl` |

### Treebank data

| File | Description |
|---|---|
| `data/github/ud-western-sierra-puebla/nhi_itml-ud-test.conllu` | Western Sierra Puebla Nahuatl UD treebank (1.3 MB) |
| `data/github/ud-highland-puebla/azz_itml-ud-test.conllu` | Highland Puebla Nahuatl UD treebank (1.1 MB) |

---

## Running the pipeline

To download all sources:
```bash
python download_all_nahuatl.py
```

To parse Siméon:
```bash
python simeon_parser.py
```

To run the full FCN ingest pipeline:
```bash
python fcn_source_parsers.py
```

See `FCN_SOURCE_PARSERS_README.md` and `README_SOURCES.txt` for full usage details.

---

## Notes

- The root-level `simeon_parsed.json`, `simeon_1885_ocr_raw.txt`, `simeon_parser.py`, and `simeon_wordlist.txt` are copies of the canonical versions here, kept at root for S3 public download compatibility.
- `data/ledger/provenance.csv` tracks the legal status and retrieval dates of all source material.
- Next step: `../lexicon_bootstrap/` imports these outputs into the first unified SQLite.
