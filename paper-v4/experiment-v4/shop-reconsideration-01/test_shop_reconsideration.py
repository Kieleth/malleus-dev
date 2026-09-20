"""Every number the Shop reconsideration subsection prints, read from its file.

Written before the subsection existed, against the manuscript as it then was,
so each assertion failed for the reason it names before it passed. The cell
produces nothing: it binds the manuscript to the frozen outputs of the staged
run, which live under ``private/`` and never enter git.

Two questions are kept apart here. Whether a record says what the manuscript
says it says is answered from the record. Whether the subsection leaks the
chapter's prose is answered from the retained sources and the packets, which
this cell reads and never reproduces.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
        paper-v4/experiment-v4/shop-reconsideration-01/test_shop_reconsideration.py
"""

from __future__ import annotations

import base64
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata

import pytest

import malleus


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAPER = ROOT / "paper-v4"
MANUSCRIPT = PAPER / "manuscript-v4-working.md"
PRIVATE = ROOT / "private/shop-progressive-01"
PRODUCER = PRIVATE / "producer"
ASSESSMENT = PRIVATE / "assessment"
PACKETS = PRIVATE / "packets"

HEADING = "### 3.2 The same history, reconsidered by a model"

# The archives, named by the launch time in their own path. A launched
# workspace is never rebuilt, so these are literals on purpose: a different
# timestamp is a different run and must not pass silently.
ARCHIVES = {
    "A": PRODUCER / "stage-a/archive/2026-09-17T04:48:13Z",
    "B": PRODUCER / "stage-b/archive/2026-09-17T14:37:05Z",
    "C": PRODUCER / "stage-c/archive/2026-09-19T01:12:08Z",
}

COVERAGE = PRODUCER / "stage-c/review-coverage.json"
REPLAY = PRODUCER / "stage-c/replay-verification.json"
REVISION = PRODUCER / "stage-c/revision-receipt.json"
RECORDS = {
    "B": ASSESSMENT / "stage-b-packet/review-record.json",
    "C": ASSESSMENT / "stage-c-packet/review-record.json",
}
RATIFIED = {
    "B": ASSESSMENT / "stage-b-packet/review-record-ratified.json",
    "C": ASSESSMENT / "stage-c-packet/review-record-ratified.json",
}
BINDING = {
    "B": PAPER / "evaluation-v4/author-ratification-2026-09-17-shop-staged-review.md",
    "C": PAPER / "evaluation-v4/author-ratification-2026-09-18-shop-third-boundary.md",
}

# Two Core coordinates, kept apart on purpose.
#
# RUN_CORE is the Core the third boundary ran against. It is a fact about the
# run, recorded in the run's own replay verification under ``private/`` and in
# this cell's README, and it never moves.
RUN_CORE = "d5d014ba1d7e3bfe906bc71dc93ded5657a3b424"
CORE_GOVERNANCE_HEAD = "OVR-000464"
MAIN_AT_CLOSE_OUT = "ff1c69315f68de949a223aedd3175e0319802807"

# GATE_CORE is the Core the paper gate exports and this module imports, bound
# by the bytes of the package rather than by the path it is imported from. The
# value is what ``git archive d89a0c4718654249ad678eaff62e7b1daba30b6f
# src/malleus`` produces, and the private export
# ``private/shop-progressive-01/runtime-d89a0c47`` gives the same 53 modules
# and the same digest, which is what makes that export that commit's Core.
#
# Moved on 2026-09-19 from d5d014ba, 52 modules
# sha256:f2fd444d…e73c, to the sealed one-call-admission Core, under E-0436:
# when Core changes the paper's pin moves to it, the cells re-run on it and the
# new fingerprints are the baseline. The one module added is
# ``_contract_pipeline/admission.py``. Nothing this cell reads moved with it;
# the cell reads frozen records and produces nothing.
GATE_CORE = "d89a0c4718654249ad678eaff62e7b1daba30b6f"
CORE_MODULE_COUNT = 53
CORE_SOURCE_DIGEST = (
    "sha256:340196130e1820e9a4f9979223f40dcf6b8c1227d8805d812fd08ca529a3ed04"
)


