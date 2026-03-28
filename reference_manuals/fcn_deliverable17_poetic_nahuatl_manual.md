# Flor y Canto Nahuatl — Poetic Nahuatl Manual
## Deliverable 17

**Project:** Flor y Canto Nahuatl
**Version:** 1.0
**Status:** Populated — Phase A seed inventory
**Scope:** Literary register (MSN-P), lyric usage, creative practice, and high-register diction
**Population source:** Phase 9 poetic inventory CSVs, Phase 10 register conversion examples, Phase 9 grammar example bank

---

## 1. Purpose and Audience

This manual defines the FCN poetic register — called MSN-P (MSN-Poetic) — and provides the vocabulary, structural patterns, annotated examples, and governance rules needed to write in elevated literary Nahuatl.

**Primary audiences:**

- Lyricists and songwriters composing in Nahuatl
- Literary poets writing in the elevated register
- Editors preparing ceremonial or public-speech texts
- Teachers designing creative writing tracks
- Literary translators working into Nahuatl

This manual does **not** teach:
- Spoken primer Nahuatl (EHN) — see Deliverable 15
- Plain written prose (MSN neutral) — see Deliverable 16

Writers must be familiar with MSN neutral before using this manual. MSN-P is built on MSN neutral; it is not an entry point.

---

## 2. The FCN Register Model and the Poetic Register

FCN uses three production registers. Each has distinct evidence sources, governance rules, and appropriate output contexts.

| Register | Label | Description | Output context |
|---|---|---|---|
| Spoken standard | EHN | Eastern Huasteca Nahuatl, spoken-first | Primer, conversation, classroom |
| Written standard | MSN neutral | Modern written norm | Education, publishing, plain prose |
| Literary elevated | MSN-P | Elevated lyric/ceremonial register | Song, poetry, ceremony, public speech |

**MSN-P is:**
- Built on MSN neutral as its foundation, not on EHN or Classical Nahuatl directly
- Selectively elevated using approved diction items, structural devices, and marked classical formulas
- Connected to Classical Nahuatl through **annotated adaptation** — not silent borrowing
- Appropriate for: song composition, ceremonial address, literary publishing, public performance

**MSN-P is not:**
- Raw Classical Nahuatl, which requires philological handling and extensive annotation
- EHN spoken usage elevated by accident or stylistic pressure
- A license for unexplained archaism, opaque vocabulary, or unannotated classical quotation
- The default register for all "formal" Nahuatl writing — MSN neutral already covers formal prose

---

## 3. Core Literary Devices

### 3.1 Repetition

Deliberate repetition of a word, phrase, or grammatical structure creates emotional intensity, lyric cadence, and the sense of invocation or insistence.

**Uncontrolled repetition** becomes redundancy. **Controlled repetition** becomes a call.

**Example (EX-P-01):**

| | Nahuatl | English |
|---|---|---|
| Plain prose | *Noyōllo mitztemoa.* | My heart seeks you. |
| Elevated | *Noyōllo, noyōllo, mitztemoa.* | My heart, my heart, seeks you. |

Evidence status: `constructed_pedagogical` (FCN-GRM-C-0001 family)
Device: double invocation — the repeated noun creates a calling or interiority effect
Grammar note: *noyōllo* = no-yōl-lo (1SG-heart-DIM); the diminutive *-lo* is part of the affective coloring, not a grammatical size marker here.

**Rule:** Add repetition to one element per clause. Multiple simultaneous repetitions collapse into noise.

---

### 3.2 Parallelism

Parallel or synonymous lines reinforce a single meaning through structural balance. This is the most pervasive device in Classical Nahuatl poetry. It remains foundational in MSN-P, but it requires approved image pairs — not improvised synonyms.

**Example (EX-P-04):**

| | Nahuatl | English |
|---|---|---|
| Plain prose | *Nicāmati in xōchitl.* | I love the flower. |
| Elevated | *Nicāmati in xōchitl, nicāmati in cuīcatl.* | I love the flower, I love the song. |

Source: `msn_neutral_to_msn_poetic_examples.csv` — parallel pairing
Device: parallel pairing using approved elevated imagery pair (ELV-0001 / ELV-0002)
Note: *xōchitl* / *cuīcatl* is an approved modern poetic pair derived from the classical emblematic compound. Both items have `poetic-high` register status.

**Rule:** Use approved pairs from Section 4 inventory. Do not substitute synonyms from the EHN spoken lexicon into parallel structures — the register signal depends on the specific elevated forms.

