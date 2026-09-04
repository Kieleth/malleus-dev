# Current public API reference

This page exercises Sphinx autodoc and autosummary against the public package
root and the public migration module. It does not promote contract-compiler
stages.

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
```
