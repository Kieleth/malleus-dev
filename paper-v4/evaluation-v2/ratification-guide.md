# Human ratification

The experiment and Codex preliminary review are frozen. Human ratification may change only the authored judgments, locators, and reasons in a copy of the preliminary record. It does not change the ontology, population, ledger, replay receipt, query binding, or query result.

## Review order

1. Read the four questions in `paper-v4/experiment/competency-questions.json`.
2. Inspect every row in `paper-v4/experiment-v2/results/query-result.json` through the cases in `paper-v4/experiment-v2/native-query-binding.json`.
3. Check each claim against the cited blocks in `private/paper-v4-text-layer/selected-reading.json`.
4. Read `paper-v4/evaluation-v2/review-record.preliminary.md`. Accept or correct each source-support label, responsiveness label, locator list, and rationale.

## Record the decision

Copy the preliminary record to `paper-v4/evaluation-v2/review-record.human.md`. Preserve the `preliminary` object and both input digests. Then:

- set `status` to `HUMAN_RATIFIED`;
- use `RATIFIED_AS_RECORDED` if no question entry changed, otherwise use `RATIFIED_WITH_EDITS`;
- set `ratification.completed_at` to the actual UTC time in `YYYY-MM-DDTHH:MM:SSZ` form;
- write a nonblank `ratification.notes` statement;
- keep `evaluator_kind` as `HUMAN_AUTHOR` and `actor_id` as `actor:luis`.

If the evidence does not support ratification, set `status` to `HUMAN_REJECTED`, disposition to `REJECTED`, and explain why in `notes`.

The human record becomes paper evidence only after the existing structural validator accepts it with human ratification required. Ask Codex to run that check after saving the file. Until then, the manuscript must call all four judgments preliminary.