---

### 3.3 Vocatives

Direct address — to a person, a collective, the heart, a natural force — opens the lyric social frame. A well-placed vocative transforms a statement into an encounter.

**Example (EX-P-03):**

| | Nahuatl | English |
|---|---|---|
| Plain prose | *Tōnatiuh mōttaz semilhuitl.* | The sun will be seen all day. |
| Elevated | *Tōnatiuh, titlatlanilia, mōttaz semilhuitl.* | O sun, I ask you — may it be seen all day. |

Source: `msn_neutral_to_msn_poetic_examples.csv` — vocative / direct address elevation
Device: vocative address to a natural force + exhortive *mā* construction
Note: Placing the addressee in initial position and following with a first-person request shifts the register from descriptive to relational.

**Rule:** Vocatives must come from the approved inventory (Section 4.2) or be clearly established as plain nouns used in address. Do not use *tlahtoani* (ceremonial) in non-ceremonial contexts without domain establishment; see Section 9.

---

### 3.4 Refrains and Refrain Particles

Refrain particles are short interjections or exclamatory markers that appear at line openings or cadences. They create a rhythmic return, signal emotional or lyric register, and serve as structural anchors in song.

**Available refrain particles:**

| Particle | Function | Example usage |
|---|---|---|
| *ah* | calling / attention | *Ah, noyōllo —* (O, my heart —) |
| *ay* | lyric exclamation / breath turn | *Ay, in xōchitl —* (O, the flower —) |
| *o* | vocative / exclamatory | *O tocnihuan —* (O our companions —) |
| *ma* | exhortive / wish | *Ma neci, ma neci.* (May it appear, may it appear.) |

**Example refrain using REF-0002 + wish construction:**

*Ay, in xōchitl —*
*mā neci, mā neci.*
(O, the flower — / may it appear, may it appear.)

Device: REF-0002 (ay) opening particle + parallel exhortive repetition
Evidence status: `constructed_pedagogical` (from approved inventory items)

**Rule:** Refrain particles mark the poetic register explicitly. Do not use them in MSN neutral prose or primer materials — they are register signals, not neutral interjections.

---

## 4. High-Register Diction Inventory

This section contains the Phase A seed inventory of approved MSN-P diction. All items come from `phase9/` FCN inventory CSVs. Phase B and C expansion details are in Section 11.

### 4.1 Elevated Diction (6 items)

These are lexical items with elevated register status approved for productive use in MSN-P composition.

| ID | FCN Form | Gloss EN | Semantic Domain | Register | Notes |
|---|---|---|---|---|---|
| ELV-0001 | xōchitl | flower | beauty / preciousness | poetic-high | Core floral imagery; approved for modern lyric use |
| ELV-0002 | cuīcatl | song | voice / song | poetic-high | Core lyric identity term; paired with xōchitl in FOR-0002 |
| ELV-0003 | tonalli | sun / animating warmth | radiance / interiority | poetic-high | High symbolic density; use with care to avoid cliché |
| ELV-0004 | yōllotl | heart | interiority | neutral-high | Reflective and lyric usage; usable in elevated prose |
| ELV-0005 | nextia | reveal / show | epiphany | poetic-high | Revelatory motion verb; approved for literary modern use |
| ELV-0006 | icuiloa | write / inscribe | creation | proposed literary-modern | Modern literary utility; status `proposed` — requires annotation |

**Usage notes:**

- **ELV-0001 + ELV-0002** (*xōchitl* / *cuīcatl*) function as an approved modern lyric pair and may be used in parallel constructions without additional annotation.
- **ELV-0006** (*icuiloa*, write/inscribe) carries `proposed literary-modern` status. It is approved for use with an editorial annotation noting its proposed status until broader community validation is achieved.
- **ELV-0003** (*tonalli*) carries significant symbolic density from Classical Nahuatl traditions. Writers should be aware that its range of meaning (day-name, animating force, solar warmth) is wider in classical sources than in the modern lexical baseline.

---

### 4.2 Vocatives (5 items)

Vocatives are terms of direct address. Register status governs where each is usable.

