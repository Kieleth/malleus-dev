# Malleus Recon contract

Malleus Recon is a local, evidence-first protocol for inspecting a paper,
technical claim, or research theme against its literature. It records what a
source says, what a reviewer infers, how works overlap, and what remains
unresolved. It does not decide novelty or truth.

## Exact claim

Given a declared review target and a bounded set of inspected sources, Recon
can preserve evidence-linked works, claims, results, comparison axes, search
events, and review boundaries in a typed append-only ledger. It can rebuild a
current graph, reject malformed or unsupported records, and generate
deterministic comparison artifacts from the recorded state.

## Smallest observation

A valid miniature review must be able to:

1. record one target, two works, their source evidence, and shared axes;
2. reject an unsupported comparison without changing current graph state;
3. revise a recorded comparison while preserving the earlier event;
4. rebuild identical JSON, JSON-LD, GraphML, CSV, and Markdown outputs; and
5. report intersection, union, target difference, work difference, and
   symmetric difference without calling any of them a novelty verdict.

## Existing artifact reused

The local literature-forensics package is the reference corpus. Its generic
ideas are reused: atomic works, claims, results and concepts; evidence-bearing
relations; priority-date provenance; bounded recursive exploration; matrices;
set comparison; deterministic exports; and a manifest. Its paper-specific
axes, conclusions, prose, and hard-coded compiler are not library behavior.

## Explicit exclusions

The first release does not:

- crawl the web or require a particular search provider;
- download or redistribute paper full text;
- infer novelty, plagiarism, copying, intent, or paper quality;
- treat `NOT_ESTABLISHED` as proof of absence;
- treat a structurally recorded claim as true;
- rank papers with a single novelty score;
- provide a database server or multi-writer protocol; or
- externally notarize the local ledger.

The shared Malleus ledger detects truncation, reordering, and inconsistent
local history. Without an external anchor, it does not prove that a party with
filesystem access could never replace the ledger and recompute its hashes.

## Two layers

The `malleus-recon` skill carries the research procedure: claim-conditioned
search, source inspection, recursion rules, cautious comparison language, and
stopping criteria. The `malleus.recon` module carries deterministic mechanics:
typed recording, replay, validation, graph projection, set algebra, matrices,
reports, and exports.

The skill may use whatever research tools are available in its environment.
The Python module remains provider-independent and makes no remote calls.

## Record meanings

`RECORDED` means the candidate passed the Recon ontology and local integrity
rules. It does not mean the candidate is empirically true. `REJECTED` means the
candidate and its exact validation errors remain in the ledger but do not
change the current graph.

Every reviewed analytical statement distinguishes:

- `SOURCE_EXPLICIT`: the inspected source states or directly links it;
- `REVIEWER_INFERENCE`: the reviewer derived the comparison from evidence; or
- `NEGATIVE_AUDIT`: the reviewer inspected a named bounded artifact and did
  not find the item there.

Comparison coverage uses `CENTRAL`, `MATERIAL`, `PARTIAL`, `ADJACENT`,
`NOT_ESTABLISHED`, `CONTRADICTED`, or `NOT_APPLICABLE`. Only `CENTRAL` and
`MATERIAL` enter the default set comparison. Partial and unresolved findings
remain visible alongside it.

## Revision

A record identifier is stable. A later event may replace its current value
only when it names the latest recorded event for that identifier. The ledger
keeps both events. A rejected revision leaves the earlier current value
unchanged.

This is transaction history, not publication history. Work records preserve
first-public, issue, revision, or other date evidence separately.

## Source boundary

An evidence attachment records a URI or local path, an in-source locator, a
description, source class, access state, and access date. When a local artifact
digest and length are supplied, Recon preserves those values. A future ingest
adapter may compute them from bytes it reads. Merely recording caller-supplied
values does not authenticate remote content.

## Recursive exploration

Recon follows a citation or concept branch only when it bears on an active
target claim or comparison axis. Each search event records the query, reason,
and outcome. Exploration stops when a declared boundary is reached, a survey
provides an explicit landscape boundary, a direct predecessor closes the
lineage, or additional sources no longer change the active comparison.

Unsuccessful searches, inaccessible sources, aliases, and unresolved branches
are data. They must not disappear from the research account.

## Set comparison

For target axis set `T` and work axis set `W`, where set membership means
`CENTRAL` or `MATERIAL`, Recon reports:

- intersection: `T ∩ W`;
- union: `T ∪ W`;
- target difference: `T − W`;
- work difference: `W − T`; and
- symmetric difference: `(T − W) ∪ (W − T)`.

These are exact statements about the reviewer-coded profile. They are not
statements about everything a paper could contain.

## Files and commands

A Recon project contains `project.json` and `ledger.jsonl`. Generated files go
under `build/`; the ledger remains the authority.

The first CLI surface is:

```text
malleus-recon init DIRECTORY --title TITLE --target TARGET
malleus-recon record DIRECTORY TYPE RECORD.json --actor ACTOR
malleus-recon record DIRECTORY TYPE RECORD.json --actor ACTOR --supersedes EVENT_ID
malleus-recon validate DIRECTORY
malleus-recon build DIRECTORY
malleus-recon compare DIRECTORY TARGET_ID WORK_ID
malleus-recon visualize DIRECTORY
```

`build` emits canonical JSON, JSON-LD, GraphML, node and edge CSV files, a
work-by-axis matrix, a Markdown report, and a checksum manifest. Interactive
HTML visualization requires the `recon` optional dependency set.

## Acceptance boundary for version 0.1

The release is complete only when a synthetic fixture demonstrates recording,
rejection, revision, replay, comparison, and deterministic generation. The
larger local literature graph then serves as a migration and usability corpus,
not as a package test fixture or as an encoded conclusion.
