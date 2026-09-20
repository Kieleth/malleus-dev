"""Deterministic typed faults injected into one admitted document population.

The paper reports seven model-produced populations admitted with one structural
refusal in total. A reader cannot tell from that whether the gate did anything
or whether the producers were careful. This module manufactures the
counterfactual: it takes run-23's admitted capture and records and returns,
for each declared fault class, several faulted copies selected by a seeded
choice over the capture's own records.

Nothing here validates anything. Every faulted population goes through the same
``run-23/run.py`` invocation the honest population went through, against Core
exported at the pinned commit, and the run's own refusal or admission is the
observation. Injected values are synthetic tokens and synthetic numbers; no
value is copied from the reading.

Fault classes, by the letter the task gives them:

a. ``VALUE_NOT_IN_BLOCK``      a value absent from its cited block
b. ``LOCATOR_REPOINTED_*``     a locator naming a block the record did not
                               come from, in three constructions
c. ``DIGEST_MISMATCH``         a sentence digest that does not match
d. ``DANGLING_ENDPOINT``       a relation endpoint that does not exist
e. ``TYPE_OUTSIDE_ONTOLOGY``   a type the compiled contract does not declare
   ``SLOT_OUTSIDE_ONTOLOGY``   a slot the compiled contract does not declare
f. ``DUPLICATE_RECORD_ID``     one record identity carried twice
g. ``RECORD_WITH_NO_SOURCE``   a record no assertion formalizes
   ``RECORD_WITH_NO_FIELDS``   the same, carrying no property at all
"""

from __future__ import annotations

import copy
from hashlib import sha256
import random
from typing import Any


SEED = 23
INSTANCES_PER_VARIANT = 5

LOCATOR_SLOT = "assertion_locator"
DIGEST_SLOT = "statement_sha256"
MODALITY_SLOT = "assertion_modality"
SUBJECT_SLOT = "subject"
EVALUATIVE_SLOT = "hypothesis_disposition"

# Slots whose range is a plain string, integer or float in the accepted
# closure, so a synthetic value of the same JSON type is well typed and the
# contract's own range check has nothing to say about it. Enum-ranged slots,
# the two provenance slots, the modality, the subject and the tags are left
# out: each is checked by a mechanism other than the one class (a) is about.
VALUE_SLOTS = (
    "analyte",
    "author_statement",
    "claim_kind",
    "container_title",
    "count",
    "count_scope",
    "description",
    "feature_kind",
    "quantity_kind",
    "ratio_value",
    "software_version",
    "uncertainty",
    "unit",
    "value_lower",
    "value_upper",
    "volume",
)

# A type the accepted closure declares, used for the records class (g) adds.
ORPHAN_TYPE = "GeologicFeature"


def digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _rng(label: str) -> random.Random:
    return random.Random(f"{SEED}:{label}")


def _records_by_id(records: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        record["id"]: record for family in sorted(records) for record in records[family]
    }


def _family_of(records: dict[str, Any], record_id: str) -> str:
    for family in sorted(records):
        for record in records[family]:
            if record["id"] == record_id:
                return family
    raise KeyError(record_id)


def _properties(record: dict[str, Any]) -> dict[str, Any]:
    properties = record.get("properties")
    return properties if isinstance(properties, dict) else {}


def _subject_targets(records: dict[str, Any]) -> set[str]:
    """Every record named as some record's subject, left alone by every class.

    A record used as a subject is read by the adapter's own naming check, so
    mutating one would exercise that check instead of the class under test.
    """

    return {
        subject
        for record in _records_by_id(records).values()
        if isinstance(subject := _properties(record).get(SUBJECT_SLOT), str)
    }


def _located(records: dict[str, Any]) -> list[str]:
    """Record IDs carrying both provenance slots, sorted, minus subjects."""

    excluded = _subject_targets(records)
    return sorted(
        record_id
        for record_id, record in _records_by_id(records).items()
        if record_id not in excluded
        and isinstance(_properties(record).get(LOCATOR_SLOT), str)
        and isinstance(_properties(record).get(DIGEST_SLOT), str)
    )


