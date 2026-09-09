# Where Malleus has a useful application case

2026-09-06. Product hypotheses grounded in the current demonstrations, not
customer validation or claims of production readiness.

## Lead with controlled changes, not PDF chat

The clearest pitch is: Malleus separates a proposed knowledge change from an
accepted one, checks it against an explicit domain contract, retains its
evidence and history, and rebuilds the accepted graph for inspection. An LLM
can propose records; its confidence is not the admission rule. Mechanical
admission still does not certify the truth of the source or its interpretation.

It fits best when several producers update shared knowledge, sources change,
mistakes are costly to trace, and users need to know which evidence and rules
produced the present state. A one-off answer to a static document usually does
not justify this machinery.

This is a write-side proposition, not a retrieval replacement. Search or an
embedding index could help find candidate evidence; Malleus would govern which
typed changes enter accepted knowledge. The marine demonstration used no
embedding index. That observation does not show that embeddings are unnecessary
for every application.

## Best application hypotheses

| Application | Concrete user question | Why the protocol may help | Evidence and missing proof |
| --- | --- | --- | --- |
| Versioned technical or operational records | Which supplier specification or accepted correction produced this current value? | Typed proposals, explicit supersession, current state and retained history. | Closest to Core's Small Shop conformance evidence. Real connectors, entity resolution, access control and operating-scale evidence are separate work. |
| Engineering requirements and evidence | Which requirement version does this test support, under which conditions, and what changed? | Connect requirements, configurations, observations and evidence while retaining accepted revisions. | Strong need, but the current missing SUPPORTS/condition structure must be resolved before claiming dependable evidence-chain reconstruction. |
| Shared knowledge maintained by several agents | What did each agent propose, what was admitted, and why did another proposal refuse? | Keep proposal generation replaceable while admission and replay remain inspectable. | Mechanically aligned with current admission/replay. This is governance of knowledge writes, not proof of safe external actions or arbitrary multi-writer execution. |
| Research evidence and technical comparison | Which reported result supports this claim, with which method, sample, units and caveats? | Preserve provenance and distinguish reported observation, estimate and hypothesis. | The marine case demonstrates scoped facts and exposes failures. Cross-paper identity, complete argument capture and expert validation are not established. |

My recommendation is to lead interviews and early adoption discussions with
the first two: a corrected operational fact and an engineering evidence chain.
They make the cost of an untraceable change concrete. Use the agent-maintained
knowledge case as the general protocol story. Present research synthesis as
both a useful application and an honest stress test, not as solved reasoning.

The engineering need is established independently of Malleus. NASA's handbook
describes bidirectional requirements traceability and management of requirement
changes, alongside controlled configuration baselines. This supports the use-case
motivation, not an endorsement or a conformance claim for Malleus.
[Requirements management](https://www.nasa.gov/reference/6-2-requirements-management/),
[configuration management](https://www.nasa.gov/reference/6-5-configuration-management/).

## Choose what a ledger entry means

The application must choose its history model before capture. A source's claim,
an observation and a business state are not interchangeable merely because each
can be stored as a record. The initial seed also needs an identified admission,
not a privileged set of unexplained starting facts.

For operational records, demonstrate a state and its explicit replacement while
retaining both. For engineering evidence, retain the requirement version,
observed configuration, result and qualification of the evidence relation.
For research, distinguish what a source asserts from what an experiment
observes and from what a reviewer accepts. A later publication can contradict
an earlier claim without erasing the fact that the earlier source asserted it.
These are proposed domain modeling rules, not semantics the protocol should
invent from a PDF.

This is where the ontology and semantic ledger meet: define identity, the unit
of change, allowed revision, and what remains historical. The pitch is not a
universal ontology. It is an explicit, inspectable boundary for each adopter's
choices, with shared mechanical admission and replay.

## Why a protocol rather than one application

The proposed benefit is a common acceptance boundary for different producers.
A document extractor, a structured-data importer and a person could propose
changes under the same identified contract without each inventing a separate
history mechanism. Consumers could inspect the accepted graph and evidence
without depending on the producer's private conversation. This is the intended
integration benefit, not a measured reduction in engineering effort.

The protocol does not replace the storage engine, domain model or source
review. Nor does a Python reference path alone prove interoperability between
independent implementations. A convincing later adoption test would introduce
a second independently implemented producer while keeping the admission and
replay contract fixed, then measure the integration work and failure behavior.

## What we must concede

Provenance, versioning and policy logs are not new. W3C PROV already models and
supports interchange of provenance, including derivation and versioning.
OpenLineage models jobs, runs and datasets with runtime and design-time lineage
events. OPA decision logs already retain policy queries, inputs and policy
bundle revisions for audit and debugging. Malleus must be compared to these
honestly, not to an imaginary world without audit trails.
[W3C PROV overview](https://www.w3.org/TR/prov-overview/),
[OpenLineage object model](https://openlineage.io/docs/spec/object-model/),
[OPA decision logs](https://www.openpolicyagent.org/docs/management-decision-logs).

The specific engineering proposition to demonstrate is their composition around
typed, evidence-bound changes to domain knowledge: compile a contract, propose
a change, check and admit it, retain history, discard live state, replay, and
query exact witnesses. This is a claim about an implemented path, not a claim
that no other system can compose comparable mechanisms. An ordinary database
with schemas, transactions and provenance may be enough for a particular user.

## Convince with one visible correction

A convincing demo should let the audience follow one value from a source to a
typed proposal, through an accepted update or a refusal, into a queryable graph.
Then show the old and current states and their evidence after replay. For the
document path, expose one successful relation and one missing one instead of
claiming that every grounded-looking answer is correct.

Measure what the proposed benefit would actually change: engineering work to
integrate a second producer, ability to reconstruct a disputed update, retained
source/role/qualifier fidelity, and behavior on invalid proposals. We have not
measured deployment cost, operational scale, user productivity or commercial
demand. Those are validation targets, not numbers for the pitch.

Do not lead with autonomous clinical, legal or trading decisions, universal
compliance, guaranteed hallucination prevention, unrestricted multi-document
reasoning, or replacing all RAG. Do not promise a durable cross-language wire
or production service from the repository-local research evidence.
