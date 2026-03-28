# Flor y Canto Nahuatl Dictionary
## Deliverable 18

**Project:** Flor y Canto Nahuatl
**Version:** 0.2
**Status:** Working draft — seed dictionary populated
**Scope:** Dictionary design, entry template, and seed entry set (46 entries)

---

## 1. Purpose

This deliverable defines the FCN dictionary as a publication-ready lexical system that connects:
- spoken EHN
- MSN neutral
- MSN poetic
- classical citation
- source tracking
- editorial status
- validation status

---

## 2. Entry Template

Each dictionary entry includes the following 18 fields:

1. `entry_id` — FCN-DICT-XXXX
2. `ehn_spoken_form` — primary spoken EHN form
3. `msn_headword` — canonical MSN neutral headword (base/lemma form)
4. `msn_poetic_form` — elevated literary form where applicable
5. `classical_citation_form` — colonial-era citation form where applicable
6. `part_of_speech` — noun, verb, adjective, adverb, pronoun, conjunction, suffix, etc.
7. `register` — spoken_safe / neutral / neutral-high / poetic-high / classical-only / proposed literary-modern
8. `variety` — EHN / MSN / MSN-P / classical-supported
9. `gloss_en` — English gloss
10. `gloss_es` — Spanish gloss
11. `root_family` — root stem if applicable
12. `source_reference` — source citation
13. `source_confidence` — high / medium / low / confirmed
14. `validation_status` — see D13 Validation Framework
15. `editorial_status` — curated / primer_safe / lesson_derived / poetic_inventory / note_only
16. `notes_public` — notes for public-facing display
17. `notes_internal` — notes for editorial/internal use only
18. `cross_references` — related entries and link types

---

## 3. Entry Directions

Users should be able to move:
- from EHN spoken form to MSN neutral headword
- from MSN neutral to MSN poetic form where allowed
- from modern form to classical citation note
- across lexical family / root family
- across variant or alternate forms

---

## 4. Cross-Reference Rules

Cross-reference types:
- `synonym` — near-equivalent in same register
- `near-synonym` — overlapping but non-identical meaning
- `root-family related` — shares a root stem
- `register-related` — same concept in different register
- `see-also poetic` — elevated form exists; see D17
- `see classical citation` — classical form available for note-only use
- `see spoken form` — EHN spoken form differs from headword
- `see neutral written form` — MSN written form differs from EHN

Cross-references must not:
- silently collapse unlike registers
- hide that one form is classical-only
- erase variant or source differences

---

## 5. Dictionary Entries

### Coverage Note

This seed dictionary contains 46 entries across five domains:
- Core spoken EHN vocabulary (primer-safe, A1–B1 range, Lessons 1–22)
- Grammar and function words
- Interaction phrases and verbs
- Poetic high-register items (Phase 9 inventory)
- Classical-note items (citation-only)

**Validation statuses used:**

| Status | Meaning |
|--------|---------|
| `accepted_for_public_use` | Verified, primer-safe, cleared for publication |
| `accepted_for_internal_use` | Verified for editorial use; pending public release review |
| `editorially_accepted` | FCN editorial judgment applied; cross-source or community validation pending |
| `provisionally_accepted` | Lesson-derived; low linked-entry count; needs further source verification |
| `restricted_to_note_only` | Classical citation form only; not for active EHN/MSN output |

---

### 5A. Model Entries — Fully Fielded

These four entries demonstrate the complete 18-field schema. All subsequent entries use a compact format.

---

#### FCN-DICT-0001 — siwatl

| Field | Value |
|---|---|
| entry_id | FCN-DICT-0001 |
| ehn_spoken_form | siwatl |
| msn_headword | siwatl |
| msn_poetic_form | siwatl |
| classical_citation_form | cihuatl |
| part_of_speech | noun |
| register | spoken_safe / neutral |
| variety | EHN / MSN |
| gloss_en | woman |
| gloss_es | mujer |
| root_family | — |
| source_reference | Kaikki NHE / Nāhuatlahtolli lesson corpus / FCN Phase 8 curation |
| source_confidence | high |
| validation_status | accepted_for_public_use |
| editorial_status | curated |
| notes_public | Core noun. Spoken-safe. Plural: siwāmeh. Used in primer from Lesson 3 onward. |
| notes_internal | Classical form cihuatl used in citation contexts only. EHN and MSN forms are identical. No register distinction needed between spoken and written forms. |
| cross_references | see tlācatl (FCN-DICT-0008, man/person); see mācēhualli (FCN-DICT-0009, community member); see FCN-DICT-0046 (cihuatl, classical citation) |

---

#### FCN-DICT-0002 — kuāwtli

| Field | Value |
|---|---|
| entry_id | FCN-DICT-0002 |
| ehn_spoken_form | kuāwtli |
| msn_headword | kuāwtli |
| msn_poetic_form | kuāwtli |
| classical_citation_form | cuauhtli |
| part_of_speech | noun |
| register | neutral-high / poetic-high |
| variety | MSN / classical-supported |
| gloss_en | eagle |
| gloss_es | águila |
| root_family | — |
| source_reference | Siméon 1885 / Classical sources / FCN editorial normalization |
| source_confidence | high (classical); medium (modern EHN attestation) |
| validation_status | editorially_accepted |
| editorial_status | curated |
| notes_public | Classical form cuauhtli; MSN form kuāwtli follows FCN orthographic normalization: k for c/qu, w for hu/uh. Used in classical and modern literary Nahuatl. Not everyday primer vocabulary. |
| notes_internal | Modern EHN spoken attestation is limited. Primary authority is classical (Siméon 1885). Treat as neutral-high in MSN prose and poetic-high in literary contexts. Do not introduce into spoken EHN primer without community-register confirmation. |
| cross_references | see symbolic imagery / elevated diction; see xōchitl (FCN-DICT-0039) for poetic context |

