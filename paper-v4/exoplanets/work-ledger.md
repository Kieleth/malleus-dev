# Exoplanet work ledger

Append-only working notes for [experiment-plan.md](experiment-plan.md).
Local EXO identifiers avoid the shared paper ledger's concurrent numbering.
Facts, decisions and recommendations are distinguished. No run is selected by
an observation or a passing mechanical check.

## EXO-001, 2026-09-14: domain selected; plan prepared

Author instruction: "perfect, exoplanets it is, lets prepare a plan for this".
Decision: exoplanets replaces the other brainstormed candidates for this front.
Authorization: prepare a plan. No execution or Core mutation is inferred.

Read current paper-v4/AGENTS.md, the September 14 paper handover, the master
plan's current directive and paper framing, and NEXT-RUN-CHECKS.md. Shared main
is dirty and contains concurrent PDF-repair work. The master currently identifies
version 1.5.42. This is context, not an exoplanet runtime pin. Do not move or
overwrite the other front's files, results or authorization.

Verified research facts: NASA distinguishes coherent reference-specific
Planetary Systems rows from composite rows that can mix incompatible estimates.
TESS exposes observation products and their documentation. Astronomy already has
the IVOA Provenance Data Model. Direct sources are linked in the plan. No
particular system, paper pair, raw-data analysis or historical correction has
been verified for this experiment yet.

Proposed plan 0.1: one planetary system; two studies; reference-specific rows;
one connected observation product; initial acceptance; two consumers; one later
source import and explicit interpretation decision; unchanged-reader comparison.
Separate ontology usefulness, population faithfulness, reconstruction and use.
The tentative calculation is density, conditional on appropriate source values.

Important distinction: the planet need not physically change. What may change is
our accepted estimate or analytical choice. A later publication can add an
alternative without superseding the older scientific claim. Import order is
not observation time or a historical community-knowledge timeline.

Scope safeguards: no shared master/ledger/manuscript edits, no Core change or
rebind, no model launch, no source downloads, no commit or push. Only the two
new exoplanet planning documents are authored by this front in this turn.
No software tests are claimed for a documentation-only plan.

Next proposed work: compare at most three real systems and present one supported
recommendation plus alternatives to Luis. Do not freeze or run the case merely
because this plan exists.

## EXO-002, 2026-09-14: source comparison and recommendation

Author instruction: "continue", following the proposed case-selection step.
Authorization interpreted narrowly: research candidates and recommend a case.
Plan advances to 0.2; no runtime or scientific acceptance decision is added.

Compared LHS 1140 b, TOI-561 b and K2-18 b. Recommendation: LHS 1140 b, using
Lillo-Box 2020 and Cadieux 2024. The separate reference columns are accessible
in NASA's overview; paper text supplies method and interpretation context.
case-selection.md records values, source links, alternatives and remaining checks.
These are investigator-read sources, not a model capture or evaluation result.

Preparation findings: bind a specific joint fit, not an abstract's different
mass; preserve a prose/table uncertainty discrepancy; treat reprocessed TESS
data as versioned products; distinguish journal and preprint dates. One spectrum
collection can yield different estimates under different analyses. A source
import is not automatically scientific supersession or Semantic Re-entry.

Limits: exact MAST product bytes and source-reading locators are not frozen.
Directory retrieval failed through the web tool; publisher HTML also refused
access, while arXiv full text was accessible. No conclusion about data absence
follows. An attempted K2-18 arXiv identifier resolved to an unrelated paper and
was discarded; the correct 1810.04731 was then found by exact-title search.
Packet preparation must mechanically verify identifier/title/author/version
agreement, with a mismatch test before any capture. No such code is claimed yet.

Documentation: an initial multi-file patch failed its ledger context check.
Read-back confirmed no files changed; corrected context was then used. Research
artifacts and links are inspected after writing, not assumed from a tool call.

No Core request exists at this boundary. No source download, model launch,
software test run, source-population authoring, shared paper edit, commit, push
or Core rebind. The marine-PDF front's master independently reached 1.5.43;
its changes are not this front's authority. Next requires Luis's case selection.

## EXO-003, 2026-09-14: LHS 1140 b approved; partial source packet retained

Author instruction: "ok, go", accepting LHS 1140 b and packet preparation.
Plan advances to 0.3. No execution approval, Core coordinate or selected reading
is inferred. Only this exoplanet directory and its ignored private source folder
were written. The shared paper, Core and Git refs remain untouched by this work.

Retained exact arXiv v1 and v2 PDFs through browser downloads, plus NASA's
overview CSV downloaded from its Source-row button. Manifest records bytes and
digests. PDF page counts, first-page identifiers, titles/authors and joint-fit
table labels were checked. Rendered both tables and visually inspected them.
The older PDF uses Table B.3 on page 21, not the HTML rendering's Table 5 label.
The later table is D1 on page 24. Corrected current case-selection prose while
preserving this account of the earlier coordinate mismatch.

TDD: five tests authored first. RED collection failed with absent implementation.
GREEN source_packet.py verifies exact bytes, paper identity/table coordinates,
and CSV reference/unit labels, duplicates, shape and unmodified string values.
Five tests passed, including real retained artifacts. No scientific compatibility
validator, selected full reading or source-population adapter is claimed.

The full pypdf 6.16.2 inspection emitted form-XObject content-skipping warnings.
This trial is not approved as the model reading. Poppler 26.03.0 layout extracts
and table renders are diagnostic artifacts, not a replacement selected silently.
The PDF skill required visual inspection; the spreadsheet skill guided raw-cell,
reference, unit and missing-value preservation. No workbook was created.

