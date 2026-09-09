# Supported links, scope-limited answer

E-0259 through E-0262. The first candidate adds two source-supported SUPPORTS
links to existing observations, preserves every old record and reproduces exactly.
Independent review is complete: the answer remains PARTIAL because its evidence
does not return the source's RC2 scope. No new thirty-question score is claimed.
Human ratification remains pending. No Core or manuscript change.

## Returned evidence

CQ-T5-01 asks which volatile-content and earthquake-depth observations support
the degassing mechanism. Before the amendment, the answer returns the qualified
hypothesis and a modelled saturation-depth support path. After it, the same
frozen query also returns these existing observation fields through new paths:

| Source record | Returned fields | New connection |
| --- | --- | --- |
| observation:abstract-primary-co2 | Approximately 0.4 to 3.0 wt% CO2 in primary melts; DERIVED; subject melt:primary-unspecified | SUPPORTS claim:co2-degassing |
| observation:abstract-deep-depth | Deep earthquake depth 10 to 20 km; MEASURED; subject ridge:mar | SUPPORTS claim:co2-degassing |

The target still says the authors prefer CO2 degassing from ascending melt as
an explanation of deep RC2 microseismicity. Its HYPOTHESISED and PREFERRED fields
are unchanged. The older approximately 25 km saturation result stays a separate
MODELLED path. It is not converted to a measured earthquake depth.

The new paths return observations, not just a hypothesis restatement. That is
a concrete improvement. Their scope is still broad: the earthquake observation
names the ridge; the melt subject says primary melts without a site. An incoming
SUPPORTS edge to an RC2 hypothesis does not assign RC2 to its source observation.

## Source and provenance checks

The producer authored four assertions. The public trace binds each new relation's
source endpoint, SUPPORTS predicate and target endpoint to them. The source
endpoint assertions and shared argument context point to page:1:block:001;
the target points to page:5:block:002. That abstract contains both observations
and the authors' proposed degassing explanation. The latter block identifies
the preferred RC2 hypothesis. The independent reviewer checked all eight
returned record identities and four composite row witnesses against the full
selected reading. All are SUPPORTED for what they assert. No unsupported new
connection or record regression was found. That is not certification of all
162 graph records or of the scientific hypothesis's truth.

The history retains three separate captures: the original observations,
the earlier model-result link, and this new two-link amendment. New links use
argument:evidence record/assertion IDs and a fresh argument-01 capture/plan/KCS
namespace. No old artifact or record identity is reused.

The source's qualification at page:5:block:007 remains important: it reports no
earthquakes below 20 km beneath RC2 and suggests a temperature explanation.
That qualification is not a returned field of the old 25 km model row. Do not
describe the three paths as numerical agreement or independent causal proof.
The proposed argument is source-attributed; its truth is not established by
structural admission.

## Mechanical result

| Check | Before | After |
| --- | --- | --- |
| Graph records | 160 | 162; every old record unchanged |
| Relations | 21 | 23 |
| Ledger events | 20 | 26; exact old prefix preserved |
| Target answer | Two rows, one path | Four rows, three paths; all old rows preserved |
| Changed query objects | None | CQ-T5-01 only; 29 unchanged |

All old record-history metadata is preserved. Public reopen reproduces the
accepted graph and receipt. Query guards record no file, network or embedding
access. A separate execution with identical protocol time reproduces all
thirteen output files byte for byte. This proves deterministic execution of
this proposal, not regeneration of the model's proposal.

## Condition and limits

One fresh Sol/ultra producer received the source, complete fixed ontology,
current graph, retained captures, CQ-T5-01 and prospective completion criteria.
All 97 declared input frames were observed in tool outputs before authoring.
It did not receive expected values, suggested endpoints, query code, earlier
grades or rationale. One candidate, no returned diagnostic or semantic coaching.

This is TASK_DIRECTED_ARGUMENT_COMPLETION. It is not question-blind acquisition,
a matched question-visibility experiment, semantic re-entry or a new model
ranking. It demonstrates that existing accepted observations can become
reachable through a preservation-checked amendment without altering them.
Why initial acquisition omitted the links remains unproven. No new Core
capability defect is established by this execution.

## Independent coverage assessment

