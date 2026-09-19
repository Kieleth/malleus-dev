# Rules inside the ontology and the semantic ledger: findings

ROADMAP item F4, research pass. 2026-09-19. Findings only; nothing in this
repository was changed, staged or committed to produce it.

The question, in Luis's words on 2026-09-19 (paper ledger E-0486, ROADMAP F4):

> if rules live "outside" the ontology+semantic-ledger+KG then it gets more and
> more complicated to integrate, since we need to integrate two different
> systems and carry ids/hashes, etc... the vision is that an extended ontology,
> maybe the ones we discovered that are closer to be instances of things rather
> than generic definitions or even in PROV-O we could define these rules
> within-system, not as external ones, but we might have to support both I fear.

And, as ROADMAP F5:

> we should have a "versioned ontology evolving" where rules automagically get
> "converted" as changes in the ontology happen, automagically detecting that
> changes in the ontology can produce the same rules.

Acronyms used once and then reused: **KG** knowledge graph. **LinkML** Linked
Data Modeling Language, the YAML schema language Malleus compiles.
**SHACL** Shapes Constraint Language, the W3C standard for validating RDF.
**RDF** Resource Description Framework, the W3C triple data model. **OWL** Web
Ontology Language. **ShEx** Shape Expressions. **SPARQL** the W3C RDF query
language. **PROV-O** the W3C Provenance Ontology. **SPIN** SPARQL Inferencing
Notation. **N3** Notation3. **SWRL** Semantic Web Rule Language. **AF**
Advanced Features (the SHACL extension note). **OWA/CWA** open-world and
closed-world assumption. **W3C** World Wide Web Consortium. **REC / WD / Note**
Recommendation, Working Draft, and Working Group Note: the W3C's standard,
draft, and non-standard-track document statuses.

---

## 1. What Malleus decided before, and why

This has surfaced four times in decisions, and a fifth time as a recon project
whose findings are used in section 3.4. Two of the four point the opposite way
from what shipped, which is the single most useful fact in this document.

### 1.1 The delimitation ruling: rules should be KG citizens

`docs/DELIMITATIONS.md`, section "Guardrails for future design" (line 217),
which opens "Standing orders for anyone (human or assistant) designing the
planned extensions. Each names what must be engaged before designing, what to
adopt, and what the actual contribution is." At lines 241-247:

> **Axioms and domain rules as data.**
> Engage first: SHACL shapes-as-data, SPARQL 1.2 RL (WD, moving), and N3.
> Adopt: representation mappable to SHACL/SRL rather than a bespoke rule
> vocabulary. Contribution: the pinned-contract lifecycle (rules as gated,
> versioned, hash-identified KG citizens whose acceptance is itself
> ontology-checked), not the rule formalism.

Read it plainly. The recorded position is that the contribution is the
*lifecycle*, not the *language*, and that rules are meant to be **KG citizens**
whose acceptance is itself ontology-checked. That is Luis's F4 vision, written
down before F4 was asked. It was never built. What shipped is a Prolog file
beside the graph whose acceptance is not ontology-checked at all.

The same file, lines 102-107, states the novelty claim the current build does
support:

> **Hash-pinned rule contracts.** The rules lineage, including SWRL, SPIN,
> SHACL-AF, and SPARQL 1.2 RL, treats rules as inference producers or
> constraint bodies. No exact match found in the current comparison set gives a
> rule set a pinned identity, binds that identity into the check record, and
> evaluates it against isolated candidates.

