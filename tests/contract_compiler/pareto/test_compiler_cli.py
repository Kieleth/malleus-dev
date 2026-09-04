"""Public command-line contract for the compiler-to-ledger population route."""

from __future__ import annotations

from hashlib import sha256
from importlib import import_module
from importlib.resources import files
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
FIXTURE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "inspection_note_capture_v1"
)
LINKML_TYPES = Path(
    str(
        files("linkml_runtime").joinpath(
            "linkml_model", "model", "schema", "types.yaml"
        )
    )
)
TRANSACTION_TIME = "2026-09-04T00:00:00Z"
ACTOR = "actor:compiler-cli"
CAPTURE_ID = "capture:inspection-note"
SOURCE_ID = "source:inspection-note"
SOURCE_ARTIFACT_ID = "artifact:inspection-note"


def _cli():
    return import_module("malleus.compiler_cli")


def _api():
    return import_module("malleus.compiler")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _run(capsysbinary, argv: list[str]) -> tuple[int, bytes, bytes]:
    code = _cli().main(argv)
    captured = capsysbinary.readouterr()
    return code, captured.out, captured.err


def _emitted(capsysbinary, argv: list[str]) -> dict:
    code, out, err = _run(capsysbinary, argv)
    assert code == 0, err.decode()
    value = json.loads(out)
    assert isinstance(value, dict)
    return value


def _contract_arguments() -> list[str]:
    return [
        "--root",
        "inspection-note",
        "--source",
        "inspection-note",
        str(FIXTURE / "inspection-note.yaml"),
        "--source",
        "malleus",
        str(ROOT / "ontology/malleus.yaml"),
        "--source",
        "linkml:types",
        str(LINKML_TYPES),
    ]


def _plan_inputs(tmp_path: Path) -> tuple[Path, Path]:
    plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    records = tmp_path / "records.json"
    supersessions = tmp_path / "supersessions.json"
    records.write_bytes(_canonical(plan["records"]))
    supersessions.write_bytes(_canonical(plan["supersessions"]))
    return records, supersessions


def _profile_file(tmp_path: Path) -> Path:
    path = tmp_path / "profile.json"
    path.write_bytes(_api().SOURCE_ASSERTION_PROFILE.canonical_bytes)
    return path