MAST portal resolved the exact TIC/Sector 3 observation ID. Product bytes and
processing version are still missing. The bulk script and direct product route
did not produce local files. Browser direct downloads returned
ERR_BLOCKED_BY_CLIENT; Chrome is unavailable. NASA's full PS table is visible,
but neither its export action nor direct TAP request yielded raw PS bytes.
The retained overview CSV is not relabelled as PS. It contains later references,
so it is investigator-only until properly sourced stage subsets are prepared.

Acquisition errors are tool/access limits, not Core defects or missing archive
data. No speculative Core request. A shell lookup also encountered an absent
requirements glob; inspected the actual pyproject.toml instead. No installation
or source rewrite followed. All missing inputs remain explicit in the manifest
and block readiness rather than being replaced with investigator transcriptions.

Next: obtain exact raw archive and observation bytes; settle the complete reading
and stage separation; then verify Core/method before seeking execution approval.

## EXO-004, 2026-09-14: remaining sources retained; format defect isolated

Author instruction: "continue". Milestone 2 preparation only. Plan stays 0.3;
there is no new author decision, producer launch, Core pin or manuscript result.

The Chrome browser-extension surface remains unavailable, but selecting the
native Chrome app through the computer-use tool worked. Opened task-only tabs,
saved NASA's full PS response and its column definitions, downloaded the exact
MAST light-curve product, and closed those tabs. No browser setting, security
warning, shell network client or dependency installation was involved. An initial
clipboard operation timed out after filling the address bar; inspection showed
the correct address, so Return completed that navigation without re-pasting.
The download UI reported an incorrect one-byte size for saved text pages; local
byte counts and parsing, not that label, established the retained artifact size.

Exact identities live in source-manifest.json. The FITS header identifies target
92226327, Sector 3, spoc-5.0.20-20201120, data release 42, 19,692 rows and 20
fields. Observation dates are in 2018, file creation is 2020-11-26. Target,
sector and pipeline version match Cadieux section II.3, but equality to the
authors' working bytes is not established. The file postdates the selected
older PDF and is a later-stage candidate, never that paper's asserted input.
No transit refit or per-sample population was performed.

The first CSV inspection used Python's permissive reader and returned seven
rows of 355 fields. This was insufficient evidence of correct parsing. The
new strict test refused the first data row. RCA found unescaped double quotes
in HTML display fields such as class="supersubNumber", at byte offset 6360
for the first inspected occurrence. Did not change bytes, escape values by
hand or weaken the reader. Retained this original CSV as a rejected source.

Used NASA's documented VOTable output for the identical all-column query. Its
original XML parses, declares QUERY_STATUS=OK and contains seven rows, 355
fields and explicit quantity/uncertainty units. Empty cells remain None in the
read result, not zero; decimal text is not converted to floating point. Current
archive metadata and mixed references still require a separately checked
initial/later projection. There is no historical snapshot claim.

TDD sequence: first four new checks failed, three absent verifiers and the old
three-source count. Initial implementation exposed the real CSV syntax defect.
The corrective RED required the VOTable reader and rejection manifest. GREEN
removed the PS CSV reader completely, added strict XML shape/status/unit/reference
checks, and retained a hard test that the rejected CSV still refuses. There is
no automatic format fallback. FITS identity checks compare exact header cards
at selected offsets and refuse missing, duplicate or changed identities. They
are not a new general FITS parser or checksum verifier. Nine tests pass, including
the six retained source identities and the malformed seventh source. Formatting
was applied only to this front's two Python files.

Reading diagnosis: reran pypdf 6.16.2 page by page on all 53 PDF pages. Only
Lillo-Box page 6 logged the 5,000-form invocation warning. Its Figure 6 plot
labels are absent and several negative Figure 5 axis values have square glyphs.
Captions and surrounding prose remain in the output. Read the library's
_extract_text__xform guard; it returns empty text for later form invocations
after the limit. This explains the warning mechanism without proving every
specific glyph defect has that same cause. The other 52 warning-free pages
are not thereby certified complete. Rendered page 6 and compared Poppler's
reading-order extraction, which includes the plot labels but still has an
awkward equation layout. Inspection files stay private; no selected reader or
producer locators were silently substituted.

The PDF skill required visual comparison. The spreadsheet skill kept source
values, units and missing cells intact. No spreadsheet or PDF was authored.
Source preparation now has six checked candidate/corroborating files and one
rejected source, not a launched experiment. Next: finish the clean reading and
mechanically isolated stage packets, then public Core/method approval. Core,
shared paper files, other runs, Git refs, commits and pushes remain untouched.

## EXO-005, 2026-09-14: protocol read-through and adoption boundaries

Author instruction: "Read malleus dev and protocol and follow/journal all this
so we can use it for the paper". Applied as a scoped read-through and standing
discipline for the exoplanet front. No new experiment, Core pin, model dispatch
or scientific selection decision. Plan remains 0.3. Corrected its stale closing
paragraph, which still called the already approved case an open decision, and
restored the missing 0.3 changelog entry from EXO-003. No past ledger entry changed.

