"""CONFORMANCE_FIXTURE: pure components, no executed or observed action."""

import ast
import builtins
from copy import deepcopy
from hashlib import sha256
from importlib import import_module
import io
import json
from pathlib import Path

import pytest


FIXTURE = Path(__file__).parent / "fixtures/supplier_commitment_v1"
MODULE = "research.semantic_reentry_external_design.supplier_components"
FIELDS = {"event_id", "product_code", "quantity", "supplier_order_id"}
SOURCE_ID = "source:reentry:supplier:authored-component-input"


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(content):
    return "sha256:" + sha256(content).hexdigest()


@pytest.fixture
def inputs():
    case = json.loads((FIXTURE / "case.json").read_bytes())
    return {
        "before_bytes": (FIXTURE / case["source"]["path"]).read_bytes(),
        "source_sha256": case["source"]["sha256"],
        "goal": case["goal"],
        "operator": case["operator"],
        "mapping": case["mapping"],
        "source_id": SOURCE_ID,
    }


@pytest.fixture
def supplied_after():
    # Authored test input only. Reading this oracle does not capture a source.
    return (FIXTURE / "oracle/supplier-after.jsonl").read_bytes()


def model(inputs):
    return import_module(MODULE).model_amendment(
        **{
            key: value
            for key, value in inputs.items()
            if key not in {"mapping", "source_id"}
        }
    )


def mapper(inputs, observed):
    return import_module(MODULE).map_observation(observed, **inputs)


def refuses(reason, function, *args):
    implementation = import_module(MODULE)
    with pytest.raises(implementation.SupplierInputError) as error:
        function(*args)
    assert error.value.reason == reason
    assert str(error.value)


def test_prediction_agrees_with_independent_oracle_and_source_frame(
    inputs, supplied_after
):
    old = deepcopy(inputs)
    predicted = model(inputs)
    assert predicted == supplied_after
    before, after = json.loads(inputs["before_bytes"]), json.loads(predicted)
    assert {key for key in before if before[key] != after[key]} == {
        "event_id",
        "quantity",
    }
    assert {key: after[key] for key in FIELDS - {"event_id", "quantity"}} == {
        "product_code": "Y",
        "supplier_order_id": "B",
    }
    assert predicted.endswith(b"\n") and predicted.count(b"\n") == 1
    assert type(predicted) is bytes
    assert model(inputs) == predicted
    assert inputs == old


def test_mapper_emits_only_existing_complete_population_fields(inputs, supplied_after):
    old = deepcopy(inputs)
    output = mapper(inputs, supplied_after)
    fragment = json.loads(output)
    replacement = inputs["mapping"]["replacement_record_id"]
    assert fragment == {
        "records": {
            "entities": [
                {
                    "id": replacement,
                    "type": "SupplierOrderState",
                    "properties": {
                        "supplier_order_id": "B",
                        "product_code": "Y",
                        "ordered_quantity": 2,
                        "source_occurrence_id": "reentry-amendment-1",
                    },
                }
            ],
            "relations": [],
        },
        "sources": [{"source_id": SOURCE_ID, "sha256": digest(supplied_after)}],
        "derivations": [
            {
                "record_id": replacement,
                "path": ["properties", field],
                "source_id": SOURCE_ID,
                "locator": f"row:0:{source}",
            }
            for field, source in sorted(inputs["mapping"]["fields"].items())
        ],
        "supersessions": [
            {
                "record_id": replacement,
                "supersedes_record_id": "supplier-order-state:B:e4",
            }
        ],
        "valid_time": {"kind": "ORDER_ONLY", "value": "reentry-amendment-1"},
    }
    assert type(output) is bytes and output == canonical(fragment)
    assert mapper(inputs, supplied_after) == output
    assert inputs == old


def test_unchanged_row_does_not_emit_replacement(inputs):
    assert mapper(inputs, inputs["before_bytes"]) is None
    reformatted = json.dumps(json.loads(inputs["before_bytes"])).encode() + b"\n"
    assert mapper(inputs, reformatted) is None


def test_supported_undesired_observation_preserves_actual_quantity(
    inputs, supplied_after
):
    observed = canonical(dict(json.loads(supplied_after), quantity=3)) + b"\n"
    output = json.loads(mapper(inputs, observed))
    record = output["records"]["entities"][0]
    assert record["properties"]["ordered_quantity"] == 3
    assert inputs["goal"]["quantity"] == inputs["operator"]["requested_quantity"] == 2
    assert output["sources"][0]["sha256"] == digest(observed)
    assert (
        output["supersessions"][0]["supersedes_record_id"]
        == "supplier-order-state:B:e4"
    )
    assert model(inputs) == supplied_after