---

#### FCN-DICT-0003 — noyōllo

| Field | Value |
|---|---|
| entry_id | FCN-DICT-0003 |
| ehn_spoken_form | noyōllo |
| msn_headword | yōllotl |
| msn_poetic_form | noyōllo (possessed poetic form) |
| classical_citation_form | noyollo / yollotl |
| part_of_speech | noun (possessed, 1sg) |
| register | neutral-high / poetic-high |
| variety | MSN / MSN-P |
| gloss_en | my heart (possessed); heart (base form yōllotl) |
| gloss_es | mi corazón (poseído); corazón (yōllotl) |
| root_family | yōl- |
| source_reference | FCN Poetic Register Inventory (Deliverable 9) ELV-0004 / Phase 8.8 lesson corpus / Classical sources |
| source_confidence | high (poetic inventory); confirmed (classical attestation) |
| validation_status | editorially_accepted |
| editorial_status | poetic_inventory |
| notes_public | In poetry and song, noyōllo is the characteristic form (my heart). The MSN headword is yōllotl. In MSN neutral prose, yōllotl can appear unpossessed. In MSN-P, noyōllo is the lyric form: the seat of interiority, address, and emotional force. Possession series: noyōllo / moyōllo / īyōllo / toyōllo. |
| notes_internal | ELV-0004 in Phase 9 inventory; listed neutral-high. Possessed poetic form noyōllo is poetic-high. Do NOT use noyōllo as spoken EHN primer vocabulary — register is elevated. This entry is for literary and MSN-P contexts only. |
| cross_references | see yōllotl (FCN-DICT-0041, base entry); see vocatives (notlazotzin); see refrain constructions; see D17 annotated example FCN-GRM-C-0001 |

---

#### FCN-DICT-0004 — Ximoquētza!

| Field | Value |
|---|---|
| entry_id | FCN-DICT-0004 |
| ehn_spoken_form | Ximoquētza! |
| msn_headword | moquētza |
| msn_poetic_form | — |
| classical_citation_form | — |
| part_of_speech | verb (imperative / reflexive) |
| register | spoken_safe |
| variety | EHN |
| gloss_en | Stand up! (imperative); to stand up, to rise (verb stem) |
| gloss_es | ¡Levántate! (imperativo); ponerse de pie (verbo) |
| root_family | quētza- |
| source_reference | Nāhuatlahtolli instructional corpus / FCN Phase 8 curation |
| source_confidence | high |
| validation_status | accepted_for_public_use |
| editorial_status | primer_safe |
| notes_public | High-frequency classroom and interaction imperative. The form xi-mo-quētza uses the 2sg imperative prefix xi-, the reflexive prefix mo-, and verb stem quētza (to raise, to stand upright). The MSN headword is the reflexive verb stem moquētza. Present 1sg: nimoquētza (I stand up). |
| notes_internal | Grammar bank entry FCN-GRM-A-0002. Primer-safe; no poetic or classical path needed. |
| cross_references | see moquētza (reflexive verb stem); see imperatives and commands; see D15 Unit drills |

---

### 5B. Core Spoken EHN Vocabulary

Entries below use a compact format. All are `variety: EHN` unless noted. Source for most: Nāhuatlahtolli lesson corpus / FCN Phase 8 curation.

---

**FCN-DICT-0005 — piyalli**
POS: interjection | Register: spoken_safe | Confidence: high
EN: hello; greeting | ES: hola; saludo
Source: Nāhuatlahtolli lesson corpus / Phase 8 dialogue sets
Notes (public): Standard EHN greeting. Opens conversations, acknowledges people passing. Primer-safe. No classical or poetic equivalent required.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see cualtitoc (FCN-DICT-0006, affirmative response); see interaction phrases

---

**FCN-DICT-0006 — cualtitoc**
POS: interjection / predicate phrase | Register: spoken_safe | Confidence: high (lesson freq. 4, score 0.9)
EN: fine; OK; all is well | ES: bien; está bien
Source: Nāhuatlahtolli lesson corpus
Notes (public): High-frequency affirming response. Used standalone or as a greeting complement. Also signals acceptance or agreement.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see piyalli (FCN-DICT-0005); see teipan (later/farewell complement)

---

**FCN-DICT-0007 — quēna**
POS: interjection / particle | Register: spoken_safe | Confidence: medium (lesson freq. 4; 0.4 linked entry count)
EN: yes | ES: sí
Source: Nāhuatlahtolli lesson corpus (lessons 11, 19, 27, 31)
Notes (public): Standard affirmative particle. Primer-safe. Used in dialogue responses and confirmations.
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see axcanah (negation forms); see interaction particles

---

**FCN-DICT-0008 — tlācatl**
POS: noun | Register: spoken_safe | Confidence: medium
EN: man; person; human being | ES: hombre; persona; ser humano
Classical citation: tlacatl
Source: Nāhuatlahtolli lesson corpus (lessons 11, 22)
Notes (public): Core person noun. Plural: tlācameh. Appears paired with siwatl (woman) in Lesson 11.
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see siwatl (FCN-DICT-0001); see mācēhualli (FCN-DICT-0009)

---

