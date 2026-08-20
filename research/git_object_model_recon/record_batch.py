#!/usr/bin/env python3
"""Record one Recon batch file through the shipped malleus-recon CLI.

Usage: record_batch.py records/01_foo.json [more.json ...]

Each batch file is a JSON array of {record_type, record, supersedes_event_id}.
Every item is handed to `malleus-recon record` one at a time; the CLI is the
only writer of ledger.jsonl. A rejection stops the batch so the operator sees
the exact validation errors before continuing.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ACTOR = "reviewer:git-object-recon"


def record_one(item: dict) -> bool:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(item["record"], handle, ensure_ascii=False, sort_keys=True)
        candidate = handle.name
    command = [
        "malleus-recon",
        "record",
        str(PROJECT),
        item["record_type"],
        candidate,
        "--actor",
        ACTOR,
    ]
    if item.get("supersedes_event_id"):
        command += ["--supersedes", item["supersedes_event_id"]]
    completed = subprocess.run(command, capture_output=True, text=True)
    output = (completed.stdout + completed.stderr).strip()
    Path(candidate).unlink(missing_ok=True)
    print(f"{item['record_type']:28} {item['record'].get('id', '?')}")
    if completed.returncode != 0:
        print(output)
        return False
    return True


def main(argv: list[str]) -> int:
    for name in argv:
        batch = json.loads(Path(name).read_text())
        print(f"### {name}: {len(batch)} records")
        for item in batch:
            if not record_one(item):
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
