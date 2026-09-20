"""What the four adopted rules must be observed to do, and what binds them.

Written before ``rules.pl`` carried a single clause. Every fixture in the rule
section is synthetic: the record identities, the slot values and the retained
text are invented here and none of them is read from the selected reading. The
rules run through Core's own ``PrologVerifier`` over a staged candidate
subgraph, which is the executor the policy uses at admission.

The gate sections read the frozen outcome files rather than rerunning the two
gates, the way ``fault-injection-02/test_rerun.py`` does.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
        paper-v4/experiment-v4/content-rules-doc-02/test_content_rules_doc_02.py
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import pytest

import malleus
import malleus.compiler as api
import malleus.logic
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

# This cell's own modules and the census's, the way bridge-01, fault-injection-02
# and rule-census-01 reach theirs. The paper gate collects
# paper-v4/experiment-v4 as a directory and runs pytest from the repository
# root, so a bare import does not resolve.
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "paper-v4/experiment-v4/rule-census-01"))
sys.path.insert(0, str(ROOT / "paper-v4/experiment-v4/fault-injection-02"))
sys.path.insert(0, str(ROOT / "paper-v4/experiment-v4/fault-injection-01"))

import compare as fault_compare  # noqa: E402
import equivalence  # noqa: E402
import gate2  # noqa: E402
import run_faults  # noqa: E402
import normalise  # noqa: E402

PRODUCER = ROOT / "private/paper-v4-v4-run-23/producer"
PRIVATE = ROOT / "private/paper-v4-content-rules-doc-02"
CENSUS_OUTCOMES = ROOT / "paper-v4/experiment-v4/rule-census-01/outcomes.json"
SECOND_FAULT_CELL = ROOT / "paper-v4/experiment-v4/fault-injection-02/outcomes.json"
OUTCOMES = HERE / "outcomes.json"
FAULT_OUTCOMES = HERE / "fault-outcomes.json"
RESULTS = HERE / "RESULTS.md"
RULES = HERE / "rules.pl"

CORE_COMMIT = "d867c3ab"
# The paper gate pins this module to d89a0c47 and exports that commit into a
# temporary directory, so Core is bound by the bytes of the package that was
# imported rather than by the path it was imported from. The three values are
# rule-census-01's, which pins the same Core the same way. Moved on 2026-09-19
# from e7937b89917c8da7ee4a08acc22e99ad12b9985b, 52 modules
# sha256:d57f3cc9…b1355, under E-0436.
CORE_PIN = "d89a0c4718654249ad678eaff62e7b1daba30b6f"
CORE_MODULE_COUNT = 53
CORE_SOURCE_DIGEST = (
    "sha256:340196130e1820e9a4f9979223f40dcf6b8c1227d8805d812fd08ca529a3ed04"
)
FROZEN_EXPORT = (
    "sha256:0634e0696a34bc2cc736f84dbeadf6b65416ebcd9f84f0e67eeb11bb9a44a286"
)
RULE_IDS = {
    "NO_CONFLICTING_QUANTITY",
    "INTERVAL_SANITY",
    "NUMBER_IN_CITED_TEXT",
    "FORMULA_IN_SOURCE",
}
CLOSURE = (
    ("paper-v4-project", "work/ontology-attempt-01.yaml"),
    ("malleus", "inputs/malleus.yaml"),
    ("linkml:types", "inputs/linkml-types.yaml"),
    ("metrology", "inputs/metrology.yaml"),
    ("chronology", "inputs/chronology.yaml"),
    ("research", "inputs/research.yaml"),
)
SELECTED_READING = PRODUCER / "inputs/selected-reading.json"

LEAK_WINDOW = 60
PUBLIC_FILES = (
    "README.md",
    "RESULTS.md",
    "logic.yaml",
    "policy.json",
    "rules.pl",
    "admit.py",
    "gate1.py",
    "gate2.py",
    "equivalence.py",
    "test_content_rules_doc_02.py",
    "outcomes.json",
    "fault-outcomes.json",
)

SOURCE = "source:synthetic-doc-02"
LOCATOR = "assertion:synthetic:001"
OTHER_LOCATOR = "assertion:synthetic:002"
# Invented sentences. Neither is a sentence of the reading.
TEXT = (
    "The synthetic column yields a carbon  dioxide content of 40 units, "
    "five samples, CO 2 and a drift of ± 0.3 units."
)
OTHER_TEXT = "A second synthetic column states nothing about that column."


# ---------------------------------------------------------------------------
# The Core this cell measured against
# ---------------------------------------------------------------------------


def core_modules(commit: str) -> list[str]:
    """The ``.py`` files a ``git archive`` of that commit carries under Core.

    The set is asked of git rather than of the filesystem, because the two
    places this module runs hold different files: the gate's export carries the
    tracked tree and nothing else, and the working checkout carries that tree
    plus seven gitignored modules (``conditions``, ``evaluator``,
    ``llm_client``, ``runner``, ``session``, ``static_loader``, ``tools``).
    """

    listed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", commit, "--", "src/malleus"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.split()
    prefix = "src/malleus/"
    return sorted(
        name[len(prefix) :]
        for name in listed
        if name.startswith(prefix) and name.endswith(".py")
    )


def core_source_identity(package, modules: list[str]) -> tuple[int, str]:
    """Digest those modules of the imported package, by a declared method.

    Each module keyed by its path relative to the package root and valued by
    the SHA-256 of its bytes, serialised as canonical JSON and digested again.
    Path-independent, so an export and a checkout of the same Core give the
    same answer. This is ``rule-census-01/test_census.py``'s method, over the
    same set it digests.
    """

    root = Path(package.__file__).resolve().parent
    rows = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in modules
    }
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return len(rows), "sha256:" + hashlib.sha256(blob).hexdigest()


def test_the_imported_core_is_the_pinned_one_by_its_own_bytes():
    """Bind Core by identity, not by the path it happens to sit at.

    The gate pins this module to ``d89a0c47`` and exports that commit into a
    temporary directory, so an assertion on the import location refuses the
    gate's own run. The commit is not recoverable from the package bytes
    either: a ``git archive`` carries no commit metadata, no ``RUNTIME.md`` and
    no overseer head, which is the finding ``rule-census-01`` records. What the
    bytes do support is a digest over the modules that export carries, and that
    is what this asserts.

    **The set is the tracked one, on purpose.** Under the gate the import
    resolves to the export, 53 modules. Under this cell's own documented
    command it resolves to the working checkout, which holds those 53 and seven
    more that are gitignored, so digesting every ``.py`` file it finds would
    refuse the gate. Restricting to the modules
    ``git archive d89a0c47 -- src/malleus`` carries gives one value both paths
    produce, and it is the value ``rule-census-01`` pins.

    **The pin moved on 2026-09-19** from ``e7937b89`` to ``d89a0c47``, the
    sealed Core that carries the one-call atomic admission, under E-0436: when
    Core changes the paper's pin moves to it and the cells re-baseline on it.
    Old value 52 modules ``sha256:d57f3cc9…b1355``, new value 53 modules
    ``sha256:340196…3ed04``; it moved because Core's own bytes moved, with
    ``_contract_pipeline/admission.py`` added. Every measurement this cell
    holds was re-run on the new pin through the gate and did not move.

    **The pin and this cell's Core constant name different trees now.**
    ``CORE_COMMIT`` here is ``d867c3ab``, the merge that put the hardened Core
    on main and the commit the four adopted rules were measured at; it stays,
    because it is a fact about the measurement and RESULTS.md records it. The
    gate's pin names the Core the gate imports today.
    """

    modules = core_modules(CORE_PIN)
    root = Path(malleus.__file__).resolve().parent
    missing = [name for name in modules if not (root / name).exists()]
    assert missing == [], f"the imported Core is missing {missing}, from {root}"
    count, digest = core_source_identity(malleus, modules)
    assert (count, digest) == (CORE_MODULE_COUNT, CORE_SOURCE_DIGEST), (
        f"imported Core is not the pin {CORE_PIN}: "
        f"{count} modules, {digest}, from {root}"
    )


def test_the_fact_contract_is_version_three():
    assert malleus.logic.FACT_CONTRACT_VERSION == "3"


def test_the_private_directory_is_ignored_by_git():
    completed = subprocess.run(
        ["git", "check-ignore", "-q", str(PRIVATE)], cwd=ROOT, capture_output=True
    )
    assert completed.returncode == 0


# ---------------------------------------------------------------------------
# The declarations, against the compiled ontology
# ---------------------------------------------------------------------------


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


def facts_of(name: str, arity: int = 1) -> set:
    """Every ground fact of one predicate the pinned rule program declares."""

    pattern = re.compile(
        rf"^{name}\(" + ", ?".join([r"'([^']*)'"] * arity) + r"\)\.\s*$", re.MULTILINE
    )
    found = pattern.findall(RULES.read_text(encoding="utf-8"))
    return {
        item if arity > 1 else (item if isinstance(item, str) else item[0])
        for item in found
    }


def local(identifier: str) -> str:
    return identifier.rsplit("/", 1)[-1]


def ranges(view) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for type_name in view.type_names():
        for slot, constraint in view.effective_slots(type_name).items():
            found.setdefault(local(slot), set()).add(local(constraint.range_id))
    return found


def non_relation_slots(view) -> set[str]:
    relation = "https://malleus.dev/schema/Relation"
    found: set[str] = set()
    for type_name in view.type_names():
        if type_name == relation or view.is_subtype_of(type_name, relation):
            continue
        found |= {local(slot) for slot in view.effective_slots(type_name)}
    return found


def test_the_numeric_slots_are_the_contracts_float_and_integer_ranges(view):
    declared = {
        slot for slot, found in ranges(view).items() if found & {"Float", "Integer"}
    }
    assert facts_of("numeric_slot") == declared


def test_the_subject_slot_is_the_contracts_entity_range_outside_relations(view):
    inside = non_relation_slots(view)
    declared = {
        slot
        for slot, found in ranges(view).items()
        if "Entity" in found and slot in inside
    }
    assert facts_of("subject_slot") == declared
    assert facts_of("subject_slot") == {"subject"}


def test_every_declared_qualifier_is_a_slot_the_contract_declares(view):
    declared = ranges(view)
    qualifiers = facts_of("qualifier")
    assert qualifiers, "the qualifier list is empty"
    assert "assertion_modality" in qualifiers
    for slot in qualifiers:
        assert slot in declared, slot
        assert not declared[slot] & {"Float", "Integer"}, slot


def test_every_formula_slot_is_declared_string(view):
    declared = ranges(view)
    formula = facts_of("formula_slot")
    assert formula == {"analyte", "numerator_kind", "denominator_kind"}
    for slot in formula:
        assert declared[slot] == {"String"}, slot


def test_every_quantity_identity_is_string_and_every_quantity_value_is_numeric(view):
    declared = ranges(view)
    numeric = facts_of("numeric_slot")
    identities = facts_of("quantity_identity", 2)
    values = facts_of("quantity_value", 2)
    assert {family for family, _ in identities} == {family for family, _ in values}
    for _, slot in identities:
        assert declared[slot] == {"String"}, slot
        assert slot not in facts_of("qualifier"), slot
    for _, slot in values:
        assert slot in numeric, slot


def test_the_interval_slots_are_declared_numeric(view):
    numeric = facts_of("numeric_slot")
    for lower, upper in facts_of("bound_pair", 2):
        assert lower in numeric and upper in numeric
    for slot in facts_of("non_negative_slot"):
        assert slot in numeric, slot


def test_the_declaration_block_points_at_the_roadmap_items():
    source = RULES.read_text(encoding="utf-8")
    assert "ROADMAP.md" in source
    assert "E2" in source and "E3" in source


# ---------------------------------------------------------------------------
# The contract and the policy
# ---------------------------------------------------------------------------


def test_the_contract_declares_the_four_rules_at_fact_contract_version_three(contract):
    assert contract.fact_contract_version == "3"
    assert set(contract.rule_ids) == RULE_IDS


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


# ---------------------------------------------------------------------------
# The normalisation and the number grammar, against the census's own Python
# ---------------------------------------------------------------------------


def census_probe_strings() -> set[str]:
    """Every string the census's own suite hands to its normaliser."""

    module = ast.parse(
        (ROOT / "paper-v4/experiment-v4/rule-census-01/test_normalise.py").read_text(
            encoding="utf-8"
        )
    )
    wanted = {"normalise", "numbers", "numbers_in", "contains"}
    found: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.Call):
            continue
        name = (
            node.func.attr
            if isinstance(node.func, ast.Attribute)
            else getattr(node.func, "id", "")
        )
        if name not in wanted:
            continue
        arguments = node.args[1:] if name == "contains" else node.args[:1]
        for argument in arguments:
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                found.add(argument.value)
    return found


