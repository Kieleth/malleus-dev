"""Guards for the shop-01 contract, its pin, its questions and its review files.

Nothing here hardcodes a commit, a tree, a digest, a pack version or a Core
refusal reason. ``pin.py`` writes those into the contract and the manifest from
one commit, and every test below recomputes the same fact at the commit the
contract names, with ``git show`` and never from the working tree.

Core does not move under this cell. It pins the commit run-21 pinned, and the
two entries that read Core rather than carrying it unread, Core-19 and Core-20,
are recomputed here at that commit and must come back LANDED.

What this cell moves is the source shape, and the tests separate the two things
that moved with it from the one thing that did not. The declared inputs moved:
twelve instead of eight, five source files where the reading was, the shipped
state-version profile where the source-assertion profile was. The gate's
required pieces moved: the document adapter's derivation content checks are not
required, because no plan the producer writes reaches them, and the plan
compiler's checks and the shipped structural bundle are required instead. The
producer's three model fields did not move at all, and neither did any other key
of the producer block, so a reader can tell which of the two the cell varies.

This cell has not run. Its results directory and its ontology-run directory do
not exist, the review task and the record still carry their placeholders, and
the tests that would read a frozen figure read the absence instead and say so.
Run-21's own frozen files are held by digest, so shop-01 existing cannot have
moved a byte of the cell it is translated from.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_21 = HERE.parent / "run-21"
EXPERIMENT = HERE.parent
EVALUATION = ROOT / "paper-v4" / "evaluation-v4"
CONTRACT_PATH = HERE / "run-contract.json"
MANIFEST_PATH = HERE / "producer-input-manifest.json"
QUESTIONS_PATH = HERE / "competency-questions.json"
SPAWN_MESSAGE = HERE / "spawn-message.md"
REVIEW_TASK = EVALUATION / "shop-01" / "review-task.md"
REVIEW_RECORD = EVALUATION / "shop-01" / "review-record.blank.md"
REVIEW_PROTOCOL_V2 = EVALUATION / "review-protocol-v2.json"
REVIEW_VALIDATOR = EVALUATION / "review.py"
ACTIVE_TEST_MANIFEST = ROOT / "paper-v4" / "active-test-manifest.json"
PAPER_LEDGER = ROOT / "paper-v4" / "paper-ledger.md"

DECLARED_SOURCES = {
    "MALLEUS_NASCENT_PROJECT_SKILL": ".claude/skills/malleus-acolyte/SKILL.md",
    "SOURCE_WAREHOUSE": (
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment"
        "/input/sources/warehouse.jsonl"
    ),
    "SOURCE_INVENTORY": (
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment"
        "/input/sources/inventory-units.csv"
    ),
    "SOURCE_INVOICES": (
        "research/ontology_driven_kg_realization/fixtures"
        "/small_shop_fulfilment_settlement_v1/input/sources/invoices.csv"
    ),
    "SOURCE_PAYMENTS": (
        "research/ontology_driven_kg_realization/fixtures"
        "/small_shop_fulfilment_settlement_v1/input/sources/payments.jsonl"
    ),
    "SOURCE_SUPPLIER_ORDERS": (
        "research/ontology_driven_kg_realization/fixtures"
        "/small_shop_fulfilment_correction_v1/input/sources"
        "/supplier-order-history.jsonl"
    ),
    "MALLEUS_ROOT": "ontology/malleus.yaml",
    "LINKML_TYPES": "paper-v4/experiment-v2/run-inputs/linkml-types.yaml",
    "METROLOGY_PACK": "ontology/packs/metrology.yaml",
    "CHRONOLOGY_PACK": "ontology/packs/chronology.yaml",
    "RESEARCH_PACK": "ontology/packs/research.yaml",
    "STATE_VERSION_PROFILE": "src/malleus/profiles/state-version.json",
}
# The six this cell shares with the document cell it is translated from. The
# other six are its own, and the manifest says so rather than reporting them
# unchanged against a manifest that never carried them.
SHARED_WITH_RUN_21 = (
    "CHRONOLOGY_PACK",
    "LINKML_TYPES",
    "MALLEUS_NASCENT_PROJECT_SKILL",
    "MALLEUS_ROOT",
    "METROLOGY_PACK",
    "RESEARCH_PACK",
)

THIS_CELL_CHANGE_IDS = (
    "CONTRACT_IDENTITY_SUPPLIED",
    "OPUS_5_PRODUCER_AT_SHOP_01",
    "PLAN_DRIVEN_RUNNER",
    "SOURCE_SHAPE_ROWS",
    "TYPE_SET_CLOSURE_BEFORE_BINDING",
)
CARRIED_CHANGE_IDS = (
    "BINDING_FROZEN_AT_ACCEPTANCE",
    "CORE_19_HONEST_REPORTING",
    "CORE_20_REFUSAL_LIST_PREFLIGHT",
    "ENTITY_KIND_RESTRICTED",
    "GATE_SURFACES_CHAINED_CAUSE",
    "INTERPRETER_PREFLIGHT",
    "LAUNCH_LOG_V2",
    "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION",
    "PACKS_0_3_0",
    "PUBLIC_COST_RECORD",
    "QUERY_CASE_KINDS_V3",
    "STOP_RULE_CLARIFIED",
    "SUBJECT_TAGS_PROJECTED",
)
CHANGE_IDS = tuple(sorted(THIS_CELL_CHANGE_IDS + CARRIED_CHANGE_IDS))
READ_AT_THE_PIN_CORE_CHANGE_IDS = (
    "CORE_19_HONEST_REPORTING",
    "CORE_20_REFUSAL_LIST_PREFLIGHT",
)
LANDED = "LANDED"

MODEL_FIELDS = {
    "requested_model": "opus",
    "model_family": "Claude Opus 5",
    "model_id": "claude-opus-5",
}
QUESTION_IDS = ["CQ-S1", "CQ-S2", "CQ-S3", "CQ-S4"]
HALF_BOUND_QUESTIONS = ("CQ-S2", "CQ-S4")
REQUIRED_PIECES = [
    "AGGREGATE_REFUSAL_DIAGNOSTICS",
    "EVENT_FAMILY_ADMISSION",
    "FULL_DOMAIN_HISTORY_PROFILE",
    "GROUNDED_PACKS_AND_PACK_GROUNDING",
    "NASCENT_PROJECT_PLAYBOOK",
    "PLAN_DERIVATION_CHECKS",
    "STRUCTURAL_HISTORY_BUNDLE",
]
BUNDLE_PATHS = (
    "src/malleus/profiles/structural-admission-check.json",
    "src/malleus/profiles/structural-admission-policy.json",
    "src/malleus/profiles/structural-history-binding.json",
    "src/malleus/profiles/structural-history-machine.json",
)
POPULATION_ENUM_BLOCK = re.compile(
    r"class PopulationPlanRefusalReason\(str, Enum\):\n(?P<body>(?:    .*\n|\n)*)"
)
ENUM_MEMBER = re.compile(r"^    (?P<name>[A-Z][A-Z0-9_]*) = \"(?P=name)\"$", re.M)

# The exact bytes run-21 left in the repository. This cell writes nothing into
# the closed one, so every one of these must read the same after shop-01 exists.
RUN_21_FROZEN = {
    "results/run-result.json": (
        "sha256:0d617b59c1e90a351cc5f9f237a7ecf15b8983ed936a814506b53995d027fb81"
    ),
    "results/launch-log.json": (
        "sha256:eb584ffd6e9ea4d4480aeed619c3866f6649f5d4b1cdf7024083859621dedde7"
    ),
    "results/census.json": (
        "sha256:af4d0bf1f4ae86966d257f6587afce986e5006806f1118873042808c09b5b99e"
    ),
    "results/usage.json": (
        "sha256:7f9b85c245afed82bec8375e6f2dc4606dd015e7805b8941ad235744fdb2a536"
    ),
    "ontology-run/result.json": (
        "sha256:e367a01fcec58bfe437944666ee6d663722b147d43967815998a7e100f946fd6"
    ),
}
# The result files this cell will write, and does not have yet.
PENDING_RESULTS = (
    "results",
    "ontology-run",
)
REVIEW_PLACEHOLDERS = (
    "{{ROWS_CQ_S1}}",
    "{{ROWS_CQ_S2}}",
    "{{ROWS_CQ_S3}}",
    "{{ROWS_CQ_S4}}",
    "{{ROWS_TOTAL}}",
    "{{WITNESS_COUNT}}",
)


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _canonical_digest(data: bytes) -> str:
    return _digest(
        json.dumps(
            json.loads(data),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    )


def _contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_bytes())


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_bytes())


def _commit() -> str:
    return _contract()["core_gate"]["execution_baseline"]["core_commit"]


def _git_show(path: str, commit: str | None = None) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit or _commit()}:{path}"],
        capture_output=True,
        cwd=ROOT,
    )
    assert completed.returncode == 0, f"{path} is unreadable at the pinned commit"
    return completed.stdout


def _changes() -> dict[str, dict[str, object]]:
    return {item["id"]: item for item in _contract()["protocol"]["changes"]}


def test_the_contract_names_this_cell_and_the_cell_it_translates() -> None:
    contract = _contract()

    assert contract["schema"] == "malleus.paper-v4.v4-run-contract/v1"
    assert contract["run_id"] == "shop-01"
    assert contract["status"] == "READY_FOR_PRODUCER"
    assert contract["scope"]["translated_from"] == "run-21"
    assert contract["scope"]["variable"] == "THE_SOURCE_SHAPE_ROWS_INSTEAD_OF_PROSE"
    assert contract["scope"]["structured_sources"] == 5
    assert contract["scope"]["documents"] == 0
    assert contract["protocol"]["opening_ledger_entry"] == "E-0201"
    assert set(contract["scope"]["held_fixed"]) == {
        "THE_SKILL",
        "THE_CORE_COMMIT",
        "THE_PRODUCER_BLOCK",
        "THE_GATE",
        "THE_BINDER",
        "THE_EXECUTOR",
    }


def test_every_declared_input_is_the_bytes_at_the_pinned_commit() -> None:
    """Twelve inputs, every one tracked, every digest recomputed with git show."""

    manifest = _manifest()
    declared = {item["name"]: item for item in manifest["declared_inputs"]}

    assert len(declared) == 12
    assert {name: item["source"] for name, item in declared.items()} == DECLARED_SOURCES
    for name, item in sorted(declared.items()):
        assert item["sha256"] == _digest(_git_show(item["source"])), name
    assert manifest["input_bytes"]["untracked_inputs"] == []
    assert manifest["run_id"] == "shop-01"
    assert manifest["status"] == "FROZEN"


def test_the_five_source_files_are_the_ones_the_fixture_reads() -> None:
    """The declared bytes are the fixture's own, not a copy that could drift."""

    declared = {item["name"]: item for item in _manifest()["declared_inputs"]}
    for name in (
        "SOURCE_WAREHOUSE",
        "SOURCE_INVENTORY",
        "SOURCE_INVOICES",
        "SOURCE_PAYMENTS",
        "SOURCE_SUPPLIER_ORDERS",
    ):
        path = ROOT / declared[name]["source"]
        assert path.exists(), name
        assert declared[name]["sha256"] == _digest(path.read_bytes()), name
    assert _contract()["source"]["source_ids"] == [
        "source:small-shop:warehouse",
        "source:small-shop:inventory",
        "source:small-shop:invoices",
        "source:small-shop:payments",
        "source:small-shop:supplier-orders",
    ]
    assert _contract()["source"]["locator_form"] == "row:N:field"


