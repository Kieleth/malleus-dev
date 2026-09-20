"""Agreement between the recorded labels of a sample and one or more judge records.

Per cell and overall: how often the judge's label equals the label the review
recorded, Cohen's kappa over the protocol's four-label space, and the confusion
counts in both directions. With two or more judge records it also reports each
pair of judges against each other, which is the number that says whether a
disagreement with the record is the judge or the task.

With no `--judge-record` it prints the sample's composition and the prevalence of
the recorded labels in it, and nothing else: what a drawn stratum contains, before
any judge exists.

Generalised from `paper-v4/evaluation-v4/reliability.py`, which reads one
hardwired question of one cell from an absolute path. Nothing is imported from
it. This script computes no faithfulness figure and changes no record.

    .venv/bin/python paper-v4/evaluation-v4/sample/agreement.py \
        --sample paper-v4/evaluation-v4/sample/sample-20260911.json \
        --judge-record private/paper-v4-evaluation-sample/judge-record-fable.md
"""

from __future__ import annotations

import argparse
import collections
import itertools
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sample_common import (  # noqa: E402
    ROOT,
    SUPPORT_LABELS,
    Refusal,
    load_sample,
    refuse,
)
from validate_judge_record import (  # noqa: E402
    DEFAULT_READING,
    load_reading,
    validate,
)


def labels_by_witness(record: dict) -> dict[tuple[str, str], str]:
    return {
        (entry["cell"], entry["witness_key"]): entry["source_support"]
        for entry in record["judgements"]
    }


def recorded_by_witness(sample: dict) -> dict[tuple[str, str], str]:
    return {
        (entry["cell"], entry["witness_key"]): entry["recorded_source_support"]
        for entry in sample["witnesses"]
    }


def percent_agreement(pairs: list[tuple[str, str]]) -> tuple[int, int, float]:
    agree = sum(1 for left, right in pairs if left == right)
    total = len(pairs)
    return agree, total, agree / total if total else float("nan")


def cohen_kappa(pairs: list[tuple[str, str]]) -> tuple[float | None, float]:
    """Kappa over the four-label space, and the expected agreement it used.

    Returns None for kappa when expected agreement is 1: both sides used one and
    the same label everywhere and chance already explains the whole agreement.
    """

    total = len(pairs)
    if not total:
        return None, float("nan")
    left = collections.Counter(pair[0] for pair in pairs)
    right = collections.Counter(pair[1] for pair in pairs)
    expected = sum((left[label] / total) * (right[label] / total) for label in SUPPORT_LABELS)
    observed = percent_agreement(pairs)[2]
    if expected >= 1.0:
        return None, expected
    return (observed - expected) / (1 - expected), expected


def _kappa_text(pairs: list[tuple[str, str]]) -> str:
    kappa, expected = cohen_kappa(pairs)
    if kappa is None:
        return "kappa undefined (both sides used one label everywhere)"
    return f"kappa {kappa:.3f} (expected agreement {expected:.3f})"


def _block(
    title: str, cells: list[str], by_cell: dict[str, list[tuple[str, str]]]
) -> list[str]:
    lines = [f"  {title}"]
    everything: list[tuple[str, str]] = []
    for cell in cells:
        pairs = by_cell.get(cell, [])
        everything += pairs
        if not pairs:
            continue
        agree, total, fraction = percent_agreement(pairs)
        lines.append(f"    {cell}: {agree}/{total} = {fraction:.3f}, {_kappa_text(pairs)}")
    agree, total, fraction = percent_agreement(everything)
    lines.append(f"    overall: {agree}/{total} = {fraction:.3f}, {_kappa_text(everything)}")
    confusion = collections.Counter(everything)
    disagreements = {
        f"{left}->{right}": count
        for (left, right), count in sorted(confusion.items())
        if left != right
    }
    matches = {
        f"{left}->{right}": count
        for (left, right), count in sorted(confusion.items())
        if left == right
    }
    lines.append(f"    confusion, agreeing: {matches or '{}'}")
    lines.append(f"    confusion, differing: {disagreements or '{}'}")
    return lines


