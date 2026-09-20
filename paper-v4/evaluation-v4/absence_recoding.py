"""Derive the cause of every non-reach absence the four validated records carry.

The review protocol's five absence codes have no word for plain omission, so
`NOT_MODELLED` carries two different facts at once: "the accepted contract has
no place for this" and "the contract has a place and this record left it
unset". `design/PAPER_EVALUATION_V32_PROPOSAL.md` names the split and its
evidence section of 2026-09-12 fixes it at four cases, each decidable from
identified artifacts:

  NO_TYPE_OR_SLOT            the accepted contract declares no type or slot
                             that could carry the element
  SLOT_WITHOUT_ENTITY        a slot exists and the graph holds no entity for
                             the referent
  SLOT_ENTITY_NAME_MISMATCH  a slot exists, an entity for the referent exists,
                             the slot is unset, and neither the entity's name
                             nor a tag occurs as a word in the sentence that
                             formalizes the record
  HELD_AS_DIGEST             the element survives only inside a statement the
                             graph holds as a locator and a digest

This file writes a derived artifact and never a review record. Under the
protocol's own `evidence_rule`, `ONLY_A_HUMAN_RATIFIED_RECORD_IS_PAPER_EVIDENCE`
(`review-protocol-v3.json`), a derived file is not review evidence: it is a
recoding of the records' own rationales against their cells' contracts, gaps,
exports and captures. Every frozen record is read and none is written.

Where the four cases do not decide an entry the entry says so, names what is
missing, and the recorded code stands. That is not a gap in the artifacts: an
element that is a whole record or a whole relation is not a slot value, and the
proposal's own table routes it to the sixth reviewer-facing code
(`NOT_CAPTURED`), which is a judgement this file does not make.

Two facts are the reviewer's and are marked as such wherever they are used: the
referent of case (b), which only a reader of the source can name, and the
holder record behind a semantic, which is read here from the *same question's*
other coverage entries rather than from prose, so that the pointer is checkable.

Run it:

    .venv/bin/python paper-v4/evaluation-v4/absence_recoding.py --write

Without ``--write`` it prints the summary and writes nothing.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUT = HERE / "absence-recoding-2026-09-12.json"
PROTOCOL = HERE / "review-protocol-v3.json"

SCHEMA = "malleus.paper-v4.absence-recoding/v1"
STATUS = "DERIVED_ARTIFACT_NOT_REVIEW_EVIDENCE"

# The four derived cases, plus the token an entry carries when they do not
# decide it. UNDECIDED is not a fifth cause; it is the statement that this
# derivation produced none.
CASES = {
    "NO_TYPE_OR_SLOT": (
        "the accepted contract declares no type or slot that could carry the"
        " element, and the capture declared a TYPE_ABSENT gap saying so"
    ),
    "SLOT_WITHOUT_ENTITY": (
        "a slot exists on the record's own type and the graph holds no entity"
        " for the referent the question asks about"
    ),
    "SLOT_ENTITY_NAME_MISMATCH": (
        "a slot exists, an entity for the referent exists, the record leaves"
        " the slot unset, and no form of the entity occurs as a word in any"
        " statement that formalizes the record, so the compiler would refuse"
        " the subject"
    ),
    "HELD_AS_DIGEST": (
        "WITHHELD_STATEMENT as recorded: the element survives only inside a"
        " retained statement the graph binds by locator and digest"
    ),
    "UNDECIDED": (
        "the four cases do not decide this entry; the recorded code stands and"
        " the entry names what is missing"
    ),
}

# Only the non-reach absences of a positive question are in scope. The control
# questions' NOT_IN_SOURCE entries are outside the positive elements, and
# UNREACHED_RECORD and LOCATOR_NOT_RESOLVABLE are reach defects with their own
# tokens.
IN_SCOPE_REASONS = ("NOT_MODELLED", "WITHHELD_STATEMENT")


class RecodingRefusal(ValueError):
    """The recoding cannot be derived from what is on disk."""


def _module(name: str):
    spec = importlib.util.spec_from_file_location(
        f"paper_v4_evaluation_v4_{name}", HERE / f"{name}.py"
    )
    if spec is None or spec.loader is None:  # pragma: no cover - import plumbing
        raise RecodingRefusal(f"cannot load {name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


review = _module("review")


def _occurs_as_word_rule():
    """Bind Core's own subject-name check rather than restating it here.

    `src/malleus/_contract_pipeline/document.py:277` is the rule the compiler
    applies: "The form's non-whitespace characters occur in the statement in
    order, with any whitespace between them, case-folded on both sides, and the
    character before the first and the character after the last are not
    letters." A copy of that regex here could drift from the compiler, and the
    claim case (c) makes is precisely that the compiler would have refused the
    subject, so the check must be the compiler's own.
    """

    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    from malleus._contract_pipeline import document

    return document._occurs_as_word


_occurs_as_word = _occurs_as_word_rule()
SUBJECT_NAME_RULE = (
    "malleus._contract_pipeline.document._occurs_as_word"
    " (src/malleus/_contract_pipeline/document.py:277)"
)

CONTRACT_FACTS = "https://malleus.dev/contract-facts/"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


# --------------------------------------------------------------------------
# The cells: which record, which question file, which frozen artifacts
# --------------------------------------------------------------------------

# Each cell's question file is the one its own frozen review input manifest
# binds by digest, not the newest: run-22 and run-23 ran on v3, run-24 and
# run-25 on v3.1.
CELLS: dict[str, dict[str, str]] = {
    # run-22's record is the v4.13 rebind's, which is the one the paper reports
    # for that cell. The rebind re-queried the same admitted ledger, so the
    # private producer artifacts are the v4.12 cell's, unchanged.
    "run-22": {
        "record": "paper-v4/evaluation-v4/run-22-v413/review-record.preliminary.md",
        "manifest": "paper-v4/evaluation-v4/run-22-v413/review-input-manifest.json",
        "questions": "paper-v4/experiment-v4/competency-questions-v3.json",
        "contract": "paper-v4/experiment-v4/run-22/ontology-run/validated-contract.json",
        "private": "private/paper-v4-v4-run-22",
    },
    "run-23": {
        "record": "paper-v4/evaluation-v4/run-23/review-record.preliminary.md",
        "manifest": "paper-v4/evaluation-v4/run-23/review-input-manifest.json",
        "questions": "paper-v4/experiment-v4/competency-questions-v3.json",
        "contract": "paper-v4/experiment-v4/run-23/ontology-run/validated-contract.json",
        "private": "private/paper-v4-v4-run-23",
    },
    "run-24": {
        "record": "paper-v4/evaluation-v4/run-24/review-record.preliminary.md",
        "manifest": "paper-v4/evaluation-v4/run-24/review-input-manifest.json",
        "questions": "paper-v4/experiment-v4/competency-questions-v3.1.json",
        "contract": "paper-v4/experiment-v4/run-24/ontology-run/validated-contract.json",
        "private": "private/paper-v4-v4-run-24",
    },
    # run-25 ran on run-23's accepted ontology. Its own compiled contract is
    # bound here and the digests are asserted equal, so the reader need not
    # take the shared ontology on trust.
    "run-25": {
        "record": "paper-v4/evaluation-v4/run-25/review-record.preliminary.md",
        "manifest": "paper-v4/evaluation-v4/run-25/review-input-manifest.json",
        "questions": "paper-v4/experiment-v4/competency-questions-v3.1.json",
        "contract": "paper-v4/experiment-v4/run-25/ontology-run/validated-contract.json",
        "contract_equals": "run-23",
        "private": "private/paper-v4-v4-run-25",
    },
}


# --------------------------------------------------------------------------
# The probes
#
# One entry per NOT_MODELLED absence in scope. A probe is not a derivation: it
# names the contract symbol, the holder record and the referent the derivation
# then checks against the artifacts. Every field is quoted from the record's own
# note or read from the same question's other coverage entries, and `from_note`
# carries the fragment it was read from so the reader can check the reading.
#
# `holders` names sibling semantics of the same question. The row those
# semantics cover is a witness the query result returned and the record judged
# SUPPORTED, so the holder record is an identity the record itself carries, not
# a name taken from prose.
#
# WITHHELD_STATEMENT entries carry no probe: case (d) is the recorded code.
# --------------------------------------------------------------------------

PROBES: dict[tuple[str, str, str], dict[str, Any]] = {
    # ---- run-22 -----------------------------------------------------------
    ("run-22", "CQ-T1-02", "deployment_event"): {
        "undecided": (
            "The element is a whole event record, not a slot value. The"
            " contract declares the class Event, so case (a) does not hold,"
            " and cases (b) and (c) are about a slot whose referent is an"
            " entity. The gaps the capture declares on the cited blocks are"
            " INTERVAL_NOT_EXPRESSIBLE, a refusal by the slot's range, which"
            " is not one of the four cases."
        ),
        "cite_class": "Event",
        "from_note": (
            "the capture's own gap on the Methods block records that the"
            " experiment's dates are not carried because the accepted slots"
            " are ranged on datetime"
        ),
    },
    ("run-22", "CQ-T1-03", "acceptance_event"): {
        "type_absent_gap": "assertion:026",
        "from_note": (
            "the accepted ontology declares no slot for the date a journal"
            " accepted a manuscript"
        ),
    },
    ("run-22", "CQ-T1-03", "calendar_date"): {
        "type_absent_gap": "assertion:026",
        "from_note": "The same gap removes the date itself",
    },
    ("run-22", "CQ-T1-04", "persistent_identifier"): {
        "undecided": (
            "The declared gap on the cited block is"
            " REQUIRED_FIELD_ABSENT_IN_SOURCE, which says the reading stops"
            " short of the value, not that the contract has no place for it."
            " That is a capture-boundary defect and none of the four cases."
        ),
        "from_note": (
            "the DOI runs across the data-availability block and the next one,"
            " and the continuation block was declared unassertable"
        ),
    },
    ("run-22", "CQ-T4-03", "claim_subject"): {
        "slot": "subject",
        "holders": ["stated_assumption"],
        "referent": {"kind": "SIBLING_SEMANTIC", "semantic": "qualified_claim"},
        "from_note": (
            "The caveat record's subject slot is empty ... no field on it or on"
            " the qualified claim carries what the caveat is about."
        ),
    },
    ("run-22", "CQ-T5-01", "evidence_relation"): {
        "undecided": (
            "The element is a relation, not a slot value. The contract declares"
            " the class Evidence and the ResearchRelationType enum carries"
            " SUPPORTS, so a type exists and case (a) does not hold; cases (b)"
            " and (c) are slot-scoped."
        ),
        "cite_class": "Evidence",
        "from_note": (
            "the graph declares no relation between an observation and the"
            " claim it supports"
        ),
    },
    ("run-22", "CQ-T5-05", "evidence_relation"): {
        "undecided": (
            "The element is a relation, not a slot value. The contract declares"
            " the class Evidence and the ResearchRelationType enum carries"
            " SUPPORTS, so a type exists and case (a) does not hold; cases (b)"
            " and (c) are slot-scoped."
        ),
        "cite_class": "Evidence",
        "from_note": "no relation type ties an observation to the claim it bears on",
    },
    # ---- run-23 -----------------------------------------------------------
    ("run-23", "CQ-T1-03", "acceptance_event"): {
        "type_absent_gap": "assertion:027",
        "from_note": (
            "that assertion formalizes no record, so no acceptance event exists"
            " in the graph"
        ),
    },
    ("run-23", "CQ-T1-03", "calendar_date"): {
        "type_absent_gap": "assertion:027",
        "from_note": (
            "The accepted date is in the same retained assertion and no record"
            " or field carries it."
        ),
    },
    ("run-23", "CQ-T3-04", "quantity_subject"): {
        "slot": "subject",
        "holders": ["bounded_quantity"],
        "referent": {"kind": "SIBLING_SEMANTIC", "semantic": "event_set"},
        "from_note": (
            "The observation type carries a subject slot and this record leaves"
            " it unset, so no row says what the uncertainty is an uncertainty"
            " of"
        ),
    },
    ("run-23", "CQ-T3-05", "quantity_subject"): {
        "slot": "subject",
        "holders": ["bounded_quantity", "temperature_unit"],
        "referent": {
            "kind": "REVIEWER_STATES_NO_RECORD",
            "phrase": "the melt these quantities describe",
            "scan_words": ["melt", "melts"],
        },
        "from_note": (
            "Both observations leave the subject slot unset and the melt they"
            " describe has no record of its own in the graph."
        ),
    },
    ("run-23", "CQ-T4-02", "claim_subject"): {
        "undecided": (
            "The note names no referent: it says no row binds the declined"
            " mechanism to a feature without naming the feature, and no sibling"
            " semantic of this question covers one. Case (b) needs the referent"
            " and case (c) needs the entity, so neither is decidable and the"
            " slot's presence alone separates nothing."
        ),
        "cite_slot": {"slot": "subject", "holders": ["candidate_mechanism"]},
        "from_note": (
            "The candidate-explanation record carries no subject and no other"
            " row binds this declined mechanism to a feature."
        ),
    },
    ("run-23", "CQ-T4-03", "claim_subject"): {
        "slot": "subject",
        "holders": ["stated_assumption"],
        "referent": {"kind": "SIBLING_SEMANTIC", "semantic": "qualified_claim"},
        "from_note": (
            "The caveat record leaves the subject slot unset and no other row"
            " binds it to a subject."
        ),
    },
    ("run-23", "CQ-T5-01", "evidence_relation"): {
        "undecided": (
            "The element is a relation, not a slot value. The contract declares"
            " the class Evidence and the ResearchRelationType enum carries"
            " SUPPORTS, so a type exists and case (a) does not hold; cases (b)"
            " and (c) are slot-scoped."
        ),
        "cite_class": "Evidence",
        "from_note": (
            "No evidence record and no relation joining an observation to a"
            " claim exists in the graph, although the question's type set"
            " admits both."
        ),
    },
    ("run-23", "CQ-T5-05", "evidence_relation"): {
        "undecided": (
            "The element is a relation, not a slot value. The contract declares"
            " the class Evidence and the ResearchRelationType enum carries"
            " SUPPORTS, so a type exists and case (a) does not hold; cases (b)"
            " and (c) are slot-scoped."
        ),
        "cite_class": "Evidence",
        "from_note": (
            "No evidence record and no relation between an observation and a"
            " claim exists in the graph."
        ),
    },
    # ---- run-24 -----------------------------------------------------------
    ("run-24", "CQ-T1-03", "acceptance_event"): {
        "type_absent_gap": "a:p1b6:dates",
        "from_note": (
            "the capture records against that block that the work type declares"
            " no slot for a received or accepted date"
        ),
    },
    ("run-24", "CQ-T1-03", "calendar_date"): {
        "type_absent_gap": "a:p1b6:dates",
        "from_note": "The date sits in the same unmodelled statement",
    },
    ("run-24", "CQ-T1-04", "persistent_identifier"): {
        "undecided": (
            "The declared gap on the cited block is"
            " REQUIRED_FIELD_ABSENT_IN_SOURCE, which says the reading stops"
            " short of the value, not that the contract has no place for it."
            " That is a capture-boundary defect and none of the four cases."
        ),
        "from_note": (
            "the digits that complete it fall in the following block, which the"
            " capture declared nothing-assertable"
        ),
    },
    ("run-24", "CQ-T3-04", "quantity_subject"): {
        "slot": "subject",
        "holders": ["bounded_quantity"],
        "referent": {"kind": "SIBLING_SEMANTIC", "semantic": "event_set"},
        "from_note": (
            "The uncertainty record's subject slot is absent ... no field on it"
            " says which body of events the average describes."
        ),
    },
    ("run-24", "CQ-T3-05", "quantity_subject"): {
        "slot": "subject",
        "holders": ["bounded_quantity", "temperature_unit"],
        "referent": {"kind": "EXPORTED_TYPE", "type": "MagmaticMelt"},
        "from_note": (
            "their subject slots are absent, so no row ties the pressure or the"
            " temperature to the melt they describe"
        ),
    },
    # ---- run-25 -----------------------------------------------------------
    ("run-25", "CQ-T4-02", "claim_subject"): {
        "undecided": (
            "The note names no referent: it compares this claim with the"
            " preferred explanation claim without saying what the subject would"
            " have been, and no sibling semantic of this question covers one."
            " Case (b) needs the referent and case (c) needs the entity."
        ),
        "cite_slot": {"slot": "subject", "holders": ["candidate_mechanism"]},
        "from_note": (
            "this explanation claim carries no subject reference, where the"
            " preferred explanation claim does"
        ),
    },
    ("run-25", "CQ-T4-03", "caveat_disposition"): {
        "undecided": (
            "The slot the element would take is hypothesis_disposition, whose"
            " range is the HypothesisDisposition enum. Cases (b) and (c) are"
            " about an entity referent and cannot arise on an enum-ranged slot,"
            " and the contract declares the slot on Claim, so case (a) does not"
            " hold either."
        ),
        "cite_slot": {"slot": "hypothesis_disposition", "holders": ["stated_assumption"]},
        "from_note": (
            "no returned row carries a typed disposition for a caveat; the only"
            " disposition field in the result is the hypothesis disposition of"
            " the explanation claims"
        ),
    },
    ("run-25", "CQ-T4-05", "hypothesised_disposition"): {
        "undecided": (
            "The slot the element would take is hypothesis_disposition, whose"
            " range is the HypothesisDisposition enum. Cases (b) and (c) are"
            " about an entity referent and cannot arise on an enum-ranged slot,"
            " and the contract declares the slot on Claim, so case (a) does not"
            " hold either."
        ),
        "cite_slot": {"slot": "hypothesis_disposition", "holders": ["hedged_claim"]},
        "from_note": (
            "this claim carries no disposition field; the dispositions in the"
            " result belong to the four explanation claims"
        ),
    },
    ("run-25", "CQ-T5-01", "evidence_relation"): {
        "undecided": (
            "The element is a relation, not a slot value. The contract declares"
            " the class Evidence and the ResearchRelationType enum carries"
            " SUPPORTS, so a type exists and case (a) does not hold; cases (b)"
            " and (c) are slot-scoped."
        ),
        "cite_class": "Evidence",
        "from_note": (
            "no returned relation ties an observation to the claim it supports,"
            " and no such relation type appears in the result"
        ),
    },
    ("run-25", "CQ-T5-05", "evidence_relation"): {
        "undecided": (
            "The element is a relation, not a slot value. The contract declares"
            " the class Evidence and the ResearchRelationType enum carries"
            " SUPPORTS, so a type exists and case (a) does not hold; cases (b)"
            " and (c) are slot-scoped."
        ),
        "cite_class": "Evidence",
        "from_note": (
            "no returned relation ties an observation to the explanation it"
            " argues against"
        ),
    },
}


# --------------------------------------------------------------------------
# Reading the frozen artifacts
# --------------------------------------------------------------------------


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


class Artifact:
    """One file read once, carrying the path and digest every pointer needs."""

    def __init__(self, relative: str) -> None:
        self.path = relative
        absolute = ROOT / relative
        if not absolute.is_file():
            raise RecodingRefusal(f"a bound input is not on disk: {relative}")
        self.bytes = absolute.read_bytes()
        self.sha256 = _digest(self.bytes)

    @property
    def json(self) -> Any:
        return json.loads(self.bytes)

    def pointer(self, **fields: Any) -> dict[str, Any]:
        return {"file": self.path, "sha256": self.sha256, **fields}


class Cell:
    """Every frozen artifact one cell's absences are derived against."""

    def __init__(self, name: str, paths: dict[str, str]) -> None:
        self.name = name
        self.record = Artifact(paths["record"])
        self.manifest = Artifact(paths["manifest"])
        self.questions = Artifact(paths["questions"])
        self.contract = Artifact(paths["contract"])
        private = paths["private"]
        self.exports = Artifact(f"{private}/results/export-records.json")
        self.gaps = Artifact(f"{private}/results/gaps.json")
        self.capture = Artifact(f"{private}/producer/work/document-population.json")
        self.contract_equals = paths.get("contract_equals")

        # The question file is the one this cell's own frozen manifest binds by
        # digest. run-22 and run-23 ran on v3 and run-24 and run-25 on v3.1, and
        # reading the newer file against the older cell would silently change
        # which semantics an absence is counted against.
        bound = self.manifest.json["fixed_identities"]["competency_questions_sha256"]
        if bound != self.questions.sha256:
            raise RecodingRefusal(
                f"{name} binds a competency question file this recoding does not"
                f" read: manifest {bound}, read {self.questions.sha256}"
            )

        self.review = review._markdown_record(self.record.bytes)
        self.question_file = review._question_file(self.questions.bytes)
        self.controls = {
            item["id"] for item in self.question_file if item.get("expected_outcome")
        }
        self.entities = {item["id"]: item for item in self.exports.json["entities"]}
        capture = self.capture.json["capture"]
        self.assertions = {item["id"]: item for item in capture["assertions"]}
        self.gap_list = self.gaps.json["gaps"]
        self.slot_uses, self.classes, self.enums = _contract_symbols(self.contract.json)

    def statements_formalizing(self, record_id: str) -> list[dict[str, Any]]:
        """Every retained assertion whose formalization names this record."""

        return [
            item
            for item in self.assertions.values()
            if any(
                entry.get("record_id") == record_id
                for entry in item.get("formalized_by", [])
            )
        ]

    def forms(self, record_id: str) -> list[str]:
        """A subject's forms: its name first and then its tags, Core's order."""

        properties = self.entities[record_id].get("properties", {})
        candidates = [properties.get("name")] + list(properties.get("tags") or [])
        return [item for item in candidates if isinstance(item, str) and item]


