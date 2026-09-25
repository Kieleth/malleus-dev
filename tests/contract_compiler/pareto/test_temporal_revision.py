"""T3, the first temporal Core cut: REVISION and TRANSITION, and the impact read.

The specification is design/temporal/g4/RULINGS.md (R-01 to R-08, D-04, D-08).
A supersession operation may declare its kind in an optional operation field
(route A, R-07): ``TRANSITION`` (the world changed) or ``REVISION`` (our account
of the record changed). An operation without the field keeps today's meaning.

Expected answers come from the G1 specimens and the rulings, never from Core:
g1-01 (``design/temporal/g1/g1-01-price-history.json``) for the timed case and
g1-04 (``g1-04-unknown-time-diameter.json``) for the untimed one. Histories are
built the way G3 builds them (``design/temporal/g3/driver.py``): the G3
contract bytes, one change set per specimen change, admitted through
``check_and_admit_change_set`` under Core's structural policy.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest
import yaml

import malleus.compiler as api


ROOT = Path(__file__).resolve().parents[3]
G1 = ROOT / "design/temporal/g1"
G3_CONTRACTS = ROOT / "design/temporal/g3/contracts"
TX = "2026-09-24T00:00:00+00:00"
ACTOR = "actor:temporal-t3"


# --- fixtures from the specimens ---------------------------------------------


def _specimen(name: str) -> dict:
    spec = json.loads((G1 / name).read_bytes())
    return {obj["id"]: obj for obj in spec["objects"]}


PRICE = _specimen("g1-01-price-history.json")
DIAMETER = _specimen("g1-04-unknown-time-diameter.json")


def _compile(source: bytes):
    return api.compile_linkml_contract(
        root_locator="contract",
        sources={
            "contract": source,
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model", "model", "schema", "types.yaml")
            .read_bytes(),
        },
    )


def _impact_contract() -> bytes:
    """The G3 g1-01 contract plus the typed references the impact read follows.

    ``Use`` carries class-ranged slots, single and multivalued, a reference to
    another ``Use`` for the transitive case, an inlined binding whose own slot
    is class-ranged, and a string-ranged slot the ontology does not know is a
    reference. ``Cites`` is a relation whose target is an ``Assertion``.
    """

    data = yaml.safe_load((G3_CONTRACTS / "g1-01.yaml").read_bytes())
    data["slots"].update(
        {
            "premise": {"range": "Assertion"},
            "premises": {"range": "Assertion", "multivalued": True},
            "basis_use": {"range": "Use"},
            "premise_label": {"range": "string"},
            "bindings": {"range": "Binding", "multivalued": True, "inlined": True},
            "bound": {"range": "Assertion"},
        }
    )
    data["classes"].update(
        {
            "Binding": {"slots": ["parameter", "bound"]},
            "Use": {
                "is_a": "Entity",
                "slots": [
                    "label",
                    "premise",
                    "premises",
                    "basis_use",
                    "premise_label",
                    "bindings",
                ],
            },
            "Cites": {
                "is_a": "Relation",
                "slot_usage": {
                    "source_id": {"range": "Use"},
                    "target_id": {"range": "Assertion"},
                },
            },
        }
    )
    return yaml.safe_dump(data, sort_keys=False).encode()


@pytest.fixture(scope="module")
def price_contract():
    return _compile((G3_CONTRACTS / "g1-01.yaml").read_bytes())


@pytest.fixture(scope="module")
def diameter_contract():
    return _compile((G3_CONTRACTS / "g1-04.yaml").read_bytes())


@pytest.fixture(scope="module")
def impact_contract():
    return _compile(_impact_contract())


# --- encoding, as G3's driver encodes these specimen objects -----------------


def _instant(value: str) -> api.KnowledgeValidTime:
    return api.KnowledgeValidTime("INSTANT", value)


NONE_STATED = api.KnowledgeValidTime("NONE_STATED", None)


def _entity(obj: dict) -> dict:
    """One specimen object as the G3 driver's operation record."""

    if obj["type"] in {"SUBJECT", "ACCOUNT"}:
        record_type = "Subject" if obj["type"] == "SUBJECT" else "Account"
        return {"type": record_type, "id": obj["id"], "properties": {"label": obj["label"]}}
    assert obj["type"] == "ASSERTION"
    props = {
        "subject": obj["subject_ref"],
        "property": obj["property"],
        "assertion_value": obj["value"],
        "basis": obj["basis"],
        "account": obj["account_ref"],
        "evidence_refs": obj["evidence_refs"],
    }
    if "corrects_ref" in obj:
        props["corrects"] = obj["corrects_ref"]
    until = obj["applicability"].get("until")
    if obj["applicability"]["kind"] == "INTERVAL" and until is not None:
        props["stated_until"] = until
    return {"type": "Assertion", "id": obj["id"], "properties": props}


