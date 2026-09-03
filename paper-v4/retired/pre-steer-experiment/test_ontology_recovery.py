"""Hard guards for the frozen post-primary ontology recovery."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from malleus._contract_pipeline import load_validated_contract_artifact
from research.ontology_driven_kg_realization.experiments.document_paper.compiled_graph_recipe_contract import (
    derive_compiled_logical_contract,
)
from research.ontology_driven_kg_realization.experiments.document_paper.ontology_compile import (
    ExactSource,
    compile_exact_ontology,
)
from research.ontology_driven_kg_realization.experiments.document_paper.ontology_review_inputs import (
    PAPER_RECORD_TYPE_IRIS,
    _schema_inventory,
)


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "paper-v4/experiment"
PRIVATE_EVALUATION = ROOT / "private/paper-v4-evaluation"
ORIGINAL = EXPERIMENT / "model-ontology-proposal.yaml"
RECOVERY = EXPERIMENT / "controlled-ontology-recovery.yaml"
COMPILED = EXPERIMENT / "ontology-recovery-compilation"

ORIGINAL_SHA256 = "5abfa4774d932ed79e637c82396538620ee7fe8e460e59ad17ecf812fa44f4df"
RECOVERY_SHA256 = "29fca9e9325c9d14e5070bcb4274c8704f9d1aaa058799e5a81f27cb5a5a99e9"
MALLEUS_SHA256 = "5b737c212a5893ceebb22be207a09f3eb09ebab269898d354bb1dacdaad0aff3"
LINKML_TYPES_SHA256 = "1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00"
CONTRACT_SHA256 = "4e5297a3844e55a17c21dbbbd94778f8426cad91a14f1f42e2c747ad8c2d72cd"
RECEIPT_SHA256 = "f8843baa1802529de46df8410dcd16f14bdebc0a9db048850175654ecad2277b"

FROZEN_EVALUATION_INPUTS = {
    EXPERIMENT / "competency-questions.json": (
        "5ec41374e32a8745963a0f0498e2044f225dec47a6cbfcfde1417752b27b9a92"
    ),
    PRIVATE_EVALUATION / "answer-oracle.json": (
        "95b206a8a8eac20f208854c2374ed8433187402d9ab1e50771003e412066b571"
    ),
    PRIVATE_EVALUATION / "oracle-locator-binding.json": (
        "bd61e591b77e05ed28babff4300b2b913f6a92a76635d15742d4530e0faaa15c"
    ),
    PRIVATE_EVALUATION / "ontology-adequacy-rubric.json": (
        "f73c86e2635afa78661acffc1cc5b8aeca6924d446d4a52e44fc7ac739936a10"
    ),
    PRIVATE_EVALUATION / "support-adjudication-guide.json": (
        "e4b0ee89ee87db51201e4e183b94162bb01ea8b81cc9bc131d0971cb792cdb53"
    ),
}


def _sha256(source: bytes) -> str:
    return sha256(source).hexdigest()


def _read_yaml(path: Path) -> dict[str, object]:
    loaded = yaml.safe_load(path.read_bytes())
    assert type(loaded) is dict
    return loaded


def _canonical(value: object) -> str:
    return json.dumps(value, separators=(",", ":"), sort_keys=True)


def _semantic_diff(
    before: object,
    after: object,
    path: tuple[str, ...] = (),
) -> list[tuple[str, str, str | None, str | None]]:
    if type(before) is dict and type(after) is dict:
        differences: list[tuple[str, str, str | None, str | None]] = []
        before_mapping = before
        after_mapping = after
        for key in sorted(set(before_mapping) | set(after_mapping)):
            child_path = (*path, str(key))
            if key not in before_mapping:
                differences.append(
                    (".".join(child_path), "ADD", None, _canonical(after_mapping[key]))
                )
            elif key not in after_mapping:
                differences.append(
                    (
                        ".".join(child_path),
                        "REMOVE",
                        _canonical(before_mapping[key]),
                        None,
                    )
                )
            else:
                differences.extend(
                    _semantic_diff(
                        before_mapping[key],
                        after_mapping[key],
                        child_path,
                    )
                )
        return differences
    if before == after:
        return []
    return [(".".join(path), "REPLACE", _canonical(before), _canonical(after))]


def _source(locator: str, source: bytes, digest: str) -> ExactSource:
    return ExactSource(locator, source, f"sha256:{digest}")


def test_original_candidate_bytes_remain_frozen() -> None:
    assert _sha256(ORIGINAL.read_bytes()) == ORIGINAL_SHA256


def test_parsed_semantic_diff_is_exactly_the_three_allowed_changes() -> None:
    original = _read_yaml(ORIGINAL)
    recovery = _read_yaml(RECOVERY)
    instrument_constraints = {
        "minimum_value": 1,
        "range": "integer",
        "required": True,
    }

    assert _sha256(RECOVERY.read_bytes()) == RECOVERY_SHA256
    assert _semantic_diff(original, recovery) == [
        (
            "classes.ObservationNetwork.slots",
            "REPLACE",
            '["instrument_count"]',
            '["deployed_instrument_count","usable_instrument_count"]',
        ),
        (
            "slots.deployed_instrument_count",
            "ADD",
            None,
            _canonical(instrument_constraints),
        ),
        (
            "slots.instrument_count",
            "REMOVE",
            _canonical(instrument_constraints),
            None,
        ),
        (
            "slots.usable_instrument_count",
            "ADD",
            None,
            _canonical(instrument_constraints),
        ),
        ("version", "REPLACE", '"0.1.0"', '"0.1.1"'),
    ]

    expected = deepcopy(original)
    expected["version"] = "0.1.1"
    classes = expected["classes"]
    assert type(classes) is dict
    observation_network = classes["ObservationNetwork"]
    assert type(observation_network) is dict
    observation_network["slots"] = [
        "deployed_instrument_count",
        "usable_instrument_count",
    ]
    slots = expected["slots"]
    assert type(slots) is dict
    previous = slots.pop("instrument_count")
    slots["deployed_instrument_count"] = previous
    slots["usable_instrument_count"] = deepcopy(previous)
    assert recovery == expected


def test_all_forbidden_semantic_surfaces_and_evaluation_inputs_are_unchanged() -> None:
    original = _read_yaml(ORIGINAL)
    recovery = _read_yaml(RECOVERY)

    assert set(recovery["classes"]) == set(original["classes"])
    assert recovery["enums"] == original["enums"]
    assert {
        key: value
        for key, value in recovery.items()
        if key not in {"classes", "slots", "version"}
    } == {
        key: value
        for key, value in original.items()
        if key not in {"classes", "slots", "version"}
    }

    original_classes = original["classes"]
    recovery_classes = recovery["classes"]
    assert type(original_classes) is dict
    assert type(recovery_classes) is dict
    for class_name in original_classes:
        if class_name != "ObservationNetwork":
            assert recovery_classes[class_name] == original_classes[class_name]
    original_network = original_classes["ObservationNetwork"]
    recovery_network = recovery_classes["ObservationNetwork"]
    assert type(original_network) is dict
    assert type(recovery_network) is dict
    assert {
        key: value for key, value in recovery_network.items() if key != "slots"
    } == {key: value for key, value in original_network.items() if key != "slots"}

    original_slots = original["slots"]
    recovery_slots = recovery["slots"]
    assert type(original_slots) is dict
    assert type(recovery_slots) is dict
    for slot_name in original_slots:
        if slot_name != "instrument_count":
            assert recovery_slots[slot_name] == original_slots[slot_name]
    assert (
        recovery_slots["deployed_instrument_count"]
        == original_slots["instrument_count"]
    )
    assert (
        recovery_slots["usable_instrument_count"] == original_slots["instrument_count"]
    )

    for path, digest in FROZEN_EVALUATION_INPUTS.items():
        assert _sha256(path.read_bytes()) == digest


def test_retained_compilation_is_exact_reproducible_and_reloadable() -> None:
    root = RECOVERY.read_bytes()
    malleus = (ROOT / "ontology/malleus.yaml").read_bytes()
    linkml_types = (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )
    reproduced = compile_exact_ontology(
        root=_source("paper-v4-domain", root, RECOVERY_SHA256),
        malleus=_source("malleus", malleus, MALLEUS_SHA256),
        linkml_types=_source("linkml:types", linkml_types, LINKML_TYPES_SHA256),
    )
    contract_bytes = (COMPILED / "validated-contract.json").read_bytes()
    receipt_bytes = (COMPILED / "compile-receipt.json").read_bytes()

    assert {path.name for path in COMPILED.iterdir()} == {
        "compile-receipt.json",
        "validated-contract.json",
    }
    assert reproduced.validated_contract_bytes == contract_bytes
    assert reproduced.receipt_bytes == receipt_bytes
    assert _sha256(contract_bytes) == CONTRACT_SHA256
    assert _sha256(receipt_bytes) == RECEIPT_SHA256

    receipt = json.loads(receipt_bytes)
    assert receipt["status"] == "ACCEPTED"
    assert receipt["fact_count"] == 1648
    assert receipt["facts_sha256"] == (
        "sha256:8fdc1ae6d76ee60d2b4f52f6b4b02c783820e34090322f2293f5e14f9a9a8df2"
    )
    assert receipt["validated_fact_set_sha256"] == (
        "sha256:c7b71d094fd8ea2bb7a9e368c581475891f110538caebeaceedca9d7532b3332"
    )
    assert receipt["validated_contract_sha256"] == f"sha256:{CONTRACT_SHA256}"
    assert receipt["resolver_selection"] == {
        "configuration_id": (
            "sha256:3d1d1e92953efb97b03c7befcf66b65752c34cfb961ac39d317c5f0b4eae5902"
        ),
        "profile_version": "MALLEUS_PAPER_V4_EXACT_MEMORY_RESOLVER_V0",
        "resolver_id": "MALLEUS_PAPER_V4_EXACT_MEMORY_RESOLVER",
    }
    assert [source["sha256"] for source in receipt["sources"]] == [
        f"sha256:{LINKML_TYPES_SHA256}",
        f"sha256:{MALLEUS_SHA256}",
        f"sha256:{RECOVERY_SHA256}",
    ]

    view = load_validated_contract_artifact(contract_bytes)
    assert view.content_hash() == (
        "c7b71d094fd8ea2bb7a9e368c581475891f110538caebeaceedca9d7532b3332"
    )


def test_recovery_review_inventory_and_eligibility_are_exact() -> None:
    root = RECOVERY.read_bytes()
    malleus = (ROOT / "ontology/malleus.yaml").read_bytes()
    linkml_types = (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )
    compilation = compile_exact_ontology(
        root=_source("paper-v4-domain", root, RECOVERY_SHA256),
        malleus=_source("malleus", malleus, MALLEUS_SHA256),
        linkml_types=_source("linkml:types", linkml_types, LINKML_TYPES_SHA256),
    )
    logical = derive_compiled_logical_contract(
        compilation.compilation,
        record_type_iris=PAPER_RECORD_TYPE_IRIS,
        contract_id="https://malleus.dev/contracts/paper-v4-domain-proposal",
    )
    inventory_path = (
        EXPERIMENT / "ontology-recovery-review-inputs/schema-inventory.json"
    )
    inventory_bytes = inventory_path.read_bytes()
    reproduced = (
        json.dumps(
            _schema_inventory(compilation, logical),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        + b"\n"
    )
    assert inventory_bytes == reproduced
    assert _sha256(inventory_bytes) == (
        "1464603552d33e8953084dbe729942eb631ea2eda0eee2f4711dadd2c183ef3a"
    )
    inventory = json.loads(inventory_bytes)
    assert inventory["candidate_sha256"] == f"sha256:{RECOVERY_SHA256}"
    assert inventory["compiled"]["fact_count"] == 1648
    assert len(inventory["compiled_classes"]) == 15
    network = next(
        item
        for item in inventory["compiled_classes"]
        if item["iri"].endswith("/ObservationNetwork")
    )
    count_slots = {
        slot["iri"].rsplit("/", 1)[-1]: slot
        for slot in network["effective_slots"]
        if slot["iri"].endswith("instrument_count")
    }
    assert set(count_slots) == {
        "deployed_instrument_count",
        "usable_instrument_count",
    }
    assert all(slot["required"] is True for slot in count_slots.values())

    eligibility = json.loads(
        (
            EXPERIMENT / "ontology-recovery-review-inputs/review-eligibility.json"
        ).read_bytes()
    )
    assert eligibility["verdict"] == "PASS"
    assert eligibility["classification"] == "POST_PRIMARY_CONTROL"
    assert eligibility["primary_result_changed"] is False
    assert eligibility["schema_inventory_sha256"] == (
        "sha256:" + _sha256(inventory_bytes)
    )
    assert all(check["verdict"] == "PASS" for check in eligibility["checks"])


def test_recovery_review_output_schema_is_valid_and_distinct() -> None:
    schema = json.loads(
        (EXPERIMENT / "ontology-recovery-review-output-schema.json").read_bytes()
    )
    Draft202012Validator.check_schema(schema)
    assert schema["properties"]["reviewer_id"]["const"] == (
        "reviewer:codex-paper-recovery-evaluator-v1"
    )
    assert schema["properties"]["status"]["enum"] == [
        "SELECTED_CONTROL",
        "REFUSED_CONTROL",
        "EVALUATION_INVALID",
    ]