def _contract_symbols(
    contract: dict[str, Any],
) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[str, str], dict[str, list[str]]]:
    """Index the compiled contract's facts by the shapes a probe asks about.

    The contract is a triple set, so a SlotUse is a node with `onClass` and
    `usesSlot` rather than a row. `review-protocol-v3.json` never reads it; this
    derivation does, which is why the output binds `validated_contract_sha256`
    beside the manifests' `accepted_ontology_sha256`, the digest of the LinkML
    source.
    """

    grouped: dict[str, dict[str, list[Any]]] = {}
    for fact in contract["facts"]:
        grouped.setdefault(fact["subject"], {}).setdefault(fact["predicate"], []).append(
            fact["object"]
        )
    slot_uses: dict[tuple[str, str], dict[str, Any]] = {}
    classes: dict[str, str] = {}
    enums: dict[str, list[str]] = {}
    for subject, predicates in grouped.items():
        types = predicates.get(RDF_TYPE, [])
        if f"{CONTRACT_FACTS}SlotUse" in types:
            on_class = predicates[f"{CONTRACT_FACTS}onClass"][0]
            uses_slot = predicates[f"{CONTRACT_FACTS}usesSlot"][0]
            slot_uses[(on_class.rsplit("/", 1)[-1], uses_slot.rsplit("/", 1)[-1])] = {
                "node": subject,
                "on_class": on_class,
                "uses_slot": uses_slot,
                "value_range": predicates[f"{CONTRACT_FACTS}valueRange"][0],
                "required": predicates[f"{CONTRACT_FACTS}required"][0],
            }
        if f"{CONTRACT_FACTS}Class" in types:
            classes[subject.rsplit("/", 1)[-1]] = subject
        if f"{CONTRACT_FACTS}Enum" in types:
            enums[subject.rsplit("/", 1)[-1]] = sorted(
                predicates.get(f"{CONTRACT_FACTS}enumValue", [])
            )
    return slot_uses, classes, enums


