#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sqlite3
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from html import unescape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    from bs4 import BeautifulSoup
except Exception as exc:  # pragma: no cover
    raise SystemExit("beautifulsoup4 is required for Phase 8 ingestion") from exc

USER_AGENT = "FCN-phase8-open-only/0.1"
TIMEOUT = 60

NAHUATL_CUES_RE = re.compile(
    r"(?i)(?:tl|tz|ch|hu|uh|qu|cu|[āēīōūç]|tli\b|tl\b|meh\b|tin\b|tzin\b|yotl\b|ni-|mo-|ti-|qui-|tla-)"
)
WORD_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑÇāēīōūç'’\-]+")
DIALOGUE_LINE_RE = re.compile(r"^([A-ZÁÉÍÓÚÜÑÇa-zāēīōūç][^:]{0,40}):\s+(.+)$")


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def clean(text: str) -> str:
    text = unescape(text or "")
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "item"


def nahuatliness_score(text: str) -> float:
    toks = WORD_RE.findall(text)
    if not toks:
        return 0.0
    hits = sum(1 for tok in toks if NAHUATL_CUES_RE.search(tok))
    bonus = 1 if re.search(r"[āēīōūç]", text) else 0
    score = (hits + bonus) / max(len(toks), 1)
    return round(min(score, 1.0), 4)


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 8 open-only builder for FCN + Nāhuatlahtolli.")
    p.add_argument("--db", required=True, help="Existing FCN SQLite DB.")
    p.add_argument("--schema", required=True, help="Phase 8 schema SQL.")
    p.add_argument("--config", required=True, help="Open-only source config JSON.")
    p.add_argument("--out-db", required=True, help="Output SQLite DB path.")
    p.add_argument("--report-dir", required=True, help="Report/output directory.")
    p.add_argument("--lesson-bank-dir", help="Optional existing nahuatlahtolli-to-bank output directory.")
    p.add_argument("--crawl", action="store_true", help="Fetch Nahuatlahtolli pages directly from root URLs.")
    p.add_argument("--max-pages", type=int, default=40)
    p.add_argument("--bootstrap-only", action="store_true", help="Apply schema and register sources without ingesting lesson data.")
    return p.parse_args(argv)


