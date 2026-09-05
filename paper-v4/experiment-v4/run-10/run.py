"""Run one accepted ontology and one producer population through Malleus.

Every step is a public ``malleus.compiler`` call or its shipped
``malleus-compiler`` subcommand. Nothing here composes a protocol program, a
policy, a history binding, an admission check outcome or a lifecycle event; Core
owns all of those, and a paper harness that restates them is no longer testing
the adopter path.

Order: compile the exact ontology closure, create the structural history, retain
the selected reading as a source and the producer capture as evidence, adapt the
capture into a neutral population plan, compile that plan, prepare the governed
change, admit it when there is one, discard every in-memory handle, reopen the
ledger from disk, replay, and compare the reopened receipt and export against the
admitted ones.

Outputs land under ``--results``. Only ``run-result.json`` and
``trace-summary.json`` are digest-bearing and free of source text; the plan, the
gaps and the export carry source values and belong beside the run in private
storage.
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


RESULT_SCHEMA = "malleus.paper-v4.run-10-result/v1"
PAPER_EVENT_SCHEMA = "malleus.paper-v4.paper-event/v1"
TRACE_SCHEMA = "malleus.paper-v4.trace-summary/v1"
POPULATION_FIELDS = {"capture", "records", "supersessions"}


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


def _population(path: Path) -> dict[str, object]:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict) or set(value) != POPULATION_FIELDS:
        raise RunRefusal(
            "producer population must contain exactly capture, records and"
            f" supersessions; found {sorted(value) if isinstance(value, dict) else value}"
        )
    return value


def _trace_record(replay, record_id: str) -> dict[str, object]:
    trace = api.trace_population_record(replay, record_id)
    return {
        "record_id": trace.record_id,
        "record_type": trace.record_history.operation.record_type,
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
            "kind": trace.record_history.valid_from.kind,
            "value": trace.record_history.valid_from.value,
        },
        "superseded_by": trace.record_history.superseded_by,
        "supersedes_record_id": trace.record_history.supersedes_record_id,
    }


def execute(arguments: argparse.Namespace) -> dict[str, object]:
    results = Path(arguments.results)
    if results.exists():
        raise RunRefusal(f"results directory already exists: {results}")
    ledger = Path(arguments.ledger)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    reading_bytes = Path(arguments.reading).read_bytes()
    population = _population(Path(arguments.population))
    capture_bytes = _canonical(population["capture"])
    sources = _sources(arguments.source)
    if arguments.root not in sources:
        raise RunRefusal(f"root locator is not among the sources: {arguments.root}")
    ontology_bytes = sources[arguments.root]

    compilation = api.compile_linkml_contract(
        root_locator=arguments.root, sources=sources
    )
    history = api.create_structural_history(
        ledger,
        compilation=compilation,
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )

    capture_path = ledger.parent / "retained-capture.json"
    capture_path.write_bytes(capture_bytes)
    retained = _quiet_cli(
        [
            "retain",
            "--ledger",
            str(ledger),
            "--source",
            arguments.source_id,
            arguments.artifact_id,
            str(Path(arguments.reading)),
            "application/json",
            "--evidence",
            arguments.capture_id,
            str(capture_path),
            "application/json",
            "--transaction-time",
            arguments.transaction_time,
            "--actor-id",
            arguments.actor_id,
        ]
    )

    history = api.KnowledgeChangeHistory.reopen(ledger)
    retention = history.replay()
    adapted = api.adapt_document_assertions(
        reading_bytes=reading_bytes,
        capture_bytes=capture_bytes,
        capture_id=arguments.capture_id,
        plan_id=arguments.plan_id,
        contract_identity=retention.partial_contract.identity,
        records=population["records"],
        supersessions=population["supersessions"],
        contract_view=retention.contract_view,
    )
    plan = json.loads(adapted.canonical_plan_bytes)
    census = json.loads(adapted.canonical_census_bytes)

    plan_compilation = api.compile_population_plan(
        plan,
        partial_contract=retention.partial_contract,
        contract_view=retention.contract_view,
        base_state=api.PopulationBaseState.from_replay(retention),
        history_profile=api.SOURCE_ASSERTION_PROFILE,
    )
    prepared = api.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(api.SOURCE_ASSERTION_PROFILE.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history,
            compilation=plan_compilation,
            profile=api.SOURCE_ASSERTION_PROFILE,
        ),
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )

    admitted_receipt: bytes | None = None
    admitted_export: object | None = None
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
    del history, prepared, retention

    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    reopened_receipt = replay.receipt.canonical_bytes
    reopened_export = replay.graph.export_records()
    traces = [
        _trace_record(replay, record_id) for record_id in sorted(replay.record_history)
    ]

    results.mkdir(parents=True)
    (results / "population-plan.json").write_bytes(adapted.canonical_plan_bytes)
    (results / "census.json").write_bytes(adapted.canonical_census_bytes)
    (results / "gaps.json").write_bytes(
        _canonical({"gaps": plan["gaps"], "plan_id": plan["plan_id"]})
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
    for gap in plan["gaps"]:
        kind = str(gap["kind"])
        gaps_by_kind[kind] = gaps_by_kind.get(kind, 0) + 1
    result = {
        "schema": RESULT_SCHEMA,
        "run_id": "run-10",
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
        "reading_sha256": _digest(reading_bytes),
        "capture": {
            "capture_id": adapted.capture_id,
            "capture_sha256": adapted.capture_identity,
            "reading_sha256": adapted.reading_identity,
        },
        "retained_after_registration": retained["retained"],
        "plan": {
            "plan_id": plan_compilation.plan_id,
            "status": plan_compilation.status.value,
            "plan_sha256": _digest(adapted.canonical_plan_bytes),
            "census_sha256": _digest(adapted.canonical_census_bytes),
            "source_record_ids": list(plan_compilation.source_record_ids),
            "evidence_record_ids": list(plan_compilation.evidence_record_ids),
        },
        "census": census,
        "gaps_by_kind": gaps_by_kind,
        "change_set_id": change_set_id,
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
        help="one exact source locator and file; repeat for the whole closure",
    )
    parser.add_argument("--reading", required=True, help="selected reading file")
    parser.add_argument(
        "--population", required=True, help="producer work/document-population.json"
    )
    parser.add_argument("--capture-id", required=True)
    parser.add_argument("--plan-id", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--ledger", required=True, help="structural history path")
    parser.add_argument("--results", required=True, help="new results directory")
    parser.add_argument("--transaction-time", required=True)
    parser.add_argument("--actor-id", required=True)
    arguments = parser.parse_args(argv)
    try:
        execute(arguments)
    except (OSError, TypeError, ValueError) as error:
        print(f"run-10: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