def _renamed(obj: dict, record_id: str, **props) -> dict:
    record = _entity(obj)
    record["id"] = record_id
    record["properties"] = {**record["properties"], **props}
    return record


def _operation(ordinal, record, target=None, kind=None) -> api.KnowledgeOperation:
    """A Core operation; the kind field is passed only when one is declared."""

    extra = {} if kind is None else {"supersession_kind": kind}
    return api.KnowledgeOperation(
        ordinal=ordinal,
        operation_id=f"operation:{record['id']}",
        operation_type=record.get("operation_type", "CREATE_ENTITY"),
        record_type=record["type"],
        record_id=record["id"],
        properties=record["properties"],
        depends_on=(),
        source_id=record.get("source_id"),
        target_id=record.get("target_id"),
        supersedes_record_id=target,
        **extra,
    )


def _ledger(history) -> tuple[str, int]:
    content = Path(history.path).read_bytes()
    return "sha256:" + sha256(content).hexdigest(), len(content)


class Build:
    """One history, one change set per position, every step through Core."""

    def __init__(self, path: Path, compilation) -> None:
        self.history = api.create_structural_history(
            path, compilation=compilation, transaction_time=TX, actor_id=ACTOR
        )
        self.positions: dict[str, tuple[str, int]] = {}
        self.replays: dict[str, object] = {}

    def compose(self, label, records, valid_time, *, sources=(), supersede=None):
        """Retain the sources and one evidence record, then compose at the head."""

        supersede = supersede or {}
        held = {m.record_id for m in self.history.replay().retained_inputs}
        anchors = []
        for source_id in sources:
            if source_id in held:
                continue
            anchors.extend(
                api.structural_source_anchors(
                    source_id=source_id,
                    artifact_id=f"artifact:{source_id}",
                    content=PRICE.get(source_id, DIAMETER.get(source_id, {"text": source_id}))[
                        "text"
                    ].encode(),
                    media_type="text/plain",
                )
            )
        source_ids = tuple(sources)
        if not source_ids:
            source_ids = (f"decl:{label}",)
            if source_ids[0] not in held:
                anchors.extend(
                    api.structural_source_anchors(
                        source_id=source_ids[0],
                        artifact_id=f"artifact:decl:{label}",
                        content=json.dumps(sorted(r["id"] for r in records)).encode(),
                        media_type="application/json",
                    )
                )
        evidence_id = f"evidence:{label}"
        if evidence_id not in held:
            anchors.append(
                api.structural_evidence_anchor(
                    record_id=evidence_id,
                    content=json.dumps({"position": label}).encode(),
                    media_type="application/json",
                )
            )
        if anchors:
            self.history.append_anchors(
                anchors=tuple(anchors), transaction_time=TX, actor_id=ACTOR
            )
        return self.history.compose_change_set(
            change_set_id=f"change:{label}",
            source_record_ids=source_ids,
            evidence_record_ids=(evidence_id,),
            operations=tuple(
                _operation(i, r, *supersede.get(r["id"], (None, None)))
                for i, r in enumerate(records)
            ),
            valid_time=valid_time,
            supersedes=(),
        )

    def admit(self, label, change):
        admitted = api.check_and_admit_change_set(
            history=self.history, change_set=change, transaction_time=TX, actor_id=ACTOR
        )
        self.positions[label] = (
            admitted.replay.ledger_head,
            admitted.replay.ledger_event_count,
        )
        self.replays[label] = admitted.replay
        return admitted.replay

    def step(self, label, records, valid_time, **kwargs):
        return self.admit(label, self.compose(label, records, valid_time, **kwargs))

    def refused(self, label, records, valid_time, **kwargs):
        """Compose and submit; return the refusal and prove no byte moved."""

        change = self.compose(label, records, valid_time, **kwargs)
        before = _ledger(self.history)
        with pytest.raises(api.PopulationAdmissionRefusal) as caught:
            api.check_and_admit_change_set(
                history=self.history,
                change_set=change,
                transaction_time=TX,
                actor_id=ACTOR,
            )
        assert _ledger(self.history) == before
        return caught.value

    def at(self, label):
        head, count = self.positions[label]
        final = self.history.replay()
        return self.history.replay_at(
            ledger_head=head,
            ledger_event_count=count,
            expected_head_hash=final.ledger_head,
            expected_event_count=final.ledger_event_count,
        )


