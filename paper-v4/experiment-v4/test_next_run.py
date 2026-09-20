"""Future launch helpers, independent of frozen per-cell implementations."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("next_run", HERE / "next_run.py")
subject = importlib.util.module_from_spec(SPEC)


@pytest.fixture(autouse=True)
def implementation():
    SPEC.loader.exec_module(subject)


def test_prepared_baseline_task_reads_real_receipt_and_exact_model(tmp_path):
    subject.PRIVATE = tmp_path
    output = tmp_path / "producer"
    subject.prepare_baseline(
        {
            "selected-reading.json": b"reading",
            "questions.json": json.dumps(
                {"scope": {"figures": "INCLUDED", "tables": "INCLUDED"}}
            ).encode(),
            "answer-file-schema.json": b"schema",
        },
        "declared-model",
        output,
    )
    receipt = json.loads((output / "producer-input-receipt.json").read_bytes())
    task = (output / "TASK.md").read_text()
    assert "producer-input-receipt.json" in task
    assert "../producer-input-receipt.json" not in task
    assert '"declared-model"' in task
    assert "the model id you are running as" not in task
    assert receipt["producer_model_id"] == "declared-model"
    assert (
        receipt["producer_task_sha256"] == "sha256:" + sha256(task.encode()).hexdigest()
    )
    answers = {
        "producer_model_id": "declared-model",
        "inputs": {
            "selected_reading_sha256": receipt["inputs"]["selected-reading.json"],
            "competency_questions_sha256": receipt["inputs"]["questions.json"],
            "producer_task_sha256": receipt["producer_task_sha256"],
        },
    }
    subject.check_answer_binding(answers, receipt)
    answers["producer_model_id"] = "declared-model[1m]"
    with pytest.raises(ValueError, match="producer model"):
        subject.check_answer_binding(answers, receipt)
    answers["producer_model_id"] = "declared-model"
    answers["inputs"]["producer_task_sha256"] = "wrong"
    with pytest.raises(ValueError, match="producer_task_sha256"):
        subject.check_answer_binding(answers, receipt)
    before = {p.name: p.read_bytes() for p in output.iterdir() if p.is_file()}
    with pytest.raises(ValueError, match="exists"):
        subject.prepare_baseline({}, "declared-model", output)
    assert before == {p.name: p.read_bytes() for p in output.iterdir() if p.is_file()}


@pytest.mark.parametrize("inputs", [{}, {"selected-reading.json": b"x"}])
def test_missing_baseline_inputs_refuse_before_write(tmp_path, inputs):
    subject.PRIVATE = tmp_path
    with pytest.raises(ValueError, match="input closure"):
        subject.prepare_baseline(inputs, "declared-model", tmp_path / "producer")
    assert not (tmp_path / "producer").exists()


def test_row_witnesses_not_trace_reach_define_review_count():
    query = {
        "queries": [
            {
                "rows": [
                    {
                        "witness": {"record_id": "claim"},
                        "subject": {"record_id": "traced-only"},
                    },
                    {"witness": {"record_id": "claim"}},
                    {"witness": {"relation_id": "edge", "record_id": "claim"}},
                ]
            }
        ]
    }
    assert subject.review_witness_count(query) == 2
    query["queries"][0]["rows"].append({"witness": {}})
    with pytest.raises(ValueError, match="witness identity"):
        subject.review_witness_count(query)


def test_corrected_counter_matches_frozen_run_25_without_counting_subject_only_record():
    root = HERE.parents[1]
    query = json.loads(
        (root / "private/paper-v4-v4-run-25/query/query-result.json").read_bytes()
    )
    manifest = json.loads(
        (root / "paper-v4/evaluation-v4/run-25/review-input-manifest.json").read_bytes()
    )
    trace = json.loads((HERE / "run-25/results/query-trace-summary.json").read_bytes())
    assert subject.review_witness_count(query) == manifest["witnesses_traced"] == 505
    assert trace["witnesses_traced"] == 506


@pytest.mark.parametrize("cell", ["reuse-01", "reuse-01-baseline"])
def test_declared_reuse_fixture_is_required_not_a_silent_skip(tmp_path, cell):
    spec = importlib.util.spec_from_file_location(
        "reuse_required_fixtures", HERE / cell / "test_contract.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        with pytest.raises(FileNotFoundError, match="declared private fixture"):
            module._need(tmp_path / "missing.json")
    except pytest.skip.Exception:
        pytest.fail("missing declared fixture silently skips the evidence check")


def review_context_fixture():
    sources = {
        "accepted_ontology": b"name: project\nimports: [root]\n",
        "ontology_import:root": b"name: root\nimports: [scalars]\n",
        "ontology_import:scalars": b"name: scalars\n",
        "competency_questions": b'{"scope":{"figures":"INCLUDED","tables":"INCLUDED"}}',
    }
    manifest = {
        "stage_identities": {
            "accepted_ontology_sha256": subject.digest(sources["accepted_ontology"])
        },
        "materials": [
            {"name": name, "sha256": subject.digest(source)}
            for name, source in sources.items()
        ],
    }
    return manifest, sources


def test_graph_review_requires_exact_semantic_sources_and_transitive_imports():
    manifest, sources = review_context_fixture()
    assert subject.check_graph_review_context(manifest, sources) == {
        "source_materials": [
            "accepted_ontology",
            "ontology_import:root",
            "ontology_import:scalars",
        ],
        "semantic_adequacy": "NOT_CHECKED",
    }


@pytest.mark.parametrize(
    "defect",
    [
        "missing_ontology",
        "missing_import",
        "changed_bytes",
        "wrong_ontology",
        "duplicate_name",
        "malformed_source",
        "missing_questions",
        "changed_questions",
    ],
)
def test_graph_review_semantic_context_refuses_incomplete_or_wrong_inputs(defect):
    manifest, sources = review_context_fixture()
    if defect == "missing_ontology":
        del sources["accepted_ontology"]
    elif defect == "missing_import":
        del sources["ontology_import:scalars"]
    elif defect == "changed_bytes":
        sources["ontology_import:root"] += b"description: changed\n"
    elif defect == "wrong_ontology":
        manifest["stage_identities"]["accepted_ontology_sha256"] = subject.digest(
            b"other"
        )
    elif defect == "duplicate_name":
        manifest["materials"].append(dict(manifest["materials"][0]))
    elif defect == "missing_questions":
        del sources["competency_questions"]
    elif defect == "changed_questions":
        sources["competency_questions"] += b"\n"
    else:
        sources["accepted_ontology"] = b"null\n"
        identity = subject.digest(sources["accepted_ontology"])
        manifest["materials"][0]["sha256"] = identity
        manifest["stage_identities"]["accepted_ontology_sha256"] = identity
    with pytest.raises(ValueError, match="review semantic context"):
        subject.check_graph_review_context(manifest, sources)


@pytest.mark.parametrize(
    "packet",
    [
        "private/paper-v4-relationship-contrast-01/b/attempts/attempt-03/review",
        "private/paper-v4-relationship-repair-01/measurement",
    ],
)
def test_historical_reviews_lack_new_semantic_context_without_rewriting_them(packet):
    root = HERE.parents[1]
    manifest_source = (root / packet / "review-input-manifest.json").read_bytes()
    manifest = json.loads(manifest_source)
    materials = {
        item["name"]: (root / item["path"]).read_bytes()
        for item in manifest["materials"]
    }
    assert "accepted_ontology" not in materials
    surface = json.loads(materials["accepted_surface"])
    assert all("description" not in t for t in surface["record_types"])
    with pytest.raises(ValueError, match="review semantic context"):
        subject.check_graph_review_context(manifest, materials)
    assert (
        root / packet / "review-input-manifest.json"
    ).read_bytes() == manifest_source


@pytest.mark.parametrize("imports", [None, "root", [""], [1], ["root", "root"]])
def test_graph_review_context_refuses_ambiguous_import_closure(imports):
    manifest, sources = review_context_fixture()
    sources["accepted_ontology"] = (
        "name: project\nimports: " + json.dumps(imports) + "\n"
    ).encode()
    identity = subject.digest(sources["accepted_ontology"])
    manifest["materials"][0]["sha256"] = identity
    manifest["stage_identities"]["accepted_ontology_sha256"] = identity
    with pytest.raises(ValueError, match="review semantic context.*imports?"):
        subject.check_graph_review_context(manifest, sources)


def test_graph_review_context_cli_checks_sources_without_writing(
    tmp_path, monkeypatch, capsys
):
    manifest, sources = review_context_fixture()
    for index, item in enumerate(manifest["materials"]):
        path = tmp_path / f"source-{index}.yaml"
        path.write_bytes(sources[item["name"]])
        item["path"] = str(path)
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest))
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    monkeypatch.setattr(
        subject.sys,
        "argv",
        ["next_run.py", "check-review-context", "--manifest", str(path)],
    )
    assert subject.main() == 0
    assert json.loads(capsys.readouterr().out)["semantic_adequacy"] == "NOT_CHECKED"
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before
    source = tmp_path / "source-1.yaml"
    source.write_bytes(b"name: unrelated\n")
    assert subject.main() == 2
    assert "review semantic context: source bytes differ" in capsys.readouterr().err


@pytest.mark.parametrize("surface", ["figures", "tables"])
@pytest.mark.parametrize("value", ["EXCLUDED", None, ""])
def test_future_document_scope_refuses_blanket_exclusion_or_undefined_scope(
    surface, value
):
    questions = {"scope": {"figures": "INCLUDED", "tables": "INCLUDED"}}
    questions["scope"][surface] = value
    with pytest.raises(ValueError, match="document scope"):
        subject.check_document_scope(questions)


def test_document_inclusion_is_not_a_capture_completeness_claim():
    assert subject.check_document_scope(
        {"scope": {"figures": "INCLUDED", "tables": "INCLUDED"}}
    ) == {
        "eligible_document_surfaces": ["figures", "tables"],
        "capture_completeness": "NOT_CHECKED",
    }
    for questions in ({}, {"scope": {"figures": "INCLUDED"}}):
        with pytest.raises(ValueError, match="document scope"):
            subject.check_document_scope(questions)


def test_historical_exclusion_refuses_future_baseline_without_rewriting_or_preparing(
    tmp_path,
):
    subject.PRIVATE = tmp_path
    path = HERE / "competency-questions-v3.json"
    source = path.read_bytes()
    with pytest.raises(ValueError, match="document scope"):
        subject.prepare_baseline(
            {
                "questions.json": source,
                "selected-reading.json": b"reading",
                "answer-file-schema.json": b"schema",
            },
            "model",
            tmp_path / "producer",
        )
    assert not (tmp_path / "producer").exists()
    assert path.read_bytes() == source


def test_future_graph_review_also_refuses_exclusion_in_exact_question_bytes():
    manifest, sources = review_context_fixture()
    sources["competency_questions"] = (
        HERE / "competency-questions-v3.json"
    ).read_bytes()
    for item in manifest["materials"]:
        if item["name"] == "competency_questions":
            item["sha256"] = subject.digest(sources["competency_questions"])
    with pytest.raises(ValueError, match="review semantic context.*document scope"):
        subject.check_graph_review_context(manifest, sources)


def test_document_scope_cli_keeps_the_frozen_question_file_unchanged(
    monkeypatch, capsys
):
    path = HERE / "competency-questions-v3.json"
    source = path.read_bytes()
    monkeypatch.setattr(
        subject.sys,
        "argv",
        ["next_run.py", "check-document-scope", "--questions", str(path)],
    )
    assert subject.main() == 2
    assert "document scope" in capsys.readouterr().err
    assert path.read_bytes() == source