def test_the_fixture_table_carries_every_string_the_census_suite_probes():
    texts = set(equivalence.fixture_texts().values())
    missing = sorted(
        text
        for text in census_probe_strings()
        if text not in texts and not any(text in item for item in texts)
    )
    assert missing == [], missing


def test_the_fixture_table_carries_the_bare_plus_or_minus_cases():
    assert set(equivalence.EXPECTED_EXTRA) <= set(equivalence.fixture_texts())
    assert len(equivalence.EXPECTED_EXTRA) >= 5


@pytest.fixture(scope="module")
def equivalence_rows():
    return equivalence.compare(equivalence.fixture_texts())


def test_the_two_implementations_agree_on_every_fixture(equivalence_rows):
    disagreeing = [row["label"] for row in equivalence_rows if not row["agrees"]]
    assert disagreeing == [], disagreeing


def test_the_bare_plus_or_minus_is_the_only_declared_difference(equivalence_rows):
    differing = {row["label"] for row in equivalence_rows if row["only_in_prolog"]}
    assert differing == set(equivalence.EXPECTED_EXTRA)
    assert all(not row["only_in_python"] for row in equivalence_rows)


def test_the_census_python_does_not_read_a_bare_plus_or_minus():
    """The production this cell adds is absent from the implementation it copies."""

    from decimal import Decimal

    parsed = normalise.numbers_in(
        "a perturbation of ± 0.3 km/s", profile=normalise.GLUED, attached=True
    )
    assert Decimal("0.3") in parsed
    assert Decimal("-0.3") not in parsed


