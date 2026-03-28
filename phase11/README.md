# Phase 11 — Editorial QA and Validation (Deliverables 12–13)

Phase 11 defines the quality assurance and validation framework that governs all FCN production outputs.

## What this phase does

- Establishes the 6-level QA scale (QA-0 through QA-5)
- Defines validation status taxonomy for lexicon entries
- Provides a publication-blocking checklist
- Documents the matrix of validation statuses across entry types

## Key files

| File | Description |
|---|---|
| `fcn_deliverable12_editorial_qa_protocol.md` | QA protocol with 6-level scale (7.3 KB) — Deliverable 12 |
| `fcn_deliverable13_validation_framework.md` | Validation framework and status taxonomy (6.4 KB) — Deliverable 13 |
| `qa_checklist_matrix.csv` | QA checklist in matrix form |
| `validation_status_matrix.csv` | Validation statuses by entry type and register |

## QA levels

| Level | Name | Description |
|---|---|---|
| QA-0 | Raw | Imported, unreviewed |
| QA-1 | Cleaned | Orthography normalized |
| QA-2 | Sourced | Source provenance confirmed |
| QA-3 | Register-resolved | Register classification confirmed |
| QA-4 | Evidence-confirmed | Attestation evidence present |
| QA-5 | Publication-ready | Cleared for public release |

## Publication blockers

An entry is blocked from publication if any of the following are unresolved:
- Missing source reference
- Unresolved register classification
- Absent evidence status
- Unresolved orthography conflict
- Unclear legal status of source
- Hidden classical contamination in primer or neutral materials

## Validation status taxonomy

- `accepted_for_public_use` — fully cleared
- `accepted_for_internal_use` — internal use only
- `editorially_accepted` — editor-approved pending formal review
- `provisionally_accepted` — provisional pending evidence confirmation
- `restricted_to_note_only` — classical-only; may not appear in production registers
