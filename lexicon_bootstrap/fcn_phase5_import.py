#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ALLOWED_REGISTERS = {
    'EHN_colloquial',
    'EHN_formal',
    'MSN_neutral',
    'MSN_public',
    'MSN_poetic',
    'Classical_citation',
    'Comparative_only',
    'Proposed',
    'Deprecated',
    'Needs_review',
}

SRC = {
    'kaikki_unified': 'FCN-SRC-KAIKKI-UNIFIED',
    'out_kaikki_jsonl': 'FCN-SRC-OUT-KAIKKI-JSONL',
    'out_kaikki_csv': 'FCN-SRC-OUT-KAIKKI-CSV',
    'simeon_parsed': 'FCN-SRC-SIMEON-PARSED',
    'simeon_ocr_raw': 'FCN-SRC-SIMEON-OCR-RAW',
    'out_classical_examples': 'FCN-SRC-OUT-CLASSICAL-EXAMPLES',
    'out_classical_blocks': 'FCN-SRC-OUT-CLASSICAL-BLOCKS',
    'out_classical_headwords': 'FCN-SRC-OUT-CLASSICAL-HEADWORDS',
    'out_ud_summary': 'FCN-SRC-OUT-UD',
    'provenance': 'FCN-SRC-PROVENANCE',
    'readme_sources': 'FCN-SRC-README-SOURCES',
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Phase 5 importer for Flor y Canto Nahuatl.')
    parser.add_argument('--repo', required=True, help='Path to fcn_ingest directory.')
    parser.add_argument('--schema', required=True, help='Path to Phase 4 schema SQL file.')
    parser.add_argument('--db', required=True, help='Output SQLite database path.')
    parser.add_argument('--qa-dir', required=True, help='Directory for QA outputs.')
    parser.add_argument('--replace-db', action='store_true', help='Delete existing database before import.')
    return parser.parse_args()


def confidence_to_float(value: Any, default: float = 0.5) -> float:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        value = float(value)
        return max(0.0, min(1.0, value))
    text = str(value).strip().lower()
    mapping = {
        'high': 0.95,
        'medium': 0.70,
        'low': 0.40,
        'unreviewed': 0.50,
    }
    if text in mapping:
        return mapping[text]
    try:
        return max(0.0, min(1.0, float(text)))
    except ValueError:
        return default


def editorial_status_to_schema(value: str | None) -> str:
    mapping = {
        None: 'Imported_raw',
        '': 'Imported_raw',
        'imported_raw': 'Imported_raw',
        'reviewed': 'Reviewed',
        'curated': 'Curated',
        'approved': 'Approved',
        'flagged': 'Flagged',
        'deprecated': 'Deprecated',
    }
    return mapping.get((value or '').strip().lower(), 'Imported_raw')


def speaker_status_to_schema(value: str | None) -> str:
    mapping = {
        None: 'Unreviewed',
        '': 'Unreviewed',
        'unreviewed': 'Unreviewed',
        'pending': 'Pending',
        'validated_speaker': 'Validated_speaker',
        'rejected_speaker': 'Rejected_speaker',
        'mixed_feedback': 'Mixed_feedback',
        'not_applicable': 'Not_applicable',
    }
    return mapping.get((value or '').strip().lower(), 'Unreviewed')


def norm_space(text: str | None) -> str:
    return re.sub(r'\s+', ' ', (text or '').strip())


def normalize_key(text: str | None) -> str:
    text = norm_space(text).lower()
    text = re.sub(r'[^\w\- ]+', '', text, flags=re.UNICODE)
    text = re.sub(r'\s+', ' ', text)
    return text


def detect_register_from_kaikki(row: dict[str, Any]) -> str:
    direct = norm_space(row.get('register'))
    if direct in ALLOWED_REGISTERS:
        return direct
    suggestion = norm_space(row.get('register_suggestion'))
    variety = norm_space(row.get('variety'))
    if variety == 'Eastern Huasteca Nahuatl':
        return 'EHN_colloquial'
    if suggestion in ALLOWED_REGISTERS and suggestion == 'Classical_citation':
        return 'Classical_citation'
    if variety == 'Classical Nahuatl':
        return 'Classical_citation'
    return 'Comparative_only'


def preferred_form_for_entry(row: dict[str, Any]) -> str:
    for key in ('ehn_spoken_form', 'msn_headword', 'classical_citation_form', 'lemma_display'):
        value = norm_space(row.get(key))
        if value:
            return value
    return ''


def choose_simeon_editorial_status(headword: str, definition_fr: str) -> str:
    suspect = is_simeon_ocr_suspect(headword, definition_fr)
    return 'Flagged' if suspect else 'Imported_raw'


def is_simeon_ocr_suspect(headword: str, definition_fr: str) -> bool:
    hw = norm_space(headword)
    if not hw:
        return True
    if re.fullmatch(r'[IVXLCDM]+T?', hw):
        return True
    if any(ch.isdigit() for ch in hw):
        return True
    if len(hw) > 35:
        return True
    if hw.startswith('DICTIONNAIRE') or hw.startswith('MISSION ') or hw in {'DE', 'LA', 'LE', 'AG'}:
        return True
    if 'ÉTUDES GRAMMATICALES' in (definition_fr or ''):
        return True
    return False


def ensure_extension_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        '''
        CREATE TABLE IF NOT EXISTS entry_payloads (
            payload_id TEXT PRIMARY KEY,
            entry_id TEXT NOT NULL,
            source_id TEXT,
            payload_kind TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (entry_id) REFERENCES lexicon_entries(entry_id) ON DELETE CASCADE,
            FOREIGN KEY (source_id) REFERENCES sources(source_id)
        );

        CREATE TABLE IF NOT EXISTS classical_examples_staging (
            staging_id TEXT PRIMARY KEY,
            source_file TEXT NOT NULL,
            source_locator TEXT NOT NULL,
            current_headword TEXT,
            nahuatliness_score REAL,
            example_text TEXT NOT NULL,
            matched_entry_id TEXT,
            match_method TEXT,
            source_id TEXT,
            notes TEXT,
            FOREIGN KEY (matched_entry_id) REFERENCES lexicon_entries(entry_id),
            FOREIGN KEY (source_id) REFERENCES sources(source_id)
        );

        CREATE TABLE IF NOT EXISTS classical_blocks_staging (
            staging_id TEXT PRIMARY KEY,
            source_file TEXT NOT NULL,
            source_locator TEXT NOT NULL,
            current_headword TEXT,
            kind TEXT,
            nahuatliness_score REAL,
            text TEXT NOT NULL,
            matched_entry_id TEXT,
            match_method TEXT,
            source_id TEXT,
            notes TEXT,
            FOREIGN KEY (matched_entry_id) REFERENCES lexicon_entries(entry_id),
            FOREIGN KEY (source_id) REFERENCES sources(source_id)
        );

        CREATE INDEX IF NOT EXISTS idx_payloads_entry_id ON entry_payloads(entry_id);
        CREATE INDEX IF NOT EXISTS idx_classical_examples_headword ON classical_examples_staging(current_headword);
        CREATE INDEX IF NOT EXISTS idx_classical_blocks_headword ON classical_blocks_staging(current_headword);
        '''
    )


