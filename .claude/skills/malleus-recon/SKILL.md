---
name: malleus-recon
description: Evidence-first literature and paper forensics with a typed knowledge graph. Use when the user asks for prior-art research, related-work analysis, closest-work comparison, paper or dataset lineage, novelty boundaries, recursive citation exploration, a literature knowledge graph, or union/intersection/difference matrices across technical claims. Use the shipped malleus-recon ledger and exports when persistent local research artifacts are wanted. Never use graph structure or scores as an automatic novelty, truth, plagiarism, or quality verdict.
---

# Malleus Recon

Recon turns a literature investigation into a typed, evidence-linked research
record. The agent researches and judges. The local Recon module records,
checks, compares, and rebuilds the artifacts. A recorded statement passed the
schema and ledger rules. It did not thereby become true.

Keep the Ordo flavor light. Call a bounded investigation a recon. Facts still
need ordinary names, locators, dates, and evidence.

## Before you build: state the claim

Before searching, write four lines for the human:

1. The exact target claim or research question.
2. The smallest observation that would materially weaken or falsify it.
3. The comparison axes that matter to this claim.
4. The boundary of this pass, including cutoff date and excluded questions.

Stop and ask when the claim itself is ambiguous. Do not quietly substitute a
broader architecture claim, a narrower implementation claim, or a chronology
claim. Search results only answer the target actually declared.

## Use the shipped instrument

Probe before assuming Recon is installed:

```bash
python3 - <<'PY'
try:
    import malleus.recon as recon
    from malleus.ontology import bundled_ontology_path
    print("status=installed-current")
    print(f"module={recon.__file__}")
    print(f"ontology={bundled_ontology_path('domains', 'recon.yaml')}")
    print(f"contract={recon.bundled_contract_path()}")
except ImportError as error:
    print("status=absent-or-stale")
    print(f"reason={error}")
PY
```

If the probe fails and a local `malleus-dev` checkout exists, run with
`PYTHONPATH=<checkout>/src`. Otherwise tell the human the instrument is not
available. Do not invent its behavior from this skill.

For a new persistent review:

```text
malleus-recon init DIRECTORY --title TITLE --target TARGET_ID --actor ACTOR
malleus-recon record DIRECTORY TYPE RECORD.json --actor ACTOR
malleus-recon validate DIRECTORY
malleus-recon build DIRECTORY
malleus-recon compare DIRECTORY TARGET_ID WORK_ID
```

Read the complete contract and ontology paths printed by the probe before the
first write in a project. The ontology defines the legal record types and
fields. Do not guess them from examples.

Use `pip install malleus-dev[recon]` only when interactive HTML visualization
is requested. Core recording, comparison, and deterministic exports do not
need that optional dependency.

## Research loop

### 1. Register the target and axes

Record one `ReviewTarget` and narrowly defined `ComparisonAxis` records. An
axis should distinguish systems, not merely rename the target claim. Prefer
questions such as "atomic admission of a proposed subgraph" or "knowledge
acceptance separated from action authorization" over labels such as
"governance" or "safety".

### 2. Search from the claim, not from keywords alone

Use available scholarly search and primary sources. Search direct terms,
synonyms, cited predecessors, citations forward, named datasets, linked code,
and patents when priority matters. Record each meaningful query and outcome as
a `SearchEvent`, including searches that fail or reach inaccessible material.

Follow a new branch only when it bears on an active claim or axis. Recursion
stops when a declared boundary is reached, a survey bounds the landscape, a
direct predecessor closes the lineage, or more sources stop changing the
active comparison. Popularity is not a stopping rule.

### 3. Inspect before asserting

Prefer the paper, publisher record, official repository, standard, dataset,
or patent itself. Record a precise locator and access state in an
`EvidenceAttachment`. Distinguish:

