"""P1 RED contract for the private neutral population-plan compiler."""

from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
import importlib
from pathlib import Path
from types import ModuleType

import pytest

import malleus
from malleus import KnowledgeGraph
from malleus._contract_pipeline.knowledge import KnowledgeOperation, KnowledgeValidTime
from tests.contract_compiler.pareto.test_domain_history_profile import (
    STATE_VERSION_PROFILE_DATA,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _admit_record_change,
    _anchor,
    _anchored_history,
    _event,
    _generic_compilation,
    _protocol_events,
    _record_change,
)
from tests.contract_compiler.pareto.test_protocol_machine import (
    _canonical,
    _effective,
)
from tests.contract_compiler.pareto.test_validated_contract import (
    ROOT,
    _binding,
    _compile_binding,
    _trusted_types,
)


MODULE = "malleus._contract_pipeline.population"
PLAN_GRAMMAR = "malleus.population-plan/private-v0"
PLAN_FIELDS = frozenset(
    {
        "adapter",
        "contract_identity",
        "derivations",
        "evidence",
        "gaps",
        "grammar",
        "history_profile",
        "plan_id",
        "records",
        "sources",
        "supersessions",
        "valid_time",
    }
)
P1_SYMBOLS = frozenset(
    {
        "PopulationBaseState",
        "PopulationPlanCompilation",
        "PopulationPlanRefusal",
        "PopulationPlanRefusalReason",
        "PopulationPlanStatus",
        "compile_population_plan",
    }
)
P2_SYMBOLS = frozenset(
    {
        "DomainHistoryProfile",
        "OBJECT_EVENT_PROFILE",
        "PopulationPreparation",
        "SOURCE_ASSERTION_PROFILE",
        "STATE_VERSION_PROFILE",
        "prepare_population_change",
    }
)
P1_REASONS = frozenset(
    {
        "ABSENT_PATH",
        "DANGLING_ENDPOINT",
        "DUPLICATE_RECORD_ID",
        "FAMILY_NOT_ADMITTED",
        "FIELDS_NOT_CLOSED",
        "IDENTITY_MISMATCH",
        "MALFORMED_EVIDENCE_REFERENCE",
        "MALFORMED_IDENTITY",
        "MALFORMED_PLAN",
        "MALFORMED_PROFILE_REFERENCE",
        "MALFORMED_SUPERSESSION",
        "SOURCES_REQUIRED",
        "SUPERSESSION_FORK",
        "SUPERSESSION_TYPE_MISMATCH",
        "SUPERSESSION_VALID_TIME_MISMATCH",
        "UNDERIVED_FIELD",
        "UNKNOWN_FAMILY",
        "UNKNOWN_GAP_KIND",
        "UNKNOWN_RECORD",
        "UNKNOWN_SUPERSESSION",
        "UNLISTED_SOURCE",
        "UNSUPPORTED_GRAMMAR",
        "UNSUPPORTED_VALID_TIME",
    }
)
PROFILE_BYTES = _canonical(STATE_VERSION_PROFILE_DATA)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _population() -> ModuleType:
    try:
        return importlib.import_module(MODULE)
    except ModuleNotFoundError as error:
        if error.name != MODULE:
            raise
        pytest.fail(
            "P1 production module malleus._contract_pipeline.population is absent",
            pytrace=False,
        )


@pytest.fixture(scope="module")
def contract_pair():
    compiled = _generic_compilation()
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    return compiled, partial


def _plan(
    contract_identity: str,
    *,
    source_identity: str | None = None,
    evidence_identity: str | None = None,
) -> dict[str, object]:
    source_identity = source_identity or _digest(b"neutral source\n")
    evidence_identity = evidence_identity or _digest(b"neutral evidence\n")
    return {
        "grammar": PLAN_GRAMMAR,
        "plan_id": "plan:neutral:1",
        "contract_identity": contract_identity,
        "history_profile": {
            "profile_id": "state-version",
            "sha256": _digest(PROFILE_BYTES),
        },
        "adapter": {"adapter_id": "neutral-row-adapter", "version": "0"},
        "sources": [{"source_id": "source-generic", "sha256": source_identity}],
        "evidence": [{"evidence_id": "evidence-generic", "sha256": evidence_identity}],
        "records": {
            "entities": [
                {
                    "type": "LeftObject",
                    "id": "left-1",
                    "properties": {"label": "left"},
                },
                {
                    "type": "RightObject",
                    "id": "right-1",
                    "properties": {"label": "right"},
                },
            ],
            "relations": [
                {
                    "type": "ObjectLink",
                    "id": "link:left-1:right-1",
                    "source_id": "left-1",
                    "target_id": "right-1",
                    "properties": {"relation_type": "LINKS"},
                }
            ],
        },
        "supersessions": [],
        "derivations": [
            {
                "record_id": "left-1",
                "path": ["properties", "label"],
                "source_id": "source-generic",
                "locator": "row:0:left",
            },
            {
                "record_id": "right-1",
                "path": ["properties", "label"],
                "source_id": "source-generic",
                "locator": "row:0:right",
            },
            {
                "record_id": "link:left-1:right-1",
                "path": ["properties", "relation_type"],
                "source_id": "source-generic",
                "locator": "row:0:kind",
            },
            {
                "record_id": "link:left-1:right-1",
                "path": ["source_id"],
                "source_id": "source-generic",
                "locator": "row:0:left",
            },
            {
                "record_id": "link:left-1:right-1",
                "path": ["target_id"],
                "source_id": "source-generic",
                "locator": "row:0:right",
            },
        ],
        "gaps": [],
        "valid_time": {"kind": "ORDER_ONLY", "value": "occurrence-1"},
    }


def _compile(plan: object, contract_pair, *, base_state=None):
    population = _population()
    compiled, partial = contract_pair
    if base_state is None:
        base_state = population.PopulationBaseState.empty()
    return population.compile_population_plan(
        plan,
        partial_contract=partial,
        contract_view=compiled.view,
        base_state=base_state,
    )


