"""The active-test runner materialises each declared Core pin from git history.

A frozen paper run replays only against the Core commit it was produced with
(answer-demonstration/pilot.py verify_runtime). The manifest therefore names
that commit per path group, and the runner exports ``src/malleus`` at that
commit from the repository's own history into a temporary directory placed
first on PYTHONPATH. No copy of Core is tracked twice and no path outside the
repository is an input to the gate.
"""
from __future__ import annotations

from hashlib import sha1
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "paper-v4"))

import run_active_tests as runner  # noqa: E402

MANIFEST = json.loads((ROOT / "paper-v4" / "active-test-manifest.json").read_bytes())


def test_manifest_declares_the_answer_demonstration_core_pin() -> None:
    """This pin did NOT move on 2026-09-19, and that is a measured refusal.

    E-0436 moves the paper's Core pin whenever Core moves, and on 2026-09-19
    the other two pins moved to the sealed one-call-admission Core
    ``d89a0c47``. This one was moved too and put back. Against a
    ``git archive`` of ``d89a0c47`` the group reads 30 failed, 631 passed,
    2 subtests passed. Twenty-nine of the failures are
    ``pilot.verify_runtime`` refusing before any Core work happens, because
    each frozen run's own manifest declares ``core_commit``
    ``160878cf14c0d27b11a440e26688708e9b7a7e2b`` and the harness compares the
    installed package with that tree before it will reproduce anything. The
    thirtieth, ``test_links_frozen_subject_reader_reproduces_baseline``, gets
    past that and is refused by Core itself with ``SOURCE_BINDING_REQUIRED``:
    the frozen populations of this lineage carry records whose type declares
    ``assertion_locator`` without setting it, which every Core from
    ``e7937b89`` onward refuses under the source-assertion profile. How many
    of the twenty-nine would also be refused on content is not established,
    because the runtime guard stops them first. Moving this pin therefore
    needs either the frozen run manifests rewritten or those populations
    produced again, and neither is a gate decision. Left at ``160878cf``,
    where the group is 661 passed plus 2 subtests, and reported.
    """

    pins = MANIFEST["core_pins"]
    assert len(pins) == 3
    pin = pins[0]
    assert pin["commit"] == "160878cf14c0d27b11a440e26688708e9b7a7e2b"
    assert pin["pythonpath"] == ["paper-v4/answer-demonstration"]
    assert set(pin["paths"]) == {
        "paper-v4/answer-demonstration",
        "paper-v4/submission-candidate/test_prepare.py",
    }
    assert set(pin["paths"]) <= set(MANIFEST["paths"])
    assert MANIFEST["pythonpath"] == [".", "src"]


def test_manifest_pins_the_rule_cells_to_the_current_core() -> None:
    """Every cell here asserts which Core it imported and which contract it declares.

    The census, the three document-path content rules and the four adopted
    rules were measured against Core e7937b89 (E-0434, E-0435, E-0439,
    E-0445), whose fact contract is version 3, and their RESULTS.md files
    still name that coordinate.

    The pin moved on 2026-09-19 from e7937b89917c8da7ee4a08acc22e99ad12b9985b
    to d89a0c4718654249ad678eaff62e7b1daba30b6f, the sealed Core carrying the
    one-call atomic admission ``check_and_admit_population_plan`` (E-0493,
    E-0494), under E-0436: when Core changes the paper's pin moves to it, the
    cells re-run on it and the new fingerprints are the baseline. Re-run
    through the gate's own mechanism on the new pin, the group is 184 passed,
    the same count and the same measurements as on e7937b89; the two Core
    fingerprints inside the cells moved from 52 modules
    sha256:d57f3cc9…b1355 to 53 modules sha256:340196…3ed04, and nothing else
    did. The fact contract is still version 3.
    """
    pin = MANIFEST["core_pins"][1]
    assert pin["commit"] == "d89a0c4718654249ad678eaff62e7b1daba30b6f"
    assert pin["pythonpath"] == []
    assert set(pin["paths"]) == {
        "paper-v4/experiment-v4/content-rules-doc-01/test_content_rules_doc.py",
        "paper-v4/experiment-v4/rule-census-01/test_census.py",
        "paper-v4/experiment-v4/rule-census-01/test_normalise.py",
        "paper-v4/experiment-v4/content-rules-doc-02/test_content_rules_doc_02.py",
    }
    assert set(pin["paths"]) <= set(MANIFEST["paths"])