def test_the_six_shared_inputs_are_run_21s_bytes_and_the_other_six_are_not_claimed() -> None:
    manifest = _manifest()
    moved = manifest["moved_since"]
    reference = {
        item["name"]: item["sha256"]
        for item in json.loads(
            (RUN_21 / "producer-input-manifest.json").read_bytes()
        )["declared_inputs"]
    }
    declared = {item["name"]: item["sha256"] for item in manifest["declared_inputs"]}

    assert moved["reference_run"] == "run-21"
    assert moved["moved"] == []
    assert sorted(moved["shared_with_reference"]) == sorted(SHARED_WITH_RUN_21)
    assert sorted(moved["unchanged"]) == sorted(SHARED_WITH_RUN_21)
    for name in SHARED_WITH_RUN_21:
        assert declared[name] == reference[name], name
    assert sorted(moved["not_in_the_reference"]) == sorted(
        set(DECLARED_SOURCES) - set(SHARED_WITH_RUN_21)
    )


def test_the_bound_profile_is_the_state_version_profile_the_fixture_declares() -> None:
    """The profile identity is recomputed from the bytes at the pinned commit.

    It is the fixture's choice and not the paper's: public_population/run.py
    admits all five of its plans under STATE_VERSION_PROFILE, and this cell
    declares the same bytes rather than choosing a profile for the producer.
    """

    contract = _contract()
    manifest = _manifest()
    profile_bytes = _git_show("src/malleus/profiles/state-version.json")
    profile = json.loads(profile_bytes)

    assert contract["history"]["profile_id"] == "state-version"
    assert contract["history"]["profile_sha256"] == _canonical_digest(profile_bytes)
    assert manifest["history_profile"]["profile_identity"] == _canonical_digest(
        profile_bytes
    )
    assert manifest["history_profile"]["semantic_unit"] == profile["semantic_unit"]
    assert manifest["history_profile"]["origin"] == profile["origin"]
    assert profile["ontology_roles"]["event"] == []
    assert contract["history"]["admitted_families"] == ["entities", "relations"]
    # And it is not the document cell's profile.
    prior = json.loads(
        (RUN_21 / "producer-input-manifest.json").read_bytes()
    )["history_profile"]
    assert prior["profile_id"] == "source-assertion"
    assert prior["profile_identity"] != manifest["history_profile"]["profile_identity"]


