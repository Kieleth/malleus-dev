"""Execute the main Shop instructions, including their public read path."""

from contextlib import redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import shlex
import subprocess
import sys

import malleus.compiler as api


ROOT = Path(__file__).resolve().parents[3]
GUIDE = ROOT / "docs/SMALL_SHOP_WALKTHROUGH.md"
SUPPLIER_SOURCE = ROOT / (
    "research/ontology_driven_kg_realization/fixtures/"
    "small_shop_fulfilment_correction_v1/input/sources/"
    "supplier-order-history.jsonl"
)
MODULE = (
    "research.ontology_driven_kg_realization.experiments.small_shop"
    ".default_admission.run"
)


def test_documented_default_run_reopens_queries_and_traces_exact_source(
    tmp_path: Path,
) -> None:
    guide = GUIDE.read_text()
    command = shlex.split(guide.split("```bash\n", 1)[1].split("```", 1)[0])
    assert command[:4] == ["python", "-m", MODULE, "--output"]
    assert len(command) == 5
    documented_output = Path(command[4])
    assert not documented_output.is_absolute()
    output = tmp_path / "fresh-shop"
    command[0] = sys.executable
    command[4] = str(output)
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)

    ledger = output / "history.jsonl"
    before = ledger.read_bytes()
    evidence_before = (output / "evidence.json").read_bytes()
    evidence = json.loads(evidence_before)
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    assert evidence["fixture"] == "small-shop-default-admission"
    assert (
        evidence["structural_bundle_identity"] == api.STRUCTURAL_HISTORY_BUNDLE.identity
    )
    assert evidence["ledger_sha256"] == "sha256:" + sha256(before).hexdigest()
    assert evidence["ledger_event_count"] == replay.ledger_event_count == 50
    assert evidence["change_count"] == len(replay.change_sets) == 5
    assert evidence["contract_revision_count"] == len(replay.contract_revisions) == 1
    assert len(replay.record_history) == len(evidence["records"]) == 10
    graph = replay.graph.snapshot()
    assert len(graph["nodes"]) + len(graph["relations"]) == 9

    section = guide.split("### Ask the rebuilt graph", 1)[1]
    code = section.split("```python\n", 1)[1].split("```", 1)[0]
    documented_ledger = str(documented_output / "history.jsonl")
    assert code.count(documented_ledger) == 1
    code = code.replace(documented_ledger, str(ledger))
    namespace: dict[str, object] = {}
    printed = StringIO()
    with redirect_stdout(printed):
        exec(compile(code, str(GUIDE), "exec"), namespace)
    assert printed.getvalue().splitlines() == [
        "2",
        "supplier-order-state:B:e4",
        "row:1:quantity",
    ]
    trace = namespace["trace"]
    source = next(
        item
        for item in trace.sources
        if item.record_id == "source:small-shop:supplier-orders"
    )
    assert source.content == SUPPLIER_SOURCE.read_bytes()
    assert source.identity == "sha256:" + sha256(source.content).hexdigest()
    assert ledger.read_bytes() == before

    repeated = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert repeated.returncode != 0
    assert "FileExistsError" in repeated.stderr
    assert ledger.read_bytes() == before
    assert (output / "evidence.json").read_bytes() == evidence_before
