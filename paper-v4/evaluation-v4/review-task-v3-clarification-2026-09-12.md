# Protocol v3 task clarification: the subject-tie rule (2026-09-12)

Status: a clarification of how coverage entries are written under
`paper-v4/evaluation-v4/review-protocol-v3.json`. The protocol file is frozen
and is not edited. This text is handed to a reviewer as an addendum to the
instantiated task, recorded in the cell's launch log as an instruction beyond
the task, and is to be folded into the task template at the next protocol
revision. Ruled by Luis on 2026-09-12 (option 1 in chat) after the first review
of run-22 under the v4.13 binder read three NONE-expected controls as PARTIAL.

## The rule

A required semantic is named by a returned row only when that row carries the
element for the question's subject matter. The row's record, subject or
relation must be the thing the question asks about, or be tied to it by a
returned relation or by a field on the row itself. A row that carries a
same-named element for a different subject does not name the semantic; write
`row_index: null` and the absence cause. A description, `count_scope` or
`quantity_kind` field can name a semantic only when it does so for the
question's subject.

Consequently a control whose quantities the source does not state reads NONE
unless a returned row carries a required element about the control's own
subject. Sample records that belong to the carbon dioxide estimation do not
name the `sample_set` of a sulfur and chlorine question.

## Why this is a clarification and not a change

The reviewers of run-22 under v4.12, run-23 and run-24 read the protocol this
way: their not-in-source controls read NONE in every cell (records under
`paper-v4/evaluation-v4/run-22`, `run-23`, `run-24`). The first v4.13 review
of run-22 counted any returned row's fields, and its three not-in-source and
excluded-surface controls read PARTIAL for that reason alone (its record is
retained as `run-22-v413/review-record.preliminary.attempt-01.md`). The rule
adds no judgement kind and moves no label by hand; it fixes which rows count,
so that coverage under the two binders is measured on one standard.
