"""Public contract for optional grounded knowledge packs."""

from __future__ import annotations

from hashlib import sha256
from importlib import import_module
from importlib.resources import files
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from malleus.ontology import bundled_ontology_path


ROOT = Path(__file__).resolve().parents[3]
PACK_NAMES = ("metrology", "chronology", "research")
ASSERTION_MODALITIES = {
    "STATED",
    "MEASURED",
    "CALCULATED",
    "HYPOTHESISED",
    "CONTESTED",
    "NEGATED",
}


def _compiler():
    return import_module("malleus.compiler")


def _inquisition():
    return import_module("malleus.inquisition")


def _linkml_types() -> bytes:
    return (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )


def _pack_sources() -> dict[str, bytes]:
    return {
        "linkml:types": _linkml_types(),
        "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
        **{
            name: bundled_ontology_path("packs", f"{name}.yaml").read_bytes()
            for name in PACK_NAMES
        },
    }


def _annotation(value: dict[str, object]) -> dict[str, object]:
    return {"grounding": {"tag": "grounding", "value": value}}


def _cited_grounding() -> dict[str, object]:
    return {
        "area": "Physical measurement",
        "taxonomy": "DDC 530.8",
        "vocabularies": [
            {
                "vocabulary": "JCGM 200:2012 (VIM), 3rd edition",
                "vocabulary_url": "https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf",
                "borrowed_terms": ["quantity value"],
            }
        ],
        "invented_terms": [],
    }


def _source(
    *,
    annotations: dict[str, object] | None = None,
    class_annotations: dict[str, object] | None = None,
    parent: str = "Entity",
) -> bytes:
    value: dict[str, object] = {
        "id": "https://example.org/project",
        "name": "project",
        "imports": ["linkml:types", "malleus"],
        "classes": {"ProjectThing": {"is_a": parent}},
    }
    if annotations is not None:
        value["annotations"] = annotations
    if class_annotations is not None:
        value["classes"]["ProjectThing"]["annotations"] = class_annotations
    return yaml.safe_dump(value, sort_keys=False).encode()


def test_public_grounding_rite_surface_is_explicit() -> None:
    api = _inquisition()
    assert {
        "PackGroundingReceipt",
        "PackGroundingRefusal",
        "PackGroundingRefusalReason",
        "validate_pack_grounding",
    } <= set(api.__all__)


@pytest.mark.parametrize("name", PACK_NAMES)
def test_shipped_pack_is_resolvable_grounded_and_compilable(name: str) -> None:
    compiler = _compiler()
    rite = _inquisition()
    path = bundled_ontology_path("packs", f"{name}.yaml")
    source = path.read_bytes()

    receipt = rite.validate_pack_grounding(source, role="PACK")
    compiled = compiler.compile_linkml_contract(
        root_locator=name,
        sources=_pack_sources(),
    )

    assert receipt.role == "PACK"
    assert receipt.source_sha256 == "sha256:" + sha256(source).hexdigest()
    assert receipt.grounded_subjects == ("https://malleus.dev/schema/packs/" + name,)
    assert compiled.artifact.validated_fact_set_sha256.startswith("sha256:")


def test_research_pack_carries_the_shared_assertion_modality() -> None:
    source = yaml.safe_load(bundled_ontology_path("packs", "research.yaml").read_bytes())
    values = source["enums"]["AssertionModality"]["permissible_values"]
    assert set(values) == ASSERTION_MODALITIES


def test_research_observation_is_explicitly_grounded_in_sosa_ssn() -> None:
    source = yaml.safe_load(bundled_ontology_path("packs", "research.yaml").read_bytes())
    vocabularies = source["annotations"]["grounding"]["value"]["vocabularies"]
    sosa = next(
        item for item in vocabularies if item["vocabulary"] == "W3C SOSA/SSN"
    )
    assert sosa["vocabulary_url"] == "https://www.w3.org/TR/vocab-ssn/"
    assert "Observation" in sosa["borrowed_terms"]