def register_sources(conn: sqlite3.Connection, repo: Path) -> None:
    rows = [
        (
            SRC['kaikki_unified'], 'nahuatl_kaikki_unified.json', 'lexical_json',
            'Unified Nahuatl Kaikki/Wiktionary extract',
            'Kaikki/Wiktionary unified lexical source used as the primary lexical intake layer.',
            'CC BY-SA 3.0 / GFDL', None, 'lexical_base', 'lexicon_intake',
            'Mixed varieties; not a final spoken norm.', 'canonical_intake', None,
        ),
        (
            SRC['out_kaikki_jsonl'], 'out_kaikki/fcn_lexical_rows.jsonl', 'derived_jsonl',
            'FCN parser output from Kaikki unified source',
            'Derived working layer created by fcn_source_parsers.py.',
            'CC BY-SA 3.0 / GFDL + FCN provenance', None, 'working_lexical_rows', 'derived_working_layer',
            'Parser-dependent normalization.', 'canonical_working', None,
        ),
        (
            SRC['out_kaikki_csv'], 'out_kaikki/fcn_lexical_rows.csv', 'derived_csv',
            'FCN CSV export from Kaikki unified source',
            'CSV export of parsed lexical rows.',
            'CC BY-SA 3.0 / GFDL + FCN provenance', None, 'working_lexical_rows', 'derived_working_layer',
            'Parser-dependent normalization.', 'canonical_working', None,
        ),
        (
            SRC['simeon_parsed'], 'simeon_parsed.json', 'classical_reference_json',
            "Siméon 1885 parsed dictionary",
            'Parsed structured reference source for classical/headword/root evidence.',
            'PUBLIC DOMAIN', None, 'classical_reference', 'classical_reference',
            'Definitions are in French; OCR/parsing imperfections remain.', 'canonical_reference', None,
        ),
        (
            SRC['simeon_ocr_raw'], 'simeon_1885_ocr_raw.txt', 'raw_ocr_text',
            'Siméon 1885 OCR raw text',
            'Raw OCR archival source retained for dispute review and recovery.',
            'PUBLIC DOMAIN', None, 'archival_ocr', 'archival_only',
            'Raw OCR with damage and structural noise.', 'noncanonical_archival', None,
        ),
        (
            SRC['out_classical_examples'], 'out_classical/classical_examples.jsonl', 'derived_jsonl',
            'FCN classical example extraction',
            'Derived example bank extracted from raw Siméon OCR.',
            'PUBLIC DOMAIN + FCN provenance', None, 'classical_examples', 'derived_working_layer',
            'Headword linkage is noisy and must be curated.', 'working_staging', None,
        ),
        (
            SRC['out_classical_blocks'], 'out_classical/classical_blocks.jsonl', 'derived_jsonl',
            'FCN classical block extraction',
            'Derived block bank extracted from raw Siméon OCR.',
            'PUBLIC DOMAIN + FCN provenance', None, 'classical_blocks', 'derived_working_layer',
            'Headword linkage is noisy and must be curated.', 'working_staging', None,
        ),
        (
            SRC['out_classical_headwords'], 'out_classical/headword_candidates.csv', 'derived_csv',
            'FCN classical headword candidates',
            'Derived headword candidate file from raw Siméon OCR.',
            'PUBLIC DOMAIN + FCN provenance', None, 'classical_headword_candidates', 'derived_working_layer',
            'Contains OCR noise and false positives.', 'working_staging', None,
        ),
        (
            SRC['out_ud_summary'], 'out_ud/summary.json', 'ud_summary',
            'UD grammar evidence summary',
            'Supporting grammar evidence layer, not a standalone norm.',
            'Per-treebank license; see provenance ledger', None, 'grammar_evidence', 'grammar_support',
            'Corpus scope limited.', 'supporting_evidence', None,
        ),
        (
            SRC['provenance'], 'data/ledger/provenance.csv', 'provenance_csv',
            'FCN provenance ledger',
            'Legal and retrieval audit trail.',
            'FCN internal provenance record', None, 'audit_trail', 'provenance_audit',
            'Administrative source, not linguistic authority.', 'canonical_audit', None,
        ),
        (
            SRC['readme_sources'], 'README_SOURCES.txt', 'source_memo',
            'Source memo / legal note',
            'Foundational project memo describing licenses and OCR limitations.',
            'Project memo', None, 'source_policy', 'policy_memo',
            'Descriptive memo, not lexical authority.', 'canonical_policy', None,
        ),
    ]
    conn.executemany(
        '''
        INSERT OR REPLACE INTO sources (
            source_id, source_file, source_type, upstream_title, provenance_note, license,
            retrieval_or_creation_date, project_role, authority_domain, limitations,
            canonical_status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        rows,
    )


def insert_entry_payload(conn: sqlite3.Connection, entry_id: str, source_id: str, kind: str, payload: dict[str, Any]) -> None:
    payload_text = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    payload_id = 'PAYLOAD-' + hashlib.sha1(f'{entry_id}|{source_id}|{kind}|{payload_text}'.encode('utf-8')).hexdigest()[:16]
    conn.execute(
        '''
        INSERT OR REPLACE INTO entry_payloads (payload_id, entry_id, source_id, payload_kind, payload_json)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (payload_id, entry_id, source_id, kind, payload_text),
    )


