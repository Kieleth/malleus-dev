"""Small, explicit extension of the frozen paper v3 review validator.

The isolated base module is unchanged on disk. Only its instrument identifiers,
assembly vocabulary and selective-result input reader are extended. Source
support, coverage, locators, witness closure and human authorship checks remain
the original functions. No judgment or query row is converted or supplied.
"""

import argparse
import importlib.util
import json
from pathlib import Path

from review_packet import PROTOCOL_IDENTITY, canonical, central_key, digest


BASE_IDENTITY = (
    "sha256:8f9dcb5d64f707eb3542119947393c9b350e1c155cc0ca567e55f2de9353e0ae"
)
PROTOCOL_SCHEMA = "malleus.paper-v4.source-grounded-review-protocol/selective-v1"
MANIFEST_SCHEMA = "malleus.paper-v4.source-grounded-review-inputs/selective-v1"
RECORD_SCHEMA = "malleus.paper-v4.source-grounded-review/selective-v1"
PROTOCOL_STATUS = "FROZEN_FOR_RETROSPECTIVE_REVIEW"


def protocol_bytes(source):
    if digest(source) != PROTOCOL_IDENTITY:
        raise ValueError("frozen base protocol differs")
    value = json.loads(source)
    value["schema"] = PROTOCOL_SCHEMA
    value["status"] = PROTOCOL_STATUS
    value["protocol_file"] = "review-protocol.json"
    value["protocol_file_version"] = "selective-v1"
    del value["supersedes"]
    value["extends"] = {
        "sha256": PROTOCOL_IDENTITY,
        "historical_records_unchanged": True,
    }
    value["frozen_before"] = "THIS_RETROSPECTIVE_REVIEW_NOT_THE_PRODUCER"
    value["judgments"]["assembly"].append("NO_ANSWER")
    value["judgments"]["assembly_note"] = (
        "NO_ANSWER iff no required semantic names an answering row. This includes "
        "empty output and unrelated candidates. Otherwise describe the assembly "
        "of the covered semantics with the existing three descriptors; missing "
        "semantics remain absent. Assembly never changes coverage or support."
    )
    value["validator"]["path"] = "selective_review.py"
    value["validator"]["entry_points"] = ["validate"]
    return canonical(value)


def replay_mode(result):
    if result["ledger_bytes_unchanged"] is not True:
        raise ValueError("selective replay/read-only check differs")
    if "historical_replay_matches" in result:
        if result["historical_replay_matches"] is not True:
            raise ValueError("selective replay/read-only check differs")
        return "RETROSPECTIVE_EXECUTED_PROGRAMS"
    if (
        result["schema"] != "malleus.paper-v4.followup-answers/v1"
        or result["execution_mode"] not in {"FRESH_FIXED_ONTOLOGY", "FRESH_END_TO_END"}
        or result["replay_matches_preclose"] is not True
        or type(result["admission_occurred"]) is not bool
    ):
        raise ValueError("fresh replay/read-only check differs")
    return result["execution_mode"]


def selective_witnesses(source, manifest):
    stage = manifest["stage_identities"]
    if digest(source) != stage["query_result_sha256"]:
        raise ValueError("selective result identity differs")
    result = json.loads(source)
    if result["status"] != "EXPLORATORY_UNREVIEWED":
        raise ValueError("not the declared exploratory result")
    for key in ("ledger_head", "replay_receipt_sha256"):
        if result["inputs"][key] != stage[key]:
            raise ValueError(f"selective result {key} differs")
    if result["forbidden_attempts"] != {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }:
        raise ValueError("selective result records forbidden access")
    replay_mode(result)
    if [q["question_id"] for q in result["queries"]] != manifest["question_ids"]:
        raise ValueError("selective question order differs")
    returned = {
        q["question_id"]: [central_key(row) for row in q["rows"]]
        for q in result["queries"]
    }
    if {k: len(v) for k, v in returned.items()} != manifest["rows_per_question"]:
        raise ValueError("selective row count differs")
    if (
        len({k for keys in returned.values() for k in keys})
        != manifest["witnesses_traced"]
    ):
        raise ValueError("selective witness count differs")
    return returned