def _price_history(tmp_path, compilation, *, k2_kind="TRANSITION", extra_k1=()):
    """g1-01 K1 and K2: r1 750 from 1 May; r2 800 from 12 May replacing r1."""

    build = Build(tmp_path / "g1-01.jsonl", compilation)
    build.step(
        "K1",
        [_entity(PRICE["product:P"]), _entity(PRICE["account:reported-price"]), _entity(PRICE["r1"]), *extra_k1],
        _instant("2026-05-01T00:00:00Z"),
        sources=("src:r1",),
    )
    build.step(
        "K2",
        [_entity(PRICE["r2"])],
        _instant("2026-05-12T00:00:00Z"),
        sources=("src:r2",),
        supersede={"r2": ("r1", k2_kind)},
    )
    return build


def _revise_r1(build, label="K3", record_id="r3", valid_from="2026-05-01T00:00:00Z"):
    records = [_renamed(PRICE["r3"], record_id)]
    return records, _instant(valid_from), {"sources": ("src:r3",), "supersede": {record_id: ("r1", "REVISION")}}


def _price_ids(replay) -> set[str]:
    return {
        node["id"]
        for node in replay.graph.export_records()["entities"]
        if node.get("properties", node).get("property") == "unit_price"
    }


# --- persisted identity: route A moves nothing -------------------------------

# Read from Core at 837908ba, before this cut, on the legacy build below: g1-01
# K1 and K2 with K2 an operation without the kind field.
LEGACY_LEDGER = (
    "sha256:703550536c24197ddeaa8436689fb9bb0b8305372861904c5c0eeab1af73ac2a",
    423819,
)
LEGACY_RECEIPT = "sha256:bea24f0a402ff379480862efd3d6a122fd74cbc399edb7c3019325a8bd1b7d36"
STRUCTURAL_BUNDLE = "sha256:8a994ed00fef8a253069808eaf68d429ed29fe2869eefe6cd30bd426c31977e8"
STRUCTURAL_CHECK = "sha256:b923c279024e7a2cf18fab86b2e9e80e8f5afecbd8e7da83be437f2fba228f41"
STATE_VERSION = "sha256:b18f3129942761e03ce754af6cec8c689c94b91468aa105a423f5b27ddf20dc3"


def test_an_operation_without_the_kind_field_writes_the_same_bytes_as_before(
    tmp_path, price_contract
):
    build = _price_history(tmp_path, price_contract, k2_kind=None)
    assert _ledger(build.history) == LEGACY_LEDGER
    assert build.history.replay().receipt.identity == LEGACY_RECEIPT
    assert api.STRUCTURAL_HISTORY_BUNDLE.identity == STRUCTURAL_BUNDLE
    assert api.STRUCTURAL_HISTORY_BUNDLE.check_contract_identity == STRUCTURAL_CHECK
    assert api.STATE_VERSION_PROFILE.identity == STATE_VERSION
    # The same bytes reopen and replay under this Core.
    reopened = api.KnowledgeChangeHistory.reopen(build.history.path).replay()
    assert reopened.receipt.identity == LEGACY_RECEIPT


def test_an_operation_without_the_kind_field_keeps_todays_history(tmp_path, price_contract):
    build = _price_history(tmp_path, price_contract, k2_kind=None)
    r1 = build.history.replay().record_history["r1"]
    assert r1.superseded_by == "r2"
    assert r1.valid_to == _instant("2026-05-12T00:00:00Z")
    assert r1.closings == ()
    assert r1.operation.supersession_kind is None
    assert _price_ids(build.history.replay()) == {"r2"}


# --- probe: a typed reference does not block superseding its target ---------