def _admit_operations(
    history,
    *,
    change_set_id: str,
    operations: tuple[KnowledgeOperation, ...],
    order: str,
    supersedes: tuple[str, ...] = (),
):
    return _admit_operations_at(
        history,
        change_set_id=change_set_id,
        operations=operations,
        valid_time=KnowledgeValidTime("ORDER_ONLY", order),
        supersedes=supersedes,
    )


def _admit_operations_at(
    history,
    *,
    change_set_id: str,
    operations: tuple[KnowledgeOperation, ...],
    valid_time: KnowledgeValidTime,
    supersedes: tuple[str, ...] = (),
):
    before = history.replay()
    change = history.compose_change_set(
        change_set_id=change_set_id,
        source_record_ids=("source-generic",),
        evidence_record_ids=("evidence-generic",),
        operations=operations,
        valid_time=valid_time,
        supersedes=supersedes,
    )
    return history.admit(
        change_set=change,
        machine_events=_protocol_events(
            change,
            before.machine_state.identity,
            identifier_suffix=f":{change_set_id}",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )


def _remove_derivation(
    plan: dict[str, object], record_id: str, path: list[str]
) -> None:
    plan["derivations"] = [
        derivation
        for derivation in plan["derivations"]
        if not (derivation["record_id"] == record_id and derivation["path"] == path)
    ]


def _single_left_base(tmp_path: Path, valid_time: KnowledgeValidTime):
    history, compiled, partial, _, _, _ = _anchored_history(tmp_path)
    replay = _admit_operations_at(
        history,
        change_set_id="change:left-old",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:left-old",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left-old",
                properties={"label": "old"},
                depends_on=(),
            ),
        ),
        valid_time=valid_time,
    )
    return history, compiled, partial, replay


def _superseded_left_base(tmp_path: Path):
    history, compiled, partial, _, _, _ = _anchored_history(tmp_path)
    _admit_operations(
        history,
        change_set_id="change:left-retired",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:left-retired",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left-retired",
                properties={"label": "retired"},
                depends_on=(),
            ),
        ),
        order="base-1",
    )
    replay = _admit_operations(
        history,
        change_set_id="change:left-current",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:left-current",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left-current",
                properties={"label": "current"},
                depends_on=(),
                supersedes_record_id="left-retired",
            ),
        ),
        order="base-2",
        supersedes=("change:left-retired",),
    )
    return history, compiled, partial, replay


def _single_replacement_plan(
    contract_identity: str,
    *,
    record_id: str,
    record_type: str,
    valid_time: KnowledgeValidTime,
) -> dict[str, object]:
    plan = _plan(contract_identity)
    plan["records"] = {
        "entities": [
            {
                "type": record_type,
                "id": record_id,
                "properties": {"label": "new"},
            }
        ],
        "relations": [],
    }
    plan["derivations"] = [
        {
            "record_id": record_id,
            "path": ["properties", "label"],
            "source_id": "source-generic",
            "locator": "row:1:label",
        }
    ]
    plan["supersessions"] = [
        {"record_id": record_id, "supersedes_record_id": "left-old"}
    ]
    plan["valid_time"] = {"kind": valid_time.kind, "value": valid_time.value}
    return plan


def _mutate(plan: dict[str, object], case: str) -> None:
    if case == "extra-root":
        plan["extra"] = True
    elif case == "missing-root":
        plan.pop("adapter")
    elif case == "grammar":
        plan["grammar"] = "malleus.population-plan/unknown"
    elif case == "contract-short":
        plan["contract_identity"] = "sha256:abc"
    elif case == "contract-nonhex":
        plan["contract_identity"] = "sha256:" + "z" * 64
    elif case == "contract-mismatch":
        plan["contract_identity"] = "sha256:" + "0" * 64
    elif case == "profile-fields":
        plan["history_profile"]["extra"] = True
    elif case == "profile-digest":
        plan["history_profile"]["sha256"] = "sha256:abc"
    elif case == "adapter-fields":
        plan["adapter"]["extra"] = True
    elif case == "adapter-missing":
        plan["adapter"].pop("adapter_id")
    elif case == "sources-empty":
        plan["sources"] = []
    elif case == "source-digest":
        plan["sources"][0]["sha256"] = "sha256:abc"
    elif case == "source-fields":
        plan["sources"][0]["extra"] = True
    elif case == "sources-duplicate":
        plan["sources"].append(deepcopy(plan["sources"][0]))
    elif case == "evidence-digest":
        plan["evidence"][0]["sha256"] = "sha256:abc"
    elif case == "evidence-fields":
        plan["evidence"][0]["extra"] = True
    elif case == "evidence-duplicate":
        plan["evidence"].append(deepcopy(plan["evidence"][0]))
    elif case == "evidence-generated-collision":
        plan["evidence"][0]["evidence_id"] = "profile:state-version"
    elif case == "unknown-family":
        plan["records"]["widgets"] = []
    elif case == "signals":
        plan["records"]["signals"] = [{"id": "signal-1"}]
    elif case == "events":
        plan["records"]["events"] = [{"id": "event-1"}]
    elif case == "records-shape":
        plan["records"] = []
    elif case == "duplicate-record":
        plan["records"]["relations"][0]["id"] = "left-1"
    elif case == "derivation-record":
        plan["derivations"][0]["record_id"] = "absent"
    elif case == "derivation-path":
        plan["derivations"][0]["path"] = ["properties", "absent"]
    elif case == "derivation-source":
        plan["derivations"][0]["source_id"] = "source:absent"
    elif case == "derivation-fields":
        plan["derivations"][0]["extra"] = True
    elif case == "derivation-path-shape":
        plan["derivations"][0]["path"] = "properties.label"
    elif case == "underived-property":
        _remove_derivation(plan, "left-1", ["properties", "label"])
    elif case == "underived-source":
        _remove_derivation(plan, "link:left-1:right-1", ["source_id"])
    elif case == "underived-target":
        _remove_derivation(plan, "link:left-1:right-1", ["target_id"])
    elif case == "supersession-record":
        plan["supersessions"] = [
            {"record_id": "absent", "supersedes_record_id": "left-old"}
        ]
    elif case == "supersession-blank":
        plan["supersessions"] = [{"record_id": "left-1", "supersedes_record_id": ""}]
    elif case == "supersession-duplicate":
        plan["supersessions"] = [
            {"record_id": "left-1", "supersedes_record_id": "left-old"},
            {"record_id": "left-1", "supersedes_record_id": "left-older"},
        ]
    elif case == "supersession-fields":
        plan["supersessions"] = [
            {
                "record_id": "left-1",
                "supersedes_record_id": "left-old",
                "extra": True,
            }
        ]
    elif case == "gap-kind":
        plan["gaps"] = [
            {
                "kind": "SHRUG",
                "statement": "not expressible",
                "source_id": "source-generic",
                "locator": "row:0",
            }
        ]
    elif case == "gap-source":
        plan["gaps"] = [
            {
                "kind": "TYPE_ABSENT",
                "statement": "not expressible",
                "source_id": "source:absent",
                "locator": "row:0",
            }
        ]
    elif case == "gap-fields":
        plan["gaps"] = [
            {
                "kind": "TYPE_ABSENT",
                "statement": "not expressible",
                "source_id": "source-generic",
                "locator": "row:0",
                "extra": True,
            }
        ]
    elif case == "time-kind":
        plan["valid_time"] = {"kind": "SOMETIME", "value": "occurrence-1"}
    elif case == "time-empty":
        plan["valid_time"] = {"kind": "ORDER_ONLY", "value": ""}
    elif case == "time-naive":
        plan["valid_time"] = {"kind": "INSTANT", "value": "2026-03-02T00:00:00"}
    elif case == "time-invalid":
        plan["valid_time"] = {"kind": "INSTANT", "value": "not-a-time"}
    elif case == "time-fields":
        plan["valid_time"] = {
            "kind": "ORDER_ONLY",
            "value": "occurrence-1",
            "extra": True,
        }
    else:
        raise AssertionError(f"unknown test mutation: {case}")


