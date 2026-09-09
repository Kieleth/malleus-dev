"""Subset checks preserve the declared surface and original judgments."""

from copy import deepcopy
import json

import pytest

from recheck import validate_subset
from review_packet import canonical, digest


pytest_plugins = ["test_selective_review"]


def subset(folder, record):
    return {
        "review_input_manifest_sha256": digest(
            (folder / "review-input-manifest.json").read_bytes()
        ),
        "questions": deepcopy(record["questions"][:1]),
        "witnesses": deepcopy(record["witnesses"]),
    }


def test_subset_uses_manifest_surface_without_changing_judgments(synthetic_packet):
    folder, record = synthetic_packet
    value = subset(folder, record)
    before = deepcopy(value)
    assert validate_subset(folder, value, ["A"]) == before
    assert value == before


def test_guessed_surface_refuses_before_locator_dispatch(synthetic_packet):
    folder, record = synthetic_packet
    path = folder / "review-input-manifest.json"
    manifest = json.loads(path.read_bytes())
    manifest["evidence_surface"]["kind"] = "TEXT_LAYER"
    path.write_bytes(canonical(manifest))
    with pytest.raises(ValueError, match="unsupported recheck evidence surface"):
        validate_subset(folder, subset(folder, record), ["A"])


@pytest.mark.parametrize("selection", [[], ["A", "A"], ["UNKNOWN"]])
def test_invalid_subset_selection_refuses(synthetic_packet, selection):
    folder, record = synthetic_packet
    with pytest.raises(ValueError, match="recheck (question selection|selects)"):
        validate_subset(folder, subset(folder, record), selection)


def test_subset_cannot_omit_witness_or_invent_source_locator(synthetic_packet):
    folder, record = synthetic_packet
    value = subset(folder, record)
    value["witnesses"] = []
    with pytest.raises(ValueError, match="every returned witness"):
        validate_subset(folder, value, ["A"])
    value = subset(folder, record)
    value["witnesses"][0]["source_locators"] = ["unknown:block"]
    with pytest.raises(ValueError, match="unknown"):
        validate_subset(folder, value, ["A"])
