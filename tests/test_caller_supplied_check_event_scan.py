"""No tracked caller may hand ``admit`` a check or verdict event of its own.

Decision D (2026-09-20, overseer ``OVR-000471`` to ``OVR-000475``) closed
Core's two-step admission door. ``KnowledgeChangeHistory.admit`` and
``admit_with_anchors`` refuse a caller-supplied ``CHECK_RECORDED`` or
``VERDICT_RECORDED`` with
``KnowledgeChangeRefusalReason.CALLER_SUPPLIED_CHECK_EVENT``: Core runs every
check its policy requires and writes the check record itself, through
``malleus.compiler.check_and_admit_population_plan`` or
``malleus.compiler.check_and_admit_change_set``.

The agents who carried that migration found the remaining callers with a
runtime probe that wrapped both methods and recorded every call carrying one
of the two events. A probe only sees what a suite happens to execute, and it
perturbed the tree it measured: it hid ``machine_events`` from
``inspect.signature`` and made
``test_no_public_callable_accepts_a_caller_check_outcome_under_a_policy`` fail
on a tree where it passes. This is that probe made permanent and static. It
reads the tracked tree, so it sees a caller no test exercises, and it changes
nothing it looks at.

**Scope.** ``src/``, ``research/`` and ``tests/``. The four Core tests named in
``ALLOWED`` are the tests *of* the door: their subject is the refusal, so they
must keep supplying the event the door rejects, and a reading of zero would
mean the door had lost its tests.

``paper-v4/`` is deliberately excluded. It is the paper front's tree, governed
by the ``malleus-paper`` skill and off limits to Core agents, and it still
holds two unmigrated runners:

- ``paper-v4/experiment-v4/content-rules-doc-01/run_policy.py``
- ``paper-v4/experiment-v4/content-rules-doc-02/admit.py``

Both are the paper front's to adapt. Nothing under ``tests/`` or ``research/``
imports either one.

**The burden is on the caller, not on the scan.** An earlier draft of this
file flagged only what it could prove was a check event, and it missed the
caller that mattered. ``document_run.py`` took a ``protocol_events`` callable
as a parameter and passed its result straight to ``admit``; the two event
literals lived in ``experiment_run.py``, one module away, so a walk of
``document_run.py`` alone saw nothing and the scan read clean on the very file
the migration was for.

So the rule is inverted. Every ``machine_events=`` at the closed door is a
finding unless the expression resolves, in its own module, to event literals
none of which is ``CHECK_RECORDED`` or ``VERDICT_RECORDED``. A caller that
cannot be shown to be check-free is reported, because the door is closed and
proving otherwise is the caller's job. That is what makes an opaque hand-off
visible rather than invisible.

**What this cannot see.** The walk follows the ``machine_events`` expression
through same-module assignments and same-module function bodies, two hops
deep, and reports anything it cannot resolve. It still does not see a caller
that reaches the door through a name this scan never inspects: a wrapper in a
third module that itself calls ``admit``, a ``getattr`` dispatch, or a method
named ``admit`` on some unrelated object, which is a false positive rather
than a miss. Events assembled from a format string rather than a literal read
as opaque, which is a finding, not a gap.
"""

from __future__ import annotations

import ast
from pathlib import Path
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCANNED_ROOTS = ("src", "research", "tests")
EXCLUDED_ROOTS = ("paper-v4",)

CLOSED_DOOR_METHODS = frozenset({"admit", "admit_with_anchors"})
CORE_AUTHORED_EVENTS = ("CHECK_RECORDED", "VERDICT_RECORDED")

ALLOWED = frozenset(
    {
        # Core's own tests of the closed door. Each one asserts the refusal.
        # The 2026-09-20 probe read four of these because it counted calls and
        # the third is parametrized ``[rejected]`` and ``[unregistered]``;
        # three functions, four readings.
        (
            "tests/contract_compiler/pareto/test_atomic_population_admission.py",
            "test_a_fabricated_check_outcome_can_no_longer_reach_the_ledger",
        ),
        (
            "tests/contract_compiler/pareto/test_atomic_population_admission.py",
            "test_the_public_door_refuses_a_caller_written_verdict_record",
        ),
        (
            "tests/contract_compiler/pareto/test_knowledge_change_history.py",
            "test_refused_change_never_changes_ledger_or_replayed_graph",
        ),
        # Core's own lifecycle tests. Both bind ``_protocol_events(...)[:1]``
        # and assert ``INCOMPLETE_ADMISSION``, so only the proposal reaches
        # the door; the slice is why the walk cannot show that by parsing.
        (
            "tests/contract_compiler/pareto/test_knowledge_change_history.py",
            "test_admit_with_anchors_refuses_the_whole_batch_when_admission_is_incomplete",
        ),
        (
            "tests/contract_compiler/pareto/test_knowledge_change_history.py",
            "test_admit_requires_one_complete_accepted_lifecycle",
        ),
    }
)

