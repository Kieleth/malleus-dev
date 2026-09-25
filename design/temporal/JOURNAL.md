# Temporal Core journal

Append observations and decisions. Correct prior conclusions explicitly rather
than editing history. Milestone state is summarized in README.md.

## TEMP-001: authorization and isolation, 2026-09-24

Luis approved a KISS Core temporal workstream: corrections, transitions and
two-coordinate historical queries first; no automatic recomputation. Calculation
integration remains a downstream requirement. TDD, milestones and retained
progress evidence are required.

Created branch `codex/core-temporal` at `ebff70f72dc4cd67b2f910b88575e558a2824728`
in `.claude/worktrees/core-temporal`. No active main or UMR bytes were copied or
changed. The initial sandbox denied writing the Git ref; the same worktree
creation succeeded through the permission mechanism. Main has unrelated active
changes to `knowledge.py` and `revision.py`; integration is not authorized here.

Read the maintainer skill and its Unix doctrine, capability declaration,
principles and implementation status. Current temporal support has two paths:
Assent supports precision-aware temporal views; compiler history has a simpler
valid-time shape and explicit record supersession. The computational experiment
separates reported and assumed premises using ordinary domain records. It does
not establish that generic computation-context semantics belong in temporal Core.

## TEMP-002: pre-implementation specification

Wrote six synthetic situations with independent expected answers. They separate
world transition, report correction, late evidence, future applicability,
uncertain transition and calculation premises. No extractor or paid model runs.

T2's contract is an exact historical knowledge-position read. The existing
`graph_at_change` already preserves old graph snapshots, so T2 must not claim to
invent historical graphs. The missing surface is a complete prefix replay with
the contract, evidence, record history and checks available at that position,
while binding and validating the containing ledger as well.

Pre-action checklist: no server interaction or endpoint; no dependency added;
required coordinates cannot default; no authoritative mechanism replaced; the
existing fold is reused; every refusal class receives a test. This step changes
no runtime, package version, shared roadmap, paper or governed overseer document.

## TEMP-003: baseline and historical-read RED

Five baseline controls passed on untouched Core: old graph preservation,
declared transition bounds, same-period correction refusal, unstated-time
preservation and existing precision-aware boundary behavior (the catalogue
guard is included in the five tests). Sources and record values are authored;
this is no extraction or interpretation result.

The first test invocation exposed a test setup error: the revision API requires
`revision=` as a keyword. Corrected the call and reran before accepting RED.
The revision test now reaches the missing read API after a real recorded revision.

