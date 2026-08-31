# Malleus documentation

This repository build presents the public guides and validated engineering
projections. It does not publish a site or create a release artifact.

Start with the
[protocol boundary taxonomy](protocol-boundary-taxonomy). It
distinguishes portable protocol invariants from optional profiles, the current
reference implementation, conformance fixtures, and adopter choices.

```{toctree}
:maxdepth: 2

ADOPTION_GUIDE
ARCHITECTURE
ASSENT_PLAN
ASSENT_PROTOCOL
DELIMITATIONS
EFFECT_PROTOCOL
IMPLEMENTATION_STATUS
KNOWLEDGE_GRAPH_PROTOCOL
ONTOLOGY_PROTOCOL
PRINCIPLES
RECIPES
RECON_CONTRACT
contract_compiler/index
reference/index
```

The executable example below proves the documentation toolchain itself. It is
not a compiler or runtime API example.

```{doctest}
>>> {"manifest": "validated"}["manifest"]
'validated'
```
