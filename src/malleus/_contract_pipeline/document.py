"""Optional document-assertion adapter for neutral population plans."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any

from malleus._contract_pipeline.population import (
    SOURCE_ASSERTION_PROFILE,
    _GAP_KINDS,
    _GRAMMAR as _POPULATION_PLAN_GRAMMAR,
)


DOCUMENT_CAPTURE_GRAMMAR = "malleus.document-capture/private-v0"
DOCUMENT_ASSERTION_ADAPTER = MappingProxyType(
    {"adapter_id": "document-assertion", "version": "0"}
)

_CAPTURE_FIELDS = {
    "assertions",
    "attribution",
    "nothing_assertable",
    "reading_sha256",
    "schema",
}
_ATTRIBUTION_FIELDS = {"author", "date", "source_id"}
_ASSERTION_FIELDS = {
    "block",
    "formalized_by",
    "gaps",
    "id",
    "modality",
    "statement",
}
_ASSERTION_TIME_FIELDS = {"assertion_time", "domain_time"}
EVALUATIVE_SLOT_MIXIN = "Evaluative"
_LOCATOR_SLOT = "assertion_locator"
_EVALUATING_MODALITY_EXCLUDED = "HYPOTHESISED"
_RELATION_FAMILY = "relations"
_CENSUS_TOP_HUBS = 5
_STATEMENT_DIGEST_SLOT = "statement_sha256"
_SUBJECT_SLOT = "subject"
_NAME_SLOT = "name"
_TAGS_SLOT = "tags"
_ENTITY_FAMILY = "entities"
_PROJECTED_ORIGIN = "PROJECTED"
_SUBJECT_PROPOSED = "proposed"
_SUBJECT_PROJECTED = "projected"
_SUBJECT_AMBIGUOUS = "ambiguous"
_SUBJECT_UNNAMED = "unnamed"
_SUBJECT_OUTCOMES = (
    _SUBJECT_AMBIGUOUS,
    _SUBJECT_PROJECTED,
    _SUBJECT_PROPOSED,
    _SUBJECT_UNNAMED,
)
_SUBJECT_PRESENT = frozenset({_SUBJECT_PROPOSED, _SUBJECT_PROJECTED})
_MODALITY_SLOT = "assertion_modality"
_DERIVATION_RULE = (
    "a record's assertion_locator names an assertion of this capture, a "
    "statement_sha256 comes with the locator that checks it and is the "
    "SHA-256 of that assertion's statement bytes, "
    "a slot the contract declares evaluative is formalized by at least one "
    "assertion whose modality is not HYPOTHESISED, a name of a "
    "record's subject, its name or one of its tags, occurs in the "
    "statement of an assertion that formalizes that subject, and a "
    "record's assertion_modality is the modality of an assertion that "
    "formalizes it"
)
_FORMALIZATION_FIELDS = {"path", "record_id"}
_GAP_FIELDS = {"kind", "statement"}
_MODALITIES = {
    "CALCULATED",
    "CONTESTED",
    "HYPOTHESISED",
    "MEASURED",
    "NEGATED",
    "STATED",
}


class DocumentAssertionRefusalReason(str, Enum):
    DIGEST_MISMATCH = "DIGEST_MISMATCH"
    DIGEST_NOT_LOCATED = "DIGEST_NOT_LOCATED"
    EVALUATIVE_SLOT_NOT_EVALUATED = "EVALUATIVE_SLOT_NOT_EVALUATED"
    FIELDS_NOT_CLOSED = "FIELDS_NOT_CLOSED"
    GAP_REQUIRED = "GAP_REQUIRED"
    MALFORMED_CAPTURE = "MALFORMED_CAPTURE"
    MALFORMED_READING = "MALFORMED_READING"
    MODALITY_NOT_ASSERTED = "MODALITY_NOT_ASSERTED"
    NOT_VERBATIM = "NOT_VERBATIM"
    READING_MISMATCH = "READING_MISMATCH"
    SUBJECT_NOT_NAMED = "SUBJECT_NOT_NAMED"
    UNKNOWN_ASSERTION_LOCATOR = "UNKNOWN_ASSERTION_LOCATOR"
    UNKNOWN_BLOCK = "UNKNOWN_BLOCK"
    UNKNOWN_FORMALIZATION_TARGET = "UNKNOWN_FORMALIZATION_TARGET"
    UNKNOWN_GAP_KIND = "UNKNOWN_GAP_KIND"
    UNKNOWN_MODALITY = "UNKNOWN_MODALITY"
    UNSUPPORTED_GRAMMAR = "UNSUPPORTED_GRAMMAR"


class DocumentAssertionRefusal(ValueError):
    def __init__(self, reason: DocumentAssertionRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


@dataclass(frozen=True, slots=True)
class DocumentAssertionCompilation:
    """Exact evidence and deterministic products of one document capture."""

    capture_id: str
    capture_bytes: bytes
    capture_identity: str
    reading_identity: str
    canonical_plan_bytes: bytes
    canonical_census_bytes: bytes


def _fail(
    reason: DocumentAssertionRefusalReason, detail: str
) -> DocumentAssertionRefusal:
    return DocumentAssertionRefusal(reason, detail)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def _load(
    source: bytes, label: str, reason: DocumentAssertionRefusalReason
) -> dict[str, object]:
    if type(source) is not bytes:
        raise _fail(reason, f"{label} must be exact bytes")
    try:
        value = json.loads(source, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError, ValueError) as error:
        raise _fail(reason, f"{label} is not unambiguous JSON") from error
    return _obj(value, label, reason)


def _canonical(value: object, label: str) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
    except (TypeError, UnicodeError, ValueError) as error:
        raise _fail(
            DocumentAssertionRefusalReason.MALFORMED_CAPTURE,
            f"{label} is not JSON data",
        ) from error


def _obj(
    value: object,
    label: str,
    reason: DocumentAssertionRefusalReason = (
        DocumentAssertionRefusalReason.MALFORMED_CAPTURE
    ),
) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _fail(reason, f"{label} must be an object")
    return value


def _items(
    value: object,
    label: str,
    reason: DocumentAssertionRefusalReason = (
        DocumentAssertionRefusalReason.MALFORMED_CAPTURE
    ),
) -> list[object]:
    if not isinstance(value, list):
        raise _fail(reason, f"{label} must be an array")
    return value


def _word(
    value: object,
    label: str,
    reason: DocumentAssertionRefusalReason = (
        DocumentAssertionRefusalReason.MALFORMED_CAPTURE
    ),
) -> str:
    if not isinstance(value, str) or not value:
        raise _fail(reason, f"{label} is required")
    return value


def _closed(value: dict[str, object], fields: set[str], label: str) -> None:
    if set(value) != fields:
        raise _fail(
            DocumentAssertionRefusalReason.FIELDS_NOT_CLOSED,
            f"{label} fields are not closed",
        )


def _reading_blocks(reading: dict[str, object]) -> tuple[tuple[str, str], ...]:
    reason = DocumentAssertionRefusalReason.MALFORMED_READING
    pages = _items(reading.get("pages"), "reading pages", reason)
    blocks: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw_page in pages:
        page = _obj(raw_page, "reading page", reason)
        for raw_block in _items(page.get("blocks"), "reading page blocks", reason):
            block = _obj(raw_block, "reading block", reason)
            block_id = _word(block.get("id"), "reading block ID", reason)
            ordinal = block.get("ordinal")
            text = block.get("text")
            if (
                isinstance(ordinal, bool)
                or not isinstance(ordinal, int)
                or not isinstance(text, str)
            ):
                raise _fail(reason, f"malformed block ordinal or text: {block_id}")
            if block_id in seen:
                raise _fail(reason, f"repeated block ID: {block_id}")
            seen.add(block_id)
            blocks.append((block_id, text))
    return tuple(blocks)


def _record_snapshot(
    records: object,
) -> tuple[dict[str, object], dict[str, dict[str, object]]]:
    root = _obj(json.loads(_canonical(records, "records")), "records")
    by_id: dict[str, dict[str, object]] = {}
    for raw_family in root.values():
        for raw_record in _items(raw_family, "record family"):
            record = _obj(raw_record, "record")
            record_id = _word(record.get("id"), "record ID")
            if record_id in by_id:
                raise _fail(
                    DocumentAssertionRefusalReason.MALFORMED_CAPTURE,
                    f"repeated record ID: {record_id}",
                )
            by_id[record_id] = record
    return root, by_id


def _path_exists(record: dict[str, object], path: list[object]) -> bool:
    if not path or not all(isinstance(step, str) and step for step in path):
        return False
    node: object = record
    for step in path:
        if not isinstance(node, dict) or step not in node:
            return False
        node = node[step]
    return True


def _normalise(text: str) -> str:
    return " ".join(text.split())


def _compact(text: str) -> str:
    return "".join(text.split())


@dataclass(frozen=True, slots=True)
class _Defect:
    """One capture locator the retained reading does not support."""

    reason: DocumentAssertionRefusalReason
    subject: str
    message: str

    @property
    def order(self) -> tuple[str, str, str]:
        return (self.reason.name, self.subject, self.message)

    def render(self) -> str:
        return f"{self.message} [{self.reason.name}]"


def _refuse_defects(defects: list[_Defect]) -> DocumentAssertionRefusal:
    ordered = sorted(defects, key=lambda defect: defect.order)
    return DocumentAssertionRefusal(
        ordered[0].reason,
        "document capture locators are not accepted: "
        + "; ".join(defect.render() for defect in ordered)
        + "; every block ID comes from the reading's inventory and every "
        "statement is copied from its block's own bytes, matching after "
        "whitespace collapse",
    )


def _refuse_derivations(defects: list[_Defect]) -> DocumentAssertionRefusal:
    """One refusal for every derivation whose content the capture denies."""

    ordered = sorted(defects, key=lambda defect: defect.order)
    return DocumentAssertionRefusal(
        ordered[0].reason,
        "document capture derivations are not accepted: "
        + "; ".join(defect.render() for defect in ordered)
        + "; "
        + _DERIVATION_RULE,
    )


def _record_properties(record: dict[str, object]) -> dict[str, object]:
    properties = record.get("properties")
    return properties if isinstance(properties, dict) else {}


def _digest_defects(
    records_by_id: dict[str, dict[str, object]],
    statements: dict[str, str],
) -> list[_Defect]:
    """Recompute every located statement digest against the capture's own text.

    A digest with no locator names no assertion to recompute from, so it is
    not a weaker binding to the words behind a record but none, and it
    refuses under its own reason.
    """

    defects: list[_Defect] = []
    for record_id in sorted(records_by_id):
        properties = _record_properties(records_by_id[record_id])
        declared = properties.get(_STATEMENT_DIGEST_SLOT)
        locator = properties.get(_LOCATOR_SLOT)
        if not isinstance(locator, str) or not locator:
            if isinstance(declared, str) and declared:
                defects.append(
                    _Defect(
                        DocumentAssertionRefusalReason.DIGEST_NOT_LOCATED,
                        record_id,
                        f"record {record_id} carries a statement digest and "
                        "no assertion_locator",
                    )
                )
            continue
        if locator not in statements:
            defects.append(
                _Defect(
                    DocumentAssertionRefusalReason.UNKNOWN_ASSERTION_LOCATOR,
                    record_id,
                    f"record {record_id} names unknown assertion {locator}",
                )
            )
            continue
        if not isinstance(declared, str) or not declared:
            continue
        recomputed = _digest(statements[locator].encode("utf-8"))
        if declared != recomputed:
            defects.append(
                _Defect(
                    DocumentAssertionRefusalReason.DIGEST_MISMATCH,
                    record_id,
                    f"record {record_id} names assertion {locator} with "
                    f"statement digest {declared}, and that assertion's "
                    f"statement digests to {recomputed}",
                )
            )
    return defects


def _evaluative_slots(contract_view: object) -> frozenset[str]:
    """The slot names the bound contract's `Evaluative` mixin declares.

    The mixin's slot list is the declaration. A contract that does not carry
    the mixin declares no evaluative slot, and no contract declares none.
    """

    if contract_view is None:
        return frozenset()
    try:
        return frozenset(contract_view.effective_slots(EVALUATIVE_SLOT_MIXIN))
    except KeyError:
        return frozenset()


def _subject_bearing_types(
    contract_view: object, types: set[str]
) -> frozenset[str]:
    """The record types the bound contract declares as carrying ``subject``.

    Which types may name a subject is a contract question, so the adapter asks
    the compiled contract and nothing else. Without one it knows no such type,
    exactly as it knows no evaluative slot, and the coverage axis stays empty.
    """

    if contract_view is None:
        return frozenset()
    bearing: set[str] = set()
    for type_name in types:
        try:
            slots = contract_view.effective_slots(type_name)
        except (KeyError, ValueError):
            continue
        if _SUBJECT_SLOT in slots:
            bearing.add(type_name)
    return frozenset(bearing)


def _subject_census(
    records_by_id: dict[str, dict[str, object]],
    bearing: frozenset[str],
    outcomes: dict[str, str],
) -> dict[str, object]:
    """Report how each subject-bearing record came by its subject, or did not.

    One axis, reported and never refused. ``by_type`` carries one entry per
    subject-bearing type present in the records, each with ``total``, the four
    outcomes and their two sums; the top-level counts are those summed.
    ``proposed`` is a subject the producer set, ``projected`` one the adapter
    derived from the single entity a formalizing sentence names, and
    ``with_subject`` is the two together. ``ambiguous`` is a record whose
    sentences name more than one entity and ``unnamed`` one whose sentences
    name none, which are the two ways the slot stays unset rather than
    invented.
    """

    by_type: dict[str, dict[str, int]] = {}
    for record_id in sorted(records_by_id):
        record = records_by_id[record_id]
        type_name = record.get("type")
        if not isinstance(type_name, str) or type_name not in bearing:
            continue
        counts = by_type.setdefault(
            type_name,
            {"total": 0, "with_subject": 0, "without_subject": 0}
            | {outcome: 0 for outcome in _SUBJECT_OUTCOMES},
        )
        outcome = outcomes.get(record_id, _SUBJECT_UNNAMED)
        counts["total"] += 1
        counts[outcome] += 1
        counts[
            "with_subject" if outcome in _SUBJECT_PRESENT else "without_subject"
        ] += 1
    totals: dict[str, object] = {
        key: sum(counts[key] for counts in by_type.values())
        for key in ("total", "with_subject", "without_subject", *_SUBJECT_OUTCOMES)
    }
    return {"by_type": dict(sorted(by_type.items())), **totals}


def _project_subjects(
    records_by_id: dict[str, dict[str, object]],
    record_data: dict[str, object],
    bearing: frozenset[str],
    derivations: list[dict[str, object]],
    statements: dict[str, str],
    source_id: str,
) -> dict[str, str]:
    """Set the subject of a record whose formalizing sentence names one entity.

    Run-11 left 77 source-asserted records with no subject whose own
    formalizing sentence nonetheless names an entity of the same capture. The
    name is in the retained bytes, so the compiler derives the attachment
    rather than leaving it to the producer's diligence, and the producer sets
    ``subject`` only where the sentence names more than one entity or where
    the one it names is not what the record is about.

    The candidates are the capture's entity records that carry a ``name`` and
    whose own type bears no subject, compared by the Core-15 rule against the
    statement of every assertion formalizing any field of the record,
    whitespace removed from both sides and case-folded. Exactly one entity
    named projects; none and more than one leave the slot unset and the census
    says which. The derivation is recorded against the first assertion, in
    capture order, whose statement names that entity, and carries
    ``origin: PROJECTED`` so a reader of the plan tells a derived subject from
    a producer's own. Nothing here refuses, and a subject the producer set is
    left alone and checked as before.
    """

    outcomes: dict[str, str] = {}
    if not bearing:
        return outcomes

    candidates: list[tuple[str, list[str]]] = []
    for raw_record in _items(
        record_data.get(_ENTITY_FAMILY, []), "record family"
    ):
        entity = _obj(raw_record, "record")
        type_name = entity.get("type")
        if not isinstance(type_name, str) or type_name in bearing:
            continue
        name = _record_properties(entity).get(_NAME_SLOT)
        if not isinstance(name, str) or not name:
            continue
        candidates.append(
            (
                _word(entity.get("id"), "record ID"),
                [_compact(form).casefold() for form in _subject_names(entity)],
            )
        )

    locators_by_record: dict[str, list[str]] = {}
    for derivation in derivations:
        locators = locators_by_record.setdefault(str(derivation["record_id"]), [])
        locator = str(derivation["locator"])
        if locator not in locators:
            locators.append(locator)

    projected: list[dict[str, object]] = []
    for record_id in sorted(records_by_id):
        record = records_by_id[record_id]
        type_name = record.get("type")
        if not isinstance(type_name, str) or type_name not in bearing:
            continue
        properties = record.get("properties")
        if not isinstance(properties, dict):
            outcomes[record_id] = _SUBJECT_UNNAMED
            continue
        subject = properties.get(_SUBJECT_SLOT)
        if isinstance(subject, str) and subject:
            outcomes[record_id] = _SUBJECT_PROPOSED
            continue
        named: dict[str, str] = {}
        for locator in locators_by_record.get(record_id, []):
            statement = _compact(statements[locator]).casefold()
            for entity_id, forms in candidates:
                if entity_id in named:
                    continue
                if any(form in statement for form in forms):
                    named[entity_id] = locator
        if len(named) != 1:
            outcomes[record_id] = (
                _SUBJECT_AMBIGUOUS if named else _SUBJECT_UNNAMED
            )
            continue
        entity_id, locator = next(iter(named.items()))
        properties[_SUBJECT_SLOT] = entity_id
        projected.append(
            {
                "locator": locator,
                "origin": _PROJECTED_ORIGIN,
                "path": ["properties", _SUBJECT_SLOT],
                "record_id": record_id,
                "source_id": source_id,
            }
        )
        outcomes[record_id] = _SUBJECT_PROJECTED
    derivations.extend(projected)
    return outcomes


def _derivation_census(
    derivations: list[dict[str, object]],
    block_by_assertion: dict[str, str],
    record_data: dict[str, object],
) -> dict[str, object]:
    """Report how far each derivation reaches, and how much each one carries.

    Three axes, reported and never refused. ``assertion_fan_out`` counts, for
    every captured assertion, the distinct records it formalizes.
    ``relation_locality`` says of every relation record whether every block
    formalizing one of its own fields also formalizes a field of at least one
    endpoint: ``LOCAL`` when it does, ``NON_LOCAL`` when a block does not, and
    ``UNDERIVED`` when no assertion formalizes the relation at all.
    ``fan_out_distribution`` maps a fan-out count, written as a string, to the
    number of assertions carrying it; ``top_hubs`` lists the assertions with
    the largest fan-out, at most five, each naming its assertion, its block
    and its count; ``non_local_relations`` counts the NON_LOCAL relations.
    """

    fan_out: dict[str, set[str]] = {
        assertion_id: set() for assertion_id in block_by_assertion
    }
    blocks_by_record: dict[str, set[str]] = {}
    for derivation in derivations:
        assertion_id = str(derivation["locator"])
        record_id = str(derivation["record_id"])
        fan_out[assertion_id].add(record_id)
        blocks_by_record.setdefault(record_id, set()).add(
            block_by_assertion[assertion_id]
        )

    locality: dict[str, str] = {}
    for raw_relation in _items(
        record_data.get(_RELATION_FAMILY, []), "record family"
    ):
        relation = _obj(raw_relation, "record")
        relation_id = _word(relation.get("id"), "record ID")
        own = blocks_by_record.get(relation_id, set())
        endpoints: set[str] = set()
        for end in ("source_id", "target_id"):
            target = relation.get(end)
            if isinstance(target, str):
                endpoints |= blocks_by_record.get(target, set())
        locality[relation_id] = (
            "UNDERIVED" if not own else "LOCAL" if own <= endpoints else "NON_LOCAL"
        )

    counts = {assertion_id: len(seen) for assertion_id, seen in fan_out.items()}
    distribution: dict[str, int] = {}
    for count in counts.values():
        key = str(count)
        distribution[key] = distribution.get(key, 0) + 1
    hubs = sorted(
        (
            (-count, assertion_id)
            for assertion_id, count in counts.items()
            if count
        )
    )[:_CENSUS_TOP_HUBS]
    return {
        "assertion_fan_out": dict(sorted(counts.items())),
        "fan_out_distribution": dict(
            sorted(distribution.items(), key=lambda item: int(item[0]))
        ),
        "non_local_relations": sum(
            1 for value in locality.values() if value == "NON_LOCAL"
        ),
        "relation_locality": dict(sorted(locality.items())),
        "top_hubs": [
            {
                "assertion": assertion_id,
                "block": block_by_assertion[assertion_id],
                "records": -negated,
            }
            for negated, assertion_id in hubs
        ],
    }


def _formalized_slots(
    derivations: list[dict[str, object]],
    modality_by_assertion: dict[str, str],
) -> dict[str, dict[str, list[tuple[str, str]]]]:
    """Group each record's property derivations by slot, with their modality."""

    formalized: dict[str, dict[str, list[tuple[str, str]]]] = {}
    for derivation in derivations:
        path = derivation["path"]
        if not isinstance(path, list) or len(path) != 2 or path[0] != "properties":
            continue
        slot = path[1]
        if not isinstance(slot, str):
            continue
        locator = str(derivation["locator"])
        record = formalized.setdefault(str(derivation["record_id"]), {})
        record.setdefault(slot, []).append(
            (locator, modality_by_assertion[locator])
        )
    return formalized


