#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import sqlite3
from typing import Dict, Iterable, List

import pandas as pd
import numpy as np

MONTH_TERMS = [
    'january','february','march','april','may','june','july','august',
    'september','october','november','december'
]

FUNCTION_POS = {'pron','det','conj','prep','particle','adv','num'}


def clean(value):
    if value is None:
        return ''
    text = str(value).strip().strip('"').strip("'").strip()
    text = re.sub(r'\s+', ' ', text)
    return text.rstrip('.')


def classify_domain(gloss: str, pos: str) -> str:
    g = gloss.lower()
    if any(k in g for k in [
        'hello','good morning','good afternoon','good night',
        'how are you','how\'s it going','thanks','you\'re welcome',
        'negative response','positive response'
    ]):
        return 'social_interaction'
    if pos in FUNCTION_POS:
        return 'function_word'
    if any(k in g for k in [
        'friend','companion','child','son','daughter','man','woman',
        'young man','young woman','father','mother','grandmother',
        'grandfather','people','person','speaker'
    ]):
        return 'people_family'
    if any(k in g for k in [
        'house','home','town','city','table','blanket','paper','book',
        'letter','map','clothing','shirt','bed','door','chair'
    ]):
        return 'home_objects'
    if any(k in g for k in [
        'water','drink','eat','tamale','tortilla','chocolate','bean',
        'milpa','chili','shrimp','avocado','orange','hungry','tasty',
        'bread','food','coffee','mandarin'
    ]):
        return 'food_water'
    if any(k in g for k in ['now','tomorrow','yesterday','before','early','night','morning','afternoon','month','spring'] + MONTH_TERMS):
        return 'time_calendar'
    if any(k in g for k in [
        'walk','go','arrive','enter','speak','talk','sleep','know','have',
        ' be','be ','write','teach','sing','fall','die','dig','send',
        'swim','cure','sign','ride','flee','grind','make tortillas',
        'be sick'
    ]):
        return 'verb_action'
    if any(k in g for k in [
        'good','bad','big','small','tiny','strong','red','blue','white',
        'orange','old','long','fast','dry','hot','angry','alone','deep',
        'tall','thin'
    ]):
        return 'quality_color'
    if any(k in g for k in ['river','wind','forest','snow','mountain','tree','flower','sun','moon','star']):
        return 'nature'
    if any(k in g for k in ['dog','bird','heron','dragonfly','raccoon','alligator','shrimp']):
        return 'animals'
    return 'general'


def beginner_rationale(gloss: str, pos: str, domain: str) -> str:
    g = gloss.lower()
    if 'obsolete spelling' in g or 'alternative spelling' in g:
        return 'unsafe: alternate_or_obsolete_spelling'
    if 'third-person singular possessed form' in g:
        return 'unsafe: inflected_reference_form'
    if pos == 'suffix':
        return 'unsafe: bound_morpheme_not_beginner_entry'
    if any(k in g for k in ['kingdom','province','country','republic']):
        return 'unsafe: advanced_civic_or_geographic_term'
    if any(k in g for k in ['priest','poison','bloody','infect','urinate','wooden spear','deadman']):
        return 'unsafe: low_priority_or_sensitive_for_beginner_set'
    if domain in {'function_word','social_interaction','verb_action','food_water','people_family','home_objects','time_calendar','quality_color'}:
        return 'safe: core_everyday_domain'
    return 'safe: general_everyday_candidate'


