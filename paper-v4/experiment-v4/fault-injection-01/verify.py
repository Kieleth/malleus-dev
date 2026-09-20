"""Checks a reader can run on one run's own artifacts, after admission.

Two of these are the gate's own checks replayed from the outside, so that an
admission is not taken on trust: ``digest_disagreements`` recomputes every
located record's statement digest from the retained capture, and
``ledger_admission_events`` says whether a ledger carries a change set at all.
The third, ``locator_disagreements``, is the one the admission path does not
make: it asks whether the assertion a record cites is among the assertions the
plan derives that record from. A record can cite one sentence and be derived
from another and still be admitted; this is where that shows.

Nothing here is part of the admission path and nothing here is allowed to
repair anything. A disagreement is reported, with the record that carries it.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any


LOCATOR_SLOT = "assertion_locator"
DIGEST_SLOT = "statement_sha256"
ADMISSION_EVENTS = (
    "KNOWLEDGE_CHANGE_SET_RETAINED",
    "CHANGE_PROPOSED",
    "CHECK_RECORDED",
    "VERDICT_RECORDED",
)


def digest_bytes(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def file_digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def exported_by_id(export: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        record["id"]: record for family in sorted(export) for record in export[family]
    }


def properties(record: dict[str, Any]) -> dict[str, Any]:
    value = record.get("properties")
    return value if isinstance(value, dict) else {}


def locator_disagreements(
    export: dict[str, Any], trace: dict[str, Any]
) -> list[dict[str, str]]:
    """Records whose cited assertion is not one the plan derives them from."""

    derived: dict[str, set[str]] = {}
    for record in trace["records"]:
        derived[record["record_id"]] = {
            item["locator"] for item in record["derivations"]
        }
    found: list[dict[str, str]] = []
    for record_id, record in sorted(exported_by_id(export).items()):
        cited = properties(record).get(LOCATOR_SLOT)
        if not isinstance(cited, str) or not cited:
            continue
        locators = derived.get(record_id, set())
        if cited not in locators:
            found.append(
                {
                    "record_id": record_id,
                    "cited": cited,
                    "derived_from": ",".join(sorted(locators)),
                }
            )
    return found


def digest_disagreements(
    export: dict[str, Any], capture: dict[str, Any]
) -> list[dict[str, str]]:
    """Records whose statement digest is not that of the assertion they cite."""

    statements = {item["id"]: item["statement"] for item in capture["assertions"]}
    found: list[dict[str, str]] = []
    for record_id, record in sorted(exported_by_id(export).items()):
        cited = properties(record).get(LOCATOR_SLOT)
        declared = properties(record).get(DIGEST_SLOT)
        if not isinstance(cited, str) or not isinstance(declared, str):
            continue
        if cited not in statements:
            found.append(
                {"record_id": record_id, "cited": cited, "recomputed": "UNKNOWN"}
            )
            continue
        recomputed = digest_bytes(statements[cited].encode("utf-8"))
        if recomputed != declared:
            found.append(
                {
                    "record_id": record_id,
                    "cited": cited,
                    "recomputed": recomputed,
                }
            )
    return found


def ledger_event_types(path: Path) -> list[str]:
    return [
        json.loads(line)["event_type"]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def ledger_admission_events(path: Path) -> list[str]:
    return [item for item in ledger_event_types(path) if item in ADMISSION_EVENTS]


def contract_artifact(ledger: Path) -> dict[str, Any]:
    """The validated contract a run's first ledger event retained."""

    from base64 import b64decode

    first = json.loads(ledger.read_text(encoding="utf-8").splitlines()[0])
    if first["event_type"] != "ARTIFACT_REGISTERED":
        raise ValueError(f"{ledger}: the first event is not an artifact")
    return json.loads(b64decode(first["payload"]["retained_bytes_base64"]))


def json_differences(left: Any, right: Any, path: str = "") -> list[dict[str, str]]:
    """Every leaf at which two decoded artifacts disagree, by path."""

    if type(left) is not type(right):
        return [{"path": path or "/", "left": str(left), "right": str(right)}]
    if isinstance(left, dict):
        found: list[dict[str, str]] = []
        for key in sorted(set(left) | set(right)):
            found += json_differences(left.get(key), right.get(key), f"{path}/{key}")
        return found
    if isinstance(left, list):
        if len(left) != len(right):
            return [
                {
                    "path": f"{path}[length]",
                    "left": str(len(left)),
                    "right": str(len(right)),
                }
            ]
        found = []
        for index, (one, other) in enumerate(zip(left, right)):
            found += json_differences(one, other, f"{path}[{index}]")
        return found
    if left != right:
        return [{"path": path or "/", "left": str(left), "right": str(right)}]
    return []


# The two leaves a different Core may move without moving meaning: the digest
# of the five Core source files ``_contract_pipeline/elaborate.py`` hashes into
# ``evidence.producer``, and the digest of the evidence block carrying it.
PRODUCER_ONLY_PATHS = ("/evidence/producer/sha256", "/evidence_sha256")


def contract_differences(frozen: Path, observed: Path) -> list[dict[str, str]]:
    return json_differences(contract_artifact(frozen), contract_artifact(observed))


def is_producer_digest_only(differences: list[dict[str, str]]) -> bool:
    return [item["path"] for item in differences] == list(PRODUCER_ONLY_PATHS)


def is_byte_prefix(candidate: Path, whole: Path) -> bool:
    """Whether one ledger file's bytes open the other's, line for line."""

    left = candidate.read_bytes()
    right = whole.read_bytes()
    return len(left) <= len(right) and right[: len(left)] == left


def fault_witness(trial: dict[str, Any], export: dict[str, Any]) -> dict[str, Any]:
    """What the exported records show of one trial's injected fault.

    An admission is only real if the fault is in the graph that came back, so
    every admitted trial is asked this and the answer goes in the record.
    """

    by_id = exported_by_id(export)
    target = trial["target"]
    record_id = target["record_id"]
    record = by_id.get(record_id)
    if record is None:
        return {"present": False, "reason": "record absent from the export"}
    fault_class = trial["fault_class"]
    if fault_class == "VALUE_NOT_IN_BLOCK":
        found = properties(record).get(target["slot"])
        return {
            "present": found == target["injected_value"],
            "slot": target["slot"],
            "observed_equals_injected": found == target["injected_value"],
        }
    if fault_class.startswith("LOCATOR_REPOINTED"):
        found = properties(record).get(LOCATOR_SLOT)
        return {
            "present": found == target["to_locator"],
            "cited": found,
            "observed_equals_injected": found == target["to_locator"],
        }
    if fault_class.startswith("RECORD_WITH_NO_SOURCE"):
        return {
            "present": True,
            "type": record.get("type"),
            "properties_count": len(properties(record)),
        }
    if fault_class == "TYPE_OUTSIDE_ONTOLOGY":
        return {
            "present": record.get("type") == target["injected"],
            "type": record.get("type"),
        }
    if fault_class == "SLOT_OUTSIDE_ONTOLOGY":
        return {
            "present": target["injected"] in properties(record),
            "slots": sorted(properties(record)),
        }
    if fault_class == "DANGLING_ENDPOINT":
        return {
            "present": record.get("target_id") == target["injected"],
            "target_id": record.get("target_id"),
        }
    if fault_class == "DUPLICATE_RECORD_ID":
        return {"present": False, "reason": "an export cannot carry one ID twice"}
    raise ValueError(f"no witness rule for {fault_class}")
