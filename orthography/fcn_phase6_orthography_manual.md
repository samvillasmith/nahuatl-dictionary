# Flor y Canto Nahuatl Orthography Manual

**Deliverable 6**  
**Project:** Flor y Canto Nahuatl  
**Subtitle:** Eastern Huasteca Nahuatl for Speech, Modern Standard Nahuatl for Writing  
**Version:** 0.1  
**Date:** 2026-03-27

## 1. Purpose

This manual defines how Flor y Canto Nahuatl writes Nahuatl across its core layers:

- **EHN** as the spoken pedagogical base
- **MSN / MSN neutral** as the written reference norm
- **MSN-P** as the elevated literary register
- **Classical citation** as source-facing historical reference

The point of this manual is not to erase variation. Its point is to give the project one consistent editorial system for storing, displaying, searching, teaching, and publishing Nahuatl forms.

## 2. Orthographic layers

FCN uses four distinct orthographic layers. They must not be collapsed.

### 2.1 Source-raw form
The source-raw form preserves the spelling found in the source, including legacy spellings, OCR damage, obsolete graphemes, and inconsistent marking of vowel length or saltillo.

This layer exists for provenance and auditability. It is never silently overwritten.

### 2.2 EHN pedagogical form
The EHN pedagogical form is the spoken-facing form used in lessons, example banks, and beginner materials derived from Eastern Huasteca Nahuatl.

Rules:
- stay close to attested EHN usage
- do not silently import classical spellings into EHN
- do not silently import poetic/high-register forms into EHN
- do not add vowel length unless directly supported or later validated
- preserve local spoken integrity over literary prestige

### 2.3 MSN canonical headword
The MSN canonical headword is the preferred written reference form for the lexicon, textbooks, public prose, and future editorial work.

FCN adopts a **modernized phonemic-facing orthography** for MSN.

Core decisions:
- prefer **k** over legacy **c/qu** for /k/
- prefer **s** over legacy **z**, **ç**, and soft **c** for /s/
- prefer **w** over legacy **hu/uh** for /w/
- prefer **ts** over legacy **tz** for /ts/
- preserve **x, ch, tl, y, ll**
- represent saltillo with **h**
- use macrons in canonical forms **only where supported strongly enough for editorial approval**

This gives FCN a consistent written norm without pretending that every current source already uses it.

### 2.4 Search fallback form
The search fallback form is not a public orthographic norm. It is a search aid.

It exists so that all of the following can find the same entry:
- traditional spellings
- phonemic spellings
- forms without macrons
- forms without saltillo marking
- common alternate spellings

Search forms must be generated mechanically and stored as redirects, aliases, or search keys.

## 3. Canonical alphabet for MSN

### 3.1 Core letters
FCN MSN uses the following core symbols:

**a, e, i, o, ā, ē, ī, ō, h, k, l, ll, m, n, p, s, t, tl, ts, w, x, y, ch**

Notes:
- `u` may still appear in loans, names, and inherited forms where required, but it is not the primary grapheme for native /w/
- `q`, `c`, `z`, `ç`, and apostrophe-style saltillo are not canonical MSN graphemes
- these legacy symbols remain searchable and citable in source-raw and historical layers

### 3.2 Capitalization
Use sentence-initial capitalization and proper-name capitalization only.

Do not capitalize common nouns, particles, or poetic diction merely for stylistic effect.

## 4. Vowel length

### 4.1 Canonical decision
FCN recognizes vowel length as a real and meaningful part of the written norm, but it does **not** force speculative length marking into every form.

### 4.2 Representation
Where length is approved, mark it with macrons:
- `ā ē ī ō`

No acute accents, circumflexes, doubled vowels, or ad hoc markers are used in canonical MSN.

### 4.3 Where length is required
Length must be preserved in:
- `msn_poetic_form`
- `classical_citation_form`
- reference-grammar discussion when supported
- dictionary headwords once editorially approved

### 4.4 Where length may be deferred
Length may remain unmarked in:
- EHN pedagogical forms
- provisional MSN headwords imported from legacy data
- beginner materials where the project has not yet validated the quantity

### 4.5 Editorial rule
If vowel length is unknown, leave it unmarked and tag the case for review. Do not invent quantity to make an entry look more classical.

## 5. Saltillo / glottal stop