def test_the_gate_pieces_are_verified_at_the_pinned_commit() -> None:
    gate = _contract()["core_gate"]
    pieces = gate["verified_pieces"]
    commit = _commit()
    tree = gate["execution_baseline"]["core_tree"]

    assert sorted(gate["required_pieces"]) == REQUIRED_PIECES
    assert sorted(pieces) == REQUIRED_PIECES
    for name, piece in sorted(pieces.items()):
        assert piece["core_commit"] == commit, name
        assert piece["core_tree"] == tree, name
        assert piece["paper_audit"] == "DIGEST_PINNED", name
    assert pieces["NASCENT_PROJECT_PLAYBOOK"]["skill_sha256"] == _digest(
        _git_show(".claude/skills/malleus-acolyte/SKILL.md")
    )
    assert pieces["GROUNDED_PACKS_AND_PACK_GROUNDING"]["pack_sha256"] == {
        name: _digest(_git_show(f"ontology/packs/{name}.yaml"))
        for name in ("chronology", "metrology", "research")
    }
    assert pieces["EVENT_FAMILY_ADMISSION"]["event_role"] == []
    assert pieces["EVENT_FAMILY_ADMISSION"]["admitted_families"] == [
        "entities",
        "relations",
    ]


def test_the_derivation_piece_is_the_plan_compilers_and_not_the_adapters() -> None:
    """The one gate piece the source shape replaces, with its reasons recomputed.

    The document adapter's content checks bind a capture. A plan the producer
    wrote never reaches them, so requiring DERIVATION_CONTENT_CHECKS here would
    pin a mechanism this cell does not run. What binds is the plan compiler's
    enum, and the piece carries it read from the enum at the pinned commit.
    """

    gate = _contract()["core_gate"]
    piece = gate["verified_pieces"]["PLAN_DERIVATION_CHECKS"]
    body = POPULATION_ENUM_BLOCK.search(
        _git_show("src/malleus/_contract_pipeline/population.py").decode("utf-8")
    )
    assert body is not None
    reasons = sorted(match.group("name") for match in ENUM_MEMBER.finditer(body.group("body")))

    assert "DERIVATION_CONTENT_CHECKS" not in gate["required_pieces"]
    assert "DERIVATION_CONTENT_CHECKS" in gate["required_pieces_moved"]["removed"]
    assert piece["refusal_reasons"] == reasons
    for reason in ("ABSENT_PATH", "UNDERIVED_FIELD", "UNLISTED_SOURCE", "UNRETAINED_SOURCE"):
        assert reason in reasons
        assert reason in piece["field_level_checks"]
    assert piece["plan_compiler_sha256"] == _digest(
        _git_show("src/malleus/_contract_pipeline/population.py")
    )
    # The locator is the one thing Core does not resolve, and the piece says so
    # rather than leaving the reviewer to assume it is checked.
    assert "THE_LOCATOR_IS_FREE_TEXT" in piece["not_checked_by_core"]
    assert (
        "row:N:field" == _contract()["source"]["locator_form"]
    )


