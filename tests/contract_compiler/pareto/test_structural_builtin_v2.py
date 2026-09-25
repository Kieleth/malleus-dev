"""Route C and route D for the T3 cut (design/temporal/g4/RULINGS.md R-07).

Route C: Core's structural builtin ``malleus.core.operations-apply-atomically``
gains version 2, the one that understands ``supersession_kind``. Version 1
keeps its behaviour and refuses the field. New histories select version 2
through the shipped default; a history built under version 1 keeps its exact
bytes and replays as recorded. No history whose policy does not require
version 2 admits the field, by any door: the check refuses it, and replay
refuses it for a change set that reached the ledger without running the check.

Route D: the state-version profile's successor distinguishes a revision from a
transition. The predecessor is kept with its exact identity.

Expected identities for the predecessors are the ones pinned before this cut
in ``test_temporal_revision.py``, read from Core at 837908ba.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import pytest

import malleus.compiler as api
from tests.contract_compiler.pareto.test_temporal_revision import (
    ACTOR,
    LEGACY_LEDGER,
    LEGACY_RECEIPT,
    PRICE,
    STATE_VERSION,
    STRUCTURAL_BUNDLE,
    STRUCTURAL_CHECK,
    TX,
    Build,
    _entity,
    _instant,
    _ledger,
    _operation,
    price_contract,  # noqa: F401  (fixture)
)


BUILTIN = "malleus.core.operations-apply-atomically"


def _builtin_version(bundle) -> str:
    return json.loads(bundle.check_contract_bytes)["executor"]["builtin_version"]


def _v1_bundle():
    (bundle,) = [
        member
        for member in api.SUPPORTED_STRUCTURAL_HISTORY_BUNDLES
        if member.identity == STRUCTURAL_BUNDLE
    ]
    return bundle


class V1Build(Build):
    """The G3 build, under the version-1 structural bundle selected explicitly."""

    def __init__(self, path: Path, compilation) -> None:
        self.history = api.create_structural_history(
            path,
            compilation=compilation,
            transaction_time=TX,
            actor_id=ACTOR,
            bundle=_v1_bundle(),
        )
        self.positions = {}
        self.replays = {}


def _k1(build):
    build.step(
        "K1",
        [_entity(PRICE["product:P"]), _entity(PRICE["account:reported-price"]), _entity(PRICE["r1"])],
        _instant("2026-05-01T00:00:00Z"),
        sources=("src:r1",),
    )


# --- the shipped defaults ------------------------------------------------------


def test_the_shipped_structural_default_names_builtin_version_2():
    bundle = api.STRUCTURAL_HISTORY_BUNDLE
    assert _builtin_version(bundle) == "2"
    assert bundle.policy_program.required_checks == (
        (bundle.check_contract_id, bundle.check_contract_identity),
    )
    assert bundle.check_contract_identity == (
        "sha256:" + sha256(bundle.check_contract_bytes).hexdigest()
    )
    assert bundle.identity != STRUCTURAL_BUNDLE
    assert api.SUPPORTED_STRUCTURAL_HISTORY_BUNDLES[-1] is bundle


def test_the_version_1_bundle_is_kept_with_its_exact_identities():
    v1 = _v1_bundle()
    assert _builtin_version(v1) == "1"
    assert v1.check_contract_identity == STRUCTURAL_CHECK
    assert [_builtin_version(b) for b in api.SUPPORTED_STRUCTURAL_HISTORY_BUNDLES] == ["1", "2"]


def test_both_builtin_versions_are_held_and_no_other():
    assert api.resolve_core_builtin(BUILTIN, "1") is not api.resolve_core_builtin(BUILTIN, "2")
    assert sorted(api.CORE_BUILTIN_CHECKS) == [(BUILTIN, "1"), (BUILTIN, "2")]
    with pytest.raises(api.CheckContractError):
        api.resolve_core_builtin(BUILTIN, "3")


def test_a_new_structural_history_retains_the_version_2_check(tmp_path, price_contract):
    history = api.create_structural_history(
        tmp_path / "h.jsonl", compilation=price_contract, transaction_time=TX, actor_id=ACTOR
    )
    retained = history.replay().retained_bytes("malleus:structural-admission-check/v1")
    assert retained == api.STRUCTURAL_HISTORY_BUNDLE.check_contract_bytes
    assert history.replay().required_checks["required-check-verdict"] == (
        (
            api.STRUCTURAL_HISTORY_BUNDLE.check_contract_id,
            api.STRUCTURAL_HISTORY_BUNDLE.check_contract_identity,
        ),
    )


def test_the_state_version_successor_tells_revision_from_transition():
    semantics = api.STATE_VERSION_PROFILE.change_semantics
    assert semantics["correction"] != semantics["transition"]
    assert api.STATE_VERSION_PROFILE.identity != STATE_VERSION
    assert api.SUPPORTED_STATE_VERSION_PROFILES[-1] is api.STATE_VERSION_PROFILE
    (predecessor,) = [
        p for p in api.SUPPORTED_STATE_VERSION_PROFILES if p.identity == STATE_VERSION
    ]
    old = predecessor.change_semantics
    assert old["correction"] == old["transition"]
    # Only the correction mapping moved; every other field is the predecessor's.
    assert {k: v for k, v in api.STATE_VERSION_PROFILE.data.items() if k != "change_semantics"} == {
        k: v for k, v in predecessor.data.items() if k != "change_semantics"
    }


# --- a version-1 history -------------------------------------------------------


def test_a_version_1_history_keeps_its_exact_bytes_and_replays(tmp_path, price_contract):
    build = V1Build(tmp_path / "g1-01.jsonl", price_contract)
    _k1(build)
    build.step(
        "K2",
        [_entity(PRICE["r2"])],
        _instant("2026-05-12T00:00:00Z"),
        sources=("src:r2",),
        supersede={"r2": ("r1", None)},
    )
    assert _ledger(build.history) == LEGACY_LEDGER
    assert build.history.replay().receipt.identity == LEGACY_RECEIPT
    reopened = api.KnowledgeChangeHistory.reopen(build.history.path).replay()
    assert reopened.receipt.identity == LEGACY_RECEIPT


@pytest.mark.parametrize("kind", ["TRANSITION", "REVISION"])
def test_a_version_1_history_refuses_a_kind_field_at_check(tmp_path, price_contract, kind):
    build = V1Build(tmp_path / "g1-01.jsonl", price_contract)
    _k1(build)
    refusal = build.refused(
        "K2",
        [_entity(PRICE["r2"])],
        _instant("2026-05-12T00:00:00Z" if kind == "TRANSITION" else "2026-05-01T00:00:00Z"),
        sources=("src:r2",),
        supersede={"r2": ("r1", kind)},
    )
    assert refusal.stage is api.PopulationAdmissionStage.CHECK
    assert "SUPERSESSION_KIND_NOT_SELECTED" in refusal.detail


def test_a_version_1_history_refuses_a_kind_field_at_replay(tmp_path, price_contract):
    """The Core-authored structural door appends without running the builtin.

    ``admit_structural_change`` writes the three protocol events itself and
    relies on replay to apply the change. Replay must refuse the field for a
    history whose policy does not require version 2, so no door admits it.
    """

    build = V1Build(tmp_path / "g1-01.jsonl", price_contract)
    _k1(build)
    change = build.compose(
        "K2",
        [_entity(PRICE["r2"])],
        _instant("2026-05-12T00:00:00Z"),
        sources=("src:r2",),
        supersede={"r2": ("r1", "TRANSITION")},
    )
    bundle = _v1_bundle()
    current = build.history.replay()
    policy = bundle.policy_program
    proposal_id = f"proposal:{change.change_set_id}:structural-admission"

    def event(event_type, **payload):
        return json.dumps(
            {"event_type": event_type, "payload": payload},
            separators=(",", ":"),
            sort_keys=True,
        ).encode()

    before = _ledger(build.history)
    with pytest.raises(api.KnowledgeChangeRefusal) as caught:
        build.history._admit(
            anchors=(),
            change_set=change,
            machine_events=(
                event(
                    "CHANGE_PROPOSED",
                    expected_machine_state_identity=current.machine_state.identity,
                    knowledge_change_set_identity=change.identity,
                    policy_id=policy.identifier,
                    policy_identity=policy.identity,
                    proposal_id=proposal_id,
                ),
                event(
                    "CHECK_RECORDED",
                    check_contract_id=bundle.check_contract_id,
                    check_contract_identity=bundle.check_contract_identity,
                    outcome=bundle.success_outcome,
                    policy_identity=policy.identity,
                    proposal_id=proposal_id,
                    receipt_id=f"receipt:{change.change_set_id}:structural-admission",
                ),
                event(
                    "VERDICT_RECORDED",
                    decision_id=f"decision:{change.change_set_id}:structural-admission",
                    proposal_id=proposal_id,
                ),
            ),
            transaction_time=TX,
            actor_id=ACTOR,
        )
    assert caught.value.reason.name == "SUPERSESSION_KIND_NOT_SELECTED"
    assert _ledger(build.history) == before


def test_a_version_2_history_admits_a_declared_transition(tmp_path, price_contract):
    """The default history: the T3 behaviour, now selected by version 2."""

    build = Build(tmp_path / "g1-01.jsonl", price_contract)
    _k1(build)
    build.step(
        "K2",
        [_entity(PRICE["r2"])],
        _instant("2026-05-12T00:00:00Z"),
        sources=("src:r2",),
        supersede={"r2": ("r1", "TRANSITION")},
    )
    r1 = build.history.replay().record_history["r1"]
    assert [(c.kind, c.record_id) for c in r1.closings] == [("TRANSITION", "r2")]
    retained = build.history.replay().retained_bytes("malleus:structural-admission-check/v1")
    assert json.loads(retained)["executor"]["builtin_version"] == "2"
