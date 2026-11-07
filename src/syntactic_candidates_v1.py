"""Parser-proposed predicate inventory; no automatic semantic reference labels."""
AUX_DEPS = {'aux','auxpass','cop'}
SUBJECT_DEPS = {'nsubj','nsubjpass','csubj','csubjpass'}
OBJECT_DEPS = {'dobj','obj','iobj','attr','acomp','oprd'}

def token_record(token):
    return {'text':token.text,'start':token.idx,'end':token.idx+len(token.text),
            'lemma':token.lemma_,'pos':token.pos_,'dependency':token.dep_}

def extract(doc):
    if not doc.has_annotation('DEP') or not doc.has_annotation('POS'):
        raise ValueError('A trained parser and POS annotations are required.')
    predicates = [t for t in doc if t.pos_ in {'VERB','AUX'} and t.dep_ not in AUX_DEPS]
    indices = {t.i for t in predicates}
    rows=[]
    for token in predicates:
        children=list(token.children)
        subjects=[c for c in children if c.dep_ in SUBJECT_DEPS]
        objects=[c for c in children if c.dep_ in OBJECT_DEPS]
        agents=[]
        for child in children:
            if child.dep_=='agent':
                agents.extend(c for c in child.children if c.dep_ in {'pobj','obj'})
        governor=next((a for a in token.ancestors if a.i in indices),None)
        rows.append({'focus':token_record(token),
            'kind':'copular_or_be_predicate' if token.lemma_=='be' else ('unattached_auxiliary_possible_ellipsis' if token.pos_=='AUX' else 'lexical_verb'),
            'sentence_start':token.sent.start_char,'sentence_end':token.sent.end_char,
            'auxiliaries':[token_record(c) for c in children if c.dep_ in AUX_DEPS],
            'negation_children':[token_record(c) for c in children if c.dep_=='neg'],
            'subject_heads':[token_record(c) for c in subjects],
            'object_or_complement_heads':[token_record(c) for c in objects],
            'passive_agent_heads':[token_record(c) for c in agents],
            'governing_predicate':token_record(governor) if governor is not None else None,
            'scope_status':'not_assigned','semantic_fields':'not_assigned'})
    return rows
