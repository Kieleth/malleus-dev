"""RED contract for retaining the ontology source as an explicit act.

A history holds the compiled contract, never the LinkML the contract was
compiled from. That is why no proposal could be composed against the real root:
Core did not have it. This contract gives the history one explicit act that
puts the source set in, and refuses unless the set compiles back to the exact
contract the history is already running.

Explicit means explicit. Genesis does not do it, a recorded revision does not do
it, and nothing already written moves because of it.
"""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import malleus.compiler as compiler
from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    ROOT,
    TRANSACTION_TIME,
    _anchor,
    _anchored_history,
    _digest,
    _event,
    _generic_compilation,
    _trusted_types,
)
from tests.contract_compiler.pareto.test_linkml_addition import BASE, CLASS_FRAGMENT
from tests.contract_compiler.pareto.test_protocol_machine import _canonical, _effective


ACTOR = "actor:test"

#: A bare subprocess resolves ``malleus`` to whatever the interpreter has
#: installed, which on this laptop is another checkout. These probes must run
#: the tree under test, so they pin the path explicitly and the program asserts
#: which tree it got. Without both, the probe measures nothing and says PASS.
PROBE_ENV = {
    **os.environ,
    "PYTHONPATH": f"{ROOT / 'src'}{os.pathsep}{ROOT}",
}
PROBE_PREAMBLE = (
    "import sys\n"
    "import malleus\n"
    f"assert malleus.__file__.startswith({str(ROOT)!r}), malleus.__file__\n"
)
PROBE_EPILOGUE = (
    "leaked = sorted(\n"
    "    name\n"
    "    for name in sys.modules\n"
    "    if name == 'linkml' or name.startswith(('linkml.', 'linkml_runtime'))\n"
    ")\n"
    "print('|'.join(leaked))\n"
)


def run_probe(body: str) -> subprocess.CompletedProcess:
    """Run one LinkML-free probe against this tree and return what it loaded."""

    return subprocess.run(
        [sys.executable, "-c", PROBE_PREAMBLE + body + PROBE_EPILOGUE],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env=PROBE_ENV,
        check=False,
    )


def _sources(root: bytes = BASE) -> dict[str, bytes]:
    return {
        "generic": root,
        "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
        "linkml:types": _trusted_types(),
    }


def _history(tmp_path: Path):
    history, _, _, _, _, _ = _anchored_history(tmp_path, contract_source=BASE)
    return history


def _retain(history: KnowledgeChangeHistory, sources=None):
    return history.retain_ontology_source(
        root_locator="generic",
        sources=sources if sources is not None else _sources(),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
    )


# --- the act -----------------------------------------------------------------


def test_the_grammar_is_versioned() -> None:
    assert compiler.ONTOLOGY_SOURCE_SET_GRAMMAR == "malleus.ontology-source-set/v1"


def test_a_new_history_holds_no_ontology_source(tmp_path) -> None:
    history = _history(tmp_path)

    assert history.replay().ontology_source_set() is None


def test_retaining_the_source_records_every_module_by_its_own_bytes(
    tmp_path,
) -> None:
    history = _history(tmp_path)
    sources = _sources()

    replay = _retain(history, sources)

    source_set = replay.ontology_source_set()
    assert source_set is not None
    assert source_set.root_locator == "generic"
    assert source_set.validated_contract_identity == (
        replay.partial_contract.validated_fact_set_sha256
    )
    modules = {module.locator: module for module in source_set.modules}
    assert set(modules) == set(sources)
    for locator, content in sources.items():
        assert modules[locator].sha256 == _digest(content)
        assert modules[locator].byte_length == len(content)
        assert modules[locator].media_type == "application/yaml"
    # Every module's bytes are in the history, addressed by their own digest.
    retained = {member.identity for member in replay.retained_inputs}
    assert {module.sha256 for module in source_set.modules} <= retained
    assert replay.ontology_source_bytes("generic") == sources["generic"]


def test_the_source_set_names_the_compiler_execution_that_produced_it(
    tmp_path,
) -> None:
    history = _history(tmp_path)
    public = compiler.compile_linkml_contract(
        root_locator="generic", sources=_sources()
    )

    replay = _retain(history)

    source_set = replay.ontology_source_set()
    assert source_set is not None
    assert source_set.compiler_execution_identity == public.artifact.evidence_sha256