def test_the_structural_bundle_the_runner_admits_through_is_pinned() -> None:
    piece = _contract()["core_gate"]["verified_pieces"]["STRUCTURAL_HISTORY_BUNDLE"]

    assert sorted(piece["file_sha256"]) == sorted(BUNDLE_PATHS)
    for path, digest in sorted(piece["file_sha256"].items()):
        assert digest == _digest(_git_show(path)), path
    assert piece["admission_path"] == (
        "CREATE_STRUCTURAL_HISTORY_THEN_ADMIT_STRUCTURAL_CHANGE"
    )


def test_the_two_core_entries_are_read_at_the_pin_and_land() -> None:
    changes = _changes()

    assert sorted(changes) == list(CHANGE_IDS)
    for change_id in READ_AT_THE_PIN_CORE_CHANGE_IDS:
        entry = changes[change_id]
        assert entry["carried_from"] == "run-21", change_id
        assert entry["pin_status"] == LANDED, change_id
    reporting = changes["CORE_19_HONEST_REPORTING"]
    assert reporting["reasons"] == ["RECORDS_NOT_REHYDRATABLE"]
    assert all(reporting["observed"].values())
    # Core-19 is carried and half of it is the document adapter's; the entry
    # says which half binds this cell rather than claiming the whole of it does.
    assert any(
        "RECORDS_NOT_REHYDRATABLE_IS_THE_PLAN_COMPILERS_AND_BINDS_THIS_CELL" == item
        for item in reporting["binds_this_cell"]
    )
    preflight = changes["CORE_20_REFUSAL_LIST_PREFLIGHT"]
    assert preflight["observed"]["reasons_absent_from_the_paragraph"] == []
    assert preflight["observed"]["guard_derives_from_both_enums"] is True
    assert preflight["governance_entry_landed"] is True


