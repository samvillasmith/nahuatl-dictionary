# **Flor y Canto Nahuatl Source Hierarchy Document**

**Version:** 0.1 draft  
**Project:** Flor y Canto Nahuatl  
**Subtitle:** Eastern Huasteca Nahuatl for Speech, Modern Standard Nahuatl for Writing

## **1\. Purpose**

This document governs how Flor y Canto Nahuatl evaluates, prioritizes, and reconciles its sources. Its purpose is to ensure that every lexical item, grammatical claim, literary form, and published text is traceable to explicit evidence, editorial status, and register assignment, in line with the project’s checklist and locked premises .

This document does four things:

1. Defines the active source inventory.  
2. Assigns authority by function rather than treating all sources as equal.  
3. Establishes conflict-resolution rules.  
4. Establishes an unresolved-case policy.

## **2\. Governing principles**

FCN operates with a three-layer framework already fixed in the project: EHN as spoken base, MSN/MSN neutral as written norm, and MSN-P as elevated literary register . Source governance must therefore follow these rules:

* No source is globally supreme across all functions.  
* Spoken EHN evidence is not replaced by Classical Nahuatl evidence.  
* Classical material may support citation, literary elevation, and root-family analysis, but it does not silently overwrite spoken EHN forms.  
* Every published form must remain traceable either to source evidence or to explicit editorial proposal status .  
* Every lexical item and text must carry a register label .

## **3\. Source inventory**

### **3.1 Active project sources**

| Source file / output | Provenance | License | Main limitations | Intended project role | Canonical status |
| ----- | ----- | ----- | ----- | ----- | ----- |
| `nahuatl_kaikki_unified.json` | Kaikki / English Wiktionary extraction | CC BY-SA 3.0 / GFDL | Lexicographic, mixed varieties, uneven depth, not a final spoken grammar | Primary lexical intake layer across varieties; EHN extraction base; comparative lexicon | Canonical intake source |
| `out_kaikki/fcn_lexical_rows.*` | Derived from `nahuatl_kaikki_unified.json` by FCN parser | Inherits upstream licensing plus FCN provenance | Parser-dependent normalization; must remain traceable to source rows | Working lexical table for import into FCN schema | Canonical derived working layer |
| `simeon_parsed.json` | Parsed from Siméon 1885 dictionary | Public domain source; parsed derivative requires provenance retention | Definitions in French; OCR/parsing imperfections remain; classical, not modern spoken EHN | Primary classical citation layer; root-family support; literary-historical support | Canonical reference source |
| `simeon_1885_ocr_raw.txt` | OCR from Siméon 1885 | Public domain | Raw OCR noise, structural corruption, orthographic ambiguity | Archival evidence; fallback verification; example harvesting support | Non-canonical raw archival layer |
| `out_classical/*` | FCN-derived from Siméon OCR \+ parsed data | Derived from public-domain source; FCN provenance required | Extraction quality varies by parser confidence | Classical example bank; literary evidence layer; headword candidate support | Canonical derived working layer |
| `out_ud/*` | UD treebank-derived evidence tables when present | Per-treebank license; must be tracked in provenance | Corpus scope limited; annotated corpus is not a full norm | Grammar evidence, morphology patterns, dependency evidence | Canonical supporting evidence layer |
| `data/ledger/provenance.csv` | FCN legal ingest ledger | FCN internal documentation of upstream licenses | Not a language source; administrative rather than linguistic | Provenance, audit trail, reproducibility, publication compliance | Canonical audit source |
| `README_SOURCES.txt` | Project source memo | Project memo referencing upstream licenses | Descriptive, not itself lexical authority | Legal/source memo; handling instructions; risk warnings | Canonical policy memo |

This inventory reflects the exact Phase 3 requirement to record each file, provenance, license, limitations, and intended role , and it uses the harvested sources explicitly named in the handoff as the immediate basis for this document .

## **4\. Source classes**

To prevent category errors, FCN divides sources into six classes.

### **Class A — Spoken lexical evidence**

Primary purpose: identify attested modern forms, senses, POS, and variety labels relevant to EHN.

**Included sources**

* `nahuatl_kaikki_unified.json`  
* `out_kaikki/*`

**Use cases**

* EHN form extraction  
* sense preservation  
* variant retention  
* part-of-speech assignment  
* comparative cross-check against other Nahuatl varieties

**Not sufficient for**

* final spoken standard approval without speaker validation  
* final prescriptive EHN grammar

### **Class B — Classical citation and literary evidence**

Primary purpose: establish classical citation forms, literary resonance, and historically attested lexical/morphological material.

**Included sources**