def test_the_reproduction_check_is_the_contract_identity_not_the_envelope(
    tmp_path,
) -> None:
    """Two compilations of one source set agree on the contract, not the envelope.

    The history's own artifact came from the fixture's closure builder; the act
    compiles through ``compile_linkml_contract``. Both produce the same
    validated contract and different compiler evidence, so the reproduction
    check compares the identity. The set records the execution, so the two are
    still told apart afterwards.
    """

    history = _history(tmp_path)
    fixture = _generic_compilation(BASE)
    public = compiler.compile_linkml_contract(
        root_locator="generic", sources=_sources()
    )

    assert (
        public.artifact.validated_fact_set_sha256
        == fixture.artifact.validated_fact_set_sha256
    )
    assert public.artifact.evidence_sha256 != fixture.artifact.evidence_sha256
    assert public.artifact.artifact_bytes != fixture.artifact.artifact_bytes
    assert _retain(history).ontology_source_set() is not None


def test_a_source_set_that_does_not_reproduce_the_contract_refuses(
    tmp_path,
) -> None:
    history = _history(tmp_path)
    other = compiler.compose_linkml_addition(BASE, CLASS_FRAGMENT)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologySourceRefusal) as caught:
        _retain(history, _sources(other))

    assert caught.value.reason == (
        compiler.OntologySourceRefusalReason.ONTOLOGY_SOURCE_DOES_NOT_REPRODUCE_CONTRACT
    )
    assert history.path.read_bytes() == before


def test_retaining_the_same_source_set_twice_refuses(tmp_path) -> None:
    history = _history(tmp_path)
    _retain(history)
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologySourceRefusal) as caught:
        _retain(history)

    assert caught.value.reason == (
        compiler.OntologySourceRefusalReason.ONTOLOGY_SOURCE_ALREADY_RETAINED
    )
    assert history.path.read_bytes() == before


def test_the_act_is_explicit_and_moves_nothing_already_written(tmp_path) -> None:
    history = _history(tmp_path)
    before = history.replay()
    prefix = history.path.read_bytes()

    replay = _retain(history)

    assert history.path.read_bytes().startswith(prefix)
    assert replay.graph.export_records() == before.graph.export_records()
    assert replay.acceptance_head == before.acceptance_head
    assert replay.materialization_head == before.materialization_head
    assert replay.partial_contract.identity == before.partial_contract.identity


def test_a_recorded_revision_does_not_retain_a_source_set_by_itself(
    tmp_path,
) -> None:
    history = _history(tmp_path)
    target = _generic_compilation(compiler.compose_linkml_addition(BASE, CLASS_FRAGMENT))
    revision = history.compose_contract_revision(
        revision_id="revision:plain",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=_effective(
            validated_fact_set_sha256=target.artifact.validated_fact_set_sha256
        ).canonical_bytes,
        reason="a revision recorded without any source retained",
        issued_at="2026-09-21T00:00:00Z",
    )

    replay = history.record_contract_revision(
        revision=revision, transaction_time=TRANSACTION_TIME, actor_id=ACTOR
    )

    assert len(replay.contract_revisions) == 1
    assert replay.ontology_source_set() is None


def test_a_retained_source_set_stops_being_current_after_a_revision(
    tmp_path,
) -> None:
    history = _history(tmp_path)
    _retain(history)
    target = _generic_compilation(compiler.compose_linkml_addition(BASE, CLASS_FRAGMENT))
    revision = history.compose_contract_revision(
        revision_id="revision:plain",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=_effective(
            validated_fact_set_sha256=target.artifact.validated_fact_set_sha256
        ).canonical_bytes,
        reason="the contract moves and the retained source no longer describes it",
        issued_at="2026-09-21T00:00:00Z",
    )

    replay = history.record_contract_revision(
        revision=revision, transaction_time=TRANSACTION_TIME, actor_id=ACTOR
    )

    assert replay.ontology_source_set() is None


def test_the_source_set_survives_a_reopen(tmp_path) -> None:
    history = _history(tmp_path)
    replay = _retain(history)
    identity = replay.ontology_source_set().identity

    reopened = KnowledgeChangeHistory.reopen(history.path).replay()

    assert reopened.ontology_source_set().identity == identity


# --- the fold checks the digests ---------------------------------------------


def test_a_source_set_naming_bytes_the_history_lacks_refuses(tmp_path) -> None:
    history = _history(tmp_path)
    record = _canonical(
        {
            "compiler_execution_identity": _digest(b"whatever"),
            "grammar": compiler.ONTOLOGY_SOURCE_SET_GRAMMAR,
            "modules": [
                {
                    "byte_length": 3,
                    "locator": "generic",
                    "media_type": "application/yaml",
                    "sha256": "sha256:" + sha256(b"absent").hexdigest(),
                }
            ],
            "root_locator": "generic",
            "validated_contract_identity": (
                history.replay().partial_contract.validated_fact_set_sha256
            ),
        }
    )
    record_id = f"ontology-source-set:{_digest(record)}"
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologySourceRefusal) as caught:
        _anchor(
            history,
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id=record_id,
                artifact_identity=_digest(record),
            ),
            record,
            "RETAINED_EVIDENCE",
            media_type="application/json",
        )

    assert caught.value.reason == (
        compiler.OntologySourceRefusalReason.ONTOLOGY_SOURCE_BYTES_NOT_RETAINED
    )
    assert history.path.read_bytes() == before


