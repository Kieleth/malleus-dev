"""Check a declared review subset without assigning or changing judgments."""

import json

from review_packet import digest
from selective_review import assembly_check, load_base, selective_witnesses


def validate_subset(folder, record, question_ids):
    source = (folder / "review-input-manifest.json").read_bytes()
    if digest(source) != record["review_input_manifest_sha256"]:
        raise ValueError("recheck manifest identity differs")
    manifest = json.loads(source)
    kind = manifest["evidence_surface"]["kind"]
    if kind != "SELECTED_READING_TEXT_LAYER":
        raise ValueError(f"unsupported recheck evidence surface: {kind}")
    materials = {}
    for item in manifest["materials"]:
        path = folder / item["path"]
        if path.parent.resolve() != folder.resolve():
            raise ValueError("recheck material escapes packet")
        data = path.read_bytes()
        if digest(data) != item["sha256"]:
            raise ValueError(f"recheck material drift: {item['name']}")
        if item["name"] in materials:
            raise ValueError("duplicate recheck material")
        materials[item["name"]] = data
    base = load_base(folder / "base-review.py")
    base.validate_review_input_manifest(source, materials["review_protocol"])
    returned = selective_witnesses(materials["query_result"], manifest)
    if not question_ids or len(question_ids) != len(set(question_ids)):
        raise ValueError("recheck question selection is empty or duplicated")
    if not set(question_ids) <= set(returned):
        raise ValueError("recheck selects an unknown question")
    selected = {q: returned[q] for q in question_ids}
    blocks = base._reading_blocks(
        materials["selected_reading"], manifest["fixed_identities"]
    )
    questions = {
        q["id"]: q for q in json.loads(materials["competency_questions"])["questions"]
    }
    judged = base._witnesses_v3(
        record,
        kind,
        {k for keys in selected.values() for k in keys},
        blocks,
        {},
        {},
        None,
    )
    base._questions_v3(
        record,
        {"question_ids": question_ids},
        [questions[q] for q in question_ids],
        selected,
        judged,
        kind,
        blocks,
        {},
        {},
        None,
    )
    assembly_check(record)
    return record