* `simeon_parsed.json`  
* `simeon_1885_ocr_raw.txt`  
* `out_classical/*`

**Use cases**

* Classical citation forms  
* MSN-P literary enrichment  
* historical examples  
* root-family support  
* rhetorical and poetic expansion

**Not sufficient for**

* direct import into beginner EHN materials  
* silent normalization into spoken EHN

### **Class C — Grammar evidence**

Primary purpose: provide structured morphological and syntactic evidence from annotated corpora.

**Included sources**

* `out_ud/*`  
* underlying local `.conllu` files when present

**Use cases**

* morphology counts  
* feature distributions  
* dependency patterns  
* example sentence structures  
* grammar blueprint evidence tables

**Not sufficient for**

* full spoken EHN norm by itself  
* automatic style or register decisions

### **Class D — Provenance and legal audit**

Primary purpose: prove where data came from, under what license, and with what retrieval history.

**Included sources**

* `data/ledger/provenance.csv`  
* `README_SOURCES.txt`

**Use cases**

* release compliance  
* source traceability  
* auditability  
* publication review

**Not sufficient for**

* linguistic decision-making by itself

### **Class E — Raw archival material**

Primary purpose: preserve source-state evidence that may be cleaned or reinterpreted later.

**Included sources**

* raw OCR files  
* raw dumps not yet normalized

**Use cases**

* re-parsing  
* manual correction  
* error tracing  
* source dispute review

**Not sufficient for**

* canonical surface-form publication without editorial review

### **Class F — FCN editorial layer**

Primary purpose: encode project decisions not directly identical to any one source.

**Included outputs**

* approved MSN headwords  
* approved register assignments  
* approved normalization decisions  
* validated speaker-backed EHN forms  
* proposed entries awaiting review

**Use cases**

* publication  
* pedagogy  
* dictionary construction  
* style enforcement

**Constraint**  
Every editorial decision must cite its source basis or be tagged as proposal status, per the project premises .

## **5\. Source authority by function**

This is the core of the hierarchy.

### **5.1 Spoken EHN evidence**

**Primary authority:** EHN-labeled rows from `nahuatl_kaikki_unified.json` / `out_kaikki`  
**Secondary authority:** additional modern Huasteca evidence when later added  
**Editorial rule:** no form becomes FCN spoken-standard output merely because it exists in a comparative or classical source. It must either be directly attested as EHN or explicitly adopted as an editorial proposal pending validation.

### **5.2 Classical citation evidence**

**Primary authority:** `simeon_parsed.json`  
**Secondary authority:** `simeon_1885_ocr_raw.txt` and `out_classical` examples  
**Editorial rule:** if a classical citation form is needed, the parsed Siméon layer outranks raw OCR. Raw OCR is used only to confirm, recover, or challenge parse output.

### **5.3 Root-family evidence**

**Primary authority:** `simeon_parsed.json`  
**Secondary authority:** Kaikki etymology and cross-variety lexical correspondences  
**Editorial rule:** root-family claims are historical-analytical, not automatic prescriptions for surface forms.

### **5.4 Comparative evidence**

**Primary authority:** non-EHN Nahuatl rows in `nahuatl_kaikki_unified.json` / `out_kaikki`  
**Secondary authority:** UD-derived material where applicable  
**Editorial rule:** comparative evidence may justify notes, hypotheses, and proposed normalization pathways, but not silent replacement of EHN evidence.

### **5.5 Poetic expansion**

**Primary authority:** `simeon_parsed.json` plus curated `out_classical` examples  
**Secondary authority:** comparative lexical material and later literary corpus additions  
**Editorial rule:** material used for MSN-P must be explicitly tagged as literary, poetic, classical, ceremonial, or proposed literary-modern as appropriate. It does not enter neutral prose or beginner pedagogy unmarked.

### **5.6 Normalization support**

**Primary authority:** FCN editorial layer using structured Kaikki \+ structured Siméon \+ provenance tracking  
**Secondary authority:** raw OCR only where needed for dispute resolution  
**Editorial rule:** normalization decisions require a recorded rationale, not just a cleaned spelling.

## **6\. Authority ranking rules**

FCN does not use one universal source ranking. It uses function-specific ranking. When a direct ranking is needed, use this order:

### **For spoken EHN forms**

1. Speaker-validated EHN evidence  
2. EHN-labeled lexical evidence from Kaikki / out\_kaikki  
3. FCN editorial proposal based on comparative support  
4. Classical evidence  
5. Raw OCR evidence

### **For MSN neutral written forms**