Read completely: `.claude/skills/malleus-dev/SKILL.md`, its Unix design doctrine,
`.claude/skills/malleus-acolyte/SKILL.md`, and `docs/IMPLEMENTATION_STATUS.md`,
`PRINCIPLES.md`, `ONTOLOGY_PROTOCOL.md`, `KNOWLEDGE_GRAPH_PROTOCOL.md`,
`ASSENT_PROTOCOL.md`, and `ADOPTION_GUIDE.md`. Also read paper standing orders,
the current governing directive and September 14 handover to preserve the
parallel marine-repair ownership. The development skill's CC-002 MCP preflight
does not apply: no CC-002 acquisition or implementation was attempted.

### What the protocol requires us to distinguish

| Boundary | Protocol role | Evidence in this front now |
| --- | --- | --- |
| Explicit contracts, identified inputs/outputs, fail-closed handling, no semantic guessing, separate structural/epistemic/authorization claims | PROTOCOL_INVARIANT | Requirements applied to preparation; no end-to-end exoplanet conformance claim. |
| Typed graph, semantic history/replay, selected domain-history semantics | OPTIONAL_PROFILE | Needed for the proposed result; exact runtime/profile selection remains open. Assent and actions are not silently added. |
| Public Python compiler, document adapter, structural admission and replay | REFERENCE_IMPLEMENTATION | Present in the inspected checkout; three existing locator tests rerun. No exoplanet history executed. |
| Synthetic invalid-input cases in the source checker | CONFORMANCE_FIXTURE | Bounded checks of our preparation contract, not scientific observations or Core protocol certification. |
| Astronomy ontology, reading, source adapters, compatible-solution rule, analysis choice and evaluation | ADOPTER_CHOICE | Ours to define and assess. None becomes a general Core rule because this case needs it. |

The developer skill changes our working procedure, not the experiment's claim:
before code, record claim, discriminator, reuse and exclusions; then a failing
mechanical test. The lowest protocol profile relevant to the intended before/after
result is semantic history/replay over the selected typed graph. Omitting it
would give up accepted-history reconstruction and provenance, not invalidate a
standalone structurally checked graph. Our Markdown journal is development
evidence, never that semantic history.

### Findings from code and exact artifacts

1. **Choose the meaning of change before ontology construction.**
   `src/malleus/profiles/source-assertion.json` declares one capture batch,
   semantic unit COMPOSITION and CAPTURE_IMPORT_ORDER. Assertion and domain times
   remain retained evidence. `state-version.json` instead declares DOMAIN_TIME
   and successive state versions. The document adapter emits an ORDER_ONLY batch
   tied to the capture ID. Neither silently supplies our scientific rule for
   selecting a mass-and-radius pair. Retain both publications; changing our
   analytical selection is distinct from correcting what a publication said.
   The exact mixed-source history and selection representation remain unchosen.
   Presence of per-plan profile references is not proof that arbitrary profile
   combinations are compatible in one history.

2. **Source identity is not table-cell verification.**
   `src/malleus/_contract_pipeline/population.py` restricts its row resolver to
   `text/csv` and `application/x-ndjson`. It checks zero-based `row:N:field`
   locators, with an optional array index. Other media types bypass that resolver;
   an existing test explicitly preserves free-text locators for unstructured
   sources. Our VOTable XML and FITS are outside this row check. This is a known
   boundary to close in our integration, not an established Core defect.
   The document adapter separately checks capture assertions against supplied
   reading blocks, not the PDF's visual content. No generic FITS/XML citation
   checker or document-reading completeness check was found on this path.

   Recommendation, not an implemented choice: retain native bytes and create an
   identified mechanical table projection in a supported row format, preserving
   lexical numbers, nulls, units, reference identity and parent cell locations.
   The selected subset must be explicit, not called a lossless copy of omitted
   fields. Alternatively define an adopter-owned native-locator check. Compare
   these before implementation. A mechanical projection is not permission for
   the evaluator to author semantic population. Tests must refuse broken parent
   mappings, changed numbers/units, invented missing values and later-stage leaks.
   These tests are requirements, not completed work. A Core request requires a
   specific missing public capability and reproducer, not a request to own astronomy.

3. **Readiness and semantic coverage are separate.**
   The acolyte requires coverage of the whole selected retained reading, even
   when the engineering implementation is lean. Cross-block context can support
   a relationship; both labels need not occur in one sentence. Conversely,
   co-occurrence supplies no relationship. The adapter's FULLY_FORMALIZED count
   means supplied targets have no declared gap, not that all source meaning is
   captured. Keep the four questions in the plan separate and assess the sources
   against the graph. One accepted history used by a calculation and an LLM
   tests reuse, not cross-language conformance or interchangeable implementations.

4. **Current documentation is not one frozen runtime description.**
   Some KG/Assent passages still describe the compiler path as private or future;
   current `malleus.compiler` exports the public compilation, population,
   structural history and trace functions. Implementation status says seven
   adapter arguments; the callable has seven required keywords plus optional
   `contract_view`, which the current acolyte explicitly supplies as the eighth.
   Omitting that view omits the adapter's contract-derived evaluative-slot check.
   Do not reuse an older seven-argument recipe. This is recorded documentation
   drift, not a reason to edit Core from the paper task.

   The skill's capability probe finds the current interfaces but the environment
   is editable: `malleus.compiler.__file__` resolves into this checkout. Installed
   distribution metadata says 0.13.3 while pyproject and status say 0.14.0.
   Therefore the probe establishes available imports, not a clean 0.14.0 package
   or a reproducible experiment. No installation was changed. Freeze and verify
   exact source/environment identity before launch, including a mismatch guard.

### Verification and scope