def test_population_p1_surface_is_private_and_dependency_neutral() -> None:
    population = _population()

    assert set(population.__all__) == P1_SYMBOLS | P2_SYMBOLS
    assert all(not hasattr(malleus, name) for name in P1_SYMBOLS | P2_SYMBOLS)
    assert {member.value for member in population.PopulationPlanStatus} == {
        "CHANGE_SET",
        "NO_DOMAIN_CHANGE",
    }
    assert P1_REASONS <= {
        member.name for member in population.PopulationPlanRefusalReason
    }

    tree = ast.parse(Path(population.__file__).read_text(encoding="utf-8"))
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports.update(
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    )
    forbidden = ("handover", "research", "tests")
    assert not {
        name
        for name in imports
        if name in forbidden or name.startswith(tuple(f"{root}." for root in forbidden))
    }


@pytest.mark.parametrize(
    ("case", "reason"),
    [
        ("extra-root", "FIELDS_NOT_CLOSED"),
        ("missing-root", "FIELDS_NOT_CLOSED"),
        ("grammar", "UNSUPPORTED_GRAMMAR"),
        ("contract-short", "MALFORMED_IDENTITY"),
        ("contract-nonhex", "MALFORMED_IDENTITY"),
        ("contract-mismatch", "IDENTITY_MISMATCH"),
        ("profile-fields", "MALFORMED_PROFILE_REFERENCE"),
        ("profile-digest", "MALFORMED_PROFILE_REFERENCE"),
        ("adapter-fields", "MALFORMED_PLAN"),
        ("adapter-missing", "MALFORMED_PLAN"),
        ("sources-empty", "SOURCES_REQUIRED"),
        ("source-digest", "SOURCES_REQUIRED"),
        ("source-fields", "SOURCES_REQUIRED"),
        ("sources-duplicate", "SOURCES_REQUIRED"),
        ("evidence-digest", "MALFORMED_EVIDENCE_REFERENCE"),
        ("evidence-fields", "MALFORMED_EVIDENCE_REFERENCE"),
        ("evidence-duplicate", "MALFORMED_EVIDENCE_REFERENCE"),
        ("evidence-generated-collision", "MALFORMED_EVIDENCE_REFERENCE"),
        ("unknown-family", "UNKNOWN_FAMILY"),
        ("signals", "FAMILY_NOT_ADMITTED"),
        ("events", "FAMILY_NOT_ADMITTED"),
        ("records-shape", "MALFORMED_PLAN"),
        ("duplicate-record", "DUPLICATE_RECORD_ID"),
        ("derivation-record", "UNKNOWN_RECORD"),
        ("derivation-path", "ABSENT_PATH"),
        ("derivation-source", "UNLISTED_SOURCE"),
        ("derivation-fields", "MALFORMED_PLAN"),
        ("derivation-path-shape", "MALFORMED_PLAN"),
        ("underived-property", "UNDERIVED_FIELD"),
        ("underived-source", "UNDERIVED_FIELD"),
        ("underived-target", "UNDERIVED_FIELD"),
        ("supersession-record", "UNKNOWN_RECORD"),
        ("supersession-blank", "MALFORMED_SUPERSESSION"),
        ("supersession-duplicate", "UNKNOWN_RECORD"),
        ("supersession-fields", "MALFORMED_SUPERSESSION"),
        ("gap-kind", "UNKNOWN_GAP_KIND"),
        ("gap-source", "UNLISTED_SOURCE"),
        ("gap-fields", "MALFORMED_PLAN"),
        ("time-kind", "UNSUPPORTED_VALID_TIME"),
        ("time-empty", "UNSUPPORTED_VALID_TIME"),
        ("time-naive", "UNSUPPORTED_VALID_TIME"),
        ("time-invalid", "UNSUPPORTED_VALID_TIME"),
        ("time-fields", "UNSUPPORTED_VALID_TIME"),
    ],
)
def test_population_plan_refuses_pinned_rule(
    contract_pair, case: str, reason: str
) -> None:
    population = _population()
    _, partial = contract_pair
    plan = _plan(partial.identity)
    _mutate(plan, case)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, contract_pair)

    assert refusal.value.reason is getattr(
        population.PopulationPlanRefusalReason, reason
    )