1. FCN approved editorial form based on EHN \+ cross-variety normalization logic  
2. EHN lexical evidence  
3. Comparative lexical evidence  
4. Classical support where relevant  
5. Raw OCR evidence

### **For MSN-P / poetic forms**

1. FCN approved literary form with explicit register tag  
2. Classical citation evidence from parsed Siméon  
3. Curated classical examples from out\_classical  
4. Comparative elevated diction  
5. Raw OCR evidence

### **For grammar claims**

1. Structured corpus evidence (`out_ud`)  
2. Repeated lexical/morphological evidence across structured sources  
3. Classical grammatical patterns from Siméon  
4. Editorial generalization marked as provisional

## **7\. Conflict-resolution rules**

When sources disagree, apply the following rules in order.

### **Rule 1 — Function first**

Ask what decision is being made: spoken form, neutral written form, poetic form, classical citation, grammar statement, or root-family claim. Do not resolve all conflicts with one hierarchy.

### **Rule 2 — Structured beats raw**

If `simeon_parsed.json` and raw OCR disagree, prefer the parsed source unless manual inspection shows the parse is clearly wrong.

### **Rule 3 — Direct attestation beats inference**

An explicitly EHN-labeled form outranks a form inferred from comparative or classical material.

### **Rule 4 — Register separation is mandatory**

A classical or poetic form may coexist with an EHN or MSN-neutral form. Coexistence is preferred over forced merger.

### **Rule 5 — Keep competing forms visible when needed**

If two forms have credible support and serve different domains, keep both and distinguish them by register, variety, source, and editorial note.

### **Rule 6 — Provenance is part of authority**

An attractive form with weak traceability loses to a less elegant form with clear provenance.

### **Rule 7 — Editorial regularization must be declared**

Any normalized or harmonized form created by FCN must be marked as editorial, with source basis documented.

### **Rule 8 — Beginner safety rule**

No poetic/classical item enters beginner EHN materials without explicit marking, consistent with the checklist premises .

## **8\. Unresolved-case policy**

When evidence is insufficient, FCN does not guess silently. It assigns a status.

### **Required unresolved statuses**

* `Needs_review` — evidence exists but is conflicting or incomplete  
* `Proposed` — editorial form proposed but not yet approved  
* `Comparative_only` — supported outside EHN but not yet approved for FCN core use  
* `Classical_citation` — valid as historical/classical reference only  
* `Deprecated` — retained for traceability but not for active publication

These statuses are already aligned with the locked register/status system in Phase 2 and the required tagging discipline in the checklist .

### **Required unresolved workflow**

1. Preserve all competing forms.  
2. Preserve exact source references.  
3. Record why the case is unresolved.  
4. Record what evidence would resolve it.  
5. Prevent automatic promotion into public-facing materials until resolved.

## **9\. Minimum source record format**

Every source in FCN should have a record containing at least:

* `source_id`  
* `source_file`  
* `source_type`  
* `upstream_title`  
* `provenance_note`  
* `license`  
* `retrieval_or_creation_date`  
* `project_role`  
* `authority_domain`  
* `limitations`  
* `canonical_status`  
* `notes`

This should map directly into the Phase 4 supporting `sources` table.

## **10\. Publication policy**

A form is publishable in FCN only if all of the following are true:

* it has a register label  
* it has a source trail or explicit proposal status  
* it has a clear function in the framework  
* it is not being silently imported across registers  
* it is not being presented as spoken EHN merely because it is classical or comparative

## **11\. Immediate implementation consequence for Phase 4**

This hierarchy implies that the Master Lexicon Schema must support:

* more than one form per lexical concept  
* register-tagged forms  
* source-level provenance  
* validation status  
* editorial status  
* parallel classical and spoken layers without collapse

That requirement is already anticipated in the checklist’s required fields and supporting tables for sources, variants, roots/families, examples, validation, and literary notes .

## **12\. Decision summary**

For FCN v0.1 source governance:

* `out_kaikki` is the primary lexical intake layer.  
* `simeon_parsed.json` is the primary classical citation and root-family reference layer.  
* `simeon_1885_ocr_raw.txt` remains archival and non-canonical unless explicitly reviewed.  
* `out_classical` is a working literary/classical evidence layer, not a spoken-standard source.  
* `out_ud` is grammar evidence, not a standalone norm.  
* `provenance.csv` and `README_SOURCES.txt` govern traceability and legal posture, not lexical authority.  
* unresolved cases remain visible and tagged; they are not silently flattened.

This is the correct Phase 3 posture given your checklist and current project state .

The next clean step is Deliverable 4: the Master Lexicon Schema, built to enforce this hierarchy rather than bypass it.