"""The repository-level leak guard over the appendix evidence catalogue.

Deep-sweep defect D-16 in ``handover/2026-09-05-deep-sweep.md``: the leak rule
is enforced per cell, over each run's own ``FROZEN_ARTIFACTS`` set, and nothing
measures a file that belongs to no cell. Every snippet under ``snippets/`` and
``catalogue.md`` itself are exactly such files: the catalogue records a maximum
shared run for each snippet it added at the second read coordinate, and until
this module nothing recomputed those numbers or measured a snippet the
catalogue forgot to list.

**The rule is the one the freezes apply, unchanged.** With Unicode whitespace
collapsed to one space, a public file shares no run of ``LEAK_WINDOW`` = 60
characters with any block of ``private/paper-v4-text-layer/selected-reading.json``.
Blocks are enumerated separately, so no match crosses a block boundary. The
reference implementation is
``paper-v4/experiment-v4/run-15/test_contract.py::test_no_frozen_artifact_reproduces_the_reading``
with its ``LEAK_WINDOW``, ``_reading_windows`` and ``_plain``.

``_plain`` and ``_reading_windows`` below are **copied** from that module, not
imported. A run directory is a frozen cell: importing from one would make this
guard depend on a closed set that a later run is free to leave behind, and would
couple the repository-level check to one cell's lifetime. The copy is
deliberate; if the freezes ever change the measure, this file has to be changed
with them.

The measure is calibrated before it is trusted:
``test_the_measure_finds_the_known_leak_in_run_03s_first_ontology`` asserts a
hit on ``paper-v4/experiment-v4/run-03/ontology-run/ontology-01.yaml``, the leak
E-0124 located and justified (the article title, measured 73 by Paper-20). A
guard that cannot see a known leak fails here rather than passing everywhere.

Scope: ``catalogue.md`` and every file under ``snippets/``. Nothing else.
``paper-v4/paper-ledger.md``, the manuscript and the handovers are outside it
and several of them measure above the threshold on the article title; D-16's
full fix, a walk over every tracked file under ``paper-v4/`` and ``handover/``
with a named allowlist, is not built here.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import json
import re

import pytest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CATALOGUE = HERE / "catalogue.md"
SNIPPETS = HERE / "snippets"
SELECTED_READING = ROOT / "private" / "paper-v4-text-layer" / "selected-reading.json"
CALIBRATION = ROOT / "paper-v4/experiment-v4/run-03/ontology-run/ontology-01.yaml"

LEAK_WINDOW = 60

# A snippet file name, as the catalogue writes it: two digits, a hyphenated
# slug, and the extension. Anchored to the backticks so that a path mentioning
# a numbered file inside a longer name (`ontology-run/attempt-01-diagnostic.json`
# in the gaps list) is not read as a snippet reference.
SNIPPET_NAME = re.compile(r"`(\d\d-[a-z0-9-]+\.(?:txt|json))`")
# Each entry added at the second read coordinate is a bullet that opens with the
# snippet name and carries one digest before the next bullet.
CATALOGUE_ENTRY = re.compile(
    r"^- `(\d\d-[a-z0-9-]+\.(?:txt|json))`(.*?)(?=^- `|\Z)",
    re.MULTILINE | re.DOTALL,
)
RECORDED_DIGEST = re.compile(r"`sha256:([0-9a-f]{64})`")


def _plain(text: str) -> str:
    """Copied from run-15's ``test_contract.py``. Do not import it from there."""
    return " ".join(text.split())


def _reading_windows(width: int) -> set[str]:
    """Copied from run-15's ``test_contract.py``. Do not import it from there."""
    reading = json.loads(SELECTED_READING.read_bytes())
    windows: set[str] = set()
    for page in reading["pages"]:
        for block in page["blocks"]:
            plain = _plain(block["text"])
            for start in range(0, max(1, len(plain) - width + 1)):
                piece = plain[start : start + width]
                if len(piece) == width:
                    windows.add(piece)
    return windows


@lru_cache(maxsize=1)
def _windows() -> frozenset[str]:
    return frozenset(_reading_windows(LEAK_WINDOW))