def _statements(capture: dict[str, Any]) -> dict[str, str]:
    return {item["id"]: item["statement"] for item in capture["assertions"]}


def _blocks(capture: dict[str, Any]) -> dict[str, str]:
    return {item["id"]: item["block"] for item in capture["assertions"]}


def _modalities(capture: dict[str, Any]) -> dict[str, str]:
    return {item["id"]: item["modality"] for item in capture["assertions"]}


def _formalizing(capture: dict[str, Any]) -> dict[str, set[str]]:
    """Each record's assertions, as the capture's own formalizations say."""

    reached: dict[str, set[str]] = {}
    for assertion in capture["assertions"]:
        for formalization in assertion["formalized_by"]:
            reached.setdefault(formalization["record_id"], set()).add(assertion["id"])
    return reached


def _synthetic(slot: str, current: Any, ordinal: int, letter: str) -> Any:
    token = f"FAULT-{letter}-{ordinal:02d}-SYNTHETIC"
    if isinstance(current, bool):
        return not current
    if isinstance(current, int):
        return 900000 + ordinal
    if isinstance(current, float):
        return 900000.0 + ordinal
    return token


def _trial(
    trial_id: str,
    fault_class: str,
    letter: str,
    designed_catcher: str,
    predicted: str,
    target: dict[str, Any],
    population: dict[str, Any],
) -> dict[str, Any]:
    return {
        "trial_id": trial_id,
        "fault_class": fault_class,
        "letter": letter,
        "designed_catcher": designed_catcher,
        "predicted_outcome": predicted,
        "target": target,
        "population": population,
    }


def value_not_in_block(honest: dict[str, Any]) -> list[dict[str, Any]]:
    """(a) Replace one well-typed property value with a synthetic value.

    The cited assertion is untouched and stays verbatim in its block, the
    locator still names it and the statement digest still checks out. Only the
    value is now absent from the block it cites.
    """

    records = honest["records"]
    candidates = [
        record_id
        for record_id in _located(records)
        if set(VALUE_SLOTS) & set(_properties(_records_by_id(records)[record_id]))
    ]
    chosen = _rng("a").sample(candidates, INSTANCES_PER_VARIANT)
    trials: list[dict[str, Any]] = []
    for ordinal, record_id in enumerate(sorted(chosen), start=1):
        population = copy.deepcopy(honest)
        record = _records_by_id(population["records"])[record_id]
        slot = sorted(set(VALUE_SLOTS) & set(_properties(record)))[0]
        before = _properties(record)[slot]
        after = _synthetic(slot, before, ordinal, "A")
        record["properties"][slot] = after
        trials.append(
            _trial(
                f"a-{ordinal:02d}",
                "VALUE_NOT_IN_BLOCK",
                "a",
                "NONE_REVIEW_ONLY",
                "ADMITTED_INVISIBLE",
                {
                    "record_id": record_id,
                    "slot": slot,
                    "locator": _properties(record)[LOCATOR_SLOT],
                    "injected_value": after,
                },
                population,
            )
        )
    return trials


def _repoint_candidates(
    capture: dict[str, Any], record_id: str, own: set[str]
) -> list[str]:
    """Assertions in a block none of the record's own assertions names."""

    blocks = _blocks(capture)
    forbidden = {blocks[locator] for locator in own}
    return sorted(
        assertion_id for assertion_id, block in blocks.items() if block not in forbidden
    )