def _evaluative_defects(
    records_by_id: dict[str, dict[str, object]],
    evaluative: frozenset[str],
    formalized: dict[str, dict[str, list[tuple[str, str]]]],
) -> list[_Defect]:
    """Collect every evaluative value no evaluating assertion formalizes."""

    defects: list[_Defect] = []
    if not evaluative:
        return defects
    for record_id in sorted(records_by_id):
        properties = _record_properties(records_by_id[record_id])
        by_slot = formalized.get(record_id, {})
        for slot in sorted(evaluative & set(properties)):
            formalizing = by_slot.get(slot, [])
            if any(
                modality != _EVALUATING_MODALITY_EXCLUDED
                for _, modality in formalizing
            ):
                continue
            named = (
                ", ".join(
                    f"{assertion_id} {modality}"
                    for assertion_id, modality in sorted(formalizing)
                )
                or "no assertion"
            )
            defects.append(
                _Defect(
                    DocumentAssertionRefusalReason.EVALUATIVE_SLOT_NOT_EVALUATED,
                    f"{record_id} {slot}",
                    f"record {record_id} evaluative slot {slot} is formalized "
                    f"by {named}",
                )
            )
    return defects


def _modality_defects(
    records_by_id: dict[str, dict[str, object]],
    formalized: dict[str, dict[str, list[tuple[str, str]]]],
) -> list[_Defect]:
    """Collect every record modality no assertion behind it asserts.

    An assertion carries one modality, and a record's ``assertion_modality``
    is the modality of an assertion that formalizes it. A sentence carrying
    two modalities is two assertions, so a record formalized from both is
    asserted under either. The slot is optional and a record that leaves it
    unset is not checked.
    """

    defects: list[_Defect] = []
    for record_id in sorted(records_by_id):
        declared = _record_properties(records_by_id[record_id]).get(_MODALITY_SLOT)
        if not isinstance(declared, str) or not declared:
            continue
        formalizing = formalized.get(record_id, {}).get(_MODALITY_SLOT, [])
        if any(modality == declared for _, modality in formalizing):
            continue
        named = (
            ", ".join(
                f"{assertion_id} {modality}"
                for assertion_id, modality in sorted(formalizing)
            )
            or "no assertion"
        )
        defects.append(
            _Defect(
                DocumentAssertionRefusalReason.MODALITY_NOT_ASSERTED,
                record_id,
                f"record {record_id} assertion_modality {declared} is "
                f"formalized by {named}",
            )
        )
    return defects


