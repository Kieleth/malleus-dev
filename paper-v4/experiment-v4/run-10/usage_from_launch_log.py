"""Derive the public cost record from the run-10 launch log.

Six cells declared ``producer-launch-log/v1`` over four incompatible shapes, and
only two of them published a cost artifact at all, so no cross-cell reader could
be written against the version string and four of six cost figures lived in
private files (deep sweep D-09 and D-19). Run-10 declares one shape for the
whole cell, ``malleus.paper-v4.producer-launch-log/v2``, publishes it as-is at
freeze, and derives ``results/usage.json`` from it here rather than by hand.

The harness reports cumulative session tokens at each resume. A stage figure is
the difference between one cumulative reading and the one before it, which is
the arithmetic this script owns so that no stage number is typed twice.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


LOG_SCHEMA = "malleus.paper-v4.producer-launch-log/v2"
USAGE_SCHEMA = "malleus.paper-v4.producer-usage/v1"
LOG_KEYS = ("schema", "run", "protocol", "launches", "gate", "runner", "query", "review")
LAUNCH_KEYS = (
    "first_stage",
    "harness",
    "model_family",
    "model_id",
    "ordinal",
    "phase",
    "requested_model",
    "role",
    "usage_by_resume",
    "usage_cumulative",
)
USAGE_KEYS = ("duration_ms", "tokens", "tool_uses")
PRODUCER = "PRODUCER"
NOTE = (
    "Harness-reported subagent tokens per stage, taken from the Claude Code"
    " Agent tool's usage report at each producer resume (cumulative per session;"
    " stage figures are differences). The count is the harness's own total for"
    " the session and is not split into input, output or cache tokens."
    " tool_uses and duration_ms are cumulative in the same way. Reasoning"
    " effort was the harness default. Derived from the launch log by"
    " usage_from_launch_log.py; no stage figure is entered by hand."
)


class UsageRefusal(ValueError):
    """The launch log does not carry the shape the public cost record needs."""


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _usage(value: object, subject: str, *, extra: tuple[str, ...] = ()) -> dict[str, int]:
    if not isinstance(value, dict) or set(value) != set(USAGE_KEYS) | set(extra):
        raise UsageRefusal(
            f"{subject} must carry exactly {', '.join(sorted(set(USAGE_KEYS) | set(extra)))};"
            f" found {sorted(value) if isinstance(value, dict) else value}"
        )
    for key in USAGE_KEYS:
        if not isinstance(value[key], int) or isinstance(value[key], bool):
            raise UsageRefusal(f"{subject}.{key} must be an integer")
    return {key: int(value[key]) for key in USAGE_KEYS}


def validate_launch_log(log: dict[str, object]) -> dict[str, object]:
    """Refuse a launch log that is not the one shape this cell declares."""

    if log.get("schema") != LOG_SCHEMA:
        raise UsageRefusal(f"launch log must declare {LOG_SCHEMA}")
    absent = [key for key in LOG_KEYS if key not in log]
    if absent:
        raise UsageRefusal(f"launch log is missing: {', '.join(absent)}")
    extra = sorted(set(log) - set(LOG_KEYS))
    if extra:
        raise UsageRefusal(f"launch log carries undeclared keys: {', '.join(extra)}")
    if not isinstance(log["launches"], list) or not log["launches"]:
        raise UsageRefusal("launch log carries no launch")
    for launch in log["launches"]:
        missing = [key for key in LAUNCH_KEYS if key not in launch]
        if missing:
            raise UsageRefusal(
                f"launch {launch.get('ordinal')} is missing: {', '.join(missing)}"
            )
    if not isinstance(log["runner"], list):
        raise UsageRefusal("launch log runner must be a list")
    for attempt in log["runner"]:
        if "execution_commit" not in attempt:
            raise UsageRefusal(
                f"runner attempt {attempt.get('attempt')} names no execution_commit"
            )
    return log


def _stages(launch: dict[str, object]) -> tuple[list[dict[str, object]], dict[str, int]]:
    cumulative = _usage(launch["usage_cumulative"], f"launch {launch['ordinal']}")
    stages = [{"stage": str(launch["first_stage"]), **cumulative}]
    previous = cumulative
    for resume in launch["usage_by_resume"]:
        if "after" not in resume:
            raise UsageRefusal(
                f"launch {launch['ordinal']} has a resume with no 'after' stage"
            )
        reading = _usage(
            resume,
            f"launch {launch['ordinal']} resume {resume['after']}",
            extra=("after",),
        )
        difference = {key: reading[key] - previous[key] for key in USAGE_KEYS}
        negative = sorted(key for key, value in difference.items() if value < 0)
        if negative:
            raise UsageRefusal(
                f"cumulative usage decreases at {resume['after']}:"
                f" {', '.join(negative)}"
            )
        stages.append({"stage": str(resume["after"]), **difference})
        previous = reading
    return stages, previous


def _population(runner: list[dict[str, object]]) -> str:
    attempts = [item for item in runner if item.get("attempt") != "shadow"]
    if not attempts:
        return "NOT_STARTED"
    last = attempts[-1]
    sentence = (
        f"{last.get('status')} at runner attempt {last.get('attempt')},"
        f" {last.get('structural_diagnostic_returns_used')} structural returns"
        f" at {last.get('execution_commit')}"
    )
    refused = [item for item in attempts[:-1] if item.get("status") != last.get("status")]
    if refused:
        earlier = "; ".join(
            f"attempt {item.get('attempt')} {item.get('status')}"
            f" ({item.get('classification')})"
            for item in refused
        )
        sentence = f"{sentence}; {earlier}"
    return sentence


def derive(log: dict[str, object]) -> dict[str, object]:
    validate_launch_log(log)
    producers = [item for item in log["launches"] if item["role"] == PRODUCER]
    if not producers:
        raise UsageRefusal(f"launch log carries no {PRODUCER} launch")
    models = {(item["model_id"], item["model_family"]) for item in producers}
    if len(models) != 1:
        raise UsageRefusal("the producer launches do not agree on one model")
    model_id, model_family = models.pop()

    stages: list[dict[str, object]] = []
    total = 0
    for launch in sorted(producers, key=lambda item: item["ordinal"]):
        launch_stages, final = _stages(launch)
        stages.extend(launch_stages)
        total += final["tokens"]

    review = log["review"]
    if review is not None and not isinstance(review, dict):
        raise UsageRefusal("the review block must be an object or null")
    return {
        "schema": USAGE_SCHEMA,
        "run": log["run"],
        "note": NOTE,
        "model_id": model_id,
        "model_family": model_family,
        "stages": stages,
        "producer_total_tokens": total,
        "population": _population(log["runner"]),
        "review": review,
    }


def execute(arguments: argparse.Namespace) -> dict[str, object]:
    output = Path(arguments.output)
    if output.exists():
        raise UsageRefusal(f"usage record already exists: {output}")
    usage = derive(json.loads(Path(arguments.launch_log).read_bytes()))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(_canonical(usage) + b"\n")
    return usage


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--launch-log", required=True, help="the cell's launch log")
    parser.add_argument("--output", required=True, help="results/usage.json to write")
    arguments = parser.parse_args(argv)
    try:
        execute(arguments)
    except (OSError, TypeError, ValueError) as error:
        print(f"usage-from-launch-log: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
