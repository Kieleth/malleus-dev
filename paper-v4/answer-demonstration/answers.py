"""Exploratory, deterministic question-specific reads. No extraction or grading.

These programs consume only the public graph read interface and its population
surface. A candidate is not a supported answer. Review makes that judgment.
There is deliberately no general query grammar, source reader or LLM fallback.
"""

from dataclasses import dataclass, field
import re
import unicodedata


TEXT_FIELDS = ("name", "description", "statement", "quantity_kind", "count_scope")
HOUSEKEEPING = {"id", "type", "created_at", "updated_at", "is_event", "is_signal"}
NUMERIC_FIELDS = ("value_lower", "value_upper", "count", "ratio_value", "uncertainty")
INSTRUMENT = ("ocean bottom seismometer", "ocean bottom seismometers", "obs", "obss")
CARBON_DIOXIDE = ("carbon dioxide", "co2", "co 2")


class QueryNotExpressible(ValueError):
    """The accepted surface does not expose a concept used by this program."""


def normal(text):
    return " ".join(re.findall(r"\w+", unicodedata.normalize("NFKC", text).casefold()))


def contains(text, phrase):
    needle = f" {normal(phrase)} "
    if needle in f" {normal(text)} ":
        return True
    # A line-end hyphen may split a word. Keep the ordinary compound reading
    # above as well; this is candidate matching, never a rewrite of graph data.
    joined = re.sub(r"(?<=\w)-[ \t]*\r?\n[ \t]*(?=\w)", "", text)
    return needle in f" {normal(joined)} "


def text_of(node):
    return " ".join(
        node[key] for key in TEXT_FIELDS if key in node and isinstance(node[key], str)
    )


@dataclass
class Selection:
    nodes: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    paths: list = field(default_factory=list)
    note: str = "Candidate fields require source-grounded review."


class GraphReads:
    def __init__(self, graph, surface):
        self.graph = graph
        self.types = {}
        for item in surface["record_types"]:
            name = item["name"]
            if item["family"] not in {
                "ENTITY",
                "EVENT",
                "RELATION",
                "SIGNAL",
                "EVENT_PARTICIPATION",
            }:
                raise ValueError(f"unknown surface family for {name}")
            for slot in item["slots"]:
                if not isinstance(slot["name"], str) or not slot["name"]:
                    raise ValueError(f"invalid slot name for {name}")
            if name in self.types:
                raise ValueError(f"duplicate surface type: {name}")
            self.types[name] = item

    def nodes(self):
        nodes = {}
        for name, item in self.types.items():
            if item["family"] != "RELATION":
                for node in self.graph.query(entity_type=name):
                    nodes[node["id"]] = node
        return [nodes[key] for key in sorted(nodes)]

    def typed(self, name):
        if name not in self.types:
            raise QueryNotExpressible(f"surface has no {name} type")
        return self.graph.query(entity_type=name)

    def matching(self, *groups, nodes=None):
        candidates = self.nodes() if nodes is None else nodes
        return [
            node
            for node in candidates
            if all(
                any(contains(text_of(node), term) for term in group) for group in groups
            )
        ]

    def quantified(self, *groups, fields=NUMERIC_FIELDS):
        return [
            node
            for node in self.matching(*groups)
            if any(key in node and type(node[key]) in (int, float) for key in fields)
        ]

    def with_fields(self, *fields):
        return [node for node in self.nodes() if any(key in node for key in fields)]

    def preferred(self):
        return [
            node
            for node in self.nodes()
            if "hypothesis_disposition" in node
            and node["hypothesis_disposition"] == "PREFERRED"
        ]

    def linked(self, nodes, predicates, *, direction="either"):
        declared = set()
        for item in self.types.values():
            if item["family"] == "RELATION":
                for slot in item["slots"]:
                    if slot["name"] == "relation_type" and "enum_values" in slot:
                        declared.update(slot["enum_values"])
        available = predicates & declared
        if not available:
            raise QueryNotExpressible(
                f"surface declares none of these relation meanings: {sorted(predicates)}"
            )
        selected = {node["id"] for node in nodes}
        edges, paths = [], []
        for edge in self.graph.query_relations():
            if edge["relation_type"] not in available:
                continue
            source, target = edge["source_id"], edge["target_id"]
            source_matches = source in selected and direction in {"out", "either"}
            target_matches = target in selected and direction in {"in", "either"}
            if source_matches or target_matches:
                edges.append(edge)
                paths.append([source, edge["key"], target])
        return Selection(
            nodes, edges, paths, "Only retained relation records establish these paths."
        )

    def row(self, node):
        fields = {
            slot["name"] for slot in self.types[node["type"]]["slots"]
        } - HOUSEKEEPING
        record = {key: node[key] for key in sorted(fields) if key in node}
        row = {
            "kind": "ENTITY",
            "record_type": node["type"],
            "record": record,
            "witness": {"record_id": node["id"]},
        }
        if "subject" in record:
            subject = self.graph.get_node(record["subject"])
            if subject is None:
                raise ValueError(
                    f"missing subject {record['subject']} for {node['id']}"
                )
            row["kind"] = "SUBJECT"
            row["subject"] = self.row_without_subject(subject)
            row["witness"]["subject_id"] = subject["id"]
        return row

    def row_without_subject(self, node):
        fields = {
            slot["name"] for slot in self.types[node["type"]]["slots"]
        } - HOUSEKEEPING
        return {key: node[key] for key in sorted(fields) if key in node}


