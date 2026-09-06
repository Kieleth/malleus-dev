"""Print the partial effective contract identity of one accepted ontology closure.

The producer of a document cell never writes a contract identity: run-21's
document adapter writes it into the plan from the identity the runner reads off
the retained history. A producer that writes its own neutral population plans
has to carry that identity itself, and it cannot compute one, because the
identity binds the validated fact set to the shipped structural admission
profile and the producer holds neither.

So the parent computes it here, between the gate and phase two, and supplies it
with the plan coordinate. Nothing is composed that Core does not ship: the
normative profile is the shipped structural bundle's and the composition is
Core's own ``compose_partial_effective_contract``. Nothing is written and no
ledger is touched.

    .venv/bin/python paper-v4/experiment-v4/shop-01/contract_identity.py \
        --root shop --source shop <ontology> --source malleus <malleus.yaml> ...
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import malleus.compiler as api


class IdentityRefusal(ValueError):
    """The ontology closure does not compile."""


def identity(*, root_locator: str, sources: dict[str, bytes]) -> dict[str, str]:
    compilation = api.compile_linkml_contract(
        root_locator=root_locator, sources=sources
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=api.STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    return {
        "contract_identity": partial.identity,
        "validated_fact_set_sha256": compilation.artifact.validated_fact_set_sha256,
        "structural_history_bundle_sha256": api.STRUCTURAL_HISTORY_BUNDLE.identity,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="root source locator")
    parser.add_argument(
        "--source",
        action="append",
        nargs=2,
        required=True,
        metavar=("LOCATOR", "PATH"),
        help="one exact source locator and file; repeat for the whole closure",
    )
    arguments = parser.parse_args(argv)
    sources: dict[str, bytes] = {}
    for locator, path in arguments.source:
        if locator in sources:
            raise IdentityRefusal(f"source locator is repeated: {locator}")
        sources[locator] = Path(path).read_bytes()
    if arguments.root not in sources:
        raise IdentityRefusal(f"root locator is not among the sources: {arguments.root}")
    try:
        report = identity(root_locator=arguments.root, sources=sources)
    except (OSError, TypeError, ValueError) as error:
        print(f"contract-identity: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
