# Flor y Canto Nahuatl Editorial QA Protocol
## Deliverable 12

**Project:** Flor y Canto Nahuatl  
**Version:** 0.1  
**Status:** Internal editorial protocol

---

## 1. Purpose

This protocol defines the required quality-assurance checks for Flor y Canto Nahuatl editorial work before material is accepted for internal use, publication staging, or public release.

It applies to:
- lexical entries
- grammatical explanations
- style-sensitive prose
- register-transformed material
- source-driven annotations
- primer/course outputs
- literary/public-facing material

This protocol is designed to prevent:
- false naturalization
- uncontrolled classical contamination
- hidden source drift
- orthographic inconsistency
- undocumented editorial intervention
- publication of material with unresolved status

---

## 2. QA Levels

### QA-0 — Raw / unreviewed
Material exists but has not passed any formal QA.

### QA-1 — Structural review
Basic structure is present and fields are complete.

### QA-2 — Editorial review
Orthography, formatting, and basic internal consistency checked.

### QA-3 — Register / source review
Register classification and source handling checked.

### QA-4 — Publication-ready internal
Material is internally acceptable for controlled release or compilation.

### QA-5 — Public-release ready
Material has passed full editorial, source, style, and publication review.

---

## 3. Universal QA Fields

Every item under review should eventually carry:
- `item_id`
- `item_type`
- `editorial_status`
- `qa_level`
- `reviewer`
- `review_date`
- `source_reference`
- `register`
- `evidence_status`
- `notes_internal`
- `blocking_issue`
- `approval_state`

---

## 4. Lexical QA Checklist

A lexical item must be checked for:

1. **Headword integrity**
   - headword present
   - headword is stable and normalized according to current policy
   - alternate forms are distinguished from canonical form

2. **Register status**
   - spoken-safe / neutral / poetic / classical-only / ceremonial status marked
   - no classical-only item silently presented as everyday spoken form

3. **Gloss quality**
   - English gloss present
   - Spanish gloss present where required
   - gloss not circular, vague, or misleading

4. **Part of speech**
   - POS is assigned and plausible
   - derivational status is marked where relevant

5. **Source integrity**
   - source file / source reference present
   - provenance not lost during curation
   - source confidence recorded where needed

6. **Editorial notes**
   - uncertainty is noted
   - variant or normalization choice is documented
   - unresolved conflicts are flagged rather than hidden

---

## 5. Grammar QA Checklist

A grammar item must be checked for:

1. **Claim type**
   - is the statement descriptive, pedagogical, comparative, or editorial?
   - if inferential, that is clearly stated

2. **Example quality**
   - example exists
   - example matches the rule being discussed
   - example has gloss and translation
   - example is not overclaimed beyond its evidence status

3. **Evidence posture**
   - attested / lesson-derived / normalized / constructed / adapted / citation-only is marked
   - constructed examples are explicitly labeled

4. **Register fit**
   - spoken examples stay in spoken domain
   - poetic examples are not used as neutral defaults unless marked
   - classical citations are not silently modernized in explanatory prose

5. **Internal consistency**
   - terminology consistent across chapters
   - abbreviations stable
   - rule does not contradict previously accepted grammar sections without note

---

## 6. Style QA Checklist

A style-sensitive item must be checked for:

1. orthographic consistency  
2. punctuation consistency  
3. capitalization policy consistency  
4. glossary / translation style consistency  
5. learner readability or publication readability, depending on target  
6. consistency with orthography manual and style manual  

Questions to ask:
- Is the line written in the project’s adopted system?
- Is the prose too colloquial for neutral writing?
- Is the prose too elevated for primer material?
- Is the diction internally consistent?

---

## 7. Register QA Checklist

All content involving register distinctions must be checked for:

1. **Correct register label**
   - EHN
   - MSN neutral
   - MSN poetic
   - Classical citation
   - note-only / citation-only

2. **Transformation transparency**
   - if transformed, source and target registers are both marked
   - if adapted from classical, that is explicit
   - if note-only, the item is not misrouted into productive pedagogy

3. **Boundary protection**
   - no hidden poetic contamination in primer material
   - no forced neutralization of explicitly literary material
   - no back-projection of classical citation into spoken EHN

---

## 8. Source QA Checklist

Each source-based item must be checked for:

1. legal status / rights class  
2. provenance preserved  
3. source reference preserved  
4. whether the item is direct, normalized, adapted, or inferred  
5. whether the source is open/public, restricted/internal, or citation-only  
6. whether publication use matches rights posture  

---

## 9. Publication QA Checklist

Before publication or release packaging, verify:

1. title and metadata present  
2. version number present  
3. changelog entry present  
4. unresolved blockers reviewed  
5. glossary / notes / citations present where required  
6. no hidden draft markers remain  
7. output matches intended audience and register  
8. source / rights posture is compliant  
9. internal references and cross-links resolve correctly  

---

## 10. Blocking Issues

An item must be blocked from publication if any of the following applies:

- source missing
- register unresolved
- evidence status missing
- orthography unresolved
- translation missing where required
- example clearly mismatched to claim
- legal status unclear for publication use
- classical-only material silently used in primer or neutral content
- unresolved contradiction to accepted project policy

---

## 11. Approval States

Use one of:
- `draft_unreviewed`
- `needs_structural_review`
- `needs_editorial_review`
- `needs_register_review`
- `needs_source_review`
- `needs_publication_review`
- `approved_internal`
- `approved_public`
- `blocked`

---

## 12. Recommended Workflow

1. create item  
2. structural check  
3. editorial check  
4. grammar/style/register/source checks as applicable  
5. resolve blockers  
6. assign QA level  
7. approve for internal or public use  

---

## 13. Minimum Acceptance Standards by Item Type

### Lexical row
Must pass:
- lexical QA
- source QA
- register QA

### Grammar section
Must pass:
- grammar QA
- style QA
- source QA

### Primer unit
Must pass:
- grammar QA
- style QA
- register QA
- publication QA

### Literary/public text
Must pass:
- style QA
- register QA
- source QA
- publication QA

---

## 14. Deliverable Completion Statement

This document completes the structural requirements for:

**Deliverable 12: Flor y Canto Nahuatl Editorial QA Protocol**

Covered:
- lexical QA checklist
- grammar QA checklist
- style QA checklist
- register QA checklist
- source QA checklist
- publication QA checklist