def test_population_plan_reports_every_underived_field_at_once(
    contract_pair,
) -> None:
    population = _population()
    _, partial = contract_pair
    plan = _plan(partial.identity)
    _remove_derivation(plan, "left-1", ["properties", "label"])
    _remove_derivation(plan, "right-1", ["properties", "label"])
    _remove_derivation(plan, "link:left-1:right-1", ["target_id"])

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, contract_pair)

    assert refusal.value.reason is (
        population.PopulationPlanRefusalReason.UNDERIVED_FIELD
    )
    assert refusal.value.detail == (
        "record fields lack derivations: "
        "left-1:['properties', 'label'], "
        "link:left-1:right-1:['target_id'], "
        "right-1:['properties', 'label']; "
        "every properties key and both relation endpoints need a derivation, "
        "type and id do not"
    )


def test_population_plan_refuses_contract_and_view_mismatch(contract_pair) -> None:
    population = _population()
    compiled, _ = contract_pair
    mismatched = _effective(validated_fact_set_sha256="sha256:" + "1" * 64)
    plan = _plan(mismatched.identity)

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        population.compile_population_plan(
            plan,
            partial_contract=mismatched,
            contract_view=compiled.view,
            base_state=population.PopulationBaseState.empty(),
        )

    assert (
        refusal.value.reason is population.PopulationPlanRefusalReason.IDENTITY_MISMATCH
    )


@pytest.mark.parametrize(
    ("source_id", "with_gap"),
    [
        ("evidence-generic", False),
        ("plan:neutral:1", False),
        ("profile:state-version", False),
        ("plan:neutral:1:gaps", True),
    ],
)
def test_population_plan_refuses_source_and_evidence_closure_id_collision(
    contract_pair, source_id: str, with_gap: bool
) -> None:
    population = _population()
    _, partial = contract_pair
    plan = _plan(partial.identity)
    plan["sources"][0]["source_id"] = source_id
    for derivation in plan["derivations"]:
        derivation["source_id"] = source_id
    if with_gap:
        plan["gaps"] = [
            {
                "kind": "TYPE_ABSENT",
                "statement": "a source statement has no contract type",
                "source_id": source_id,
                "locator": "row:0",
            }
        ]

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, contract_pair)

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.MALFORMED_EVIDENCE_REFERENCE
    )


@pytest.mark.parametrize("plan", [None, [], "not a plan"])
def test_population_plan_refuses_non_mapping_root(contract_pair, plan: object) -> None:
    population = _population()

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, contract_pair)

    assert refusal.value.reason is population.PopulationPlanRefusalReason.MALFORMED_PLAN


@pytest.mark.parametrize(
    ("endpoint", "reason"),
    [
        ("source_id", "DANGLING_ENDPOINT"),
        ("target_id", "DANGLING_ENDPOINT"),
    ],
)
def test_population_lowering_refuses_dangling_endpoint(
    contract_pair, endpoint: str, reason: str
) -> None:
    population = _population()
    _, partial = contract_pair
    plan = _plan(partial.identity)
    relation = plan["records"]["relations"][0]
    missing_id = relation[endpoint]
    plan["records"]["entities"] = [
        record for record in plan["records"]["entities"] if record["id"] != missing_id
    ]
    plan["derivations"] = [
        item for item in plan["derivations"] if item["record_id"] != missing_id
    ]

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, contract_pair)

    assert refusal.value.reason is getattr(
        population.PopulationPlanRefusalReason, reason
    )


SUBJECT_SCHEMA = b"""\
id: https://example.malleus.dev/pareto-history
name: pareto_history
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  test: https://example.malleus.dev/pareto-history/
imports:
  - linkml:types
  - malleus
enums:
  LinkKind:
    permissible_values:
      LINKS:
slots:
  label:
    range: string
  subject:
    range: Entity
classes:
  LeftObject:
    is_a: Entity
    slots:
      - label
      - subject
    slot_usage:
      label:
        required: true
  RightObject:
    is_a: Entity
    slots:
      - label
    slot_usage:
      label:
        required: true
  ObjectLink:
    is_a: Relation
    slot_usage:
      relation_type:
        range: LinkKind
        required: true
        equals_string: LINKS
      source_id:
        range: LeftObject
        required: true
      target_id:
        range: RightObject
        required: true
"""


def _subject_pair():
    """A contract whose LeftObject carries an Entity-ranged subject reference."""

    compiled = _generic_compilation(SUBJECT_SCHEMA)
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    return compiled, partial


def _subject_plan(subject: str, *, origin: str | None = None):
    pair = _subject_pair()
    plan = _plan(pair[1].identity)
    plan["records"]["entities"][0]["properties"]["subject"] = subject
    derivation = {
        "record_id": "left-1",
        "path": ["properties", "subject"],
        "source_id": "source-generic",
        "locator": "row:0:subject",
    }
    if origin is not None:
        derivation["origin"] = origin
    plan["derivations"].append(derivation)
    return plan, pair


def test_population_lowering_accepts_a_subject_named_in_the_change_set() -> None:
    """Core-13. A subject is a reference to a record, like a relation endpoint,
    and one that resolves in the same change set lowers unchanged."""

    plan, pair = _subject_plan("right-1")

    result = _compile(plan, pair)

    assert result.status is _population().PopulationPlanStatus.CHANGE_SET


def test_population_lowering_refuses_a_subject_that_resolves_nowhere() -> None:
    """The document adapter is handed one change set and reads a subject's name
    from it alone, so it cannot tell a base-state subject from a typo. The plan
    compiler sees the change set and the base state together, which is where
    the endpoint check already lives, so the resolution check belongs here."""

    population = _population()
    plan, pair = _subject_plan("right-404")

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, pair)

    assert (
        refusal.value.reason is population.PopulationPlanRefusalReason.DANGLING_SUBJECT
    )
    assert refusal.value.detail == "record left-1 has absent subject: right-404"


