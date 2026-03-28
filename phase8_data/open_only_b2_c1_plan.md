# FCN Open-Only EHN Proficiency Plan (B2 Core, C1 Stretch)

## Goal
Build an open-only, legally clean pathway that gets average motivated learners to B2-style conversational and reading/writing competence in Eastern Huasteca Nahuatl, with a stretch goal of documentary C1 in controlled domains.

## Open assets already available
- FCN lexical DB and schema
- Phase 6 orthography/style layer
- Phase 7 core lexicon and example exports
- Kaikki EHN + comparative rows
- Siméon classical/reference layer
- UD grammar evidence
- Molina raw OCR for future parsing
- FCN parser pipeline already scoped to ingest Nahuatlahtolli

## Target definitions
- B2 core: independent conversation, narration, explanation, routine argument, connected writing, topic flexibility across familiar and semi-familiar domains.
- Documentary C1 stretch: advanced reading/writing and controlled speaking across curated domains, without claiming field-validated native-like naturalness.

## Workstreams
1. Nahuatlahtolli ingestion
2. Grammar and construction mining
3. Pedagogical corpus generation
4. Curriculum and assessment
5. Tooling/app surface
6. Molina expansion

## Phase A — Unlock the modern course source
Deliverables:
- ingest all Nahuatlahtolli lessons
- create tables: lesson_units, lesson_dialogues, lesson_vocab, lesson_exercises, lesson_notes
- align lesson vocabulary to lexicon_entries
- attach confidence tiers

Exit condition:
- every lesson is queryable as structured rows
- all dialogues exported to CSV/JSONL

## Phase B — Build the construction bank
Deliverables:
- 300–500 reusable sentence patterns
- pattern classes: greeting, identity, possession, location, transitive action, intransitive action, questions, negation, requests, time, cause/purpose, narration, comparison, opinion, repair
- substitution slots linked to lexicon entries
- grammar notes from UD + lesson evidence

Exit condition:
- enough patterns to generate controlled dialogues across 20+ domains

## Phase C — B2 curriculum engine
Deliverables:
- 24 units
- 8 domains for A1/A2
- 8 domains for B1
- 8 domains for B2
- each unit includes: dialogue, vocab, construction drills, grammar focus, listening/reading text, writing task, speaking task, review set

Exit condition:
- a learner can progress from zero to independent conversation in curated domains

## Phase D — Assessment ladder
Deliverables:
- FCN-A1, A2, B1, B2 descriptors
- task bank for each level
- placement test
- mastery checklists
- automated quiz exports

Exit condition:
- learner progress is measurable by communicative tasks, not just word count

## Phase E — Molina expansion
Deliverables:
- parse Molina into structured rows
- align roots, alternants, and lexical families
- use Molina to widen lexical coverage and derivational transparency
- do not let Molina overwrite modern EHN labels

Exit condition:
- richer lexical support for advanced reading/writing and MSN/MSN-P

## Phase F — Documentary C1 stretch
Deliverables:
- curated advanced readings
- essay and summary prompts
- structured debate and explanation tasks
- domain packs: history, religion, literature, governance, education, daily life, public speech
- register control between EHN / MSN / MSN-P

Exit condition:
- strong learners can sustain advanced controlled discourse in curated domains

## Honest ceiling
- B2 is the main public target
- C1 is a documentary/controlled-domain stretch target
- native-like full-spectrum spontaneity is not claimed under the open-only plan

## Immediate next actions
1. finish Nahuatlahtolli ingest
2. add lesson tables to the DB
3. generate first 100 construction patterns
4. ship Units 1–6
5. parse Molina
6. expand to Units 7–24
