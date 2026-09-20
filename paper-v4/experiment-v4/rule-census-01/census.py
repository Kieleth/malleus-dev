"""A read-only census of five candidate adopter rules over two populations.

Nothing here is a rule. No Prolog, no policy, no check contract, no admission.
Every candidate is a query, every refusal is counted and labelled with a
mechanism, and the definitions are the ones [README.md](README.md) fixed before
this file ran.

    CORE=private/shop-progressive-01/runtime
    PYTHONDONTWRITEBYTECODE=1 \\
      PYTHONPATH="$CORE/src:$CORE:paper-v4/experiment-v4/rule-census-01:." \\
      .venv/bin/python paper-v4/experiment-v4/rule-census-01/census.py \\
      --private private/paper-v4-rule-census-01
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field, replace
from decimal import Decimal
import json
from pathlib import Path
import shutil
import subprocess

import malleus.compiler as api

import normalise
from normalise import GLUED, UNGLUED

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_23 = ROOT / "private/paper-v4-v4-run-23"
PRODUCER = RUN_23 / "producer"
RUNTIME = ROOT / "private/shop-progressive-01/runtime"
PRIVATE = ROOT / "private/paper-v4-rule-census-01"

OUTCOME_SCHEMA = "malleus.paper-v4.rule-census-01-outcomes/v1"
CORE_COMMIT = "e7937b89"

CLOSURE = (
    ("paper-v4-project", "work/ontology-attempt-01.yaml"),
    ("malleus", "inputs/malleus.yaml"),
    ("linkml:types", "inputs/linkml-types.yaml"),
    ("metrology", "inputs/metrology.yaml"),
    ("chronology", "inputs/chronology.yaml"),
    ("research", "inputs/research.yaml"),
)
READING = "inputs/selected-reading.json"
POPULATION = "work/document-population.json"
CAPTURE_ID = "capture:paper-v4:yu-2025:v4:23"
PLAN_ID = "plan:paper-v4:yu-2025:v4:23"

CITED = "CITED"
DERIVED = "DERIVED"
SCOPES = (CITED, DERIVED)

NUMERIC_RANGES = ("Float", "Integer")
CITATION_SLOT = "assertion_locator"

# Candidate (a), exactly as content-rules-doc-01 defined it.
QUANTITY_FAMILIES = (
    ("QUANTIFIED", ("quantity_kind",), ("value_lower", "value_upper")),
    ("COUNTED", ("count_scope",), ("count",)),
    ("RATIO", ("numerator_kind", "denominator_kind"), ("ratio_value",)),
)
QUALIFIERS = (
    "unit",
    "determination",
    "value_qualification",
    "depth_reference",
    "melt_stage",
    "analyte",
    "estimation_proxy",
    "begins_at",
    "ends_at",
    "temporal_precision",
    "temporal_reference_system",
)
ADDED_QUALIFIER = "assertion_modality"

# The Shop's own conflict keying, never counted as candidate (a).
SHOP_CONFLICT_FAMILY = (
    "SHOP_OWN_CONFLICT_KEYING",
    ("order_id", "product_code"),
    ("ordered_quantity",),
)

# Candidate (b).
INTERVAL_CLAUSES = (
    "value_lower<=value_upper",
    "uncertainty>=0",
    "count>=0",
    "ratio_value>=0",
)
INTERVAL_SLOTS = ("count", "ratio_value", "uncertainty", "value_lower", "value_upper")
SHOP_NON_NEGATIVE = "ordered_quantity>=0"

# Candidate (c): the five slots the task names, kept beside the contract-derived
# set so the difference between a named list and a declared range is a measured
# number rather than an assumption.
NAMED_NUMERIC_SLOTS = frozenset(
    {"count", "ratio_value", "uncertainty", "value_lower", "value_upper"}
)

# Candidate (c): the three declared readings of "a number in the text".
NUMBER_READINGS = (
    ("UNGLUED_FREE", UNGLUED, False),
    ("GLUED_ATTACHED", GLUED, True),
    ("GLUED_FREE", GLUED, False),
)

UNIT_SLOTS = ("unit",)
FORMULA_SLOTS = ("analyte", "numerator_kind", "denominator_kind")


# ---------------------------------------------------------------------------
# Populations
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Record:
    record_id: str
    record_type: str
    properties: dict[str, object]
    cited: str | None


@dataclass(frozen=True)
class Population:
    name: str
    workspace: Path
    view: object
    ontology_hash: str
    records: dict[str, Record]
    texts: dict[str, str]
    derivation_rows: list[tuple[str, tuple[str, ...], str]]
    record_level_citation: bool
    by_record: dict[str, tuple[str, ...]] = field(default_factory=dict)
    by_slot: dict[tuple[str, str], tuple[str, ...]] = field(default_factory=dict)


def _index(rows):
    by_record: dict[str, set[str]] = {}
    by_slot: dict[tuple[str, str], set[str]] = {}
    for record_id, path, locator in rows:
        by_record.setdefault(record_id, set()).add(locator)
        if len(path) == 2 and path[0] == "properties":
            by_slot.setdefault((record_id, path[1]), set()).add(locator)
    return (
        {key: tuple(sorted(value)) for key, value in by_record.items()},
        {key: tuple(sorted(value)) for key, value in by_slot.items()},
    )


def private_is_ignored(path: Path) -> bool:
    """Confirm the private directory is git-ignored before anything is written."""

    completed = subprocess.run(
        ["git", "check-ignore", "-q", str(path)], cwd=ROOT, capture_output=True
    )
    return completed.returncode == 0


def stage_document(into: Path) -> dict[str, object]:
    """Copy exactly the files this census reads, the way bridge-01 does."""

    copied = {}
    for relative in [path for _, path in CLOSURE] + [READING, POPULATION]:
        destination = into / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PRODUCER / relative, destination)
        copied[relative] = destination
    return copied


def load_document(private: Path = PRIVATE) -> Population:
    """Run-23's records, the adapter's derivations, and the retained sentences."""

    workspace = private / "document"
    shutil.rmtree(workspace, ignore_errors=True)
    copied = stage_document(workspace)
    compilation = api.compile_linkml_contract(
        root_locator="paper-v4-project",
        sources={locator: copied[path].read_bytes() for locator, path in CLOSURE},
    )
    population = json.loads(copied[POPULATION].read_bytes())
    capture = population["capture"]
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=api.STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    adapted = api.adapt_document_assertions(
        reading_bytes=copied[READING].read_bytes(),
        capture_bytes=canonical(capture),
        capture_id=CAPTURE_ID,
        plan_id=PLAN_ID,
        contract_identity=partial.identity,
        records=population["records"],
        supersessions=population["supersessions"],
        contract_view=compilation.view,
    )
    plan = json.loads(adapted.canonical_plan_bytes)
    rows = [
        (
            str(item["record_id"]),
            tuple(str(step) for step in item["path"]),
            str(item["locator"]),
        )
        for item in plan["derivations"]
    ]
    records = {}
    for family in sorted(population["records"]):
        for record in population["records"][family]:
            properties = dict(record.get("properties", {}))
            cited = properties.get(CITATION_SLOT)
            records[str(record["id"])] = Record(
                record_id=str(record["id"]),
                record_type=str(record["type"]),
                properties=properties,
                cited=str(cited) if cited else None,
            )
    by_record, by_slot = _index(rows)
    return Population(
        name="run-23",
        workspace=workspace,
        view=compilation.view,
        ontology_hash=compilation.view.content_hash(),
        records=records,
        texts={
            str(item["id"]): str(item["statement"]) for item in capture["assertions"]
        },
        derivation_rows=rows,
        record_level_citation=True,
        by_record=by_record,
        by_slot=by_slot,
    )


def _shop_cell(rows: list[dict], locator: str) -> str | None:
    """Resolve one ``row:N:field`` or ``row:N:field[i]`` against the retained rows."""

    _, ordinal, field_name = locator.split(":", 2)
    row = rows[int(ordinal)]
    if field_name.endswith("]") and "[" in field_name:
        name, index = field_name[:-1].split("[", 1)
        if name not in row:
            return None
        return str(row[name][int(index)])
    if field_name not in row:
        return None
    return str(row[field_name])


def load_shop(private: Path = PRIVATE) -> Population:
    """The honest Table 1 population, through the connected story's own adapter."""

    from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (  # noqa: PLC0415
        run as story,
    )

    workspace = private / "shop"
    shutil.rmtree(workspace, ignore_errors=True)
    (workspace / "ledger").mkdir(parents=True)
    replay = story.run_story(workspace / "ledger/history.jsonl")
    source_rows = [
        json.loads(line)
        for line in replay.retained_bytes(story.SOURCE_ID).decode().splitlines()
        if line.strip()
    ]
    rows: list[tuple[str, tuple[str, ...], str]] = []
    for member in replay.retained_inputs:
        if not member.record_id.startswith("plan:") or member.record_id.endswith(
            ":gaps"
        ):
            continue
        for item in json.loads(replay.retained_bytes(member.record_id))["derivations"]:
            rows.append(
                (
                    str(item["record_id"]),
                    tuple(str(step) for step in item["path"]),
                    str(item["locator"]),
                )
            )
    records = {}
    for family, exported in sorted(replay.graph.export_records().items()):
        for record in exported:
            records[str(record["id"])] = Record(
                record_id=str(record["id"]),
                record_type=str(record["type"]),
                properties=dict(record.get("properties", {})),
                cited=None,
            )
    texts = {}
    for _, _, locator in rows:
        cell = _shop_cell(source_rows, locator)
        if cell is not None:
            texts[locator] = cell
    by_record, by_slot = _index(rows)
    return Population(
        name="shop-table-1",
        workspace=workspace,
        view=story.compile_shop().view,
        ontology_hash=story.compile_shop().view.content_hash(),
        records=records,
        texts=texts,
        derivation_rows=rows,
        record_level_citation=False,
        by_record=by_record,
        by_slot=by_slot,
    )