def test_population_lowering_refuses_a_derivation_that_marks_its_origin() -> None:
    """Core-17 withdraws the projected subject, and `origin` leaves the plan
    grammar with it: every derivation is again four fields, and a fifth is
    refused for the reason a fifth was always refused. A reader of a plan
    needs no mark to tell a derived subject from a producer's own, because
    nothing derives one."""

    population = _population()
    plan, pair = _subject_plan("right-1", origin="PROJECTED")

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, pair)

    assert (
        refusal.value.reason is population.PopulationPlanRefusalReason.MALFORMED_PLAN
    )
    assert refusal.value.detail == "derivation fields are not closed"


def test_population_lowering_refuses_unknown_supersession(contract_pair) -> None:
    population = _population()
    _, partial = contract_pair
    plan = _plan(partial.identity)
    plan["supersessions"] = [
        {"record_id": "left-1", "supersedes_record_id": "left-old"}
    ]

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, contract_pair)

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.UNKNOWN_SUPERSESSION
    )


def test_valid_plan_lowers_exact_operations_closures_and_time_without_io(
    contract_pair, monkeypatch: pytest.MonkeyPatch
) -> None:
    population = _population()
    _, partial = contract_pair
    plan = _plan(partial.identity)
    original = deepcopy(plan)
    assert set(plan) == PLAN_FIELDS

    def forbidden_io(*_args, **_kwargs):
        raise AssertionError("the pure population compiler attempted filesystem I/O")

    monkeypatch.setattr(Path, "open", forbidden_io)
    monkeypatch.setattr(Path, "write_bytes", forbidden_io)
    first = _compile(plan, contract_pair)
    second = _compile(plan, contract_pair)

    assert first == second
    assert isinstance(first, population.PopulationPlanCompilation)
    assert plan == original
    assert first.status is population.PopulationPlanStatus.CHANGE_SET
    assert first.canonical_plan_bytes == _canonical(plan)
    assert first.plan_id == "plan:neutral:1"
    assert first.source_record_ids == ("source-generic",)
    assert first.evidence_record_ids == (
        "profile:state-version",
        "plan:neutral:1",
        "evidence-generic",
    )
    assert first.valid_time == KnowledgeValidTime("ORDER_ONLY", "occurrence-1")
    assert first.supersedes == ()
    assert [operation.ordinal for operation in first.operations] == [0, 1, 2]
    assert [operation.operation_id for operation in first.operations] == [
        "operation:plan:neutral:1:0",
        "operation:plan:neutral:1:1",
        "operation:plan:neutral:1:2",
    ]
    assert [operation.operation_type for operation in first.operations] == [
        "CREATE_ENTITY",
        "CREATE_ENTITY",
        "CREATE_RELATION",
    ]
    assert first.operations[2].depends_on == (
        "operation:plan:neutral:1:0",
        "operation:plan:neutral:1:1",
    )
    assert all(operation.supersedes_record_id is None for operation in first.operations)
    with pytest.raises(TypeError):
        first.operations[0].properties["label"] = "mutated"


def test_relation_dependencies_follow_endpoint_roles_not_record_order(
    contract_pair,
) -> None:
    _, partial = contract_pair
    plan = _plan(partial.identity)
    entities = plan["records"]["entities"]
    assert [entity["id"] for entity in entities] == ["left-1", "right-1"]
    plan["records"]["entities"] = [entities[1], entities[0]]

    result = _compile(plan, contract_pair)

    relation = result.operations[2]
    assert [operation.record_id for operation in result.operations] == [
        "right-1",
        "left-1",
        "link:left-1:right-1",
    ]
    assert (relation.source_id, relation.target_id) == ("left-1", "right-1")
    assert relation.depends_on == (
        "operation:plan:neutral:1:1",
        "operation:plan:neutral:1:0",
    )


def test_relation_dependency_omits_endpoint_already_in_base(tmp_path: Path) -> None:
    population = _population()
    history, compiled, partial, _, _, _ = _anchored_history(tmp_path)
    replay = _admit_operations(
        history,
        change_set_id="change:base-left",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:base-left",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left-base",
                properties={"label": "base"},
                depends_on=(),
            ),
        ),
        order="base-1",
    )
    plan = _plan(partial.identity)
    plan["records"]["entities"] = [plan["records"]["entities"][1]]
    plan["records"]["relations"][0]["source_id"] = "left-base"
    plan["derivations"] = [
        item for item in plan["derivations"] if item["record_id"] != "left-1"
    ]
    base = population.PopulationBaseState.from_replay(replay)

    result = _compile(plan, (compiled, partial), base_state=base)

    assert result.operations[-1].depends_on == ("operation:plan:neutral:1:0",)


def _self_link_contract():
    source = b"""\
id: https://example.malleus.dev/self-link
name: self_link
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  peer: https://example.malleus.dev/self-link/
imports:
  - linkml:types
  - malleus
enums:
  SelfLinkKind:
    permissible_values:
      LINKS:
slots:
  label:
    range: string
classes:
  BareObject:
    is_a: Entity
  Object:
    is_a: Entity
    slots:
      - label
    slot_usage:
      label:
        required: true
  SelfLink:
    is_a: Relation
    slot_usage:
      relation_type:
        range: SelfLinkKind
        required: true
        equals_string: LINKS
      source_id:
        range: Object
        required: true
      target_id:
        range: Object
        required: true
"""
    compiled = _compile_binding(
        _binding(
            {
                "self-link": source,
                "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
                "linkml:types": _trusted_types(),
            },
            "self-link",
        )
    )
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    return compiled, partial


