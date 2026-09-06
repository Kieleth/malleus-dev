"""Run one accepted ontology and the producer's population plans through Malleus.

This is run-21's runner with the document adapter taken out. Run-21 adapts one
document capture into one neutral population plan and admits it; the producer of
this cell writes the neutral plans itself, from rows, so there is nothing to
adapt and the runner drives the plans directly. Everything else is the same
path: every step is a public ``malleus.compiler`` call or its shipped
``malleus-compiler`` subcommand, and nothing here composes a protocol program, a
policy, a history binding, an admission check outcome or a lifecycle event.

The admission path is the one
``research/ontology_driven_kg_realization/experiments/small_shop/public_population/run.py``
walks: compile the exact ontology closure, create the history, retain the source
anchors, compile each plan, retain its plan and profile anchors, admit it,
discard every in-memory handle, reopen the ledger from disk, replay, and compare
the reopened receipt and export against the admitted ones. The fixture assembles
its own machine, policy and binding out of ``pareto/``; this runner uses the
shipped structural bundle through ``create_structural_history`` and
``admit_structural_change`` instead, which is the same admission path run-21
uses and the reason no Core protocol internal is named here.

Two artifacts run-21 writes do not exist for rows. There is no capture, because
the plan is not adapted from one, and there is no census, because the census is
the document adapter's report and the plan compiler produces none. The run
contract says so in ``population.census``.

Refusals come back typed from ``malleus.compiler``: a plan the compiler refuses
raises ``PopulationPlanRefusal``, whose text is its reason and its detail, the
way run-21's runner returns the document adapter's.

Outputs land under ``--results``. Only ``run-result.json`` and
``trace-summary.json`` are digest-bearing and free of source values; the plans,
the gaps and the export carry row values and belong beside the run.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import sys

import malleus.compiler as api
import malleus.compiler_cli as cli


RESULT_SCHEMA = "malleus.paper-v4.shop-01-result/v1"
PAPER_EVENT_SCHEMA = "malleus.paper-v4.paper-event/v1"
TRACE_SCHEMA = "malleus.paper-v4.trace-summary/v1"
PLAN_GRAMMAR = "malleus.population-plan/private-v0"
CENSUS_NOT_REPORTED = (
    "NO_CENSUS_EXISTS_FOR_ROWS_THE_CENSUS_IS_THE_DOCUMENT_ADAPTERS_REPORT"
)


class RunRefusal(ValueError):
    """The producer output or the run inputs do not satisfy the run contract."""


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


class _Sink:
    """Collect the shipped CLI's byte output instead of printing it."""

    def __init__(self) -> None:
        self.buffer = io.BytesIO()

    def write(self, text: str) -> int:
        return self.buffer.write(text.encode("utf-8"))

    def flush(self) -> None:
        return None


def _quiet_cli(argv: list[str]) -> dict[str, object]:
    sink = _Sink()
    previous = sys.stdout
    sys.stdout = sink
    try:
        code = cli.main(argv)
    finally:
        sys.stdout = previous
    if code != 0:
        raise RunRefusal(f"malleus-compiler refused: {argv[0]}")
    return json.loads(sink.buffer.getvalue())


def _sources(pairs: list[list[str]]) -> dict[str, bytes]:
    sources: dict[str, bytes] = {}
    for locator, path in pairs:
        if locator in sources:
            raise RunRefusal(f"source locator is repeated: {locator}")
        sources[locator] = Path(path).read_bytes()
    return sources


def _data_sources(rows: list[list[str]]) -> list[tuple[str, str, Path, str]]:
    """The declared source files, by id, artifact id, path and media type."""

    declared: list[tuple[str, str, Path, str]] = []
    seen: set[str] = set()
    for source_id, artifact_id, path, media_type in rows:
        if source_id in seen:
            raise RunRefusal(f"data source is repeated: {source_id}")
        seen.add(source_id)
        declared.append((source_id, artifact_id, Path(path), media_type))
    if not declared:
        raise RunRefusal("at least one data source is required")
    return declared


def _plans(directory: Path, plan_id_prefix: str) -> list[tuple[Path, dict[str, object]]]:
    """The producer's plans, in the lexicographic order of their file names.

    A plan is read as strict canonical JSON, the way the Small Shop fixture reads
    its own: the bytes retained in the ledger are the bytes on disk, so a plan
    that is not already canonical would be retained under a digest its file does
    not carry. The plan id must sit under the coordinate the parent supplied, so
    a producer that invented its own identity is refused here and not at replay.
    """

    if not directory.is_dir():
        raise RunRefusal(f"population-plan directory is absent: {directory}")
    paths = sorted(path for path in directory.iterdir() if path.suffix == ".json")
    if not paths:
        raise RunRefusal(f"population-plan directory carries no plan: {directory}")
    plans: list[tuple[Path, dict[str, object]]] = []
    identifiers: set[str] = set()
    for path in paths:
        source = path.read_bytes()
        try:
            plan = json.loads(source)
        except ValueError as error:
            raise RunRefusal(f"population plan cannot be read: {path}") from error
        if not isinstance(plan, dict) or _canonical(plan) != source:
            raise RunRefusal(f"population plan must be strict canonical JSON: {path}")
        if plan.get("grammar") != PLAN_GRAMMAR:
            raise RunRefusal(f"population plan must declare {PLAN_GRAMMAR}: {path}")
        plan_id = plan.get("plan_id")
        if not isinstance(plan_id, str) or not plan_id.startswith(plan_id_prefix):
            raise RunRefusal(
                f"plan id is not under the supplied coordinate {plan_id_prefix}:"
                f" {plan_id!r} in {path}"
            )
        if plan_id in identifiers:
            raise RunRefusal(f"plan id is repeated: {plan_id}")
        identifiers.add(plan_id)
        plans.append((path, plan))
    return plans


