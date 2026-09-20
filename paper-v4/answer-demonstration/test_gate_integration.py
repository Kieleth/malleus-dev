"""The active paper gate must collect the answer harness in its declared mode."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def test_answer_harness_is_part_of_the_active_paper_gate():
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())
    assert "paper-v4/answer-demonstration" in manifest["paths"]
    assert "--import-mode=importlib" in manifest["pytest_args"]


def test_isolated_gate_declares_its_private_fixture_inputs():
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())
    assert manifest["private_fixture_patterns"] == [
        "private/paper-v4-text-layer",
        "private/paper-v4-v4-run-*",
        "private/paper-v4-v4-shop-01",
        "private/paper-v4-answer-demonstration",
        # Added 2026-09-12 with the in-context baseline and the independent-judge
        # sample; the list is pinned so a new private input is a deliberate edit.
        "private/paper-v4-baseline-01",
        "private/paper-v4-evaluation-sample",
        "private/paper-v4-reuse-01",
        "private/paper-v4-reuse-01-baseline",
        "private/paper-v4-relationship-contrast-01",
        # Added 2026-09-14 by the guided-amendment cut (E-0383 to E-0392); the
        # manifest carried it without this pin, so the gate was red until
        # 2026-09-16. Added the same day: the fault-injection cell (E-0402),
        # whose control test reads its private outputs.
        "private/paper-v4-relationship-repair-01",
        "private/paper-v4-fault-injection-01",
        # Added 2026-09-17 with the two cells that measure the candidate Core
        # e7937b89 (E-0429): the bridge replay of the seven frozen populations
        # and the rerun of the same 55 faults. Neither cell's tests read these
        # directories; they hold the retained run outputs the public
        # outcomes.json files are rendered from, and the isolated gate carries
        # a cell's evidence rather than leaving it on the machine that ran it.
        "private/paper-v4-bridge-01",
        "private/paper-v4-fault-injection-02",
        # Added 2026-09-17 with the two rule cells pinned to Core e7937b89
        # (E-0434, E-0435): the three document-path content rules and the
        # census that read every honest population before them. Neither cell's
        # tests read these directories; they hold the per-refusal detail the
        # public outcomes.json and RESULTS.md are rendered from, and the
        # isolated gate carries a cell's evidence rather than leaving it on
        # the machine that ran it.
        "private/paper-v4-content-rules-doc-01",
        "private/paper-v4-rule-census-01",
        # Added 2026-09-17 with the rule-adoption cell (E-0439, E-0445), which
        # runs the four adopted rules over the honest population and then over
        # the fault trials. No test reads this directory; one checks only that
        # git ignores the path. It holds the per-refusal detail and the
        # fault-trial outputs that outcomes.json, fault-outcomes.json and
        # RESULTS.md are rendered from.
        "private/paper-v4-content-rules-doc-02",
        # Added 2026-09-18 with shop-reconsideration-01, the cell that binds the
        # manuscript's Shop staged reconsideration (Section 3.2). Unlike the
        # cells above, this one's tests DO read these directories: every number
        # and digest the subsection prints is read out of a launched archive, a
        # producer verification file or an assessor's record. The paths are
        # narrow on purpose. The four Core exports beside them are a gigabyte of
        # a Core the gate pins by commit instead, and nothing here reads them.
        "private/shop-progressive-01/packets",
        "private/shop-progressive-01/producer/stage-a/archive",
        "private/shop-progressive-01/producer/stage-b/archive",
        "private/shop-progressive-01/producer/stage-c",
        "private/shop-progressive-01/assessment/stage-b-packet",
        "private/shop-progressive-01/assessment/stage-c-packet",
    ]
    assert manifest["private_fixture_excludes"] == ["*.pdf", "__pycache__/"]


# Every private output the manuscript's Shop staged reconsideration rests on,
# by path and by the digest it had when the subsection was written. A launched
# workspace is never rebuilt and a ratified record is never edited, so any
# movement here is a fact about the run that must be read before the paper is
# allowed to keep its sentence. The two binding files are public and pinned in
# the same list because the ratification claim is only as good as their bytes.
SHOP_RECONSIDERATION_PINS = {
    "private/shop-progressive-01/producer/stage-a/archive/2026-09-17T04:48:13Z/ARCHIVE.json": "8bcff240afc98c35cea400649a1f706655bdd0d30407782fce9cc3f90c1286cd",
    "private/shop-progressive-01/producer/stage-b/archive/2026-09-17T14:37:05Z/ARCHIVE.json": "ec2335eaf6382714b641f811e9e68623442696f2583515dddfb441528d5a998c",
    "private/shop-progressive-01/producer/stage-c/archive/2026-09-19T01:12:08Z/ARCHIVE.json": "6d624d962bfd70cac92634b4e31a18f6dfd0b7e5b7d0783b4c567edad4052146",
    "private/shop-progressive-01/producer/stage-c/review-coverage.json": "e240d837cd2c6da3dc05a562724c530dc279a798eb7f724746dfd742e1557aec",
    "private/shop-progressive-01/producer/stage-c/replay-verification.json": "b8ef94776e318b6869fc54c8280673d78ded21cbd00ff994439e93759481915f",
    "private/shop-progressive-01/producer/stage-c/revision-receipt.json": "a286dbef69dfaddcd1aaadc5c0f2ffbd87a15ece141da1007fa85c5a001e4e81",
    "private/shop-progressive-01/assessment/stage-b-packet/review-record.json": "d35ab5a9c7ec90157be62f4f1a1143afac00a79a8b8b607ad6b744980b92176b",
    "private/shop-progressive-01/assessment/stage-b-packet/review-record-ratified.json": "541130a46b54165b0507405cad22c8cfad6144f8e72c8ac75ccac8b256264de2",
    "private/shop-progressive-01/assessment/stage-c-packet/review-record.json": "90723d8fb9f97e2aeb0c8b0e64c394fc82e6616cd034677bc6225fae378420c5",
    "private/shop-progressive-01/assessment/stage-c-packet/review-record-ratified.json": "c4d001108edc5773ad48478de6a6f8b827fa1af454102cbf4bb5dffef0ec8310",
    "paper-v4/evaluation-v4/author-ratification-2026-09-17-shop-staged-review.md": "552592661bae1b4d27eb581f6fdccc91d7348e9c51da88c5a911c2e658d00cbc",
    "paper-v4/evaluation-v4/author-ratification-2026-09-18-shop-third-boundary.md": "ff172ee78de718330c60f9e8f287fb28dd795695a9324fbd9ad11c5dc2238256",
}


def test_the_shop_reconsideration_outputs_are_pinned_by_path_and_digest():
    for relative, expected in SHOP_RECONSIDERATION_PINS.items():
        path = ROOT / relative
        assert path.exists(), f"declared evidence is missing: {relative}"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == expected, f"{relative} moved: {actual}"


def test_the_shop_reconsideration_cell_is_registered_with_its_core_pin():
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())
    relative = "paper-v4/experiment-v4/shop-reconsideration-01/test_shop_reconsideration.py"
    assert relative in manifest["paths"]
    # The Core the gate exports for this cell. The pin moved on 2026-09-19 from
    # d5d014ba, the Core the third boundary and its certificate were produced
    # on, to the sealed one-call-admission Core, under E-0436. The run's own
    # Core stays recorded in the cell's replay verification and README. Two pin
    # entries now name this commit, so the entry is selected by the path it
    # holds and not by the commit alone.
    holders = [pin for pin in manifest["core_pins"] if relative in pin["paths"]]
    assert len(holders) == 1, "the cell is named by more than one Core pin"
    assert holders[0]["commit"] == "d89a0c4718654249ad678eaff62e7b1daba30b6f"
    assert holders[0]["paths"] == [relative]


def test_active_import_mode_collects_standalone_answer_modules():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--import-mode=importlib",
            "-q",
            "-p",
            "no:cacheprovider",
            str(HERE / "test_subject_answers.py"),
            "-k",
            "existing_subject_recovers",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