def test_self_relation_dependency_is_unique() -> None:
    compiled, partial = _self_link_contract()
    contract_pair = (compiled, partial)
    plan = _plan(partial.identity)
    plan["records"] = {
        "entities": [
            {"type": "Object", "id": "object-1", "properties": {"label": "one"}}
        ],
        "relations": [
            {
                "type": "SelfLink",
                "id": "self-link-1",
                "source_id": "object-1",
                "target_id": "object-1",
                "properties": {"relation_type": "LINKS"},
            }
        ],
    }
    plan["derivations"] = [
        {
            "record_id": "object-1",
            "path": ["properties", "label"],
            "source_id": "source-generic",
            "locator": "row:0:label",
        },
        {
            "record_id": "self-link-1",
            "path": ["properties", "relation_type"],
            "source_id": "source-generic",
            "locator": "row:0:kind",
        },
        {
            "record_id": "self-link-1",
            "path": ["source_id"],
            "source_id": "source-generic",
            "locator": "row:0:id",
        },
        {
            "record_id": "self-link-1",
            "path": ["target_id"],
            "source_id": "source-generic",
            "locator": "row:0:id",
        },
    ]

    result = _compile(plan, contract_pair)

    assert result.operations[1].depends_on == ("operation:plan:neutral:1:0",)


def test_population_plan_refuses_null_properties_even_when_contract_has_no_slots() -> (
    None
):
    population = _population()
    compiled, partial = _self_link_contract()
    plan = _plan(partial.identity)
    plan["records"] = {
        "entities": [{"type": "BareObject", "id": "bare-1", "properties": None}],
        "relations": [],
    }
    plan["derivations"] = []

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(plan, (compiled, partial))

    assert refusal.value.reason is population.PopulationPlanRefusalReason.MALFORMED_PLAN


def test_supersession_copies_records_and_deduplicates_creator_changes(
    tmp_path: Path,
) -> None:
    population = _population()
    history, compiled, partial, _, _, _ = _anchored_history(tmp_path)
    _admit_operations(
        history,
        change_set_id="change:B",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:right-old",
                operation_type="CREATE_ENTITY",
                record_type="RightObject",
                record_id="right-old",
                properties={"label": "old B"},
                depends_on=(),
            ),
        ),
        order="base-1",
    )
    replay = _admit_operations(
        history,
        change_set_id="change:A",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:left-old-1",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left-old-1",
                properties={"label": "old A1"},
                depends_on=(),
            ),
            KnowledgeOperation(
                ordinal=1,
                operation_id="operation:left-old-2",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left-old-2",
                properties={"label": "old A2"},
                depends_on=(),
            ),
        ),
        order="base-2",
    )
    plan = _plan(partial.identity)
    plan["records"] = {
        "entities": [
            {
                "type": "RightObject",
                "id": "right-new",
                "properties": {"label": "new B"},
            },
            {
                "type": "LeftObject",
                "id": "left-new-1",
                "properties": {"label": "new A1"},
            },
            {
                "type": "LeftObject",
                "id": "left-new-2",
                "properties": {"label": "new A2"},
            },
        ],
        "relations": [],
    }
    plan["derivations"] = [
        {
            "record_id": record["id"],
            "path": ["properties", "label"],
            "source_id": "source-generic",
            "locator": f"row:{index}:label",
        }
        for index, record in enumerate(plan["records"]["entities"])
    ]
    plan["supersessions"] = [
        {"record_id": "right-new", "supersedes_record_id": "right-old"},
        {"record_id": "left-new-1", "supersedes_record_id": "left-old-1"},
        {"record_id": "left-new-2", "supersedes_record_id": "left-old-2"},
    ]
    base = population.PopulationBaseState.from_replay(replay)

    result = _compile(plan, (compiled, partial), base_state=base)

    assert [operation.supersedes_record_id for operation in result.operations] == [
        "right-old",
        "left-old-1",
        "left-old-2",
    ]
    assert result.supersedes == ("change:B", "change:A")
    governed = _admit_operations(
        history,
        change_set_id="change:replacement",
        operations=result.operations,
        order=result.valid_time.value,
        supersedes=result.supersedes,
    )
    assert {row["id"] for row in governed.graph.query("LeftObject")} == {
        "left-new-1",
        "left-new-2",
    }
    assert {row["id"] for row in governed.graph.query("RightObject")} == {"right-new"}
    assert governed.record_history["right-old"].superseded_by == "right-new"
    assert governed.record_history["left-old-1"].superseded_by == "left-new-1"
    assert governed.record_history["left-old-2"].superseded_by == "left-new-2"


def test_population_plan_refuses_two_replacements_of_one_active_record(
    tmp_path: Path,
) -> None:
    population = _population()
    _, compiled, partial, replay = _single_left_base(
        tmp_path, KnowledgeValidTime("ORDER_ONLY", "base-1")
    )
    plan = _single_replacement_plan(
        partial.identity,
        record_id="left-new-1",
        record_type="LeftObject",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "base-2"),
    )
    plan["records"]["entities"].append(
        {
            "type": "LeftObject",
            "id": "left-new-2",
            "properties": {"label": "new two"},
        }
    )
    plan["derivations"].append(
        {
            "record_id": "left-new-2",
            "path": ["properties", "label"],
            "source_id": "source-generic",
            "locator": "row:2:label",
        }
    )
    plan["supersessions"].append(
        {"record_id": "left-new-2", "supersedes_record_id": "left-old"}
    )

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )

    assert (
        refusal.value.reason is population.PopulationPlanRefusalReason.SUPERSESSION_FORK
    )


def test_population_plan_refuses_reusing_the_superseded_record_id(
    tmp_path: Path,
) -> None:
    population = _population()
    _, compiled, partial, replay = _single_left_base(
        tmp_path, KnowledgeValidTime("ORDER_ONLY", "base-1")
    )
    plan = _single_replacement_plan(
        partial.identity,
        record_id="left-old",
        record_type="LeftObject",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "base-2"),
    )

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.DUPLICATE_RECORD_ID
    )


def test_population_plan_refuses_reusing_an_inactive_historical_record_id(
    tmp_path: Path,
) -> None:
    population = _population()
    _, compiled, partial, replay = _superseded_left_base(tmp_path)
    plan = _single_replacement_plan(
        partial.identity,
        record_id="left-retired",
        record_type="LeftObject",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "base-3"),
    )
    plan["supersessions"][0]["supersedes_record_id"] = "left-current"

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.DUPLICATE_RECORD_ID
    )


