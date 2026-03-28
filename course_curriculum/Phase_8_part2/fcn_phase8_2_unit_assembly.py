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

LESSON_PREFIX_RE = re.compile(r'^\s*Tlamachtiliztli\s+(\d+)\s*', re.I)
PAREN_RE = re.compile(r'\(([^()]*)\)')


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', (text or '').strip())


def extract_theme(title: str) -> str:
    t = clean(title)
    t = LESSON_PREFIX_RE.sub('', t)
    parens = PAREN_RE.findall(t)
    if parens:
        return clean(parens[-1])
    return t


def infer_domain(theme: str) -> str:
    x = theme.lower()
    mapping = [
        ('alphabet', 'orthography'),
        ('preguntas', 'interaction'), ('questions', 'interaction'),
        ('name', 'identity'), ('llamas', 'identity'),
        ('color', 'description'), ('number', 'description'), ('número', 'description'),
        ('profession', 'work'), ('profesione', 'work'),
        ('intransitive', 'grammar'), ('verbos', 'grammar'), ('verbs', 'grammar'),
        ('day', 'time'), ('día', 'time'),
        ('possessive', 'possession'), ('posesivo', 'possession'),
        ('family', 'family'), ('familia', 'family'),
        ('appearance', 'description'), ('apariencia', 'description'),
        ('greet', 'social'), ('farewell', 'social'), ('saluda', 'social'), ('despide', 'social'),
        ('future', 'tense_aspect'), ('futuro', 'tense_aspect'), ('past', 'tense_aspect'), ('pretérito', 'tense_aspect'),
        ('field', 'rural_life'), ('milpa', 'rural_life'), ('food', 'food'), ('comida', 'food'),
        ('house', 'home'), ('casa', 'home'), ('city', 'travel'), ('ciudad', 'travel'), ('market', 'commerce'), ('mercado', 'commerce'),
        ('illness', 'health'), ('enfermedad', 'health'),
        ('conditional', 'grammar'), ('condicional', 'grammar'),
        ('specific object', 'grammar'), ('objetos', 'grammar'), ('grammar', 'grammar'), ('gramática', 'grammar'),
        ('chair', 'daily_actions'), ('levántate', 'commands'), ('stand up', 'commands'),
    ]
    for key, val in mapping:
        if key in x:
            return val
    return 'general'


def infer_communicative_goal(theme: str, domain: str) -> str:
    x = theme.lower()
    if 'alphabet' in x:
        return 'Recognize and pronounce the core alphabet and basic sound patterns.'
    if 'question' in x or 'pregunta' in x:
        return 'Ask and answer simple information questions in everyday exchanges.'
    if 'name' in x or 'llamas' in x:
        return 'Introduce yourself and ask another person’s name.'
    if 'color' in x or 'number' in x or 'número' in x:
        return 'Describe objects with colors and count basic quantities.'
    if 'profession' in x or 'profesione' in x:
        return 'State and ask about occupations and basic social roles.'
    if 'family' in x or 'familia' in x:
        return 'Describe family members and basic kin relationships.'
    if 'appearance' in x or 'apariencia' in x:
        return 'Describe physical appearance using simple adjectives and nouns.'
    if 'greet' in x or 'farewell' in x or 'saluda' in x or 'despide' in x:
        return 'Manage greetings, farewells, and short social openings.'
    if 'market' in x or 'mercado' in x or 'buy' in x:
        return 'Handle simple buying, asking, and exchange interactions.'
    if 'illness' in x or 'enfermedad' in x:
        return 'Talk about common illnesses, symptoms, and basic health topics.'
    if domain == 'grammar':
        return f'Practice the lesson’s core construction set through controlled production tasks for {theme}.'
    return f'Build usable speech routines around {theme}.'


def infer_grammar_focus(theme: str) -> str:
    x = theme.lower()
    if 'intransitive' in x:
        return 'Intransitive verb morphology and person marking.'
    if 'possessive' in x or 'posesivo' in x:
        return 'Possessive markers and possessed noun phrases.'
    if 'future' in x or 'futuro' in x:
        return 'Future and indefinite verbal morphology.'
    if 'past' in x or 'pretérito' in x:
        return 'Past-tense verbal morphology.'
    if 'conditional' in x or 'condicional' in x or 'zquia' in x:
        return 'Conditional morphology and controlled hypothetical clauses.'
    if 'specific object' in x or 'objetos' in x or 'tē-' in x or 'tla-' in x:
        return 'Object marking and argument structure.'
    if 'grammar' in x or 'gramática' in x or '-pil' in x or '-tzin' in x:
        return 'Nominal derivation and discourse nuance in learned forms.'
    if 'question' in x or 'pregunta' in x:
        return 'Interrogative patterns and short-answer structures.'
    return 'Core lesson constructions and reusable sentence patterns.'


