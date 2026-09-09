"""Literal common-profile observations through two real owning histories.

Distinct bootstraps mean distinct IDs/hashes. This is behavioral comparison,
not wire equality or an independent implementation of the shared calculator.
"""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from malleus.ledger import content_digest, record_hash
from malleus.protocol import ProtocolError, ProtocolLedger
from research.action_history_contract_freeze.programs import (
    test_authorization_history as finite,
)
from tests import test_protocol as assent


TABLE = json.loads(
    Path(__file__).with_name("authorization_lifecycle_cases.json").read_bytes()
)
CASES = TABLE["cases"]


@pytest.fixture(scope="module")
def finite_prefixes(tmp_path_factory):
    return finite.assessed.__wrapped__(tmp_path_factory)


@pytest.fixture(scope="module")
def standalone_prefixes(tmp_path_factory):
    directory = tmp_path_factory.mktemp("standalone-authorization-comparison")
    registry = assent.registry.__wrapped__(directory)
    prefixes = {}
    for case in CASES:
        ledger = ProtocolLedger(directory / (case["verdict"] + ".jsonl"), registry)
        assent.anchor(ledger)
        artifacts = assent.setup_artifacts(ledger, include_grant=False)
        monitors = [artifacts["authority_monitor"]]
        monitors.append(
            assent.add_monitor(ledger, "artifact:authority-monitor:2", "AUTHORITY", 5)
        )
        artifacts["authorization_policy"] = assent.add_authorization_policy(
            ledger, monitors, 5, policy_id="artifact:two-monitor-policy"
        )
        artifacts["grant"] = assent.add_artifact(
            ledger,
            "artifact:grant",
            "AUTHORITY_GRANT",
            5,
            record_type="AuthorityGrant",
            grantor_actor_id="actor:system",
            grantee_actor_id=case["grantee"],
            permitted_action_types=["TEST"],
            scope_record_id="scope:comparison",
            may_subdelegate=False,
            grant_valid_from=assent.time_at(5),
            grant_valid_to=assent.time_at(20),
        )
        proposal, claim, action = assent.record_proposal(
            ledger,
            include_action=True,
            authorization_policy=artifacts["authorization_policy"],
        )
        assessment = assent.record_type_assessment(
            ledger, proposal, artifacts["monitor"]
        )
        epistemic = assent.decide_epistemically(ledger, proposal, assessment, artifacts)
        outputs = []
        for ordinal, (monitor, outcome) in enumerate(
            zip(monitors, case["outcomes"], strict=True)
        ):
            selected = {**artifacts, "authority_monitor": monitor}
            kwargs = {"assessment_id": "authority:" + str(ordinal)}
            if outcome == "UNKNOWN":
                output = assent.record_authority_failure(
                    ledger,
                    proposal,
                    action,
                    selected,
                    evaluated_grant=artifacts["grant"],
                    **kwargs,
                )
            else:
                output = assent.record_authority_assessment(
                    ledger,
                    proposal,
                    action,
                    selected,
                    outcome=outcome,
                    violated=["actor_in_scope"] if outcome == "VIOLATED" else [],
                    **kwargs,
                )
            outputs.append(output)
        prefixes[case["verdict"]] = (
            ledger.path.read_bytes(),
            (proposal, action, claim, epistemic, outputs, artifacts),
        )
    return registry, prefixes


class DraftCollector:
    """Use the existing test producer without giving it an append capability."""

    def __init__(self, ledger):
        self.replay = ledger.replay
        self.draft = None

    def append_event(self, **draft):
        assert self.draft is None
        self.draft = draft


def standalone_episode(directory, prefixes, case):
    registry, values = prefixes
    content, records = deepcopy(values[case["verdict"]])
    path = directory / "standalone.jsonl"
    path.write_bytes(content)
    ledger = ProtocolLedger(path, registry)
    proposal, action, claim, epistemic, outputs, artifacts = records
    collector = DraftCollector(ledger)
    assent.decide_authorization(
        collector,
        proposal,
        action,
        claim,
        epistemic,
        outputs,
        artifacts,
        cite_grant=True,
    )
    assert collector.draft is not None
    return ledger, collector.draft


