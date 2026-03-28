# Flor y Canto Nahuatl Validation Framework
## Deliverable 13

**Project:** Flor y Canto Nahuatl  
**Version:** 0.1  
**Status:** Internal validation framework

---

## 1. Purpose

This framework defines how Flor y Canto Nahuatl records, evaluates, and resolves validation judgments for:
- spoken EHN-oriented material
- literary/public material
- editorial decisions
- disagreement cases
- approval and rejection outcomes

Validation is not the same as QA.

- **QA** asks: is the item structurally and editorially acceptable?
- **Validation** asks: what kind of authority supports the item, and what decision has been made about its acceptability?

---

## 2. Validation Domains

### A. Spoken EHN validation
Used for:
- primer/dialogue material
- construction bank items
- conversational examples
- speech-oriented grammar examples
- spoken-safe lexical items

### B. Literary / public validation
Used for:
- poetic-high items
- elevated diction
- refrain and vocative usage
- public-performance texts
- literary adaptations from classical material
- ceremonial/public address material

---

## 3. Core Validation Concepts

Each item should be evaluated in terms of:
- attestation
- acceptability
- intelligibility
- register fit
- source fit
- editorial suitability
- disagreement state

---

## 4. Validation Statuses

Recommended statuses:

- `unvalidated`
- `documentary_supported`
- `editorially_accepted`
- `provisionally_accepted`
- `accepted_for_internal_use`
- `accepted_for_public_use`
- `restricted_to_note_only`
- `rejected`
- `needs_further_review`
- `disputed`

### Notes on use
- `documentary_supported` means the item is supported by sources but not necessarily externally validated.
- `editorially_accepted` means the editorial team accepts it under current policy.
- `provisionally_accepted` means acceptable for controlled use pending stronger review.
- `restricted_to_note_only` means preserved, but not productive for active pedagogy or public normalized output.

---

## 5. Spoken EHN Validation Rules

Spoken EHN material should be evaluated for:

1. **spoken plausibility**
2. **primer safety**
3. **non-poetic default suitability**
4. **absence of hidden classical contamination**
5. **high-frequency / pedagogical usefulness**
6. **consistency with current spoken-EHN posture**

### Spoken EHN decision ladder
- documentary-supported but uncertain → `documentary_supported`
- acceptable for primer/internal course use → `accepted_for_internal_use`
- strong confidence for learner-facing release → `accepted_for_public_use`
- doubtful / mixed / over-literary → `needs_further_review` or `restricted_to_note_only`

---

## 6. Literary / Public Validation Rules

Literary/public material should be evaluated for:

1. **register appropriateness**
2. **elevated diction legitimacy**
3. **adaptation transparency**
4. **intelligibility**
5. **non-confusion with raw classical citation**
6. **public-readiness**

### Literary/public decision ladder
- literary but source-anchored and annotated → `editorially_accepted`
- suitable for poetic/public use → `accepted_for_public_use`
- too opaque / too classical / too unstable → `needs_further_review`
- evidence-only classical line → `restricted_to_note_only`

---

## 7. Validation Record Fields

Each validation record should eventually include:
- `validation_id`
- `item_id`
- `item_type`
- `validation_domain`
- `current_validation_status`
- `evidence_basis`
- `register`
- `decision_summary`
- `reviewer`
- `review_date`
- `disagreement_flag`
- `disagreement_summary`
- `final_action`

---

## 8. Disagreement Logging

Disagreement must not be hidden. Record it explicitly.

### Required disagreement fields
- what the disagreement is about
- who flagged it
- which register/domain it affects
- what options are on the table
- temporary status while unresolved
- final disposition once decided

### Typical disagreement types
- spoken vs literary suitability
- neutral vs poetic classification
- normalization choice
- source confidence dispute
- adaptation too strong / too weak
- note-only vs productive-use routing

---

## 9. Approval / Rejection Rules

### Approve when
- source/evidence posture is known
- register fit is acceptable
- QA blockers are resolved
- item has a stable role in FCN

### Reject when
- evidence is too weak for intended use
- register assignment is misleading
- item creates unacceptable contamination
- legal/source posture blocks the intended output
- item contradicts settled FCN policy without reason

### Restrict instead of reject when
- item is important evidence
- but should not be used productively
- or belongs only in notes, appendices, or commentary

---

## 10. Final Actions

Possible final actions:
- `approve_internal`
- `approve_public`
- `hold_for_review`
- `route_to_note_only`
- `reject`
- `reclassify_register`
- `reclassify_evidence_status`

---

## 11. Default Validation Policy by Item Type

### Primer dialogue
Default target: `accepted_for_internal_use` → then `accepted_for_public_use` if clean and stable

### Neutral written example
Default target: `editorially_accepted`

### Poetic adaptation
Default target: `editorially_accepted` or `accepted_for_public_use` with annotation

### Classical citation
Default target: `documentary_supported` or `restricted_to_note_only`

### Constructed pedagogical sentence
Default target: `provisionally_accepted` if useful and clearly labeled

---

## 12. Relationship to Later Phases

This framework should later connect to:
- editorial QA protocol
- grammar blueprint
- register conversion guide
- master sourcebook
- public book workflows
- annotated corpus
- literary workflow
- operations/review queue

---

## 13. Interim Policy

Until external validation capacity expands:

- spoken EHN validation remains conservative
- primer/public spoken content should prefer documentary-supported, internally accepted material
- literary/public texts may proceed under editorial acceptance with clear annotation
- classical material defaults to citation, adaptation, or note-only — never silent assimilation

---

## 14. Deliverable Completion Statement

This document completes the structural requirements for:

**Deliverable 13: Flor y Canto Nahuatl Validation Framework**

Covered:
- spoken EHN validation
- literary/public validation
- validation statuses
- disagreement logging
- approval/rejection rules