Inspected HEAD: `6118257d53844f205f8dedd1a1ea4c84c9b70595`. The tracked skill,
protocol and implementation files inspected here have no local diff; the shared
worktree has unrelated changes. This is a diagnostic coordinate, not an exoplanet
Core pin, clean-checkout audit or package gate. No living shared document was
added to the experiment's identity manifest.

Ran the nine existing exoplanet source tests and three existing Core locator
tests: 12 passed. The latter check aggregated unresolved-locator refusal with
unchanged ledger bytes, resolvable CSV/JSONL locations, and deliberately unchecked
free-text locations. They do not test XML/FITS admission, scientific agreement,
mixed-profile history, or this experiment's two consumers. Existing test nodes:
`test_unresolvable_locators_refuse_together_before_any_write`,
`test_resolvable_locators_admit_over_csv_and_jsonl`, and
`test_locators_over_an_unstructured_source_stay_free_text`, all in
`tests/contract_compiler/pareto/test_governed_population.py`. Used the repository
`.venv/bin/python`, disabled bytecode and pytest cache. One guessed structural
test filename did not exist; located the real files with `rg --files` before
selecting any tests. No missing test was counted as a pass or silently skipped.

Scoped self-check under `protocol_role_is_explicit` and
`optional_profile_stays_optional`: no astronomy rule, source fixture, default
profile, public API or journal entry has acquired base-protocol authority. No
schema changed, so no root-ontology rite or semantic-completeness seal is claimed.
Only this front's plan, source-preparation note and journal were edited. No Core,
shared paper, accepted history, source bytes, Python code, Git refs, commit or
push changed. Next remains source reading/binding and the explicit history/method
decision, followed by execution approval. No new paper result exists yet.

Final read-back checked local Markdown links, whitespace, unique ordered EXO
entries and corrected authorization wording. The source verifier still reports
six verified files, PDFs of 22 and 31 pages, and `launch_ready: false`.

## EXO-006, 2026-09-14: source-binding and history proposal preparation

Author instruction: "go". Continue milestone 2 preparation. No profile or
scientific selection policy is adopted, no source projection is selected by
implication, and no model execution is authorized. Re-read the development and
adopter skills. Current shared HEAD is 18015352e2eb5bffbb58125c95de40eba0f4c992;
its intervening commits concern Shop. Inspected compiler and skill paths are
unchanged from EXO-005. This is still not an experiment pin.

Before the diagnostic: requirement is to determine whether the public API can
retain different explicit per-batch profiles in one structural history, replace
only an identified choice record, and reconstruct both the earlier and later
states. Smallest discriminator: three synthetic batches, one source statement,
one initial choice, one replacement choice. Reuse public compiler, population,
structural admission, reopen and trace APIs. Exclude astronomy data, PDF capture,
scientific selection rules, new profiles, custom protocol machines, new Core
code, model production and a general mixed-profile compatibility claim.

This is a diagnostic conformance fixture for the existing reference
implementation, not the model-authored experiment. Its hand-authored neutral
schema and rows must never become producer inputs or evaluator population.
Add a retained test to this owned directory; a test of existing behavior is not
reported as a new RED/GREEN implementation. The chosen experiment still needs
an explicit meaning-of-change decision and source-grounded assessment.

Diagnostic outcome: `test_history_feasibility.py` passes using only public
runtime imports, an explicit neutral schema and three synthetic source rows.
Source-assertion and state-version profile identities remain independently
traceable in one default structural history. The statement survives unchanged;
choice A is historical and choice B is current. All three exact saved prefixes
reopen to their recorded graph and receipt. Wrong supplied profile identities
refuse before writes. No live history was truncated; prefix copies are temporary
test artifacts. Domain time for the two choices is NONE_STATED, not the invented
fixture transaction time. This proves neither general profile compatibility nor
the document-adapter-to-history composition, which was not exercised.

The first diagnostic reached admission and reopen but failed because I called
nonexistent `get_entity` in the assertions. Inspected the public graph surface,
changed the assertions to its actual `get_node`, and reran the complete test.
This was a probe-author error, not a Core failure or a valid TDD RED against
production. The retained executable test now checks the real interface.

Important unresolved interpretation: the source-assertion profile declares a
partial-import capture origin; state-version declares genesis over an empty
graph. The test proves mechanical acceptance of their per-plan references, not
what both declarations mean for one containing history. No per-stream genesis
semantics was found and verified. Do not call a successful composition of bytes
a demonstrated composition of meanings. The existing pure transition-rule
extension also binds one exact history-profile identity, so do not assume it
automatically covers any mixed-profile history. No Core defect is asserted and
no request has been sent.

`preparation-proposal.md` recommends a mechanical VOTable-to-NDJSON projection
with exact parent locations, preserved lexical numbers/nulls/units and explicit
stage subsets. Native sources stay unchanged. The alternative is an adopter
native-locator checker. Source conversion must not create astronomical facts,
select estimates, or supply an answer-shaped ontology. Application choices need
their own identified basis, not attribution to the papers. History selection
remains a decision before production. The development skill's distinction
between structural success and semantic composition is why this issue remains
open despite the passing probe.

An initial documentation patch had an invalid plan context. The tool refused
the whole patch; a read-back confirmed the new proposal file was absent. Applied
the corrected patch against inspected text. No partially written proposal was
treated as complete. Plan stays 0.3; no new author decision is inferred.

Final verification: nine existing source tests plus the new history diagnostic,
10 passed. Changed-file Ruff and formatting checks pass. Documentation read-back
checks local links, whitespace, EXO numbering and the unchanged plan version.
No new library dependency, astronomical record, model run, Core edit, shared
paper edit, source-byte change, commit, push or ref movement by this task.