# ---------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------


def manuscript() -> str:
    return MANUSCRIPT.read_text()


def subsection() -> str:
    body = manuscript()
    assert HEADING in body, f"the manuscript carries no {HEADING!r}"
    return body.split(HEADING, 1)[1].split("\n## 4. ", 1)[0]


def prose() -> str:
    """One line, so an assertion binds a claim and not a line break."""
    return " ".join(subsection().split())


def load(path: Path):
    return json.loads(path.read_bytes())


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def archive_manifest(stage: str):
    return load(ARCHIVES[stage] / "ARCHIVE.json")


def history_lines(stage: str) -> list[bytes]:
    return (ARCHIVES[stage] / "work/history.jsonl").read_bytes().splitlines(keepends=True)


def reviews(stage: str) -> dict[str, dict]:
    directory = ARCHIVES[stage] / "work/reviews"
    return {path.name: load(path) for path in sorted(directory.iterdir())}


def retained_receipt(stage: str, receipt_id: str) -> dict:
    """The check receipt as the history retains it, not as a report restates it.

    Core registers the receipt bytes in the ledger; the counts and the rule
    identifiers below are read back out of those bytes, from the ``check``
    member that carries the verifier's own result.
    """

    for line in history_lines(stage):
        event = json.loads(line)
        payload = event.get("payload", {})
        if payload.get("record_id") != receipt_id:
            continue
        return json.loads(base64.b64decode(payload["retained_bytes_base64"]))["check"]
    raise AssertionError(f"{receipt_id} is not retained in stage {stage}'s history")


def core_source_identity(package) -> tuple[int, str]:
    """Digest every module of the imported package, by a declared method.

    Each ``.py`` file under the package root, keyed by its path relative to
    that root and valued by the SHA-256 of its bytes, serialised as canonical
    JSON and digested again. Path-independent, so an export and a checkout of
    the same Core give the same answer. The method is rule-census-01's, so the
    two cells' pins are comparable.
    """

    root = Path(package.__file__).resolve().parent
    rows = {
        str(path.relative_to(root)): sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*.py"))
    }
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return len(rows), "sha256:" + sha256(blob).hexdigest()


# ---------------------------------------------------------------------------
# The Core the records were produced on, and the Core the gate imports
# ---------------------------------------------------------------------------


def test_the_imported_core_is_the_pin_the_gate_declares():
    count, source = core_source_identity(malleus)
    assert (count, source) == (CORE_MODULE_COUNT, CORE_SOURCE_DIGEST), (
        f"imported Core is not the pin {GATE_CORE}: {count} modules, {source}, "
        f"from {Path(malleus.__file__).resolve()}"
    )


def test_the_checker_the_certificate_names_is_a_shipped_core_capability():
    from malleus.acquisition import check_review_coverage

    assert callable(check_review_coverage)
    assert load(COVERAGE)["checker"] == "malleus.acquisition.check_review_coverage"


def test_the_replay_verification_names_the_core_the_readme_and_the_run_core():
    """The run's Core, not the gate's.

    The third boundary was produced on ``d5d014ba`` and its replay
    verification says so. The gate's pin moved to ``d89a0c47`` on 2026-09-19
    (E-0436) and this record did not move with it, because a record of what a
    run was produced on is not a coordinate anyone is free to re-point.
    """

    replay = load(REPLAY)
    assert replay["core_commit"] == RUN_CORE
    assert replay["core_governance_head"] == CORE_GOVERNANCE_HEAD
    readme = (HERE / "README.md").read_text()
    assert RUN_CORE in readme and CORE_GOVERNANCE_HEAD in readme
    assert MAIN_AT_CLOSE_OUT in readme
    assert GATE_CORE in readme, "the README does not name the Core the gate pins"


# ---------------------------------------------------------------------------
# The condition: three fresh sessions on one growing history
# ---------------------------------------------------------------------------


