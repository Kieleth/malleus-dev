"""Draw a seeded, stratified sample of witnesses from the named cells' review records.

The population of a cell is the `witnesses` array of its preliminary review
record, one entry per distinct witness. A draw is stratified proportionally to
each cell's population, at least one per cell, and is a function of the seed
alone: the population is ordered by `witness_key`, so a record whose witnesses
are rewritten in a different order draws the same sample as long as the keys and
the count are the same. The record digest travels with the sample, so a record
that changed after the draw is caught by the packet builder.

Three strata, one per invocation:

- neither option: the population is every witness of every named cell.
- `--only-label LABEL`: the population is the witnesses the review recorded with
  that label, and the draw is proportional inside it. A cell with no witness of
  that label is refused, because a stratum that silently drops a cell is not the
  stratum that was asked for.
- `--all-label LABEL`: every witness with that label, all cells, no sampling and
  no size. A cell with none of them is reported as zero and not refused.

The second and third exist because the recorded labels are lopsided. Kappa on a
draw from the whole population is arithmetic about a constant. A random stratum
inside `SUPPORTED` asks whether an independent judge finds anything the first
reviewer waved through, and a complete `PARTIAL` stratum is small enough to be
judged whole.

The output carries the recorded `source_support` because agreement is computed
against it later. It carries no rationale and no reading text.

`--cells` is required and has no default. A default would name a cell set that
goes stale the moment a cell is rebound or a run is added.

    .venv/bin/python paper-v4/evaluation-v4/sample/sample_witnesses.py \
        --cells run-22-v413 run-23 run-24 run-25 \
        --seed 20260912 --size 200 --only-label SUPPORTED \
        --output paper-v4/evaluation-v4/sample
"""

from __future__ import annotations

import argparse
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sample_common import (  # noqa: E402
    REVIEW_RECORD_SCHEMA,
    ROOT,
    SAMPLE_SCHEMA,
    SUPPORT_LABELS,
    Refusal,
    digest,
    markdown_record,
    refuse,
    write_json,
)


def record_path(root: Path, cell: str) -> Path:
    return root / "paper-v4" / "evaluation-v4" / cell / "review-record.preliminary.md"


def load_cell(root: Path, cell: str) -> dict:
    path = record_path(root, cell)
    if not path.exists():
        refuse(f"review record is missing for {cell}: {path}")
    source = path.read_bytes()
    root_object = markdown_record(source, f"{cell} review record")
    if root_object.get("schema") != REVIEW_RECORD_SCHEMA:
        refuse(
            f"{cell} review record schema is not {REVIEW_RECORD_SCHEMA}: "
            f"{root_object.get('schema')!r}"
        )
    witnesses = root_object.get("witnesses")
    if not isinstance(witnesses, list) or not witnesses:
        refuse(f"{cell} review record carries no witnesses")
    population: list[dict] = []
    keys: set[str] = set()
    for position, witness in enumerate(witnesses):
        if not isinstance(witness, dict):
            refuse(f"{cell} witness {position} is not an object")
        key = witness.get("witness_key")
        if not isinstance(key, str) or not key:
            refuse(f"{cell} witness {position} carries no witness_key")
        if key in keys:
            refuse(f"{cell} witness_key is not unique: {key}")
        keys.add(key)
        support = witness.get("source_support")
        if support not in SUPPORT_LABELS:
            refuse(f"{cell} witness {key} carries an unknown source_support: {support!r}")
        locators = witness.get("source_locators")
        if not isinstance(locators, list) or not locators:
            refuse(f"{cell} witness {key} cites no source_locators")
        for locator in locators:
            if not isinstance(locator, str) or not locator:
                refuse(f"{cell} witness {key} cites an empty locator")
        population.append(
            {
                "witness_key": key,
                "source_locators": list(locators),
                "recorded_source_support": support,
            }
        )
    population.sort(key=lambda entry: entry["witness_key"])
    return {
        "cell": cell,
        "record_path": str(path.relative_to(root)),
        "record_sha256": digest(source),
        "witnesses_in_record": len(population),
        "population": population,
    }


def allocate(counts: dict[str, int], size: int) -> dict[str, int]:
    """Largest-remainder apportionment, at least one per cell, capped per cell."""

    cells = list(counts)
    if not cells:
        refuse("no cells named")
    total = sum(counts.values())
    if size < len(cells):
        refuse(f"size {size} is below one per cell for {len(cells)} cells")
    if size > total:
        refuse(f"size {size} exceeds the {total} witnesses the cells hold")
    order = {cell: index for index, cell in enumerate(cells)}
    quota = {cell: size * counts[cell] / total for cell in cells}
    share = {cell: int(quota[cell]) for cell in cells}
    remainder = size - sum(share.values())
    by_fraction = sorted(
        cells, key=lambda cell: (-(quota[cell] - share[cell]), order[cell])
    )
    for cell in by_fraction[:remainder]:
        share[cell] += 1
    for cell in cells:
        share[cell] = min(max(share[cell], 1), counts[cell])
    while sum(share.values()) > size:
        donor = max(cells, key=lambda cell: (share[cell], -order[cell]))
        if share[donor] <= 1:
            refuse(f"size {size} cannot keep one witness per cell")
        share[donor] -= 1
    while sum(share.values()) < size:
        taker = max(cells, key=lambda cell: (counts[cell] - share[cell], -order[cell]))
        if share[taker] >= counts[taker]:
            refuse(f"size {size} exceeds what the cells can supply")
        share[taker] += 1
    return share