def locator_repointed(honest: dict[str, Any]) -> list[dict[str, Any]]:
    """(b) Three constructions of a locator naming the wrong block.

    ``STALE_DIGEST`` moves the record's locator and leaves the digest it came
    with. ``COHERENT_DIGEST`` moves both, leaving the capture's own
    formalizations where they were. ``COHERENT_DERIVATION`` moves the locator,
    the digest and every formalization of the record together, so that nothing
    inside the change set disagrees with anything else.
    """

    records = honest["records"]
    capture = honest["capture"]
    statements = _statements(capture)
    modalities = _modalities(capture)
    reached = _formalizing(capture)
    by_id = _records_by_id(records)
    located = _located(records)

    trials: list[dict[str, Any]] = []
    for variant, letter, catcher, predicted in (
        ("STALE_DIGEST", "B1", "DIGEST_BINDING", "REFUSED"),
        ("COHERENT_DIGEST", "B2", "TRACE_DERIVATION", "ADMITTED_EXPOSED"),
        ("COHERENT_DERIVATION", "B4", "NONE_REVIEW_ONLY", "ADMITTED_INVISIBLE"),
    ):
        if variant == "COHERENT_DERIVATION":
            candidates = _coherent_move_candidates(honest, located)
        else:
            candidates = [record_id for record_id in located if reached.get(record_id)]
        rng = _rng(f"b:{variant}")
        chosen = sorted(rng.sample(candidates, INSTANCES_PER_VARIANT))
        for ordinal, record_id in enumerate(chosen, start=1):
            population = copy.deepcopy(honest)
            own = set(reached.get(record_id, set())) | {
                _properties(by_id[record_id])[LOCATOR_SLOT]
            }
            pool = _repoint_candidates(capture, record_id, own)
            if variant == "COHERENT_DERIVATION":
                pool = [
                    assertion_id
                    for assertion_id in pool
                    if modalities[assertion_id]
                    == _properties(by_id[record_id]).get(MODALITY_SLOT)
                ]
            target_assertion = pool[
                _rng(f"b:{variant}:{record_id}").randrange(len(pool))
            ]
            record = _records_by_id(population["records"])[record_id]
            record["properties"][LOCATOR_SLOT] = target_assertion
            if variant != "STALE_DIGEST":
                record["properties"][DIGEST_SLOT] = digest(
                    statements[target_assertion].encode("utf-8")
                )
            if variant == "COHERENT_DERIVATION":
                _move_formalizations(population["capture"], record_id, target_assertion)
            trials.append(
                _trial(
                    f"b{letter[1]}-{ordinal:02d}",
                    f"LOCATOR_REPOINTED_{variant}",
                    "b",
                    catcher,
                    predicted,
                    {
                        "record_id": record_id,
                        "from_locator": sorted(own),
                        "to_locator": target_assertion,
                        "from_blocks": sorted({_blocks(capture)[item] for item in own}),
                        "to_block": _blocks(capture)[target_assertion],
                    },
                    population,
                )
            )
    return trials


def _coherent_move_candidates(honest: dict[str, Any], located: list[str]) -> list[str]:
    """Records whose whole derivation can move without tripping another check.

    A record with a subject, an evaluative value or no declared modality is
    left out: moving it would exercise the naming check, the evaluation check
    or nothing at all rather than the locator itself. An assertion that would
    be left with neither a formalization nor a gap is left out too, because
    the adapter refuses that on its own terms.
    """

    capture = honest["capture"]
    reached = _formalizing(capture)
    by_id = _records_by_id(honest["records"])
    gaps = {item["id"]: bool(item["gaps"]) for item in capture["assertions"]}
    fan_out: dict[str, int] = {}
    for assertion in capture["assertions"]:
        fan_out[assertion["id"]] = len(assertion["formalized_by"])
    held: dict[str, dict[str, int]] = {}
    for assertion in capture["assertions"]:
        for formalization in assertion["formalized_by"]:
            counts = held.setdefault(formalization["record_id"], {})
            counts[assertion["id"]] = counts.get(assertion["id"], 0) + 1

    candidates: list[str] = []
    for record_id in located:
        properties = _properties(by_id[record_id])
        if properties.get(SUBJECT_SLOT) or EVALUATIVE_SLOT in properties:
            continue
        if not isinstance(properties.get(MODALITY_SLOT), str):
            continue
        own = reached.get(record_id, set())
        if not own:
            continue
        if any(
            fan_out[assertion_id] - held[record_id][assertion_id] == 0
            and not gaps[assertion_id]
            for assertion_id in own
        ):
            continue
        candidates.append(record_id)
    return candidates