def test_three_producer_sessions_were_archived_one_per_instalment():
    """The table population's archive is honest about where it came from.

    Its workspace was destroyed by a later test fixture and recovered byte for
    byte from the producer session's transcript, so its manifest records
    ``archived_from_workspace`` false and a recovery source. The two boundaries
    the subsection rests on were archived straight from their own workspaces.
    """

    stages = {stage: archive_manifest(stage) for stage in ARCHIVES}
    assert [stages[key]["stage"] for key in ("A", "B", "C")] == ["A", "B", "C"]
    assert stages["A"]["archived_from_workspace"] is False
    assert stages["A"]["source"].startswith("recovery/")
    assert stages["B"]["archived_from_workspace"] is True
    assert stages["C"]["archived_from_workspace"] is True
    assert "Three fresh" in prose()


def test_every_archived_file_still_matches_its_manifest():
    for stage, root in ARCHIVES.items():
        manifest = archive_manifest(stage)
        for entry in manifest["files"]:
            path = root / "work" / entry["path"]
            assert digest(path) == entry["sha256"].removeprefix("sha256:"), (
                f"stage {stage}: {entry['path']} moved since it was archived"
            )
        assert manifest["file_count"] == len(manifest["files"])


def test_neither_boundary_rewrote_what_it_inherited():
    a, b, c = history_lines("A"), history_lines("B"), history_lines("C")
    assert (len(a), len(b), len(c)) == (22, 38, 50)
    assert b[:22] == a, "the second boundary did not inherit the table population byte for byte"
    assert c[:38] == b, "the third boundary did not inherit the second boundary byte for byte"
    replay = load(REPLAY)
    assert replay["history"]["lines"] == 50
    assert replay["history"]["inherited_prefix_lines"] == 41
    assert replay["history"]["inherited_prefix_sha256"] == "sha256:" + sha256(
        b"".join(c[:41])
    ).hexdigest()
    body = prose()
    assert "first 22 lines" in body
    assert "first 41 lines of the third boundary's 50" in body


# ---------------------------------------------------------------------------
# What each producer answered
# ---------------------------------------------------------------------------


def test_the_reviews_written_at_each_boundary_match_the_archives():
    second = reviews("B")
    third = reviews("C")
    assert len(second) == 3 and len(third) == 5
    assert sorted(review["outcome"] for review in second.values()) == [
        "CORRECTION",
        "CORRECTION",
        "NO_CHANGE",
    ]
    assert sorted(review["outcome"] for review in third.values()) == [
        "CORRECTION",
        "NO_CHANGE",
        "NO_CHANGE",
        "NO_CHANGE",
        "NO_CHANGE",
    ]
    body = prose()
    assert "answered NO_CHANGE once and CORRECTION twice" in body
    assert "answered NO_CHANGE four times and CORRECTION once" in body


def test_the_declared_gaps_are_counted_from_the_plans_and_the_verification():
    second = [
        gap
        for name in sorted((ARCHIVES["B"] / "work").glob("plan-*.json"))
        for gap in load(name)["gaps"]
    ]
    assert sorted(gap["kind"] for gap in second) == ["RELATION_ABSENT", "TYPE_ABSENT"]
    third = [
        gap
        for entry in load(REPLAY)["gaps"].values()
        for gap in entry["gaps"]
    ]
    assert [gap["kind"] for gap in third] == ["RELATION_ABSENT"]
    body = prose()
    assert "declared two gaps, of kinds TYPE_ABSENT and RELATION_ABSENT" in body
    assert "declared one gap, of kind RELATION_ABSENT" in body


def test_the_admissions_match_the_change_sets_the_replay_reads():
    operations = {
        entry["change_set_id"]: entry["operations"] for entry in load(REPLAY)["change_sets"]
    }
    assert operations["change:shop-context-order-relationship-v1"] == 5
    assert operations["change:shop-context-shipment-eligibility-v1"] == 5
    assert operations["change:shop-context-order-correction-v1"] == 2
    body = prose()
    assert "two change sets of five operations each" in body
    assert "one change set of two operations" in body


# ---------------------------------------------------------------------------
# The layer every SATISFIED verdict tested
# ---------------------------------------------------------------------------