def insert_root_family(conn: sqlite3.Connection, root_label: str, source_id: str, source_reference: str) -> str:
    root_label = norm_space(root_label)
    if not root_label:
        return ''
    code = 'ROOT-' + hashlib.sha1(root_label.lower().encode('utf-8')).hexdigest()[:12]
    conn.execute(
        '''
        INSERT OR IGNORE INTO roots_families (
            root_family_code, root_family_label, description, source_id, source_reference, confidence, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (code, root_label, None, source_id, source_reference, 0.8, None),
    )
    return code


def insert_variant(
    conn: sqlite3.Connection,
    entry_id: str,
    source_id: str,
    source_reference: str,
    form_text: str,
    form_role: str,
    register: str,
    variety: str,
    confidence: float,
    editorial_status: str,
    raw_form: str | None = None,
    normalized_form: str | None = None,
    orthography_status: str = 'source_attested',
    sort_order: int = 1,
    is_preferred: int = 0,
    notes: str | None = None,
) -> None:
    form_text = norm_space(form_text)
    if not form_text:
        return
    variant_seed = '|'.join([entry_id, form_text, form_role, register, variety, str(sort_order)])
    variant_id = 'VAR-' + hashlib.sha1(variant_seed.encode('utf-8')).hexdigest()[:16]
    conn.execute(
        '''
        INSERT OR IGNORE INTO variants (
            variant_id, entry_id, form_text, form_role, register, variety, raw_form,
            normalized_form, orthography_status, source_id, source_reference,
            confidence, editorial_status, sort_order, is_preferred, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            variant_id, entry_id, form_text, form_role, register, variety,
            raw_form or form_text, normalized_form or form_text, orthography_status,
            source_id, source_reference, confidence, editorial_status, sort_order,
            is_preferred, notes,
        ),
    )