# ---------------------------------------------------------------------------
# The four rules, over synthetic candidates, through Core's own executor
# ---------------------------------------------------------------------------


def _check(view, contract, writes, *, texts=((LOCATOR, TEXT),), derivations=()):
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


def _violated(result) -> set[str]:
    return {violation.rule_id for violation in result.violations}


def _witnesses(result, rule_id: str) -> set[str]:
    return {
        record_id
        for violation in result.violations
        if violation.rule_id == rule_id
        for record_id in violation.witness_record_ids
    }


def _codes(result, rule_id: str) -> set[str]:
    return {
        violation.violation_code
        for violation in result.violations
        if violation.rule_id == rule_id
    }


def _located(extra: dict, locator: str = LOCATOR) -> dict:
    base = {
        "assertion_locator": locator,
        "statement_sha256": "sha256:" + "0" * 64,
    }
    base.update(extra)
    return base


def _observation(record_id: str, properties: dict) -> ProposedOperation:
    return ProposedOperation(
        "CREATE_ENTITY", "GeochemicalObservation", record_id, properties
    )


FEATURE = ProposedOperation(
    "CREATE_ENTITY", "GeologicFeature", "syn:feature", {"name": "the synthetic column"}
)


def _quantified(record_id: str, extra: dict) -> ProposedOperation:
    properties = _located(
        {
            "name": "the synthetic column",
            "subject": "syn:feature",
            "quantity_kind": "the synthetic column",
        }
    )
    properties.update(extra)
    return ProposedOperation(
        "CREATE_ENTITY", "GeophysicalObservation", record_id, properties
    )