| ID | FCN Form | Gloss EN | Addressee Type | Register | Notes |
|---|---|---|---|---|---|
| VOC-0001 | notlazotzin | beloved / dear one | personal | poetic-high | Intimate elevated address; -tzin is honorific suffix |
| VOC-0002 | nopiltzin | dear child / my child | personal | poetic-high | Familial elevated address; appropriate in lyric to a child-figure |
| VOC-0003 | tocnihuan | our companions / our people | collective | neutral-high | Usable in public or communal register; accessible without poetic framing |
| VOC-0004 | noteiccauh | my companion / comrade | personal | poetic-high | Solidarity address between peers; lyric or ceremonial |
| VOC-0005 | tlahtoani | speaker / lord / public voice | ceremonial / public | ceremonial | Domain-restricted; see Section 9 governance note |

**Vocative construction patterns:**

- Initial position: *Notlazotzin, nikmati…* (Beloved, I feel…)
- Post-refrain particle: *O noteiccauh, tiyāzqueh.* (O comrade, we will go.)
- Collective opener: *Tocnihuan, timoyōltonehuahqueh.* (Companions, we feel sorrow together.) [neutral-high, appropriate for public address without full poetic framing]

---

### 4.3 Refrain Particles (4 items)

| ID | Particle | Function Label | Annotation Role | Register | Notes |
|---|---|---|---|---|---|
| REF-0001 | ah | calling particle | REFRAIN_CALL | poetic-high | Attention / call opening; marks lyric onset |
| REF-0002 | ay | lyric exclamation | REFRAIN_CALL | poetic-high | Breath / emotional turn; used at caesura or line break |
| REF-0003 | o | vocative / exclamatory particle | REFRAIN_CALL | poetic-high | Address marker; precedes vocative or noun of address |
| REF-0004 | ma | exhortive / wish particle | REFRAIN_EXHORT | poetic-high | Wish or exhortive force; combined with intransitive or stative verb |

**Refrain particle combinations:**

- *O [vocative]* — standard vocative opening (REF-0003 + VOC item)
- *Ay, [noun phrase] —* — lyric exclamation + pause (REF-0002 + noun)
- *Ah, [interjection or address] —* — call opening (REF-0001 + address)
- *Ma [verb phrase], ma [verb phrase].* — parallel wish (REF-0004 + parallel construction)

---

### 4.4 Rhetorical Formulas (6 items)

Rhetorical formulas are structural patterns, not individual words. They function as compositional building blocks.

| ID | Type | Formula / Pattern | Poetic Function | Register | Notes |
|---|---|---|---|---|---|
| FOR-0001 | parallelism | [Line A] // [Line B, same structure] | Balanced reinforcement | poetic-high | Paired or synonymous line structure; core device |
| FOR-0002 | paired expression | *in xōchitl, in cuīcatl* | Compressed dual image | classical-only | Classical emblematic pair; requires annotation as classical-derived |
| FOR-0003 | vocative opening | *O [vocative], …* | Address framing | poetic-high | Opens lyric social frame; usable with any approved vocative |
| FOR-0004 | refrain return | repeated closing or opening line | Lyric anchor | poetic-high | Structural repetition creates song form |
| FOR-0005 | heart address | *O my heart / my heart speaks* | Interiority turn | poetic-high | Inward address; uses *noyōllo* or *noyōllotl* |
| FOR-0006 | public voice | *thus we speak / thus it is said* | Proclamatory turn | neutral-high | Usable in public-elevated prose and formal speech |

**FOR-0002 governance note:** The formula *in xōchitl, in cuīcatl* is classified `classical-only`. It may be adapted into MSN-P form (FCN form: *in xōchitl, in cuīcatl* with vowel marking) but must carry an editorial annotation: "Adapted from classical emblematic pair; not for use in primer or neutral prose without literary context note." See Section 8 for the classical-only and note-only policy.

---

## 5. Annotated Examples

Each example shows: source register → elevated form, morpheme gloss, translation, devices used, evidence status, and any governance notes.

---

### EX-P-01 — Repetition: Interiority Address

**Source:** FCN-GRM-C-0001
**Register:** MSN-P
**Evidence status:** `constructed_pedagogical`

| | |
|---|---|
| **Nahuatl** | *Noyōllo, noyōllo, ticuīca.* |
| **Morphemes** | no-yōl-lo — no-yōl-lo — ti-cuīca |
| **Gloss** | 1SG-heart-DIM — 1SG-heart-DIM — 2SG-sing |
| **English** | My little heart, my little heart, you sing. |
| **Spanish** | Corazoncito mío, corazoncito mío, cantas. |