def test_the_pack_versions_are_the_ones_at_the_pinned_commit() -> None:
    entry = _changes()["PACKS_0_3_0"]
    version_line = re.compile(r"^version: (?P<version>\S+)\s*$", re.M)
    observed = {}
    for name in ("metrology", "research"):
        match = version_line.search(_git_show(f"ontology/packs/{name}.yaml").decode())
        assert match is not None, name
        observed[name] = match.group("version")

    assert entry["versions"] == observed
    assert entry["moved_since_run_08"] == sorted(
        name
        for name, version in observed.items()
        if version != entry["expected_versions"][name]
    )


def test_the_producer_model_fields_are_run_21s() -> None:
    producer = _contract()["producer"]
    prior = json.loads((RUN_21 / "run-contract.json").read_bytes())["producer"]
    entry = _changes()["OPUS_5_PRODUCER_AT_SHOP_01"]

    for field, value in MODEL_FIELDS.items():
        assert producer[field] == value, field
        assert prior[field] == value, field
        assert entry[field] == value, field
    assert entry["model_fields_moved"] == []
    assert entry["kind"] == "MODEL_CELL"
    assert entry["harness_matched_cell"] == "run-21"
    assert _manifest()["producer"] == producer


def test_the_spawn_message_tells_the_producer_the_source_shape_and_nothing_more() -> None:
    message = SPAWN_MESSAGE.read_text(encoding="utf-8")

    assert "work/population-plans/" in message
    assert "document-population.json" not in message
    assert "selected-reading.json" not in message
    assert "profile-state-version.json" in message
    assert "the twelve declared inputs" in message
    for name in (
        "warehouse.jsonl",
        "inventory-units.csv",
        "invoices.csv",
        "payments.jsonl",
        "supplier-order-history.jsonl",
    ):
        assert f"sources/{name}" in message, name
    # The producer is told nothing about the questions, the binding, or a type.
    for withheld in ("CQ-S", "SupplierOrderState", "settle", "competency"):
        assert withheld not in message, withheld
    assert _changes()["STOP_RULE_CLARIFIED"]["sentence"] in " ".join(message.split())


def test_the_questions_are_frozen_withheld_and_exactly_the_four() -> None:
    questions = json.loads(QUESTIONS_PATH.read_bytes())

    assert questions["schema"] == "malleus.paper-v4.competency-questions/v2"
    assert questions["status"] == "FROZEN_BEFORE_PRODUCER"
    assert questions["visibility"] == "WITHHELD_FROM_PRODUCER_UNTIL_POST_REPLAY"
    assert [item["id"] for item in questions["questions"]] == QUESTION_IDS
    assert questions["scope"] == {
        "answer_surface": "REPLAY_DERIVED_NATIVE_GRAPH_QUERY_WITH_PROVENANCE_TRACE",
        "source_support": "THE_FIVE_SMALL_SHOP_SOURCE_FILES",
        "free_form_synthesis": "EXCLUDED",
    }
    semantics = {item["id"]: item["required_semantics"] for item in questions["questions"]}
    assert semantics["CQ-S1"] == ["payment", "invoice", "settlement_relation"]
    assert semantics["CQ-S2"] == [
        "supplier_order",
        "current_state",
        "superseded_state",
        "ordered_quantity",
    ]
    assert semantics["CQ-S3"] == [
        "sales_order",
        "inventory_unit",
        "containment_relation",
        "product",
    ]
    assert semantics["CQ-S4"] == ["source", "derivation_locator", "current_record"]
    assert _contract()["query"]["questions"]["ids"] == QUESTION_IDS
    assert _contract()["query"]["producer_visibility"] == "WITHHELD"


