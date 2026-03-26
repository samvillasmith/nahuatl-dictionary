MSN WORD INVENTORY — SOURCE DOCUMENTATION
==========================================
For Sam Itzli / The Amoxtli Project / Modern Standard Nahuatl

LEGAL STATUS OF ALL FILES IN THIS DIRECTORY
--------------------------------------------

1. nahuatl_kaikki_raw.jsonl / nahuatl_kaikki_unified.json / kaikki_*.jsonl
   Source: kaikki.org (extraction of English Wiktionary)
   License: CC BY-SA 3.0 / GFDL
   You may use, modify, and redistribute with attribution.
   Citation: Tatu Ylonen, "Wiktextract: Wiktionary as Machine-Readable
   Structured Data," LREC 2022, pp. 1317-1325.

2. molina_1571_ocr_raw.txt
   Source: Alonso de Molina, "Vocabulario en lengua castellana y mexicana" (1571)
   Reprint: Julius Platzmann, Leipzig: B.G. Teubner, 1880
   Scanned by: Google Books / Harvard University Library
   Hosted at: archive.org/details/vocabulariodela00platgoog
   License: PUBLIC DOMAIN (published 1571)
   This is auto-generated OCR text. It contains errors.

3. simeon_1885_ocr_raw.txt
   Source: Rémi Siméon, "Dictionnaire de la langue nahuatl ou mexicaine" (1885)
   Hosted at: archive.org/details/dictionnairedela00sime
   License: PUBLIC DOMAIN (published 1885)
   This is auto-generated OCR text. It contains errors. Text is in French.

WHAT TO DO WITH THE OCR FILES
------------------------------
The Molina and Siméon OCR files are RAW. They are not clean datasets.
They contain:
  - OCR errors (misread characters, garbled text)
  - Page headers, footers, and numbers mixed into the text
  - Colonial Spanish orthography (different from modern Spanish)
  - 16th-century Nahuatl orthography (no macrons, no glottal stops)

To turn this into a proper machine-readable dictionary, you would need to:
  1. Clean the OCR errors (semi-automated with manual review)
  2. Parse the dictionary structure (headword, definition, examples)
  3. Normalize the orthography to modern conventions
  4. Cross-reference with Karttunen for vowel length and glottal stops

This is a significant project. But if completed, it would be the largest
open Nahuatl dataset in existence. ~23,000 entries from Molina alone.

Ni cuicani, ni tlahtoani.
The library has to exist before anyone can walk into it.
