#!/usr/bin/env python3
"""
SIMÉON 1885 DICTIONARY PARSER
===============================
Parses the OCR text of Rémi Siméon's "Dictionnaire de la langue nahuatl
ou mexicaine" (1885) into structured JSON.

Input:  simeon_1885_ocr_raw.txt (from archive.org)
Output: simeon_parsed.json — structured dictionary entries
        simeon_wordlist.txt — plain list of all headwords (one per line)

Source is PUBLIC DOMAIN (published 1885).

For Sam Itzli / The Amoxtli Project / Modern Standard Nahuatl
"""

import re
import json
import sys
import os

INPUT_FILE = "simeon_1885_ocr_raw.txt"
OUTPUT_JSON = "simeon_parsed.json"
OUTPUT_WORDLIST = "simeon_wordlist.txt"

# ============================================================
# PATTERNS
# ============================================================

# A headword line starts with 2+ uppercase letters (allowing Ç, É, etc.)
# followed by a comma, period, space, or "ou" (indicating alternate form)
HEADWORD_RE = re.compile(
    r'^([A-ZÇÉÈÊËÎÏÔÜÛ][A-ZÇÉÈÊËÎÏÔÜÛ]+(?:\s+ou\s+[A-ZÇÉÈÊËÎÏÔÜÛ]+)?)'
    r'[\s,.]'
)

# Page headers to skip
PAGE_HEADER_RE = re.compile(
    r'^\d+\s+DICTIONNAIRE|^DICTIONNAIRE DE LA LANGUE|'
    r'^\d+\s*$|^[A-Z]\.\s*$|^[A-Z]\s*$|'
    r'^\s*Fr\s*$|^\s*ra\]\s*$|^\s*P\+\s'
)

# Part of speech markers
POS_PATTERNS = {
    "s. v.": "noun (verbal/derived)",
    "s.": "noun",
    "adj. v.": "adjective (verbal/derived)",
    "adj. s.": "adjective/noun",
    "adj.": "adjective",
    "adv.": "adverb",
    "v. n.": "verb (neutral/intransitive)",
    "v. a.": "verb (active/transitive)", 
    "v.": "verb",
    "interj.": "interjection",
    "conj.": "conjunction",
    "prép.": "preposition",
    "pron.": "pronoun",
    "postp.": "postposition",
    "préf.": "prefix",
    "suff.": "suffix",
    "part.": "particle",
    "fréq.": "frequentative",
}

# Root reference patterns
ROOT_SINGLE_RE = re.compile(r'\bR\.\s+([a-zçéèêëîïôüûñ]+(?:\s*\(\?\))?)')
ROOT_COMPOUND_RE = re.compile(r'\bRR\.\s+([a-zçéèêëîïôüûñ,\s]+?)(?:\.|$|\n)')


def is_headword_line(line):
    """Check if a line starts a new dictionary entry."""
    stripped = line.strip()
    if not stripped:
        return False
    # Must start with 2+ uppercase chars
    if not HEADWORD_RE.match(stripped):
        return False
    # Skip page headers and noise
    if PAGE_HEADER_RE.match(stripped):
        return False
    # Skip lines that are just numbers or single letters
    if re.match(r'^\d+\s*$', stripped) or re.match(r'^[A-Z]\s*$', stripped):
        return False
    return True


def extract_headword(line):
    """Extract the headword(s) from the first line of an entry."""
    m = HEADWORD_RE.match(line.strip())
    if m:
        raw = m.group(1).strip()
        # Handle "WORD ou WORD2" (alternate forms)
        if " ou " in raw.upper():
            parts = re.split(r'\s+ou\s+', raw, flags=re.IGNORECASE)
            primary = parts[0].strip()
            alternates = [p.strip() for p in parts[1:]]
            return primary, alternates
        return raw, []
    return None, []


def extract_pos(text):
    """Extract part of speech from the entry text."""
    # Check longer patterns first (s. v. before s.)
    for marker, pos_name in sorted(POS_PATTERNS.items(), key=lambda x: -len(x[0])):
        # Look for the marker near the beginning of the entry
        # It typically appears right after the headword
        pattern = re.escape(marker)
        if re.search(r'(?:^|[,\s])' + pattern + r'(?:\s|$)', text[:200]):
            return pos_name, marker
    return None, None


def extract_roots(text):
    """Extract root references (R. and RR.)."""
    roots = []
    # Single root
    for m in ROOT_SINGLE_RE.finditer(text):
        root = m.group(1).strip().rstrip('.')
        if root and len(root) > 1:
            roots.append(root)
    # Compound roots
    for m in ROOT_COMPOUND_RE.finditer(text):
        parts = [p.strip().rstrip('.') for p in m.group(1).split(',')]
        roots.extend([p for p in parts if p and len(p) > 1])
    return roots