# --------------------------------------------------------------------------
# The derivation
# --------------------------------------------------------------------------


def _coverage_in_scope(cell: Cell) -> list[dict[str, Any]]:
    """Every non-reach absence of a positive question, in record order."""

    found: list[dict[str, Any]] = []
    for question in cell.review["questions"]:
        question_id = question["question_id"]
        if question_id in cell.controls:
            continue
        rows = [item["witness_key"] for item in question["rows"]]
        for index, entry in enumerate(question["coverage"]):
            if entry["row_index"] is not None:
                continue
            if entry["absent_reason"] not in IN_SCOPE_REASONS:
                continue
            found.append(
                {
                    "question": question,
                    "question_id": question_id,
                    "rows": rows,
                    "coverage_index": index,
                    "entry": entry,
                }
            )
    return found


def _covered_witness(item: dict[str, Any], semantic: str) -> str | None:
    """The witness the same question's coverage names for a sibling semantic."""

    for entry in item["question"]["coverage"]:
        if entry.get("semantic") != semantic:
            continue
        if entry["row_index"] is None:
            return None
        return item["rows"][entry["row_index"]]
    return None


def _recorded_pointer(cell: Cell, item: dict[str, Any]) -> dict[str, Any]:
    return cell.record.pointer(
        kind="RECORDED_COVERAGE_ENTRY",
        question_id=item["question_id"],
        coverage_index=item["coverage_index"],
        semantic=item["entry"]["semantic"],
        recorded_reason=item["entry"]["absent_reason"],
        quote=item["entry"]["note"],
    )