def _use(record_id, **props):
    return {"type": "Use", "id": record_id, "properties": {"label": record_id, **props}}


def test_probe_a_class_ranged_reference_does_not_block_superseding_its_target(
    tmp_path, impact_contract
):
    """R-05 was code-read. This is today's behaviour, on an undeclared supersession."""

    build = _price_history(
        tmp_path,
        impact_contract,
        k2_kind=None,
        extra_k1=(_use("u1", premise="r1", premises=["r1"]),),
    )
    replay = build.history.replay()
    assert _price_ids(replay) == {"r2"}
    assert replay.graph.get_node("u1")["premise"] == "r1"


# --- G4's first test: a revision after a transition -------------------------


def test_g1_01_k3_revises_r1_after_its_transition(tmp_path, price_contract):
    build = _price_history(tmp_path, price_contract)
    k1_before = build.history.replay_at(
        ledger_head=build.positions["K1"][0],
        ledger_event_count=build.positions["K1"][1],
        expected_head_hash=build.positions["K2"][0],
        expected_event_count=build.positions["K2"][1],
    )
    k2_before = build.history.replay()

    records, valid_time, kwargs = _revise_r1(build)
    k3 = build.step("K3", records, valid_time, **kwargs)

    # r2 stays the only current price; r1 and r3 are not current.
    assert _price_ids(k3) == {"r2"}
    assert build.at("K3").graph.state_digest() == k2_before.graph.state_digest()
    history = k3.record_history
    r1, r2, r3 = history["r1"], history["r2"], history["r3"]
    # r3 covers 1 May to 12 May and is followed by r2 (specimen r3 applicability).
    assert r3.valid_from == _instant("2026-05-01T00:00:00Z")
    assert r3.valid_to == _instant("2026-05-12T00:00:00Z")
    assert r3.superseded_by == "r2"
    assert r3.supersedes_record_id == "r1"
    assert r3.operation.supersession_kind == "REVISION"
    # r1 stays in history: closed by the K2 transition, revised at K3.
    assert r1.valid_from == _instant("2026-05-01T00:00:00Z")
    assert r1.valid_to == _instant("2026-05-12T00:00:00Z")
    assert [(c.kind, c.record_id, c.change_set_id) for c in r1.closings] == [
        ("TRANSITION", "r2", "change:K2"),
        ("REVISION", "r3", "change:K3"),
    ]
    assert r1.operation.properties["assertion_value"]["lexical"] == "750"
    assert r2.superseded_by is None and r2.closings == ()

    # K2 and K1 read exactly as before K3 existed.
    k2_after = build.at("K2")
    assert k2_after.receipt.identity == k2_before.receipt.identity
    assert k2_after.graph.state_digest() == k2_before.graph.state_digest()
    assert dict(k2_after.record_history) == dict(k2_before.record_history)
    k1_after = build.at("K1")
    assert k1_after.receipt.identity == k1_before.receipt.identity
    assert dict(k1_after.record_history) == dict(k1_before.record_history)

    # A reopened ledger replays to the same history.
    reopened = api.KnowledgeChangeHistory.reopen(build.history.path).replay()
    assert dict(reopened.record_history) == dict(k3.record_history)


def test_a_second_revision_of_r1_composed_at_k3_refuses_as_a_stale_target(
    tmp_path, price_contract
):
    build = _price_history(tmp_path, price_contract)
    records, valid_time, kwargs = _revise_r1(build)
    build.step("K3", records, valid_time, **kwargs)

    records, valid_time, kwargs = _revise_r1(build, label="K3b", record_id="r3-stale")
    refusal = build.refused("K3b", records, valid_time, **kwargs)
    assert refusal.stage is api.PopulationAdmissionStage.CHECK
    assert "STALE_TARGET" in refusal.detail
    assert "forks prior record" not in refusal.detail


def test_the_transition_kind_is_recorded_and_r1_is_still_believed_at_k2(
    tmp_path, price_contract
):
    build = _price_history(tmp_path, price_contract)
    r1 = build.history.replay().record_history["r1"]
    assert r1.valid_to == _instant("2026-05-12T00:00:00Z")
    assert r1.superseded_by == "r2"
    assert [(c.kind, c.record_id, c.change_set_id) for c in r1.closings] == [
        ("TRANSITION", "r2", "change:K2")
    ]
    assert not any(c.kind == "REVISION" for c in r1.closings)
    assert _price_ids(build.history.replay()) == {"r2"}


