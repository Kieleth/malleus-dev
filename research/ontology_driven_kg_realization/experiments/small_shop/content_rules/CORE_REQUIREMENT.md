# Prolog fact contract v2 carries no provenance

Status: open request. Nothing here is implemented, and nothing under `src/malleus`
was changed. The Shop rule layer in this directory ships without the rule this
gap blocks, and says so in [README.md](README.md).

## Consumer requirement

An adopter wants one admission rule: **a record property that cites a source cell
must carry a value the cited cell supports**. The fault-injection control on the
paper's document path recorded that nothing on the admission path makes that
comparison, so a producer can copy a sentence honestly, bind it by digest, and
put any well-typed value it likes in the record
(`paper-v4/experiment-v4/fault-injection-01/RESULTS.md`, gap 1: five trials
admitted, invisible).

The Shop already runs adopter rules at admission through the public policy path:
a `PolicyProgram` with a pinned `check_contract_identity`, executed by
`PrologVerifier` over the candidate subgraph, with a violated outcome refusing
the whole atomic admission. That path works and is not in question here.

## The finding

`PrologVerifier` sees exactly what `GraphFactCompiler` emits, and
`GraphFactCompiler.compile` (`src/malleus/logic.py:284`) builds every fact from
`graph.snapshot()`. The complete input vocabulary is fixed at
`src/malleus/logic.py:37`, `FACT_CONTRACT_VERSION = "2"`:

```text
m_ontology_hash/1  m_type/1   m_mixin/1     m_subtype/2  m_has_mixin/2
m_record/3         m_relation/4  m_property/4  m_list/3  m_list_item/5
```

None of them carries a derivation, a source locator, or retained source text.
Derivations live in the population plan and the change set. They are retained in
the same history, and they never reach the graph, so they never reach a rule.

## Executable witness

```sh
PYTHONPATH=src:. .venv/bin/python -m \
  research.ontology_driven_kg_realization.experiments.small_shop.content_rules.run \
  /tmp/shop-content-rules.jsonl

PYTHONPATH=src:. .venv/bin/python -m \
  research.ontology_driven_kg_realization.experiments.small_shop.content_rules.fact_census \
  /tmp/shop-content-rules.jsonl
```

Observed on the honest Table 1 population, 21 rows, 106 current records:

```json
{
  "fact_contract_version": "2",
  "facts_total": 549,
  "provenance_bearing_facts": 0,
  "records": 106,
  "retained_derivations": 294
}
```

549 facts compiled, none provenance-bearing, while the same history retains 294
derivations naming the exact source cell behind every property. A rule can read
the value and cannot read what the value claims to come from.

## What this blocks, exactly

The rule cannot be written. It needs two terms per property that no predicate
supplies: the locator the derivation names, and the retained bytes of the cell at
that locator. Both are present in the history and absent from the fact set.

Two workarounds were considered and neither was taken:

- Declaring adopter provenance types and staging them into a check-only overlay
  keeps everything in Prolog, at the cost of a check receipt whose
  `candidate_state_digest` describes a graph that is never accepted. That
  weakens the attestation the receipt exists to make.
- Retaining provenance as real domain records changes the admitted records, which
  is the thing the comparison against the connected story exists to hold fixed.

## The request

Extend the fact contract with provenance predicates and bump
`FACT_CONTRACT_VERSION`. A shape that would serve this consumer, offered as an
illustration and not as a proposed spelling:

```text
m_derivation(RecordId, PropertyName, SourceId, Locator)
m_source_cell(SourceId, Locator, Text)
```

This is a fact-contract extension with a version bump, not a change to admission,
policy, verdict or KG semantics. `LogicContract.fact_contract_version` is already
pinned per contract and `PrologVerifier` already compares it, so an existing
contract at version 2 keeps compiling against the old vocabulary.

Not requested: a new rule language, a derivation-aware admission check inside
Core, a provenance record family in the graph, any change to the outcome or
verdict grammar, or a generic side-input mechanism for rules.

## Related observation, not part of this request

`m_record/3` carries the record type exactly as the caller spelled it, short name
or URI, while `m_type/1` and `m_subtype/2` carry the registry's URIs. A rule
therefore cannot join a record to its ontology ancestors. The conflict rule in
this directory is keyed on the Shop's quantity slots instead of on a
`RecordedOrderState` subtype test for that reason. Recorded because it was hit
while writing the rules; no decision has been asked for or given.
