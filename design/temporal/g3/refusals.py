"""Attempt every G1 expected refusal through Core, on a copy of the history.

Each attempt follows the main run's procedure: a declared replacement is tried
as an explicit supersession first; if Core refuses it, the same records are
tried as plain additions. The refusal is OBSERVED when the procedure ends
refused, and NOT_OBSERVED when some step is admitted. Alternative encodings are
reported beside it and do not change the class. Ledger bytes are measured around
each admission call; source retention for the attempt is a separate, earlier
write and is listed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

import malleus.compiler as api

from driver import (
    ACTOR,
    NOT_OBSERVED,
    OBSERVED,
    TX,
    Attempt,
    Run,
    SpecimenDriver,
    admit,
    build,
    canonical,
    compile_contract,
    core_valid_time,
    encode,
    ledger_state,
    operations,
    source_anchors,
)


@dataclass
class RefusalOutcome:
    specimen: str
    refusal_id: str
    expected_category: str
    head: str
    base: str
    classification: str
    procedure: list[Attempt]
    alternatives: dict[str, list[Attempt]] = field(default_factory=dict)
    retained_first: list[str] = field(default_factory=list)
    head_unchanged: bool = True
    notes: list[str] = field(default_factory=list)
    history_after: object | None = None


def compose_attempt(history, change_set_id, records, sources, evidence, supersedes, valid_time) -> tuple[object | None, Attempt | None]:
    """Compose through Core. A composition refusal is an attempt outcome."""
    try:
        change = history.compose_change_set(
            change_set_id=change_set_id,
            source_record_ids=tuple(sources),
            evidence_record_ids=tuple(evidence),
            operations=operations(records, supersedes),
            valid_time=valid_time,
            supersedes=(),
        )
    except api.KnowledgeChangeRefusal as refusal:
        state = ledger_state(history)
        return None, Attempt(
            change_set_id, valid_time, dict(supersedes), tuple(r["record_id"] for r in records),
            "REFUSED", "COMPOSE", refusal.reason.name, refusal.detail,
            f"{state[0]} ({state[1]} bytes)", f"{state[0]} ({state[1]} bytes)",
        )
    return change, None


class Attempter:
    def __init__(self, run: Run, history):
        self.run = run
        self.history = history
        self.driver: SpecimenDriver = run.driver
        self.retained: list[str] = []

    def retain(self, source_ids=(), evidence_id=None, evidence=None):
        anchors = []
        for sid in source_ids:
            anchors.extend(source_anchors(self.driver.objects[sid]))
            self.retained.append(sid)
        if evidence_id:
            anchors.append(
                api.structural_evidence_anchor(record_id=evidence_id, content=canonical(evidence), media_type="application/json")
            )
            self.retained.append(evidence_id)
        if anchors:
            self.history.append_anchors(anchors=tuple(anchors), transaction_time=TX, actor_id=ACTOR)

    def records(self, ids):
        out = []
        for rid in ids:
            obj = self.driver.rejected.get(rid) or self.driver.objects[rid]
            out.extend(encode(obj, self.run.positions, self.run.key))
        return out

    def compose(self, change_set_id, ids, sources, evidence, supersedes, valid_time=None):
        if valid_time is None:
            times = {core_valid_time(self.driver.rejected.get(i) or self.driver.objects[i]) for i in ids} - {None}
            valid_time = times.pop() if len(times) == 1 else api.KnowledgeValidTime("NONE_STATED", None)
        return compose_attempt(self.history, change_set_id, self.records(ids), sources, evidence, supersedes, valid_time)

    def procedure(self, change_set_id, ids, sources, evidence, supersedes, *, composed=None) -> list[Attempt]:
        """Supersession first, then plain; stop at the first admission or at a compose refusal."""
        attempts = []
        variants = [supersedes, {}] if supersedes else [{}]
        for number, variant in enumerate(variants):
            change, refused = composed[number] if composed else self.compose(change_set_id, ids, sources, evidence, variant)
            if refused is not None:
                attempts.append(refused)
                break
            replay, attempt = admit(self.history, change)
            attempts.append(attempt)
            if replay is not None:
                break
        return attempts


def _head(history):
    replay = history.replay()
    return replay.ledger_head, replay.ledger_event_count


def _classify(attempts: list[Attempt]) -> str:
    return OBSERVED if attempts and attempts[-1].outcome == "REFUSED" else NOT_OBSERVED


def _outcome(run, refusal_id, attempter, attempts, alternatives=None, notes=(), before=None):
    spec_refusal = next(r for r in run.driver.spec["refusals"] if r["id"] == refusal_id)
    unchanged = before is None or _head(attempter.history) == before
    return RefusalOutcome(
        run.key, refusal_id, spec_refusal["category"], spec_refusal["head"], spec_refusal.get("base", spec_refusal["head"]),
        _classify(attempts), attempts, alternatives or {}, list(attempter.retained),
        unchanged if _classify(attempts) == OBSERVED else False, list(notes), attempter.history,
    )


def _stale(run_key, workdir, base, head, refusal_id, ids, sources, supersedes, notes):
    """Compose at the base position, advance to the head, then submit."""
    held = {}

    def at_base(run: Run):
        attempter = Attempter(run, run.history)
        retained_ids = {m.record_id for m in run.history.replay().retained_inputs}
        attempter.retain([s for s in sources if s not in retained_ids], f"evidence:{refusal_id}", {"refusal": refusal_id, "composed_at": base})
        variants = [supersedes, {}] if supersedes else [{}]
        held["composed"] = [
            attempter.compose(f"change:{run_key}:{refusal_id}", ids, sources, [f"evidence:{refusal_id}"], v) for v in variants
        ]
        held["attempter"] = attempter

    run = build(run_key, workdir, stop_after=head, hooks={base: at_base}, name=f"stale-{refusal_id}")
    attempter = held["attempter"]
    attempter.history = run.history
    before = _head(run.history)
    attempts = attempter.procedure(None, ids, sources, None, supersedes, composed=held["composed"])
    return _outcome(run, refusal_id, attempter, attempts, notes=notes, before=before), run


def run_refusals(runs: dict[str, Run], workdir: Path) -> list[RefusalOutcome]:
    out: list[RefusalOutcome] = []

    # g1-01 ------------------------------------------------------------------
    outcome, _ = _stale(
        "g1-01", workdir, "K1", "K2", "RF-STALE-BASE", ["r3-stale"], ["src:r3"], {"r3-stale": "r1"},
        ["Composed at K1 after retaining src:r3; K1a, K1b and K2 were then admitted; submitted at K2."],
    )
    out.append(outcome)

    run = runs["g1-01"]
    a = Attempter(run, run.fork("K2", "RF-OVERLAP"))
    a.retain(["src:r3"], "evidence:RF-OVERLAP", {"refusal": "RF-OVERLAP"})
    before = _head(a.history)
    attempts = a.procedure("change:g1-01:RF-OVERLAP", ["r3-overlap"], ["src:r3"], ["evidence:RF-OVERLAP"], {"r3-overlap": "r1"})
    out.append(
        _outcome(
            run, "RF-OVERLAP", a, attempts,
            notes=[
                "The supersession step refuses for the same reason the valid correction r3 refused at K3 "
                "(r1 is already superseded by r2); it does not read the overlap with b. The plain step is admitted.",
            ],
            before=before,
        )
    )

    # g1-02 ------------------------------------------------------------------
    outcome, _ = _stale_exec(workdir)
    out.append(outcome)

    run = runs["g1-02"]
    a = Attempter(run, run.fork("O6", "RF-BORROWED"))
    decl = _declaration(a, "RF-BORROWED", ["exec:XC-borrowed", "result:XC-borrowed"])
    before = _head(a.history)
    attempts = a.procedure("change:g1-02:RF-BORROWED", ["exec:XC-borrowed", "result:XC-borrowed"], [decl], ["evidence:RF-BORROWED"], {})
    out.append(
        _outcome(
            run, "RF-BORROWED", a, attempts,
            notes=[
                "Core's structural check and the contract accept it: nothing Core runs compares an execution's "
                "bindings with its context's bindings. Core can run an adopter Prolog rule at admission "
                "(PROLOG_RULES check contract); none was built or run here, so whether such a rule would refuse it "
                "is not established."
            ],
            before=before,
        )
    )

    # g1-05 ------------------------------------------------------------------
    run = runs["g1-05"]
    a = Attempter(run, run.fork("G2", "RF-CITED-MODEL"))
    decl = _declaration(a, "RF-CITED-MODEL", ["exec:cited-only"])
    before = _head(a.history)
    attempts = a.procedure("change:g1-05:RF-CITED-MODEL", ["exec:cited-only"], [decl], ["evidence:RF-CITED-MODEL"], {})
    slot_only = _slot_only(a, "exec:cited-only", decl, "RF-CITED-MODEL")
    out.append(_outcome(run, "RF-CITED-MODEL", a, attempts, {"model link as a slot only": slot_only}, before=before))

    # g1-06 ------------------------------------------------------------------
    outcome, _ = _stale(
        "g1-06", workdir, "J3p", "J4p", "RF-STALE-REVIEW", ["J2-stale"], ["src:challenge"], {"J2-stale": "J1"},
        ["Composed at J3p after retaining src:challenge; J4p was then admitted; submitted at J4p."],
    )
    run = runs["g1-06"]
    fresh = Attempter(run, run.fork("J4p", "RF-STALE-REVIEW-fresh"))
    fresh.retain([], "evidence:RF-STALE-REVIEW-fresh", {"refusal": "RF-STALE-REVIEW", "composed_at": "J4p"})
    outcome.alternatives["composed fresh at J4p (base not stale)"] = fresh.procedure(
        "change:g1-06:RF-STALE-REVIEW-fresh", ["J2-stale"], ["src:challenge"], ["evidence:RF-STALE-REVIEW-fresh"], {"J2-stale": "J1"}
    )
    out.append(outcome)

    # g1-07 ------------------------------------------------------------------
    run = runs["g1-07"]
    a = Attempter(run, run.fork("V3", "RF-NO-EVIDENCE"))
    decl = _declaration(a, "RF-NO-EVIDENCE", ["ev-undocumented"])
    before = _head(a.history)
    attempts = a.procedure("change:g1-07:RF-NO-EVIDENCE", ["ev-undocumented"], [decl], ["evidence:RF-NO-EVIDENCE"], {})
    no_source = [a.compose("change:g1-07:RF-NO-EVIDENCE:no-source", ["ev-undocumented"], [], ["evidence:RF-NO-EVIDENCE"], {})[1]]
    out.append(
        _outcome(
            run, "RF-NO-EVIDENCE", a, attempts, {"change set names no source at all": no_source},
            notes=["The main procedure names a retained declaration as the change's source (Core requires one); the record's own evidence_refs is empty."],
            before=before,
        )
    )

    # g1-08 ------------------------------------------------------------------
    run = runs["g1-08"]
    a = Attempter(run, run.fork("R4", "RF-PARTIAL"))
    a.retain([], "evidence:RF-PARTIAL", {"refusal": "RF-PARTIAL"})
    before = _head(a.history)
    attempts = a.procedure("change:g1-08:RF-PARTIAL", ["q-weight", "rel:bad"], ["src:quote"], ["evidence:RF-PARTIAL"], {})
    out.append(_outcome(run, "RF-PARTIAL", a, attempts, before=before))

    a = Attempter(run, run.fork("R4", "RF-MISSING-MODEL"))
    decl = _declaration(a, "RF-MISSING-MODEL", ["exec:bad"])
    before = _head(a.history)
    attempts = a.procedure("change:g1-08:RF-MISSING-MODEL", ["exec:bad"], [decl], ["evidence:RF-MISSING-MODEL"], {})
    slot_only = _slot_only(a, "exec:bad", decl, "RF-MISSING-MODEL")
    out.append(_outcome(run, "RF-MISSING-MODEL", a, attempts, {"model link as a slot only": slot_only}, before=before))

    a = Attempter(run, run.fork("R4", "RF-MISSING-EVIDENCE"))
    decl = _declaration(a, "RF-MISSING-EVIDENCE", ["q-corr"])
    before = _head(a.history)
    attempts = a.procedure("change:g1-08:RF-MISSING-EVIDENCE", ["q-corr"], [decl], ["evidence:RF-MISSING-EVIDENCE"], {"q-corr": "q-price"})
    out.append(
        _outcome(
            run, "RF-MISSING-EVIDENCE", a, attempts,
            notes=["q-corr corrects q-price, so the procedure tries the supersession first."],
            before=before,
        )
    )

    a = Attempter(run, run.fork("R4", "RF-UNSUPPORTED"))
    a.retain([], "evidence:RF-UNSUPPORTED", {"refusal": "RF-UNSUPPORTED"})
    before = _head(a.history)
    attempts = a.procedure("change:g1-08:RF-UNSUPPORTED", ["q-recurring"], ["src:quote"], ["evidence:RF-UNSUPPORTED"], {})
    out.append(_outcome(run, "RF-UNSUPPORTED", a, attempts, before=before))

    out.append(_missing_contract(run, workdir))
    return out


def _declaration(attempter: Attempter, refusal_id: str, ids) -> str:
    """The main procedure's source for a change citing none: a retained declaration."""
    driver = attempter.driver
    objects = [driver.rejected.get(i) or driver.objects[i] for i in ids]
    cited = sorted({ref for o in objects for ref in o.get("evidence_refs", [])})
    anchors = [
        api.structural_evidence_anchor(
            record_id=f"evidence:{refusal_id}", content=canonical({"refusal": refusal_id}), media_type="application/json"
        )
    ]
    if cited:
        attempter.history.append_anchors(anchors=tuple(anchors), transaction_time=TX, actor_id=ACTOR)
        attempter.retained.append(f"evidence:{refusal_id}")
        return cited[0]
    anchors.extend(
        api.structural_source_anchors(
            source_id=f"decl:{refusal_id}", artifact_id=f"artifact:decl:{refusal_id}",
            content=canonical({"refusal": refusal_id, "objects": objects}), media_type="application/json",
        )
    )
    attempter.history.append_anchors(anchors=tuple(anchors), transaction_time=TX, actor_id=ACTOR)
    attempter.retained.extend([f"evidence:{refusal_id}", f"decl:{refusal_id}"])
    return f"decl:{refusal_id}"


