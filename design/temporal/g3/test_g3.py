"""G3: what Malleus Core at e7020879 does with the G1 temporal specimens, today.

Every test asserts current behaviour. A test named ``..._today`` passing means
Core still behaves that way; it is not a statement that the behaviour is right.
RESULTS.md says which behaviours are gaps.

    export PYTHONPATH=$PWD/src:$PWD
    python -m pytest design/temporal/g3/test_g3.py -q
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import malleus.compiler as api  # noqa: E402

import blast_radius  # noqa: E402
import queries  # noqa: E402
import report  # noqa: E402
from expected_today import CHANGES, QUERIES, REFUSALS  # noqa: E402


@pytest.fixture(scope="session")
def gate(tmp_path_factory):
    return report.run_all(tmp_path_factory.mktemp("g3"))


def _query(gate, specimen, query_id, branch=""):
    [outcome] = [o for o in gate["queries"] if (o.specimen, o.query_id, o.branch or "") == (specimen, query_id, branch)]
    return outcome


def _field(outcome, name):
    [field] = [f for f in outcome.fields if f.name == name]
    return field


# Every query answer, change and refusal, row by row.


def test_every_query_answer_is_listed_once(gate):
    keys = [(o.specimen, o.query_id, o.branch or "") for o in gate["queries"]]
    assert len(keys) == len(set(keys)) == len(QUERIES) == 100
    assert set(keys) == set(QUERIES)


@pytest.mark.parametrize("key", sorted(QUERIES), ids=lambda k: "-".join(p for p in k if p)[:80])
def test_query_classification_today(gate, key):
    outcome = _query(gate, *key)
    wrong = tuple(f.name for f in outcome.fields if f.status == queries.CORE_WRONG)
    missing = tuple(f.name for f in outcome.fields if f.status == queries.NE)
    reasons = tuple(dict.fromkeys(f.note for f in outcome.fields if f.status == queries.NE and f.note))
    assert (outcome.classification, wrong, missing, reasons) == QUERIES[key]


def test_outcome_counts_today(gate):
    assert Counter(o.classification for o in gate["queries"]) == {
        "ANSWERED_CORRECT": 45, "NOT_EXPRESSIBLE": 53, "ANSWERED_WRONG": 2,
    }
    assert Counter(o.classification for o in gate["refusals"]) == {
        "EXPECTED_REFUSAL_OBSERVED": 10, "EXPECTED_REFUSAL_NOT_OBSERVED": 2,
    }


def test_no_query_matches_a_forbidden_answer_today(gate):
    assert [(o.specimen, o.query_id, o.forbidden_hit) for o in gate["queries"] if o.forbidden_hit] == []


@pytest.mark.parametrize("key", sorted(CHANGES), ids=lambda k: "-".join(k))
def test_change_outcome_today(gate, key):
    specimen, position = key
    [log] = [log for log in gate["runs"][specimen].logs if log.position == position]
    assert log.outcome == CHANGES[key]


@pytest.mark.parametrize("key", sorted(REFUSALS), ids=lambda k: "-".join(k))
def test_refusal_today(gate, key):
    [outcome] = [o for o in gate["refusals"] if (o.specimen, o.refusal_id) == key]
    procedure = tuple((bool(a.supersedes), a.outcome, a.stage, a.reason, a.detail) for a in outcome.procedure)
    alternatives = {k: tuple((a.outcome, a.stage, a.reason) for a in v) for k, v in outcome.alternatives.items()}
    assert (outcome.classification, procedure, alternatives) == REFUSALS[key]


@pytest.mark.parametrize("key", sorted(REFUSALS), ids=lambda k: "-".join(k))
def test_refused_admission_leaves_ledger_bytes_unchanged(gate, key):
    [outcome] = [o for o in gate["refusals"] if (o.specimen, o.refusal_id) == key]
    attempts = list(outcome.procedure) + [a for v in outcome.alternatives.values() for a in v]
    for attempt in attempts:
        if attempt.outcome == "REFUSED" and attempt.stage != "COMPOSE":
            assert attempt.bytes_before == attempt.bytes_after


# The findings, named.


def test_transition_supersession_ends_knowledge_of_prior_version_today(gate):
    """g1-01 PH-K2: a transition is not a correction, yet Core retires r1 at K2."""
    field = _field(_query(gate, "g1-01", "PH-K2"), "metadata[a2].knowledge_until")
    assert (field.status, field.core, field.expected) == (queries.CORE_WRONG, "K2", None)


def test_correction_after_transition_is_dated_at_the_transition_today(gate):
    """g1-01 PH-K3-META: the specimen says a2 stopped being believed at K3."""
    field = _field(_query(gate, "g1-01", "PH-K3-META"), "metadata[a2].knowledge_until")
    assert (field.status, field.core, field.expected) == (queries.CORE_WRONG, "K2", "K3")


def test_correction_of_superseded_report_is_refused_as_a_fork_today(gate):
    [log] = [log for log in gate["runs"]["g1-01"].logs if log.position == "K3"]
    [refused] = [a for a in log.attempts if a.outcome == "REFUSED"]
    assert (refused.stage, refused.reason) == ("CHECK", "CONTENT_RULE_VIOLATED")
    assert refused.detail.endswith("record supersession forks prior record: r1")
    assert log.outcome == "ADMITTED_WITHOUT_SUPERSESSION"


def test_correction_superseding_the_current_version_is_refused_by_valid_time_today(gate):
    attempt = gate["probes"]["P-K3-TARGET-R2"]["attempt"]
    assert attempt.outcome == "REFUSED"
    assert attempt.detail.endswith("record replacement contradicts prior valid time: r2")


def test_relation_to_a_record_blocks_its_supersession_today(gate):
    probe = gate["probes"]["P-REL-SUPERSEDE"]
    assert probe["link"].outcome == "ADMITTED"
    assert probe["transition"].outcome == "REFUSED"
    assert "Target entity 'r1' does not exist" in probe["transition"].detail
    assert probe["transition"].bytes_before == probe["transition"].bytes_after


def test_one_valid_time_per_change_set_forces_a_forbidden_answer_or_a_split_today(gate):
    probe = gate["probes"]["P-R2-ONE-CHANGE"]
    assert probe["INSTANT 2026-05-01"]["q-qty"] == {"kind": "INTERVAL", "from": "2026-05-01T00:00:00Z", "until": None}
    assert probe["NONE_STATED"]["q-price"] == {"kind": "NONE_STATED"}
    assert CHANGES[("g1-08", "R2")] == "SPLIT"


def test_untimed_records_inherit_the_change_set_valid_time_today(gate):
    untimed = gate["probes"]["P-UNTIMED"]
    assert untimed["product:P valid_from"] == api.KnowledgeValidTime("INSTANT", "2026-05-01T00:00:00Z")
    assert untimed["valve:V valid_from"] == api.KnowledgeValidTime("INSTANT", "2026-06-03T09:00:00Z")


def test_decimal_range_does_not_compile_and_float_drops_the_lexical_today(gate):
    probe = gate["probes"]["P-FLOAT"]
    assert probe["decimal"].startswith("BindingRefusal: UNKNOWN_REFERENCE")
    assert probe["float_stored"] == 5.4
    assert probe["float_in_change_set_bytes"] is True


def test_required_multivalued_slot_admits_an_empty_list_today(gate):
    probe = gate["probes"]["P-REQUIRED-EMPTY-LIST"]
    assert probe["attempt"].outcome == "ADMITTED"
    assert probe["stored_evidence_refs"] == []


def test_withheld_artifacts_refuse_the_whole_replay_without_naming_them_today(gate):
    source = gate["probes"]["P-WITHHELD-SOURCE"]
    contract = gate["probes"]["P-WITHHELD-CONTRACT"]
    assert (source["outcome"], source["reason"], source["detail"]) == (
        "REFUSED", "STALE_BASE", "change-set base ledger head is stale",
    )
    assert "src:quote" not in source["detail"]
    assert (contract["outcome"], contract["reason"]) == ("REFUSED", "MALFORMED_HISTORY")


def test_read_command_reads_only_the_head_today(gate):
    probe = gate["probes"]["P-CLI"]
    assert probe["head"]["exit"] == 0
    assert [r["id"] for r in probe["head"]["output"]["records"]] == ["Q1", "Q2", "H1"]
    assert probe["expect A2"]["exit"] == 2
    assert "STALE_BASE" in probe["expect A2"]["output"]


def test_record_trace_refuses_composed_change_sets_today(gate):
    assert gate["probes"]["P-TRACE"]["reason"] == "POPULATION_PLAN_NOT_BOUND"


def test_shipped_state_version_profile_equates_correction_and_transition_today(gate):
    semantics = gate["probes"]["P-PROFILES"]["state-version change_semantics"]
    assert semantics["correction"] == semantics["transition"] == "SUPERSEDE_STATE_VERSION"


# Obligations.


@pytest.mark.parametrize("specimen", sorted({k for k, _ in CHANGES}))
def test_rebuild_reproduces_every_position(gate, specimen):
    assert all(gate["rebuild"][specimen].values())


@pytest.mark.parametrize("specimen", sorted({k for k, _ in CHANGES}))
def test_round_trip_changes_no_carried_field(gate, specimen):
    assert gate["round_trip"][specimen]["differ"] == {}


@pytest.mark.parametrize("specimen", sorted({k for k, _ in CHANGES}))
def test_reads_write_nothing(gate, specimen):
    assert gate["reads_wrote_nothing"][specimen]


# Blast radius at e7020879.


def test_blast_radius_recomposition_reproduces_shipped_identities(gate):
    ids = blast_radius.shipped()
    moved = gate["blast"]["C"]["moved"]
    for name, row in moved.items():
        assert row["before"] == ids[name] != row["after"]


def test_optional_operation_field_is_refused_by_todays_reader(gate):
    assert gate["blast"]["A"]["today's reader on a change set with the field"] == (
        "MALFORMED_CHANGE_SET: operation fields are not closed"
    )


def test_grammar_bump_is_refused_by_todays_reader_and_named_in_18_files(gate):
    b = gate["blast"]["B"]
    assert b["today's reader on the bumped grammar"].startswith("UNSUPPORTED_GRAMMAR")
    assert b["example"]["before"] != b["example"]["after"]
    assert b["files naming the grammar string"]["full"] == 18


def test_builtin_version_bump_file_counts(gate):
    moved = gate["blast"]["C"]["moved"]
    counts = {name: (row["files"]["full"], row["files"]["prefix8"]) for name, row in moved.items()}
    assert counts == {
        "check contract": (2, 6),
        "structural admission policy": (0, 4),
        "normative profile": (0, 4),
        "structural history bundle": (0, 6),
    }
    assert gate["blast"]["C"]["today's builtin registry on the bumped version"].startswith("Core holds no builtin check")


def test_state_version_profile_change_file_counts(gate):
    d = gate["blast"]["D"]
    assert (d["moved"]["state-version profile"]["files"]["full"], d["moved"]["state-version profile"]["files"]["prefix8"]) == (29, 31)
    assert (d["unmoved"]["source-assertion profile"]["full"], d["unmoved"]["object-event profile"]["full"]) == (114, 8)
