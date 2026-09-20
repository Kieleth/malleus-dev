"""What each of the three document-path rules must be observed to do.

Written before the rules were implemented. Every fixture here is synthetic:
the record identities, the slot values and the retained text are invented in
this file and none of them is read from the selected reading. The rules run
through Core's own ``PrologVerifier`` over a staged candidate subgraph, which
is the same executor the policy uses at admission.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
        paper-v4/experiment-v4/content-rules-doc-01/test_content_rules_doc.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import malleus.compiler as api
from malleus.kg import KnowledgeGraph
from malleus.logic import (
    GraphProvenance,
    LogicContract,
    RecordDerivation,
    RetainedSourceText,
)
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, stage_subgraph


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRODUCER = ROOT / "private/paper-v4-v4-run-23/producer"
SELECTED_READING = PRODUCER / "inputs/selected-reading.json"
RESULTS = HERE / "RESULTS.md"
CORE_COMMIT = "e7937b89"

CLOSURE = (
    ("paper-v4-project", "work/ontology-attempt-01.yaml"),
    ("malleus", "inputs/malleus.yaml"),
    ("linkml:types", "inputs/linkml-types.yaml"),
    ("metrology", "inputs/metrology.yaml"),
    ("chronology", "inputs/chronology.yaml"),
    ("research", "inputs/research.yaml"),
)

# Nothing public may reproduce the reading. Sixty normalized characters is the
# threshold every file this cell writes clears, as in every other v4 cell.
LEAK_WINDOW = 60
PUBLIC_FILES = (
    "README.md",
    "RESULTS.md",
    "logic.yaml",
    "policy.json",
    "rules.pl",
    "run_policy.py",
    "test_content_rules_doc.py",
    "outcomes.json",
)

SOURCE = "source:synthetic-doc-01"
LOCATOR = "assertion:synthetic:001"
OTHER_LOCATOR = "assertion:synthetic:002"
# Invented sentences. Neither is a sentence of the reading.
TEXT = "The synthetic column yields a carbon  dioxide content of 40 units."
OTHER_TEXT = "A second synthetic column states nothing about that column."


def _plain(text: str) -> str:
    return " ".join(text.split())


def _reading_windows(width: int) -> set[str]:
    reading = json.loads(SELECTED_READING.read_bytes())
    windows: set[str] = set()
    for page in reading["pages"]:
        for block in page["blocks"]:
            plain = _plain(block["text"])
            for start in range(0, max(1, len(plain) - width + 1)):
                piece = plain[start : start + width]
                if len(piece) == width:
                    windows.add(piece)
    return windows


@pytest.fixture(scope="module")
def view():
    assert PRODUCER.exists(), f"declared private fixture is missing: {PRODUCER}"
    sources = {locator: (PRODUCER / rel).read_bytes() for locator, rel in CLOSURE}
    return api.compile_linkml_contract(
        root_locator="paper-v4-project", sources=sources
    ).view


@pytest.fixture(scope="module")
def contract() -> LogicContract:
    return LogicContract.load(HERE / "logic.yaml")


def _check(view, contract, writes, *, derivations=(), texts=((LOCATOR, TEXT),)):
    """One Prolog check over a staged synthetic candidate, no history involved."""

    candidate = stage_subgraph(KnowledgeGraph(view), list(writes))
    provenance = GraphProvenance(
        derivations=tuple(
            RecordDerivation(record_id, path, SOURCE, locator)
            for record_id, path, locator in derivations
        ),
        source_texts=tuple(
            RetainedSourceText(SOURCE, locator, text) for locator, text in texts
        ),
    )
    return PrologVerifier(contract).verify_candidate_subgraph(
        candidate, provenance=provenance
    )


def _violated_rules(result) -> set[str]:
    return {violation.rule_id for violation in result.violations}


def _witnesses(result, rule_id: str) -> set[str]:
    return {
        record_id
        for violation in result.violations
        if violation.rule_id == rule_id
        for record_id in violation.witness_record_ids
    }


def _observation(record_id: str, properties: dict) -> ProposedOperation:
    return ProposedOperation(
        "CREATE_ENTITY", "GeochemicalObservation", record_id, properties
    )


def _located(extra: dict, locator: str = LOCATOR) -> dict:
    base = {
        "assertion_locator": locator,
        "statement_sha256": "sha256:" + "0" * 64,
        "assertion_modality": "MEASURED",
    }
    base.update(extra)
    return base


# ---------------------------------------------------------------------------
# Rule 1: VALUE_IN_CITED_TEXT
# ---------------------------------------------------------------------------


def test_rule_one_refuses_a_value_the_cited_text_does_not_contain(view, contract):
    result = _check(
        view,
        contract,
        [_observation("syn:absent", _located({"analyte": "SYNTHETIC-ABSENT-VALUE"}))],
    )
    assert "VALUE_IN_CITED_TEXT" in _violated_rules(result)
    assert _witnesses(result, "VALUE_IN_CITED_TEXT") == {"syn:absent"}


def test_rule_one_names_the_slot_it_refused_in_the_violation_code(view, contract):
    result = _check(
        view,
        contract,
        [_observation("syn:absent", _located({"analyte": "SYNTHETIC-ABSENT-VALUE"}))],
    )
    codes = {
        violation.violation_code
        for violation in result.violations
        if violation.rule_id == "VALUE_IN_CITED_TEXT"
    }
    assert codes == {"VALUE_NOT_IN_CITED_TEXT/analyte"}


def test_rule_one_admits_a_value_the_cited_text_contains(view, contract):
    result = _check(
        view,
        contract,
        [_observation("syn:present", _located({"analyte": "carbon  dioxide"}))],
    )
    assert _violated_rules(result) == set()


def test_rule_one_normalises_case_and_whitespace_and_nothing_else(view, contract):
    """``Carbon   Dioxide`` matches; a value differing by a comma does not."""

    folded = _check(
        view,
        contract,
        [_observation("syn:folded", _located({"analyte": "Carbon   Dioxide"}))],
    )
    assert _violated_rules(folded) == set()
    punctuated = _check(
        view,
        contract,
        [_observation("syn:punctuated", _located({"analyte": "carbon, dioxide"}))],
    )
    assert _witnesses(punctuated, "VALUE_IN_CITED_TEXT") == {"syn:punctuated"}


def test_rule_one_reads_integer_and_float_values(view, contract):
    """``40`` is in the text; ``40.0`` is the same number and is not."""

    integral = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "CountObservation",
                "syn:count",
                _located({"count": 40, "count_scope": "synthetic column"}),
            )
        ],
    )
    assert _violated_rules(integral) == set()
    rounded = _check(
        view,
        contract,
        [_observation("syn:float", _located({"value_lower": 40.0}))],
    )
    assert _witnesses(rounded, "VALUE_IN_CITED_TEXT") == {"syn:float"}


def test_rule_one_reads_the_locator_the_record_cites_not_another(view, contract):
    result = _check(
        view,
        contract,
        [
            _observation(
                "syn:elsewhere", _located({"analyte": "carbon dioxide"}, OTHER_LOCATOR)
            )
        ],
        texts=((LOCATOR, TEXT), (OTHER_LOCATOR, OTHER_TEXT)),
    )
    assert _witnesses(result, "VALUE_IN_CITED_TEXT") == {"syn:elsewhere"}


def test_rule_one_excludes_enumerations_record_references_and_coordinates(
    view, contract
):
    """None of the excluded slots occurs in the cited text, and none refuses."""

    writes = [
        ProposedOperation("CREATE_ENTITY", "GeologicFeature", "syn:feature", {}),
        _observation(
            "syn:excluded",
            _located(
                {
                    "analyte": "carbon dioxide",
                    "subject": "syn:feature",
                    "determination": "MODELLED",
                    "melt_stage": "PRIMARY_MELT",
                    "quantity_kind_class": "MassFraction",
                    "value_qualification": "APPROXIMATE",
                }
            ),
        ),
    ]
    result = _check(view, contract, writes)
    assert _violated_rules(result) == {"NO_EMPTY_RECORD"}
    assert _witnesses(result, "NO_EMPTY_RECORD") == {"syn:feature"}


def test_rule_one_ignores_a_record_that_cites_no_assertion(view, contract):
    result = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "Method",
                "syn:unlocated",
                {"name": "SYNTHETIC-ABSENT-VALUE"},
            )
        ],
    )
    assert _violated_rules(result) == set()


# ---------------------------------------------------------------------------
# Rule 2: NO_CONFLICTING_QUANTITY
# ---------------------------------------------------------------------------


def _quantified(record_id: str, extra: dict) -> ProposedOperation:
    properties = _located(
        {
            "name": "the synthetic column",
            "subject": "syn:feature",
            "quantity_kind": "the synthetic column",
            "unit": "the synthetic column",
        }
    )
    properties.update(extra)
    return ProposedOperation(
        "CREATE_ENTITY", "GeophysicalObservation", record_id, properties
    )


FEATURE = ProposedOperation(
    "CREATE_ENTITY", "GeologicFeature", "syn:feature", {"name": "the synthetic column"}
)


def test_rule_two_refuses_two_live_values_for_one_subject_and_quantity_kind(
    view, contract
):
    result = _check(
        view,
        contract,
        [
            FEATURE,
            _quantified("syn:q:a", {"value_lower": 1.0, "value_upper": 1.0}),
            _quantified("syn:q:b", {"value_lower": 2.0, "value_upper": 2.0}),
        ],
    )
    assert _witnesses(result, "NO_CONFLICTING_QUANTITY") == {"syn:q:a", "syn:q:b"}


def test_rule_two_admits_the_same_value_stated_twice(view, contract):
    result = _check(
        view,
        contract,
        [
            FEATURE,
            _quantified("syn:q:a", {"value_lower": 1.0, "value_upper": 1.0}),
            _quantified("syn:q:b", {"value_lower": 1.0, "value_upper": 1.0}),
        ],
    )
    assert "NO_CONFLICTING_QUANTITY" not in _violated_rules(result)


def test_rule_two_admits_two_values_whose_qualifiers_disagree(view, contract):
    """A different unit, determination or melt stage is a different quantity."""

    for slot, left, right in (
        ("unit", "the synthetic column", "a second synthetic column"),
        ("determination", "MEASURED", "MODELLED"),
        ("value_qualification", "EXACT", "APPROXIMATE"),
        ("depth_reference", "BELOW_SEAFLOOR", "BELOW_SEA_LEVEL"),
    ):
        result = _check(
            view,
            contract,
            [
                FEATURE,
                _quantified("syn:q:a", {"value_lower": 1.0, slot: left}),
                _quantified("syn:q:b", {"value_lower": 2.0, slot: right}),
            ],
        )
        assert "NO_CONFLICTING_QUANTITY" not in _violated_rules(result), slot


def test_rule_two_admits_two_values_a_qualifier_only_one_record_sets(view, contract):
    result = _check(
        view,
        contract,
        [
            FEATURE,
            _quantified("syn:q:a", {"value_lower": 1.0, "determination": "MEASURED"}),
            _quantified("syn:q:b", {"value_lower": 2.0}),
        ],
    )
    assert "NO_CONFLICTING_QUANTITY" not in _violated_rules(result)


def test_rule_two_admits_two_values_for_different_subjects(view, contract):
    second = ProposedOperation(
        "CREATE_ENTITY",
        "GeologicFeature",
        "syn:feature:2",
        {"name": "the synthetic column"},
    )
    left = _quantified("syn:q:a", {"value_lower": 1.0})
    right = _quantified("syn:q:b", {"value_lower": 2.0, "subject": "syn:feature:2"})
    result = _check(view, contract, [FEATURE, second, left, right])
    assert "NO_CONFLICTING_QUANTITY" not in _violated_rules(result)


def test_rule_two_reads_the_count_and_ratio_axes_too(view, contract):
    counted = _check(
        view,
        contract,
        [
            FEATURE,
            ProposedOperation(
                "CREATE_ENTITY",
                "CountObservation",
                "syn:c:a",
                _located(
                    {
                        "subject": "syn:feature",
                        "count_scope": "the synthetic column",
                        "count": 1,
                    }
                ),
            ),
            ProposedOperation(
                "CREATE_ENTITY",
                "CountObservation",
                "syn:c:b",
                _located(
                    {
                        "subject": "syn:feature",
                        "count_scope": "the synthetic column",
                        "count": 2,
                    }
                ),
            ),
        ],
    )
    assert _witnesses(counted, "NO_CONFLICTING_QUANTITY") == {"syn:c:a", "syn:c:b"}
    ratios = _check(
        view,
        contract,
        [
            FEATURE,
            ProposedOperation(
                "CREATE_ENTITY",
                "ElementRatio",
                "syn:r:a",
                _located(
                    {
                        "subject": "syn:feature",
                        "numerator_kind": "the synthetic column",
                        "denominator_kind": "a second synthetic column",
                        "ratio_value": 1.0,
                    }
                ),
            ),
            ProposedOperation(
                "CREATE_ENTITY",
                "ElementRatio",
                "syn:r:b",
                _located(
                    {
                        "subject": "syn:feature",
                        "numerator_kind": "the synthetic column",
                        "denominator_kind": "a second synthetic column",
                        "ratio_value": 2.0,
                    }
                ),
            ),
        ],
    )
    assert _witnesses(ratios, "NO_CONFLICTING_QUANTITY") == {"syn:r:a", "syn:r:b"}


# ---------------------------------------------------------------------------
# Rule 3: NO_EMPTY_RECORD
# ---------------------------------------------------------------------------


def test_rule_three_refuses_a_record_carrying_no_property(view, contract):
    result = _check(
        view, contract, [ProposedOperation("CREATE_ENTITY", "Method", "syn:empty", {})]
    )
    assert _witnesses(result, "NO_EMPTY_RECORD") == {"syn:empty"}


def test_rule_three_admits_a_record_carrying_one_property(view, contract):
    result = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY", "Method", "syn:named", {"name": "the synthetic column"}
            )
        ],
    )
    assert _violated_rules(result) == set()


def test_rule_three_admits_a_record_carrying_only_a_multivalued_slot(view, contract):
    result = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "Method",
                "syn:tagged",
                {"tags": ["the synthetic column"]},
            )
        ],
    )
    assert _violated_rules(result) == set()


# ---------------------------------------------------------------------------
# The layer itself
# ---------------------------------------------------------------------------


def test_the_contract_declares_the_three_rules_at_fact_contract_version_three(contract):
    assert contract.fact_contract_version == "3"
    assert set(contract.rule_ids) == {
        "VALUE_IN_CITED_TEXT",
        "NO_CONFLICTING_QUANTITY",
        "NO_EMPTY_RECORD",
    }


def test_the_policy_requires_this_exact_check_contract(contract):
    policy = api.PolicyProgram.from_bytes(
        json.dumps(
            json.loads((HERE / "policy.json").read_bytes()),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
    )
    assert policy.required_checks == ((contract.contract_id, contract.contract_hash),)
    outcomes = json.loads((HERE / "policy.json").read_bytes())["outcome_verdicts"]
    assert outcomes == {"SATISFIED": "ACCEPT", "UNKNOWN": "DEFER", "VIOLATED": "REJECT"}


def test_the_contract_pins_run_23s_compiled_ontology(view, contract):
    assert view.verifies(contract.ontology_hash)


def test_no_public_file_reproduces_the_reading() -> None:
    windows = _reading_windows(LEAK_WINDOW)
    for name in PUBLIC_FILES:
        path = HERE / name
        assert path.exists(), name
        plain = _plain(path.read_text(encoding="utf-8"))
        shared = [
            plain[start : start + LEAK_WINDOW]
            for start in range(0, max(1, len(plain) - LEAK_WINDOW + 1))
            if plain[start : start + LEAK_WINDOW] in windows
        ]
        assert shared == [], name


def test_the_results_note_carries_the_coordinate_and_every_rule() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert CORE_COMMIT in text
    for rule_id in (
        "VALUE_IN_CITED_TEXT",
        "NO_CONFLICTING_QUANTITY",
        "NO_EMPTY_RECORD",
    ):
        assert rule_id in text, rule_id
