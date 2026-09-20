"""Project selected PS XML cells to source rows. No semantic mapping or population."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

import source_packet as packet


class ProjectionRefusal(ValueError):
    def __init__(self, reason, message):
        self.reason = reason
        super().__init__(f"{reason}: {message}")


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")


def _names(value):
    return (
        isinstance(value, list)
        and bool(value)
        and all(
            isinstance(item, str) and re.fullmatch(r"[A-Za-z0-9_]+", item)
            for item in value
        )
        and len(value) == len(set(value))
    )


def stage_selection(config, stage):
    """Resolve an explicitly requested stage, never infer it from output metadata."""
    if (
        not isinstance(config, dict)
        or set(config) != {"schema", "parent_sha256", "columns", "stages"}
        or config["schema"] != "exoplanet-table-selection/v1"
        or not isinstance(config["parent_sha256"], str)
        or not re.fullmatch(r"[0-9a-f]{64}", config["parent_sha256"])
        or not _names(config["columns"])
        or not isinstance(config["stages"], dict)
        or not isinstance(stage, str)
        or not stage.strip()
        or stage not in config["stages"]
    ):
        raise ProjectionRefusal(
            "INVALID_SELECTION", "supply the complete selection and a named stage"
        )
    selected = config["stages"][stage]
    if (
        not isinstance(selected, dict)
        or set(selected) != {"reference_ids"}
        or not _names(selected["reference_ids"])
    ):
        raise ProjectionRefusal(
            "INVALID_SELECTION", "stage requires unique reference IDs"
        )
    return {
        "stage": stage,
        "reference_ids": list(selected["reference_ids"]),
        "columns": list(config["columns"]),
    }


def project(data, spec, selection):
    """Return NDJSON and derivation bytes, preserving parsed XML cell strings/nulls."""
    if (
        not isinstance(data, bytes)
        or sha256(data).hexdigest() != packet.required(spec, "sha256")
        or len(data) != packet.required(spec, "bytes")
    ):
        raise ProjectionRefusal(
            "PARENT_MISMATCH", "supply the exact retained XML bytes"
        )
    try:
        table, fields, references = packet.read_ps_votable(data, spec)
    except ValueError as exc:
        raise ProjectionRefusal("SOURCE_INVALID", str(exc)) from exc
    headers = table[0]
    if (
        not isinstance(selection, dict)
        or set(selection) != {"stage", "reference_ids", "columns"}
        or not isinstance(selection["stage"], str)
        or not selection["stage"].strip()
        or not _names(selection["reference_ids"])
        or not _names(selection["columns"])
        or not set(selection["reference_ids"]) <= set(references)
        or not {"pl_name", "pl_refname"} <= set(selection["columns"]) <= set(headers)
    ):
        raise ProjectionRefusal(
            "INVALID_SELECTION",
            "select explicit unique rows and existing columns, including planet and reference",
        )
    indices = [references.index(reference) for reference in selection["reference_ids"]]
    columns = {name: headers.index(name) for name in selection["columns"]}
    rows = b"".join(
        canonical({name: table[index + 1][column] for name, column in columns.items()})
        + b"\n"
        for index in indices
    )
    metadata = canonical(
        {
            "schema": "exoplanet-source-projection/v1",
            "converter": "source_projection.project/v1",
            "parent_sha256": spec["sha256"],
            "selection": selection,
            "source_row_indices": indices,
            "rows_sha256": sha256(rows).hexdigest(),
            "fields": {
                name: {
                    "source_column_index": column,
                    "definition_xml": ElementTree.tostring(
                        fields[column], encoding="unicode"
                    ),
                }
                for name, column in columns.items()
            },
        }
    )
    return rows, metadata


def verify(data, spec, expected_selection, rows, metadata):
    if project(data, spec, expected_selection) != (rows, metadata):
        raise ProjectionRefusal(
            "PROJECTION_MISMATCH",
            "rebuild from the retained parent and externally selected stage",
        )


def trace_cell(data, spec, expected_selection, rows, metadata, locator):
    verify(data, spec, expected_selection, rows, metadata)
    match = (
        re.fullmatch(r"row:(0|[1-9][0-9]*):([A-Za-z0-9_]+)", locator)
        if isinstance(locator, str)
        else None
    )
    detail = json.loads(metadata)
    if (
        not match
        or int(match[1]) >= len(detail["source_row_indices"])
        or match[2] not in detail["fields"]
    ):
        raise ProjectionRefusal(
            "INVALID_LOCATOR", "use row:<zero-based row>:<selected field>"
        )
    row, field = int(match[1]), match[2]
    return {
        "parent_sha256": detail["parent_sha256"],
        "source_row_index": detail["source_row_indices"][row],
        **detail["fields"][field],
        "value": json.loads(rows.splitlines()[row])[field],
    }


def publish(destination, rows, metadata):
    """Publish a complete new directory; single-writer preparation only."""
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"refusing to overwrite {destination}")
    with TemporaryDirectory(
        prefix=".source-projection-", dir=destination.parent
    ) as scratch:
        ready = Path(scratch) / "ready"
        ready.mkdir()
        (ready / "rows.ndjson").write_bytes(rows)
        (ready / "derivation.json").write_bytes(metadata)
        ready.rename(destination)


def prepare(manifest, source_dir, config, stage):
    selection = stage_selection(config, stage)
    sources = [
        s
        for s in packet.required(manifest, "sources")
        if packet.required(s, "kind") == "archive_ps_votable"
    ]
    if len(sources) != 1 or config["parent_sha256"] != packet.required(
        sources[0], "sha256"
    ):
        raise ProjectionRefusal(
            "PARENT_MISMATCH", "selection must identify the single manifest PS source"
        )
    data = packet.verified_bytes(source_dir, sources[0])
    rows, metadata = project(data, sources[0], selection)
    verify(data, sources[0], selection, rows, metadata)
    return rows, metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "source-manifest.json").read_text())
    config = json.loads((root / "table-selections.json").read_text())
    source_dir = root.parents[1] / "private/paper-v4-exoplanets-lhs1140-01/sources"
    rows, metadata = prepare(manifest, source_dir, config, args.stage)
    publish(args.output, rows, metadata)
    print(
        json.dumps(
            {
                "stage": args.stage,
                "rows": len(rows.splitlines()),
                "columns": len(config["columns"]),
                "rows_sha256": sha256(rows).hexdigest(),
                "metadata_sha256": sha256(metadata).hexdigest(),
            },
            sort_keys=True,
        )
    )