def test_population_plan_refuses_superseding_an_inactive_record_as_a_fork(
    tmp_path: Path,
) -> None:
    population = _population()
    _, compiled, partial, replay = _superseded_left_base(tmp_path)
    plan = _single_replacement_plan(
        partial.identity,
        record_id="left-new",
        record_type="LeftObject",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "base-3"),
    )
    plan["supersessions"][0]["supersedes_record_id"] = "left-retired"

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )

    assert (
        refusal.value.reason is population.PopulationPlanRefusalReason.SUPERSESSION_FORK
    )


def test_population_plan_refuses_cross_type_supersession(tmp_path: Path) -> None:
    population = _population()
    _, compiled, partial, replay = _single_left_base(
        tmp_path, KnowledgeValidTime("ORDER_ONLY", "base-1")
    )
    plan = _single_replacement_plan(
        partial.identity,
        record_id="right-new",
        record_type="RightObject",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "base-2"),
    )

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.SUPERSESSION_TYPE_MISMATCH
    )


def test_population_plan_refuses_cross_family_supersession(tmp_path: Path) -> None:
    population = _population()
    _, compiled, partial, replay = _single_left_base(
        tmp_path, KnowledgeValidTime("ORDER_ONLY", "base-1")
    )
    plan = _plan(partial.identity)
    plan["supersessions"] = [
        {"record_id": "link:left-1:right-1", "supersedes_record_id": "left-old"}
    ]

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.SUPERSESSION_TYPE_MISMATCH
    )


@pytest.mark.parametrize(
    ("base_time", "replacement_time"),
    [
        (
            KnowledgeValidTime("ORDER_ONLY", "base-1"),
            KnowledgeValidTime("INSTANT", "2026-03-03T00:00:00Z"),
        ),
        (
            KnowledgeValidTime("INSTANT", "2026-03-02T00:00:00Z"),
            KnowledgeValidTime("ORDER_ONLY", "base-2"),
        ),
        (
            KnowledgeValidTime("INSTANT", "2026-03-02T00:00:00Z"),
            KnowledgeValidTime("INSTANT", "2026-03-02T00:00:00Z"),
        ),
        (
            KnowledgeValidTime("INSTANT", "2026-03-02T00:00:00Z"),
            KnowledgeValidTime("INSTANT", "2026-03-01T19:00:00-05:00"),
        ),
        (
            KnowledgeValidTime("INSTANT", "2026-03-02T00:00:00Z"),
            KnowledgeValidTime("INSTANT", "2026-03-01T00:00:00Z"),
        ),
    ],
)
def test_population_plan_refuses_incompatible_supersession_time(
    tmp_path: Path,
    base_time: KnowledgeValidTime,
    replacement_time: KnowledgeValidTime,
) -> None:
    population = _population()
    _, compiled, partial, replay = _single_left_base(tmp_path, base_time)
    plan = _single_replacement_plan(
        partial.identity,
        record_id="left-new",
        record_type="LeftObject",
        valid_time=replacement_time,
    )

    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )

    assert (
        refusal.value.reason
        is population.PopulationPlanRefusalReason.SUPERSESSION_VALID_TIME_MISMATCH
    )


def test_population_plan_accepts_strictly_later_instant_supersession(
    tmp_path: Path,
) -> None:
    population = _population()
    history, compiled, partial, replay = _single_left_base(
        tmp_path, KnowledgeValidTime("INSTANT", "2026-03-02T00:00:00Z")
    )
    plan = _single_replacement_plan(
        partial.identity,
        record_id="left-new",
        record_type="LeftObject",
        valid_time=KnowledgeValidTime("INSTANT", "2026-03-03T00:00:00Z"),
    )

    result = _compile(
        plan,
        (compiled, partial),
        base_state=population.PopulationBaseState.from_replay(replay),
    )

    assert result.status is population.PopulationPlanStatus.CHANGE_SET
    admitted = _admit_operations_at(
        history,
        change_set_id="change:left-new",
        operations=result.operations,
        valid_time=result.valid_time,
        supersedes=result.supersedes,
    )
    assert {row["id"] for row in admitted.graph.query("LeftObject")} == {"left-new"}


@pytest.mark.parametrize("replacement_order", ["base-1", "before-base-1"])
def test_population_plan_does_not_invent_order_for_order_only_supersession(
    tmp_path: Path, replacement_order: str
) -> None:
    population = _population()
    history, compiled, partial, replay = _single_left_base(
        tmp_path, KnowledgeValidTime("ORDER_ONLY", "base-1")
    )
    plan = _single_replacement_plan(
        partial.identity,
        record_id="left-new",
        record_type="LeftObject",
        valid_time=KnowledgeValidTime("ORDER_ONLY", replacement_order),
    )

    result = _compile(
        plan,
        (compiled, partial),
        base_state=population.PopulationBaseState.from_replay(replay),
    )
    admitted = _admit_operations(
        history,
        change_set_id="change:left-new",
        operations=result.operations,
        order=replacement_order,
        supersedes=result.supersedes,
    )

    assert {row["id"] for row in admitted.graph.query("LeftObject")} == {"left-new"}


def test_population_plan_refuses_supersession_that_orphans_active_relation(
    tmp_path: Path,
) -> None:
    population = _population()
    history, compiled, partial, _, _, _ = _anchored_history(tmp_path)
    replay = _admit_operations(
        history,
        change_set_id="change:linked-base",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:left-old",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left-old",
                properties={"label": "old"},
                depends_on=(),
            ),
            KnowledgeOperation(
                ordinal=1,
                operation_id="operation:right-base",
                operation_type="CREATE_ENTITY",
                record_type="RightObject",
                record_id="right-base",
                properties={"label": "right"},
                depends_on=(),
            ),
            KnowledgeOperation(
                ordinal=2,
                operation_id="operation:link-old",
                operation_type="CREATE_RELATION",
                record_type="ObjectLink",
                record_id="link-old",
                properties={"relation_type": "LINKS"},
                depends_on=("operation:left-old", "operation:right-base"),
                source_id="left-old",
                target_id="right-base",
            ),
        ),
        order="base-1",
    )
    plan = _plan(partial.identity)
    plan["records"] = {
        "entities": [
            {
                "type": "LeftObject",
                "id": "left-new",
                "properties": {"label": "new"},
            }
        ],
        "relations": [],
    }
    plan["derivations"] = [
        {
            "record_id": "left-new",
            "path": ["properties", "label"],
            "source_id": "source-generic",
            "locator": "row:1:left",
        }
    ]
    plan["supersessions"] = [
        {"record_id": "left-new", "supersedes_record_id": "left-old"}
    ]

    with pytest.raises(ValueError, match="Source entity 'left-old' does not exist"):
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )


