# GraphRecipe research runner

This runner executes the frozen `GE-000` through `GE-020` corpus through one
path shared by pytest and the interactive command. It is research-local. It is
not a public Malleus API and is not included in release artifacts.

Run the tests from the repository root:

```text
PYTHONPATH=src python -m pytest -q \
  research/ontology_driven_kg_realization/experiments/graph_recipe/test_cases.py
```

The frozen first-slice result and its bound identities are recorded in
`research/ontology_driven_kg_realization/experiments/graph_recipe/FIRST_SLICE_CONFORMANCE_REPORT.json`.
The corpus declaration, profile, and complete source-byte checksum set live at
`conformance/graph_recipe/v0/corpus.json`,
`conformance/graph_recipe/v0/profile.json`, and
`conformance/graph_recipe/v0/checksums.json`.

Run one case interactively:

```text
PYTHONPATH=src python -m \
  research.ontology_driven_kg_realization.experiments.graph_recipe.run_cases \
  GE-010-ONE-ENTITY alice
```

The command prints a canonical `ConformanceReceipt`. It never updates frozen
expected artifacts. Add `--propose-digests` to print proposed replacements for
pending digest obligations without writing files. The frozen corpus currently
has no pending digest obligations, so that mode is only useful while reviewing
a deliberate fixture change.

The report covers this research runner and the ten declared synthetic cases.
It does not make GraphRecipe a public or shipped Malleus capability, and it
does not establish behavior for `GE-030` or later experiments.
