"""A declared ontology gap as an open question with a recorded answer.

A population plan or a capture declares a typed gap when the ontology cannot
type what the source states. Two of the six kinds are questions the ontology
itself can answer: ``TYPE_ABSENT`` and ``RELATION_ABSENT``. This module gives
those gaps an identity, a proposal grammar, and one recorded decision each.

What is closed here:

* A gap's identity is derived from the bytes it identifies. Core digests the
  canonical JSON object ``{"gap": <the gap>, "plan_id": <the plan it was
  declared in>}``, where ``<the gap>`` is the four-field object exactly as the
  retained gaps artifact holds it. Nothing is derived from a path or a name.
* A proposal is retained evidence under ``malleus.ontology-revision-proposal/v1``
  and carries the LinkML addition its owner wrote and the identities of the gaps
  it answers. It is born a fragment: Core composes that fragment onto the
  history's retained root, compiles it, and retains the compiled target
  alongside, so a proposer needs no compiler and cannot hand Core an artifact
  Core did not derive. Core never drafts a proposal and never reads a class or
  slot name out of a gap's statement (architectural law 8).
* Retention is the check. Any door that retains proposal bytes runs this
  validation inside the fold, so a proposal that names an unknown gap, an
  already answered gap, a gap of a non-ontology kind, or that does not compose
  additively against the history's current contract is refused before the ledger
  is written.
* Acceptance is the revision and refusal closes with a reason. Both are one
  recorded ``malleus.ontology-gap-answer/v1`` act. There is no state in which a
  proposal is accepted and not applied: an ``ACCEPTED`` answer only folds when
  the revision its proposal named is recorded in the same history.

What is not here: Core decides nothing. The deciding actor is recorded, not
authenticated; authorization is the adopter's.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from hashlib import sha256
import json
from typing import Mapping

from malleus._contract_pipeline.model import canonical_json


ONTOLOGY_GAP_KINDS = ("RELATION_ABSENT", "TYPE_ABSENT")
"""The declared gap kinds an ontology revision can answer.

