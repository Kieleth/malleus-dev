# GraphRecipe v0 conformance corpus

This directory is the public-safe, synthetic corpus for the accepted first
GraphRecipe TDD slice: `GE-000`, `GE-010`, and `GE-020`.

`profile.json` is the fixture wire contract. `diagnostics.json` is the closed
diagnostic registry for this slice. `corpus.json` is the discovery manifest.
Every negative case contains complete inputs and complete expected artifacts;
no case inherits a patch from another case.

The profile freezes the canonical payload for every semantic digest. All
required source, effective-recipe, invocation, plan, candidate, and final-state
digests are reviewed values, with no pending sentinels. Each case manifest pins
the exact source bytes of its declared profile, inputs, and expected artifacts.
`checksums.json` independently covers every file in this directory except
itself, using exact source-byte SHA-256 values.

The corpus is self-contained and offline. Raw recipe bytes remain evidence,
while recipe meaning, invocations, plans, candidates, and graph state have
separate identities. The checksum set proves the bytes being examined, not the
completeness of GraphRecipe beyond the declared `GE-000` through `GE-020`
slice.

The corpus contains only invented people, organizations, identifiers, and
values. It contains no production data, credentials, network locations, or
mutable remote dependencies.
