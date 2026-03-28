PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS lesson_units (
    lesson_unit_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    lesson_slug TEXT NOT NULL,
    lesson_title TEXT NOT NULL,
    lesson_url TEXT,
    lesson_order INTEGER,
    proficiency_band TEXT NOT NULL DEFAULT 'A1',
    domain_label TEXT,
    summary TEXT,
    source_reference TEXT,
    editorial_status TEXT NOT NULL DEFAULT 'Imported_raw',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_id, lesson_slug),
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS lesson_blocks (
    lesson_block_id TEXT PRIMARY KEY,
    lesson_unit_id TEXT NOT NULL,
    block_order INTEGER NOT NULL,
    block_type TEXT NOT NULL,
    section_label TEXT,
    text_original TEXT NOT NULL,
    text_normalized TEXT,
    translation_en TEXT,
    translation_es TEXT,
    nahuatliness_score REAL DEFAULT 0.0 CHECK (nahuatliness_score >= 0 AND nahuatliness_score <= 1),
    attestation_tier TEXT NOT NULL DEFAULT 'Lesson_attested',
    notes TEXT,
    FOREIGN KEY (lesson_unit_id) REFERENCES lesson_units(lesson_unit_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lesson_dialogues (
    lesson_dialogue_id TEXT PRIMARY KEY,
    lesson_unit_id TEXT NOT NULL,
    block_id TEXT,
    dialogue_order INTEGER NOT NULL,
    speaker_label TEXT,
    utterance_original TEXT NOT NULL,
    utterance_normalized TEXT,
    translation_en TEXT,
    translation_es TEXT,
    communicative_function TEXT,
    attestation_tier TEXT NOT NULL DEFAULT 'Lesson_attested',
    FOREIGN KEY (lesson_unit_id) REFERENCES lesson_units(lesson_unit_id) ON DELETE CASCADE,
    FOREIGN KEY (block_id) REFERENCES lesson_blocks(lesson_block_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS lesson_vocab (
    lesson_vocab_id TEXT PRIMARY KEY,
    lesson_unit_id TEXT NOT NULL,
    surface_form TEXT NOT NULL,
    normalized_form TEXT,
    gloss_en TEXT,
    gloss_es TEXT,
    part_of_speech TEXT,
    variety TEXT NOT NULL DEFAULT 'Eastern Huasteca Nahuatl',
    register TEXT NOT NULL DEFAULT 'EHN_colloquial',
    linked_entry_id TEXT,
    confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    attestation_tier TEXT NOT NULL DEFAULT 'Lesson_attested',
    FOREIGN KEY (lesson_unit_id) REFERENCES lesson_units(lesson_unit_id) ON DELETE CASCADE,
    FOREIGN KEY (linked_entry_id) REFERENCES lexicon_entries(entry_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS pedagogical_units (
    pedagogical_unit_id TEXT PRIMARY KEY,
    unit_code TEXT NOT NULL UNIQUE,
    unit_title TEXT NOT NULL,
    target_band TEXT NOT NULL,
    domain_label TEXT,
    lesson_unit_id TEXT,
    communicative_goal TEXT NOT NULL,
    grammar_focus TEXT,
    lexical_focus TEXT,
    output_task TEXT,
    editorial_status TEXT NOT NULL DEFAULT 'Imported_raw',
    FOREIGN KEY (lesson_unit_id) REFERENCES lesson_units(lesson_unit_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS construction_bank (
    construction_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    lesson_unit_id TEXT,
    source_block_id TEXT,
    proficiency_band TEXT NOT NULL DEFAULT 'A1',
    domain_label TEXT,
    construction_label TEXT NOT NULL,
    pattern_text TEXT NOT NULL,
    slot_schema_json TEXT,
    example_original TEXT,
    example_normalized TEXT,
    explanation TEXT,
    attestation_tier TEXT NOT NULL DEFAULT 'Lesson_attested',
    confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    FOREIGN KEY (source_id) REFERENCES sources(source_id),
    FOREIGN KEY (lesson_unit_id) REFERENCES lesson_units(lesson_unit_id) ON DELETE SET NULL,
    FOREIGN KEY (source_block_id) REFERENCES lesson_blocks(lesson_block_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_lesson_units_band ON lesson_units(proficiency_band);
CREATE INDEX IF NOT EXISTS idx_lesson_blocks_lesson ON lesson_blocks(lesson_unit_id);
CREATE INDEX IF NOT EXISTS idx_lesson_dialogues_lesson ON lesson_dialogues(lesson_unit_id);
CREATE INDEX IF NOT EXISTS idx_lesson_vocab_lesson ON lesson_vocab(lesson_unit_id);
CREATE INDEX IF NOT EXISTS idx_lesson_vocab_linked_entry ON lesson_vocab(linked_entry_id);
CREATE INDEX IF NOT EXISTS idx_construction_bank_band ON construction_bank(proficiency_band);

CREATE VIEW IF NOT EXISTS v_phase8_dialogue_export AS
SELECT
    lu.lesson_unit_id,
    lu.lesson_title,
    lu.proficiency_band,
    d.dialogue_order,
    d.speaker_label,
    d.utterance_original,
    d.utterance_normalized,
    d.translation_en,
    d.translation_es,
    d.communicative_function,
    d.attestation_tier
FROM lesson_units lu
JOIN lesson_dialogues d ON lu.lesson_unit_id = d.lesson_unit_id
ORDER BY lu.lesson_order, d.dialogue_order;

CREATE VIEW IF NOT EXISTS v_phase8_vocab_alignment AS
SELECT
    lu.lesson_title,
    lv.surface_form,
    lv.normalized_form,
    lv.gloss_en,
    lv.part_of_speech,
    lv.linked_entry_id,
    le.msn_headword,
    le.ehn_spoken_form,
    le.gloss_en AS linked_gloss_en,
    lv.confidence
FROM lesson_vocab lv
JOIN lesson_units lu ON lu.lesson_unit_id = lv.lesson_unit_id
LEFT JOIN lexicon_entries le ON le.entry_id = lv.linked_entry_id
ORDER BY lu.lesson_order, lv.surface_form;