**Devices:** Double invocation (repetition) + interiority address (FOR-0005)
**Commentary:** The noun *noyōllo* is doubled before the predicate, creating a calling effect — the speaker summons the heart as an addressee before attributing action to it. This is the FOR-0005 heart-address formula in its simplest form. The diminutive suffix *-lo* adds affective intimacy, not grammatical diminution.
**Source note:** Constructed from approved inventory; no classical citation required.

---

### EX-P-02 — Classical Formula Adapted: *in xōchitl, in cuīcatl*

**Source:** FCN-GRM-C-0002 + `classical_to_msn_poetic_examples.csv` item 1
**Register:** MSN-P
**Evidence status:** `adapted_from_classical`

| | |
|---|---|
| **Classical citation form** | *in xochitl in cuicatl* |
| **MSN-P adapted form** | *In xōchitl, in cuīcatl.* |
| **Morphemes** | in xōchitl — in cuīcatl |
| **Gloss** | DET flower — DET song |
| **English** | The flower, the song. |
| **Spanish** | La flor, el canto. |

**Operation:** Modernized orthography and vowel marking; retained formulaic parallel structure (FOR-0002)
**Devices:** Paired expression (FOR-0002) — compressed dual image
**Commentary:** The classical form uses the determiner *in* before each noun, creating the characteristic Nahuatl paired-image construction. In MSN-P, this is preserved with modern FCN orthography (vowel length marked with macrons). The pair *xōchitl / cuīcatl* functions as a compressed metaphor for "poetry" or "valued artistic expression."
**Required annotation:** "Adapted from classical emblematic pair (FOR-0002). Classical-only status (classical_to_msn_poetic); not for use in primer or neutral prose. Cross-reference FCN-DICT-0039, FCN-DICT-0040."

---

### EX-P-03 — Vocative Elevation: Nature Address

**Source:** `msn_neutral_to_msn_poetic_examples.csv` item 2
**Register:** MSN-P
**Evidence status:** `editorially_normalized`

| | Plain (MSN neutral) | Elevated (MSN-P) |
|---|---|---|
| **Nahuatl** | *Tōnatiuh mōttaz semilhuitl.* | *Tōnatiuh, titlatlanilia, mōttaz semilhuitl.* |
| **English** | The sun will be seen all day. | O sun, I ask you — may it be seen all day. |

**Operation:** Vocative / direct address elevation
**Devices:** Vocative address to natural force + exhortive particle construction
**Commentary:** In the plain form, *tōnatiuh* is the grammatical subject of a neutral future-tense statement. The elevated form repositions *tōnatiuh* as a second-person addressee: the speaker inserts *titlatlanilia* (I ask you-[sun]) between the address and the resultant wish. This converts a descriptive statement into a lyric petition. The *mā* construction in the original request creates an exhortive or optative force.
**Device used:** FOR-0003 (vocative opening) + extended first-person request clause
**Note:** *Tōnatiuh* is not in the Phase A elevated diction inventory (it is a common noun in EHN). When used as a vocative address to a natural force, context establishes poetic register — no special inventory status is required for common nouns used as direct address.

---

### EX-P-04 — Parallel Pairing: Approved Image Pair

**Source:** `msn_neutral_to_msn_poetic_examples.csv` item 3
**Register:** MSN-P
**Evidence status:** `editorially_normalized`

| | Plain (MSN neutral) | Elevated (MSN-P) |
|---|---|---|
| **Nahuatl** | *Nicāmati in xōchitl.* | *Nicāmati in xōchitl, nicāmati in cuīcatl.* |
| **English** | I love the flower. | I love the flower, I love the song. |

**Operation:** Parallel pairing using approved elevated imagery
**Devices:** FOR-0001 (parallelism) + ELV-0001 (xōchitl) + ELV-0002 (cuīcatl)
**Commentary:** The plain sentence is extended through exact grammatical repetition of the predicate *nicāmati in…* with the second approved pair-term (*cuīcatl*) substituted as object. The structure is symmetric: same verb, same determiner, different noun. This is the canonical FOR-0001 parallel construction. The approval of *xōchitl / cuīcatl* as a modern lyric pair (distinct from the classical-only compound FOR-0002) means this construction can be used without a classical citation annotation.
**Cross-reference:** FCN-DICT-0039 (xōchitl), FCN-DICT-0040 (cuīcatl)

---

### EX-P-05 — Classical Adaptation: Literary Expansion

**Source:** `classical_to_msn_poetic_examples.csv` item 2
**Register:** MSN-P
**Evidence status:** `adapted_from_classical`