def _gaps_on(cell: Cell, blocks: list[str]) -> list[dict[str, Any]]:
    found = []
    for gap in cell.gap_list:
        assertion = cell.assertions.get(gap["locator"])
        if assertion is None or assertion["block"] not in blocks:
            continue
        found.append(gap)
    return found


def _held_as_digest(cell: Cell, item: dict[str, Any]) -> dict[str, Any]:
    """Case (d): the recorded code, with the digest-bound records it names.

    The derivation is the identity, so the corroboration is what the entry
    carries beyond the record's own words: the blocks the question cites, and
    every witness of that question whose exported record binds a statement by
    `assertion_locator` and `statement_sha256` on one of those blocks. That is
    the shape "held as a locator and a digest" means.
    """

    evidence = [_recorded_pointer(cell, item)]
    blocks = list(item["question"]["source_locators"])
    bound: list[dict[str, Any]] = []
    for witness in dict.fromkeys(item["rows"]):
        record = cell.entities.get(witness)
        if record is None:
            continue
        properties = record.get("properties", {})
        locator = properties.get("assertion_locator")
        digest = properties.get("statement_sha256")
        if not locator or not digest:
            continue
        assertion = cell.assertions.get(locator)
        if assertion is None or assertion["block"] not in blocks:
            continue
        bound.append(
            {
                "record_id": witness,
                "type": record["type"],
                "assertion_locator": locator,
                "block_id": assertion["block"],
                "statement_sha256": digest,
            }
        )
    evidence.append(
        cell.record.pointer(
            kind="QUESTION_SOURCE_LOCATORS",
            question_id=item["question_id"],
            block_ids=blocks,
            fact="the blocks the record cites for this question",
        )
    )
    if not bound:
        return {
            "derived_case": "UNDECIDED",
            "judgement": "MECHANICAL",
            "undecided_reason": (
                "No witness of this question carries an assertion locator and a"
                " statement digest on a block the question cites, so the"
                " recorded WITHHELD_STATEMENT has nothing here to bind it to."
            ),
            "evidence": evidence,
        }
    evidence.append(
        cell.exports.pointer(
            kind="DIGEST_BOUND_RECORDS",
            records=bound,
            fact=(
                "records the question returns that bind a cited block's"
                " statement by locator and digest"
            ),
        )
    )
    return {
        "derived_case": "HELD_AS_DIGEST",
        "judgement": "RECORDED_CODE_CARRIED_FORWARD",
        "undecided_reason": None,
        "evidence": evidence,
    }


