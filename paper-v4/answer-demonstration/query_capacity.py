"""Schema-only spelling/shape audit for one frozen reader, not semantic QA."""

import json

from binding import QUESTION_IDENTITY
from review_packet import digest

PROGRAM_IDENTITY = (
    "sha256:5d977130df337a72faf76f847354f1096e0a48d5919e61d7947add1ae57a779e"
)
NUMERIC = ("value_lower", "value_upper", "count", "ratio_value", "uncertainty")
TEXT = ("name", "description", "statement", "quantity_kind", "count_scope")
RANGE = "https://malleus.dev/contract-facts/"

# Each tuple is (exact node types, any scalar field group, predicates, direction,
# disposition/dimension enum). These are reader dependencies, not answer needs.
RULES = {
    "CQ-T1-01": (
        ("Campaign",),
        (),
        ("PART_OF_CAMPAIGN", "OBSERVED_WITH"),
        "either",
        None,
    ),
    "CQ-T1-02": ((), ("count",), (), None, None),
    "CQ-T1-03": ((), ("accepted_date",), (), None, None),
    "CQ-T1-04": (
        (),
        ("locator", "access_url", "doi"),
        ("DEPOSITED_IN", "REPORTED_BY"),
        "either",
        None,
    ),
    "CQ-T1-05": (
        ("Instrument",),
        ("duration", "value_lower", "value_upper"),
        ("OBSERVED_WITH",),
        "out",
        None,
    ),
    "CQ-T2-01": ((), (), ("BOUNDED_BY",), "in", None),
    "CQ-T2-02": ((), (), ("PRECEDES", "FOLLOWED_BY", "APPLIED_AFTER"), "either", None),
    "CQ-T2-03": (
        (),
        (),
        ("LOCATED_IN", "LOCATED_BENEATH", "PART_OF", "ADJACENT_TO"),
        "either",
        None,
    ),
    "CQ-T2-04": (
        (),
        NUMERIC,
        ("REPORTED_BY", "DERIVED_FROM", "LOCATED_IN"),
        "either",
        None,
    ),
    "CQ-T2-05": ((), ("award_identifier",), (), None, None),
    "CQ-T3-01": (
        (),
        ("value_lower", "value_upper"),
        (),
        None,
        ("quantity_kind_class", "Length"),
    ),
    "CQ-T3-02": ((), NUMERIC, (), None, None),
    "CQ-T3-03": ((), NUMERIC, (), None, None),
    "CQ-T3-04": ((), NUMERIC, (), None, None),
    "CQ-T3-05": ((), NUMERIC, (), None, None),
    "CQ-T4-01": ((), (), (), None, ("hypothesis_disposition", "PREFERRED")),
    "CQ-T4-02": ((), (), (), None, ("hypothesis_disposition", "NOT_SUPPORTED")),
    "CQ-T4-03": ((), (), (), None, None),
    "CQ-T4-04": ((), (), (), None, None),
    "CQ-T4-05": ((), (), (), None, None),
    "CQ-T5-01": ((), (), ("SUPPORTS",), "in", ("hypothesis_disposition", "PREFERRED")),
    "CQ-T5-02": ((), NUMERIC, (), None, None),
    "CQ-T5-03": ((), NUMERIC, (), None, None),
    "CQ-T5-04": ((), (), (), None, None),
    "CQ-T5-05": ((), (), ("CHALLENGES", "SUPPORTS"), "in", None),
    "CQ-C-01": ((), NUMERIC, (), None, None),
    "CQ-C-02": ((), NUMERIC, (), None, None),
    "CQ-C-03": ((), NUMERIC, (), None, None),
    "CQ-C-04": ((), ("count",), (), None, None),
    "CQ-C-05": ((), NUMERIC, (), None, None),
}
NO_TEXT = {"CQ-T1-01", "CQ-T1-03", "CQ-T2-05", "CQ-T4-01", "CQ-T4-02", "CQ-T5-01"}