# ---------------------------------------------------------------------------
# What the compiled ontology declares
# ---------------------------------------------------------------------------


def _slots(population: Population, type_name: str) -> dict[str, str]:
    try:
        declared = population.view.effective_slots(type_name)
    except (KeyError, ValueError):
        return {}
    return {
        slot.rsplit("/", 1)[-1]: constraint.range_id.rsplit("/", 1)[-1]
        for slot, constraint in declared.items()
    }


def declared_range(population: Population, type_name: str, slot: str) -> str | None:
    return _slots(population, type_name).get(slot)


def declared_anywhere(population: Population, slot: str) -> bool:
    return any(
        slot in _slots(population, record.record_type)
        for record in population.records.values()
    )


def numeric_slots(population: Population) -> set[str]:
    """Every slot the compiled contract declares Float or Integer on a live type.

    Derived from the contract, never from a hand-written list. ``id`` is not a
    property fact and relation endpoints are not properties, so neither appears.
    """

    found = set()
    for record in population.records.values():
        for slot, range_name in _slots(population, record.record_type).items():
            if range_name in NUMERIC_RANGES:
                found.add(slot)
    return found


# ---------------------------------------------------------------------------
# Refusal rows
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Refusal:
    candidate: str
    population: str
    record_id: str
    record_type: str
    slot: str
    scope: str | None = None
    reading: str | None = None
    mechanism: str | None = None
    clause: str | None = None
    record_ids: tuple[str, ...] = ()


