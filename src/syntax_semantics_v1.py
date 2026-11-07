"""Conservative partial semantic proposals from saved parser rows, not gold."""
REPORTING = {'say','tell','claim','think','believe','confess','report'}
KILLING = {'kill','murder','execute'}
KNOWLEDGE = {'know','understand'}

def person(heads):
    if len(heads)!=1:return 'unclear'
    text=heads[0]['text'].lower()
    if text in {'i','me','myself'}:return 'self'
    if text in {'you','he','she','they','him','her','them'}:return 'other'
    if text in {'anyone','someone','anybody','somebody'}:return 'unspecified'
    # No pronoun/coreference or named-entity resolution is performed here.
    return 'unclear'

def propose(row, context, by_start):
    focus=row['focus'];lemma=focus['lemma'].lower();flags=[]
    passive=any(h['dependency'] in {'nsubjpass','csubjpass'} for h in row['subject_heads']) or any(a['dependency']=='auxpass' for a in row['auxiliaries'])
    actor=person(row['passive_agent_heads'] if passive else row['subject_heads'])
    if passive and not row['passive_agent_heads']:flags.append('passive_agent_not_explicitly_recovered')
    objects={h['lemma'].lower() for h in row['object_or_complement_heads']}
    patients={h['lemma'].lower() for h in row['subject_heads'] if h['dependency'] in {'nsubjpass','csubjpass'}}
    if lemma in KILLING:event='killing_action'
    elif lemma=='take' and ('life' in objects or (passive and 'life' in patients)):event='killing_action'
    elif lemma in KNOWLEDGE:event='knowledge'
    elif (lemma=='take' and 'blame' in objects) or (lemma=='be' and 'responsible' in objects) or lemma=='wrong':event='wrongdoing_unspecified'
    elif lemma in {'do','choose','happen'}:
        event='unclear';flags.append('implicit_action_or_ellipsis_unresolved')
    else:event='other'
    polarity='negated' if row['negation_children'] else 'affirmed'
    flags.append('polarity_uses_direct_dependency_negation_only')
    governor=row['governing_predicate'];source='unclear'
    sentence=context[row['sentence_start']:row['sentence_end']]
    quotes=any(q in sentence for q in ['"','“','”'])
    if governor is None and row['subject_heads'] and not quotes:
        source='self'
    elif governor is not None:
        parent=by_start.get(governor['start'])
        if parent and governor['lemma'].lower() in REPORTING:
            owner=person(parent['subject_heads'])
            if owner=='other':source='other'
            elif owner=='self' and parent['governing_predicate'] is None and not quotes:source='self'
        flags.append('embedded_source_not_general_attribution_resolution')
    if quotes:flags.append('quotation_scope_unresolved')
    # Modal, imperative, embedded and coordination presentations require more
    # evidence than this saved direct-child representation supplies.
    modal=any(a['lemma'].lower() in {'would','could','can','may','might','must','should'} for a in row['auxiliaries'])
    question='?' in sentence
    if governor is None and row['subject_heads'] and not quotes and not modal and not question:
        status='presented_as_true'
    else:
        status='unclear';flags.append('presentation_or_modality_unresolved')
    fields={'claim_source':source,'event_type':event,'event_actor':actor,'polarity':polarity,'proposition_status':status}
    if event not in {'killing_action','unclear'}:label='other'
    elif event=='unclear':label='abstain'
    elif source=='other' or actor=='other' or actor=='unspecified':label='other'
    elif source==actor=='self' and status=='presented_as_true':label='denial' if polarity=='negated' else 'admission'
    else:label='abstain'
    return {'proposed_fields':fields,'target_prediction':label,'flags':flags,
            'voice_evidence':'passive' if passive else 'active_or_unresolved',
            'scope_status':'not_assigned','review_status':'automatic_partial_proposal_not_owner_adjudicated'}
