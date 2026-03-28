# Flor y Canto Nahuatl Phase 7 — Core Lexicon Deliverable

## Deliverable 8
**Flor y Canto Nahuatl Core EHN Lexicon**

This phase operationalizes the imported lexical base into pedagogical core lists. It is grounded in the Phase 5 lexical database and the Phase 6 orthography layer.

## What was built

- 250-word core EHN list
- 500-word expanded EHN list
- 1,000-item core lexicon package
- 100-verb list
- function-word list
- social-interaction list
- everyday example bank

## Current source-boundary reality

The current imported database contains **683 attested EHN rows** and **41 attested EHN verbs**. That means the 1,000-item and 100-verb targets cannot be satisfied from attested EHN alone without pretending the evidence base is larger than it is.

FCN therefore keeps the boundary explicit:

- `EHN_attested` rows come directly from the imported EHN lexical layer.
- `Comparative_gap_fill` rows are proposed expansion candidates drawn from comparative Nahuatl data, prioritized toward Huasteca-adjacent material, and clearly labeled as proposed rather than silently merged into spoken EHN.

## Beginner safety policy

Every Phase 7 list row carries a beginner flag:

- `safe` = usable in beginner materials now
- `unsafe` = keep in the lexicon, but do not place in beginner materials without editorial review

Unsafe rows are typically:

- obsolete/alternate spellings
- bound morphemes
- inflected reference forms
- low-priority or sensitive lexical items
- advanced civic/geographic terms

## Output files

- `core_ehn_250.csv`
- `core_ehn_500.csv`
- `core_ehn_1000.csv`
- `core_verbs_100.csv`
- `function_words.csv`
- `social_interaction.csv`
- `everyday_example_bank.csv`
- `summary.json`
- `fcn_master_lexicon_phase7_review.sqlite`

## Phase 7 completion statement

Phase 7 is complete at the **v0.1 infrastructure level**. The deliverable exists, is queryable, and is aligned with the FCN source and register rules. The next improvement step is not re-architecture; it is **editorial curation and speaker validation** on top of these lists.