def _scope_texts(population: Population, record: Record, slot: str, scope: str):
    if scope == DERIVED:
        locators = population.by_record.get(record.record_id, ())
    elif population.record_level_citation:
        locators = (record.cited,) if record.cited else ()
    else:
        locators = population.by_slot.get((record.record_id, slot), ())
    return [
        population.texts[locator] for locator in locators if locator in population.texts
    ]


def _in_reach(population: Population, slot: str):
    """Records that set the slot and have a narrow-scope text to compare against."""

    for record in sorted(population.records.values(), key=lambda item: item.record_id):
        if slot not in record.properties or record.properties[slot] is None:
            continue
        if slot not in _slots(population, record.record_type):
            continue
        if population.record_level_citation and not record.cited:
            continue
        if not population.record_level_citation and not population.by_slot.get(
            (record.record_id, slot)
        ):
            continue
        yield record


# ---------------------------------------------------------------------------
# (a) NO_CONFLICTING_QUANTITY
# ---------------------------------------------------------------------------


def _quantity_groups(population: Population, qualifiers, families):
    groups: dict[tuple, dict[tuple, set[str]]] = {}
    for record in population.records.values():
        declared = _slots(population, record.record_type)
        subject = record.properties.get("subject")
        if "subject" in declared and subject is None:
            continue
        if "subject" not in declared and population.record_level_citation:
            continue
        for label, identity, values in families:
            if any(record.properties.get(slot) is None for slot in identity):
                continue
            if all(record.properties.get(slot) is None for slot in values):
                continue
            key = (
                subject,
                label,
                tuple(record.properties.get(slot) for slot in identity),
                tuple(record.properties.get(slot) for slot in qualifiers),
            )
            value = tuple(record.properties.get(slot) for slot in values)
            groups.setdefault(key, {}).setdefault(value, set()).add(record.record_id)
    return groups


