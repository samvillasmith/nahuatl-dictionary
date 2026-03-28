#!/usr/bin/env python3
"""FCN Phase 6 orthography utilities.

This script operationalizes the Phase 6 orthography decisions by:
- normalizing legacy/traditional spellings toward FCN MSN candidates
- generating search fallback keys
- exporting candidate EHN -> MSN mappings from the SQLite lexicon DB

It is deliberately conservative:
- it never edits the database in place
- it prefers explicit source gloss targets when available
- it emits reviewable CSV/JSON reports for editorial approval
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
import unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Tuple

MACRON_MAP = str.maketrans({
    "ā": "a", "ē": "e", "ī": "i", "ō": "o",
    "Ā": "A", "Ē": "E", "Ī": "I", "Ō": "O",
})

LEGACY_SEARCH_EQUIV = [
    ("ts", "tz"),
    ("w", "hu"),
    ("kw", "cu"),  # included for future compatibility even if canonical favors ku- outputs today
    ("s", "z"),
]

GLOSS_TARGET_RE = re.compile(
    r"^(obsolete spelling of|alternative spelling of|alternative form of)\s+([^;,.]+)",
    re.IGNORECASE,
)

VOWELS = "aeiouāēīōAEIOUĀĒĪŌ"


@dataclass
class CandidateRow:
    entry_id: str
    source_form: str
    source_register: str
    source_variety: str
    gloss_en: str
    source_note: str
    candidate_msn_headword: str
    candidate_search_key: str
    search_fallbacks_json: str
    rule_trace: str


def strip_macrons(text: str) -> str:
    return text.translate(MACRON_MAP)


def ascii_fold(text: str) -> str:
    text = strip_macrons(text)
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def clean_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def replace_hu_to_w(text: str) -> Tuple[str, List[str]]:
    rules: List[str] = []
    out = text
    # hu before vowel -> w
    new = re.sub(r"(?i)hu(?=[aeiouāēīō])", "w", out)
    if new != out:
        rules.append("hu> w before vowel")
        out = new
    # uh after vowel -> w
    new = re.sub(rf"(?i)(?<=[{VOWELS}])uh", "w", out)
    if new != out:
        rules.append("uh> w after vowel")
        out = new
    return out, rules


def normalize_legacy_to_msn(text: str) -> Tuple[str, List[str]]:
    """Normalize a legacy spelling toward FCN MSN.

    This is a conservative graphemic conversion. It does not infer vowel length.
    """
    if not text:
        return text, []

    s = clean_spaces(text.lower())
    rules: List[str] = []

    # Normalize quote-like saltillo markers to h later only when they are explicit.
    if any(q in s for q in ["'", "’", "ʻ"]):
        s = s.replace("’", "h").replace("ʻ", "h").replace("'", "h")
        rules.append("apostrophe-style saltillo > h")

    # Legacy cedilla forms -> s-series base.
    if "ç" in s:
        s = s.replace("ç", "s")
        rules.append("ç > s")

    # hu / uh sequences spelling /w/
    s, hu_rules = replace_hu_to_w(s)
    rules.extend(hu_rules)

    # qu before front vowels -> k
    new = re.sub(r"qu(?=[eiēī])", "k", s)
    if new != s:
        s = new
        rules.append("qu > k before front vowel")

    # soft c before e/i -> s
    new = re.sub(r"c(?=[eiēī])", "s", s)
    if new != s:
        s = new
        rules.append("soft c > s")

    # z -> s
    if "z" in s:
        s = s.replace("z", "s")
        rules.append("z > s")

    # remaining c -> k, but preserve ch
    new = re.sub(r"c(?!h)", "k", s)
    if new != s:
        s = new
        rules.append("hard c > k")

    # tz -> ts
    if "tz" in s:
        s = s.replace("tz", "ts")
        rules.append("tz > ts")

    return s, rules


def gloss_target(gloss: str) -> str | None:
    if not gloss:
        return None
    m = GLOSS_TARGET_RE.match(gloss.strip())
    if not m:
        return None
    target = clean_spaces(m.group(2))
    return target or None


def generate_search_fallbacks(source_form: str, candidate: str) -> List[str]:
    values = []
    for base in [source_form or "", candidate or ""]:
        if not base:
            continue
        base = clean_spaces(base.lower())
        values.append(base)
        values.append(strip_macrons(base))
        values.append(ascii_fold(base))
        values.append(ascii_fold(base).replace("h", ""))
    # generate legacy-friendly alternates from candidate
    c = ascii_fold(candidate.lower()) if candidate else ""
    if c:
        legacy = c
        # reverse-ish convenience replacements for search only
        legacy = legacy.replace("w", "hu")
        legacy = legacy.replace("ts", "tz")
        legacy = legacy.replace("k", "c")
        values.append(legacy)
    deduped = []
    seen = set()
    for v in values:
        v = clean_spaces(v)
        if not v:
            continue
        if v not in seen:
            deduped.append(v)
            seen.add(v)
    return deduped


def candidate_from_row(source_form: str, gloss: str) -> Tuple[str, List[str], str]:
    target = gloss_target(gloss)
    if target:
        norm_target, target_rules = normalize_legacy_to_msn(target)
        # If the source gloss already provides a normalized target, trust that first.
        return norm_target, [f"gloss target: {target}"] + target_rules, "explicit_gloss_target"
    norm, rules = normalize_legacy_to_msn(source_form)
    return norm, rules or ["identity"], "rule_based_from_source_form"


def export_candidates(db_path: Path, out_csv: Path, out_json: Path) -> dict:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute(
        """
        SELECT entry_id, ehn_spoken_form, msn_headword, gloss_en, register, variety
        FROM lexicon_entries
        WHERE ehn_spoken_form IS NOT NULL
        ORDER BY entry_id
        """
    ).fetchall()

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    stats = {
        "input_rows": len(rows),
        "explicit_gloss_target": 0,
        "rule_based_from_source_form": 0,
        "changed_vs_source_form": 0,
        "same_as_source_form": 0,
        "same_as_current_msn_headword": 0,
        "different_from_current_msn_headword": 0,
        "rule_frequencies": {},
    }

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(CandidateRow(
            entry_id="",
            source_form="",
            source_register="",
            source_variety="",
            gloss_en="",
            source_note="",
            candidate_msn_headword="",
            candidate_search_key="",
            search_fallbacks_json="",
            rule_trace="",
        )).keys()))
        writer.writeheader()

        for row in rows:
            source_form = row["ehn_spoken_form"] or row["msn_headword"] or ""
            candidate, trace, source_note = candidate_from_row(source_form, row["gloss_en"] or "")
            fallbacks = generate_search_fallbacks(source_form, candidate)
            primary_search_key = ascii_fold(candidate.lower()) if candidate else (fallbacks[0] if fallbacks else "")

            rec = CandidateRow(
                entry_id=row["entry_id"],
                source_form=source_form,
                source_register=row["register"] or "",
                source_variety=row["variety"] or "",
                gloss_en=row["gloss_en"] or "",
                source_note=source_note,
                candidate_msn_headword=candidate,
                candidate_search_key=primary_search_key,
                search_fallbacks_json=json.dumps(fallbacks, ensure_ascii=False),
                rule_trace="; ".join(trace),
            )
            writer.writerow(asdict(rec))

            stats[source_note] += 1
            if clean_spaces(candidate) == clean_spaces(source_form.lower()):
                stats["same_as_source_form"] += 1
            else:
                stats["changed_vs_source_form"] += 1
            current = (row["msn_headword"] or "").lower().strip()
            if current == clean_spaces(candidate):
                stats["same_as_current_msn_headword"] += 1
            else:
                stats["different_from_current_msn_headword"] += 1
            for item in trace:
                stats["rule_frequencies"][item] = stats["rule_frequencies"].get(item, 0) + 1

    with out_json.open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2, sort_keys=True)

    conn.close()
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="FCN Phase 6 orthography utilities")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_norm = sub.add_parser("normalize", help="Normalize one form toward FCN MSN")
    p_norm.add_argument("form", help="Input form")

    p_export = sub.add_parser("export-candidates", help="Export EHN -> MSN candidate mappings from SQLite DB")
    p_export.add_argument("--db", required=True, help="Path to fcn_master_lexicon.sqlite")
    p_export.add_argument("--out-csv", required=True, help="Output CSV path")
    p_export.add_argument("--out-json", required=True, help="Output JSON summary path")

    args = parser.parse_args()

    if args.cmd == "normalize":
        normalized, rules = normalize_legacy_to_msn(args.form)
        fallbacks = generate_search_fallbacks(args.form, normalized)
        print(json.dumps({
            "input": args.form,
            "normalized": normalized,
            "rules": rules,
            "search_fallbacks": fallbacks,
        }, ensure_ascii=False, indent=2))
        return

    if args.cmd == "export-candidates":
        stats = export_candidates(Path(args.db), Path(args.out_csv), Path(args.out_json))
        print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
        return


if __name__ == "__main__":
    main()
