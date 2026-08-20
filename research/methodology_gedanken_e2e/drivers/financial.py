"""Toy 2 — the financial recommendation. Provenance shape, and self-reported order.

Three graphs from GEDANKEN.md:153-203, plus one variant that exists only to be
run: B2 with its timestamps edited to lie. The lie changes nothing about which
records exist or how they are linked, and the rule that caught B2 goes silent.
That silent pass is the point of the toy.
"""

from __future__ import annotations

from malleus.staging import ProposedOperation as Op

try:
    from drivers.common import check, findings, report
except ImportError:  # direct execution
    from common import check, findings, report

TOY = "financial"


def _derived(edge_id: str, source: str, target: str) -> Op:
    return Op.relation(
        "DerivedFromRelation", edge_id, source, target, {"relation_type": "DERIVED_FROM"}
    )


def _about(edge_id: str, source: str) -> Op:
    return Op.relation("AboutRelation", edge_id, source, "acme", {"relation_type": "ABOUT"})


def graph_a_writes() -> list[Op]:
    """GEDANKEN.md:157-167. Every stage present, timestamps running forward."""
    return [
        Op.entity("Company", "acme", {"name": "Acme"}),
        Op.entity("Metric", "m1", {"metric_name": "revenue_growth", "period": "2025"}),
        Op.entity("Metric", "m2", {"metric_name": "gross_margin", "period": "2025"}),
        Op.entity("Metric", "m3", {"metric_name": "client_concentration"}),
        Op.entity("Peer", "beta", {"name": "Beta"}),
        Op.entity("Peer", "gamma", {"name": "Gamma"}),
        Op.entity("Observation", "o1", {"asserted_at": "2026-02-10", "statement": "growth 34%"}),
        Op.entity("Observation", "o2", {"asserted_at": "2026-02-10", "statement": "margin 61%"}),
        Op.entity(
            "Observation",
            "o3",
            {"asserted_at": "2026-02-12", "statement": "top client 41% of revenue"},
        ),
        Op.entity(
            "Comparison",
            "x1",
            {"asserted_at": "2026-02-11", "statement": "growth above peer median 12%"},
        ),
        Op.entity(
            "RiskAssessment",
            "k1",
            {"asserted_at": "2026-02-12", "statement": "customer concentration high"},
        ),
        Op.entity("Recommendation", "rec1", {"asserted_at": "2026-02-13", "stance": "BUY"}),
        _derived("d1", "o1", "m1"),
        _derived("d2", "o2", "m2"),
        _derived("d3", "o3", "m3"),
        _derived("d4", "x1", "o1"),
        _derived("d5", "x1", "beta"),
        _derived("d6", "x1", "gamma"),
        _derived("d7", "k1", "o3"),
        _derived("d8", "rec1", "x1"),
        _derived("d9", "rec1", "k1"),
        _about("a1", "o1"),
        _about("a2", "o2"),
        _about("a3", "o3"),
        _about("a4", "x1"),
        _about("a5", "k1"),
        _about("a6", "rec1"),
    ]


def graph_b1_writes() -> list[Op]:
    """GEDANKEN.md:177-179. Evidence straight to conclusion, no middle stages."""
    return [
        Op.entity("Company", "acme", {"name": "Acme"}),
        Op.entity("Metric", "m1", {"metric_name": "revenue_growth", "period": "2025"}),
        Op.entity("Observation", "o1", {"asserted_at": "2026-02-10", "statement": "growth 34%"}),
        Op.entity("Recommendation", "rec2", {"asserted_at": "2026-02-09", "stance": "BUY"}),
        _derived("d1", "o1", "m1"),
        _derived("d2", "rec2", "o1"),
        _about("a1", "o1"),
        _about("a2", "rec2"),
    ]


def graph_b2_writes(risk_asserted_at: str = "2026-02-14") -> list[Op]:
    """GEDANKEN.md:181-183. Right shape, wrong order.

    `risk_asserted_at` is the only knob. Every record, every type and every
    edge is fixed; only the string the writer supplies for when they say they
    assessed the risk moves.
    """
    return [
        Op.entity("Company", "acme", {"name": "Acme"}),
        Op.entity("Metric", "m1", {"metric_name": "revenue_growth", "period": "2025"}),
        Op.entity("Metric", "m3", {"metric_name": "client_concentration"}),
        Op.entity("Peer", "beta", {"name": "Beta"}),
        Op.entity("Peer", "gamma", {"name": "Gamma"}),
        Op.entity("Observation", "o1", {"asserted_at": "2026-02-10", "statement": "growth 34%"}),
        Op.entity(
            "Observation",
            "o3",
            {"asserted_at": "2026-02-12", "statement": "top client 41% of revenue"},
        ),
        Op.entity(
            "Comparison",
            "x2",
            {"asserted_at": "2026-02-11", "statement": "growth above peer median 12%"},
        ),
        Op.entity(
            "RiskAssessment",
            "k3",
            {"asserted_at": risk_asserted_at, "statement": "customer concentration high"},
        ),
        Op.entity("Recommendation", "rec3", {"asserted_at": "2026-02-13", "stance": "BUY"}),
        _derived("d1", "o1", "m1"),
        _derived("d2", "o3", "m3"),
        _derived("d3", "x2", "o1"),
        _derived("d4", "x2", "beta"),
        _derived("d5", "x2", "gamma"),
        _derived("d6", "k3", "o3"),
        _derived("d7", "rec3", "x2"),
        _derived("d8", "rec3", "k3"),
        _about("a1", "o1"),
        _about("a2", "o3"),
        _about("a3", "x2"),
        _about("a4", "k3"),
        _about("a5", "rec3"),
    ]


def self_report_trap() -> tuple[tuple, tuple, bool]:
    """Run B2 honest and B2 lying, and compare what the rules saw.

    Returns the honest verdict, the lying verdict, and whether the two graphs
    are structurally identical: same records, same types, same edges.
    """
    honest = check(TOY, graph_b2_writes("2026-02-14"))
    lying = check(TOY, graph_b2_writes("2026-02-12"))
    same_shape = honest.translated_record_ids == lying.translated_record_ids
    return findings(honest), findings(lying), same_shape


def main() -> None:
    report("toy 2, graph A (sound)", check(TOY, graph_a_writes()))
    report("toy 2, graph B1 (missing stage)", check(TOY, graph_b1_writes()))
    report("toy 2, graph B2 (post-hoc, honest timestamps)", check(TOY, graph_b2_writes()))
    report(
        "toy 2, graph B2' (post-hoc, timestamp edited to lie)",
        check(TOY, graph_b2_writes("2026-02-12")),
    )
    honest, lying, same_shape = self_report_trap()
    print("\n--- the self-report trap ---")
    print(f"same record set in both graphs : {same_shape}")
    print(f"honest B2 violations           : {honest}")
    print(f"lying  B2 violations           : {lying}")
    print(
        "the only edit was k3.asserted_at, 2026-02-14 -> 2026-02-12; "
        "no record, type or edge changed"
    )


if __name__ == "__main__":
    main()
