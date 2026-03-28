#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, shutil, sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS unit_export_manifest (
    export_id TEXT PRIMARY KEY,
    lesson_number INTEGER,
    unit_title TEXT,
    proficiency_band TEXT,
    export_kind TEXT,
    relative_path TEXT
);
"""

def q(conn, sql, params=()):
    cur = conn.execute(sql, params)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]

def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

def values_to_lessons(r):
    nums = []
    if r.get("lessons_json"):
        try:
            nums = [int(x) for x in json.loads(r.get("lessons_json") or "[]") if x is not None]
        except Exception:
            nums = []
    if not nums and r.get("first_lesson_number") not in (None, ""):
        nums = [int(r["first_lesson_number"])]
    return nums

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--out-db", required=True)
    ap.add_argument("--report-dir", required=True)
    args = ap.parse_args()

    in_db = Path(args.db)
    out_db = Path(args.out_db)
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(in_db, out_db)
    conn = sqlite3.connect(out_db)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(SCHEMA_SQL)

    unit_plan = q(conn, "SELECT * FROM v_phase82_unit_plan ORDER BY lesson_number")
    vocab = q(conn, "SELECT * FROM v_phase82_vocab_priority")
    constr = q(conn, "SELECT * FROM v_phase82_construction_priority")
    dialogues = q(conn, "SELECT * FROM v_phase82_dialogue_samples ORDER BY lesson_number, dialogue_order")

    by_lesson_vocab = {}
    for r in vocab:
        for n in values_to_lessons(r):
            rr = dict(r)
            rr["lesson_number"] = int(n)
            by_lesson_vocab.setdefault(int(n), []).append(rr)

    by_lesson_con = {}
    for r in constr:
        for n in values_to_lessons(r):
            rr = dict(r)
            rr["lesson_number"] = int(n)
            by_lesson_con.setdefault(int(n), []).append(rr)

    by_lesson_dia = {}
    for r in dialogues:
        by_lesson_dia.setdefault(int(r["lesson_number"]), []).append(dict(r))

    exports_root = report_dir / "unit_exports"
    (exports_root / "markdown").mkdir(parents=True, exist_ok=True)
    (exports_root / "json").mkdir(parents=True, exist_ok=True)
    (exports_root / "csv").mkdir(parents=True, exist_ok=True)
    (exports_root / "printable").mkdir(parents=True, exist_ok=True)

    manifest = []
    for idx, unit in enumerate(unit_plan, start=1):
        ln = int(unit["lesson_number"])
        title = unit.get("theme_en") or unit.get("english_lesson_title") or unit.get("spanish_lesson_title") or f"Unit {ln}"
        band = unit.get("target_band") or ""
        unit_slug = f"unit_{ln:02d}"
        lesson_overview = {
            "communicative_goal": unit.get("communicative_goal", ""),
            "grammar_focus": unit.get("grammar_focus", ""),
            "theme_focus": unit.get("theme_en", ""),
            "output_task": unit.get("output_task", ""),
            "domain_label": unit.get("domain_label", ""),
        }
        unit_payload = {
            "lesson_number": ln,
            "unit_title": title,
            "proficiency_band": band,
            "english_lesson_title": unit.get("english_lesson_title", ""),
            "spanish_lesson_title": unit.get("spanish_lesson_title", ""),
            "lesson_overview": lesson_overview,
            "target_vocab": by_lesson_vocab.get(ln, [])[:60],
            "target_constructions": by_lesson_con.get(ln, [])[:30],
            "dialogue_set": by_lesson_dia.get(ln, [])[:6],
            "exercises": [
                {"type": "substitution", "prompt": f"Use a target construction from Unit {ln} with new lexical fills."},
                {"type": "comprehension", "prompt": f"Answer questions about the Unit {ln} dialogue set."},
                {"type": "production", "prompt": f"Produce a short response using Unit {ln} vocabulary."},
            ],
            "quiz_review_items": [
                {"type": "recall", "prompt": f"Recall five Unit {ln} vocabulary items."},
                {"type": "dialogue", "prompt": f"Complete one missing line from a Unit {ln} dialogue."},
                {"type": "construction", "prompt": f"Transform a sentence using a Unit {ln} construction."},
            ],
        }
        jp = exports_root / "json" / f"{unit_slug}.json"
        jp.write_text(json.dumps(unit_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest.append((f"EXP-{idx:04d}", ln, title, band, "json", str(jp.relative_to(report_dir))))

        md = exports_root / "markdown" / f"{unit_slug}.md"
        vocab_lines = "\n".join(
            f"- {r.get('headword', r.get('surface_form', r.get('form_text','')))} — {r.get('gloss_en','')}"
            for r in unit_payload["target_vocab"][:20]
        )
        con_lines = "\n".join(
            f"- {r.get('pattern_text','')}"
            for r in unit_payload["target_constructions"][:15]
        )
        dia_lines = "\n".join(
            f"- {r.get('speaker_label','')}: {r.get('utterance_original', r.get('example_original',''))}"
            for r in unit_payload["dialogue_set"][:4]
        )
        md_text = (
            f"# Unit {ln}: {title}\n\n"
            f"## Band\n{band}\n\n"
            f"## Overview\n"
            f"- communicative goal: {lesson_overview['communicative_goal']}\n"
            f"- grammar focus: {lesson_overview['grammar_focus']}\n"
            f"- theme focus: {lesson_overview['theme_focus']}\n"
            f"- output task: {lesson_overview['output_task']}\n\n"
            f"## Target vocab\n{vocab_lines}\n\n"
            f"## Target constructions\n{con_lines}\n\n"
            f"## Dialogue set\n{dia_lines}\n"
        )
        md.write_text(md_text, encoding="utf-8")
        manifest.append((f"EXP-{idx+1000:04d}", ln, title, band, "markdown", str(md.relative_to(report_dir))))

        cp = exports_root / "csv" / f"{unit_slug}_vocab.csv"
        write_csv(cp, unit_payload["target_vocab"])
        manifest.append((f"EXP-{idx+2000:04d}", ln, title, band, "csv_vocab", str(cp.relative_to(report_dir))))

        pp = exports_root / "printable" / f"{unit_slug}_packet.md"
        pp.write_text(md_text + "\n## Review items\n" + "\n".join(f"- {x['prompt']}" for x in unit_payload["quiz_review_items"]), encoding="utf-8")
        manifest.append((f"EXP-{idx+3000:04d}", ln, title, band, "printable", str(pp.relative_to(report_dir))))

    conn.executemany(
        "INSERT OR REPLACE INTO unit_export_manifest(export_id, lesson_number, unit_title, proficiency_band, export_kind, relative_path) VALUES (?, ?, ?, ?, ?, ?)",
        manifest
    )
    conn.commit()

    summary = {
        "units_exported": len(unit_plan),
        "json_exports": len(unit_plan),
        "markdown_exports": len(unit_plan),
        "csv_vocab_exports": len(unit_plan),
        "printable_packets": len(unit_plan),
        "manifest_rows": len(manifest),
    }
    (report_dir / "phase83_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    conn.close()
    print(f"Phase 8.3 complete: {out_db}")

if __name__ == "__main__":
    main()