def campaign(g):
    return g.linked(g.typed("Campaign"), {"PART_OF_CAMPAIGN", "OBSERVED_WITH"})


def instrument_count(g):
    # Local scope selects the count's role. Subject identity may identify the
    # instrument, but must not turn a subset into the deployed/network total.
    roles = (
        "deployed",
        "deployment",
        "in the network",
        "network total",
        "whole network",
        "entire network",
    )
    excluded = (
        "useful",
        "recovered",
        "operational",
        "subset",
        "minimum",
        "at least",
        "detecting",
        "detection",
        "not deployed",
        "undeployed",
    )
    return Selection(
        [
            node
            for node in g.matching(INSTRUMENT)
            if "count" in node
            and type(node["count"]) is int
            and any(contains(text_of(node), role) for role in roles)
            and not any(contains(text_of(node), term) for term in excluded)
        ],
        note="Explicit deployment or network-membership count candidates; original scope retained, no deployment event inferred. Named subsets and detection thresholds are excluded.",
    )


def accepted_date(g):
    return Selection(g.with_fields("accepted_date"))


def catalogue(g):
    nodes = g.matching(
        ("catalogue", "catalog", "picked arrivals", "arrival times"),
        nodes=g.with_fields("locator", "access_url", "doi"),
    )
    return g.linked(nodes, {"DEPOSITED_IN", "REPORTED_BY"})


def recording_duration(g):
    result = g.linked(
        g.matching(
            ("recording", "recorded", "seismic data"),
            nodes=g.with_fields("duration", "value_lower", "value_upper"),
        ),
        {"OBSERVED_WITH"},
        direction="out",
    )
    instruments = []
    for edge in result.edges:
        target = g.graph.get_node(edge["target_id"])
        if target is None:
            raise ValueError(f"missing instrument endpoint for {edge['key']}")
        if target["type"] == "Instrument":
            instruments.append(edge)
    result.edges = instruments
    result.paths = [[e["source_id"], e["key"], e["target_id"]] for e in instruments]
    result.note = "Stored recording durations and their explicit outgoing OBSERVED_WITH links to Instrument records. Original scope and qualifiers retained; no instrument or recording interval inferred."
    return result


def bounded_subsection(g):
    result = g.linked(g.matching(("detachment",)), {"BOUNDED_BY"}, direction="in")
    subsections = {edge["source_id"] for edge in result.edges}
    result.nodes = [
        node
        for node in g.matching(("detachment",), ("oceanic core complex",))
        if "subject" in node and node["subject"] in subsections
    ]
    result.note = "The bounding edge is explicit. Subject-linked wording may carry spatial qualifiers; no directional edge is inferred from prose."
    return result


