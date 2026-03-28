#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

LESSON_RE = re.compile(r'^\s*Tlamachtiliztli\s+(\d+)\b', re.I)
PAREN_TAIL_RE = re.compile(r'\(([^()]*)\)\s*$')

EN_MARKERS = [
    'the alphabet', 'questions', 'what is your name', 'colors and numbers', 'the professions',
    'intransitive verbs', 'how to divide up the day', 'possessive markers', 'the family',
    'my appearance', 'when you greet', 'future tense', 'past tense', 'stand up',
    'our cornfield', 'inside the house', 'i had gone to the city', 'conditional',
    'non-specific object markers', 'what illnesses do you know', 'i was passing by your house',
    'i came to buy', 'it’s market day', "it's market day", 'what we have in the field',
    'what i like', 'and say farewell', 'the grammar of', 'how to divide', 'chair'
]
ES_MARKERS = [
    'el alfabeto', 'preguntas', '¿cómo te llamas', 'los colores', 'los números', 'las profesiones',
    'verbos', 'cómo se divide', 'marcadores posesivos', 'la familia', 'mi apariencia',
    'cuando se saluda', 'cuando se despide', 'tiempo futuro', 'pretérito', 'parte 1', 'parte 2',
    'parte 3', 'yo me siento', 'que me gusta', '¡levántate', 'la gramática', 'la milpa',
    'nuestra comida', 'que hay dentro', 'yo había ido a la ciudad', 'ahorita hay mercado',
    'yo pasaba por tu casa', '¿cuáles enfermedades', 'modo condicional', 'objetos no específicos',
    'las ceremonias de limpia', 'sufijos', 'como se divide', 'como te llamas'
]
NON_LESSON_EXACT = {
    'language', 'funding', 'team', 'resources', 'units', 'introduction', 'contact',
    'idioma', 'fondos', 'equipo', 'recursos', 'unidades', 'introducción', 'introduccion', 'contacto'
}


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', (text or '').strip())


def infer_locale(title: str, url: str = "") -> str:
    u = (url or "").lower()
    if "/es/" in u or "leccion" in u:
        return "es"
    if "lesson" in u:
        return "en"
    t = clean(title).lower()
    tail = ''
    m = PAREN_TAIL_RE.search(t)
    if m:
        tail = m.group(1).lower()
    blob = f'{t} {tail}'
    en_score = sum(1 for m in EN_MARKERS if m in blob)
    es_score = sum(1 for m in ES_MARKERS if m in blob)
    if '¿cómo' in blob or '¿cuáles' in blob or '¡' in blob:
        es_score += 2
    if en_score > es_score and en_score > 0:
        return 'en'
    if es_score > en_score and es_score > 0:
        return 'es'
    # site-page fallback heuristics
    if t in NON_LESSON_EXACT:
        if t in {'idioma','fondos','equipo','recursos','unidades','introducción','introduccion','contacto'}:
            return 'es'
        return 'en'
    # If title contains obvious English article in tail
    if re.search(r'\b(the|what|when|how|my|our|questions|future|past|conditional)\b', blob):
        return 'en'
    if re.search(r'\b(el|la|los|las|cómo|preguntas|parte|verbos|gramática|familia|mercado)\b', blob):
        return 'es'
    return 'other'


def page_kind(title: str) -> str:
    t = clean(title)
    if LESSON_RE.match(t):
        return 'lesson'
    if t.lower() in NON_LESSON_EXACT or t.lower().startswith('nāhuatlahtolli') or t.lower().startswith('nahuatlahtolli'):
        return 'site'
    return 'other'


def lesson_number(title: str) -> Optional[int]:
    m = LESSON_RE.match(clean(title))
    return int(m.group(1)) if m else None


