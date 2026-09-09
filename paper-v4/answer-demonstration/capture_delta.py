"""Read-only snapshot differences, not semantic equivalence or admission policy."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

FAMILIES = {"entities", "relations", "events", "signals", "event_participations"}


def indexed(records):
    if set(records) != FAMILIES:
        raise ValueError("export record families must be explicit and closed")
    result = {}
    for family, rows in records.items():
        for row in rows:
            key = row["id"]
            if key in result:
                raise ValueError("duplicate record identity")
            if not isinstance(row["properties"], dict) or not row["type"]:
                raise ValueError("record type and property mapping are required")
            result[key] = (family, row)
    return result


def compare(before, after):
    old, new = indexed(before), indexed(after)
    shared = old.keys() & new.keys()
    lost, changed, added = {}, {}, {}
    for key in sorted(old.keys() | new.keys()):
        previous = old[key][1]["properties"] if key in old else {}
        current = new[key][1]["properties"] if key in new else {}
        if previous.keys() - current.keys():
            lost[key] = sorted(previous.keys() - current.keys())
        if current.keys() - previous.keys():
            added[key] = sorted(current.keys() - previous.keys())
        differences = [
            k
            for k in previous.keys() & current.keys()
            if previous[k] != current[k] or type(previous[k]) is not type(current[k])
        ]
        if differences:
            changed[key] = sorted(differences)

    def numeric(index):
        return sum(
            type(value) in (int, float)
            for _, row in index.values()
            for value in row["properties"].values()
        )

    return {
        "removed_record_ids": sorted(old.keys() - new.keys()),
        "added_record_ids": sorted(new.keys() - old.keys()),
        "changed_record_ids": sorted(k for k in shared if old[k] != new[k]),
        "unchanged_record_ids": sorted(k for k in shared if old[k] == new[k]),
        "lost_properties": lost,
        "added_properties": added,
        "changed_properties": changed,
        "numeric_properties_before": numeric(old),
        "numeric_properties_after": numeric(new),
        "limit": "Exact identity and scalar-property comparison only. Renamed records and prose are not asserted semantically equivalent or different.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    before, after = args.before.read_bytes(), args.after.read_bytes()
    report = {
        "before_export_sha256": "sha256:" + sha256(before).hexdigest(),
        "after_export_sha256": "sha256:" + sha256(after).hexdigest(),
        **compare(json.loads(before), json.loads(after)),
    }
    with args.output.open("x") as stream:
        json.dump(report, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")
