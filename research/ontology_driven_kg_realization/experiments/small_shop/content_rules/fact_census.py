"""Census of what the Prolog fact contract can see of one retained Shop history.

The executable witness for CORE_REQUIREMENT.md. It compiles the same facts the
verifier compiles and counts the ones that carry provenance. Read only.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

import malleus.compiler as api
from malleus.logic import FACT_PREDICATES, GraphFactCompiler


PROVENANCE_MARKERS = ("row:", "locator", "derivation", "assertion", "source_text")


def census(path: Path):
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    compiled = GraphFactCompiler().compile(replay.graph)
    return {
        "declared_predicates": sorted(
            f"{name}/{arity}" for name, arity in FACT_PREDICATES.items()
        ),
        "emitted_by_predicate": dict(
            sorted(Counter(fact.split("(", 1)[0] for fact in compiled.facts).items())
        ),
        "fact_contract_version": GraphFactCompiler.contract_version,
        "facts_total": len(compiled.facts),
        "provenance_bearing_facts": sum(
            1
            for fact in compiled.facts
            if any(marker in fact for marker in PROVENANCE_MARKERS)
        ),
        "records": len(compiled.record_ids),
        "retained_derivations": sum(
            len(json.loads(replay.retained_bytes(member.record_id))["derivations"])
            for member in replay.retained_inputs
            if member.record_id.startswith("plan:")
            and not member.record_id.endswith(":gaps")
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    args = parser.parse_args()
    print(json.dumps(census(args.history), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
