# Current public API reference

This page exercises Sphinx autodoc and autosummary against the public package
root, migration module, narrow compiler facade, and pack checkers. It
does not promote private compiler stages or CLI implementation modules.

`compile_population_plan` raises `PopulationPlanRefusal` with reason
`PopulationPlanRefusalReason.FAMILY_NOT_ADMITTED` when a plan contains event or
signal records.

`adapt_document_assertions` validates a document capture and emits the same
neutral population-plan grammar. Captured assertions remain evidence rather
than graph records.

`trace_population_record` follows one accepted record through its change set,
population plan, history profile, field derivations, and retained inputs. It is
read-only and refuses to guess when a plan is absent or inconsistent.

`KnowledgeChangeHistory.compose_contract_revision` derives an additive
contract revision from two compiled contracts. The current policy admits added
classes, slots, and enum values and refuses added imports.

`validate_pack_grounding` checks the closed provenance annotation on an
optional knowledge pack or project ontology. It checks citation structure, not
the intellectual suitability of a cited vocabulary.

`validate_pack_conformance` checks an edited pack against exact reference
bytes. It permits documentation changes, new declarations, and new enum values
while refusing removal or strengthening of the reference declaration surface.
Reference imports must remain unique and set-equivalent.

```{eval-rst}
.. autosummary::

   malleus.OntologyRegistry
   malleus.OntologySource
   malleus.OntologyImportResolution
   malleus.OntologyDefinitionSource
   malleus.OntologySourceClosure
   malleus.migration.MigrationVerification
   malleus.migration.MigrationVerifier
   malleus.migration.MigrationAwareJsonlLedger
   malleus.compiler
   malleus.compiler.compile_linkml_contract
   malleus.compiler.compile_population_plan
   malleus.compiler.prepare_population_change
   malleus.compiler.trace_population_record
   malleus.compiler.adapt_document_assertions
   malleus.compiler.compile_contract_revision
   malleus.compiler.KnowledgeChangeHistory
   malleus.compiler.ContractRevision
   malleus.compiler.ContractRevisionRefusal
   malleus.compiler.ContractRevisionRefusalReason
   malleus.compiler.PopulationPlanRefusal
   malleus.compiler.PopulationPlanRefusalReason
   malleus.compiler.PopulationRecordTrace
   malleus.compiler.PopulationTraceRefusal
   malleus.compiler.PopulationTraceRefusalReason
   malleus.compiler.DocumentAssertionCompilation
   malleus.compiler.DocumentAssertionRefusal
   malleus.compiler.DocumentAssertionRefusalReason
   malleus.inquisition
   malleus.inquisition.validate_pack_conformance
   malleus.inquisition.validate_pack_grounding
   malleus.inquisition.PackConformanceReceipt
   malleus.inquisition.PackGroundingReceipt
   malleus.inquisition.PackGroundingRefusal
   malleus.inquisition.PackGroundingRefusalReason
   malleus.inquisition.PACK_GROUNDING_RITE_IDENTITY

.. automodule:: malleus

.. autoclass:: malleus.OntologyRegistry
   :members: source_closure

.. autoclass:: malleus.OntologySource

.. autoclass:: malleus.OntologyImportResolution

.. autoclass:: malleus.OntologyDefinitionSource

.. autoclass:: malleus.OntologySourceClosure

.. autoclass:: malleus.migration.MigrationVerification
   :members: receipt_digests

.. autoclass:: malleus.migration.MigrationVerifier
   :members: verify

.. autoclass:: malleus.migration.MigrationAwareJsonlLedger
   :members: read_verified

.. automodule:: malleus.compiler

.. autofunction:: malleus.compiler.compile_linkml_contract

.. autofunction:: malleus.compiler.compile_population_plan

.. autofunction:: malleus.compiler.prepare_population_change

.. autofunction:: malleus.compiler.trace_population_record

.. autofunction:: malleus.compiler.adapt_document_assertions

.. autofunction:: malleus.compiler.compile_contract_revision

.. autoclass:: malleus.compiler.KnowledgeChangeHistory
   :members: compose_contract_revision, record_contract_revision

.. autoclass:: malleus.compiler.ContractRevision

.. autoclass:: malleus.compiler.ContractRevisionRefusal

.. autoclass:: malleus.compiler.ContractRevisionRefusalReason

.. autoclass:: malleus.compiler.PopulationPlanRefusal

.. autoclass:: malleus.compiler.PopulationPlanRefusalReason

.. autoclass:: malleus.compiler.PopulationRecordTrace

.. autoclass:: malleus.compiler.PopulationTraceRefusal

.. autoclass:: malleus.compiler.PopulationTraceRefusalReason

.. autoclass:: malleus.compiler.DocumentAssertionCompilation

.. autoclass:: malleus.compiler.DocumentAssertionRefusal

.. autoclass:: malleus.compiler.DocumentAssertionRefusalReason

.. automodule:: malleus.inquisition

.. autofunction:: malleus.inquisition.validate_pack_conformance

.. autofunction:: malleus.inquisition.validate_pack_grounding

.. autoclass:: malleus.inquisition.PackConformanceReceipt

.. autoclass:: malleus.inquisition.PackGroundingReceipt

.. autoclass:: malleus.inquisition.PackGroundingRefusal

.. autoclass:: malleus.inquisition.PackGroundingRefusalReason

.. autodata:: malleus.inquisition.PACK_GROUNDING_RITE_IDENTITY
```
