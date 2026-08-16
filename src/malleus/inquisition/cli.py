"""Command-line entry for the Ordo Malleus mechanical rites.

Usage:
    malleus-inquisitor path/to/schema.yaml
    malleus-inquisitor path/to/schema.yaml --map malleus=vendor/malleus.yaml --json
    malleus-inquisitor install-skills [--user | --project DIR]

Exit code 0 with a purity seal, 1 when heresies are recorded, 2 on bad usage
or a broken instrument (an unreadable or malformed rubric). A broken subject
is a finding; a broken instrument is never reported as one, because an
operator reading exit 1 must be able to trust that their schema was judged.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import sysconfig
from pathlib import Path

from malleus.inquisition import (
    COMMENDATION,
    HERESY,
    NOTE,
    SUSPICION,
    RubricError,
    run_rites,
)

_BADGES = {HERESY: "✠ HERESY     ", SUSPICION: "? suspicion  ",
           NOTE: "· note       ", COMMENDATION: "+ commended  "}


def _bundled_skills_dir() -> Path:
    """Resolve the shipped skills, source tree first, installed data second."""
    source = Path(__file__).resolve().parents[3] / ".claude" / "skills"
    if source.is_dir():
        return source
    installed = Path(sysconfig.get_path("data")) / "share" / "malleus" / "skills"
    if installed.is_dir():
        return installed
    raise FileNotFoundError(
        "Bundled skills not found in the source tree or the installed data "
        "directory; reinstall malleus-dev or run from a checkout."
    )


def _install_skills(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="malleus-inquisitor install-skills",
        description="Copy the shipped agent skills into a .claude/skills directory.",
    )
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--user", action="store_true",
                        help="install into ~/.claude/skills (every project on this machine)")
    target.add_argument("--project", metavar="DIR", default=None,
                        help="install into DIR/.claude/skills (default: current directory)")
    args = parser.parse_args(argv)

    base = Path.home() if args.user else Path(args.project or ".")
    destination = base / ".claude" / "skills"
    destination.mkdir(parents=True, exist_ok=True)
    installed = []
    for skill_dir in sorted(_bundled_skills_dir().iterdir()):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        shutil.copytree(skill_dir, destination / skill_dir.name, dirs_exist_ok=True)
        installed.append(skill_dir.name)
    for name in installed:
        print(f"installed skill: {name} -> {destination / name}")
    print("Re-run after upgrading malleus-dev; new rites exist because "
          "someone paid for them.")
    return 0 if installed else 1


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] == "install-skills":
        return _install_skills(argv[1:])
    parser = argparse.ArgumentParser(
        prog="malleus-inquisitor",
        description="Ordo Malleus: mechanical rites over a malleus-derived schema.",
    )
    parser.add_argument("schema", help="path to the project's LinkML schema")
    parser.add_argument("--map", action="append", default=[], metavar="NAME=PATH",
                        help="import map entry, repeatable (e.g. malleus=vendor/malleus.yaml)")
    parser.add_argument("--root", default=None,
                        help="path to the reference malleus root (default: the installed one)")
    parser.add_argument("--rubric", default=None, metavar="PATH",
                        help="path to a tuned rubric (default: the packaged one). "
                             "Tune severities and set `enabled: false` in a copy; "
                             "editing the packaged file is reverted by the next upgrade")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    import_map: dict[str, str] = {}
    for entry in args.map:
        if "=" not in entry:
            parser.error(f"--map entries take NAME=PATH form, got {entry!r}")
        name, _, path = entry.partition("=")
        import_map[name] = path

    try:
        report = run_rites(args.schema, import_map=import_map or None,
                           root_path=args.root, rubric_path=args.rubric)
    except RubricError as exc:
        # The rubric is the instrument, never the subject. Exit 2 keeps this
        # distinguishable from exit 1 ("your schema has heresies") for any CI
        # gate keyed on the documented codes, and no traceback reaches an
        # operator who would read it as a fault in their own schema.
        print(f"malleus-inquisitor: broken rubric, no schema was judged: {exc}",
              file=sys.stderr)
        return 2

    if args.json:
        print(report.to_json())
        return 0 if report.purity else 1

    rites = report.rites
    disabled, downgraded = rites.disabled, rites.downgraded
    # The version and the resolved root, on every run. An adopter reading a
    # current rubric while running a package several minor versions old sees
    # a confusing ImportError instead of a version complaint; one command
    # should answer "which malleus am I actually running against".
    import malleus
    from malleus.ontology import bundled_ontology_path
    try:
        root_used = str(Path(args.root).resolve()) if args.root \
            else str(bundled_ontology_path("malleus.yaml").resolve())
    except Exception:  # noqa: BLE001 - reporting must never outrank the report
        root_used = args.root or "<no bundled root found>"
    print(f"ORDO MALLEUS :: inquisition of {args.schema}")
    print(f"malleus {malleus.__version__}, root {root_used}")
    print(f"rubric {rites.path} (v{rites.version}, sha256 {rites.digest[:12]}…)")
    print(f"{len(rites.disabled_mechanical)} mechanical and "
          f"{len(rites.disabled_judgment)} judgment rites disabled"
          + (f": {', '.join(disabled)}" if disabled else "")
          + (f"; {len(downgraded)} downgraded: {', '.join(downgraded)}"
             if downgraded else ""))
    print("=" * 60)
    for finding in report.findings:
        print(f"{_BADGES[finding.severity]}[{finding.rite}] {finding.subject}")
        print(f"              {finding.message}")
    print("=" * 60)
    heresies = len(report.heresies)
    if report.purity:
        # A seal is only as wide as the rubric that granted it, and it says so
        # on its face: silence from a rite that never ran is not a pass.
        print("PURITY SEAL GRANTED"
              + (f" UNDER A TUNED RUBRIC ({len(disabled)} disabled, "
                 f"{len(downgraded)} downgraded). "
                 "The unjudged are not thereby innocent."
                 if rites.narrowed else ". The schema may serve."))
        return 0
    if report.unconstructed:
        # The floor the rubric cannot lower. Say which floor, so nobody hunts
        # for a heresy that is not there.
        print("NO SEAL: the schema did not construct, so nothing could be "
              "judged. No rubric severity lowers this.")
        return 1
    print(f"{heresies} {'heresies' if heresies != 1 else 'heresy'} recorded. "
          "No seal until the schema recants.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