def conflicting_quantity(
    population: Population, *, with_modality: bool
) -> list[Refusal]:
    """Two current records stating a different value for the same quantity."""

    if population.record_level_citation:
        families = QUANTITY_FAMILIES
    elif declared_anywhere(population, "quantity_kind"):
        families = QUANTITY_FAMILIES
    else:
        return []
    qualifiers = QUALIFIERS + ((ADDED_QUALIFIER,) if with_modality else ())
    groups = _quantity_groups(population, qualifiers, families)
    refusals = []
    for key, values in sorted(groups.items(), key=lambda item: str(item[0])):
        if len(values) < 2:
            continue
        witnesses = tuple(sorted({item for group in values.values() for item in group}))
        refusals.append(
            Refusal(
                candidate="NO_CONFLICTING_QUANTITY",
                population=population.name,
                record_id=witnesses[0],
                record_type=population.records[witnesses[0]].record_type,
                slot=str(key[1]),
                mechanism="QUANTITY_DISAGREEMENT",
                record_ids=witnesses,
            )
        )
    return refusals


def shop_own_conflict_keying(population: Population) -> list[Refusal]:
    """The Shop's already-shipped keying, measured and labelled as its own rule."""

    groups = _quantity_groups(population, (), (SHOP_CONFLICT_FAMILY,))
    refusals = []
    for key, values in sorted(groups.items(), key=lambda item: str(item[0])):
        if len(values) < 2:
            continue
        witnesses = tuple(sorted({item for group in values.values() for item in group}))
        refusals.append(
            Refusal(
                candidate="SHOP_OWN_CONFLICT_KEYING",
                population=population.name,
                record_id=witnesses[0],
                record_type=population.records[witnesses[0]].record_type,
                slot=str(key[1]),
                mechanism="QUANTITY_DISAGREEMENT",
                record_ids=witnesses,
            )
        )
    return refusals


# ---------------------------------------------------------------------------
# (b) INTERVAL_SANITY
# ---------------------------------------------------------------------------


def _decimal(value):
    try:
        return normalise.as_decimal(value)
    except TypeError:
        return None


def interval_sanity(population: Population) -> list[Refusal]:
    """Typed, internal to one record, no text read."""

    refusals = []
    for record in sorted(population.records.values(), key=lambda item: item.record_id):
        declared = _slots(population, record.record_type)
        held = {
            slot: _decimal(record.properties[slot])
            for slot in (
                "value_lower",
                "value_upper",
                "uncertainty",
                "count",
                "ratio_value",
            )
            if slot in declared and record.properties.get(slot) is not None
        }
        broken = []
        lower, upper = held.get("value_lower"), held.get("value_upper")
        if lower is not None and upper is not None and lower > upper:
            broken.append(("value_lower<=value_upper", "value_lower"))
        for slot, clause in (
            ("uncertainty", "uncertainty>=0"),
            ("count", "count>=0"),
            ("ratio_value", "ratio_value>=0"),
        ):
            if held.get(slot) is not None and held[slot] < 0:
                broken.append((clause, slot))
        for clause, slot in broken:
            refusals.append(
                Refusal(
                    candidate="INTERVAL_SANITY",
                    population=population.name,
                    record_id=record.record_id,
                    record_type=record.record_type,
                    slot=slot,
                    clause=clause,
                    mechanism="TYPED_INTERNAL",
                )
            )
    return refusals


