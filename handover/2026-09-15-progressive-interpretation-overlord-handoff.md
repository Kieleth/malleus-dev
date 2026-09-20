# Maintaining interpretations as evidence accumulates

15 September 2026. Author-approved direction and coordination request from the KGs research session. The requirement and three-case research plan are accepted. Runtime mechanisms, new public contracts and individual INDRA transfers are not thereby approved.

## Author instruction

Luis: “maintaining interpretations as evidence accumulate” must be in the skill and start to be enforced. He accepts the research plan and asks Overlord to coordinate Core, paper, skills and other sessions around this missing process.

## The requirement

Malleus acquisition maintains interpretations as evidence accumulates. It does not merely turn successive blocks into independent records.

Retain the evidence unchanged. Interpret it using the relevant source context, ontology and current knowledge. Preserve specific unresolved questions without guessing required fields. At declared reading or evidence-change boundaries, reconsider affected earlier interpretations, including ones previously considered complete. Record a supported correction, justified no-change, conflict or specific remaining uncertainty. Review alone changes no accepted knowledge. Any accepted change still passes through the selected admission policy, preserves history and identifies affected downstream uses.

This does not require every number to become a node or every uncertainty to become a probability. Source assertion, interpretation confidence, scientific support, measurement uncertainty, applicability, policy acceptance and adequacy for a use are distinct. More evidence can expose mistakes or increase uncertainty. Reading order is not world time.

Distinguish acquiring detail, correcting an interpretation and representing a change in the world. Citation, attribution, scientific support and refinement are not interchangeable relationships. Registering new evidence or completing a reading pass does not prove that earlier meanings were reconsidered.

## Why this is a project issue

The earlier vision exists. [Intellectual Substrate, section 4.3](../design/MALLEUS_INTELLECTUAL_SUBSTRATE.md) explicitly identifies dependency-closed revision and evidence-triggered revalidation as missing general mechanisms. [Semantic-log design](../design/SEMANTIC_LOG_KNOWLEDGE_PROJECTION.md) discusses evolving meanings and justifications. Those are design intent, not shipped guarantees.

The active [Acolyte skill](../.claude/skills/malleus-acolyte/SKILL.md) already distinguishes attempted work from substantive completion. Its step 9 grows the ontology from recorded structural gaps. That is insufficient when a legal representation assigns the wrong subject or loses a qualification without recording a gap. The document adapter retains evidence and gaps; it does not select earlier interpretations for reconsideration. The ledger preserves accepted changes; it does not decide what a new passage means.

## First coordinated deliverables

1. **Core owns the shared-skill update.** Extend the existing acquisition and completion guidance with the requirement above, keeping one source of truth. Make the domain-neutral rule available on skill reload. Route from development guidance where necessary; do not paste marine answers into general instructions. Check the installed skill as well as repository text. Do not silently alter the isolated 0.15.0 release candidate.
2. **Start enforcement with a bounded behavioral check.** Use generic staged evidence, not PDF answer values. Show an unresolved reference becoming resolvable and an already-completed interpretation becoming review-relevant. A completion claim with an outstanding declared review obligation must fail. A justified unchanged or still-unresolved disposition remains legitimate, with its limitation visible. Reaching a retry budget is not semantic completion. New evidence alone must not mutate accepted state. A wording-presence test can protect distribution, but is not this behavioral check.
3. **KGs owns the three thought experiments below.** First compare minimal representations, then test the chosen representation and reader obligations. Preserve the frozen paper evidence. No new full-document capture is implied.
4. **Paper and other consumers receive the requirement and boundaries.** Paper owns acquisition and semantic evaluation. Shop, Robotics, Semantic Re-entry, Recon and code consumers should identify analogous obligations in their own workflows, without importing the paper schema or changing their current scope automatically. Overlord coordinates shared needs and any follow-up decision.

For the first behavioral check, full review of a small declared interpretation set at each evidence boundary is sufficient. Do not invent a general relevance engine, scheduler or truth-maintenance service. If no existing surface can enforce the check, report that exact missing mechanism and propose the smallest placement before creating a Core contract. Mechanical enforcement can detect skipped review, stale declared dependencies or a missing disposition. It cannot certify arbitrary source meaning, discover every undeclared dependency or guarantee model compliance.