KNOWN_UNMIGRATED = frozenset(
    {
        # Found by this scan on 2026-09-21 and left alone: outside the brief
        # that wrote this file, which covered the document path. It is a real
        # unmigrated caller, red at ``4ad1367f`` before any change here with
        # ``CALLER_SUPPLIED_CHECK_EVENT`` at setup of seven tests, and it went
        # unnoticed because ``research/action_history_contract_freeze`` is not
        # in ``testpaths``. It imports ``_protocol_events`` from
        # ``sequential_fixture`` and calls ``history.admit`` with it.
        (
            "research/action_history_contract_freeze/programs/test_action_inputs.py",
            "prefix",
        ),
    }
)


def _tracked_python_files() -> tuple[Path, ...]:
    """Every tracked ``.py`` under the scanned roots, excluding ``paper-v4``."""

    listed = subprocess.run(
        ["git", "ls-files", "-z", "--", *SCANNED_ROOTS],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    ).stdout
    paths = []
    for entry in listed.split("\0"):
        if not entry.endswith(".py"):
            continue
        if entry.startswith(EXCLUDED_ROOTS):
            continue
        paths.append(ROOT / entry)
    return tuple(paths)


def _enclosing_function(tree: ast.AST, target: ast.AST) -> str:
    """The name of the innermost function holding ``target``, or ``<module>``."""

    best = "<module>"
    best_span = None
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        end = getattr(node, "end_lineno", None)
        if end is None or not node.lineno <= target.lineno <= end:
            continue
        span = end - node.lineno
        if best_span is None or span < best_span:
            best, best_span = node.name, span
    return best


def _resolve(
    tree: ast.AST,
    expression: ast.AST,
    parameters: frozenset[str],
    hops: int = 2,
) -> tuple[list[ast.AST], bool]:
    """``expression`` plus what it names, and whether the walk gave up.

    A ``machine_events`` argument is rarely a literal tuple. It is usually a
    name bound earlier in the function, or a call to a helper defined beside
    it. Both are followed. What is not followed is recorded rather than
    ignored: a name that is a parameter of the enclosing function (the caller
    handed the events in), a slice (which members survive needs the slice
    evaluated), and a call to something this module does not define.
    """

    functions = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assignments: dict[str, list[ast.AST]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                assignments.setdefault(target.id, []).append(node.value)

    collected: list[ast.AST] = [expression]
    opaque = False
    seen: set[str] = set()
    frontier: list[ast.AST] = [expression]
    for _ in range(hops):
        wanted: set[str] = set()
        for node in frontier:
            for inner in ast.walk(node):
                if isinstance(inner, ast.Subscript):
                    opaque = True
                elif isinstance(inner, ast.Name):
                    wanted.add(inner.id)
                elif isinstance(inner, ast.Attribute):
                    wanted.add(inner.attr)
        wanted -= seen
        seen |= wanted
        frontier = []
        for name in wanted:
            if name in parameters:
                # The caller passed these events, or the factory that makes
                # them, in from outside. This module cannot show them to be
                # check-free, and that is the finding.
                opaque = True
                continue
            resolved = False
            if name in functions:
                frontier.append(functions[name])
                resolved = True
            for value in assignments.get(name, ()):
                frontier.append(value)
                resolved = True
            if not resolved and name in _CALLED_NAMES.get(id(tree), frozenset()):
                opaque = True
        collected.extend(frontier)
    return collected, opaque


_CALLED_NAMES: dict[int, frozenset[str]] = {}


def _event_literals(nodes: list[ast.AST]) -> set[str]:
    """Every string literal in ``nodes`` that reads as a protocol event type."""

    found = set()
    for node in nodes:
        for inner in ast.walk(node):
            if (
                isinstance(inner, ast.Constant)
                and isinstance(inner.value, str)
                and inner.value.isupper()
                and inner.value.endswith(("_RECORDED", "_PROPOSED"))
            ):
                found.add(inner.value)
    return found


def _caller_authored_admissions(path: Path) -> list[tuple[str, int, str]]:
    """Every closed-door call this file cannot show to be check-free.

    Returns ``(function, line, detail)``. A call is clean only when the walk
    resolved and every protocol event it reaches is something other than
    ``CHECK_RECORDED`` or ``VERDICT_RECORDED``.
    """

    tree = ast.parse(path.read_text(encoding="utf-8"))
    _CALLED_NAMES[id(tree)] = frozenset(
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    )
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        if name not in CLOSED_DOOR_METHODS:
            continue
        events_argument = next(
            (kw.value for kw in node.keywords if kw.arg == "machine_events"),
            None,
        )
        if events_argument is None:
            continue
        function = _enclosing_function(tree, node)
        if isinstance(events_argument, (ast.Tuple, ast.List)):
            # A literal batch. Its membership is fully visible at the call
            # site, whatever module canonicalizes each event, so the helper
            # being cross-module does not make the batch unknowable.
            reached, opaque = [events_argument], False
        else:
            reached, opaque = _resolve(
                tree, events_argument, _parameters_of(tree, function)
            )
        literals = _event_literals(reached)
        authored = sorted(literals & set(CORE_AUTHORED_EVENTS))
        if authored:
            findings.append((function, node.lineno, ", ".join(authored)))
        elif opaque or not literals:
            findings.append(
                (
                    function,
                    node.lineno,
                    "events this module cannot show to be check-free",
                )
            )
    _CALLED_NAMES.pop(id(tree), None)
    return findings


def _parameters_of(tree: ast.AST, function: str) -> frozenset[str]:
    """Every parameter name of ``function``, or nothing at module scope."""

    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function
        ):
            arguments = node.args
            return frozenset(
                argument.arg
                for group in (
                    arguments.posonlyargs,
                    arguments.args,
                    arguments.kwonlyargs,
                )
                for argument in group
            ) | frozenset(
                argument.arg
                for argument in (arguments.vararg, arguments.kwarg)
                if argument is not None
            )
    return frozenset()