## EXO-007, 2026-09-14: source conversion and Core clarification approved

Luis says "go" to the source-to-cell conversion with tests and the bounded Core
clarification. Plan advances to 0.4 at this author decision. No model launch,
astronomy population, history-profile choice, runtime rebind or Core modification.
Sent Malleus Core the neutral three-batch reproducer and the origin/genesis scope
question against 18015352e2eb5bffbb58125c95de40eba0f4c992. A response is pending.

Before implementation: this is ADOPTER_CHOICE source preparation, not a new
protocol profile. Requirement: selected XML cells become deterministic NDJSON
rows, retaining lexical values, nulls, FIELD definitions and parent coordinates.
The fixed caller-selected stage must govern both generation and verification;
returned metadata cannot authorize a different stage or extra columns itself.
Smallest discriminator: a synthetic two-study table with a null and an exact
decimal, corruption/selection refusals, then both real selected reference rows.
Reuse the existing strict PS reader, source manifest and Core row convention.
Exclude semantic mapping, facts, calculations, PDF reading, FITS conversion,
new general ingestion machinery, and claims of historical archive snapshots.

Pre-action check: no server call from code; coordination uses the app tool. No
endpoint, installation, missing-value default or existing-reader fallback.
Use stdlib serialization/XML plus the already declared project dependencies.
Pure conversion returns no partial result; generated files publish only as a
complete new directory, never over an existing packet. Tests precede production
changes. A prepared table subset is not yet a complete or approved producer packet.

Implementation and results: added `source_projection.py`, the explicit candidate
`table-selections.json`, and `test_source_projection.py`; reused and tightened
the existing PS XML reader. The first test execution failed at collection because
the converter module did not exist. This is the recorded RED, followed by the
minimum conversion, verification, cell trace and new-directory publication path.
No second permissive parser or new dependency was added.

The old synthetic source fixture lacked a version attribute. The tightened
reader refused it while the real source and new projection cases passed. Updated
that fixture to declare the real source's 1.3 version; added explicit missing
and conflicting version refusals. This narrows the preparation reader to the
declared source surface, not a general VOTable compatibility promise. It also
refuses nested/non-cell elements instead of silently dropping their content.

The public-API diagnostic initially used `record_id` instead of `evidence_id`
inside a plan evidence reference. Core correctly returned
MALFORMED_EVIDENCE_REFERENCE before reaching the intended locator test. Inspected
the actual contract, corrected the test input and retained the wrong-key case
as an explicit refusal assertion with unchanged ledger bytes. This was a
test-author mistake, not a Core regression. The positive test then admitted and
reopened a synthetic source statement with the original XML, projected cells
and conversion description all recoverable. It uses only public Core APIs and
the existing neutral diagnostic ontology. Missing/excluded row locations refuse.

Candidate scope: all 151 selected planet-parameter fields, retaining alternate
units, uncertainty/limit/display fields, not only the candidate calculation's
inputs. Five archive-wide flags/counters and all non-planet fields are excluded.
This explicit candidate requires review with the complete source packet; it is
not a new scientific selection policy. The initial reference maps to original
row 5, later reference to row 3, with 52 and 57 nulls respectively. All 302 cells
match their parent coordinates. Both outputs rebuilt byte-for-byte. Exact paths,
digests, code identities, commands and limits are in `source-packet.md`.

Stage limitation exposed during integration: Core can retain the complete native
XML for audit, but a trace returning it would reveal later-study rows to an early
consumer. The stage-specific rows and derivation metadata exclude later rows;
that does not establish the complete model-delivery boundary. The full XML and
two-stage configuration remain investigator-only. This access design must be
settled before execution, not papered over by passing table tests.

The skills kept the claim at ADOPTER_CHOICE source preparation: a checked cell
location is not faithful interpretation, and structural acceptance is not a
chosen history semantics. Core's origin/genesis clarification remains pending.
No Core change request arose from the locator/replay test.

Editing checks caught a misplaced block of test assertions during a patch and
an unmatched documentation context. Corrected the assertions before execution;
the scoped Ruff/test checks enforce valid names and the complete write-failure
and no-overwrite assertions. The documentation patch was refused atomically;
read-back confirmed unchanged text before a smaller exact-context patch. Neither
editing error is reported as a product failure or meaningful TDD RED.

Verification: 53 local preparation tests passed, including 43 projection cases,
the nine source checks and the earlier history diagnostic. Ruff and formatting
checks pass on changed Python files. This does not run or replace the shared
paper gate. No astronomical ontology/population, model execution, FITS conversion,
selected PDF reading, Core edit/rebind, shared-paper edit, commit, push or ref
movement by this task. Plan remains 0.4; no further decision is inferred.

## EXO-008, 2026-09-14: PDF reading investigation and Core reply

Luis says "Next" after the recommendation to resolve PDF reading while Core
handles the profile question. This authorizes the next source-preparation step,
not a model launch, Core edit/rebind, selected history policy or manuscript claim.
Plan advances to 0.5 at this decision. Apply the PDF, malleus-dev and acolyte
skills. No PDF is edited, re-exported, published or hand-transcribed.

Pre-action classification: ADOPTER_CHOICE source-reading preparation. Claim:
detect material reading defects before treating extractor output as the source
for capture. Smallest discriminator: the already identified plot labels and
negative signs on the earlier PDF's page 6, both parameter tables, plus complete
page accounting. Reuse retained sources, their identity checker, installed
extractors and existing renders. Exclude OCR, scientific reconstruction, manual
text repairs, another PDF engine, astronomy population, evaluation answers and
full-reading approval from a small set of markers. A known incomplete output
must not pass just because its extractor emitted no warning.

