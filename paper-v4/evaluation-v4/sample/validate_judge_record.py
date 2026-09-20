"""Validate an independent judge's record against the sample it was drawn from.

Each check refuses with its own named reason: the schema string, the record's
root and judge keys, the evaluator kind, the sample digest, that the judgements
cover exactly the sampled witnesses once each, that every label is one of the
protocol's four, that every rationale says something, and that no rationale
reproduces a 60-character run of the reading. That last one is the check
`paper-v4/experiment-v4/run-23/results/withheld-artifacts.json` describes:
unicode whitespace collapsed to a single space, then a shared normalized
character run against every reading block, at the frozen threshold of 60.

This file chooses nothing and aggregates nothing. It refuses or it returns.

    .venv/bin/python paper-v4/evaluation-v4/sample/validate_judge_record.py \
        --sample paper-v4/evaluation-v4/sample/sample-20260911.json \
        --record private/paper-v4-evaluation-sample/judge-record-fable.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sample_common import (  # noqa: E402
    JUDGE_RECORD_SCHEMA,
    ROOT,
    SAMPLE_SCHEMA,
    SHARED_RUN_CHARS,
    SUPPORT_LABELS,
    Refusal,
    digest,
    load_sample,
    markdown_record,
    reading_run_index,
    read_json,
    refuse,
    shared_run,
)


EVALUATOR_KIND = "INDEPENDENT_MODEL_JUDGE"
DEFAULT_READING = Path("private/paper-v4-text-layer/selected-reading.json")
_JUDGE_KEYS = {"evaluator_kind", "model_id", "actor_id", "reasoning_effort"}
_ROOT_KEYS = {"schema", "sample_sha256", "judge", "judgements"}
_JUDGEMENT_KEYS = {"cell", "witness_key", "source_support", "rationale"}


def _text(value: object, subject: str) -> str:
    if not isinstance(value, str) or not value.strip():
        refuse(f"{subject} must be a non-empty string")
    return value


def validate(record_source: bytes, sample_source: bytes, reading: dict) -> dict:
    record = markdown_record(record_source, "judge record")
    if record.get("schema") != JUDGE_RECORD_SCHEMA:
        refuse(f"judge record schema is not {JUDGE_RECORD_SCHEMA}: {record.get('schema')!r}")
    if set(record) != _ROOT_KEYS:
        refuse(f"judge record root keys must be exactly {sorted(_ROOT_KEYS)}: {sorted(record)}")

    sample = _sample_from_bytes(sample_source)
    if record.get("sample_sha256") != digest(sample_source):
        refuse(
            "judge record binds a different sample: it records "
            f"{record.get('sample_sha256')!r} and the sample file is {digest(sample_source)}"
        )

    judge = record["judge"]
    if not isinstance(judge, dict) or set(judge) != _JUDGE_KEYS:
        refuse(f"judge block keys must be exactly {sorted(_JUDGE_KEYS)}")
    if judge.get("evaluator_kind") != EVALUATOR_KIND:
        refuse(f"judge evaluator_kind must be {EVALUATOR_KIND}: {judge.get('evaluator_kind')!r}")
    for key in ("model_id", "actor_id", "reasoning_effort"):
        _text(judge.get(key), f"judge {key}")

    judgements = record["judgements"]
    if not isinstance(judgements, list):
        refuse("judgements must be an array")
    expected = {(entry["cell"], entry["witness_key"]) for entry in sample["witnesses"]}
    seen: set[tuple[str, str]] = set()
    index = reading_run_index(reading, SHARED_RUN_CHARS)
    for position, entry in enumerate(judgements):
        if not isinstance(entry, dict) or set(entry) != _JUDGEMENT_KEYS:
            refuse(
                f"judgement {position} keys must be exactly {sorted(_JUDGEMENT_KEYS)}"
            )
        cell = _text(entry.get("cell"), f"judgement {position} cell")
        key = _text(entry.get("witness_key"), f"judgement {position} witness_key")
        identity = (cell, key)
        if identity not in expected:
            refuse(f"judgement {position} judges {cell} {key}, which the sample did not draw")
        if identity in seen:
            refuse(f"judgement {position} judges {cell} {key} a second time")
        seen.add(identity)
        label = entry.get("source_support")
        if label not in SUPPORT_LABELS:
            refuse(
                f"judgement for {cell} {key} carries a label outside "
                f"{list(SUPPORT_LABELS)}: {label!r}"
            )
        rationale = entry.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            refuse(f"judgement for {cell} {key} carries no rationale")
        run = shared_run(rationale, index, SHARED_RUN_CHARS)
        if run is not None:
            refuse(
                f"judgement for {cell} {key} reproduces a {SHARED_RUN_CHARS}-character run "
                f"of the reading: {run!r}"
            )
    missing = expected - seen
    if missing:
        example = sorted(missing)[0]
        refuse(
            f"{len(missing)} sampled witnesses are unjudged, {example[0]} {example[1]} among them"
        )
    return record


def _sample_from_bytes(sample_source: bytes) -> dict:
    try:
        sample = json.loads(sample_source)
    except json.JSONDecodeError as error:
        raise Refusal(f"sample file is not JSON: {error}") from error
    if not isinstance(sample, dict) or sample.get("schema") != SAMPLE_SCHEMA:
        refuse(f"sample schema is not {SAMPLE_SCHEMA}")
    drawn = sample.get("witnesses")
    if not isinstance(drawn, list) or not drawn:
        refuse("sample file carries no witnesses")
    for position, entry in enumerate(drawn):
        if not isinstance(entry, dict) or not {"cell", "witness_key"} <= set(entry):
            refuse(f"sample witness {position} carries no cell and witness_key")
    return sample


def load_reading(path: Path) -> dict:
    reading = read_json(path, "selected reading")
    if not isinstance(reading, dict):
        refuse("selected reading must be an object")
    return reading


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--reading", type=Path, default=ROOT / DEFAULT_READING)
    args = parser.parse_args(argv)
    try:
        load_sample(args.sample)
        record = validate(
            args.record.read_bytes(),
            args.sample.read_bytes(),
            load_reading(args.reading),
        )
    except Refusal as refusal:
        print(f"REFUSED: {refusal}", file=sys.stderr)
        return 2
    judge = record["judge"]
    print(
        f"VALID: {len(record['judgements'])} judgements by {judge['model_id']} "
        f"({judge['actor_id']}, {judge['reasoning_effort']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
