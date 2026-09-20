# BEAM reader comparison: reusable evidence, incomplete meaning

Date: 2026-09-15. Capture 01 unchanged. Two fresh Sol readers, observed low
reasoning effort, one twenty-question batch each, no semantic feedback.

## Result in plain English

The reader with the original conversation recovered important changes that the
graph-only reader missed. It found the later 78% API-integration test coverage,
distinguished it from 65% earlier coverage and 85% broader core-module coverage,
and reported both sides of the contradictory API-key and bug-fix accounts.
The graph reader returned the older 65% and only the positive acquisition/fix
reports. Its caveats about unverified execution did not expose those conflicts.

There are useful graph answers too. It compared the reported 250 ms fetch latency
and 280 ms autocomplete response time, with appropriate comparability limits.
It recovered the intended 1,200-call daily quota from retained wording and
explicitly flagged the conflicting numeric field of 200. Both readers declined
to invent the other two Jira tickets. These are specific observations, not an
accuracy total or proof of a generally adequate representation.

The graph result is weaker than the record count suggests. Of its 62 citations,
55 cite prose in quantity_kind. Thirty-six cite one long recap field,
quantity:beam:2138, across ten questions. Successful answers therefore often use
source prose carried inside measurement records, not composition of precise
typed relationships. Record counts alone would conceal that distinction.

The full graph-plus-retained-evidence workflow was not tested by this reader.
That restriction matters: the research vocabulary permits a claim to omit copied
statement text and retain its locator and digest. The missing detailed meaning
is sometimes available through that evidence path. This experiment deliberately
withheld it to measure graph-only reuse. It cannot establish that normal
evidence-following use fails in the same way.

## Assessment of every question

This is the parent model's source-grounded assessment, not human ratification or
an independent review. Reader status labels are not grades. All answer bytes and
citations remain in the private packets. Numbers in the source column identify
original conversation messages, not inferred dates. Criteria remain unchanged.

