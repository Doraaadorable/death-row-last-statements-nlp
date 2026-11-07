"""Local construction checks over v1 literal matches; not a dependency parser.

Every original match is retained with a disposition. Proposed merges and
nonverbal uses remain auditable; ambiguous forms are not silently discarded.
"""
import re
from run_sampled_focus_smoke_v1 import literal_foci

LEXICAL_AFTER_AUX = re.compile(
    r"\s+(?:not\s+)?(?:(?:really|personally)\s+)?"
    r'(know|understand|kill|murder|execute|commit|do|come|receive|want|need|have|say|think|believe)\b', re.I)
LIFE_OBJECT = re.compile(r'\s+(?:(?:a|an|the|his|her|their|your|my|our|another)\s+)?(?:life|lives)\b', re.I)

def candidates(context):
    text = context.lower().replace('\u2019', "'").replace('\u2018', "'")
    output = []
    for start, end, focus in literal_foci(context):
        word = text[start:end]
        before, after = text[max(0,start-70):start], text[end:end+90]
        disposition, reason = 'retain_literal_focus', 'no_local_construction_flag'
        linked_head = None
        if word in {'did','do','does'}:
            match = LEXICAL_AFTER_AUX.match(after)
            if match:
                hs, he = end+match.start(1), end+match.end(1)
                disposition, reason = 'merge_auxiliary_with_head', 'local_auxiliary_plus_base_verb'
                linked_head = {'start':hs,'end':he,'text':context[hs:he]}
            elif word == 'do' and (re.match(r'\s+away\s+with\b',after) or re.search(r'\bnothing\s+to\s*$',before)):
                disposition, reason = 'needs_multiword_interpretation', 'do_away_with_or_nothing_to_do_with'
            elif re.search(r'\b(?:yes\s+i|he|she|it|they|we|you)\s*$',before) and re.match(r'\s*[,;.!?]',after):
                disposition, reason = 'needs_ellipsis_interpretation', 'possible_proverb_or_elliptical_response'
        if word in {'killing','murders'} and (re.search(r'\b(?:more|any|the|a)\s*$',before) or re.search(r"\b\w+'s\s*$",before)):
            disposition, reason = 'possible_nominal_use', 'local_determiner_or_possessive_cue_not_pos_proof'
        if word in {'take','takes','took','taking','taken'}:
            passive_life = word == 'taken' and bool(re.search(r'\b(?:life|lives)\s+(?:was|were|is|are|had\s+been|have\s+been)\s+(?:not\s+)?$',before))
            if LIFE_OBJECT.match(after) or passive_life:
                reason = 'local_life_argument_pattern'
            else:
                disposition, reason = 'life_attachment_not_established', 'no_direct_life_object_or_supported_passive_pattern'
        output.append({'focus_start':start,'focus_end':end,'predicate_focus':focus,
            'disposition':disposition,'reason':reason,'linked_lexical_head':linked_head})
    return output