def finite_episode(directory, prefixes, case):
    content, request = prefixes[case["verdict"]]
    history = finite.reopen(directory, content)
    draft, _ = finite.event(history, request)
    return history, draft


def records(draft, kind):
    if kind == "standalone":
        return draft["payload"]["decision"], draft["payload"]["transition"]
    data = draft["data"]
    return data["decision"]["value"][0]["record"], data["transition"]["value"][0][
        "record"
    ]


def append(history, draft, kind, case):
    if kind == "standalone":
        history.append_event(**draft)
    else:
        finite.authorize(history, draft, case["verdict"])


def projection(history, kind):
    replay = history.replay()
    if kind == "standalone":
        return {
            "count": replay.event_count,
            "objects": replay.objects,
            "permission": {
                key: value.value for key, value in replay.authorization_states.items()
            },
            "decisions": replay.authorization_decision_ids,
            "knowledge": (replay.acceptance_head, replay.current_claim_by_key),
        }
    protocol = replay.protocol_replay.data
    decisions = {
        identifier
        for identifier, entry in protocol["records"].items()
        if entry["record_type"] == "AuthorizationDecision"
    }
    indexes = protocol["state"]["protocol"]
    # The finite index is introduced by its first decision, not bootstrap.
    # Once a decision exists, a missing or incomplete index is an error.
    if decisions or "authorization_decisions" in indexes:
        assert {
            entry["value"] for entry in indexes["authorization_decisions"]
        } == decisions
    return {
        "count": replay.ledger_event_count,
        "objects": protocol["records"],
        "permission": {
            entry["keys"][0]: entry["value"]
            for entry in protocol["state"]["protocol"]["authorization_states"]
        },
        "decisions": decisions,
        "knowledge": (
            replay.acceptance_head,
            replay.materialization_head,
            protocol["state"]["action_acceptance_head"],
            replay.graph.export_records(),
            replay.change_sets,
        ),
    }


def expected_observation(history, draft, kind, case, before):
    after = projection(history, kind)
    decision, transition = records(draft, kind)
    assert after["count"] == before["count"] + 1
    assert after["permission"] == {decision["action_proposal_id"]: case["state"]}
    assert after["knowledge"] == before["knowledge"]
    assert after["decisions"] - before["decisions"] == {decision["id"]}
    assert set(after["objects"]) - set(before["objects"]) == {
        decision["id"],
        transition["id"],
    }
    for identifier, value in before["objects"].items():
        assert after["objects"][identifier] == value
    applied = after["objects"][decision["id"]]["record"]
    assert applied == decision
    assert applied["authorization_verdict"] == case["verdict"]
    # An actual incompatibility, not normalized away as record equivalence.
    assert applied["relied_on_claim_version_ids"] == (
        ["claim:1"] if kind == "standalone" else []
    )
    ids = applied["authority_assessment_ids"]
    assert len(ids) == 2
    assert applied["triggered_assessment_ids"] == [
        ids[index] for index in case["triggers"]
    ]
    assert [
        after["objects"][identifier]["record"]["assessment_outcome"]
        for identifier in ids
    ] == case["outcomes"]
    assert (applied["authorization_valid_from"] is not None) == (
        case["verdict"] == "AUTHORIZE"
    )
    assert (applied["authorization_valid_to"] is not None) == (
        case["verdict"] == "AUTHORIZE"
    )
    reopened = (
        ProtocolLedger(history.path, history.registry)
        if kind == "standalone"
        else finite.KnowledgeChangeHistory.reopen(history.path)
    )
    assert projection(reopened, kind) == after
    return {
        "state": after["permission"][decision["action_proposal_id"]],
        "verdict": applied["authorization_verdict"],
        "triggers": [
            ids.index(identifier) for identifier in applied["triggered_assessment_ids"]
        ],
    }