def _no_type_or_slot(
    cell: Cell, item: dict[str, Any], probe: dict[str, Any]
) -> dict[str, Any]:
    """Case (a): a TYPE_ABSENT gap the producer declared, on a cited block."""

    locator = probe["type_absent_gap"]
    gap = next((item_ for item_ in cell.gap_list if item_["locator"] == locator), None)
    if gap is None:
        raise RecodingRefusal(f"{cell.name}: no gap is declared at {locator}")
    if gap["kind"] != "TYPE_ABSENT":
        raise RecodingRefusal(
            f"{cell.name}: the gap at {locator} is {gap['kind']}, not TYPE_ABSENT"
        )
    assertion = cell.assertions.get(locator)
    if assertion is None:
        raise RecodingRefusal(f"{cell.name}: no retained assertion at {locator}")
    blocks = list(item["question"]["source_locators"])
    if assertion["block"] not in blocks:
        raise RecodingRefusal(
            f"{cell.name}: the gap at {locator} sits on {assertion['block']},"
            f" which this question does not cite"
        )
    return {
        "derived_case": "NO_TYPE_OR_SLOT",
        "judgement": "MECHANICAL",
        "undecided_reason": None,
        "evidence": [
            _recorded_pointer(cell, item),
            cell.gaps.pointer(
                kind="DECLARED_GAP",
                gap_kind=gap["kind"],
                locator=locator,
                block_id=assertion["block"],
                quote=gap["statement"],
                fact="the capture's own declaration that no type or slot carries it",
            ),
            cell.capture.pointer(
                kind="CAPTURE_ASSERTION",
                assertion_locator=locator,
                block_id=assertion["block"],
                formalizes=len(assertion.get("formalized_by", [])),
                fact="the retained assertion the gap is declared at",
            ),
            cell.contract.pointer(
                kind="CONTRACT_IDENTITY",
                fact="the accepted contract the gap is a statement about",
            ),
        ],
    }