Confirmed RED: **18 failed, 5 passed**, all 18 failures state that Core has no
public complete historical-position read. Command, from the isolated worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider --tb=line tests/contract_compiler/pareto/test_temporal_history.py tests/contract_compiler/pareto/test_historical_position.py
```

Pre-GREEN SHA-256 values:

- Baseline tests: `22ddcfaf3ce9a641cfca57f772c4434d3e62ab459e256d17ebfcba865c979d5b`.
- Historical-read tests: `dd768179be4953cba08ff324518d64a764e682f59811150351567ba4ced55104`.
- Authored situations: `807aa037f9fce05dafd84f080da3ab7f7d2d526ab77cbab53bde158169c7f755`.

Same-period correction fails at Core's check stage with ledger bytes unchanged
relative to the attempted admission. The separately retained source remains.
That is a measured missing correction contract, not permission to weaken the
existing transition ordering guard.

## TEMP-004: historical read implementation and review

Added `KnowledgeChangeHistory.replay_at` through the existing public facade.
It reads one ledger snapshot, verifies both checkpoint pairs, validates the
containing history, then folds the selected prefix with the existing executor.
The method supplies no date default, domain-time filtering or alternate writer.
The maintained reader and historical reader now share the existing completeness
check rather than duplicating it.

The first GREEN selector included the original 23 tests plus all maintained
projection tests: **36 passed**. This includes the existing supplier episode and
partial-shipment revision/recovery controls, not only the price fixture.

Additional checks cover one containing-ledger read, mandatory coordinates,
equal transaction timestamps, future-effective state and correction of a retired
period. The final two new test files have **30 passing tests**. A separate run
of history, contract revision, public compiler and capability declaration passed
**120 tests**. An earlier combined run including the existing valid-time and
unstated-time suites passed **67 tests**; selectors overlap and these counts
must not be added as independent tests.

Review exposed a boundary to preserve: the ledger envelope does not identify
generic filesystem append batches. Complete knowledge admissions and finite
transactions are checked, but arbitrary invented prefixes cannot be certified
as previously persisted snapshots. Documented use therefore selects checkpoints
retained from completed calls. No new batch-marker grammar was introduced.

Ruff initially rejected imported pytest fixture names being shadowed by test
arguments. Reused the fixtures through an explicit module binding instead of
disabling the check. Ruff and formatting checks then passed.

## TEMP-005: documentation governance failure and correction

The first documentation run returned **3 failed, 167 passed**. Root cause:
the new compiler-guide section changed an already governed document without
a forward digest revision. The existing strict HTML/doctest tests caught it.
No test or validation condition was weakened.

The first unvalidated ledger draft also used the illegal reference combination
`EVIDENCES` -> `DOCUMENT`. The ledger validator rejected it. Removed that draft
reference, recomputed the draft hash and head, and regenerated the projection.
The repeated documentation failure was the same draft error, not a runtime
regression. Future validation commands in this workstream stop on a failed
ledger check before starting the documentation build.

Branch-local ledger now validates 483 entries, ending at OVR-000483,
`sha256:7cc8f789b170674ec763a233041c2b58453606e4eb78f7c916f55b7debf1f951`.
This is not a reservation of a shared-main sequence number. Reconcile the local
document revision with the owning ledger before integration; another isolated
branch can legitimately have a different successor to OVR-000482.

The maintainer capability declaration, implementation status, compiler guide
and changelog describe only the unreleased historical reader. The package
version and stage remain unchanged: the broader temporal stage is incomplete,
and no distribution or release is being published.

## TEMP-006: final bounded verification

After the forward documentation revision, the combined capability, documentation,
two temporal files and compiler-governance selector passed **337 tests**. This
includes the 30 new temporal tests. Command and plain-language outcomes are in
[RESULTS-01.md](RESULTS-01.md). No failure was suppressed and the governed runtime
and test bytes remain those recorded by the validated branch-local OVR-000483.

T0 through T2 are complete at this local boundary. T3 through T6 remain pending.
The historical reader adds no persisted format, domain-time selector or writer.
Correction of the same period and correction of an already retired period still
refuse, as the baseline tests explicitly demonstrate. No automatic recomputation,
source extraction or paid model execution occurred.

All work is confined to the isolated worktree. No commit, push, main integration,
package build or release has occurred. The current main checkout's active Core
changes were not imported or edited. Integration must reconcile both source
changes and the fork-local governance successor.

## TEMP-007: correction semantics expose a check-scope choice

Reread the full maintainer skill, Unix doctrine, principles, implementation status
and capability declaration. Rechecked compiler and Assent temporal writes before
proposing another primitive. Both paths close a prior period at the replacement
boundary and reject an already superseded target. Neither supplies whole-period
correction merely by exposing a temporal API.

Followed the candidate through actual admission: the Prolog executor receives
one candidate graph, built from current accepted records after retirements. A
correction of an ended period cannot safely reuse that input contract unchanged.
This is a design obligation for new support, not a claim that an existing
supported correction escaped its checks.

Wrote CHECK-SCOPE-02.md and two baseline observations. They instrument the check
request and forward it to the unchanged real executor, including the existing
order fixture's Prolog rule. They are not runtime REDs for an unapproved grammar.
Pre-action checklist: local tests only, no server/endpoint/dependency, no new
runtime or public API, no required-input defaults, no replaced production path.
The first-cut correction policy needs an explicit decision before implementation.

Asked Luis whether to use structural scope first with explicit refusal of custom
domain-rule histories, or to define historical domain-rule checking now. The
former is recommended for KISS but is not selected silently. No code narrows an
existing admission guarantee, and no new correction grammar has been introduced.

The first observation run failed twice in the observer: it called `get_node`
on `CheckRequest.candidate_graph`, following that field's `KnowledgeGraph` type
annotation. The actual value produced by `_check_stage` is a `CandidateSubgraph`.
Inspected staging, corrected the observer to call `overlay()` and added an
explicit actual-type assertion. These are test-setup failures, not temporal REDs.
The mismatched production annotation is a separate recorded cleanup, not silently
changed as part of the temporal design. Real checks had executed; those failed
observer assertions did not establish the claimed inspection results.

Corrected observation run: **32 passed**, including the two new scope controls
and all 30 temporal tests from T2. The real Prolog control executed, not skipped.
Ruff, formatting and diff checks pass. Command from this worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/contract_compiler/pareto/test_temporal_check_scope.py tests/contract_compiler/pareto/test_temporal_history.py tests/contract_compiler/pareto/test_historical_position.py
```