def shop_non_negative_quantity(population: Population) -> list[Refusal]:
    refusals = []
    for record in sorted(population.records.values(), key=lambda item: item.record_id):
        if "ordered_quantity" not in _slots(population, record.record_type):
            continue
        value = _decimal(record.properties.get("ordered_quantity"))
        if value is not None and value < 0:
            refusals.append(
                Refusal(
                    candidate="SHOP_NON_NEGATIVE_QUANTITY",
                    population=population.name,
                    record_id=record.record_id,
                    record_type=record.record_type,
                    slot="ordered_quantity",
                    clause=SHOP_NON_NEGATIVE,
                    mechanism="TYPED_INTERNAL",
                )
            )
    return refusals


def with_planted_bounds(
    population: Population, lower_slot: str, lower: float, upper_slot: str, upper: float
) -> Population:
    """One deliberately inverted interval, so the clause is shown not to be vacuous."""

    for record in sorted(population.records.values(), key=lambda item: item.record_id):
        declared = _slots(population, record.record_type)
        if lower_slot in declared and upper_slot in declared:
            planted = dict(record.properties)
            planted[lower_slot] = lower
            planted[upper_slot] = upper
            records = dict(population.records)
            records[record.record_id] = replace(record, properties=planted)
            return replace(population, records=records)
    raise ValueError(f"no type declares both {lower_slot} and {upper_slot}")


# ---------------------------------------------------------------------------
# (c) NUMBER_IN_CITED_TEXT
# ---------------------------------------------------------------------------


def number_matches(value, text: str, reading) -> bool:
    _, profile, attached = reading
    return normalise.as_decimal(value) in normalise.numbers_in(
        text, profile=profile, attached=attached
    )


def _numbers_of(texts, reading) -> set[Decimal]:
    _, profile, attached = reading
    found: set[Decimal] = set()
    for text in texts:
        found |= normalise.numbers_in(text, profile=profile, attached=attached)
    return found


def number_in_text(
    population: Population, scope: str, reading, slots=None
) -> list[Refusal]:
    label = reading[0]
    everything = list(population.texts.values())
    refusals = []
    read = numeric_slots(population) if slots is None else set(slots)
    for slot in sorted(read):
        for record in _in_reach(population, slot):
            value = normalise.as_decimal(record.properties[slot])
            in_scope = _scope_texts(population, record, slot, scope)
            if value in _numbers_of(in_scope, reading):
                continue
            derived = _scope_texts(population, record, slot, DERIVED)
            others = [other for other in NUMBER_READINGS if other[0] != label]
            if any(value in _numbers_of(in_scope, other) for other in others):
                mechanism = "MATCHES_UNDER_ANOTHER_DECLARED_READING"
            elif scope == CITED and value in _numbers_of(derived, reading):
                mechanism = "IN_A_SENTENCE_THE_RECORD_DERIVES_FROM_NOT_THE_CITED_ONE"
            elif value in _numbers_of(everything, reading):
                mechanism = "IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE"
            else:
                mechanism = "IN_NO_RETAINED_SENTENCE"
            refusals.append(
                Refusal(
                    candidate="NUMBER_IN_CITED_TEXT",
                    population=population.name,
                    record_id=record.record_id,
                    record_type=record.record_type,
                    slot=slot,
                    scope=scope,
                    reading=label,
                    mechanism=mechanism,
                )
            )
    return refusals


# ---------------------------------------------------------------------------
# (d) UNIT_IN_SOURCE and (e) FORMULA_IN_SOURCE
# ---------------------------------------------------------------------------


