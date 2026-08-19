# Cost-aware model architecture recon

Status: recorded research, not an implemented Malleus capability and not a
paper result.

The evidence project is
[`research/cost_aware_model_architecture_recon`](../research/cost_aware_model_architecture_recon/).
It uses Malleus Recon 0.10.0 as research tooling. It does not change the
paper's frozen Malleus 0.9.0 execution substrate.

## Question

Can typed external memory, deterministic checks, one bounded diagnostic
revision, and selective escalation let a cheaper model tier handle routine
pipeline work at lower expected cost without giving up measurable
reliability?

The bounded answer is: individual components often help, but the complete
claim is not established.

Primary studies report material savings from learned routing, task-specific
harnesses, reusable procedural memory, and selective cascades. Other studies
show that routing, verification, memory, and orchestration can reverse those
economics or reduce reliability. No reviewed evidence establishes that the
complete target architecture lowers lifecycle cost while preserving
reliability against both a strong-only baseline and a simple router.

This is an empirical gap, not a universal novelty result.

## What the literature establishes

### Routing and escalation can reduce cost conditionally

[FrugalGPT](https://arxiv.org/abs/2305.05176) reports large savings from a
learned cascade on its studied tasks and price snapshot.
[TwinRouterBench](https://arxiv.org/abs/2605.18859) reports a trained router
that roughly halves cost at similar task completion in one live evaluation.
The same study reports a rule router that costs more than the strongest single
tier and performs worse. [Is Escalation Worth
It?](https://arxiv.org/abs/2605.06350) identifies the structural cause: a
cascade pays for the cheap attempt before every escalation, while a
pre-generation router can avoid that duplicate work.

The economic question is therefore expected cost per valid completed task,
not price per call.

### Harnesses and memory can move routine work out of the producer

[Better Harnesses, Smaller Models](https://arxiv.org/abs/2607.08938) reports
that task-specific instructions, tools, checks, and control loops close much
of the stronger-tier gap for some repetitive tasks at much lower source-
reported cost. Gains vary by task and base capability.

[MemFlow](https://arxiv.org/abs/2605.03312) directly combines a smaller
producer, intent-routed external memory, deterministic evidence preparation,
validation, and bounded retry. [AgentRR](https://arxiv.org/abs/2505.17716)
records and replays structured experience with check functions. These works
occupy the broad idea of using memory and scaffolding to support a cheaper
producer. They do not establish Malleus's typed commitment, fail-closed
control, or replay semantics, and they do not establish complete lifecycle
cost.

### External diagnostics can make bounded repair useful

[DSPy Assertions](https://arxiv.org/abs/2312.13382),
[Divide-Verify-Refine](https://aclanthology.org/2025.findings-acl.709/), and
[self-debugging with execution feedback](https://arxiv.org/abs/2304.05128)
report gains from executable constraints or localized external feedback.
[Intrinsic self-correction](https://arxiv.org/abs/2310.01798) can instead
degrade performance when no reliable external signal identifies the defect.

The useful unit is a bounded revision after a specific diagnostic, not an
unlimited request to reconsider.

### Replay can save recomputation without proving correctness

[Deterministic execution lineage](https://arxiv.org/abs/2605.06365) reports
large token savings on one update pattern and exact preservation of unaffected
artifacts. It also reports a case where dependency-aware recomputation takes
longer than a simple loop. [Proof of
Execution](https://arxiv.org/abs/2607.05397) evaluates authorization and trace
integrity with small prototype overhead. [SagaLLM](https://www.vldb.org/pvldb/vol18/p4874-chang.pdf)
uses persistent context, validation, checkpoints, compensation, and replay.

These systems support the value of durable execution state. Replay fidelity
does not establish semantic task correctness.

## What can break the architecture

The research spike treats these as falsifiers and design constraints:

1. A strong-only call or simple pre-generation router has lower expected cost
   at the same risk and coverage.
2. Cheap-first escalation duplicates enough work to erase savings.
3. An imperfect checker admits wrong results or rejects correct ones often
   enough to set a lower accuracy ceiling.
4. Verification consumes more compute than producing another candidate.
5. Stored memory is stale, crosses task boundaries, or induces later errors.
6. Orchestration adds handoff, termination, recovery, or context failures.
7. Setup, calibration, drift monitoring, and maintenance do not amortize over
   the actual task volume.
8. Replay reconstructs the trace but not a correct result.

[Inference Scaling fLaws](https://arxiv.org/abs/2411.17501) and
[verifier-guided search scaling flaws](https://arxiv.org/abs/2502.00271) show
why weak or incomplete verifiers are a hard boundary.
[When To Solve, When To Verify](https://arxiv.org/abs/2504.01005) reports that
verification can be less compute-efficient than generating more solutions at
practical budgets. [PersistBench](https://arxiv.org/abs/2602.01146) shows that
long-lived memory can create severe cross-domain and stale-context failures.
[AI Agents That Matter](https://arxiv.org/abs/2407.01502) shows why strong
simple baselines and amortized fixed costs are mandatory.

## Candidate system boundary

The evidence supports testing this composition. It does not authorize its
implementation in Malleus core.

1. An external scheduler selects a routine producer, a stronger producer, or
   a human path. Malleus does not schedule calls.
2. A memory layer supplies typed, source-bound records at a declared cutoff.
3. The producer returns a proposed transaction rather than mutating accepted
   state directly.
4. Malleus runs the proposal-precommitted registered checks and records their
   witnesses. Missing checks fail closed.
5. A nonaccept decision may expose bounded diagnostics for exactly one linked
   revision and recheck.
6. The scheduler may escalate an unresolved result. It may not reinterpret a
   failed Malleus check as acceptance.
7. Durable events retain the proposal, checks, witnesses, decision, revision,
   recheck, and accepted or unresolved terminal state for replay.

This places model selection outside Malleus and commitment control inside it.
The split preserves the current protocol boundary.

## Required evaluation

A future cross-tier study needs at least these matched conditions:

1. Strong-only production.
2. Small-only production.
3. A simple pre-generation router.
4. Cheap-first cascade with the same escalation ceiling.
5. The same router and producer opportunity with external memory.
6. The same system with Malleus commitment and bounded diagnostic revision.

Every started task must remain in the denominator. Report task correctness,
selective risk and coverage, unresolved rate, false rejection, invalid
acceptance, calls, tokens, wall-clock latency, monetary cost, stored bytes,
adapter work, human intervention, recovery work, and recalibration work.
Separate one-time setup cost from per-task cost. Report the break-even task
volume rather than hiding setup cost in a large batch.

The decisive comparison is the strongest simple baseline at prespecified
coverage. Reject the cost claim if the Malleus condition crosses any
prespecified risk, false-rejection, unresolved-rate, latency, or cost limit.

## Relevance to the current paper

The current paper does not test cross-tier routing. Its producer and generation
budget are fixed. The cost-aware literature can justify why a reliable
commitment substrate matters when cheaper producers are used more often, but
it cannot be used as evidence that Malleus saves money.

Paper-safe motivation:

> Making externalized commitments inspectable is not free. Typed staging,
> deterministic checks, durable event history, and replay move work into
> validation latency, storage, integration, and recovery. Malleus therefore
> treats checkability as a cost-constrained systems property: an outcome study
> must hold producer opportunity and information constant, report calls,
> tokens, latency, monetary cost, stored bytes, and adapter work separately,
> and reject an apparent task gain that exceeds prespecified cost or coverage
> limits. The literature motivates this measurement frame; it does not show
> that Malleus is cheaper, faster, or more accurate.

This text is candidate background, not manuscript text and not a new paper
claim. The paper's accepted claim, controls, falsifiers, and version split stay
unchanged. Any paper integration must cite the primary sources, not the Recon
edges, and requires the normal literature and claim-ledger update.

## Nonclaims

This research does not establish that:

1. Malleus is a router, scheduler, memory manager, or model selector.
2. Malleus is cheaper, faster, more accurate, or cost-optimal.
3. The reviewed components are novel individually or as a broad architecture.
4. Executable checks are complete specifications.
5. Replay, provenance, or trace integrity imply semantic correctness.
6. A smaller producer can replace a stronger one on every task.
7. Cost results transfer across workloads, providers, hardware, prices, or
   time.
8. The current paper tests this cross-tier architecture.

## Research artifacts

The canonical evidence lives in the separate Recon project:

* [Frozen scope](../research/cost_aware_model_architecture_recon/scope.md)
* [Evidence synthesis](../research/cost_aware_model_architecture_recon/synthesis.md)
* [Ledger](../research/cost_aware_model_architecture_recon/ledger.jsonl)
* [Generated report](../research/cost_aware_model_architecture_recon/build/report.md)
* [Comparison matrix](../research/cost_aware_model_architecture_recon/build/work_axis_matrix.csv)
* [Graph JSON](../research/cost_aware_model_architecture_recon/build/literature_kg.json)
* [GraphML](../research/cost_aware_model_architecture_recon/build/literature_kg.graphml)
* [Build manifest](../research/cost_aware_model_architecture_recon/build/manifest.json)
* [Tooling provenance](../research/cost_aware_model_architecture_recon/tooling_provenance.json)
* [Visualization status](../research/cost_aware_model_architecture_recon/visualization_status.json)

The deterministic bundle SHA-256 is
`3dc956d7f178e1d3a1fb3f3e93153ee2c2bd314bce485f815a994676a4a2e561`.
Interactive HTML was not generated because the declared optional visualization
dependency is absent from the project environment. No dependency was installed
ad hoc. The canonical JSON, JSON-LD, GraphML, CSV, and ZIP artifacts are
available.

Recon recording establishes typed, replayable review state. It does not
establish source truth, novelty, completeness, or a paper result.
