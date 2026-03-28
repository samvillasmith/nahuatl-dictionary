# FCN Source Parsers

`fcn_source_parsers.py` is the second-stage parser companion to `fcn_legal_ingest.py`.
It converts downloaded or local source files into FCN-ready rows/tables while preserving provenance.

## Subcommands

### 1. Wiktionary -> FCN lexical rows
Supports:
- Kaikki/Wiktextract unified JSON (`nahuatl_kaikki_unified.json` style)
- Wiktextract JSONL
- Raw Wiktionary XML dumps (`.xml` / `.bz2`) via best-effort parsing

Outputs:
- `fcn_lexical_rows.jsonl`
- `fcn_lexical_rows.csv`
- `summary.json`

Example:
```bash
python fcn_source_parsers.py wiktionary-to-fcn \
  --input nahuatl_kaikki_unified.json \
  --out out_kaikki
```

### 2. UD CoNLL-U -> grammar evidence tables
Outputs:
- `sentences.jsonl`
- `tokens.csv`
- `feature_counts.csv`
- `lemma_feature_counts.csv`
- `dependency_counts.csv`
- `grammar_evidence_examples.jsonl`
- `summary.json`

Example:
```bash
python fcn_source_parsers.py ud-to-grammar \
  --input treebank.conllu \
  --out out_ud
```

### 3. Internet Archive OCR/PDF -> classical example bank
Supports:
- `.txt` OCR files
- `.pdf` files (via `pypdf`)
- parsed `.json` files with an `entries` array (for convenience)

Outputs:
- `classical_blocks.jsonl`
- `classical_examples.jsonl`
- `headword_candidates.csv`
- `summary.json`

Example:
```bash
python fcn_source_parsers.py ia-to-classical-bank \
  --input simeon_1885_ocr_raw.txt simeon_parsed.json \
  --out out_classical
```

### 4. Nahuatlahtolli HTML -> modern Huasteca grammar/example bank
Supports:
- local HTML files
- lesson URLs

Outputs:
- `lessons_index.csv`
- `lesson_blocks.jsonl`
- `grammar_example_bank.jsonl`
- `summary.json`

Example:
```bash
python fcn_source_parsers.py nahuatlahtolli-to-bank \
  --input lesson.html \
  --out out_lesson
```

## Known caveats

- Raw Wiktionary XML parsing is **best effort**. Prefer structured Kaikki/Wiktextract data whenever possible.
- OCR/PDF example extraction is a **candidate bank**, not a fully cleaned scholarly edition.
- Nahuatlahtolli HTML parsing is intentionally conservative and keeps blocks with provenance; you should still curate the resulting grammar/example bank.
- The script avoids automatic irreversible normalization. It emits evidence tables and candidate rows for later FCN review.