def _slot_only(attempter: Attempter, record_id: str, source: str, refusal_id: str) -> list[Attempt]:
    """The same execution without the model relation: the model_ref slot alone."""
    probe = Attempter(attempter.run, attempter.run.fork(
        {"g1-05": "G2", "g1-08": "R4"}[attempter.run.key], f"{refusal_id}-slot"))
    source = _declaration(probe, refusal_id, [record_id])
    records = [r for r in probe.records([record_id]) if r["operation_type"] != "CREATE_RELATION"]
    change, refused = compose_attempt(
        probe.history, f"change:{probe.run.key}:{refusal_id}:slot", records, [source], [f"evidence:{refusal_id}"], {},
        api.KnowledgeValidTime("NONE_STATED", None),
    )
    if refused:
        return [refused]
    return [admit(probe.history, change)[1]]


def _stale_exec(workdir):
    held = {}
    ids = ["exec:XC-stale", "result:XC-stale"]

    def at_base(run: Run):
        attempter = Attempter(run, run.history)
        source = _declaration(attempter, "RF-STALE-EXEC", ids)
        held["composed"] = [attempter.compose("change:g1-02:RF-STALE-EXEC", ids, [source], ["evidence:RF-STALE-EXEC"], {})]
        held["attempter"] = attempter

    run = build("g1-02", workdir, stop_after="O6", hooks={"O5": at_base}, name="stale-RF-STALE-EXEC")
    attempter = held["attempter"]
    before = _head(run.history)
    attempts = attempter.procedure(None, ids, None, None, {}, composed=held["composed"])
    return _outcome(
        run, "RF-STALE-EXEC", attempter, attempts,
        notes=["Composed at O5 (with a retained declaration as its source), O6 then admitted, submitted at O6."],
        before=before,
    ), run


