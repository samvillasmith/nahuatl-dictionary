# Nahuatl Dictionary Project

**The first machine-readable dataset of Classical Nahuatl — 28,709 entries, open and free.**

---

## What This Is

28,709 structured dictionary entries of Classical Nahuatl, parsed from Rémi Siméon's *Dictionnaire de la langue nahuatl ou mexicaine* (1885). Siméon compiled his dictionary from Fray Alonso de Molina's *Vocabulario* (1571), Sahagún's *Florentine Codex*, and other colonial-era manuscripts — the primary sources of the Nahuatl language as recorded directly from native speakers in the 16th and 17th centuries.

The source material is **public domain** (published 1885). The parsed data is released under **CC BY-SA 4.0**.

This is the largest open, machine-readable Classical Nahuatl dataset in existence.

## Why This Exists

There are 1.7 million speakers of Nahuatl varieties alive today — the most widely spoken indigenous language family in North America. Until now, the major historical dictionaries have been locked inside scanned page images and physical books, inaccessible to the communities who actually speak the language.

Classical Nahuatl is the shared root of every modern variety, the language of the surviving poetry and philosophy, and the natural foundation for a living literary standard. This project makes that foundation available to anyone with a computer.

## Data

| File | Description | Entries |
|------|-------------|---------|
| `simeon_parsed.json` | Full parsed dictionary with definitions, parts of speech, and root morphology | 28,709 |
| `simeon_wordlist.txt` | Plain headword list, one word per line | 26,806 |
| `amoxtli_glossary.json` | Curated philosophical and theological glossary with English definitions and pronunciation | 44 |
| `simeon_parser.py` | The parser itself — reproduce or improve the extraction |

## Entry Format

```json
{
  "headword": "TONALLI",
  "definition_fr": "Ardeur, chaleur du soleil, été; au fig. âme, esprit, signe de nativité; ration, part, portion, ce qui est destiné à quelqu'un...",
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

## Stats

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

## Limitations

**Definitions are in French.** Translating to English and Spanish is on the roadmap.

**This is OCR.** The source text was auto-OCR'd from a 19th-century scan hosted on archive.org. It contains errors — garbled characters, misread letters, broken line joins. Use with judgment. Corrections are welcome as pull requests.

**Colonial orthography.** Headwords use 16th/17th-century spelling. No macrons (vowel length), no glottal stops. For phonological detail, cross-reference with Karttunen's *Analytical Dictionary of Nahuatl*.

## Sources

| Source | Date | License |
|--------|------|---------|
| Rémi Siméon, *Dictionnaire de la langue nahuatl ou mexicaine* | 1885 | Public domain |
| Alonso de Molina, *Vocabulario en lengua castellana y mexicana* | 1571 | Public domain |
| Bernardino de Sahagún, *Florentine Codex* | 1577 | Public domain |

OCR source file: [archive.org/details/dictionnairedela00sime](https://archive.org/details/dictionnairedela00sime)

## Citation

```
Sam Itzli, "Nahuatl Dictionary Project," GitHub, 2026.
https://github.com/[username]/nahuatl-dictionary

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
- [ ] Parse Molina's 1571 *Vocabulario* directly (23,000+ additional entries)

## License

The parsed data in this repository is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The source material is public domain.