def _string_candidate(
    population: Population, slots, candidate: str, scope: str, profile: str
) -> list[Refusal]:
    other = UNGLUED if profile == GLUED else GLUED
    everything = list(population.texts.values())
    refusals = []
    for slot in sorted(slots):
        for record in _in_reach(population, slot):
            value = str(record.properties[slot])
            in_scope = _scope_texts(population, record, slot, scope)
            if any(
                normalise.contains(value, text, profile=profile) for text in in_scope
            ):
                continue
            derived = _scope_texts(population, record, slot, DERIVED)
            if any(normalise.contains(value, text, profile=other) for text in in_scope):
                mechanism = "MATCHES_UNDER_THE_OTHER_PROFILE"
            elif scope == CITED and any(
                normalise.contains(value, text, profile=profile) for text in derived
            ):
                mechanism = "IN_A_SENTENCE_THE_RECORD_DERIVES_FROM_NOT_THE_CITED_ONE"
            elif any(
                normalise.contains(value, text, profile=profile) for text in everything
            ):
                mechanism = "IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE"
            else:
                mechanism = "IN_NO_RETAINED_SENTENCE"
            refusals.append(
                Refusal(
                    candidate=candidate,
                    population=population.name,
                    record_id=record.record_id,
                    record_type=record.record_type,
                    slot=slot,
                    scope=scope,
                    reading=profile,
                    mechanism=mechanism,
                )
            )
    return refusals


def unit_in_source(population: Population, scope: str, profile: str) -> list[Refusal]:
    return _string_candidate(population, UNIT_SLOTS, "UNIT_IN_SOURCE", scope, profile)


def formula_in_source(
    population: Population, scope: str, profile: str
) -> list[Refusal]:
    return _string_candidate(
        population, FORMULA_SLOTS, "FORMULA_IN_SOURCE", scope, profile
    )


# ---------------------------------------------------------------------------
# The census
# ---------------------------------------------------------------------------


def canonical(value) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def reach(population: Population, slots, *, cited_only: bool = True) -> dict[str, int]:
    """How many record-and-slot pairs a candidate actually reads.

    ``cited_only`` is the text-reading reach: a record with no narrow-scope text
    is out of reach of a rule that compares against one. Candidate (b) reads no
    text, so it passes ``cited_only=False`` and reaches every record that sets
    the slot.
    """

    declared = numeric_slots(population) if slots is None else set(slots)
    counts = {}
    for slot in sorted(declared):
        if cited_only:
            counts[slot] = len(list(_in_reach(population, slot)))
            continue
        counts[slot] = sum(
            1
            for record in population.records.values()
            if record.properties.get(slot) is not None
            and slot in _slots(population, record.record_type)
        )
    return counts