def test_action_strategy_rejects_mappable_but_undesired_prediction(
    inputs, supplied_after
):
    from research.semantic_reentry_external_design.supplier_reentry import (
        ReentryRefusal,
        SupplierActionStrategy,
    )

    prediction = canonical(dict(json.loads(supplied_after), quantity=3)) + b"\n"
    assert mapper(inputs, prediction) is not None
    with pytest.raises(ReentryRefusal) as caught:
        SupplierActionStrategy().payload(
            before_bytes=inputs["before_bytes"],
            prediction=prediction,
            source_sha256=inputs["source_sha256"],
            goal=inputs["goal"],
            operator=inputs["operator"],
            mapping=inputs["mapping"],
            logical_source_id=inputs["source_id"],
        )
    assert caught.value.reason == "MODEL_DISAGREEMENT"


def test_source_level_satisfaction_is_noop_but_checks_pin_first(inputs, supplied_after):
    inputs["before_bytes"] = supplied_after
    refuses("STALE_SOURCE", model, inputs)
    refuses("STALE_SOURCE", mapper, inputs, supplied_after)
    inputs["source_sha256"] = digest(supplied_after)
    assert model(inputs) is None
    assert mapper(inputs, supplied_after) is None


def test_semantically_identical_prestate_bytes_do_not_satisfy_exact_pin(inputs):
    inputs["before_bytes"] = json.dumps(json.loads(inputs["before_bytes"])).encode()
    refuses("STALE_SOURCE", model, inputs)


@pytest.mark.parametrize(
    "observed",
    [
        None,
        {},
        bytearray(b"{}"),
        b"",
        b"[]",
        b"null",
        b"\xff",
        b"{",
        b'{"event_id":"e4","event_id":"e4","supplier_order_id":"B","product_code":"Y","quantity":1}',
        b'{"event_id":"e4","supplier_order_id":"B","product_code":"Y","quantity":NaN}',
        '{"event_id":"e4","supplier_order_id":"B","product_code":"Y","quantity":1}'.encode(
            "utf-16"
        ),
        b'{"event_id":"\\ud800","supplier_order_id":"B","product_code":"Y","quantity":1}',
        b'{\n"event_id":"e4","supplier_order_id":"B","product_code":"Y","quantity":1}',
    ],
)
def test_bad_bytes_never_become_source_evidence(inputs, observed):
    refuses("MALFORMED_INPUT", mapper, inputs, observed)


@pytest.mark.parametrize("field", sorted(FIELDS))
@pytest.mark.parametrize("side", ["before", "observed"])
def test_every_required_source_field_is_enforced(inputs, supplied_after, field, side):
    row = json.loads(inputs["before_bytes"] if side == "before" else supplied_after)
    del row[field]
    if side == "before":
        inputs["before_bytes"] = canonical(row)
        inputs["source_sha256"] = digest(inputs["before_bytes"])
        refuses("MALFORMED_INPUT", model, inputs)
    else:
        refuses("MALFORMED_INPUT", mapper, inputs, canonical(row))


@pytest.mark.parametrize(
    "update",
    [
        {"quantity": True},
        {"quantity": "2"},
        {"quantity": 2.0},
        {"quantity": None},
        {"event_id": ""},
        {"supplier_order_id": None},
        {"product_code": ""},
        {"extra": "ignored?"},
        {"execution_status": "SUCCEEDED"},
        {"execution_status": "FAILED"},
    ],
)
def test_mistyped_or_undeclared_source_semantics_refuse(inputs, supplied_after, update):
    row = json.loads(supplied_after)
    row.update(update)
    refuses("MALFORMED_INPUT", mapper, inputs, canonical(row))


@pytest.mark.parametrize("side", ["before", "observed"])
def test_multiple_eligible_rows_refuse_without_implicit_selection(
    inputs, supplied_after, side
):
    if side == "before":
        inputs["before_bytes"] *= 2
        inputs["source_sha256"] = digest(inputs["before_bytes"])
        refuses("AMBIGUOUS", model, inputs)
    else:
        refuses("AMBIGUOUS", mapper, inputs, supplied_after * 2)


@pytest.mark.parametrize(
    "update",
    [
        {"quantity": 4},
        {"quantity": 0},
        {"quantity": -1},
        {"quantity": 1},
        {"event_id": "e7"},
        {"event_id": "e4"},
        {"supplier_order_id": "other"},
        {"product_code": "X"},
    ],
)
def test_well_formed_but_unsupported_observation_refuses(
    inputs, supplied_after, update
):
    row = json.loads(supplied_after)
    row.update(update)
    refuses("UNSUPPORTED_CHANGE", mapper, inputs, canonical(row))


@pytest.mark.parametrize(
    "update",
    [
        {"quantity": 3},
        {"quantity": 0},
        {"product_code": "X"},
        {"supplier_order_id": "other"},
        {"event_id": "reentry-amendment-1"},
    ],
)
def test_model_does_not_fabricate_a_plan_for_ineligible_prestate(inputs, update):
    row = json.loads(inputs["before_bytes"])
    row.update(update)
    inputs["before_bytes"] = canonical(row)
    inputs["source_sha256"] = digest(inputs["before_bytes"])
    refuses("UNREALIZABLE", model, inputs)


