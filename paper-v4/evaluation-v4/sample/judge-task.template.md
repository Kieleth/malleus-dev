# Independent judgement of a sampled witness set

Template. The dispatching session substitutes `<PACKET_PATH>`, `<RECORD_PATH>`,
`<SAMPLE_SHA256>`, `<WITNESS_COUNT>`, `<MODEL_ID>`, `<ACTOR_ID>` and
`<REASONING_EFFORT>` and writes the result next to the packet. No placeholder may
survive instantiation, and the sample file's path is not one of them: its name
says which stratum this is, and the stratum is the recorded label of every
witness in the packet.

You are a fresh judging session. You are not the session that produced the
graph, and you are not the session that reviewed it. Your labels are compared
with labels another model already wrote for the same witnesses, and you are not
shown those labels. If you find yourself reasoning about what the first review
probably said, stop and judge the block in front of you instead.

## What you are given

`<PACKET_PATH>`, a JSON file with `<WITNESS_COUNT>` witnesses. Per witness:

- `cell`, the run the witness comes from.
- `witness_key`, its identity in that run's graph.
- `kind`, one of `ENTITY`, `SUBJECT` or `RELATION`.
- `returned`, the fields the query returned for it: the `record` the graph
  holds, plus `subject` on a `SUBJECT` witness and `relation`, `source` and
  `target` on a `RELATION` witness.
- `cited_blocks`, the reading blocks the first review cited for it, each with
  its `id` and its full text.
- `judgement`, an empty slot you do not fill in the packet.

The packet is private. It reproduces the text of a copyrighted source. Do not
copy any of that text into your record, do not write it into any other file,
and do not quote it back in prose.

## What you judge

One thing per witness: whether the cited block or blocks support the claims the
returned fields make. This is block-local, the same rule protocol v3 applies at
`paper-v4/evaluation-v4/review-protocol-v3.json`. Judge against the cited blocks
and nothing else. You have no network, and you do not open the source document,
the graph, the ontology, any other run's files, or any other block of the
reading.

Do not judge the ontology, the modelling decisions, the retrieval, the choice of
locator, or whether a better block exists somewhere else. Do not compute a
score, a total, a percentage or an average. Aggregation happens elsewhere, from
your record.

## The four labels

Their definitions, verbatim from the frozen v3 review task
`paper-v4/evaluation-v4/review-task-protocol-v3.template.md`, which instantiates
the `judgments.source_support` set of `review-protocol-v3.json`:

- `SUPPORTED`: the cited surface supports every material claim in the row.
- `PARTIAL`: it supports some but not all of them, or a needed qualifier is
  absent.
- `UNSUPPORTED`: it contradicts a material claim or supplies no support for it.
- `NOT_EVALUABLE`: the allowed source surface is insufficient to decide. This
  is the label an unresolvable locator takes, by rule.

A witness whose packet entry carries no `cited_blocks`, or whose cited block
carries no text, is `NOT_EVALUABLE` by that last rule, and the rationale says
what did not resolve.

## The rationale

One per witness, in your own words, one or two sentences. Name the claim you
tested and what in the block decided it. Do not quote the block: a rationale
that reproduces sixty consecutive characters of the reading is refused by the
validator, and paraphrase is what the rule asks for.

## Recording

Copy `paper-v4/evaluation-v4/sample/judge-record.blank.md` to `<RECORD_PATH>`
and fill the single JSON block:

- `sample_sha256` is `<SAMPLE_SHA256>`, copied verbatim. It is the digest of the
  sample file, which you are not given and do not need.
- `judge.evaluator_kind` is `INDEPENDENT_MODEL_JUDGE`. This is not the
  `CLAUDE_PRELIMINARY` kind of a v3 review and it is not a human ratification.
  Your record is a second opinion on a sample, never paper evidence on its own.
- `judge.model_id` is `<MODEL_ID>`, `judge.actor_id` is `<ACTOR_ID>`,
  `judge.reasoning_effort` is `<REASONING_EFFORT>`.
- `judgements` carries one entry per packet witness, exactly once each, with the
  witness's own `cell` and `witness_key`, one of the four labels, and your
  rationale.

Then hand the record back and stop. The dispatching session runs
`validate_judge_record.py` against it, because that script needs the sample file
and the sample file's name says which stratum this is. The validator refuses with
one named reason: a wrong schema, a sample digest that does not match, a witness
judged twice or not at all, a label outside the four, an empty rationale, or a
rationale that shares a sixty-character run with the reading. A refusal comes
back to you in those words, and none of them names a recorded label. Fix what it
names and hand the record back again.

Before you hand it back, check by eye what you can check without the sample: one
entry per packet witness, each witness once, every label one of the four, every
rationale your own words and not a quotation.

Do not run `agreement.py` and do not go looking for the sample file.
