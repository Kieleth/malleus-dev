"""Command-line interface for Malleus Recon."""

from __future__ import annotations

import argparse
import json
import sys
from malleus.ledger import LedgerError
from malleus.recon.analysis import build_outputs, compare_subjects, visualize
from malleus.recon.import_v1 import import_literature_kg_v1
from malleus.recon.store import ReconError, ReconProject, load_record_file


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="malleus-recon",
        description="Evidence-first, typed literature review and claim comparison.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    initialize = subcommands.add_parser("init", help="create one local Recon project")
    initialize.add_argument("directory")
    initialize.add_argument("--title", required=True)
    initialize.add_argument("--target", required=True, dest="target_id")
    initialize.add_argument("--actor", required=True, dest="creator_id")

    record = subcommands.add_parser("record", help="validate and record one JSON candidate")
    record.add_argument("directory")
    record.add_argument("record_type")
    record.add_argument("record_file")
    record.add_argument("--actor", required=True, dest="actor_id")
    record.add_argument("--supersedes", default=None, dest="supersedes_event_id")

    validate = subcommands.add_parser("validate", help="replay and validate the project")
    validate.add_argument("directory")

    build = subcommands.add_parser("build", help="generate deterministic review artifacts")
    build.add_argument("directory")
    build.add_argument("--output", default=None)

    compare = subcommands.add_parser("compare", help="compare two recorded review subjects")
    compare.add_argument("directory")
    compare.add_argument("target_id")
    compare.add_argument("work_id")

    graph = subcommands.add_parser("visualize", help="write an interactive HTML graph")
    graph.add_argument("directory")
    graph.add_argument("--output", default=None)

    importer = subcommands.add_parser(
        "import-v1", help="import one canonical literature-forensics graph v1.x"
    )
    importer.add_argument("directory")
    importer.add_argument("source")
    importer.add_argument("--actor", required=True, dest="actor_id")
    importer.add_argument("--allow-unmapped", action="store_true")
    return parser


def _run(args: argparse.Namespace) -> int:
    if args.command == "init":
        project = ReconProject.initialize(
            args.directory,
            title=args.title,
            target_id=args.target_id,
            creator_id=args.creator_id,
        )
        print(f"created Recon project: {project.root}")
        print(f"ontology: {project.ontology_hash}")
        return 0

    project = ReconProject(args.directory)
    if args.command == "record":
        event = project.record(
            args.record_type,
            load_record_file(args.record_file),
            actor_id=args.actor_id,
            supersedes_event_id=args.supersedes_event_id,
        )
        payload = event["payload"]
        print(f"{payload['decision']}: {event['event_id']} {payload['candidate_hash']}")
        for error in payload["errors"]:
            print(f"  {error}")
        return 0 if payload["decision"] == "RECORDED" else 1
    if args.command == "validate":
        events, state = project.snapshot()
        errors = project.validate(state)
        if errors:
            for error in errors:
                print(f"invalid: {error}")
            return 1
        print(
            f"valid: {len(state)} current records, "
            f"{len(events)} ledger events"
        )
        return 0
    if args.command == "build":
        paths = build_outputs(project, args.output)
        for name, path in sorted(paths.items()):
            print(f"built {name}: {path}")
        return 0
    if args.command == "compare":
        print(
            json.dumps(
                compare_subjects(project, args.target_id, args.work_id),
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    if args.command == "import-v1":
        print(
            json.dumps(
                import_literature_kg_v1(
                    project,
                    args.source,
                    actor_id=args.actor_id,
                    allow_unmapped=args.allow_unmapped,
                ),
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    path = visualize(project, args.output)
    print(f"built interactive graph: {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    try:
        args = parser.parse_args(sys.argv[1:] if argv is None else argv)
        return _run(args)
    except (ReconError, LedgerError, OSError) as error:
        print(f"malleus-recon: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
