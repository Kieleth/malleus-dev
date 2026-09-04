# Current public API reference

This page exercises Sphinx autodoc and autosummary against the public package
root, migration module, and narrow compiler facade. It does not promote private
compiler stages or CLI implementation modules.

`compile_population_plan` raises `PopulationPlanRefusal` with reason
`PopulationPlanRefusalReason.FAMILY_NOT_ADMITTED` when a plan contains event or
signal records.

`adapt_document_assertions` validates a document capture and emits the same
neutral population-plan grammar. Captured assertions remain evidence rather
than graph records.

`KnowledgeChangeHistory.compose_contract_revision` derives an additive
contract revision from two compiled contracts. The current policy admits added
classes, slots, and enum values and refuses added imports.

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
   malleus.compiler.adapt_document_assertions
   malleus.compiler.compile_contract_revision
   malleus.compiler.KnowledgeChangeHistory
   malleus.compiler.ContractRevision
   malleus.compiler.ContractRevisionRefusal
   malleus.compiler.ContractRevisionRefusalReason
   malleus.compiler.PopulationPlanRefusal
   malleus.compiler.PopulationPlanRefusalReason
   malleus.compiler.DocumentAssertionCompilation
   malleus.compiler.DocumentAssertionRefusal
   malleus.compiler.DocumentAssertionRefusalReason

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

.. autofunction:: malleus.compiler.adapt_document_assertions

.. autofunction:: malleus.compiler.compile_contract_revision

.. autoclass:: malleus.compiler.KnowledgeChangeHistory
   :members: compose_contract_revision, record_contract_revision

.. autoclass:: malleus.compiler.ContractRevision

.. autoclass:: malleus.compiler.ContractRevisionRefusal

.. autoclass:: malleus.compiler.ContractRevisionRefusalReason

.. autoclass:: malleus.compiler.PopulationPlanRefusal

.. autoclass:: malleus.compiler.PopulationPlanRefusalReason

.. autoclass:: malleus.compiler.DocumentAssertionCompilation

.. autoclass:: malleus.compiler.DocumentAssertionRefusal

.. autoclass:: malleus.compiler.DocumentAssertionRefusalReason
```