def test_the_rule_layer_numbers_come_from_the_retained_check_receipt():
    receipt = retained_receipt("C", "receipt:change:shop-context-order-correction-v1")
    assert receipt["outcome"] == "SATISFIED"
    assert receipt["violations"] == []
    assert receipt["fact_count"] == 764
    assert receipt["checked_rule_ids"] == ["NO_CONFLICTING_QUANTITY", "NO_EMPTY_RECORD"]
    assert receipt["engine_name"] == "SWI-Prolog"
    assert receipt["contract_hash"] == load(REVISION)["required_check_after"]
    body = prose()
    assert "764 compiled facts" in body
    assert "zero violations" in body
    assert "NO_CONFLICTING_QUANTITY and NO_EMPTY_RECORD" in body


def test_the_second_boundarys_two_admissions_were_checked_and_satisfied():
    recorded = [
        json.loads(line)["payload"]
        for line in history_lines("B")
        if json.loads(line)["event_type"] == "CHECK_RECORDED"
    ]
    at_this_boundary = [
        payload
        for payload in recorded
        if payload["proposal_id"].startswith("proposal:change:shop-context-")
    ]
    assert len(at_this_boundary) == 2
    assert {payload["outcome"] for payload in at_this_boundary} == {"SATISFIED"}


def test_a_structural_claim_never_stands_alone_where_the_rules_ran():
    """Luis's rule: say which layer a result tested, and never let a narrower
    test read as the whole gate. Here the rules did run, so every mention of
    the structural gate in this subsection names them in the same breath."""

    body = prose()
    for match in re.finditer(r"structural gate", body):
        tail = body[match.end() : match.end() + 40]
        assert tail.startswith(" plus the two Prolog rules"), (
            f"unqualified structural-gate claim: ...{body[match.start():match.end() + 40]}..."
        )
    assert "structural gate alone" not in body


# ---------------------------------------------------------------------------
# The two review-coverage certificates
# ---------------------------------------------------------------------------


def test_the_third_boundarys_certificate_is_complete_over_the_producers_reviews():
    coverage = load(COVERAGE)
    assert coverage["complete"] is True
    assert coverage["missing"] == [] and coverage["stale"] == []
    assert coverage["require_complete"] == "require_complete() RETURNED WITHOUT RAISING"
    assert coverage["boundary_identity"] == coverage["declared_boundary_identity"]
    groups = coverage["document"]["groups"]
    assert len(groups["pending_corrections"]) == 1
    assert len(groups["unchanged"]) == 4
    assert groups["conflicts"] == [] and groups["unresolved"] == []
    read = {
        name: value.removeprefix("sha256:")
        for name, value in coverage["reviews_read"].items()
    }
    for name, value in read.items():
        assert digest(ARCHIVES["C"] / "work/reviews" / name) == value, (
            f"{name} is not the file the checker read"
        )
    body = prose()
    assert "nothing missing and nothing stale" in body
    assert "one pending correction and four unchanged" in body
    assert "exactly as the session wrote them" in body


def test_the_second_boundarys_reviews_carry_the_name_where_the_digest_is_required():
    carried = {review["boundary_identity"] for review in reviews("B").values()}
    assert carried == {"reading:shop-context-stage-b"}
    assert not any(value.startswith("sha256:") for value in carried)
    third = {review["boundary_identity"] for review in reviews("C").values()}
    assert third == {load(COVERAGE)["boundary_identity"]}
    binding = " ".join(BINDING["B"].read_text().split())
    assert "the producer's reviews carry the boundary's name where the checker" in binding
    assert "requires its identity digest, a packet defect" in binding
    body = prose()
    assert "has no completion certificate as produced" in body
    assert "the boundary's name in the field where the checker requires" in body


# ---------------------------------------------------------------------------
# The recorded additive ontology revision
# ---------------------------------------------------------------------------