def _move_formalizations(
    capture: dict[str, Any], record_id: str, target_assertion: str
) -> None:
    """Move every formalization of one record onto one other assertion."""

    moved: list[dict[str, Any]] = []
    for assertion in capture["assertions"]:
        keep = []
        for formalization in assertion["formalized_by"]:
            if formalization["record_id"] == record_id:
                moved.append(formalization)
            else:
                keep.append(formalization)
        assertion["formalized_by"] = keep
    for assertion in capture["assertions"]:
        if assertion["id"] == target_assertion:
            assertion["formalized_by"].extend(moved)
            return
    raise KeyError(target_assertion)


def digest_mismatch(honest: dict[str, Any]) -> list[dict[str, Any]]:
    """(c) Replace a statement digest with the digest of synthetic bytes."""

    records = honest["records"]
    candidates = _located(records)
    chosen = sorted(_rng("c").sample(candidates, INSTANCES_PER_VARIANT))
    trials: list[dict[str, Any]] = []
    for ordinal, record_id in enumerate(chosen, start=1):
        population = copy.deepcopy(honest)
        record = _records_by_id(population["records"])[record_id]
        injected = digest(f"FAULT-C-{ordinal:02d}-SYNTHETIC".encode())
        record["properties"][DIGEST_SLOT] = injected
        trials.append(
            _trial(
                f"c-{ordinal:02d}",
                "DIGEST_MISMATCH",
                "c",
                "DIGEST_BINDING",
                "REFUSED",
                {
                    "record_id": record_id,
                    "locator": _properties(record)[LOCATOR_SLOT],
                    "injected_digest": injected,
                },
                population,
            )
        )
    return trials


def dangling_endpoint(honest: dict[str, Any]) -> list[dict[str, Any]]:
    """(d) Point one relation endpoint at a record identity that is absent."""

    relations = sorted((relation["id"] for relation in honest["records"]["relations"]))
    chosen = sorted(_rng("d").sample(relations, INSTANCES_PER_VARIANT))
    trials: list[dict[str, Any]] = []
    for ordinal, record_id in enumerate(chosen, start=1):
        population = copy.deepcopy(honest)
        record = _records_by_id(population["records"])[record_id]
        absent = f"fault:d:{ordinal:02d}:absent-endpoint"
        before = record["target_id"]
        record["target_id"] = absent
        trials.append(
            _trial(
                f"d-{ordinal:02d}",
                "DANGLING_ENDPOINT",
                "d",
                "ADMISSION_STRUCTURAL_CHECK",
                "REFUSED",
                {
                    "record_id": record_id,
                    "endpoint": "target_id",
                    "was": before,
                    "injected": absent,
                },
                population,
            )
        )
    return trials


def outside_ontology(honest: dict[str, Any]) -> list[dict[str, Any]]:
    """(e) A type, and a slot, the compiled contract does not declare.

    The slot variant also cites the new slot from one of the record's own
    assertions, so the fault reaches the compiled contract instead of being
    refused earlier as an undeclared formalization target.
    """

    records = honest["records"]
    capture = honest["capture"]
    reached = _formalizing(capture)
    located = [record_id for record_id in _located(records) if reached.get(record_id)]

    trials: list[dict[str, Any]] = []
    for variant, catcher, predicted in (
        ("TYPE", "COMPILER", "REFUSED"),
        ("SLOT", "COMPILER", "REFUSED"),
    ):
        chosen = sorted(_rng(f"e:{variant}").sample(located, INSTANCES_PER_VARIANT))
        for ordinal, record_id in enumerate(chosen, start=1):
            population = copy.deepcopy(honest)
            record = _records_by_id(population["records"])[record_id]
            if variant == "TYPE":
                injected = f"FaultInjectedTypeE{ordinal:02d}"
                was = record["type"]
                record["type"] = injected
                target = {"record_id": record_id, "was": was, "injected": injected}
            else:
                injected = f"fault_injected_slot_e{ordinal:02d}"
                record["properties"][injected] = f"FAULT-E-{ordinal:02d}-SYNTHETIC"
                host = sorted(reached[record_id])[0]
                for assertion in population["capture"]["assertions"]:
                    if assertion["id"] == host:
                        assertion["formalized_by"].append(
                            {
                                "path": ["properties", injected],
                                "record_id": record_id,
                            }
                        )
                        break
                target = {
                    "record_id": record_id,
                    "injected": injected,
                    "cited_from": host,
                }
            trials.append(
                _trial(
                    f"e{variant[0].lower()}-{ordinal:02d}",
                    f"{variant}_OUTSIDE_ONTOLOGY",
                    "e",
                    catcher,
                    predicted,
                    target,
                    population,
                )
            )
    return trials


