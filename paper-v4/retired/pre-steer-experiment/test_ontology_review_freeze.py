from __future__ import annotations

from hashlib import sha256
from importlib.metadata import version
from importlib.resources import files
import json
import platform
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "paper-v4" / "experiment"
PRIVATE_EVAL = ROOT / "private" / "paper-v4-evaluation"
PRIVATE_READING = (
    ROOT / "private" / "paper-v4-ocr" / "yu-2025-tesseract-v1" / "selected-reading.json"
)


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_bytes())


def test_review_contract_and_schema_are_frozen_and_well_formed() -> None:
    assert _digest(EXPERIMENT / "ontology-review-task.md") == (
        "sha256:314d79841aa9d937eff732173d81dc5b24cb122de5f369c2a92c4d58a57e97a5"
    )
    schema = _load(EXPERIMENT / "ontology-review-output-schema.json")
    Draft202012Validator.check_schema(schema)
    assert _digest(EXPERIMENT / "ontology-review-output-schema.json") == (
        "sha256:f434dc7590ab3cb3dbb309d09cd4660546837a58a6735df2ece4724818080dfe"
    )


def test_bound_support_blocks_are_an_exact_closed_subset_of_the_reading() -> None:
    reading = _load(PRIVATE_READING)
    bound = _load(PRIVATE_EVAL / "bound-support-blocks.json")
    source = {
        block["id"]: block for page in reading["pages"] for block in page["blocks"]
    }

    assert _digest(PRIVATE_EVAL / "bound-support-blocks.json") == (
        "sha256:36cb8c6a51f18aecc7acdf9ab257029e96578addcb36e891047ebb02cfcc22ac"
    )
    assert len(bound["blocks"]) == 6
    assert len({block["id"] for block in bound["blocks"]}) == 6
    for block in bound["blocks"]:
        assert block == source[block["id"]]
        assert len(block["text"].encode("utf-8")) == block["byte_length"]
        assert (
            "sha256:" + sha256(block["text"].encode("utf-8")).hexdigest()
            == (block["sha256"])
        )


def test_bound_support_pairs_equal_the_sealed_locator_closure() -> None:
    bound = _load(PRIVATE_EVAL / "bound-support-blocks.json")
    locator = _load(PRIVATE_EVAL / "oracle-locator-binding.json")
    actual = {(block["id"], block["sha256"]) for block in bound["blocks"]}
    expected = {
        (block["id"], block["sha256"])
        for binding in locator["bindings"]
        for block in binding["blocks"]
    }
    assert actual == expected


def test_review_input_manifest_closes_runtime_and_input_bytes() -> None:
    manifest = _load(EXPERIMENT / "ontology-review-input-manifest.json")
    assert manifest["schema"] == ("malleus.paper-v4.ontology-review-input-manifest/v1")
    execution = manifest["execution"]
    assert platform.python_implementation() == execution["python_implementation"]
    assert platform.python_version() == execution["python_version"]
    for distribution, expected_version in execution["distributions"].items():
        assert version(distribution) == expected_version

    inputs = manifest["inputs"]
    assert len(inputs) == 16
    assert len({item["role"] for item in inputs}) == 16
    for item in inputs:
        if "path" in item:
            source = (ROOT / item["path"]).read_bytes()
        else:
            assert item["role"] == "linkml_types"
            source = (
                files("linkml_runtime")
                .joinpath("linkml_model", "model", "schema", "types.yaml")
                .read_bytes()
            )
            assert len(source) == item["byte_length"]
        assert "sha256:" + sha256(source).hexdigest() == item["sha256"]