def test_a_revision_of_a_record_closed_without_a_declared_kind_refuses(
    tmp_path, price_contract
):
    """Choice made here: an undeclared closing may have been a revision."""

    build = _price_history(tmp_path, price_contract, k2_kind=None)
    records, valid_time, kwargs = _revise_r1(build)
    refusal = build.refused("K3", records, valid_time, **kwargs)
    assert "STALE_TARGET" in refusal.detail
    assert "declares no kind" in refusal.detail


def test_a_revision_of_a_revision_is_ordinary(tmp_path, price_contract):
    build = _price_history(tmp_path, price_contract)
    records, valid_time, kwargs = _revise_r1(build)
    build.step("K3", records, valid_time, **kwargs)
    k4 = build.step(
        "K4",
        [_renamed(PRICE["r3"], "r3b", corrects="r3")],
        _instant("2026-05-01T00:00:00Z"),
        sources=("src:r3",),
        supersede={"r3b": ("r3", "REVISION")},
    )
    history = k4.record_history
    assert history["r3b"].valid_to == _instant("2026-05-12T00:00:00Z")
    assert history["r3b"].superseded_by == "r2"
    assert [(c.kind, c.record_id) for c in history["r3"].closings] == [
        ("TRANSITION", "r2"),
        ("REVISION", "r3b"),
    ]
    assert _price_ids(k4) == {"r2"}


def test_a_revision_of_the_current_record_may_keep_its_period(tmp_path, price_contract):
    """Today this refuses 'record replacement contradicts prior valid time'."""

    build = _price_history(tmp_path, price_contract)
    k3 = build.step(
        "K3",
        [_renamed(PRICE["r2"], "r2b")],
        _instant("2026-05-12T00:00:00Z"),
        sources=("src:r2",),
        supersede={"r2b": ("r2", "REVISION")},
    )
    assert _price_ids(k3) == {"r2b"}
    history = k3.record_history
    assert history["r2b"].valid_from == _instant("2026-05-12T00:00:00Z")
    assert history["r2b"].valid_to is None and history["r2b"].superseded_by is None
    assert history["r2"].valid_to is None
    assert [(c.kind, c.record_id) for c in history["r2"].closings] == [("REVISION", "r2b")]


def test_a_revision_that_changes_the_record_type_refuses(tmp_path, price_contract):
    build = _price_history(tmp_path, price_contract)
    refusal = build.refused(
        "K3",
        [{"type": "Account", "id": "r3", "properties": {"label": "not a price"}}],
        _instant("2026-05-01T00:00:00Z"),
        sources=("src:r3",),
        supersede={"r3": ("r1", "REVISION")},
    )
    assert refusal.stage is api.PopulationAdmissionStage.CHECK
    assert "TYPE_CHANGE" in refusal.detail


def test_a_revision_whose_valid_time_differs_from_its_target_refuses(
    tmp_path, price_contract
):
    build = _price_history(tmp_path, price_contract)
    records, valid_time, kwargs = _revise_r1(build, valid_from="2026-05-03T00:00:00Z")
    refusal = build.refused("K3", records, valid_time, **kwargs)
    assert refusal.stage is api.PopulationAdmissionStage.CHECK
    assert "VALID_TIME_EXTENT" in refusal.detail


def test_a_kind_without_a_target_or_an_unknown_kind_is_malformed(tmp_path, price_contract):
    build = _price_history(tmp_path, price_contract)
    record = _renamed(PRICE["r3"], "r3")
    for target, kind in ((None, "REVISION"), ("r1", "CORRECTION")):
        operation = api.KnowledgeOperation(
            ordinal=0,
            operation_id="operation:r3",
            operation_type="CREATE_ENTITY",
            record_type="Assertion",
            record_id="r3",
            properties=record["properties"],
            depends_on=(),
            supersedes_record_id=target,
            supersession_kind=kind,
        )
        with pytest.raises(api.KnowledgeChangeRefusal) as caught:
            build.history.compose_change_set(
                change_set_id="change:bad",
                source_record_ids=("src:r2",),
                evidence_record_ids=("evidence:K2",),
                operations=(operation,),
                valid_time=_instant("2026-05-01T00:00:00Z"),
                supersedes=(),
            )
        assert caught.value.reason is api.KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET


# --- the untimed case: g1-04 --------------------------------------------------


def _diameter_history(tmp_path, compilation):
    build = Build(tmp_path / "g1-04.jsonl", compilation)
    build.step(
        "M1",
        [_entity(DIAMETER["pipe:Q"]), _entity(DIAMETER["account:diameter-report"]), _entity(DIAMETER["m1"])],
        NONE_STATED,
        sources=("src:m1",),
    )
    return build


def test_g1_04_revision_of_an_untimed_record_keeps_no_stated_time(
    tmp_path, diameter_contract
):
    build = _diameter_history(tmp_path, diameter_contract)
    m2 = build.step(
        "M2",
        [_entity(DIAMETER["m2"])],
        NONE_STATED,
        sources=("src:m2",),
        supersede={"m2": ("m1", "REVISION")},
    )
    history = m2.record_history
    assert history["m2"].valid_from == NONE_STATED
    assert history["m2"].valid_to is None
    assert history["m1"].valid_to is None
    assert [(c.kind, c.record_id, c.change_set_id) for c in history["m1"].closings] == [
        ("REVISION", "m2", "change:M2")
    ]
    diameters = {
        node["id"]
        for node in m2.graph.export_records()["entities"]
        if node.get("properties", node).get("property") == "diameter"
    }
    assert diameters == {"m2"}
    # Revising the revision is ordinary.
    m3 = build.step(
        "M3",
        [_renamed(DIAMETER["m2"], "m2b", corrects="m2")],
        NONE_STATED,
        sources=("src:m2",),
        supersede={"m2b": ("m2", "REVISION")},
    )
    assert m3.record_history["m2b"].valid_from == NONE_STATED


def test_g1_04_a_revision_that_invents_a_date_refuses(tmp_path, diameter_contract):
    build = _diameter_history(tmp_path, diameter_contract)
    refusal = build.refused(
        "M2",
        [_entity(DIAMETER["m2"])],
        _instant("2026-05-05T12:00:00Z"),
        sources=("src:m2",),
        supersede={"m2": ("m1", "REVISION")},
    )
    assert "VALID_TIME_EXTENT" in refusal.detail


# --- a revision Core cannot check against a rule layer ------------------------


from tests.contract_compiler.pareto.test_atomic_population_admission import (  # noqa: E402
    SOURCE_ID,
    _record,
    swipl,
)
from tests.contract_compiler.pareto.test_check_contract_executor import (  # noqa: E402
    _two_check_history,
)


@swipl
def test_a_revision_of_a_closed_period_refuses_under_a_rule_layer(tmp_path):
    """Custom rules read the current graph only (CHECK-SCOPE-02, R-04)."""

    history, _, _ = _two_check_history(tmp_path)

    def compose(change_set_id, record, valid, target=None, kind=None):
        return history.compose_change_set(
            change_set_id=change_set_id,
            source_record_ids=(SOURCE_ID,),
            evidence_record_ids=("artifact:logic",),
            operations=(
                _operation(
                    0,
                    {"type": record["type"], "id": record["id"], "properties": record["properties"]},
                    target,
                    kind,
                ),
            ),
            valid_time=api.KnowledgeValidTime("ORDER_ONLY", valid),
            supersedes=(),
        )

    def admit(change):
        return api.check_and_admit_change_set(
            history=history, change_set=change, transaction_time=TX, actor_id=ACTOR
        )

    first = _record("e1", 2)
    admit(compose("change:e1", first, "e1"))
    second = _record("e2", 5)
    admit(compose("change:e2", second, "e2", first["id"], "TRANSITION"))
    revised = {**_record("e1", 3), "id": "supplier-order-state:B:e1-revised"}
    before = _ledger(history)
    with pytest.raises(api.PopulationAdmissionRefusal) as caught:
        admit(compose("change:e1-revised", revised, "e1", first["id"], "REVISION"))
    assert caught.value.stage is api.PopulationAdmissionStage.CHECK
    assert caught.value.reason == "CUSTOM_POLICY_HISTORICAL_SCOPE"
    assert _ledger(history) == before


# --- the impact read (R-05) ----------------------------------------------------