def _trace_record(replay, record_id: str) -> dict[str, object]:
    trace = api.trace_population_record(replay, record_id)
    history = trace.record_history
    return {
        "record_id": trace.record_id,
        "record_type": history.operation.record_type,
        "change_set_id": trace.change_set.change_set_id,
        "contract_identity": trace.change_set.contract_identity,
        "plan_id": str(trace.population_plan["plan_id"]),
        "plan_sha256": trace.population_plan_identity,
        "history_profile": {
            "profile_id": trace.history_profile.profile_id,
            "sha256": trace.history_profile.identity,
        },
        "evidence": {item.record_id: item.identity for item in trace.evidence},
        "sources": {item.record_id: item.identity for item in trace.sources},
        "derivations": [
            {
                "path": list(item["path"]),
                "locator": item["locator"],
                "source_id": item["source_id"],
            }
            for item in trace.derivations
        ],
        "valid_from": {
            "kind": history.valid_from.kind,
            "value": history.valid_from.value,
        },
        # The one field this runner records that run-21's does not. A
        # state-version record can close, and CQ-S2 is judged from this summary.
        "valid_to": (
            None
            if history.valid_to is None
            else {"kind": history.valid_to.kind, "value": history.valid_to.value}
        ),
        "superseded_by": history.superseded_by,
        "supersedes_record_id": history.supersedes_record_id,
    }