def test_the_revision_paragraph_matches_the_receipt():
    receipt = load(REVISION)
    assert receipt["status"] == "RECORDED"
    assert receipt["actor_id"] == "actor:luis"
    assert receipt["changes"] == ["ADD_CLASS", "ADD_CLASS", "REBIND_CHECK_CONTRACT"]
    assert receipt["graph_unchanged"] is True
    assert (receipt["ledger_events_before"], receipt["ledger_events_after"]) == (38, 41)
    assert receipt["required_check_before"] != receipt["required_check_after"]
    retained = load(REPLAY)["retained_rule_contract"]
    assert (
        retained["shop-run-d-content-rules:rules:ae8de5879af5"]
        == retained["shop:run-d-content-rules:rules"]
    ), "the rule bytes moved across the revision"
    body = prose()
    assert "two classes added" in body
    assert "the rule bytes unchanged" in body
    assert "38 events to 41" in body
    assert receipt["revision_identity"].removeprefix("sha256:") in manuscript()


def test_the_receipts_written_before_the_revision_keep_their_own_contract():
    before = load(REVISION)["required_check_before"]
    after = load(REVISION)["required_check_after"]
    recorded = [
        json.loads(line)["payload"]
        for line in history_lines("C")
        if json.loads(line)["event_type"] == "CHECK_RECORDED"
    ]
    assert len(recorded) == 5
    earlier = [payload for payload in recorded if payload["check_contract_identity"] == before]
    later = [payload for payload in recorded if payload["check_contract_identity"] == after]
    assert len(earlier) == 4 and len(later) == 1
    assert {payload["outcome"] for payload in recorded} == {"SATISFIED"}
    body = prose()
    assert "the four check receipts written before it" in body


def test_the_graph_is_byte_identical_across_the_revision():
    """``graph_unchanged`` is the receipt's word; this checks the bytes it
    names, the second boundary's archived export, are the ones on disk."""

    exported = ARCHIVES["B"] / "work/stage-b-export.json"
    recorded = next(
        entry["sha256"]
        for entry in archive_manifest("B")["files"]
        if entry["path"] == "stage-b-export.json"
    )
    assert "sha256:" + digest(exported) == recorded
    assert load(REVISION)["graph_unchanged"] is True


# ---------------------------------------------------------------------------
# The assessors and the author
# ---------------------------------------------------------------------------


COUNTS = {
    "B": {"correctly_changed": 2, "correctly_preserved": 1, "missed": 0, "spurious": 0},
    "C": {"correctly_changed": 1, "correctly_preserved": 4, "missed": 0, "spurious": 0},
}
OBLIGATIONS = {"B": 3, "C": 5}


@pytest.mark.parametrize("stage", ["B", "C"])
def test_the_assessors_counts_are_the_records_own(stage):
    record = load(RECORDS[stage])
    assert record["counts"] == COUNTS[stage]
    assert len(record["obligations"]) == OBLIGATIONS[stage]
    assert sum(record["counts"].values()) == OBLIGATIONS[stage]
    assert record["status"] == "PRELIMINARY_COMPLETE"
    assert record["ratification"]["status"] == "PENDING"


@pytest.mark.parametrize("stage", ["B", "C"])
def test_ratifying_changed_no_judgement(stage):
    record, ratified = load(RECORDS[stage]), load(RATIFIED[stage])
    assert ratified["counts"] == record["counts"]
    assert ratified["obligations"] == record["obligations"]
    assert ratified["inputs"] == record["inputs"]
    assert ratified["schema"] == record["schema"]
    assert ratified["status"] == "HUMAN_RATIFIED"
    block = ratified["ratification"]
    assert block["status"] == "RATIFIED" and block["actor_id"] == "actor:luis"
    assert block["binding_file"] == str(BINDING[stage].relative_to(ROOT))
    assert block["binding_file_sha256"] == "sha256:" + digest(BINDING[stage])
    without_block = {key: value for key, value in ratified.items() if key != "ratification"}
    blob = json.dumps(without_block, sort_keys=True, separators=(",", ":")).encode("utf-8")
    assert block["record_sha256"] == "sha256:" + sha256(blob).hexdigest()