def duplicate_record_id(honest: dict[str, Any]) -> list[dict[str, Any]]:
    """(f) Carry one record identity twice in its own family."""

    records = honest["records"]
    candidates = _located(records)
    chosen = sorted(_rng("f").sample(candidates, INSTANCES_PER_VARIANT))
    trials: list[dict[str, Any]] = []
    for ordinal, record_id in enumerate(chosen, start=1):
        population = copy.deepcopy(honest)
        family = _family_of(population["records"], record_id)
        original = _records_by_id(population["records"])[record_id]
        twin = copy.deepcopy(original)
        twin["properties"] = dict(twin["properties"])
        population["records"][family].append(twin)
        trials.append(
            _trial(
                f"f-{ordinal:02d}",
                "DUPLICATE_RECORD_ID",
                "f",
                "ADMISSION_STRUCTURAL_CHECK",
                "REFUSED",
                {"record_id": record_id, "family": family},
                population,
            )
        )
    return trials


def record_with_no_source(honest: dict[str, Any]) -> list[dict[str, Any]]:
    """(g) A record no assertion of the capture formalizes.

    ``WITH_FIELDS`` carries one property, so every properties key of it is
    underived. ``NO_FIELDS`` carries none, which is the same record with
    nothing for a derivation to be required of.
    """

    trials: list[dict[str, Any]] = []
    for variant, catcher, predicted, properties in (
        (
            "WITH_FIELDS",
            "ADMISSION_STRUCTURAL_CHECK",
            "REFUSED",
            lambda ordinal: {"name": f"FAULT-G-{ordinal:02d}-SYNTHETIC"},
        ),
        ("NO_FIELDS", "NONE_REVIEW_ONLY", "ADMITTED_INVISIBLE", lambda ordinal: {}),
    ):
        for ordinal in range(1, INSTANCES_PER_VARIANT + 1):
            population = copy.deepcopy(honest)
            record_id = f"fault:g:{variant.lower()}:{ordinal:02d}"
            population["records"]["entities"].append(
                {
                    "id": record_id,
                    "properties": properties(ordinal),
                    "type": ORPHAN_TYPE,
                }
            )
            trials.append(
                _trial(
                    f"g{variant[0].lower()}-{ordinal:02d}",
                    f"RECORD_WITH_NO_SOURCE_{variant}",
                    "g",
                    catcher,
                    predicted,
                    {"record_id": record_id, "type": ORPHAN_TYPE},
                    population,
                )
            )
    return trials


BUILDERS = (
    value_not_in_block,
    locator_repointed,
    digest_mismatch,
    dangling_endpoint,
    outside_ontology,
    duplicate_record_id,
    record_with_no_source,
)


def catalog(honest: dict[str, Any]) -> list[dict[str, Any]]:
    """Every trial, in a fixed order, built from one honest population."""

    trials: list[dict[str, Any]] = []
    for builder in BUILDERS:
        trials.extend(builder(honest))
    identifiers = [trial["trial_id"] for trial in trials]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("trial identifiers are not unique")
    return trials
