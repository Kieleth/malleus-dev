"""Command-line entry point for the research-local GraphRecipe v0 harness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from .case_harness import (
    CaseHarnessError,
    ReceiptMismatch,
    assert_receipt,
    propose_pending_digests,
    run_experiment,
)
from .model import load_json_object


DEFAULT_CORPUS = Path(__file__).resolve().parents[4] / "conformance" / "graph_recipe" / "v0"


def _canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _manifest_for(corpus_root: Path, experiment_id: str) -> Path:
    root = corpus_root.expanduser().resolve(strict=True)
    declaration = load_json_object(root / "corpus.json")
    experiments = declaration.get("experiments")
    if not isinstance(experiments, list):
        raise CaseHarnessError(f"{root / 'corpus.json'} experiments must be an array")
    matches: list[Mapping[str, Any]] = []
    for index, value in enumerate(experiments):
        if not isinstance(value, Mapping):
            raise CaseHarnessError(
                f"{root / 'corpus.json'} experiments[{index}] must be an object"
            )
        if value.get("experiment_id") == experiment_id:
            matches.append(value)
    if len(matches) != 1:
        declared = sorted(
            value.get("experiment_id")
            for value in experiments
            if isinstance(value, Mapping) and isinstance(value.get("experiment_id"), str)
        )
        raise CaseHarnessError(
            f"experiment {experiment_id!r} is not declared exactly once; declared: {declared}"
        )
    locator = matches[0].get("manifest")
    if not isinstance(locator, str) or not locator.strip() or Path(locator).is_absolute():
        raise CaseHarnessError(f"experiment {experiment_id!r} has an invalid manifest locator")
    manifest = (root / locator).resolve(strict=True)
    try:
        manifest.relative_to(root)
    except ValueError as error:
        raise CaseHarnessError(
            f"experiment {experiment_id!r} manifest escapes the corpus root"
        ) from error
    if not manifest.is_file():
        raise CaseHarnessError(f"experiment manifest is not a regular file: {manifest}")
    return manifest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one frozen GraphRecipe v0 conformance case offline."
    )
    parser.add_argument("experiment_id")
    parser.add_argument("case_id")
    parser.add_argument(
        "--corpus",
        type=Path,
        default=DEFAULT_CORPUS,
        help="GraphRecipe v0 corpus root",
    )
    parser.add_argument(
        "--propose-digests",
        action="store_true",
        help="print pending digest replacement candidates without writing files",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        manifest = _manifest_for(arguments.corpus, arguments.experiment_id)
        receipt = run_experiment(manifest, arguments.case_id)
        if arguments.propose_digests:
            print(_canonical(propose_pending_digests(receipt, manifest, arguments.case_id)))
            return 0
        print(_canonical(receipt.as_dict()))
        assert_receipt(receipt, manifest, arguments.case_id)
        return 0
    except (ReceiptMismatch, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
