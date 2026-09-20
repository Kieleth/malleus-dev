"""Stage the baseline producer's workspace and freeze what it was given.

The graph cells stage nine inputs from a pinned Core commit because their
producer runs a compiler whose bytes are part of the result. This producer runs
nothing. It reads a reading and a question file and writes prose, so the staging
is four files and a receipt, and the receipt's job is the same as the cells':
the digests it records are what `producer_task_sha256` and the answer file's own
`inputs` block are checked against later.

The declared inputs come from `run-contract.json`, not from a list restated
here, so a contract and a builder that disagree refuse rather than stage bytes
nobody declared. The tracked ones are read from the working tree, because none
of them is Core: they are this cell's own files, frozen beside this script.

    .venv/bin/python paper-v4/experiment-v4/reuse-01-baseline/prepare_producer.py \\
        --reading private/paper-v4-text-layer/selected-reading.json \\
        --output private/paper-v4-reuse-01-baseline/producer
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTRACT = HERE / "run-contract.json"
UNTRACKED_INPUTS = {"SELECTED_READING"}
WORK = "work"


class ProducerPreparationRefusal(ValueError):
    """The workspace cannot be staged from what is on disk."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def prepare(reading: Path, output: Path) -> dict[str, object]:
    contract = json.loads(CONTRACT.read_bytes())
    if contract["schema"] != "malleus.paper-v4.baseline-run-contract/v1":
        raise ProducerPreparationRefusal("the run contract is not this cell's")
    if contract["condition"] != "IN_CONTEXT_BASELINE":
        raise ProducerPreparationRefusal("the run contract is not the baseline's")

    private_root = (ROOT / "private").resolve()
    output = output.resolve()
    if output == private_root or not _inside(output, private_root):
        raise ProducerPreparationRefusal("producer output must be below private/")
    if output.exists():
        raise ProducerPreparationRefusal("producer output already exists")

    staged: dict[str, bytes] = {}
    for item in contract["declared_inputs"]:
        name = item["name"]
        if name in UNTRACKED_INPUTS:
            if not reading.is_file():
                raise ProducerPreparationRefusal(
                    f"declared input is not on disk: {name}"
                )
            staged[name] = reading.read_bytes()
            continue
        source = ROOT / item["source"]
        if not source.is_file():
            raise ProducerPreparationRefusal(f"declared input is not on disk: {name}")
        staged[name] = source.read_bytes()

    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    (output / WORK).mkdir()
    declared_targets: set[Path] = set()
    for item in contract["declared_inputs"]:
        target = output / item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(staged[item["name"]])
        declared_targets.add(target.resolve())

    actual = {
        path.resolve()
        for path in output.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual != declared_targets:
        raise ProducerPreparationRefusal("producer input closure is not exact")

    receipt = {
        "schema": "malleus.paper-v4.baseline-producer-input-receipt/v1",
        "run_id": contract["run_id"],
        "condition": contract["condition"],
        "questions_are_visible_to_this_producer": contract[
            "questions_are_visible_to_this_producer"
        ],
        "producer": {
            "model": contract["producer"]["model"],
            "skill": contract["producer"]["skill"],
            "isolation": contract["producer"]["isolation"],
            "workspace": str(output.relative_to(ROOT)),
        },
        "files": [
            {
                "name": item["name"],
                "path": item["target"],
                "sha256": _digest((output / item["target"]).read_bytes()),
            }
            for item in contract["declared_inputs"]
        ],
        "run_contract_sha256": _digest(CONTRACT.read_bytes()),
        "status": "FROZEN",
    }
    receipt_path = output.parent / "producer-input-receipt.json"
    receipt_path.write_bytes(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    )
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reading", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        receipt = prepare(arguments.reading, arguments.output)
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"baseline-producer: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
