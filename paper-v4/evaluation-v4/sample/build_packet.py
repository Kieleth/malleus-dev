"""Build the private, blind judging packet for a drawn sample.

The packet carries, per sampled witness, the fields the query returned for it and
the full text of every block its recorded locators cite. It carries no recorded
label and no recorded rationale: the judge must not see what the first review
decided. It reproduces reading text, so it is written under `private/` and the
builder refuses any other destination.

    .venv/bin/python paper-v4/evaluation-v4/sample/build_packet.py \
        --sample paper-v4/evaluation-v4/sample/sample-20260911.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sample_common import (  # noqa: E402
    PACKET_SCHEMA,
    ROOT,
    Refusal,
    digest,
    load_sample,
    markdown_record,
    read_json,
    reading_blocks,
    refuse,
    write_json,
)


DEFAULT_OUTPUT = Path("private/paper-v4-evaluation-sample")


def _material(manifest: dict, name: str, cell: str) -> dict:
    for material in manifest.get("materials", []):
        if isinstance(material, dict) and material.get("name") == name:
            return material
    refuse(f"{cell} review input manifest declares no {name} material")
    raise AssertionError  # unreachable


def _bound(root: Path, material: dict, cell: str, name: str) -> bytes:
    path = root / material["path"]
    if not path.exists():
        refuse(f"{cell} {name} is missing: {path}")
    source = path.read_bytes()
    if digest(source) != material.get("sha256"):
        refuse(f"{cell} {name} differs from the digest its review input manifest binds")
    return source


def _payloads(query_result: dict, cell: str) -> dict[str, dict]:
    """One returned payload per distinct witness, refusing if a witness has two."""

    payloads: dict[str, dict] = {}
    for query in query_result.get("queries", []):
        for position, row in enumerate(query.get("rows", [])):
            witness = row.get("witness")
            if not isinstance(witness, dict):
                refuse(f"{cell} query result row {position} carries no witness object")
            key = witness.get("relation_id") or witness.get("record_id")
            if not isinstance(key, str) or not key:
                refuse(f"{cell} query result row {position} carries no witness identity")
            payload = {name: value for name, value in row.items() if name != "case_ordinals"}
            seen = payloads.get(key)
            if seen is None:
                payloads[key] = payload
            elif json.dumps(seen, sort_keys=True) != json.dumps(payload, sort_keys=True):
                refuse(f"{cell} witness {key} is returned with two different payloads")
    return payloads


def build(root: Path, sample: dict, sample_sha256: str) -> dict:
    cells = {}
    for entry in sample["cells"]:
        cell = entry["cell"]
        record = root / entry["record_path"]
        if not record.exists():
            refuse(f"{cell} review record is missing: {record}")
        if digest(record.read_bytes()) != entry["record_sha256"]:
            refuse(
                f"{cell} review record changed after the sample was drawn; draw the sample again"
            )
        markdown_record(record.read_bytes(), f"{cell} review record")
        manifest_path = root / "paper-v4" / "evaluation-v4" / cell / "review-input-manifest.json"
        manifest = read_json(manifest_path, f"{cell} review input manifest")
        if not isinstance(manifest, dict):
            refuse(f"{cell} review input manifest must be an object")
        reading_material = _material(manifest, "selected_reading", cell)
        query_material = _material(manifest, "query_result", cell)
        reading_source = _bound(root, reading_material, cell, "selected reading")
        query_source = _bound(root, query_material, cell, "query result")
        fixed = manifest.get("fixed_identities", {})
        if fixed.get("selected_reading_sha256") != reading_material.get("sha256"):
            refuse(f"{cell} manifest binds a selected reading its fixed identities do not name")
        reading = json.loads(reading_source)
        query_result = json.loads(query_source)
        cells[cell] = {
            "blocks": reading_blocks(reading),
            "payloads": _payloads(query_result, cell),
            "reading_sha256": reading_material["sha256"],
            "query_result_sha256": query_material["sha256"],
        }

    witnesses = []
    for entry in sample["witnesses"]:
        cell = entry["cell"]
        if cell not in cells:
            refuse(f"sample names a witness in {cell}, which the sample's cells do not list")
        loaded = cells[cell]
        key = entry["witness_key"]
        payload = loaded["payloads"].get(key)
        if payload is None:
            refuse(f"{cell} query result returns no witness {key}")
        cited = []
        for locator in entry["source_locators"]:
            text = loaded["blocks"].get(locator)
            if text is None:
                refuse(f"{cell} witness {key} cites {locator}, which is not a reading block id")
            cited.append({"id": locator, "text": text})
        witnesses.append(
            {
                "cell": cell,
                "witness_key": key,
                "kind": payload.get("kind"),
                "returned": payload,
                "cited_blocks": cited,
                "judgement": {"source_support": None, "rationale": None},
            }
        )

    return {
        "schema": PACKET_SCHEMA,
        "visibility": "PRIVATE",
        "reproduces": "SELECTED_READING_BLOCK_TEXT",
        "sample_sha256": sample_sha256,
        "seed": sample["seed"],
        "size": sample["size"],
        "blind": "NO_RECORDED_SOURCE_SUPPORT_NO_RECORDED_RATIONALE_NO_STRATUM_LABEL",
        "cells": [
            {
                "cell": entry["cell"],
                "sampled": entry["sampled"],
                "record_sha256": entry["record_sha256"],
                "reading_sha256": cells[entry["cell"]]["reading_sha256"],
                "query_result_sha256": cells[entry["cell"]]["query_result_sha256"],
            }
            for entry in sample["cells"]
        ],
        "witnesses": witnesses,
    }


def packet_name(seed: int, sample_sha256: str) -> str:
    """`packet-<seed>-<eight digest characters>.json`.

    Two strata drawn at one seed need two names, and the name is read by the
    judging session: naming a packet after its stratum would tell the judge the
    label every witness in it carries. Eight characters of the sample digest
    separate the files and say nothing.
    """

    return f"packet-{seed}-{sample_sha256.removeprefix('sha256:')[:8]}.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=f"directory the packet is written into (default {DEFAULT_OUTPUT})",
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = (args.output if args.output is not None else root / DEFAULT_OUTPUT).resolve()
    try:
        private = (root / "private").resolve()
        if private != output and private not in output.parents:
            refuse(f"the packet reproduces reading text and must stay under {private}: {output}")
        sample_source = args.sample.read_bytes()
        sample = load_sample(args.sample)
        sample_sha256 = digest(sample_source)
        packet = build(root, sample, sample_sha256)
        target = output / packet_name(sample["seed"], sample_sha256)
        write_json(target, packet)
    except Refusal as refusal:
        print(f"REFUSED: {refusal}", file=sys.stderr)
        return 2
    print(f"wrote {target}")
    print(f"  {len(packet['witnesses'])} witnesses, sample {packet['sample_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
