"""Fresh bytes, not a preauthored plan, cross the existing public Shop path."""

import ast
from importlib import import_module
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

import pytest

import malleus.compiler as api


ROOT = Path(__file__).resolve().parents[3]
HERE = (
    ROOT / "research/ontology_driven_kg_realization/experiments/small_shop/fresh_import"
)
MODULE = "research.ontology_driven_kg_realization.experiments.small_shop.fresh_import"
SOURCE_ID = "source:small-shop:fresh-suppliers"
PLAN_ID = "plan:small-shop:fresh-suppliers"
TIME = "2026-09-06T01:00:00Z"
ACTOR = "actor:small-shop-fresh-import"


def _adapter():
    return import_module(MODULE + ".adapter")


def _runner():
    return import_module(MODULE + ".run")


def test_mapper_is_read_only_and_derives_every_field_from_new_rows(monkeypatch):
    adapter = _adapter()
    source = (HERE / "supplier-orders.jsonl").read_bytes()

    def forbidden(*args, **kwargs):
        pytest.fail("supplier mapping attempted I/O")

    with monkeypatch.context() as guard:
        guard.setattr(Path, "open", forbidden)
        guard.setattr("builtins.open", forbidden)
        plan = adapter.adapt_supplier_rows(
            source_bytes=source,
            source_id=SOURCE_ID,
            plan_id=PLAN_ID,
            contract_identity="sha256:" + "a" * 64,
        )
        assert plan == adapter.adapt_supplier_rows(
            source_bytes=source,
            source_id=SOURCE_ID,
            plan_id=PLAN_ID,
            contract_identity="sha256:" + "a" * 64,
        )
    assert plan["valid_time"] == {"kind": "NONE_STATED", "value": None}
    changed = adapter.adapt_supplier_rows(
        source_bytes=source.replace(b'"ordered_quantity":5', b'"ordered_quantity":9'),
        source_id=SOURCE_ID,
        plan_id=PLAN_ID,
        contract_identity="sha256:" + "a" * 64,
    )
    assert changed["records"]["entities"][1]["properties"]["ordered_quantity"] == 9
    assert changed["sources"] != plan["sources"]
    assert plan["supersessions"] == []
    assert [
        row["properties"]["ordered_quantity"] for row in plan["records"]["entities"]
    ] == [3, 5]
    assert len(plan["derivations"]) == 8
    assert {d["locator"] for d in plan["derivations"]} == {
        f"row:{index}:{field}"
        for index in (0, 1)
        for field in (
            "source_occurrence_id",
            "supplier_order_id",
            "product_code",
            "ordered_quantity",
        )
    }


@pytest.mark.parametrize(
    "defect",
    [
        "invalid_json",
        "duplicate_key",
        "missing",
        "extra",
        "boolean",
        "negative",
        "empty",
        "duplicate_occurrence",
    ],
)
def test_malformed_supplier_file_refuses_before_history_writes(tmp_path, defect):
    runner, adapter = _runner(), _adapter()
    history = runner.start_existing_shop(tmp_path / "shop")
    rows = [
        json.loads(line)
        for line in (HERE / "supplier-orders.jsonl").read_bytes().splitlines()
    ]
    if defect == "missing":
        del rows[1]["ordered_quantity"]
    elif defect == "extra":
        rows[1]["unknown"] = "not declared"
    elif defect == "boolean":
        rows[1]["ordered_quantity"] = True
    elif defect == "negative":
        rows[1]["ordered_quantity"] = -1
    elif defect == "empty":
        rows[1]["supplier_order_id"] = ""
    elif defect == "duplicate_occurrence":
        rows[1]["source_occurrence_id"] = rows[0]["source_occurrence_id"]
    source = b"\n".join(json.dumps(row).encode() for row in rows)
    if defect == "invalid_json":
        source += b"\n{"
    elif defect == "duplicate_key":
        source = source.replace(
            b'"ordered_quantity": 5', b'"ordered_quantity": 5, "ordered_quantity": 6'
        )
    before = history.path.read_bytes()
    with pytest.raises(adapter.SupplierImportRefusal) as error:
        runner.prepare_import(history, source, transaction_time=TIME, actor_id=ACTOR)
    assert error.value.reason == "MALFORMED_SUPPLIER_ROWS"
    assert history.path.read_bytes() == before