def load_base(path):
    if digest(path.read_bytes()) != BASE_IDENTITY:
        raise ValueError("frozen base validator differs")
    spec = importlib.util.spec_from_file_location("isolated_paper_v3_review", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PROTOCOL_SCHEMA_V3 = PROTOCOL_SCHEMA
    module.PROTOCOL_STATUS_V3 = PROTOCOL_STATUS
    module.MANIFEST_SCHEMA_V3 = MANIFEST_SCHEMA
    module.REVIEW_SCHEMA_V3 = RECORD_SCHEMA
    module.ASSEMBLY_DESCRIPTORS = (*module.ASSEMBLY_DESCRIPTORS, "NO_ANSWER")
    module._query_witnesses = selective_witnesses
    return module


def assembly_check(record):
    for question in record["questions"]:
        none = not any(c["row_index"] is not None for c in question["coverage"])
        if (question["assembly"] == "NO_ANSWER") != none:
            raise ValueError("NO_ANSWER must describe exactly zero covered semantics")


def validate(folder, record_path):
    manifest_source = (folder / "review-input-manifest.json").read_bytes()
    manifest = json.loads(manifest_source)
    materials = {}
    for material in manifest["materials"]:
        path = folder / material["path"]
        if path.parent.resolve() != folder.resolve():
            raise ValueError("review material escapes frozen packet")
        source = path.read_bytes()
        if digest(source) != material["sha256"]:
            raise ValueError(f"review material drift: {material['name']}")
        if material["name"] in materials:
            raise ValueError("duplicate review material")
        materials[material["name"]] = source
    binding = json.loads(materials["query_binding"])
    result = json.loads(materials["query_result"])
    if binding["mode"] != replay_mode(result):
        raise ValueError("selective binding must state actual execution mode")
    if binding["mode"] in {"FRESH_FIXED_ONTOLOGY", "FRESH_END_TO_END"}:
        acceptance = json.loads(materials["acceptance_query_binding"])
        if (
            digest(materials["acceptance_query_binding"])
            != result["inputs"]["query_binding_sha256"]
        ):
            raise ValueError("acceptance-time binding differs")
        if acceptance["core_commit"] != result["core_commit"]:
            raise ValueError("acceptance-time Core differs")
        for key in (
            "query_program_sha256",
            "question_set_sha256",
            "population_surface_sha256",
        ):
            if acceptance[key] != result["inputs"][key]:
                raise ValueError(f"acceptance-time input differs: {key}")
    if binding["recorded_query_inputs"] != result["inputs"]:
        raise ValueError("selective input binding differs from executed inputs")
    if binding["query_result_sha256"] != digest(materials["query_result"]):
        raise ValueError("binding names a different selective result")
    if (
        digest(materials["query_binding"])
        != manifest["stage_identities"]["query_binding_sha256"]
    ):
        raise ValueError("selective binding identity differs")
    for material, key in (
        ("query_program", "query_program_sha256"),
        ("query_runner", "runner_sha256"),
        ("program_binding_helper", "binding_program_sha256"),
        ("population_surface", "population_surface_sha256"),
        ("competency_questions", "question_set_sha256"),
    ):
        if digest(materials[material]) != result["inputs"][key]:
            raise ValueError(f"executed program/input bytes differ: {material}")
    if "base_query_program_sha256" in result["inputs"]:
        if (
            digest(materials["base_query_program"])
            != result["inputs"]["base_query_program_sha256"]
        ):
            raise ValueError("executed base query bytes differ")
    base = load_base(folder / "base-review.py")
    record = base.validate_review(
        record_path.read_bytes(),
        materials["review_protocol"],
        review_input_manifest_source=manifest_source,
        query_result_source=materials["query_result"],
        selected_reading_source=materials["selected_reading"],
        competency_questions_source=materials["competency_questions"],
    )
    assembly_check(record)
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    args = parser.parse_args()
    record = validate(args.packet, args.record)
    print(
        json.dumps(
            {
                "status": record["status"],
                "questions": len(record["questions"]),
                "witnesses": len(record["witnesses"]),
                "human_ratification": record["ratification"]["disposition"],
            }
        )
    )
