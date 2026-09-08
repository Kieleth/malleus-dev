# Initial supplier source to candidate

This is a REFERENCE_IMPLEMENTATION of an adopter source mapper and preparation
coordinator under the selected compiler-enabled state-version profile. The
source grammar, four-field mapping and synthetic e4/B/Y/1 attribution are the
already frozen ADOPTER_CHOICE. Tests are CONFORMANCE_FIXTURE. No Core contract,
public change identity, fixture/TBox extension or new accepted authority is added.

Claim: independently retain the one-row initial source and derive its existing
SupplierOrderState through ordinary public population compilation, preparation
and KCS admission. RET-010 O1, X1 and their relation remain unchanged. The
smallest observation is that preparation leaves only the complement accepted;
only the separate admission introduces supplier-order-state:B:e4, and JSONL-only
reopen traces that fact to exactly the one-row source, not the historical e4/e7
file or the expected amendment oracle.

The pure initial mapper consumes exact source bytes/digest, the frozen complete
mapping and an explicit source ID. It returns canonical existing population-plan
fields with no supersession. It uses the same closed JSONL parser and field
projection as the existing observed-replacement mapper. Source quantity is
faithfully mapped, not checked against the goal: representable quantities two
and three must not be rewritten to one or treated as goal verdicts. Missing,
mistyped, duplicate, ambiguous, unsupported or hash-mismatched inputs refuse.

The preparation coordinator consumes that source/mapping, explicit source,
artifact, mapping and plan IDs, the selected history profile, and actor/time.
It binds the exact mapper/coordinator implementation identity in the plan,
uses public structural source/evidence constructors, retains inputs and asks
the public population path to prepare the existing KCS. It never admits that
candidate or calls graph mutation methods. The caller separately invokes
admit_structural_change. Preparation is not pure: evidence retention advances
the single history, as the existing Core contract declares. This multi-stage
workflow is not represented as one atomic transaction. Individual Core appends
and admission retain their actual atomicity boundaries.

The coordinator validates source and mapping before retention. It supplies no
required ID, profile, actor, time, missing source field or quantity default.
Existing Source/Population/KnowledgeChange refusal types are preserved; source
mapping refusals remain SupplierInputError. A stale prepared KCS fails at Core
admission without changing accepted state or ledger bytes.

Conformance: exact one-row lineage; complete mapping and ORDER_ONLY occurrence;
source versus goal separation; malformed/ambiguous/digest refusal; no-I/O pure
mapping; immutable deterministic output; no supplier state before admission;
unchanged complement; stale admission; JSONL-only reopen; and no reads of the
historical supplier source or amendment oracle. Old model and replacement-mapper
tests must still pass after sharing their field-projection implementation.

This proves initial source population only, not Re-entry synthesis, an executed
amendment, observed success or episode closure. Another implementation has not
demonstrated replacement. No observer, effect, second writer or Core interpreter
is introduced. Runtime dependencies remain those already declared by the project.

Dependencies: InitialMapper consumes SourceBytes and Mapping; InitialMapper
produces PopulationFields; Coordinator consumes those fields and owning History;
Coordinator produces existing PopulationPreparation/KnowledgeChangeSet;
CoreAdmission alone applies that KCS; CoreReplay derives the accepted KG.

Pre-action checks: no server/endpoint, installation, production replacement,
new Core/public ontology surface or external effect. Test requirements precede
the new mapper/preparation implementation.