Pre-action checks: no server interaction in code, no endpoints, no installation,
no missing-input defaults or implicit extraction fallback. Diagnostic outputs
remain private. Runtime/tool identities and reproducible commands must accompany
any candidate; no clean-environment execution claim follows from local tools.
Tests precede the new mechanical reading audit. Scope stays in exoplanets and
its ignored private workspace.

Core's explicit authorized handoff has arrived. The inspected coordinate is
18015352e2eb5bffbb58125c95de40eba0f4c992, tree
04b6ee7b6a0417e5eb7b31d381625c456bfabe3a. Its full read-only memo is
`/private/tmp/malleus-required-lists.wqymkE/HISTORY-PROFILE-SCOPE.md`.
Per-change profile identity is retained, but mixed origin/genesis semantics are
not defined or enforced. No typed stream or second genesis exists implicitly.
The single-profile COMPOSITION pattern used by connected Shop is a smaller
existing-runtime option, not astronomy policy. The document adapter deliberately
emits SOURCE_ASSERTION_PROFILE; relabeling its plan is not a supported shortcut.
Core did not rerun our test or change runtime behavior for this inquiry.
The mixed probe remains mechanically admitted/replayable, semantic compatibility
unestablished. Profile composition or an explicit producer-contract change now
requires an author decision. This does not block independent PDF investigation.

Reading outcome: ran pypdf 6.16.2 plain/layout and Poppler 26.03.0 default/layout
over all 53 pages. Retained all 212 page texts and diagnostics, with 14 visual
source probes. Reviewed the earlier page 6/Table B.3 and later Table D1 and
equation pages 19, 22, 23, 25 against full renders. This is not a complete visual
audit of both papers. No extractor was selected and no output was hand-repaired.

The concrete causes are different. The earlier page 6 contains 14,396 Form
XObject invocations (11 distinct forms); pypdf's plain traversal guard stops at
5,000. Layout also drops tested labels without a warning on that page, but we
did not prove that its internal cause is the same. Poppler recovers the labels
and negative ticks but loses the solar-unit symbol in Table B.3. Its source
txsy font lacks a ToUnicode map and explicit Encoding; pypdf resolves the symbol.
The later PDF's CMEX10 map is incomplete for mathematical delimiters. All four
conditions expose control characters on pages 19, 22, 23 and 25. Presence of a
ToUnicode object alone is therefore not evidence of a complete mapping.

Before implementation, the 17 initial reading-audit tests failed because the
module did not exist. Implemented explicit page/source accounting, diagnostic
and glyph screens, private visual probes, and a result that can never authorize
launch. Real output exposed an overstatement in our first classifier: an
unfamiliar private-use math glyph was labeled as a defect without assessment.
Added a failing test, then separated REVIEW_REQUIRED from missing probes,
extractor warnings and control characters. Retained both investigation versions.
All 212 page texts and warnings repeat identically; only audit interpretation
and code identity changed. There was no extraction improvement between reports.

Added a separate RED/GREEN test for complete-or-absent diagnostic publication
and refusal to overwrite. The final retained comparison is
`reading-investigation-v2.json`, SHA-256
4a05200d6057932c8b1e7554a5a28de3ac3656676faa24ecac6859dff6d62eef.
Exact versions, probes, source identities and code hashes are bound inside it.
The Poppler executable hash is not its dynamic-library closure; clean-runtime
packaging remains unresolved, not implied by local reproduction. No dependency
was installed. PDFium/pdfplumber were existing bundled spot-check tools only.

`READING-FINDINGS.md` holds the results, positive table controls, root causes,
limits and proposed next cut. Recommendation, not authorization: constrain the
first experiment to supported prose plus exact archive parameter rows, preserve
unreadable regions as explicit limits and original images for review, and avoid
building a new PDF engine. Any necessary additional evidence surface or narrowed
claim needs Luis's decision. One compatible history profile/producer contract
also remains a decision; do not relabel the current adapter output. No new Core
implementation request was sent.

Verification: 74 preparation tests pass, including 21 reading tests; existing
source/projection/history diagnostics still pass. Changed-file Ruff/format and
private-artifact identity checks pass. No Core/shared-paper/full-package gate,
new graph, model run, accepted reading, manuscript edit, commit or ref movement.
Plan remains 0.5 after this outcome. The skills affected the boundary directly:
visual evidence revealed losses that hashes and extractor success cannot prove
away, and the adopter skill prevents turning a finished diagnostic into a
complete source capture.

## EXO-009, 2026-09-14: causal PDF-reading review, no repair authorized

Luis challenged "Keep damaged equations and figure regions explicitly unresolved,
without hand-repairing text or inventing facts" with "RCA this, is weird".
Authorization: diagnose. No source change, runtime patch, acquisition change,
scope reduction, model launch or Core implementation request follows.

Read the PDF skill completely, the development skill completely, current paper
standing instructions and the exoplanet plan/findings. PDF skill required visual
checks, not confidence from extracted strings. The development skill kept this
at the adopter source-reading boundary; no new protocol semantics were needed.
The standing paper instructions explicitly reject blanket figure/table exclusion.
Main remains at 18015352e2eb5bffbb58125c95de40eba0f4c992 with unrelated concurrent
changes. Ownership stays in this exoplanet directory and private source workspace.

