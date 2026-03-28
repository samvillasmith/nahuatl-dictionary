# Flor y Canto Nahuatl Poetic Register Inventory
**Deliverable 9**  
**Project:** Flor y Canto Nahuatl  
**Version:** 0.1 draft  
**Status:** Foundational literary inventory for MSN-P / poetic-high work

## Purpose

This document establishes the starter inventory for the Flor y Canto Nahuatl poetic register. It is not a final dictionary of poetic Nahuatl. It is the first controlled inventory for identifying, tagging, and expanding high-register material for:

- poetry
- song
- ceremony
- public oratory
- refrain language
- vocative address
- elevated public diction

It is designed to serve the FCN framework already fixed in the project:

- **EHN** = spoken base
- **MSN** = neutral written reference norm
- **MSN-P** = poetic / elevated register

## What this deliverable does

This inventory completes the checklist items for the original Phase 8:

- starter poetic lexicon
- refrain-particle inventory
- vocative inventory
- elevated diction inventory
- rhetorical formula inventory
- annotation rules for songs and poems
- status classification for items as:
  - neutral-high
  - poetic-high
  - classical-only
  - ceremonial
  - proposed literary-modern

## Core principles

1. **Poetic material does not silently overwrite EHN.**  
   A poetic form can be available and valuable without becoming default spoken usage.

2. **Classical evidence is a resource, not a license to flatten registers.**  
   Classical citation can support MSN-P strongly, but it should be marked.

3. **Repetition, parallelism, vocative framing, and ceremonial uplift are structural, not ornamental.**  
   MSN-P is not just “fancier vocabulary.” It is a patterned literary mode.

4. **Every item in the poetic inventory must carry a status.**  
   This prevents uncontrolled mixing of neutral prose, ceremonial language, and classical quotation.

---

# A. Starter Poetic Lexicon

The starter lexicon is intentionally small and high-value. It is meant to seed songwriting, poetic drafting, annotation, and later corpus expansion.

## A1. Seed lexical fields

### Nature / cosmos
- xōchitl / xochitl — flower
- cuīcatl / cuicatl — song
- yōllotl / yollotl — heart
- tonalli — sun / animating warmth / spirit domain
- metztli — moon
- ilhuicatl — sky / heaven
- atl — water
- ehecatl — wind
- tlalli — earth / land

### Human / communal address
- notlaçotzin / notlazotzin — my beloved / dear one
- nopiltzin — my child / dear child
- noteiccauh — my companion / sibling / compatriot
- tocnihuan / tocnihuanh — our companions / our people
- tlahtoani — speaker / ruler / public voice
- macehual — ordinary person / member of the people

### Creative / public acts
- cuīca — to sing
- ītoa / itoa — to speak / to say
- tlatoa — to speak publicly
- ihcuiloa / icuiloa — to write / paint / inscribe
- nextia — to show / reveal
- melahua — to make straight / clarify / set in order

### Affect / inward states
- tlaçōtl / tlazotl — precious / beloved / cherished
- yōllo- compounds — heart / inward feeling compounds
- chōca — to cry / lament
- paqui — to rejoice
- neyolnonotza — to address the heart / inward exhortation

## A2. Usage note

This list is not yet claiming that every item above should always surface in MSN-P in the same form. The point of the seed list is to identify **high-yield poetic domains** that recur across song, lyric, invocation, and public expression.

---

# B. Refrain-Particle Inventory

Refrain particles and refrain-like insertions are central to lyric rhythm, emphasis, and oral recurrence. They should be tagged separately from ordinary lexical items.

## B1. Inventory categories

### B1a. Repetition markers
Used to repeat a line, clause, or phrase with variation.

Examples of annotation tags:
- `REFRAIN_REPEAT`
- `REFRAIN_RETURN`
- `REFRAIN_CLOSER`

### B1b. Calling particles
Used to summon attention or mark an address.

Examples:
- ah
- ay
- o
- ma (when used in exhortive / wishful force)

### B1c. Lyrical fillers / breath markers
Used to carry meter, pacing, or emotional turn.

These must be marked carefully because some may be inherited from performance practice rather than lexical semantics.

## B2. FCN rule

A refrain particle is never treated as “noise.” It is always tagged with:
- formal role
- repeated vs one-off use
- line position
- emotional / rhetorical function if known

---

# C. Vocative Inventory

Vocatives are central to MSN-P because they create the social and ceremonial frame of the utterance.

## C1. Vocative domains

### C1a. Personal address
- beloved
- companion
- child
- friend
- mother / father / elder type address forms

### C1b. Collective address
- people
- companions
- listeners
- community

### C1c. Sacred / ceremonial address
- Lord / Creator / high sacred reference forms
- ceremonial addressee formulas
- public invocation openings

## C2. Annotation requirements

Every vocative should be tagged for:
- addressee type
- intimacy level
- ceremonial force
- line position
- whether literal, metaphorical, or public-oratorical

---

# D. Elevated Diction Inventory

Elevated diction is the lexical layer that helps distinguish MSN-P from neutral MSN.

## D1. High-value elevated diction classes

### D1a. Precious / beauty diction
- flower
- jade / precious stone
- beloved / precious
- radiance / brilliance