def test_project_importing_research_and_metrology_compiles_through_public_api() -> None:
    sources = _pack_sources()
    sources["project"] = b"""\
id: https://example.org/grounded-project
name: grounded_project
imports:
  - linkml:types
  - malleus
  - research
  - metrology
classes:
  StudyObservation:
    is_a: Observation
"""

    compiled = _compiler().compile_linkml_contract(
        root_locator="project",
        sources=sources,
    )

    assert compiled.view.is_subtype_of("StudyObservation", "Entity")
    assert compiled.view.has_enum("AssertionModality")


def test_pack_without_grounding_refuses_with_typed_reason() -> None:
    api = _inquisition()
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(_source(), role="PACK")
    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_REQUIRED


@pytest.mark.parametrize(
    "mutation,reason",
    [
        (
            lambda value: value.update({"surprise": "not declared"}),
            "GROUNDING_NOT_CLOSED",
        ),
        (
            lambda value: value["vocabularies"][0].update({"vocabulary_url": ""}),
            "GROUNDING_INCOMPLETE",
        ),
        (
            lambda value: value["vocabularies"][0].update({"borrowed_terms": []}),
            "GROUNDING_INCOMPLETE",
        ),
    ],
)
def test_grounding_shape_refuses_unknown_or_missing_meaning(mutation, reason: str) -> None:
    api = _inquisition()
    grounding = _cited_grounding()
    mutation(grounding)
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            _source(annotations=_annotation(grounding)),
            role="PACK",
        )
    assert caught.value.reason.name == reason


def test_project_direct_root_extension_requires_its_own_grounding() -> None:
    api = _inquisition()
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(_source(), role="PROJECT")
    assert (
        caught.value.reason
        is api.PackGroundingRefusalReason.DIRECT_ROOT_GROUNDING_REQUIRED
    )


def test_project_may_record_a_bounded_none_found_search() -> None:
    api = _inquisition()
    none_found = {
        "area": "Retail operations",
        "taxonomy": "DDC 658.8",
        "none_found": True,
        "search": "No shared vocabulary found for the local shelf marker.",
        "invented_terms": ["LocalShelfMarker"],
    }
    receipt = api.validate_pack_grounding(
        _source(class_annotations=_annotation(none_found)),
        role="PROJECT",
    )
    assert receipt.grounded_subjects == ("ProjectThing",)


def test_project_class_extending_a_pack_class_needs_no_duplicate_grounding() -> None:
    receipt = _inquisition().validate_pack_grounding(
        _source(parent="Observation"),
        role="PROJECT",
    )
    assert receipt.grounded_subjects == ()


def test_grounding_changes_source_attestation_not_contract_fact_identity() -> None:
    sources = _pack_sources()
    baseline = _compiler().compile_linkml_contract(
        root_locator="metrology",
        sources=sources,
    )
    changed = yaml.safe_load(sources["metrology"])
    changed["annotations"]["grounding"]["value"]["area"] = (
        "Physical measurement and metrology"
    )
    sources["metrology"] = yaml.safe_dump(changed, sort_keys=False).encode()
    described = _compiler().compile_linkml_contract(
        root_locator="metrology",
        sources=sources,
    )

    assert baseline.artifact.validated_fact_set_sha256 == (
        described.artifact.validated_fact_set_sha256
    )
    assert baseline.artifact.evidence != described.artifact.evidence
    assert baseline.artifact.artifact_bytes != described.artifact.artifact_bytes


def test_pack_grounding_cli_reports_the_exact_receipt() -> None:
    path = bundled_ontology_path("packs", "metrology.yaml")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.inquisition.cli",
            "pack-grounding",
            str(path),
            "--role",
            "PACK",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["role"] == "PACK"
    assert payload["source_sha256"] == "sha256:" + sha256(path.read_bytes()).hexdigest()