# (a) NO_CONFLICTING_QUANTITY


def test_rule_a_refuses_two_live_values_for_one_subject_and_quantity_kind(
    view, contract
):
    result = _check(
        view,
        contract,
        [
            FEATURE,
            _quantified("syn:q:a", {"value_lower": 40.0, "value_upper": 40.0}),
            _quantified("syn:q:b", {"value_lower": 5.0, "value_upper": 5.0}),
        ],
    )
    assert _witnesses(result, "NO_CONFLICTING_QUANTITY") == {"syn:q:a", "syn:q:b"}
    assert _codes(result, "NO_CONFLICTING_QUANTITY") == {"QUANTITY_DISAGREEMENT"}


def test_rule_a_admits_the_same_value_stated_twice(view, contract):
    result = _check(
        view,
        contract,
        [
            FEATURE,
            _quantified("syn:q:a", {"value_lower": 40.0, "value_upper": 40.0}),
            _quantified("syn:q:b", {"value_lower": 40.0, "value_upper": 40.0}),
        ],
    )
    assert "NO_CONFLICTING_QUANTITY" not in _violated(result)


def test_rule_a_admits_two_values_whose_assertion_modality_differs(view, contract):
    """The census's first rule defect, removed by the qualifier Luis added."""

    result = _check(
        view,
        contract,
        [
            FEATURE,
            _quantified(
                "syn:q:a",
                {
                    "value_lower": 40.0,
                    "value_upper": 40.0,
                    "assertion_modality": "STATED",
                },
            ),
            _quantified(
                "syn:q:b",
                {
                    "value_lower": 5.0,
                    "value_upper": 5.0,
                    "assertion_modality": "HYPOTHESISED",
                },
            ),
        ],
    )
    assert "NO_CONFLICTING_QUANTITY" not in _violated(result)