| ID and question | Graph reader | Source reader | Assessment and criterion boundary |
| :--- | :--- | :--- | :--- |
| q01, enforced Airbnb rules | Cannot recover individual rules. | Gives attempted indent, semicolon and camelcase settings; separates assistant suggestions from final enforcement. | Source 58, 59, 110. Some settings are present; actual final enforcement is not established. Pre-existing disputed absence criterion. |
| q02, other Jira bugs | Declines to assign unrelated errors to tickets. | Same, identifies only one of three named tickets. | Source 124 supports the partial inventory. Neither reader fabricates the other two. Their agreement does not certify exhaustive semantic absence across all messages. |
| q03, API-key acquisition | Gives the March 10 positive report, omits denial. | Contrasts obtained, never obtained, and later configuration reports. | Source 32, 70, 72. Source reader covers the substantive contradiction; graph answer does not. Neither asks the rubric's literal clarification question. |
| q04, autocomplete fixes | Gives null-check improvement, omits never-fixed account. | Reports both the fix and denial. | Source 88, 124, 132. Graph caveat about remaining errors is not the explicit contradiction. Source covers that contradiction without resolving it as fact; literal clarification question absent. |
| q05, five autocomplete aspects in order | Cannot establish order from opaque record IDs. | Gives five ordered aspects at messages 8, 20, 22, 24, 52. | Those are grounded and ordered, but repeat debounce and omit the rubric's dropdown/error and listener-cleanup items. The question does not specify the five intended aspects. This additional selection ambiguity was noticed after answers, not preflight. No full rubric coverage claim. |
| q06, five error-handling aspects in order | Cannot establish order. | Gives five early aspects, omits later promise-rejection discussion. | Source 6, 10, 14, 18, 28 supports its sequence, not a comprehensive trajectory. Pre-existing disputed rubric orders topics differently from the source. Both the flawed criterion and the source answer's limited coverage remain recorded. |
| q07, starting technologies | Names tools but refuses to infer starting stack. | Gives vanilla JavaScript ES2021, HTML5, CSS3 and the original Axios import. | Source 10, 14. Source answer covers the named stack; graph answer does not recover its starting role. |
| q08, earlier request-flow recommendation | Cannot recover it; supplies clearly labelled new queue/backoff advice. | Recovers rate counters, queue and backoff, plus later jitter/retry advice. | Source 33, 35, 37, 98, 99. Source recovers the main recommendation but omits the rubric's explicit counter-reset intervals and capped delays. New generic advice is not recalled evidence. |
| q09, common API failures | General advice with numeric codes, scoped project examples. | Codes and meanings tied to conversation passages. | Source 28, 29, 74, 75, 98, 130, 173. Both meet the narrow code-inclusion criterion. This does not prove a graph-derived domain inference or validate an API implementation. |
| q10, errors to handle | General advice and reported 401/429/fetch failures. | Broader source-backed categories including malformed data, cancellation and promise handling. | Source 22, 28, 48, 98, 114, 115, 138, 162. Both include numeric codes, the narrow criterion. Advice is not observed implementation. |
| q11, daily quota | Reads 1,200 from prose, flags numeric 200 conflict; qualifies intended settings. | Reports update from 1,000 to 1,200, qualifies provider and key uncertainty. | Source 32, 66, 70. Both recover the requested value. The successful graph answer does not repair the wrong stored number. |
| q12, integration coverage | Returns historical 65%, not latest specifically scoped 78%. | Gives 78%, separates broader 85% and 100% goal. | Source 114, 128, 148. Source covers update. Graph answer is a true historical report but incomplete for the requested latest value. 78% exists numerically in the graph, without its integration-module scope. |
| q13, number of features/concerns | Declines exact count without counting rule. | Offers 20 explicitly grouped categories, not a source total. | Pre-existing disputed Four criterion. No canonical unit. Source reader's single short recap citation does not independently support all twenty category memberships; its grouping is not a benchmark answer. |
| q14, faster fetch or autocomplete | 250 versus 280 ms, difference 30 ms, warns about conditions. | Same, distinguishes later 220 ms overall and 290 ms input-latency metrics. | Source 38, 80, 124, 150. Both cover named-test comparison. Neither establishes a simultaneous current retest. |
| q15, simple caching | Dependency-free Map proposal with optional localStorage, labelled advice. | Similar, plus retained history-size and expiry suggestions. | Source 46, 47, 54, 55, 140, 141. Both align with lightweight preference and criterion. No code was deployed or tested. |
| q16, deployment-step monitoring | Suggests structured workflow logging and GitHub Actions; cannot recover existing setup. | Recovers Actions jobs, step logs, optional artifacts and timestamp requests. | Source 176, 182, 184, 185, 192. Both mention automated workflow tooling. Source's UI inspection is not manual deployment; neither demonstrates a functioning pipeline. |
| q17, project summary | Useful recap, older coverage, misses explicit denials and several milestones. | Wider summary including updates, competing metrics and contradictory release accounts. | Source 10, 42, 114, 124, 128, 148, 186, 195, 196, 198. Source is richer, but neither fully covers the rubric's original modularization/configuration advice and requirements-definition trajectory. No comprehensive-summary pass. |
| q18, autocomplete summary | Parameters and performance, omits cancellation/caching/loading details and explicit denial. | Adds AbortController, debounce adjustment, caching, loading, cleanup and conflicting fix account. | Source 23, 25, 83, 85, 91, 93, 124, 132, 161. Source improves coverage. Neither fully states every rubric detail, including fetching weather for a selected city and conditional-fetching semantics. |
| q19, acquisition to wireframe interval | Refuses to assign March 12 to completed wireframe. | Computes two days between reported dates, conditioned on contradictory acquisition account. | Source 32, 42, 70. Source supports conditional arithmetic, not verified event occurrence. Graph abstention avoids inventing the missing event meaning. |
| q20, scheduling to testing interval | Declines ambiguous event/date assignment. | Gives a conditional 22 days using an assumed April 6 start, then explains conflicting plans and missing scheduling-action date. | Source 0, 50, 51. Pre-existing disputed 21-day criterion. April 6 is an added assumption, not an observed start; correctly labelled conditional but unnecessary. No unique supported duration from either answer. |

## What explains the main failures

### 1. Preserving a number is not preserving what it measures

ratio:beam:2273 retains 0.78, the text 78%, topic TESTING and a link to
proposition:beam:2301. Neither record expresses API-integration coverage or its
relation to the earlier measure. The precise sentence remains in
assertion:beam:2301 at source message 128. The producer explicitly declared that
percentage scope remained in evidence. This was not replay loss.

The graph reader searched string properties for coverage and related words.
That finds the old 65% recap but not the scope-free 78% record. Its returned
citations never reach that ratio. Both representation and retrieval matter:
a broader numeric search could find 0.78, but could not safely supply the missing
scope or update relationship. This is not proof that every possible graph reader
must return 65%.