def _subject_defects(
    records_by_id: dict[str, dict[str, object]],
    formalized: dict[str, dict[str, list[tuple[str, str]]]],
    statements: dict[str, str],
) -> list[_Defect]:
    """Collect every subject the sentence that asserts it does not name.

    A source calls the same thing several things: "Mid-Atlantic Ridge" once
    and "the MAR" thereafter. The subject entity carries its own forms, its
    ``name`` and each member of ``tags``, and at least one of them must occur
    in the statement of an assertion formalizing the record's ``subject``
    path. Both sides drop whitespace and case-fold, so a name the text layer
    breaks across a space or a line still matches its own bytes; neither side
    is rewritten. The forms are read from this change set, which is all the
    adapter is handed: a subject naming no record here may still resolve in
    the base state, so the adapter claims nothing about it and the plan
    compiler refuses one that resolves nowhere.
    """

    defects: list[_Defect] = []
    for record_id in sorted(records_by_id):
        subject = _record_properties(records_by_id[record_id]).get(_SUBJECT_SLOT)
        if not isinstance(subject, str) or not subject:
            continue
        target = records_by_id.get(subject)
        if target is None:
            continue
        names = _subject_names(target)
        if not names:
            defects.append(
                _Defect(
                    DocumentAssertionRefusalReason.SUBJECT_NOT_NAMED,
                    record_id,
                    f"record {record_id} names subject {subject}, which "
                    "carries no name",
                )
            )
            continue
        wanted = [_compact(name).casefold() for name in names]
        formalizing = formalized.get(record_id, {}).get(_SUBJECT_SLOT, [])
        if any(
            form in _compact(statements[assertion_id]).casefold()
            for assertion_id, _ in formalizing
            for form in wanted
        ):
            continue
        named = (
            ", ".join(sorted(assertion_id for assertion_id, _ in formalizing))
            or "no assertion"
        )
        listed = ", ".join(names)
        tried = (
            f"name {listed} is" if len(names) == 1 else f"names {listed} are"
        )
        defects.append(
            _Defect(
                DocumentAssertionRefusalReason.SUBJECT_NOT_NAMED,
                record_id,
                f"record {record_id} names subject {subject}, whose {tried} "
                f"absent from the statement of {named}",
            )
        )
    return defects