**FCN-DICT-0009 — mācēhualli**
POS: noun | Register: spoken_safe / neutral | Confidence: medium (lesson freq. 4)
EN: indigenous community member; Nahua person | ES: persona indígena; comunero; macehualli
Classical citation: maceualli
MSN note: In classical Nahuatl, maceualli referred to a commoner within a hierarchical system. In modern EHN, mācēhualli refers to an indigenous community member or Nahua person — the hierarchical sense is not the primary modern meaning. Context-sensitive gloss required.
Source: Nāhuatlahtolli lesson corpus
Notes (public): Core social identity noun in modern EHN. Plural: mācēhualmeh. Do not gloss as "commoner" without historical context note.
Status: accepted_for_internal_use | Editorial: curated
Cross-refs: see tlācatl (FCN-DICT-0008); see register caution — classical meaning differs from modern usage

---

**FCN-DICT-0010 — tequitl**
POS: noun | Register: spoken_safe | Confidence: high (lesson freq. 16, score 0.9)
EN: work; task; job | ES: trabajo; tarea; obligación
Classical citation: tequitl
Source: Nāhuatlahtolli lesson corpus (lessons 10, 12, 17–29)
Notes (public): High-frequency core noun. Possessed forms: notequiuh (my work), motequiuh (your work), ītequiuh (his/her work), totequiuh (our work). When tequitl is possessed, the absolutive suffix -tl drops and -uh is added.
Status: accepted_for_public_use | Editorial: curated
Cross-refs: see nimomachtia (FCN-DICT-0037); see nitlamachtia (FCN-DICT-0038)

---

**FCN-DICT-0011 — tlacualli**
POS: noun | Register: spoken_safe | Confidence: high (lesson freq. 5, score 0.9)
EN: food; meal | ES: comida; alimento
Source: Nāhuatlahtolli lesson corpus (lessons 18, 19, 22, 25, 31)
Notes (public): Core food noun. Communal possessed form: totlacualiz (our food). Key vocabulary in Unit 22 (Our Cornfield and Our Food).
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see chilli (FCN-DICT-0014); see etl (FCN-DICT-0013); see cīntli (FCN-DICT-0016); see tlacualchīhua (to cook — not in current seed set)

---

**FCN-DICT-0012 — ātl**
POS: noun | Register: spoken_safe | Confidence: medium (lesson freq. 4; 0.4 linked entry count; but foundational EHN item)
EN: water | ES: agua
Classical citation: atl
Source: Nāhuatlahtolli lesson corpus (lesson 19, 22, 25, 30)
Notes (public): Core noun. Appears in lesson vocabulary and attested across all Nahuatl varieties. Classical and modern forms are identical (ātl with macron in FCN notation).
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see food and natural environment set

---

**FCN-DICT-0013 — etl**
POS: noun | Register: spoken_safe | Confidence: high (lesson freq. 3, score 0.9)
EN: bean; beans | ES: frijol; frijoles
Classical citation: etl
Source: Nāhuatlahtolli lesson corpus (lessons 7, 21, 22)
Notes (public): Staple food. One of the three foundational Nahua food plants (corn, bean, chili). Classical and EHN forms are identical.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see chilli (FCN-DICT-0014); see cīntli (FCN-DICT-0016); see tlacualli (FCN-DICT-0011)

---

**FCN-DICT-0014 — chilli**
POS: noun | Register: spoken_safe | Confidence: high (lesson freq. 4, score 0.9)
EN: chili pepper | ES: chile
Classical citation: chilli
Source: Nāhuatlahtolli lesson corpus (lessons 18, 19, 22, 27)
Notes (public): Core food noun. Classical and EHN forms identical. One of the three sisters (corn, bean, chili) central to Nahua foodways.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see etl (FCN-DICT-0013); see cīntli (FCN-DICT-0016); see tlacualli (FCN-DICT-0011)

---

**FCN-DICT-0015 — chocolatl**
POS: noun | Register: spoken_safe | Confidence: high (score 0.9)
EN: chocolate drink; cacao-based beverage | ES: chocolate; bebida de cacao
Classical citation: chocolatl
Source: Nāhuatlahtolli lesson corpus (lesson 3)
Notes (public): A drink of pulverized toasted cacao beans and water — cold, foamy, sometimes fermented, sometimes thick. Can include chili, honey, vanilla, and other ingredients. Classical and modern forms identical. Widely known internationally as a Nahuatl-origin loanword.
Status: accepted_for_public_use | Editorial: curated
Cross-refs: see tlacualli (FCN-DICT-0011); see food and drink vocabulary

---

**FCN-DICT-0016 — cīntli**
POS: noun | Register: spoken_safe | Confidence: medium (lesson freq. 2, score 0.4; but core agricultural item)
EN: dried ear of corn; corn cob | ES: mazorca seca de maíz
Classical citation: cintli
Source: Nāhuatlahtolli lesson corpus (lessons 8, 22)
Notes (public): Refers specifically to a dried ear of corn, distinct from fresh cob or the corn plant. Foundational to milpa vocabulary.
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see mīllah (FCN-DICT-0018); see etl, chilli; see Unit 22

---

**FCN-DICT-0017 — tiotlac**
POS: noun | Register: spoken_safe | Confidence: high (lesson freq. 4, score 0.9)
EN: evening; afternoon | ES: tarde
Source: Nāhuatlahtolli lesson corpus (lessons 12, 21, 22, 24)
Notes (public): Time-of-day noun for the afternoon/evening period. Used in daily routine and time-telling vocabulary.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see yāhuatzinco (early morning — not in current seed set); see time vocabulary set

