"""RED before GREEN: the environment, the extraction, and the five candidates.

Nothing here admits anything, runs Prolog, or writes outside this cell and its
private directory.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_23 = ROOT / "private/paper-v4-v4-run-23"

# Core's identity, bound by the bytes of the package that was imported rather
# than by the path it was imported from. See the test below for why the commit
# itself is not available to assert.
#
# Moved on 2026-09-19 from e7937b89917c8da7ee4a08acc22e99ad12b9985b, 52 modules
# sha256:d57f3cc9…b1355, to the sealed one-call-admission Core, 53 modules,
# under E-0436: when Core changes the paper's pin moves to it, the cells re-run
# on it and the new fingerprints become the baseline. The one module added is
# ``_contract_pipeline/admission.py``, which carries
# ``check_and_admit_population_plan``. The census itself was measured on
# e7937b89 and RESULTS.md still names that coordinate; nothing this cell
# measures moved with the pin.
CORE_COMMIT = "d89a0c4718654249ad678eaff62e7b1daba30b6f"
CORE_MODULE_COUNT = 53
CORE_SOURCE_DIGEST = (
    "sha256:340196130e1820e9a4f9979223f40dcf6b8c1227d8805d812fd08ca529a3ed04"
)

# This cell's own modules, the way bridge-01 and fault-injection-02 reach
# theirs. The paper gate collects paper-v4/experiment-v4 as a directory and
# runs pytest from the repository root, so a bare import does not resolve.
sys.path.insert(0, str(HERE))

import census  # noqa: E402
import malleus  # noqa: E402
import malleus.logic  # noqa: E402


# ---------------------------------------------------------------------------
# The Core this census measured against
# ---------------------------------------------------------------------------


def core_source_identity(package) -> tuple[int, str]:
    """Digest every module of the imported package, by a declared method.

    Each ``.py`` file under the package root, keyed by its path relative to
    that root and valued by the SHA-256 of its bytes, serialised as canonical
    JSON and digested again. Path-independent, so an export and a checkout of
    the same Core give the same answer.
    """

    root = Path(package.__file__).resolve().parent
    rows = {
        str(path.relative_to(root)): sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*.py"))
    }
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return len(rows), "sha256:" + sha256(blob).hexdigest()


def test_the_imported_core_is_the_pinned_one_by_its_own_bytes():
    """Bind Core by identity, not by the path it happens to sit at.

    **The commit is not recoverable from the package bytes alone.** A gate
    export is ``git archive <commit> src/malleus ontology``, which carries no
    commit metadata, no ``RUNTIME.md`` and no
    ``design/contract_compiler/overseer/head.json``. Those are the two markers
    ``private/shop-progressive-01/d0/runner.py:core_markers`` reads, and a
    check for either would refuse every gate export. So this test asserts the
    strongest identity the bytes do support: a digest over every module of the
    package that was actually imported.

    The pinned value is what ``git archive d89a0c4718654249ad678eaff62e7b1daba30b6f
    src/malleus`` produces. The correspondence between the commit and these
    bytes is made by the export command, once, outside this test; the test's
    job is to refuse a Core whose bytes are not those.

    **The pin moved on 2026-09-19** from ``e7937b89`` to ``d89a0c47``, the
    sealed Core that carries the one-call atomic admission, under E-0436:
    when Core changes the paper's pin moves to it and the cells re-baseline
    on it. Old value 52 modules ``sha256:d57f3cc9…b1355``, new value 53
    modules ``sha256:340196…3ed04``; it moved because Core's own bytes moved,
    one module added. Everything this cell measures was re-run on the new pin
    through the gate and did not move.
    """

    count, digest = core_source_identity(malleus)
    assert (count, digest) == (CORE_MODULE_COUNT, CORE_SOURCE_DIGEST), (
        f"imported Core is not the pin {CORE_COMMIT}: "
        f"{count} modules, {digest}, from {Path(malleus.__file__).resolve()}"
    )


def test_the_fact_contract_is_version_three():
    """A property of the Core in use, not a binding of which Core it is.

    More than one Core declares version 3, so this discriminates far less than
    the digest above and never stands in for it.
    """

    assert malleus.logic.FACT_CONTRACT_VERSION == "3"


def test_the_private_directory_is_ignored_by_git():
    assert census.private_is_ignored(census.PRIVATE)


# ---------------------------------------------------------------------------
# The document extraction, against run-23's own frozen plan
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def document():
    return census.load_document()


def test_the_document_population_is_run_23s_own(document):
    assert len(document.records) == 440
    assert sum(1 for record in document.records.values() if record.cited) == 236
    assert len(document.texts) == 333


def test_the_adapter_reproduces_run_23s_frozen_derivations(document):
    frozen = json.loads((RUN_23 / "results/population-plan.json").read_bytes())
    assert document.derivation_rows == [
        (item["record_id"], tuple(item["path"]), item["locator"])
        for item in frozen["derivations"]
    ]


def test_every_derivation_locator_names_a_retained_assertion(document):
    assert {locator for _, _, locator in document.derivation_rows} <= set(
        document.texts
    )


def test_the_compiled_ontology_is_run_23s(document):
    assert document.ontology_hash == (
        "67e164bcc578fb4714eb4c59eb7559c3f10f412b599a2306ef6d8433ba7a73cd"
    )


def test_nothing_under_the_run_23_directory_was_opened_for_writing(document):
    assert document.workspace.is_relative_to(census.PRIVATE)
    assert not document.workspace.is_relative_to(RUN_23)


# ---------------------------------------------------------------------------
# The declared slots come from the compiled contract, not from a hand list
# ---------------------------------------------------------------------------


def test_the_numeric_slots_come_from_the_contract_not_from_a_named_list(document):
    """The contract declares eight, not the five the candidate names."""

    assert census.numeric_slots(document) == {
        "assertion_confidence",
        "count",
        "publication_year",
        "ratio_value",
        "strength",
        "uncertainty",
        "value_lower",
        "value_upper",
    }
    assert census.NAMED_NUMERIC_SLOTS < census.numeric_slots(document)


def test_the_three_extra_numeric_slots_change_no_count_on_run_23(document):
    """Measured, not assumed: they are unset, or set only on uncited records."""

    for reading in census.NUMBER_READINGS:
        for scope in census.SCOPES:
            declared = census.number_in_text(document, scope, reading)
            named = census.number_in_text(
                document, scope, reading, slots=census.NAMED_NUMERIC_SLOTS
            )
            assert declared == named, (scope, reading[0])


def test_the_unit_slot_is_declared_string(document):
    assert census.declared_range(document, "GeophysicalObservation", "unit") == "String"


def test_the_formula_slots_are_declared_string(document):
    assert (
        census.declared_range(document, "GeochemicalObservation", "analyte") == "String"
    )
    for slot in ("numerator_kind", "denominator_kind"):
        assert census.declared_range(document, "ElementRatio", slot) == "String"


def test_assertion_modality_is_a_declared_enum(document):
    assert (
        census.declared_range(document, "GeophysicalObservation", "assertion_modality")
        == "AssertionModality"
    )


# ---------------------------------------------------------------------------
# The Shop extraction
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def shop():
    return census.load_shop()


def test_the_shop_population_is_the_honest_table_1(shop):
    assert len(shop.records) == 106
    assert len(shop.derivation_rows) == 294


def test_the_shop_declares_one_numeric_slot(shop):
    assert census.numeric_slots(shop) == {"ordered_quantity"}


def test_the_shop_declares_none_of_the_document_quantity_slots(shop):
    for slot in ("subject", "quantity_kind", "count_scope", "unit", "analyte"):
        assert census.declared_anywhere(shop, slot) is False, slot


# ---------------------------------------------------------------------------
# The five candidates
# ---------------------------------------------------------------------------


def test_candidate_a_reproduces_the_prolog_result_without_the_added_qualifier(document):
    refusals = census.conflicting_quantity(document, with_modality=False)
    assert len(refusals) == 1
    assert set(refusals[0].record_ids) == {"obs:bdb-isotherm", "obs:h1-isotherms"}


def test_candidate_a_with_assertion_modality_added(document):
    refusals = census.conflicting_quantity(document, with_modality=True)
    assert [r.record_ids for r in refusals] == []


def test_candidate_a_has_no_reach_on_the_shop(shop):
    assert census.conflicting_quantity(shop, with_modality=False) == []


def test_candidate_b_reads_only_records_that_set_its_slots(document):
    for refusal in census.interval_sanity(document):
        assert refusal.clause in census.INTERVAL_CLAUSES


def test_candidate_b_catches_a_planted_inversion(document):
    planted = census.with_planted_bounds(
        document, "value_lower", 9.0, "value_upper", 1.0
    )
    clauses = {r.clause for r in census.interval_sanity(planted)}
    assert "value_lower<=value_upper" in clauses


def test_candidate_c_compares_numbers_and_not_spellings(document):
    """991.0 in a float slot is 991 in the sentence, under both live readings."""

    for reading in census.NUMBER_READINGS:
        matched = census.number_matches(991.0, "a ratio of 991", reading)
        assert matched is (reading[0] != "GLUED_FREE"), reading[0]


def test_the_glued_free_reading_is_degenerate_and_is_reported_as_such(document):
    """The declared normalisation welds a number to the word before it."""

    assert not census.number_matches(
        991.0, "a ratio of 991", ("GLUED_FREE", "GLUED", False)
    )
    assert census.number_matches(991.0, "991", ("GLUED_FREE", "GLUED", False))


def test_candidate_c_reads_the_five_numeric_slots_only(document):
    rows = census.number_in_text(document, census.CITED, census.NUMBER_READINGS[0])
    assert {row.slot for row in rows} <= census.NAMED_NUMERIC_SLOTS


def test_candidate_d_and_e_read_their_declared_slots_only(document):
    unit = census.unit_in_source(document, census.CITED, census.GLUED)
    formula = census.formula_in_source(document, census.CITED, census.GLUED)
    assert {row.slot for row in unit} <= {"unit"}
    assert {row.slot for row in formula} <= {
        "analyte",
        "denominator_kind",
        "numerator_kind",
    }


def test_the_derived_scope_is_never_narrower_than_the_cited_scope(document):
    for reading in census.NUMBER_READINGS:
        cited = {
            (r.record_id, r.slot)
            for r in census.number_in_text(document, census.CITED, reading)
        }
        derived = {
            (r.record_id, r.slot)
            for r in census.number_in_text(document, census.DERIVED, reading)
        }
        assert derived <= cited


# ---------------------------------------------------------------------------
# The public record
# ---------------------------------------------------------------------------


def test_outcomes_json_carries_no_value_and_no_text():
    rows = json.loads((HERE / "outcomes.json").read_bytes())["refusals"]
    forbidden = {"value", "text", "sentence", "cited_text", "statement"}
    for row in rows:
        assert not forbidden & set(row), row


def test_every_refusal_carries_a_class():
    rows = json.loads((HERE / "outcomes.json").read_bytes())["refusals"]
    assert rows
    for row in rows:
        assert row["class"] in {"RULE_DEFECT", "GRAPH_DEFECT", "UNDECIDED"}


def test_the_classification_table_leaves_nothing_undecided():
    """A refusal the table does not reach must surface, not default quietly."""

    rows = json.loads((HERE / "outcomes.json").read_bytes())["refusals"]
    assert [row for row in rows if row["class"] == "UNDECIDED"] == []


def test_the_counts_results_md_reports_are_the_counts_outcomes_json_holds():
    rows = json.loads((HERE / "outcomes.json").read_bytes())["refusals"]
    counted = Counter((row["candidate"], row["reading"], row["scope"]) for row in rows)
    assert counted[("NO_CONFLICTING_QUANTITY", None, None)] == 1
    assert counted[("NUMBER_IN_CITED_TEXT", "UNGLUED_FREE", "CITED")] == 1
    assert counted[("NUMBER_IN_CITED_TEXT", "UNGLUED_FREE", "DERIVED")] == 1
    assert counted[("NUMBER_IN_CITED_TEXT", "GLUED_ATTACHED", "CITED")] == 1
    assert counted[("NUMBER_IN_CITED_TEXT", "GLUED_FREE", "CITED")] == 51
    assert counted[("UNIT_IN_SOURCE", "GLUED", "CITED")] == 1
    assert counted[("FORMULA_IN_SOURCE", "GLUED", "CITED")] == 0
    assert counted[("FORMULA_IN_SOURCE", "UNGLUED", "CITED")] == 8
    assert [row for row in rows if row["population"] != "run-23"] == []


def test_every_private_row_carries_one_line_of_reason():
    private = census.PRIVATE / "run-23-detail.json"
    rows = json.loads(private.read_bytes())
    assert rows
    for row in rows:
        assert row["reason"].strip()
        assert row["class"] != "UNDECIDED"


def test_no_public_file_shares_a_sixty_character_run_with_the_reading():
    reading = (RUN_23 / "producer/inputs/selected-reading.json").read_bytes()
    folded = re.sub(r"\s+", " ", reading.decode("utf-8")).casefold()
    runs = {folded[index : index + 60] for index in range(len(folded) - 59)}
    for path in sorted(HERE.glob("*")):
        if path.is_dir() or path.suffix == ".pyc":
            continue
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).casefold()
        shared = [
            text[index : index + 60]
            for index in range(len(text) - 59)
            if text[index : index + 60] in runs
        ]
        assert not shared, (path.name, shared[:1])