### 2. A contradiction edge must connect the actual conflicting assertions

The producer's acquire.py explicitly chooses message pairs, then uses the first
assertion of the earlier message as the target. relation:beam:6505 therefore
connects the never-obtained denial at proposition:beam:1255 to
proposition:beam:446, a request about using a rate-limit counter. That target is
not the acquisition statement later in message 32. The edge exists and replays,
but its target selection does not express the intended contradiction.

There are other CHALLENGES edges, including a denial linked to key-configuration
and a bug-fix denial linked to a null-check report. Those are positive controls
against saying that no conflicts were captured. Their endpoint text is still in
retained evidence rather than graph properties. The reader's observed queries
do not inspect CHALLENGES. Thus omitted contradiction answers involve at least
three separable issues: one demonstrated wrong endpoint, thin endpoint meaning,
and an unexercised relation-reading strategy. No single-factor cause is proven.

### 3. Free text can rescue an answer without validating the typed graph

quantity_kind is defined as the kind of quantity in the source's words. The
producer assigns it the entire source span. Sentence splitting can leave long
mixed recaps intact, so a measurement field carries many unrelated assertions.
That explains the reader's heavy dependence on one recap. It also explains why
the quota answer survives the numeric extraction defect: the field still says
1,200 while the numeric bounds say 200. A future test must distinguish correct
answers read from prose from correct typed measurements and relationship use.

These are acquisition and consumer-design findings. No missing Core retention,
replay or evidence-trace capability is established. Malleus's structural admission
does not promise that a producer selected the semantically correct edge target.

## Execution checks and limits

Both bundles contain all twenty questions with the same question bytes and no
rubrics. All 62 graph and 122 source citations resolve to the quoted fields.
That proves citation location, not entailment. Exact framed tool output verifies
all 88 source frames plus task/questions, and all 14 graph task/question/schema
frames. Graph records were selectively queried, not fully delivered in context.
Both observed settings are gpt-5.6-sol/low, no compactions. There was one frozen
answer bundle per reader and no parent semantic feedback. Authors corrected
their own scripts before submission; that is not an extra model sample.

Inspection of recorded tool calls and generated scripts found packet-local
reads/writes, no observed answer-key, other-condition or external-source access.
Graph made an outbound status report to its parent, with no semantic reply sent
back. Access was instruction-constrained in a shared filesystem, not enforced
by a dedicated operating-system sandbox. These checks do not prove isolation
from pretraining knowledge. The source, generated text markers and questions
are synthetic and were not an unseen selection.

| Session | Cumulative input | Cached input, included in input | Output |
| :--- | ---: | ---: | ---: |
| Producer | 6,051,621 | 5,751,168 | 19,177 |
| Graph reader | 1,072,896 | 971,136 | 8,453 |
| Source reader | 2,527,841 | 2,353,920 | 8,308 |

These are repeated session tokens, not unique source length, monetary cost or
matched budgets. The graph condition uses fewer observed reader tokens here,
but acquisition has a cost and answer coverage differs. No efficiency win,
context-overflow result, incremental-acquisition result, aggregate accuracy,
human ratification or paper claim follows.

## Retained evidence and next decision

Private run root: private/beam-weather-calibration-01/readers-01/.
Each condition retains task, input manifest, launch record, evidence, questions,
reader scripts and work/answers.json. audit.json records exact identities,
delivery counts, actual settings and usage. ASSESSMENT-RULES.md predates returned
answers. test_beam_reader_results.py verifies the frozen bundles, delivery,
citation concentration and the specific scope/endpoint witnesses above.

Graph answer SHA-256: c9ff18eb0212dedd484ff7fbee678a08c3ab8369e549397030693d6f85275e37.
Source answer SHA-256: 237702aedacf0ec2a5402adcfb943c57a69a818bb194f078d682e48896053baa.
The earlier capture, ledger and replay identities remain those in RESULT-01.md.

Recommendation, not launched: first measure the intended graph-plus-evidence
consumer on the same frozen capture, with evidence access and costs explicit.
That separates inaccessible retained meaning from genuinely wrong representation
before changing acquisition. A separate bounded repair would need whole-number
span tests, measurement-scope checks and assertion-level conflict endpoints,
with successful controls preserved. Scaling this unchanged capture now would
multiply known defects rather than establish living domain memory.