def _subject_names(target: dict[str, object]) -> list[str]:
    """Every form a subject carries, its ``name`` first and then its tags.

    ``tags`` is a root slot every Entity already has, string-ranged and
    multivalued, so a source's abbreviation or bare head noun needs no new
    slot. A malformed ``tags`` contributes no form here and is the range
    check's to refuse.
    """

    properties = _record_properties(target)
    declared = [properties.get(_NAME_SLOT)]
    tags = properties.get(_TAGS_SLOT)
    if isinstance(tags, list):
        declared.extend(tags)
    forms = [
        _normalise(value) for value in declared if isinstance(value, str)
    ]
    return [form for form in forms if form]


def _checked_assertions(
    assertions: list[object],
) -> tuple[tuple[dict[str, object], str, str, str], ...]:
    """Close each assertion's shape and return its ID, block, and statement."""

    checked: list[tuple[dict[str, object], str, str, str]] = []
    seen: set[str] = set()
    for raw_assertion in assertions:
        assertion = _obj(raw_assertion, "assertion")
        if not _ASSERTION_FIELDS <= set(assertion) or set(assertion) - (
            _ASSERTION_FIELDS | _ASSERTION_TIME_FIELDS
        ):
            raise _fail(
                DocumentAssertionRefusalReason.FIELDS_NOT_CLOSED,
                "assertion fields are not closed",
            )
        for field in sorted(_ASSERTION_TIME_FIELDS & set(assertion)):
            _word(assertion[field], f"assertion {field}")
        assertion_id = _word(assertion["id"], "assertion ID")
        if assertion_id in seen:
            raise _fail(
                DocumentAssertionRefusalReason.MALFORMED_CAPTURE,
                f"repeated assertion ID: {assertion_id}",
            )
        seen.add(assertion_id)
        checked.append(
            (
                assertion,
                assertion_id,
                _word(assertion["block"], "assertion block"),
                _word(assertion["statement"], "assertion statement"),
            )
        )
    return tuple(checked)