def test_manifest_pins_the_shop_reconsideration_cell_to_the_current_core() -> None:
    """The third boundary, its completion certificate and the recorded ontology
    revision were produced against Core d5d014ba, whose governance head is
    OVR-000464. That stays recorded in the run's replay verification and in the
    cell's README; it is a fact about the run.

    The pin moved on 2026-09-19 from d5d014ba1d7e3bfe906bc71dc93ded5657a3b424
    to d89a0c4718654249ad678eaff62e7b1daba30b6f, the sealed Core carrying the
    one-call atomic admission, under E-0436. The cell reads frozen records and
    produces nothing, so the move changes which Core its assertions import and
    no measured value: re-run through the gate's own mechanism on the new pin
    the cell is 32 passed, as on d5d014ba. Its Core fingerprint moved from 52
    modules sha256:f2fd444d…e73c to 53 modules sha256:340196…3ed04, Core's own
    bytes, with ``_contract_pipeline/admission.py`` added.

    The cell asserts the imported Core by a digest over the package's own
    modules, so the pin has to hold in process; without it the checkout's
    ``src/malleus``, which carries gitignored modules no commit does, is what
    the cell would measure.
    """
    pin = MANIFEST["core_pins"][2]
    assert pin["commit"] == "d89a0c4718654249ad678eaff62e7b1daba30b6f"
    assert pin["pythonpath"] == []
    assert pin["paths"] == [
        "paper-v4/experiment-v4/shop-reconsideration-01/test_shop_reconsideration.py"
    ]
    assert set(pin["paths"]) <= set(MANIFEST["paths"])