### 5.1 Canonical decision
FCN represents saltillo with **h** in MSN and MSN-P.

### 5.2 Prohibited canonical spellings
The following are not canonical for saltillo in MSN:
- apostrophe (`'`)
- typographic right quote (`’`)
- omitted marking where the project has approved the segment

### 5.3 When to keep `h`
Keep `h` when it represents saltillo or an approved lexical segment.

Examples from the imported evidence and its normalization environment include patterns such as:
- `ahtlatl`
- `teohcalli`
- `ihxili`
- `xihuitl`

### 5.4 Interaction with `w`
Legacy `hu/uh` sequences representing /w/ are normalized to `w`. Remaining `h` is interpreted as saltillo or as part of a loan or editorially justified form.

Thus:
- `cihuatl` → `siwatl`
- `cuahuitl` → `kuawitl`
- but `ahtlatl` stays `ahtlatl`, not `awtlatl`

## 6. Grapheme normalization rules

These rules define the normal path from legacy/traditional spellings into MSN.

### 6.1 `c / qu / k`
Normalize as follows:
- `qu` before `e/i` → `k`
- hard `c` → `k`
- soft `c` before `e/i` → `s`

Examples:
- `acatl` → `akatl`
- `comalli` → `komalli`
- `cihuatl` → `siwatl`

### 6.2 `z / ç / c(e,i)`
Normalize all /s/-series legacy spellings to `s`.

Examples:
- `eztli` → `estli`
- `oztotl` → `ostotl`
- `miztli` → `mistli`

### 6.3 `hu / uh`
Normalize legacy /w/ spelling to `w`.

Examples:
- `ahuacatl` → `awakatl`
- `ahuiyac` → `awiyak`
- `cohuatl` → `kowatl`
- `cuahuitl` → `kuawitl`

### 6.4 `tz`
Canonical MSN writes `ts`.

Examples:
- source `tz` remains preserved in raw/source forms
- canonical MSN uses `ts` in normalized display and headwording

### 6.5 `x`
Keep `x`.

FCN does not replace canonical `x` with `sh` in MSN.

### 6.6 `ch`
Keep `ch`.

### 6.7 `tl`
Keep `tl`.

### 6.8 `y / i`
Use `y` for the consonantal glide and `i` for the vowel. Do not introduce archaizing `y` where a vowel is intended.

### 6.9 Legacy special characters
Legacy `ç`, inconsistent diacritics, and OCR oddities remain in raw/source layers only. They do not survive into approved MSN headwords.

## 7. Verb citation conventions

### 7.1 Lexical citation rule
FCN cites verbs in their **dictionary lemma form as curated in the lexicon**, without personal prefixes unless the prefix is lexicalized.

### 7.2 Prefix rule
Do not cite ordinary finite person-marked verb tokens as headwords.

### 7.3 Derivational rule
Keep lexicalized derivational material in the headword when it is part of the lexical item, not a runtime inflection.

### 7.4 Future grammar alignment
If later grammar work requires transitivity-class metadata or alternate citation conventions, those belong in the grammar blueprint and metadata tables, not as ad hoc changes to spelling.

## 8. Compound-writing conventions

### 8.1 Solid writing by default
Write lexicalized compounds solid when FCN treats them as established lexical units.

### 8.2 Spaced writing for phrases
Keep transparent phrases spaced when they remain syntactic phrases rather than dictionary compounds.

### 8.3 Hyphen policy
Do not use hyphens in ordinary running Nahuatl orthography except for:
- metalinguistic notation
- suffix or bound-form discussion
- editorial segmentation tables

### 8.4 Reduplication
Write lexicalized reduplication solid unless a special pedagogical note requires segmentation.

## 9. Alternate spellings

### 9.1 Preservation rule
All meaningful alternate spellings must be preserved in `variants` or equivalent alias structures.

### 9.2 Preference rule
Each sense receives one preferred form per relevant register:
- preferred EHN form
- preferred MSN headword
- preferred MSN-P form where applicable
- preferred classical citation form

### 9.3 Labeling rule
Alternate forms must be labeled as one of the following where possible:
- legacy spelling
- comparative spelling
- classical-only
- poetic-only
- source-raw
- OCR-damaged
- proposed

### 9.4 Redirect rule
Non-preferred spellings remain searchable. They are not deleted.

## 10. Search-friendly fallback forms

