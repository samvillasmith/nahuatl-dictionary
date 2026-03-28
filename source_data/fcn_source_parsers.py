#!/usr/bin/env python3
"""
FCN source parsers: lexical rows, grammar evidence, classical example banks,
and Nahuatlahtolli lesson banks.

Designed to sit next to `fcn_legal_ingest.py` in a legal-first ingestion workflow.
The script prefers structured/local inputs and preserves provenance rather than
making irreversible editorial decisions.

Subcommands
-----------
1) wiktionary-to-fcn
   Convert one of the following into FCN lexical rows:
   - Kaikki/Wiktextract unified JSON (`nahuatl_kaikki_unified.json`-style)
   - Wiktextract JSONL
   - Raw Wiktionary XML dump (best-effort, much weaker than structured data)

2) ud-to-grammar
   Parse CoNLL-U / UD treebanks into raw token tables and aggregated grammar
   evidence tables.

3) ia-to-classical-bank
   Parse public-domain OCR/PDF/JSON sources into a classical example bank.

4) nahuatlahtolli-to-bank
   Parse HTML lesson pages (local files or URLs) into a modern Huasteca lesson
   bank and grammar/example bank.

Example usage
-------------
  python fcn_source_parsers.py wiktionary-to-fcn \
      --input /mnt/data/nahuatl_kaikki_unified.json \
      --out /mnt/data/out/kaikki_rows

  python fcn_source_parsers.py ud-to-grammar \
      --input treebank.conllu --out /mnt/data/out/ud

  python fcn_source_parsers.py ia-to-classical-bank \
      --input /mnt/data/simeon_1885_ocr_raw.txt --out /mnt/data/out/simeon_bank

  python fcn_source_parsers.py nahuatlahtolli-to-bank \
      --input lesson.html --out /mnt/data/out/nahuatlahtolli
"""

from __future__ import annotations

import argparse
import bz2
import csv
import html
import io
import json
import os
from pathlib import Path
import re
import sys
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

try:
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover
    BeautifulSoup = None  # type: ignore

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover
    PdfReader = None  # type: ignore

USER_AGENT = "FCN-source-parsers/0.1"
TIMEOUT = 60

FCN_PROJECT_NAME = "Flor y Canto Nahuatl"

POS_HEADINGS = {
    "noun": "noun",
    "proper noun": "proper_noun",
    "pronoun": "pronoun",
    "verb": "verb",
    "adjective": "adjective",
    "adverb": "adverb",
    "numeral": "numeral",
    "number": "numeral",
    "particle": "particle",
    "interjection": "interjection",
    "postposition": "postposition",
    "preposition": "preposition",
    "conjunction": "conjunction",
    "determiner": "determiner",
    "prefix": "prefix",
    "suffix": "suffix",
    "phrase": "phrase",
    "participle": "participle",
}

GRAMMAR_KEYWORDS = {
    "grammar", "verb", "verbs", "tense", "future", "past", "conditional",
    "possessive", "marker", "markers", "object", "objects", "prefix", "prefixes",
    "suffix", "suffixes", "plural", "pronoun", "pronouns", "noun", "adjective",
    "numbers", "number", "questions", "question", "commands", "intransitive",
    "transitive", "declension", "conjugation", "conjugations", "particle",
    "particles", "family", "colors", "colour", "colors and numbers",
}

NAHUATL_CUES_RE = re.compile(
    r"(?i)(?:tl|tz|ch|hu|uh|qu|cu|[āēīōūç]|tli\\b|tl\\b|meh\\b|tin\\b|tzin\\b|yotl\\b|ni-|mo-|ti-|qui-|tla-)"
)

HEADWORD_LINE_RE = re.compile(r"^[A-ZÁÉÍÓÚÜÑÇ'’\- ]{2,40}$")

WIKI_LINK_RE = re.compile(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]")
WIKI_TEMPLATE_RE = re.compile(r"\{\{[^{}]*\}\}")
HTML_TAG_RE = re.compile(r"<[^>]+>")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
REF_RE = re.compile(r"<ref[^>]*>.*?</ref>", re.S)
BOLD_ITALIC_RE = re.compile(r"'{2,5}")


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)



def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "item"



def write_csv(path: Path, rows: Iterable[Dict[str, Any]], fieldnames: Sequence[str]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})



def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")



