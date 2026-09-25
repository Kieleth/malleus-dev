"""Run the whole gate once and print the tables RESULTS.md carries.

    PYTHONPATH=src:. python design/temporal/g3/report.py > /tmp/g3-tables.md
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))

import blast_radius  # noqa: E402
import obligations  # noqa: E402
import probes  # noqa: E402
import queries  # noqa: E402
import refusals  # noqa: E402
from driver import SPECIMENS, build  # noqa: E402


def run_all(workdir: Path) -> dict:
    runs = {key: build(key, workdir) for key in SPECIMENS}
    before = {key: run.path.read_bytes() for key, run in runs.items()}
    refused = refusals.run_refusals(runs, workdir)
    after_refusal = {o.refusal_id: o.history_after for o in refused}
    outcomes = [o for run in runs.values() for o in queries.evaluate_specimen(run, after_refusal)]
    unchanged = {key: runs[key].path.read_bytes() == before[key] for key in runs}
    return {
        "runs": runs,
        "queries": outcomes,
        "refusals": refused,
        "probes": probes.run_probes(runs, workdir),
        "rebuild": {key: obligations.rebuild(run) for key, run in runs.items()},
        "round_trip": {key: obligations.round_trip(run) for key, run in runs.items()},
        "reads_wrote_nothing": unchanged,
        "blast": blast_radius.scenarios(runs["g1-01"].history.replay().change_sets[0]),
    }


def short(value, width=90) -> str:
    text = json.dumps(value, default=str) if not isinstance(value, str) else value
    return text if len(text) <= width else text[: width - 3] + "..."


def tables(result: dict) -> str:
    lines = []
    counts = Counter(o.classification for o in result["queries"])
    lines.append("## Counts\n")
    lines.append(f"Query answers (open-choice queries counted once per branch): {dict(counts)}, total {sum(counts.values())}")
    lines.append(f"Refusals: {dict(Counter(o.classification for o in result['refusals']))}, total {len(result['refusals'])}\n")
    lines.append("## Changes\n")
    lines.append("| Specimen | Position | Declared kind | Core outcome | Notes |")
    lines.append("|---|---|---|---|---|")
    for key, run in result["runs"].items():
        for log in run.logs:
            refused = [f"{a.stage}/{a.reason}: {a.detail}" for a in log.attempts if a.outcome == "REFUSED"]
            note = "; ".join(refused + log.notes)
            lines.append(f"| {key} | {log.position} | {log.kind} | {log.outcome} | {note} |")
    lines.append("\n## Queries\n")
    lines.append("| Specimen | Query | Kind | Branch | Class | Wrong (Core vs expected) | Not expressible | Reason | Core gave | Harness did | Harness naive | Notes |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for o in result["queries"]:
        wrong = "; ".join(f"{f.name}: {short(f.core, 30)} vs {short(f.expected, 30)}" for f in o.fields if f.status == queries.CORE_WRONG)
        missing = ", ".join(f.name for f in o.fields if f.status == queries.NE)
        reasons = "; ".join(dict.fromkeys(f.note for f in o.fields if f.status != queries.CORE and f.note))
        naive = "; ".join(f"{m} {v['verdict']}" for m, v in o.naive.items())
        notes = " ".join(o.notes + [f"FORBIDDEN MATCH: {h}" for h in o.forbidden_hit])
        lines.append(f"| {o.specimen} | {o.query_id} | {o.kind} | {o.branch or ''} | {o.classification} | {wrong} | {missing} | {reasons} | {o.core_part} | {o.harness_part} | {naive} | {notes} |")
    lines.append("\n## Refusals\n")
    lines.append("| Specimen | Refusal | Expected category | Class | Procedure steps (stage/reason: detail) | Alternatives | Ledger bytes around each admission |")
    lines.append("|---|---|---|---|---|---|---|")
    for o in result["refusals"]:
        steps = "; ".join(f"{'supersede ' if a.supersedes else ''}{a.outcome} {a.stage or ''}/{a.reason or ''}: {a.detail or ''}" for a in o.procedure)
        alts = "; ".join(f"{k}: " + ", ".join(f"{a.outcome} {a.stage or ''}/{a.reason or ''}" for a in v) for k, v in o.alternatives.items())
        byte_note = "; ".join(f"{a.bytes_before} -> {'same' if a.bytes_before == a.bytes_after else a.bytes_after}" for a in o.procedure)
        lines.append(f"| {o.specimen} | {o.refusal_id} | {o.expected_category} | {o.classification} | {steps} | {alts} | {byte_note} |")
    return "\n".join(lines)


if __name__ == "__main__":
    result = run_all(Path(tempfile.mkdtemp()))
    print(tables(result))
    print("\n## Probes\n")
    print(json.dumps(result["probes"], indent=1, default=str))
    print("\n## Obligations\n")
    print(json.dumps({"rebuild": result["rebuild"], "round_trip": result["round_trip"], "reads_wrote_nothing": result["reads_wrote_nothing"]}, indent=1, default=str))
