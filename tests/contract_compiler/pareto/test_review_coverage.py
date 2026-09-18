"""Declared review accounting, not evaluation of a source or a reviewer."""

from copy import deepcopy
from dataclasses import FrozenInstanceError
from hashlib import sha256
import importlib
import json

import pytest


def canonical(value):
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def identity(value):
    return "sha256:" + sha256(canonical(value)).hexdigest()


def ref(name, value=None):
    return {"id": name, "sha256": identity(name if value is None else value)}


@pytest.fixture
def api():
    return importlib.import_module("malleus.acquisition")


@pytest.fixture
def boundary():
    return {
        "schema": "malleus.interpretation-review-boundary/private-v0",
        "id": "boundary:second-reading",
        "evidence": [ref("source:first"), ref("source:later")],
        "ontology": ref("ontology:current"),
        "knowledge": ref("knowledge:position"),
        "dependencies": [ref("context:current")],
        "interpretations": [ref("interpretation:complete"), ref("interpretation:open")],
    }


def review(boundary, name, outcome="NO_CHANGE"):
    target = next(item for item in boundary["interpretations"] if item["id"] == name)
    return {
        "schema": "malleus.interpretation-review/private-v0",
        "id": "review:" + name,
        "boundary_identity": identity(boundary),
        "interpretation": deepcopy(target),
        "outcome": outcome,
        "rationale": "Compared the earlier interpretation with both retained passages.",
        "supporting_references": deepcopy(boundary["evidence"]),
        "proposed_change": ref("proposal:correction")
        if outcome == "CORRECTION"
        else None,
        "open_issue": "The later passage does not identify the referent."
        if outcome in {"CONFLICT", "UNRESOLVED"}
        else None,
        "affected_uses": [],
    }


def check(api, boundary, reviews=()):
    return api.check_review_coverage(
        boundary_bytes=canonical(boundary),
        review_bytes=tuple(canonical(item) for item in reviews),
    )


def test_new_evidence_requires_review_of_open_and_previously_complete_interpretations(
    api, boundary
):
    earlier = deepcopy(boundary)
    earlier["id"] = "boundary:first-reading"
    earlier["evidence"] = earlier["evidence"][:1]
    old_reviews = [
        review(earlier, "interpretation:complete"),
        review(earlier, "interpretation:open", "UNRESOLVED"),
    ]
    assert check(api, earlier, old_reviews).require_complete().complete

    # Finishing an inventory or reaching a retry bound is not a review input.
    missing = check(api, boundary)
    assert missing.missing == ("interpretation:complete", "interpretation:open")
    assert missing.stale == ()
    with pytest.raises(api.ReviewCoverageRefusal) as caught:
        missing.require_complete()
    assert caught.value.reason is api.ReviewCoverageRefusalReason.INCOMPLETE_REVIEW
    assert all(name in caught.value.detail for name in missing.missing)

    stale = check(api, boundary, old_reviews)
    assert stale.missing == ()
    assert stale.stale == missing.missing
    assert not stale.complete
    resolved_reference = review(boundary, "interpretation:open", "CORRECTION")
    partial = check(api, boundary, [resolved_reference])
    assert partial.missing == ("interpretation:complete",)
    assert not partial.complete

    completed = review(boundary, "interpretation:complete", "UNRESOLVED")
    completed["open_issue"] = (
        "Later evidence qualifies the earlier statement; applicability is still unspecified."
    )
    result = check(api, boundary, [resolved_reference, completed])
    assert result.require_complete() is result
    assert result.complete
    assert result.document["groups"] == {
        "pending_corrections": [resolved_reference],
        "unchanged": [],
        "conflicts": [],
        "unresolved": [completed],
    }


@pytest.mark.parametrize(
    "field", ["evidence", "ontology", "knowledge", "dependencies", "interpretations"]
)
def test_every_declared_context_change_makes_old_reviews_stale(api, boundary, field):
    old = [review(boundary, item["id"]) for item in boundary["interpretations"]]
    changed = deepcopy(boundary)
    target = changed[field][0] if isinstance(changed[field], list) else changed[field]
    target["sha256"] = identity("changed context")
    result = check(api, changed, old)
    assert not result.complete
    assert result.stale == ("interpretation:complete", "interpretation:open")
    with pytest.raises(api.ReviewCoverageRefusal, match="INCOMPLETE_REVIEW"):
        result.require_complete()


