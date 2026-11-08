# Responsibility, connection and approaching death in Texas last statements

Exploratory report; institutional-context framing updated 8 November 2026.

## Research question
How do people facing execution express feelings, sustain relationships and make
sense of their situation, particularly when discussing responsibility and death?

Chinese: 面对执行时，人们如何表达感受、维系关系，并在谈论责任与死亡时理解自身处境？

The aim is to understand psychological expression in context. The unit of
interpretation is the complete recorded statement; shorter passages provide
traceable evidence within that statement. This report concerns public language,
not a diagnosis of private experience or a determination of actual guilt.

## Materials and approach
The project inventory contains 603 execution records, leading to 480 candidate
person-level documents, 479 prepared texts and 477 nonzero-feature NMF texts.
The existing development sample has 50 people, ten per decade. The present
reading uses the 20 complete candidate texts listed in
[the reading selection](../reports/open_reading_selection_v1.json), chosen from
that development material for contrast. Their selection used earlier categories
and discussions; this is a purposive comparison, not a prevalence sample.

The [workbook](OPEN_READING_WORKBOOK_v1.md) preserves each complete candidate
text and its existing source-context hash. Every memo separates evidence,
interpretation and alternative readings. All 20 statements were examined in dialogue with the project owner. Memos
now incorporate her interpretations, subsequent refinements and unresolved
readings. Completion refers to discussion of the texts, not agreement on every
possible meaning or a new set of frozen labels. No new reference labels have been assigned.
The eight-category annotations, NMF results and syntax experiments are retained
as earlier work; none was refitted for this report.

Two organizing questions emerged from reading. They are lenses for comparison,
not a newly validated codebook:

1. **Responsibility and judgment:** what is accepted, denied, explained or
   criticized, and who is positioned to judge or forgive?
2. **Connection and approaching death:** to whom are feelings addressed, what
   relationships are maintained, and how are departure and death described?

Self-reported feelings and changes of addressee are tracked across both lenses.
Unexpected cases remain visible rather than being forced into both.

## Descriptive context from the frozen 50-person sample
The existing development labels provide context for the case readings. They
are unchanged and are not psychological diagnoses. Each decade contributes ten
people, so the sample's composition differs from the candidate corpus. The
following are raw document counts in these 50 records, not estimates for 480
candidate statements or all executed people. Unresolved values remain visible.

| Existing category | Present (1) | Absent (0) | Unresolved (u) |
| --- | ---: | ---: | ---: |
| Affection / relational connection | 37 | 12 | 1 |
| Gratitude | 24 | 26 | 0 |
| Faith / spirituality | 27 | 20 | 3 |
| Apology / forgiveness | 22 | 26 | 2 |
| Harm acknowledgment | 12 | 32 | 6 |
| Culpability dispute | 8 | 40 | 2 |
| Justice criticism | 8 | 38 | 4 |
| Farewell / closure / readiness | 33 | 13 | 4 |

The combined apology/forgiveness category includes different directions and
objects; its count is not an apology prevalence measure. Likewise, farewell,
closure and readiness are combined in the old coding, and culpability dispute
is broader than an explicit claim of complete innocence. Later reading memos
do not retroactively replace these frozen decisions.

Selected pair counts connect the descriptive material with the case questions.
Every row retains denominator 50; unresolved means at least one of the two
labels is u. The display is chosen for interpretive relevance after the reading,
not as a prespecified hypothesis test. All 28 pairs, their full five-way counts
and supporting execution IDs are available in the
[machine-readable summary](../reports/expression_sample_descriptive_v1.json).

| Pair of existing categories | Both present | At least one unresolved | Denominator |
| --- | ---: | ---: | ---: |
| Affection / relational connection + Apology / forgiveness | 19 | 3 | 50 |
| Faith / spirituality + Farewell / closure / readiness | 19 | 7 | 50 |
| Apology / forgiveness + Culpability dispute | 3 | 3 | 50 |
| Justice criticism + Farewell / closure / readiness | 5 | 8 | 50 |
| Culpability dispute + Farewell / closure / readiness | 7 | 6 | 50 |

