"""Drive the public Malleus compiler, ledger, and knowledge-graph facade.

Every subcommand is a thin wrapper over ``malleus.compiler``. Nothing here
decides identity: the transaction time, the actor, the history profile, and
every source, evidence, and plan file are named on the command line. Typed
refusals reach stderr with exit code 2 and change no accepted history.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Sequence

from malleus.compiler import (
    STRUCTURAL_HISTORY_BUNDLE,
    DomainHistoryProfile,
    KnowledgeAnchorInput,
    KnowledgeChangeHistory,
    KnowledgeChangeSet,
    PopulationBaseState,
    PopulationPreparation,
    adapt_document_assertions,
    admit_structural_change,
    compile_linkml_contract,
    compile_population_plan,
    compose_partial_effective_contract,
    create_structural_history,
    population_retention_events,
    prepare_population_change,
)


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


def _event(event_type: str, **payload: object) -> bytes:
    return _canonical({"event_type": event_type, "payload": payload})


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def _emit(value: object) -> None:
    sys.stdout.buffer.write(_canonical(_plain(value)) + b"\n")


def _read_json(path: str) -> object:
    source = Path(path).read_bytes()
    try:
        return json.loads(source)
    except (UnicodeDecodeError, ValueError) as error:
        raise ValueError(f"file is not valid JSON: {path}") from error


def _sources(pairs: Sequence[Sequence[str]]) -> dict[str, bytes]:
    sources: dict[str, bytes] = {}
    for locator, raw_path in pairs:
        if locator in sources:
            raise ValueError(f"source locator is repeated: {locator}")
        sources[locator] = Path(raw_path).read_bytes()
    return sources


def _compiled(arguments: argparse.Namespace):
    return compile_linkml_contract(
        root_locator=arguments.root,
        sources=_sources(arguments.source),
    )


def _retained_summary(replay) -> list[dict[str, str]]:
    return [
        {
            "identity": member.identity,
            "media_type": member.media_type,
            "record_id": member.record_id,
            "role": member.role,
        }
        for member in replay.retained_inputs
    ]


def _compile_plan(history: KnowledgeChangeHistory, plan: object, profile):
    replay = history.replay()
    compilation = compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=PopulationBaseState.from_replay(replay),
        history_profile=profile,
    )
    return replay, compilation


def _run_contract(arguments: argparse.Namespace) -> int:
    compilation = _compiled(arguments)
    sys.stdout.buffer.write(compilation.artifact.artifact_bytes)
    return 0


def _run_history_create(arguments: argparse.Namespace) -> int:
    history = create_structural_history(
        arguments.ledger,
        compilation=_compiled(arguments),
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )
    replay = history.replay()
    _emit(
        {
            "contract_identity": replay.partial_contract.identity,
            "graph_state_digest": replay.graph.state_digest(),
            "ledger_event_count": replay.ledger_event_count,
            "ledger_head": replay.ledger_head,
            "ledger_path": str(Path(arguments.ledger)),
            "receipt_identity": replay.receipt.identity,
            "retained_record_ids": [
                member.record_id for member in replay.retained_inputs
            ],
        }
    )
    return 0


def _run_retain(arguments: argparse.Namespace) -> int:
    anchors: list[KnowledgeAnchorInput] = []
    registered: list[str] = []
    for source_id, artifact_id, raw_path, media_type in arguments.source or ():
        content = Path(raw_path).read_bytes()
        anchors.append(
            KnowledgeAnchorInput(
                machine_event=_event(
                    "ARTIFACT_REGISTERED",
                    artifact_id=artifact_id,
                    artifact_identity=_digest(content),
                ),
                retained_bytes=content,
                media_type=media_type,
                role="SOURCE_ARTIFACT",
            )
        )
        anchors.append(
            KnowledgeAnchorInput(
                machine_event=_event(
                    "SOURCE_REGISTERED",
                    artifact_id=artifact_id,
                    source_id=source_id,
                    source_identity=_digest(content),
                ),
                retained_bytes=content,
                media_type=media_type,
                role="RETAINED_SOURCE",
            )
        )
        registered.extend((artifact_id, source_id))
    for evidence_id, raw_path, media_type in arguments.evidence or ():
        content = Path(raw_path).read_bytes()
        anchors.append(
            KnowledgeAnchorInput(
                machine_event=_event(
                    "ARTIFACT_REGISTERED",
                    artifact_id=evidence_id,
                    artifact_identity=_digest(content),
                ),
                retained_bytes=content,
                media_type=media_type,
                role="RETAINED_EVIDENCE",
            )
        )
        registered.append(evidence_id)
    if not anchors:
        raise ValueError("at least one --source or --evidence input is required")
    history = KnowledgeChangeHistory.reopen(arguments.ledger)
    history.append_anchors(
        anchors=tuple(anchors),
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )
    replay = history.replay()
    admitted = set(registered)
    _emit(
        {
            "ledger_event_count": replay.ledger_event_count,
            "receipt_identity": replay.receipt.identity,
            "retained": [
                member
                for member in _retained_summary(replay)
                if member["record_id"] in admitted
            ],
        }
    )
    return 0


def _run_capture(arguments: argparse.Namespace) -> int:
    compilation = _compiled(arguments)
    partial = compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    adapted = adapt_document_assertions(
        reading_bytes=Path(arguments.reading).read_bytes(),
        capture_bytes=Path(arguments.capture).read_bytes(),
        capture_id=arguments.capture_id,
        plan_id=arguments.plan_id,
        contract_identity=partial.identity,
        records=_read_json(arguments.records),
        supersessions=_read_json(arguments.supersessions),
    )
    Path(arguments.plan_out).write_bytes(adapted.canonical_plan_bytes)
    Path(arguments.census_out).write_bytes(adapted.canonical_census_bytes)
    _emit(
        {
            "capture_id": adapted.capture_id,
            "capture_identity": adapted.capture_identity,
            "census_path": str(Path(arguments.census_out)),
            "contract_identity": partial.identity,
            "plan_id": arguments.plan_id,
            "plan_path": str(Path(arguments.plan_out)),
            "reading_identity": adapted.reading_identity,
        }
    )
    return 0


def _run_populate(arguments: argparse.Namespace) -> int:
    history = KnowledgeChangeHistory.reopen(arguments.ledger)
    plan = _read_json(arguments.plan)
    profile_data = _read_json(arguments.profile)
    profile = DomainHistoryProfile.from_data(profile_data)
    _, compilation = _compile_plan(history, plan, profile)
    prepared = prepare_population_change(
        history=history,
        plan=plan,
        profile=profile_data,
        retention_events=population_retention_events(
            history=history,
            compilation=compilation,
            profile=profile,
        ),
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )
    change = prepared.change_set
    if change is not None:
        Path(arguments.change_set_out).write_bytes(change.canonical_bytes)
    _emit(
        {
            "change_set_id": None if change is None else change.change_set_id,
            "change_set_identity": None if change is None else change.identity,
            "change_set_path": (
                None if change is None else str(Path(arguments.change_set_out))
            ),
            "evidence_record_ids": list(prepared.compilation.evidence_record_ids),
            "history_profile_identity": prepared.profile.identity,
            "plan_id": prepared.compilation.plan_id,
            "receipt_identity": prepared.retention_replay.receipt.identity,
            "source_record_ids": list(prepared.compilation.source_record_ids),
            "status": prepared.compilation.status.value,
        }
    )
    return 0


def _run_admit(arguments: argparse.Namespace) -> int:
    history = KnowledgeChangeHistory.reopen(arguments.ledger)
    profile = DomainHistoryProfile.from_data(_read_json(arguments.profile))
    replay, compilation = _compile_plan(history, _read_json(arguments.plan), profile)
    admitted = admit_structural_change(
        history=history,
        preparation=PopulationPreparation(
            profile=profile,
            compilation=compilation,
            change_set=KnowledgeChangeSet.from_bytes(
                Path(arguments.change_set).read_bytes()
            ),
            retention_replay=replay,
        ),
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )
    change = admitted.change_sets[-1]
    _emit(
        {
            "change_set_id": change.change_set_id,
            "change_set_identity": change.identity,
            "graph_state_digest": admitted.graph.state_digest(),
            "ledger_event_count": admitted.ledger_event_count,
            "ledger_head": admitted.ledger_head,
            "receipt_identity": admitted.receipt.identity,
        }
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="malleus-compiler", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    def add_contract_sources(target: argparse.ArgumentParser) -> None:
        target.add_argument("--root", required=True, help="root source locator")
        target.add_argument(
            "--source",
            action="append",
            nargs=2,
            required=True,
            metavar=("LOCATOR", "PATH"),
            help="exact source locator and file; repeat for every imported source",
        )

    def add_actor(target: argparse.ArgumentParser) -> None:
        target.add_argument(
            "--transaction-time",
            required=True,
            help="exact transaction time recorded on every written ledger event",
        )
        target.add_argument(
            "--actor-id", required=True, help="exact actor ID recorded on every event"
        )

    def add_ledger(target: argparse.ArgumentParser) -> None:
        target.add_argument("--ledger", required=True, help="structural history path")

    contract = commands.add_parser(
        "contract",
        help="compile one LinkML root from exact named source files",
    )
    add_contract_sources(contract)

    history = commands.add_parser(
        "history", help="create a structural history from exact contract sources"
    )
    history_commands = history.add_subparsers(dest="history_command", required=True)
    history_create = history_commands.add_parser(
        "create", help="bootstrap one structural history at a new ledger path"
    )
    add_ledger(history_create)
    add_contract_sources(history_create)
    add_actor(history_create)

    retain = commands.add_parser(
        "retain", help="retain exact source and evidence bytes in one history"
    )
    add_ledger(retain)
    retain.add_argument(
        "--source",
        action="append",
        nargs=4,
        metavar=("SOURCE_ID", "ARTIFACT_ID", "PATH", "MEDIA_TYPE"),
        help="register one source artifact and its retained source; repeatable",
    )
    retain.add_argument(
        "--evidence",
        action="append",
        nargs=3,
        metavar=("EVIDENCE_ID", "PATH", "MEDIA_TYPE"),
        help="retain one evidence artifact; repeatable",
    )
    add_actor(retain)

    capture = commands.add_parser(
        "capture", help="adapt one document capture into a neutral population plan"
    )
    add_contract_sources(capture)
    capture.add_argument("--reading", required=True, help="exact reading file")
    capture.add_argument("--capture", required=True, help="exact document-capture file")
    capture.add_argument("--capture-id", required=True, help="retained capture ID")
    capture.add_argument("--plan-id", required=True, help="population plan ID")
    capture.add_argument(
        "--records", required=True, help="proposed records file for the plan"
    )
    capture.add_argument(
        "--supersessions", required=True, help="proposed supersessions file"
    )
    capture.add_argument("--plan-out", required=True, help="plan bytes output path")
    capture.add_argument("--census-out", required=True, help="census bytes output path")

    populate = commands.add_parser(
        "populate", help="compile one plan and prepare its governed change"
    )
    add_ledger(populate)
    populate.add_argument("--plan", required=True, help="population plan file")
    populate.add_argument(
        "--profile", required=True, help="domain-history profile file the plan binds"
    )
    populate.add_argument(
        "--change-set-out",
        required=True,
        help="change-set bytes output path; unwritten on NO_DOMAIN_CHANGE",
    )
    add_actor(populate)

    admit = commands.add_parser("admit", help="admit one prepared structural change")
    add_ledger(admit)
    admit.add_argument("--plan", required=True, help="population plan file")
    admit.add_argument("--profile", required=True, help="domain-history profile file")
    admit.add_argument(
        "--change-set", required=True, help="change-set bytes written by populate"
    )
    add_actor(admit)

    return parser


_COMMANDS = {
    "contract": _run_contract,
    ("history", "create"): _run_history_create,
    "retain": _run_retain,
    "capture": _run_capture,
    "populate": _run_populate,
    "admit": _run_admit,
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    key = (
        (arguments.command, arguments.history_command)
        if arguments.command == "history"
        else arguments.command
    )
    handler = _COMMANDS.get(key)
    if handler is None:
        parser.error("a supported compiler command is required")
    try:
        return handler(arguments)
    except (OSError, TypeError, ValueError) as error:
        print(f"malleus-compiler: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