@pytest.mark.parametrize(
    "outcome,group",
    [
        ("CORRECTION", "pending_corrections"),
        ("NO_CHANGE", "unchanged"),
        ("CONFLICT", "conflicts"),
        ("UNRESOLVED", "unresolved"),
    ],
)
def test_all_current_dispositions_close_review_without_settling_knowledge(
    api, boundary, outcome, group
):
    reviews = [
        review(boundary, item["id"], outcome) for item in boundary["interpretations"]
    ]
    result = check(api, boundary, reviews)
    assert result.complete
    assert result.document["groups"][group] == reviews
    assert result.boundary_identity == identity(boundary)
    assert result.profile_identity == api.REVIEW_COVERAGE_PROFILE_IDENTITY
    assert result.identity == "sha256:" + sha256(result.canonical_bytes).hexdigest()


def test_order_serialization_and_caller_mutation_do_not_change_the_receipt(
    api, boundary
):
    reviews = [review(boundary, item["id"]) for item in boundary["interpretations"]]
    result = check(api, boundary, reviews)
    boundary["evidence"].reverse()
    boundary["interpretations"].reverse()
    for item in reviews:
        item["supporting_references"].reverse()
    reordered = api.check_review_coverage(
        boundary_bytes=json.dumps(boundary, indent=2).encode(),
        review_bytes=[canonical(item) for item in reversed(reviews)],
    )
    assert reordered.canonical_bytes == result.canonical_bytes
    document = result.document
    document["complete"] = False
    assert result.complete
    with pytest.raises(FrozenInstanceError):
        result.canonical_bytes = b"forged"


@pytest.mark.parametrize(
    "mutation",
    [
        "missing-field",
        "extra-field",
        "empty-set",
        "duplicate-id",
        "invalid-digest",
        "wrong-type",
        "blank-id",
        "unsupported-grammar",
        "conflicting-reference",
    ],
)
def test_bad_boundary_inputs_refuse_without_defaults(api, boundary, mutation):
    if mutation == "missing-field":
        del boundary["knowledge"]
    elif mutation == "extra-field":
        boundary["retry_budget_exhausted"] = True
    elif mutation == "empty-set":
        boundary["interpretations"] = []
    elif mutation == "duplicate-id":
        boundary["interpretations"].append(boundary["interpretations"][0])
    elif mutation == "invalid-digest":
        boundary["evidence"][0]["sha256"] = "sha256:unknown"
    elif mutation == "wrong-type":
        boundary["ontology"] = []
    elif mutation == "blank-id":
        boundary["id"] = " "
    elif mutation == "unsupported-grammar":
        boundary["schema"] = "future"
    else:
        boundary["dependencies"] = [ref("source:first", "different content")]
    with pytest.raises(api.ReviewCoverageRefusal):
        check(api, boundary)


@pytest.mark.parametrize(
    "raw",
    [b'{"id":"a","id":"b"}', b'{"x":NaN}', b"[]", b"null", b"\xff", b"{", b'"\\ud800"'],
)
def test_malformed_wire_has_typed_refusal(api, raw):
    with pytest.raises(api.ReviewCoverageRefusal) as caught:
        api.check_review_coverage(boundary_bytes=raw, review_bytes=())
    assert caught.value.reason is api.ReviewCoverageRefusalReason.MALFORMED_INPUT


