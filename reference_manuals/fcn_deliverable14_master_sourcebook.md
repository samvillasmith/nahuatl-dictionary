# Flor y Canto Nahuatl Master Sourcebook
## Deliverable 14

**Project:** Flor y Canto Nahuatl  
**Subtitle:** Eastern Huasteca Nahuatl for Speech · Modern Standard Nahuatl for Writing  
**Version:** 0.1  
**Status:** Internal master compilation draft

---

## Title Page

**Flor y Canto Nahuatl Master Sourcebook**  
A constitutional, linguistic, editorial, instructional, and literary framework for Flor y Canto Nahuatl.

---

## Subtitle Page

**Eastern Huasteca Nahuatl for Speech · Modern Standard Nahuatl for Writing**  
With a poetic high register for literature, song, ceremony, and public voice.

---

## Table of Contents

1. Mission Statement  
2. Founding Charter  
3. Register Charter  
4. Source Hierarchy  
5. Orthography Manual  
6. Style Manual  
7. Lexicon Schema  
8. Curation Rules  
9. Grammar Blueprint  
10. Register Conversion Guide  
11. Editorial QA Protocol  
12. Validation Framework  
13. Appendices  
14. Open Issues Log  
15. Version Log  

---

## 1. Mission Statement

Flor y Canto Nahuatl exists to establish Eastern Huasteca Nahuatl as a teachable spoken standard, Modern Standard Nahuatl as a respected written norm, and a living poetic high register that reconnects Nahuatl speech, literature, song, and public life.

### Expanded mission
The project is infrastructure-first. Its purpose is not merely to preserve Nahuatl as archival material, but to make it teachable, writable, analyzable, publishable, and singable. Flor y Canto Nahuatl therefore treats:
- spoken EHN as the living pedagogical foundation,
- MSN neutral as the written reference norm,
- MSN poetic as the elevated literary-public register,
- and classical material as a source of depth, continuity, and literary inheritance rather than a substitute for living speech.

---

## 2. Founding Charter

### Identity
Flor y Canto Nahuatl is a standardization, pedagogy, and literary framework project.

### Core identity decisions
- **FCN** = Flor y Canto Nahuatl
- **EHN** = Eastern Huasteca Nahuatl (spoken base)
- **MSN** = Modern Standard Nahuatl (written reference norm)
- **MSN-P** = Modern Standard Nahuatl Poetic register

### Founding principles
1. Spoken EHN is the foundation of the project’s conversational and pedagogical work.
2. MSN is a neutral written norm, not a disguised classical register.
3. MSN-P exists to support poetry, song, ceremony, and elevated public discourse.
4. Classical material is a literary and historical source, not a default spoken norm.
5. All editorial transformation should remain source-traceable.
6. Open infrastructure matters: parsable data, provenance, and reusable outputs are part of the mission.

---

## 3. Register Charter

Flor y Canto Nahuatl works with a three-layer register model.

### Spoken Foundation
**EHN**  
Used for:
- primer/dialogue work
- speech-oriented pedagogy
- conversational examples
- spoken-safe lexical defaults

### Written Standard
**MSN neutral**  
Used for:
- manuals
- textbook prose
- public explanatory writing
- dictionary headword normalization
- neutral reference usage

### Poetic Register
**MSN-P**  
Used for:
- poetry
- songs
- elevated lyrical diction
- ceremony/public artistic voice
- controlled literary adaptation

### Charter constraint
No layer may silently replace another. Spoken EHN must not be hidden inside classicalizing prose, and poetic diction must not be quietly injected into primer-safe speech material.

---

## 4. Source Hierarchy

### Primary source classes
1. **Modern spoken / modern pedagogical EHN-aligned material**
2. **Open modern Nahuatl instructional material**
3. **Structured lexical sources**
4. **Grammar evidence sources**
5. **Classical/reference sources**
6. **Editorially constructed pedagogical examples**
7. **Citation-only / note-only evidence**

