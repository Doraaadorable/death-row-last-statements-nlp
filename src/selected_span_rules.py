"""Known-example-informed rules; no reference labels or record IDs as inputs."""
import re

KILL = r'\b(?:kill(?:s|ed|ing|er|ers)?|murder(?:s|ed|ing|er|ers)?|execut(?:e|es|ed|ing))\b|\b(?:take|takes|took|taken|taking)\b.{0,35}\b(?:life|lives)\b|\b(?:life|lives)\b.{0,35}\b(?:taken|took)\b'
NEG = r"\b(?:not|never|no|didn't|don't|can't|couldn't)\b"
FIRST = r'\b(?:i|me|my|myself)\b'
DIRECT = r"\bi\s+(?:(?:did\s+not|didn't|never|have\s+not|haven't)\s+)?(?:personally\s+)?(?:kill(?:ed)?|murder(?:ed)?|execut(?:e|ed)|took|take)\b"
DIRECT_LIFE = r'\bi\s+(?:(?:did\s+not|never)\s+)?(?:took|take)\b.{0,30}\blife\b'
PASSIVE = r'\b(?:life|lives)\b.{0,25}\b(?:taken)\b.{0,15}\bby\s+me\b'
FORGIVE = r'\bforgive\s+me\s+for\s+taking\b.{0,25}\blife\b'
REPORT = r'\b(?:people|they|you)\s+(?:say|said|think|believe|claim)\b|\baccording\s+to\b'
HYPOTHETICAL = r'\b(?:if|would|could|might)\b'
AMBIGUOUS = r'\bi\s+(?:(?:did\s+not|didn.t)\s+)?(?:did|do|chose)\s+(?:it|this)\b|\b(?:blame|responsible)\b'

def clean(text):
    return text.lower().replace('\u2019', "'").replace('\u2018', "'")

def hit(pattern, text):
    return bool(re.search(pattern, text, flags=re.I))

def lexical(span, preceding=''):
    text=clean(span)
    if not hit(KILL,text):return 'other','no_killing_lexeme'
    if not hit(FIRST,text):return 'other','no_first_person_mention'
    return ('denial' if hit(NEG,text) else 'admission'),'first_person_mention_plus_killing_lexeme'

def constrained(span, preceding=''):
    text=clean(span)
    # Only the preceding fragment of the same sentence, bounded to 150 characters.
    before=re.split(r'[.!?]',clean(preceding))[-1][-150:]
    if not hit(KILL,text):
        return ('abstain','unresolved_action_or_responsibility') if hit(AMBIGUOUS,text) else ('other','no_explicit_killing_proposition')
    if hit(r'\b(?:killer|killers|murderer|murderers)\b',text) and not hit(r'\b(?:kill|killed|murder|murdered|taking|taken|took|executed)\b',text):
        return 'other','agent_noun_characterization'
    if hit(r'\b(?:warden|go ahead)\b',text) and hit(r'\bmurder\s+me\b',text):
        return 'other','imperative_directed_at_other'
    if hit(HYPOTHETICAL,text) and not hit(r'\bwill\b',text):
        return 'other','hypothetical_or_modal_frame'
    if hit(FORGIVE,text):return 'admission','explicit_life_taking_in_self_forgiveness_frame'
    passive=re.search(PASSIVE,text)
    direct=re.search(DIRECT,text)
    # A took/take match must explicitly supply life; no implicit result resolution.
    if direct and hit(r'\b(?:take|took)\b',direct.group()) and not hit(DIRECT_LIFE,text):direct=None
    if passive or direct:
        if direct and hit(r"\b(?:don't|do not|didn't|did not)\s+(?:know|understand)\b", text[:direct.start()]):
            return 'abstain','knowledge_governs_embedded_action'
        local=text[:direct.start()] if direct else ''
        if hit(REPORT,before+' '+local):return 'abstain','possible_external_attribution'
        return ('denial' if hit(NEG,text) else 'admission'),('passive_by_me' if passive else 'direct_first_person_action')
    if hit(r'\b(?:you|they|texas|people)\b',text) or hit(r'\bkill\s+me\b',text):
        return 'other','not_explicit_self_agent'
    return 'abstain','unresolved_killing_agent_or_attribution'

METHODS={'B0_lexical':lexical,'B1_constrained':constrained}
