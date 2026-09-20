"""Offline checks. Synthetic text tests the boundary, not BEAM answers."""

import copy
import hashlib
import json

import pytest

from beam_prepare import InputRefusal, check_questions, project_chat, unpack_source


def encode(value):
    return json.dumps(value, ensure_ascii=False).encode()


def sample():
    return [
        {
            "batch_number": 1,
            "time_anchor": "ANNOTATION_ONLY_DATE",
            "turns": [
                [
                    {
                        "id": 9,
                        "role": "user",
                        "content": "Want café alerts.\n  Keep spacing ->-> 1,1",
                        "index": "ANNOTATION_ONLY_INDEX",
                        "question_type": "ANNOTATION_ONLY_QUESTION",
                        "time_anchor": "ANNOTATION_ONLY_TIME",
                    },
                    {"id": 3, "role": "assistant", "content": "I suggest a test."},
                ]
            ],
        },
        {
            "batch_number": 2,
            "turns": [[{"id": 15, "role": "user", "content": "Not yet done."}]],
        },
    ]


def test_lossless_text_roles_order_and_json_pointers():
    source = sample()
    reading, locators = project_chat(encode(source))
    blocks = [block for page in reading["pages"] for block in page["blocks"]]
    assert [item["message_id"] for item in locators] == [9, 3, 15]
    assert [len(page["blocks"]) for page in reading["pages"]] == [2, 1]
    assert [block["ordinal"] for block in blocks] == [0, 1, 2]
    assert len({block["id"] for block in blocks}) == 3
    for block, item in zip(blocks, locators, strict=True):
        value = source
        for segment in item["json_pointer"].split("/")[1:]:
            value = value[int(segment)] if isinstance(value, list) else value[segment]
        assert block["id"] == item["block_id"]
        assert block["text"] == item["prefix"] + value
        assert item["prefix"] == f"[speaker={item['role']}]\n"
    assert source == sample()


def test_metadata_never_enters_reading_or_locator_map():
    reading, locators = project_chat(encode(sample()))
    assert "ANNOTATION_ONLY" not in json.dumps([reading, locators])
    assert "->-> 1,1" in json.dumps(reading)


def test_projection_is_deterministic():
    assert project_chat(encode(sample())) == project_chat(encode(sample()))


@pytest.mark.parametrize("field", ["id", "role", "content"])
def test_missing_message_field_refuses(field):
    data = sample()
    del data[0]["turns"][0][0][field]
    with pytest.raises(InputRefusal, match="MESSAGE_SHAPE"):
        project_chat(encode(data))


@pytest.mark.parametrize(
    "field,value",
    [
        ("id", True),
        ("id", -1),
        ("id", "9"),
        ("role", "system"),
        ("content", None),
        ("content", "  "),
    ],
)
def test_invalid_required_message_value_refuses(field, value):
    data = sample()
    data[0]["turns"][0][0][field] = value
    with pytest.raises(InputRefusal):
        project_chat(encode(data))


def test_duplicate_id_refuses_across_batches():
    data = sample()
    data[1]["turns"][0][0]["id"] = 9
    with pytest.raises(InputRefusal, match="DUPLICATE_MESSAGE_ID"):
        project_chat(encode(data))


@pytest.mark.parametrize(
    "data",
    [
        None,
        {},
        [],
        [{"batch_number": 1, "turns": []}],
        [{"batch_number": 1, "turns": [[]]}],
    ],
)
def test_bad_or_empty_layout_refuses(data):
    with pytest.raises(InputRefusal):
        project_chat(encode(data))


def test_unrecognised_source_fields_refuse_instead_of_silent_loss():
    data = sample()
    data[0]["turns"][0][0]["new_evidence_field"] = "unknown"
    with pytest.raises(InputRefusal, match="MESSAGE_SHAPE"):
        project_chat(encode(data))


def test_duplicate_json_key_refuses():
    with pytest.raises(InputRefusal, match="DUPLICATE_JSON_KEY"):
        project_chat(b'[{"turns":[],"turns":[]}]')


def archive_and_pin():
    content = '[\n  {"unicode": "café"}\n]'
    raw = content.encode()
    pin = {
        "repository": "owner/repo",
        "ref": "a" * 40,
        "path": "chat.json",
        "git_blob": hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest(),
        "byte_length": len(raw),
        "sha256": "sha256:" + hashlib.sha256(raw).hexdigest(),
    }
    return {**pin, "content": content}, pin


def test_exact_upstream_bytes_survive_archive_without_final_newline():
    archive, pin = archive_and_pin()
    assert unpack_source(encode(archive), pin) == archive["content"].encode()


@pytest.mark.parametrize(
    "field,value",
    [
        ("content", "[]\n"),
        ("git_blob", "b" * 40),
        ("path", "questions.json"),
        ("byte_length", 1),
        ("sha256", "sha256:" + "f" * 64),
    ],
)
def test_corrupt_or_substituted_archive_refuses(field, value):
    archive, pin = archive_and_pin()
    archive[field] = value
    with pytest.raises(InputRefusal):
        unpack_source(encode(archive), pin)


def questions():
    return {
        "update": [
            {
                "question": "What changed?",
                "rubric": [{"criterion": "test"}],
                "source_chat_ids": {"earlier": [9], "later": [15]},
            }
        ],
        "abstention": [
            {"question": "What is unknown?", "rubric": [{"criterion": "test"}]}
        ],
    }


def test_question_check_resolves_nested_references_without_scoring():
    before = copy.deepcopy(questions())
    result = check_questions(encode(before), {9, 3, 15})
    assert result == {
        "questions": 2,
        "categories": {"update": 1, "abstention": 1},
        "source_references": 2,
        "semantic_review": "NOT_PERFORMED",
    }
    assert before == questions()


def test_unresolvable_question_reference_refuses():
    with pytest.raises(InputRefusal, match="UNKNOWN_MESSAGE_REFERENCE"):
        check_questions(encode(questions()), {9})


@pytest.mark.parametrize(
    "field,value",
    [
        ("question", ""),
        ("rubric", []),
        ("source_chat_ids", [True]),
        ("source_chat_ids", "9"),
    ],
)
def test_malformed_evaluation_fields_refuse(field, value):
    data = questions()
    data["update"][0][field] = value
    with pytest.raises(InputRefusal):
        check_questions(encode(data), {9, 15})