### D1b. Voice / speech diction
- song
- speech
- proclamation
- utterance
- testimony / witness

### D1c. Motion / epiphany diction
- arise
- reveal
- descend
- open
- appear
- make known

### D1d. Heart / interiority diction
- heart
- inwardness
- memory
- desire
- sorrow
- joy

## D2. FCN rule

Elevated diction can be:
- fully productive in MSN-P
- restricted to ceremonial usage
- classical citation only
- proposed literary-modern

The inventory must preserve that distinction.

---

# E. Rhetorical Formula Inventory

The poetic register depends as much on formulas as on individual words.

## E1. Core formula types

### E1a. Parallelism
Two balanced lines expressing synonymous or intensifying content.

### E1b. Difrasismo / paired expression
Two-word or two-image expression functioning as one semantic unit.

### E1c. Vocative opening
Line opens by naming the addressee.

### E1d. Refrain return
A repeating line or line fragment that anchors the lyric.

### E1e. Heart-address formula
Speech turns inward and addresses the heart/self.

### E1f. Public-voice formula
The utterance shifts into proclamation, witness, or communal declaration.

## E2. Minimum formula metadata

For every formula entry, record:
- `formula_id`
- `formula_type`
- `formula_text`
- `literal_gloss`
- `poetic_function`
- `register_status`
- `source_basis`
- `notes`

---

# F. Annotation Rules for Songs and Poems

## F1. Minimum annotation layers

Every annotated song or poem should support:

1. **surface text**
2. **normalized text**
3. **translation**
4. **line segmentation**
5. **refrain tagging**
6. **vocative tagging**
7. **formula tagging**
8. **register status tagging**
9. **source / provenance note**

## F2. Required tags

Recommended tags:
- `VOC`
- `REFRAIN`
- `PARALLEL`
- `PAIR_EXPR`
- `CEREMONIAL`
- `CLASSICAL_CITATION`
- `PROPOSED_LITERARY_MODERN`
- `NEUTRAL_HIGH`
- `POETIC_HIGH`

## F3. Annotation rule for bilingual presentation

When a poem or song is published in FCN working materials:
- keep the original lineation
- do not collapse refrains into prose translation
- keep vocatives visible
- gloss formulas in notes, not only in running translation

---

# G. Status System for Poetic/Register Items

Every item in the literary inventory must carry one of the following statuses.

## G1. neutral-high
Definition: elevated but still acceptable in serious neutral prose or public writing.

Use cases:
- public statement
- formal letter
- reflective prose
- careful essay language

## G2. poetic-high
Definition: clearly literary, songlike, or lyric-coded; available for poems and songs, not default neutral prose.

Use cases:
- lyrics
- poems
- public recitation
- elevated dedication language

## G3. classical-only
Definition: retained primarily as citation, allusion, or scholarly/literary reference; not default FCN productive output.

Use cases:
- epigraphs
- annotation
- explicit classical invocation
- citation in literary notes

## G4. ceremonial
Definition: restricted to prayer, invocation, ritualized speech, public ceremony, or sacred address.

Use cases:
- blessings
- formal invocation
- ceremonial song
- ritual speech

## G5. proposed literary-modern
Definition: not directly inherited as a settled productive item but proposed by FCN as a modern literary extension supported by source logic and register need.

Use cases:
- new lyric writing
- songwriting
- literary experiments
- modern public-poetic expression

---

# H. Starter Classification Table

| Item / class | Suggested status | Reason |
|---|---|---|
| xochitl / xōchitl | poetic-high | central flower imagery and lyric emblem |
| cuicatl / cuīcatl | poetic-high | song-identity core term |
| in xochitl in cuicatl | classical-only → poetic-high when explicitly adopted | classical resonance; may be adopted in FCN literary identity |
| yollotl / yōllotl | neutral-high / poetic-high | available in reflective and lyric usage |
| beloved / precious address forms | poetic-high | intimate and elevated address |
| refrain particles | poetic-high / ceremonial | driven by lyric/ritual function |
| strong sacred invocation formulas | ceremonial | domain-restricted |
| direct classical paired expressions | classical-only until adopted | should not be silently normalized |
| carefully regularized high-register compounds | proposed literary-modern | FCN literary extension category |

---

# I. Immediate Build Targets After This Inventory

1. Build a **poetic item table** in the lexicon DB.
2. Build a **formula table** for rhetorical patterns.
3. Build a **song/poem annotation template**.
4. Seed the first **50–100 high-register items**.
5. Annotate the first **10 FCN song/poem samples** with these rules.

---

# J. Completion status against original checklist

This deliverable now covers the original Phase 8 / Deliverable 9 requirements at the framework level:

- starter poetic lexicon — complete as seed inventory
- refrain-particle inventory — complete as inventory class
- vocative inventory — complete as inventory class
- elevated diction inventory — complete as inventory class
- rhetorical formula inventory — complete as inventory class
- annotation rules for songs and poems — complete
- item-status framework — complete

What remains after this deliverable is expansion and population:
- more items
- more examples
- corpus annotation
- integration into the poetic manual and literary workflow
