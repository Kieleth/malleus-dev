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
        "PackConformanceReceipt",
        "PackGroundingReceipt",
        "PackGroundingRefusal",
        "PackGroundingRefusalReason",
        "validate_pack_conformance",
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
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    values = source["enums"]["AssertionModality"]["permissible_values"]
    assert set(values) == ASSERTION_MODALITIES


def test_metrology_uses_the_exact_vim_term_for_quantity_kind() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    )
    vocabularies = source["annotations"]["grounding"]["value"]["vocabularies"]
    vim_terms = next(
        item["borrowed_terms"]
        for item in vocabularies
        if item["vocabulary"].startswith("JCGM 200:2012")
    )

    assert "kind of quantity" in vim_terms
    assert "quantity kind" not in vim_terms
    assert "quantity_kind" in source["slots"]


def test_research_observation_is_explicitly_grounded_in_sosa_ssn() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    vocabularies = source["annotations"]["grounding"]["value"]["vocabularies"]
    sosa = next(item for item in vocabularies if item["vocabulary"] == "W3C SOSA/SSN")
    assert sosa["vocabulary_url"] == "https://www.w3.org/TR/vocab-ssn/"
    assert "Observation" in sosa["borrowed_terms"]


def test_research_grounding_assigns_only_supported_term_groups() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    grounding = source["annotations"]["grounding"]["value"]
    vocabularies = {
        item["vocabulary"]: item["borrowed_terms"] for item in grounding["vocabularies"]
    }

    assert vocabularies["W3C SOSA/SSN"] == ["Observation", "Sample"]
    assert vocabularies["JCGM 200:2012 (VIM), 3rd edition"] == ["measuring instrument"]
    assert vocabularies["OECD Frascati Manual 2015"] == [
        "research and experimental development",
        "investigation",
        "method",
    ]
    assert vocabularies["SEPIO"] == [
        "assertion",
        "Data Item",
        "Evidence Line",
        "support",
        "refute",
    ]
    assert {"Agent", "Campaign", "Instrument"}.isdisjoint(
        term for terms in vocabularies.values() for term in terms
    )
    assert grounding["invented_terms"] == ["Campaign", "Instrument"]
    assert grounding["invention_search"]


def test_research_pack_matches_the_accepted_campaign_surface() -> None:
    source = yaml.safe_load(
        bundled_ontology_path("packs", "research.yaml").read_bytes()
    )
    classes = source["classes"]
    relations = source["enums"]["ResearchRelationType"]["permissible_values"]

    assert source["imports"] == ["linkml:types", "malleus", "metrology", "chronology"]
    assert classes["Campaign"]["is_a"] == "Entity"
    assert classes["Campaign"]["mixins"] == ["TemporalExtent", "Counted"]
    assert "Investigation" not in classes
    assert "PART_OF_CAMPAIGN" in relations
    assert "PART_OF_INVESTIGATION" not in relations


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


def test_edited_pack_conformance_refuses_a_deleted_reference_surface() -> None:
    api = _inquisition()
    reference = bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    edited = yaml.safe_load(reference)
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    del edited["classes"]
    del edited["slots"]
    del edited["enums"]
    candidate = yaml.safe_dump(edited, sort_keys=False).encode()

    assert api.validate_pack_grounding(candidate, role="PACK")
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_conformance(candidate, reference=reference)

    assert (
        caught.value.reason is api.PackGroundingRefusalReason.PACK_SURFACE_NOT_PRESERVED
    )
    assert "classes.Counted" in caught.value.detail
    assert "enums.Determination" in caught.value.detail
    assert "slots.quantity_kind" in caught.value.detail


def test_edited_pack_conformance_allows_documentation_and_additive_changes() -> None:
    api = _inquisition()
    reference = bundled_ontology_path("packs", "metrology.yaml").read_bytes()
    edited = yaml.safe_load(reference)
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    edited["description"] = "A locally documented compatible copy."
    edited["classes"]["LocalReading"] = {"is_a": "QuantityValue"}
    edited["enums"]["Determination"]["permissible_values"]["CALIBRATED"] = None
    candidate = yaml.safe_dump(edited, sort_keys=False).encode()

    receipt = api.validate_pack_conformance(candidate, reference=reference)

    assert receipt.source_id == "https://example.org/packs/local-metrology"
    assert receipt.reference_id == "https://malleus.dev/schema/packs/metrology"
    assert receipt.source_sha256 == "sha256:" + sha256(candidate).hexdigest()
    assert receipt.reference_sha256 == "sha256:" + sha256(reference).hexdigest()


def test_pack_without_grounding_refuses_with_typed_reason() -> None:
    api = _inquisition()
    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(_source(), role="PACK")
    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_REQUIRED


def test_duplicate_yaml_key_refuses_as_malformed_source() -> None:
    api = _inquisition()

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            b"id: https://example.org/one\nid: https://example.org/two\n",
            role="PACK",
        )

    assert caught.value.reason is api.PackGroundingRefusalReason.MALFORMED_SOURCE
    assert "Duplicate YAML key 'id'" in caught.value.detail


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
def test_grounding_shape_refuses_unknown_or_missing_meaning(
    mutation, reason: str
) -> None:
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


def test_cited_grounding_requires_a_search_when_it_invents_terms() -> None:
    api = _inquisition()
    grounding = _cited_grounding()
    grounding["invented_terms"] = ["LocalInstrument"]

    with pytest.raises(api.PackGroundingRefusal) as caught:
        api.validate_pack_grounding(
            _source(annotations=_annotation(grounding)),
            role="PACK",
        )

    assert caught.value.reason is api.PackGroundingRefusalReason.GROUNDING_INCOMPLETE


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


def test_pack_grounding_cli_reports_duplicate_key_as_typed_refusal(
    tmp_path: Path,
) -> None:
    path = tmp_path / "duplicate.yaml"
    path.write_bytes(b"id: https://example.org/one\nid: https://example.org/two\n")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.inquisition.cli",
            "pack-grounding",
            str(path),
            "--role",
            "PACK",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "MALFORMED_SOURCE" in result.stderr
    assert "Duplicate YAML key 'id'" in result.stderr
    assert "Traceback" not in result.stderr


def test_pack_conformance_cli_refuses_a_deleted_reference_surface(
    tmp_path: Path,
) -> None:
    reference = bundled_ontology_path("packs", "metrology.yaml")
    edited = yaml.safe_load(reference.read_bytes())
    edited["id"] = "https://example.org/packs/local-metrology"
    edited["name"] = "local_metrology"
    del edited["classes"]
    del edited["slots"]
    del edited["enums"]
    candidate = tmp_path / "local-metrology.yaml"
    candidate.write_text(yaml.safe_dump(edited, sort_keys=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.inquisition.cli",
            "pack-conformance",
            str(candidate),
            "--against",
            str(reference),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "PACK_SURFACE_NOT_PRESERVED" in result.stderr
    assert "Traceback" not in result.stderr