Please acknowledge the owners and first atomic deliverable, then return the actual changed paths and failing-then-passing test evidence. Until that exists, report **skill update requested**, not **enforced**. Keep research recommendations, approved direction and implemented behavior separate.

## Accepted thought-experiment plan

**GE-1: estimate, application and reference resolution.** The body at `page:2:block:006` already attributes 5.4 ± 0.3 km to western-flank crust and reference 32. The caption at `page:7:block:011` applies the estimate beneath RC2. The bibliography at `page:9:block:036` resolves the publication identity. Later reading should connect these roles, not invent an RC2 measurement, count a second independent measurement or claim the cited study was inspected. Compare the minimal origin/use/attribution representation first. One reader retrieves origin; another explains application.

**GE-2: a conditional model statement.** `page:5:block:006` relates a CO2 threshold, pressure, temperature, a reported depth correspondence and predicted degassing. Four quantities sharing a locator do not by themselves encode their joint roles. One reader must recover the qualified prediction; another must distinguish retrieving a reported value from calculating a new one. Missing equations or conversion assumptions cannot be supplied silently.

**GE-3: publication identity, attribution and argument.** A bibliography entry identifies a work. It is not itself scientific evidence for the article's whole hypothesis. Readers must distinguish citation, attribution of the estimate and its use as one premise in a scoped argument. Changing a premise requires reconsidering its dependent argument, while any genuinely independent justification remains separate.

These are controlled research cases, not evaluator-authored population, executed model results or new paper scores. The reading stages are proposed experimental inputs, not a reconstruction of an earlier model's internal process.

## Evidence and research packet

