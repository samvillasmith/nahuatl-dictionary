#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil, sqlite3
from pathlib import Path

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS unit_assessment_manifest (
    assessment_id TEXT PRIMARY KEY,
    lesson_number INTEGER,
    proficiency_band TEXT,
    item_type TEXT,
    prompt TEXT
);
"""

def q(conn, sql):
    cur = conn.execute(sql)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]

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
    conn.executescript(SCHEMA_SQL)

    units = q(conn, "SELECT * FROM v_phase82_unit_plan ORDER BY lesson_number")
    items = []
    for u in units:
        ln = int(u["lesson_number"])
        band = u.get("target_band") or u.get("proficiency_band") or ""
        prompts = [
            ("mastery_checklist", f"Can complete the core communicative task for Unit {ln}."),
            ("quiz", f"Answer three comprehension questions for Unit {ln}."),
            ("speaking", f"Produce a short spoken response using Unit {ln} target constructions."),
            ("writing", f"Write 3–5 lines using Unit {ln} vocabulary and constructions."),
            ("review", f"Review Unit {ln} against prior material in the same band."),
        ]
        for i, (typ, prompt) in enumerate(prompts, start=1):
            items.append((f"ASM-{ln:02d}-{i}", ln, band, typ, prompt))

    conn.executemany(
        "INSERT OR REPLACE INTO unit_assessment_manifest(assessment_id, lesson_number, proficiency_band, item_type, prompt) VALUES (?, ?, ?, ?, ?)",
        items
    )
    conn.commit()

    by_band = {}
    for _, _, band, typ, _ in items:
        by_band.setdefault(band, 0)
        by_band[band] += 1

    (report_dir / "phase84_summary.json").write_text(json.dumps({
        "assessment_items": len(items),
        "units_covered": len(units),
        "items_by_band": by_band,
        "item_types": sorted(list({x[3] for x in items}))
    }, indent=2), encoding="utf-8")
    conn.close()
    print(f"Phase 8.4 complete: {out_db}")

if __name__ == "__main__":
    main()
