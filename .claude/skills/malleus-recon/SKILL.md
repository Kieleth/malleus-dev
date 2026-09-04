---
name: malleus-recon
description: Evidence-first literature and paper forensics with a typed knowledge graph. Use for prior-art and related-work analysis, closest-work comparison, paper or dataset lineage, novelty boundaries, recursive citation exploration, literature knowledge graphs, set comparisons across technical claims, or source-grounded literature-to-design reinforcement. Use the shipped malleus-recon ledger and exports when persistent local research artifacts are wanted. Never use graph structure or scores as an automatic novelty, truth, plagiarism, quality, or adoption verdict.
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
`EvidenceAttachment`. On every reviewed relation, distinguish:

- `SOURCE_EXPLICIT`: the inspected source states it.
- `REVIEWER_INFERENCE`: the reviewer derives it from named evidence.
- `NEGATIVE_AUDIT`: a named bounded artifact was inspected and the item was
  not found there.

Never turn a search snippet, abstract alone, or missing search result into a
claim about an entire paper. `NOT_ESTABLISHED` means this review did not
establish the property. It does not mean the property is absent.

`Claim` and `Result` records can name evidence but do not currently carry this
status or a basis. Put the provenance-qualified analytical assertion on the
relation instead of inventing fields the schema does not declare.

### 4. Atomize the paper

Record works, their atomic claims, reported results, and evidence-bearing
relations separately. Do not compare two papers as indivisible blobs. A work
can precede one claim, overlap another, and omit a third.

Use `CENTRAL` or `MATERIAL` only when the axis is genuinely claim-bearing for
that subject. Keep `PARTIAL`, `ADJACENT`, `NOT_ESTABLISHED`, `CONTRADICTED`,
and `NOT_APPLICABLE` visible. Do not promote them to manufacture a cleaner
set result.

No coverage record means the subject is unassessed against that axis. It does
not mean `NOT_ESTABLISHED`. Record `NOT_ESTABLISHED` explicitly, with basis and
evidence, when that is the review finding.

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
bibliography, readable report, checksums, and an archive deterministic for the
manifest's declared input, ontology, generator, and runtime closure. Use a
fresh CLI process if implementation source files changed during the current
Python process. Inspect the report and at least one exact per-work comparison
before handing off.

Manifest v3 binds the registry's exact source closure, all authored import
resolutions, retained definition owners, the JSON-LD term map, and separated
grammar and migration verification evidence. Canonical ontology locators are
absolute, so moving the same ontology bytes changes exact build identity even
though the structural ontology hash remains unchanged. Treat that as declared
provenance, not drift to normalize away.

Rejected candidates stay in the ledger and leave current graph state
unchanged. Fix the candidate or revise the ontology deliberately. Never edit
the JSONL ledger by hand.

## Governed promotion

Recon is the structural capture authority for its own project. `RECORDED`
means the candidate passed the Recon ontology and replay rules. It is not an
Assent decision, an accepted-history write, or permission to act.

There is no shipped promotion command yet. Do not imitate one by writing the
same result to both ledgers, by mapping `REVIEWED` to an Assent `ACCEPT` verdict
or `ProposalState.ACCEPTED`, or by calling private compiler or change-set
modules. Until the public governed-promotion adapter exists, prepare a reviewer
handoff and leave core state unchanged.

A future promotion attempt must select records from one validated Recon
snapshot. Bind the structural-capture profile, project and ledger wire,
record-event and replay-validator identities, exact project bytes, current
ontology hash, the separated grammar and migration identities verified during
the read, every crossed migration-receipt identity, ledger head and event
count, selected event and record hashes, and the complete evidence and endpoint
dependency closure. Also bind the current `ReviewTarget` and every
applicable `ReviewBoundary` and `SearchEvent`, the selection policy,
source-to-target mapping, target contract, and admission profile.

For the current public Assent path, also bind the target graph ontology hash,
`GraphBaseArtifact` ID and content hash, acceptance head, materialization head,
state digest, and exact `EpistemicPolicyArtifact` ID and content hash. Policy
applicability remains the adopter's responsibility. A receipt must be source
provenance of the candidate, not a detached side file. If represented by a
`SourceArtifact`, it records the receipt byte identity and locator, not the
bytes themselves; retain the exact bytes at that locator. The proposal must
bind the receipt-bearing `CandidateSubgraphArtifact.content_hash`, because
`candidate_digest` and `artifact_hash` do not include `source_record_ids`.

Missing or merely caller-declared evidence properties remain explicit
limitations and must cause refusal when the target contract requires stronger
evidence. A later Recon revision creates a new promotion attempt; it never
silently rewrites an earlier governed record. Recon has no typed promotion
outcome record, so do not write target outcomes back into Recon under an
unrelated type.

## Literature-to-design handoff

When the recon is meant to reinforce a protocol or implementation, follow the
comparison with a source-grounded transfer handoff. This is a reviewer report,
not a new Recon record type and not authorization to change core.

For each candidate transfer, state:

1. `SOURCE_MECHANISM`: Cite the applicable work, claim, and evidence records or
   their precise locators, then state the source mechanism and what the
   inspected evidence establishes. Cite a result record only when the source
   establishes one. When no result was established, say so explicitly rather
   than requiring or inventing a result record.
2. `ASSUMPTIONS_AND_THREAT_MODEL`: State the source's assumptions and threat
   model, including anything the inspected evidence does not establish.
3. `REUSABLE_TECHNIQUE`: Name the bounded technique that could transfer.
4. `FAILURE_BASELINE_OR_ORACLE`: Record any failure case, baseline, or
   independent oracle the source supplies.
5. `TARGET_BOUNDARY`: Name the existing Malleus role or boundary and current
   consumer the transfer could serve. If neither exists, say so rather than
   inventing an extension point.
6. `EXCLUDED_TRANSFER`: State what must not transfer because its assumptions,
   scope, or semantics differ.
7. `SMALLEST_EMPIRICAL_TEST`: State the smallest empirical test that could
   support or reject the transfer.

Present each item as a proposed `ADOPT`, `COMPOSE`, `REFUSE`, or `DEFER`
candidate with a short reason. `ADOPT` reuses the bounded mechanism at an
existing boundary. `COMPOSE` combines it with existing mechanisms while
preserving their contracts. `REFUSE` records a demonstrated mismatch. `DEFER`
keeps a useful possibility outside the current slice until evidence, a role,
or a consumer exists. The human chooses the disposition. A transfer remains
proposed until that decision and does not become implemented merely because it
appears in the handoff.

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