def test_rule_a_still_refuses_two_values_of_one_modality(view, contract):
    result = _check(
        view,
        contract,
        [
            FEATURE,
            _quantified(
                "syn:q:a",
                {
                    "value_lower": 40.0,
                    "value_upper": 40.0,
                    "assertion_modality": "STATED",
                },
            ),
            _quantified(
                "syn:q:b",
                {
                    "value_lower": 5.0,
                    "value_upper": 5.0,
                    "assertion_modality": "STATED",
                },
            ),
        ],
    )
    assert _witnesses(result, "NO_CONFLICTING_QUANTITY") == {"syn:q:a", "syn:q:b"}


def test_rule_a_admits_two_values_whose_qualifiers_disagree(view, contract):
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
                _quantified("syn:q:a", {"value_lower": 40.0, slot: left}),
                _quantified("syn:q:b", {"value_lower": 5.0, slot: right}),
            ],
        )
        assert "NO_CONFLICTING_QUANTITY" not in _violated(result), slot


def test_rule_a_admits_two_values_for_different_subjects(view, contract):
    second = ProposedOperation(
        "CREATE_ENTITY",
        "GeologicFeature",
        "syn:feature:2",
        {"name": "the synthetic column"},
    )
    result = _check(
        view,
        contract,
        [
            FEATURE,
            second,
            _quantified("syn:q:a", {"value_lower": 40.0}),
            _quantified("syn:q:b", {"value_lower": 5.0, "subject": "syn:feature:2"}),
        ],
    )
    assert "NO_CONFLICTING_QUANTITY" not in _violated(result)


def test_rule_a_reads_the_count_and_ratio_families_too(view, contract):
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
                        "count": 5,
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
                        "count": 40,
                    }
                ),
            ),
        ],
    )
    assert _witnesses(counted, "NO_CONFLICTING_QUANTITY") == {"syn:c:a", "syn:c:b"}
    assert _codes(counted, "NO_CONFLICTING_QUANTITY") == {"COUNT_DISAGREEMENT"}
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
                        "numerator_kind": "CO2",
                        "denominator_kind": "CO2",
                        "ratio_value": 40.0,
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
                        "numerator_kind": "CO2",
                        "denominator_kind": "CO2",
                        "ratio_value": 5.0,
                    }
                ),
            ),
        ],
    )
    assert _witnesses(ratios, "NO_CONFLICTING_QUANTITY") == {"syn:r:a", "syn:r:b"}
    assert _codes(ratios, "NO_CONFLICTING_QUANTITY") == {"RATIO_DISAGREEMENT"}


# (b) INTERVAL_SANITY


def test_rule_b_refuses_an_inverted_pair_of_bounds(view, contract):
    result = _check(
        view,
        contract,
        [
            _observation(
                "syn:i:inverted", _located({"value_lower": 40.0, "value_upper": 5.0})
            )
        ],
    )
    assert _witnesses(result, "INTERVAL_SANITY") == {"syn:i:inverted"}
    assert _codes(result, "INTERVAL_SANITY") == {"BOUNDS_INVERTED"}


def test_rule_b_admits_equal_bounds_and_an_absent_bound(view, contract):
    result = _check(
        view,
        contract,
        [
            _observation(
                "syn:i:equal", _located({"value_lower": 40.0, "value_upper": 40.0})
            ),
            _observation("syn:i:open", _located({"value_lower": 40.0})),
        ],
    )
    assert "INTERVAL_SANITY" not in _violated(result)


def test_rule_b_refuses_a_negative_magnitude_in_each_declared_slot(view, contract):
    counted = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "CountObservation",
                "syn:i:count",
                _located({"count": -5, "count_scope": "the synthetic column"}),
            )
        ],
    )
    assert _witnesses(counted, "INTERVAL_SANITY") == {"syn:i:count"}
    assert _codes(counted, "INTERVAL_SANITY") == {"NEGATIVE_VALUE/count"}
    uncertain = _check(
        view,
        contract,
        [_observation("syn:i:uncertainty", _located({"uncertainty": -0.3}))],
    )
    assert _codes(uncertain, "INTERVAL_SANITY") == {"NEGATIVE_VALUE/uncertainty"}
    ratio = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "ElementRatio",
                "syn:i:ratio",
                _located({"ratio_value": -5.0}),
            )
        ],
    )
    assert _codes(ratio, "INTERVAL_SANITY") == {"NEGATIVE_VALUE/ratio_value"}


