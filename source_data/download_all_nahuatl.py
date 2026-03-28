#!/usr/bin/env python3
"""
MSN WORD INVENTORY DOWNLOADER
==============================
Downloads every legally-free Nahuatl word source available online.

Source 1: Kaikki.org — Wiktionary extraction (CC BY-SA 3.0)
          ~8,400 entries across 4 Nahuatl varieties

Source 2: Molina's Vocabulario (1571) — Public domain (450 years old)
          Auto-OCR text from archive.org's 1880 Platzmann reprint
          ~23,000 entries (raw OCR, needs cleaning)

Source 3: Siméon's Dictionnaire (1885) — Public domain
          Auto-OCR text from archive.org
          Thousands of entries (raw OCR, needs cleaning)

Run: python3 download_all_nahuatl.py
No dependencies beyond standard Python 3.

Output files:
  nahuatl_kaikki_raw.jsonl        — Raw kaikki.org entries (all 4 varieties)
  nahuatl_kaikki_unified.json     — Merged & deduplicated kaikki.org data
  molina_1571_ocr_raw.txt         — Raw OCR of Molina's Vocabulario
  simeon_1885_ocr_raw.txt         — Raw OCR of Siméon's Dictionnaire
  README_SOURCES.txt              — License and citation info

For Sam Itzli / The Amoxtli Project / Modern Standard Nahuatl
"""

import json
import urllib.request
import os
import sys

# ============================================================
# CONFIG
# ============================================================
OUTPUT_DIR = "msn_word_inventory"

KAIKKI_VARIETIES = {
    "Classical Nahuatl": {
        "url": "https://kaikki.org/dictionary/Classical%20Nahuatl/kaikki.org-dictionary-ClassicalNahuatl.jsonl",
        "iso": "nci",
        "region": "Valley of Mexico (colonial era literary standard)",
    },
    "Central Nahuatl": {
        "url": "https://kaikki.org/dictionary/Central%20Nahuatl/kaikki.org-dictionary-CentralNahuatl.jsonl",
        "iso": "nhn",
        "region": "Puebla, Tlaxcala, Mexico State",
    },
    "Central Huasteca Nahuatl": {
        "url": "https://kaikki.org/dictionary/Central%20Huasteca%20Nahuatl/kaikki.org-dictionary-CentralHuastecaNahuatl.jsonl",
        "iso": "nch",
        "region": "Hidalgo",
    },
    "Eastern Huasteca Nahuatl": {
        "url": "https://kaikki.org/dictionary/Eastern%20Huasteca%20Nahuatl/kaikki.org-dictionary-EasternHuastecaNahuatl.jsonl",
        "iso": "nhe",
        "region": "Veracruz (Yan Garcia's variety)",
    }
}

# Archive.org OCR text files (public domain)
ARCHIVE_ORG_SOURCES = {
    "molina_1571": {
        "url": "https://archive.org/download/vocabulariodela00platgoog/vocabulariodela00platgoog_djvu.txt",
        "filename": "molina_1571_ocr_raw.txt",
        "description": "Molina's Vocabulario en lengua castellana y mexicana (1571), 1880 Platzmann reprint",
        "license": "Public domain (published 1571, reprinted 1880)",
        "note": "This is AUTO-OCR of a 16th-century dictionary. It WILL contain errors. The colonial Spanish typeface and Nahuatl orthography are challenging for OCR. This is raw material that needs human review and cleaning to become a proper dataset. But the words are in there.",
        "entries_estimate": "~23,000 (Nahuatl->Spanish section) + ~17,600 (Spanish->Nahuatl section)"
    },
    "simeon_1885": {
        "url": "https://archive.org/download/dictionnairedela00sime/dictionnairedela00sime_djvu.txt",
        "filename": "simeon_1885_ocr_raw.txt",
        "description": "Siméon's Dictionnaire de la langue nahuatl ou mexicaine (1885)",
        "license": "Public domain (published 1885)",
        "note": "Nahuatl-French dictionary compiled from colonial manuscripts. Better typography than Molina original = potentially better OCR. But it's in French.",
        "entries_estimate": "Thousands (710 pages, double-column)"
    }
}

HEADERS = {"User-Agent": "MSN-NahuatlProject/1.0 (language-revitalization)"}


# ============================================================
# DOWNLOAD FUNCTIONS
# ============================================================

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}/")
    print()