def _resolve_holders(
    cell: Cell, item: dict[str, Any], probe: dict[str, Any]
) -> list[str]:
    holders: list[str] = []
    for semantic in probe["holders"]:
        witness = _covered_witness(item, semantic)
        if witness is None:
            raise RecodingRefusal(
                f"{cell.name}/{item['question_id']}: the sibling semantic"
                f" {semantic!r} names no row, so the holder record is not fixed"
            )
        if witness not in cell.entities:
            raise RecodingRefusal(
                f"{cell.name}: {witness} is not an exported entity record"
            )
        if witness not in holders:
            holders.append(witness)
    return holders


def _slot_case(
    cell: Cell, item: dict[str, Any], probe: dict[str, Any]
) -> dict[str, Any]:
    """Cases (a), (b) and (c) for a probe that names a slot and its holders."""

    slot = probe["slot"]
    holders = _resolve_holders(cell, item, probe)
    evidence = [_recorded_pointer(cell, item)]

    uses: list[dict[str, Any]] = []
    for holder in holders:
        record = cell.entities[holder]
        key = (record["type"], slot)
        use = cell.slot_uses.get(key)
        if use is None:
            return {
                "derived_case": "NO_TYPE_OR_SLOT",
                "judgement": "MECHANICAL",
                "undecided_reason": None,
                "evidence": evidence
                + [
                    cell.contract.pointer(
                        kind="CONTRACT_SLOT_USE_ABSENT",
                        on_class=record["type"],
                        uses_slot=slot,
                        fact=(
                            f"the contract declares no use of {slot} on"
                            f" {record['type']}, the type of {holder}"
                        ),
                    )
                ],
            }
        if record.get("properties", {}).get(slot) is not None:
            raise RecodingRefusal(
                f"{cell.name}: {holder} carries {slot}, so the absence the"
                " record reports is not this record's unset slot"
            )
        uses.append({"holder": holder, "type": record["type"], "use": use})

    for entry in uses:
        use = entry["use"]
        evidence.append(
            cell.contract.pointer(
                kind="CONTRACT_SLOT_USE",
                node=use["node"],
                on_class=use["on_class"],
                uses_slot=use["uses_slot"],
                value_range=use["value_range"],
                required=use["required"],
                fact=f"the contract declares {slot} on {entry['type']}",
            )
        )
        evidence.append(
            cell.exports.pointer(
                kind="EXPORTED_RECORD_SLOT_UNSET",
                record_id=entry["holder"],
                type=entry["type"],
                slot=slot,
                fact=f"{entry['holder']} leaves {slot} unset",
            )
        )

    referent = probe["referent"]
    candidates, judgement, referent_evidence = _referent_candidates(cell, item, referent)
    evidence.extend(referent_evidence)

    if not candidates:
        return {
            "derived_case": "SLOT_WITHOUT_ENTITY",
            "judgement": judgement,
            "undecided_reason": None,
            "evidence": evidence,
        }

    matched: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    for entry in uses:
        statements = cell.statements_formalizing(entry["holder"])
        if not statements:
            raise RecodingRefusal(
                f"{cell.name}: no retained assertion formalizes {entry['holder']}"
            )
        for assertion in statements:
            for candidate in candidates:
                forms = cell.forms(candidate)
                hits = [form for form in forms if _occurs_as_word(form, assertion["statement"])]
                checks.append(
                    {
                        "holder": entry["holder"],
                        "assertion_locator": assertion["id"],
                        "block_id": assertion["block"],
                        "referent": candidate,
                        "forms": forms,
                        "occurs_as_word": hits,
                    }
                )
                if hits:
                    matched.append(checks[-1])

    evidence.append(
        cell.capture.pointer(
            kind="SUBJECT_NAME_RULE",
            rule=SUBJECT_NAME_RULE,
            checks=checks,
            fact=(
                "the compiler's own subject check, run over every form of every"
                " candidate referent against every statement formalizing the"
                " holder"
            ),
        )
    )
    if matched:
        return {
            "derived_case": "UNDECIDED",
            "judgement": "MECHANICAL",
            "undecided_reason": (
                "A form of the referent does occur as a word in a statement"
                " formalizing the record, so the compiler would have accepted"
                " the subject and case (c) does not explain the empty slot."
            ),
            "evidence": evidence,
        }
    return {
        "derived_case": "SLOT_ENTITY_NAME_MISMATCH",
        "judgement": judgement,
        "undecided_reason": None,
        "evidence": evidence,
    }