def pedagogical_score(row: pd.Series) -> int:
    score = 0
    pos = row['part_of_speech']
    g = row['gloss_en'].lower()
    rat = row['beginner_rationale']
    if rat.startswith('safe'):
        score += 40
    elif 'alternate_or_obsolete' in rat:
        score -= 50
    else:
        score -= 25
    score += {
        'pron': 35, 'det': 35, 'particle': 35, 'intj': 35,
        'conj': 32, 'prep': 30, 'adv': 28, 'num': 27,
        'verb': 30, 'noun': 20, 'adj': 18, 'name': 5, 'suffix': -30,
    }.get(pos, 0)
    score += {
        'social_interaction': 40,
        'function_word': 35,
        'verb_action': 25,
        'food_water': 22,
        'time_calendar': 20,
        'people_family': 20,
        'home_objects': 18,
        'quality_color': 16,
        'nature': 8,
        'animals': 6,
        'general': 4,
    }.get(row['semantic_domain'], 0)
    if len(row['display_form']) <= 8:
        score += 3
    if any(k in g for k in [
        'hello','thanks','good morning','good night','yes','no','where',
        'what','who','why','how','here','there','tomorrow','now','good',
        'bad','big','small','water','house','friend','man','woman',
        'child','book','paper','eat','drink','go','arrive','sleep','know',
        'speak','write','teach','have','be'
    ]):
        score += 10
    if row['variety'] == 'Central Huasteca Nahuatl':
        score += 8
    if row['register'] == 'EHN_colloquial':
        score += 25
    if row['gloss_en'].lower() in MONTH_TERMS or row['gloss_en'].lower() in {m.capitalize() for m in MONTH_TERMS}:
        score -= 20
    return int(score)


def add_common_annotations(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out['gloss_en'] = out['gloss_en'].fillna('').map(clean)
    out['gloss_es'] = out['gloss_es'].fillna('').map(clean)
    out['ehn_spoken_form'] = out['ehn_spoken_form'].fillna('').map(clean)
    out['msn_headword'] = out['msn_headword'].fillna('').map(clean)
    out['current_msn_headword'] = out['current_msn_headword'].fillna('').map(clean)
    out['part_of_speech'] = out['part_of_speech'].fillna('').map(clean)
    out['register'] = out['register'].fillna('').map(clean)
    out['variety'] = out['variety'].fillna('').map(clean)
    out['source_file'] = out['source_file'].fillna('').map(clean)
    out['source_reference'] = out['source_reference'].fillna('').map(clean)
    out['rule_trace'] = out['rule_trace'].fillna('').map(clean)
    out['display_form'] = np.where(out['ehn_spoken_form'].ne(''), out['ehn_spoken_form'], out['msn_headword'])
    out['semantic_domain'] = out.apply(lambda r: classify_domain(r['gloss_en'], r['part_of_speech']), axis=1)
    out['beginner_rationale'] = out.apply(lambda r: beginner_rationale(r['gloss_en'], r['part_of_speech'], r['semantic_domain']), axis=1)
    out['beginner_flag'] = np.where(out['beginner_rationale'].str.startswith('safe'), 'safe', 'unsafe')
    out['pedagogical_score'] = out.apply(pedagogical_score, axis=1)
    out['key'] = (
        out['msn_headword'].str.lower() + '||' + out['gloss_en'].str.lower() + '||' + out['part_of_speech'].str.lower()
    )
    out['is_month'] = out['gloss_en'].str.lower().isin(MONTH_TERMS)
    return out


def pick_quota(df: pd.DataFrame, quota: int, picked: set) -> List[int]:
    selected = []
    for idx, _ in df.iterrows():
        if idx in picked:
            continue
        selected.append(idx)
        picked.add(idx)
        if len(selected) >= quota:
            break
    return selected


def select_core_250(ehn_safe: pd.DataFrame) -> pd.DataFrame:
    social = ehn_safe[((ehn_safe['semantic_domain'] == 'social_interaction') | (ehn_safe['part_of_speech'].isin(['intj','particle']))) & (~ehn_safe['is_month'])].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True])
    function = ehn_safe[(ehn_safe['part_of_speech'].isin(['pron','det','conj','prep','adv','num'])) & (~ehn_safe['is_month'])].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True])
    verbs = ehn_safe[(ehn_safe['part_of_speech'] == 'verb') & (~ehn_safe['is_month'])].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True])
    nouns = ehn_safe[(ehn_safe['part_of_speech'] == 'noun') & (~ehn_safe['is_month'])].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True])
    adjs = ehn_safe[(ehn_safe['part_of_speech'] == 'adj') & (~ehn_safe['is_month'])].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True])

    picked = set()
    selected: List[int] = []
    for frame, quota in [(social, 20), (function, 55), (verbs, 40), (nouns, 110), (adjs, 25)]:
        selected.extend(pick_quota(frame, quota, picked))

    filler = ehn_safe[~ehn_safe['is_month']].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True])
    for idx, _ in filler.iterrows():
        if len(selected) >= 250:
            break
        if idx in picked:
            continue
        selected.append(idx)
        picked.add(idx)

    out = ehn_safe.loc[selected].copy().sort_values(['pedagogical_score','msn_headword'], ascending=[False, True]).reset_index(drop=True)
    out['rank'] = range(1, len(out) + 1)
    out['list_name'] = 'core_ehn_250'
    out['attestation_status'] = 'EHN_attested'
    out['phase7_status'] = 'approved_core_candidate'
    return out


