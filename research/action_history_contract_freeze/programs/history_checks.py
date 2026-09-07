"""Research orchestration of explicit checks before any assessment append.

Reads the owning replay and invokes the existing producer. No history writer,
effect, supplied outcome or policy decision is exposed by this helper.
"""

from dataclasses import dataclass

from malleus.compiler import KnowledgeChangeHistory
from malleus._contract_pipeline.protocol_runtime import load_bundle, raw
from research.action_history_contract_freeze.programs.check_executor import (
    CheckExecution,
    CheckRefusal,
    load_check_executor,
)


@dataclass(frozen=True)
class HistoryCheckRun:
    ledger_head: str
    ledger_event_count: int
    execution: CheckExecution


def run_history_check(
    history: KnowledgeChangeHistory, *, invocation
) -> HistoryCheckRun:
    """Compute from one actual prefix; the result is not an admitted assessment.

    The prefix coordinates accompany the computation for later stale-base
    checks. A different prefix after this call is not silently substituted.
    Replay itself never calls this function or the producer.
    """
    replay = history.replay()
    if replay.protocol_replay is None:
        raise CheckRefusal("no finite protocol definition is selected")
    protocol = replay.protocol_replay.data
    selected = {
        member.content
        for member in replay.retained_inputs
        if member.role == "RETAINED_EVIDENCE"
        and member.identity == protocol["bundle_identity"]
    }
    if len(selected) != 1:
        raise CheckRefusal("selected exact program bytes are missing or inconsistent")
    bundle = load_bundle(selected.pop())
    engine = load_check_executor()
    result = engine.execute(
        invocation=invocation,
        records=protocol["records"],
        retained_bytes={
            member.record_id: member.content for member in replay.retained_inputs
        },
        contract_bytes=raw(bundle["record_contract_base64"]),
    )
    return HistoryCheckRun(replay.ledger_head, replay.ledger_event_count, result)
