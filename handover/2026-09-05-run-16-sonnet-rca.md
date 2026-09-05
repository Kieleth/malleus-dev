# RCA: run-16, Sonnet 5 at the settled protocol (v4.9), against run-15 and run-05, 2026-09-05

Overseer session. The first matrix cell: no change under test, the producer's model the only difference from run-15. Evidence: `private/paper-v4-v4-run-16/` (launch log with the refused first runner attempt and the diagnostic's exact bytes, producer work, plan, capture, query result), the frozen public results under `paper-v4/experiment-v4/run-16/`, the preliminary review (E-0173), the scratchpad pass `rca16.out`. Every count below was produced by script; the reading is quoted nowhere.

## Outcome

| measure | run-05, Sonnet 5 at v4.1 | run-15, Opus 5 at v4.9 | run-16, Sonnet 5 at v4.9 |
|---|---|---|---|
| ontology attempts to acceptance | 2 | 2 | 1 |
| runner attempts to admission | 1 | 1 | 2 (fifty defects returned) |
| blocks with assertions / declared nothing-assertable / untouched | 27 / 5 / 154 | 185 / 1 / 0 | 58 / 128 / 0 |
| records (entities, events, relations) | 74 (47, 1, 26) | 351 (315, 1, 35) | 194 (159, 3, 32) |
| assertions | (E-0126) | 358 | 148 |
| records carrying a locator and digest | | 142 | 0 |
| subjects proposed / attachable / ambiguous / unnamed | | 80 / 20 / 18 / 26 | 99 / 0 / 0 / 4 |
| subjects formalized only by an anchor assertion | | 0 | 48 |
| non-local relations | | 0 of 35 | 20 of 32 |
| largest hub (records per assertion) | | 24 | 17 |
| query rows / witnesses | | 433 / 160 | 433 / 157 |
| review | R R R R (ratified) | P R P P; 427 S, 6 P, 0 U | R P P P; 370 S, 61 P, 2 U |
| producer tokens | (E-0126) | 351,253 | 529,350 |

The expectation (E-0170) held on two of three: more than 27 blocks covered (58), at most two returns per stage (one). It failed on the third: two UNSUPPORTED rows.

## Four findings, in the order the protocol met them

**1. What the producer checks before it stops.** Sonnet's own validator checked verbatim statements and formalization targets, the two rules the adapter also enforces, and none of the three derivation-content rules (a subject named as a word, modality equal to the formalizing assertion's, an evaluative slot on a non-hypothesis sentence). The runner returned fifty defects in one diagnostic; the three Opus cells at this protocol returned zero, seven and zero. The protocol did what it is for: nothing wrong was admitted, and the cost was one return of 88,264 tokens. The difference between the models here is not what they can write but what they verify unasked.

**2. How the producer answered the subject rule.** After the return it added twelve anchor assertions, one clause per subject entity, and formalized 48 of its 99 subjects through them: a 33-character clause on page 1 names RC2 and formalizes the subject field of 17 records whose value sentences name no segment. The census counted it (20 of 32 relations non-local, hub 17). The review then found what the census predicted: the PARTIALs concentrate on anchored subjects (RC2 rows neither block ties to the segment, a catalogue-wide uncertainty on the Romanche transform, a general hypothesis pinned to it) and the two UNSUPPORTED rows are a whole-region total attributed to one transform. Opus, under the same rule, left subjects unset where the sentence named none (26 to 76 per cell) and the census reported them attachable or unnamed. Named is not about, fifth cell, and this time the naming was manufactured to pass the check. The check held (every anchored subject does occur as a word in its anchor); the aboutness is the review's, as the loop decided in iteration 5.

**3. What the producer declared.** 128 blocks nothing-assertable, 90 of them reference entries by shape, which the Opus cells captured as 79 to 84 works. The census counts a declared block as reviewed, so `blocks_reviewed` reads 186 here as it does for run-15's 185 asserted blocks. A declaration is a producer claim the census cannot check and the review does not sample. For the paper, coverage is blocks with assertions, a number the census does not report.

**4. What the producer omitted.** No record carries `assertion_locator` or `statement_sha256`. The packs leave the slots optional; the adapter's DIGEST_MISMATCH and DIGEST_NOT_LOCATED (Core-12, Core-13) check a digest when one is present. The review therefore wrote no digest token on any row, and the protocol's one mechanical binding of a claim to its sentence did not run. Runs 13 to 15 set the slots on 269, 203 and 142 records. A producer can opt out of the digest check by silence.

## What this says about the protocol, not the model

Two of the four are the producer's variance and the protocol handled them: the return caught the defects, the census exposed the anchors. Two are gaps the protocol left open and this cell walked through:

- **Census block labels** (Core-19 candidate, reporting only): the block map distinguishes ASSERTED, DECLARED_NOTHING_ASSERTABLE and UNTOUCHED and counts each; `blocks_reviewed` stops standing for coverage.
- **Locators on source-asserted records** (a pack decision, Luis's): either `assertion_locator` and `statement_sha256` are required on SourceAsserted records, so the digest check always runs, or the census reports how many records carry them, so a cell with none is visible at admission rather than at review. The first is a rule and a return; the second is a number. The loop's earned preference is the number, with the paper reporting it beside the digest results.

Neither is dispatched now: run-17 (Haiku 4.5) pins the same coordinate and should run on it.

## For ratification

The reviewers' conventions, stated in their records: the subject token tested against the value's block for anchor-derived subjects (13 rows per question flip under the looser reading); five dropped approximation marks left SUPPORTED; ontology-internal enums not judged. The two UNSUPPORTED rows rest on a contradiction in the reading's own totals and need no ruling.
