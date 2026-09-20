"""Bind each frozen cell to the exact invocation that produced it.

Nothing here runs a process or decides an outcome. Every argument the runner
needs is read back out of that cell's own frozen artifacts: the source closure
and the reading from ``run-result.json`` by digest, the population by the
capture digest it canonicalizes to, the capture and plan identifiers from the
same file, and the source and artifact identifiers from the cell's own ledger.
No per-cell table is written down here, so a cell that staged a different file
is resolved by what it recorded rather than by what run-23 happened to do.

``producer_digest`` recomputes the digest Core puts in the validated contract's
``evidence.producer``: the canonical digest of five Core source files, the loop
in ``_contract_pipeline/elaborate.py``. It is recomputed from a Core export so
that a claim about which Core produced a run is checked against the bytes, not
taken from the artifact that is under question. Reading that artifact back out
of a ledger, and diffing two of them, is ``fault-injection-01/verify.py``'s
job and is not repeated here.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIVATE = ROOT / "private"

CELLS = tuple(f"run-{number}" for number in range(20, 27))
ROOT_LOCATOR = "paper-v4-project"
POPULATION_FIELDS = {"capture", "records", "supersessions"}

# The five files ``_contract_pipeline/elaborate.py`` hashes into
# ``evidence.producer``. ``test_bridge.py`` checks the recomputation against
# the digest each run's own ledger carries, so a move in that loop shows up as
# a failure here rather than as a silent disagreement.
PRODUCER_INPUTS = (
    "_contract_compiler.py",
    "_contract_pipeline/__init__.py",
    "_contract_pipeline/elaborate.py",
    "_contract_pipeline/model.py",
    "_contract_pipeline/view.py",
)


class BridgeRefusal(ValueError):
    """A cell's frozen artifacts do not determine its invocation."""


def canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def digest_bytes(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def file_digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def private_root(cell: str) -> Path:
    return PRIVATE / f"paper-v4-v4-{cell}"


def producer_root(cell: str) -> Path:
    return private_root(cell) / "producer"


def frozen_result(cell: str) -> dict[str, Any]:
    return json.loads((private_root(cell) / "results/run-result.json").read_bytes())


def frozen_ledger(cell: str) -> Path:
    return private_root(cell) / "ledger/history.jsonl"


def frozen_results_dir(cell: str) -> Path:
    return private_root(cell) / "results"


def _sole_match(cell: str, wanted: str, label: str) -> Path:
    root = producer_root(cell)
    matches = [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and file_digest(path) == wanted
    ]
    if not matches:
        raise BridgeRefusal(f"{cell}: no producer file digests to {label} {wanted}")
    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(root)) for path in matches)
        raise BridgeRefusal(f"{cell}: {label} {wanted} is ambiguous between {names}")
    return matches[0]


def source_closure(cell: str) -> list[tuple[str, Path]]:
    """The cell's own closure, each locator bound to the file it recorded."""

    frozen = frozen_result(cell)
    closure = frozen["source_closure_sha256"]
    if ROOT_LOCATOR not in closure:
        raise BridgeRefusal(f"{cell}: closure has no {ROOT_LOCATOR} entry")
    if closure[ROOT_LOCATOR] != frozen["ontology_sha256"]:
        raise BridgeRefusal(f"{cell}: the root locator is not the accepted ontology")
    return [
        (locator, _sole_match(cell, wanted, f"source {locator}"))
        for locator, wanted in sorted(closure.items())
    ]


def reading_path(cell: str) -> Path:
    return _sole_match(cell, frozen_result(cell)["reading_sha256"], "reading")


def population_path(cell: str) -> Path:
    """The producer population whose capture is the one the run retained."""

    wanted = frozen_result(cell)["capture"]["capture_sha256"]
    root = producer_root(cell)
    matches = []
    for path in sorted(root.rglob("*.json")):
        try:
            value = json.loads(path.read_bytes())
        except (ValueError, UnicodeDecodeError):
            continue
        if not isinstance(value, dict) or set(value) != POPULATION_FIELDS:
            continue
        if digest_bytes(canonical(value["capture"])) == wanted:
            matches.append(path)
    if len(matches) != 1:
        raise BridgeRefusal(
            f"{cell}: {len(matches)} producer populations carry capture {wanted}"
        )
    return matches[0]


def ledger_events(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def identifiers(cell: str) -> dict[str, str]:
    """Capture, plan, source and artifact identifiers, from the cell's own record."""

    frozen = frozen_result(cell)
    events = ledger_events(frozen_ledger(cell))
    sources = [
        event["payload"]["machine_payload"]["source_id"]
        for event in events
        if event["event_type"] == "SOURCE_REGISTERED"
    ]
    artifacts = [
        event["payload"]["record_id"]
        for event in events
        if event["event_type"] == "ARTIFACT_REGISTERED"
        and event["payload"].get("machine_payload", {}).get("artifact_identity")
        == frozen["reading_sha256"]
    ]
    if len(sources) != 1:
        raise BridgeRefusal(f"{cell}: {len(sources)} sources registered, expected one")
    if len(artifacts) != 1:
        raise BridgeRefusal(
            f"{cell}: {len(artifacts)} artifacts carry the reading, expected one"
        )
    return {
        "capture_id": frozen["capture"]["capture_id"],
        "plan_id": frozen["plan"]["plan_id"],
        "source_id": sources[0],
        "artifact_id": artifacts[0],
        "transaction_time": frozen["transaction_time"],
        "actor_id": frozen["actor_id"],
    }


def producer_digest(core_src: Path) -> str:
    """Recompute ``evidence.producer.sha256`` from an exported Core tree."""

    inputs = []
    for relative in PRODUCER_INPUTS:
        source = (core_src / "malleus" / relative).read_bytes()
        inputs.append({"path": relative, "sha256": digest_bytes(source)})
    return digest_bytes(canonical(inputs))


def declared_producer_digest(artifact: dict[str, Any]) -> str:
    """The producer digest a validated contract artifact declares."""

    return str(artifact["evidence"]["producer"]["sha256"])