The other four kinds of ``malleus.compiler.POPULATION_GAP_KINDS`` are not
questions about the ontology's vocabulary, so a proposal that names one is
refused rather than silently ignored.
"""

ONTOLOGY_REVISION_PROPOSAL_GRAMMAR = "malleus.ontology-revision-proposal/v1"
ONTOLOGY_GAP_ANSWER_GRAMMAR = "malleus.ontology-gap-answer/v1"
ONTOLOGY_GAP_ANSWER_EVENT = "ONTOLOGY_GAP_ANSWER_RECORDED"
ONTOLOGY_GAP_DISPOSITIONS = ("ACCEPTED", "REFUSED")

#: The closed field set of one declared gap inside a retained gaps artifact.
#: ``_contract_pipeline.population`` writes exactly these four fields; this
#: module reads them and moves none of those bytes.
#: ``tests/contract_compiler/pareto/test_ontology_gap_answer.py`` holds the two
#: literals to one value.
GAP_FIELDS = frozenset({"kind", "locator", "source_id", "statement"})

#: The closed field set of the Core-generated gaps artifact.
_GAPS_ARTIFACT_FIELDS = frozenset({"gaps", "plan_id"})

_PROPOSAL_FIELDS = frozenset(
    {
        "answers_gaps",
        "grammar",
        "issued_at",
        "linkml_addition",
        "proposal_id",
        "reason",
        "revision_id",
    }
)
_ANSWER_FIELDS = frozenset(
    {
        "answered_gaps",
        "deciding_actor",
        "disposition",
        "grammar",
        "proposal_id",
        "reason",
        "revision_identity",
    }
)
_PROPOSAL_MARKER = ONTOLOGY_REVISION_PROPOSAL_GRAMMAR.encode("utf-8")
_GAPS_MARKER = b'"plan_id"'


class OntologyGapAnswerRefusalReason(Enum):
    """Every way answering a declared ontology gap fails closed."""

    MALFORMED_PROPOSAL = auto()
    MALFORMED_ANSWER = auto()
    UNKNOWN_GAP = auto()
    GAP_ALREADY_ANSWERED = auto()
    GAP_KIND_NOT_ONTOLOGY = auto()
    PROPOSAL_NOT_ADDITIVE = auto()
    PROPOSAL_DOES_NOT_COMPILE = auto()
    UNKNOWN_PROPOSAL = auto()
    PROPOSAL_ALREADY_DECIDED = auto()
    MISSING_DECIDING_ACTOR = auto()
    PROPOSAL_TARGET_NOT_DERIVED = auto()


class OntologyGapAnswerRefusal(ValueError):
    def __init__(self, reason: OntologyGapAnswerRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def refuse(reason: OntologyGapAnswerRefusalReason, detail: str) -> Exception:
    return OntologyGapAnswerRefusal(reason, detail)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith("sha256:")
        and all(character in "0123456789abcdef" for character in value[7:])
    )


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} is required")
    return value


def _identities(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a nonempty array")
    if not all(_is_digest(item) for item in value):
        raise ValueError(f"{label} must hold SHA-256 gap identities")
    identities = tuple(value)
    if identities != tuple(sorted(set(identities))):
        raise ValueError(f"{label} must be sorted and unique")
    return identities


def ontology_gap_identity(*, gap: Mapping[str, object], plan_id: str) -> str:
    """The identity of one declared gap, derived from the bytes it identifies.

    Exactly this is digested: the canonical JSON encoding (UTF-8, sorted keys,
    no whitespace) of ``{"gap": <gap>, "plan_id": <plan_id>}``, where ``<gap>``
    is the gap's four declared fields ``kind``, ``locator``, ``source_id`` and
    ``statement``. Nothing else enters it, so the same gap declared in another
    plan is another gap, and a gap re-declared verbatim in a later plan is a new
    one with a new identity.
    """

    if not isinstance(gap, Mapping):
        raise refuse(
            OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL,
            "a gap object is required",
        )
    if set(gap) != GAP_FIELDS:
        raise refuse(
            OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL,
            "gap fields are not closed",
        )
    if not isinstance(plan_id, str) or not plan_id:
        raise refuse(
            OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL,
            "a plan ID is required",
        )
    fields = {}
    for field in sorted(GAP_FIELDS):
        value = gap[field]
        if not isinstance(value, str) or not value:
            raise refuse(
                OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL,
                f"gap {field} is required",
            )
        fields[field] = value
    return _digest(canonical_json({"gap": fields, "plan_id": plan_id}))


@dataclass(frozen=True, slots=True)
class DeclaredGap:
    """One gap read back out of a retained gaps artifact."""

    identity: str
    kind: str
    locator: str
    plan_id: str
    source_id: str
    statement: str


@dataclass(frozen=True, slots=True)
class OpenRevisionProposal:
    """One retained, undecided proposal, as a report names it."""

    proposal_id: str
    identity: str


@dataclass(frozen=True, slots=True)
class OpenOntologyGap:
    """One open ontology gap with the proposals still open against it."""

    identity: str
    kind: str
    locator: str
    plan_id: str
    source_id: str
    statement: str
    open_proposals: tuple[OpenRevisionProposal, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "identity": self.identity,
            "kind": self.kind,
            "locator": self.locator,
            "open_proposals": [
                {"identity": item.identity, "proposal_id": item.proposal_id}
                for item in self.open_proposals
            ],
            "plan_id": self.plan_id,
            "source_id": self.source_id,
            "statement": self.statement,
        }


def declared_gaps(record_id: str, content: bytes) -> tuple[DeclaredGap, ...]:
    """The gaps one retained input declares, or nothing if it declares none.

    A gaps artifact is recognised by its own bytes and checked against its own
    record ID: canonical JSON with exactly ``gaps`` and ``plan_id``, retained
    under ``<plan_id>:gaps``, which is the ID ``prepare_population_change``
    derives when it generates one. Anything else is not a gaps artifact, and
    nothing here is inferred from a name alone.
    """

    if _GAPS_MARKER not in content:
        return ()
    try:
        data = json.loads(content)
    except (UnicodeDecodeError, ValueError):
        return ()
    if not isinstance(data, dict) or set(data) != _GAPS_ARTIFACT_FIELDS:
        return ()
    plan_id = data["plan_id"]
    gaps = data["gaps"]
    if not isinstance(plan_id, str) or not plan_id:
        return ()
    if record_id != f"{plan_id}:gaps":
        return ()
    if not isinstance(gaps, list) or not gaps:
        return ()
    if canonical_json(data) != content:
        return ()
    declared: list[DeclaredGap] = []
    for gap in gaps:
        if not isinstance(gap, dict) or set(gap) != GAP_FIELDS:
            return ()
        if any(not isinstance(gap[field], str) or not gap[field] for field in gap):
            return ()
        declared.append(
            DeclaredGap(
                ontology_gap_identity(gap=gap, plan_id=plan_id),
                gap["kind"],
                gap["locator"],
                plan_id,
                gap["source_id"],
                gap["statement"],
            )
        )
    return tuple(declared)


@dataclass(frozen=True, slots=True)
class OntologyRevisionProposal:
    """One proposed additive ontology revision answering named gaps."""

    canonical_bytes: bytes
    identity: str
    proposal_id: str
    revision_id: str
    reason: str
    issued_at: str
    linkml_addition: str
    answers_gaps: tuple[str, ...]

    @classmethod
    def from_bytes(cls, source: bytes) -> OntologyRevisionProposal:
        if type(source) is not bytes:
            raise refuse(
                OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL,
                "proposal input must be exact bytes",
            )
        try:
            data = json.loads(source)
            if not isinstance(data, dict):
                raise ValueError("proposal root must be an object")
            if canonical_json(data) != source:
                raise ValueError("proposal bytes are not canonical")
            if set(data) != _PROPOSAL_FIELDS:
                if "target" in set(data) - _PROPOSAL_FIELDS:
                    raise ValueError(
                        "Core derives a proposal's target from the retained "
                        "source; a proposal that supplies target is not one"
                    )
                raise ValueError("proposal fields are not closed")
            if data["grammar"] != ONTOLOGY_REVISION_PROPOSAL_GRAMMAR:
                raise ValueError("proposal grammar is unsupported")
            return cls(
                source,
                _digest(source),
                _text(data["proposal_id"], "proposal ID"),
                _text(data["revision_id"], "revision ID"),
                _text(data["reason"], "revision reason"),
                _text(data["issued_at"], "revision issue time"),
                _text(data["linkml_addition"], "LinkML addition"),
                _identities(data["answers_gaps"], "answered gap identities"),
            )
        except OntologyGapAnswerRefusal:
            raise
        except (TypeError, ValueError) as error:
            raise refuse(
                OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL,
                str(error),
            ) from error


def read_proposal(record_id: str, content: bytes) -> OntologyRevisionProposal | None:
    """The proposal one retained input declares, or ``None``.

    Bytes that claim the proposal grammar are read as a proposal and refused if
    they are not one, so a malformed proposal never hides behind its own
    malformation. The retained record ID must be the proposal ID its owner
    declared, which is what makes a proposal addressable for acceptance.
    """

    if _PROPOSAL_MARKER not in content:
        return None
    try:
        data = json.loads(content)
    except (UnicodeDecodeError, ValueError):
        return None
    if (
        not isinstance(data, dict)
        or data.get("grammar") != ONTOLOGY_REVISION_PROPOSAL_GRAMMAR
    ):
        return None
    proposal = OntologyRevisionProposal.from_bytes(content)
    if proposal.proposal_id != record_id:
        raise refuse(
            OntologyGapAnswerRefusalReason.MALFORMED_PROPOSAL,
            "a retained proposal's record ID must be its declared proposal ID: "
            f"{record_id} holds {proposal.proposal_id}",
        )
    return proposal


@dataclass(frozen=True, slots=True)
class OntologyGapAnswer:
    """One recorded decision closing the gaps it names."""

    canonical_bytes: bytes
    identity: str
    disposition: str
    answered_gaps: tuple[str, ...]
    deciding_actor: str
    reason: str
    proposal_id: str | None
    revision_identity: str | None

    @classmethod
    def from_bytes(cls, source: bytes) -> OntologyGapAnswer:
        if type(source) is not bytes:
            raise refuse(
                OntologyGapAnswerRefusalReason.MALFORMED_ANSWER,
                "answer input must be exact bytes",
            )
        try:
            data = json.loads(source)
            if not isinstance(data, dict):
                raise ValueError("answer root must be an object")
            if canonical_json(data) != source:
                raise ValueError("answer bytes are not canonical")
            if set(data) != _ANSWER_FIELDS:
                raise ValueError("answer fields are not closed")
            if data["grammar"] != ONTOLOGY_GAP_ANSWER_GRAMMAR:
                raise ValueError("answer grammar is unsupported")
            disposition = data["disposition"]
            if disposition not in ONTOLOGY_GAP_DISPOSITIONS:
                raise ValueError("answer disposition is not a declared one")
            proposal_id = data["proposal_id"]
            revision_identity = data["revision_identity"]
            if disposition == "ACCEPTED":
                proposal_id = _text(proposal_id, "answered proposal ID")
                if not _is_digest(revision_identity):
                    raise ValueError("an accepted answer names its revision identity")
            elif proposal_id is not None or revision_identity is not None:
                raise ValueError("a refused answer names no proposal and no revision")
            return cls(
                source,
                _digest(source),
                disposition,
                _identities(data["answered_gaps"], "answered gap identities"),
                _text(data["deciding_actor"], "deciding actor"),
                _text(data["reason"], "decision reason"),
                proposal_id,
                revision_identity,
            )
        except OntologyGapAnswerRefusal:
            raise
        except (TypeError, ValueError) as error:
            raise refuse(
                OntologyGapAnswerRefusalReason.MALFORMED_ANSWER,
                str(error),
            ) from error

    @classmethod
    def compose(
        cls,
        *,
        disposition: str,
        answered_gaps: tuple[str, ...],
        deciding_actor: str,
        reason: str,
        proposal_id: str | None = None,
        revision_identity: str | None = None,
    ) -> OntologyGapAnswer:
        if not isinstance(deciding_actor, str) or not deciding_actor:
            raise refuse(
                OntologyGapAnswerRefusalReason.MISSING_DECIDING_ACTOR,
                "a deciding actor is required; Core records who, it does not decide",
            )
        return cls.from_bytes(
            canonical_json(
                {
                    "answered_gaps": sorted(set(answered_gaps)),
                    "deciding_actor": deciding_actor,
                    "disposition": disposition,
                    "grammar": ONTOLOGY_GAP_ANSWER_GRAMMAR,
                    "proposal_id": proposal_id,
                    "reason": reason,
                    "revision_identity": revision_identity,
                }
            )
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "answered_gaps": list(self.answered_gaps),
            "deciding_actor": self.deciding_actor,
            "disposition": self.disposition,
            "identity": self.identity,
            "proposal_id": self.proposal_id,
            "reason": self.reason,
            "revision_identity": self.revision_identity,
        }


def gap_index(
    retained: Mapping[str, object],
) -> dict[str, DeclaredGap]:
    """Every gap the history's retained inputs declare, keyed by identity."""

    index: dict[str, DeclaredGap] = {}
    for record_id, member in retained.items():
        for gap in declared_gaps(record_id, bytes(member.content)):
            index[gap.identity] = gap
    return index