This turn changed only local design/journal documents and added the observation
test file. T2 runtime bytes, its governed revision and existing checks are
unchanged. No commit, integration, new correction implementation or release.
The checks are CONFORMANCE_FIXTURE observations of the REFERENCE_IMPLEMENTATION;
they do not choose the future OPTIONAL_PROFILE's historical admission guarantee.

## TEMP-008: author corrects the graph model; implementation paused

Luis explicitly requires keeping all versions of a value in the KG and selecting
their use by time and context. He requested a pause, bitemporal KG research and
a skill reread. Withdrawn: the structural-only first-cut recommendation from
TEMP-007. It was never an accepted decision or implemented restriction.

Root of the reasoning mistake: treated the existing current-record projection
too much like the whole knowledge representation. The observed checks do receive
that projection, but this implementation fact does not constrain the intended
temporal KG. Existing PRINCIPLES.md already distinguishes accepted temporal
history from a selected view. Retention and applicability must not be conflated.

Reread the complete maintainer, acolyte and Recon skills, Unix doctrine, the
relevant principles and temporal code. Investigated primary bitemporal graph
models, their queries and edge-integrity differences, plus W3C relation-instance
modelling and XTDB's operational semantics. BITEMPORAL-RESEARCH-01.md records
sources, limitations, an authored version table and candidate transfer.

Important new expected control: even a period's end is knowledge with a history.
Learning on 12 May that an earlier price ended then cannot rewrite the view
available on 10 May. Also distinguish stable subject references from exact
premise references; correction cannot rewire an old calculation silently.
No synthetic expected answer is presented as a passed Malleus experiment.

Used Recon's public API for a bounded private literature comparison. Pre-action
check: local ignored research records and design prose only; no server, endpoint,
dependency installation, runtime change, mechanism replacement or model call.
Read its complete contract and ontology before writing. The first atomic batch
refused because I supplied scalar SearchEvent.notes where the schema requires
a list. Corrected the research input, mechanically checked all supplied
multivalued fields against the registry, and asserted the refused batch left
zero events and zero records before retrying. The corrected 16-record batch
validated and exported. This was a research-input error, not a temporal Core bug.

Both source works cover the two coded requirements. That comparison is about
source definitions and proposed requirements, not a claim of implemented Malleus
parity. A publisher correction notice for the Anselma chapter was discovered;
its full text was inaccessible, so exact formal adoption is not supported by
this pass. No performance, source-truth or novelty claim is made.

Updated the local plan and added forward supersession notes to the earlier
drafts. Full-version representation, query semantics and rule scope now precede
the next correction RED. No temporal runtime, tests, skills, checks, package or
Core governance changed. No commit, integration, push or cross-session message.

Research verification: 16 records and 16 events validate; all 14 exports rebuild
byte-for-byte. The T2 runtime SHA-256 remains
`dc1e26104a920516aa6898f8a94139e958a1c81c42da700cff2a3e99ff31d9a5`.
Scoped prose whitespace checks and git diff check pass. No temporal runtime test
suite was rerun during this implementation pause; prior counts remain prior
evidence, not fresh bitemporal results.

## TEMP-009: prepare the bitemporal design checkpoint