### 10.1 Purpose
Every approved entry should have at least one search-safe fallback key.

### 10.2 Minimum fallback behavior
Generate search keys by:
- lowercasing
- removing macrons
- normalizing apostrophes and quotes away
- generating both canonical and legacy-compatible spellings where practical

### 10.3 Search examples
Approved entry `siwatl` should be findable by at least:
- `siwatl`
- `cihuatl`
- `siwatl`
- a no-macron equivalent if the stored form contains macrons

Approved entry `kuawitl` should be findable by at least:
- `kuawitl`
- `cuahuitl`
- `kuawitl` without macrons if present in a literary version

### 10.4 Search policy
Search fallback forms are generated automatically. They are never displayed as if they were normative unless the user explicitly requests raw or alternate forms.

## 11. EHN to MSN mapping policy

EHN and MSN are linked, not identical.

### 11.1 Default mapping rule
If an EHN form already matches the approved MSN orthography, keep it.

### 11.2 Graphemic normalization rule
If the EHN source form is a legacy or traditional spelling, map it to the approved MSN graphemes.

### 11.3 Quantity rule
Do not add macrons to EHN merely because a classical form has them.

### 11.4 Saltillo rule
Add or preserve `h` only when there is sufficient source or editorial support.

### 11.5 Example mappings from the imported lexical base
The current imported data already supports normalization pairs such as:

- `acatl` → `akatl`
- `cihuatl` → `siwatl`
- `cuahuitl` → `kuawitl`
- `coyotl` → `koyotl`
- `cohuatl` → `kowatl`
- `oztotl` → `ostotl`
- `eztli` → `estli`
- `miztli` → `mistli`
- `ahuacatl` → `awakatl`
- `ahuiyac` → `awiyak`

These pairs should be treated as the first batch of FCN EHN → MSN normalization evidence, not as isolated curiosities.

## 12. Register-specific orthographic policy

### 12.1 EHN_colloquial
- prioritize spoken usability
- keep forms close to attested EHN evidence
- avoid speculative macrons
- never inject poetic/classical elevation silently

### 12.2 EHN_formal
- same basic orthography as EHN_colloquial
- slightly tighter editorial consistency
- still not identical to MSN by default

### 12.3 MSN_neutral
- use the canonical MSN grapheme system
- use approved normalization rules
- prefer consistent public-readable forms
- use macrons when editorially approved, not merely guessed

### 12.4 MSN_public
- same orthographic base as MSN_neutral
- favor readability and consistency over philological display density

### 12.5 MSN_poetic
- may restore approved macrons more fully
- may preserve saltillo more aggressively
- may prefer elevated lexical choices
- still remains standardized, not orthographically chaotic

### 12.6 Classical_citation
- preserve source-facing historical citation spellings
- do not force classical citation into MSN spelling in the citation field itself

## 13. Editorial approval workflow

### 13.1 Imported state
Imported forms begin as source-faithful or minimally normalized, not as fully approved MSN.

### 13.2 Approval state
A form becomes canonical MSN only after it is:
- source-linked
- orthographically normalized
- checked against variants
- assigned a register
- marked with editorial status

### 13.3 Unknown cases
When orthography is uncertain:
- keep the raw/source form
- generate a provisional normalized candidate if possible
- mark the case `Needs_review`
- do not silently publish the candidate as final

## 14. Operational implementation

Phase 6 is not just a document decision. It must be operationalized.

FCN therefore uses:
- a normalization script to generate candidate MSN forms from imported legacy spellings
- a search-key generator to create fallback lookup forms
- review CSVs so the editorial layer can approve or reject candidates before database write-back

## 15. Locked orthographic decisions for FCN v0.1

For FCN v0.1, the following are now locked:

1. MSN uses a modernized phonemic-facing orthography.
2. `k` replaces legacy `c/qu` for canonical MSN headwords.
3. `s` replaces legacy `z/ç/soft c` for canonical MSN headwords.
4. `w` replaces legacy `hu/uh` where those spell /w/.
5. `ts` replaces legacy `tz` in canonical MSN.
6. Saltillo is written with `h`.
7. Macrons are the only approved length marker.
8. Raw/source spellings are preserved and never silently discarded.
9. Search fallback forms are mandatory infrastructure.
10. EHN and MSN remain linked but distinct layers.

