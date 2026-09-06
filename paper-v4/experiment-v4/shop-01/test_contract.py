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

This cell has run and is frozen. Every file under ``ontology-run/`` and
``results/`` is held by digest, the set is closed, and each figure the entry for
this cell states is recomputed here from those files and from the private launch
log they were copied out of. Nothing is withheld: the five sources are the
repository's own tracked fixtures, so the reading ladder run-21 runs against a
private text layer has nothing to measure and is not run.
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
# The exact bytes this cell leaves in the repository. A frozen run is a closed
# set: a file added, removed or rewritten later is a different run.
FROZEN_ARTIFACTS = {
    "ontology-run/attempt-01-diagnostic.json": (
        "sha256:d1040ca7175f282d24add722ec5122166944b69ad7220945f549712324651092"
    ),
    "ontology-run/grounding-receipt.json": (
        "sha256:aa9a68fa9e1925059c14db415f3186ee02e1857e9edcfe75776102c47607b57a"
    ),
    "ontology-run/ontology-01.yaml": (
        "sha256:e795d73122109e75b1301660c347155cafdd8156a8c54f6c025bd4d35becdd1a"
    ),
    "ontology-run/population-surface.json": (
        "sha256:9de0fd563e41be3743b11a14d83e8b1932083c3c1f64f4788cb63dc6dc5e4f44"
    ),
    "ontology-run/result.json": (
        "sha256:590e6fff4fe32dc133a635cfac664bc29fca19877c7933bf3ab2d315770623b5"
    ),
    "ontology-run/validated-contract.json": (
        "sha256:e3f9796e5abb01382af4bb0e12284b9185110d3b57480273b2edf8d9a4d74309"
    ),
    "results/contract-identity.json": (
        "sha256:1820e793855cec81eaea7bd881970d237444dac57f68aeaf1faa15992c741bba"
    ),
    "results/export-records.json": (
        "sha256:8fc4e29a55ed968cedd7d727c108312ae5dd86c305edc6f10fbfcfb4e3ba917e"
    ),
    "results/gaps.json": (
        "sha256:57dda7d4d7a7c05dafe94f5c9640d9552e68bb4f9a5319f4410223e3b5f09def"
    ),
    "results/launch-log.json": (
        "sha256:3e6d26b102f0f8e27835b837c96dd08a7d3322b23bbc238036eba1e919a5092b"
    ),
    "results/native-query-binding.json": (
        "sha256:7f3dfda2e2196320db662593a732a4d8ce434846b2c6f89d60f2a3a47cf38d30"
    ),
    "results/paper-events.json": (
        "sha256:90283b14dbbb101de8ea859e004482e5e35cdb48a3d9427ab273f9965e4995e7"
    ),
    "results/population-plan.01-inventory.json": (
        "sha256:c49750378e01b7c2251a260a164ed85b257dc2639fbe110877db4db350d9c4c6"
    ),
    "results/population-plan.02-warehouse.json": (
        "sha256:9850f3f5d8373113b465f94f7b9cab0fa2ab457a67f84ac0af4c657b7d114722"
    ),
    "results/population-plan.03-supplier-orders.json": (
        "sha256:64aee1d65fd10944095b4afd4d5ec34c5f31af01006f1e160c63099dfa938897"
    ),
    "results/population-plan.04-invoices-payments.json": (
        "sha256:4b67971c6762fab2a4730b07df7a95e37377e93d6e13e8f118b9e87550a3b4ee"
    ),
    "results/query-binding.acceptance.json": (
        "sha256:e5a0a0eaebb430231987577df2c3f32e52057ade78e3c6ade984365ace9f2c59"
    ),
    "results/query-result.json": (
        "sha256:85adb10bcc7f2d3d8dabbc899fbe01f98d038950382d2f0d9326ff576d022d2c"
    ),
    "results/query-trace-summary.json": (
        "sha256:5118a16c6e938261b1f4fe99ec7adc9923ebc83ca348f658f7e787378aab3fdc"
    ),
    "results/query-type-sets.json": (
        "sha256:72a5ed45a5d513331ba17dd021c104b63a66305e79a6ebd501a75f9a2f297d66"
    ),
    "results/query-type-sets.note.json": (
        "sha256:6b467cebbdf5c4d4192462b32e00107fa3122e89a037fb56a61d5a08a65963ef"
    ),
    "results/replay-receipt.json": (
        "sha256:6dc2bf18e88150387caf646f64fad6a79e921fd467da3dbd6461f422fa5580c4"
    ),
    "results/run-result.json": (
        "sha256:28f1eb29e56767b9edbfa76f15b51a59050591835b54981745e0aa3b473ce48f"
    ),
    "results/trace-summary.json": (
        "sha256:a3d00069a86f073340f227f837c30084c8222120b285d1ad581ce24a4c66e970"
    ),
    "results/transaction-time.txt": (
        "sha256:913277dbd653bc78820a98e59ea0ea5b7c4efcb481001971d7b56ba5d35e5fd3"
    ),
    "results/usage.json": (
        "sha256:9c203fabd7fa092980cbf305ef3826beddf3a7915950adeb8dadb641b6a02194"
    ),
    "results/withheld-artifacts.json": (
        "sha256:7e98b861866b890569df0048f60543fae31f8e3fef05baa5b54e02d62ae15cc4"
    ),
}

