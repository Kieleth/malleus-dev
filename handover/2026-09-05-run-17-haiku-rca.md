# RCA: run-17, Haiku 4.5 at the settled protocol (v4.9), against runs 06, 07 and 16, 2026-09-05

Overseer session. The second matrix cell: no change under test, the producer's model the only difference from runs 15 and 16. Evidence: `private/paper-v4-v4-run-17/` (launch log, the three refused attempts with the diagnostics' exact bytes, producer work, gate). The reading is quoted nowhere.

## Outcome

| measure | run-06, Haiku at v4.1 | run-07, paired Haiku at v4.1 | run-17, Haiku at v4.9 |
|---|---|---|---|
| ontology | accepted at attempt 02 (a fabricated ISO standard cited) | accepted | accepted at attempt 01 (three institution home pages cited as vocabularies; nothing fabricated) |
| population | 7 assertions, 5 declared, 174 untouched | (E-0130) | 8 assertions over 7 blocks, 0 declared, 179 untouched (E-0176 said 178; corrected by E-0177) |
| runner refusals | envelope keys; a phantom block id; a paraphrase (one per refusal) | (E-0130) | all 8 NOT_VERBATIM (aggregated); rehydration (6 unknown properties, a missing required slot, 2 enum values); GAP_REQUIRED (all 8 assertions empty) |
| terminal | refused after two returns | refused after two returns | refused after two returns |
| producer tokens | 137,734 | (pair 265,340) | 151,411 |

## What changed and what did not

The v4.9 skill was written from run-06's RCA: the verbatim method (locate by a whitespace-insensitive anchor, copy the block's bytes), the block-inventory rule, the honest citation form, and aggregated diagnostics. Three of those four reached this producer: no block id was constructed, the citations are real organisations rather than a nonexistent standard, and the first return turned eight paraphrases into eight byte spans with the text layer's damage preserved, which run-06 could not do in two returns. Aggregation cut the cost of the first defect class from two returns to one.

What the skill did not reach is the step between reading the accepted surface and writing records: the producer wrote six properties the surface does not declare, omitted a required slot, and invented two relation-type values; then, told which, it removed the properties and left every assertion with no target and no gap. The Opus and Sonnet producers validated every field against the staged surface and every assertion for a target or a gap before writing, unasked; run-16's did so only after a return, and run-17's not at all. Across the five cells at the settled protocol the axis that separates the models is the same: what the producer checks before it stops.

## What the protocol got wrong, in two small places

- The rehydration refusal is a raw `ValueError` from `kg.py`, exact and aggregated in its text and untyped. The paper's claim that every refusal is typed is not true at that stage.
- GAP_REQUIRED names the first assertion without a target or a gap; all eight were in that state.

Both are in Core-19 with run-16's two (census block labels; locator coverage).

## What this cell is evidence for

One session on one document. It says that the settled protocol admits nothing wrong from a small producer, names each defect class exactly, and reaches the producer on the two classes the skill states as method; it does not reach the two the skill states as rules without method (validate against the surface; every assertion carries a target or a gap). Whether a skill sentence with a method would carry a Haiku producer to admission is a question for a later cell, after Luis's rulings; it is not a Core question.