def title_variant(title: str) -> str:
    # Strip the leading lesson number for grouping fallback/debugging.
    t = clean(title)
    m = LESSON_RE.match(t)
    if m:
        return clean(t[m.end():]).lower()
    return t.lower()


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Phase 8.1 cleanup for Nahuatlahtolli crawl output.')
    p.add_argument('--db', required=True, help='Input Phase 8 SQLite DB')
    p.add_argument('--out-db', required=True, help='Output SQLite DB with Phase 8.1 cleanup views/tables')
    p.add_argument('--report-dir', required=True, help='Output report directory')
    return p.parse_args(argv)


def rows_as_dicts(cur: sqlite3.Cursor) -> List[Dict[str, object]]:
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def ensure_phase81_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        '''
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS phase81_page_audit (
            lesson_unit_id TEXT PRIMARY KEY,
            lesson_title TEXT NOT NULL,
            lesson_order INTEGER,
            lesson_url TEXT,
            page_kind TEXT NOT NULL,
            lesson_number INTEGER,
            locale TEXT NOT NULL,
            title_variant TEXT,
            keep_status TEXT NOT NULL,
            duplicate_rank INTEGER,
            canonical_group TEXT,
            duplicate_reason TEXT,
            preferred_for_curriculum INTEGER NOT NULL DEFAULT 0,
            english_partner_lesson_unit_id TEXT,
            spanish_partner_lesson_unit_id TEXT,
            notes TEXT,
            FOREIGN KEY (lesson_unit_id) REFERENCES lesson_units(lesson_unit_id) ON DELETE CASCADE
        );
        DELETE FROM phase81_page_audit;
        DROP VIEW IF EXISTS v_phase81_canonical_lesson_pages;
        DROP VIEW IF EXISTS v_phase81_english_core_lessons;
        DROP VIEW IF EXISTS v_phase81_spanish_parallel_lessons;
        DROP VIEW IF EXISTS v_phase81_canonical_lessons;
        DROP VIEW IF EXISTS v_phase81_noise_pages;
        DROP VIEW IF EXISTS v_phase81_duplicate_pages;
        DROP VIEW IF EXISTS v_phase81_vocab_bilingual;
        DROP VIEW IF EXISTS v_phase81_vocab_english;
        DROP VIEW IF EXISTS v_phase81_dialogues_bilingual;
        DROP VIEW IF EXISTS v_phase81_dialogues_english;
        DROP VIEW IF EXISTS v_phase81_constructions_bilingual;
        DROP VIEW IF EXISTS v_phase81_constructions_english;
        DROP VIEW IF EXISTS v_phase81_lesson_counts;
        '''
    )