def test_the_two_half_bound_questions_are_declared_before_the_producer_runs() -> None:
    """CQ-S2's history half and CQ-S4's derivation half, and the executor unchanged.

    Both are the boundary of a type-only binding and both are recorded here
    rather than discovered from a row count after the run. The executor is
    run-21's bytes, so neither can have been reached by extending it.
    """

    declared = _contract()["query"]["questions_the_executor_answers_only_in_part"]

    assert sorted(declared) == sorted(HALF_BOUND_QUESTIONS)
    for question_id in HALF_BOUND_QUESTIONS:
        entry = declared[question_id]
        assert entry["binds_to"] == "CURRENT_GRAPH_TYPES_ONLY", question_id
        assert "trace-summary.json" in entry["judged_from"], question_id
        assert entry["executor_not_extended"], question_id
    assert (HERE / "native_query.py").read_bytes() == (
        RUN_21 / "native_query.py"
    ).read_bytes()
    assert "CQ-S2" in REVIEW_TASK.read_text(encoding="utf-8")
    assert "CQ-S4" in REVIEW_TASK.read_text(encoding="utf-8")


def test_the_review_task_moves_the_evidence_surface_to_the_rows() -> None:
    task = REVIEW_TASK.read_text(encoding="utf-8")
    record = REVIEW_RECORD.read_text(encoding="utf-8")

    for placeholder in REVIEW_PLACEHOLDERS:
        assert placeholder in task, placeholder
    for placeholder in ("{{ROWS_CQ_S1}}", "{{ROWS_TOTAL}}"):
        assert placeholder in record, placeholder
    # The task names run-21 twice: the line saying what it was translated from
    # and the line saying the input manifest is built in that cell's shape.
    # No run-21 input, result or figure reaches this reviewer.
    assert task.count("run-21") == 2
    assert "paper-v4/evaluation-v4/run-21/review-task.md" in task
    assert "built at freeze in run-21's shape" in task
    assert "selected reading" not in task.lower()
    assert "row:N:field" in task
    for name in (
        "warehouse.jsonl",
        "inventory-units.csv",
        "invoices.csv",
        "payments.jsonl",
        "supplier-order-history.jsonl",
    ):
        assert name in task, name
    # The three tokens the record's rationale opens with, and the one that is gone.
    for token in (
        "VALUE_MATCHES_ROW",
        "VALUE_DIFFERS_FROM_ROW",
        "LOCATOR_NOT_RESOLVABLE",
        "DERIVATION_LOCAL",
        "SUBJECT_IN_ROW",
        "NO_SUBJECT_IN_ROW",
    ):
        assert token in task, token
        assert token in record, token
    assert "DIGEST_OK" not in task
    assert "statement_sha256" in task  # named only to say it does not exist here
    assert "public_population" in task  # the answer key the reviewer must not open
    duties = _contract()["evaluation"]["review_task"]["duties"]
    assert duties == [
        "ROW_OPENED_AND_THE_VALUE_COMPARED_PER_ROW",
        "DERIVATION_LOCALITY_PER_RELATION_ROW",
        "SUBJECT_IN_ROW_PER_SUBJECT_AND_ENTITY_ROW",
    ]