# The private cell the public copies were taken from. Every figure below is
# recomputed against it, so a public file edited after the freeze fails here.
PRIVATE_CELL = ROOT / "private" / "paper-v4-v4-shop-01"
RETAINED_PLANS_FILES = (
    "01-inventory.json",
    "02-warehouse.json",
    "03-supplier-orders.json",
    "04-invoices-payments.json",
)
RETAINED_PLANS = tuple(f"population-plan.{name}" for name in RETAINED_PLANS_FILES)
FACT_COUNT = 945
SURFACE_FAMILIES = {"ENTITY": 7, "EVENT": 1, "RELATION": 1}
ADMITTED_FAMILIES = ["entities", "relations"]
RUNNER_STATUSES = ["REFUSED", "REFUSED", "REFUSED", "ADMITTED_AND_REPLAYED"]
EXECUTION_COMMIT = "0f013ba"
GATE_STATUSES = ["ACCEPTED"]
GRAPH = {
    "entities": 7,
    "event_participations": 0,
    "events": 0,
    "relations": 2,
    "signals": 0,
}
GAPS_BY_KIND = {"RELATION_ABSENT": 2, "TYPE_ABSENT": 11}
LEDGER_EVENT_COUNT = 38
WITNESSES_TRACED = 9
QUERY_CASES = 56
QUERY_CASES_BY_KIND = {"ENTITY": 11, "RELATION": 45}
ROWS_BY_QUESTION = {"NQ-CQ-S1": 5, "NQ-CQ-S2": 1, "NQ-CQ-S3": 2, "NQ-CQ-S4": 9}
ROWS_TOTAL = 17
ROWS_BY_KIND = {"ENTITY": 13, "RELATION": 4}
USAGE_STAGES = [
    "ONTOLOGY_ATTEMPT_01",
    "POPULATION",
    "POPULATION_CORRECTION_01_PLAN_LOADER_COORDINATES",
    "POPULATION_CORRECTION_02_FIELDS_NOT_CLOSED",
    "POPULATION_CORRECTION_03_PROFILE_IDENTITY",
]
USAGE_TOKENS = [138864, 50777, 11653, 27128, 22321]
PRODUCER_TOTAL_TOKENS = 250743
# The record template keeps its placeholders; the task's are substituted at
# freeze and none may survive.
RECORD_PLACEHOLDERS = (
    "{{ROWS_CQ_S1}}",
    "{{ROWS_CQ_S2}}",
    "{{ROWS_CQ_S3}}",
    "{{ROWS_CQ_S4}}",
    "{{ROWS_TOTAL}}",
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
    # The status the contract carries after the freeze. Run-21's frozen contract
    # reads the same value: the freeze writes results and a ledger entry, and no
    # closed cell of this loop moves its contract's status or adds a field for
    # the frozen state, so shop-01's is left as run-21's is.
    assert contract["status"] == "READY_FOR_PRODUCER"
    assert (
        json.loads((RUN_21 / "run-contract.json").read_bytes())["status"]
        == contract["status"]
    )
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

    # The task was instantiated at freeze and no placeholder survived it. The
    # blank record is still a template and keeps its own.
    assert "{{" not in task
    for placeholder in RECORD_PLACEHOLDERS:
        assert placeholder in record, placeholder
    assert f"{ROWS_BY_QUESTION['NQ-CQ-S1']} rows for CQ-S1" in task
    assert f"{ROWS_TOTAL} in all" in task
    assert f"the {WITNESSES_TRACED} witnesses the returned rows use" in task
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


def test_the_frozen_artifact_set_is_exact_and_digest_pinned() -> None:
    """The closed set. A file added, removed or rewritten later is another run."""

    for name in ("ontology-run", "results"):
        directory = HERE / name
        assert directory.is_dir()
        observed = sorted(
            f"{name}/{path.name}"
            for path in directory.iterdir()
            if path.is_file() and path.suffix != ".pyc" and path.name != ".gitkeep"
        )
        expected = sorted(
            relative for relative in FROZEN_ARTIFACTS if relative.startswith(f"{name}/")
        )
        assert observed == expected, name
    for relative, digest in sorted(FROZEN_ARTIFACTS.items()):
        assert _digest((HERE / relative).read_bytes()) == digest, relative
    assert _contract()["launch_log"]["path"] == (
        "paper-v4/experiment-v4/shop-01/results/launch-log.json"
    )
    # No census is written for rows, and the contract said so before the run.
    assert _contract()["population"]["results_not_written"] == ["census.json"]
    assert not (HERE / "results/census.json").exists()


def test_nothing_is_withheld_and_the_record_says_why() -> None:
    """The one part of run-21's freeze that does not translate.

    Run-21 withholds eight files because each reproduces the private text layer,
    and it measures a normalized character run against every reading block to
    prove the public ones do not. This cell's evidence surface is five tracked
    fixtures in the repository, so there is no private text to reproduce, the
    ladder has nothing to measure and it is not run. The record carries an empty
    list and the reason rather than a measurement that would mean nothing.
    """

    record = json.loads((HERE / "results/withheld-artifacts.json").read_bytes())

    assert record["schema"] == "malleus.paper-v4.shop-01-withheld-artifacts/v1"
    assert record["run_id"] == "shop-01"
    assert record["withheld"] == []
    assert "public" in record["reason"]
    declared = {item["name"]: item["source"] for item in _manifest()["declared_inputs"]}
    for path in _contract()["source"]["paths"]:
        assert (ROOT / path).exists(), path
        assert path in declared.values(), path


def test_the_public_launch_log_is_the_private_one_with_the_review_section_empty() -> None:
    public = json.loads((HERE / "results/launch-log.json").read_bytes())
    private = json.loads((PRIVATE_CELL / "launch-log.json").read_bytes())

    assert public["review"] == {}
    assert public["schema"] == "malleus.paper-v4.producer-launch-log/v2"
    assert public["run"] == "shop-01"
    assert set(public) == set(_contract()["launch_log"]["required_keys"])
    assert public["launches"] == private["launches"]
    assert public["gate"] == private["gate"]
    assert public["runner"] == private["runner"]
    assert public["query"] == private["query"]
    assert {**public, "review": private["review"]} == private


def test_the_runner_admitted_at_the_fourth_attempt_at_one_execution_commit() -> None:
    log = json.loads((HERE / "results/launch-log.json").read_bytes())
    gate = log["gate"][-1]

    assert [entry["status"] for entry in log["gate"]] == GATE_STATUSES
    assert gate["fact_count"] == FACT_COUNT
    assert gate["surface_families"] == SURFACE_FAMILIES
    assert gate["families_admitted"] == ADMITTED_FAMILIES
    assert gate["citation_check"]["fabricated"] == 0
    assert gate["citation_check"]["unverified"] == []
    assert gate["diagnostic_returns_used"] == 0
    assert [entry["status"] for entry in log["runner"]] == RUNNER_STATUSES
    assert {entry["execution_commit"] for entry in log["runner"]} == {EXECUTION_COMMIT}
    assert log["runner"][-1]["structural_diagnostic_returns_used"] == 1
    assert (
        log["runner"][-1]["structural_diagnostic_returns_used"]
        <= _contract()["producer"]["max_compiler_diagnostic_returns"]
    )
    # The two refusals that are not structural returns say so in the log.
    uncounted = [
        entry
        for entry in log["runner"]
        if entry.get("counts_against_diagnostic_budget") is False
    ]
    assert [entry["attempt"] for entry in uncounted] == [1, 3]


def test_the_usage_record_agrees_with_the_launch_log() -> None:
    usage = json.loads((HERE / "results/usage.json").read_bytes())
    log = json.loads((HERE / "results/launch-log.json").read_bytes())
    launch = log["launches"][0]

    assert usage["schema"] == "malleus.paper-v4.producer-usage/v1"
    assert usage["run"] == "shop-01"
    assert usage["model_id"] == MODEL_FIELDS["model_id"]
    assert usage["model_family"] == MODEL_FIELDS["model_family"]
    assert usage["review"] == {}
    assert [stage["stage"] for stage in usage["stages"]] == USAGE_STAGES
    assert [stage["tokens"] for stage in usage["stages"]] == USAGE_TOKENS
    assert usage["producer_total_tokens"] == PRODUCER_TOTAL_TOKENS
    assert usage["producer_total_tokens"] == launch["usage_by_resume"][-1]["tokens"]
    assert sum(stage["tokens"] for stage in usage["stages"]) == PRODUCER_TOTAL_TOKENS
    assert usage["stages"][0]["tokens"] == launch["usage_cumulative"]["tokens"]


def test_the_query_result_returns_the_frozen_rows_over_nine_witnesses() -> None:
    result = json.loads((HERE / "results/query-result.json").read_bytes())
    trace = json.loads((HERE / "results/query-trace-summary.json").read_bytes())
    log = json.loads((HERE / "results/launch-log.json").read_bytes())

    assert result["schema"] == _contract()["query"]["result_schema"]
    assert [query["question_id"] for query in result["queries"]] == QUESTION_IDS
    rows_by_question = {
        query["query_id"]: len(query["rows"]) for query in result["queries"]
    }
    assert rows_by_question == ROWS_BY_QUESTION == log["query"]["rows_by_question"]
    assert sum(rows_by_question.values()) == ROWS_TOTAL == log["query"]["rows_total"]
    rows_by_kind: dict[str, int] = {}
    for query in result["queries"]:
        for row in query["rows"]:
            rows_by_kind[row["kind"]] = rows_by_kind.get(row["kind"], 0) + 1
    assert rows_by_kind == ROWS_BY_KIND == log["query"]["rows_by_kind"]
    assert trace["witnesses_traced"] == WITNESSES_TRACED == log["query"]["witnesses_traced"]
    assert len(trace["records"]) == WITNESSES_TRACED
    assert result["forbidden_attempts"] == log["query"]["forbidden_attempts"]
    assert result["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert log["query"]["rows_from_more_than_one_case"] == 0
    assert result["inputs"]["query_binding_sha256"] == _digest(
        (HERE / "results/native-query-binding.json").read_bytes()
    )


def test_the_binding_was_frozen_at_acceptance_and_executed_unchanged() -> None:
    accepted = json.loads((HERE / "results/query-binding.acceptance.json").read_bytes())
    executed = json.loads((HERE / "results/native-query-binding.json").read_bytes())
    result = json.loads((HERE / "results/run-result.json").read_bytes())
    log = json.loads((HERE / "results/launch-log.json").read_bytes())
    type_sets = json.loads((HERE / "results/query-type-sets.json").read_bytes())

    assert accepted["bound_at_stage"] == executed["bound_at_stage"] == "ONTOLOGY_ACCEPTANCE"
    assert executed["schema"] == _contract()["query"]["binding_schema"]
    assert accepted["bound_after_replay_receipt_sha256"] == "PENDING"
    assert executed["bound_after_replay_receipt_sha256"] == result["replay_receipt_sha256"]
    assert accepted["cases_sha256"] == executed["cases_sha256"] == log["query"]["cases_sha256"]
    assert log["query"]["binding_at_acceptance_sha256"] == _digest(
        (HERE / "results/query-binding.acceptance.json").read_bytes()
    )
    assert log["query"]["type_sets_sha256"] == _digest(
        (HERE / "results/query-type-sets.json").read_bytes()
    )
    assert log["query"]["bound_at"] < log["launches"][0]["phase_two"]["dispatched_at"]
    assert sorted(type_sets) == QUESTION_IDS
    assert sum(len(query["cases"]) for query in executed["queries"]) == QUERY_CASES
    assert log["query"]["cases"] == QUERY_CASES
    assert log["query"]["cases_by_kind"] == QUERY_CASES_BY_KIND
    cases_by_kind: dict[str, int] = {}
    for query in executed["queries"]:
        for case in query["cases"]:
            cases_by_kind[case["kind"]] = cases_by_kind.get(case["kind"], 0) + 1
    assert cases_by_kind == QUERY_CASES_BY_KIND
    assert log["query"]["closure_preflight"]["status"] == "ACCEPTED"
    assert log["query"]["closure_preflight"]["omissions"] == {}


def test_the_run_result_is_admitted_replayed_and_reports_no_census() -> None:
    result = json.loads((HERE / "results/run-result.json").read_bytes())
    events = json.loads((HERE / "results/paper-events.json").read_bytes())
    ontology_run = json.loads((HERE / "ontology-run/result.json").read_bytes())

    assert result["schema"] == "malleus.paper-v4.shop-01-result/v1"
    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["run_id"] == "shop-01"
    assert result["actor_id"] == "actor:overseer-shop-01"
    assert (
        result["transaction_time"]
        == (HERE / "results/transaction-time.txt").read_text(encoding="utf-8").strip()
    )
    assert result["ontology_sha256"] == ontology_run["accepted_ontology_sha256"]
    assert result["graph"] == GRAPH
    assert result["gaps_by_kind"] == GAPS_BY_KIND
    assert sum(result["gaps_by_kind"].values()) == 13
    assert result["reopen_matches_admitted"] == {"export_records": True, "receipt": True}
    assert result["admitted_receipt_sha256"] == result["replay_receipt_sha256"]
    assert result["replay_receipt_sha256"] == _digest(
        (HERE / "results/replay-receipt.json").read_bytes()
    )
    assert result["export_records_sha256"] == _digest(
        (HERE / "results/export-records.json").read_bytes()
    )
    assert result["trace_summary_sha256"] == _digest(
        (HERE / "results/trace-summary.json").read_bytes()
    )
    assert result["ledger_event_count"] == LEDGER_EVENT_COUNT
    assert result["records_traced"] == WITNESSES_TRACED
    assert result["census"] is None
    assert result["data_sources"] == _contract()["source"]["source_sha256"]
    assert [plan["file"] for plan in result["plans"]] == list(RETAINED_PLANS_FILES)
    assert events["events"][0]["ontology_sha256"] == result["ontology_sha256"]
    assert events["events"][0]["contract_identity"] == result["contract_identity"]


def test_the_contract_identity_is_one_value_across_the_cell() -> None:
    """The coordinate the parent supplied, read back from every file that carries it."""

    identity = json.loads((HERE / "results/contract-identity.json").read_bytes())
    log = json.loads((HERE / "results/launch-log.json").read_bytes())
    result = json.loads((HERE / "results/run-result.json").read_bytes())
    phase_two = log["launches"][0]["phase_two"]

    assert identity["contract_identity"] == phase_two["contract_identity"]
    assert identity["contract_identity"] == result["contract_identity"]
    assert identity["validated_fact_set_sha256"] == log["gate"][-1]["validated_fact_set_sha256"]
    assert identity["validated_fact_set_sha256"] == result["validated_fact_set_sha256"]
    for name in RETAINED_PLANS:
        plan = json.loads((HERE / "results" / name).read_bytes())
        assert plan["contract_identity"] == identity["contract_identity"], name
        assert plan["grammar"] == _contract()["population"]["plan_grammar"], name


def test_the_ontology_run_result_records_one_accepted_attempt() -> None:
    result = json.loads((HERE / "ontology-run/result.json").read_bytes())
    producer = result["producer"]
    attempts = result["attempts"]
    log = json.loads((HERE / "results/launch-log.json").read_bytes())

    assert result["schema"] == "malleus.paper-v4.ontology-run-result/v1"
    assert result["status"] == "ACCEPTED"
    assert result["run_id"] == "shop-01"
    assert result["core"] == {
        "commit": _contract()["core_gate"]["execution_baseline"]["core_commit"],
        "tree": _contract()["core_gate"]["execution_baseline"]["core_tree"],
    }
    assert result["producer_input_manifest_sha256"] == _digest(MANIFEST_PATH.read_bytes())
    assert producer["kind"] == "CLAUDE_CODE_FRESH_SUBAGENT"
    for field, value in MODEL_FIELDS.items():
        assert producer[field] == value, field
    assert producer["questions_visible"] is False
    assert producer["fallback_used"] is False
    assert producer["hand_repair_used"] is False
    assert producer["diagnostic_returns"] == len(log["gate"]) - 1
    assert [item["status"] for item in attempts] == ["ACCEPTED"]
    for item in attempts:
        assert _digest((ROOT / item["ontology_path"]).read_bytes()) == item["ontology_sha256"]
        assert _digest((ROOT / item["diagnostic_path"]).read_bytes()) == item["diagnostic_sha256"]
    accepted = result["accepted"]
    assert accepted["fact_count"] == FACT_COUNT
    assert accepted["population_surface_families"] == SURFACE_FAMILIES
    assert accepted["families_admitted"] == ADMITTED_FAMILIES
    assert result["citation_check"] == log["gate"][-1]["citation_check"]
    assert result["citation_check"]["fabricated"] == 0


def test_the_accepted_surface_carries_the_seven_entity_names_and_the_one_relation() -> None:
    surface = json.loads((HERE / "ontology-run/population-surface.json").read_bytes())
    receipt = json.loads((HERE / "ontology-run/grounding-receipt.json").read_bytes())
    by_family: dict[str, list[str]] = {}
    for item in surface["record_types"]:
        by_family.setdefault(item["family"], []).append(item["name"])

    assert {family: len(names) for family, names in by_family.items()} == SURFACE_FAMILIES
    assert sorted(by_family["RELATION"]) == ["PaymentInvoiceRelation"]
    assert sorted(by_family["EVENT"]) == ["Event"]
    assert sorted(by_family["ENTITY"]) == [
        "Actor",
        "Entity",
        "InventoryUnit",
        "Invoice",
        "Order",
        "Payment",
        "SupplierOrder",
    ]
    # No Event class of the producer's own: the bound profile admits no event.
    assert surface["families_admitted"] == ADMITTED_FAMILIES
    assert sorted(receipt["grounded_subjects"]) == sorted(
        set(by_family["ENTITY"] + by_family["RELATION"]) - {"Entity"}
    )


def test_the_evaluation_directory_carries_the_frozen_review_package() -> None:
    directory = EVALUATION / "shop-01"
    present = {path.name for path in directory.iterdir() if path.name != "__pycache__"}

    assert {
        "review-input-manifest.json",
        "review-record.blank.md",
        "review-task.md",
    } <= present
    manifest = json.loads((directory / "review-input-manifest.json").read_bytes())
    assert manifest["schema"] == "malleus.paper-v4.source-grounded-review-inputs/v2"
    assert manifest["run_id"] == "shop-01"
    assert manifest["rows_per_question"] == {
        question_id.removeprefix("NQ-"): rows
        for question_id, rows in ROWS_BY_QUESTION.items()
    }
    assert manifest["witnesses_traced"] == WITNESSES_TRACED
    names = [item["name"] for item in manifest["materials"]]
    assert names[-5:] == [
        "retained_plan_01_inventory",
        "retained_plan_02_warehouse",
        "retained_plan_03_supplier_orders",
        "retained_plan_04_invoices_payments",
        "query_trace_summary",
    ]
    for item in manifest["materials"]:
        assert item["visibility"] == "PUBLIC", item["name"]
        assert _digest((ROOT / item["path"]).read_bytes()) == item["sha256"], item["name"]
    fixed = manifest["fixed_identities"]
    assert fixed["source_sha256"] == _contract()["source"]["source_sha256"]
    assert fixed["competency_questions_sha256"] == _digest(QUESTIONS_PATH.read_bytes())
    assert fixed["accepted_ontology_sha256"] == json.loads(
        (HERE / "ontology-run/result.json").read_bytes()
    )["accepted_ontology_sha256"]
    assert fixed["contract_identity"] == json.loads(
        (HERE / "results/contract-identity.json").read_bytes()
    )["contract_identity"]
    # No frozen protocol binds this cell, so the manifest was not validated and
    # says so rather than carrying a digest it cannot honour.
    assert manifest["review_protocol"] == "NONE_FROZEN"
    assert "review_protocol_sha256" not in manifest
    assert manifest["validation"]["validated"] is False
    assert manifest["validation"]["validator"].endswith(
        "review.py::validate_review_input_manifest"
    )
    assert "{{" not in (directory / "review-task.md").read_text(encoding="utf-8")


def test_run_21_is_frozen_and_this_cell_moved_none_of_its_bytes() -> None:
    for path, digest in sorted(RUN_21_FROZEN.items()):
        assert _digest((RUN_21 / path).read_bytes()) == digest, path


def test_shop_01_is_an_active_test_path() -> None:
    manifest = json.loads(ACTIVE_TEST_MANIFEST.read_bytes())

    assert "paper-v4/experiment-v4/shop-01" in manifest["paths"]
    assert "paper-v4/experiment-v4/run-21" in manifest["paths"]
    for value in manifest["paths"]:
        assert (ROOT / value).exists(), value


def test_the_paper_ledger_opens_pins_and_closes_this_cell_at_e_0201_to_e_0203() -> None:
    """Three entries in order, each bounded at the next heading.

    E-0201 opens the cell, E-0202 records the pin the overseer verified before
    the producer ran, and E-0203 is the frozen run. Every entry is read between
    its own heading and the next one, so a later entry cannot satisfy an earlier
    entry's checks: reading E-0201 to the end of the file is what made this guard
    pass a figure E-0202 carried.
    """

    ledger = PAPER_LEDGER.read_text(encoding="utf-8")
    headings = re.findall(r"^### (E-\d{4})", ledger, re.M)

    assert "E-0201" in headings
    assert headings.index("E-0201") == headings.index("E-0200") + 1
    assert headings.index("E-0202") == headings.index("E-0201") + 1
    assert headings.index("E-0203") == headings.index("E-0202") + 1
    entry = ledger.split("### E-0201", 1)[1].split("\n### E-")[0]
    assert "shop-01" in entry
    assert "E-0202" not in entry
    for fact in ("rows instead of prose", "census", "falsifier", "expected"):
        assert fact in entry.lower(), fact

    pin = ledger.split("### E-0202", 1)[1].split("\n### E-")[0]
    assert "shop-01" in pin
    assert _commit() in pin
    assert "the producer has not run" in pin.lower()
    assert "E-0203" not in pin

    frozen = ledger.split("### E-0203", 1)[1].split("\n### E-")[0]
    assert "shop-01" in frozen
    assert "actor:overseer-shop-01" in frozen
    assert EXECUTION_COMMIT in frozen
    # Every figure the closing entry states is recomputed elsewhere in this file
    # from the frozen artifacts. What this test checks is that the entry states
    # them rather than pointing at them.
    for phrase in (
        "945 facts",
        "six entity types and one",
        "7 entities, 2 relations, 15 derivations",
        "11 TYPE_ABSENT, 2",
        "0 supersessions",
        "nine physical rows",
        "38 ledger events",
        "9 records traced",
        "56 cases: 11 ENTITY, 45 RELATION",
        "CQ-S1 5, CQ-S2 1, CQ-S3 2, CQ-S4 9, 17 rows",
        "13 ENTITY, 4 RELATION) over 9 witnesses",
        "138,864",
        "50,777",
        "11,653",
        "27,128",
        "22,321",
        "250,743",
        "387,470",
        "two of the three",
        "nothing in this cell is withheld",
    ):
        assert phrase in frozen, phrase
    # The refusals it counts are the log's, and the admission is the last one.
    log = json.loads((HERE / "results/launch-log.json").read_bytes())
    refusals = [entry for entry in log["runner"] if entry["status"] == "REFUSED"]
    assert len(refusals) == 3
    assert len(log["runner"]) == 4
    assert "fourth runner attempt" in frozen


@pytest.mark.parametrize("change_id", CHANGE_IDS)
def test_every_change_entry_says_whether_it_is_carried(change_id: str) -> None:
    entry = _changes()[change_id]

    if change_id in THIS_CELL_CHANGE_IDS:
        assert entry.get("carried_from") in (None, "the v4.11 finding"), change_id
    else:
        assert entry["carried_from"] == "run-21", change_id
    assert entry["id"] == change_id
    assert entry.get("detail")