def select_core_500(ehn: pd.DataFrame) -> pd.DataFrame:
    out = ehn.sort_values(['beginner_flag','pedagogical_score','msn_headword'], ascending=[True, False, True]).head(500).copy().reset_index(drop=True)
    out['rank'] = range(1, len(out) + 1)
    out['list_name'] = 'core_ehn_500'
    out['attestation_status'] = 'EHN_attested'
    out['phase7_status'] = np.where(out['beginner_flag'].eq('safe'), 'approved_core_candidate', 'review_before_beginner_use')
    return out


def select_core_1000(ehn: pd.DataFrame, comp: pd.DataFrame) -> pd.DataFrame:
    ehn_sorted = ehn.sort_values(['beginner_flag','pedagogical_score','msn_headword'], ascending=[True, False, True]).copy().reset_index(drop=True)
    ehn_sorted['rank'] = range(1, len(ehn_sorted) + 1)
    ehn_sorted['list_name'] = 'core_ehn_1000'
    ehn_sorted['attestation_status'] = 'EHN_attested'
    ehn_sorted['phase7_status'] = np.where(ehn_sorted['beginner_flag'].eq('safe'), 'attested_core_row', 'attested_review_row')

    ehn_keys = set(ehn['key'])
    comp2 = comp[~comp['key'].isin(ehn_keys)].copy()
    comp2['variety_priority'] = comp2['variety'].map({'Central Huasteca Nahuatl': 0, 'Central Nahuatl': 1}).fillna(9)
    comp2 = comp2.sort_values(['beginner_flag','variety_priority','pedagogical_score','msn_headword'], ascending=[True, True, False, True])
    comp2 = comp2.head(max(0, 1000 - len(ehn_sorted))).copy().reset_index(drop=True)
    comp2['rank'] = range(len(ehn_sorted) + 1, len(ehn_sorted) + len(comp2) + 1)
    comp2['list_name'] = 'core_ehn_1000'
    comp2['attestation_status'] = 'Comparative_gap_fill'
    comp2['phase7_status'] = np.where(
        comp2['beginner_flag'].eq('safe'),
        'proposed_gap_fill_from_comparative',
        'review_gap_fill_from_comparative'
    )

    out = pd.concat([ehn_sorted, comp2], ignore_index=True)
    return out