@pytest.mark.parametrize(
    "section,key,value",
    [
        ("goal", "kind", "ViewDelta"),
        ("goal", "operator", "AT_LEAST"),
        ("goal", "quantity", 3),
        ("goal", "quantity", True),
        ("operator", "kind", "CREATE_SUPPLIER_ORDER"),
        ("operator", "expected_quantity", True),
        ("operator", "expected_quantity", 0),
        ("operator", "requested_quantity", 3),
        ("operator", "precondition", "BEST_EFFORT"),
        ("operator", "changed_fields", ["quantity"]),
        ("operator", "new_source_occurrence_id", ""),
        ("goal", "supplier_order_id", ""),
        ("goal", "product_code", None),
    ],
)
def test_unsupported_rule_never_silently_falls_back(
    inputs, supplied_after, section, key, value
):
    inputs[section][key] = value
    refuses("UNSUPPORTED_RULE", model, inputs)
    refuses("UNSUPPORTED_RULE", mapper, inputs, supplied_after)


@pytest.mark.parametrize("section", ["goal", "operator", "mapping"])
def test_every_rule_field_required_and_extra_fields_refused(
    inputs, supplied_after, section
):
    for field in [*inputs[section], "extra"]:
        changed = deepcopy(inputs)
        if field == "extra":
            changed[section][field] = "undeclared"
        else:
            del changed[section][field]
        refuses("UNSUPPORTED_RULE", mapper, changed, supplied_after)


@pytest.mark.parametrize(
    "update",
    [
        {"type": "SalesOrder"},
        {"valid_time_kind": "INSTANT"},
        {"replacement_record_id": "supplier-order-state:B:e4"},
        {"supersedes_record_id": "different"},
        {"initial_record_id": ""},
        {"fields": {"ordered_quantity": "quantity"}},
        {
            "fields": {
                "ordered_quantity": "event_id",
                "source_occurrence_id": "quantity",
                "supplier_order_id": "supplier_order_id",
                "product_code": "product_code",
            }
        },
    ],
)
def test_mapping_cannot_drop_fields_change_types_or_hide_supersession(
    inputs, supplied_after, update
):
    inputs["mapping"].update(update)
    refuses("UNSUPPORTED_RULE", mapper, inputs, supplied_after)


@pytest.mark.parametrize(
    "field,value",
    [
        ("source_id", ""),
        ("source_id", None),
        ("source_sha256", "bad"),
        ("source_sha256", None),
    ],
)
def test_missing_or_malformed_binding_has_no_default(
    inputs, supplied_after, field, value
):
    inputs[field] = value
    refuses("MALFORMED_INPUT", mapper, inputs, supplied_after)


def test_receipt_is_not_a_source_and_no_receipt_capability_is_accepted(inputs):
    for status in ["SUCCEEDED", "FAILED", "ATTEMPTED"]:
        refuses("MALFORMED_INPUT", mapper, inputs, canonical({"status": status}))
    with pytest.raises(TypeError):
        import_module(MODULE).map_observation(
            inputs["before_bytes"],
            **inputs,
            execution_status="SUCCEEDED",
        )


def test_runtime_has_no_oracle_io_import_or_mutation_capability(
    inputs, supplied_after, monkeypatch
):
    implementation = import_module(MODULE)
    tree = ast.parse(Path(implementation.__file__).read_bytes())
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in {"eval", "exec", "__import__", "open", "compile"}
    assert imports <= {"hashlib", "json"}
    original = deepcopy(inputs)

    def forbidden(*args, **kwargs):
        pytest.fail("pure supplier component attempted I/O")

    with monkeypatch.context() as guard:
        guard.setattr(builtins, "open", forbidden)
        guard.setattr(io, "open", forbidden)
        assert model(inputs) == supplied_after
        assert mapper(inputs, supplied_after) is not None
    assert inputs == original


def test_output_and_ordering_do_not_depend_on_mapping_dictionary_order(
    inputs, supplied_after
):
    first = mapper(inputs, supplied_after)
    inputs["mapping"]["fields"] = dict(
        reversed(list(inputs["mapping"]["fields"].items()))
    )
    assert mapper(inputs, supplied_after) == first


@pytest.mark.parametrize("character", ["\u0085", "\u2028", "\u2029"])
def test_utf8_string_characters_are_not_jsonl_row_delimiters(inputs, character):
    # Authored adversarial input, not an observation produced by the model.
    before = json.loads(inputs["before_bytes"])
    before["product_code"] += character
    inputs["goal"]["product_code"] = before["product_code"]
    inputs["before_bytes"] = canonical(before) + b"\n"
    inputs["source_sha256"] = digest(inputs["before_bytes"])
    supplied = (
        canonical({**before, "quantity": 2, "event_id": "reentry-amendment-1"}) + b"\n"
    )
    assert model(inputs) == supplied
    fragment = json.loads(mapper(inputs, supplied))
    assert (
        fragment["records"]["entities"][0]["properties"]["product_code"]
        == before["product_code"]
    )