def import_kaikki(conn: sqlite3.Connection, repo: Path) -> dict[str, Any]:
    path = repo / 'out_kaikki' / 'fcn_lexical_rows.jsonl'
    inserted = 0
    ehn = 0
    comparative = 0
    classical = 0
    missing_gloss = 0
    missing_forms = 0

    with path.open('r', encoding='utf-8') as fh:
        for line in fh:
            row = json.loads(line)
            entry_id = row['entry_id']
            register = detect_register_from_kaikki(row)
            variety = norm_space(row.get('variety')) or 'Unknown'
            confidence = confidence_to_float(row.get('source_confidence'), 0.95)
            editorial_status = editorial_status_to_schema(row.get('editorial_status'))
            speaker_status = speaker_status_to_schema(row.get('speaker_validation_status'))
            preferred_form = preferred_form_for_entry(row)

            if register == 'EHN_colloquial':
                ehn += 1
            elif register == 'Classical_citation':
                classical += 1
            else:
                comparative += 1

            if not norm_space(row.get('gloss_en')) and not norm_space(row.get('gloss_es')):
                missing_gloss += 1

            notes_internal_parts = []
            if row.get('register_suggestion'):
                notes_internal_parts.append(f"register_suggestion={row['register_suggestion']}")
            if row.get('parser'):
                notes_internal_parts.append(f"parser={row['parser']}")
            if row.get('etymology'):
                notes_internal_parts.append(f"etymology={row['etymology']}")
            if row.get('notes_internal'):
                notes_internal_parts.append(str(row['notes_internal']))
            notes_internal = ' | '.join(part for part in notes_internal_parts if part)

            conn.execute(
                '''
                INSERT OR REPLACE INTO lexicon_entries (
                    entry_id, project_name, sense_order, ehn_spoken_form, msn_headword,
                    msn_poetic_form, classical_citation_form, part_of_speech, register,
                    variety, gloss_en, gloss_es, root_family, root_family_code,
                    source_file, source_reference, source_confidence,
                    speaker_validation_status, editorial_status, notes_internal,
                    notes_public, source_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    entry_id,
                    norm_space(row.get('project_name')) or 'Flor y Canto Nahuatl',
                    1,
                    norm_space(row.get('ehn_spoken_form')) or None,
                    norm_space(row.get('msn_headword')) or None,
                    norm_space(row.get('msn_poetic_form')) or None,
                    norm_space(row.get('classical_citation_form')) or None,
                    norm_space(row.get('part_of_speech')) or 'unknown',
                    register,
                    variety,
                    norm_space(row.get('gloss_en')) or None,
                    norm_space(row.get('gloss_es')) or None,
                    norm_space(row.get('root_family')) or None,
                    None,
                    norm_space(row.get('source_file')) or 'nahuatl_kaikki_unified.json',
                    norm_space(row.get('source_reference')) or entry_id,
                    confidence,
                    speaker_status,
                    editorial_status,
                    notes_internal or None,
                    norm_space(row.get('notes_public')) or None,
                    SRC['kaikki_unified'],
                ),
            )
            conn.execute(
                '''
                INSERT OR REPLACE INTO entry_sources (
                    entry_source_id, entry_id, source_id, source_reference, evidence_role,
                    confidence, is_primary, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    'ESR-' + hashlib.sha1(f'{entry_id}|{SRC["kaikki_unified"]}'.encode('utf-8')).hexdigest()[:16],
                    entry_id, SRC['kaikki_unified'],
                    norm_space(row.get('source_reference')) or entry_id,
                    'lexical_base', confidence, 1, None,
                ),
            )
            conn.execute(
                '''
                INSERT OR REPLACE INTO entry_sources (
                    entry_source_id, entry_id, source_id, source_reference, evidence_role,
                    confidence, is_primary, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    'ESR-' + hashlib.sha1(f'{entry_id}|{SRC["out_kaikki_jsonl"]}'.encode('utf-8')).hexdigest()[:16],
                    entry_id, SRC['out_kaikki_jsonl'], entry_id,
                    'parser_output', confidence, 0, 'Derived FCN lexical row',
                ),
            )
            insert_entry_payload(conn, entry_id, SRC['out_kaikki_jsonl'], 'out_kaikki_row', row)

            insert_variant(
                conn=conn,
                entry_id=entry_id,
                source_id=SRC['kaikki_unified'],
                source_reference=norm_space(row.get('source_reference')) or entry_id,
                form_text=preferred_form,
                form_role='preferred_headword',
                register=register,
                variety=variety,
                confidence=confidence,
                editorial_status=editorial_status,
                raw_form=preferred_form,
                normalized_form=preferred_form,
                sort_order=1,
                is_preferred=1,
            )

            try:
                forms = json.loads(row.get('forms_json') or '[]')
            except json.JSONDecodeError:
                forms = []
            if not forms:
                missing_forms += 1
            for idx, form_obj in enumerate(forms, start=2):
                if isinstance(form_obj, dict):
                    form_text = norm_space(form_obj.get('form'))
                    tags = form_obj.get('tags') or []
                    if isinstance(tags, list):
                        form_role = ','.join(str(tag) for tag in tags) or 'source_form'
                    else:
                        form_role = str(tags) or 'source_form'
                    var_variety = norm_space(form_obj.get('variety')) or variety
                else:
                    form_text = norm_space(str(form_obj))
                    form_role = 'source_form'
                    var_variety = variety
                insert_variant(
                    conn=conn,
                    entry_id=entry_id,
                    source_id=SRC['kaikki_unified'],
                    source_reference=norm_space(row.get('source_reference')) or entry_id,
                    form_text=form_text,
                    form_role=form_role,
                    register=register,
                    variety=var_variety,
                    confidence=confidence,
                    editorial_status=editorial_status,
                    raw_form=form_text,
                    normalized_form=form_text,
                    sort_order=idx,
                    is_preferred=1 if normalize_key(form_text) == normalize_key(preferred_form) else 0,
                )

            inserted += 1

    return {
        'inserted_entries': inserted,
        'ehn_entries': ehn,
        'comparative_entries': comparative,
        'classical_entries': classical,
        'missing_gloss_entries': missing_gloss,
        'entries_without_forms_json': missing_forms,
    }


def import_simeon(conn: sqlite3.Connection, repo: Path) -> dict[str, Any]:
    path = repo / 'simeon_parsed.json'
    with path.open('r', encoding='utf-8') as fh:
        payload = json.load(fh)
    entries = payload['entries']

    inserted = 0
    flagged = 0
    with_roots = 0
    with_verbs = 0

    for idx, row in enumerate(entries, start=1):
        entry_id = f'SM::{idx:06d}'
        headword = norm_space(row.get('headword'))
        definition_fr = norm_space(row.get('definition_fr'))
        part_of_speech = norm_space(row.get('pos')) or 'unknown'
        roots = row.get('roots') or []
        root_family = '; '.join(norm_space(r) for r in roots if norm_space(r)) or None
        root_family_code = None
        if roots:
            with_roots += 1
            root_family_code = insert_root_family(conn, norm_space(roots[0]), SRC['simeon_parsed'], f'simeon_parsed.json::entry-{idx:06d}')
        if row.get('is_verb'):
            with_verbs += 1

        editorial_status = choose_simeon_editorial_status(headword, definition_fr)
        if editorial_status == 'Flagged':
            flagged += 1

        notes_internal_parts = []
        if definition_fr:
            notes_internal_parts.append(f'definition_fr={definition_fr}')
        if row.get('is_verb'):
            notes_internal_parts.append('is_verb=True')
        if roots:
            notes_internal_parts.append('roots=' + '; '.join(norm_space(r) for r in roots if norm_space(r)))
        if row.get('calendar'):
            notes_internal_parts.append('calendar=' + json.dumps(row.get('calendar'), ensure_ascii=False))
        if editorial_status == 'Flagged':
            notes_internal_parts.append('ocr_damage_suspected=True')
        notes_internal = ' | '.join(notes_internal_parts)

        conn.execute(
            '''
            INSERT OR REPLACE INTO lexicon_entries (
                entry_id, project_name, sense_order, ehn_spoken_form, msn_headword,
                msn_poetic_form, classical_citation_form, part_of_speech, register,
                variety, gloss_en, gloss_es, root_family, root_family_code,
                source_file, source_reference, source_confidence,
                speaker_validation_status, editorial_status, notes_internal,
                notes_public, source_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                entry_id,
                'Flor y Canto Nahuatl',
                1,
                None,
                None,
                None,
                headword or None,
                part_of_speech,
                'Classical_citation',
                'Classical Nahuatl',
                None,
                None,
                root_family,
                root_family_code,
                'simeon_parsed.json',
                f'simeon_parsed.json::entry-{idx:06d}::{headword}',
                0.75 if editorial_status == 'Flagged' else 0.90,
                'Not_applicable',
                editorial_status,
                notes_internal or None,
                None,
                SRC['simeon_parsed'],
            ),
        )
        conn.execute(
            '''
            INSERT OR REPLACE INTO entry_sources (
                entry_source_id, entry_id, source_id, source_reference, evidence_role,
                confidence, is_primary, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                'ESR-' + hashlib.sha1(f'{entry_id}|{SRC["simeon_parsed"]}'.encode('utf-8')).hexdigest()[:16],
                entry_id, SRC['simeon_parsed'], f'simeon_parsed.json::entry-{idx:06d}::{headword}',
                'classical_reference', 0.90, 1, None,
            ),
        )
        conn.execute(
            '''
            INSERT OR REPLACE INTO entry_sources (
                entry_source_id, entry_id, source_id, source_reference, evidence_role,
                confidence, is_primary, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                'ESR-' + hashlib.sha1(f'{entry_id}|{SRC["simeon_ocr_raw"]}'.encode('utf-8')).hexdigest()[:16],
                entry_id, SRC['simeon_ocr_raw'], f'simeon_1885_ocr_raw.txt::headword::{headword}',
                'archival_backstop', 0.50, 0, 'Raw OCR retained for dispute review only',
            ),
        )
        insert_entry_payload(conn, entry_id, SRC['simeon_parsed'], 'simeon_parsed_entry', row)
        insert_variant(
            conn=conn,
            entry_id=entry_id,
            source_id=SRC['simeon_parsed'],
            source_reference=f'simeon_parsed.json::entry-{idx:06d}::{headword}',
            form_text=headword,
            form_role='classical_headword',
            register='Classical_citation',
            variety='Classical Nahuatl',
            confidence=0.90,
            editorial_status=editorial_status,
            raw_form=headword,
            normalized_form=headword,
            sort_order=1,
            is_preferred=1,
        )
        inserted += 1

    return {
        'inserted_entries': inserted,
        'flagged_ocr_suspect_entries': flagged,
        'entries_with_roots': with_roots,
        'entries_marked_verb': with_verbs,
    }