Causal evidence, detailed in READING-RCA.md:

- Plain pypdf's 5,000-form cap is consumed by repeated non-text plotting markers
  in the first figure. Raising only the in-process cap to 20,000 restores the
  second figure's `Peak periods (d)` and `24.7`, but not the minus signs. The
  module constant was restored, no dependency file was edited. This is a probe,
  not an approved way to remove a resource limit in production.
- Layout mode has no `Do` traversal into the figures. Presenting the second
  figure's original content as an isolated in-memory page restores its labels
  with that same layout reader. A page without warnings can omit whole forms.
- The first figure's explicit font encoding maps code 0 to `/minus`. Pypdf's
  built-in Type1 fallback overrides it with `.notdef`, producing `□`. Preventing
  only that override in memory restores five minus signs and changes nothing
  else in the first figure's text.
- Later CMEX9/CMEX10 maps omit used delimiters and radicals, but their embedded
  font programs name them correctly and pypdf already understands those names.
  Temporarily removing only the two incomplete maps from the in-memory reader
  restores 30 delimiters and three square roots across pages 19, 22, 23, 24, 25
  and 27. The other 25 page strings remain identical. No source PDF was written,
  no candidate reading was saved, and no global mapping-deletion fix is approved.
- Our literal marker check falsely calls `Normalized ﬂux` absent because it
  expects `Normalized flux`. Conversely, the wrong ordinary letter `p` in place
  of `√` is not flagged. Page 24 had no audit issue despite a corrupted radical
  in its noise-test formula below Table D1. Passing table probes was not proof
  of whole-page faithfulness. The audit code and frozen report remain unchanged.

The precise Poppler-internal reason for dropping the source's `/circledot` solar
symbol remains untraced. Its loss is reproduced, while the embedded glyph name,
visible symbol and pypdf output demonstrate that the source information exists.
Recovering glyphs does not by itself recover fraction/exponent scope or figure
relationships. No full-reading approval or version-regression claim is made.

Correction to our interpretation, not an author scope decision: "damaged" was
too broad and the narrowing recommendation was premature. Withdraw that
recommendation. Preserve source scope and investigate a bounded reader repair.
READING-RCA.md records proposed mechanical regression cases for traversal,
font precedence, partial mappings, ligature comparison and silent substitutions.
They are not implemented fixes or new passing tests. No new runtime is selected.
Plan stays at 0.5. Added forward pointers, preserved prior chronology and outputs.

Verification after journaling: 74 existing exoplanet preparation tests pass in
2.71 seconds. This does not establish a fix for the newly diagnosed checker or
extractor problems. Both source PDF hashes, the retained v2 report hash and the
two audit implementation hashes still match their previous identities. No code
file, installed dependency, Core path, shared paper file, Git ref or commit was
changed by this RCA. Only exoplanet diagnosis/status documents were updated.

## EXO-010, 2026-09-15: OCR ownership and original mixed-source purpose reviewed

Luis asks whether the reading work belongs in malleus-ocr, and whether the
original multi-document idea needs this depth of PDF work. Authorization is
review and discussion, not a reader fix, source replacement, scope change,
model launch or cross-task instruction. Plan remains 0.5.

Read the development skill, Unix design doctrine, full implementation status
and principles; inspected OCR exports, bundle types, verifier, CLI, decisions
and corpus documentation. Current checkout remains
18015352e2eb5bffbb58125c95de40eba0f4c992. The shipped package is an AUDIT_ONLY
evidence verifier, not an extraction/recognition engine. It records sources,
renderings, regions, attempts, candidate readings, selections and corrections;
it does not run OCR, repair font mappings or establish semantic fidelity.
Its region representation is raster-based, so a direct text-layer/native-source
adapter must be checked for honest fit rather than given fictitious rasters.

Existing design F1, dated September 5, already assigns text-layer reconstruction
to the OCR extraction/reconciliation front and requires both reading candidates
and their reconciliation evidence to remain retained. This is design direction,
not a delivered reconciler. The current corpus uses controlled readings, not a
production recognition engine. Current CLI conformance reproduced all seven
packaged expectations. That result tests verification, not these scientific PDFs.

Read the task "Study OCR vs Malleus Core Changes" and inspected its standalone
proof README plus exact HEAD 5769c34a381f8fb6d2dafcf8db1c2e5831740dff. It proves
ordered failed-attempt/retry imports against candidate Core b34c706, retaining
both attempts through replay. No production OCR engine or recognition accuracy
is claimed. It is outside this checkout and was not rerun or modified here.
Some OCR prose still says Core cannot populate Events or record reviews;
current implementation status supersedes those historical Core limitations.
OCR's own review integration remains absent. Do not turn stale prose into a
new Core capability request.

Revisited EXO-001/002, case-selection and the experiment plan. The intended
demonstration is a small mixed-source, changing interpretation before a context-
overflow experiment: one scientific object, two published solutions, exact
archive rows, source-supported methods/qualifications, a calculation and an LLM
explanation using one accepted representation, then a justified analytical
update with the older result reproducible. It is not a test of universal PDF
conversion, transit refitting or complete formalization of every equation.
LHS 1140 b was selected over TOI-561 b and K2-18 b for a clearer focal-object
before/after interpretation, explicit numerical solutions and observing links.