def _missing_contract(run: Run, workdir: Path) -> RefusalOutcome:
    """A change bound to a contract this history never accepted.

    contract:c1 is the history's own contract, so phantom:contract is a
    different contract. The change is composed in a second history running a
    contract with one extra class, then submitted here.
    """
    foreign_source = (Path(__file__).parent / "contracts" / "g1-08.yaml").read_bytes() + (
        b"  ForeignOnly:\n    is_a: Entity\n    slots: [label]\n"
    )
    other_path = workdir / "g1-08-foreign-contract.jsonl"
    other = api.create_structural_history(
        other_path, compilation=compile_contract("g1-08-foreign", foreign_source), transaction_time=TX, actor_id=ACTOR
    )
    helper = Attempter(run, other)
    helper.retain(["src:quote"], "evidence:RF-MISSING-CONTRACT", {"refusal": "RF-MISSING-CONTRACT"})
    change, refused = helper.compose("change:g1-08:RF-MISSING-CONTRACT", ["q-foreign"], ["src:quote"], ["evidence:RF-MISSING-CONTRACT"], {})
    assert refused is None
    target = Attempter(run, run.fork("R4", "RF-MISSING-CONTRACT"))
    before = _head(target.history)
    attempts = [admit(target.history, change)[1]]
    slot = Attempter(run, run.fork("R4", "RF-MISSING-CONTRACT-slot"))
    slot.retain([], "evidence:RF-MISSING-CONTRACT", {"refusal": "RF-MISSING-CONTRACT"})
    slot_attempts = slot.procedure("change:g1-08:RF-MISSING-CONTRACT:slot", ["q-foreign"], ["src:quote"], ["evidence:RF-MISSING-CONTRACT"], {})
    return _outcome(
        run, "RF-MISSING-CONTRACT", target, attempts,
        {"contract named only in the record's contract_ref slot": slot_attempts},
        notes=[
            "Primary: composed in a second history whose contract has one more class, submitted to this one. "
            "In Core the governing contract is the history's, bound by identity in every change set."
        ],
        before=before,
    )
