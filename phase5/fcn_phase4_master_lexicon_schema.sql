PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    source_file TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL,
    upstream_title TEXT,
    provenance_note TEXT,
    license TEXT NOT NULL,
    retrieval_or_creation_date TEXT,
    project_role TEXT NOT NULL,
    authority_domain TEXT NOT NULL,
    limitations TEXT,
    canonical_status TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS roots_families (
    root_family_code TEXT PRIMARY KEY,
    root_family_label TEXT NOT NULL,
    description TEXT,
    source_id TEXT,
    source_reference TEXT,
    confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    notes TEXT,
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS lexicon_entries (
    entry_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL DEFAULT 'Flor y Canto Nahuatl',
    sense_order INTEGER NOT NULL DEFAULT 1,
    ehn_spoken_form TEXT,
    msn_headword TEXT,
    msn_poetic_form TEXT,
    classical_citation_form TEXT,
    part_of_speech TEXT NOT NULL,
    register TEXT NOT NULL,
    variety TEXT NOT NULL,
    gloss_en TEXT,
    gloss_es TEXT,
    root_family TEXT,
    root_family_code TEXT,
    source_file TEXT NOT NULL,
    source_reference TEXT NOT NULL,
    source_confidence REAL NOT NULL DEFAULT 0.5 CHECK (source_confidence >= 0 AND source_confidence <= 1),
    speaker_validation_status TEXT NOT NULL DEFAULT 'Unreviewed',
    editorial_status TEXT NOT NULL DEFAULT 'Imported_raw',
    notes_internal TEXT,
    notes_public TEXT,
    source_id TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    CHECK (register IN (
        'EHN_colloquial',
        'EHN_formal',
        'MSN_neutral',
        'MSN_public',
        'MSN_poetic',
        'Classical_citation',
        'Comparative_only',
        'Proposed',
        'Deprecated',
        'Needs_review'
    )),
    CHECK (speaker_validation_status IN (
        'Unreviewed',
        'Pending',
        'Validated_speaker',
        'Rejected_speaker',
        'Mixed_feedback',
        'Not_applicable'
    )),
    CHECK (editorial_status IN (
        'Imported_raw',
        'Reviewed',
        'Curated',
        'Approved',
        'Flagged',
        'Deprecated'
    )),
    FOREIGN KEY (source_id) REFERENCES sources(source_id),
    FOREIGN KEY (root_family_code) REFERENCES roots_families(root_family_code)
);

CREATE TABLE IF NOT EXISTS entry_sources (
    entry_source_id TEXT PRIMARY KEY,
    entry_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    source_reference TEXT NOT NULL,
    evidence_role TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    is_primary INTEGER NOT NULL DEFAULT 0 CHECK (is_primary IN (0,1)),
    notes TEXT,
    FOREIGN KEY (entry_id) REFERENCES lexicon_entries(entry_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS variants (
    variant_id TEXT PRIMARY KEY,
    entry_id TEXT NOT NULL,
    form_text TEXT NOT NULL,
    form_role TEXT NOT NULL,
    register TEXT NOT NULL,
    variety TEXT NOT NULL,
    raw_form TEXT,
    normalized_form TEXT,
    orthography_status TEXT NOT NULL DEFAULT 'source_attested',
    source_id TEXT,
    source_reference TEXT,
    confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    editorial_status TEXT NOT NULL DEFAULT 'Imported_raw',
    sort_order INTEGER NOT NULL DEFAULT 1,
    is_preferred INTEGER NOT NULL DEFAULT 0 CHECK (is_preferred IN (0,1)),
    notes TEXT,
    FOREIGN KEY (entry_id) REFERENCES lexicon_entries(entry_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id),
    CHECK (register IN (
        'EHN_colloquial',
        'EHN_formal',
        'MSN_neutral',
        'MSN_public',
        'MSN_poetic',
        'Classical_citation',
        'Comparative_only',
        'Proposed',
        'Deprecated',
        'Needs_review'
    ))
);

CREATE TABLE IF NOT EXISTS examples (
    example_id TEXT PRIMARY KEY,
    entry_id TEXT NOT NULL,
    example_text_original TEXT NOT NULL,
    example_text_normalized TEXT,
    translation_en TEXT,
    translation_es TEXT,
    register TEXT NOT NULL,
    variety TEXT,
    example_type TEXT NOT NULL,
    source_id TEXT,
    source_reference TEXT,
    confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
    notes_public TEXT,
    notes_internal TEXT,
    FOREIGN KEY (entry_id) REFERENCES lexicon_entries(entry_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id),
    CHECK (register IN (
        'EHN_colloquial',
        'EHN_formal',
        'MSN_neutral',
        'MSN_public',
        'MSN_poetic',
        'Classical_citation',
        'Comparative_only',
        'Proposed',
        'Deprecated',
        'Needs_review'
    ))
);

CREATE TABLE IF NOT EXISTS validation (
    validation_id TEXT PRIMARY KEY,
    entry_id TEXT NOT NULL,
    validation_scope TEXT NOT NULL,
    validator_type TEXT NOT NULL,
    validator_name TEXT,
    validation_status TEXT NOT NULL,
    decision_date TEXT,
    comments_public TEXT,
    comments_internal TEXT,
    source_id TEXT,
    FOREIGN KEY (entry_id) REFERENCES lexicon_entries(entry_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE TABLE IF NOT EXISTS literary_notes (
    literary_note_id TEXT PRIMARY KEY,
    entry_id TEXT NOT NULL,
    note_type TEXT NOT NULL,
    usage_domain TEXT,
    note_text TEXT NOT NULL,
    source_id TEXT,
    source_reference TEXT,
    editorial_status TEXT NOT NULL DEFAULT 'Imported_raw',
    notes TEXT,
    FOREIGN KEY (entry_id) REFERENCES lexicon_entries(entry_id) ON DELETE CASCADE,
    FOREIGN KEY (source_id) REFERENCES sources(source_id)
);

CREATE INDEX IF NOT EXISTS idx_lexicon_msn_headword ON lexicon_entries(msn_headword);
CREATE INDEX IF NOT EXISTS idx_lexicon_ehn_spoken_form ON lexicon_entries(ehn_spoken_form);
CREATE INDEX IF NOT EXISTS idx_lexicon_register ON lexicon_entries(register);
CREATE INDEX IF NOT EXISTS idx_lexicon_variety ON lexicon_entries(variety);
CREATE INDEX IF NOT EXISTS idx_lexicon_editorial_status ON lexicon_entries(editorial_status);
CREATE INDEX IF NOT EXISTS idx_lexicon_root_family ON lexicon_entries(root_family);
CREATE INDEX IF NOT EXISTS idx_variants_entry_id ON variants(entry_id);
CREATE INDEX IF NOT EXISTS idx_examples_entry_id ON examples(entry_id);
CREATE INDEX IF NOT EXISTS idx_entry_sources_entry_id ON entry_sources(entry_id);
CREATE INDEX IF NOT EXISTS idx_validation_entry_id ON validation(entry_id);

CREATE VIEW IF NOT EXISTS v_lexicon_flat_export AS
SELECT
    entry_id,
    project_name,
    ehn_spoken_form,
    msn_headword,
    msn_poetic_form,
    classical_citation_form,
    part_of_speech,
    register,
    variety,
    gloss_en,
    gloss_es,
    root_family,
    source_file,
    source_reference,
    source_confidence,
    speaker_validation_status,
    editorial_status,
    notes_internal,
    notes_public
FROM lexicon_entries
WHERE is_active = 1;