The three documents coded present for both apology/forgiveness and culpability
dispute are #508, #595 and #600. Their complete-text readings differ: an accident
account, denial of harmful intent, and a partially specified involvement account.
This makes them useful contrasts, not three interchangeable examples of
apologizing while claiming complete innocence. Similarly, the five documents
with justice criticism and closing/readiness codes (#58, #138, #219, #461,
#583) do not establish acceptance of punishment.

These are descriptions of the development labels and partly overlapping
material already used to choose the reading set. They do not independently
validate the six-case interpretations. No inferential test, association effect,
causal inference or population estimate is reported.

Reproduce from the released data snapshot at the project root:

```bash
python src/summarize_expression_sample.py
```

The script uses Python's standard library, checks 50 unique IDs and valid
1/0/u values, records the input SHA-256, and retains unresolved pair counts.
It produces the same output when rerun on the same input. It does not overwrite
a differing existing result.

## Findings from contextual comparison

### 1. Responsibility has an object; accepting it is not a single all-purpose position
In #508, apology for the family's loss and acceptance of responsibility coexist
with an accident account and denial of murder. The speaker reports being at
peace and signals readiness, without withdrawing that explanation. In #407,
acknowledgment of wrong and willingness to bear a penalty coexist with criticism
of its consequences for loved ones. #138 combines an apology, a narrative of
personal change and opposition to execution.

These cases distinguish several objects of judgment: loss, involvement, intent,
characterization of the act, the penalty and its effects. They do not demonstrate
that the speakers privately resolved every moral conflict. They show why a
single confession/denial or acceptance/rejection summary can omit what is said.

Boundary cases strengthen this interpretation. #595 denies intending harm while
acknowledging wrong choices. #600 combines partial involvement, uncertain event
knowledge and a conditional offer to take blame. Neither should be reduced to
an unqualified confession or a complete denial. By contrast, #58 explicitly
asserts innocence. These are different textual positions, not judgments about
which account is factually correct.

### 2. Family connection is maintained amid unresolved responsibility and forgiveness
In #407, the speaker says he understands his uncle cannot forgive him, then
reasserts that he remains his nephew. The relationship claim persists without a
recorded reconciliation. #461 turns from a condemnation of execution to mother
and father, invoking love and home. #433 moves between harm acknowledgment,
forgiveness requests and continuing presence for a loved one.

Family language is not confined to accounts of victimhood or defense. #413
pairs explicit harm acknowledgment with thanks and relationships; #49 contains
only a request to convey love to a mother. These contrasts challenge the idea
that affection itself establishes either moral evasion or moral redemption.
They also distinguish a statement's content from an inferred personality trait:
a particular family address does not establish that family values dominate the
speaker's whole life.

### 3. Spiritual references perform different functions
In #508, God's knowledge can support the speaker's explanation of the event.
In #413, religious petitions accompany explicit acknowledgment of harm. #153
frames departure through mercy, reunion and a religious purpose for death.
#600 invokes a religious obligation in an appeal for forgiveness, which could
be heard as consolation or as pressure. #1 explicitly differentiates bodily
fear from fear directed toward God.

Faith is therefore not treated as one emotion, one coping mechanism or a proxy
for acceptance. The wording can identify a judge, a source of mercy, a future
relationship or a meaning for departure. Determining whether religion caused
calm or transformation would require evidence beyond a final statement.

### 4. Readiness, emotional state and endorsement of punishment are separable
#58 combines readiness with emphatic innocence and rejection of what is happening.
#15 gives only a brief closing and readiness; it does not name a feeling.
#11 adds a statement of desert, a substantively different evaluation. #39
couples a positively described destination with a signal to proceed.

The strongest emotional evidence is specific self-description: #508 reports
peace, while #1 distinguishes the objects of fear. #32 instead wishes peace
for another person. Recording whose peace or fear is at issue matters before
summarizing emotional orientation. The crying annotation in #461 is a recorded
observation, not the speaker's own identification of a particular emotion.

### 5. A reading response can shift without revealing the speaker's motive
The discussion of #461 documented movement from irritation at the accusation,
to sympathy with the family address, to suspicion that the sequence solicits
sympathy. The owner connected the sympathy to her own strong family orientation.
This is a useful reflexive record of one encounter with the text.

The statement foregrounds the speaker's treatment and family, while leaving the
original offense and its victims unmentioned. That distribution of attention is
observable. Deliberate manipulation, hypocrisy and an absence of private remorse
are not established. Genuine attachment and a self-presentational function are
also compatible. No audience experiment or independent reader sample was
conducted, so this episode is not a finding about how readers generally react.

## Case contrasts and evidence trail
| Comparison | Executions | What the comparison supports |
| --- | --- | --- |
| Responsibility with different limits | 508, 407, 595, 600 | Distinguish harm, intent, involvement and penalty |
| Affection with and without explicit defense | 407, 461, 413, 49 | Family address does not by itself identify avoidance |
| Religious judgment, mercy and future connection | 508, 413, 153, 1 | Interpret spiritual language in its local role |
| Ready versus deserving | 58, 15, 11, 39 | Procedural readiness is not a uniform moral position |
| Own peace versus another person's hoped-for peace | 508, 524, 32 | Identify experiencer and addressee before affect interpretation |
| Case-focused versus relationship-focused statements | 219, 583, 49 | Leave room for statements that do not fit every lens |

The remaining cases, including #330, #433 and #138, are retained in full in the
workbook. The evidence trail covers all 20 texts without treating each as an
instance of every proposed interpretation.

## Revisions arising from the reading discussion
The discussion sharpened the following interpretations without changing source
texts or the earlier labels:

| Cases | Revision or unresolved distinction |
| --- | --- |
| 330, 433 | Comfort and continued connection are contextual readings; love and thanks are explicit. The final apology in 433 may concern separation or earlier harm. |
| 413 | Strong self-reproach is supported; the closing may seek relief, but does not establish achieved peace. The earlier peace wish addresses others. |
| 138 | Friends being punished may refer to suffering a loss or to imprisoned friends; neither is silently resolved. Completed punishment is not a statement that sins were erased. |
| 595 | A hoped-for encounter with the victim is read as possible reconciliation, not established fixation. Family apologies address absence; broad wrong-choice language does not specify every act. |
| 600 | Religious conditionality can be experienced as pressure to forgive. The owner's doubt about sincerity is separated from the observable lack of responsibility detail. |
| 58, 219, 583 | Readiness and ending a speech coexist with continued protest. Helplessness, irony and resistance are contextual readings, not personality diagnoses. |
| 153 | Offering death for a religious purpose is distinguished from declaring the punishment deserved. |
| 524 | The owner withdrew sarcasm in favor of anticipated hostility after reading the context. |
| 11, 15 | Desert is an explicit evaluation; bare readiness does not identify emotion. |
| 32, 39, 1, 49 | Identify whose peace, what destination, what object of fear and which explicitly named relationship; do not fill missing content with presumed experience. |

In #600, the owner felt that linking another person's forgiveness to God's
forgiveness imposed a moral burden on the listener. This concerns the experienced
force of the words; a deliberate intention to coerce is not established.
In #433, the owner moved from a sense of moral distance in the declaration of
love to greater closeness in the forgiveness requests. Together with #461,
these responses show why the analyst's reactions should be recorded as reactions,
not converted into facts about the speaker or other listeners.

The counterexamples remain important. #413 combines explicit harm acknowledgment
with religious petitions; #595 links family attachment with responsibility
language; #49 expresses love without a developed defense. They prevent the
initial suspicion of self-presentation from becoming a blanket interpretation
of affection or faith.

## Relation to existing research
The sources below were checked on 7 November 2026. The two previously outstanding papers have now been supplied and read; the
[full-text comparison](LITERATURE_COMPARISON.md) records methods and page anchors.

| Source | Evidence accessed and relevance | Consequence for this project |
| --- | --- | --- |
| Schuck & Ward (2008), [DOI](https://doi.org/10.1177/0957926507083687) | Relevant sections of author-uploaded text checked; see the [literature comparison](LITERATURE_COMPARISON.md) | The broad contextual approach has a direct precedent; it is not a new research gap |
| Hirschmüller & Egloff (2016), [full text](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.01985/full) | Methods/results: LIWC word proportions in 407 statements; more positive than negative emotion words | Word proportions answer a different question from the objects and functions of statements |
| Eaton & Theuer (2009), [publication](https://doi.org/10.1080/07418820802245078) | Full text: separate apology, remorse, guilt and responsibility variables; 305 statements | Compare textual definitions and distinguish explicit peace from perceived peace |
| Mehra et al. (2024), [full text](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2024.1463692/full) | Methods/results: 466 statements, computational emotion/notion analysis including co-occurrence and sequencing | Neither mixed expression nor sequence alone can be claimed as novel |
| Zhuo & Chun (2026), [publication](https://journals.sagepub.com/doi/abs/10.1177/00302228261437890) | Full text: 198 White-classified inmates, iterative manual expression coding | Close conceptual and source overlap, including religious admonition and our Green/Mason cases |

The closer full-text check confirms substantial prior coverage; the present
case distinctions should be framed as illustrations and contextual elaborations,
not discoveries absent from the 2008 framework.

There is no demonstrated contradiction between positive-word proportions and
other studies' dominant-emotion classifications: samples, measurement units and
category definitions differ. This report does not reproduce either measure.

The defensible contribution at this stage is a transparent contextual comparison
on this saved corpus: distinguish the object of responsibility, the direction of
forgiveness, the experiencer of emotion and the meaning of readiness. It is an
exploratory extension and research portfolio result. A distinct publication-level
gap is not established, particularly given the close 2008 and 2026 precedents. The 2009 paper also
separates guilt and responsibility; the 2026 paper directly discusses forgiveness
with theological admonition. These points are not claimed as new findings here.

## Conclusions and limits
The reviewed statements give examples of attachment alongside dispute, apology
alongside criticism of execution, and spiritual expression with differing
functions. Their coexistence does not automatically indicate inconsistency.
Interpreting the object, addressee and local sequence explains more than assigning
one overall emotional or moral position to each speaker.

The selected cases do not establish how common these patterns are among all
available statements or all executed people. A final public statement also cannot
establish sincerity, actual guilt, psychological diagnosis, emotional change over
time or the speaker's full relationship history. Missing text is particularly
important: recorded ellipses and editorial notes are preserved, and a complete
candidate record is not a guarantee of a complete original utterance.

This report completes the synthesis of the 20-case reading discussion.
Interpretations remain open to revision; disagreement and ambiguity are retained. Any empirical expansion should retain
contradictory and brief cases rather than select only examples supporting the
initial interpretation.

## Focused comparison: forgiveness, responsibility and relational repair

### Question and evidence
How do people facing execution use requests for, and declarations of,
forgiveness to express self-reproach, sustain relationships and negotiate
responsibility?

The six cases below were chosen from the already discussed 20-case set for
contrasting forms of forgiveness and relationship address. This is a further
interpretation of the same material, not an additional sample or a frequency
analysis. The whole statements remain in the [workbook](OPEN_READING_WORKBOOK_v1.md).
The comparison uses four questions: who addresses whom, what is being forgiven,
what position the speaker takes, and what response is actually available in the
record. No new reference labels are assigned.

| Execution | Evidence in the recorded statement | Relation being attempted | What remains unresolved |
| --- | --- | --- | --- |
| 413 | “Please forgive me.”; “I have done some horrible things.” | Harm acknowledgment and repeated requests to families and God | Whether forgiveness is granted or emotional relief achieved |
| 407 | “I know you can't give your forgiveness”; “I am still your nephew” | Maintaining kinship despite the speaker's account of unavailable forgiveness | The uncle's actual response and whether reconciliation follows |
| 600 | “I will take the blame if it will help”; “He will not forgive us” | Seeking forgiveness while invoking a religious consequence | Scope of responsibility and the listener's response |
| 461 | “they are all forgiven by me” | Granting forgiveness from the position of someone who describes being wronged | Exact recipients; this is not an explicit claim of innocence |
| 595 | “I never meant to hurt her”; “forgive me for giving up on y'all and walking away” | Moving between the victim's family and wife/children with different objects of apology | Specific acts meant by giving up and whether either relationship is repaired |
| 508 | “sorry for your loss”; “I take full responsibility”; “it was an accident” | Apology and responsibility alongside a qualified account of the event | Exact responsibility accepted and the family's response |

### 1. Self-reproach does not supply the recipient's answer
In #413, repeated acknowledgment of harm accompanies questions about whether he
is worthy of asking for forgiveness. The speaker addresses both people and God,
but those appeals do not have interchangeable recipients. Forgiveness from one
would not establish forgiveness from the other. The wish that the people harmed
find peace also does not describe peace already obtained by the speaker.

#407 provides a contrasting configuration. He says he understands his uncle
cannot forgive him and still calls himself a nephew. Instead of a completed
repair, the text presents the persistence of a relationship claim where repair
is unresolved. The owner reads a wish to remain recognized as family. That
reading concerns the relation he tries to sustain, not evidence that his uncle
accepts it or that he privately fears abandonment.

These cases make a useful psychological distinction: expressed self-reproach,
hope for recognition and achieved reconciliation are different matters. A final
statement can articulate the first two without recording the third.

### 2. Asking for forgiveness can also define what the other person ought to do
In #600, the desired response is explicit and repeated: forgive me and do not
hate me. His account of involvement is less specific, including partial
participation, uncertain event knowledge and conditional willingness to take
blame. These features should be retained together rather than reduced to either
full responsibility or no responsibility.

The religious argument changes the terms of the appeal. Connecting refusal to
forgive with exclusion from divine forgiveness can make forgiveness sound like
an obligation for the listener. In discussion, the owner experienced this as
pressure and felt that the strong request was not matched by equivalent detail
about responsibility. That is a documented reading response, not proof of
intentional manipulation or the response of the victim's family.

This interpretation has a close precedent in Zhuo & Chun's Example 10
(pp. 14–15), which discusses a theological warning in forgiveness language.
Our contribution here is the explicit within-case comparison between the scope
of responsibility and the terms of the appeal, not discovery of religious
pressure as an unknown phenomenon.

### 3. Granting forgiveness changes the speaker's relational position
#461 reverses the direction of the exchange. Rather than asking forgiveness
for the original offense, he declares forgiveness for people involved in what
he calls an atrocity. He thereby speaks from the position of the person wronged
by execution and authorized, in his own account, to forgive.

His turn toward parents and home then makes family connection salient. The
owner's reaction moved from irritation, through sympathy, to concern about
self-presentation. None of those responses establishes insincerity. The
observable contrast is that he discusses his treatment and family while not
discussing the original offense or its victims. Those omissions describe the
statement's focus, not an absence of private remorse or an explicit declaration
of innocence.

Placed beside #413, the word forgiveness does not indicate a uniform stance.
In one, it is sought after harm acknowledgment; in the other, it is granted
from an asserted position of injury. Their emotional meanings depend partly
on the different relations each utterance constructs.

### 4. A change of addressee can change what the apology is about
In #595, an appeal to the victim's family includes a denial of intending harm
and a wished-for afterlife encounter with the dead person. The owner came to
read this as possible reconciliation rather than fixation. The statement then
addresses wife and daughters about giving up and leaving, explicitly telling
them they did nothing wrong. The latter apology concerns absence and family
roles, even though its precise circumstances are not specified.

The broad acknowledgment of wrong choices later in the statement does not
remove those differences. It offers a life-level summary without specifying
every act. Similarly, #508 apologizes for loss while maintaining an accident
account. Sorrow about a consequence, acknowledgment of involvement and a
claim about intent should remain distinguishable.

Eaton & Theuer already code recipients and separate guilt from responsibility
(pp. 334–335). The present comparison uses those distinctions in complete
statements to examine the relationships being addressed. It does not present
them as a newly discovered conceptual framework.

### Religious context and the function of a particular appeal
Smith (2019, p. 348) defines nonreligious forgiveness by the absence of religious
expression anywhere in the statement. Our memos ask a complementary question:
what work does a particular religious reference do in its local sequence?
In #413, petitions address mercy alongside explicit harm acknowledgment; in
#600, religious consequences bear on the listener's forgiveness; in #508, God
is invoked as a judge who knows what happened; #595 imagines an encounter beyond
death. These can all belong to religious-context statements without becoming
one kind of appeal or demonstrating one psychological outcome.

This is a possible analytical elaboration rather than a competing classifier.
There is no new recoding, accuracy claim or category-frequency estimate. Nor
does it establish that earlier qualitative interpretation lacked such nuance.
It keeps the original question about psychological expression attached to
specific language and relationships.

### Boundary and alternative cases
The comparison should not make forgiveness the meaning of every final statement.
#49 only requests that love be conveyed to a mother; #15 does not provide enough
information to name an emotion. Their brevity does not license a missing
forgiveness narrative. #58 expresses readiness while asserting innocence; it
prevents procedural readiness from becoming a proxy for reconciliation.

Nor does religious language invariably reduce acknowledgment of harm. #413
explicitly acknowledges serious harm while praying; #153 joins a sinner identity,
petitions for mercy and hopes of reunion. These cases challenge a blanket
interpretation that faith or affection serves only to avoid responsibility.
They do not establish the opposite blanket claim of authentic remorse either.

### Answer to the focused question
In these selected cases, forgiveness language helps articulate several relational
positions: seeking acceptance after acknowledged harm, maintaining kinship
without recorded forgiveness, urging another to forgive, granting forgiveness
from a position of injury, or addressing different harms to different audiences.
These positions can coexist with self-reproach, faith, attachment or dispute.
They should not be ranked as a scale of sincerity.

A useful interpretive conclusion is that **a statement can attempt relational
repair without establishing that repair has occurred**. The direction, object
and terms of forgiveness clarify that attempt. This conclusion concerns the
reviewed texts and aligns with an existing literature; it is not a causal model,
a population estimate or a demonstration of a previously unstudied phenomenon.

## Religious care, judicial punishment and policy context

The owner's broader interest concerns how religious care, judicial severity and
retention or abolition of capital punishment affect people under death sentence.
The existing forgiveness comparison is one part of that interest. Three
questions should be kept distinct: how people describe their experience, what
institutional conditions they actually encounter, and what changing those
conditions would cause. Current last statements directly support the first;
the other two require additional evidence.

### Religious language and experienced care
Religious expression is not a record of how much pastoral support a person
received. A prayer may address God without describing any encounter with a
chaplain. Conversely, thanking a spiritual adviser identifies perceived support
without measuring its duration, quality or psychological effect.

| Case and exact wording | What the statement supports | What it does not establish |
| --- | --- | --- |
| 595: “To my spiritual advisors, I love y'all, thank you.” | Recognition of spiritual advisers and an appreciative relationship | Amount of care, its quality, or its causal effect |
| 138: “He has changed me in the past two months.” | A religiously framed account of personal change | A measured before/after change or the cause of it |
| 1: “My fear is for Allah, God only” | A distinction in the object and meaning of fear | Elimination of every fear through religious support |
| 600: “this is the will of God” | Religious interpretation of the present situation | Agreement with the court's justification or measured emotional relief |

The potential functions discussed by the owner remain useful questions: comfort,
relief, belonging, self-understanding, mercy, an afterlife and moral authority.
They are not presumed benefits in every religious statement. #413's self-reproach,
#600's forgiveness pressure and #508's appeal to divine knowledge show why a
single soothing function would be too narrow. Reader judgments of superiority
or sincerity remain separate from the speaker's explicit claims.

### Punishment severity and perceived justice
A death sentence, the experienced conditions of confinement, and the perceived
fairness of a trial are different dimensions. Calling a trial unfair does not
measure its legal fairness, just as saying that a penalty is deserved does not
measure fear or remorse. Statements can nevertheless show how those dimensions
are interpreted and connected by the speaker.

| Cases | Contrast in the already discussed texts | Psychological-expression question |
| --- | --- | --- |
| 407 and 11 | Willingness to bear a penalty while criticizing its consequences, versus an explicit statement of desert | How is responsibility connected to the meaning of punishment? |
| 219 and 583 | Continued evidence/appeal claims and perceived procedural injustice | How are grievance and a wish to remain heard expressed near execution? |
| 138 and 508 | Changed-self and accident accounts alongside criticism or qualified responsibility | How does a speaker explain the relation between present identity and punishment? |
| 461 and 595 | Family address within different responsibility and forgiveness positions | How are threatened separation and continuing family identity expressed? |

These comparisons concern narratives of punishment. They do not show that a
harsher sentence causes defiance, that a fairer procedure causes remorse, or
that one individual has experienced more psychological harm than another.
The current eight-category labels contain no validated measure of judicial
severity, psychiatric symptoms or receipt of religious care.

### Retention, abolition and reform: a separate empirical extension
The current corpus contains published statements of people who were executed
in Texas. It has no group observed under an abolished death-penalty regime and
no outcome trajectory for people whose sentences were commuted. Dividing these
statements into decades would not create that missing policy comparison.
Absence of a person's statement is not evidence of a particular psychological
response to policy.

A future policy-effects study would need a precisely defined change, actual
exposure to it, a justified comparison and a defined outcome. For example:

| Proposed question | Evidence needed beyond this corpus |
| --- | --- |
| Does access to spiritual care affect distress or perceived support? | Actual contact/access records, timing, repeated outcomes and a design addressing who receives care |
| How does a sentence being commuted or execution suspended relate to hope, fear or future orientation? | Comparable material from affected and unaffected people, dated before/after the change; other simultaneous changes considered |
| How does abolishing death sentences change the experience of people already sentenced? | The specific legal treatment of existing sentences, affected population, comparison jurisdictions or periods, and comparable outcomes |
| How do changes in execution procedures affect public last statements? | Verified policy timing and implementation plus consistent recording practices and a defensible comparison |

One policy question should be selected at a time. Do not assume that repeal,
suspension, commutation and procedural reform are the same exposure. Nor should
all people eligible for a study be restricted after the fact to those eventually
executed: that would omit people whose outcome the policy may have changed.
These are prospective design requirements; no policy-effect analysis or new
sample has been undertaken here.

### Research decision
Continue the present study as an analysis of expressed experience: how religious
meaning, relationships and perceived punishment are connected in the reviewed
statements. Preserve forgiveness as a focused comparison within that study,
not its exclusive subject. Record new questions about support and policy as an
explicit extension rather than attributing effects to the existing texts.

The next evidence task is a feasibility check for one institutional contrast,
not another round of labels for the same 20 statements. Before collecting data,
establish that both exposed and comparison groups have comparable material
and that the proposed outcome is observable. If that is not feasible, the
contextual reading remains the appropriate result for this dataset.

## Feasibility check for an institutional extension

Checked 8 November 2026. This check assesses available source structure, not
psychological outcomes. It prioritizes a bounded religious-accommodation context
rather than claiming an abolition or commutation effect from executed-only data.

### Documented milestones
- **21 April 2021:** the revised TDCJ procedure is described in the Fifth
  Circuit record as allowing an adviser in the execution chamber (printed p. 5):
  [official court record](https://www.govinfo.gov/content/pkg/USCOURTS-ca5-21-70004/pdf/USCOURTS-ca5-21-70004-0.pdf).
- **24 March 2022:** *Ramirez v. Collier* addressed restrictions on religious
  touch and audible prayer. The Court found likely success on the statutory
  claim at the preliminary-relief stage:
  [Supreme Court opinion](https://www.supremecourt.gov/opinions/21pdf/21-5592_feah.pdf).

These dates do not establish individual receipt of care or universal compliance
from that day. Adviser presence, permitted activity and actual provision must
be distinguished. They are milestones for a source-availability check, not a
completed legal history or a treatment assignment.

### Saved corpus availability
The dates were fixed from those documents before counting the saved corpus.
Every inventory and candidate record is included in one calendar group; no
keywords or emotional results were used to select a window.

| Calendar group | Inventory records | Candidate statements |
| --- | ---: | ---: |
| Before 21 April 2021 | 570 | 450 |
| 21 April 2021–23 March 2022 | 3 | 2 |
| On/after 24 March 2022 | 30 | 28 |
| Total | 603 | 480 |

The saved snapshot ends on 7 October 2026. The groups describe material available
in this snapshot; they are not counts of people known to receive or not receive
religious care. The intermediate interval is especially sparse. Earlier records
also span very different periods and should not be treated as one uniform
no-care control group.

Reproduce with `python src/check_institutional_feasibility.py`. The
[availability result](../reports/institutional_feasibility_v1.json) records input
hashes, milestone sources and all group IDs. The script checks unique IDs and
matching inventory/candidate dates. No statement or label is changed.

### Comparison of the two possible routes
| Route | What is available in this check | Missing evidence | Decision |
| --- | --- | --- | --- |
| Spiritual accommodation around execution | Dated official procedural/court records and existing final statements | Actual request, approval and care for each person; comparable emotional outcomes | Prioritize a contextual documentary study; do not estimate a care effect yet |
| Execution stay or sentence commutation | Public court/procedural records can identify particular decisions | Comparable personal material before/after and for people not ultimately executed | Requires a new source design; not supported by the current snapshot alone |
| Retention versus abolition | The current corpus documents executed people in Texas | Affected population under abolition and comparable observations/outcomes | Do not use the current corpus as an abolition experiment |

The [current TDCJ scheduled-executions page](https://www.tdcj.texas.gov/death_row/scheduled_executions.html)
was checked as a potential source. It lists scheduled dates, not a complete
historical series of personal psychological outcomes. Its contents can change;
it is not used to alter the frozen execution inventory or to create a historical
comparison group.

### Concrete next study and evidence threshold
The feasible next question is contextual: **How do documented arrangements for
spiritual support relate to the ways individuals describe support, faith and
approaching death?** This sits within the overall psychological-expression
question. The present check does not yet answer it.

Begin with a small documentary case feasibility check, keeping the existing
20-case work as background rather than repeatedly recoding it. Before analyzing
any new person's experience, require:
1. a dated primary record distinguishing the requested accommodation from the
   decision or rule;
2. a source establishing what was actually provided, or an explicit unknown;
3. that person's attributable statement about the significance of support,
   with its date and context retained;
4. a clear separation of the person's words, legal argument and third-party
   interpretation.

A lawyer's assertion is not automatically a direct psychological self-report.
A legal entitlement is not evidence of uptake or effectiveness. If those sources
are missing, describe the institutional issue and mark individual experience
unknown; do not substitute a before/after word-count comparison.

A causal policy study is deferred unless individual exposure, comparable outcomes
and a credible comparison become available. The 28 later candidate statements
are enough to show some material exists, not enough to establish that design.
This is a bounded next-source task, not a request for another broad owner-labeling
round or a claim that a new study has already been completed.

## Documentary extension: John Henry Ramirez (#576)

### Selection and source chain
This is a purposively selected institutional-context case, outside the completed
20-case reading set. Selection followed the availability check: a named Supreme
Court case could potentially connect a request, actual accommodation and an
attributable account of its significance. It is not a representative additional
sample or a search for a favorable psychological outcome. Sources were checked
on November 8, 2026; the underlying events occurred in 2021–2022.

| Evidence | Dated source and location | What it establishes |
| --- | --- | --- |
| Request and judicial decision | Supreme Court, *Ramirez v. Collier*, March 24, 2022, majority opinion, Parts I and III–IV; [official opinion](https://www.supremecourt.gov/opinions/21pdf/21-5592_feah.pdf) | Ramirez requested audible prayer and pastoral touch; Texas restricted them. The Court found likely success on the RLUIPA claim and entitlement to preliminary relief on the circumstances addressed. This is a legal record, not a psychological outcome measure. |
| Anticipated personal significance | Ken Camp, Baptist Standard, October 3, 2022, reporting a May 25 interview at Polunsky; [article](https://baptiststandard.com/news/texas/corpus-christi-pastor-plans-to-pray-in-death-chamber/) | Ramirez attributed spiritual significance to Moore's presence, prayer and touch, and described an affectionate bond with him. These are Ramirez's statements as reported by an interviewer, before execution. |
| Actual provision | Juan A. Lozano, Associated Press, October 5, 2022, updated 8:35 p.m., republished by Click2Houston; [report](https://www.click2houston.com/news/national/2022/10/05/texas-inmate-who-fought-prayer-touch-rules-to-be-executed/) | The report describes Moore placing his hand on Ramirez's chest, praying, and Ramirez responding to the prayer. This supports occurrence of accommodation; it does not measure its subjective effectiveness. |
| Final public expression | TDCJ, October 5, 2022; [official statement](https://www.tdcj.texas.gov/death_row/dr_info/ramirezjohnlast.html), also frozen candidate corpus #576 | Ramirez addresses Castro's family, expresses remorse, hopes for their comfort, expresses love to his own circle and closes with readiness. The archived statement is a bounded transcription, not a complete record of the execution. |

The court's opinion is used for the legal history rather than treating the
plaintiff's pleadings as independently verified personal experience. The interview
and execution report are journalism, with their respective attribution and
observational limits. The judicial decision predates the execution; the fact that
accommodation was provided is established separately by the execution report.

### Reading the evidence together
In the reported May interview, Ramirez said: “He's my brother. I've grown to love
him.” He also described wanting Moore's touch and prayer during the transition to
death. This supports a reading of support as both a religious practice and a
relationship with a particular trusted person. It does not establish how much
fear he felt, whether the relationship changed his mental health, or that everyone
would experience this practice in the same way.

His final statement begins with the victim's family and an attempted communication
through a victim-advocacy program. He acknowledges the limits of what he could
say or do for them, expresses regret and remorse, and hopes they find comfort.
Here, comfort is wished for the listeners; it is not his own report of feeling
comforted. The statement then turns to love for his wife, son, friends and others,
including Dana, before closing: “I am ready Warden.” The closing permits proceeding
in context; it does not by itself establish serenity, approval of the sentence,
or absence of fear. Neither the family's reconciliation nor their relief can be
inferred from his wishes.

The frozen statement contains no explicit reference to God, prayer or heaven.
Nevertheless, the independent source chain documents a request for religious
support, his anticipation of its significance, and reported provision at execution.
The execution report also includes a response to prayer absent from the official
last-statement transcription. These sources cover different boundaries of the
event; their difference need not be a transcription error.

**Case-level result:** the content of a final statement and the circumstances of
spiritual support are distinct evidence. In this case, a reading confined to
religious words in the final statement would miss documented religious practice
and the expressed importance of a pastoral relationship. Conversely, pastoral
presence does not establish that religion produced his remorse, readiness or
emotional relief. This observation concerns this case and source boundary; it is
not an estimated frequency of such omissions across the corpus.

### What remains open
There is no comparable before/after psychological assessment, no untreated
comparison, and no direct self-report after the accommodation whose effect is at
issue. This case therefore supports an account of anticipated meaning and actual
arrangements, not a causal conclusion about comfort. It also cannot adjudicate
abolition versus retention, deterrence or government costs.

The next bounded task is a contrasting documentary case selected for its ability
to challenge this account: for example, requested support denied or modified,
with attributable personal material. An absence of religious words is not a
selection rule for absence of faith or support. Record any missing provision or
personal-experience evidence as unknown. Before adding a new case, check whether
it contributes a different institutional arrangement rather than merely another
illustration of comfort. No new coding round is needed for the present result.


## Contrasting institutional record: Patrick Henry Murphy (2019)

### Why examine this record
Murphy was selected after the Ramirez case to test whether desired spiritual
support can be treated as a uniform package of presence, prayer and touch. This
is an institutional and preference contrast, not a second completed psychological
case. It is outside the frozen executed-person corpus: a local search found no
Murphy record in either the 603-row inventory or the 480-row candidate corpus.
That absence establishes only the boundary of these frozen files, not his current
legal or vital status. The events examined here are limited to 2019.

### Evidence and attribution
The March 28, 2019 petition and its appendices on the Supreme Court docket include
counsel's February 28 request and the agency's March 5 response. Counsel sought
a Buddhist adviser's presence and also requested avoidance of touch at death,
explaining Murphy's religious preference. The agency excluded outside clergy
from the chamber while offering other arrangements and agreeing that a chaplain
need not touch him. These are documented requests and responses, not proof of
what occurred in an execution.

- [Petition and appendices](https://www.supremecourt.gov/DocketPDF/18/18-8615/94533/20190328130707260_murphy-sct-prohibit-FINAL.20190328.pdf): Appendix F, February 28 correspondence; Appendix G, March 5 response (also reproduced in Appendix H). The account of Murphy's preference is mediated by counsel, not a direct interview or psychological assessment.
- [Supreme Court order](https://www.supremecourt.gov/opinions/18pdf/18a985_1a72.pdf), March 28, 2019, opening order: the Court stayed execution subject to the stated condition concerning a Buddhist adviser's presence. Justice Kavanaugh's accompanying explanation is a concurrence, not the Court's full merits opinion.
- [Fifth Circuit majority opinion](https://law.justia.com/cases/federal/appellate-courts/ca5/19-70020/19-70020-2019-11-12.html), November 12, 2019, Parts II–III, pp. 3–9: after Texas barred all advisers from the chamber, the dispute also concerned unequal faith-specific access in the pre-execution holding area. The court declined to vacate the stay. Its discussion separates chamber access from earlier access; it does not measure distress.

Sources checked November 8, 2026. The March and November stays concern their
respective scheduled executions. Neither supplies an observed execution without
the requested support. Do not label Murphy an untreated executed control.

### What the contrast changes
| Question | Ramirez | Murphy's 2019 record |
| --- | --- | --- |
| Desired contact | Pastoral touch sought, with a directly attributed interview about its significance | Counsel conveyed a preference against touch at death |
| Desired presence | Particular pastor's presence, prayer and touch | Buddhist adviser's presence; faith-specific practice described in litigation |
| Actual execution arrangement | Prayer and touch reported at October 2022 execution | Scheduled executions stayed; no corresponding executed-event observation in these sources |
| Personal experience evidence | Reported May 2022 interview and official final statement | Counsel-mediated preference; no direct personal account analyzed here |
| Defensible comparison | Meaning anticipated and accommodation reportedly delivered | Requested support differed; institutional access was contested |

**Interpretive implication:** spiritual support should be understood in terms of
fit with the person's stated preferences and religious practice, not a scale on
which more contact necessarily means more comfort. This is an interpretation of
two documentary records, not a demonstrated psychological mechanism or a claim
that all members of either religion share these preferences.

For the broader psychological-expression study, this redirects attention toward
what a person seeks from religion: a trusted relationship, a particular practice,
a way to approach death, or another purpose. It does not establish whether either
person was less afraid, more reconciled or more accepting because of support.

### Evidence gap and next step
A published interview with Murphy has been located ([Keri Blakinger, November 11,
2019](https://www.chron.com/local/behind-the-walls-podcast/article/LISTEN-Yoga-Buddha-and-death-row-An-interview-14824834.php)),
but its audio has not been listened to or transcribed in this study. The page
summary is not substituted for his words. Consequently, the earlier threshold
for analyzing personal experience has not yet been met for this contrast.

The next source task is to obtain and check that attributable interview, keeping
its pre-execution context. If unavailable, retain this as an institutional
boundary case and leave personal experience unknown. Do not enlarge the sample
or train a model to fill that gap. The existing 20-case expression analysis and
Ramirez case remain the completed interpretive material; this contrast adds a
specific question about preference-sensitive support.


## Current result and next research decision
The exploratory project now includes a corpus preparation trail, earlier topic
analysis, 20 discussed reading memos, a full-text literature comparison, a reproducible summary of the 50 frozen
development records and this focused six-case analysis. The narrower question has an initial answer supported
by the reviewed material. No further owner labeling is required to produce this
version of the report.

The supplied Smith (2019) full text now confirms direct prior coverage of
forgiveness direction, religious warnings and the forgiveness/reconciliation
distinction. The account above is a contextual elaboration, not the first
statement of these distinctions. Smith's examples also contain wording matching
our #413 and #433 passages; these are overlapping textual material, not an
independent validation set. A stronger publication claim needs a justified
extension beyond the current development cases. Before selecting anything
new, state what a further case could change: for example, whether a forgiveness
appeal clearly accepts the listener's refusal, or whether explicit reconciliation
is reported. Such examples must not be assumed to exist, and a one-sided public
statement still cannot verify the other person's experience.

For now, retain the case-comparison result and its psychological-expression
question. Do not substitute a classifier or add model complexity to compensate
for an unestablished literature gap.
