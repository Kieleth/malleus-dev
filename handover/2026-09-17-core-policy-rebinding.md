# Policy re-binding across an additive contract revision

The census under `private/shop-progressive-01/census/revision-01` (E-0458) found
that an adopter with a rule layer can never grow its ontology. Core records the
additive revision and the graph replays byte-identical, but the rule layer
cannot follow: re-pinning the same rule bytes to the new ontology hash moves the
check contract identity, hence the policy, hence the normative profile, and
`compile_contract_revision` refuses
`INCOMPATIBLE_CONTRACT: domain revision changes the normative protocol profile`.
Keeping the old pin makes every later admission fail
`Logic contract and compiled facts use different ontologies`. Both refusals are
right alone. Together they are a dead end.

This candidate lets an additive revision carry the re-binding as a declared,
recorded act.

## The slice, bound before any code

**Profile classification.** `OPTIONAL_PROFILE`, the compiler-enabled
semantic-history profile. This is not a base-protocol invariant: an adopter that
does not select the compiler-enabled profile, or that selects it without a
policy whose required checks pin an ontology, is unaffected and gains no
guarantee. The lowest affected profile is the one `KnowledgeChangeHistory`
already governs; nothing in `docs/PRINCIPLES.md`'s base contract moves.

1. **The exact claim.** An additive contract revision may carry, as a declared
   part of the same revision, the re-binding of the selected policy's required
   check contracts to the target ontology, when and only when nothing but the
   ontology binding inside each check contract changes. The revision refuses,
   with a typed reason naming what moved, when anything else about the policy
   moves.
2. **The smallest observation.** One Small Shop history with a check contract
   pinned to the compiled ontology: today the re-binding revision refuses
   `INCOMPATIBLE_CONTRACT`; after the change it is recorded, a later admission
   under the re-pinned check identity is accepted, the earlier check receipts
   still verify against their recorded identities, and reopen replays the same
   graph. Negative controls: changed rule bytes, an added check, a changed
   verdict, each refused with its own typed reason and the ledger byte-identical.
3. **The artifact reused.** `compile_contract_revision`,
   `ContractRevisionPolicy`, `PartialEffectiveContract`,
   `NormativeAdmissionProfile`, `PolicyProgram` and the existing
   `CONTRACT_REVISION_RECORDED` event. No new stage, no new authority, no new
   store.
4. **Excluded.** General policy migration. A revision that changes rule bytes,
   adds or removes a required check, changes a verdict mapping, its precedence,
   the policy identifier, the set of bound policies or the protocol machine
   program. Core still executes no Prolog and produces no check outcome. The
   adopter runner is not changed here.