def build_simeon_headword_map(conn: sqlite3.Connection) -> dict[str, str]:
    mapping: dict[str, str] = {}
    rows = conn.execute(
        '''
        SELECT entry_id, classical_citation_form
        FROM lexicon_entries
        WHERE source_id = ? AND classical_citation_form IS NOT NULL
        ''',
        (SRC['simeon_parsed'],),
    ).fetchall()
    for entry_id, headword in rows:
        key = normalize_key(headword)
        if key and key not in mapping:
            mapping[key] = entry_id
    return mapping


def import_classical_staging(conn: sqlite3.Connection, repo: Path) -> dict[str, Any]:
    examples_path = repo / 'out_classical' / 'classical_examples.jsonl'
    blocks_path = repo / 'out_classical' / 'classical_blocks.jsonl'
    headword_map = build_simeon_headword_map(conn)

    linked_examples = 0
    staged_examples = 0
    staged_blocks = 0

    with examples_path.open('r', encoding='utf-8') as fh:
        for line in fh:
            row = json.loads(line)
            current_headword = norm_space(row.get('current_headword'))
            source_locator = norm_space(row.get('source_locator'))
            example_text = norm_space(row.get('example_text'))
            score = float(row.get('nahuatliness_score') or 0.0)
            key = normalize_key(current_headword)
            matched_entry_id = None
            match_method = None
            if key and len(key) >= 5 and ' ' not in key and score >= 0.80:
                matched_entry_id = headword_map.get(key)
                if matched_entry_id:
                    match_method = 'exact_headword_high_score'
            staging_id = 'CEX-' + hashlib.sha1(f'{source_locator}|{example_text}'.encode('utf-8')).hexdigest()[:16]
            conn.execute(
                '''
                INSERT OR REPLACE INTO classical_examples_staging (
                    staging_id, source_file, source_locator, current_headword,
                    nahuatliness_score, example_text, matched_entry_id,
                    match_method, source_id, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    staging_id,
                    norm_space(row.get('source_file')) or 'simeon_1885_ocr_raw.txt',
                    source_locator,
                    current_headword or None,
                    score,
                    example_text,
                    matched_entry_id,
                    match_method,
                    SRC['out_classical_examples'],
                    None,
                ),
            )
            if matched_entry_id:
                example_id = 'EX-' + hashlib.sha1(f'{matched_entry_id}|{source_locator}|{example_text}'.encode('utf-8')).hexdigest()[:16]
                conn.execute(
                    '''
                    INSERT OR IGNORE INTO examples (
                        example_id, entry_id, example_text_original, example_text_normalized,
                        translation_en, translation_es, register, variety, example_type,
                        source_id, source_reference, confidence, notes_public, notes_internal
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        example_id,
                        matched_entry_id,
                        example_text,
                        example_text,
                        None,
                        None,
                        'Classical_citation',
                        'Classical Nahuatl',
                        'classical_example',
                        SRC['out_classical_examples'],
                        source_locator,
                        min(0.95, max(0.30, score / 1.33)),
                        None,
                        f'match_method={match_method}',
                    ),
                )
                linked_examples += 1
            staged_examples += 1

    with blocks_path.open('r', encoding='utf-8') as fh:
        for line in fh:
            row = json.loads(line)
            current_headword = norm_space(row.get('current_headword'))
            source_locator = norm_space(row.get('source_locator'))
            text = norm_space(row.get('text'))
            score = float(row.get('nahuatliness_score') or 0.0)
            kind = norm_space(row.get('kind')) or 'unknown'
            key = normalize_key(current_headword)
            matched_entry_id = None
            match_method = None
            if key and len(key) >= 5 and ' ' not in key and score >= 0.80:
                matched_entry_id = headword_map.get(key)
                if matched_entry_id:
                    match_method = 'exact_headword_high_score'
            staging_id = 'CBL-' + hashlib.sha1(f'{source_locator}|{text}'.encode('utf-8')).hexdigest()[:16]
            conn.execute(
                '''
                INSERT OR REPLACE INTO classical_blocks_staging (
                    staging_id, source_file, source_locator, current_headword,
                    kind, nahuatliness_score, text, matched_entry_id,
                    match_method, source_id, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    staging_id,
                    norm_space(row.get('source_file')) or 'simeon_1885_ocr_raw.txt',
                    source_locator,
                    current_headword or None,
                    kind,
                    score,
                    text,
                    matched_entry_id,
                    match_method,
                    SRC['out_classical_blocks'],
                    None,
                ),
            )
            staged_blocks += 1

    return {
        'staged_examples': staged_examples,
        'linked_examples': linked_examples,
        'staged_blocks': staged_blocks,
    }


def flag_duplicate_candidates(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = conn.execute(
        '''
        SELECT entry_id,
               COALESCE(ehn_spoken_form, msn_headword, classical_citation_form, '') AS headword,
               part_of_speech, variety, COALESCE(gloss_en, '') AS gloss_en,
               editorial_status, COALESCE(notes_internal, '') AS notes_internal
        FROM lexicon_entries
        '''
    ).fetchall()
    groups: dict[tuple[str, str, str, str], list[str]] = defaultdict(list)
    for entry_id, headword, pos, variety, gloss_en, _status, _notes in rows:
        key = (normalize_key(headword), normalize_key(pos), normalize_key(variety), normalize_key(gloss_en))
        if key[0]:
            groups[key].append(entry_id)
    duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}
    flagged_entries = 0
    for key, entry_ids in duplicate_groups.items():
        note_fragment = f'duplicate_candidate_key={"|".join(key)}'
        for entry_id in entry_ids:
            current_status, current_notes = conn.execute(
                'SELECT editorial_status, COALESCE(notes_internal, "") FROM lexicon_entries WHERE entry_id = ?',
                (entry_id,),
            ).fetchone()
            updated_notes = current_notes
            if note_fragment not in updated_notes:
                updated_notes = (updated_notes + ' | ' if updated_notes else '') + note_fragment
            new_status = 'Flagged' if current_status == 'Imported_raw' else current_status
            conn.execute(
                'UPDATE lexicon_entries SET editorial_status = ?, notes_internal = ?, updated_at = CURRENT_TIMESTAMP WHERE entry_id = ?',
                (new_status, updated_notes, entry_id),
            )
            flagged_entries += 1
    return {
        'duplicate_groups': len(duplicate_groups),
        'duplicate_flagged_entries': flagged_entries,
    }


def write_qa_reports(conn: sqlite3.Connection, qa_dir: Path) -> dict[str, Any]:
    qa_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {}

    summary['lexicon_total'] = conn.execute('SELECT COUNT(*) FROM lexicon_entries').fetchone()[0]
    summary['variant_total'] = conn.execute('SELECT COUNT(*) FROM variants').fetchone()[0]
    summary['example_total'] = conn.execute('SELECT COUNT(*) FROM examples').fetchone()[0]
    summary['payload_total'] = conn.execute('SELECT COUNT(*) FROM entry_payloads').fetchone()[0]
    summary['sources_total'] = conn.execute('SELECT COUNT(*) FROM sources').fetchone()[0]
    summary['entries_missing_pos'] = conn.execute("SELECT COUNT(*) FROM lexicon_entries WHERE part_of_speech IS NULL OR TRIM(part_of_speech) = '' OR part_of_speech = 'unknown'").fetchone()[0]
    summary['entries_missing_gloss'] = conn.execute('SELECT COUNT(*) FROM lexicon_entries WHERE gloss_en IS NULL AND gloss_es IS NULL').fetchone()[0]
    summary['entries_missing_source_link'] = conn.execute('SELECT COUNT(*) FROM lexicon_entries WHERE source_id IS NULL').fetchone()[0]
    summary['entries_needs_review_register'] = conn.execute("SELECT COUNT(*) FROM lexicon_entries WHERE register = 'Needs_review'").fetchone()[0]
    summary['entries_flagged_editorially'] = conn.execute("SELECT COUNT(*) FROM lexicon_entries WHERE editorial_status = 'Flagged'").fetchone()[0]
    summary['entries_without_variants'] = conn.execute(
        'SELECT COUNT(*) FROM lexicon_entries le LEFT JOIN variants v ON le.entry_id = v.entry_id WHERE v.entry_id IS NULL'
    ).fetchone()[0]

    register_counts = conn.execute(
        'SELECT register, COUNT(*) AS n FROM lexicon_entries GROUP BY register ORDER BY n DESC'
    ).fetchall()
    variety_counts = conn.execute(
        'SELECT variety, COUNT(*) AS n FROM lexicon_entries GROUP BY variety ORDER BY n DESC'
    ).fetchall()
    source_counts = conn.execute(
        'SELECT source_id, COUNT(*) AS n FROM lexicon_entries GROUP BY source_id ORDER BY n DESC'
    ).fetchall()
    variant_distribution = conn.execute(
        '''
        SELECT variant_count, COUNT(*) AS entry_count
        FROM (
            SELECT le.entry_id, COUNT(v.variant_id) AS variant_count
            FROM lexicon_entries le
            LEFT JOIN variants v ON le.entry_id = v.entry_id
            GROUP BY le.entry_id
        )
        GROUP BY variant_count
        ORDER BY variant_count
        '''
    ).fetchall()
    duplicate_rows = conn.execute(
        '''
        SELECT entry_id,
               COALESCE(ehn_spoken_form, msn_headword, classical_citation_form, '') AS headword,
               part_of_speech,
               variety,
               COALESCE(gloss_en, '') AS gloss_en,
               editorial_status,
               COALESCE(notes_internal, '') AS notes_internal
        FROM lexicon_entries
        WHERE notes_internal LIKE '%duplicate_candidate_key=%'
        ORDER BY headword, part_of_speech, variety
        '''
    ).fetchall()

    def write_csv(path: Path, headers: list[str], rows: list[tuple[Any, ...]]) -> None:
        with path.open('w', encoding='utf-8', newline='') as fh:
            writer = csv.writer(fh)
            writer.writerow(headers)
            writer.writerows(rows)

    write_csv(qa_dir / 'register_counts.csv', ['register', 'count'], register_counts)
    write_csv(qa_dir / 'variety_counts.csv', ['variety', 'count'], variety_counts)
    write_csv(qa_dir / 'source_counts.csv', ['source_id', 'count'], source_counts)
    write_csv(qa_dir / 'variant_distribution.csv', ['variants_per_entry', 'entry_count'], variant_distribution)
    write_csv(
        qa_dir / 'duplicate_candidates.csv',
        ['entry_id', 'headword', 'part_of_speech', 'variety', 'gloss_en', 'editorial_status', 'notes_internal'],
        duplicate_rows,
    )

    with (qa_dir / 'summary.json').open('w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)

    return summary


def main() -> None:
    args = parse_args()
    repo = Path(args.repo).resolve()
    schema_path = Path(args.schema).resolve()
    db_path = Path(args.db).resolve()
    qa_dir = Path(args.qa_dir).resolve()

    if args.replace_db and db_path.exists():
        db_path.unlink()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    conn.execute('PRAGMA journal_mode = WAL;')
    conn.execute('PRAGMA synchronous = NORMAL;')

    with schema_path.open('r', encoding='utf-8') as fh:
        conn.executescript(fh.read())
    ensure_extension_tables(conn)
    register_sources(conn, repo)
    conn.commit()

    kaikki_stats = import_kaikki(conn, repo)
    conn.commit()
    simeon_stats = import_simeon(conn, repo)
    conn.commit()
    classical_stats = import_classical_staging(conn, repo)
    conn.commit()
    duplicate_stats = flag_duplicate_candidates(conn)
    conn.commit()
    qa_summary = write_qa_reports(conn, qa_dir)
    conn.commit()

    run_summary = {
        'db_path': str(db_path),
        'repo': str(repo),
        'kaikki': kaikki_stats,
        'simeon': simeon_stats,
        'classical_staging': classical_stats,
        'duplicates': duplicate_stats,
        'qa_summary': qa_summary,
    }
    with (qa_dir / 'import_run_summary.json').open('w', encoding='utf-8') as fh:
        json.dump(run_summary, fh, indent=2, ensure_ascii=False)

    print(json.dumps(run_summary, indent=2, ensure_ascii=False))
    conn.close()


if __name__ == '__main__':
    main()
