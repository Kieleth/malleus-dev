"""Deliver runner-owned coordinates and bound one administrative correction."""

from copy import deepcopy
import json

from review_packet import canonical, digest, new_private_directory


def coordinates(run):
    initial = json.loads((run / "producer-input-manifest.json").read_bytes())
    accepted = json.loads((run / "manifest.json").read_bytes())
    ids = accepted["interface_coordinates"]
    if ids != initial["interface_coordinates"] or set(ids) != {
        "source_id",
        "capture_id",
        "plan_id",
    }:
        raise ValueError("runner coordinates differ from declared configuration")
    if any(type(value) is not str or not value.strip() for value in ids.values()):
        raise ValueError("all runner coordinates are required")
    return ids


def check_message(text, ids):
    for key in ("source_id", "capture_id", "plan_id"):
        if key not in text or ids[key] not in text:
            raise ValueError("handoff omits required coordinate: " + key)


def message(run):
    ids = coordinates(run)
    text = f"""Administrative structural return 1 of at most 2. Continue in the same session.
The parent omitted the runner's interface coordinates in the phase-two handoff.
Core refused the first submission with this exact diagnostic:
{(run / "attempt-01/run-result.json").read_text().strip()}

The runner-owned coordinates already frozen before population are:
{json.dumps(ids, indent=2, sort_keys=True)}

Set capture.attribution.source_id to the supplied source_id. This identifies
the source retained by the runner, not an entity in your graph. Preserve every
other JSON value, including all assertions, records, record IDs, graph relation
endpoints, supersessions, and the accepted ontology. Do not rename the article
entity or change its graph references. No semantic feedback is supplied.
The exact original submission is retained in attempt-01; do not access that
directory. Update only your own work/document-population.json, session-log.md
and status.json. Return POPULATION_READY with the corrected file's digest.
All other frozen task boundaries and the single-producer condition remain.
"""
    check_message(text, ids)
    return text


def check_identity_only_return(original, corrected, source_id):
    expected = deepcopy(original)
    expected["capture"]["attribution"]["source_id"] = source_id
    if corrected != expected:
        raise ValueError("administrative return changed more than the source identity")


def execute_return(run, transaction_time):
    from e2e_execute import execute

    original = json.loads((run / "attempt-01/submitted-population.json").read_bytes())
    path = run / "producer/work/document-population.json"
    check_identity_only_return(
        original, json.loads(path.read_bytes()), coordinates(run)["source_id"]
    )
    return execute(run, path, run / "attempt-02", transaction_time)


def prepare_return(run):
    target = new_private_directory(run / "population-return-01", run)
    result = json.loads((run / "attempt-01/run-result.json").read_bytes())
    if (
        result["status"] != "REFUSED"
        or len(result["cause_chain"]) != 1
        or result["cause_chain"][0]["reason"] != "UNRETAINED_SOURCE"
    ):
        raise ValueError("this return requires the exact source-retention refusal")
    body = message(run)
    files = {
        "message.md": body.encode(),
        "refusal.json": (run / "attempt-01/run-result.json").read_bytes(),
    }
    receipt = {
        "kind": "COORDINATOR_CONFIGURATION_CORRECTION",
        "structural_return": 1,
        "interface_coordinates": coordinates(run),
        "original_population_sha256": digest(
            (run / "attempt-01/submitted-population.json").read_bytes()
        ),
        "materials": [
            {"path": name, "sha256": digest(data)} for name, data in files.items()
        ],
    }
    target.mkdir()
    for name, data in files.items():
        (target / name).write_bytes(data)
    (target / "receipt.json").write_bytes(canonical(receipt))
    return body
