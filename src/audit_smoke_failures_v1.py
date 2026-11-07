"""AI qualitative triage of known smoke outputs, not reference annotation."""
from pathlib import Path
from collections import Counter
import hashlib
import json

# Manual inspection after seeing predictions. No new predictions or tuning.
GROUPS = {
    'auxiliary_selected_without_lexical_head': [(211,754),(320,94),(320,162),(372,256),(372,283),(372,331),(256,644)],
    'ellipsis_needs_reconstruction_and_scope_check': [(372,6),(378,331)],
    'nominal_action_word_not_independent_verb': [(248,1145),(273,51)],
    'nearby_life_token_crosses_selected_predicate': [(211,1483)],
    'self_speech_frame_triggers_reporting_abstention': [(372,264)],
    'multiword_expression_not_resolved': [(273,31),(122,406)],
    'procedural_do_context_needs_scope_filter': [(211,1964),(211,1984),(256,735),(256,755),(256,810),(256,822)],
    'remaining_action_reference_agent_or_mood_limit': [(211,248),(211,659),(211,724),(211,928),(211,1467),(211,1549),(248,1051),(320,170),(372,291)],
}

def build(root):
    root = Path(root)
    path = root / 'reports/sampled_focus_smoke_v1.json'
    smoke = json.loads(path.read_text())
    abstentions = [p for p in smoke['predictions'] if p['prediction'] == 'abstain']
    lookup = {(p['execution_number'],p['focus_start']):p for p in abstentions}
    assigned = [key for keys in GROUPS.values() for key in keys]
    if len(assigned) != len(set(assigned)) or set(assigned) != set(lookup) or len(assigned) != 30:
        raise ValueError('Qualitative crosswalk must cover exactly the original 30 abstentions once.')
    output = []
    for category, keys in GROUPS.items():
        for key in keys:
            output.append({**lookup[key], 'proposed_primary_triage': category,
                           'review_status':'AI_post_prediction_inspection_not_owner_adjudicated'})
    zero_ids = [d['execution_number'] for d in smoke['documents'] if d['literal_focus_count']==0]
    if sorted(zero_ids) != [108,216,409]:
        raise ValueError('Zero-focus documents differ from known run.')
    return {'scope':'post_prediction_development_triage_not_error_rate',
        'inputs_sha256': {'reports/sampled_focus_smoke_v1.json':hashlib.sha256(path.read_bytes()).hexdigest(),
                          'src/audit_smoke_failures_v1.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'original_rule_reason_counts':dict(Counter(p['reason'] for p in abstentions)),
        'proposed_triage_counts':{category:len(keys) for category,keys in GROUPS.items()},
        'abstention_triage':output,
        'zero_focus_document_notes':[
            {'execution_number':108,'note':'Religious message includes innocent ones; this is not automatically a personal legal innocence claim. No exhaustive scope judgment is claimed.'},
            {'execution_number':216,'note':'Religious crucified-with-Christ wording is outside the literal focus inventory. Figurative/religious harm language needs an explicit scope decision, not automatic literal killing interpretation.'},
            {'execution_number':409,'note':'Biblical comfort and closure language; no literal focus found. This is not proof of complete extraction.'}],
        'limitations':['Categories are manually assigned AI observations after predictions, not reference truth.',
            'Primary triage categories are mutually exclusive for bookkeeping; mechanisms can overlap.',
            'Abstention is not by itself an error, and remaining predictions were not exhaustively adjudicated.',
            'No automatic-extraction recall can be estimated without a complete independent predicate inventory.',
            'B2 and literal adapter remain unchanged.']}

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = build(root)
    output = root/'reports/smoke_failure_triage_v1.json'
    payload = json.dumps(result,indent=2)+'\n'
    if output.exists() and output.read_text()!=payload:
        raise FileExistsError('Preserve old triage; version changed observations.')
    if not output.exists():output.write_text(payload)
    print(json.dumps(result['proposed_triage_counts'],indent=2))
    print('30 abstentions cross-referenced; 3 zero-focus document notes. No labels or methods changed.')