And lines 133-140 carry the formalism-by-formalism verdicts already taken:
OWL 2 **Reject** ("Open world plus no unique-name assumption: a missing
required property is 'unknown,' not a violation"); SHACL Core **Inherit**;
ShEx **Note**; SWRL and SPIN **Note** ("Legacy; SPIN formally superseded by
SHACL ... Lineage material only"); N3 plus the EYE reasoner **Note**
("Rules-as-data in a live non-Rec ecosystem; open-world defaults"); and, for
PROV-O:

> | Named graphs + PROV-O | RDF 1.1 datasets; PROV-O Rec 2013, stable |
> **Reuse (map onto).** Staged candidates are named-graph-shaped; acceptance
> events are PROV activities. PROV is passive vocabulary; malleus makes the
> structure a condition of materialization. |

"PROV is passive vocabulary" is the answer to the PROV-O half of the F4
question, decided and recorded. Section 3 below confirms it against the
specification rather than restating it.

The evidence behind those verdicts is `paper/research/1-owl-shacl-rules-stack.md`,
87 lines, primary sources per formalism. Its conclusion on the whole rules
lineage:

> Whole lineage (SWRL -> SPIN -> SHACL-AF -> SHACL 1.2 Rules) treats rules as
> inference producers or post-hoc constraint bodies. None gives rules pinned
> identity (exact bytes hashed) or evaluates against isolated pre-commit
> candidates. Malleus's pinned Prolog contracts have no analog here.

### 1.2 The North Star ruling: a rule in a source is knowledge, not a check

Paper ledger `paper-v4/paper-ledger.md`, entry **E-0457** (2026-09-17), after
Luis read the Shop run end to end. Luis's observation, recorded there: the Shop
prose shows a source can carry evidence, a rule, and ontology-level content at
once, and

> "we cannot have an ontology phase and a population one, the population one
> should be able to put the ontology one at any given time when needed".

The ruling recorded in the same entry:

> a rule in the source is knowledge about a rule, not a live check, and
> promoting it is a deliberate act by a named decider, or a document could
> install its own gate, so the missing piece is a check with provenance, a
> policy rule whose source is a claim in the ledger; the separation of contract
> and tuple stays because a check reads the contract, so the shape is two
> transaction kinds in one ledger, ordered (revise, re-pin, admit) with the gap
> as the honest stop between them.

Three commitments in one sentence, and they bound every option in section 4:

1. A rule may live in the KG as a record. It is then **knowledge about a rule**.
2. Turning that record into a **live check** is a deliberate recorded act by a
   named decider. It does not happen because the record exists.
3. **The separation of contract and tuple stays, because a check reads the
   contract.** A check cannot be a tuple in the graph it checks without
   answering what it means for a check to check itself.

Point 3 is the constraint that rules out the most attractive-sounding option.

The live instance already exists. In the Shop's third round the producer
captured the source's shipment policy as a record, not as a rule
(`private/shop-progressive-01/producer/workspace-stage-c/inputs/context.yaml`,
lines 13-35):

```yaml
slots:
  maximum_unpaid_invoices:
    range: integer
    required: true
    minimum_value: 0
    description: Source-stated per-customer threshold, not a calculated account status.
classes:
  ShipmentRuleClaim:
    is_a: ShopContextClaim
    slots: [maximum_unpaid_invoices]
```

Paper ledger E-0451 records what was admitted: "a ShipmentRuleClaim with
maximum_unpaid_invoices 1, RULE_CUSTOMER_SCOPE to the shared-customer claim,
DELAY_PAYMENT and DELAY_INVOICE to P1, I1 and I2", and, at E-0457, that it was
"stored as knowledge and not run". A rule as an instance, with its threshold as
a typed slot, its sentence verbatim, and its own digest. Nothing executes it.

### 1.3 The mechanical ruling: Prolog is the only admissible check

Asked and answered inside the paper cell before any rule was written.
`paper-v4/experiment-v4/content-rules-doc-02/README.md`, section "Prolog is the
only admissible check implementation, and why" (lines 45-70), repeated in that
cell's `RESULTS.md` lines 51-66:

> Core's check contract admits a pinned Prolog rule program and nothing else:
>
> - `LogicContract.load` closes the contract's fields against
>   `logic.CONTRACT_FIELDS` and refuses any key outside them. The only
>   implementation the contract can name is `rules_file`, whose bytes are hashed
>   into `ruleset_hash` and from there into `contract_hash`.
> - `PrologVerifier._execute` concatenates `fact_declarations(version)`, the
>   compiled facts, its own JSON runner and `contract.rules_source` into one
>   program and runs `swipl` on it. It is the only verifier Core ships.
> - `LogicCheckResult` is a plain dataclass. Its `engine_name` and
>   `engine_version` are set by the verifier that produced it; nothing in the
>   contract, the policy or the protocol machine identifies a check
>   implementation.
>
> So a Python check would be an outcome the caller authored, with no identity
> the contract could pin.

This is not a preference for Prolog. It is the observation that the check
contract has exactly one implementation field, `rules_file`, and no field that
identifies which engine reads it. Any second engine needs a contract field that
does not exist today. That is the real shape of "support both".

The same cell records the cost in the other direction. Luis ruled that the
adopter's formula-slot declarations belong in `logic.yaml`; Core refuses,
because `CONTRACT_FIELDS` is closed, so they live inside `rules.pl` instead:

> This is a mechanical deviation from the ruling, not a preference, and it is
> reported as one.

A declaration about the ontology ended up inside opaque rule bytes because the
rule layer has nowhere else to put it. That is the same wound F4 names.

### 1.4 The re-binding ruling: what it cost to move one ontology hash

Paper ledger **E-0458** (2026-09-17) is the census that measured the coupling.
Nine copies of the archived 38-event Shop history, Core pinned at `e7937b89`.
An additive revision adding two classes was recorded successfully and the graph
replayed byte-identical. Then:

> Step 3 re-pin the rule layer: logic.yaml re-pinned to ontology 72343049 with
> rules bytes ae8de587 unchanged gives rule contract identity 1bf386c3 and
> policy.json re-pointed; composing the revision with the new profile REFUSED,
> exit 1, ledger byte-identical: {"reason": "INCOMPATIBLE_CONTRACT", "detail":
> "domain revision changes the normative protocol profile", ...}

And step 5, admitting one record of the new class with the old pin kept:

> REFUSED {"reason": "RULE_CHECK_FAILED", "detail": "Logic contract and
> compiled facts use different ontologies"}; no admission event, graph
> unchanged ... the record, the classes and the rules are sound, only the
> binding between rules and ontology is broken; inference stated as such: once
> the revision is recorded with the old pin, the required check can no longer
> execute, so no further change admits on that history at all.

The reading recorded in the same entry:

> not a Core bug; both refusals are deliberate and right alone (a revision must
> not silently change what checks govern admission; a rule contract must not be
> applied to an ontology it did not pin); the missing capability is policy
> re-binding across an additive revision

Luis ruled at E-0459 to build it. It shipped as `REBIND_CHECK_CONTRACT`,
recorded at overseer entry **OVR-000464**:

> A policy whose required check contract pins the compiled ontology inside its
> own digest made ontology growth impossible for that adopter: re-pinning the
> same rule bytes moved the check identity, the policy and the normative
> profile, so the revision refused INCOMPATIBLE_CONTRACT, and keeping the old
> pin left the check unable to execute against the revised graph. Luis ruled
> the fix is a declared recorded act, not a loophole. ... Core runs no rule: not
> policy migration.

The final clause matters for F5. `REBIND_CHECK_CONTRACT` re-points identities.
It does not read a rule, does not know what a rule reads, and does not decide
anything. A person decides, and Core checks that nothing but the ontology
binding moved.

The blast radius was then measured, at overseer entry **OVR-000466**:

> the revision policy is content-addressed over its declared kinds, so
> CONTRACT_REVISION_POLICY.identity moved from 05b68805 to e129b6e8 and every
> recompiled revision records the new one. The Small Shop's frozen evidence and
> its connected-story warehouse boundary were cut against the old identity and
> refused to reproduce (three evidence tests and the fourteen paper calibration
> tests behind them).
>
> Lesson recorded: a moved content-addressed policy digest moves every frozen
> artifact that records a ledger coordinate, and the check is regenerating the
> family, not grepping.

Adding one change kind to the revision policy invalidated frozen evidence three
layers away. Any option in section 4 that changes the contract grammar pays
that same toll once.

### 1.5 Two standing constraints that bind every option

From the `malleus-dev` skill's architectural law, point 13, `EXECUTOR_ONLY`:

> Put profile-specific event, record, field, precondition, transition, effect,
> atomicity, and refusal semantics in exact identified artifacts. The executor
> implements only generic operations and declared typed capabilities. A second
> conforming interpreter must consume the same artifact and produce the same
> accepted state or typed refusal without copying private branches from the
> first implementation. Never add an unrestricted callback or arbitrary-code
> escape hatch.

And from the same skill's "Accepted compiler-enabled profile boundary":

> Generated JSON Schema, SHACL, OWL, RDF, Python, or other schemas are optional
> projections of this profile. Each binds its generator and profile and reports
> semantic coverage and loss. While the compiler-enabled profile is claimed, no
> projection can bypass the effective contract.

SHACL is already classified in this repository: a **projection**, never an
authority. An option that makes SHACL the place rules live would have to
reclassify it, and would owe the argument for doing so.

---

## 2. The mechanism today, in one page

### 2.1 What runs

A rule set is a **LogicContract**: a YAML document (`logic.yaml`) naming a
Prolog file and pinning the ontology it was written against.
`src/malleus/logic.py:26-37` closes its field set:

```python
CONTRACT_FIELDS = {
    "schema_version", "contract_id", "contract_version", "ontology_hash",
    "fact_contract_version", "ruleset_id", "ruleset_version", "rules_file",
    "rule_ids", "timeout_seconds",
}
```

`LogicContract.load` calls `_exact_fields(document, CONTRACT_FIELDS, ...)`
(`logic.py:219`) and refuses any other key. There is no field naming an engine,
no field naming a class or slot the rules read, and no field an adopter may add.

The graph is compiled to Prolog facts by `GraphFactCompiler` under a versioned
**fact contract**. Version 3 declares twelve predicates (`logic.py:38-60`):
ten structural (`m_ontology_hash/1`, `m_type/1`, `m_mixin/1`, `m_subtype/2`,
`m_has_mixin/2`, `m_record/3`, `m_relation/4`, `m_property/4`, `m_list/3`,
`m_list_item/5`) and two provenance (`m_derivation/4`, `m_source_text/3`, added
at OVR-000461). A contract declaring version 2 receives only the ten, so a
version-2 rule reaching for a provenance predicate fails loudly rather than
matching an empty relation (`logic.py:74-86`).

`PrologVerifier._execute` (`prolog_verifier.py:130-142`) finds `swipl` on
`PATH`, concatenates the fact declarations, the compiled facts, its own JSON
runner and the contract's rule bytes into one program, and runs a fresh
SWI-Prolog process. Rules declare `malleus_rule/1` and prove
`malleus_violation/3`; the verifier checks the declared rule set against the
contract's `rule_ids` (`prolog_verifier.py:97`) and returns `SATISFIED` or
`VIOLATED` with exhaustive witnesses. Any failure raises
`LogicExecutionError`; nothing can report `SATISFIED` by accident.

Selection is by a **PolicyProgram** in the normative profile
(`_contract_pipeline/machine.py:566-573`): `policy_id`, `outcome_verdicts`,
`precedence`, and `required_checks`, a tuple of
`(check_contract_id, check_contract_identity)` pairs. Its fields are closed too
("policy fields are not closed" is the refusal at `machine.py:585`).

### 2.2 The artifacts and hashes that must travel together

One chain, from ontology bytes to what the history will admit. Shop values from
E-0458 in brackets.

| # | Artifact | Identity | Carries |
|---|---|---|---|
| 1 | Ontology source bytes (LinkML YAML: `shop.yaml`, `context.yaml`, plus imports) | content hash [6ef56157 → 72343049] | classes, slots, ranges, and the in-ontology constraints of 2.4 |
| 2 | `logic.yaml`, the check contract | `contract_hash` [83816c3a → 1bf386c3] | the ten closed fields, including `ontology_hash` (1) and `ruleset_hash` (3) |
| 3 | `rules.pl`, the rule bytes | `ruleset_hash = sha256(bytes)` [ae8de587, unchanged] | every rule, plus whatever the adopter had to declare there |
| 4 | fact contract version | the literal `"2"` or `"3"` inside (2) | which predicates the rules may read |
| 5 | `policy.json`, the PolicyProgram | canonical-bytes digest [policy program 5886c397] | `required_checks` naming (2) by id **and** by `contract_hash` |
| 6 | `NormativeAdmissionProfile` | identity [6fe5c4d9] | the machine program plus the selected policies (5) |
| 7 | `PartialEffectiveContract` | identity [af74ca2a → 191d58df] | the compiled contract (1) plus the normative profile (6) |
| 8 | `CONTRACT_REVISION_POLICY` | identity [05b68805 → e129b6e8] | which change kinds a revision may declare |
| 9 | the history | ledger head, event count, accepted state digest | what (7) it currently requires |

`logic_contract_digest` (`logic.py:90-116`) folds `ontology_hash` and
`ruleset_hash` into `contract_hash`. The policy names that `contract_hash`
verbatim. So **one byte changing in the ontology moves identities 1, 2, 5, 6
and 7**, with the rule bytes untouched. That is the arithmetic behind Luis's
"carry ids/hashes, etc.", measured rather than asserted: E-0458 step 3.

Two refusals enforce the chain at runtime:

- `prolog_verifier.py:89-90`: `if not overlay.registry.verifies(self.contract.ontology_hash)` raises `LogicError("Logic contract and compiled facts use different ontologies")`. (`verifies` goes through the payload-grammar capability, so a hash recorded under an earlier grammar still matches.)
- `CHECK_CONTRACT_NOT_RETAINED` at the next admission, if a revision declares a re-bound check contract and the act does not retain its bytes (`malleus-dev` skill, from E-0458 and E-0465).

### 2.3 What crosses an ontology revision today

`compose_contract_revision` computes the diff as a **set difference over
triple-shaped semantic facts** (`_contract_pipeline/revision.py:857-895`):
`before, after = _facts(current), _facts(target)`, refuse if
`set(before) - set(after)` is non-empty, then classify `added_keys` into
`ADD_CLASS`, `ADD_SLOT`, `ADD_ENUM_VALUE`, `ADD_IMPORT` (refused) and, since
OVR-000464, `REBIND_CHECK_CONTRACT` (`revision.py:27-28`).

The re-binding is validated by `_compile_rebinding` (`revision.py:690-770`): it
requires that every check whose identity moved is declared, that no check that
did not move is declared, that each declared before-and-after pair hashes to
the identity the current and target policies require, that exactly one field
moved and that it moved from the current ontology's content hash to the
target's, and that undoing the re-binding reproduces the current normative
profile byte for byte. Runners read `KnowledgeHistoryReplay.required_checks`
(`knowledge.py:775-790`) rather than a fixed id.

**What no artifact records: which classes and slots each rule reads.** The rule's
dependency on the ontology is expressed only as quoted atoms inside opaque
Prolog bytes, for example `m_property(A, 'order_id', SubjectKind, Subject)`.
The only recorded dependency is one whole-ontology hash, per rule *set*, not per
rule. This single sentence is why F5 cannot be derived today: there is nothing
to intersect the diff with.

### 2.4 The part that is already inside the ontology

Malleus's LinkML support profile already admits a bounded set of in-ontology
constraints, enforced closed-world at write time, and they already travel
inside the ontology hash with no second identity of any kind:

- Slot level (`_contract_compiler_profile.json`, `node_shapes.slot.fields`):
  `range`, `required`, `multivalued`, `identifier`, `inlined`,
  `minimum_value`, `maximum_value`, `equals_string`, `value_presence`.
- Class level (`node_shapes.class.fields`): `is_a`, `mixins`, `abstract`,
  `slots`, `attributes`, `slot_usage`, and `exactly_one_of` over
  `slot_conditions`, where a condition may carry `required`, `equals_string`
  or `value_presence` (`PRESENT` / `ABSENT`).
- Enforced at write time: `ontology.py:1450-1456` appends
  `Property 'x' must be at least {minimum_value}` and the `equals_string`
  error; the constraint values enter the schema's content hash at
  `ontology.py:1637-1646`.

The Shop already uses them. `context.yaml:15-17` declares
`maximum_unpaid_invoices` as `required: true, minimum_value: 0`, and
`context.yaml:63-93` pins six relation types with `equals_string`. E-0458's
negative control confirms they are load-bearing: narrowing `minimum_value` 0 to
1 "refuse[s] NON_ADDITIVE_CHANGE before any write".

So the premise "rules live outside" is true of the Prolog layer and false of
the constraint layer. Malleus already has a small in-ontology rule surface that
costs no second engine, no second identity, and no re-binding. The real
question is how much of the Prolog layer can move into it, and what is left
over.

### 2.5 The six live rules, and what they demand

| Rule | Where | What it needs |
|---|---|---|
| `NO_CONFLICTING_QUANTITY` (Shop) | `private/shop-progressive-01/producer/workspace-stage-c/inputs/rules.pl` | join **two different records**; `A @< B` to avoid mirrored witnesses; inequality of two property values |
| `NO_EMPTY_RECORD` (Shop) | same file | negation-as-failure over *any* property: `\+ m_property(Record, _, _, _)` |
| `NO_CONFLICTING_QUANTITY` (document) | `paper-v4/experiment-v4/content-rules-doc-02/rules.pl:472-513` | the above, plus `forall/2` (universal quantification over a declared family table), `findall/3` (aggregation into lists), list equality, and a violation code built at runtime by `atom_concat` |
| `INTERVAL_SANITY` | same file, 518-541 | two sub-forms: `value_lower > value_upper` (**cross-slot comparison inside one record**) and a negative value on a declared non-negative slot (a literal bound) |
| `NUMBER_IN_CITED_TEXT` | same file, 552-566 | join a record to its retained source sentence through `m_source_text/3`; parse a **number grammar out of free text**; compare as exact rationals; negation-as-failure |
| `FORMULA_IN_SOURCE` | same file, 572-578 | a six-stage string normalisation (ligatures, hyphen-space breaks, spaced digits, letter-to-digit gluing, whitespace collapse, case folding), **each rewrite run to a fixed point**; substring containment; negation-as-failure |

The four document rules also depend on a declaration block
(`rules.pl:25-108`): nine `numeric_slot/1` facts and one `subject_slot/1`
derived from the compiled contract's ranges, then `formula_slot/1`,
`qualifier/1`, `quantity_family/1`, `quantity_identity/2`, `quantity_value/2`,
`bound_pair/2` and `non_negative_slot/1`, which the contract cannot supply
because it declares `analyte`, `numerator_kind`, `quantity_kind`, `name` and
`description` all as `String` and says nothing about which is copied from the
source. That is the per-slot source relation, recorded at E-0430 and carried as
ROADMAP items E2 and E3, and declared "not implemented" in
`.claude/skills/malleus-dev/references/CAPABILITIES.md`.

Read as a capability ladder, our six rules need: (i) literal bounds, (ii)
cross-slot comparison inside one record, (iii) existence and negation, (iv)
cross-instance joins, (v) aggregation and universal quantification, (vi) exact
rational arithmetic, (vii) fixed-point string rewriting and a number grammar
over free text, (viii) exhaustive witnesses naming record ids, and (ix) a place
to declare distinctions the ontology does not carry. Level (i) is in the
ontology today. Everything from (iv) up is what keeps the second system alive.

---

## 3. The survey

Rule: every external claim below carries a URL or DOI that was fetched on
2026-09-19, or is marked as recorded earlier in this repository and not
re-verified today. Where a specification does not state something negatively,
the finding says so rather than pretending to a quote.

### 3.0 Three facts that reshape the survey

**(a) LinkML's own rules are SHACL rules.** The LinkML metamodel gives the
`rules` slot the `slot_uri` **`sh:rule`**
(https://linkml.io/linkml-model/latest/docs/rules/, fetched today; domain
`ClassDefinition`, range `ClassRule`, multivalued, description "the collection
of rules that apply to all members of this class"). LinkML rules and SHACL
rules are not two options. They are one option with two syntaxes.

**(b) The W3C's live rules track just moved rules out of RDF.**
`https://www.w3.org/TR/shacl12-rules/` now **301-redirects** to
`https://www.w3.org/TR/sparql12-rl/`, titled **SPARQL 1.2 RL**, W3C Working
Draft **19 September 2026** (fetched today; independently confirmed twice). The
rename landed **25 August 2026** after 39 Working Drafts under the SHACL name
(https://www.w3.org/standards/history/shacl12-rules/). Its abstract, verbatim:

> "This document defines SPARQL-RL, a datalog-style rules language for RDF.
> SPARQL-RL provides inferencing with the generation of new RDF data from a
> combination of a set of rules and a base data RDF graph. It provides a
> SPARQL-like text syntax and defines how a set of rules is evaluated against an
> RDF graph."

**SRL** in that document is the **SPARQL Rule Language**, not a "Shape Rules
Language": "The SPARQL Rule Language can be referred to as simply SRL when the
context is clear." `sh:TripleRule` and `sh:SPARQLRule` do not appear in it. A
rule in SRL is a text document, not a set of triples. `docs/DELIMITATIONS.md`
line 243 ("mappable to SHACL/SRL") was written when SRL was expected to be a
shapes-side language; that expectation no longer holds, and the standing order
needs re-reading in that light.

**(c) Every rules-as-RDF mechanism is off the standards track.**
SHACL-AF is a Working Group Note of 8 June 2017, never revised
(https://www.w3.org/TR/shacl-af/: "Publication as a Working Group Note does not
imply endorsement by the W3C Membership ... It is inappropriate to cite this
document as other than work in progress"). SPIN is a Member Submission of
22 February 2011 (https://www.w3.org/Submission/spin-overview/). SWRL is a
Member Submission of 21 May 2004 (https://www.w3.org/Submission/SWRL/). N3 has
**no W3C Technical Report at all**: `https://www.w3.org/TR/n3/` returns HTTP
404; it exists as a Team Submission of 28 March 2011
(https://www.w3.org/TeamSubmission/n3/) and as a living Community Group report
(https://w3c-cg.github.io/N3/spec/: "It is not a W3C Standard nor is it on the
W3C Standards Track"). ShEx is a Final Community Group Report of 8 October 2019
(http://shex.io/shex-semantics/), same disclaimer, never Recommendation-track.

The one stable Recommendation in the area, SHACL Core (20 July 2017,
https://www.w3.org/TR/shacl/), is normatively forbidden from changing the graph:

> "During validation, the data graph and the shapes graph MUST remain
> immutable, i.e. both graphs at the end of the validation MUST be identical to
> the graph at the beginning of validation. ... SHACL processing is thus
> idempotent."

So "put the rules in the graph, the way the semantic web does it" is not a
path with a standard at the end of it. That is a fact about the field, not an
argument against Luis's vision, and it is worth knowing before choosing.

### 3.1 What each approach can express against our six rules

Legend: **Y** expressible; **P** partial, with the gap named; **N** not
expressible; **--** out of scope for that mechanism.

| Approach | Where the rule lives | (1) Shop NO_CONFLICTING_QUANTITY | (2) Shop NO_EMPTY_RECORD | (3) doc NO_CONFLICTING_QUANTITY | (4) INTERVAL_SANITY | (5) NUMBER_IN_CITED_TEXT | (6) FORMULA_IN_SOURCE |
|---|---|---|---|---|---|---|---|
| **Malleus in-ontology constraints today** (`required`, `minimum_value`, `maximum_value`, `equals_string`, `value_presence`, `exactly_one_of`) | ontology bytes | N | N | N | **P** (non-negative half: `minimum_value: 0`; bounds-inverted half N) | N | N |
| **LinkML `rules`** (ClassRule) | ontology bytes | N | P | N | P | N | N |
| **LinkML `classification_rules`** | ontology bytes | -- | -- | -- | -- | -- | -- |
| **LinkML `slot_usage` + `equals_expression`** | ontology bytes | N | N | N | P | N | N |
| **LinkML `unique_keys`** | ontology bytes | **N (wrong constraint)** | N | N | N | N | N |
| **SHACL Core** | shapes graph (RDF) | N | P | N | P | N | N |
| **SHACL-SPARQL** (same 2017 REC, §5) | shapes graph (RDF) | Y | Y | Y | Y | P | **N** |
| **SHACL-AF rules `sh:rule`** | shapes graph (RDF) | -- (inference) | -- | -- | -- | -- | -- |
| **SPARQL 1.2 RL / SRL** | a text rule document | -- (inference) | -- | -- | -- | -- | -- |
| **ShEx** | schema document | N | P | N | P | N | N |
| **SPIN** `spin:constraint` | RDF, attached to the class | Y | Y | Y | Y | P | N |
| **N3 + `log:implies`** | triples in the graph | Y | Y (scoped `log:notIncludes`) | Y | Y | P | P |
| **Prolog over the fact contract (today)** | beside the ontology | Y | Y | Y | Y | Y | Y |
| **PROV-O** | -- | -- | -- | -- | -- | -- | -- |

Why each verdict, with the source:

- **Malleus in-ontology today.** `minimum_value` is enforced at write time
  (`ontology.py:1453-1456`) and the Shop already declares it
  (`context.yaml:17`). `value_lower <= value_upper` is a comparison between two
  slots; no admitted construct expresses it. Everything else needs a second
  record, or free text.
- **LinkML `rules`.** `preconditions`, `postconditions` and `elseconditions`
  each range over `AnonymousClassExpression`, whose `slot_conditions` maps slot
  names to `SlotDefinition`s
  (https://linkml.io/linkml-model/latest/docs/ClassRule/,
  https://linkml.io/linkml-model/latest/docs/AnonymousClassExpression/). Every
  condition is evaluated against one instance of the class. Nothing quantifies
  over a second instance. `NO_EMPTY_RECORD` is **P**: you can require presence
  per class with `value_presence`, which is a different, stronger statement than
  "carries at least one property of any kind". Also: the LinkML specification's
  `### Rules` and `### Uniqueness checks` headings are **empty**, with no
  normative text under them (`05validation.md` in linkml/linkml-model); only
  `### Rule evaluation` carries one line. And `rules` is not in Malleus's
  support profile: `node_shapes.class.fields` in
  `src/malleus/_contract_compiler_profile.json` admits `description`,
  `class_uri`, `abstract`, `mixin`, `is_a`, `mixins`, `slots`, `attributes`,
  `exactly_one_of`, `slot_usage`, `annotations`, and nothing else.
- **LinkML `classification_rules`.** "Classification rules allow for
  automatically assigning the instantiated type of an instance"
  (https://linkml.io/linkml-model/latest/docs/classification_rules/). That is
  type inference, not a constraint, so it answers none of our six. Its spec
  section `### Classification Rule evaluation` is also empty, and
  `linkml-validate` does not evaluate it.
- **LinkML `equals_expression`.** "the value of the slot must equal the value
  of the evaluated expression"
  (https://linkml.io/linkml-model/latest/docs/equals_expression/); the
  expression is "a simple subset of Python" whose bindings are the object's own
  attributes (https://linkml.io/linkml/schemas/advanced.html). Arithmetic and
  the comparisons `Eq, Lt, LtE, Gt, GtE` are supported; `!=` is not; the
  function table is `max, min, len, str, strlen, case`, with **no regex and no
  string replace**. So an interval check is reachable only by contrivance (a
  derived boolean slot), and text rules are out. `equals_expression` is also
  absent from Malleus's support profile and, by source inspection, from the
  default `linkml-validate` path.
- **LinkML `unique_keys`.** "A collection of named unique keys for this class.
  Unique keys may be singular or compound"
  (https://linkml.io/linkml-model/latest/docs/unique_keys/); scope is "that of
  the container (the multi-valued slot) that contains instances of the
  identified class" (https://linkml.io/linkml/schemas/constraints.html). Marked
  **N (wrong constraint)** deliberately: `unique_keys` on (order, product)
  forbids *any* two records sharing that pair, including two that agree on the
  quantity. Our rule forbids only disagreement. A functional dependency is not a
  uniqueness constraint, and LinkML has no construct for one. LinkML's own
  JSON Schema generator documents that it cannot enforce even the weaker thing:
  "Currently JSON-Schema does not yet support unique keys"
  (https://linkml.io/linkml/generators/json-schema.html).
- **SHACL Core.** The four comparison components (`sh:equals`, `sh:disjoint`,
  `sh:lessThan`, `sh:lessThanOrEquals`, §4.5) all compare the shape's value
  nodes against "the objects of the triples that have **the focus node** as
  subject and the value of sh:equals as predicate" (https://www.w3.org/TR/shacl/,
  §4.5.1). One focus node. `sh:lessThan` gives INTERVAL_SANITY's bounds check as
  **P** (it needs the compared value to be a plain predicate at the same node,
  which our two bounds are). The string family is exactly
  `sh:minLength, sh:maxLength, sh:pattern, sh:languageIn, sh:uniqueLang` (§4.4):
  regex can test, nothing can rewrite. Cross-focus-node joins and string
  transformation are both absent; the specification does not deny them in words,
  so these two findings come from the exhaustive §4 component list, not a quote.
  The spec's own admission, verbatim: "Not all use cases can be expressed by the
  Core language alone."
- **SHACL-SPARQL.** Part of the same 2017 Recommendation, §5
  ("SHACL-SPARQL supports a constraint component that can be used to express
  restrictions based on a SPARQL SELECT query"), not the AF Note. SPARQL 1.1
  (https://www.w3.org/TR/sparql11-query/, REC 21 March 2013) gives self-joins,
  `NOT EXISTS` (§8.1.1) and aggregation (`COUNT, SUM, MIN, MAX, AVG,
  GROUP_CONCAT, SAMPLE`), which covers rules 1-4. Rule 5 is **P**: the number
  grammar is reachable by regex, exact rational comparison is not guaranteed by
  SPARQL's numeric typing and was not established here. Rule 6 is **N**:
  `REPLACE` "returns a string with matched substrings replaced by a replacement
  string" and, following `fn:replace`, rewrites all non-overlapping matches in
  one pass (https://www.w3.org/TR/sparql11-query/#func-replace). Our
  normalisation runs each rewrite **to a fixed point** (`rules.pl:142-148`);
  SPARQL offers no construct that repeats a string rewrite until stable. Caveat:
  that last sentence is a reading of the function library, not a quoted denial.
  One portability warning from the spec itself: "SHACL Core processors that do
  not also support SHACL-SPARQL ignore any SHACL-SPARQL constructs such as
  sh:sparql triples." Silent ignoring is exactly the failure mode Malleus
  forbids.
- **SHACL-AF rules and SPARQL 1.2 RL.** Both are inference, not validation, so
  they answer none of our six. AF, verbatim: "SHACL rules build on SHACL to form
  a light-weight RDF vocabulary for the exchange of rules that can be used to
  derive inferred RDF triples from existing asserted triples", and "A SHACL
  rules engine ... is capable of adding triples to the data graph". SRL defines
  exactly two operations, "infer" and "query", and no validation operation. AF
  also never specified fixpoint semantics: "this algorithm only covers a single
  'iteration' over all rules ... The latter is left to future work."
- **ShEx.** Shape conformance over a node's neighbourhood; no join, no
  cross-instance value equality. Its only extension point is Semantic Actions,
  whose semantics are implementation-defined. Recorded honestly as "no standard
  mechanism found", not "proven impossible".
- **SPIN.** The mechanism Luis's "rules as instances" describes, built in 2011:
  "In SPIN, constraints are attached to classes using the property
  spin:constraint" and "Since SPIN is entirely based on and represented in RDF,
  rules and constraints can be shared on the web together with the class
  definitions they are associated with" (https://spinrdf.org/spin-shacl.html,
  https://www.w3.org/Submission/spin-overview/). A `spin:constraint` is a SPARQL
  ASK, so its expressiveness is SPARQL's, hence the same column as
  SHACL-SPARQL. It is superseded by its own vendor: "SHACL supersedes SPIN in
  almost every respect ... TopQuadrant will prefer SHACL over SPIN for new
  features."
- **N3.** The most literal answer to "rules within-system": "An N3 rule is
  actually a N3 statement, where the subject and object constitute graph terms,
  and the predicate is `log:implies`", and graph terms "can be used in any
  position in an N3 statement" (https://w3c-cg.github.io/N3/spec/). It adds
  scoped negation-as-failure via `log:notIncludes`. Rules 5 and 6 are **P**
  rather than N only because N3 builtin libraries are open-ended and
  implementation-specific; nothing in the spec supplies a fixed-point string
  rewrite. Cost: no W3C Technical Report, open-world defaults, and a rule engine
  (EYE or equivalent) outside anything Malleus ships.
- **PROV-O.** W3C Recommendation 30 April 2013 (https://www.w3.org/TR/prov-o/).
  The whole definition of `prov:Plan` is one sentence: "A plan is an entity that
  represents a set of actions or steps intended by one or more agents to achieve
  some goals." The specification then declines to say more: **"Both prov:Plan
  and prov:Role are left to be extended by applications."** `prov:wasDerivedFrom`
  records *that* a derivation happened, never *how*. So PROV-O can hold the
  identifier of a rule and say which activity followed it. It cannot express the
  rule. That matches what `docs/DELIMITATIONS.md:140` already recorded: "PROV is
  passive vocabulary". Defining our rules in PROV-O is not an available option;
  pointing at them from PROV-O is, and is cheap.

### 3.2 OWL 2, and why "just use axioms" is not available

OWL 2 is a W3C Recommendation, Second Edition, 11 December 2012
(https://www.w3.org/TR/owl2-overview/). Its three profiles, verbatim: **EL**
"enables polynomial time algorithms for all the standard reasoning tasks";
**QL** "enables conjunctive queries to be answered in LogSpace (more precisely,
AC0) using standard relational database technology"; **RL** "enables the
implementation of polynomial time reasoning algorithms using rule-extended
database technologies operating directly on RDF triples".

A naming trap worth one line: **OWL 2 RL and SPARQL 1.2 RL are different things
that share two letters.** OWL 2 RL is a profile of OWL. SPARQL 1.2 RL is the
2026 rules Working Draft from 3.0(b).

Why OWL cannot carry our rules, from the primary source. Tao, Sirin, Bao and
McGuinness, "Integrity Constraints in OWL", AAAI 2010, DOI
**10.1609/aaai.v24i1.7525** (https://ojs.aaai.org/index.php/AAAI/article/view/7525).
Verbatim from the abstract:

> "challenges arise due to the Open World Assumption (OWA) and the lack of a
> Unique Name Assumption (UNA) in OWL's standard semantics."
>
> "conditions that trigger constraint violations in systems using the Closed
> World Assumption (CWA), will generate new inferences in standard OWL-based
> reasoning applications."

And from the paper's worked examples: "due to the OWA, not having a known
producer for p does not cause a logical inconsistency", and "Since m1 and m2 are
not explicitly defined to be different, they will be inferred to be same due to
the cardinality restriction."

Read against our rules, that is fatal twice. `NO_EMPTY_RECORD` would infer
unknown properties rather than refuse. `NO_CONFLICTING_QUANTITY` would infer
that two disagreeing records are the same record, which is the exact opposite of
the violation we want. Motik, Horrocks and Sattler make the same point about
schema statements generally in "Bridging the gap between OWL and relational
databases", WWW 2007, DOI **10.1145/1242572.1242681** (journal version DOI
**10.1016/j.websem.2009.02.001**): "Schema statements in OWL are interpreted
quite differently from analogous statements in relational databases. ... If
these statements are meant to be interpreted as integrity constraints (ICs),
OWL's interpretation may seem confusing and/or inappropriate."

Bolting rules onto OWL is also bounded. Motik, Sattler and Studer, "Query
Answering for OWL-DL with rules", Journal of Web Semantics 3(1):41-60, 2005,
DOI **10.1016/j.websem.2005.05.001**: "A combination of OWL-DL and rules is
desirable for the Semantic Web; however, it might easily lead to the
undecidability of interesting reasoning problems", and the fix is the DL-safe
restriction, "each variable in the rule is required to occur in a non-DL-atom in
the rule body".

`docs/DELIMITATIONS.md:133` already records **Reject** on these grounds. The
sources confirm it. Nothing here changes that verdict.

### 3.3 Datalog and Prolog over graphs

| Engine | Rule language | Store / transaction | Incremental under change | Primary source |
|---|---|---|---|---|
| **RDFox** | Datalog plus stratified negation-as-failure, aggregation, built-ins, equality, named graphs, n-ary relations | in-memory RDF store with transactions | **yes, and it covers rule changes** | https://docs.oxfordsemantic.tech/reasoning.html |
| **Vadalog** | Warded Datalog+/-, existential quantification in PTIME | reasoning system, not a governed store | not claimed | Bellomarini, Sallinger, Gottlob, PVLDB 11(9):975-987, 2018, DOI **10.14778/3213880.3213888** |
| **Soufflé** | Datalog compiled to parallel C++ | **none**: no store, no transaction, no graph identity | not applicable | https://souffle-lang.github.io/ ; release 2.5, 24 March 2024 |
| **SWI-Prolog (ours)** | full Prolog | none; we supply the facts and the isolation | not applicable | `prolog_verifier.py:130-142` |

RDFox is the one engine in the comparison set that already does something F5
asks for. Verbatim: "RDFox implements sophisticated algorithms for both
efficiently computing materializations and maintaining them under
addition/deletion updates that **may affect both the data and the rules**."
That is rule-change-aware incremental maintenance, shipped. Its own caveat,
also verbatim: "deletion of triples is restricted to those that are explicit in
the input graph and hence one does not consider deletion of derived triples."

On write gating, RDFox is honest about the shape of it and it is instructive.
Its docs section "Rejection of Non-Conforming Updates" says: "one can query the
SHACL tuple table before committing a transaction as follows and, in case any
violations are detected, adding an instance of the rdfox:ConstraintViolation
class in the default graph; ... the latter will prevent a transaction from
committing." The abort exists; the author must wire it into each transaction.
There is no declarative validate-on-commit switch. This resolves the residual
recorded at `docs/DELIMITATIONS.md:323-325` ("whether it aborts transactions on
violation was not established"): the mechanism exists and is user-assembled.

On standards: **there is still no finished standard rules language for RDF.**
SPARQL 1.2 RL is a first Working Draft from today. RIF, the Rule Interchange
Format, is a W3C Working Group Note, Second Edition, 5 February 2013
(https://www.w3.org/TR/rif-overview/), "a standard for exchanging rules among
rule systems, in particular among Web rule engines", designed for "exchange
rather than trying to develop a single one-fits-all rule language". It has been
static for thirteen years. RDF 1.2 Semantics is a Candidate Recommendation
Snapshot of 7 April 2026 (https://www.w3.org/TR/rdf12-semantics/) and defines
entailment regimes, not a rule language.

### 3.4 Versioned ontology evolution with rule migration (F5's literature)

The foundational statement of why this is hard is Noy and Klein, "Ontology
Evolution: Not the Same as Schema Evolution", Knowledge and Information Systems
6(4):428-440, 2004, DOI **10.1007/s10115-003-0137-2**. Verbatim:

> "A lot of problems that existed only in theory in database research come to
> the forefront as practical problems in ontology evolution."
>
> "The traditional distinction between versioning and evolution is not
> applicable to ontologies."
>
> "We must develop automatic techniques for finding similarities and differences
> between versions."

The methodology reference is Stojanovic, "Methods and Tools for Ontology
Evolution", PhD thesis, Universität Karlsruhe (TH), 2004, DOI
**10.5445/IR/1000003270** (https://publikationen.bibliothek.kit.edu/1000003270).
Warning for anyone citing it: the repository's own metadata shows the **wrong
title** ("Business-process oriented knowledge management"); the PDF title page
is correct. The change-representation framework is Klein and Noy, "A
Component-Based Framework For Ontology Evolution", IJCAI-03 workshop,
CEUR-WS Vol-71 (https://ceur-ws.org/Vol-71/Klein.pdf), no DOI. Its kernel is
"an ontology of change operations", and its first enumerated task is exactly
ours: "Data Transformation: When an ontology version Vold is changed to Vnew,
data described by Vold might need to translated to bring it in line with Vnew."

**Diff tools report axioms, not impact.** ROBOT's `diff`
(https://robot.obolibrary.org/diff) compares two ontologies "while ignoring
these differences" of serialisation and emits an axiom-level diff in OWL
Functional or Manchester syntax. Bubastis "is able to analyse two ontologies
(typically two versions of the same ontology) to highlight logical changes which
have occurred"; its EBI tool page and the `EBISPOT/bubastis` repository are both
gone, surviving as forks (https://github.com/dgarijo/bubastis), and it has no
dedicated publication. Neither tool says which downstream artifact a change
breaks. LinkML has **no schema diff at all**: not in the generator list
(https://linkml.io/linkml/cli/generate.html), not in the CLI command
registration, not in the 100 repositories of the `linkml` GitHub organisation.
The nearest thing, `linkml-dataops`, diffs instance data.

**The headline finding for F5, stated plainly: migrating rules or constraints
when the ontology changes has no established primary line in the semantic-web
literature.** The SHACL "updates" literature that sounds like it is about this
is uniformly about data updates against fixed shapes:

- Ahmetaj, Konstantinidis, Ortiz, Pareti, Simkus, "SHACL Validation Under Graph
  Updates", ISWC 2025, DOI **10.1007/978-3-032-09527-5_8**, extended version
  arXiv:2508.00137 (https://arxiv.org/abs/2508.00137): "we present a SHACL-based
  update language that can capture intuitive and realistic modifications on RDF
  graphs and study the problem of static validation under such updates."
  Insertions and deletions of triples; shapes fixed.
- Zacouris, Ke, Acosta, "UpSHACL: Targeted Constraint Validation for Updates
  over Knowledge Graphs", ISWC 2025, DOI **10.1007/978-3-032-09527-5_7**:
  "UpSHACL introduces a formal model to identify the subgraph affected by an
  update and constructs a reduced subgraph that can be validated using existing
  SHACL engines." Incremental validation; shapes fixed. Directly relevant to
  **F3** (check only what a change touches), not to F5.
- Ahmetaj, Ortiz, Šimkus, "Towards SHACL Validation of Evolving Graphs", AMW
  2024, CEUR-WS Vol-3954 (https://ceur-ws.org/Vol-3954/paper1130.pdf): despite
  "evolving" in the title, "the graph" is what evolves.

The nearest verified analogues to what F5 asks are in two other communities:

- Kondylakis and Plexousakis, "Ontology Evolution: Assisting Query Migration",
  ER 2012, DOI **10.1007/978-3-642-34002-4_26**. Migrates **queries** when the
  ontology changes. A rule is a query with a verdict attached, so this is the
  closest semantic-web relative of F5.
- Kessentini, Sahraoui, Wimmer, "Automated Co-evolution of Metamodels and
  Transformation Rules: A Search-Based Approach", SSBSE 2018, DOI
  **10.1007/978-3-319-99241-9_12**. Model-driven engineering, not semantic web,
  and structurally the same problem: the metamodel moves, the rules that read it
  must follow.
- Seifer, Hernández, Lämmel, Staab, "Transforming Shape Schemas with Composable
  Property-Graph Queries", arXiv:2606.14309, 12 June 2026
  (https://arxiv.org/abs/2606.14309): "the question arises of which schema can be
  expected after one (or several) transformation steps." Derives constraints
  under transformation, in the property-graph world.

Two phrases that do **not** name real literature, checked and not found:
"SHACL shapes evolution" and "constraint evolution ontology". If either appears
in a Malleus design document as a citation, it does not survive checking.

This repository already ran a recon on the neighbouring question:
`research/ontology_change_rules_recon` (2026-08-20), "Reading rules over an
append-only ledger: expression, partiality, hard breaks, and authorisation",
34 works, 74 claims, 18 axes. Its coded result is worth quoting as a count:
`axis:reading-rule-as-data` is shared by 9 of the 34 works (JSON Schema,
Kubernetes CRD, KGCL, OWL 2, R2RML, SHACL-AF, SHACL Core, SPARQL Update, XSLT
3.0); `axis:reading-rule-identity` by 7; and
**`axis:reading-rule-content-addressed` by 2, neither of them a semantic-web
work** (Cosmos SDK's upgrade module and the in-toto attestation framework). Its
own boundary statement: "Missing coverage means not established in the recorded
review, not proof of absence."

### 3.5 What the diff would be expressed in

`design/ONTOLOGY_MIGRATION_RECEIPT.md:91-105` already decided the delta
language, and the reasoning matters for F3 and F5:

> - **A typed delta.** KGCL already exists, is LinkML, and carries node and edge
>   changes with `old_value`, `new_value` and `has_undo`. Do not invent one.
> - **The reading rule.** Given a record written under A, what it means under B.
>   KGCL does not supply this and binds no version identity at all.
>
> The recorded delta is a convenience. The derivation from the two ontologies is
> the authority.

KGCL is the Knowledge Graph Change Language, a LinkML schema
(https://incatools.github.io/kgcl/, https://github.com/INCATools/kgcl). Its
change classes are term-centric: NodeCreation, NodeDeletion, NodeRename,
NodeObsoletion, NodeMove, EdgeCreation, EdgeDeletion, EdgeRewiring,
PredicateChange, ClassCreation, ObjectPropertyCreation, plus MultiNodeObsoletion
and Transaction. It carries `old_value`, `new_value`, `old_datatype`,
`new_datatype`, `has_undo`. Bounded reading, stated as one: KGCL has no
construct for "this slot's range changed" or "this `slot_usage` constraint was
added", which is exactly the granularity a Malleus revision moves at. Malleus's
own diff already operates at that granularity, over compiled semantic facts
(`revision.py:857-895`), so KGCL is a projection candidate for readability, not
the authority.

The same design file, `S6`, also fixes the shape of any answer to F5:

> A change is legitimate when it arrives with a rule of one of these grades, and
> the grade is declared: **Total** ... **Partial, declaring its own gaps** ...
> **A hard break** ... What malleus refuses is a break that is not declared. You
> may break history. You may not break it silently.

F5's "automagically" must land inside that grading, not beside it. An automatic
re-binding is the **Total** grade derived rather than asserted. A rule the diff
touches is the **Partial** grade with the rule named. Neither is a new concept;
both already have a declared home.

---

## 4. Four options for Malleus

Each is classified with the `malleus-dev` skill's research-to-core promotion
gate: `EVIDENCE_BINDING`, `ROLE_AND_CONSUMER`, `USE_CLASSIFICATION` (one of
`DESIGN_CONSTRAINT`, `BASELINE_OR_ORACLE`, `CONFORMANCE_FIXTURE`,
`IMPLEMENTATION_CANDIDATE`, `EXPLICIT_EXCLUSION`), `MATURITY` (`PROPOSED`,
`ACCEPTED`, `IMPLEMENTED`), and `PLACEMENT`. None of them is proposed as
accepted; acceptance is Luis's.

One finding applies to all four and should be read first.

> **`REBIND_CHECK_CONTRACT` is already engine-neutral.** From
> `handover/2026-09-17-core-policy-rebinding.md`: "Core does not know that
> vocabulary and does not name a field of it", and "`rebound_field` is derived,
> not declared. Core finds the field that carries the current ontology hash
> rather than being told which one it is, so a caller cannot point the rule at a
> field of its choosing." Any second rule representation whose check contract
> carries exactly one field holding the ontology hash rides the existing
> re-binding machinery with no Core change. "Supporting both" does not require
> rebuilding the revision path.

The other fact applying to all four: **adding any field to the check contract
moves `contract_hash` for every existing contract**, hence the policy, hence the
normative profile. OVR-000466 measured what that costs downstream ("a moved
content-addressed policy digest moves every frozen artifact that records a
ledger coordinate"). Whatever is added should be added once.

### Option A. Widen the ontology's own constraint surface

**What.** Admit more of LinkML's in-schema constraint vocabulary into the
Malleus support profile, compiled into contract facts and enforced closed-world
at write time, the way `minimum_value`, `required`, `equals_string`,
`value_presence` and `exactly_one_of` already are.

**Where the rule lives.** In the ontology bytes. No second artifact, no second
identity, no second engine.

**EVIDENCE_BINDING.** The surface exists and is live:
`_contract_compiler_profile.json` node shapes, enforcement at
`ontology.py:1450-1456`, constraint values in the content hash at
`ontology.py:1637-1646`, and the Shop using it at `context.yaml:15-17, 63-93`.
The limit is measured in 3.1: of our six rules this reaches one half of one
(`INTERVAL_SANITY`'s non-negative branch, already covered). `unique_keys` does
not reach `NO_CONFLICTING_QUANTITY`, because a functional dependency is not a
uniqueness constraint. `equals_expression` has no `!=`, no regex and no string
replace.

**ROLE_AND_CONSUMER.** Role: the compiled contract's closed-world validation
boundary. Consumers: both, today.

**USE_CLASSIFICATION.** `DESIGN_CONSTRAINT` for the boundary rule it implies:
*what belongs in the ontology is what the compiled contract can enforce against
one instance at write time, and nothing else.* Specific widenings are
`IMPLEMENTATION_CANDIDATE`. LinkML `rules`, `classification_rules` and
`unique_keys` are `EXPLICIT_EXCLUSION` for v0, on evidence: `rules` and
`classification_rules` have **empty specification sections** in LinkML's own
validation spec, `classification_rules` is type inference not validation and is
not evaluated by `linkml-validate`, and `unique_keys` is documented as not
enforced by the JSON Schema path.

**MATURITY.** Boundary rule: `PROPOSED`. The surface itself: `IMPLEMENTED`.

**Supports both?** Yes, trivially. It is purely additive to today's Prolog
layer and removes nothing.

**F5 under it.** Vacuous, in the good sense. An in-ontology constraint has no
separate identity, so there is nothing to re-bind and no decision to derive. Any
rule that can move here stops being an F5 problem permanently. That is the
strongest argument for the option and the reason to take whatever it will take,
even though it is not much.

**Cost.** Neither a second engine nor a second identity. Each admitted
construct needs a compiler branch, a write-time check, a refusal, and fixtures.
It does not reduce the Prolog layer for the six rules we have.

### Option B. Declare each rule's ontology dependencies, keep the rules outside

**What.** Add to the check contract a declared dependency set per rule: the
classes, slots and enum values the rule reads, plus an explicit marker when a
rule quantifies over *all* types rather than named ones. Core checks that every
declared name exists in the pinned contract and refuses an undeclared name.
The adopter's own test holds the rule bytes to the declaration.

**Where the rule lives.** Beside the ontology, exactly as today. What moves
inside is the *dependency*, as declared, checkable data.

**EVIDENCE_BINDING.** Section 2.3 establishes the gap: "the only recorded
dependency is one whole-ontology hash, per rule *set*, not per rule", while the
diff Core already computes is a set difference over triple-shaped semantic facts
(`revision.py:857-895`) whose subjects are class and slot names. The two sides
of the intersection exist; the declaration is the missing half. The document
cell already writes such a declaration by hand and tests it: `rules.pl:26-51`
carries nine `numeric_slot/1` facts and one `subject_slot/1` "read off run-23's
compiled contract", and `test_content_rules_doc_02.py` "recomputes both sets
from that contract and fails if this block differs by one slot". That is Option
B implemented once, in the wrong place, by hand, by one consumer.

**ROLE_AND_CONSUMER.** Role: the check contract and the contract-revision
boundary. Consumers: both, and the declaration is what the document cell was
already forced to invent.

**USE_CLASSIFICATION.** `IMPLEMENTATION_CANDIDATE`, with a `DESIGN_CONSTRAINT`
attached: *a rule declares what it reads, or it is treated as reading
everything.*

**MATURITY.** `PROPOSED`.

**Supports both?** Yes, and it is the option that makes "both" cheap. The
declaration is a set of ontology names; it says nothing about Prolog, SPARQL or
anything else. A SHACL shapes graph or a rule record would carry the same field
with the same meaning.

**F5 under it.** This is the mechanism F5 asks for, and it is computable.
Intersect the revision's added and moved facts with each rule's declared reads.
Empty intersection: derive the re-binding, record it as
`REBIND_CHECK_CONTRACT` with the derivation bound as its evidence, no decision
needed. Non-empty: refuse the automatic path and flag that rule with exactly
which declared names moved. One honest subtlety, and it is why the "all types"
marker is not optional: an *additive* change can still change an open-ended
rule's answer. `NO_EMPTY_RECORD` matches `m_record(Record, _, _)` over every
type, so every `ADD_CLASS` widens what it judges, even though it names no class.
Under this option that rule declares "all types" and is correctly flagged by
every class addition, which is the right answer rather than a nuisance: it says
out loud which rules are open-ended. `INTERVAL_SANITY` names seven slots and
would pass untouched through the Shop's two-class revision.

**Cost.** One field in the check contract, paid once, with the OVR-000466 toll
of re-pinning existing contracts. No second engine, no second identity scheme.
The residual: a declaration is an assertion unless Core can check it against the
rule bytes, and Core cannot read Prolog. Two honest answers, both available:
verify the names exist in the contract (Core can), and leave rule-to-declaration
agreement to the adopter's test, as the document cell already does; or restrict
rules to a grammar Core can parse, which is Option C's territory.

### Option C. Rules as records in the KG, with a recorded activation act

**What.** Build what E-0457 described. A rule is admitted as a typed record
with its source, its verbatim sentence and its provenance, the way
`ShipmentRuleClaim` already is. A separate recorded act promotes a rule record
to a required check, naming the record and the check-contract identity it
compiles to. The rule's references to classes and slots are typed KG edges.

**Where the rule lives.** Its content and provenance in the KG as records; its
executable form still an identified artifact; the link between them recorded in
the ledger.

**EVIDENCE_BINDING.** The instance exists (`ShipmentRuleClaim`,
`context.yaml:33-35`, admitted at E-0451, "stored as knowledge and not run" at
E-0457). The standing order asks for it: rules as "gated, versioned,
hash-identified KG citizens whose acceptance is itself ontology-checked"
(`DELIMITATIONS.md:245-247`). The blocking constraint is in the same ruling:
"the separation of contract and tuple stays because a check reads the contract".

**ROLE_AND_CONSUMER.** Role: the semantic-history profile's change kinds, and
a new promotion act. Consumer: the Shop has one rule record today; the document
path has none. By `CORE_PROMOTION` that is **one** consumer, so a rule grammar
built for it would be an adapter, not core vocabulary, until a second consumer
with a different shape exists.

**USE_CLASSIFICATION.** Split deliberately.
- The **activation act** (a recorded, refusable promotion from rule record to
  required check, with the record id bound): `DESIGN_CONSTRAINT`, and it is the
  piece with real value now, because it answers "a check with provenance, a
  policy rule whose source is a claim in the ledger" (E-0457).
- The **rule grammar** (a typed, ontology-referencing rule language stored as
  records): `IMPLEMENTATION_CANDIDATE`, `MATURITY: PROPOSED`, and held there
  until the second consumer exists. The 2026-09-03 rule in `~/.claude/CLAUDE.md`
  and the skill's `CORE_PROMOTION` both say the same thing: one consumer means
  it is an adapter.

**Supports both?** Yes by construction. A rule record can name a Prolog
check contract as its executable form on day one. Nothing has to move for the
record to exist, and the two live rule sets keep running unchanged.

**F5 under it.** The strongest story available. The diff's moved facts name
classes and slots; the rule records reference them as typed edges; affected
rules fall out of graph reachability with no separate declaration to keep in
sync. F3 falls out the same way. This is the option where "automagically" is
literally true.

**Cost.** Highest, and there are three distinct costs, not one. First, a rule
grammar expressive enough for rules 1 to 4 and honestly incapable of rules 5 and
6, which are a string library rather than a rule; those stay in Prolog under any
design. Second, the self-reference question E-0457 flagged and did not answer:
if a rule is a record in the graph, what checks the change set that admits it,
and in what order. Third, "acceptance is itself ontology-checked" means the rule
records must be typed by the ontology, so the ontology grows a rule vocabulary,
which is itself subject to revision, which is a second-order version of the
problem being solved.

### Option D. A second engine: SHACL-SPARQL or SRL as an alternative check

**What.** Open the check contract to a second implementation kind with an
engine field, and admit a shapes graph with SPARQL constraints as a rule
artifact, pinned by digest exactly as `rules.pl` is.

**Where the rule lives.** In an RDF graph beside the ontology.

**EVIDENCE_BINDING.** Expressiveness is good but not sufficient: 3.1 puts
SHACL-SPARQL at four of our six rules fully, `NUMBER_IN_CITED_TEXT` partial and
`FORMULA_IN_SOURCE` not expressible, because `REPLACE` rewrites all
non-overlapping matches once and SPARQL has no fixed-point iteration. Its
genuine advantage is dependency declaration: a shape names its `sh:targetClass`
and `sh:path` in machine-readable RDF, so F5's intersection needs no new
declaration at all. Against it: the W3C's own rules track moved away from
rules-as-RDF on 25 August 2026 (3.0(b)); SHACL Core cannot join two focus nodes;
SHACL-SPARQL portability is explicitly weak ("SHACL Core processors that do not
also support SHACL-SPARQL ignore any SHACL-SPARQL constructs"), and silent
ignoring is what Malleus exists to refuse; and this repository already
classifies SHACL as a **projection**, never an authority (skill, "Accepted
compiler-enabled profile boundary"), a classification Core has never
contradicted in code (no occurrence of "shacl" anywhere under `src/`).

**ROLE_AND_CONSUMER.** Role: the check-contract boundary. Consumer: **none
today.** No adopter has asked for SHACL rules. By `ROLE_AND_CONSUMER` that alone
means the finding stays proposed and deferred rather than creating generic
machinery.

**USE_CLASSIFICATION.** `EXPLICIT_EXCLUSION` for v0, with the reason retained:
the one property Malleus needs that no shapes standard supplies is a rule set
with pinned byte identity evaluated against an isolated pre-commit candidate
(`DELIMITATIONS.md:102-107`), and adopting SHACL as a rule authority would
reverse its standing classification as a projection while buying four of six
rules and a second runtime. Keep SHACL where it is: an interoperability
projection with declared coverage and loss. Keep the exclusion recorded so the
question does not get re-asked from scratch.

**Supports both?** By definition, and it is the most expensive form of "both":
a second engine, a second identity scheme (IRIs), a second runtime dependency,
and a second conformance suite.

**F5 under it.** Free, and this is the honest credit due to the option: shapes
declare their own targets and paths, so the intersection with a compiled diff
needs nothing new. Option B buys the same property by declaring it, at a
fraction of the cost.

### The four at a glance

| | A. widen the ontology | B. declare dependencies | C. rules as records | D. second engine |
|---|---|---|---|---|
| rule lives in | ontology bytes | beside (unchanged) | KG records + artifact | shapes graph |
| covers our six | 0.5 | 6 (unchanged) | 4, with 5 and 6 staying in Prolog | 4.5 |
| second engine | no | no | no | **yes** |
| second identity scheme | no | no | record ids (already ours) | **yes, IRIs** |
| dependency declared | inherently | explicitly | as typed edges | inherently |
| F5 automatic | vacuous | **computable** | **by reachability** | free |
| consumers today | 2 | 2 | 1 | **0** |
| classification | DESIGN_CONSTRAINT + candidates | IMPLEMENTATION_CANDIDATE | DESIGN_CONSTRAINT (act) + PROPOSED (grammar) | EXPLICIT_EXCLUSION |

---

## 5. What I recommend Luis decide

The premise behind F4 is half right, and the half that is wrong is the
expensive half. The pain Luis felt is real and was measured at E-0458: one byte
moving in the ontology moves five identities, and before `REBIND_CHECK_CONTRACT`
it froze a live history dead. But that pain is not caused by the rules being
Prolog, and moving them inside the ontology would not have prevented it. It is
caused by one missing fact: **a rule records no dependency finer than a hash of
the whole ontology.** Of the six rules actually running, the in-ontology
constraint surface can absorb half of one, because four of them join two records
or read free text and no schema language expresses that; and SHACL, the one
place that does, is a second engine, a second identity scheme, and a
classification reversal for four of the six. So my recommendation is to decide
**Option B now**: make each rule declare the classes and slots it reads, checked
against the pinned contract, with an explicit "reads all types" marker for the
open-ended ones. That single field is what turns F5 from "automagic" into
arithmetic, gives F3 its dependency graph, is engine-neutral so it costs nothing
if you later want both, and rides the re-binding machinery that already exists
because Core derives the re-bound field rather than being told it. Alongside it,
take **Option A** wherever it is free, because anything that moves into the
ontology bytes stops being an F5 problem forever, and record **Option D** as an
explicit exclusion with its reason so it stops being re-asked. Keep **Option C**
as the design target and specify only its cheap half now, the recorded
activation act that promotes a rule record to a live check, because that is what
E-0457 already ruled and what `DELIMITATIONS.md` has been asking for since
before F4 was written; hold its rule grammar at `PROPOSED` until a second
consumer with a different shape exists, since the Shop's one `ShipmentRuleClaim`
makes it an adapter today. The cost of B is one field in the check contract,
paid once, which moves `contract_hash` for every existing contract and therefore
re-pins every policy, normative profile and frozen receipt that records a ledger
coordinate: OVR-000466 measured that exact blast radius when one change kind was
added, and the fix there was regenerating the family rather than grepping for
it. The residual I cannot close from here: a declaration Core cannot read
against the rule bytes is an adopter assertion, and closing it means either
trusting the adopter's test, as the document cell already does, or restricting
rules to a grammar Core can parse, which is Option C and a different decision.

---

## Sources

**Internal.** `docs/DELIMITATIONS.md` (102-107, 133-140, 217-247, 323-328);
`docs/PRINCIPLES.md` (38-56, 391-407); `docs/IMPLEMENTATION_STATUS.md`
(395-412); `docs/ARCHITECTURE.md` (298-328); `docs/ONTOLOGY_PROTOCOL.md` (204);
`.claude/skills/malleus-dev/SKILL.md` (research-to-core promotion gate;
architectural law 13 `EXECUTOR_ONLY`; accepted compiler-enabled profile
boundary); `.claude/skills/malleus-dev/references/CAPABILITIES.md` (logic
monitoring; check-contract re-binding; per-slot source relation);
`design/ONTOLOGY_MIGRATION_RECEIPT.md` (13-30, 91-133, 201-208);
`design/VERDICT_HARMONY.md` (30-55); `design/MALLEUS_INTELLECTUAL_SUBSTRATE.md`
(195-225, 495-525); `paper/research/1-owl-shacl-rules-stack.md` (whole);
`research/ontology_change_rules_recon/` (project.json, ledger.jsonl,
build/report.md, build/comparisons.json); `ROADMAP.md` F1-F5 (1015-1079);
`src/malleus/logic.py` (26-60, 74-116, 219, 267-292, 405-411);
`src/malleus/prolog_verifier.py` (80-97, 130-142);
`src/malleus/ontology.py` (112, 237-262, 1060-1070, 1450-1456, 1637-1646);
`src/malleus/_contract_compiler_profile.json` (node shapes for class, slot,
alternative, condition, slot_usage);
`src/malleus/_contract_pipeline/revision.py` (27-28, 200-300, 690-770, 845-895);
`src/malleus/_contract_pipeline/machine.py` (566-610);
`src/malleus/_contract_pipeline/knowledge.py` (775-790);
`private/shop-progressive-01/producer/workspace-stage-c/inputs/`
(rules.pl, logic.yaml, policy.json, context.yaml);
`paper-v4/experiment-v4/content-rules-doc-02/` (README.md 45-100, RESULTS.md
51-66, rules.pl 1-108 and 460-578, logic.yaml, policy.json);
`paper-v4/paper-ledger.md` E-0430, E-0451, E-0453, E-0457, E-0458, E-0459,
E-0486; overseer entries OVR-000437, OVR-000461, OVR-000464, OVR-000465,
OVR-000466; `handover/2026-09-16-overlord-claude-resume.md` (85-100);
`handover/2026-09-17-core-policy-rebinding.md` (1-120); `README.md` (197);
`pyproject.toml` (27-33).

**External, all fetched 2026-09-19.**
W3C: OWL 2 Overview https://www.w3.org/TR/owl2-overview/ (REC, 2nd ed.,
11 Dec 2012); SHACL https://www.w3.org/TR/shacl/ (REC 20 Jul 2017);
SHACL Advanced Features https://www.w3.org/TR/shacl-af/ (WG Note 8 Jun 2017);
SHACL 1.2 Core https://www.w3.org/TR/shacl12-core/ (WD 18 Sep 2026);
SHACL 1.2 Node Expressions https://www.w3.org/TR/shacl12-node-expr/ (WD
21 Jul 2026); SPARQL 1.2 RL https://www.w3.org/TR/sparql12-rl/ (WD 19 Sep 2026;
`/TR/shacl12-rules/` 301-redirects here; history at
https://www.w3.org/standards/history/shacl12-rules/);
SPARQL 1.1 Query https://www.w3.org/TR/sparql11-query/ (REC 21 Mar 2013),
`#func-replace`; RDF 1.2 Semantics https://www.w3.org/TR/rdf12-semantics/
(CR Snapshot 7 Apr 2026); RIF Overview https://www.w3.org/TR/rif-overview/
(WG Note, 2nd ed., 5 Feb 2013); PROV-O https://www.w3.org/TR/prov-o/ (REC
30 Apr 2013); SPIN Overview https://www.w3.org/Submission/spin-overview/
(Member Submission 22 Feb 2011); SWRL https://www.w3.org/Submission/SWRL/
(Member Submission 21 May 2004); N3 Team Submission
https://www.w3.org/TeamSubmission/n3/ (28 Mar 2011).
Non-W3C: N3 Community Group spec https://w3c-cg.github.io/N3/spec/ (undated);
ShEx 2.1 http://shex.io/shex-semantics/ (Final CG Report 8 Oct 2019);
From SPIN to SHACL https://spinrdf.org/spin-shacl.html;
LinkML https://linkml.io/linkml-model/latest/docs/rules/, `/ClassRule/`,
`/AnonymousClassExpression/`, `/classification_rules/`, `/slot_usage/`,
`/equals_expression/`, `/unique_keys/`,
https://linkml.io/linkml/schemas/advanced.html,
https://linkml.io/linkml/schemas/constraints.html,
https://linkml.io/linkml/data/validating-data.html,
https://linkml.io/linkml/generators/json-schema.html,
https://linkml.io/linkml/cli/generate.html, https://pypi.org/project/linkml/
(1.11.1, 2026-05-20); KGCL https://incatools.github.io/kgcl/,
https://github.com/INCATools/kgcl; RDFox https://docs.oxfordsemantic.tech/
and `/reasoning.html`; Soufflé https://souffle-lang.github.io/ (2.5,
24 Mar 2024); ROBOT diff https://robot.obolibrary.org/diff; Bubastis fork
https://github.com/dgarijo/bubastis.
Papers: Tao, Sirin, Bao, McGuinness, AAAI 2010, DOI 10.1609/aaai.v24i1.7525;
Motik, Horrocks, Sattler, WWW 2007, DOI 10.1145/1242572.1242681 (journal
version DOI 10.1016/j.websem.2009.02.001); Motik, Sattler, Studer, JWS 3(1),
2005, DOI 10.1016/j.websem.2005.05.001; Bellomarini, Sallinger, Gottlob,
PVLDB 11(9), 2018, DOI 10.14778/3213880.3213888; Noy and Klein, KAIS 6(4),
2004, DOI 10.1007/s10115-003-0137-2; Stojanovic, PhD thesis, 2004, DOI
10.5445/IR/1000003270; Klein and Noy, CEUR-WS Vol-71,
https://ceur-ws.org/Vol-71/Klein.pdf; Ahmetaj et al., ISWC 2025, DOI
10.1007/978-3-032-09527-5_8, arXiv:2508.00137; Zacouris, Ke, Acosta, ISWC 2025,
DOI 10.1007/978-3-032-09527-5_7; Ahmetaj, Ortiz, Šimkus, AMW 2024,
https://ceur-ws.org/Vol-3954/paper1130.pdf; Kondylakis and Plexousakis, ER 2012,
DOI 10.1007/978-3-642-34002-4_26; Kessentini, Sahraoui, Wimmer, SSBSE 2018,
DOI 10.1007/978-3-319-99241-9_12; Seifer, Hernández, Lämmel, Staab,
arXiv:2606.14309.

**Stated as not established.**
1. SHACL Core's inability to join two focus nodes, and its lack of any string
   transformation, are inferences from the exhaustive component list of §4. The
   Recommendation makes no negative statement, so these are strong readings, not
   quotations.
2. Whether SPARQL can be made to reach a fixed point on a string rewrite inside
   one constraint evaluation was not established; the claim here is only that no
   construct for it was found.
3. Exact rational comparison in SPARQL, which `NUMBER_IN_CITED_TEXT` needs, was
   not checked against SPARQL's numeric typing rules.
4. "SHACL shapes evolution" and "constraint evolution ontology" were searched
   for as named literature and **not found**. Anything citing them should be
   corrected.
5. ShEx's inability to compare across nodes is recorded as "no standard
   mechanism found", from the fetched specification page, not from an exhaustive
   reading of the 2.1 grammar.
6. The N3 Community Group report carries no publication date, and the phrase
   "open world" does not appear in it; the open-world characterisation follows
   from N3 being a superset of RDF plus its scoped `log:notIncludes`.
7. KGCL's inability to express a slot-range or `slot_usage` change is a bounded
   reading of its published change-class list, not a statement from its
   specification.
8. `docs/DELIMITATIONS.md:326-328` still carries the unverified residual that
   TerminusDB's core and schema checker are implemented in SWI-Prolog. Not
   checked here; it remains open and matters to any paper paragraph placed
   beside our Prolog contracts.
