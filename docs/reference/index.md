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
   malleus.compiler.KnowledgeChangeHistory
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

.. autoclass:: malleus.compiler.KnowledgeChangeHistory

.. autoclass:: malleus.compiler.PopulationPlanRefusal

.. autoclass:: malleus.compiler.PopulationPlanRefusalReason

.. autoclass:: malleus.compiler.DocumentAssertionCompilation

.. autoclass:: malleus.compiler.DocumentAssertionRefusal

.. autoclass:: malleus.compiler.DocumentAssertionRefusalReason
```