def extract_calendar_info(text):
    """Check if the entry has calendar (Cal.) information."""
    cal_match = re.search(r'Cal[.,]\s*([^;.]+)', text)
    if cal_match:
        return cal_match.group(1).strip()
    return None


def clean_definition(text, headword):
    """Clean up the raw definition text."""
    # Remove the headword from the start
    cleaned = text.strip()
    # Remove leading headword pattern
    cleaned = re.sub(r'^[A-ZÇÉÈÊËÎÏÔÜÛ]+(?:\s+ou\s+[A-ZÇÉÈÊËÎÏÔÜÛ]+)?\s*[,.]?\s*', '', cleaned, count=1)
    # Remove POS markers from the start
    for marker in sorted(POS_PATTERNS.keys(), key=len, reverse=True):
        if cleaned.lstrip().startswith(marker):
            cleaned = cleaned.lstrip()[len(marker):].lstrip()
            break
    # Clean up OCR artifacts
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    return cleaned


def parse_dictionary(filepath):
    """Parse the entire OCR text into structured entries."""
    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    print(f"Total lines: {len(lines):,}")

    # Find where the actual dictionary starts (skip front matter)
    dict_start = 0
    for i, line in enumerate(lines):
        # The dictionary proper starts with the first A entry
        if line.strip().startswith('A, adv') or line.strip().startswith('A,adv'):
            dict_start = i
            break
        # Or look for the first real headword after page 5000+ 
        if i > 5000 and is_headword_line(line.strip()):
            dict_start = i
            break
    
    # If we didn't find the specific start, look for the pattern
    if dict_start == 0:
        for i, line in enumerate(lines):
            if i > 5600 and is_headword_line(line.strip()):
                dict_start = i
                break

    print(f"Dictionary entries start at line {dict_start}")

    # First pass: identify all headword lines and group entry text
    raw_entries = []
    current_headword_line = None
    current_text_lines = []

    for i in range(dict_start, len(lines)):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines and page noise
        if not stripped:
            continue
        if PAGE_HEADER_RE.match(stripped):
            continue
        if re.match(r'^\d+\s*$', stripped):
            continue

        if is_headword_line(stripped):
            # Save previous entry
            if current_headword_line is not None:
                raw_entries.append({
                    'first_line': current_headword_line,
                    'full_text': ' '.join(current_text_lines)
                })
            current_headword_line = stripped
            current_text_lines = [stripped]
        else:
            # Continuation line
            if current_headword_line is not None:
                current_text_lines.append(stripped)

    # Don't forget the last entry
    if current_headword_line is not None:
        raw_entries.append({
            'first_line': current_headword_line,
            'full_text': ' '.join(current_text_lines)
        })

    print(f"Raw entries found: {len(raw_entries):,}")

    # Second pass: parse each entry into structured data
    entries = []
    seen_words = set()

    for raw in raw_entries:
        headword, alternates = extract_headword(raw['first_line'])
        if not headword:
            continue
        if len(headword) < 2:
            continue
        # Skip obvious OCR garbage
        if re.match(r'^[^A-Z]', headword):
            continue

        pos, pos_marker = extract_pos(raw['full_text'])
        roots = extract_roots(raw['full_text'])
        calendar = extract_calendar_info(raw['full_text'])
        definition = clean_definition(raw['full_text'], headword)

        # Determine if this is a verb by checking for perfect tense marker
        is_verb = bool(re.search(r'P\.\s+O[A-Z]', raw['full_text']))
        if is_verb and pos is None:
            pos = "verb"

        entry = {
            "headword": headword,
            "definition_fr": definition,
            "pos": pos,
        }

        if alternates:
            entry["alternates"] = alternates
        if roots:
            entry["roots"] = roots
        if calendar:
            entry["calendar"] = calendar
        if is_verb:
            entry["is_verb"] = True

        entries.append(entry)

        # Track unique words
        seen_words.add(headword.upper())
        for alt in alternates:
            seen_words.add(alt.upper())

    print(f"Parsed entries: {len(entries):,}")
    print(f"Unique headwords (including alternates): {len(seen_words):,}")

    return entries, sorted(seen_words)