The same prospective definitions were supplied to producer and reviewer. The
reviewer interprets their scope-preservation requirement using the full article's
RC2 restriction and its contrast with neighboring subsections. This remains a
model-assisted judgment for human ratification, not a compiler refusal or an
automated exact-match score.

| Required semantic | Before | After |
| --- | --- | --- |
| Proposed mechanism and hypothesis status | Present | Present, unchanged |
| Distinct supporting evidence record | Present, model result | Present, model plus two observations |
| Geochemical evidence with its scope and status | Unreached | Quantity and derived status returned; site scope incomplete |
| Earthquake-depth evidence with its scope and status | Unreached | Depth and observed status returned; site scope incomplete |
| Explicit paths for both evidence roles | Absent | Present, both supported |

The review therefore finds two of five criteria fully satisfied before and
three after, PARTIAL in both cases. New quantities and paths are real content
gains even though the overall label is unchanged. No earlier grades are replaced
or mixed into this assessment. The review does not independently rerun admission;
its record/query closure checks are separate from our ledger reproduction.

The 27-material packet excludes producer rationale and historical grades. Its
fresh gpt-6-astra/xhigh reviewer initially hit a usage limit. Luis's instruction
to resume restarted the same reviewer on the same packet and model, without
substantive feedback. The earlier failed launch remains recorded. The completed
review is scoped Markdown, not a complete validator-certified v3 review.

## What this isolates, and the next bounded test

The remaining failure is not missing scalar data or a broken SUPPORTS mechanism.
Two separate representation choices are visible:

1. The new links select broad abstract summaries. Existing RC2-specific depth
   and primary-melt estimates remain unlinked to this hypothesis. Their distinct
   subjects are already stored; no new values or ontology are needed to inspect
   them. We have not tested why the producer selected the broader records.
2. Relation rows use answers.py's `row_without_subject` for their endpoints.
   They preserve a subject ID but do not expand its properties. Entity rows
   already have a one-hop subject expansion. The RC2 primary-melt label lives
   in its subject's tags, so selecting a more specific endpoint alone does not
   prove that the current relation projection will expose its scope adequately.

A regression test retains these exact distinctions. It checks that a hypothesis's
subject is not substituted for evidence scope, that the specific observations
are presently unreturned, and that existing entity-row expansion exposes their
stored RC2 labels. Expanding the two selected broad subjects cannot manufacture
RC2: those subjects do not contain it.

The next proposed sequence is a query-only, scope-preserving relation projection
with the current graph as control, then a separately frozen source-grounded
amendment linking suitable existing scoped evidence. Keep both effects separate
and preserve every accepted record. Review qualifications again; do not promise
full coverage merely from changing endpoints. At E-0262 neither change had
been applied or dispatched. No Core capability request was established.

Follow-up, E-0263 through E-0265: the first step is now implemented in TDD and
tested in a separately frozen query-only comparison. Endpoint context is
displayed and traced; records and paths are unchanged. The broad subjects still
do not supply RC2. See [projection fix](RELATION-SCOPE-RESULTS.md). The later
scope-specific link amendment is not dispatched, and this review is unchanged.

## Exact evidence

Private root: private/paper-v4-answer-demonstration/sol-argument-01.
evidence/attempt-01 and evidence/reproduction-01 are the exact execution copies.
review-01/review.md contains the completed independent assessment. Its digest
is sha256:f2b03bf1c91520c859a47acbb0a2ec91e0783f7ea902e29b5273c2e7f50d77c7.
review-launch-01.json and review-resume-01.json retain both dispatch boundaries
outside the frozen packet.

Core: 160878cf14c0d27b11a440e26688708e9b7a7e2b.
Reading: sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17.
Ontology: sha256:49f0a4d3568740ffb8138d4841015f98adb31fc9865a45d8319641eb2270b6a5.
Ledger head: sha256:dda19b0b4f908fd93199dba310db7a976a302abf331ac462f006229c474fb7e0.
Replay receipt: sha256:6bc621091ae4918c2079fae7a9a611058fc25fe5c2c29af321e821fadfa9232e.
Query result: sha256:774668ad478e357e00a329718ad6f04c66fdc9598dc313ccee14d2953eaaec8e.
Query implementations and reader remain digest-frozen in manifest.json.
