"""Real e4/e7 domain changes composed with the complete neutral action lifecycle.

The historical correction is independent of the synthetic receipt/observation.
This is not the supplier amendment consumer or a causality claim.
"""

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from malleus.compiler import PolicyProgram
from malleus.ledger import record_hash
from research.action_history_contract_freeze.programs import (
    test_initialization_history as initialization,
)
from research.action_history_contract_freeze.programs import (
    test_dispatch_history as dispatching,
)
from research.action_history_contract_freeze.programs import (
    test_execution_history as receipts,
)
from research.action_history_contract_freeze.programs import (
    test_observation_history as observations,
)
from research.action_history_contract_freeze.programs.dispatch_bundle import (
    add_dispatch,
)
from research.action_history_contract_freeze.programs.execution_bundle import (
    add_execution,
)
from research.action_history_contract_freeze.programs.observation_bundle import (
    add_observation,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    append,
)
from research.ontology_driven_kg_realization.experiments.small_shop.public_population import (
    run as shop,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api


def shop_through_e4(directory):
    history, base, target, partial, target_partial, policy = shop._runtime(
        directory / "history.jsonl"
    )
    shop._bootstrap(history, base, partial)
    shop._admit_plan(history, policy, shop.PLAN_PATHS[0], shop.TIMES[1])
    revision = history.compose_contract_revision(
        revision_id="revision:small-shop:full-public-v1",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=target_partial.canonical_bytes,
        reason="add the full Small Shop conformance-fixture vocabulary",
        issued_at=shop.TIMES[2],
    )
    history.record_contract_revision(
        revision=revision, transaction_time=shop.TIMES[2], actor_id=shop.ACTOR
    )
    for path, when in zip(shop.PLAN_PATHS[1:-1], shop.TIMES[3:-1], strict=True):
        shop._admit_plan(history, policy, path, when)
    replay = history.replay()
    assert len(replay.change_sets) == 4
    assert replay.graph.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1
    return replay


@pytest.fixture(scope="module")
def authorized_e4(tmp_path_factory):
    bundle = add_observation(
        add_execution(add_dispatch(dispatching.authorization.build_bundle()))
    )
    # Only fixture construction changes: every ledger entry is still produced
    # and checked by the actual history. No replay/guard/outcome is patched.
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(initialization, "run_full_shop", shop_through_e4)
        content, _ = dispatching.authorized_prefix(
            tmp_path_factory.mktemp("shop-action-e4"), bundle
        )
    return content


def admit_historical_e7(history):
    policy = PolicyProgram.from_bytes(shop.POLICY_PATH.read_bytes())
    return shop._admit_plan(
        history, policy, shop.PLAN_PATHS[-1], "2026-09-07T00:15:00Z"
    )


def test_real_domain_correction_stales_earlier_dispatch_permission(
    tmp_path, authorized_e4
):
    history = initialization.reopen(tmp_path, authorized_e4)
    before = history.replay()
    changed = admit_historical_e7(history)
    assert changed.graph.get_node("supplier-order-state:B:e7")["ordered_quantity"] == 2
    assert changed.acceptance_head != before.acceptance_head
    prior_bytes = history.path.read_bytes()
    candidate = dispatching.event(history)
    value = candidate["data"]["records"]["value"][0]["record"]
    candidate["transaction_time"] = value["generated_at"] = value["dispatched_at"] = (
        "2026-09-07T00:16:00Z"
    )
    value["content_hash"] = record_hash("ActionDispatch", value)
    with pytest.raises(api().ProtocolProgramRefusal, match="STALE_DISPATCH_DOMAIN"):
        dispatching.dispatch(history, candidate)
    assert history.path.read_bytes() == prior_bytes


def test_inflight_receipt_and_observation_survive_real_domain_change_and_clean_reopen(
    tmp_path, authorized_e4
):
    history = initialization.reopen(tmp_path, authorized_e4)
    initial = history.replay()
    dispatching.dispatch(history, dispatching.event(history))
    corrected = admit_historical_e7(history)
    after_receipt = receipts.execute(history, receipts.event(history, "FAILED"))
    observations.observer_inputs(history)
    final = append(history, "observation", observations.event(history))
    assert len(final.change_sets) == 5
    assert len(final.contract_revisions) == 1
    assert (
        final.record_history["supplier-order-state:B:e4"].superseded_by
        == "supplier-order-state:B:e7"
    )
    assert final.graph.export_records() == corrected.graph.export_records()
    assert (
        final.acceptance_head
        == corrected.acceptance_head
        == after_receipt.acceptance_head
    )
    assert final.materialization_head == corrected.materialization_head
    assert (
        final.protocol_replay.data["state"]["action_acceptance_head"]
        == initial.protocol_replay.data["state"]["action_acceptance_head"]
    )
    assert (
        final.protocol_replay.data["records"]["execution:1"]["record"][
            "execution_status"
        ]
        == "FAILED"
    )
    assert (
        final.protocol_replay.data["records"]["observation:1"]["record"][
            "observation_result"
        ]
        == "CONFIRMED"
    )
    # Knowledge changed only at the ordinary KCS, not because a receipt or an
    # observer stated a result. The failed execution remains failed.
    for record_id in ("O1", "X1", "contains:O1:X1"):
        assert final.record_history[record_id] == initial.record_history[record_id]

    script = """
import importlib.abc, json, sys
class NoResearch(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"research", "tests"}:
            raise AssertionError("replay imported a research/test dependency: " + fullname)
sys.meta_path.insert(0, NoResearch())
from malleus.compiler import KnowledgeChangeHistory
r = KnowledgeChangeHistory.reopen(sys.argv[1]).replay()
print(json.dumps([r.ledger_head, r.ledger_event_count, r.graph.state_digest(), r.protocol_replay.identity]))
"""
    isolated = tmp_path / "jsonl-only"
    isolated.mkdir()
    ledger = isolated / "history.jsonl"
    ledger.write_bytes(history.path.read_bytes())
    result = subprocess.run(
        [sys.executable, "-c", script, str(ledger)],
        cwd=isolated,
        env={
            **os.environ,
            "PYTHONPATH": str(Path(__file__).resolve().parents[3] / "src"),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        text=True,
        capture_output=True,
        check=True,
    )
    assert json.loads(result.stdout) == [
        final.ledger_head,
        final.ledger_event_count,
        final.graph.state_digest(),
        final.protocol_replay.identity,
    ]
    assert tuple(isolated.iterdir()) == (ledger,)