def _referent_candidates(
    cell: Cell, item: dict[str, Any], referent: dict[str, Any]
) -> tuple[list[str], str, list[dict[str, Any]]]:
    """The entities the slot could have taken, and how they were fixed."""

    kind = referent["kind"]
    if kind == "SIBLING_SEMANTIC":
        witness = _covered_witness(item, referent["semantic"])
        if witness is None:
            raise RecodingRefusal(
                f"{cell.name}/{item['question_id']}: the referent semantic"
                f" {referent['semantic']!r} names no row"
            )
        if witness not in cell.entities:
            raise RecodingRefusal(f"{cell.name}: {witness} is not an exported record")
        return (
            [witness],
            "MECHANICAL",
            [
                cell.record.pointer(
                    kind="REFERENT_FROM_SIBLING_SEMANTIC",
                    question_id=item["question_id"],
                    semantic=referent["semantic"],
                    record_id=witness,
                    fact=(
                        "the same question's coverage names this row for the"
                        " referent, so the referent is an identity the record"
                        " already carries"
                    ),
                ),
                cell.exports.pointer(
                    kind="EXPORTED_RECORD",
                    record_id=witness,
                    type=cell.entities[witness]["type"],
                    forms=cell.forms(witness),
                    fact="the entity the slot could have taken",
                ),
            ],
        )
    if kind == "EXPORTED_TYPE":
        wanted = referent["type"]
        if wanted not in cell.classes:
            raise RecodingRefusal(f"{cell.name}: the contract declares no {wanted}")
        found = sorted(
            record_id
            for record_id, record in cell.entities.items()
            if record["type"] == wanted
        )
        return (
            found,
            "MECHANICAL",
            [
                cell.contract.pointer(
                    kind="CONTRACT_CLASS",
                    node=cell.classes[wanted],
                    fact=f"the contract declares the class {wanted}",
                ),
                cell.exports.pointer(
                    kind="EXPORTED_RECORDS_OF_TYPE",
                    type=wanted,
                    records=[
                        {"record_id": record_id, "forms": cell.forms(record_id)}
                        for record_id in found
                    ],
                    fact=(
                        "every entity of that type in the graph; the slot could"
                        " have taken any of them"
                    ),
                ),
            ],
        )
    if kind == "REVIEWER_STATES_NO_RECORD":
        scan = sorted(
            {
                record_id
                for record_id, record in cell.entities.items()
                for form in cell.forms(record_id)
                for word in referent["scan_words"]
                if _occurs_as_word(word, form)
            }
        )
        return (
            [],
            "THE_REVIEWER_S",
            [
                cell.record.pointer(
                    kind="REFERENT_FROM_REVIEWER_NOTE",
                    question_id=item["question_id"],
                    phrase=referent["phrase"],
                    fact=(
                        "the referent is the reviewer's: only a reader of the"
                        " source can say what these quantities are about, and"
                        " the note states the graph holds no record for it"
                    ),
                ),
                cell.exports.pointer(
                    kind="REFERENT_SCAN",
                    scan_words=referent["scan_words"],
                    records=[
                        {
                            "record_id": record_id,
                            "type": cell.entities[record_id]["type"],
                            "forms": cell.forms(record_id),
                        }
                        for record_id in scan
                    ],
                    fact=(
                        "every exported record writing one of those words as a"
                        " word in a name or a tag: the set the reviewer's"
                        " judgement excludes, carried so it can be checked"
                    ),
                ),
            ],
        )
    raise RecodingRefusal(f"unknown referent kind {kind!r}")


def _undecided(
    cell: Cell, item: dict[str, Any], probe: dict[str, Any]
) -> dict[str, Any]:
    """An entry the four cases do not decide, with the facts behind the reason."""

    evidence = [_recorded_pointer(cell, item)]
    blocks = list(item["question"]["source_locators"])
    gaps = _gaps_on(cell, blocks)
    evidence.append(
        cell.gaps.pointer(
            kind="DECLARED_GAPS_ON_CITED_BLOCKS",
            block_ids=blocks,
            gaps=[
                {
                    "kind": gap["kind"],
                    "locator": gap["locator"],
                    "block_id": cell.assertions[gap["locator"]]["block"],
                    "quote": gap["statement"],
                }
                for gap in gaps
            ],
            fact="every gap the capture declares on a block this question cites",
        )
    )
    if "cite_class" in probe:
        wanted = probe["cite_class"]
        if wanted not in cell.classes:
            raise RecodingRefusal(f"{cell.name}: the contract declares no {wanted}")
        evidence.append(
            cell.contract.pointer(
                kind="CONTRACT_CLASS",
                node=cell.classes[wanted],
                fact=f"the contract declares the class {wanted}, so case (a) fails",
            )
        )
    if "cite_slot" in probe:
        cited = probe["cite_slot"]
        holders = _resolve_holders(cell, item, cited)
        for holder in holders:
            record = cell.entities[holder]
            use = cell.slot_uses.get((record["type"], cited["slot"]))
            if use is None:
                raise RecodingRefusal(
                    f"{cell.name}: the contract declares no {cited['slot']} on"
                    f" {record['type']}, so this entry is case (a), not undecided"
                )
            evidence.append(
                cell.contract.pointer(
                    kind="CONTRACT_SLOT_USE",
                    node=use["node"],
                    on_class=use["on_class"],
                    uses_slot=use["uses_slot"],
                    value_range=use["value_range"],
                    required=use["required"],
                    fact=(
                        f"the contract declares {cited['slot']} on"
                        f" {record['type']}, the type of {holder}"
                    ),
                )
            )
    return {
        "derived_case": "UNDECIDED",
        "judgement": "MECHANICAL",
        "undecided_reason": probe["undecided"],
        "evidence": evidence,
    }


def _derive(cell: Cell, item: dict[str, Any]) -> dict[str, Any]:
    entry = item["entry"]
    key = (cell.name, item["question_id"], entry["semantic"])
    if entry["absent_reason"] == "WITHHELD_STATEMENT":
        if key in PROBES:
            raise RecodingRefusal(
                f"{key} carries a probe; case (d) is the recorded code and takes none"
            )
        derived = _held_as_digest(cell, item)
        probe: dict[str, Any] = {}
    else:
        if key not in PROBES:
            raise RecodingRefusal(f"no probe is declared for {key}")
        probe = PROBES[key]
        if "undecided" in probe:
            derived = _undecided(cell, item, probe)
        elif "type_absent_gap" in probe:
            derived = _no_type_or_slot(cell, item, probe)
        else:
            derived = _slot_case(cell, item, probe)
    result = {
        "cell": cell.name,
        "question_id": item["question_id"],
        "semantic": entry["semantic"],
        "recorded_reason": entry["absent_reason"],
        "recorded_note": entry["note"],
        "probe": {key_: value for key_, value in probe.items() if key_ != "undecided"},
        **derived,
    }
    if not result["evidence"]:
        raise RecodingRefusal(f"{key} carries no evidence pointer")
    return result