def http_get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        raw = resp.read()
        content_type = resp.headers.get_content_charset() or "utf-8"
    return raw.decode(content_type, errors="replace")



def clean_whitespace(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()



def json_dumps_compact(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True)



def split_paragraphs(text: str) -> List[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = []
    current: List[str] = []
    for line in text.split("\n"):
        raw = line.strip()
        if not raw:
            if current:
                blocks.append(clean_whitespace(" ".join(current)))
                current = []
            continue
        current.append(raw)
    if current:
        blocks.append(clean_whitespace(" ".join(current)))
    return [b for b in blocks if b]



def tokenise_simple(text: str) -> List[str]:
    return re.findall(r"[A-Za-zÁÉÍÓÚÜÑÇāēīōūç'’\-]+", text)



def nahuatliness_score(text: str) -> float:
    tokens = tokenise_simple(text)
    if not tokens:
        return 0.0
    cue_hits = sum(1 for tok in tokens if NAHUATL_CUES_RE.search(tok))
    diacritic_bonus = 1 if re.search(r'[āēīōūç]', text) else 0
    return round((cue_hits + diacritic_bonus) / max(len(tokens), 1), 4)



def looks_like_headword(line: str) -> bool:
    line = line.strip()
    if not line or len(line) > 40:
        return False
    if not HEADWORD_LINE_RE.match(line):
        return False
    tokens = line.split()
    return 1 <= len(tokens) <= 5



def wiki_clean(text: str) -> str:
    text = COMMENT_RE.sub(" ", text)
    text = REF_RE.sub(" ", text)
    prev = None
    while prev != text:
        prev = text
        text = WIKI_TEMPLATE_RE.sub(" ", text)
    text = WIKI_LINK_RE.sub(r"\1", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = BOLD_ITALIC_RE.sub("", text)
    text = html.unescape(text)
    text = re.sub(r"\[http[^\]]+\]", " ", text)
    text = re.sub(r"\{[^{}]*\}", " ", text)
    return clean_whitespace(text)



def guess_register_suggestion(variety: str) -> str:
    variety_l = (variety or "").lower()
    if "eastern huasteca" in variety_l:
        return "EHN_colloquial"
    if "classical" in variety_l:
        return "Classical_citation"
    return "Needs_review"



def build_fcn_row(
    *,
    entry_id: str,
    source_file: str,
    source_reference: str,
    lemma: str,
    part_of_speech: str,
    variety: str,
    gloss_en: str = "",
    gloss_es: str = "",
    forms: Optional[List[Dict[str, Any]]] = None,
    etymology: str = "",
    parser_name: str = "",
    parser_confidence: str = "",
    notes_internal: str = "",
) -> Dict[str, Any]:
    register_suggestion = guess_register_suggestion(variety)
    row = {
        "entry_id": entry_id,
        "project_name": FCN_PROJECT_NAME,
        "source_file": source_file,
        "source_reference": source_reference,
        "lemma_display": lemma,
        "ehn_spoken_form": lemma if register_suggestion == "EHN_colloquial" else "",
        "msn_headword": lemma,
        "msn_poetic_form": "",
        "classical_citation_form": lemma if register_suggestion == "Classical_citation" else "",
        "part_of_speech": part_of_speech,
        "register": "",
        "register_suggestion": register_suggestion,
        "variety": variety,
        "gloss_en": gloss_en,
        "gloss_es": gloss_es,
        "root_family": "",
        "source_confidence": parser_confidence or "medium",
        "speaker_validation_status": "unreviewed",
        "editorial_status": "imported_raw",
        "forms_json": json_dumps_compact(forms or []),
        "etymology": etymology or "",
        "parser": parser_name,
        "notes_internal": notes_internal,
        "notes_public": "",
    }
    return row


# ---------------------------------------------------------------------------
# 1) Wiktionary / Kaikki / Wiktextract -> FCN lexical rows
# ---------------------------------------------------------------------------


def parse_kaikki_unified(path: Path) -> Iterator[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    words = payload.get("words", {})
    for lemma, entry in words.items():
        forms = entry.get("forms", []) or []
        senses = entry.get("senses", []) or []
        etymology = entry.get("etymology") or ""
        if not senses:
            yield build_fcn_row(
                entry_id=f"kw::{slug(lemma)}::0",
                source_file=path.name,
                source_reference=f"{path.name}::{lemma}",
                lemma=entry.get("word", lemma),
                part_of_speech=",".join(entry.get("pos_tags", []) or []),
                variety="; ".join(entry.get("varieties", []) or []),
                forms=forms,
                etymology=etymology,
                parser_name="kaikki_unified",
                parser_confidence="high",
            )
            continue

        for i, sense in enumerate(senses, start=1):
            yield build_fcn_row(
                entry_id=f"kw::{slug(lemma)}::{i}",
                source_file=path.name,
                source_reference=f"{path.name}::{lemma}::sense-{i}",
                lemma=entry.get("word", lemma),
                part_of_speech=sense.get("pos") or ",".join(entry.get("pos_tags", []) or []),
                variety=sense.get("variety") or "; ".join(entry.get("varieties", []) or []),
                gloss_en=sense.get("gloss", ""),
                forms=[f for f in forms if not sense.get("variety") or f.get("variety") == sense.get("variety")],
                etymology=etymology,
                parser_name="kaikki_unified",
                parser_confidence="high",
            )



def parse_wiktextract_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            lang = obj.get("lang") or obj.get("lang_name") or obj.get("language", "")
            if "nahuatl" not in lang.lower():
                continue
            lemma = obj.get("word") or obj.get("title") or ""
            pos = obj.get("pos") or obj.get("part_of_speech") or ""
            forms = obj.get("forms") or []
            etymology = obj.get("etymology_text") or obj.get("etymology") or ""
            senses = obj.get("senses") or []
            if not senses:
                yield build_fcn_row(
                    entry_id=f"wt::{slug(lemma)}::{line_no}::0",
                    source_file=path.name,
                    source_reference=f"{path.name}:{line_no}",
                    lemma=lemma,
                    part_of_speech=pos,
                    variety=lang,
                    forms=forms,
                    etymology=etymology,
                    parser_name="wiktextract_jsonl",
                    parser_confidence="high",
                )
                continue
            for i, sense in enumerate(senses, start=1):
                glosses = sense.get("glosses") or []
                gloss = "; ".join(glosses) if isinstance(glosses, list) else str(glosses)
                yield build_fcn_row(
                    entry_id=f"wt::{slug(lemma)}::{line_no}::{i}",
                    source_file=path.name,
                    source_reference=f"{path.name}:{line_no}:sense-{i}",
                    lemma=lemma,
                    part_of_speech=pos,
                    variety=lang,
                    gloss_en=gloss,
                    forms=forms,
                    etymology=etymology,
                    parser_name="wiktextract_jsonl",
                    parser_confidence="high",
                )



def _strip_ns(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]



def iter_mediawiki_pages(path: Path) -> Iterator[Tuple[str, str]]:
    opener = bz2.open if path.suffix == ".bz2" else open
    with opener(path, "rb") as f:
        context = ET.iterparse(f, events=("end",))
        for _event, elem in context:
            if _strip_ns(elem.tag) != "page":
                continue
            title = None
            ns = "0"
            text = None
            for child in elem:
                tag = _strip_ns(child.tag)
                if tag == "title":
                    title = child.text or ""
                elif tag == "ns":
                    ns = child.text or "0"
                elif tag == "revision":
                    for rev_child in child:
                        if _strip_ns(rev_child.tag) == "text":
                            text = rev_child.text or ""
                            break
            if ns == "0" and title and text:
                yield title, text
            elem.clear()


@dataclass
class WikiSection:
    title: str
    level: int
    lines: List[str]



def split_wikitext_sections(text: str) -> List[WikiSection]:
    sections: List[WikiSection] = []
    current_title = "__lead__"
    current_level = 0
    current_lines: List[str] = []
    for line in text.splitlines():
        m = re.match(r"^(=+)\s*(.*?)\s*\1\s*$", line)
        if m:
            sections.append(WikiSection(current_title, current_level, current_lines))
            current_title = m.group(2).strip()
            current_level = len(m.group(1))
            current_lines = []
        else:
            current_lines.append(line)
    sections.append(WikiSection(current_title, current_level, current_lines))
    return sections



def extract_nahuatl_section(text: str) -> List[WikiSection]:
    sections = split_wikitext_sections(text)
    in_target = False
    target_sections: List[WikiSection] = []
    for sec in sections:
        title_l = sec.title.lower()
        if sec.level == 2:
            in_target = title_l == "nahuatl"
            continue
        if in_target:
            target_sections.append(sec)
    return target_sections



def parse_wiktionary_xml_best_effort(path: Path) -> Iterator[Dict[str, Any]]:
    for page_idx, (title, text) in enumerate(iter_mediawiki_pages(path), start=1):
        nahuatl_sections = extract_nahuatl_section(text)
        if not nahuatl_sections:
            continue
        for sec_idx, sec in enumerate(nahuatl_sections, start=1):
            pos = POS_HEADINGS.get(sec.title.lower(), sec.title.lower())
            raw_lines = sec.lines
            glosses = []
            for line in raw_lines:
                if line.lstrip().startswith("#"):
                    glosses.append(wiki_clean(line.lstrip("#* ")))
            forms = []
            for line in raw_lines[:8]:
                if "{{head" in line or "{{nah-" in line:
                    forms.append({"form": title, "tags": ["page-title"], "variety": "Nahuatl"})
                    break
            if not glosses:
                cleaned = wiki_clean("\n".join(raw_lines[:12]))
                if cleaned:
                    glosses = [cleaned[:400]]
            for i, gloss in enumerate(glosses, start=1):
                yield build_fcn_row(
                    entry_id=f"xml::{slug(title)}::{page_idx}::{sec_idx}::{i}",
                    source_file=path.name,
                    source_reference=f"{title}::{sec.title}::{i}",
                    lemma=title,
                    part_of_speech=pos,
                    variety="Nahuatl",
                    gloss_en=gloss,
                    forms=forms,
                    etymology="",
                    parser_name="wiktionary_xml_best_effort",
                    parser_confidence="low",
                    notes_internal="Best-effort XML parse; prefer structured Wiktextract/Kaikki when available.",
                )



def detect_wiktionary_input_format(path: Path, explicit: str) -> str:
    if explicit != "auto":
        return explicit
    if path.suffix == ".json":
        with path.open("r", encoding="utf-8") as f:
            first = f.read(2048)
        if '"words"' in first and '"_metadata"' in first:
            return "kaikki_unified"
        return "json"
    if path.suffix == ".jsonl":
        return "wiktextract_jsonl"
    if path.suffix in {".xml", ".bz2"}:
        return "wiktionary_xml"
    raise ValueError(f"Could not auto-detect Wiktionary input format for {path}")



def cmd_wiktionary_to_fcn(args: argparse.Namespace) -> int:
    path = Path(args.input)
    fmt = detect_wiktionary_input_format(path, args.input_format)
    if fmt == "kaikki_unified":
        rows = list(parse_kaikki_unified(path))
    elif fmt == "wiktextract_jsonl":
        rows = list(parse_wiktextract_jsonl(path))
    elif fmt == "wiktionary_xml":
        rows = list(parse_wiktionary_xml_best_effort(path))
    else:
        raise ValueError(f"Unsupported Wiktionary input format: {fmt}")

    out_dir = Path(args.out)
    ensure_dir(out_dir)
    jsonl_path = out_dir / "fcn_lexical_rows.jsonl"
    csv_path = out_dir / "fcn_lexical_rows.csv"
    fieldnames = list(rows[0].keys()) if rows else [
        "entry_id", "project_name", "source_file", "source_reference", "lemma_display",
        "ehn_spoken_form", "msn_headword", "msn_poetic_form", "classical_citation_form",
        "part_of_speech", "register", "register_suggestion", "variety", "gloss_en",
        "gloss_es", "root_family", "source_confidence", "speaker_validation_status",
        "editorial_status", "forms_json", "etymology", "parser", "notes_internal",
        "notes_public",
    ]
    write_jsonl(jsonl_path, rows)
    write_csv(csv_path, rows, fieldnames)

    summary = {
        "input": str(path),
        "input_format": fmt,
        "rows": len(rows),
        "out_jsonl": str(jsonl_path),
        "out_csv": str(csv_path),
        "variety_counts": Counter(r["variety"] for r in rows).most_common(20),
        "pos_counts": Counter(r["part_of_speech"] for r in rows).most_common(20),
    }
    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    log(f"Wrote {len(rows)} lexical rows to {out_dir}")
    return 0


# ---------------------------------------------------------------------------
# 2) UD / CoNLL-U -> grammar evidence tables
# ---------------------------------------------------------------------------


def parse_conllu_feats(feats: str) -> Dict[str, str]:
    if not feats or feats == "_":
        return {}
    out: Dict[str, str] = {}
    for item in feats.split("|"):
        if "=" in item:
            k, v = item.split("=", 1)
            out[k] = v
    return out



def parse_conllu_sentences(path: Path) -> Iterator[Dict[str, Any]]:
    sent_comments: Dict[str, str] = {}
    token_rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            if not line:
                if token_rows:
                    yield {
                        "comments": dict(sent_comments),
                        "tokens": list(token_rows),
                    }
                sent_comments = {}
                token_rows = []
                continue
            if line.startswith("#"):
                if "=" in line:
                    k, v = line[1:].split("=", 1)
                    sent_comments[k.strip()] = v.strip()
                continue
            cols = line.split("\t")
            if len(cols) != 10:
                continue
            tok_id = cols[0]
            if "-" in tok_id or "." in tok_id:
                # Skip multiword tokens and empty nodes for the token table; sentence text preserves them elsewhere.
                continue
            token_rows.append({
                "id": tok_id,
                "form": cols[1],
                "lemma": cols[2],
                "upos": cols[3],
                "xpos": cols[4],
                "feats": parse_conllu_feats(cols[5]),
                "head": cols[6],
                "deprel": cols[7],
                "deps": cols[8],
                "misc": cols[9],
            })
    if token_rows:
        yield {
            "comments": dict(sent_comments),
            "tokens": list(token_rows),
        }



def cmd_ud_to_grammar(args: argparse.Namespace) -> int:
    out_dir = Path(args.out)
    ensure_dir(out_dir)

    sentence_rows: List[Dict[str, Any]] = []
    token_rows: List[Dict[str, Any]] = []
    feat_counts: Counter[Tuple[str, str, str]] = Counter()
    lemma_feat_counts: Counter[Tuple[str, str, str]] = Counter()
    dep_counts: Counter[Tuple[str, str, str]] = Counter()
    morph_examples: Dict[Tuple[str, str], Dict[str, Any]] = {}

    sent_counter = 0
    token_counter = 0

    for input_path in args.input:
        path = Path(input_path)
        for sent in parse_conllu_sentences(path):
            sent_counter += 1
            comments = sent["comments"]
            sent_id = comments.get("sent_id") or f"{path.stem}-sent-{sent_counter}"
            sent_text = comments.get("text") or " ".join(tok["form"] for tok in sent["tokens"])
            sentence_rows.append({
                "source_file": path.name,
                "sent_id": sent_id,
                "text": sent_text,
                "token_count": len(sent["tokens"]),
                "comments_json": json_dumps_compact(comments),
            })

            token_by_id = {tok["id"]: tok for tok in sent["tokens"]}
            for tok in sent["tokens"]:
                token_counter += 1
                feats_json = json_dumps_compact(tok["feats"])
                token_rows.append({
                    "source_file": path.name,
                    "sent_id": sent_id,
                    "token_id": tok["id"],
                    "form": tok["form"],
                    "lemma": tok["lemma"],
                    "upos": tok["upos"],
                    "xpos": tok["xpos"],
                    "feats_json": feats_json,
                    "head": tok["head"],
                    "deprel": tok["deprel"],
                    "deps": tok["deps"],
                    "misc": tok["misc"],
                })
                for feat_name, feat_val in tok["feats"].items():
                    feat_counts[(tok["upos"], feat_name, feat_val)] += 1
                feat_bundle = "|".join(f"{k}={v}" for k, v in sorted(tok["feats"].items())) or "_"
                lemma_feat_counts[(tok["lemma"], tok["upos"], feat_bundle)] += 1
                head_tok = token_by_id.get(tok["head"])
                head_upos = head_tok["upos"] if head_tok else "ROOT"
                dep_counts[(tok["deprel"], head_upos, tok["upos"])] += 1
                for feat_name, feat_val in tok["feats"].items():
                    morph_examples.setdefault(
                        (feat_name, feat_val),
                        {
                            "feature_name": feat_name,
                            "feature_value": feat_val,
                            "source_file": path.name,
                            "sent_id": sent_id,
                            "token_id": tok["id"],
                            "form": tok["form"],
                            "lemma": tok["lemma"],
                            "upos": tok["upos"],
                            "sentence_text": sent_text,
                        },
                    )

    write_jsonl(out_dir / "sentences.jsonl", sentence_rows)
    write_csv(
        out_dir / "tokens.csv",
        token_rows,
        [
            "source_file", "sent_id", "token_id", "form", "lemma", "upos", "xpos",
            "feats_json", "head", "deprel", "deps", "misc",
        ],
    )
    write_csv(
        out_dir / "feature_counts.csv",
        (
            {"upos": u, "feature_name": n, "feature_value": v, "count": c}
            for (u, n, v), c in sorted(feat_counts.items(), key=lambda x: (-x[1], x[0]))
        ),
        ["upos", "feature_name", "feature_value", "count"],
    )
    write_csv(
        out_dir / "lemma_feature_counts.csv",
        (
            {"lemma": lemma, "upos": upos, "feature_bundle": bundle, "count": c}
            for (lemma, upos, bundle), c in sorted(lemma_feat_counts.items(), key=lambda x: (-x[1], x[0]))
        ),
        ["lemma", "upos", "feature_bundle", "count"],
    )
    write_csv(
        out_dir / "dependency_counts.csv",
        (
            {"deprel": d, "head_upos": h, "child_upos": cpos, "count": c}
            for (d, h, cpos), c in sorted(dep_counts.items(), key=lambda x: (-x[1], x[0]))
        ),
        ["deprel", "head_upos", "child_upos", "count"],
    )
    write_jsonl(out_dir / "grammar_evidence_examples.jsonl", morph_examples.values())

    summary = {
        "input_files": list(args.input),
        "sentences": sent_counter,
        "tokens": token_counter,
        "unique_features": len(morph_examples),
        "out_dir": str(out_dir),
    }
    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    log(f"Wrote UD grammar evidence tables to {out_dir}")
    return 0


# ---------------------------------------------------------------------------
# 3) Internet Archive OCR/PDF -> classical example bank
# ---------------------------------------------------------------------------


def extract_text_from_pdf(path: Path) -> List[Tuple[str, str]]:
    if PdfReader is None:
        raise RuntimeError("pypdf is not installed; cannot parse PDFs")
    reader = PdfReader(str(path))
    pages: List[Tuple[str, str]] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages.append((f"page-{i}", clean_whitespace(text)))
    return pages



def extract_text_units(path: Path) -> List[Tuple[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".txt":
        with path.open("r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        return [(f"block-source", clean_whitespace(text))]
    if suffix == ".pdf":
        return extract_text_from_pdf(path)
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        if isinstance(payload, dict) and "entries" in payload and isinstance(payload["entries"], list):
            units = []
            for i, entry in enumerate(payload["entries"], start=1):
                headword = entry.get("headword", "")
                definition = entry.get("definition_fr", "")
                pos = entry.get("pos", "") or ""
                roots = entry.get("roots") or []
                blob = f"{headword}\nPOS: {pos}\nROOTS: {', '.join(roots)}\n{definition}"
                units.append((f"entry-{i}", clean_whitespace(blob)))
            return units
    raise ValueError(f"Unsupported classical-bank input type: {path}")



def split_classical_units_to_blocks(locator: str, text: str) -> List[Tuple[str, str]]:
    if locator.startswith("page-"):
        return [(f"{locator}:block-{i}", block) for i, block in enumerate(split_paragraphs(text), start=1)]
    return [(f"block-{i}", block) for i, block in enumerate(split_paragraphs(text), start=1)]



def extract_example_fragments(text: str) -> List[str]:
    parts = []
    for chunk in re.split(r"(?i)\b(?:Ex\.|Exemple[s]?|Ej\.)\b", text):
        chunk = clean_whitespace(chunk)
        if chunk:
            parts.append(chunk)
    if len(parts) > 1:
        return parts[1:]
    semi_parts = [clean_whitespace(p) for p in re.split(r"[;:]", text) if clean_whitespace(p)]
    return [p for p in semi_parts if nahuatliness_score(p) >= 0.18 and 3 <= len(tokenise_simple(p)) <= 40]



def cmd_ia_to_classical_bank(args: argparse.Namespace) -> int:
    out_dir = Path(args.out)
    ensure_dir(out_dir)
    block_rows: List[Dict[str, Any]] = []
    example_rows: List[Dict[str, Any]] = []
    headword_rows: List[Dict[str, Any]] = []

    for input_path in args.input:
        path = Path(input_path)
        current_headword = ""
        units = extract_text_units(path)
        for unit_locator, unit_text in units:
            for block_locator, block in split_classical_units_to_blocks(unit_locator, unit_text):
                if not block:
                    continue
                lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
                first_line = lines[0] if lines else block[:60]
                if looks_like_headword(first_line):
                    current_headword = first_line
                    headword_rows.append({
                        "source_file": path.name,
                        "source_locator": block_locator,
                        "headword_candidate": current_headword,
                    })
                score = nahuatliness_score(block)
                kind = "definition_like"
                if looks_like_headword(first_line):
                    kind = "headword_like"
                elif (score >= 0.18 and 3 <= len(tokenise_simple(block)) <= 60) or re.search(r"(?i)\b(?:Ex\.|Ej\.)\b", block):
                    kind = "example_like"
                block_rows.append({
                    "source_file": path.name,
                    "source_locator": block_locator,
                    "current_headword": current_headword,
                    "kind": kind,
                    "nahuatliness_score": score,
                    "text": block,
                })
                for i, frag in enumerate(extract_example_fragments(block), start=1):
                    example_rows.append({
                        "source_file": path.name,
                        "source_locator": f"{block_locator}:frag-{i}",
                        "current_headword": current_headword,
                        "nahuatliness_score": nahuatliness_score(frag),
                        "example_text": frag,
                    })
                if kind == "example_like" and not extract_example_fragments(block):
                    if 3 <= len(tokenise_simple(block)) <= 60:
                        example_rows.append({
                            "source_file": path.name,
                            "source_locator": f"{block_locator}:whole",
                            "current_headword": current_headword,
                            "nahuatliness_score": score,
                            "example_text": block,
                        })

    write_jsonl(out_dir / "classical_blocks.jsonl", block_rows)
    write_jsonl(out_dir / "classical_examples.jsonl", example_rows)
    write_csv(out_dir / "headword_candidates.csv", headword_rows, ["source_file", "source_locator", "headword_candidate"])
    summary = {
        "input_files": list(args.input),
        "blocks": len(block_rows),
        "examples": len(example_rows),
        "headword_candidates": len(headword_rows),
        "out_dir": str(out_dir),
    }
    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    log(f"Wrote classical example bank to {out_dir}")
    return 0


# ---------------------------------------------------------------------------
# 4) Nahuatlahtolli lesson HTML -> modern Huasteca grammar/example bank
# ---------------------------------------------------------------------------


def get_html_source(input_value: str) -> Tuple[str, str]:
    if re.match(r"https?://", input_value):
        return input_value, http_get_text(input_value)
    path = Path(input_value)
    with path.open("r", encoding="utf-8", errors="replace") as f:
        return path.name, f.read()



def pick_main_content(soup: BeautifulSoup) -> Any:
    selectors = [
        "article",
        ".entry-content",
        ".post-content",
        "main",
        "#content",
        ".site-content",
        ".content",
    ]
    for selector in selectors:
        node = soup.select_one(selector)
        if node is not None:
            return node
    return soup.body or soup



def normalise_block_text(text: str) -> str:
    text = html.unescape(text)
    text = clean_whitespace(text)
    return text



def detect_grammar_block(section: str, text: str) -> bool:
    blob = f"{section} {text}".lower()
    return any(kw in blob for kw in GRAMMAR_KEYWORDS)



def cmd_nahuatlahtolli_to_bank(args: argparse.Namespace) -> int:
    if BeautifulSoup is None:
        raise RuntimeError("beautifulsoup4 is required for HTML parsing")

    out_dir = Path(args.out)
    ensure_dir(out_dir)

    lesson_rows: List[Dict[str, Any]] = []
    block_rows: List[Dict[str, Any]] = []
    grammar_rows: List[Dict[str, Any]] = []

    for input_value in args.input:
        source_label, html_text = get_html_source(input_value)
        soup = BeautifulSoup(html_text, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "aside", "noscript"]):
            tag.decompose()
        main = pick_main_content(soup)
        title_tag = main.find(["h1", "title"]) if hasattr(main, "find") else None
        page_title = normalise_block_text(title_tag.get_text(" ", strip=True)) if title_tag else ""
        if not page_title:
            page_title = normalise_block_text(soup.title.get_text(" ", strip=True)) if soup.title else source_label
        lesson_match = re.search(r"(Tlamachtiliztli\s+\d+)", page_title, re.I)
        lesson_id = lesson_match.group(1) if lesson_match else page_title[:80]
        lesson_rows.append({
            "source": source_label,
            "lesson_id": lesson_id,
            "page_title": page_title,
        })

        current_section = page_title
        block_index = 0
        for elem in main.descendants:
            name = getattr(elem, "name", None)
            if name in {"h1", "h2", "h3", "h4"}:
                current_section = normalise_block_text(elem.get_text(" ", strip=True))
                continue
            if name in {"p", "li", "blockquote"}:
                text = normalise_block_text(elem.get_text(" ", strip=True))
                if not text or len(text) < args.min_chars:
                    continue
                block_index += 1
                row = {
                    "source": source_label,
                    "lesson_id": lesson_id,
                    "page_title": page_title,
                    "section": current_section,
                    "block_id": f"{slug(lesson_id)}-b{block_index}",
                    "block_type": name,
                    "nahuatliness_score": nahuatliness_score(text),
                    "text": text,
                }
                block_rows.append(row)
                if detect_grammar_block(current_section, text):
                    grammar_rows.append({
                        **row,
                        "kind": "grammar_or_example",
                    })
            elif name == "table":
                rows = []
                for tr in elem.find_all("tr"):
                    cells = [normalise_block_text(td.get_text(" ", strip=True)) for td in tr.find_all(["th", "td"])]
                    cells = [c for c in cells if c]
                    if cells:
                        rows.append(cells)
                if rows:
                    block_index += 1
                    text = " | ".join(" ; ".join(r) for r in rows)
                    row = {
                        "source": source_label,
                        "lesson_id": lesson_id,
                        "page_title": page_title,
                        "section": current_section,
                        "block_id": f"{slug(lesson_id)}-b{block_index}",
                        "block_type": "table",
                        "nahuatliness_score": nahuatliness_score(text),
                        "text": text,
                    }
                    block_rows.append(row)
                    grammar_rows.append({**row, "kind": "grammar_or_example"})

    write_csv(out_dir / "lessons_index.csv", lesson_rows, ["source", "lesson_id", "page_title"])
    write_jsonl(out_dir / "lesson_blocks.jsonl", block_rows)
    write_jsonl(out_dir / "grammar_example_bank.jsonl", grammar_rows)
    summary = {
        "inputs": list(args.input),
        "lessons": len(lesson_rows),
        "blocks": len(block_rows),
        "grammar_or_example_blocks": len(grammar_rows),
        "out_dir": str(out_dir),
    }
    with (out_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    log(f"Wrote Nahuatlahtolli lesson bank to {out_dir}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FCN parsers for Wiktionary, UD, OCR/PDF, and Nahuatlahtolli HTML.")
    sub = parser.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("wiktionary-to-fcn", help="Convert Kaikki/Wiktextract/Wiktionary dumps into FCN lexical rows.")
    p1.add_argument("--input", required=True, help="Input file: unified JSON, Wiktextract JSONL, or XML(.bz2) dump.")
    p1.add_argument("--input-format", default="auto", choices=["auto", "kaikki_unified", "wiktextract_jsonl", "wiktionary_xml"], help="Explicit input type when auto-detection is insufficient.")
    p1.add_argument("--out", required=True, help="Output directory.")
    p1.set_defaults(func=cmd_wiktionary_to_fcn)

    p2 = sub.add_parser("ud-to-grammar", help="Convert CoNLL-U files into grammar evidence tables.")
    p2.add_argument("--input", required=True, nargs="+", help="One or more .conllu files.")
    p2.add_argument("--out", required=True, help="Output directory.")
    p2.set_defaults(func=cmd_ud_to_grammar)

    p3 = sub.add_parser("ia-to-classical-bank", help="Convert public-domain OCR/PDF/JSON sources into a classical example bank.")
    p3.add_argument("--input", required=True, nargs="+", help="One or more .txt, .pdf, or parsed .json inputs.")
    p3.add_argument("--out", required=True, help="Output directory.")
    p3.set_defaults(func=cmd_ia_to_classical_bank)

    p4 = sub.add_parser("nahuatlahtolli-to-bank", help="Convert Nahuatlahtolli lesson HTML into a modern Huasteca lesson bank.")
    p4.add_argument("--input", required=True, nargs="+", help="Local HTML files and/or lesson URLs.")
    p4.add_argument("--out", required=True, help="Output directory.")
    p4.add_argument("--min-chars", type=int, default=25, help="Minimum characters for keeping a text block.")
    p4.set_defaults(func=cmd_nahuatlahtolli_to_bank)

    return parser



def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