@pytest.mark.parametrize("stage", ["B", "C"])
def test_each_binding_file_names_the_record_it_ratifies(stage):
    """And states, in its own bytes, that the certificate is outside its scope."""

    binding = " ".join(BINDING[stage].read_text().split())
    assert digest(RECORDS[stage]) in binding
    assert "Scope:" in binding
    assert "review-coverage certificate" in binding
    excluded = (
        "It does not cover the run's review-coverage certificate",
        "it is a mechanical result of Core's checker and is recorded, not ratified",
    )
    assert any(phrase in binding for phrase in excluded), (
        "the binding file does not put the certificate outside its scope"
    )


def test_the_two_boundary_rows_match_the_records():
    body = manuscript()
    for stage, label in (("B", "second"), ("C", "third")):
        counts = load(RECORDS[stage])["counts"]
        row = (
            f"| {label} "
            f"| {OBLIGATIONS[stage]} "
            f"| {counts['correctly_changed']} "
            f"| {counts['correctly_preserved']} "
            f"| {counts['missed']} "
            f"| {counts['spurious']} "
        )
        assert row in body, f"the {label} boundary's row does not match its record"
    assert "| 8 |" not in body.split(HEADING, 1)[1].split("\n## 4. ", 1)[0]


def test_the_counts_are_declared_tallies_and_never_a_rate():
    body = prose()
    assert "not a rate, a score or a percentage" in body
    assert "eight judgements" in body
    # "percentage" is the word the disclaimer itself uses, so the guard names
    # the constructions a reader would mistake for a measured rate. Whole words
    # only: the digest table is full of hexadecimal that spells short tokens.
    forbidden = ("accuracy", "success rate", "completion rate", "f1", "precision", "recall")
    for word in forbidden:
        assert not re.search(rf"\b{word}\b", body.lower()), f"the subsection uses {word!r}"
    assert "%" not in body
    assert "how often" in body, "the subsection does not refuse a frequency claim"


# ---------------------------------------------------------------------------
# The digests a reader needs, and the prose that must not carry the chapter
# ---------------------------------------------------------------------------


PRINTED_DIGESTS = {
    "review-coverage.json": COVERAGE,
    "replay-verification.json": REPLAY,
    "revision-receipt.json": REVISION,
    "stage-b review-record.json": RECORDS["B"],
    "stage-c review-record.json": RECORDS["C"],
    "stage-b review-record-ratified.json": RATIFIED["B"],
    "stage-c review-record-ratified.json": RATIFIED["C"],
    "second binding file": BINDING["B"],
    "third binding file": BINDING["C"],
}


def test_every_sixty_four_character_digest_in_the_subsection_names_a_real_file():
    printed = set(re.findall(r"\b[0-9a-f]{64}\b", subsection()))
    assert printed, "the subsection prints no digest a reader could check"
    available = {digest(path) for path in PRINTED_DIGESTS.values()}
    available |= {
        entry["sha256"].removeprefix("sha256:")
        for stage in ARCHIVES
        for entry in archive_manifest(stage)["files"]
    }
    available |= {
        value.removeprefix("sha256:")
        for key, value in load(REVISION).items()
        if isinstance(value, str) and value.startswith("sha256:")
    }
    available |= {
        load(COVERAGE)[key].removeprefix("sha256:")
        for key in ("identity", "boundary_identity", "profile_identity")
    }
    available |= {
        entry["identity"].removeprefix("sha256:") for entry in load(REPLAY)["change_sets"]
    }
    available |= {
        load(REPLAY)["replay"][key].removeprefix("sha256:")
        for key in ("export_sha256", "receipt_identity", "contract_identity", "ontology_hash")
    }
    available |= {
        entry["sha256"].removeprefix("sha256:")
        for entry in load(REPLAY)["check_receipts"].values()
    }
    available |= {
        value.removeprefix("sha256:")
        for value in load(REPLAY)["history"].values()
        if isinstance(value, str) and value.startswith("sha256:")
    }
    unknown = printed - available
    assert not unknown, f"digests in the subsection that no frozen file carries: {sorted(unknown)}"