def build() -> dict[str, Any]:
    """Read the four frozen records and derive one entry per absence in scope."""

    protocol = Artifact(str(PROTOCOL.relative_to(ROOT)))
    cells = {name: Cell(name, paths) for name, paths in CELLS.items()}
    for name, paths in CELLS.items():
        twin = paths.get("contract_equals")
        if twin and cells[name].contract.sha256 != cells[twin].contract.sha256:
            raise RecodingRefusal(
                f"{name}'s contract is recorded as {twin}'s and their digests differ"
            )

    entries: list[dict[str, Any]] = []
    for name in CELLS:
        cell = cells[name]
        for item in _coverage_in_scope(cell):
            entries.append(_derive(cell, item))

    declared = set(PROBES)
    used = {
        (entry["cell"], entry["question_id"], entry["semantic"])
        for entry in entries
        if entry["recorded_reason"] == "NOT_MODELLED"
    }
    unused = sorted(declared - used)
    if unused:
        raise RecodingRefusal(f"probes declared for absences no record carries: {unused}")

    summary: dict[str, dict[str, int]] = {}
    for entry in entries:
        summary.setdefault(entry["cell"], {})
        summary[entry["cell"]][entry["derived_case"]] = (
            summary[entry["cell"]].get(entry["derived_case"], 0) + 1
        )

    return {
        "schema": SCHEMA,
        "status": STATUS,
        "generated_by": "paper-v4/evaluation-v4/absence_recoding.py",
        "derived_on": "2026-09-12",
        "is_not": (
            "This is not a review record and no validator reads it. Under"
            " review-protocol-v3.json's evidence_rule only a human-ratified"
            " record is paper evidence; this file recodes the records' own"
            " rationales against their cells' contracts, gaps, exports and"
            " captures, and re-judges nothing."
        ),
        "scope": (
            "every coverage entry of a positive question whose row_index is"
            " null and whose absent_reason is NOT_MODELLED or"
            " WITHHELD_STATEMENT, in the four validated records the paper"
            " reports"
        ),
        "cases": CASES,
        "subject_name_rule": SUBJECT_NAME_RULE,
        "inputs": {
            "review_protocol": {
                "path": protocol.path,
                "sha256": protocol.sha256,
            },
            "cells": {
                name: {
                    "record": {"path": cell.record.path, "sha256": cell.record.sha256},
                    "review_input_manifest": {
                        "path": cell.manifest.path,
                        "sha256": cell.manifest.sha256,
                    },
                    "competency_questions": {
                        "path": cell.questions.path,
                        "sha256": cell.questions.sha256,
                    },
                    "validated_contract": {
                        "path": cell.contract.path,
                        "sha256": cell.contract.sha256,
                        "same_contract_as": cell.contract_equals,
                    },
                    "export_records": {
                        "path": cell.exports.path,
                        "sha256": cell.exports.sha256,
                    },
                    "gaps": {
                        "path": cell.gaps.path,
                        "sha256": cell.gaps.sha256,
                        "declared": len(cell.gap_list),
                    },
                    "document_population": {
                        "path": cell.capture.path,
                        "sha256": cell.capture.sha256,
                    },
                }
                for name, cell in cells.items()
            },
        },
        "summary": {
            "by_cell_and_case": summary,
            "entries": len(entries),
            "undecided": sum(
                1 for entry in entries if entry["derived_case"] == "UNDECIDED"
            ),
        },
        "entries": entries,
    }


def render(document: dict[str, Any]) -> str:
    """The summary table by cell and case, and the undecided count."""

    order = [
        "NO_TYPE_OR_SLOT",
        "SLOT_WITHOUT_ENTITY",
        "SLOT_ENTITY_NAME_MISMATCH",
        "HELD_AS_DIGEST",
        "UNDECIDED",
    ]
    short = {name: name.replace("_", " ").lower() for name in order}
    width = max(len(short[name]) for name in order)
    cells = list(document["summary"]["by_cell_and_case"])
    lines = [
        "case".ljust(width) + "".join(f"{name:>9}" for name in cells) + f"{'total':>9}",
        "-" * (width + 9 * (len(cells) + 1)),
    ]
    for name in order:
        counts = [
            document["summary"]["by_cell_and_case"].get(cell, {}).get(name, 0)
            for cell in cells
        ]
        lines.append(
            short[name].ljust(width)
            + "".join(f"{count:>9}" for count in counts)
            + f"{sum(counts):>9}"
        )
    totals = [
        sum(document["summary"]["by_cell_and_case"].get(cell, {}).values())
        for cell in cells
    ]
    lines.append("-" * (width + 9 * (len(cells) + 1)))
    lines.append(
        "total".ljust(width)
        + "".join(f"{count:>9}" for count in totals)
        + f"{sum(totals):>9}"
    )
    lines.append("")
    lines.append(
        f"{document['summary']['entries']} absences recoded,"
        f" {document['summary']['undecided']} left undecided with the recorded"
        " code standing"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--write", action="store_true", help="write the derived file to disk"
    )
    arguments = parser.parse_args(argv)
    try:
        document = build()
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"absence-recoding: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    if arguments.write:
        OUTPUT.write_bytes(
            json.dumps(document, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        )
        print(f"wrote {OUTPUT.relative_to(ROOT)}  {_digest(OUTPUT.read_bytes())}")
    print(render(document))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