def _stratum(cell: dict, label: str | None) -> list[dict]:
    if label is None:
        return cell["population"]
    return [
        entry
        for entry in cell["population"]
        if entry["recorded_source_support"] == label
    ]


def _taken(cell: dict, keys: list[str]) -> list[dict]:
    by_key = {entry["witness_key"]: entry for entry in cell["population"]}
    return [
        {
            "cell": cell["cell"],
            "witness_key": key,
            "source_locators": by_key[key]["source_locators"],
            "recorded_source_support": by_key[key]["recorded_source_support"],
            "record_sha256": cell["record_sha256"],
        }
        for key in keys
    ]


def _sample(cells: list[dict], label: str | None, taken: dict[str, list[dict]], head: dict) -> dict:
    witnesses = [entry for cell in cells for entry in taken[cell["cell"]]]
    return {
        "schema": SAMPLE_SCHEMA,
        **head,
        "stratum": {
            "label": label,
            "population": "EVERY_WITNESS" if label is None else f"RECORDED_{label}",
        },
        "population_order": "WITNESS_KEY_ASCENDING",
        "cells": [
            {
                "cell": cell["cell"],
                "record_path": cell["record_path"],
                "record_sha256": cell["record_sha256"],
                "witnesses_in_record": cell["witnesses_in_record"],
                "witnesses_in_stratum": len(_stratum(cell, label)),
                "sampled": len(taken[cell["cell"]]),
            }
            for cell in cells
        ],
        "witnesses": witnesses,
    }


def draw(cells: list[dict], size: int, seed: int, label: str | None = None) -> dict:
    """A seeded proportional draw from the stratum, at least one per cell."""

    counts = {cell["cell"]: len(_stratum(cell, label)) for cell in cells}
    if label is not None:
        for cell, count in counts.items():
            if count == 0:
                refuse(
                    f"{cell} holds no witness recorded {label}; name only the cells that do"
                )
    share = allocate(counts, size)
    taken: dict[str, list[dict]] = {}
    for cell in cells:
        stream = f"{seed}:{cell['cell']}" if label is None else f"{seed}:{label}:{cell['cell']}"
        rng = random.Random(stream)
        keys = [entry["witness_key"] for entry in _stratum(cell, label)]
        taken[cell["cell"]] = _taken(cell, sorted(rng.sample(keys, share[cell["cell"]])))
    return _sample(
        cells,
        label,
        taken,
        {
            "seed": seed,
            "size": size,
            "stratification": "PROPORTIONAL_TO_STRATUM_COUNT_AT_LEAST_ONE_PER_CELL",
        },
    )


def complete(cells: list[dict], seed: int, label: str) -> dict:
    """Every witness of the stratum, all cells, no sampling. A cell may hold none."""

    taken = {
        cell["cell"]: _taken(
            cell, sorted(entry["witness_key"] for entry in _stratum(cell, label))
        )
        for cell in cells
    }
    return _sample(
        cells,
        label,
        taken,
        {
            "seed": seed,
            "size": sum(len(entries) for entries in taken.values()),
            "stratification": "COMPLETE_STRATUM_NOT_SAMPLED",
        },
    )


def build(
    root: Path,
    cells: list[str],
    seed: int,
    *,
    size: int | None = None,
    only_label: str | None = None,
    all_label: str | None = None,
) -> dict:
    if len(set(cells)) != len(cells):
        refuse("a cell is named twice")
    if only_label is not None and all_label is not None:
        refuse("--only-label and --all-label write different files; run the script twice")
    for label in (only_label, all_label):
        if label is not None and label not in SUPPORT_LABELS:
            refuse(f"{label!r} is not one of {list(SUPPORT_LABELS)}")
    if all_label is not None:
        if size is not None:
            refuse("a complete stratum has no size; drop --size")
        return complete([load_cell(root, cell) for cell in cells], seed, all_label)
    if size is None:
        refuse("a random draw needs --size")
    return draw([load_cell(root, cell) for cell in cells], size, seed, only_label)


def target_name(seed: int, only_label: str | None, all_label: str | None) -> str:
    if all_label is not None:
        return f"sample-{seed}-{all_label.lower()}-all.json"
    if only_label is not None:
        return f"sample-{seed}-{only_label.lower()}.json"
    return f"sample-{seed}.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--cells",
        nargs="+",
        required=True,
        help=(
            "the cell directories under paper-v4/evaluation-v4/ to draw from, named "
            "every time: a default would go stale the moment a cell is rebound"
        ),
    )
    parser.add_argument("--size", type=int, default=None)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument(
        "--only-label",
        default=None,
        help="draw only from the witnesses the review recorded with this label",
    )
    parser.add_argument(
        "--all-label",
        default=None,
        help="take every witness with this label, all cells, no sampling",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="directory the sample file is written into",
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args(argv)
    try:
        sample = build(
            args.root.resolve(),
            list(args.cells),
            args.seed,
            size=args.size,
            only_label=args.only_label,
            all_label=args.all_label,
        )
        target = args.output / target_name(args.seed, args.only_label, args.all_label)
        write_json(target, sample)
    except Refusal as refusal:
        print(f"REFUSED: {refusal}", file=sys.stderr)
        return 2
    print(f"wrote {target}")
    print(f"  stratification: {sample['stratification']}")
    print(f"  stratum: {sample['stratum']['population']}")
    for cell in sample["cells"]:
        print(
            f"  {cell['cell']}: {cell['sampled']} of {cell['witnesses_in_stratum']} "
            f"in the stratum, {cell['witnesses_in_record']} in the record"
        )
    print(f"  total: {len(sample['witnesses'])} at seed {sample['seed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