def infer_output_task(theme: str, band: str) -> str:
    if band == 'A1':
        return f'Complete a short guided dialogue and mini self-introduction on {theme}.'
    if band == 'A2':
        return f'Produce a short descriptive or transactional exchange built around {theme}.'
    if band == 'B1':
        return f'Hold a longer guided conversation or narration using the constructions from {theme}.'
    return f'Produce an extended controlled task using the lesson material for {theme}.'


def rows_as_dicts(cur: sqlite3.Cursor) -> List[Dict[str, object]]:
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def write_csv(path: Path, rows: Iterable[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k) for k in fieldnames})


def require_object(conn: sqlite3.Connection, name: str, obj_type: str = 'view') -> None:
    row = conn.execute(
        'SELECT name FROM sqlite_master WHERE type = ? AND name = ?',
        (obj_type, name),
    ).fetchone()
    if not row:
        raise SystemExit(f'Missing required {obj_type}: {name}. Run Phase 8.1 cleanup first.')


def ensure_phase82_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        '''
        PRAGMA foreign_keys = ON;
        CREATE TABLE IF NOT EXISTS phase82_unit_plan (
            pedagogical_unit_id TEXT PRIMARY KEY,
            unit_code TEXT NOT NULL UNIQUE,
            lesson_number INTEGER NOT NULL,
            english_lesson_unit_id TEXT,
            spanish_lesson_unit_id TEXT,
            english_lesson_title TEXT,
            spanish_lesson_title TEXT,
            target_band TEXT NOT NULL,
            domain_label TEXT NOT NULL,
            theme_en TEXT NOT NULL,
            communicative_goal TEXT NOT NULL,
            grammar_focus TEXT NOT NULL,
            lexical_focus TEXT NOT NULL,
            output_task TEXT NOT NULL,
            english_vocab_count INTEGER NOT NULL DEFAULT 0,
            english_dialogue_count INTEGER NOT NULL DEFAULT 0,
            english_construction_count INTEGER NOT NULL DEFAULT 0,
            bilingual_vocab_count INTEGER NOT NULL DEFAULT 0,
            bilingual_dialogue_count INTEGER NOT NULL DEFAULT 0,
            bilingual_construction_count INTEGER NOT NULL DEFAULT 0,
            b2_bridge_priority_rank INTEGER,
            notes TEXT,
            FOREIGN KEY (english_lesson_unit_id) REFERENCES lesson_units(lesson_unit_id),
            FOREIGN KEY (spanish_lesson_unit_id) REFERENCES lesson_units(lesson_unit_id)
        );
        DELETE FROM phase82_unit_plan;

        CREATE TABLE IF NOT EXISTS phase82_band_pack (
            pack_code TEXT PRIMARY KEY,
            pack_label TEXT NOT NULL,
            target_band TEXT NOT NULL,
            lesson_numbers_json TEXT NOT NULL,
            lesson_count INTEGER NOT NULL,
            focus_description TEXT NOT NULL
        );
        DELETE FROM phase82_band_pack;

        CREATE TABLE IF NOT EXISTS phase82_vocab_priority (
            priority_id TEXT PRIMARY KEY,
            headword TEXT NOT NULL,
            gloss_en TEXT,
            part_of_speech TEXT,
            first_lesson_number INTEGER,
            lesson_frequency INTEGER NOT NULL,
            occurrence_count INTEGER NOT NULL,
            linked_entry_count INTEGER NOT NULL,
            avg_confidence REAL,
            lessons_json TEXT NOT NULL
        );
        DELETE FROM phase82_vocab_priority;

        CREATE TABLE IF NOT EXISTS phase82_construction_priority (
            priority_id TEXT PRIMARY KEY,
            construction_label TEXT,
            pattern_text TEXT NOT NULL,
            proficiency_band TEXT,
            first_lesson_number INTEGER,
            lesson_frequency INTEGER NOT NULL,
            occurrence_count INTEGER NOT NULL,
            avg_confidence REAL,
            lessons_json TEXT NOT NULL,
            example_original TEXT
        );
        DELETE FROM phase82_construction_priority;

        CREATE TABLE IF NOT EXISTS phase82_dialogue_samples (
            sample_id TEXT PRIMARY KEY,
            lesson_number INTEGER NOT NULL,
            lesson_unit_id TEXT NOT NULL,
            lesson_title TEXT NOT NULL,
            dialogue_order INTEGER NOT NULL,
            speaker_label TEXT,
            utterance_original TEXT NOT NULL,
            utterance_normalized TEXT,
            translation_en TEXT,
            communicative_function TEXT
        );
        DELETE FROM phase82_dialogue_samples;

        DELETE FROM pedagogical_units WHERE editorial_status = 'Phase82_generated';

        DROP VIEW IF EXISTS v_phase82_unit_plan;
        DROP VIEW IF EXISTS v_phase82_a1_units;
        DROP VIEW IF EXISTS v_phase82_a2_units;
        DROP VIEW IF EXISTS v_phase82_b1_units;
        DROP VIEW IF EXISTS v_phase82_b2_bridge_units;
        DROP VIEW IF EXISTS v_phase82_vocab_priority;
        DROP VIEW IF EXISTS v_phase82_construction_priority;
        DROP VIEW IF EXISTS v_phase82_dialogue_samples;
        DROP VIEW IF EXISTS v_phase82_band_pack;
        '''
    )


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Phase 8.2 curriculum assembly on cleaned Phase 8.1 lesson corpus.')
    p.add_argument('--db', required=True, help='Input Phase 8.1 cleaned DB')
    p.add_argument('--out-db', required=True, help='Output Phase 8.2 DB')
    p.add_argument('--report-dir', required=True, help='Output report directory')
    return p.parse_args(argv)


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

    for view in [
        'v_phase81_canonical_lessons',
        'v_phase81_english_core_lessons',
        'v_phase81_spanish_parallel_lessons',
        'v_phase81_lesson_counts',
        'v_phase81_vocab_english',
        'v_phase81_dialogues_english',
        'v_phase81_constructions_english',
        'v_phase81_canonical_lesson_pages'
    ]:
        require_object(conn, view, 'view')

    ensure_phase82_schema(conn)

    lessons = rows_as_dicts(conn.execute('SELECT * FROM v_phase81_canonical_lessons ORDER BY lesson_number'))
    counts = rows_as_dicts(conn.execute('SELECT * FROM v_phase81_lesson_counts ORDER BY lesson_number, locale'))
    counts_idx: Dict[Tuple[int, str], Dict[str, object]] = {}
    for r in counts:
        counts_idx[(int(r['lesson_number']), str(r['locale']))] = r

    unit_rows: List[Dict[str, object]] = []
    b1_priority: List[Tuple[int, int]] = []
    for lesson in lessons:
        num = int(lesson['lesson_number'])
        eng_title = clean(str(lesson['english_lesson_title'] or ''))
        es_title = clean(str(lesson['spanish_lesson_title'] or ''))
        band = clean(str(lesson['target_band'] or 'A1')) or 'A1'
        theme_en = extract_theme(eng_title or es_title)
        domain = infer_domain(theme_en)
        communicative_goal = infer_communicative_goal(theme_en, domain)
        grammar_focus = infer_grammar_focus(theme_en)
        lexical_focus = f'Core vocabulary and reusable expressions for {theme_en}.'
        output_task = infer_output_task(theme_en, band)

        en_counts = counts_idx.get((num, 'en'), {})
        es_counts = counts_idx.get((num, 'es'), {})
        unit = {
            'pedagogical_unit_id': f'FCN-PED-{num:04d}',
            'unit_code': f'FCN-U{num:02d}',
            'lesson_number': num,
            'english_lesson_unit_id': lesson['english_lesson_unit_id'],
            'spanish_lesson_unit_id': lesson['spanish_lesson_unit_id'],
            'english_lesson_title': eng_title,
            'spanish_lesson_title': es_title,
            'target_band': band,
            'domain_label': domain,
            'theme_en': theme_en,
            'communicative_goal': communicative_goal,
            'grammar_focus': grammar_focus,
            'lexical_focus': lexical_focus,
            'output_task': output_task,
            'english_vocab_count': int(en_counts.get('vocab_count', 0) or 0),
            'english_dialogue_count': int(en_counts.get('dialogue_count', 0) or 0),
            'english_construction_count': int(en_counts.get('construction_count', 0) or 0),
            'bilingual_vocab_count': int(en_counts.get('vocab_count', 0) or 0) + int(es_counts.get('vocab_count', 0) or 0),
            'bilingual_dialogue_count': int(en_counts.get('dialogue_count', 0) or 0) + int(es_counts.get('dialogue_count', 0) or 0),
            'bilingual_construction_count': int(en_counts.get('construction_count', 0) or 0) + int(es_counts.get('construction_count', 0) or 0),
            'b2_bridge_priority_rank': None,
            'notes': None,
        }
        unit_rows.append(unit)
        if band == 'B1':
            score = unit['english_construction_count'] * 1000 + unit['english_dialogue_count']
            b1_priority.append((score, num))

    b1_priority.sort(reverse=True)
    b2_priority_map = {num: i for i, (_score, num) in enumerate(b1_priority, start=1)}
    for unit in unit_rows:
        if unit['target_band'] == 'B1':
            unit['b2_bridge_priority_rank'] = b2_priority_map.get(int(unit['lesson_number']))

    conn.executemany(
        '''
        INSERT INTO phase82_unit_plan (
            pedagogical_unit_id, unit_code, lesson_number, english_lesson_unit_id, spanish_lesson_unit_id,
            english_lesson_title, spanish_lesson_title, target_band, domain_label, theme_en,
            communicative_goal, grammar_focus, lexical_focus, output_task,
            english_vocab_count, english_dialogue_count, english_construction_count,
            bilingual_vocab_count, bilingual_dialogue_count, bilingual_construction_count,
            b2_bridge_priority_rank, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        [(
            r['pedagogical_unit_id'], r['unit_code'], r['lesson_number'], r['english_lesson_unit_id'], r['spanish_lesson_unit_id'],
            r['english_lesson_title'], r['spanish_lesson_title'], r['target_band'], r['domain_label'], r['theme_en'],
            r['communicative_goal'], r['grammar_focus'], r['lexical_focus'], r['output_task'],
            r['english_vocab_count'], r['english_dialogue_count'], r['english_construction_count'],
            r['bilingual_vocab_count'], r['bilingual_dialogue_count'], r['bilingual_construction_count'],
            r['b2_bridge_priority_rank'], r['notes']
        ) for r in unit_rows]
    )

    conn.executemany(
        '''
        INSERT INTO pedagogical_units (
            pedagogical_unit_id, unit_code, unit_title, target_band, domain_label, lesson_unit_id,
            communicative_goal, grammar_focus, lexical_focus, output_task, editorial_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Phase82_generated')
        ''',
        [(
            r['pedagogical_unit_id'], r['unit_code'], r['theme_en'], r['target_band'], r['domain_label'],
            r['english_lesson_unit_id'] or r['spanish_lesson_unit_id'],
            r['communicative_goal'], r['grammar_focus'], r['lexical_focus'], r['output_task']
        ) for r in unit_rows]
    )

    packs = []
    for code, label, band, filt, desc in [
        ('A1_CORE', 'A1 Core Units', 'A1', lambda u: u['target_band'] == 'A1', 'Foundational pronunciation, interaction, and core everyday routines.'),
        ('A2_EXPANSION', 'A2 Expansion Units', 'A2', lambda u: u['target_band'] == 'A2', 'Expanded descriptive and transactional capacity in familiar domains.'),
        ('B1_CONVERSATION', 'B1 Conversation Units', 'B1', lambda u: u['target_band'] == 'B1', 'Longer guided conversations, narration, and morphosyntactic expansion.'),
        ('B2_BRIDGE', 'B2 Bridge Units', 'B2', lambda u: u['target_band'] == 'B1' and (u['b2_bridge_priority_rank'] or 999) <= 8, 'Bridge pack built from the densest B1 lessons for extended controlled speaking.'),
    ]:
        nums = [int(u['lesson_number']) for u in unit_rows if filt(u)]
        packs.append({
            'pack_code': code,
            'pack_label': label,
            'target_band': band,
            'lesson_numbers_json': json.dumps(nums, ensure_ascii=False),
            'lesson_count': len(nums),
            'focus_description': desc,
        })
    conn.executemany(
        'INSERT INTO phase82_band_pack (pack_code, pack_label, target_band, lesson_numbers_json, lesson_count, focus_description) VALUES (?, ?, ?, ?, ?, ?)',
        [(p['pack_code'], p['pack_label'], p['target_band'], p['lesson_numbers_json'], p['lesson_count'], p['focus_description']) for p in packs]
    )

    vocab_rows = rows_as_dicts(conn.execute('SELECT lesson_number, lesson_unit_id, surface_form, normalized_form, gloss_en, part_of_speech, linked_entry_id, confidence FROM v_phase81_vocab_english'))
    vocab_group: Dict[Tuple[str, str, str], Dict[str, object]] = {}
    for r in vocab_rows:
        head = clean(str(r['normalized_form'] or r['surface_form'] or ''))
        key = (head.lower(), clean(str(r['gloss_en'] or '')), clean(str(r['part_of_speech'] or '')))
        if key not in vocab_group:
            vocab_group[key] = {
                'headword': head,
                'gloss_en': clean(str(r['gloss_en'] or '')),
                'part_of_speech': clean(str(r['part_of_speech'] or '')),
                'first_lesson_number': int(r['lesson_number']),
                'lesson_numbers': set(),
                'occurrence_count': 0,
                'linked_entry_ids': set(),
                'conf_sum': 0.0,
                'conf_n': 0,
            }
        g = vocab_group[key]
        g['lesson_numbers'].add(int(r['lesson_number']))
        g['occurrence_count'] += 1
        if r['linked_entry_id']:
            g['linked_entry_ids'].add(str(r['linked_entry_id']))
        if r['confidence'] is not None:
            g['conf_sum'] += float(r['confidence'])
            g['conf_n'] += 1
        g['first_lesson_number'] = min(int(g['first_lesson_number']), int(r['lesson_number']))

    vocab_priority_rows = []
    for i, g in enumerate(sorted(vocab_group.values(), key=lambda x: (-len(x['lesson_numbers']), x['first_lesson_number'], x['headword'].lower())), start=1):
        vocab_priority_rows.append({
            'priority_id': f'FCN-VP-{i:05d}',
            'headword': g['headword'],
            'gloss_en': g['gloss_en'],
            'part_of_speech': g['part_of_speech'],
            'first_lesson_number': g['first_lesson_number'],
            'lesson_frequency': len(g['lesson_numbers']),
            'occurrence_count': g['occurrence_count'],
            'linked_entry_count': len(g['linked_entry_ids']),
            'avg_confidence': round(g['conf_sum'] / g['conf_n'], 4) if g['conf_n'] else None,
            'lessons_json': json.dumps(sorted(g['lesson_numbers']), ensure_ascii=False),
        })
    conn.executemany(
        'INSERT INTO phase82_vocab_priority (priority_id, headword, gloss_en, part_of_speech, first_lesson_number, lesson_frequency, occurrence_count, linked_entry_count, avg_confidence, lessons_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        [(r['priority_id'], r['headword'], r['gloss_en'], r['part_of_speech'], r['first_lesson_number'], r['lesson_frequency'], r['occurrence_count'], r['linked_entry_count'], r['avg_confidence'], r['lessons_json']) for r in vocab_priority_rows]
    )

    c_rows = rows_as_dicts(conn.execute('SELECT lesson_number, construction_label, pattern_text, proficiency_band, confidence, example_original FROM v_phase81_constructions_english'))
    c_group: Dict[Tuple[str, str], Dict[str, object]] = {}
    for r in c_rows:
        label = clean(str(r['construction_label'] or ''))
        pat = clean(str(r['pattern_text'] or ''))
        key = (label.lower(), pat.lower())
        if key not in c_group:
            c_group[key] = {
                'construction_label': label,
                'pattern_text': pat,
                'proficiency_band': clean(str(r['proficiency_band'] or '')),
                'first_lesson_number': int(r['lesson_number']),
                'lesson_numbers': set(),
                'occurrence_count': 0,
                'conf_sum': 0.0,
                'conf_n': 0,
                'example_original': clean(str(r['example_original'] or '')),
            }
        g = c_group[key]
        g['lesson_numbers'].add(int(r['lesson_number']))
        g['occurrence_count'] += 1
        g['first_lesson_number'] = min(int(g['first_lesson_number']), int(r['lesson_number']))
        if r['confidence'] is not None:
            g['conf_sum'] += float(r['confidence'])
            g['conf_n'] += 1
        if not g['example_original'] and r['example_original']:
            g['example_original'] = clean(str(r['example_original']))
    construction_priority_rows = []
    for i, g in enumerate(sorted(c_group.values(), key=lambda x: (-len(x['lesson_numbers']), x['first_lesson_number'], x['pattern_text'].lower())), start=1):
        construction_priority_rows.append({
            'priority_id': f'FCN-CP-{i:05d}',
            'construction_label': g['construction_label'],
            'pattern_text': g['pattern_text'],
            'proficiency_band': g['proficiency_band'],
            'first_lesson_number': g['first_lesson_number'],
            'lesson_frequency': len(g['lesson_numbers']),
            'occurrence_count': g['occurrence_count'],
            'avg_confidence': round(g['conf_sum'] / g['conf_n'], 4) if g['conf_n'] else None,
            'lessons_json': json.dumps(sorted(g['lesson_numbers']), ensure_ascii=False),
            'example_original': g['example_original'],
        })
    conn.executemany(
        'INSERT INTO phase82_construction_priority (priority_id, construction_label, pattern_text, proficiency_band, first_lesson_number, lesson_frequency, occurrence_count, avg_confidence, lessons_json, example_original) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        [(r['priority_id'], r['construction_label'], r['pattern_text'], r['proficiency_band'], r['first_lesson_number'], r['lesson_frequency'], r['occurrence_count'], r['avg_confidence'], r['lessons_json'], r['example_original']) for r in construction_priority_rows]
    )

    d_rows = rows_as_dicts(conn.execute(
        'SELECT d.lesson_number, e.lesson_unit_id, e.lesson_title, d.dialogue_order, d.speaker_label, d.utterance_original, d.utterance_normalized, d.translation_en, d.communicative_function FROM v_phase81_dialogues_english d JOIN v_phase81_english_core_lessons e USING (lesson_number) ORDER BY d.lesson_number, d.dialogue_order'
    ))
    sample_rows = []
    seen_per_lesson: Dict[int, int] = {}
    for r in d_rows:
        num = int(r['lesson_number'])
        seen_per_lesson[num] = seen_per_lesson.get(num, 0) + 1
        if seen_per_lesson[num] > 2:
            continue
        sample_rows.append({
            'sample_id': f'FCN-DS-{num:02d}-{seen_per_lesson[num]:02d}',
            'lesson_number': num,
            'lesson_unit_id': r['lesson_unit_id'],
            'lesson_title': r['lesson_title'],
            'dialogue_order': int(r['dialogue_order']),
            'speaker_label': r['speaker_label'],
            'utterance_original': r['utterance_original'],
            'utterance_normalized': r['utterance_normalized'],
            'translation_en': r['translation_en'],
            'communicative_function': r['communicative_function'],
        })
    conn.executemany(
        'INSERT INTO phase82_dialogue_samples (sample_id, lesson_number, lesson_unit_id, lesson_title, dialogue_order, speaker_label, utterance_original, utterance_normalized, translation_en, communicative_function) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        [(r['sample_id'], r['lesson_number'], r['lesson_unit_id'], r['lesson_title'], r['dialogue_order'], r['speaker_label'], r['utterance_original'], r['utterance_normalized'], r['translation_en'], r['communicative_function']) for r in sample_rows]
    )

    conn.executescript(
        '''
        CREATE VIEW v_phase82_unit_plan AS
        SELECT * FROM phase82_unit_plan ORDER BY lesson_number;

        CREATE VIEW v_phase82_a1_units AS
        SELECT * FROM phase82_unit_plan WHERE target_band = 'A1' ORDER BY lesson_number;

        CREATE VIEW v_phase82_a2_units AS
        SELECT * FROM phase82_unit_plan WHERE target_band = 'A2' ORDER BY lesson_number;

        CREATE VIEW v_phase82_b1_units AS
        SELECT * FROM phase82_unit_plan WHERE target_band = 'B1' ORDER BY lesson_number;

        CREATE VIEW v_phase82_b2_bridge_units AS
        SELECT * FROM phase82_unit_plan WHERE b2_bridge_priority_rank IS NOT NULL AND b2_bridge_priority_rank <= 8 ORDER BY b2_bridge_priority_rank, lesson_number;

        CREATE VIEW v_phase82_vocab_priority AS
        SELECT * FROM phase82_vocab_priority ORDER BY lesson_frequency DESC, first_lesson_number, headword;

        CREATE VIEW v_phase82_construction_priority AS
        SELECT * FROM phase82_construction_priority ORDER BY lesson_frequency DESC, first_lesson_number, pattern_text;

        CREATE VIEW v_phase82_dialogue_samples AS
        SELECT * FROM phase82_dialogue_samples ORDER BY lesson_number, dialogue_order;

        CREATE VIEW v_phase82_band_pack AS
        SELECT * FROM phase82_band_pack ORDER BY CASE target_band WHEN 'A1' THEN 1 WHEN 'A2' THEN 2 WHEN 'B1' THEN 3 WHEN 'B2' THEN 4 ELSE 5 END;
        '''
    )
    conn.commit()

    summary = dict(conn.execute(
        '''
        SELECT
            (SELECT COUNT(*) FROM phase82_unit_plan) AS pedagogical_units,
            (SELECT COUNT(*) FROM v_phase82_a1_units) AS a1_units,
            (SELECT COUNT(*) FROM v_phase82_a2_units) AS a2_units,
            (SELECT COUNT(*) FROM v_phase82_b1_units) AS b1_units,
            (SELECT COUNT(*) FROM v_phase82_b2_bridge_units) AS b2_bridge_units,
            (SELECT COUNT(*) FROM phase82_vocab_priority) AS prioritized_vocab_items,
            (SELECT COUNT(*) FROM phase82_construction_priority) AS prioritized_constructions,
            (SELECT COUNT(*) FROM phase82_dialogue_samples) AS dialogue_samples,
            (SELECT COUNT(*) FROM phase82_band_pack) AS band_packs
        '''
    ).fetchone())

    unit_plan = rows_as_dicts(conn.execute('SELECT * FROM v_phase82_unit_plan'))
    band_packs = rows_as_dicts(conn.execute('SELECT * FROM v_phase82_band_pack'))
    vocab_top = rows_as_dicts(conn.execute('SELECT * FROM v_phase82_vocab_priority LIMIT 500'))
    construction_top = rows_as_dicts(conn.execute('SELECT * FROM v_phase82_construction_priority LIMIT 300'))
    dialogue_samples = rows_as_dicts(conn.execute('SELECT * FROM v_phase82_dialogue_samples'))

    (report_dir / 'phase82_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    write_csv(report_dir / 'phase82_unit_plan.csv', unit_plan, [
        'pedagogical_unit_id', 'unit_code', 'lesson_number', 'english_lesson_unit_id', 'spanish_lesson_unit_id',
        'english_lesson_title', 'spanish_lesson_title', 'target_band', 'domain_label', 'theme_en',
        'communicative_goal', 'grammar_focus', 'lexical_focus', 'output_task',
        'english_vocab_count', 'english_dialogue_count', 'english_construction_count',
        'bilingual_vocab_count', 'bilingual_dialogue_count', 'bilingual_construction_count',
        'b2_bridge_priority_rank', 'notes'
    ])
    write_csv(report_dir / 'phase82_band_packs.csv', band_packs, [
        'pack_code', 'pack_label', 'target_band', 'lesson_numbers_json', 'lesson_count', 'focus_description'
    ])
    write_csv(report_dir / 'phase82_vocab_priority_top500.csv', vocab_top, [
        'priority_id', 'headword', 'gloss_en', 'part_of_speech', 'first_lesson_number', 'lesson_frequency',
        'occurrence_count', 'linked_entry_count', 'avg_confidence', 'lessons_json'
    ])
    write_csv(report_dir / 'phase82_construction_priority_top300.csv', construction_top, [
        'priority_id', 'construction_label', 'pattern_text', 'proficiency_band', 'first_lesson_number',
        'lesson_frequency', 'occurrence_count', 'avg_confidence', 'lessons_json', 'example_original'
    ])
    write_csv(report_dir / 'phase82_dialogue_samples.csv', dialogue_samples, [
        'sample_id', 'lesson_number', 'lesson_unit_id', 'lesson_title', 'dialogue_order', 'speaker_label',
        'utterance_original', 'utterance_normalized', 'translation_en', 'communicative_function'
    ])

    conn.close()
    print(f'Phase 8.2 unit assembly complete: {out_db}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