def _locator_defects(
    checked: tuple[tuple[dict[str, object], str, str, str], ...],
    block_text: dict[str, str],
) -> list[_Defect]:
    """Collect every unknown assertion block and every non-verbatim statement."""

    defects: list[_Defect] = []
    for _, assertion_id, block_id, statement in checked:
        if block_id not in block_text:
            defects.append(
                _Defect(
                    DocumentAssertionRefusalReason.UNKNOWN_BLOCK,
                    assertion_id,
                    f"assertion {assertion_id} names unknown block {block_id}",
                )
            )
            continue
        if _normalise(statement) not in _normalise(block_text[block_id]):
            defects.append(
                _Defect(
                    DocumentAssertionRefusalReason.NOT_VERBATIM,
                    assertion_id,
                    f"assertion {assertion_id} is not verbatim in {block_id}",
                )
            )
    return defects


def adapt_document_assertions(
    *,
    reading_bytes: bytes,
    capture_bytes: bytes,
    capture_id: str,
    plan_id: str,
    contract_identity: str,
    records: object,
    supersessions: object,
    contract_view: object | None = None,
) -> DocumentAssertionCompilation:
    """Turn one checked document capture into one neutral population plan.

    ``contract_view`` is the compiled contract the records are written
    against. The adapter reads one thing from it, the slot list of the
    ``Evaluative`` mixin, which is the pack's declaration of which slots
    carry a source's evaluation. Without it the adapter knows no evaluative
    slot and checks none.
    """

    reading = _load(
        reading_bytes,
        "reading",
        DocumentAssertionRefusalReason.MALFORMED_READING,
    )
    capture = _load(
        capture_bytes,
        "capture",
        DocumentAssertionRefusalReason.MALFORMED_CAPTURE,
    )
    _closed(capture, _CAPTURE_FIELDS, "capture")
    if capture["schema"] != DOCUMENT_CAPTURE_GRAMMAR:
        raise _fail(
            DocumentAssertionRefusalReason.UNSUPPORTED_GRAMMAR,
            "document-capture grammar is unsupported",
        )

    reading_identity = _digest(reading_bytes)
    if capture["reading_sha256"] != reading_identity:
        raise _fail(
            DocumentAssertionRefusalReason.READING_MISMATCH,
            "capture does not name the supplied reading bytes",
        )
    blocks = _reading_blocks(reading)
    block_text = dict(blocks)

    attribution = _obj(capture["attribution"], "capture attribution")
    _closed(attribution, _ATTRIBUTION_FIELDS, "capture attribution")
    source_id = _word(attribution["source_id"], "capture source ID")
    _word(attribution["author"], "capture author")
    _word(attribution["date"], "capture date")

    record_data, records_by_id = _record_snapshot(records)
    checked = _checked_assertions(_items(capture["assertions"], "capture assertions"))
    reviewed, defects = _reviewed_blocks(capture, block_text)
    defects.extend(_locator_defects(checked, block_text))
    if defects:
        raise _refuse_defects(defects)
    derivations: list[dict[str, object]] = []
    gaps: list[dict[str, object]] = []
    modality_by_assertion: dict[str, str] = {}
    counts = {
        "FULLY_FORMALIZED": 0,
        "PARTLY_FORMALIZED": 0,
        "UNFORMALIZED": 0,
    }
    gaps_by_kind: dict[str, int] = {}

    for assertion, assertion_id, block_id, _ in checked:
        reviewed.add(block_id)
        modality = _word(assertion["modality"], "assertion modality")
        if modality not in _MODALITIES:
            raise _fail(
                DocumentAssertionRefusalReason.UNKNOWN_MODALITY,
                f"unsupported assertion modality: {modality}",
            )
        modality_by_assertion[assertion_id] = modality

        formalizations = _items(assertion["formalized_by"], "formalized_by")
        assertion_gaps = _items(assertion["gaps"], "assertion gaps")
        if not formalizations and not assertion_gaps:
            raise _fail(
                DocumentAssertionRefusalReason.GAP_REQUIRED,
                f"assertion has no formalization or gap: {assertion_id}",
            )
        _append_formalizations(
            formalizations,
            assertion_id,
            source_id,
            records_by_id,
            derivations,
        )
        _append_gaps(
            assertion_gaps,
            assertion_id,
            source_id,
            gaps,
            gaps_by_kind,
        )
        key = (
            "PARTLY_FORMALIZED"
            if formalizations and assertion_gaps
            else "FULLY_FORMALIZED"
            if formalizations
            else "UNFORMALIZED"
        )
        counts[key] += 1

    statements = {
        assertion_id: statement for _, assertion_id, _, statement in checked
    }
    bearing = _subject_bearing_types(
        contract_view,
        {
            record["type"]
            for record in records_by_id.values()
            if isinstance(record.get("type"), str)
        },
    )
    subject_outcomes = _project_subjects(
        records_by_id,
        record_data,
        bearing,
        derivations,
        statements,
        source_id,
    )
    formalized = _formalized_slots(derivations, modality_by_assertion)
    derivation_defects = _digest_defects(records_by_id, statements)
    derivation_defects.extend(
        _evaluative_defects(
            records_by_id,
            _evaluative_slots(contract_view),
            formalized,
        )
    )
    derivation_defects.extend(
        _subject_defects(records_by_id, formalized, statements)
    )
    derivation_defects.extend(_modality_defects(records_by_id, formalized))
    if derivation_defects:
        raise _refuse_derivations(derivation_defects)

    capture_id = _word(capture_id, "capture ID")
    plan_id = _word(plan_id, "plan ID")
    contract_identity = _word(contract_identity, "contract identity")
    if (
        SOURCE_ASSERTION_PROFILE.time_semantics["knowledge_valid_time"]
        != "CAPTURE_IMPORT_ORDER"
    ):
        raise RuntimeError(
            "the document adapter requires capture-import-order history semantics"
        )
    capture_identity = _digest(capture_bytes)
    plan = {
        "adapter": dict(DOCUMENT_ASSERTION_ADAPTER),
        "contract_identity": contract_identity,
        "derivations": derivations,
        "evidence": [{"evidence_id": capture_id, "sha256": capture_identity}],
        "gaps": gaps,
        "grammar": _POPULATION_PLAN_GRAMMAR,
        "history_profile": {
            "profile_id": SOURCE_ASSERTION_PROFILE.profile_id,
            "sha256": SOURCE_ASSERTION_PROFILE.identity,
        },
        "plan_id": plan_id,
        "records": record_data,
        "sources": [{"sha256": reading_identity, "source_id": source_id}],
        "supersessions": json.loads(_canonical(supersessions, "supersessions")),
        "valid_time": {"kind": "ORDER_ONLY", "value": capture_id},
    }
    census = {
        "assertions": counts,
        "blocks": {
            block_id: "REVIEWED" if block_id in reviewed else "UNTOUCHED"
            for block_id, _ in blocks
        },
        "blocks_reviewed": len(reviewed),
        "blocks_total": len(blocks),
        "capture_sha256": capture_identity,
        "derivation": _derivation_census(
            derivations,
            {assertion_id: block for _, assertion_id, block, _ in checked},
            record_data,
        ),
        "gaps_by_kind": dict(sorted(gaps_by_kind.items())),
        "subject_coverage": _subject_census(
            records_by_id, bearing, subject_outcomes
        ),
    }
    return DocumentAssertionCompilation(
        capture_id=capture_id,
        capture_bytes=capture_bytes,
        capture_identity=capture_identity,
        reading_identity=reading_identity,
        canonical_plan_bytes=_canonical(plan, "population plan"),
        canonical_census_bytes=_canonical(census, "capture census"),
    )