Luis asked to get ready for the next stage. Prepared NEXT-STAGE.md and
expected-views-v1.json; linked them from the roadmap and recorded proposed
dependencies in the workstream design graph. No representation or policy was
selected on his behalf. Runtime remains paused.

The packet separates retained versions, selected applicability and exact
consumer premises. Three authored controls cover price correction after a real
transition, a differently shaped scientific report with no stated time, and a
calculation's premise references. The answer key includes ten price selections,
four scientific queries, four prefix-history expectations and seven consumer
obligations. These are proposed expected behaviours, never measured results.

Additional prevention target: returning an old value with its future closure
date still leaks later knowledge. Prefix assertions cover the metadata as well
as the value. Another prevents declaring success merely because full and
incremental replay agree: both must also match independently authored answers.

Reread the maintainer skill, doctrine, principles, current capability declaration
and implementation status. The skill keeps the new semantics OPTIONAL_PROFILE
and requires a rule census before selecting new domain checks. The packet
therefore proposes no Prolog body and does not silently discard required checks.
The exact grammar, policy input scope, refusals and profile remain a design
approval before RED, not details for an implementation to invent.

Pre-action boundary: design prose, authored JSON and proposed design tuples only.
No server/endpoint, dependency, runtime edit, model dispatch, shared-tree edit or
new accepted ledger. Do not confuse the draft JSON with a new Core wire grammar.
Candidate A, explicit addressable versions, is recommended for the first control
but not selected. Candidate B, native temporal properties, remains a comparison.

Preparation verification: JSON parses with duplicate keys refused; identifiers,
evidence/position references, intervals and ten price answers agree with the
authored table. Unknown-time and no-future-metadata expectations are explicit.
The Turtle graph parses and its two proposed stages have no conformance claim.
Local document links, whitespace and git diff checks pass. These checks establish
internal consistency of the review packet, not implemented temporal behaviour.
No Core test suite was rerun. The T2 runtime digest is unchanged from TEMP-008.

## TEMP-010: research the representation choice before asking for approval

Luis said the A/B packet did not provide enough information for an informed
decision and requested research into what each option provides. No approval of
A, B or a combined approach is inferred. Temporal implementation stays paused.

The previous comparison conflated assertion identity, temporal query semantics
and physical representation. An exact version handle need not be a node; an
ordinary version node does not enforce correct temporal selection. Therefore
the next decision should not treat those responsibilities as exclusive choices.

Reread the complete maintainer and Recon skills plus the maintainer's Unix
doctrine. Inspected primary graph literature, official Wikibase model/export
documentation, the W3C n-ary modelling note and XTDB's documented temporal
queries/read resolution. Rechecked local graph query, history application and
Prolog fact-compilation code. No external system was installed or benchmarked.

REPRESENTATION-OPTIONS-01.md records the price example under both options,
comparison axes, evidence limits and the Malleus change surface. Important
distinctions: finer-grained updates do not require native property storage;
full evidence views can coexist with simple selected values; simple values
must not discard relevant qualifiers; producers should not manually maintain
derived history cells. A source assertion remains distinct from the several
applicability accounts reconstructed as evidence arrives.

Recommendation, not decision: an optional Core temporal contract with identified
qualified assertions, Core-owned selection and traceable exact premises, first
projected through ordinary graph records. No new database or independent writer.
A later native property/index implementation would have to preserve the same
observations. Physical replaceability and runtime performance are unproved.
P1 must still specify actual representation, diagnostics and check inputs before
RED. Existing required rules cannot simply receive a historical union or be
dropped. The authored answer key remains unchanged.

Recon retention: appended 19 source/axis/comparison/search/boundary records
through its public failure-atomic batch API. All 35 records and 35 events
validate. All 16 earlier records and their ledger byte prefix are unchanged.
All 13 currently emitted exports reproduce byte-for-byte on a second build.
These are research-instrument checks, not Core bitemporal conformance results.
NOT_ESTABLISHED is scoped to the inspected sections, never a product-wide
absence claim. Relation confidence records coding certainty, not a probability
of architectural success.