| | |
|---|---|
| **Classical citation** | *nicuicanitl* ("I am the singer / I am the song-person") |
| **MSN-P adaptation** | *Ni-cuīca, nicuīca in yōllotl.* |
| **Gloss** | 1SG-sing — 1SG-sing — DET heart |
| **English** | I sing, I sing — the heart. |

**Operation:** Literary expansion — classical nominalized singer-form expanded into repeated verbal predicate with interior-noun object
**Devices:** Repetition (controlled double) + ELV-0004 (yōllotl) as final image
**Commentary:** The classical form *nicuicanitl* compresses "I am a singer" into a single nominalized construction. The MSN-P adaptation unpacks this into a repeated verbal form (*nicuīca, nicuīca*) and ends with the heart as the object or companion of the singing act. This expansion is allowed in literary modern use **only with annotation** that the origin is classical-derived.
**Required annotation:** "Literary expansion from classical *nicuicanitl*; adapted_from_classical. Do not use in primer or neutral prose. Cross-reference FCN-DICT-0041 (yōllotl)."

---

### EX-P-06 — Refrain Particle Construction

**Source:** REF inventory (Phase 9) + constructed
**Register:** MSN-P
**Evidence status:** `constructed_pedagogical`

**Full refrain example:**

*Ay, in xōchitl —*
*mā neci, mā neci.*

| Line | Nahuatl | Gloss | English |
|---|---|---|---|
| 1 | *Ay, in xōchitl —* | EXCL DET flower | O, the flower — |
| 2 | *mā neci, mā neci.* | EXHORT appear EXHORT appear | May it appear, may it appear. |

**Devices:** REF-0002 (ay, lyric exclamation) + ELV-0001 (xōchitl) + REF-0004 (ma, exhortive) + repetition
**Commentary:** The first line opens with the emotional exclamation particle *ay*, introduces the elevated image *xōchitl*, and closes with a syntactic pause (dash). The second line delivers the exhortive wish in parallel — the same construction twice. This is a minimal, functional lyric couplet. It demonstrates how refrain particles and repetition work together: the particle signals register, the image carries content, the parallel repetition creates song-form closure.

---

### EX-P-07 — Communal Vocative: Public Voice

**Source:** FOR-0003 (vocative opening) + VOC-0003 (tocnihuan) + FOR-0006 (public voice)
**Register:** MSN-P (neutral-high blend)
**Evidence status:** `constructed_pedagogical`

*O tocnihuan,*
*ihuiyān timoyōltonehuahqueh.*
*Yuh timitztlahtōhzqueh —*
*ma yuh mochihua.*

| Line | English |
|---|---|
| *O tocnihuan,* | O our companions, |
| *ihuiyān timoyōltonehuahqueh.* | carefully we feel sorrow together. |
| *Yuh timitztlahtōhzqueh —* | Thus we will speak to you — |
| *ma yuh mochihua.* | may it be so. |

**Devices:** FOR-0003 (vocative opening with *o*) + VOC-0003 (tocnihuan, collective, neutral-high) + FOR-0006 (public voice formula) + REF-0004 (*ma* exhortive close)
**Commentary:** This four-line construction opens a public-address lyric. *Tocnihuan* is neutral-high, making it accessible without full poetic framing while still registering elevated intent. The closing *ma yuh mochihua* (may it be so) is a standard public/ceremonial close using the FOR-0006 proclamatory pattern with an exhortive. This combination is appropriate for public speeches, communal songs, or ceremonial address that stops short of full classical-ceremonial register.

---

## 6. Songwriting Exercises

The following exercises develop each of the six core MSN-P skills. Each includes an input, target, worked sample answer, and the governing rule.

---

### Exercise 1: Convert Neutral Prose into Elevated Lyric Form

**Skill:** Applying a single elevation device to a plain sentence
**Input (MSN neutral):** *Noyōllo mitztemoa.* (My heart seeks you.)
**Target:** Elevate using repetition or vocative
**Sample answer:** *Noyōllo, noyōllo, mitztemoa.* — Device: controlled repetition (EX-P-01)
**Rule:** Add **one** device. Do not stack repetition + vocative + elevated noun in a single attempt. Overloading a one-clause sentence collapses the register.

---

### Exercise 2: Write a Refrain from a Thematic Keyword

**Skill:** Building a lyric couplet using a refrain particle and an elevated image
**Keyword:** *yōllotl* (heart, ELV-0004)
**Target:** Write a two-line refrain using the keyword and one refrain particle
**Sample answer:**