def test_fresh_import_replays_and_traces_after_complete_shop(tmp_path):
    runner = _runner()
    guide = (HERE / "README.md").read_text()
    command = shlex.split(guide.split("```bash\n", 1)[1].split("```", 1)[0])
    assert command[:4] == ["python", "-m", MODULE + ".run", "--output"]
    assert len(command) == 5
    command[0], command[4] = sys.executable, str(tmp_path / "first")
    subprocess.run(command, cwd=ROOT, capture_output=True, check=True)
    report = json.loads((tmp_path / "first/evidence.json").read_bytes())
    assert runner.run_import(tmp_path / "second") == report
    path = tmp_path / "first/shop/history.jsonl"
    assert path.read_bytes() == (tmp_path / "second/shop/history.jsonl").read_bytes()
    assert (tmp_path / "first/evidence.json").read_bytes() == (
        tmp_path / "second/evidence.json"
    ).read_bytes()
    isolated = tmp_path / "only-ledger.jsonl"
    shutil.copyfile(path, isolated)
    replay = api.KnowledgeChangeHistory.reopen(isolated).replay()
    assert len(replay.change_sets) == 6
    assert len(replay.record_history) == 12
    assert report["rows_imported"] == 2
    assert report["prior_records_unchanged"] is True
    for order, quantity, occurrence, row_index in (
        ("SYN-C", 3, "synthetic:receipt:C", 0),
        ("SYN-D", 5, "synthetic:receipt:D", 1),
    ):
        rows = replay.graph.query("SupplierOrderState", supplier_order_id=order)
        assert len(rows) == 1 and rows[0]["ordered_quantity"] == quantity
        record_id = rows[0]["id"]
        trace = api.trace_population_record(replay, record_id)
        assert trace.record_history.valid_from.kind == "NONE_STATED"
        assert trace.sources[0].content == (HERE / "supplier-orders.jsonl").read_bytes()
        retained_evidence = {item.record_id: item.content for item in trace.evidence}
        assert (
            retained_evidence["artifact:small-shop:fresh-import:mapping"]
            == (HERE / "mapping.json").read_bytes()
        )
        assert (
            retained_evidence["artifact:small-shop:fresh-import:adapter"]
            == (HERE / "adapter.py").read_bytes()
        )
        assert {d["locator"] for d in trace.derivations} == {
            f"row:{row_index}:{field}"
            for field in (
                "source_occurrence_id",
                "supplier_order_id",
                "product_code",
                "ordered_quantity",
            )
        }
        assert rows[0]["source_occurrence_id"] == occurrence
    assert isolated.read_bytes() == path.read_bytes()


def test_stale_import_refuses_after_evidence_only_append(tmp_path):
    runner = _runner()
    history = runner.start_existing_shop(tmp_path / "shop")
    prepared = runner.prepare_import(
        history,
        (HERE / "supplier-orders.jsonl").read_bytes(),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    history.append_anchors(
        anchors=(
            runner.evidence_anchor("artifact:later", b"later evidence", "text/plain"),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    before = history.path.read_bytes()
    before_graph = history.replay().graph.export_records()
    with pytest.raises(api.KnowledgeChangeRefusal) as error:
        api.admit_structural_change(
            history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
        )
    assert error.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert history.path.read_bytes() == before
    assert (
        api.KnowledgeChangeHistory.reopen(history.path).replay().graph.export_records()
        == before_graph
    )


def test_adopter_has_no_private_core_import_or_handmade_check_outcome():
    for module in (_adapter(), _runner()):
        source = Path(module.__file__).read_text()
        imports = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom):
                imports.add(node.module or "")
            elif isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
        assert {name for name in imports if name.startswith("malleus")} <= {
            "malleus.compiler"
        }
        assert "_contract_pipeline" not in source
        assert "SATISFIED" not in source
        assert "CHECK_RECORDED" not in source