def select_verbs_100(ehn: pd.DataFrame, comp: pd.DataFrame) -> pd.DataFrame:
    ehn_verbs = ehn[ehn['part_of_speech'] == 'verb'].sort_values(['beginner_flag','pedagogical_score','msn_headword'], ascending=[True, False, True]).copy().reset_index(drop=True)
    ehn_keys = set(ehn_verbs['key'])
    comp_verbs = comp[(comp['part_of_speech'] == 'verb') & (~comp['key'].isin(ehn_keys))].copy()
    comp_verbs['variety_priority'] = comp_verbs['variety'].map({'Central Huasteca Nahuatl': 0, 'Central Nahuatl': 1}).fillna(9)
    comp_verbs = comp_verbs.sort_values(['beginner_flag','variety_priority','pedagogical_score','msn_headword'], ascending=[True, True, False, True])
    comp_verbs = comp_verbs.head(max(0, 100 - len(ehn_verbs))).copy().reset_index(drop=True)

    ehn_verbs['rank'] = range(1, len(ehn_verbs) + 1)
    ehn_verbs['list_name'] = 'core_verbs_100'
    ehn_verbs['attestation_status'] = 'EHN_attested'
    ehn_verbs['phase7_status'] = np.where(ehn_verbs['beginner_flag'].eq('safe'), 'attested_core_row', 'attested_review_row')

    comp_verbs['rank'] = range(len(ehn_verbs) + 1, len(ehn_verbs) + len(comp_verbs) + 1)
    comp_verbs['list_name'] = 'core_verbs_100'
    comp_verbs['attestation_status'] = 'Comparative_gap_fill'
    comp_verbs['phase7_status'] = np.where(comp_verbs['beginner_flag'].eq('safe'), 'proposed_gap_fill_from_comparative', 'review_gap_fill_from_comparative')

    return pd.concat([ehn_verbs, comp_verbs], ignore_index=True)


def select_function_words(ehn: pd.DataFrame) -> pd.DataFrame:
    out = ehn[ehn['part_of_speech'].isin(sorted(FUNCTION_POS))].copy()
    out = out.sort_values(['beginner_flag','part_of_speech','pedagogical_score','msn_headword'], ascending=[True, True, False, True]).reset_index(drop=True)
    out['rank'] = range(1, len(out) + 1)
    out['list_name'] = 'function_words'
    out['subgroup'] = out['part_of_speech']
    return out


def social_hit(gloss: str, pos: str) -> bool:
    g = gloss.lower()
    if pos in {'intj','particle','pron'}:
        return True
    patterns = [
        r'\bhello\b', r'\bgood morning\b', r'\bgood afternoon\b', r'\bgood night\b',
        r'\bhow are you\b', r"\bhow's it going\b", r'\bthanks\b', r"\byou're welcome\b",
        r'\byes\b', r'\bfriend\b', r'\bcompanion\b', r'\bchild\b', r'\bson\b',
        r'\bdaughter\b', r'\bman\b', r'\bwoman\b', r'\bfather\b', r'\bmother\b',
        r'\bgrandmother\b', r'\bgrandfather\b', r'\bpeople\b', r'\bspeak\b',
        r'\btalk\b', r'\bspeaker\b'
    ]
    return any(re.search(p, g) for p in patterns)


def select_social_interaction(ehn: pd.DataFrame) -> pd.DataFrame:
    out = ehn[ehn.apply(lambda r: social_hit(r['gloss_en'], r['part_of_speech']), axis=1)].copy()
    out = out[out['beginner_flag'] == 'safe'].copy()
    out = out.sort_values(['pedagogical_score','msn_headword'], ascending=[False, True]).reset_index(drop=True)
    out['rank'] = range(1, len(out) + 1)
    out['list_name'] = 'social_interaction'
    return out


def lookup(entries: pd.DataFrame, **kwargs) -> Dict[str, str]:
    mask = pd.Series([True] * len(entries), index=entries.index)
    for k, v in kwargs.items():
        mask &= entries[k].eq(v)
    if mask.any():
        row = entries[mask].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True]).iloc[0]
        return row.to_dict()

    # fallback for gloss formatting mismatches
    narrowed = entries.copy()
    if 'display_form' in kwargs:
        narrowed = narrowed[narrowed['display_form'].eq(kwargs['display_form'])]
    if 'msn_headword' in kwargs and not narrowed.empty:
        narrowed = narrowed[narrowed['msn_headword'].eq(kwargs['msn_headword'])]
    if 'gloss_en' in kwargs and not narrowed.empty:
        gloss_target = kwargs['gloss_en'].lower()
        gloss_mask = narrowed['gloss_en'].str.lower().str.contains(re.escape(gloss_target), regex=True)
        if gloss_mask.any():
            narrowed = narrowed[gloss_mask]
    if narrowed.empty:
        raise KeyError(f'No row found for {kwargs}')
    row = narrowed.sort_values(['pedagogical_score','msn_headword'], ascending=[False, True]).iloc[0]
    return row.to_dict()