def mutate(draft, kind, fault):
    decision, transition = records(draft, kind)
    if fault == "evaluation":
        decision["policy_evaluation_hash"] = content_digest("forged")
    elif fault == "actor":
        decision["authorized_actor_id"] = "actor:other"
    elif fault == "assessment_order":
        decision["authority_assessment_ids"].reverse()
    elif fault == "grant":
        decision["authority_grant_hash"] = content_digest("wrong grant")
    elif fault == "interval":
        decision["authorization_valid_to"] = (
            assent.time_at(21) if kind == "standalone" else "2026-09-07T03:00:00Z"
        )
        if kind == "finite":
            draft["data"]["intervals"]["authorization"]["end"] = decision[
                "authorization_valid_to"
            ]
    elif fault == "transition":
        transition["to_state"] = "BLOCKED"
    elif fault == "source":
        decision["source_record_ids"].remove(decision["action_proposal_id"])
        if kind == "finite":
            draft["data"]["decision_dependencies"]["value"] = list(
                decision["source_record_ids"]
            )
    elif fault == "stale_head":
        decision["base_acceptance_head"] = content_digest("old head")
    else:
        raise AssertionError(f"undeclared mutation: {fault}")
    decision["content_hash"] = record_hash("AuthorizationDecision", decision)
    transition["content_hash"] = record_hash("TransitionRecord", transition)


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["verdict"])
def test_both_owning_histories_match_literal_permissions_and_reopen(
    tmp_path,
    standalone_prefixes,
    finite_prefixes,
    case,
):
    observations = []
    for kind, build, prefixes in (
        ("standalone", standalone_episode, standalone_prefixes),
        ("finite", finite_episode, finite_prefixes),
    ):
        directory = tmp_path / kind
        directory.mkdir()
        history, draft = build(directory, prefixes, case)
        before = projection(history, kind)
        assert set(before["permission"].values()) == {"PENDING"}
        append(history, draft, kind, case)
        observations.append(expected_observation(history, draft, kind, case, before))
        # Agreement is insufficient: an explicitly wrong expected state must fail.
        wrong = {**case, "state": "PENDING"}
        with pytest.raises(AssertionError):
            expected_observation(history, draft, kind, wrong, before)
    assert observations[0] == observations[1]


@pytest.mark.parametrize("fault", TABLE["refused_mutations"])
def test_both_refuse_semantic_mutations_atomically_then_accept_valid_retry(
    tmp_path,
    standalone_prefixes,
    finite_prefixes,
    fault,
):
    case = CASES[0]
    for kind, build, prefixes, refusal in (
        ("standalone", standalone_episode, standalone_prefixes, ProtocolError),
        (
            "finite",
            finite_episode,
            finite_prefixes,
            finite.api().ProtocolProgramRefusal,
        ),
    ):
        directory = tmp_path / kind
        directory.mkdir()
        history, valid = build(directory, prefixes, case)
        invalid = deepcopy(valid)
        mutate(invalid, kind, fault)
        before_bytes = history.path.read_bytes()
        before = projection(history, kind)
        with pytest.raises(refusal):
            append(history, invalid, kind, case)
        assert history.path.read_bytes() == before_bytes
        assert projection(history, kind) == before
        append(history, valid, kind, case)
        expected_observation(history, valid, kind, case, before)


def test_empty_relied_claim_list_is_not_a_shared_authorization_record_shape(
    tmp_path,
    standalone_prefixes,
):
    history, draft = standalone_episode(tmp_path, standalone_prefixes, CASES[0])
    decision, _ = records(draft, "standalone")
    decision["relied_on_claim_version_ids"] = []
    decision["content_hash"] = record_hash("AuthorizationDecision", decision)
    assert (
        finite.authority.decisions.compiled().validate_instance(
            "AuthorizationDecision", decision
        )
        == []
    )
    before = history.path.read_bytes()
    with pytest.raises(
        ProtocolError, match="Required slot 'relied_on_claim_version_ids' missing"
    ):
        append(history, draft, "standalone", CASES[0])
    assert history.path.read_bytes() == before