def test_rule_b_reads_a_record_that_cites_nothing(view, contract):
    """Interval sanity reads no text, so a record with no locator is in reach."""

    result = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "QuantityValue",
                "syn:i:unlocated",
                {"value_lower": 40.0, "value_upper": 5.0},
            )
        ],
    )
    assert _witnesses(result, "INTERVAL_SANITY") == {"syn:i:unlocated"}


# (c) NUMBER_IN_CITED_TEXT


def test_rule_c_refuses_a_number_the_cited_text_does_not_state(view, contract):
    result = _check(
        view,
        contract,
        [_observation("syn:n:absent", _located({"value_lower": 900001.0}))],
    )
    assert _witnesses(result, "NUMBER_IN_CITED_TEXT") == {"syn:n:absent"}
    assert _codes(result, "NUMBER_IN_CITED_TEXT") == {
        "NUMBER_NOT_IN_CITED_TEXT/value_lower"
    }


def test_rule_c_admits_an_integral_float_the_sentence_writes_without_its_zero(
    view, contract
):
    result = _check(
        view,
        contract,
        [_observation("syn:n:integral", _located({"value_lower": 40.0}))],
    )
    assert "NUMBER_IN_CITED_TEXT" not in _violated(result)


def test_rule_c_admits_a_count_the_sentence_states_as_a_word(view, contract):
    result = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "CountObservation",
                "syn:n:word",
                _located({"count": 5, "count_scope": "the synthetic column"}),
            )
        ],
    )
    assert "NUMBER_IN_CITED_TEXT" not in _violated(result)


def test_rule_c_reads_a_bare_plus_or_minus_as_a_two_ended_interval(view, contract):
    """The census's second rule defect, removed by the production Luis added."""

    result = _check(
        view,
        contract,
        [
            _observation(
                "syn:n:perturbation",
                _located({"value_lower": -0.3, "value_upper": 0.3}),
            )
        ],
    )
    assert "NUMBER_IN_CITED_TEXT" not in _violated(result)


def test_rule_c_reads_the_locator_the_record_cites_and_not_another(view, contract):
    result = _check(
        view,
        contract,
        [
            _observation(
                "syn:n:elsewhere", _located({"value_lower": 40.0}, OTHER_LOCATOR)
            )
        ],
        texts=((LOCATOR, TEXT), (OTHER_LOCATOR, OTHER_TEXT)),
    )
    assert _witnesses(result, "NUMBER_IN_CITED_TEXT") == {"syn:n:elsewhere"}


def test_rule_c_ignores_a_record_that_cites_no_assertion(view, contract):
    result = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "QuantityValue",
                "syn:n:unlocated",
                {"value_lower": 900001.0, "value_upper": 900002.0},
            )
        ],
    )
    assert "NUMBER_IN_CITED_TEXT" not in _violated(result)


# (e) FORMULA_IN_SOURCE


def test_rule_e_refuses_a_formula_the_cited_text_does_not_carry(view, contract):
    result = _check(
        view,
        contract,
        [_observation("syn:f:absent", _located({"analyte": "FAULT-SYNTHETIC"}))],
    )
    assert _witnesses(result, "FORMULA_IN_SOURCE") == {"syn:f:absent"}
    assert _codes(result, "FORMULA_IN_SOURCE") == {"FORMULA_NOT_IN_CITED_TEXT/analyte"}


def test_rule_e_admits_a_formula_whose_subscript_the_text_layer_spaces_out(
    view, contract
):
    """The gluing step of the declared normalisation, which is why it is there."""

    result = _check(
        view,
        contract,
        [_observation("syn:f:glued", _located({"analyte": "CO2"}))],
    )
    assert "FORMULA_IN_SOURCE" not in _violated(result)


def test_rule_e_reads_both_ratio_kinds(view, contract):
    result = _check(
        view,
        contract,
        [
            ProposedOperation(
                "CREATE_ENTITY",
                "ElementRatio",
                "syn:f:ratio",
                _located(
                    {"numerator_kind": "CO2", "denominator_kind": "FAULT-SYNTHETIC"}
                ),
            )
        ],
    )
    assert _codes(result, "FORMULA_IN_SOURCE") == {
        "FORMULA_NOT_IN_CITED_TEXT/denominator_kind"
    }


