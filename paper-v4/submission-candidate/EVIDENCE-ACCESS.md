# Claim and evidence map

This is an access map, not a new receipt system. Every figure printed in the
manuscript is read from a frozen public file, a validated review record, or a
fresh run of a public fixture. The table names the check behind each claim and
where a reader can open it.

| Printed claim | Retained check | Access |
| --- | --- | --- |
| Six fresh ontologies compiled at the first attempt | `ontology-run/result.json` in run-20 to run-24 and run-26; run-25 reuses run-23's ontology | Public, `paper-v4/experiment-v4/run-NN/` |
| Six populations admitted at runner attempt 1, run-20 at attempt 2 | `results/launch-log.json` runner entries; `results/usage.json` population line | Public, same directories |
| Every history reopens to its recorded graph | `results/run-result.json`, `reopen_matches_admitted` both true, 14 ledger events, ledger head and replay receipt | Public; the ledgers themselves are withheld |
| Every block asserted or declared nothing assertable; every record traced | `results/run-result.json` census block counts and `records_traced` against the graph counts | Public |
| 2,353 witnesses, none initially labelled UNSUPPORTED, 24 PARTIAL | `review-record.preliminary.md` of run-22-v413, run-23, run-24, run-25 and run-26, `witnesses` block | Public, `paper-v4/evaluation-v4/` |
| Earlier-protocol support for run-20 and run-21 | `review-record.human.md` rows, ratified by the author | Public, same directories |
| Selected first-set coverage: 90, 92, 90, 93 and 96 of 102 elements | `questions` blocks of run-22-v413 through run-26 against their frozen question files; run-22 v4.12 retained separately at 82 | Public; question files under `paper-v4/experiment-v4/` |
| 20 cited vocabulary URLs, none fabricated, in the first five fresh ontologies | `ontology-run/result.json` citation check of run-20 to run-24 | Public |
| Relations 55, 26, 31, 22, 21 and gaps 77, 94, 15, 20, 153 | `results/run-result.json` graph and `gaps_by_kind` | Public |
| Small Shop connected history: 21 changes / 0 revisions / 121 events, then 34 / 1 / 193, then 37 / 2 / 216; the ordering comparison; the occurrence-replacement refusal | A fresh run of the chain from empty into a new path; `paper-v4/test_shop_connected_calibration.py` rebuilds it and compares every printed figure and both new Appendix B exhibits | Public and reproducible from the repository |
| Small Shop shipment policy: 3 accepted changes, 32 ledger events, the duplicate assignment refused as VIOLATED | A fresh run of the policy fixture; `paper-v4/test_shop_calibration.py` reruns it and compares the prose figures and its Appendix B exhibit | Public and reproducible from the repository; needs SWI-Prolog on the path |
| Injected faults: 55 trials, 35 refused with a typed diagnostic, 30 of those a byte-exact ledger prefix, 20 admitted, 5 exposed, 15 invisible | `paper-v4/experiment-v4/fault-injection-01/outcomes.json` carries every trial's population digest, ledger, diagnostic and post-admission checks; `RESULTS.md` states the classification and `test_faults.py` binds it | Public; the faulted populations, ledgers and exports are private, they reproduce the reading |
| The digest binding declared on five record types and covering 236 of run-23's 440 records | `results/census.json` `provenance_coverage` and `results/run-result.json` `records_traced` | Public, `paper-v4/experiment-v4/run-23/` |
| Appendix A exhibits | Exact subsets of run-23's retained query result and its review record; `test_manuscript.py` checks the subsets and the locators | Review record public; query result withheld |
| The in-context baseline: 101 of 102, 24 of 25 questions, 130 of 135 claims supported, 127,303 tokens | `paper-v4/experiment-v4/baseline-01/` (answer grammar, validator, producer task, contract) and `paper-v4/evaluation-v4/baseline-01/` (v3.2 manifest, task, review record, ticked checklist) | Public; the producer's answer file is withheld, it quotes the reading |
| The derived absence split, 41 absences over four cells | `paper-v4/evaluation-v4/absence-recoding-2026-09-12.json` with its script and tests; frozen records untouched | Public |
| The independent judge, 196 of 200 and 18 of 22 | `paper-v4/evaluation-v4/sample/` (samples, both judge records, dispatch log, agreement script); excludes run-26 | Public; the blind packets are private, they carry block text |
| Reuse: 88 of 102 versus 101, no recapture, both cost accounts | `experiment-v4/reuse-01/read_results.py`, RESULTS.md and both reuse review packages | Public reviews and results; private reading and launch logs required for full regeneration |
| Original set A and set B control defects, revised set A assessment accepted | `evaluation-v4/audit_controls.py` and `test_control_screen.py` | Derived from retained model judgements; no new independent semantic review |
| Run-22 re-queried under the v4.13 binder: 90 of 102, controls 5 of 5; the first reading 93 and 2 of 5 | `paper-v4/experiment-v4/run-22/rebind-v4.13/` (binding, comparison, README) and `paper-v4/evaluation-v4/run-22-v413/` (manifest, task, both review records); the clarification at `paper-v4/evaluation-v4/review-task-v3-clarification-2026-09-12.md` | Public; the re-query's result rows withheld like every query result |
| Shop staged reconsideration: 3 and 5 obligations, counts 2 / 1 / 0 / 0 and 1 / 4 / 0 / 0, the third boundary's complete certificate, the recorded additive revision, 764 facts and zero violations | `paper-v4/experiment-v4/shop-reconsideration-01/` binds every printed number to the launched archives, the producer verification files and the two assessors' records, and refuses any 60 character run shared with the chapter's text or the evidence packets | The two author ratifications are public under `paper-v4/evaluation-v4/`; the archives, packets and assessors' records are private under `private/shop-progressive-01/`, available to the author, withheld because the packets carry the chapter's sentences |