def measure(population: Population) -> dict[str, object]:
    """Every candidate, every scope, every reading. Nothing is applied."""

    result: dict[str, object] = {"population": population.name}
    result["records"] = len(population.records)
    result["derivations"] = len(population.derivation_rows)
    result["retained_texts"] = len(population.texts)
    result["ontology_hash"] = population.ontology_hash

    refusals: list[Refusal] = []
    conflict = {}
    for flag, label in (
        (False, "without_assertion_modality"),
        (True, "with_assertion_modality"),
    ):
        rows = conflicting_quantity(population, with_modality=flag)
        groups = _quantity_groups(
            population,
            QUALIFIERS + ((ADDED_QUALIFIER,) if flag else ()),
            QUANTITY_FAMILIES,
        )
        compared = {
            item
            for values in groups.values()
            for group in values.values()
            for item in group
        }
        conflict[label] = {
            "violations": len(rows),
            "records": sorted({item for row in rows for item in row.record_ids}),
            "records_compared": len(compared),
            "groups": len(groups),
            "groups_holding_more_than_one_record": sum(
                1
                for values in groups.values()
                if sum(len(group) for group in values.values()) > 1
            ),
        }
        if flag is False:
            refusals += rows
    result["a_no_conflicting_quantity"] = conflict

    interval = interval_sanity(population)
    result["b_interval_sanity"] = {
        "refusals": len(interval),
        "by_clause": dict(sorted(Counter(row.clause for row in interval).items())),
        "reach": reach(population, INTERVAL_SLOTS, cited_only=False),
    }
    refusals += interval

    numbers: dict[str, object] = {"reach": reach(population, None)}
    for scope in SCOPES:
        for reading in NUMBER_READINGS:
            rows = number_in_text(population, scope, reading)
            numbers[f"{scope}/{reading[0]}"] = {
                "refusals": len(rows),
                "records": len({row.record_id for row in rows}),
                "by_slot": dict(sorted(Counter(row.slot for row in rows).items())),
                "by_mechanism": dict(
                    sorted(Counter(row.mechanism for row in rows).items())
                ),
            }
            refusals += rows
    result["c_number_in_cited_text"] = numbers

    for key, candidate, slots, runner in (
        ("d_unit_in_source", "UNIT_IN_SOURCE", UNIT_SLOTS, unit_in_source),
        ("e_formula_in_source", "FORMULA_IN_SOURCE", FORMULA_SLOTS, formula_in_source),
    ):
        block: dict[str, object] = {"reach": reach(population, slots)}
        for scope in SCOPES:
            for profile in normalise.PROFILES:
                rows = runner(population, scope, profile)
                block[f"{scope}/{profile}"] = {
                    "refusals": len(rows),
                    "records": len({row.record_id for row in rows}),
                    "by_slot": dict(sorted(Counter(row.slot for row in rows).items())),
                    "by_mechanism": dict(
                        sorted(Counter(row.mechanism for row in rows).items())
                    ),
                }
                refusals += rows
        result[key] = block

    if not population.record_level_citation:
        shop_conflict = shop_own_conflict_keying(population)
        result["shop_own_conflict_keying"] = {
            "violations": len(shop_conflict),
            "records": sorted(
                {item for row in shop_conflict for item in row.record_ids}
            ),
        }
        shop_sign = shop_non_negative_quantity(population)
        result["shop_non_negative_quantity"] = {"refusals": len(shop_sign)}
        refusals += shop_conflict + shop_sign

    result["_refusals"] = refusals
    return result


# ---------------------------------------------------------------------------
# The classification, written after reading each record and its cited sentence
# ---------------------------------------------------------------------------

RULE_DEFECT = "RULE_DEFECT"
GRAPH_DEFECT = "GRAPH_DEFECT"
UNDECIDED = "UNDECIDED"

# Each entry matches on candidate, and optionally on record id, slot or
# mechanism. The first match wins; a refusal matching none stays UNDECIDED and
# RESULTS.md has to account for it.
CLASSIFICATION = (
    {
        "candidate": "NO_CONFLICTING_QUANTITY",
        "record_id": "obs:bdb-isotherm",
        "class": RULE_DEFECT,
        "reason": (
            "The two records report the same quantity of the same subject under two "
            "different assertion modalities, one stated and one hypothesised. The "
            "shipped qualifier list does not read assertion_modality, so the rule "
            "compares a hypothesis the source goes on to weigh against a convention "
            "the source states. Adding that qualifier removes the refusal."
        ),
    },
    {
        "candidate": "NUMBER_IN_CITED_TEXT",
        "record_id": "obs:velocity-perturbation",
        "slot": "value_lower",
        "class": RULE_DEFECT,
        "reason": (
            "The record carries a symmetric perturbation as a negative lower bound "
            "and a positive upper bound. The cited sentence states it once, as a "
            "bare plus-or-minus with no left operand. The declared grammar reads "
            "'a plus-or-minus b' and produces a, b, a-b and a+b; it produces no "
            "negative end from a bare plus-or-minus, so the lower bound is "
            "unreachable. The record and its citation are right and the grammar is "
            "short one production."
        ),
    },
    {
        "candidate": "UNIT_IN_SOURCE",
        "record_id": "obs:profile-halfwidth",
        "slot": "unit",
        "class": RULE_DEFECT,
        "reason": (
            "The cited block is a figure caption whose text layer sets a long run of "
            "it one character at a time, so the two letters of the unit are not "
            "adjacent in the retained bytes. The declared normalisation closes "
            "letter-to-digit spacing and hyphen breaks; it does not close spacing "
            "inside a word, and widening it to do so would join unrelated words. "
            "The record is right about the unit the source states."
        ),
    },
    {
        "candidate": "FORMULA_IN_SOURCE",
        "mechanism": "MATCHES_UNDER_THE_OTHER_PROFILE",
        "class": RULE_DEFECT,
        "reason": (
            "The record carries a chemical formula and the reading's text layer "
            "separates the subscript from the element with a space. The UNGLUED "
            "profile does not close that space, so the value is refused; the same "
            "value matches under GLUED. The defect is in the profile, not the record."
        ),
    },
    {
        "candidate": "NUMBER_IN_CITED_TEXT",
        "mechanism": "MATCHES_UNDER_ANOTHER_DECLARED_READING",
        "class": RULE_DEFECT,
        "reason": (
            "The GLUED_FREE reading welds the number onto the word before it, so no "
            "free-standing number is left to parse. The same value matches under "
            "both other declared readings. This is the degeneracy README.md predicted "
            "when the string normalisation is applied to numeric parsing."
        ),
    },
)