### Current principal sources in project state
- Kaikki / Wiktionary lexical rows
- Siméon parsed dictionary
- Molina OCR/reference layer
- UD grammar evidence
- Nāhuatlahtolli-derived instructional corpus
- internally curated FCN review DBs

### Source use hierarchy by function
- spoken pedagogy → modern/open/lesson-derived sources first
- neutral writing → normalized spoken + lexical + editorial sources
- poetic writing → poetic inventory + controlled classical adaptation
- citation and philology → classical/reference sources preserved explicitly

### Source limitations
- open documentary material is not the same as full field validation
- classical sources require annotation and source transparency
- constructed examples remain valid for pedagogy only when clearly marked

---

## 5. Orthography Manual

### Current orthographic posture
FCN uses a modernized, teachable representation aligned to the project’s adopted conventions, including:
- `k` rather than legacy `c/qu` for /k/
- `s` rather than historical soft-c variants
- `w` for /w/
- `ts` rather than legacy `tz` where adopted
- `h` for saltillo
- macrons where length marking is editorially supported

### Orthographic goals
- readability
- teachability
- consistency
- reversibility where source comparison matters

### Manual constraints
- primer materials must stay orthographically stable
- classical citation forms may be preserved separately
- normalization choices must be documented, not hidden

---

## 6. Style Manual

### Style goals
The style manual governs:
- prose clarity
- punctuation consistency
- gloss formatting
- translation presentation
- example labeling
- learner readability
- register-appropriate diction

### Style distinctions
- EHN-facing teaching prose should remain plain and stable
- MSN neutral should be controlled and expository
- MSN poetic may be elevated but must remain internally coherent

### Editorial discipline
The style manual exists to prevent drift:
- toward uncontrolled classicization,
- toward mixed orthographies,
- or toward unmarked register confusion.

---

## 7. Lexicon Schema

### Core schema logic
The master lexicon schema is designed to support:
- spoken forms
- neutral written forms
- poetic forms
- classical citation forms
- provenance
- validation
- editorial status
- public vs internal notes

### Canonical fields
- `entry_id`
- `project_name`
- `ehn_spoken_form`
- `msn_headword`
- `msn_poetic_form`
- `classical_citation_form`
- `part_of_speech`
- `register`
- `variety`
- `gloss_en`
- `gloss_es`
- `root_family`
- `source_file`
- `source_reference`
- `source_confidence`
- `speaker_validation_status`
- `editorial_status`
- `notes_internal`
- `notes_public`

### Schema function
The schema is designed not just for storage, but for downstream products:
- dictionaries
- course apps
- lesson packs
- literary inventories
- QA workflows
- validation workflows

---

## 8. Curation Rules

### Curation principles
1. No lexical row without provenance.
2. No silent register reassignment.
3. No classical-only item silently used as everyday speech.
4. No editorial normalization without internal traceability.
5. No pedagogical construction presented as attested unless marked.

### Evidence classes used in current project work
- attested_modern_ehn
- lesson_derived_modern
- editorially_normalized
- comparative_support
- adapted_classical
- citation_only
- constructed_pedagogical

### Current curation posture
The project is honest about its evidence: documentary-engineered where necessary, open-source grounded where possible, and annotation-heavy where literary/classical adaptation occurs.

---

## 9. Grammar Blueprint

### Part A — Spoken EHN grammar
Focus:
- pronunciation
- orthography
- person marking
- possession
- intransitive and transitive verb structure
- imperatives
- questions
- negation
- time/aspect
- location/motion
- discourse and conversation management

### Part B — MSN neutral written grammar
Focus:
- written standard purpose
- normalization
- clause structure
- public prose style
- explanatory syntax
- lexical policy
- cross-register contrast

### Part C — MSN poetic/classical stylistics
Focus:
- elevated diction
- vocatives
- refrain particles
- parallelism
- literary adaptation
- line shaping
- poetic annotation

