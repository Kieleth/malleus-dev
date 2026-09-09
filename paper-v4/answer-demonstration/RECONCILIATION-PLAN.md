# Source-to-record reconciliation pilot

Proposed E-0285, approved by Luis's Go at E-0286. Master 1.5.23.

Completed E-0291: first proposal passes structural checks, but one unresolved
asserted determination withholds the atomic batch. No retention or after-query.
The execution guard is verified against the actual candidate and decision.
See [results](RECONCILIATION-RESULTS.md). The approved scope below is retained;
it does not authorize a semantic retry or a supported-subset admission.

Purpose: establish what a quantity means in its source context and what the
accepted graph actually represents. A valid locator is not sufficient evidence;
unchanged numbers do not establish unchanged meaning. This follows the concrete
errors in INTEGRATION-RESULTS.md, not a new claim about model internals.

## Fixed boundary

Start from the accepted sol-qualification-01 history, not the withheld integration
candidate. Keep Core 160878cf14c0d27b11a440e26688708e9b7a7e2b, source, selected
reading, ontology, five captures and depth-method-01 queries unchanged. Preserve
all prior attempts and reviews. No Core, manuscript, dependency or Git changes.

The proposed six-record scope is verified against that graph:

| Existing record | What the pilot examines |
| --- | --- |
| observation:lab-melt-fraction | Resolve the actual subject and distinguish cited interpretation from measurement |
| observation:lab-water-content | Preserve the shared subject while checking this quantity's own scope |
| observation:average-depth-uncertainty | Distinguish source context from falsely claimed existing fields |
| observation:abstract-primary-co2 | Keep a synthesis distinct from a specifically attributed estimate |
| observation:rc2-primary-ba90 | Positive control for a genuinely identified proxy estimate |
| qualification:evidence:observation:rc2-deep-depth:v1 | Reconcile depth reference and observational context across passages |

Three existing SUPPORTS relations touch these targets. Retarget one only if its
endpoint is explicitly replaced, preserving predicate and target. No new entities,
independent relations or ontology revision. Numerical bounds and units stay fixed;
any needed numerical correction is reported separately. Other contextual property
changes or removals require explicit source support and independent assessment.
Do not preserve an unsupported classification merely to make a candidate pass.

This is an RCA-guided pilot. Target selection exposes known problem areas. It
is not question-blind acquisition, a replication of the broad integration run,
or a controlled estimate of this procedure's causal effect.

## Milestones and exit conditions

### 1. Mechanical reconciliation checks, in TDD

Build the input view from actual records, their one-hop subjects and ontology
definitions. Render real field values, not a generated paraphrase of the graph.
Require claims of existing representation to cite resolvable record/property
paths. Missing paths are failures, not empty values or inferred defaults.

Reuse capture identities and assertion references in the report, with the full
containing source blocks available. For newly cited evidence in this pilot,
copy complete model-selected blocks from the selected reading into the existing
capture format. The model chooses evidence and mappings; deterministic copying
does not invent facts. Do not duplicate quotes under a second report grammar.
Multiple blocks can support one interpretation. A block remains an evidence
address, not a unit of meaning.

Tests must distinguish valid paths from absent or misbound fields, same assertion
IDs in different captures, wrong source identities, truncated new block evidence,
unexplained changes and missing relation replacements. Reuse current preservation
and public preflight checks. Add a paper execution guard that refuses retention
without an affirmative source-review decision bound to the exact candidate bytes.
Neither structural success nor a stale review can supply that decision. This
guard checks authorization and identity, not semantic truth.

Exit: positive and negative controls pass; prior run artifacts remain exact.

### 2. One model-produced proposal

Proposed condition: one fresh Sol/ultra session, with verified complete input
delivery. Supply the six targets, actual context, source and defect categories.
Do not supply evaluator-authored replacement values, questions or query code.
For each context claim, distinguish represented, missing, proposed and unresolved.
The existence of a field does not settle whether its meaning is correct.

Return one scoped candidate plus the reconciliation account. No required positive
result or quota. Preserve each attempt, with at most two exact structural returns.
No semantic retry within the run. Old rejected proposals are not promoted by hand.

Exit: one retained proposal or explicit incomplete/refused result, not a selected
best-of-several sample. No claim that all document context has been reconciled.

### 3. Independent source assessment before admission

Assess every proposed change and every claimed existing context against the
source and actual graph. Explicitly inspect subject identity, attribution,
summary versus specific estimate, and complete supporting evidence. Keep useful
qualifications separate from unsupported assertions. An unresolved correspondence
must not become an established identity because its numbers match.

One unsupported or unresolved asserted change withholds this atomic batch.
Do not silently select a passing subset. Incompleteness is not itself falsehood,
but an unresolved required context cannot be reported as completed. Record the
paper-owned decision; do not claim Core performed semantic evaluation. Human
ratification remains pending unless Luis ratifies the assessment.

### 4. Admit, replay and compare only a supported batch

Use the existing public path on a sibling history. Check exact delta, old record
versions, unchanged records and ledger prefix. Repeat with the same explicit
transaction time. Run the thirty unchanged queries without source access, then
assess changed answers under unchanged requirements. Preserve historical grades.

If withheld, retain the reason and diagnose the failed stage; do not execute an
accepted-state answer demonstration or launch a replacement sample. This pilot
tests a bounded repair procedure, not general completeness or scientific truth.

## Author decision

Luis approved this six-record scope and RCA-guided condition. The source-role
questions, evidence references and explicit field checks above are the selected
change. No new Core capability is currently needed.
