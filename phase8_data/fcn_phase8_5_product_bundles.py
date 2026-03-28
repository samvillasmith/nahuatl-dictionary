#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, shutil, sqlite3
from pathlib import Path

def q(conn, sql):
    cur = conn.execute(sql)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]

def write_csv(path: Path, rows):
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

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
    units = q(conn, "SELECT * FROM v_phase82_unit_plan ORDER BY lesson_number")
    vocab = q(conn, "SELECT * FROM v_phase82_vocab_priority")
    constructions = q(conn, "SELECT * FROM v_phase82_construction_priority")
    dialogues = q(conn, "SELECT * FROM v_phase82_dialogue_samples")
    assessments = q(conn, "SELECT * FROM unit_assessment_manifest ORDER BY lesson_number, item_type")

    app = report_dir / "app_bundle"; app.mkdir(exist_ok=True)
    textbook = report_dir / "textbook_bundle"; textbook.mkdir(exist_ok=True)
    flash = report_dir / "flashcard_bundle"; flash.mkdir(exist_ok=True)
    teacher = report_dir / "teacher_bundle"; teacher.mkdir(exist_ok=True)

    manifest = {
        "units": units,
        "counts": {
            "units": len(units),
            "vocab": len(vocab),
            "constructions": len(constructions),
            "dialogues": len(dialogues),
            "assessments": len(assessments),
        }
    }
    (app / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    (app / "units.json").write_text(json.dumps(units, ensure_ascii=False, indent=2), encoding="utf-8")
    (app / "vocab.json").write_text(json.dumps(vocab, ensure_ascii=False, indent=2), encoding="utf-8")
    (app / "constructions.json").write_text(json.dumps(constructions, ensure_ascii=False, indent=2), encoding="utf-8")
    (app / "dialogues.json").write_text(json.dumps(dialogues, ensure_ascii=False, indent=2), encoding="utf-8")
    (app / "review.json").write_text(json.dumps(assessments, ensure_ascii=False, indent=2), encoding="utf-8")

    toc_lines = ["# FCN Spoken EHN Course — Textbook Bundle\n"]
    for u in units:
        ln = int(u["lesson_number"]); title = u["unit_title"]
        chapter = textbook / f"unit_{ln:02d}.md"
        chapter.write_text(f"# Unit {ln}: {title}\n\nBand: {u['proficiency_band']}\n", encoding="utf-8")
        toc_lines.append(f"- Unit {ln}: {title}")
    (textbook / "TOC.md").write_text("\n".join(toc_lines), encoding="utf-8")

    write_csv(flash / "vocab_deck.csv", vocab)
    write_csv(flash / "construction_deck.csv", constructions)
    write_csv(flash / "dialogue_prompt_deck.csv", dialogues)

    teacher_payload = []
    for u in units:
        teacher_payload.append({
            "lesson_number": u["lesson_number"],
            "unit_title": u["unit_title"],
            "proficiency_band": u["proficiency_band"],
            "objective": f"Teach the core communicative objective of Unit {u['lesson_number']}.",
            "pacing_note": "Single-session or double-session depending on dialogue density.",
            "answer_key_note": "See assessment/review bundle for scaffolded keys."
        })
    write_csv(teacher / "teacher_notes.csv", teacher_payload)

    (report_dir / "phase85_summary.json").write_text(json.dumps({
        "app_bundle_files": 6,
        "textbook_chapters": len(units),
        "flashcard_csvs": 3,
        "teacher_rows": len(teacher_payload)
    }, indent=2), encoding="utf-8")
    conn.close()
    print(f"Phase 8.5 complete: {out_db}")

if __name__ == "__main__":
    main()
