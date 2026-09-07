"""Freeze the input incompatibility, not a passing action implementation.

The current refusals are snapshot observations. A future fix must replace this
blocked packet with positive compiled-contract and full action conformance.
No private imports, outcome stubs, interpreter, or ledger writes are used.
"""

from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest

import malleus.compiler as api
from malleus import OntologyRegistry


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(value):
    return "sha256:" + sha256(value).hexdigest()


def canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sources():
    return {
        "assent": (ROOT / "ontology/assent.yaml").read_bytes(),
        "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
        "linkml:types": files("linkml_runtime")
        .joinpath("linkml_model/model/schema/types.yaml")
        .read_bytes(),
    }


def test_exact_record_and_implementation_inputs_are_bound():
    manifest = json.loads((HERE / "inputs.json").read_bytes())
    for path, identity in manifest["repository_inputs"].items():
        assert digest((ROOT / path).read_bytes()) == identity
    assert digest(sources()["linkml:types"]) == manifest["linkml_types"]["sha256"]


@pytest.mark.parametrize("root", ["assent", "action-probe"])
def test_exact_assent_closure_refuses_before_action_contract_can_be_frozen(root):
    inputs = sources()
    if root == "action-probe":
        inputs[root] = (HERE / "action-probe.yaml").read_bytes()
    before = dict(inputs)
    with pytest.raises(api.ElaborationRefusal) as caught:
        api.compile_linkml_contract(root_locator=root, sources=inputs)
    assert caught.value.reason.name == "INVALID_RANGE"
    assert "https://malleus.dev/schema/assent/calendar_date" in str(caught.value)
    assert "https://w3id.org/linkml/types/date" in str(caught.value)
    assert inputs == before


def test_same_assent_and_adopter_import_load_in_existing_registry():
    registry = OntologyRegistry(
        HERE / "action-probe.yaml",
        import_map={"assent": ROOT / "ontology/assent.yaml"},
    )
    assert registry.is_subtype_of("LocalAction", "ActionProposal")
    assert registry.has_type("ActionDispatch")
    assert registry.has_type("AuthorityGrant")
    assert registry.has_type("OutcomeObservation")
    assert not registry.get_type("LocalAction").abstract


def test_public_compiler_positive_control_without_assent():
    inputs = sources()
    del inputs["assent"]
    inputs["entity-control"] = (HERE / "entity-control.yaml").read_bytes()
    result = api.compile_linkml_contract(root_locator="entity-control", sources=inputs)
    assert result.view.is_subtype_of("LocalEntity", "Entity")


@pytest.mark.parametrize("kind", ["BOOLEAN", "INTEGER", "ARRAY", "OBJECT"])
def test_current_machine_does_not_claim_richer_record_field_types(kind):
    program = json.loads(
        (ROOT / "src/malleus/profiles/structural-history-machine.json").read_bytes()
    )
    first_schema = next(iter(program["record_schemas"].values()))
    first_field = next(iter(first_schema["fields"]))
    first_schema["fields"][first_field] = kind
    with pytest.raises(api.ProtocolMachineProgramRefusal) as caught:
        api.ProtocolMachineProgram.from_bytes(canonical(program))
    assert "unsupported field type" in str(caught.value)


@pytest.mark.parametrize("verdict", ["AUTHORIZE", "BLOCK", "CLARIFY"])
def test_current_policy_cannot_disguise_authorization_as_epistemic_verdict(verdict):
    policy = json.loads(
        (ROOT / "src/malleus/profiles/structural-admission-policy.json").read_bytes()
    )
    policy["outcome_verdicts"] = {
        outcome: verdict for outcome in policy["outcome_verdicts"]
    }
    policy["precedence"] = [verdict]
    with pytest.raises(api.MachineArtifactRefusal) as caught:
        api.PolicyProgram.from_bytes(canonical(policy))
    assert "outcome mapping is malformed" in str(caught.value)


def test_unmodified_machine_and_policy_positive_controls():
    program = api.ProtocolMachineProgram.from_bytes(
        canonical(
            json.loads(
                (
                    ROOT / "src/malleus/profiles/structural-history-machine.json"
                ).read_bytes()
            )
        )
    )
    policy = api.PolicyProgram.from_bytes(
        canonical(
            json.loads(
                (
                    ROOT / "src/malleus/profiles/structural-admission-policy.json"
                ).read_bytes()
            )
        )
    )
    assert program.capabilities == ()
    assert set(policy.outcome_verdicts.values()) <= {
        "ACCEPT",
        "REJECT",
        "DEFER",
        "CONTEST",
    }


@pytest.mark.parametrize(
    "name,loader,refusal",
    [
        (
            "structural-history-machine.json",
            api.ProtocolMachineProgram.from_bytes,
            api.ProtocolMachineProgramRefusal,
        ),
        (
            "structural-admission-policy.json",
            api.PolicyProgram.from_bytes,
            api.MachineArtifactRefusal,
        ),
    ],
)
def test_raw_resource_format_is_not_mistaken_for_canonical_artifact(
    name, loader, refusal
):
    raw = (ROOT / "src/malleus/profiles" / name).read_bytes()
    normalized = canonical(json.loads(raw))
    assert raw != normalized
    with pytest.raises(refusal) as caught:
        loader(raw)
    assert caught.value.reason.name.startswith("NONCANONICAL")
    assert loader(normalized).canonical_bytes == normalized