def composition(sample: dict) -> list[str]:
    """What was drawn and what the review recorded for it. No judge needed."""

    stratum = sample.get("stratum", {"label": None, "population": "EVERY_WITNESS"})
    recorded = recorded_by_witness(sample)
    lines = [
        f"sample seed {sample['seed']}, {len(sample['witnesses'])} witnesses over "
        f"{len(sample['cells'])} cells",
        f"stratification: {sample.get('stratification', 'UNSTATED')}",
        f"stratum: {stratum['population']}",
        "composition, and the labels the review recorded for what was drawn:",
    ]
    for entry in sample["cells"]:
        drawn = [
            witness
            for witness in sample["witnesses"]
            if witness["cell"] == entry["cell"]
        ]
        counts = collections.Counter(
            witness["recorded_source_support"] for witness in drawn
        )
        lines.append(
            f"  {entry['cell']}: {entry['sampled']} drawn of "
            f"{entry.get('witnesses_in_stratum', entry['witnesses_in_record'])} in the "
            f"stratum, {entry['witnesses_in_record']} in the record; recorded "
            f"{dict(sorted(counts.items()))}"
        )
    total = collections.Counter(recorded.values())
    drawn_total = sum(total.values())
    lines.append(f"  all cells: {drawn_total} drawn; recorded {dict(sorted(total.items()))}")
    for label in SUPPORT_LABELS:
        if total[label]:
            lines.append(
                f"    prevalence of {label}: {total[label]}/{drawn_total} = "
                f"{total[label] / drawn_total:.3f}"
            )
    return lines


def report(sample: dict, records: list[tuple[str, dict]]) -> list[str]:
    cells = [entry["cell"] for entry in sample["cells"]]
    recorded = recorded_by_witness(sample)
    lines = composition(sample) + [
        "",
        f"cells: {', '.join(cells)}",
        "labels from the review records are 'recorded', labels from a judge record are 'judge'",
    ]
    judged: list[tuple[str, dict[tuple[str, str], str]]] = []
    for name, record in records:
        labels = labels_by_witness(record)
        judged.append((name, labels))
        judge = record["judge"]
        lines.append("")
        lines.append(
            f"{name}: {judge['model_id']}, {judge['actor_id']}, "
            f"effort {judge['reasoning_effort']}"
        )
        by_cell: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
        for identity, label in recorded.items():
            by_cell[identity[0]].append((label, labels[identity]))
        lines += _block("recorded vs judge", cells, by_cell)
        lines.append(
            f"    label totals: recorded "
            f"{dict(collections.Counter(recorded.values()))} | judge "
            f"{dict(collections.Counter(labels.values()))}"
        )

    for (left_name, left), (right_name, right) in itertools.combinations(judged, 2):
        lines.append("")
        lines.append(f"{left_name} vs {right_name}")
        by_cell = collections.defaultdict(list)
        for identity in recorded:
            by_cell[identity[0]].append((left[identity], right[identity]))
        lines += _block("judge vs judge", cells, by_cell)
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument(
        "--judge-record",
        type=Path,
        action="append",
        default=None,
        help="omit to print the sample composition and prevalence only",
    )
    parser.add_argument("--reading", type=Path, default=ROOT / DEFAULT_READING)
    args = parser.parse_args(argv)
    try:
        sample = load_sample(args.sample)
        if not args.judge_record:
            print("\n".join(composition(sample)))
            print("no judge record given: agreement and kappa are not computed")
            return 0
        sample_source = args.sample.read_bytes()
        reading = load_reading(args.reading)
        records = []
        for path in args.judge_record:
            if not path.exists():
                refuse(f"judge record is missing: {path}")
            records.append((path.name, validate(path.read_bytes(), sample_source, reading)))
    except Refusal as refusal:
        print(f"REFUSED: {refusal}", file=sys.stderr)
        return 2
    print("\n".join(report(sample, records)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