def build_audit(lesson_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    audited: List[Dict[str, object]] = []
    grouped: Dict[Tuple[Optional[int], str], List[Dict[str, object]]] = {}

    for r in lesson_rows:
        title = clean(str(r['lesson_title']))
        locale = infer_locale(title, str(r['lesson_url']))
        kind = page_kind(title)
        num = lesson_number(title)
        aud = {
            'lesson_unit_id': r['lesson_unit_id'],
            'lesson_title': title,
            'lesson_order': r['lesson_order'],
            'lesson_url': r['lesson_url'],
            'page_kind': kind,
            'lesson_number': num,
            'locale': locale,
            'title_variant': title_variant(title),
            'keep_status': 'drop_nonlesson' if kind != 'lesson' else 'pending',
            'duplicate_rank': None,
            'canonical_group': f'{num:02d}:{locale}' if kind == 'lesson' and num is not None else None,
            'duplicate_reason': None,
            'preferred_for_curriculum': 0,
            'english_partner_lesson_unit_id': None,
            'spanish_partner_lesson_unit_id': None,
            'notes': None,
        }
        audited.append(aud)
        if kind == 'lesson' and num is not None:
            grouped.setdefault((num, locale), []).append(aud)

    # Rank duplicates within lesson_number x locale and choose earliest page as canonical.
    for key, bucket in grouped.items():
        bucket.sort(key=lambda x: (int(x['lesson_order'] or 999999), str(x['lesson_title'])))
        for i, row in enumerate(bucket, start=1):
            row['duplicate_rank'] = i
            row['keep_status'] = 'keep_canonical' if i == 1 else 'drop_duplicate'
            row['preferred_for_curriculum'] = 1 if i == 1 else 0
            row['duplicate_reason'] = None if i == 1 else f'duplicate_{key[1]}_lesson_page'
            if i > 1:
                row['notes'] = 'Later duplicate of same lesson number and locale.'

    # Wire bilingual partners for canonical pages only.
    canon_lookup: Dict[Tuple[int, str], str] = {}
    for row in audited:
        if row['keep_status'] == 'keep_canonical' and row['lesson_number'] is not None:
            canon_lookup[(int(row['lesson_number']), str(row['locale']))] = str(row['lesson_unit_id'])
    for row in audited:
        if row['keep_status'] == 'keep_canonical' and row['lesson_number'] is not None:
            num = int(row['lesson_number'])
            row['english_partner_lesson_unit_id'] = canon_lookup.get((num, 'en'))
            row['spanish_partner_lesson_unit_id'] = canon_lookup.get((num, 'es'))

    return audited


def write_csv(path: Path, rows: Iterable[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k) for k in fieldnames})


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    in_db = Path(args.db)
    out_db = Path(args.out_db)
    out_db.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(in_db, out_db)
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(out_db))
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    ensure_phase81_schema(conn)

    cur = conn.execute(
        'SELECT lesson_unit_id, lesson_title, lesson_order, lesson_url, proficiency_band FROM lesson_units ORDER BY lesson_order, lesson_title'
    )
    lessons = rows_as_dicts(cur)
    audited = build_audit(lessons)

    conn.executemany(
        '''
        INSERT INTO phase81_page_audit (
            lesson_unit_id, lesson_title, lesson_order, lesson_url, page_kind, lesson_number,
            locale, title_variant, keep_status, duplicate_rank, canonical_group, duplicate_reason,
            preferred_for_curriculum, english_partner_lesson_unit_id, spanish_partner_lesson_unit_id, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        [(
            r['lesson_unit_id'], r['lesson_title'], r['lesson_order'], r['lesson_url'], r['page_kind'], r['lesson_number'],
            r['locale'], r['title_variant'], r['keep_status'], r['duplicate_rank'], r['canonical_group'], r['duplicate_reason'],
            r['preferred_for_curriculum'], r['english_partner_lesson_unit_id'], r['spanish_partner_lesson_unit_id'], r['notes']
        ) for r in audited]
    )

    conn.executescript(
        '''
        CREATE VIEW v_phase81_canonical_lesson_pages AS
        SELECT a.*, u.proficiency_band
        FROM phase81_page_audit a
        JOIN lesson_units u ON u.lesson_unit_id = a.lesson_unit_id
        WHERE a.keep_status = 'keep_canonical'
        ORDER BY a.lesson_number, CASE a.locale WHEN 'en' THEN 1 WHEN 'es' THEN 2 ELSE 3 END, a.lesson_order;

        CREATE VIEW v_phase81_english_core_lessons AS
        SELECT * FROM v_phase81_canonical_lesson_pages WHERE locale = 'en' ORDER BY lesson_number;

        CREATE VIEW v_phase81_spanish_parallel_lessons AS
        SELECT * FROM v_phase81_canonical_lesson_pages WHERE locale = 'es' ORDER BY lesson_number;

        CREATE VIEW v_phase81_noise_pages AS
        SELECT * FROM phase81_page_audit WHERE keep_status = 'drop_nonlesson' ORDER BY lesson_order, lesson_title;

        CREATE VIEW v_phase81_duplicate_pages AS
        SELECT * FROM phase81_page_audit WHERE keep_status = 'drop_duplicate' ORDER BY lesson_number, locale, lesson_order;

        CREATE VIEW v_phase81_canonical_lessons AS
        SELECT
            n.lesson_number,
            en.lesson_unit_id AS english_lesson_unit_id,
            en.lesson_title AS english_lesson_title,
            en.lesson_order AS english_lesson_order,
            es.lesson_unit_id AS spanish_lesson_unit_id,
            es.lesson_title AS spanish_lesson_title,
            es.lesson_order AS spanish_lesson_order,
            COALESCE(en.proficiency_band, es.proficiency_band) AS target_band
        FROM (SELECT DISTINCT lesson_number FROM v_phase81_canonical_lesson_pages WHERE lesson_number IS NOT NULL) n
        LEFT JOIN v_phase81_canonical_lesson_pages en ON en.lesson_number = n.lesson_number AND en.locale = 'en'
        LEFT JOIN v_phase81_canonical_lesson_pages es ON es.lesson_number = n.lesson_number AND es.locale = 'es'
        ORDER BY n.lesson_number;

        CREATE VIEW v_phase81_vocab_bilingual AS
        SELECT a.lesson_number, a.locale, lv.*
        FROM lesson_vocab lv
        JOIN v_phase81_canonical_lesson_pages a ON a.lesson_unit_id = lv.lesson_unit_id
        ORDER BY a.lesson_number, a.locale, lv.surface_form;

        CREATE VIEW v_phase81_vocab_english AS
        SELECT * FROM v_phase81_vocab_bilingual WHERE locale = 'en' ORDER BY lesson_number, surface_form;

        CREATE VIEW v_phase81_dialogues_bilingual AS
        SELECT a.lesson_number, a.locale, d.*
        FROM lesson_dialogues d
        JOIN v_phase81_canonical_lesson_pages a ON a.lesson_unit_id = d.lesson_unit_id
        ORDER BY a.lesson_number, a.locale, d.dialogue_order;

        CREATE VIEW v_phase81_dialogues_english AS
        SELECT * FROM v_phase81_dialogues_bilingual WHERE locale = 'en' ORDER BY lesson_number, dialogue_order;

        CREATE VIEW v_phase81_constructions_bilingual AS
        SELECT a.lesson_number, a.locale, c.*
        FROM construction_bank c
        JOIN v_phase81_canonical_lesson_pages a ON a.lesson_unit_id = c.lesson_unit_id
        ORDER BY a.lesson_number, a.locale, c.construction_id;

        CREATE VIEW v_phase81_constructions_english AS
        SELECT * FROM v_phase81_constructions_bilingual WHERE locale = 'en' ORDER BY lesson_number, construction_id;

        CREATE VIEW v_phase81_lesson_counts AS
        SELECT
            a.lesson_number,
            a.locale,
            a.lesson_title,
            a.proficiency_band,
            COUNT(DISTINCT lv.lesson_vocab_id) AS vocab_count,
            COUNT(DISTINCT d.lesson_dialogue_id) AS dialogue_count,
            COUNT(DISTINCT c.construction_id) AS construction_count
        FROM v_phase81_canonical_lesson_pages a
        LEFT JOIN lesson_vocab lv ON lv.lesson_unit_id = a.lesson_unit_id
        LEFT JOIN lesson_dialogues d ON d.lesson_unit_id = a.lesson_unit_id
        LEFT JOIN construction_bank c ON c.lesson_unit_id = a.lesson_unit_id
        GROUP BY a.lesson_number, a.locale, a.lesson_title, a.proficiency_band
        ORDER BY a.lesson_number, a.locale;
        '''
    )
    conn.commit()

    summary = dict(conn.execute(
        '''
        SELECT
            (SELECT COUNT(*) FROM lesson_units) AS total_lesson_pages,
            (SELECT COUNT(*) FROM phase81_page_audit WHERE page_kind = 'lesson') AS lesson_like_pages,
            (SELECT COUNT(*) FROM v_phase81_canonical_lesson_pages) AS canonical_lesson_pages,
            (SELECT COUNT(*) FROM v_phase81_english_core_lessons) AS english_core_pages,
            (SELECT COUNT(*) FROM v_phase81_spanish_parallel_lessons) AS spanish_parallel_pages,
            (SELECT COUNT(*) FROM v_phase81_canonical_lessons) AS unique_lesson_numbers,
            (SELECT COUNT(*) FROM v_phase81_noise_pages) AS dropped_noise_pages,
            (SELECT COUNT(*) FROM v_phase81_duplicate_pages) AS dropped_duplicate_pages,
            (SELECT COUNT(*) FROM v_phase81_vocab_bilingual) AS canonical_vocab_items_bilingual,
            (SELECT COUNT(*) FROM v_phase81_vocab_english) AS canonical_vocab_items_english,
            (SELECT COUNT(*) FROM v_phase81_dialogues_bilingual) AS canonical_dialogues_bilingual,
            (SELECT COUNT(*) FROM v_phase81_dialogues_english) AS canonical_dialogues_english,
            (SELECT COUNT(*) FROM v_phase81_constructions_bilingual) AS canonical_constructions_bilingual,
            (SELECT COUNT(*) FROM v_phase81_constructions_english) AS canonical_constructions_english
        '''
    ).fetchone())

    canonical_lessons = rows_as_dicts(conn.execute('SELECT * FROM v_phase81_canonical_lessons'))
    english_core = rows_as_dicts(conn.execute('SELECT lesson_number, lesson_title, lesson_order, proficiency_band, lesson_unit_id FROM v_phase81_english_core_lessons'))
    spanish_parallel = rows_as_dicts(conn.execute('SELECT lesson_number, lesson_title, lesson_order, proficiency_band, lesson_unit_id FROM v_phase81_spanish_parallel_lessons'))
    duplicate_pages = rows_as_dicts(conn.execute('SELECT lesson_unit_id, lesson_title, lesson_order, lesson_number, locale, duplicate_rank, duplicate_reason FROM v_phase81_duplicate_pages'))
    noise_pages = rows_as_dicts(conn.execute('SELECT lesson_unit_id, lesson_title, lesson_order, locale, keep_status FROM v_phase81_noise_pages'))
    lesson_counts = rows_as_dicts(conn.execute('SELECT * FROM v_phase81_lesson_counts'))

    (report_dir / 'phase81_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    write_csv(report_dir / 'phase81_canonical_lessons.csv', canonical_lessons, [
        'lesson_number', 'english_lesson_unit_id', 'english_lesson_title', 'english_lesson_order',
        'spanish_lesson_unit_id', 'spanish_lesson_title', 'spanish_lesson_order', 'target_band'
    ])
    write_csv(report_dir / 'phase81_english_core_lessons.csv', english_core, [
        'lesson_number', 'lesson_title', 'lesson_order', 'proficiency_band', 'lesson_unit_id'
    ])
    write_csv(report_dir / 'phase81_spanish_parallel_lessons.csv', spanish_parallel, [
        'lesson_number', 'lesson_title', 'lesson_order', 'proficiency_band', 'lesson_unit_id'
    ])
    write_csv(report_dir / 'phase81_duplicate_pages.csv', duplicate_pages, [
        'lesson_unit_id', 'lesson_title', 'lesson_order', 'lesson_number', 'locale', 'duplicate_rank', 'duplicate_reason'
    ])
    write_csv(report_dir / 'phase81_noise_pages.csv', noise_pages, [
        'lesson_unit_id', 'lesson_title', 'lesson_order', 'locale', 'keep_status'
    ])
    write_csv(report_dir / 'phase81_lesson_counts.csv', lesson_counts, [
        'lesson_number', 'locale', 'lesson_title', 'proficiency_band', 'vocab_count', 'dialogue_count', 'construction_count'
    ])

    conn.close()
    print(f'Phase 8.1 cleanup complete: {out_db}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
