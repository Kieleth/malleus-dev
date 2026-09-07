# Current Shop evidence, 6 September 2026

These eight files were generated from Core
`7c5fdb491721122b6e0c7243862935acc8303a1f` in fresh temporary histories using
the existing correction, object-event and showcase runners. Tests require
exact bytes, including every identity. This is a conformance evidence
generation, not a new protocol, ontology, source set or release.

The earlier files remain at `correction/evidence-role-v1/`,
`object_event/evidence.json` and `showcase/evidence/`, relative to the parent
Small Shop directory. `test_evidence_archive.py` pins all eight historical
hashes and proves that both old graph files and the object-event observations
remain unchanged. The original published correction generation at
`correction/evidence/` is also untouched.

Why another generation? Compiler commit `e4fa5fd` changed an error message.
The compiled artifact records the compiler producer's bytes, so that change
also changed the retained artifact and all dependent history fingerprints.
It did not change these Shop facts. The three old byte-regeneration tests pass
at that commit's direct parent and fail afterwards. The
[RCA and validation record](../../../../../handover/2026-09-06-shop-evidence-refresh.md)
records the exact boundary.

The runners still write to an explicitly chosen output directory. The showcase
evidence command now defaults to `build/small-shop-showcase-evidence`, never
to historical evidence. Future drift must be inspected and recorded; do not
remove identity comparisons or overwrite earlier generations to make CI green.
