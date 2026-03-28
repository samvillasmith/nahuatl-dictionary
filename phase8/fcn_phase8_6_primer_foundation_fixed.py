#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, shutil, sqlite3
from pathlib import Path
from typing import Any

def rows(conn: sqlite3.Connection, sql: str, params: tuple=()) -> list[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, params)
    return [dict(r) for r in cur.fetchall()]

def write_csv(path: Path, rows_: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows_:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows_[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows_)

def lesson_nums_from_row(r: dict[str, Any]) -> list[int]:
    vals: list[int] = []
    if r.get("lessons_json"):
        try:
            vals = [int(x) for x in json.loads(r["lessons_json"] or "[]")]
        except Exception:
            vals = []
    if not vals and r.get("first_lesson_number") is not None:
        try:
            vals = [int(r["first_lesson_number"])]
        except Exception:
            vals = []
    if not vals and r.get("lesson_number") is not None:
        try:
            vals = [int(r["lesson_number"])]
        except Exception:
            vals = []
    return vals

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--out-db", required=True)
    ap.add_argument("--report-dir", required=True)
    args = ap.parse_args()

    in_db = Path(args.db)
    out_db = Path(args.out_db)
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    if not in_db.exists():
        raise SystemExit(f"Input DB not found: {in_db}")

    if out_db.exists():
        out_db.unlink()
    shutil.copy2(in_db, out_db)

    conn = sqlite3.connect(str(out_db))
    conn.row_factory = sqlite3.Row

    units = rows(conn, "SELECT * FROM v_phase82_unit_plan ORDER BY lesson_number")
    vocab = rows(conn, "SELECT * FROM v_phase82_vocab_priority")
    constructions = rows(conn, "SELECT * FROM v_phase82_construction_priority")
    dialogues = rows(conn, "SELECT * FROM v_phase82_dialogue_samples")

    primer_units = []
    b1_taken = 0
    for u in units:
        band = u.get("target_band") or u.get("proficiency_band") or ""
        ln = int(u["lesson_number"])
        include = False
        tier = None
        if band == "A1":
            include = True
            tier = "core_a1"
        elif band == "A2":
            include = True
            tier = "core_a2"
        elif band == "B1" and b1_taken < 4:
            include = True
            tier = "bridge_b1"
            b1_taken += 1
        if include:
            primer_units.append({
                "lesson_number": ln,
                "target_band": band,
                "primer_tier": tier,
                "theme_en": u.get("theme_en"),
                "english_lesson_title": u.get("english_lesson_title"),
                "spanish_lesson_title": u.get("spanish_lesson_title"),
            })

    primer_numbers = {u["lesson_number"] for u in primer_units}

    primer_vocab = [r for r in vocab if any(n in primer_numbers for n in lesson_nums_from_row(r))]
    primer_constructions = [r for r in constructions if any(n in primer_numbers for n in lesson_nums_from_row(r))]
    primer_dialogues = [r for r in dialogues if any(n in primer_numbers for n in lesson_nums_from_row(r))]

    contamination_hits = []
    check_fields = ["register_status","status","register","notes_internal","notes_public","category","confidence","source_basis"]
    for collection_name, coll in [("vocab", primer_vocab), ("construction", primer_constructions), ("dialogue", primer_dialogues)]:
        for r in coll:
            blob = " ".join(str(r.get(f,"")) for f in check_fields).lower()
            if any(k in blob for k in ["classical-only","classical_only","ceremonial"]):
                contamination_hits.append({"collection": collection_name, **{k:v for k,v in r.items() if k in ("headword","pattern_text","utterance_original","lesson_number","first_lesson_number","lessons_json","register_status","status","register")}})

    conn.executescript("""
    DROP TABLE IF EXISTS primer_units;
    DROP TABLE IF EXISTS primer_vocab;
    DROP TABLE IF EXISTS primer_constructions;
    DROP TABLE IF EXISTS primer_dialogues;
    CREATE TABLE primer_units (
        lesson_number INTEGER PRIMARY KEY,
        target_band TEXT,
        primer_tier TEXT,
        theme_en TEXT,
        english_lesson_title TEXT,
        spanish_lesson_title TEXT
    );
    CREATE TABLE primer_vocab AS SELECT * FROM v_phase82_vocab_priority WHERE 0;
    CREATE TABLE primer_constructions AS SELECT * FROM v_phase82_construction_priority WHERE 0;
    CREATE TABLE primer_dialogues AS SELECT * FROM v_phase82_dialogue_samples WHERE 0;
    """)
    conn.executemany(
        "INSERT INTO primer_units (lesson_number,target_band,primer_tier,theme_en,english_lesson_title,spanish_lesson_title) VALUES (?,?,?,?,?,?)",
        [(r["lesson_number"], r["target_band"], r["primer_tier"], r["theme_en"], r["english_lesson_title"], r["spanish_lesson_title"]) for r in primer_units]
    )

    def insert_dynamic(table: str, rows_: list[dict[str, Any]]):
        if not rows_:
            return
        cols = list(rows_[0].keys())
        placeholders = ",".join(["?"]*len(cols))
        sql = f'INSERT INTO {table} ({",".join(cols)}) VALUES ({placeholders})'
        conn.executemany(sql, [[r.get(c) for c in cols] for r in rows_])

    insert_dynamic("primer_vocab", primer_vocab)
    insert_dynamic("primer_constructions", primer_constructions)
    insert_dynamic("primer_dialogues", primer_dialogues)

    conn.executescript("""
    DROP VIEW IF EXISTS v_phase86_primer_unit_plan;
    DROP VIEW IF EXISTS v_phase86_primer_vocab;
    DROP VIEW IF EXISTS v_phase86_primer_constructions;
    DROP VIEW IF EXISTS v_phase86_primer_dialogues;
    CREATE VIEW v_phase86_primer_unit_plan AS SELECT * FROM primer_units ORDER BY lesson_number;
    CREATE VIEW v_phase86_primer_vocab AS SELECT * FROM primer_vocab;
    CREATE VIEW v_phase86_primer_constructions AS SELECT * FROM primer_constructions;
    CREATE VIEW v_phase86_primer_dialogues AS SELECT * FROM primer_dialogues;
    """)
    conn.commit()
    conn.close()

    write_csv(report_dir / "phase86_primer_units.csv", primer_units)
    write_csv(report_dir / "phase86_contamination_hits.csv", contamination_hits)
    summary = {
        "primer_units": len(primer_units),
        "primer_a1_units": sum(1 for r in primer_units if r["target_band"] == "A1"),
        "primer_a2_units": sum(1 for r in primer_units if r["target_band"] == "A2"),
        "primer_b1_bridge_units": sum(1 for r in primer_units if r["target_band"] == "B1"),
        "primer_vocab_items": len(primer_vocab),
        "primer_constructions": len(primer_constructions),
        "primer_dialogues": len(primer_dialogues),
        "contamination_hits": len(contamination_hits),
        "contamination_status": "clean" if not contamination_hits else "needs_review",
    }
    (report_dir / "phase86_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Phase 8.6 complete: {out_db.name}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