*Ah, noyōllotl —*
*mā tlahtoa, mā tlahtoa.*
(O my heart — / may it speak, may it speak.)

**Devices:** REF-0001 (ah) + ELV-0004 (yōllotl) + REF-0004 (ma) + repetition
**Rule:** The refrain particle comes first. It signals register before the image appears. If the particle is removed, the line becomes neutral prose.

---

### Exercise 3: Build a Vocative Line

**Skill:** Opening a lyric with a vocative from the approved inventory
**Addressee:** collective audience (use VOC-0003: *tocnihuan*)
**Target:** Write a single opening line that addresses the collective and sets the lyric frame
**Sample answer:** *O tocnihuan, tiyāzqueh.* (O our companions, we will go.)
**Rule:** Use neutral-high *tocnihuan* for group address without domain restriction. Do not substitute *tlahtoani* (VOC-0005, ceremonial) unless the text explicitly establishes a public-ceremonial context. See Section 9.

---

### Exercise 4: Expand a Neutral Line into Parallel Structure

**Skill:** Applying FOR-0001 (parallelism) with approved image pairs
**Input:** *Nicāmati in xōchitl.* (I love the flower.)
**Target:** Expand into a two-clause parallel using the approved elevated pair
**Sample answer:** *Nicāmati in xōchitl, nicāmati in cuīcatl.* (I love the flower, I love the song.)
**Devices:** FOR-0001 (parallelism) + ELV-0001 + ELV-0002
**Rule:** Use the approved pairs from the Phase A inventory. Do not create ad hoc synonym pairs from the EHN lexicon — unapproved pairs signal neutral register, not poetic elevation.

---

### Exercise 5: Adapt a Classical Formula into a Marked Modern Poetic Line

**Skill:** Converting a classical citation into an annotated MSN-P form
**Classical source:** *in xochitl in cuicatl* (unmodified classical orthography, FOR-0002)
**Target:** Adapt into FCN MSN-P form with required annotation
**Sample answer:**

FCN adapted form: *In xōchitl, in cuīcatl.*
Required annotation: "Adapted from classical emblematic pair (FOR-0002); `adapted_from_classical`. Not for use in primer or neutral prose. Source: Classical Nahuatl poetic tradition."

**Operation:** Modernized orthography (vowel length marked, FCN conventions applied); retained formulaic parallel structure
**Rule:** Every classical adaptation requires its annotation. Stripping the source note makes the adapted formula unauditable and breaks the reversibility of the FCN data model.

---

### Exercise 6: Three-Version Comparison — Too Neutral / Balanced Poetic / Too Archaic

**Skill:** Calibrating register — recognizing undershoot and overshoot
**Topic:** Addressing the sun in a lyric

| Version | Nahuatl | Register | Assessment |
|---|---|---|---|
| Too neutral | *Tōnatiuh tlapoa tlali.* | MSN neutral | Grammatically correct neutral prose. No elevation device. Appropriate for a plain statement, wrong for a lyric. |
| Balanced poetic | *Tōnatiuh, titlatlanilia, mōttaz semilhuitl.* | MSN-P | Vocative direct address + exhortive wish. Correct elevation. (EX-P-03) |
| Too archaic | *Ipalnemohuani, tōnatiuhtzin, mā xinehnemi ōcān* (unannotated classical fragment) | Classical-only violation | Raw classical citation in production text without annotation. Intelligibility blocked for modern readers; register confusion for all audiences. |

**Assessment criteria for "balanced poetic":**
- At least one approved elevation device is present
- Vocabulary comes from the approved inventory or plain nouns in clear address function
- No unannotated classical-only material
- The sentence would be interpretable by a reader with MSN neutral competency

---

## 7. Governance — What Not To Do

The following rules come from `phase10/what_not_to_do_examples.csv`. Each entry names a violation and its consequence.

| Rule | Risk |
|---|---|
| Do not convert classical citation directly into primer dialogue | False everyday naturalness — readers receive archaism as if it were colloquial EHN |
| Do not elevate every neutral sentence into poetic diction | Register inflation — the poetic register loses meaning when applied indiscriminately |
| Do not strip source tracking from adapted classical material | Loss of reversibility — the FCN data model requires annotation for auditing and future correction |
| Do not use ceremonial or classical-only items as default spoken forms | Pedagogical distortion — primer students learn unreachable forms as everyday vocabulary |
| Do not mix EHN spoken forms and classical citation forms in one output without annotation | Register confusion — the reader cannot determine which norm governs the output |

