"""B2: conservative development baseline using an exact human-selected focus.

Not a parser, extractor, five-field annotator or independently validated model.
Returns admission/denial/other/abstain with an inspectable reason.
"""
import re

def predict(context, focus_start, focus_end):
    if not isinstance(context, str) or not (0 <= focus_start < focus_end <= len(context)):
        raise ValueError('Focus must be a nonempty exact interval in context.')
    # Substitutions preserve offsets. Windows are bounded heuristics, not clauses.
    text = context.lower().replace('\u2019', "'").replace('\u2018', "'")
    focus = text[focus_start:focus_end].strip()
    before = re.split(r'[.!?;]', text[:focus_start])[-1][-180:]
    after = re.split(r'[.!?;]', text[focus_end:])[0][:100]
    if re.fullmatch(r'(?:did|do|does|chose|choose|happened|happen)', focus) or re.search(r'\b(?:blame|responsible)\b', focus):
        return 'abstain', 'unresolved_selected_action_or_responsibility'
    life_action = focus in {'take', 'takes', 'took', 'taking', 'taken'} and bool(re.search(r'\b(?:life|lives)\b', before[-45:] + ' ' + after[:45]))
    killing = bool(re.fullmatch(r'(?:kill|kills|killed|killing|murder|murders|murdered|murdering|execute|executes|executed|executing)', focus)) or life_action
    if not killing:
        return 'other', 'selected_focus_not_explicit_killing_action'
    if re.search(r'\b(?:say|says|said|think|thinks|thought|believe|believes|believed|claim|claims|claimed|confessed)\b', before):
        return 'abstain', 'possible_reporting_frame_in_bounded_prefix'
    if re.search(r'\b(?:if|would|could|might|may)\b', before):
        return 'abstain', 'possible_nonasserted_frame_in_bounded_prefix'
    if re.search(r'\b(?:warden|go ahead)\s*,?\s*$', before) or (focus in {'kill', 'murder', 'execute'} and not before.strip()):
        return 'abstain', 'possible_imperative'
    # Explicit life-taking in a forgiveness frame; this pattern does not infer
    # sincerity or establish guilt and does not cover arbitrary embedded acts.
    if life_action and focus == 'taking' and re.search(r'\bforgive\s+me\s+for\s*$', before):
        return 'admission', 'selected_life_taking_in_explicit_self_frame'
    passive = life_action and focus == 'taken' and re.match(r'\s+by\s+me\b', after)
    active = re.search(r"\bi\s+(?:(?:did\s+not|do\s+not|didn't|don't|have\s+not|haven't|never)\s+)?(?:(?:really|personally)\s+)?$", before)
    if passive:
        negated = bool(re.search(r'\b(?:not|never)\s*$', before))
        return ('denial' if negated else 'admission'), 'explicit_selected_passive_by_me'
    if active:
        negated = bool(re.search(r"\b(?:not|never|didn't|don't|haven't)\b", active.group()))
        return ('denial' if negated else 'admission'), 'explicit_selected_first_person_action'
    # A first-person patient is not a first-person agent. Other configurations
    # remain unresolved rather than being forced to ordinary negatives.
    if re.match(r'\s+me\b', after):
        return 'other', 'selected_action_has_self_patient_not_explicit_self_agent'
    return 'abstain', 'selected_agent_or_construction_not_covered'