def build_example_bank(ehn: pd.DataFrame) -> pd.DataFrame:
    safe = ehn[ehn['beginner_flag'] == 'safe'].copy()
    rows: List[Dict[str, str]] = []
    n = 1

    def add_row(example_ehn: str, example_msn: str, en: str, example_type: str, evidence_status: str, source_ids: List[str], notes: str = ''):
        nonlocal n
        rows.append({
            'example_id': f'FCN-EX-P7-{n:04d}',
            'example_ehn': example_ehn,
            'example_msn': example_msn,
            'translation_en': en,
            'example_type': example_type,
            'evidence_status': evidence_status,
            'beginner_flag': 'safe',
            'source_entry_ids_json': json.dumps(source_ids, ensure_ascii=False),
            'notes': notes,
        })
        n += 1

    # attested social phrases and response tokens
    attested = safe[safe['part_of_speech'].isin(['intj','particle'])].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True])
    for _, row in attested.iterrows():
        add_row(row['display_form'], row['msn_headword'], row['gloss_en'], 'attested_phrase', 'attested_lexical_item', [row['entry_id']])

    # question / time / place tokens
    token_glosses = [
        'who?', 'what', 'where', 'how', 'how much?', 'now', 'right now',
        'tomorrow', 'yesterday', 'here', 'there', 'not', 'not yet',
        'before', 'because'
    ]
    token_rows = safe[safe['gloss_en'].str.lower().isin(token_glosses)].sort_values(['pedagogical_score','msn_headword'], ascending=[False, True])
    seen = set()
    for _, row in token_rows.iterrows():
        key = (row['display_form'], row['gloss_en'])
        if key in seen:
            continue
        seen.add(key)
        add_row(row['display_form'], row['msn_headword'], row['gloss_en'], 'attested_token', 'attested_lexical_item', [row['entry_id']])

    # editorial demonstrative phrases
    ni = lookup(safe, display_form='ni', gloss_en='this')
    ne = lookup(safe, display_form='ne', gloss_en='that')
    noun_targets = [
        ('calli', 'house'), ('amatl', 'paper'), ('tamalli', 'tamale'), ('tlaxcalli', 'tortilla'),
        ('amigo', 'friend'), ('libro', 'book'), ('amacamanalli', 'map'), ('amatlahcuilolli', 'A letter'),
        ('altepetl', 'altepetl, city, town'), ('huicatl', 'song'), ('siwatl', 'woman'),
        ('tlacatl', 'man'), ('pilconetzi', 'child'), ('komalli', 'a pan used to grill tortillas'),
        ('atemitl', 'river')
    ]
    nouns = []
    for form, gloss in noun_targets:
        matches = safe[(safe['display_form'] == form) | (safe['msn_headword'] == form)]
        if gloss:
            matches = matches[matches['gloss_en'].eq(gloss)] if matches['gloss_en'].eq(gloss).any() else matches
        if not matches.empty:
            nouns.append(matches.sort_values(['pedagogical_score','msn_headword'], ascending=[False, True]).iloc[0].to_dict())
    for det in [ni, ne]:
        det_en = clean(det['gloss_en'])
        for noun in nouns:
            ehn_phrase = f"{det['display_form']} {noun['display_form']}"
            msn_phrase = f"{det['msn_headword']} {noun['msn_headword']}"
            en = f"{det_en} {noun['gloss_en'].lower()}"
            add_row(ehn_phrase, msn_phrase, en, 'editorial_demonstrative_phrase', 'editorial_generated_phrase', [det['entry_id'], noun['entry_id']], 'Conservative nominal phrase built from attested EHN determiner + noun.')

    # editorial number phrases
    num_targets = [('ce', 'one'), ('ome', 'two'), ('eyi', 'three'), ('nahui', 'four'), ('macuilli', 'five')]
    num_rows = []
    for form, gloss in num_targets:
        match = safe[(safe['display_form'] == form) | (safe['msn_headword'] == form)]
        match = match[match['gloss_en'].str.lower().str.startswith(gloss)] if match['gloss_en'].str.lower().str.startswith(gloss).any() else match
        if not match.empty:
            num_rows.append(match.sort_values(['pedagogical_score','msn_headword'], ascending=[False, True]).iloc[0].to_dict())
    noun_targets_small = [
        ('tamalli', 'tamale'), ('tlaxcalli', 'tortilla'), ('amigo', 'friend'),
        ('calli', 'house'), ('amatl', 'paper'), ('chilli', 'chili pepper')
    ]
    count_nouns = []
    for form, gloss in noun_targets_small:
        match = safe[(safe['display_form'] == form) | (safe['msn_headword'] == form)]
        match = match[match['gloss_en'].eq(gloss)] if match['gloss_en'].eq(gloss).any() else match
        if not match.empty:
            count_nouns.append(match.sort_values(['pedagogical_score','msn_headword'], ascending=[False, True]).iloc[0].to_dict())
    for num in num_rows:
        gloss_num = clean(num['gloss_en']).split(';')[0].split()[0]
        for noun in count_nouns:
            ehn_phrase = f"{num['display_form']} {noun['display_form']}"
            msn_phrase = f"{num['msn_headword']} {noun['msn_headword']}"
            en = f"{gloss_num} {noun['gloss_en'].lower()}"
            add_row(ehn_phrase, msn_phrase, en, 'editorial_number_phrase', 'editorial_generated_phrase', [num['entry_id'], noun['entry_id']], 'Conservative numeral + noun phrase for beginner practice.')

    return pd.DataFrame(rows)