def test_the_digest_table_rows_match_the_files_they_name():
    body = subsection()
    for label, path in PRINTED_DIGESTS.items():
        if str(path.relative_to(ROOT)) not in body and path.name not in body:
            continue
        assert digest(path) in body, f"{label} is named without its current digest"


def normalised(text: str) -> str:
    """Letters and digits only, case folded, accents dropped.

    The comparison the public-file rule is written against: a shared run
    survives re-spacing, re-casing and punctuation changes.
    """

    stripped = unicodedata.normalize("NFKD", text)
    return "".join(
        char for char in stripped.casefold() if char.isalnum()
    )


def runs_of(text: str, width: int = 60) -> set[str]:
    value = normalised(text)
    return {value[index : index + width] for index in range(0, max(len(value) - width + 1, 0))}


SHOP_SOURCES = (
    ROOT
    / "research/ontology_driven_kg_realization/experiments/small_shop/connected_story/sources"
)


def test_the_subsection_shares_no_long_run_with_the_chapter_or_the_packets():
    """The three packets carry the chapter's text this run used.

    ``packets/stage-a/table-1.jsonl`` is byte-identical to the transcription
    the repository already holds, and the two context packets are the four
    passages of that transcription split three and one, the fourth withheld
    until the third boundary. The public copies are read here as well so the
    guard does not depend on a private declaration to have any teeth.
    """

    guarded = [
        PACKETS / name
        for name in ("stage-a/table-1.jsonl", "stage-b/context.jsonl", "stage-c/context.jsonl")
    ]
    guarded += [
        ARCHIVES["C"] / "work/stage-c-context.jsonl",
        SHOP_SOURCES / "table-1.jsonl",
        SHOP_SOURCES / "context.jsonl",
    ]
    for path in guarded:
        assert path.exists(), f"declared private fixture missing: {path}"
    mine = runs_of(subsection())
    assert mine, "the subsection is too short to check"
    for path in guarded:
        shared = mine & runs_of(path.read_text())
        assert not shared, (
            f"the subsection shares a 60 character run with {path.name}: "
            f"{sorted(shared)[0][:20]}..."
        )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def test_the_cell_is_registered_under_the_paper_gate():
    manifest = load(PAPER / "active-test-manifest.json")
    relative = "paper-v4/experiment-v4/shop-reconsideration-01/test_shop_reconsideration.py"
    assert relative in manifest["paths"]
    pins = {pin["commit"]: pin for pin in manifest["core_pins"] if relative in pin["paths"]}
    assert GATE_CORE in pins, "the cell's Core is not a declared pin"
    assert relative in pins[GATE_CORE]["paths"]


def test_the_private_outputs_this_cell_reads_are_declared():
    manifest = load(PAPER / "active-test-manifest.json")
    declared = manifest["private_fixture_patterns"]
    for path in (
        "private/shop-progressive-01/packets",
        "private/shop-progressive-01/producer/stage-a/archive",
        "private/shop-progressive-01/producer/stage-b/archive",
        "private/shop-progressive-01/producer/stage-c",
        "private/shop-progressive-01/assessment/stage-b-packet",
        "private/shop-progressive-01/assessment/stage-c-packet",
    ):
        assert path in declared, f"{path} is read here and not declared"


def test_the_private_tree_is_ignored_by_git():
    import subprocess

    result = subprocess.run(
        ["git", "check-ignore", "-q", str(PRIVATE / "D0-REPORT.md")],
        cwd=ROOT,
        capture_output=True,
    )
    assert result.returncode == 0, "private/shop-progressive-01 is not ignored by git"


def test_the_readme_binds_the_cell_before_the_section():
    readme = (HERE / "README.md").read_text()
    for phrase in (
        "The exact claim this cell puts in the paper",
        "The smallest observation that supports or falsifies it",
        "The artifacts reused",
        "What this cell excludes",
    ):
        assert phrase in readme
    for path in PRINTED_DIGESTS.values():
        assert digest(path) in readme, f"{path.name} is bound in the cell without its digest"
