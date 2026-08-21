"""Toy 3 — the diagnosis. Differential before conclusion.

Graphs C and D come from GEDANKEN.md:282-312. Graph C2 does not: it was added
because COMPETITOR_NOT_REFUTED cannot fire on either sketched graph, so without
it the second violation code is never observed to work.

`batch_writes()` collapses every `entered_at` in graph D to the turn of the
conclusion. It is the clinician who reverse-engineered the differential after
deciding, and it is here to be run rather than asserted.
"""

from __future__ import annotations

from malleus.staging import ProposedOperation as Op

try:
    from drivers.common import check, findings, report
except ImportError:  # direct execution
    from common import check, findings, report

TOY = "diagnosis"


def _presents(edge_id: str, finding: str) -> Op:
    return Op.relation("PresentsRelation", edge_id, "pt", finding, {"relation_type": "PRESENTS"})


def _explains(edge_id: str, hypothesis: str, finding: str) -> Op:
    return Op.relation(
        "ExplainsRelation", edge_id, hypothesis, finding, {"relation_type": "EXPLAINS"}
    )


def _discriminates(edge_id: str, order: str, hypothesis: str) -> Op:
    return Op.relation(
        "DiscriminatesRelation", edge_id, order, hypothesis, {"relation_type": "DISCRIMINATES"}
    )


def _bears_on(edge_id: str, result: str, hypothesis: str) -> Op:
    return Op.relation(
        "BearsOnRelation", edge_id, result, hypothesis, {"relation_type": "BEARS_ON"}
    )


def _concludes(edge_id: str, diagnosis: str, hypothesis: str) -> Op:
    return Op.relation(
        "ConcludesRelation", edge_id, diagnosis, hypothesis, {"relation_type": "CONCLUDES"}
    )


def _presentation() -> list[Op]:
    return [
        Op.entity("Patient", "pt", {"name": "patient"}),
        Op.entity("Finding", "f1", {"name": "chest pain"}),
        Op.entity("Finding", "f2", {"name": "dyspnoea"}),
        Op.entity("Finding", "f3", {"name": "raised troponin"}),
        _presents("pr1", "f1"),
        _presents("pr2", "f2"),
        _presents("pr3", "f3"),
    ]


def _mi_line(turn: dict[str, int]) -> list[Op]:
    """The one hypothesis every graph here shares, and its conclusion."""
    return [
        Op.entity("Hypothesis", "h1", {"name": "myocardial infarction", "entered_at": turn["h"]}),
        Op.entity("TestOrder", "t1", {"name": "ECG", "entered_at": turn["t"]}),
        Op.entity(
            "TestResult",
            "r1",
            {"name": "ST elevation", "verdict": "SUPPORTS", "entered_at": turn["r"]},
        ),
        Op.entity("Diagnosis", "dx1", {"name": "MI", "entered_at": turn["d"]}),
        _explains("e1", "h1", "f1"),
        _explains("e2", "h1", "f2"),
        _explains("e3", "h1", "f3"),
        _discriminates("s1", "t1", "h1"),
        _bears_on("b1", "r1", "h1"),
        _concludes("c1", "dx1", "h1"),
    ]


SKETCH_TURNS = {"h": 3, "t": 4, "r": 5, "d": 6}
BATCH_TURNS = {"h": 6, "t": 6, "r": 6, "d": 6}


def graph_c_writes() -> list[Op]:
    """GEDANKEN.md:284-292. Exactly one hypothesis was ever entered."""
    return [*_presentation(), *_mi_line(SKETCH_TURNS)]


def _competitors(turn: dict[str, int]) -> list[Op]:
    """Two rival hypotheses, each explaining every finding the winner explains.

    The sketch names the rivals and never says which findings they explain.
    SINGLE_HYPOTHESIS quantifies over every finding the concluded hypothesis
    explains, so partial coverage would leave graph D failing. Full coverage is
    also the clinical reading: PE and dissection both raise troponin.
    """
    return [
        Op.entity("Hypothesis", "h2", {"name": "pulmonary embolism", "entered_at": turn["h"]}),
        Op.entity("Hypothesis", "h3", {"name": "aortic dissection", "entered_at": turn["h"]}),
        Op.entity("TestOrder", "t2", {"name": "CT angiogram", "entered_at": turn["t"]}),
        _explains("e4", "h2", "f1"),
        _explains("e5", "h2", "f2"),
        _explains("e6", "h2", "f3"),
        _explains("e7", "h3", "f1"),
        _explains("e8", "h3", "f2"),
        _explains("e9", "h3", "f3"),
        _discriminates("s2", "t2", "h2"),
        _discriminates("s3", "t2", "h3"),
    ]


def _refutations(turn: dict[str, int]) -> list[Op]:
    return [
        Op.entity(
            "TestResult",
            "r2",
            {"name": "no filling defect", "verdict": "REFUTES", "entered_at": turn["r"]},
        ),
        Op.entity(
            "TestResult",
            "r3",
            {"name": "no intimal flap", "verdict": "REFUTES", "entered_at": turn["r"]},
        ),
        _bears_on("b2", "r2", "h2"),
        _bears_on("b3", "r3", "h3"),
    ]


def graph_c2_writes() -> list[Op]:
    """Not in the sketch. Competitors entered, neither refuted."""
    return [*_presentation(), *_mi_line(SKETCH_TURNS), *_competitors(SKETCH_TURNS)]


def graph_d_writes() -> list[Op]:
    """GEDANKEN.md:308-312. Competitors entered and both explicitly refuted."""
    return [
        *_presentation(),
        *_mi_line(SKETCH_TURNS),
        *_competitors(SKETCH_TURNS),
        *_refutations(SKETCH_TURNS),
    ]


def batch_writes() -> list[Op]:
    """Graph D with every step claiming the conclusion's own turn."""
    return [
        *_presentation(),
        *_mi_line(BATCH_TURNS),
        *_competitors(BATCH_TURNS),
        *_refutations(BATCH_TURNS),
    ]


def main() -> None:
    report("toy 3, graph C (single hypothesis)", check(TOY, graph_c_writes()))
    report("toy 3, graph C2 (competitors unrefuted, added)", check(TOY, graph_c2_writes()))
    report("toy 3, graph D (sound)", check(TOY, graph_d_writes()))
    report("toy 3, graph D written as one batch at turn 6", check(TOY, batch_writes()))
    print("\n--- what entered_at bought ---")
    print(f"graph D  violations : {findings(check(TOY, graph_d_writes()))}")
    print(f"batch    violations : {findings(check(TOY, batch_writes()))}")
    print("entered_at is declared, required, and compiled into facts; no rule reads it")


if __name__ == "__main__":
    main()
