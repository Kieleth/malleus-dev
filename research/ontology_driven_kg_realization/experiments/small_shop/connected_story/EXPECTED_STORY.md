# What the connected Shop run must explain

These are expected source answers, written before the connected mapper. They
are not results obtained from the graph and not a new Core evaluation system.
The source is the retained Table 1 and four section 1 excerpts credited in the
[README](README.md). Human ratification remains pending.

The machine-readable [source expectations](source_expectations.json) contain
nine questions, literal expected answers, interpretation limits and exact source
field witnesses. A witness is an existing value in a numbered source row. Its
mechanical check proves that the cited value exists, not that our interpretation
is correct. A human can inspect the retained table image and challenge the
interpretation separately.

## The connected account

| Question | Expected account | What we must not invent |
|---|---|---|
| What was requested? | O1 needs two X and one Y; O2 needs one X and one Y. | Requested quantities do not assign physical units yet. |
| What changed in procurement? | A requests three X. B first requests one Y, then the update states two Y. | Do not count B's update as another independent order or replace one physical Y unit with another. |
| Which units go where? | A's received units are X1, X2, X3; B's are Y1, Y2. O1's packing names X1, X2, Y1; O2's names X3, Y2. | Packing is a recorded assignment, not a claim of permanent ownership. |
| Which invoices belong to the orders? | The creation occurrences associate I1 with O1 and I2 with O2. | No invoice amount is stated. |
| What does payment connect? | P1 is received at e29; e30 clears I1 and I2 with P1. | Payment receipt and invoice clearing are not the same occurrence. |
| What was changed on I2? | e9 says the invoice was updated. | The changed field and new value are absent. Keep the occurrence and the gap. |
| Why can one order depend on the other? | Both orders concern one unnamed customer. The stated rule permits shipment only with at most one unpaid invoice. The prose says O2 waits for P1 covering both invoices. | This does not establish balances at every checkpoint, a causal proof, or an authorization to ship. |
| What do the times establish? | Retain the printed time strings, including the two `00-01` dates. | No year, timezone, repaired date, elapsed duration or domain ordering from row position. |
| What makes packing multi-object? | e27 relates R4, O1, X1, X2 and Y1 in one occurrence. | Do not split it into unrelated per-object occurrences or infer causation from participation. |

The original source has 21 selected events. These nine questions are inspection
cases, not permission to populate only the events they mention. Every row and
populated source field still belongs to the [coverage obligation](SOURCE_COVERAGE.md).

## How this becomes a test of Malleus

The future producer reads source bytes, the selected ontology and identified
mapping/rule artifacts. It must not read this answer file. It proposes records
through Core's public interfaces. The test then discards in-memory state,
reopens the retained history, queries the rebuilt graph and compares the
independently expected facts and their source witnesses.

This separates three questions:

1. Did we retain the source and write the expected interpretation honestly?
2. Did the source mapper produce the intended records and explicit gaps?
3. Did admission, supersession, replay and queries preserve those records and
   their evidence?

Current tests cover the witness accounting for the first question and the small
B/e4 to B/e7 compatibility probe. They do not yet cover the connected run in
questions 2 and 3. `NOT_STATED` and `NOT_JUSTIFIED` are labels in this test data,
not proposed domain enum values or strings that the population should insert.

The source rule will require its own frozen evidence scope before shipment
eligibility is calculated. An absent payment row cannot silently become an
unpaid balance. A recorded historical shipment must stay visible even if a
later check finds a violation. Eligibility and authorization remain separate.

## TDD boundary

RED `50b7df40` contains seven failing tests for the missing answer file. Adding
the hand-authored file makes those tests pass. Four deliberately broken copies
exercise a missing row, missing field, substituted value and repeated question.
This is test-data contract work, not a claim that the connected mapper went
from failing to passing. That mapper still needs its own behavioral RED after
the history selection is resolved.

Run the evidence checks with the existing declared environment:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story/test_source_expectations.py
```

No new dependencies, Core edits, policy selection or source mutation are part
of this addition.