## Files the manuscript links

| Linked file | What it is | Boundary |
| --- | --- | --- |
| [Questions v3.1](../experiment-v4/competency-questions-v3.1.json) | The thirty questions bound by run-24, frozen | Public |
| [Questions v3](../experiment-v4/competency-questions-v3.json) | The thirty questions bound by run-22 and run-23, frozen | Public |
| [Subject-tie clarification](../evaluation-v4/review-task-v3-clarification-2026-09-12.md) | The written clarification of protocol v3 applied to the second review of run-22's re-query | Public |
| [Protocol v3.2](../evaluation-v4/review-protocol-v3.2.json) | The review protocol the baseline binds: six absence codes, identities per surface kind, the in-context answer surface, and the thirteen-entry checklist | Public |
| [Shop second boundary ratification](../evaluation-v4/author-ratification-2026-09-17-shop-staged-review.md) | The author's ratification of the assessor's record over three obligations, bound to that record's digest; the certificate is outside its scope | Public |
| [Shop third boundary ratification](../evaluation-v4/author-ratification-2026-09-18-shop-third-boundary.md) | The author's ratification of the assessor's record over five obligations, bound to that record's digest; the certificate is recorded beside it and not ratified | Public |

## Withheld per cell, with public digests

The producer capture, the exported records, the gap statements, the ledger and
the query results reproduce text of the selected reading and are withheld. Each
cell's `results/withheld-artifacts.json` names them with their digests and the
measured character-run ladder. The gap counts by kind are public in the run
result. The source article is under CC BY-NC-ND 4.0; redistribution of a
derived text layer is a rights decision the author has not taken.

## What the public files establish and what they do not

They establish the pins, the isolation message, the ontology and its
compilation, the admission and replay outcome, the census, the token usage and
every review judgement with its locator. They do not let a reader replay a
document ledger or recompute a statement digest against the article's text
without obtaining the article and the pinned reader. The Small Shop fixtures
need neither; they run from the repository and refuse to write over a history
whose prefix they do not expect. The fault-injection control needs run-23's
retained producer directory, which is private. The author read the model-assisted judgements of run-22 to run-26 in full and
ratified them on 2026-09-16 ([record](../evaluation-v4/author-ratification-2026-09-16.md));
the baseline and reuse judgements remain unratified. Public here describes the intended distributable evidence surface;
uncommitted files still require an approved commit and publication.