**Application to MSN-P work:**

- Every poetic text produced using this manual should be auditable: each elevated item should map to an inventory ID, and each classical-adapted formula should carry its annotation.
- MSN-P is a **production register**, not a citation field. Items in MSN-P should be writable and readable by a person with solid MSN neutral competency. If a word requires a classical dictionary to parse, it requires annotation.

---

## 8. Classical-Only and Note-Only Material

Some Classical Nahuatl material has strong philological value but is **not suitable for productive reuse** in EHN, MSN neutral, or MSN-P without extensive annotation. These items are designated `note_only`.

From `phase10/classical_to_note_only_examples.csv`:

| Source | Treatment | Policy |
|---|---|---|
| Raw classical citation line | Preserve as note-only citation | Do not force into EHN or neutral-modern prose |
| Classical-only formula with strong philological value | Retain citation + gloss + commentary only | Used as evidence, not productive learning output |

**Policy:** Note-only items appear in editorial apparatus — footnotes, source citations, comparative glossary entries — not in body text. When a classical source is so embedded in a ceremonial or archaic context that adaptation would misrepresent its meaning, it should stay in the note. This is not a failure of the item; it is an accurate representation of what it is.

**FOR-0002 (in xōchitl in cuīcatl)** sits at the boundary: it is `classical-only` but has been authorized for MSN-P adaptation with annotation (see Section 4.4 and EX-P-02). That authorization is formula-specific and does not generalize to other classical-only items.

---

## 9. Ceremonial Item Governance: *tlahtoani* (VOC-0005)

**tlahtoani** — *speaker / lord / public voice* — is the only vocative in the Phase A inventory classified `ceremonial`. It requires special handling.

**What *tlahtoani* means:** In Classical Nahuatl, *tlahtoani* designates a ruler or authoritative public speaker. In modern usage it can mean "the one who speaks" or "speaker/orator" in a public or formal context. The ceremonial classification reflects its domain-restriction: it carries strong formal or authoritative register force that is inappropriate in most lyric contexts.

**Where *tlahtoani* may appear:**
- Clearly marked ceremonial texts (civic, religious, or formal public address)
- Public speech scripts for formal performances where the speaker-as-authority role is established
- Literary texts that explicitly invoke the classical public-voice tradition

**Where *tlahtoani* must not appear:**
- EHN primer materials (EHN register; see Deliverable 15)
- MSN neutral prose (would impose unwarranted ceremonial authority on plain text)
- Personal lyric poetry unless the poem is explicitly about public speech, governance, or ceremony

**For most collective vocative needs:** Use *tocnihuan* (VOC-0003, neutral-high) — "our companions / our people." It carries communal address without domain restriction.

---

## 10. Register Integrity: EHN / MSN-P Boundary

MSN-P is an elevated register built from MSN neutral. EHN (spoken primer) is a distinct register. The two must not be silently merged.

**EHN forms that appear elevated are not automatically MSN-P:**
Adding a refrain particle to an EHN spoken sentence does not produce MSN-P. It produces an annotated spoken register text. If a writer is working from EHN source forms (from Deliverable 15), they must pass through MSN neutral normalization before poetic elevation. The sequence is:

EHN spoken → MSN neutral → MSN-P

**The contamination direction runs both ways:**
- Classical-only or ceremonial items must not silently appear in primer materials (covered in Deliverable 15, Appendix B)
- EHN spoken-only forms must not silently appear in MSN-P as if elevated (covered in Deliverable 16, Section 5)

**Cross-register contrast reminder** (from FCN-GRM-B-0002):

| | Nahuatl | English |
|---|---|---|
| EHN | *EHN ītech tlakakilistli* | EHN belongs to hearing/speech |
| MSN neutral | *MSN neutral ītech tlahcuilōlistli* | MSN neutral belongs to writing |
| MSN-P | MSN-P belongs to elevated literary production — neither primer speech nor plain prose |

---

## 11. Seed Inventory Completeness and Phase B / C Expansion

**Phase A seed inventory (this document):**

| Category | Count |
|---|---|
| Elevated diction items | 6 (ELV-0001 through ELV-0006) |
| Vocatives | 5 (VOC-0001 through VOC-0005) |
| Refrain particles | 4 (REF-0001 through REF-0004) |
| Rhetorical formulas | 6 (FOR-0001 through FOR-0006) |
| **Total Phase A inventory items** | **21** |