---

**FCN-DICT-0018 — mīllah**
POS: noun (locative) | Register: spoken_safe / neutral | Confidence: medium (lesson freq. 4, score 0.4)
EN: milpa; cornfield; cultivated plot | ES: milpa; sembradío; parcela
Classical citation: millah
Source: Nāhuatlahtolli lesson corpus (lessons 7, 8, 22, 24)
Notes (public): A milpa is a multi-crop cultivated plot, central to Nahua agriculture and community life. The suffix -llah marks a location characterized by the base noun. Communal form: tomīllah (our milpa).
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see cīntli (FCN-DICT-0016); see tequitl (FCN-DICT-0010); see Unit 22

---

**FCN-DICT-0019 — nicān**
POS: adverb | Register: spoken_safe | Confidence: medium (lesson freq. 5, score 0.4)
EN: here | ES: aquí
Source: Nāhuatlahtolli lesson corpus (lessons 3, 22, 26, 27, 31)
Notes (public): High-frequency locative adverb. Attested constructions: nicān niēhua (I am from here), nicān pan caltlamachticān (here at school).
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see cānin (where, FCN-DICT-0024); see niēhua (FCN-DICT-0036)

---

**FCN-DICT-0020 — mōztla**
POS: adverb | Register: spoken_safe | Confidence: medium (lesson freq. 3, score 0.4)
EN: tomorrow | ES: mañana
Classical citation: moztla
Source: Nāhuatlahtolli lesson corpus (lessons 11, 12, 26)
Notes (public): High-frequency time adverb. Attested in Unit 11 future-planning dialogues: tlen ticchīhuaz mōztla? (What will you do tomorrow?), axcanah nihueliz mōztla (I can't tomorrow).
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see tiotlac (evening, FCN-DICT-0017); see future tense constructions (D15 Unit 11)

---

**FCN-DICT-0021 — tōnatiuh**
POS: noun | Register: spoken_safe / neutral-high | Confidence: medium (lesson freq. 3, score 0.4)
EN: the sun; sun | ES: el sol
Classical citation: tonatiuh
Source: Nāhuatlahtolli lesson corpus (lessons 7, 22, 24) / FCN Poetic Inventory (cross-register)
Notes (public): In everyday EHN speech, tōnatiuh is an ordinary noun for the sun and for time-of-day expressions (Quēn moxēloa tōnatiuh — How the day/sun divides). In elevated MSN and MSN-P, tōnatiuh can be addressed as a vocative. See D11 register conversion example. Distinct from tonalli (FCN-DICT-0042).
Status: accepted_for_internal_use | Editorial: curated
Cross-refs: see tonalli (FCN-DICT-0042); see D11 MSN neutral → MSN poetic conversion example (vocative use)

---

### 5C. Grammar and Function Words

---

**FCN-DICT-0022 — huan**
POS: conjunction | Register: spoken_safe | Confidence: high (lesson freq. 24, score 0.9)
EN: and | ES: y
Source: Nāhuatlahtolli lesson corpus (lessons 2–31)
Notes (public): Highest-frequency coordinator. Appears in all 24 primer units. Note: huanya (with/together with) is a related but distinct form appearing in Unit 7. Huan coordinates nouns, clauses, and phrases.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see tlen (FCN-DICT-0023); see grammar function words

---

**FCN-DICT-0023 — tlen**
POS: pronoun / subordinator | Register: spoken_safe | Confidence: high (lesson freq. 32, score 0.9 — appears in all 32 lessons)
EN: what; which; that (relative) | ES: qué; cuál; que (relativo)
MSN note: tlen is the EHN spoken form of classical tlein / tleh
Source: Nāhuatlahtolli lesson corpus (all 32 lessons)
Notes (public): Most frequent item across the entire lesson corpus. Functions as: interrogative (tlen ticchīhua? — what do you do?), relative pronoun (tlen titequiti — what you do/your work), and complementizer (tlen panoc — what happened).
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see cānin (FCN-DICT-0024); see quēniuhqui (FCN-DICT-0025); see quēmman (FCN-DICT-0026)

---

**FCN-DICT-0024 — cānin**
POS: interrogative adverb | Register: spoken_safe | Confidence: medium (lesson freq. 2, score 0.4)
EN: where | ES: dónde
Source: Nāhuatlahtolli lesson corpus (lessons 3, 24)
Notes (public): Interrogative for origin and location. Key Unit 3 constructions: cānin tiēhua? (Where are you from?), cānin titequitiz? (Where will you work?).
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see nicān (here, FCN-DICT-0019); see tlen (what, FCN-DICT-0023); see niēhua (FCN-DICT-0036)

---

**FCN-DICT-0025 — quēniuhqui**
POS: interrogative adverb | Register: spoken_safe | Confidence: medium (lesson freq. 7, score 0.4)
EN: how; in what manner; what (in name questions) | ES: cómo; de qué manera
Source: Nāhuatlahtolli lesson corpus (lessons 3, 8, 9, 10, 18, 19, 31)
Notes (public): Central to the most common primer question: Quēniuhqui motōcah? (What is your name? — literally: How does your name go?). Also used for general how-questions about manner, state, or form.
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see notōcah (FCN-DICT-0035); see tlen (FCN-DICT-0023); see D15 Unit 3 (grammar note on quēniuhqui)

---

**FCN-DICT-0026 — quēmman**
POS: interrogative adverb / temporal adverb | Register: spoken_safe | Confidence: medium (lesson freq. 7, score 0.4)
EN: when; at what time | ES: cuándo; a qué hora
Source: Nāhuatlahtolli lesson corpus (lessons 7, 11, 13, 19, 22, 29, 31)
Notes (public): Used in time-planning contexts. Quēmman motlahpaloah moilliah (When you greet, you say...). Also as an open time reference: quēmman quinequi mocuapaz (when he wants to return home).
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see mōztla (tomorrow, FCN-DICT-0020); see time vocabulary set

---

**FCN-DICT-0027 — quezqui**
POS: interrogative / quantifier | Register: spoken_safe | Confidence: high (lesson freq. 4, score 0.9)
EN: how many; how much | ES: cuánto; cuántos
Source: Nāhuatlahtolli lesson corpus (lessons 4, 9, 21, 27)
Notes (public): Key quantifier in family and counting vocabulary. Quezqui mochochohuan ticpiya? (How many younger siblings do you have?). Age expression: quezqui xīhuitl quipiya (how many years does he/she have = how old is he/she).
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see nahui (FCN-DICT-0028); see mahtlactli (FCN-DICT-0029); see D15 Unit 9

---

**FCN-DICT-0028 — nahui**
POS: numeral | Register: spoken_safe | Confidence: high (score 0.9)
EN: four | ES: cuatro
Source: Nāhuatlahtolli lesson corpus (lessons 7, 19, 22, 28)
Notes (public): Cardinal number. Number series: cē (1), ōme (2), eyi (3), nahui (4), mācuilli (5), chicuacē (6), chicōme (7), chicuēyi (8), chiucnahui (9), mahtlactli (10).
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see mahtlactli (ten, FCN-DICT-0029); see numbers set

---

**FCN-DICT-0029 — mahtlactli**
POS: numeral | Register: spoken_safe | Confidence: high (score 0.9)
EN: ten | ES: diez
Source: Nāhuatlahtolli lesson corpus
Notes (public): Base for numbers 11–19: mahtlactli huan cē (11), mahtlactli huan ōme (12), mahtlactli huan eyi (13), etc. Used in age expressions with xīhuitl (year).
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see nahui (four, FCN-DICT-0028); see numbers and counting set; see D15 Unit 9 (age expressions)

---

**FCN-DICT-0030 — achi**
POS: adverb | Register: spoken_safe | Confidence: high (lesson freq. 3, score 0.9)
EN: a little; somewhat; small | ES: un poco; algo; pequeño
Source: Nāhuatlahtolli lesson corpus (lessons 8, 10, 22)
Notes (public): Degree modifier used before adjectives and verbs: achi huēyi (a bit big), achi tomāhuac (somewhat stout). Core adverb for degree expressions in spoken EHN.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see tlahuel (very, FCN-DICT-0031); see descriptors set

---

**FCN-DICT-0031 — tlahuel**
POS: adverb | Register: spoken_safe | Confidence: high (lesson freq. 5, score 0.9)
EN: very; greatly; really | ES: muy; mucho; bastante
Source: Nāhuatlahtolli lesson corpus (lessons 19, 22, 28, 30, 32)
Notes (public): Intensifier. tlahuel cualli (very good), tlahuel huēyi (very big), tlahuel momati (it is very well understood). High frequency in evaluative and descriptive speech.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see achi (a little, FCN-DICT-0030); see cualtitoc (fine/good, FCN-DICT-0006)

---

**FCN-DICT-0032 — nochi**
POS: determiner / pronoun | Register: spoken_safe | Confidence: high (lesson freq. 3, score 0.9)
EN: all; everything; everyone | ES: todo; todos
Source: Nāhuatlahtolli lesson corpus (lessons 19, 22, 31)
Notes (public): Total quantifier. nochi in tlacualli (all the food), nochi mācēhualmeh (all the community members), nochi tēhuāntin (all of us).
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see quantifiers set

---

**FCN-DICT-0033 — tlamantli**
POS: noun | Register: spoken_safe | Confidence: high (lesson freq. 7, score 0.9)
EN: thing; object; matter; item | ES: cosa; objeto; asunto
Source: Nāhuatlahtolli lesson corpus (lessons 8, 19, 21, 22, 27, 29, 31)
Notes (public): General noun for objects and matters. Used in naming questions: tlen ītōcah tlamantli? (What is the name of this thing?). Also a hedging/general noun when a more specific word is unavailable.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see general vocabulary set

---

**FCN-DICT-0034 — -meh**
POS: suffix (plural marker) | Register: spoken_safe | Confidence: high (score 0.9)
EN: plural suffix for absolutive nouns ending in -tl/-tli | ES: sufijo de plural para sustantivos absolutivos
Source: Nāhuatlahtolli lesson corpus (lesson 3)
Notes (public): Marks the plural of absolutive nouns. Examples: siwatl (woman) → siwāmeh (women); mācēhualli → mācēhualmeh; tlācatl → tlācameh. Stem vowel may lengthen or alter before -meh.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see siwatl (FCN-DICT-0001); see absolutive morphology set

---

### 5D. Interaction Phrases and Verbs

---

**FCN-DICT-0035 — notōcah**
POS: noun (possessed, 1sg) | Register: spoken_safe | Confidence: high
EN: my name | ES: mi nombre
MSN headword: tōcahtli (base/unpossessed nominal stem)
Source: Nāhuatlahtolli lesson corpus (lesson 3)
Notes (public): Most common form in lessons and dialogues. Full possession series: notōcah (my name), motōcah (your name), ītōcah (his/her name), totōcah (our name), amotōcah (your [pl] name), intōcah (their name). Used in canonical primer exchange: Quēniuhqui motōcah? / Na notōcah X.
Status: accepted_for_public_use | Editorial: primer_safe
Cross-refs: see quēniuhqui (FCN-DICT-0025); see D15 Unit 3 (dialogue and constructions)

---

**FCN-DICT-0036 — niēhua**
POS: verb (1sg present) | Register: spoken_safe | Confidence: medium
EN: I am from; I come from; I originate from [place] | ES: soy de; vengo de
MSN headword: ēhua (to come from; to depart from)
Source: Nāhuatlahtolli lesson corpus (lessons 3, 6)
Notes (public): High-frequency construction for personal origin: na niēhua Chicontepec (I am from Chicontepec). Base verb ēhua. Person forms: niēhua (1sg), tiēhua (2sg), ēhua (3sg), tiēhuāh (1pl), anēhuāh (2pl), ēhuāh (3pl). Note: macron on ā in plural forms marks length.
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see cānin (where, FCN-DICT-0024); see nicān (here, FCN-DICT-0019); see D15 Unit 3

---

**FCN-DICT-0037 — nimomachtia**
POS: verb (1sg present) | Register: spoken_safe | Confidence: medium (lesson freq. 3, score 0.4)
EN: I study; I am a student | ES: estudio; soy estudiante
MSN headword: momachtia (to study; to learn)
Source: Nāhuatlahtolli lesson corpus (lessons 3, 5, 6)
Notes (public): Used in occupation and identity dialogues. Full paradigm: nimomachtia (I), timomachtia (you), momachtia (he/she), timomachtiāh (we), anmomachtiāh (you pl.), momachtiāh (they). Pairs with nitlamachtia in Unit 3 and Unit 5 profession dialogues.
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see nitlamachtia (FCN-DICT-0038); see professions vocabulary (D15 Unit 5)

---

**FCN-DICT-0038 — nitlamachtia**
POS: verb (1sg present) | Register: spoken_safe | Confidence: medium (lesson freq. 3, score 0.4)
EN: I teach | ES: enseño; soy maestro/maestra
MSN headword: tlamachtia (to teach)
Source: Nāhuatlahtolli lesson corpus (lessons 3, 5, 6)
Notes (public): Occupation verb used in profession dialogues. Attested construction: na nitlamachtia nāhuatl (I teach Nahuatl). Paradigm: nitlamachtia (1sg), titlamachtia (2sg), tlamachtia (3sg).
Status: accepted_for_internal_use | Editorial: primer_safe
Cross-refs: see nimomachtia (FCN-DICT-0037); see tequitl (FCN-DICT-0010); see D15 Unit 5

---

### 5E. Poetic High-Register Items

These items are drawn from the FCN Poetic Register Inventory (Deliverable 9). They are NOT primer vocabulary. They belong to MSN-P (elevated literary register) and must not appear in spoken EHN pedagogy without explicit register marking.

---

**FCN-DICT-0039 — xōchitl**
POS: noun | Register: poetic-high | Confidence: confirmed (classical + Phase 9 inventory ELV-0001)
EN: flower | ES: flor
Classical citation: xochitl
Semantic domain: beauty / preciousness
Source: FCN Phase 9 Poetic Inventory ELV-0001 / Classical sources
Notes (public): Core floral imagery in Nahuatl poetic tradition. The flower is a central emblem of beauty, value, and lyric identity. In classical poetry: xōchitl pairs with cuīcatl in the formula in xōchitl in cuīcatl (the flower, the song). In MSN-P, xōchitl is available as a living poetic image, not only a citation.
Notes (internal): Do NOT use as everyday EHN spoken word without register context. This is a literary item.
Status: editorially_accepted | Editorial: poetic_inventory
Cross-refs: see cuīcatl (FCN-DICT-0040); see FOR-0002 (classical formula, D9); see D17 annotated examples

---

**FCN-DICT-0040 — cuīcatl**
POS: noun | Register: poetic-high | Confidence: confirmed (classical + Phase 9 inventory ELV-0002)
EN: song; lyric utterance | ES: canto; canción; voz lírica
Classical citation: cuicatl
Semantic domain: voice / song
Source: FCN Phase 9 Poetic Inventory ELV-0002 / Classical sources
Notes (public): Core lyric identity term. In MSN-P, cuīcatl names the elevated speech-act of singing — the poetic/song act itself, not merely a melody. Paired with xōchitl in the classical formula in xōchitl in cuīcatl. Not interchangeable with an ordinary word for song in EHN conversation.
Status: editorially_accepted | Editorial: poetic_inventory
Cross-refs: see xōchitl (FCN-DICT-0039); see D17 High-Register Diction; see FOR-0002 (D9)

---

**FCN-DICT-0041 — yōllotl**
POS: noun | Register: neutral-high / poetic-high | Confidence: confirmed (classical + Phase 9 ELV-0004)
EN: heart | ES: corazón
Classical citation: yollotl
Root family: yōl-
Semantic domain: interiority
Source: FCN Phase 9 Poetic Inventory ELV-0004 / Classical sources
Notes (public): Base headword for the heart. In MSN neutral, yōllotl is neutral-high — it can appear as an ordinary noun for heart (organ or seat of emotion). In MSN-P, the possessed form noyōllo is the characteristic lyric form. Possession series: noyōllo / moyōllo / īyōllo / toyōllo. See FCN-DICT-0003 for the possessed poetic entry.
Status: editorially_accepted | Editorial: curated
Cross-refs: see noyōllo (FCN-DICT-0003); see tonalli (FCN-DICT-0042); see D17 annotated examples

---

**FCN-DICT-0042 — tonalli**
POS: noun | Register: poetic-high | Confidence: confirmed (Phase 9 ELV-0003 / classical sources)
EN: animating warmth; spirit-heat; solar essence; day-sign | ES: calor animador; fuerza solar; tonalli
Classical citation: tonalli
Semantic domain: radiance / interiority
Source: FCN Phase 9 Poetic Inventory ELV-0003 / Classical sources
Notes (public): tonalli carries dense symbolic meaning: the animating warmth granted by the sun, the day-sign given at birth, the spirit-quality associated with solar force. In MSN-P, tonalli is used for internal radiance, gifted vitality, and solar imagery of selfhood. Distinct from tōnatiuh (the sun as physical object, FCN-DICT-0021). Not for EHN spoken primer use.
Status: editorially_accepted | Editorial: poetic_inventory
Cross-refs: see tōnatiuh (FCN-DICT-0021); see xōchitl (FCN-DICT-0039); see D17 High-Register Diction

---

**FCN-DICT-0043 — nextia**
POS: verb | Register: poetic-high | Confidence: editorially confirmed (Phase 9 ELV-0005 / classical)
EN: to reveal; to make appear; to show forth | ES: revelar; hacer aparecer; manifestar
Classical citation: nextia
Semantic domain: epiphany / revelation
Source: FCN Phase 9 Poetic Inventory ELV-0005 / Classical sources
Notes (public): A revelatory motion verb. In poetic contexts, nextia conveys something made manifest — light, beauty, truth being brought into appearance. In MSN-P, nextia carries the sense of a poetic epiphany: something revealed through the act of song or speech. Not used as an ordinary verb of showing in EHN conversation.
Status: editorially_accepted | Editorial: poetic_inventory
Cross-refs: see xōchitl (FCN-DICT-0039); see D17 annotated examples; see cuīcatl (FCN-DICT-0040)

---

**FCN-DICT-0044 — icuiloa**
POS: verb | Register: proposed literary-modern | Confidence: classical confirmed; modern literary extension is FCN editorial proposal
EN: to write; to inscribe; to compose in writing | ES: escribir; inscribir; componer por escrito
Classical citation: ihcuiloa (to write, paint, inscribe)
Semantic domain: creation / inscription
Source: FCN Phase 9 Poetic Inventory ELV-0006
**CAUTION — PROPOSED STATUS:** The modern literary extension of ihcuiloa to mean "to compose poetically / to inscribe literary work" is an FCN editorial proposal, not independently attested in modern EHN. Must be used with annotation in published material until community validation.
Notes (public): Classical ihcuiloa means to write, paint, or draw. The FCN project proposes this verb for modern literary Nahuatl (MSN-P) as a verb of poetic composition and inscription. Users should be aware this is a proposed literary-modern extension, not a documented modern spoken form.
Status: provisionally_accepted (editorial proposal only)
Cross-refs: see cuīcatl (FCN-DICT-0040); see D9 ELV-0006; see validation framework (D13, proposed status)

---

### 5F. Classical-Note Items

These entries are present as classical citation forms. Not recommended as active EHN spoken forms or MSN neutral prose vocabulary without explicit register annotation.

---

**FCN-DICT-0045 — tlahtolli**
POS: noun | Register: neutral / classical-supported | Confidence: medium (Lesson 8 corpus; 0.4)
EN: word; speech; language; discourse | ES: palabra; habla; lengua; discurso
Classical citation: tlahtoli / tlatoli
Source: Nāhuatlahtolli lesson corpus (lesson 8) / Classical sources
Notes (public): In classical and literary Nahuatl, tlahtolli is a foundational cultural concept — speech as a precious, formal act. In modern EHN, tlahtolli is used for "word" or "language." In MSN neutral, appropriate as a formal noun for language, discourse, or text. Not classical-only — has modern MSN neutral use.
Status: accepted_for_internal_use | Editorial: curated
Cross-refs: see mācēhualli (FCN-DICT-0009); see nāhuatl (language name — not a separate entry in current set)

---

**FCN-DICT-0046 — cuauhtli (classical citation)**
POS: noun | Register: classical citation / note-only | Confidence: confirmed (Siméon 1885)
EN: eagle | ES: águila
EHN/MSN active form: kuāwtli (see FCN-DICT-0002)
Source: Siméon 1885 / Colonial Nahuatl sources
Notes (public): This entry preserves the classical citation form cuauhtli for reference and cross-linking. The active MSN dictionary headword is kuāwtli (FCN-DICT-0002). Do not use cuauhtli as the primary headword in EHN or MSN neutral output. In classical quotations and philological notes, cuauhtli is the correct citation form.
Status: restricted_to_note_only
Cross-refs: see kuāwtli (FCN-DICT-0002, active MSN headword)

---

## 6. Cross-Reference Chains — Worked Examples

### Chain A: siwatl — From spoken form to classical citation, plural, and semantic neighbors

```
siwatl (FCN-DICT-0001)
  → classical citation: cihuatl (FCN-DICT-0046) — "see classical spelling in citation contexts"
  → plural form: siwāmeh — "see -meh suffix (FCN-DICT-0034) for plural formation"
  → gender pair: tlācatl (FCN-DICT-0008) — "man/person"
  → social category: mācēhualli (FCN-DICT-0009) — "broader community member category"
```

This chain demonstrates: EHN spoken form → classical citation → morphological derivation → semantic neighbors.

---

### Chain B: noyōllo — From possessed poetic form to base headword, root family, and literary context

```
noyōllo (FCN-DICT-0003) — poetic possessed form "my heart"
  → base headword: yōllotl (FCN-DICT-0041) — "heart, neutral-high"
  → root family: yōl- — also in moyōllo (your heart), toyōllo (our heart), inyōllo (their heart)
  → literary context: D17 annotated example FCN-GRM-C-0001
       "Noyōllo, noyōllo, ticuīca." — My little heart, my little heart, you sing.
  → register caution: noyōllo is poetic-high; do not use in EHN spoken primer
```

This chain demonstrates: possessed poetic form → base headword → root family → literary register context.

---

### Chain C: Ximoquētza! — From imperative form to verb stem and paradigm

```
Ximoquētza! (FCN-DICT-0004) — imperative "Stand up!"
  → verb stem: moquētza (reflexive: to stand up) — see FCN-DICT-0004 notes
  → root: quētza- (to raise, to set upright, to stand)
  → morphology: xi- (2sg imperative prefix) + mo- (reflexive) + quētza (verb stem)
  → present paradigm:
      nimoquētza (I stand up)
      timoquētza (you stand up)
      moquētza (he/she stands up)
  → related: Ximotlālī! (sit down! — not in current seed set; same xi- + mo- pattern)
```

This chain demonstrates: imperative form → verb stem → morphological transparency → verb paradigm.

---

## 7. Publication Format Examples — siwatl in Four Formats

### 7A. Database Row (CSV)

```
FCN-DICT-0001,siwatl,siwatl,siwatl,cihuatl,noun,spoken_safe / neutral,EHN / MSN,woman,mujer,—,"Kaikki NHE / Nāhuatlahtolli / FCN Phase 8",high,accepted_for_public_use,curated,"Core noun. Spoken-safe. Plural: siwāmeh.","Classical form cihuatl citation-only. EHN and MSN forms identical.","see tlācatl; see cihuatl (classical, FCN-DICT-0046); see mācēhualli"
```

---

### 7B. Web Display Card (Markdown)

```markdown
## siwatl
**woman** | *mujer*

| | |
|---|---|
| Spoken EHN | siwatl |
| Written standard (MSN) | siwatl |
| Classical citation | cihuatl |
| Part of speech | noun |
| Plural | siwāmeh |
| Register | spoken-safe |

> Core spoken form. Primer-safe. No register caution.

**See also:** tlācatl (man/person) · mācēhualli (community member)
```

---

### 7C. Compact App Lookup

```
siwatl
woman · mujer
noun · EHN spoken-safe
Plural: siwāmeh  |  Classical: cihuatl
→ tlācatl  ·  mācēhualli
```

---

### 7D. Print Dictionary Entry

**siwatl** *n.* woman; *mujer*. EHN spoken form. MSN headword: siwatl. Classical citation: cihuatl. Plural: siwāmeh. Source: Kaikki NHE; FCN Phase 8 corpus. Status: accepted for public use. *See also:* tlācatl, mācēhualli.

---

## 8. Coverage and Expansion Roadmap

### Current seed set (version 0.2)

| Domain | Entry count |
|--------|------------|
| Core spoken EHN vocabulary | 20 |
| Grammar / function words | 8 |
| Interaction phrases and verbs | 4 |
| Poetic high-register (Phase 9) | 6 |
| Classical-note items | 2 |
| **Subtotal** | **40** |
| Model entries (4 already counted above) | — |
| Fully-fielded model entries | 4 (overlap with above) |

Total: 46 distinct entries.

### Gaps in current seed set

- Body parts vocabulary (needs EHN attestation from Kaikki NHE or new curation)
- Extended family terms (beyond Unit 9 possession series)
- Household items and interior vocabulary (Unit 23 content not yet sourced)
- Weather, environment, and plant vocabulary
- Color terms (Unit 4: xoxoctic, tzictic, cōztic, chīchīltic, xoxoctīc, āchīlcōz)
- Verb paradigm tables as standalone entries
- Numbers cē–chiucnahui (1–9) as individual entries

### Phase B expansion (requires SQLite query of Phase 8 corpus)

Target: 200–350 entries from the full 23-unit primer vocabulary.
Method: query `fcn_master_lexicon_phase8_6_primer.sqlite`, filter by `avg_confidence ≥ 0.7` and `gloss_en IS NOT NULL`. Apply Phase 11 QA protocol (D12) to validate register and status before inclusion.

### Phase C expansion (requires new curation work)

- Systematic Siméon 1885 sampling: 50–100 high-value classical-note items
- Kaikki NHE cross-check: verify all `accepted_for_internal_use` entries against 657 NHE rows
- Community speaker validation: elevate `editorially_accepted` items to `accepted_for_public_use`

---

## 9. Deliverable Completion Statement

This document completes the structural and initial content requirements for:

**Deliverable 18: Flor y Canto Nahuatl Dictionary**

Completed in version 0.2:
- 18-field entry template — Section 2
- Entry directions — Section 3
- Cross-reference type taxonomy — Section 4
- 46 populated seed entries across 5 register domains — Section 5
- 3 worked cross-reference chains — Section 6
- siwatl rendered in all 4 publication formats — Section 7
- Coverage roadmap for Phase B and C expansion — Section 8

**Status:** Working seed dictionary. Not a public release dictionary. Entries marked `accepted_for_internal_use` require Phase B source verification before public release. Entries marked `editorially_accepted` require Phase B community/source validation. Entries marked `accepted_for_public_use` are cleared pending final editorial review.
