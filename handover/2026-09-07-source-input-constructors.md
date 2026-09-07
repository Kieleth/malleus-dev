# Default source-input constructors

Luis approved this bounded Core cleanup after the fresh supplier-file proof.

## Contract before implementation

Role: REFERENCE_IMPLEMENTATION of the existing OPTIONAL_PROFILE selected by
`STRUCTURAL_HISTORY_BUNDLE`. No base protocol invariant or custom binding changes.
The CLI and two Shop runners are concrete consumers of duplicated construction.

Claim: public `structural_source_anchors` and `structural_evidence_anchor` build
the existing immutable `KnowledgeAnchorInput` values from exact bytes, explicit
record IDs and media type. The source constructor returns the ordered artifact
and source pair; the evidence constructor returns one evidence anchor. Neither
reads a file, receives history, appends, admits, invents an ID, or interprets a
source. Existing `append_anchors` owns validation and atomic persistence.

Input errors use `KnowledgeChangeRefusal(MALFORMED_HISTORY)`: content must be
exact bytes and IDs/media type must be nonempty strings. Empty byte content is
valid. Duplicate or conflicting history identities remain the ledger's check.
The constructors use the shipped bundle's existing event vocabulary only;
custom bindings continue to use `KnowledgeAnchorInput` directly. No new wire,
profile or capability-negotiation mechanism is introduced.

Smallest observation: exact equality with independently authored current event
bytes, no-I/O construction, changed content changes its digest, batch refusal
preserves history bytes, and complete Shop replay reproduces frozen evidence.
Reuse: canonical JSON/digest functions, KnowledgeAnchorInput, the installed
machine and binding, append_anchors, the existing CLI and Shop tests.

Dependency projection:

```text
DefaultSourceInputConstructors implements DefaultStructuralInputConstruction
DefaultSourceInputConstructors consumes ExactBytesAndExplicitRecordIDs
DefaultSourceInputConstructors produces KnowledgeAnchorInput
DefaultSourceInputConstructors governedBy STRUCTURAL_HISTORY_BUNDLE
CompilerCLI consumes KnowledgeAnchorInput
DefaultShop consumes KnowledgeAnchorInput
FreshShopImport consumes KnowledgeAnchorInput
KnowledgeChangeHistory.append_anchors consumes KnowledgeAnchorInput
DefaultSourceInputConstructors conformsTo SourceInputConstructorTests
```

Replaceability is not claimed. Byte parity is a regression check, not evidence
of a different conforming engine. Mapping, source observation, normalization,
domain correction, runtime policy, arbitrary binding generation, dependency
updates, package/version changes, release and publication are excluded.

The same slice clarifies an already author-endorsed distinction in Core's
principles: structural validity, source faithfulness and use-specific sufficiency
need separate support. Replay proves reconstruction; it does not prove the
other two or world truth. No evaluation API or mandatory coverage policy is added.

## Execution evidence

The shared paper/research worktree is excluded. Work runs in an isolated local
clone of `63a05659`, using the repository's configured CPython 3.12 environment.
There are no dependency installs or wheel/version changes.

RED `70d8861` collected ten expected failures for the absent constructors and
unreplaced consumers; the pre-existing complete fresh-Shop import still passed
against its frozen report. GREEN `f65e929ee10ccc65dc84482851ab1c654b2ac6e6`,
tree `6f3e0270ca8f49285104f2ddf0802133e433fb46`, exposes the two constructors,
removes all three consumers' handwritten retention event construction, and
removes the now-unused CLI event serializer. The four changed runtime/runner
files have 121 additions and 129 deletions. This is not an additional runtime
policy or a second serializer for custom bindings.

Focused command, with the configured workspace interpreter used by absolute
path in the isolated clone:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_source_input_constructors.py tests/contract_compiler/pareto/test_compiler_cli.py tests/contract_compiler/pareto/test_fresh_shop_import.py --tb=short
```

Final focused result: 37 passed. It executes the documented constructor example,
checks public signatures and the no-I/O boundary, compares independently authored
event bytes, rejects malformed inputs, and exercises atomic ledger refusal and
reopen. The fresh-Shop command runs twice and still reproduces the exact frozen
report: six change sets, twelve historical records, eleven current records,
59 events, and the same ledger SHA-256
`c20c0c802b695a34983de1245b8f20cd3eba6ecbf2ce580ac213c316fe0cba7f`.
No source, mapping, ontology, profile, machine, binding or frozen evidence bytes
changed. Source interpretation remains the existing adopter's responsibility.

Sphinx API reference, a runnable guide example and implementation status expose
the public methods. The principles now separate structural validity, source
faithfulness and use-specific sufficiency, as explicitly endorsed by Luis.
The associated guard checks those distinct claims, not their semantic truth.

Complete compiler/Shop/Re-entry selection: 854 passed, one preserved historical
xfail. Documentation, integration and ledger selection: 490 passed. These were
two separate successful invocations, not a claimed full-repository run. Focused
counts must not be added to overlapping broad counts.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto research/ontology_driven_kg_realization/experiments/small_shop research/semantic_reentry_protocol --tb=short
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_docs.py tests/test_contract_compiler_integration.py tests/test_contract_compiler_ledger.py --tb=short
```

Changed-file Ruff, formatting and diff checks passed. The standalone integration
check validates 75 workstreams, 39 cards and four selections. The successful docs
suite includes strict HTML, exact Sphinx public API inventory and source-pure
example checks. Existing strict policies were not relaxed.

The final evidence-only revision is rendered and checked again before local
integration. No remote push or release gate is included in this slice.

## Scoped self-inquisition

`protocol_role_is_explicit`: default reference constructors, not universal rules.
`optional_profile_stays_optional`: custom bindings retain their existing path.
`protocol_authority_is_data`: the identified default machine, binding and policy
remain unchanged; constructors only assemble their existing input vocabulary.
`single_ledger_knowledge_change`: source registration remains evidence retention,
not a graph write or admission. The existing atomic gate remains authoritative.
No ontology rite is needed because no schema changed. No new protocol behavior,
observer, generalized mapping engine, cross-language parity or release is claimed.

## Separate consumer requirement, pending Core review

The Re-entry specialist reports a missing way to persist protocol-only external
action lifecycle events in the same KCS history, against predecessor `63a05659`.
Its isolated design and reproducer remain consumer-owned. This is recorded as
a proposed composition requirement, not an independently verified Core defect,
an API decision or an implementation addition here. The old retained e7 is not
a fresh external observation. Review that dependency-closed request separately
after this cleanup; source-input construction does not solve it.