def check_answerable(
    identities: tuple[str, ...],
    *,
    index: Mapping[str, DeclaredGap],
    answered: frozenset[str],
) -> None:
    """Refuse unless every named gap is an open gap of an ontology kind."""

    for identity in identities:
        gap = index.get(identity)
        if gap is None:
            raise refuse(
                OntologyGapAnswerRefusalReason.UNKNOWN_GAP,
                f"no retained gaps artifact declares gap {identity}",
            )
        if gap.kind not in ONTOLOGY_GAP_KINDS:
            raise refuse(
                OntologyGapAnswerRefusalReason.GAP_KIND_NOT_ONTOLOGY,
                f"gap {identity} is {gap.kind}; permitted kinds: "
                + ", ".join(ONTOLOGY_GAP_KINDS),
            )
        if identity in answered:
            raise refuse(
                OntologyGapAnswerRefusalReason.GAP_ALREADY_ANSWERED,
                f"gap {identity} is already answered; a later plan may declare "
                "it again with new evidence, which is a new gap",
            )


__all__ = (
    "GAP_FIELDS",
    "ONTOLOGY_GAP_ANSWER_EVENT",
    "ONTOLOGY_GAP_ANSWER_GRAMMAR",
    "ONTOLOGY_GAP_DISPOSITIONS",
    "ONTOLOGY_GAP_KINDS",
    "ONTOLOGY_REVISION_PROPOSAL_GRAMMAR",
    "DeclaredGap",
    "OntologyGapAnswer",
    "OntologyGapAnswerRefusal",
    "OntologyGapAnswerRefusalReason",
    "OntologyRevisionProposal",
    "OpenOntologyGap",
    "OpenRevisionProposal",
    "check_answerable",
    "declared_gaps",
    "gap_index",
    "ontology_gap_identity",
    "read_proposal",
)