def test_the_rules_read_no_slot_outside_their_declarations(view, contract):
    """A producer-authored label refuses nothing, which is the census's finding."""

    result = _check(
        view,
        contract,
        [
            _observation(
                "syn:labels",
                _located(
                    {
                        "name": "a name no sentence carries",
                        "description": "a description no sentence carries",
                        "quantity_kind": "a quantity kind no sentence carries",
                        "unit": "a unit no sentence carries",
                        "estimation_proxy": "a proxy no sentence carries",
                    }
                ),
            )
        ],
    )
    assert _violated(result) == set()


# ---------------------------------------------------------------------------
# Gate 1, the honest population
# ---------------------------------------------------------------------------


def outcomes() -> dict:
    if not OUTCOMES.exists():
        pytest.fail("outcomes.json is not written yet")
    return json.loads(OUTCOMES.read_bytes())


def test_gate_one_admits_the_honest_population():
    honest = outcomes()["gate_1"]["honest"]
    assert honest["outcome"] == "ADMITTED"
    assert honest["check_outcome"] == "SATISFIED"
    assert honest["violated_rule_ids"] == []
    assert set(honest["checked_rule_ids"]) == RULE_IDS


def test_every_gate_one_refusal_is_classified_with_rule_defects_at_zero():
    gate = outcomes()["gate_1"]
    classes = [row["class"] for row in gate["honest"]["refused"]]
    assert "UNDECIDED" not in classes
    assert classes.count("RULE_DEFECT") == 0
    assert gate["acceptance"]["rule_defects"] == 0
    assert gate["acceptance"]["unclassified"] == 0


def test_the_honest_export_is_byte_identical_to_run_23s_frozen_export():
    gate = outcomes()["gate_1"]
    assert gate["honest"]["export_records_sha256"] == FROZEN_EXPORT
    assert gate["honest"]["export_equals_frozen_run_23"] is True


def test_the_controls_receipt_moves_only_at_the_producer_digest_leaves():
    control = outcomes()["gate_1"]["control"]
    assert control["export_records_sha256"] == FROZEN_EXPORT
    assert control["contract_differences_from_frozen_run_23"] == [
        "/evidence/producer/sha256",
        "/evidence_sha256",
    ]


def test_the_policied_receipt_differs_by_the_policy_it_selects():
    """The domain contract does not move; the normative profile does."""

    gate = outcomes()["gate_1"]
    assert (
        gate["honest"]["replay_receipt_sha256"]
        != gate["control"]["replay_receipt_sha256"]
    )
    assert gate["honest"]["contract_differences_from_the_control"] == []
    partial = gate["honest"]["partial_contract_differences_from_the_control"]
    assert partial, "a policied history must carry a different normative profile"
    assert all(path.startswith("/normative_profile") for path in partial), partial


def test_the_corpus_disagrees_only_by_the_declared_production():
    """Every sentence and every string value of run-23, through both."""

    block = outcomes()["gate_1"]["equivalence"]
    assert block["fixtures_disagreeing"] == []
    assert block["corpus_strings"] > 2000
    assert block["corpus_normalisation_disagreeing"] == 0
    assert block["corpus_disagreeing_otherwise"] == 0
    assert (
        block["corpus_disagreeing_count"]
        == (block["corpus_disagreeing_by_the_declared_production"])
    )


def test_the_census_oracle_rows_are_reproduced():
    """The four adopted candidates, as rule-census-01 measured them on run-23."""

    census = json.loads(CENSUS_OUTCOMES.read_bytes())
    document = census["populations"]["run-23"]
    assert (
        document["a_no_conflicting_quantity"]["with_assertion_modality"]["violations"]
        == 0
    )
    assert document["b_interval_sanity"]["refusals"] == 0
    assert document["e_formula_in_source"]["CITED/GLUED"]["refusals"] == 0
    numbers = document["c_number_in_cited_text"]["CITED/GLUED_ATTACHED"]
    assert numbers["refusals"] == 1
    expected = {
        row["record_id"]
        for row in census["refusals"]
        if row["candidate"] == "NUMBER_IN_CITED_TEXT"
        and row["population"] == "run-23"
        and row["reading"] == "GLUED_ATTACHED"
        and row["scope"] == "CITED"
    }
    observed = {
        record
        for row in outcomes()["gate_1"]["honest"]["refused"]
        for record in row["record_ids"]
    }
    assert observed == set()
    assert outcomes()["gate_1"]["census_oracle"]["reproduced"] is True
    assert outcomes()["gate_1"]["census_oracle"]["removed_by_the_added_production"] == (
        sorted(expected)
    )