**Phase B expansion (planned):**

- Additional elevated diction from Siméon 1885 parsed data (`simeon_parsed.json`, 28,709 entries) — particularly nature, time, and cosmic vocabulary with strong attestation
- Expanded vocative forms beyond the personal + collective seed set
- Additional refrain particle combinations and particle + noun collocations
- Classical formulaic pairs beyond *in xōchitl in cuīcatl* with careful annotation governance

**Phase C expansion (community validation):**

- Formal review of `proposed literary-modern` items — starting with ELV-0006 (*icuiloa*, write/inscribe)
- Community validation pipeline for new modern literary coinages
- Consolidation of approved items into a versioned MSN-P poetic lexicon release

**Status of ELV-0006 (*icuiloa*):** Currently `proposed literary-modern`. It is editorially approved for use with annotation. Promotion to `poetic-high` status requires Phase C community validation. Texts using *icuiloa* in literary contexts should note: "proposed literary-modern status; subject to Phase C review."

---

## 12. Cross-References to FCN Dictionary (Deliverable 18)

The following D18 entries are relevant to MSN-P composition. All entries listed carry validation status `editorially_accepted` or `accepted_for_public_use`.

| D18 Entry ID | FCN Form | Gloss | Register in D18 | Relevant to D17 |
|---|---|---|---|---|
| FCN-DICT-0002 | kuāwtli | eagle | neutral-high / poetic-high | ELV candidate; not yet in Phase A inventory |
| FCN-DICT-0003 | noyōllo | my heart | poetic-high | FOR-0005 (heart address); used in EX-P-01, EX-P-05 |
| FCN-DICT-0039 | xōchitl | flower | poetic-high | ELV-0001; used in EX-P-02, EX-P-04, EX-P-06 |
| FCN-DICT-0040 | cuīcatl | song | poetic-high | ELV-0002; used in EX-P-02, EX-P-04 |
| FCN-DICT-0041 | yōllotl | heart | poetic-high | ELV-0004; used in EX-P-05 |
| FCN-DICT-0042 | tonalli | sun / animating warmth | poetic-high | ELV-0003 |
| FCN-DICT-0043 | nextia | reveal / show | poetic-high | ELV-0005 |
| FCN-DICT-0044 | icuiloa | write / inscribe | proposed literary-modern | ELV-0006 |

Consult Deliverable 18 for full 18-field entries including morpheme segmentation, classical citation forms, and source references.

---

## 13. Deliverable Completion Statement

This document constitutes the populated version of:

**Deliverable 17: Flor y Canto Nahuatl — Poetic Nahuatl Manual**

**Covered in this version (Phase A):**

- FCN register model and MSN-P position within it (Section 2)
- Four core literary devices with worked examples: repetition, parallelism, vocatives, refrains (Section 3)
- Full Phase A seed inventory: 6 elevated diction items, 5 vocatives, 4 refrain particles, 6 rhetorical formulas (Section 4)
- 7 annotated examples drawn from Phase 9 inventory, Phase 10 conversion examples, and Phase 9 grammar example bank (Section 5)
- 6 songwriting exercises, each worked with actual content (Section 6)
- Governance rules: 5 "what not to do" rules with risk labels from Phase 10 data (Section 7)
- Classical-only and note-only policy (Section 8)
- Ceremonial item governance for *tlahtoani* (Section 9)
- EHN / MSN-P register boundary statement (Section 10)
- Phase B / C expansion roadmap and ELV-0006 status note (Section 11)
- Cross-references to 8 FCN-DICT entries in Deliverable 18 (Section 12)

**Population sources used:**
- `phase9/elevated_diction_inventory.csv` — ELV-0001 through ELV-0006
- `phase9/vocative_inventory.csv` — VOC-0001 through VOC-0005
- `phase9/refrain_particle_inventory.csv` — REF-0001 through REF-0004
- `phase9/rhetorical_formula_inventory.csv` — FOR-0001 through FOR-0006
- `phase9/grammar_example_bank.csv` — FCN-GRM-C-0001, FCN-GRM-C-0002, FCN-GRM-B-0002
- `phase10/msn_neutral_to_msn_poetic_examples.csv` — items 1–3
- `phase10/classical_to_msn_poetic_examples.csv` — items 1–2
- `phase10/classical_to_note_only_examples.csv` — policy source
- `phase10/what_not_to_do_examples.csv` — rules 1–5
