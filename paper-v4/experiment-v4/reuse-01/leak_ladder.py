"""Measure how much of the selected reading a file reproduces.

The rule this implements is run-25's, in
``paper-v4/experiment-v4/run-25/results/withheld-artifacts.json``: nothing that
shares a sixty-character normalized run with a reading block leaves ``private/``.
The measurement is the same one ``run-25/freeze.py`` and
``baseline-01/validate_answers.py`` use, and the normalization is the one every
cell's leak check uses, ``" ".join(text.split())``.

For each file named on the command line it prints the highest rung of the ladder
the file reaches and the path, one per line, which is the format
``run-25/freeze.py`` reads. A file that shares no forty-character run prints 0.

    .venv/bin/python paper-v4/experiment-v4/reuse-01/leak_ladder.py FILE...
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


READING = Path("private/paper-v4-text-layer/selected-reading.json")
LADDER = (40, 60, 80, 120, 200, 320)
LEAK_WINDOW = 60


def plain(text: str) -> str:
    return " ".join(text.split())


def windows(reading: dict, width: int) -> set[str]:
    found: set[str] = set()
    for page in reading["pages"]:
        for block in page["blocks"]:
            text = plain(block["text"])
            for start in range(0, max(1, len(text) - width + 1)):
                piece = text[start : start + width]
                if len(piece) == width:
                    found.add(piece)
    return found


def shares(text: str, haystack: set[str], width: int) -> bool:
    for start in range(0, max(1, len(text) - width + 1)):
        piece = text[start : start + width]
        if len(piece) == width and piece in haystack:
            return True
    return False


def measure(paths: list[Path], reading_path: Path = READING) -> dict[str, int]:
    reading = json.loads(reading_path.read_bytes())
    by_width = {width: windows(reading, width) for width in LADDER}
    result: dict[str, int] = {}
    for path in paths:
        text = plain(path.read_text(encoding="utf-8", errors="replace"))
        reached = 0
        for width in LADDER:
            if shares(text, by_width[width], width):
                reached = width
            else:
                break
        result[str(path)] = reached
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--reading", type=Path, default=READING)
    arguments = parser.parse_args(argv)
    measured = measure(arguments.paths, arguments.reading)
    for path, rung in measured.items():
        print(f"{rung} {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