@pytest.mark.parametrize(
    "mutation",
    [
        "unknown-interpretation",
        "stale-interpretation",
        "duplicate-review",
        "duplicate-review-id",
        "unsupported-outcome",
        "empty-rationale",
        "empty-support",
        "unbound-support",
        "missing-proposal",
        "unspecific-unresolved",
        "extra-field",
    ],
)
def test_review_contract_refuses_ambiguity_and_missing_payload(api, boundary, mutation):
    item = review(boundary, "interpretation:complete")
    reviews = [item]
    if mutation == "unknown-interpretation":
        item["interpretation"] = ref("unknown")
    elif mutation == "stale-interpretation":
        item["interpretation"]["sha256"] = identity("earlier interpretation")
        result = check(api, boundary, reviews)
        assert result.stale == ("interpretation:complete",)
        assert not result.complete
        return
    elif mutation == "duplicate-review":
        duplicate = deepcopy(item)
        duplicate["id"] = "review:second"
        reviews.append(duplicate)
    elif mutation == "duplicate-review-id":
        other = review(boundary, "interpretation:open")
        other["id"] = item["id"]
        reviews.append(other)
    elif mutation == "unsupported-outcome":
        item["outcome"] = "TRUE"
    elif mutation == "empty-rationale":
        item["rationale"] = " "
    elif mutation == "empty-support":
        item["supporting_references"] = []
    elif mutation == "unbound-support":
        item["supporting_references"] = [ref("source:undeclared")]
    elif mutation == "missing-proposal":
        item["outcome"] = "CORRECTION"
    elif mutation == "unspecific-unresolved":
        item["outcome"] = "UNRESOLVED"
    else:
        item["inventory_complete"] = True
    with pytest.raises(api.ReviewCoverageRefusal):
        check(api, boundary, reviews)


def test_explicit_absence_of_unselected_context_is_not_an_invented_identity(
    api, boundary
):
    boundary["ontology"] = None
    boundary["knowledge"] = None
    assert check(api, boundary).missing


def test_evidence_and_review_leave_real_accepted_history_unchanged(
    api, tmp_path, boundary
):
    from malleus.compiler import KnowledgeChangeHistory
    from tests.contract_compiler.pareto.test_knowledge_change_history import (
        TRANSACTION_TIME,
        _admit_record_change,
        _anchored_history,
        _evidence_anchor,
        _record_change,
    )

    history, compiled, partial, _, source, evidence = _anchored_history(tmp_path)
    change = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="seed",
        record_id="record:one",
        label="original",
        order="seed",
    )
    _admit_record_change(history, change, suffix="seed")
    before = history.replay()
    graph_bytes = canonical(before.graph.export_records())
    boundary["ontology"] = {
        "id": "compiled",
        "sha256": compiled.artifact.validated_fact_set_sha256,
    }
    boundary["knowledge"] = {
        "id": "history-position",
        "sha256": before.receipt.identity,
    }

    new_evidence = canonical(
        {"statement": "A later passage qualifies the earlier statement."}
    )
    history.append_anchors(
        anchors=(_evidence_anchor("later-evidence", new_evidence),),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    after_evidence = history.replay()
    assert after_evidence.receipt.identity != before.receipt.identity
    assert canonical(after_evidence.graph.export_records()) == graph_bytes
    boundary["knowledge"]["sha256"] = after_evidence.receipt.identity
    boundary["evidence"] = [
        {"id": "later-evidence", "sha256": "sha256:" + sha256(new_evidence).hexdigest()}
    ]
    reviews = [
        review(boundary, "interpretation:complete", "UNRESOLVED"),
        review(boundary, "interpretation:open", "CORRECTION"),
    ]
    ledger_bytes = history.path.read_bytes()
    check(api, boundary, reviews).require_complete()
    assert history.path.read_bytes() == ledger_bytes
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    assert canonical(reopened.graph.export_records()) == graph_bytes
    assert reopened.acceptance_head == before.acceptance_head
    assert reopened.materialization_head == before.materialization_head


def test_the_boundary_identity_is_reachable_without_a_dummy_coverage_call(
    api, boundary
):
    """A producer needs the digest before it can author one review.

    On 2026-09-17 three archived reviews of a launched stage carried the
    boundary's ``id`` because the packet gave them no digest and the only route
    to one was calling the coverage checker with an empty review tuple, which
    nobody preparing the run knew. The accessor is that route, named.
    """
    computed = api.review_boundary_identity(boundary_bytes=canonical(boundary))

    assert computed == identity(boundary)
    assert computed == check(api, boundary).boundary_identity


def test_a_boundary_identity_refusal_says_where_the_digest_comes_from(api, boundary):
    """A refusal that names no route is one the producer cannot act on."""
    wrong = review(boundary, "interpretation:open")
    wrong["boundary_identity"] = boundary["id"]

    with pytest.raises(api.ReviewCoverageRefusal) as caught:
        check(api, boundary, [wrong])

    assert caught.value.reason is api.ReviewCoverageRefusalReason.MALFORMED_INPUT
    assert "lowercase SHA-256 identity required" in caught.value.detail
    assert "review_boundary_identity" in caught.value.detail