Pre-action boundary: local design prose and ignored research artifacts only.
No server request through a shell, endpoint, dependency installation, new
runtime mechanism, semantic test implementation, shared mutation or model call.
No new error was encountered by the research batch; supplied multivalued fields
and duplicate keys/IDs were checked before append, retaining TEMP-008's guard.

No Core, policy, ontology, skill, governance or runtime test changes this turn.
No commit, push, integration or cross-session message. T2 runtime SHA-256 remains
`dc1e26104a920516aa6898f8a94139e958a1c81c42da700cff2a3e99ff31d9a5`.
The Core test suite was not rerun during this research pause. Local research
consistency and link/whitespace checks do not establish temporal implementation.

## TEMP-011: broaden the thought experiments before selecting the architecture

Luis requested worked experiments across the marine PDF, computation, temporal
updates, knowledge maintenance and storage before choosing the future path.
The TEMP-010 recommendation remains a candidate. No backend or temporal policy
was approved. The new G0 to G4 research gates precede runtime implementation.

Reread the maintainer and Recon skills, the full Unix doctrine and the shared
progressive interpretation-review instructions. Reviewed the declared temporal,
revision, check and review mechanisms and the bounded local baseline. Inspected
actual consumer reports and selected retained outputs in the main checkout and
the isolated UMR worktree, without editing either. The manifest identifies 12
inspected files and two exact source blocks; it is not a rebind or a requirement
that those living research documents remain unchanged forever.

GEDANKENEXPERIMENTS-01.md now works through twelve named flows. It separates
source retention, proposal, vocabulary/revision, review/admission, reconstructed
graph, use and reconsideration. Each has required answers, forbidden inference,
storage obligations and evidence limits. The existing computation checkpoints
confirm the sequence: model stored, model selected, externally executed, result
admitted. The existing re-entry coverage confirms its authored five-item review
set, not discovery of all affected arguments.

Two previously unstated requirements surfaced. First, the old valve fixtures
assume persistence: an opening event alone does not justify next-day OPEN.
Their bytes and old baseline evidence are preserved. GE-07 explicitly separates
event-only, rule-supported state and planned-action cases; a future conformance
test must discriminate them before any persistence semantics enter Core. This
is an under-specified expected-behaviour fixture, not a newly observed runtime
failure. Second, the dated product-price account must not be confused with the
order's explicitly selected quote. A date-free quote can support the existing
calculation; a request for applicability on a date has stronger prerequisites.

Other failure cases keep a scientific estimate distinct from its application,
an affected justification distinct from a false conclusion, old/new formula
graphs separate despite shared terms, and withdrawal/cache pruning distinct
from destruction of authoritative evidence. Native temporal values require
account/assertion identity when multiple meanings share the same times and
number. Explicit nodes require qualified selection rather than historical union.

STORAGE-FLOWS-01.md supplies constructive mappings for ordinary graph records,
relational projection, native temporal interfaces and named model/claim graphs.
It explicitly separates finite representability from implemented query semantics,
Core admission, crash safety and performance. No new temporal engine, prototype
selector, policy or storage implementation was written. The proposed next storage
witness must execute actual queries and preserve semantics, not just serialize
opaque blobs or compare counts.

Primary sources inspected: de Kleer's assumption-based TMS, Kowalski/Sergot's
event-calculus introduction/example, PROV-O, RDF dataset semantics and SQLite
identity/reference documentation. They constrain the cases; none is automatically
adopted. Appended 12 records through Recon's public API: 47 total records/events
validate, the earlier 35-record prefix remains unchanged, and all 13 exports
rebuild byte-for-byte. New works are source constraints, not unearned coverage
scores against all temporal requirements.

Fresh execution was deliberately narrow: the five existing marine exact-arithmetic
witness tests passed with pytest configuration isolated via `-c /dev/null`.
They discriminate uncertainty from a physical bound and incompatible depth
references using authored mathematical controls. They do not repair an LLM,
validate new scientific premises or execute the proposed storage designs.