def register_source(conn: sqlite3.Connection, source: Dict[str, Any]) -> None:
    cols = [
        "source_id", "source_file", "source_type", "upstream_title", "provenance_note", "license",
        "retrieval_or_creation_date", "project_role", "authority_domain", "limitations", "canonical_status", "notes"
    ]
    row = {k: source.get(k) for k in cols}
    existing = conn.execute(
        "SELECT source_id FROM sources WHERE source_id = ? OR source_file = ? LIMIT 1",
        (row.get("source_id"), row.get("source_file")),
    ).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE sources
            SET source_file = ?, source_type = ?, upstream_title = ?, provenance_note = ?,
                license = ?, retrieval_or_creation_date = COALESCE(?, retrieval_or_creation_date),
                project_role = ?, authority_domain = ?, limitations = ?, canonical_status = ?, notes = ?
            WHERE source_id = ?
            """,
            (
                row.get("source_file"), row.get("source_type"), row.get("upstream_title"), row.get("provenance_note"),
                row.get("license"), row.get("retrieval_or_creation_date"), row.get("project_role"), row.get("authority_domain"),
                row.get("limitations"), row.get("canonical_status"), row.get("notes"), existing[0],
            ),
        )
    else:
        conn.execute(
            f"INSERT INTO sources ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",
            [row.get(c) for c in cols],
        )


def extract_links(base_url: str, html_text: str, include_markers: List[str], same_host_only: bool) -> List[str]:
    soup = BeautifulSoup(html_text, "lxml")
    out: List[str] = []
    base_host = urllib.parse.urlparse(base_url).netloc
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        if not href:
            continue
        abs_url = urllib.parse.urljoin(base_url, href)
        parsed = urllib.parse.urlparse(abs_url)
        if same_host_only and parsed.netloc != base_host:
            continue
        url_l = abs_url.lower()
        if include_markers and not any(marker in url_l for marker in include_markers):
            continue
        if abs_url not in out:
            out.append(abs_url)
    return out


def crawl_root_urls(source: Dict[str, Any], max_pages: int) -> List[Tuple[str, str]]:
    root_urls = source.get("root_urls") or []
    if not root_urls:
        return []
    include_markers = (source.get("crawl_rules") or {}).get("include_if_url_contains") or []
    exclude_markers = (source.get("crawl_rules") or {}).get("exclude_if_url_contains") or []
    same_host_only = bool((source.get("crawl_rules") or {}).get("same_host_only", True))

    seen: Set[str] = set()
    queue: List[str] = list(root_urls)
    pages: List[Tuple[str, str]] = []

    while queue and len(pages) < max_pages:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            html_text = http_get(url)
        except Exception as exc:
            log(f"WARN could not fetch {url}: {exc}")
            continue
        pages.append((url, html_text))
        for candidate in extract_links(url, html_text, include_markers, same_host_only):
            if any(marker in candidate.lower() for marker in exclude_markers):
                continue
            if candidate not in seen and candidate not in queue:
                queue.append(candidate)
    return pages


def parse_html_lessons(pages: List[Tuple[str, str]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    lessons: List[Dict[str, Any]] = []
    blocks: List[Dict[str, Any]] = []
    vocab: List[Dict[str, Any]] = []
    lesson_order = 0
    for url, html_text in pages:
        soup = BeautifulSoup(html_text, "lxml")
        for tag in soup(["script", "style", "nav", "footer", "aside", "noscript"]):
            tag.decompose()
        main = soup.find("article") or soup.find("main") or soup.find(id="content") or soup.body or soup
        title_tag = main.find(["h1", "title"]) if main else None
        page_title = clean(title_tag.get_text(" ", strip=True) if title_tag else (soup.title.get_text(" ", strip=True) if soup.title else url))
        if not page_title:
            continue
        if len(page_title) > 200:
            page_title = page_title[:200]
        lesson_order += 1
        lesson_slug = slug(f"{lesson_order:04d}-" + page_title + "-" + urllib.parse.urlparse(url).path)
        lesson_id = f"FCN-LSN-{lesson_order:04d}"
        band = "A1"
        lower_title = page_title.lower()
        if any(tok in lower_title for tok in ["6", "7", "8", "9", "10", "advanced"]):
            band = "B1"
        elif any(tok in lower_title for tok in ["intermediate", "4", "5"]):
            band = "A2"
        lessons.append({
            "lesson_unit_id": lesson_id,
            "lesson_slug": lesson_slug,
            "lesson_title": page_title,
            "lesson_url": url,
            "lesson_order": lesson_order,
            "proficiency_band": band,
            "domain_label": "Nahuatlahtolli",
            "summary": "Auto-harvested from open lesson HTML.",
            "source_reference": url,
        })
        current_section = page_title
        block_order = 0
        for elem in main.find_all(["h2", "h3", "h4", "p", "li", "blockquote", "table"]):
            if elem.name in {"h2", "h3", "h4"}:
                current_section = clean(elem.get_text(" ", strip=True)) or current_section
                continue
            text = clean(elem.get_text(" ", strip=True))
            if len(text) < 25:
                continue
            block_order += 1
            block_id = f"{lesson_id}-B{block_order:03d}"
            blocks.append({
                "lesson_block_id": block_id,
                "lesson_unit_id": lesson_id,
                "block_order": block_order,
                "block_type": elem.name,
                "section_label": current_section,
                "text_original": text,
                "text_normalized": text,
                "translation_en": None,
                "translation_es": None,
                "nahuatliness_score": nahuatliness_score(text),
                "attestation_tier": "Lesson_attested",
                "notes": None,
            })
            for line in re.split(r"\s{2,}|\n+", text):
                m = DIALOGUE_LINE_RE.match(line)
                if m:
                    speaker, utt = m.groups()
                    blocks[-1].setdefault("dialogue_lines", []).append((speaker.strip(), utt.strip()))
            tokens = [tok for tok in WORD_RE.findall(text) if len(tok) >= 3 and NAHUATL_CUES_RE.search(tok)]
            freq = defaultdict(int)
            for tok in tokens:
                freq[tok.lower()] += 1
            for tok, count in list(freq.items())[:12]:
                vocab.append({
                    "lesson_unit_id": lesson_id,
                    "surface_form": tok,
                    "normalized_form": tok,
                    "gloss_en": None,
                    "gloss_es": None,
                    "part_of_speech": None,
                    "variety": "Eastern Huasteca Nahuatl",
                    "register": "EHN_colloquial",
                    "count": count,
                })
    return lessons, blocks, vocab


def load_lesson_bank(lesson_bank_dir: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    lessons_index = lesson_bank_dir / "lessons_index.csv"
    blocks_jsonl = lesson_bank_dir / "lesson_blocks.jsonl"
    if not lessons_index.exists() or not blocks_jsonl.exists():
        raise FileNotFoundError("lesson_bank_dir must contain lessons_index.csv and lesson_blocks.jsonl")

    lessons: List[Dict[str, Any]] = []
    with lessons_index.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            lesson_id = f"FCN-LSN-{i:04d}"
            title = row.get("page_title") or row.get("lesson_id") or f"Lesson {i}"
            lessons.append({
                "lesson_unit_id": lesson_id,
                "lesson_slug": slug(row.get("lesson_id") or title),
                "lesson_title": title,
                "lesson_url": row.get("source"),
                "lesson_order": i,
                "proficiency_band": "A1",
                "domain_label": "Nahuatlahtolli",
                "summary": "Imported from nahuatlahtolli-to-bank output.",
                "source_reference": row.get("source"),
            })
    lesson_map = {l["lesson_title"]: l["lesson_unit_id"] for l in lessons}
    blocks: List[Dict[str, Any]] = []
    vocab: List[Dict[str, Any]] = []
    order_by_lesson = defaultdict(int)
    with blocks_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            lesson_title = row.get("page_title") or row.get("lesson_id") or "Unknown Lesson"
            lesson_id = lesson_map.get(lesson_title)
            if not lesson_id:
                continue
            order_by_lesson[lesson_id] += 1
            block_id = f"{lesson_id}-B{order_by_lesson[lesson_id]:03d}"
            text = clean(row.get("text") or "")
            if not text:
                continue
            blocks.append({
                "lesson_block_id": block_id,
                "lesson_unit_id": lesson_id,
                "block_order": order_by_lesson[lesson_id],
                "block_type": row.get("block_type") or "p",
                "section_label": row.get("section"),
                "text_original": text,
                "text_normalized": text,
                "translation_en": None,
                "translation_es": None,
                "nahuatliness_score": float(row.get("nahuatliness_score") or 0.0),
                "attestation_tier": "Lesson_attested",
                "notes": None,
            })
            for tok in {t.lower() for t in WORD_RE.findall(text) if len(t) >= 3 and NAHUATL_CUES_RE.search(t)}:
                vocab.append({
                    "lesson_unit_id": lesson_id,
                    "surface_form": tok,
                    "normalized_form": tok,
                    "gloss_en": None,
                    "gloss_es": None,
                    "part_of_speech": None,
                    "variety": "Eastern Huasteca Nahuatl",
                    "register": "EHN_colloquial",
                    "count": 1,
                })
    return lessons, blocks, vocab


def align_vocab(conn: sqlite3.Connection, vocab_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    index: Dict[str, Tuple[str, str, str, str]] = {}
    for row in conn.execute(
        "SELECT entry_id, lower(coalesce(ehn_spoken_form,'')), lower(coalesce(msn_headword,'')), coalesce(gloss_en,''), coalesce(part_of_speech,'') FROM lexicon_entries"
    ):
        entry_id, ehn, msn, gloss, pos = row
        if ehn:
            index.setdefault(ehn, (entry_id, ehn, gloss, pos))
        if msn:
            index.setdefault(msn, (entry_id, msn, gloss, pos))
    out: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str]] = set()
    for i, row in enumerate(vocab_rows, start=1):
        key = (row["lesson_unit_id"], row["surface_form"])
        if key in seen:
            continue
        seen.add(key)
        form = row["surface_form"].lower()
        linked = index.get(form)
        out.append({
            "lesson_vocab_id": f"FCN-LVC-{i:06d}",
            "lesson_unit_id": row["lesson_unit_id"],
            "surface_form": row["surface_form"],
            "normalized_form": row.get("normalized_form") or row["surface_form"],
            "gloss_en": linked[2] if linked else row.get("gloss_en"),
            "gloss_es": row.get("gloss_es"),
            "part_of_speech": linked[3] if linked else row.get("part_of_speech"),
            "variety": row.get("variety") or "Eastern Huasteca Nahuatl",
            "register": row.get("register") or "EHN_colloquial",
            "linked_entry_id": linked[0] if linked else None,
            "confidence": 0.9 if linked else 0.4,
            "attestation_tier": "Lesson_attested",
        })
    return out


def derive_dialogues(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    idx = 0
    for block in blocks:
        text = block["text_original"]
        lines = re.split(r"(?:(?<=\.)\s+)|\n+", text)
        local_order = 0
        for line in lines:
            m = DIALOGUE_LINE_RE.match(line.strip())
            if not m:
                continue
            speaker, utt = m.groups()
            idx += 1
            local_order += 1
            out.append({
                "lesson_dialogue_id": f"FCN-LDG-{idx:06d}",
                "lesson_unit_id": block["lesson_unit_id"],
                "block_id": block["lesson_block_id"],
                "dialogue_order": local_order,
                "speaker_label": clean(speaker),
                "utterance_original": clean(utt),
                "utterance_normalized": clean(utt),
                "translation_en": None,
                "translation_es": None,
                "communicative_function": block.get("section_label") or "dialogue",
                "attestation_tier": "Lesson_attested",
            })
    return out


def derive_pedagogical_units(lessons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    units: List[Dict[str, Any]] = []
    for i, lesson in enumerate(lessons, start=1):
        units.append({
            "pedagogical_unit_id": f"FCN-PED-{i:04d}",
            "unit_code": f"U{i:02d}",
            "unit_title": lesson["lesson_title"],
            "target_band": lesson["proficiency_band"],
            "domain_label": lesson.get("domain_label") or "General",
            "lesson_unit_id": lesson["lesson_unit_id"],
            "communicative_goal": f"Use lesson {i} material for spoken interaction and controlled practice.",
            "grammar_focus": "Derived from lesson content and construction bank.",
            "lexical_focus": "Core lesson vocabulary aligned to FCN lexicon.",
            "output_task": "Dialogue performance, substitution drill, short narration.",
            "editorial_status": "Imported_raw",
        })
    return units


def derive_constructions(source_id: str, blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    constructions: List[Dict[str, Any]] = []
    idx = 0
    for block in blocks:
        text = block["text_original"]
        if len(text.split()) < 3:
            continue
        if nahuatliness_score(text) < 0.12:
            continue
        idx += 1
        tokens = WORD_RE.findall(text)[:12]
        pattern = " ".join(tokens)
        constructions.append({
            "construction_id": f"FCN-CXN-{idx:06d}",
            "source_id": source_id,
            "lesson_unit_id": block["lesson_unit_id"],
            "source_block_id": block["lesson_block_id"],
            "proficiency_band": "A1" if idx <= 100 else ("A2" if idx <= 220 else "B1"),
            "domain_label": block.get("section_label") or "General",
            "construction_label": f"Construction {idx}",
            "pattern_text": pattern,
            "slot_schema_json": json_dumps({"tokens": tokens}),
            "example_original": text,
            "example_normalized": text,
            "explanation": "Auto-derived candidate construction from open lesson material.",
            "attestation_tier": "Lesson_attested",
            "confidence": min(0.95, 0.45 + nahuatliness_score(text)),
        })
        if idx >= 350:
            break
    return constructions


def apply_schema(conn: sqlite3.Connection, schema_path: Path) -> None:
    conn.executescript(read_text(schema_path))


def exec_many(conn: sqlite3.Connection, sql: str, rows: Iterable[Tuple[Any, ...]]) -> None:
    conn.executemany(sql, list(rows))


def write_reports(report_dir: Path, lessons: List[Dict[str, Any]], blocks: List[Dict[str, Any]], dialogs: List[Dict[str, Any]], vocab: List[Dict[str, Any]], constructions: List[Dict[str, Any]]) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "lessons": len(lessons),
        "blocks": len(blocks),
        "dialogues": len(dialogs),
        "vocab_items": len(vocab),
        "construction_candidates": len(constructions),
    }
    (report_dir / "phase8_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (report_dir / "phase8_lessons.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["lesson_unit_id", "lesson_title", "lesson_url", "proficiency_band", "lesson_order"])
        writer.writeheader()
        for row in lessons:
            writer.writerow({k: row.get(k) for k in writer.fieldnames})
    with (report_dir / "phase8_constructions.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["construction_id", "proficiency_band", "domain_label", "pattern_text", "example_original", "confidence"])
        writer.writeheader()
        for row in constructions:
            writer.writerow({k: row.get(k) for k in writer.fieldnames})


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    in_db = Path(args.db)
    out_db = Path(args.out_db)
    out_db.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(in_db, out_db)

    config = load_json(Path(args.config))
    open_sources = config.get("sources") or []
    nh_source = next((s for s in open_sources if s.get("source_id") == "FCN-SRC-NHTL-001"), None)
    if not nh_source:
        raise SystemExit("Config must include FCN-SRC-NHTL-001")

    conn = sqlite3.connect(str(out_db))
    conn.execute("PRAGMA foreign_keys = ON")
    apply_schema(conn, Path(args.schema))
    for source in open_sources:
        register_source(conn, source)
    conn.commit()

    if args.bootstrap_only:
        lessons, blocks, vocab_seed = [], [], []
    elif args.lesson_bank_dir:
        lessons, blocks, vocab_seed = load_lesson_bank(Path(args.lesson_bank_dir))
    elif args.crawl:
        pages = crawl_root_urls(nh_source, args.max_pages)
        if not pages:
            raise SystemExit("No pages fetched; try --lesson-bank-dir, --bootstrap-only, or run in a networked environment.")
        lessons, blocks, vocab_seed = parse_html_lessons(pages)
    else:
        raise SystemExit("Provide --lesson-bank-dir, enable --crawl, or use --bootstrap-only")

    vocab = align_vocab(conn, vocab_seed)
    dialogues = derive_dialogues(blocks)
    pedagogical_units = derive_pedagogical_units(lessons)
    constructions = derive_constructions("FCN-SRC-NHTL-001", blocks)

    conn.executemany(
        """
        INSERT OR REPLACE INTO lesson_units (
            lesson_unit_id, source_id, lesson_slug, lesson_title, lesson_url, lesson_order,
            proficiency_band, domain_label, summary, source_reference, editorial_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(
            row["lesson_unit_id"], "FCN-SRC-NHTL-001", row["lesson_slug"], row["lesson_title"], row.get("lesson_url"),
            row.get("lesson_order"), row.get("proficiency_band"), row.get("domain_label"), row.get("summary"),
            row.get("source_reference"), "Imported_raw"
        ) for row in lessons],
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO lesson_blocks (
            lesson_block_id, lesson_unit_id, block_order, block_type, section_label,
            text_original, text_normalized, translation_en, translation_es,
            nahuatliness_score, attestation_tier, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(
            row["lesson_block_id"], row["lesson_unit_id"], row["block_order"], row["block_type"], row.get("section_label"),
            row["text_original"], row.get("text_normalized"), row.get("translation_en"), row.get("translation_es"),
            row.get("nahuatliness_score", 0.0), row.get("attestation_tier", "Lesson_attested"), row.get("notes")
        ) for row in blocks],
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO lesson_dialogues (
            lesson_dialogue_id, lesson_unit_id, block_id, dialogue_order, speaker_label,
            utterance_original, utterance_normalized, translation_en, translation_es,
            communicative_function, attestation_tier
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(
            row["lesson_dialogue_id"], row["lesson_unit_id"], row.get("block_id"), row["dialogue_order"], row.get("speaker_label"),
            row["utterance_original"], row.get("utterance_normalized"), row.get("translation_en"), row.get("translation_es"),
            row.get("communicative_function"), row.get("attestation_tier", "Lesson_attested")
        ) for row in dialogues],
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO lesson_vocab (
            lesson_vocab_id, lesson_unit_id, surface_form, normalized_form, gloss_en, gloss_es,
            part_of_speech, variety, register, linked_entry_id, confidence, attestation_tier
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(
            row["lesson_vocab_id"], row["lesson_unit_id"], row["surface_form"], row.get("normalized_form"), row.get("gloss_en"), row.get("gloss_es"),
            row.get("part_of_speech"), row.get("variety"), row.get("register"), row.get("linked_entry_id"), row.get("confidence", 0.5), row.get("attestation_tier", "Lesson_attested")
        ) for row in vocab],
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO pedagogical_units (
            pedagogical_unit_id, unit_code, unit_title, target_band, domain_label,
            lesson_unit_id, communicative_goal, grammar_focus, lexical_focus,
            output_task, editorial_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(
            row["pedagogical_unit_id"], row["unit_code"], row["unit_title"], row["target_band"], row.get("domain_label"),
            row.get("lesson_unit_id"), row.get("communicative_goal"), row.get("grammar_focus"), row.get("lexical_focus"), row.get("output_task"), row.get("editorial_status", "Imported_raw")
        ) for row in pedagogical_units],
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO construction_bank (
            construction_id, source_id, lesson_unit_id, source_block_id, proficiency_band,
            domain_label, construction_label, pattern_text, slot_schema_json,
            example_original, example_normalized, explanation, attestation_tier, confidence
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [(
            row["construction_id"], row["source_id"], row.get("lesson_unit_id"), row.get("source_block_id"), row.get("proficiency_band"), row.get("domain_label"),
            row["construction_label"], row["pattern_text"], row.get("slot_schema_json"), row.get("example_original"), row.get("example_normalized"),
            row.get("explanation"), row.get("attestation_tier", "Lesson_attested"), row.get("confidence", 0.5)
        ) for row in constructions],
    )
    conn.commit()
    write_reports(Path(args.report_dir), lessons, blocks, dialogues, vocab, constructions)
    conn.close()
    log(f"Phase 8 open-only build complete: {out_db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