def _shared_runs(text: str) -> list[str]:
    """Every ``LEAK_WINDOW``-character window of ``text`` that a block contains."""
    windows = _windows()
    plain = _plain(text)
    return [
        plain[start : start + LEAK_WINDOW]
        for start in range(0, max(1, len(plain) - LEAK_WINDOW + 1))
        if plain[start : start + LEAK_WINDOW] in windows
    ]


def _leaking(paths: list[Path]) -> dict[str, str]:
    """The first shared run of each path that reproduces the reading."""
    found: dict[str, str] = {}
    for path in paths:
        shared = _shared_runs(path.read_text(encoding="utf-8"))
        if shared:
            found[path.name] = shared[0]
    return found


def _catalogue_files() -> list[Path]:
    return [CATALOGUE, *sorted(SNIPPETS.iterdir())]


def _recorded_digests() -> dict[str, str]:
    text = CATALOGUE.read_text(encoding="utf-8")
    recorded: dict[str, str] = {}
    for name, body in CATALOGUE_ENTRY.findall(text):
        digests = set(RECORDED_DIGEST.findall(body))
        if len(digests) == 1:
            recorded[name] = digests.pop()
    return recorded


def test_no_catalogue_file_reproduces_the_reading() -> None:
    """The guard itself: catalogue.md and every snippet, at the freeze rule."""
    files = _catalogue_files()

    assert files, "the catalogue set is empty; the guard would measure nothing"
    # The failure names the files and never quotes the run it found: a guard
    # that printed the leak would put the reading in the test log.
    leaking = _leaking(files)
    assert leaking == {}, sorted(leaking)


def test_the_catalogue_and_the_snippet_directory_name_the_same_files() -> None:
    """No snippet may sit under snippets/ unlisted, and so unmeasured above."""
    named = set(SNIPPET_NAME.findall(CATALOGUE.read_text(encoding="utf-8")))
    present = {path.name for path in SNIPPETS.iterdir()}

    assert named - present == set(), "the catalogue names a snippet that is absent"
    assert present - named == set(), "a snippet sits under snippets/ unlisted"


def test_every_recorded_snippet_digest_matches_its_file() -> None:
    """The digests the catalogue records, against the bytes on disk.

    Only the entries added at the second read coordinate record a digest;
    sections 1 to 12 name their snippets in tables and record none. Those files
    are still measured and still held to the naming bijection above.
    """
    recorded = _recorded_digests()
    if not recorded:
        pytest.skip("the catalogue records no digest in a parseable form")

    present = {path.name for path in SNIPPETS.iterdir()}
    assert set(recorded) <= present
    for name, digest in sorted(recorded.items()):
        assert sha256((SNIPPETS / name).read_bytes()).hexdigest() == digest, name


def test_the_measure_finds_the_known_leak_in_run_03s_first_ontology() -> None:
    """Calibration. E-0124's located leak, measured 73 by Paper-20.

    A guard that reports nothing everywhere is indistinguishable from a guard
    that cannot see. This one is required to fire on the one public file in the
    tree that is known to carry a run over the threshold.
    """
    if not CALIBRATION.is_file():
        pytest.skip(f"the calibration file is not in the tree: {CALIBRATION}")

    shared = _shared_runs(CALIBRATION.read_text(encoding="utf-8"))

    assert shared != [], "the measure found no run in a file known to carry one"
    assert len(shared[0]) == LEAK_WINDOW


def test_a_snippet_that_copied_a_reading_block_fails_the_leak_test(
    tmp_path: Path,
) -> None:
    """The negative control for ``test_no_catalogue_file_reproduces_the_reading``.

    A snippet that copied one reading block is written to a temporary directory,
    never to ``snippets/``, and the same measure the guard runs is asked about
    it. That test, and only that one, is what such a snippet would break: the
    naming and digest tests would pass, because a copied block can be listed and
    hashed like any other file.
    """
    reading = json.loads(SELECTED_READING.read_bytes())
    blocks = [
        block["text"]
        for page in reading["pages"]
        for block in page["blocks"]
        if len(_plain(block["text"])) >= LEAK_WINDOW
    ]
    assert blocks, "no reading block is long enough to measure"

    leaked = tmp_path / "99-copied-reading-block.txt"
    leaked.write_text(
        f"# source: a reading block, copied\n\n{blocks[0]}\n", encoding="utf-8"
    )

    assert _leaking([leaked]) != {}
    assert _leaking(_catalogue_files()) == {}