def download_file(url, filepath, description):
    """Download a URL to a file with progress indication."""
    print(f"  Downloading: {description}")
    print(f"  URL: {url}")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            total = response.headers.get('Content-Length')
            data = b""
            block_size = 65536
            downloaded = 0
            while True:
                chunk = response.read(block_size)
                if not chunk:
                    break
                data += chunk
                downloaded += len(chunk)
                if total:
                    pct = downloaded / int(total) * 100
                    print(f"\r  Progress: {downloaded:,} bytes ({pct:.0f}%)", end="", flush=True)
                else:
                    print(f"\r  Downloaded: {downloaded:,} bytes", end="", flush=True)
            print()

        with open(filepath, "wb") as f:
            f.write(data)

        size_mb = len(data) / 1024 / 1024
        print(f"  Saved: {filepath} ({size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def download_kaikki():
    """Download all Nahuatl varieties from kaikki.org."""
    print("=" * 60)
    print("SOURCE 1: Kaikki.org (Wiktionary extraction)")
    print("License: CC BY-SA 3.0 / GFDL")
    print("=" * 60)

    all_entries = []
    for name, info in KAIKKI_VARIETIES.items():
        filepath = os.path.join(OUTPUT_DIR, f"kaikki_{info['iso']}.jsonl")
        success = download_file(info["url"], filepath, f"{name} ({info['iso']})")
        if success:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    count = 0
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                obj = json.loads(line)
                                obj["_variety"] = name
                                obj["_iso"] = info["iso"]
                                all_entries.append(obj)
                                count += 1
                            except json.JSONDecodeError:
                                pass
                print(f"  Parsed: {count} entries")
            except Exception as e:
                print(f"  Parse error: {e}")
        print()

    # Save combined raw JSONL
    raw_path = os.path.join(OUTPUT_DIR, "nahuatl_kaikki_raw.jsonl")
    with open(raw_path, "w", encoding="utf-8") as f:
        for entry in all_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Combined kaikki.org raw data: {raw_path} ({len(all_entries)} entries)")

    # Build unified dictionary
    unified = {}
    for entry in all_entries:
        word = entry.get("word", "")
        if not word:
            continue
        key = word.lower()
        if key not in unified:
            unified[key] = {
                "word": word,
                "varieties": [],
                "senses": [],
                "forms": [],
                "pos_tags": [],
                "etymology": None
            }
        record = unified[key]
        variety = entry.get("_variety", "unknown")
        if variety not in record["varieties"]:
            record["varieties"].append(variety)
        pos = entry.get("pos", "")
        if pos and pos not in record["pos_tags"]:
            record["pos_tags"].append(pos)
        for sense in entry.get("senses", []):
            for gloss in sense.get("glosses", []):
                sense_entry = {"gloss": gloss, "pos": pos, "variety": variety}
                if sense_entry not in record["senses"]:
                    record["senses"].append(sense_entry)
        for form in entry.get("forms", []):
            form_entry = {"form": form.get("form", ""), "tags": form.get("tags", []), "variety": variety}
            if form_entry not in record["forms"]:
                record["forms"].append(form_entry)
        if not record["etymology"] and entry.get("etymology_text"):
            record["etymology"] = entry["etymology_text"]

    unified_path = os.path.join(OUTPUT_DIR, "nahuatl_kaikki_unified.json")
    output = {
        "_metadata": {
            "source": "kaikki.org (Wiktionary extraction)",
            "license": "CC BY-SA 3.0 / GFDL",
            "citation": "Tatu Ylonen, Wiktextract: Wiktionary as Machine-Readable Structured Data, LREC 2022",
            "unique_words": len(unified),
            "total_raw_entries": len(all_entries),
        },
        "words": unified
    }
    with open(unified_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Unified kaikki.org dictionary: {unified_path} ({len(unified)} unique words)")
    print()
    return len(all_entries), len(unified)


def download_archive_org():
    """Download public domain dictionaries from archive.org."""
    print("=" * 60)
    print("SOURCE 2 & 3: Archive.org (Public Domain Dictionaries)")
    print("=" * 60)

    for key, info in ARCHIVE_ORG_SOURCES.items():
        filepath = os.path.join(OUTPUT_DIR, info["filename"])
        print()
        print(f"--- {info['description']} ---")
        print(f"License: {info['license']}")
        print(f"Estimated entries: {info['entries_estimate']}")
        success = download_file(info["url"], filepath, info["description"])
        if success:
            # Show first few lines as sanity check
            try:
                with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                    lines = f.readlines()
                    print(f"  Total lines: {len(lines):,}")
                    print(f"  First 5 non-empty lines:")
                    shown = 0
                    for line in lines:
                        if line.strip() and shown < 5:
                            print(f"    {line.strip()[:100]}")
                            shown += 1
            except Exception as e:
                print(f"  Preview error: {e}")
        print(f"  NOTE: {info['note']}")
        print()


def write_readme():
    """Write license and citation info."""
    readme_path = os.path.join(OUTPUT_DIR, "README_SOURCES.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""MSN WORD INVENTORY — SOURCE DOCUMENTATION
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
""")
    print(f"README written to {readme_path}")


# ============================================================
# MAIN
# ============================================================

def main():
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║     MSN WORD INVENTORY DOWNLOADER                   ║")
    print("║     Modern Standard Nahuatl — Every Legal Word      ║")
    print("║     For Sam Itzli / The Amoxtli Project             ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    ensure_dir()

    # Download kaikki.org data
    total_raw, total_unique = download_kaikki()

    # Download archive.org public domain texts
    download_archive_org()

    # Write documentation
    write_readme()

    # Final summary
    print()
    print("=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)
    print(f"  Kaikki.org (Wiktionary): {total_raw} raw entries, {total_unique} unique words")
    print(f"  Molina 1571 OCR: see molina_1571_ocr_raw.txt")
    print(f"  Siméon 1885 OCR: see simeon_1885_ocr_raw.txt")
    print()
    print(f"  All files in: {os.path.abspath(OUTPUT_DIR)}/")
    print()
    print("  NEXT STEPS:")
    print("  1. The kaikki.org data is ready to use as-is (JSON)")
    print("  2. The Molina OCR needs cleaning — this is the big project")
    print("  3. Buy Karttunen's dictionary for cross-referencing")
    print("  4. Every word you write in MSN expands the corpus")
    print()
    print("  Yo no escribo canciones, yo levanto sistemas.")
    print()


if __name__ == "__main__":
    main()