def test_zero_records_returns_no_domain_change_with_complete_closures(
    contract_pair,
) -> None:
    population = _population()
    _, partial = contract_pair
    plan = _plan(partial.identity)
    plan["records"] = {"entities": [], "relations": []}
    plan["derivations"] = []
    plan["gaps"] = [
        {
            "kind": "TYPE_ABSENT",
            "statement": "the contract has no type for this source statement",
            "source_id": "source-generic",
            "locator": "row:0",
        }
    ]

    result = _compile(plan, contract_pair)

    assert result.status is population.PopulationPlanStatus.NO_DOMAIN_CHANGE
    assert result.operations == ()
    assert result.supersedes == ()
    assert result.source_record_ids == ("source-generic",)
    assert result.evidence_record_ids == (
        "profile:state-version",
        "plan:neutral:1",
        "evidence-generic",
        "plan:neutral:1:gaps",
    )


@pytest.mark.parametrize("defect", ["unknown-type", "unexpected-record-field"])
def test_compiler_surfaces_structural_contract_refusal_unchanged(
    contract_pair, defect: str
) -> None:
    compiled, partial = contract_pair
    plan = _plan(partial.identity)
    if defect == "unknown-type":
        plan["records"]["entities"][0]["type"] = "Nope"
    else:
        plan["records"]["entities"][0]["extra"] = True
    with pytest.raises(ValueError) as direct:
        KnowledgeGraph.from_records(compiled.view, plan["records"])

    with pytest.raises(ValueError) as compiled_refusal:
        _compile(plan, contract_pair)

    assert type(compiled_refusal.value) is type(direct.value)
    assert str(compiled_refusal.value) == str(direct.value)


@pytest.mark.parametrize("defect", ["missing-type", "unknown-type"])
def test_supersession_surfaces_structural_contract_refusal_unchanged(
    tmp_path: Path, defect: str
) -> None:
    population = _population()
    _, compiled, partial, replay = _single_left_base(
        tmp_path, KnowledgeValidTime("ORDER_ONLY", "base-1")
    )
    plan = _single_replacement_plan(
        partial.identity,
        record_id="left-new",
        record_type="LeftObject",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "base-2"),
    )
    if defect == "missing-type":
        del plan["records"]["entities"][0]["type"]
    else:
        plan["records"]["entities"][0]["type"] = "Nope"

    with pytest.raises(ValueError) as direct:
        KnowledgeGraph.from_records(compiled.view, plan["records"])
    with pytest.raises(ValueError) as compiled_refusal:
        _compile(
            plan,
            (compiled, partial),
            base_state=population.PopulationBaseState.from_replay(replay),
        )

    assert type(compiled_refusal.value) is type(direct.value)
    assert str(compiled_refusal.value) == str(direct.value)


def test_base_state_from_replay_exposes_current_endpoints_only(tmp_path: Path) -> None:
    population = _population()
    history, compiled, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-1",
        record_id="left-version-1",
        label="before",
        order="event-1",
    )
    _admit_record_change(history, first, suffix="-version-1")
    second = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-2",
        record_id="left-version-2",
        label="after",
        order="event-2",
        supersedes_record_id="left-version-1",
    )
    replay = _admit_record_change(history, second, suffix="-version-2")

    base = population.PopulationBaseState.from_replay(replay)
    current = _plan(partial.identity)
    current["records"]["entities"] = [current["records"]["entities"][1]]
    current["records"]["relations"][0]["source_id"] = "left-version-2"
    current["derivations"] = [
        item for item in current["derivations"] if item["record_id"] != "left-1"
    ]

    result = _compile(current, (compiled, partial), base_state=base)

    assert result.operations[-1].depends_on == ("operation:plan:neutral:1:0",)
    historical = deepcopy(current)
    historical["records"]["relations"][0]["source_id"] = "left-version-1"
    with pytest.raises(population.PopulationPlanRefusal) as refusal:
        _compile(historical, (compiled, partial), base_state=base)

    assert (
        refusal.value.reason is population.PopulationPlanRefusalReason.DANGLING_ENDPOINT
    )


def test_direct_records_equal_governed_replay(
    tmp_path: Path,
) -> None:
    history, compiled, partial, _, source, evidence = _anchored_history(tmp_path)
    plan = _plan(
        partial.identity,
        source_identity=source,
        evidence_identity=evidence,
    )
    result = _compile(plan, (compiled, partial))
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="profile:state-version",
            artifact_identity=_digest(PROFILE_BYTES),
        ),
        PROFILE_BYTES,
        "RETAINED_EVIDENCE",
    )
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id=plan["plan_id"],
            artifact_identity=_digest(result.canonical_plan_bytes),
        ),
        result.canonical_plan_bytes,
        "RETAINED_EVIDENCE",
    )
    change = history.compose_change_set(
        change_set_id="change:plan:neutral:1",
        source_record_ids=result.source_record_ids,
        evidence_record_ids=result.evidence_record_ids,
        operations=result.operations,
        valid_time=result.valid_time,
        supersedes=result.supersedes,
    )
    before = history.replay()
    admitted = history.admit(
        change_set=change,
        machine_events=_protocol_events(
            change,
            before.machine_state.identity,
            identifier_suffix="-population-plan",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    direct = KnowledgeGraph.from_records(compiled.view, plan["records"])

    assert admitted.graph.export_records() == direct.export_records()
