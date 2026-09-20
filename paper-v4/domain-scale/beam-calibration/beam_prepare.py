"""Lossless, offline BEAM reading preparation. No extraction or model calls."""

import argparse
import hashlib
import json
from pathlib import Path


class InputRefusal(ValueError):
    """A declared input cannot satisfy the preparation contract."""


def _require(condition, reason):
    if not condition:
        raise InputRefusal(reason)


def _object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"DUPLICATE_JSON_KEY: {key}")
        result[key] = value
    return result


def _invalid_constant(value):
    raise InputRefusal(f"NON_JSON_NUMBER: {value}")


def decode(raw):
    try:
        return json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_object,
            parse_constant=_invalid_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InputRefusal(f"INVALID_JSON: {exc}") from exc


def canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(raw):
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def unpack_source(archive_bytes, pin):
    """Recover exact fetched UTF-8 bytes, including their newline convention."""
    fields = {"repository", "ref", "path", "git_blob", "byte_length", "sha256"}
    archive = decode(archive_bytes)
    _require(isinstance(pin, dict) and set(pin) == fields, "PIN_SHAPE")
    _require(
        isinstance(archive, dict) and set(archive) == fields | {"content"},
        "ARCHIVE_SHAPE",
    )
    _require(all(archive[key] == pin[key] for key in fields), "ARCHIVE_PIN_MISMATCH")
    _require(isinstance(archive["content"], str), "ARCHIVE_CONTENT_NOT_TEXT")
    raw = archive["content"].encode("utf-8")
    _require(len(raw) == pin["byte_length"], "SOURCE_LENGTH_MISMATCH")
    _require(digest(raw) == pin["sha256"], "SOURCE_DIGEST_MISMATCH")
    blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    _require(blob == pin["git_blob"], "SOURCE_GIT_BLOB_MISMATCH")
    return raw


def project_chat(raw):
    """Select roles/content only; retain all utterances and supplied order."""
    data = decode(raw)
    _require(isinstance(data, list) and bool(data), "BATCHES_REQUIRED")
    pages, locators = [], []
    seen_ids, seen_batches = set(), set()
    required = {"id", "role", "content"}
    allowed = required | {"time_anchor", "index", "question_type"}
    for bi, batch in enumerate(data):
        _require(
            isinstance(batch, dict)
            and {"batch_number", "turns"} <= set(batch)
            and set(batch) <= {"batch_number", "turns", "time_anchor"},
            "BATCH_SHAPE",
        )
        number = batch["batch_number"]
        _require(
            type(number) is int and number > 0 and number not in seen_batches,
            "BATCH_NUMBER_INVALID_OR_DUPLICATE",
        )
        seen_batches.add(number)
        _require(
            isinstance(batch["turns"], list) and bool(batch["turns"]), "TURNS_REQUIRED"
        )
        blocks = []
        for ti, turn in enumerate(batch["turns"]):
            _require(isinstance(turn, list) and bool(turn), "MESSAGES_REQUIRED")
            for mi, message in enumerate(turn):
                where = f"/{bi}/turns/{ti}/{mi}"
                _require(
                    isinstance(message, dict)
                    and required <= set(message)
                    and set(message) <= allowed,
                    f"MESSAGE_SHAPE: {where}",
                )
                mid, role, content = (message[k] for k in ("id", "role", "content"))
                _require(type(mid) is int and mid >= 0, f"MESSAGE_ID_INVALID: {where}")
                _require(mid not in seen_ids, f"DUPLICATE_MESSAGE_ID: {mid}")
                _require(role in ("user", "assistant"), f"ROLE_INVALID: {where}")
                _require(
                    isinstance(content, str) and bool(content.strip()),
                    f"CONTENT_REQUIRED: {where}",
                )
                seen_ids.add(mid)
                block_id, prefix = f"beam:100K:2:message:{mid}", f"[speaker={role}]\n"
                blocks.append(
                    {"id": block_id, "ordinal": len(locators), "text": prefix + content}
                )
                locators.append(
                    {
                        "block_id": block_id,
                        "message_id": mid,
                        "role": role,
                        "json_pointer": where + "/content",
                        "prefix": prefix,
                        "batch_number": number,
                    }
                )
        pages.append({"page": bi + 1, "blocks": blocks})
    return {"pages": pages}, locators


def _references(value):
    if type(value) is int and value >= 0:
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in _references(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in _references(child)]
    raise InputRefusal("MESSAGE_REFERENCE_SHAPE")


def check_questions(raw, message_ids):
    """Check reference closure only. Never turn an answer key into source truth."""
    data = decode(raw)
    _require(isinstance(data, dict) and bool(data), "QUESTION_CATEGORIES_REQUIRED")
    categories, refs = {}, []
    for category, questions in data.items():
        _require(isinstance(questions, list) and bool(questions), "QUESTIONS_REQUIRED")
        categories[category] = len(questions)
        for question in questions:
            _require(
                isinstance(question, dict) and {"question", "rubric"} <= set(question),
                "QUESTION_SHAPE",
            )
            _require(
                isinstance(question["question"], str)
                and bool(question["question"].strip()),
                "QUESTION_TEXT_REQUIRED",
            )
            _require(
                isinstance(question["rubric"], (dict, list))
                and bool(question["rubric"]),
                "RUBRIC_REQUIRED",
            )
            if "source_chat_ids" in question:
                refs.extend(_references(question["source_chat_ids"]))
    unknown = set(refs) - message_ids
    _require(not unknown, f"UNKNOWN_MESSAGE_REFERENCE: {sorted(unknown)}")
    return {
        "questions": sum(categories.values()),
        "categories": categories,
        "source_references": len(refs),
        "semantic_review": "NOT_PERFORMED",
    }


def prepare(archive_bytes, pin):
    raw = unpack_source(archive_bytes, pin)
    reading, locators = project_chat(raw)
    artifacts = {
        "reading.json": canonical(reading),
        "source-map.json": canonical(locators),
    }
    report = {
        "status": "READING_PREPARED_NOT_CAPTURED",
        "source": pin,
        "projection": "beam-weather-reading/v1",
        "messages": len(locators),
        "batch_messages": [len(page["blocks"]) for page in reading["pages"]],
        "roles": {
            role: sum(item["role"] == role for item in locators)
            for role in ("user", "assistant")
        },
        "generation_marker_occurrences": sum(
            block["text"].count("->->")
            for page in reading["pages"]
            for block in page["blocks"]
        ),
        "artifacts": {
            name: {"sha256": digest(value), "bytes": len(value)}
            for name, value in artifacts.items()
        },
        "token_count": {
            "status": "UNMEASURED",
            "reason": "Named tokenizer not yet selected",
        },
        "model_launched": False,
        "producer_isolation_verified": False,
    }
    return {**artifacts, "input-manifest.json": canonical(report)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--pins", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    outputs = prepare(
        args.archive.read_bytes(), decode(args.pins.read_bytes())["conversation"]
    )
    # All input checks precede writes. A new directory prevents overwriting an earlier packet.
    args.output.mkdir(parents=True, exist_ok=False)
    for name, raw in outputs.items():
        (args.output / name).write_bytes(raw)
    print(outputs["input-manifest.json"].decode())


if __name__ == "__main__":
    main()