def test_the_frozen_v2_review_protocol_refuses_this_cell_and_the_contract_says_so() -> None:
    """The one thing this cell could not translate, stated as a refusal, not a gap.

    The frozen validator pins the evidence surface to the selected reading, the
    fixed-identity keys to the document cell's three, and a record's question ids
    to the protocol's. None of the three can hold for rows, so no protocol was
    written for this cell: any file it could write would be refused by the very
    validator that makes a protocol worth having.
    """

    protocol = json.loads(REVIEW_PROTOCOL_V2.read_bytes())
    validator = REVIEW_VALIDATOR.read_text(encoding="utf-8")
    declared = _contract()["evaluation"]["review_protocol"]

    assert protocol["question_ids"] == ["CQ-01", "CQ-02", "CQ-03", "CQ-04"]
    assert protocol["evidence_surface"]["authoritative"] == "SELECTED_READING_TEXT_LAYER"
    assert protocol["evidence_surface"]["locator_kind"] == "SELECTED_READING_BLOCK_ID"
    assert '!= "SELECTED_READING_TEXT_LAYER"' in validator
    assert '!= "SELECTED_READING_BLOCK_ID"' in validator
    assert 'protocol["question_ids"]' in validator
    assert declared["status"] == "OPEN_NO_FROZEN_PROTOCOL_BINDS_THIS_CELL"
    assert declared["blocked_by"] == (
        "paper-v4/evaluation-v4/review.py::validate_protocol"
    )
    assert "decision_for_luis" in declared
    assert "review_protocol_sha256" in REVIEW_RECORD.read_text(encoding="utf-8")
    # And the frozen protocol is not edited by this cell.
    assert _digest(REVIEW_PROTOCOL_V2.read_bytes()) == (
        "sha256:88b69f6e80a3b9eac3a2c990178186df9c52fed3ced5c4e020162b0c202fa795"
    )


def test_the_census_note_names_every_field_that_has_no_reading_for_rows() -> None:
    note = _contract()["population"]["census_not_reported"]

    assert _contract()["population"]["census"] is None
    assert _contract()["population"]["results_not_written"] == ["census.json"]
    census = json.loads((RUN_21 / "results/census.json").read_bytes())
    for field in ("blocks_total", "assertions", "provenance_coverage"):
        assert field in census, field
        assert field in note, field
    for absent in ("subject", "statement_sha256", "assertion_locator"):
        assert absent in note, absent
    # What survives as a count is named too, so the note is not only a denial.
    for survives in ("records by family", "gaps by kind"):
        assert survives in note, survives


def test_the_cell_has_not_run_and_its_result_directories_are_empty() -> None:
    """Frozen-run guards, read against an empty cell.

    Every figure a closed cell's tests hold is a figure this one does not have
    yet. The guard is the absence: a results file appearing before the overseer
    launches the producer would mean a run happened outside the protocol.
    """

    for name in PENDING_RESULTS:
        directory = HERE / name
        assert not directory.exists() or not any(directory.iterdir()), name
    assert _contract()["status"] == "READY_FOR_PRODUCER"
    assert _contract()["launch_log"]["path"] == (
        "paper-v4/experiment-v4/shop-01/results/launch-log.json"
    )
    assert not (HERE / "results/launch-log.json").exists()
    assert not (EVALUATION / "shop-01" / "review-input-manifest.json").exists()
    assert not (EVALUATION / "shop-01" / "review-record.preliminary.md").exists()


def test_run_21_is_frozen_and_this_cell_moved_none_of_its_bytes() -> None:
    for path, digest in sorted(RUN_21_FROZEN.items()):
        assert _digest((RUN_21 / path).read_bytes()) == digest, path


def test_shop_01_is_an_active_test_path() -> None:
    manifest = json.loads(ACTIVE_TEST_MANIFEST.read_bytes())

    assert "paper-v4/experiment-v4/shop-01" in manifest["paths"]
    assert "paper-v4/experiment-v4/run-21" in manifest["paths"]
    for value in manifest["paths"]:
        assert (ROOT / value).exists(), value


def test_the_paper_ledger_opens_this_cell_at_e_0201() -> None:
    ledger = PAPER_LEDGER.read_text(encoding="utf-8")
    headings = re.findall(r"^### (E-\d{4})", ledger, re.M)

    assert "E-0201" in headings
    assert headings.index("E-0201") == headings.index("E-0200") + 1
    entry = ledger.split("### E-0201", 1)[1]
    assert "shop-01" in entry
    assert "E-0202" not in entry
    for fact in ("rows instead of prose", "census", "falsifier", "expected"):
        assert fact in entry.lower(), fact


@pytest.mark.parametrize("change_id", CHANGE_IDS)
def test_every_change_entry_says_whether_it_is_carried(change_id: str) -> None:
    entry = _changes()[change_id]

    if change_id in THIS_CELL_CHANGE_IDS:
        assert entry.get("carried_from") in (None, "the v4.11 finding"), change_id
    else:
        assert entry["carried_from"] == "run-21", change_id
    assert entry["id"] == change_id
    assert entry.get("detail")