def finalize_export(df: pd.DataFrame, extra_cols: Iterable[str] = ()) -> pd.DataFrame:
    cols = [
        'rank','list_name','entry_id','attestation_status','phase7_status','beginner_flag','beginner_rationale',
        'display_form','ehn_spoken_form','msn_headword','current_msn_headword','gloss_en','gloss_es',
        'part_of_speech','semantic_domain','register','variety','pedagogical_score','source_file',
        'source_reference','source_confidence','rule_trace'
    ] + list(extra_cols)
    keep = [c for c in cols if c in df.columns]
    return df[keep].copy()


def write_markdown(path: str, summary: Dict[str, int]):
    content = f"""# Flor y Canto Nahuatl Phase 7 — Core Lexicon Deliverable\n\n## Deliverable 8\n**Flor y Canto Nahuatl Core EHN Lexicon**\n\nThis phase operationalizes the imported lexical base into pedagogical core lists. It is grounded in the Phase 5 lexical database and the Phase 6 orthography layer.\n\n## What was built\n\n- 250-word core EHN list\n- 500-word expanded EHN list\n- 1,000-item core lexicon package\n- 100-verb list\n- function-word list\n- social-interaction list\n- everyday example bank\n\n## Current source-boundary reality\n\nThe current imported database contains **{summary['ehn_total']} attested EHN rows** and **{summary['ehn_verbs']} attested EHN verbs**. That means the 1,000-item and 100-verb targets cannot be satisfied from attested EHN alone without pretending the evidence base is larger than it is.\n\nFCN therefore keeps the boundary explicit:\n\n- `EHN_attested` rows come directly from the imported EHN lexical layer.\n- `Comparative_gap_fill` rows are proposed expansion candidates drawn from comparative Nahuatl data, prioritized toward Huasteca-adjacent material, and clearly labeled as proposed rather than silently merged into spoken EHN.\n\n## Beginner safety policy\n\nEvery Phase 7 list row carries a beginner flag:\n\n- `safe` = usable in beginner materials now\n- `unsafe` = keep in the lexicon, but do not place in beginner materials without editorial review\n\nUnsafe rows are typically:\n\n- obsolete/alternate spellings\n- bound morphemes\n- inflected reference forms\n- low-priority or sensitive lexical items\n- advanced civic/geographic terms\n\n## Output files\n\n- `core_ehn_250.csv`\n- `core_ehn_500.csv`\n- `core_ehn_1000.csv`\n- `core_verbs_100.csv`\n- `function_words.csv`\n- `social_interaction.csv`\n- `everyday_example_bank.csv`\n- `summary.json`\n- `fcn_master_lexicon_phase7_review.sqlite`\n\n## Phase 7 completion statement\n\nPhase 7 is complete at the **v0.1 infrastructure level**. The deliverable exists, is queryable, and is aligned with the FCN source and register rules. The next improvement step is not re-architecture; it is **editorial curation and speaker validation** on top of these lists.\n"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description='Build FCN Phase 7 core lexicon exports from the Phase 6 review DB.')
    parser.add_argument('--db', default='/mnt/data/fcn_master_lexicon_phase6_review.sqlite')
    parser.add_argument('--out-dir', default='/mnt/data/phase7_reports')
    parser.add_argument('--review-db', default='/mnt/data/fcn_master_lexicon_phase7_review.sqlite')
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    conn = sqlite3.connect(args.db)
    query = """
    SELECT e.entry_id, e.ehn_spoken_form, COALESCE(v.candidate_msn_headword, e.msn_headword) AS msn_headword,
           e.msn_headword AS current_msn_headword,
           e.msn_poetic_form, e.classical_citation_form, e.part_of_speech, e.register, e.variety,
           e.gloss_en, e.gloss_es, e.source_file, e.source_reference, e.source_confidence,
           e.speaker_validation_status, e.editorial_status, e.notes_internal, e.notes_public,
           v.rule_trace, v.search_fallbacks_json
    FROM lexicon_entries e
    LEFT JOIN v_phase6_ehn_review v ON e.entry_id = v.entry_id
    WHERE e.register IN ('EHN_colloquial','Comparative_only')
    """
    src = pd.read_sql_query(query, conn)
    conn.close()
    src = add_common_annotations(src)

    ehn = src[src['register'] == 'EHN_colloquial'].copy()
    comp = src[src['register'] == 'Comparative_only'].copy()
    ehn_safe = ehn[ehn['beginner_flag'] == 'safe'].copy()

    core250 = select_core_250(ehn_safe)
    core500 = select_core_500(ehn)
    core1000 = select_core_1000(ehn, comp)
    verbs100 = select_verbs_100(ehn, comp)
    function_words = select_function_words(ehn)
    social_interaction = select_social_interaction(ehn)
    examples = build_example_bank(ehn)

    core250_export = finalize_export(core250)
    core500_export = finalize_export(core500)
    core1000_export = finalize_export(core1000)
    verbs100_export = finalize_export(verbs100)
    function_export = finalize_export(function_words, extra_cols=['subgroup'])
    social_export = finalize_export(social_interaction)

    core250_export.to_csv(os.path.join(args.out_dir, 'core_ehn_250.csv'), index=False)
    core500_export.to_csv(os.path.join(args.out_dir, 'core_ehn_500.csv'), index=False)
    core1000_export.to_csv(os.path.join(args.out_dir, 'core_ehn_1000.csv'), index=False)
    verbs100_export.to_csv(os.path.join(args.out_dir, 'core_verbs_100.csv'), index=False)
    function_export.to_csv(os.path.join(args.out_dir, 'function_words.csv'), index=False)
    social_export.to_csv(os.path.join(args.out_dir, 'social_interaction.csv'), index=False)
    examples.to_csv(os.path.join(args.out_dir, 'everyday_example_bank.csv'), index=False)

    summary = {
        'ehn_total': int(len(ehn)),
        'ehn_safe': int((ehn['beginner_flag'] == 'safe').sum()),
        'ehn_unsafe': int((ehn['beginner_flag'] == 'unsafe').sum()),
        'ehn_verbs': int((ehn['part_of_speech'] == 'verb').sum()),
        'core_250_count': int(len(core250_export)),
        'core_500_count': int(len(core500_export)),
        'core_1000_count': int(len(core1000_export)),
        'core_1000_ehn_attested_count': int((core1000_export['attestation_status'] == 'EHN_attested').sum()),
        'core_1000_gap_fill_count': int((core1000_export['attestation_status'] == 'Comparative_gap_fill').sum()),
        'verbs_100_count': int(len(verbs100_export)),
        'verbs_100_ehn_attested_count': int((verbs100_export['attestation_status'] == 'EHN_attested').sum()),
        'verbs_100_gap_fill_count': int((verbs100_export['attestation_status'] == 'Comparative_gap_fill').sum()),
        'function_words_count': int(len(function_export)),
        'social_interaction_count': int(len(social_export)),
        'everyday_example_bank_count': int(len(examples)),
    }
    with open(os.path.join(args.out_dir, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Write deliverable docs
    write_markdown('/mnt/data/amoxcalli-nahuatl-project-main/phase7/fcn_phase7_core_lexicon.md', summary)
    readme = f"""# Phase 7 — Core Lexicon\n\nBuild command:\n\n```bash\npython3 fcn_phase7_build_core_lexicon.py \\\n  --db /mnt/data/fcn_master_lexicon_phase6_review.sqlite \\\n  --out-dir /mnt/data/phase7_reports \\\n  --review-db /mnt/data/fcn_master_lexicon_phase7_review.sqlite\n```\n\nThis generates the Phase 7 CSV exports and a review database with Phase 7 tables.\n\nCurrent counts:\n\n- EHN rows: {summary['ehn_total']}\n- EHN verbs: {summary['ehn_verbs']}\n- Core 250 rows: {summary['core_250_count']}\n- Core 500 rows: {summary['core_500_count']}\n- Core 1000 rows: {summary['core_1000_count']}\n- Function words: {summary['function_words_count']}\n- Social interaction rows: {summary['social_interaction_count']}\n- Everyday examples: {summary['everyday_example_bank_count']}\n"""
    with open('/mnt/data/amoxcalli-nahuatl-project-main/phase7/PHASE7_README.md', 'w', encoding='utf-8') as f:
        f.write(readme)

    # Review DB
    shutil.copyfile(args.db, args.review_db)
    review_conn = sqlite3.connect(args.review_db)
    core250_export.to_sql('phase7_core_250', review_conn, if_exists='replace', index=False)
    core500_export.to_sql('phase7_core_500', review_conn, if_exists='replace', index=False)
    core1000_export.to_sql('phase7_core_1000', review_conn, if_exists='replace', index=False)
    verbs100_export.to_sql('phase7_verbs_100', review_conn, if_exists='replace', index=False)
    function_export.to_sql('phase7_function_words', review_conn, if_exists='replace', index=False)
    social_export.to_sql('phase7_social_interaction', review_conn, if_exists='replace', index=False)
    examples.to_sql('phase7_everyday_examples', review_conn, if_exists='replace', index=False)
    review_conn.executescript("""
    DROP VIEW IF EXISTS v_phase7_gap_fill;
    CREATE VIEW v_phase7_gap_fill AS
    SELECT *
    FROM phase7_core_1000
    WHERE attestation_status = 'Comparative_gap_fill';

    DROP VIEW IF EXISTS v_phase7_beginner_unsafe;
    CREATE VIEW v_phase7_beginner_unsafe AS
    SELECT *
    FROM phase7_core_1000
    WHERE beginner_flag = 'unsafe';
    """)
    review_conn.commit()
    review_conn.close()


if __name__ == '__main__':
    main()
