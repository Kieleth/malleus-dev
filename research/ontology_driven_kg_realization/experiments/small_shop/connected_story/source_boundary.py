"""Read-only inventory of the selected Shop sources. No Core or graph writes."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


IDENTIFIER_FIELDS = (
    "actor_ids",
    "order_ids",
    "supplier_order_ids",
    "item_ids",
    "invoice_ids",
    "payment_ids",
)


def load_sources(directory: Path):
    boundary = json.loads((directory / "source_boundary.json").read_bytes())
    required = {"sources/table-1.png", "sources/table-1.jsonl", "sources/context.jsonl"}
    if set(boundary["artifacts"]) != required:
        raise ValueError("source inventory must bind the table image, rows and context")
    for relative, expected in boundary["artifacts"].items():
        actual = "sha256:" + sha256((directory / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"source digest differs: {relative}")
    rows = [
        json.loads(line)
        for line in (directory / "sources/table-1.jsonl").read_bytes().splitlines()
    ]
    return rows, boundary


def inspect_sources(rows, boundary):
    """Check the declared denominator without pretending it measures meaning."""

    ids = [row["event_id"] for row in rows]
    if ids != boundary["selected_event_ids"] or len(set(ids)) != len(ids):
        raise ValueError(
            "selected table rows are missing, repeated, reordered or added"
        )
    dispositions = boundary["field_dispositions"]
    if any(name != item["source_field"] for name, item in dispositions.items()):
        raise ValueError("field disposition refers to a different source field")
    coverage = []
    for ordinal, row in enumerate(rows):
        if not set(boundary["required_fields"]) <= row.keys():
            raise ValueError(f"required source fields absent at row {ordinal}")
        if row.keys() - dispositions.keys():
            raise ValueError(f"undeclared source fields at row {ordinal}")
        for field, value in row.items():
            if field in IDENTIFIER_FIELDS:
                if (
                    not isinstance(value, list)
                    or not value
                    or any(not isinstance(x, str) or not x for x in value)
                ):
                    raise ValueError(
                        f"nonempty source identifier list required: row:{ordinal}:{field}"
                    )
                if len(set(value)) != len(value):
                    raise ValueError(f"repeated identifier: row:{ordinal}:{field}")
            elif not isinstance(value, str) or not value:
                raise ValueError(
                    f"nonempty source text required: row:{ordinal}:{field}"
                )
            coverage.append(
                {
                    "event_id": row["event_id"],
                    "locator": f"row:{ordinal}:{field}",
                    "disposition": dispositions[field]["disposition"],
                }
            )
    return {
        "boundary_id": boundary["boundary_id"],
        "selected_rows": len(rows),
        "nonempty_fields": len(coverage),
        "inventory": {
            field: sorted(
                {value for row in rows if field in row for value in row[field]}
            )
            for field in IDENTIFIER_FIELDS
        },
        "coverage": coverage,
        "unaccounted_fields": [],
        "graph_populated": False,
        "semantic_coverage": "NOT_ASSESSED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory", nargs="?", type=Path, default=Path(__file__).resolve().parent
    )
    args = parser.parse_args()
    rows, boundary = load_sources(args.directory)
    print(json.dumps(inspect_sources(rows, boundary), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