def _reviewed_blocks(
    capture: dict[str, object], block_text: dict[str, str]
) -> tuple[set[str], list[_Defect]]:
    reviewed: set[str] = set()
    defects: list[_Defect] = []
    for value in _items(capture["nothing_assertable"], "nothing_assertable"):
        block_id = _word(value, "nothing_assertable block ID")
        if block_id not in block_text:
            defects.append(
                _Defect(
                    DocumentAssertionRefusalReason.UNKNOWN_BLOCK,
                    block_id,
                    f"nothing_assertable names unknown block {block_id}",
                )
            )
            continue
        reviewed.add(block_id)
    return reviewed, defects


def _append_formalizations(
    values: list[object],
    assertion_id: str,
    source_id: str,
    records: dict[str, dict[str, object]],
    output: list[dict[str, object]],
) -> None:
    for value in values:
        formalization = _obj(value, "formalization")
        _closed(formalization, _FORMALIZATION_FIELDS, "formalization")
        record_id = _word(
            formalization["record_id"],
            "formalization record ID",
            DocumentAssertionRefusalReason.UNKNOWN_FORMALIZATION_TARGET,
        )
        path = _items(
            formalization["path"],
            "formalization path",
            DocumentAssertionRefusalReason.UNKNOWN_FORMALIZATION_TARGET,
        )
        record = records.get(record_id)
        if record is None or not _path_exists(record, path):
            raise _fail(
                DocumentAssertionRefusalReason.UNKNOWN_FORMALIZATION_TARGET,
                f"missing formalization target: {record_id}:{path}",
            )
        output.append(
            {
                "locator": assertion_id,
                "path": path,
                "record_id": record_id,
                "source_id": source_id,
            }
        )


def _append_gaps(
    values: list[object],
    assertion_id: str,
    source_id: str,
    output: list[dict[str, object]],
    counts: dict[str, int],
) -> None:
    for value in values:
        gap = _obj(value, "assertion gap")
        _closed(gap, _GAP_FIELDS, "assertion gap")
        kind = _word(
            gap["kind"],
            "assertion gap kind",
            DocumentAssertionRefusalReason.UNKNOWN_GAP_KIND,
        )
        if kind not in _GAP_KINDS:
            raise _fail(
                DocumentAssertionRefusalReason.UNKNOWN_GAP_KIND,
                f"unsupported assertion gap kind: {kind}",
            )
        output.append(
            {
                "kind": kind,
                "locator": assertion_id,
                "source_id": source_id,
                "statement": _word(gap["statement"], "assertion gap statement"),
            }
        )
        counts[kind] = counts.get(kind, 0) + 1


__all__ = (
    "DOCUMENT_ASSERTION_ADAPTER",
    "DOCUMENT_CAPTURE_GRAMMAR",
    "DocumentAssertionCompilation",
    "DocumentAssertionRefusal",
    "DocumentAssertionRefusalReason",
    "adapt_document_assertions",
)