def compute_stats(entries):
    """Compute statistics about the parsed dictionary."""
    pos_counts = {}
    verb_count = 0
    with_roots = 0
    with_calendar = 0

    for e in entries:
        pos = e.get('pos', 'unknown') or 'unknown'
        pos_counts[pos] = pos_counts.get(pos, 0) + 1
        if e.get('is_verb'):
            verb_count += 1
        if e.get('roots'):
            with_roots += 1
        if e.get('calendar'):
            with_calendar += 1

    return {
        "total_entries": len(entries),
        "pos_distribution": dict(sorted(pos_counts.items(), key=lambda x: -x[1])),
        "entries_with_verb_conjugation": verb_count,
        "entries_with_root_analysis": with_roots,
        "entries_with_calendar_info": with_calendar,
    }


def main():
    # Find the input file
    input_path = INPUT_FILE
    if not os.path.exists(input_path):
        # Try common locations
        for try_path in [
            "/mnt/user-data/uploads/simeon_1885_ocr_raw.txt",
            os.path.join("msn_word_inventory", INPUT_FILE),
            os.path.expanduser(f"~/{INPUT_FILE}"),
        ]:
            if os.path.exists(try_path):
                input_path = try_path
                break
        else:
            print(f"ERROR: Cannot find {INPUT_FILE}")
            print("Place it in the current directory or run download_all_nahuatl.py first.")
            sys.exit(1)

    print("=" * 60)
    print("SIMÉON 1885 DICTIONARY PARSER")
    print("Parsing Dictionnaire de la langue nahuatl ou mexicaine")
    print("Public domain (1885)")
    print("=" * 60)
    print()

    entries, wordlist = parse_dictionary(input_path)

    if not entries:
        print("ERROR: No entries parsed. Check input file.")
        sys.exit(1)

    stats = compute_stats(entries)

    # Build output
    output = {
        "_metadata": {
            "title": "Siméon's Dictionnaire de la langue nahuatl (1885) — Parsed",
            "source": "Rémi Siméon, Dictionnaire de la langue nahuatl ou mexicaine, Paris, 1885",
            "original_sources": "Based on Molina (1571), Florentine Codex, and other colonial manuscripts",
            "license": "PUBLIC DOMAIN (published 1885)",
            "language_of_definitions": "French",
            "ocr_quality": "Auto-OCR from archive.org scan. Contains errors. Use with scholarly judgment.",
            "parser": "simeon_parser.py (for Sam Itzli / The Amoxtli Project)",
            "stats": stats,
            "note": "Definitions are in French. For MSN work, cross-reference with Karttunen (English) and kaikki.org data."
        },
        "entries": entries
    }

    # Save JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    json_size = os.path.getsize(OUTPUT_JSON) / 1024 / 1024
    print(f"\nSaved: {OUTPUT_JSON} ({json_size:.1f} MB)")

    # Save plain wordlist
    with open(OUTPUT_WORDLIST, 'w', encoding='utf-8') as f:
        for word in wordlist:
            f.write(word + '\n')
    print(f"Saved: {OUTPUT_WORDLIST} ({len(wordlist)} unique headwords)")

    # Print stats
    print(f"\n{'=' * 60}")
    print("RESULTS")
    print(f"{'=' * 60}")
    print(f"Total parsed entries: {stats['total_entries']:,}")
    print(f"Entries with root analysis: {stats['entries_with_root_analysis']:,}")
    print(f"Entries with verb conjugation: {stats['entries_with_verb_conjugation']:,}")
    print(f"Entries with calendar info: {stats['entries_with_calendar_info']:,}")
    print(f"\nPart of speech distribution:")
    for pos, count in stats['pos_distribution'].items():
        print(f"  {pos}: {count:,}")

    # Show sample entries
    print(f"\n{'=' * 60}")
    print("SAMPLE ENTRIES")
    print(f"{'=' * 60}")
    samples = ["ATL", "CUICATL", "TEOTL", "TONALLI", "IHIOTL", "XOCHITL", 
               "CALLI", "TLALTICPAC", "NELTILIZTLI", "IPALNEMOANI", "CUICANI",
               "MOYOCOYA", "OCELOTL", "TLETL", "TEYOLIA"]
    for target in samples:
        for e in entries:
            if e['headword'].upper() == target or target in [a.upper() for a in e.get('alternates', [])]:
                defn = e['definition_fr'][:120]
                roots = ', '.join(e.get('roots', []))
                pos = e.get('pos', '?')
                print(f"\n  {e['headword']} [{pos}]")
                print(f"    {defn}...")
                if roots:
                    print(f"    Roots: {roots}")
                break

    print(f"\n\nDone. {stats['total_entries']:,} Nahuatl words parsed from Siméon 1885.")
    print("Yo no escribo canciones, yo levanto sistemas.")


if __name__ == "__main__":
    main()