def test_export_matches_the_pinned_git_tree_blob_for_blob() -> None:
    commit = MANIFEST["core_pins"][0]["commit"]
    with tempfile.TemporaryDirectory() as tmp:
        exported = runner.export_core(commit, Path(tmp))
        assert exported == Path(tmp) / "src"
        listing = subprocess.run(
            ["git", "ls-tree", "-r", commit, *runner.CORE_TREES],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        assert listing
        for line in listing:
            entry, name = line.split("\t")
            expected = entry.split()[2]
            data = (Path(tmp) / name).read_bytes()
            assert sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected, name


def test_the_export_carries_the_bundled_ontology_of_the_same_commit() -> None:
    """Core reads its bundled ontology from ``<root>/ontology``, beside ``src``.

    ``malleus.ontology.bundled_ontology_path`` resolves
    ``Path(malleus.__file__).parents[2] / "ontology"`` first, so an export of
    ``src/malleus`` alone raises OntologyError for every bundled profile the
    moment a pinned group loads one in process. The export is the pinned
    commit's runtime, not its package directory.
    """
    commit = MANIFEST["core_pins"][1]["commit"]
    with tempfile.TemporaryDirectory() as tmp:
        core = runner.export_core(commit, Path(tmp))
        probe = subprocess.run(
            [
                sys.executable,
                "-c",
                "from malleus.ontology import bundled_ontology_path\n"
                "print(bundled_ontology_path('profiles', 'object-event.yaml'))",
            ],
            cwd=ROOT,
            env={**os.environ, "PYTHONPATH": str(core), "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
        )
        assert probe.returncode == 0, probe.stdout + probe.stderr
        resolved = Path(probe.stdout.strip()).resolve()
        assert resolved.is_relative_to(Path(tmp).resolve()), probe.stdout


def test_plan_partitions_pinned_paths_and_orders_the_pin_first() -> None:
    """Two pin entries naming one commit stay two groups.

    Since 2026-09-19 the rule cells and the Shop reconsideration cell are both
    pinned to d89a0c47 and are still planned separately, because a group is a
    commit plus an import path and only the commit is shared. They export into
    the same directory, keyed by the commit, and the export is written once per
    group.
    """

    manifest, paths = runner.load_active_paths()
    plan = runner.plan(manifest, paths, export_root=Path("/exports"))
    assert [group["pin"] for group in plan] == [
        "160878cf14c0d27b11a440e26688708e9b7a7e2b",
        "d89a0c4718654249ad678eaff62e7b1daba30b6f",
        "d89a0c4718654249ad678eaff62e7b1daba30b6f",
        None,
    ]
    pinned, rules, shop, rest = plan
    assert set(pinned["paths"]) == set(manifest["core_pins"][0]["paths"])
    assert set(rules["paths"]) == set(manifest["core_pins"][1]["paths"])
    assert set(shop["paths"]) == set(manifest["core_pins"][2]["paths"])
    assert set(rest["paths"]) == (
        set(paths) - set(pinned["paths"]) - set(rules["paths"]) - set(shop["paths"])
    )
    assert pinned["pythonpath"][0] == str(Path("/exports") / pinned["pin"] / "src")
    assert pinned["pythonpath"][1] == str((ROOT / "paper-v4/answer-demonstration").resolve())
    assert pinned["pythonpath"][2:] == [str((ROOT / p).resolve()) for p in manifest["pythonpath"]]
    assert rules["pythonpath"][0] == str(Path("/exports") / rules["pin"] / "src")
    assert rules["pythonpath"][1:] == [str((ROOT / p).resolve()) for p in manifest["pythonpath"]]
    assert shop["pythonpath"][0] == str(Path("/exports") / shop["pin"] / "src")
    assert shop["pythonpath"][1:] == [str((ROOT / p).resolve()) for p in manifest["pythonpath"]]
    assert rest["pythonpath"] == [str((ROOT / p).resolve()) for p in manifest["pythonpath"]]


def test_the_unpinned_partition_does_not_sweep_a_pinned_cell_back_in() -> None:
    """paper-v4/experiment-v4 is a directory entry, and every pinned cell sits in it.

    Without this the pinned modules would be collected twice, once against the
    Core the cell was measured on and once against whatever the checkout holds.
    The Shop reconsideration cell joined them on 2026-09-18, so the unpinned
    partition ignores five files, not four. Both groups moved to the d89a0c47
    pin on 2026-09-19.
    """
    manifest, paths = runner.load_active_paths()
    pinned, rules, shop, rest = runner.plan(manifest, paths, export_root=Path("/exports"))
    assert pinned["ignore"] == []
    assert rules["ignore"] == []
    assert shop["ignore"] == []
    swept = set(manifest["core_pins"][1]["paths"]) | set(manifest["core_pins"][2]["paths"])
    assert set(rest["ignore"]) == swept
    command = runner.pytest_command(manifest, rest, [])
    for value in sorted(swept):
        assert f"--ignore={(ROOT / value).resolve()}" in command
    assert not any(option.startswith("-o") for option in command)


def test_a_pin_that_is_not_a_full_commit_identity_is_refused() -> None:
    manifest = json.loads(json.dumps(MANIFEST))
    manifest["core_pins"][0]["commit"] = "160878cf"
    try:
        runner.plan(manifest, manifest["paths"], export_root=Path("/exports"))
    except ValueError as error:
        assert "full commit identity" in str(error)
    else:
        raise AssertionError("short pin accepted")


# ---------------------------------------------------------------------------
# A pinned group must import its export in process, not only in subprocesses
# ---------------------------------------------------------------------------
#
# pyproject's ``[tool.pytest.ini_options] pythonpath = [".", "src"]`` is
# inserted at the front of ``sys.path`` by pytest itself, ahead of everything
# the runner puts on PYTHONPATH. A pinned test module that imports Core at
# collection therefore got the checkout's ``src/malleus`` while the pin was
# only honoured by tests that shell out (E-0434). The invocation the runner
# builds must override that ini value for a pinned group.


def _fixture_group(tmp: Path) -> Path:
    """A one-test group that reports which Core the pytest process imported."""
    module = tmp / "group" / "test_pinned_group_fixture.py"
    module.parent.mkdir(parents=True)
    module.write_text(
        "import os\n"
        "from pathlib import Path\n"
        "\n"
        "import malleus\n"
        "\n"
        "\n"
        "def test_core_comes_from_the_pinned_export():\n"
        "    expected = Path(os.environ['EXPECTED_CORE']).resolve()\n"
        "    assert Path(malleus.__file__).resolve().is_relative_to(expected)\n"
    )
    return module


def _run_pinned_group(core: Path, module: Path) -> subprocess.CompletedProcess[str]:
    """Run the runner's own pinned-group invocation over one fixture module.

    ``-c`` names this repository's pyproject so the fixture module, which lives
    outside the tree, is collected under the same ini options the gate runs
    with. Nothing else about the invocation is changed.
    """
    group = {"pin": "0" * 40, "paths": [str(module)], "ignore": [], "pythonpath": [
        str(core),
        *(str((ROOT / value).resolve()) for value in MANIFEST["pythonpath"]),
    ]}
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(group["pythonpath"])
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["EXPECTED_CORE"] = str(core)
    command = runner.pytest_command(
        MANIFEST, group, extra=["-p", "no:cacheprovider", "-c", str(ROOT / "pyproject.toml")]
    )
    return subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True)


def test_a_pinned_group_reaches_a_poisoned_core_in_process() -> None:
    """The proof that the pin binds in process: a Core that refuses to import."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        poison = root / "poison"
        (poison / "malleus").mkdir(parents=True)
        (poison / "malleus" / "__init__.py").write_text(
            'raise ImportError("POISONED CORE REACHED IN PROCESS")\n'
        )
        result = _run_pinned_group(poison, _fixture_group(root))
        assert result.returncode != 0, result.stdout + result.stderr
        assert "POISONED CORE REACHED IN PROCESS" in result.stdout + result.stderr


def test_a_pinned_group_imports_the_exported_core_in_process() -> None:
    """And the export itself, not the checkout, satisfies the same import."""
    commit = MANIFEST["core_pins"][0]["commit"]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        core = runner.export_core(commit, root / "export")
        result = _run_pinned_group(core, _fixture_group(root))
        assert result.returncode == 0, result.stdout + result.stderr