def method_sequence(g):
    return g.linked(
        g.matching(("initial", "relocation", "relocate", "relocated")),
        {"PRECEDES", "FOLLOWED_BY", "APPLIED_AFTER"},
    )


def extinct_vent(g):
    return g.linked(
        g.matching(("vent", "hydrothermal"), ("extinct",)),
        {"LOCATED_IN", "LOCATED_BENEATH", "PART_OF", "ADJACENT_TO"},
    )


def crustal_thickness(g):
    return g.linked(
        g.quantified(("crust", "crustal"), ("thickness",)),
        {"REPORTED_BY", "DERIVED_FROM", "LOCATED_IN"},
    )


def funding(g):
    edges = [edge for edge in g.graph.query_relations() if "award_identifier" in edge]
    return Selection(
        edges=edges, paths=[[e["source_id"], e["key"], e["target_id"]] for e in edges]
    )


def earthquake_depth(g):
    return Selection(
        [
            node
            for node in g.quantified(
                (
                    "earthquake",
                    "earthquakes",
                    "events",
                    "seismicity",
                    "microseismicity",
                ),
                ("depth", "depths"),
                fields=("value_lower", "value_upper"),
            )
            if "quantity_kind_class" in node and node["quantity_kind_class"] == "Length"
        ],
        note="Only explicitly classified Length quantities with numeric bounds are candidates; missing dimensions are not inferred. Segment, axis, observational origin and reference-surface scope still require review.",
    )


def primary_carbon(g):
    return Selection(
        g.quantified(CARBON_DIOXIDE, ("primary melt", "primary melts")),
        note="All primary-melt quantities remain; no site alias or intended range is supplied.",
    )


def pre_eruptive_carbon(g):
    return Selection(g.quantified(CARBON_DIOXIDE, ("pre eruptive",)))


def horizontal_uncertainty(g):
    return Selection(g.quantified(("horizontal",), ("uncertainty", "error", "errors")))


def saturation_conditions(g):
    return Selection(
        g.quantified(("saturation", "saturated"), ("pressure", "temperature"))
    )


def preferred_mechanism(g):
    return Selection(
        g.preferred(),
        note="Preferred disposition is read, not inferred; the stored modality is unchanged.",
    )


def declined_mechanism(g):
    return Selection(
        [
            node
            for node in g.nodes()
            if "hypothesis_disposition" in node
            and node["hypothesis_disposition"] == "NOT_SUPPORTED"
        ],
        note="All explicitly declined candidates remain. The query does not resolve which involves the requested process or supply its missing grounds.",
    )


def concentration_caveat(g):
    return Selection(
        g.matching(
            CARBON_DIOXIDE,
            ("trace element", "trace elements"),
            ("assumption", "assume", "uncertainty", "caveat", "limitation"),
        )
    )


def active_vent(g):
    return Selection(g.matching(("hydrothermal", "vent", "venting"), ("active",)))


def long_period(g):
    return Selection(g.matching(("long period",)))


def mechanism_evidence(g):
    return g.linked(g.preferred(), {"SUPPORTS"}, direction="in")


def compare_carbon(g):
    result = primary_carbon(g)
    result.note = "Values are returned without inventing site ordering or pairing; the requested comparison requires explicit scope."
    return result


def depth_expectation(g):
    return Selection(
        g.quantified(("depth", "depths"), ("maximum", "expected", "spreading"))
    )


def location_categories(g):
    return Selection(
        g.matching(
            ("category", "categories"),
            ("location", "located", "earthquake", "earthquakes"),
        )
    )


def cold_lithosphere(g):
    nodes = g.matching(("lithosphere",), ("cold", "thick"))
    return g.linked(nodes, {"CHALLENGES", "SUPPORTS"}, direction="in")


