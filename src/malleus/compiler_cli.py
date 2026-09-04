"""Compile exact LinkML sources with the public Malleus compiler facade."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Sequence

from malleus.compiler import compile_linkml_contract


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="malleus-compiler", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    contract = commands.add_parser(
        "contract",
        help="compile one LinkML root from exact named source files",
    )
    contract.add_argument("--root", required=True, help="root source locator")
    contract.add_argument(
        "--source",
        action="append",
        nargs=2,
        required=True,
        metavar=("LOCATOR", "PATH"),
        help="exact source locator and file; repeat for every imported source",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    if arguments.command != "contract":
        parser.error("a supported compiler command is required")
    sources: dict[str, bytes] = {}
    try:
        for locator, raw_path in arguments.source:
            if locator in sources:
                raise ValueError(f"source locator is repeated: {locator}")
            sources[locator] = Path(raw_path).read_bytes()
        compilation = compile_linkml_contract(
            root_locator=arguments.root,
            sources=sources,
        )
    except (OSError, TypeError, ValueError) as error:
        print(f"malleus-compiler: {error}", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(compilation.artifact.artifact_bytes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