def audit(surface, program_source, question_source):
    if (
        digest(program_source) != PROGRAM_IDENTITY
        or digest(question_source) != QUESTION_IDENTITY
    ):
        raise ValueError(
            "capacity audit requires the exact frozen reader and questions"
        )
    types, slots, ignored = {}, [], []
    for record in surface["record_types"]:
        name, family = record["name"], record["family"]
        if name in types or family not in {
            "ENTITY",
            "EVENT",
            "SIGNAL",
            "RELATION",
            "EVENT_PARTICIPATION",
        }:
            raise ValueError(f"invalid or duplicate surface type: {name}")
        types[name] = family
        names = set()
        for slot in record["slots"]:
            key = slot["name"]
            if key in names:
                raise ValueError(f"duplicate slot: {name}.{key}")
            names.add(key)
            if (
                type(slot["multivalued"]) is not bool
                or type(slot["identifier"]) is not bool
            ):
                raise ValueError(f"invalid slot flags: {name}.{key}")
            slots.append((name, family, slot))
            if (
                family != "RELATION"
                and slot["range_id"] == RANGE + "String"
                and not slot["identifier"]
                and key not in TEXT
            ):
                ignored.append(f"{name}.{key}")

    def available(fields, family_relation=False):
        matches = []
        for name, family, s in slots:
            if (
                (family == "RELATION") != family_relation
                or s["name"] not in fields
                or s["multivalued"]
            ):
                continue
            key, kind = s["name"], s["range_id"]
            if key in NUMERIC and kind not in {RANGE + "Integer", RANGE + "Float"}:
                continue
            if key == "count" and kind != RANGE + "Integer":
                continue
            matches.append(f"{name}.{key}")
        return sorted(matches)

    def enum_present(key, values, relation=False):
        return sorted(
            {
                value
                for _, family, s in slots
                if (family == "RELATION") == relation
                and s["name"] == key
                and not s["multivalued"]
                and "enum_values" in s
                for value in s["enum_values"]
                if value in values
            }
        )

    questions = json.loads(question_source)["questions"]
    if len(questions) != len(RULES) or {q["id"] for q in questions} != set(RULES):
        raise ValueError("capacity rules must cover all frozen questions")
    rows = []
    for q in questions:
        qid = q["id"]
        exact, fields, predicates, direction, enum = RULES[qid]
        missing = [
            "exact node type: " + name
            for name in exact
            if name not in types or types[name] == "RELATION"
        ]
        matched = available(fields, qid == "CQ-T2-05")
        if fields and not matched:
            missing.append("scalar field, any of: " + ", ".join(fields))
        meanings = enum_present("relation_type", predicates, relation=True)
        if predicates and not meanings:
            missing.append("relation predicate, any of: " + ", ".join(predicates))
        if enum and not enum_present(enum[0], (enum[1],)):
            missing.append("enum value: " + ".".join(enum))
        if qid not in NO_TEXT and not available(TEXT) and not available(("subject",)):
            missing.append("searchable local text or explicit subject reference")
        rows.append(
            {
                "question_id": qid,
                "status": "DECLARATION_GAP" if missing else "DECLARED_SHAPES_PRESENT",
                "missing_declarations": missing,
                "scalar_field_candidates": matched,
                "available_predicates": meanings,
                "reader_direction": direction,
                "exact_node_types": list(exact),
            }
        )
    return {
        "schema": "malleus.paper-v4.reader-declaration-audit/v1",
        "query_program_sha256": digest(program_source),
        "question_set_sha256": digest(question_source),
        "questions": rows,
        "text_slots_not_searched_locally": sorted(ignored),
        "limit": "Declaration shapes only, not semantic compatibility, matching population, source truth or coverage. No aliases, subclass expansion or data inspection. Subject matching reads name/description/tags one hop; local matching uses only the frozen text slots. Relation endpoint restrictions and co-location of all needed fields can further limit answers.",
    }