### Example-bank logic
The grammar blueprint requires examples with:
- register
- evidence status
- glossing
- English translation
- Spanish translation
- source reference
- editorial notes

---

## 10. Register Conversion Guide

### Allowed standard flows
- EHN → MSN neutral
- MSN neutral → MSN poetic
- Classical citation → MSN poetic
- Classical citation → note-only

### Core conversion principle
No register transformation is allowed to erase source identity.

### Summary of rules
- EHN → MSN neutral: normalize for written clarity without importing literary coloration
- MSN neutral → MSN poetic: elevate through approved devices only
- Classical citation → MSN poetic: adapt with annotation
- Classical citation → note-only: preserve when transformation would distort evidence

### Prohibited habits
- back-projecting classical material into spoken EHN
- treating poetic diction as primer default
- hiding adaptation
- collapsing citation and productive output

---

## 11. Editorial QA Protocol

### QA domains
- lexical QA
- grammar QA
- style QA
- register QA
- source QA
- publication QA

### QA levels
- QA-0 raw
- QA-1 structural
- QA-2 editorial
- QA-3 register/source
- QA-4 publication-ready internal
- QA-5 public-release ready

### Blocking conditions
Publication is blocked when:
- source is missing
- register is unresolved
- evidence status is absent
- orthography is unresolved
- translation is missing where required
- hidden classical contamination appears in primer/neutral content
- legal posture is unclear

---

## 12. Validation Framework

### Validation domains
- spoken EHN validation
- literary/public validation

### Core statuses
- unvalidated
- documentary_supported
- editorially_accepted
- provisionally_accepted
- accepted_for_internal_use
- accepted_for_public_use
- restricted_to_note_only
- needs_further_review
- disputed
- rejected

### Disagreement policy
Disagreement must be logged rather than hidden. Items may be:
- held for review,
- routed to note-only,
- reclassified,
- or rejected,
but all such actions must remain visible in internal records.

---

## 13. Appendices

### Appendix A — Current instructional-track achievements
The open-only instructional track now includes:
- a cleaned canonical lesson corpus
- assembled units
- assessment layers
- product bundles
- primer foundation outputs

### Appendix B — Current literary inventory achievements
The poetic register inventory now includes:
- starter poetic lexicon
- refrain-particle inventory
- vocative inventory
- elevated diction inventory
- rhetorical formula inventory
- annotation rules

### Appendix C — Current grammar and conversion architecture
The project now possesses:
- grammar blueprint
- glossing conventions
- conversion guide
- QA and validation framework

---

## 14. Open Issues Log

1. **One-page vision statement** still open.
2. Spoken EHN remains documentary-engineered rather than fully field-validated.
3. Dictionary publication layer still needs final entry-template and public sample build.
4. Public manuals/books still need full drafting and packaging.
5. Corpus folders, workflow templates, and operations system still need formal completion.
6. Release roadmap still needs milestone packaging.
7. Audio / pronunciation support is still a major future expansion area for learner-facing tools.

---

## 15. Version Log

### v0.1
Included:
- mission statement
- founding charter
- register charter
- source hierarchy summary
- orthography summary
- style summary
- lexicon schema summary
- curation rules summary
- grammar blueprint summary
- register conversion summary
- editorial QA summary
- validation framework summary
- appendices
- open issues log
- version log

### Future expansions
Later versions should embed or append the full text of each underlying deliverable rather than summary-level integration only.

---

## Deliverable Completion Statement

This document completes the structural requirements for:

**Deliverable 14: Flor y Canto Nahuatl Master Sourcebook**

Covered:
- Title page
- Subtitle page
- Mission statement
- Founding charter
- Register charter
- Source hierarchy
- Orthography manual
- Style manual
- Lexicon schema
- Curation rules
- Grammar blueprint
- Register conversion guide
- QA protocol
- Validation protocol
- Appendices
- Open issues log
- Version log