Pre-action scope: research documents and private Recon retention only; no network
from shell, endpoint, installation, paid model, cross-session message, Core or
consumer edit. All 12 file digests and two block digests match the inspected
inputs. Local document links and whitespace checks pass; T2 runtime digest is
unchanged. No full Core or consumer suite was rerun, commit made, branch moved,
integration performed or release claimed.

## TEMP-012: T3 cut, REVISION and TRANSITION kinds and the impact read, 2026-09-24

Built on `codex/core-temporal` from 837908ba under route A (R-07), RED then
GREEN. Specification: `g4/RULINGS.md` R-01 to R-08. Protocol role:
OPTIONAL_PROFILE semantic-history; the impact read is a
REFERENCE_IMPLEMENTATION under it. Histories without the kind field keep their
meaning, so the lowest affected profile omits nothing for them.

Commands, from the worktree:

    export PYTHONPATH=$PWD/src:$PWD
    python -m pytest tests/contract_compiler/pareto/test_temporal_revision.py -q
    python -m pytest design/temporal/g3/test_g3.py design/temporal/g1 -q
    python -m pytest tests/contract_compiler -q
    python -m pytest -q

RED, Core untouched: 19 tests, 17 failed and 2 passed. The 2 passes are
today's behaviour kept as guards: an operation without the kind field writes
the g1-01 K1 and K2 ledger at pinned bytes (sha256 7035505…, 423819 bytes) with
the structural bundle, check contract and state-version profile at pinned
identities; and the R-05 probe, a class-ranged slot naming r1, did not block
superseding r1. 16 failures stopped at the missing `supersession_kind`
constructor argument and 1 at the missing `closings` field, so no RED test
reached Core behaviour. One expectation was corrected after RED: the transitive
impact case missed that relations c1 and c2 name u1 as their source, which the
R-05 definition (relation endpoints, followed backwards) includes.

GREEN: the 19 pass. g3 and g1: 222 passed, so no pinned "today" row in
`g3/expected_today.py` changed, because the G3 driver sends no kind. The
temporal suites (valid time, temporal history, check scope, historical
position, unstated valid time, this file): 90 passed. `tests/contract_compiler`:
1455 passed. Full `pytest -q`: 3793 passed, 3 skipped, 24 failed. All 24 fail on
one cause: OVR-000483 governs `docs/IMPLEMENTATION_STATUS.md`,
`CAPABILITIES.md` and `knowledge.py`, and this cut moves all three. The
validator stops at the first, the status document. 7 are in
`test_contract_compiler_ledger.py`, 14 in `test_contract_compiler_integration.py`
and 3 Sphinx builds in `test_docs.py` whose manifest directive validates the same
ledger. Expected before sealing; not sealed here.

What was built. `KnowledgeOperation.supersession_kind`, persisted only when
declared. `KnowledgeRecordClosing` and `KnowledgeRecordHistory.closings`. A
REVISION of a record a transition closed covers that closed period, inherits
its successor link and never enters the current graph; on g1-01 at K3, r3
covers 1 May to 12 May, followed by r2, and r2 is the only current price. Three
new `KnowledgeChangeRefusalReason` members, appended: `STALE_TARGET`,
`TYPE_CHANGE`, `VALID_TIME_EXTENT`. No code enumerates that enum and no
persisted artifact names its members. A string reason at CHECK,
`CUSTOM_POLICY_HISTORICAL_SCOPE`. `KnowledgeHistoryReplay.version_referrers`.

Choices the rulings did not cover, each open for Luis: an undeclared closing
refuses a revision as `STALE_TARGET`, because it may have been a revision;
closings are recorded only for declared kinds, so undeclared histories compare
equal to before; the impact read descends into inlined values and follows event
participation endpoints; a revision of a closed period refuses under any rule
layer, since R-04 lists that category and rules read only the current graph.

Limits. Two specimens, both synthetic; no second consumer. The impact read uses
the head contract view for every version, sound only while revisions stay
additive. RF-OVERLAP stays unobservable, because an interval end lives in an
adopter slot Core cannot read. A reference to a closed record is admitted
without resolution. Nothing here measures size or speed. Merging needs route C
with route D and regenerated evidence.