Read the [research index](../private/kg-representation-recon-2026-09-15/README.md), [progressive-interpretation study](../private/kg-representation-recon-2026-09-15/PROGRESSIVE-KNOWLEDGE-THOUGHT-EXPERIMENTS.md), [Astra's INDRA study](../private/kg-representation-recon-2026-09-15/indra/INDRA-TRANSFER.md), then the [first representation audit](../private/kg-representation-recon-2026-09-15/RESEARCH.md) as needed. These are local ignored research, not publication artifacts. Do not stage them implicitly.

INDRA supplies useful precedents for partial statements and separating captured meaning from model-construction assumptions. Its refinement hierarchy is not scientific support or correction; its confidence machinery is not a truth certificate. The inspected incremental module did not establish the accountable reconsideration workflow we need. Official documentation and rendered source were inspected, but no exact INDRA source commit or executed integration was established. Proposed static counterexamples remain unexecuted.

The [marine audit snapshot](../private/kg-representation-recon-2026-09-15/audit-snapshot.json) binds the exact source reading, ontology, exported records, history, replay receipt and query result. Paper remains frozen to Core `c95dba7b86bb61487bda9a52458e1ea47cce20ab`. This coordination is not a rebind request. The research produced no accepted graph change and ran no new capture. No shared skill or Core runtime was changed by this session.

## Ownership and routing

- KGs research: `01a0a5c7-8275-75e3-bd31-0958b7417d15`.
- Malleus Overlord: `01a0a228-9e0b-76c1-a498-eccd6ea60034`.
- Malleus Core, shared runtime and skills: `01a02f71-fec6-7382-9c68-c3efd3dba5d4`.
- Draft lean Malleus arXiv paper (2), original PDF: `01a0a290-234e-7c12-90e4-41085bba10cf`.
- Malleus arXiv MultiDOC-RAG, separate paper research: `01a063a6-2b96-7cf1-bb53-1df3c6df63ba`.

Overlord should resolve the remaining live consumer sessions before notifying them. Awareness is not permission to rebind experiments, broaden implementation, publish, or change another owner's plan.

## Resume checkpoint: research-only ownership and proposed transfer

Checked on 15 September 2026 after the author's ownership clarification. This
section supersedes any earlier wording assigning executable validation to KGs.
KGs owns research, meaning requirements, proposed relationships, counterexamples
and interpretation of results. Paper owns executable scientific experiments and
accepted amendments; Shop owns its fixture and consumer work; Core owns generic
runtime and shared skills. Overlord coordinates only the necessary owners.

### Recoverable state

- Checkout: `/Users/luis/Projects/malleus-dev`, branch `main`, commit
  `18015352e2eb5bffbb58125c95de40eba0f4c992`, tree
  `04b6ee7b6a0417e5eb7b31d381625c456bfabe3a`. The shared checkout is dirty;
  that commit does not include the uncommitted research and Paper work.
- This owned handover is untracked. The research directory
  `private/kg-representation-recon-2026-09-15/` is ignored. Preserve it in full:
  README, RESEARCH, PROGRESSIVE-KNOWLEDGE-THOUGHT-EXPERIMENTS, the three GE-1
  reports, `ge-1.proposed.yaml`, `test_ge1_schema_contract.py`,
  `audit-snapshot.json`, `indra/INDRA-TRANSFER.md`, Recon project/candidate
  files, `ledger.jsonl` and `build/` evidence/export files. GE-2 and GE-3 remain
  in the thought-experiment document, not separate implemented experiments.
- GE-1 draft 0.0.2 SHA-256:
  `78cbe173e6c0ae21019f773657ac1dece026aa97bb2a1d0f1239683dd02848d3`.
  Its historical static-test file SHA-256:
  `a5e167daea6c729c5d11b94177bc02a85f65bf5ed1b686f1e3b2786c3962eb05`.
  The previously reported four passing tests protect declarations and ancestry,
  not compiler support, reader behaviour or model understanding. None rerun now.
- External private inputs needed to resume:
  `private/paper-v4-relationship-repair-01/producer/inputs/`, including the
  selected reading and complete frozen ontology/import closure, and its
  `accepted/` records, ledger, replay receipt and query result. All six file
  digests in `audit-snapshot.json` were rechecked and match. Paper's frozen Core
  coordinate remains `c95dba7b86bb61487bda9a52458e1ea47cce20ab`.
- The optional review-checker candidate still exists locally at
  `/private/tmp/malleus-progressive-guidance.uxhila/repo`, commit
  `25f94cbf0fe84a9a66b1511deb9b8a99b4c32709`. Its location is temporary, not a
  preservation guarantee. Recover its exact Core-owned coordinate and artifacts
  through Core before any selected use; this checkpoint does not adopt it.

No KGs run is active. This checkpoint changes only this handover. No compiler,
reader, model, test suite, accepted population or runtime was executed or
selected. No stash, reset, staging, commit, push or source mutation was performed.
Existing unrelated work remains untouched.

### Smallest meaningful progressive-interpretation test

Research recommendation, not a selected execution plan: use two exact evidence
boundaries, a small declared set of interpretation versions and two fixed reader
obligations. Retain the actual first interpretation before revealing the second
input. At the second boundary, require reconsideration of every declared target,
including completed ones. Distinguish new detail, correction, conflict,
justified no-change and a remaining unknown. Preserve original evidence and prior
interpretations; review alone admits nothing.

Include one question later evidence can resolve, one established interpretation
that must be checked again without gratuitous rewriting, and one unknown the
later evidence does not resolve. These are investigator-side expectations, not
answers or mandatory review outcomes supplied to a model. A model that was wrong
initially may require correction rather than the expected no-change; assess its
actual output, not a prewritten trajectory.

The primary semantic falsifier is an unsupported strengthening after new
context: an attribution becomes proof, an unresolved balance becomes permission,
or an application becomes a second measurement. The procedural falsifier is a
claim of current review completion with an omitted target or a review bound to
the old evidence. Passing the accounting check while failing the semantic test
is a failed meaning-preservation result, not a successful learning cycle.

Scripted reviews test the mechanics of identities, stale/missing reviews and
completion. Synthetic graphs test whether chosen representations and readers
preserve a distinction. Neither demonstrates model reconsideration. That needs
retained model-produced first-stage interpretations, genuinely withheld later
evidence, the model's subsequent dispositions and independent source-grounded
assessment. One successful run is a case result, not proof of general improvement.

### A faithful but limited Shop analogue

Inspected existing `connected_story/sources/table-1.jsonl` and `context.jsonl`,
plus `SHIPMENT_EXPLANATION.md`. Their current source SHA-256 values are
`37fab6c52bcc05e5fca08be67ef779fa27bfa8c960ccdee0f341e70166c8907c` and
`eab62357c1f41b049bd5a4f6c1589abaaed1559cb6f572912af986c2f9538525`.
No Shop files changed or tests ran during this inspection.

One proposed case keeps the same historical table throughout and later adds its
retained prose context. This is an investigator-selected reading order, not an
assertion about publication order, business time or when the original system
knew something. Exact extracts and required headings remain Shop-owned inputs.

| Interpretation | Table first | After the relevant retained prose |
| :--- | :--- | :--- |
| What P1 connects | e29 records receipt; e30 records clearing I1 and I2 with P1. | Review again. The connections remain; prose adds that P1 covers both invoices. Do not merge receipt and clearing into one event. |
| Why the orders are related in the shipment explanation | The table alone does not supply the shared-customer scope or stated policy explanation. | `intro-1-customer`, `intro-7-policy` and `intro-7-payment` supply one unnamed customer, a rule and the author's explanation for O2's delay. Preserve the attribution. |
| Whether shipment eligibility is established for the complete customer account | The account and explicit unpaid-status inventory are incomplete. | They remain incomplete. Report that limitation, not a newly proved authorization or independently established cause. |

This can test contextual joining, reconsideration, justified no-change and
persistent unknowns without adding a new world event. Merely replaying B's e4/e7
quantity change or comparing graph checkpoints before and after payment is not
that test. The existing shipment explanation already uses all retained context;
its historical checkpoints cannot be relabelled a staged acquisition experiment.

No concrete research objection to one such bounded Shop case followed immediately
by GE-1, if Luis selects that order and the Shop owner confirms the inputs. The
objections would be expanding it into another Shop milestone, importing complete
context into its first stage, or claiming Shop success establishes the scientific
distinctions below. No new Core capability gap is demonstrated by this proposal.

### GE-1 transfer acceptance criteria

Shop can exercise the procedure. GE-1 must still establish these domain-specific
distinctions with the selected B approach and two fixed readers:

1. Return original estimate scope separately from its later application target.
   Equal numbers do not establish either identity or independent measurement.
2. Distinguish a source-local reference, its containing article and the publication
   it resolves to. Resolution establishes neither direct inspection nor scientific
   support. Ambiguous and unresolved references must remain visible.
3. Preserve reported numerical uncertainty separately from approximation in the
   application. Do not invent a confidence interval, observation date or transfer
   calculation. Citation resolution does not improve scientific confidence.
4. Preserve direct source statements separately from the supported synthesis that
   the caption applies the body estimate. The available passages establish no
   second independent measurement; they do not prove one never occurred.
5. Respect the actual reading boundary. The body already states western-flank
   origin and argumentative use. The caption refines context; the bibliography
   resolves identity. Neither may be leaked into an earlier-stage interpretation.

Shop business rules cannot establish geological applicability, measurement
uncertainty semantics, scientific premise support or the distinction between a
cited study and one actually inspected. GE-2's joint conditional statement and
GE-3's support argument remain necessary research cases, not implied successes.

No unresolved semantic choice prevents writing these bounded criteria. Concrete
schema adoption, exact runtime/input selection and experimental authorization
remain separate decisions. The old bibliography record's lifecycle stays Paper's
separate decision, not a blocker to non-accepted synthetic tests.

### Next decisions and actual remaining work

Luis has selected B, not yet the proposed Shop-first order. Overlord should present
that order and its bounded deliverables without reopening A versus B. Executable
owners must then obtain the required approval for concrete inputs, schema/runtime
selection and each model trial. Current authorization here is preservation and
research-only planning, not execution.

KGs next supplies or clarifies meaning requirements and counterexamples, then
interprets results returned by the executable owners. The underlying outstanding
claim remains whether a model actually maintains better contextual interpretations
as evidence accumulates. No current artifact proves that claim.