Primary sources checked again: NASA's PS/PSCompPars construction documentation,
Lillo-Box's arXiv record and Cadieux v2's record/full HTML. The selected studies
disagree over the preferred composition interpretation; the later source keeps
gas-envelope and water-rich alternatives. NASA PS rows preserve one published
solution per row; its composite table explicitly trades internal consistency
for completeness. Archive rows are structured representations of the studies,
not an independent scientific replication of them. Merely looking up or
recomputing two densities would not establish the Malleus contribution.

Both exact selected editions have reachable official arXiv HTML:
https://arxiv.org/html/2010.06928v1 and
https://arxiv.org/html/2310.15490v2. Their records also offer TeX source links.
This establishes an alternative source-reading route to assess, not complete
HTML/PDF equivalence, frozen HTML bytes, a selected replacement or a completed
delivery packet. Edition-specific table labels and locators must remain separate.

Recommendation for Luis, not adopted: keep the scientific case and test its
original semantic purpose; assess native structured rows plus a faithful full
document representation before funding a general PDF repair. Retain access to
figures, tables, equations and their context. Do not strip damaged regions out
of the reading or feed investigator answers to a producer. Faithfulness of
evidence used is mandatory; converting every appendix equation into executable
mathematics and independently reproducing the astrophysical analysis are not.
Raw-observation analysis stays deferred as already planned. The observation
product may remain a linked source rather than a new numerical analysis task.

If a reusable reading repair is selected, propose it to the OCR/acquisition
owner with the exact generic reproducer. Core owns any shared runtime/profile
change. A new OCR verifier rule is justified only by a demonstrated missing
contract; known pypdf defects do not by themselves require Core semantics.
No task was messaged or resumed and no implementation was dispatched.

## EXO-011, 2026-09-15: native-source feasibility checked against the PDFs

Luis accepted assessing the native-source-first route while retaining PDFs as
the verification reference. This authorizes the assessment, not a completed
reading selection, source-scope reduction or model launch. Plan remains 0.5.

Used the PDF skill for rendered-page comparison and the Malleus development
skill to keep acquisition findings separate from protocol claims. Inspected both
versioned arXiv HTML pages through web and browser tools. Complete HTML inventories
found 17/18 figure containers, 5/8 table containers and 790/563 MathML elements;
all mathematical elements had TeX annotations and neither page had duplicate IDs.
Targeted comparisons are recorded in [NATIVE-READING-ASSESSMENT.md](NATIVE-READING-ASSESSMENT.md).

Both principal result tables preserve their compared values, units and structure.
Native images preserve earlier Figures 5/6 and their previously lost labels/signs.
Later C1/C2 equations and the noise-test radical preserve their mathematical scope.
The central scientific qualifications remain present. These positive checks
support the route, not whole-document fidelity or a producer delivery claim.

Found two new HTML-generated `CLOSE` operators at a math-to-text boundary in
later IV.2 and E.1. PDF pages 7/26 have the closing parenthesis without this word.
Both TeX annotations end before the parenthesis supplied by the next text node.
Two additional explicit conversion errors contain `\tablenocomments`. Recorded
these separately from the malformed earlier uncertainty and later mass/radius
unit inconsistency that are present in the original PDFs too. No hand repair.
Listed mechanical regression requirements before any reader implementation;
no new tests or fix are claimed during this inspection-only step.

All 43 observed scientific assets downloaded through the browser's page-asset
capability and were copied unchanged into the ignored native-html-inspection-v1
directory. All 30 SVGs parsed and their href targets passed the documented narrow
closure check. The whole-page export method was unsupported by the selected
browser, so no complete HTML byte freeze is claimed. Read-only browser inspection
continued through supported methods; no direct-network workaround was used.

Original PDF hashes remain unchanged. This front added the assessment, private
inspection assets/renders and this journal entry only. No source selection,
Core mutation, cross-session message, model launch, commit or ref change occurred.

The existing exoplanet preparation suite still passes: 74 tests in 2.76 seconds.
It does not validate the newly inspected HTML or establish a repaired reading.

## EXO-012, 2026-09-15: author pauses exoplanets and reopens the larger-domain question

Luis: "lets park exoplanets for a second, document all and progress, and probe
another dataset". The immediate research question is now persistent, reusable
domain knowledge beyond one context window, alongside the separately owned
Small Shop, single-PDF and robotics demonstrations. Dataset choice is reopened;
no replacement is selected and no experiment is launched by this instruction.

Plan advances to 0.6 for this author decision. Retain all source bytes,
projections, private inspection assets, causal findings and tests. EXO-011 is
the last completed reading assessment. The 74-test result remains the last
observed preparation result, not a new rerun or an astronomy result. Reading
selection, history-profile selection and model capture remain incomplete.

The sources were selected to demonstrate connected published measurements and
changing interpretations, not to test universal PDF conversion. Acquisition
work has displaced that purpose. This motivates the pause; it does not show
that Malleus failed or that the scientific case is unusable.

The next investigation will separate exceeding a context window from maintaining
faithful, reusable and revisable knowledge. It will revisit prior art and compare
source-native datasets before requesting another author choice. Retrieval,
ordinary databases and existing graph-memory systems are comparison candidates,
not capabilities the corpus size alone eliminates. No Core change, cross-session
dispatch, shared manuscript edit, commit or branch/ref movement accompanies
this pause.

The completed bounded investigation is
[Persistent domain knowledge beyond one context window](../domain-scale/RESEARCH-OPTIONS.md).
It compares published memory benchmarks, a versioned technical corpus and native
scientific literature. The separate ignored Recon notebook validated and built
68 structural research records; this is not benchmark execution. No replacement
dataset, raw-instance freeze or model launch was selected.