# ---------------------------------------------------------------------------
# Gate 2, the 55 faults with the rules on
# ---------------------------------------------------------------------------


def fault_outcomes() -> dict:
    if not FAULT_OUTCOMES.exists():
        pytest.fail("fault-outcomes.json is not written yet")
    return json.loads(FAULT_OUTCOMES.read_bytes())


def test_gate_two_is_the_same_catalogue_as_the_first_cell():
    before = json.loads(SECOND_FAULT_CELL.read_bytes())
    after = fault_outcomes()
    assert [trial["trial_id"] for trial in after["trials"]] == [
        trial["trial_id"] for trial in before["trials"]
    ]
    assert [trial["population_sha256"] for trial in after["trials"]] == [
        trial["population_sha256"] for trial in before["trials"]
    ]
    assert len(after["trials"]) == 55


def test_gate_two_ran_the_policy_and_not_the_structural_runner_alone():
    after = fault_outcomes()
    assert after["runner"].endswith("content-rules-doc-02/admit.py")


def test_the_first_cells_default_coordinate_did_not_move():
    """The runner is an argument; its default is run-23's own, as before."""

    minimal = ["--producer", "p", "--private", "q"]
    default = run_faults.build_parser().parse_args(minimal)
    assert default.runner == run_faults.RUNNER
    assert default.core_commit == run_faults.CORE_COMMIT
    assert default.core_repo == run_faults.CORE_REPOSITORY
    assert default.outcomes is None
    chosen = run_faults.build_parser().parse_args(
        minimal + ["--runner", "/elsewhere/admit.py"]
    )
    assert str(chosen.runner) == "/elsewhere/admit.py"


def test_the_first_cells_frozen_record_is_untouched():
    """fault-injection-01/outcomes.json still digests to what its note states."""

    path = ROOT / "paper-v4/experiment-v4/fault-injection-01/outcomes.json"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == (
        "7b7dd161a969f099af5f28f139e74f98198081b73185173dae84b2a74429adb9"
    )


def test_the_diagnostic_still_reads_run_23s_own_stderr():
    """The runner prefix became a group; what it captures did not change."""

    parsed = run_faults.diagnostic(
        "run-23: KnowledgeChangeRefusal: DIGEST_MISMATCH: record x names y"
    )
    assert parsed == {
        "error": "KnowledgeChangeRefusal",
        "reason": "DIGEST_MISMATCH",
        "detail": "record x names y",
    }
    mine = run_faults.diagnostic(
        "content-rules-doc-02: RunRefusal: CONTENT_RULE_VIOLATED: the selected policy"
    )
    assert mine["reason"] == "CONTENT_RULE_VIOLATED"


def test_no_refusal_in_gate_two_writes_an_admission_event():
    refused = [
        trial for trial in fault_outcomes()["trials"] if trial["outcome"] == "REFUSED"
    ]
    assert refused
    for trial in refused:
        assert trial["ledger"]["admission_events"] == [], trial["trial_id"]


def test_the_side_by_side_table_in_results_is_the_one_gate2_renders():
    before = json.loads(SECOND_FAULT_CELL.read_bytes())
    after = fault_outcomes()
    rendered = gate2.markdown(before, after)
    printed = [
        line.strip()
        for line in RESULTS.read_text(encoding="utf-8").splitlines()
        if line.startswith("| ")
    ]
    for line in rendered:
        if line.startswith("| # ") or line.startswith("| :--"):
            continue
        assert line in printed, line
    assert set(fault_compare.CONSTRUCTIONS) == {
        trial["fault_class"] for trial in after["trials"]
    }


def test_every_moved_trial_is_named_in_the_results_note():
    changed = fault_compare.moved(
        json.loads(SECOND_FAULT_CELL.read_bytes()), fault_outcomes()
    )
    assert changed["other"] == []
    text = RESULTS.read_text(encoding="utf-8")
    for direction in ("admitted_to_refused", "refused_to_admitted"):
        assert str(len(changed[direction])) in text, direction
        for entry in changed[direction]:
            assert entry["trial_id"] in text, entry["trial_id"]


# ---------------------------------------------------------------------------
# The leak rule and the note
# ---------------------------------------------------------------------------


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


def test_no_public_file_reproduces_the_reading():
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


def test_the_results_note_carries_the_coordinate_and_every_rule():
    text = RESULTS.read_text(encoding="utf-8")
    assert CORE_COMMIT in text
    for rule_id in sorted(RULE_IDS):
        assert rule_id in text, rule_id