- `SOURCE_EXPLICIT`: the inspected source states it.
- `REVIEWER_INFERENCE`: the reviewer derives it from named evidence.
- `NEGATIVE_AUDIT`: a named bounded artifact was inspected and the item was
  not found there.

Never turn a search snippet, abstract alone, or missing search result into a
claim about an entire paper. `NOT_ESTABLISHED` means this review did not
establish the property. It does not mean the property is absent.

### 4. Atomize the paper

Record works, their atomic claims, reported results, and evidence-bearing
relations separately. Do not compare two papers as indivisible blobs. A work
can precede one claim, overlap another, and omit a third.

Use `CENTRAL` or `MATERIAL` only when the axis is genuinely claim-bearing for
that subject. Keep `PARTIAL`, `ADJACENT`, `NOT_ESTABLISHED`, `CONTRADICTED`,
and `NOT_APPLICABLE` visible. Do not promote them to manufacture a cleaner
set result.

### 5. Compare with set algebra, then interpret

For target set `T` and work set `W`, inspect intersection, union, both
directional differences, symmetric difference, partial coverage, unresolved
axes, and contested axes. Use `malleus-recon compare` for the exact recorded
sets. Then write a plain-language explanation tied to the claim and evidence.

The set result is a compact account of reviewer-coded axes. It is not a
novelty score. Network centrality, citation count, graph distance, and date
ordering may guide inspection. None decides scientific priority or novelty.

### 6. Challenge the current position

Before concluding, actively seek:

- the strongest earlier conceptual statement;
- the strongest earlier implementation;
- the closest complete lifecycle;
- evidence that a supposed omission is actually present;
- a date or artifact that changes the chronology; and
- a work whose composition makes the target contribution narrower.

Record contradictions and unresolved branches. Do not reconcile them by
averaging confidence or choosing the preferred narrative.

### 7. Validate and build

Run `malleus-recon validate` before reporting. Run `malleus-recon build` to
emit the graph, evidence table, work-axis matrix, exact comparisons, metrics,
bibliography, readable report, checksums, and deterministic archive. Inspect
the report and at least one exact per-work comparison before handing off.

Rejected candidates stay in the ledger and leave current graph state
unchanged. Fix the candidate or revise the ontology deliberately. Never edit
the JSONL ledger by hand.

## Writing the conclusion

Report three layers separately:

1. **Union:** what the target and prior work share.
2. **Intersection boundary:** the strongest directly overlapping claims and
   implementations.
3. **Differences and unknowns:** what only one side establishes, what is
   partial, and what remains unresolved.

Use bounded language such as "No inspected artifact implemented this exact
lifecycle within the declared corpus and cutoff date." Do not write "No one
has done this" unless a separate proof could support that universal claim.

Chronology and novelty are different questions. Independent arrival can be a
documented chronology statement when dated artifacts support it. It does not
erase prior art, grant priority, or make the contribution novel by itself.

## Where a recon project lives

A recon project is personal working notes: a ledger, its records, and whatever
the build generates. It is not repository content.

Create it under a path the repository ignores, and confirm the ignore covers
it before writing the first record. `git check-ignore -v <path>` answers in one
command. If nothing covers it, add the rule first, then create the project.

Two reasons, and the second is the one that bites. A ledger mid-ingest is a
half-formed thought and committing it publishes a draft nobody finished. And a
repository is not always yours alone: an unignored project directory is picked
up by anyone else's broad `git add`, which is how one landed inside another
session's release commit.

Never stage a recon project by hand either. If it needs to be shared, that is a
decision for the human, made once, with a destination chosen on purpose.

## Hard boundaries

Recon has no crawler, provider integration, automatic truth judge, automatic
novelty verdict, plagiarism detector, or paper-quality ranker. Its local hash
chain detects inconsistent recorded history but is not external notarization.
Caller-supplied source digests are preserved, not independently authenticated.
The local store is single-writer research tooling, not a database service.

If the human asks for a verdict outside those boundaries, present the evidence
and options. The human decides.