def _impact_history(tmp_path, compilation):
    """u1 names r1 through typed slots; u2 names u1; n1 names r1 as a string.

    c1 cites r1 as a relation. A relation into r1 blocks retiring r1, so the
    K2 transition restates it onto r2 as c2 (A13, A15). K3 revises r1.
    """

    uses = (
        _use(
            "u1",
            premise="r1",
            premises=["r1", "account:reported-price"],
            bindings=[{"parameter": "unit_price", "bound": "r1"}],
        ),
        _use("u2", basis_use="u1"),
        _use("n1", premise_label="r1"),
        {
            "type": "Cites",
            "id": "c1",
            "operation_type": "CREATE_RELATION",
            "source_id": "u1",
            "target_id": "r1",
            "properties": {"relation_type": "CITES"},
        },
    )
    build = Build(tmp_path / "impact.jsonl", compilation)
    build.step(
        "K1",
        [_entity(PRICE["product:P"]), _entity(PRICE["account:reported-price"]), _entity(PRICE["r1"]), *uses],
        _instant("2026-05-01T00:00:00Z"),
        sources=("src:r1",),
    )
    build.step(
        "K2",
        [
            _entity(PRICE["r2"]),
            {
                "type": "Cites",
                "id": "c2",
                "operation_type": "CREATE_RELATION",
                "source_id": "u1",
                "target_id": "r2",
                "properties": {"relation_type": "CITES"},
            },
        ],
        _instant("2026-05-12T00:00:00Z"),
        sources=("src:r2",),
        supersede={"r2": ("r1", "TRANSITION"), "c2": ("c1", "TRANSITION")},
    )
    records, valid_time, kwargs = _revise_r1(build)
    build.step("K3", records, valid_time, **kwargs)
    return build


def _refs(result):
    return {
        (ref.record_id, ref.via, ref.refers_to, ref.depth, ref.change_set_id, ref.current)
        for ref in result.references
    }


def test_the_impact_read_reports_every_typed_use_of_the_revised_version(
    tmp_path, impact_contract
):
    build = _impact_history(tmp_path, impact_contract)
    replay = build.history.replay()
    before = _ledger(build.history)

    result = replay.version_referrers("r1")

    assert result.record_id == "r1"
    assert (result.ledger_head, result.ledger_event_count) == (
        replay.ledger_head,
        replay.ledger_event_count,
    )
    assert _refs(result) == {
        ("u1", "premise", "r1", 1, "change:K1", True),
        ("u1", "premises", "r1", 1, "change:K1", True),
        ("u1", "bindings.bound", "r1", 1, "change:K1", True),
        ("c1", "target_id", "r1", 1, "change:K1", False),
        # Followed backwards from u1: every version naming u1.
        ("u2", "basis_use", "u1", 2, "change:K1", True),
        ("c1", "source_id", "u1", 2, "change:K1", False),
        ("c2", "source_id", "u1", 2, "change:K2", True),
    }
    # The string-ranged slot is not followed, and the result says so.
    assert "n1" not in {ref.record_id for ref in result.references}
    assert "STRING_RANGED_SLOTS" in result.not_covered
    assert set(result.not_covered) == {
        "UNRECORDED_USES",
        "RULE_READS",
        "QUERY_SCOPES",
        "STRING_RANGED_SLOTS",
    }
    # The use still names the version it used; the read wrote nothing.
    assert replay.graph.get_node("u1")["premise"] == "r1"
    assert _ledger(build.history) == before


def test_the_impact_read_on_a_version_nobody_names_is_empty_not_absent(
    tmp_path, impact_contract
):
    build = _impact_history(tmp_path, impact_contract)
    result = build.history.replay().version_referrers("r3")
    assert result.references == ()
    assert "UNRECORDED_USES" in result.not_covered


def test_the_impact_read_refuses_an_unknown_version(tmp_path, impact_contract):
    build = _impact_history(tmp_path, impact_contract)
    with pytest.raises(KeyError):
        build.history.replay().version_referrers("r9")


def test_the_impact_read_at_an_earlier_position_sees_that_position_only(
    tmp_path, impact_contract
):
    build = _impact_history(tmp_path, impact_contract)
    at_k1 = build.at("K1").version_referrers("r1")
    assert ("c1", "target_id", "r1", 1, "change:K1", True) in _refs(at_k1)