def _create_history(capsysbinary, tmp_path: Path) -> Path:
    ledger = tmp_path / "history.jsonl"
    _emitted(
        capsysbinary,
        [
            "history",
            "create",
            "--ledger",
            str(ledger),
            *_contract_arguments(),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    return ledger


def _retain_inputs(capsysbinary, ledger: Path, capture: Path | None = None) -> dict:
    return _emitted(
        capsysbinary,
        [
            "retain",
            "--ledger",
            str(ledger),
            "--source",
            SOURCE_ID,
            SOURCE_ARTIFACT_ID,
            str(FIXTURE / "reading.json"),
            "application/json",
            "--evidence",
            CAPTURE_ID,
            str(capture or FIXTURE / "document-capture.json"),
            "application/json",
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )


def _capture_plan(
    capsysbinary, tmp_path: Path, capture: Path | None = None
) -> tuple[Path, Path, dict]:
    records, supersessions = _plan_inputs(tmp_path)
    plan_out = tmp_path / "plan.json"
    census_out = tmp_path / "census.json"
    summary = _emitted(
        capsysbinary,
        [
            "capture",
            *_contract_arguments(),
            "--reading",
            str(FIXTURE / "reading.json"),
            "--capture",
            str(capture or FIXTURE / "document-capture.json"),
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            "plan:inspection-note:1",
            "--records",
            str(records),
            "--supersessions",
            str(supersessions),
            "--plan-out",
            str(plan_out),
            "--census-out",
            str(census_out),
        ],
    )
    return plan_out, census_out, summary


def _populate(capsysbinary, tmp_path: Path, ledger: Path, plan: Path) -> dict:
    return _emitted(
        capsysbinary,
        [
            "populate",
            "--ledger",
            str(ledger),
            "--plan",
            str(plan),
            "--profile",
            str(_profile_file(tmp_path)),
            "--change-set-out",
            str(tmp_path / "change-set.json"),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )


def _admit(capsysbinary, tmp_path: Path, ledger: Path, plan: Path) -> dict:
    return _emitted(
        capsysbinary,
        [
            "admit",
            "--ledger",
            str(ledger),
            "--plan",
            str(plan),
            "--profile",
            str(_profile_file(tmp_path)),
            "--change-set",
            str(tmp_path / "change-set.json"),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )


def test_cli_parses_every_population_subcommand_with_explicit_inputs(
    tmp_path: Path,
) -> None:
    parser = _cli()._parser()

    history = parser.parse_args(
        [
            "history",
            "create",
            "--ledger",
            "ledger.jsonl",
            *_contract_arguments(),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ]
    )
    assert (history.command, history.history_command) == ("history", "create")
    assert history.ledger == "ledger.jsonl"
    assert history.root == "inspection-note"
    assert history.transaction_time == TRANSACTION_TIME
    assert history.actor_id == ACTOR

    retain = parser.parse_args(
        [
            "retain",
            "--ledger",
            "ledger.jsonl",
            "--source",
            SOURCE_ID,
            SOURCE_ARTIFACT_ID,
            "reading.json",
            "application/json",
            "--evidence",
            CAPTURE_ID,
            "capture.json",
            "application/json",
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ]
    )
    assert retain.command == "retain"
    assert retain.source == [
        [SOURCE_ID, SOURCE_ARTIFACT_ID, "reading.json", "application/json"]
    ]
    assert retain.evidence == [[CAPTURE_ID, "capture.json", "application/json"]]

    capture = parser.parse_args(
        [
            "capture",
            *_contract_arguments(),
            "--reading",
            "reading.json",
            "--capture",
            "capture.json",
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            "plan:inspection-note:1",
            "--records",
            "records.json",
            "--supersessions",
            "supersessions.json",
            "--plan-out",
            "plan.json",
            "--census-out",
            "census.json",
        ]
    )
    assert capture.command == "capture"
    assert capture.capture_id == CAPTURE_ID
    assert capture.plan_id == "plan:inspection-note:1"
    assert capture.plan_out == "plan.json"
    assert capture.census_out == "census.json"

    populate = parser.parse_args(
        [
            "populate",
            "--ledger",
            "ledger.jsonl",
            "--plan",
            "plan.json",
            "--profile",
            "profile.json",
            "--change-set-out",
            "change-set.json",
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ]
    )
    assert populate.command == "populate"
    assert populate.change_set_out == "change-set.json"

    admit = parser.parse_args(
        [
            "admit",
            "--ledger",
            "ledger.jsonl",
            "--plan",
            "plan.json",
            "--profile",
            "profile.json",
            "--change-set",
            "change-set.json",
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ]
    )
    assert admit.command == "admit"
    assert admit.change_set == "change-set.json"

    for missing in (
        ["history", "create", "--ledger", "ledger.jsonl", *_contract_arguments()],
        ["populate", "--ledger", "ledger.jsonl", "--plan", "plan.json"],
        ["admit", "--ledger", "ledger.jsonl", "--plan", "plan.json"],
        ["capture", *_contract_arguments()],
    ):
        with pytest.raises(SystemExit):
            parser.parse_args(missing)


def test_history_create_bootstraps_one_structural_history(
    tmp_path: Path, capsysbinary
) -> None:
    api = _api()
    ledger = tmp_path / "history.jsonl"

    summary = _emitted(
        capsysbinary,
        [
            "history",
            "create",
            "--ledger",
            str(ledger),
            *_contract_arguments(),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )

    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    assert summary["ledger_path"] == str(ledger)
    assert summary["contract_identity"] == replay.partial_contract.identity
    assert summary["receipt_identity"] == replay.receipt.identity
    assert summary["graph_state_digest"] == replay.graph.state_digest()
    assert summary["ledger_event_count"] == replay.ledger_event_count
    assert summary["retained_record_ids"] == [
        "malleus:bootstrap:validated-contract",
        "malleus:bootstrap:partial-effective-contract",
        "malleus:bootstrap:knowledge-history-binding",
        "malleus:structural-admission-check/v1",
    ]
    assert (
        replay.partial_contract.normative_profile.identity
        == api.STRUCTURAL_HISTORY_BUNDLE.normative_profile.identity
    )


def test_retain_registers_the_named_source_and_evidence_bytes(
    tmp_path: Path, capsysbinary
) -> None:
    api = _api()
    ledger = _create_history(capsysbinary, tmp_path)

    summary = _retain_inputs(capsysbinary, ledger)

    retained = {
        member.record_id: member
        for member in api.KnowledgeChangeHistory.reopen(ledger).replay().retained_inputs
    }
    reading = (FIXTURE / "reading.json").read_bytes()
    capture = (FIXTURE / "document-capture.json").read_bytes()
    assert retained[SOURCE_ARTIFACT_ID].role == "SOURCE_ARTIFACT"
    assert retained[SOURCE_ID].role == "RETAINED_SOURCE"
    assert retained[SOURCE_ID].identity == _digest(reading)
    assert retained[CAPTURE_ID].role == "RETAINED_EVIDENCE"
    assert retained[CAPTURE_ID].identity == _digest(capture)
    assert {item["record_id"] for item in summary["retained"]} == {
        SOURCE_ARTIFACT_ID,
        SOURCE_ID,
        CAPTURE_ID,
    }


def test_capture_writes_the_fixture_plan_and_census(
    tmp_path: Path, capsysbinary
) -> None:
    plan_out, census_out, summary = _capture_plan(capsysbinary, tmp_path)

    expected_plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    expected_census = json.loads((FIXTURE / "document-census.json").read_bytes())
    produced = json.loads(plan_out.read_bytes())
    assert plan_out.read_bytes() == _canonical(produced)
    assert json.loads(census_out.read_bytes()) == expected_census
    assert summary["capture_identity"] == _digest(
        (FIXTURE / "document-capture.json").read_bytes()
    )
    assert summary["reading_identity"] == _digest((FIXTURE / "reading.json").read_bytes())
    assert summary["contract_identity"] == produced["contract_identity"]
    assert {
        key: value
        for key, value in produced.items()
        if key != "contract_identity"
    } == {
        key: value
        for key, value in expected_plan.items()
        if key != "contract_identity"
    }


def test_populate_prepares_the_governed_change_and_writes_its_bytes(
    tmp_path: Path, capsysbinary
) -> None:
    api = _api()
    ledger = _create_history(capsysbinary, tmp_path)
    _retain_inputs(capsysbinary, ledger)
    plan_out, _, _ = _capture_plan(capsysbinary, tmp_path)

    summary = _populate(capsysbinary, tmp_path, ledger, plan_out)

    change_bytes = (tmp_path / "change-set.json").read_bytes()
    change = api.KnowledgeChangeSet.from_bytes(change_bytes)
    assert summary["status"] == "CHANGE_SET"
    assert summary["plan_id"] == "plan:inspection-note:1"
    assert summary["change_set_id"] == "change:plan:inspection-note:1"
    assert summary["change_set_identity"] == change.identity
    assert summary["source_record_ids"] == [SOURCE_ID]
    assert summary["evidence_record_ids"] == [
        "profile:source-assertion",
        "plan:inspection-note:1",
        CAPTURE_ID,
        "plan:inspection-note:1:gaps",
    ]
    retained = {
        member.record_id
        for member in api.KnowledgeChangeHistory.reopen(ledger).replay().retained_inputs
    }
    assert {
        "profile:source-assertion",
        "plan:inspection-note:1",
        "plan:inspection-note:1:gaps",
    } <= retained
    assert not api.KnowledgeChangeHistory.reopen(ledger).replay().change_sets


def test_admit_accepts_the_prepared_change(tmp_path: Path, capsysbinary) -> None:
    api = _api()
    ledger = _create_history(capsysbinary, tmp_path)
    _retain_inputs(capsysbinary, ledger)
    plan_out, _, _ = _capture_plan(capsysbinary, tmp_path)
    prepared = _populate(capsysbinary, tmp_path, ledger, plan_out)

    summary = _admit(capsysbinary, tmp_path, ledger, plan_out)

    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    assert summary["change_set_identity"] == prepared["change_set_identity"]
    assert summary["receipt_identity"] == replay.receipt.identity
    assert summary["graph_state_digest"] == replay.graph.state_digest()
    assert [change.change_set_id for change in replay.change_sets] == [
        "change:plan:inspection-note:1"
    ]


def test_admit_refuses_a_change_set_whose_base_moved(
    tmp_path: Path, capsysbinary
) -> None:
    ledger = _create_history(capsysbinary, tmp_path)
    _retain_inputs(capsysbinary, ledger)
    plan_out, _, _ = _capture_plan(capsysbinary, tmp_path)
    _populate(capsysbinary, tmp_path, ledger, plan_out)
    later = tmp_path / "later-evidence.json"
    later.write_bytes(b'{"note":"retained after the change was prepared"}')
    _emitted(
        capsysbinary,
        [
            "retain",
            "--ledger",
            str(ledger),
            "--evidence",
            "evidence:later",
            str(later),
            "application/json",
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    before = ledger.read_bytes()

    code, out, err = _run(
        capsysbinary,
        [
            "admit",
            "--ledger",
            str(ledger),
            "--plan",
            str(plan_out),
            "--profile",
            str(_profile_file(tmp_path)),
            "--change-set",
            str(tmp_path / "change-set.json"),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )

    assert code == 2
    assert out == b""
    assert b"STALE_BASE" in err
    assert err.startswith(b"malleus-compiler: ")
    assert ledger.read_bytes() == before


def test_typed_population_refusals_print_to_stderr_with_exit_two(
    tmp_path: Path, capsysbinary
) -> None:
    ledger = _create_history(capsysbinary, tmp_path)
    plan_out, _, _ = _capture_plan(capsysbinary, tmp_path)

    code, out, err = _run(
        capsysbinary,
        [
            "populate",
            "--ledger",
            str(ledger),
            "--plan",
            str(plan_out),
            "--profile",
            str(_profile_file(tmp_path)),
            "--change-set-out",
            str(tmp_path / "change-set.json"),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )

    assert code == 2
    assert out == b""
    assert err.startswith(b"malleus-compiler: ")
    assert b"UNRETAINED_SOURCE" in err
    assert not (tmp_path / "change-set.json").exists()


def _capture_without_targets(
    tmp_path: Path, targets: tuple[tuple[str, list[str]], ...]
) -> Path:
    """Drop named formalization targets from the fixture capture."""

    capture = json.loads((FIXTURE / "document-capture.json").read_bytes())
    dropped = 0
    for assertion in capture["assertions"]:
        kept = [
            formalization
            for formalization in assertion["formalized_by"]
            if (formalization["record_id"], formalization["path"]) not in targets
        ]
        assert kept or not assertion["formalized_by"], (
            "an assertion that formalized something keeps a target"
        )
        dropped += len(assertion["formalized_by"]) - len(kept)
        assertion["formalized_by"] = kept
    assert dropped == len(targets)
    path = tmp_path / "capture-missing-targets.json"
    path.write_bytes(_canonical(capture))
    return path


def test_populate_surfaces_every_underived_field_from_the_document_route(
    tmp_path: Path, capsysbinary
) -> None:
    """The adapter route and the command line carry the whole refusal detail.

    Two targets are dropped from one capture, so the plan the document
    adapter emits is missing two derivations. One populate call must name
    both, not the first.
    """

    ledger = _create_history(capsysbinary, tmp_path)
    capture = _capture_without_targets(
        tmp_path,
        (
            ("asset:P-7", ["properties", "name"]),
            ("inspection-of:P-7:2026-03-02", ["target_id"]),
        ),
    )
    _retain_inputs(capsysbinary, ledger, capture)
    plan_out, _, _ = _capture_plan(capsysbinary, tmp_path, capture)

    code, out, err = _run(
        capsysbinary,
        [
            "populate",
            "--ledger",
            str(ledger),
            "--plan",
            str(plan_out),
            "--profile",
            str(_profile_file(tmp_path)),
            "--change-set-out",
            str(tmp_path / "change-set.json"),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )

    assert code == 2
    assert out == b""
    message = err.decode()
    assert message.startswith("malleus-compiler: UNDERIVED_FIELD: ")
    assert "record fields lack derivations: " in message
    assert "asset:P-7:['properties', 'name']" in message
    assert "inspection-of:P-7:2026-03-02:['target_id']" in message
    assert (
        "every properties key and both relation endpoints need a derivation, "
        "type and id do not"
    ) in message
    assert not (tmp_path / "change-set.json").exists()


def _admitted_history(capsysbinary, tmp_path: Path) -> tuple[Path, Path, dict, dict]:
    ledger = _create_history(capsysbinary, tmp_path)
    _retain_inputs(capsysbinary, ledger)
    plan_out, census_out, capture_summary = _capture_plan(capsysbinary, tmp_path)
    _populate(capsysbinary, tmp_path, ledger, plan_out)
    admitted = _admit(capsysbinary, tmp_path, ledger, plan_out)
    return ledger, plan_out, capture_summary, admitted


def _library_route(path: Path) -> object:
    """Drive the same fixture through malleus.compiler with no command line."""

    api = _api()
    compilation = api.compile_linkml_contract(
        root_locator="inspection-note",
        sources={
            "inspection-note": (FIXTURE / "inspection-note.yaml").read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": LINKML_TYPES.read_bytes(),
        },
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=api.STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    history = api.create_structural_history(
        path,
        compilation=compilation,
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    reading = (FIXTURE / "reading.json").read_bytes()
    capture = (FIXTURE / "document-capture.json").read_bytes()

    def anchor(record_id, content, role, event_type, **payload):
        return api.KnowledgeAnchorInput(
            machine_event=_canonical(
                {"event_type": event_type, "payload": payload}
            ),
            retained_bytes=content,
            media_type="application/json",
            role=role,
        )

    history.append_anchors(
        anchors=(
            anchor(
                SOURCE_ARTIFACT_ID,
                reading,
                "SOURCE_ARTIFACT",
                "ARTIFACT_REGISTERED",
                artifact_id=SOURCE_ARTIFACT_ID,
                artifact_identity=_digest(reading),
            ),
            anchor(
                SOURCE_ID,
                reading,
                "RETAINED_SOURCE",
                "SOURCE_REGISTERED",
                artifact_id=SOURCE_ARTIFACT_ID,
                source_id=SOURCE_ID,
                source_identity=_digest(reading),
            ),
            anchor(
                CAPTURE_ID,
                capture,
                "RETAINED_EVIDENCE",
                "ARTIFACT_REGISTERED",
                artifact_id=CAPTURE_ID,
                artifact_identity=_digest(capture),
            ),
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    fixture_plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    adapted = api.adapt_document_assertions(
        reading_bytes=reading,
        capture_bytes=capture,
        capture_id=CAPTURE_ID,
        plan_id="plan:inspection-note:1",
        contract_identity=partial.identity,
        records=fixture_plan["records"],
        supersessions=fixture_plan["supersessions"],
    )
    plan = json.loads(adapted.canonical_plan_bytes)
    profile_data = json.loads(api.SOURCE_ASSERTION_PROFILE.canonical_bytes)
    profile = api.DomainHistoryProfile.from_data(profile_data)
    replay = history.replay()
    compiled_plan = api.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=profile,
    )
    prepared = api.prepare_population_change(
        history=history,
        plan=plan,
        profile=profile_data,
        retention_events=api.population_retention_events(
            history=history, compilation=compiled_plan, profile=profile
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    api.admit_structural_change(
        history=history,
        preparation=prepared,
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )
    return api.KnowledgeChangeHistory.reopen(path).replay()


def test_replay_writes_the_export_records_and_the_receipt(
    tmp_path: Path, capsysbinary
) -> None:
    api = _api()
    ledger, _, _, _ = _admitted_history(capsysbinary, tmp_path)
    records_out = tmp_path / "records.json"
    receipt_out = tmp_path / "receipt.json"

    summary = _emitted(
        capsysbinary,
        [
            "replay",
            "--ledger",
            str(ledger),
            "--records-out",
            str(records_out),
            "--receipt-out",
            str(receipt_out),
        ],
    )

    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    assert json.loads(records_out.read_bytes()) == replay.graph.export_records()
    assert records_out.read_bytes() == _canonical(replay.graph.export_records())
    assert receipt_out.read_bytes() == replay.receipt.canonical_bytes
    assert summary["receipt_identity"] == replay.receipt.identity
    assert summary["graph_state_digest"] == replay.graph.state_digest()
    assert summary["records_path"] == str(records_out)
    assert summary["receipt_path"] == str(receipt_out)


def test_query_reads_the_replayed_graph_through_its_public_signature(
    tmp_path: Path, capsysbinary
) -> None:
    ledger, _, _, _ = _admitted_history(capsysbinary, tmp_path)

    code, out, err = _run(
        capsysbinary, ["query", "--ledger", str(ledger), "--type", "Asset"]
    )
    assert code == 0, err.decode()
    assert json.loads(out) == [{"id": "asset:P-7", "name": "P-7", "type": "Asset"}]

    code, filtered, _ = _run(
        capsysbinary,
        ["query", "--ledger", str(ledger), "--type", "Asset", "--where", "name=P-7"],
    )
    assert code == 0
    assert json.loads(filtered) == json.loads(out)

    code, empty, _ = _run(
        capsysbinary,
        ["query", "--ledger", str(ledger), "--type", "Asset", "--where", "name=P-8"],
    )
    assert code == 0
    assert json.loads(empty) == []

    code, nothing, err = _run(
        capsysbinary,
        ["query", "--ledger", str(ledger), "--type", "Asset", "--where", "name"],
    )
    assert code == 2
    assert nothing == b""
    assert err.startswith(b"malleus-compiler: ")


def test_trace_reaches_the_retained_plan_source_and_capture(
    tmp_path: Path, capsysbinary
) -> None:
    api = _api()
    ledger, plan_out, _, _ = _admitted_history(capsysbinary, tmp_path)

    trace = _emitted(
        capsysbinary,
        ["trace", "--ledger", str(ledger), "--record-id", "asset:P-7"],
    )

    plan_bytes = plan_out.read_bytes()
    assert trace["record_id"] == "asset:P-7"
    assert trace["record_type"] == "Asset"
    assert trace["change_set_id"] == "change:plan:inspection-note:1"
    assert trace["population_plan"] == {
        "plan_id": "plan:inspection-note:1",
        "sha256": _digest(plan_bytes),
    }
    assert trace["history_profile"] == {
        "profile_id": "source-assertion",
        "sha256": api.SOURCE_ASSERTION_PROFILE.identity,
    }
    assert trace["sources"] == [
        {
            "record_id": SOURCE_ID,
            "sha256": _digest((FIXTURE / "reading.json").read_bytes()),
        }
    ]
    assert {item["record_id"] for item in trace["evidence"]} == {
        "profile:source-assertion",
        "plan:inspection-note:1",
        CAPTURE_ID,
        "plan:inspection-note:1:gaps",
    }
    assert trace["derivations"] == [
        {
            "locator": "asr:001",
            "path": ["properties", "name"],
            "record_id": "asset:P-7",
            "source_id": SOURCE_ID,
        }
    ]
    assert trace["supersedes_record_id"] is None
    assert trace["superseded_by"] is None
    assert trace["valid_from"] == {"kind": "ORDER_ONLY", "value": CAPTURE_ID}


def test_cli_chain_equals_the_library_route_on_the_inspection_note_fixture(
    tmp_path: Path, capsysbinary
) -> None:
    api = _api()
    cli_root = tmp_path / "cli"
    cli_root.mkdir()

    code, artifact, err = _run(capsysbinary, ["contract", *_contract_arguments()])
    assert code == 0, err.decode()
    ledger, plan_out, capture_summary, admitted = _admitted_history(
        capsysbinary, cli_root
    )
    records_out = cli_root / "records.json"
    _emitted(
        capsysbinary,
        [
            "replay",
            "--ledger",
            str(ledger),
            "--records-out",
            str(records_out),
            "--receipt-out",
            str(cli_root / "receipt.json"),
        ],
    )
    _run(capsysbinary, ["query", "--ledger", str(ledger), "--type", "Asset"])
    _emitted(
        capsysbinary,
        ["trace", "--ledger", str(ledger), "--record-id", "asset:P-7"],
    )

    library = _library_route(tmp_path / "library-history.jsonl")
    exported = json.loads(records_out.read_bytes())
    fixture_plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    fixture_change = json.loads((FIXTURE / "document-change.json").read_bytes())

    assert json.loads(artifact)["grammar"] == (
        "malleus.validated-contract-artifact/private-v0"
    )
    assert exported == library.graph.export_records()
    assert exported["entities"] == fixture_plan["records"]["entities"]
    assert exported["relations"] == fixture_plan["records"]["relations"]
    assert exported["events"] == []
    assert exported["event_participations"] == []
    assert exported["signals"] == []
    assert admitted["receipt_identity"] == library.receipt.identity
    assert admitted["graph_state_digest"] == library.graph.state_digest()
    assert ledger.read_bytes() == (tmp_path / "library-history.jsonl").read_bytes()

    # The fixture's change set cannot be reproduced from this route and the
    # graph export is what is asserted instead. The fixture plan binds a
    # partial effective contract composed with the seed script's own normative
    # profile; this route composes the shipped structural one, so the bound
    # contract identity differs before any base coordinate is compared.
    assert fixture_change["contract_identity"] == fixture_plan["contract_identity"]
    assert fixture_plan["contract_identity"] != capture_summary["contract_identity"]
    assert admitted["change_set_identity"] != _digest(
        _canonical(fixture_change)
    )
    assert api.STRUCTURAL_HISTORY_BUNDLE.normative_profile.identity not in json.dumps(
        fixture_change
    )
