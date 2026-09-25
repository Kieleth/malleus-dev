# G2a: the G1 specimens as ordinary graph records

24 September 2026. Gate G2, witness a, of
[GEDANKENEXPERIMENTS-01.md](../GEDANKENEXPERIMENTS-01.md): Construction A of
[STORAGE-FLOWS-01.md](../STORAGE-FLOWS-01.md), ordinary graph records, with
named subgraphs (Construction D) where a specimen groups records. Results and
findings are in [RESULTS.md](RESULTS.md).

Role: research-local `CONFORMANCE_FIXTURE` evidence under the proposed
`OPTIONAL_PROFILE` for temporal semantic history. The selector here is not a
Core proposal and adds no `PROTOCOL_INVARIANT`. It reads the specimens in
`../g1/` and never writes them.

## Files

| File | Role |
|---|---|
| `graph.py` | Encoder and decoder. Specimen objects and changes to a graph of nodes, typed directed edges and named subgraphs; canonical JSON; prefix at a position; withholding records for a rebuild. |
| `query.py` | Query layer. Replays the prefix at `at` to derive versions, then answers the nine query kinds. Open choices are explicit selector parameters. |
| `admission.py` | Accepts one proposed change whole or refuses it whole, with a category, before anything is added. |
| `runner.py` | Runs every query and branch, the forbidden answers, the refusals, branch invariance, round trip, rebuild and the prefix check. Holds the list of findings. |
| `test_g2a.py` | Pytest over all of the above, plus broken variants that must turn red. |

## Commands

From the worktree root:

```sh
export PYTHONPATH=$PWD/src:$PWD
/Users/luis/Projects/malleus-dev/.venv/bin/python design/temporal/g2a/runner.py
/Users/luis/Projects/malleus-dev/.venv/bin/python design/temporal/g2a/runner.py --markdown
/Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider design/temporal/g2a/test_g2a.py
```

Standard library only. Nothing is imported from `src/malleus`.

## Graph type: a minimal stdlib graph, not `malleus.KnowledgeGraph`

`malleus.KnowledgeGraph` (`src/malleus/kg.py`) was read and not used, for two
reasons found in its code.

1. Its relation endpoints must be entities. `_validate_relation` refuses with
   "Source '...' is not an Entity" when an endpoint is a relation. G1-06 needs
   an assessment J1 whose subject is the relation A1, and an argument D1 whose
   premise is A1. Using `KnowledgeGraph` would force A1 to become an entity,
   which is the loss this gate is meant to detect, not to introduce.
2. It validates every write against a LinkML schema, closed-world. There is no
   schema for these temporal records, and writing one would be a second design
   artifact outside this gate.

The stdlib graph has one element namespace: a node id or an edge id can be an
edge endpoint. A RELATION object is an edge whose id is the object id. Every
other reference an object holds is a LINK edge with a structural id
`<owner>~<field>~<ordinal>`. No element is identified by a value. Composition with shipped Core
mechanisms is gate G3 in GEDANKENEXPERIMENTS-01.md; this witness stays off them.
