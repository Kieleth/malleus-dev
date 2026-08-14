"""Command-line entry for the Ordo Malleus mechanical rites.

Usage:
    malleus-inquisitor path/to/schema.yaml
    malleus-inquisitor path/to/schema.yaml --map malleus=vendor/malleus.yaml --json

Exit code 0 with a purity seal, 1 when heresies are recorded, 2 on bad usage.
"""

from __future__ import annotations

import argparse
import sys

from malleus.inquisition import COMMENDATION, HERESY, NOTE, SUSPICION, run_rites

_BADGES = {HERESY: "✠ HERESY     ", SUSPICION: "? suspicion  ",
           NOTE: "· note       ", COMMENDATION: "+ commended  "}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="malleus-inquisitor",
        description="Ordo Malleus: mechanical rites over a malleus-derived schema.",
    )
    parser.add_argument("schema", help="path to the project's LinkML schema")
    parser.add_argument("--map", action="append", default=[], metavar="NAME=PATH",
                        help="import map entry, repeatable (e.g. malleus=vendor/malleus.yaml)")
    parser.add_argument("--root", default=None,
                        help="path to the reference malleus root (default: the installed one)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    import_map: dict[str, str] = {}
    for entry in args.map:
        if "=" not in entry:
            parser.error(f"--map entries take NAME=PATH form, got {entry!r}")
        name, _, path = entry.partition("=")
        import_map[name] = path

    report = run_rites(args.schema, import_map=import_map or None, root_path=args.root)

    if args.json:
        print(report.to_json())
        return 0 if report.purity else 1

    print(f"ORDO MALLEUS :: inquisition of {args.schema}")
    print("=" * 60)
    for finding in report.findings:
        print(f"{_BADGES[finding.severity]}[{finding.rite}] {finding.subject}")
        print(f"              {finding.message}")
    print("=" * 60)
    heresies = len(report.heresies)
    if report.purity:
        print("PURITY SEAL GRANTED. The schema may serve.")
        return 0
    print(f"{heresies} heresy{'ies' if heresies != 1 else ''} recorded. "
          "No seal until the schema recants.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