def classify(row: Refusal) -> tuple[str, str]:
    """One class and one line of reason per refusal, by the declared table."""

    for entry in CLASSIFICATION:
        if entry["candidate"] != row.candidate:
            continue
        if "record_id" in entry and entry["record_id"] not in (
            (row.record_id,) + tuple(row.record_ids)
        ):
            continue
        if "slot" in entry and entry["slot"] != row.slot:
            continue
        if "mechanism" in entry and entry["mechanism"] != row.mechanism:
            continue
        return entry["class"], entry["reason"]
    return (
        UNDECIDED,
        "no entry of the declared classification table matches this refusal",
    )


def detail(population: Population, refusals: list[Refusal]) -> list[dict]:
    """The private file: the same rows with the value and the text beside them."""

    rows = []
    for item in refusals:
        record = population.records[item.record_id]
        scope = item.scope or CITED
        classification, reason = classify(item)
        rows.append(
            {
                "class": classification,
                "reason": reason,
                "candidate": item.candidate,
                "record_id": item.record_id,
                "record_type": item.record_type,
                "slot": item.slot,
                "scope": item.scope,
                "reading": item.reading,
                "clause": item.clause,
                "mechanism": item.mechanism,
                "record_ids": list(item.record_ids),
                "value": record.properties.get(item.slot),
                "cited_locator": record.cited,
                "cited_text": _scope_texts(population, record, item.slot, CITED),
                "derived_text": _scope_texts(population, record, item.slot, scope)
                if item.scope == DERIVED
                else [],
                "properties": record.properties,
            }
        )
    return rows


def public(refusals: list[Refusal]) -> list[dict]:
    rows = []
    for item in refusals:
        rows.append(
            {
                "candidate": item.candidate,
                "population": item.population,
                "record_id": item.record_id,
                "record_type": item.record_type,
                "slot": item.slot,
                "scope": item.scope,
                "reading": item.reading,
                "clause": item.clause,
                "mechanism": item.mechanism,
                "record_ids": list(item.record_ids),
                "class": classify(item)[0],
            }
        )
    return rows


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private", type=Path, default=PRIVATE)
    arguments = parser.parse_args(argv)
    private = arguments.private.resolve()
    if not private_is_ignored(private):
        raise SystemExit(f"refusing to write an unignored private directory: {private}")
    private.mkdir(parents=True, exist_ok=True)

    outcomes: dict[str, object] = {
        "schema": OUTCOME_SCHEMA,
        "core_commit": CORE_COMMIT,
        "populations": {},
        "refusals": [],
    }
    for loader in (load_document, load_shop):
        population = loader(private)
        measured = measure(population)
        refusals = measured.pop("_refusals")
        (private / f"{population.name}-detail.json").write_bytes(
            canonical(detail(population, refusals))
        )
        outcomes["populations"][population.name] = measured
        outcomes["refusals"] += public(refusals)
        print(population.name, "refusal rows", len(refusals), flush=True)

    (HERE / "outcomes.json").write_bytes(
        json.dumps(outcomes, ensure_ascii=False, indent=1, sort_keys=True).encode(
            "utf-8"
        )
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