def execute(arguments: argparse.Namespace) -> dict[str, object]:
    results = Path(arguments.results)
    if results.exists():
        raise RunRefusal(f"results directory already exists: {results}")
    ledger = Path(arguments.ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    declared = _data_sources(arguments.data_source)
    plans = _plans(Path(arguments.plans), arguments.plan_id_prefix)
    sources = _sources(arguments.source)
    if arguments.root not in sources:
        raise RunRefusal(f"root locator is not among the sources: {arguments.root}")
    ontology_bytes = sources[arguments.root]

    compilation = api.compile_linkml_contract(
        root_locator=arguments.root, sources=sources
    )
    api.create_structural_history(
        ledger,
        compilation=compilation,
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )

    retain: list[str] = ["retain", "--ledger", str(ledger)]
    for source_id, artifact_id, path, media_type in declared:
        retain.extend(["--source", source_id, artifact_id, str(path), media_type])
    retain.extend(
        [
            "--transaction-time",
            arguments.transaction_time,
            "--actor-id",
            arguments.actor_id,
        ]
    )
    retained = _quiet_cli(retain)

    history = api.KnowledgeChangeHistory.reopen(ledger)
    admitted_receipt: bytes | None = None
    admitted_export: object | None = None
    plan_results: list[dict[str, object]] = []
    gaps: list[dict[str, object]] = []
    for path, plan in plans:
        before = history.replay()
        plan_compilation = api.compile_population_plan(
            plan,
            partial_contract=before.partial_contract,
            contract_view=before.contract_view,
            base_state=api.PopulationBaseState.from_replay(before),
            history_profile=api.STATE_VERSION_PROFILE,
        )
        prepared = api.prepare_population_change(
            history=history,
            plan=plan,
            profile=json.loads(api.STATE_VERSION_PROFILE.canonical_bytes),
            retention_events=api.population_retention_events(
                history=history,
                compilation=plan_compilation,
                profile=api.STATE_VERSION_PROFILE,
            ),
            transaction_time=arguments.transaction_time,
            actor_id=arguments.actor_id,
        )
        change_set_id: str | None = None
        if prepared.change_set is not None:
            admitted = api.admit_structural_change(
                history=history,
                preparation=prepared,
                transaction_time=arguments.transaction_time,
                actor_id=arguments.actor_id,
            )
            admitted_receipt = admitted.receipt.canonical_bytes
            admitted_export = admitted.graph.export_records()
            change_set_id = admitted.change_sets[-1].change_set_id
            del admitted
        gaps.extend(plan["gaps"])
        plan_results.append(
            {
                "file": path.name,
                "plan_id": plan_compilation.plan_id,
                "status": plan_compilation.status.value,
                "plan_sha256": _digest(plan_compilation.canonical_plan_bytes),
                "source_record_ids": list(plan_compilation.source_record_ids),
                "evidence_record_ids": list(plan_compilation.evidence_record_ids),
                "change_set_id": change_set_id,
                "gap_count": len(plan["gaps"]),
            }
        )
        del prepared, plan_compilation, before
    del history

    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    reopened_receipt = replay.receipt.canonical_bytes
    reopened_export = replay.graph.export_records()
    traces = [
        _trace_record(replay, record_id) for record_id in sorted(replay.record_history)
    ]

    results.mkdir(parents=True)
    for path, plan in plans:
        (results / f"population-plan.{path.name}").write_bytes(_canonical(plan))
    (results / "gaps.json").write_bytes(
        _canonical({"gaps": gaps, "plans": [item["plan_id"] for item in plan_results]})
    )
    (results / "replay-receipt.json").write_bytes(reopened_receipt)
    (results / "export-records.json").write_bytes(_canonical(reopened_export))
    (results / "trace-summary.json").write_bytes(
        _canonical(
            {
                "schema": TRACE_SCHEMA,
                "evidence_selection": "BY_RECORD_ID_NEVER_BY_POSITION",
                "records": traces,
            }
        )
    )
    (results / "paper-events.json").write_bytes(
        _canonical(
            {
                "schema": PAPER_EVENT_SCHEMA,
                "events": [
                    {
                        "event": "ONTOLOGY_ACCEPTED_FOR_POPULATION",
                        "ontology_sha256": _digest(ontology_bytes),
                        "root_locator": arguments.root,
                        "validated_fact_set_sha256": (
                            compilation.artifact.validated_fact_set_sha256
                        ),
                        "contract_identity": replay.partial_contract.identity,
                        "actor_id": arguments.actor_id,
                        "transaction_time": arguments.transaction_time,
                        "non_claim": "STAGE_ACCEPTANCE_NOT_DOMAIN_ADEQUACY",
                    }
                ],
            }
        )
    )

    gaps_by_kind: dict[str, int] = {}
    for gap in gaps:
        kind = str(gap["kind"])
        gaps_by_kind[kind] = gaps_by_kind.get(kind, 0) + 1
    result = {
        "schema": RESULT_SCHEMA,
        "run_id": "shop-01",
        "status": (
            "ADMITTED_AND_REPLAYED"
            if admitted_receipt is not None
            else "NO_DOMAIN_CHANGE"
        ),
        "actor_id": arguments.actor_id,
        "transaction_time": arguments.transaction_time,
        "ontology_sha256": _digest(ontology_bytes),
        "source_closure_sha256": {
            locator: _digest(source) for locator, source in sources.items()
        },
        "validated_contract_sha256": _digest(compilation.artifact.artifact_bytes),
        "validated_fact_set_sha256": compilation.artifact.validated_fact_set_sha256,
        "contract_identity": replay.partial_contract.identity,
        "data_sources": {
            source_id: _digest(path.read_bytes())
            for source_id, _, path, _ in declared
        },
        "retained_after_registration": retained["retained"],
        "plans": plan_results,
        "census": None,
        "census_not_reported": CENSUS_NOT_REPORTED,
        "gaps_by_kind": gaps_by_kind,
        "admitted_receipt_sha256": (
            None if admitted_receipt is None else _digest(admitted_receipt)
        ),
        "replay_receipt_sha256": _digest(reopened_receipt),
        "export_records_sha256": _digest(_canonical(reopened_export)),
        "trace_summary_sha256": _digest((results / "trace-summary.json").read_bytes()),
        "ledger_event_count": replay.ledger_event_count,
        "ledger_head": replay.ledger_head,
        "graph": {
            family: len(records) for family, records in sorted(reopened_export.items())
        },
        "records_traced": len(traces),
        "reopen_matches_admitted": {
            "receipt": admitted_receipt == reopened_receipt,
            "export_records": admitted_export == reopened_export,
        },
    }
    (results / "run-result.json").write_bytes(_canonical(result))
    if not all(result["reopen_matches_admitted"].values()):
        raise RunRefusal("reopened replay does not reproduce the admitted state")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="root source locator")
    parser.add_argument(
        "--source",
        action="append",
        nargs=2,
        required=True,
        metavar=("LOCATOR", "PATH"),
        help="one exact ontology source locator and file; repeat for the closure",
    )
    parser.add_argument(
        "--data-source",
        action="append",
        nargs=4,
        required=True,
        metavar=("SOURCE_ID", "ARTIFACT_ID", "PATH", "MEDIA_TYPE"),
        help="one declared source file to retain verbatim; repeat for all five",
    )
    parser.add_argument(
        "--plans", required=True, help="producer work/population-plans/ directory"
    )
    parser.add_argument(
        "--plan-id-prefix",
        required=True,
        help="the plan coordinate the parent supplied; every plan id sits under it",
    )
    parser.add_argument("--ledger", required=True, help="structural history path")
    parser.add_argument("--results", required=True, help="new results directory")
    parser.add_argument("--transaction-time", required=True)
    parser.add_argument("--actor-id", required=True)
    arguments = parser.parse_args(argv)
    try:
        execute(arguments)
    except (OSError, TypeError, ValueError) as error:
        print(f"shop-01: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