def sulfur_chlorine(g):
    return Selection(g.quantified(("sulfur", "sulphur", "chlorine")))


def recurrence(g):
    return Selection(
        g.quantified(("recurrence",), ("earthquake", "earthquakes", "events"))
    )


def comparison_sites(g):
    return Selection(
        g.quantified(("spreading rate", "maximum depth", "maximum earthquake depth")),
        note="No plotted values are inferred; site pairing and excluded-surface scope require review.",
    )


PROGRAMS = {
    "CQ-T1-01": campaign,
    "CQ-T1-02": instrument_count,
    "CQ-T1-03": accepted_date,
    "CQ-T1-04": catalogue,
    "CQ-T1-05": recording_duration,
    "CQ-T2-01": bounded_subsection,
    "CQ-T2-02": method_sequence,
    "CQ-T2-03": extinct_vent,
    "CQ-T2-04": crustal_thickness,
    "CQ-T2-05": funding,
    "CQ-T3-01": earthquake_depth,
    "CQ-T3-02": primary_carbon,
    "CQ-T3-03": pre_eruptive_carbon,
    "CQ-T3-04": horizontal_uncertainty,
    "CQ-T3-05": saturation_conditions,
    "CQ-T4-01": preferred_mechanism,
    "CQ-T4-02": declined_mechanism,
    "CQ-T4-03": concentration_caveat,
    "CQ-T4-04": active_vent,
    "CQ-T4-05": long_period,
    "CQ-T5-01": mechanism_evidence,
    "CQ-T5-02": compare_carbon,
    "CQ-T5-03": depth_expectation,
    "CQ-T5-04": location_categories,
    "CQ-T5-05": cold_lithosphere,
    "CQ-C-01": sulfur_chlorine,
    "CQ-C-02": recurrence,
    "CQ-C-03": comparison_sites,
    "CQ-C-04": instrument_count,
    "CQ-C-05": primary_carbon,
}


def answer(reads, question_id):
    if question_id not in PROGRAMS:
        raise ValueError(f"unknown question: {question_id}")
    try:
        selection = PROGRAMS[question_id](reads)
    except QueryNotExpressible as error:
        return {
            "question_id": question_id,
            "outcome": "NOT_EXPRESSIBLE",
            "note": str(error),
            "rows": [],
            "paths": [],
            "witness_ids": [],
        }
    rows, witnesses = [], set()
    for node in sorted(
        {n["id"]: n for n in selection.nodes}.values(), key=lambda n: n["id"]
    ):
        row = reads.row(node)
        rows.append(row)
        witnesses.update(row["witness"].values())
    for edge in sorted(
        {e["key"]: e for e in selection.edges}.values(), key=lambda e: e["key"]
    ):
        source = reads.graph.get_node(edge["source_id"])
        target = reads.graph.get_node(edge["target_id"])
        if source is None or target is None:
            raise ValueError(f"missing relation endpoint for {edge['key']}")
        witness = {
            "relation_id": edge["key"],
            "source_id": source["id"],
            "target_id": target["id"],
        }
        row = {
            "kind": "RELATION",
            "record_type": edge["type"],
            "relation": {
                k: v
                for k, v in edge.items()
                if k not in HOUSEKEEPING | {"key", "source_id", "target_id"}
            },
            "witness": witness,
        }
        for role, node in (("source", source), ("target", target)):
            endpoint = reads.row(node)
            row[role] = endpoint["record"]
            if endpoint["kind"] == "SUBJECT":
                row[role + "_subject"] = endpoint["subject"]
                witness[role + "_subject_id"] = endpoint["witness"]["subject_id"]
        rows.append(row)
        witnesses.update(witness.values())
    return {
        "question_id": question_id,
        "program": PROGRAMS[question_id].__name__,
        "outcome": "CANDIDATES_FOR_REVIEW" if rows else "NO_CANDIDATE",
        "rows": rows,
        "paths": sorted(selection.paths),
        "witness_ids": sorted(witnesses),
        "note": selection.note,
    }