def test_no_tracked_caller_supplies_core_a_check_or_verdict_event() -> None:
    """The door is closed for every tracked caller but its own four tests."""

    violations = []
    for path in _tracked_python_files():
        relative = path.relative_to(ROOT).as_posix()
        for function, lineno, detail in _caller_authored_admissions(path):
            if (relative, function) in ALLOWED | KNOWN_UNMIGRATED:
                continue
            violations.append(
                f"{relative}:{lineno} in {function}() hands the closed door "
                f"{detail}; admit through check_and_admit_change_set or "
                "check_and_admit_population_plan"
            )
    assert violations == [], "\n".join(violations)


def test_the_core_door_tests_still_exercise_the_refusal() -> None:
    """A zero reading would mean the door had lost its tests, not gained safety."""

    observed = set()
    for path in _tracked_python_files():
        relative = path.relative_to(ROOT).as_posix()
        for function, _lineno, _detail in _caller_authored_admissions(path):
            if (relative, function) in ALLOWED:
                observed.add((relative, function))
    missing = sorted(f"{path}::{function}" for path, function in ALLOWED - observed)
    assert not missing, (
        "these door tests no longer supply the event the door refuses: "
        + ", ".join(missing)
    )


def test_the_unmigrated_residue_is_exactly_what_was_declared() -> None:
    """``KNOWN_UNMIGRATED`` may shrink. It may not grow, and it may not rot.

    A waiver list that nobody checks becomes the place drift hides. Every
    entry must still be a finding, so a migrated caller has to be removed
    here rather than left as a standing exemption.
    """

    observed = set()
    for path in _tracked_python_files():
        relative = path.relative_to(ROOT).as_posix()
        for function, _lineno, _detail in _caller_authored_admissions(path):
            observed.add((relative, function))
    stale = sorted(
        f"{path}::{function}" for path, function in KNOWN_UNMIGRATED - observed
    )
    assert not stale, (
        "these callers are migrated; drop them from KNOWN_UNMIGRATED: "
        + ", ".join(stale)
    )


@pytest.mark.parametrize("path", ("src", "research", "tests"))
def test_the_scan_reads_a_nonempty_tracked_tree(path: str) -> None:
    """A scan over nothing passes for the wrong reason."""

    assert any(
        candidate.relative_to(ROOT).as_posix().startswith(path)
        for candidate in _tracked_python_files()
    )