def test_a_source_set_record_id_that_is_not_its_digest_refuses(tmp_path) -> None:
    history = _history(tmp_path)
    _retain(history)
    record = json.loads(
        history.replay().ontology_source_set().canonical_bytes
    )
    content = _canonical(record)

    with pytest.raises(compiler.OntologySourceRefusal) as caught:
        _anchor(
            history,
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="ontology-source-set:chosen-by-hand",
                artifact_identity=_digest(content),
            ),
            content,
            "RETAINED_EVIDENCE",
            media_type="application/json",
        )

    assert caught.value.reason == (
        compiler.OntologySourceRefusalReason.MALFORMED_SOURCE_SET
    )


# --- the derived target is checked at retention too ---------------------------


def _target_record(**fields) -> bytes:
    return _canonical({"grammar": compiler.ONTOLOGY_REVISION_TARGET_GRAMMAR, **fields})


def _retain_record(history: KnowledgeChangeHistory, content: bytes, record_id: str):
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id=record_id,
            artifact_identity=_digest(content),
        ),
        content,
        "RETAINED_EVIDENCE",
        media_type="application/json",
    )


def test_a_revision_target_record_id_that_is_not_its_digest_refuses(tmp_path) -> None:
    history = _history(tmp_path)
    replay = _retain(history)
    source_set = replay.ontology_source_set()
    content = _target_record(
        composed_root_sha256=source_set.root_sha256,
        partial_contract=json.loads(replay.partial_contract.canonical_bytes),
        proposal_identity=_digest(b"a proposal"),
        source_set_identity=source_set.identity,
        validated_contract=json.loads(replay.contract_view.artifact_bytes),
    )
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologySourceRefusal) as caught:
        _retain_record(history, content, "ontology-revision-target:chosen-by-hand")

    assert caught.value.reason == (
        compiler.OntologySourceRefusalReason.MALFORMED_REVISION_TARGET
    )
    assert history.path.read_bytes() == before


def test_a_target_composed_onto_a_stale_source_set_refuses(tmp_path) -> None:
    """A derived target composes onto the active contract's source, not an old one."""

    history = _history(tmp_path)
    replay = _retain(history)
    stale = replay.ontology_source_set()
    target = _generic_compilation(compiler.compose_linkml_addition(BASE, CLASS_FRAGMENT))
    revision = history.compose_contract_revision(
        revision_id="revision:plain",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=_effective(
            validated_fact_set_sha256=target.artifact.validated_fact_set_sha256
        ).canonical_bytes,
        reason="the contract moves, so the retained source stops being current",
        issued_at="2026-09-21T00:00:00Z",
    )
    moved = history.record_contract_revision(
        revision=revision, transaction_time=TRANSACTION_TIME, actor_id=ACTOR
    )
    assert moved.ontology_source_set() is None
    content = _target_record(
        composed_root_sha256=stale.root_sha256,
        partial_contract=json.loads(moved.partial_contract.canonical_bytes),
        proposal_identity=_digest(b"a proposal"),
        source_set_identity=stale.identity,
        validated_contract=json.loads(moved.contract_view.artifact_bytes),
    )
    before = history.path.read_bytes()

    with pytest.raises(compiler.OntologySourceRefusal) as caught:
        _retain_record(
            history, content, f"ontology-revision-target:{_digest(content)}"
        )

    assert caught.value.reason == (
        compiler.OntologySourceRefusalReason.REVISION_TARGET_SOURCE_SET_NOT_CURRENT
    )
    assert history.path.read_bytes() == before


# --- replay stays LinkML-free ------------------------------------------------


def test_the_fold_replays_a_retained_source_set_without_importing_linkml(
    tmp_path,
) -> None:
    history = _history(tmp_path)
    _retain(history)

    finished = run_probe(
        "from malleus._contract_pipeline.knowledge import KnowledgeChangeHistory\n"
        f"replay = KnowledgeChangeHistory.reopen({str(history.path)!r}).replay()\n"
        "assert replay.ontology_source_set() is not None\n"
    )

    assert finished.returncode == 0, finished.stderr
    assert finished.stdout.strip() == ""


def test_the_linkml_free_probe_runs_the_tree_under_test() -> None:
    """The control for the probe above: it must fail when the tree is wrong."""

    assert run_probe("").returncode == 0
    wrong = subprocess.run(
        [sys.executable, "-c", PROBE_PREAMBLE],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env={**os.environ, "PYTHONPATH": ""},
        check=False,
    )
    assert wrong.returncode != 0
    assert "AssertionError" in wrong.stderr
