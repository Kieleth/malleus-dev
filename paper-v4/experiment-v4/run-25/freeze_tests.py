"""Rewrite run-25's contract tests from the frozen files, never by hand.

Run after ``freeze.py``, from the repository root:

    .venv/bin/python paper-v4/experiment-v4/run-25/freeze_tests.py

Three edits, each derived from a file this cell froze. The open-stage test that
asserts ``ontology-run/`` and ``results/`` hold nothing but ``.gitkeep`` is
replaced by the frozen block: the exact artefact set with its digests, the
sixty-character leak check over every one of them, the withheld list read back
against its own private paths, the ontology-run record, the run result, the
binding and the cost record. The open-stage review-package test is replaced by
the frozen one, which reads the manifest's row counts against this cell's own
query result. And the two placeholder assertions, which at open stage require
the row counts to be absent, are inverted to require them present.

No figure here is typed. Every count comes from the frozen file that carries it.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path("/Users/luis/Projects/malleus-dev")
HERE = ROOT / "paper-v4/experiment-v4/run-25"
PRIVATE = ROOT / "private/paper-v4-v4-run-25"
PUBLIC = HERE / "results"
ONTOLOGY_RUN = HERE / "ontology-run"
PACKAGE = ROOT / "paper-v4/evaluation-v4/run-25"
TEST = HERE / "test_contract.py"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frozen_block() -> str:
    log = json.loads((PUBLIC / "launch-log.json").read_bytes())
    usage = json.loads((PUBLIC / "usage.json").read_bytes())
    result = json.loads((PUBLIC / "run-result.json").read_bytes())
    census = json.loads((PUBLIC / "census.json").read_bytes())
    binding = json.loads((PUBLIC / "native-query-binding.json").read_bytes())
    surface = json.loads((ONTOLOGY_RUN / "population-surface.json").read_bytes())
    gate = json.loads((ONTOLOGY_RUN / "result.json").read_bytes())
    withheld = json.loads((PUBLIC / "withheld-artifacts.json").read_bytes())
    questions = json.loads(
        (ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json").read_bytes()
    )
    question_ids = sorted(item["id"] for item in questions["questions"])
    families: dict[str, list[str]] = {}
    for item in surface["record_types"]:
        families.setdefault(item["family"], []).append(item["name"])
    cases = sum(len(query["cases"]) for query in binding["queries"])
    rows = log["query"]["rows_by_question"]
    artifacts = {}
    for name in ("ontology-run", "results"):
        for path in sorted((HERE / name).iterdir()):
            if path.is_file() and path.suffix != ".pyc" and path.name != ".gitkeep":
                artifacts[f"{name}/{path.name}"] = digest(path)
    lines = ["FROZEN_ARTIFACTS = {"]
    for relative, value in artifacts.items():
        lines.append(f'    "{relative}": (')
        lines.append(f'        "{value}"')
        lines.append("    ),")
    lines.append("}")
    names = json.dumps(sorted(item["name"] for item in withheld["withheld"]), indent=4)
    return f'''
# The exact bytes this run leaves in the repository. A frozen run is a closed
# set: a file added, removed or rewritten later is a different run.
{chr(10).join(lines)}

# Nothing public may reproduce the reading. Sixty normalized characters is the
# threshold every frozen file clears.
LEAK_WINDOW = 60
WITHHELD_NAMES = {names}
RUNNER_STATUSES = {json.dumps([item["status"] for item in log["runner"]])}
EXECUTION_COMMIT = {json.dumps(log["runner"][-1]["execution_commit"])}
USAGE_STAGES = {json.dumps([stage["stage"] for stage in usage["stages"]])}


def _reading_windows(width: int) -> set[str]:
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


def test_the_frozen_artifact_set_is_exact_and_digest_pinned() -> None:
    for name in ("ontology-run", "results"):
        directory = HERE / name
        assert directory.is_dir()
        observed = sorted(
            f"{{name}}/{{path.name}}"
            for path in directory.iterdir()
            if path.is_file() and path.suffix != ".pyc" and path.name != ".gitkeep"
        )
        expected = sorted(
            relative for relative in FROZEN_ARTIFACTS if relative.startswith(f"{{name}}/")
        )
        assert observed == expected
    for relative, value in FROZEN_ARTIFACTS.items():
        assert _digest(HERE / relative) == value, relative


def test_no_frozen_artifact_reproduces_the_reading() -> None:
    windows = _reading_windows(LEAK_WINDOW)

    for relative in FROZEN_ARTIFACTS:
        text = _plain((HERE / relative).read_text(encoding="utf-8"))
        shared = [
            text[start : start + LEAK_WINDOW]
            for start in range(0, max(1, len(text) - LEAK_WINDOW + 1))
            if text[start : start + LEAK_WINDOW] in windows
        ]
        assert shared == [], (relative, shared[:1])


def test_every_withheld_artifact_is_named_by_identity_and_stays_private() -> None:
    record = json.loads((HERE / "results/withheld-artifacts.json").read_bytes())
    public = {{Path(relative).name for relative in FROZEN_ARTIFACTS}}

    assert record["schema"] == "malleus.paper-v4.run-25-withheld-artifacts/v1"
    assert record["run_id"] == "run-25"
    names = [item["name"] for item in record["withheld"]]
    assert sorted(names) == WITHHELD_NAMES
    assert not set(names) & public
    assert max(record["check"]["public_files_measured"].values()) < LEAK_WINDOW
    for item in record["withheld"]:
        private = item["private_path"]
        assert private.startswith("private/paper-v4-v4-run-25/")
        assert _digest(ROOT / private) == item["sha256"], private


def test_the_ontology_run_result_records_the_given_ontology_not_an_authored_one() -> None:
    result = json.loads((HERE / "ontology-run/result.json").read_bytes())
    producer = result["producer"]
    attempts = result["attempts"]

    assert result["schema"] == "malleus.paper-v4.ontology-run-result/v1"
    assert result["status"] == "ACCEPTED"
    assert result["run_id"] == "run-25"
    assert result["core"] == {{
        "core_commit": _contract()["core_gate"]["execution_baseline"]["core_commit"],
        "core_tree": _contract()["core_gate"]["execution_baseline"]["core_tree"],
    }}
    assert result["producer_input_manifest_sha256"] == _digest(PRODUCER_MANIFEST)
    # The ontology is not this producer's and the record says so three ways.
    assert result["ontology_source"] == "FIXED_RUN_23_ACCEPTED_ONTOLOGY"
    assert result["ontology_authored_by"] == FIXED_ONTOLOGY_RUN
    assert result["ontology_source_commit"] == FIXED_ONTOLOGY_COMMIT
    assert result["ontology_source_path"] == FIXED_ONTOLOGY_PATH
    assert result["accepted_ontology_sha256"] == FIXED_ONTOLOGY_SHA
    assert producer["ontology_authored"] is False
    assert producer["phases"] == "POPULATION_ONLY"
    assert producer["diagnostic_return_limit"] == 0
    assert producer["kind"] == "CLAUDE_CODE_FRESH_SUBAGENT"
    assert producer["requested_model"] == {json.dumps(log["launches"][0]["requested_model"])}
    assert producer["model_id"] == {json.dumps(log["launches"][0]["model_id"])}
    assert producer["questions_visible"] is False
    assert producer["fallback_used"] is False
    assert producer["hand_repair_used"] is False
    log = json.loads((HERE / "results/launch-log.json").read_bytes())
    assert producer["diagnostic_returns"] == len(log["gate"]) - 1
    assert [item["status"] for item in attempts] == ["ACCEPTED"]
    for item in attempts:
        assert _digest(ROOT / item["ontology_path"]) == item["ontology_sha256"]
        assert _digest(ROOT / item["diagnostic_path"]) == item["diagnostic_sha256"]
        assert item["authored_by"] == FIXED_ONTOLOGY_RUN
    accepted = result["accepted"]
    assert accepted["fact_count"] == FIXED_ONTOLOGY_FACTS
    assert accepted["population_surface_families"] == {json.dumps({k: len(v) for k, v in sorted(families.items())})}
    # The gate reproduced run-23's five digests and its fact count at the same
    # Core commit, which is what makes this the same ontology and not a copy.
    reproduces = result["reproduces_run_23"]
    prior = json.loads((RUN_23 / "ontology-run/result.json").read_bytes())["accepted"]
    for key in (
        "ontology_sha256",
        "validated_contract_sha256",
        "validated_fact_set_sha256",
        "population_surface_sha256",
        "grounding_receipt_sha256",
        "fact_count",
    ):
        assert reproduces[key] is True, key
        assert accepted[key] == prior[key], key
    assert result["citation_check"]["fabricated"] == 0
    assert result["citation_check"]["unverified"] == 0
    assert result["citation_check"]["inherited"] is False


def test_the_accepted_surface_is_run_23s_surface() -> None:
    surface = json.loads((HERE / "ontology-run/population-surface.json").read_bytes())
    by_family: dict[str, list[str]] = {{}}
    for item in surface["record_types"]:
        by_family.setdefault(item["family"], []).append(item["name"])

    assert sorted(by_family) == ["ENTITY", "EVENT", "RELATION"]
    assert sorted(by_family["EVENT"]) == {json.dumps(sorted(families.get("EVENT", [])))}
    assert sorted(by_family["RELATION"]) == {json.dumps(sorted(families.get("RELATION", [])))}
    # Byte for byte run-23's, because the ontology and the compiler are.
    assert (HERE / "ontology-run/population-surface.json").read_bytes() == (
        RUN_23 / "ontology-run/population-surface.json"
    ).read_bytes()


def test_the_run_result_is_admitted_replayed_and_binds_the_frozen_stage() -> None:
    result = json.loads((HERE / "results/run-result.json").read_bytes())
    census = json.loads((HERE / "results/census.json").read_bytes())
    events = json.loads((HERE / "results/paper-events.json").read_bytes())
    ontology_run = json.loads((HERE / "ontology-run/result.json").read_bytes())

    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["run_id"] == "run-25"
    assert result["actor_id"] == "actor:overseer-run-25"
    assert (
        result["transaction_time"]
        == (HERE / "results/transaction-time.txt").read_text(encoding="utf-8").strip()
    )
    assert result["ontology_sha256"] == ontology_run["accepted_ontology_sha256"]
    assert result["ontology_sha256"] == FIXED_ONTOLOGY_SHA
    assert result["reading_sha256"] == _contract()["source"]["selected_reading_sha256"]
    assert result["reopen_matches_admitted"] == {{"receipt": True, "export_records": True}}
    assert result["admitted_receipt_sha256"] == result["replay_receipt_sha256"]
    assert result["trace_summary_sha256"] == _digest(HERE / "results/trace-summary.json")
    assert result["ledger_event_count"] == {result["ledger_event_count"]}
    assert result["graph"] == {json.dumps(result["graph"])}
    assert result["gaps_by_kind"] == {json.dumps(result["gaps_by_kind"])}
    assert result["census"] == census
    assert census["assertions"] == {json.dumps(census["assertions"])}
    assert census["blocks_total"] == census["blocks_reviewed"] == 186
    assert census["derivation"]["non_local_relations"] == {census["derivation"]["non_local_relations"]}
    assert census["derivation"]["top_hubs"][0]["records"] == {census["derivation"]["top_hubs"][0]["records"]}
    # The stage-acceptance event names whose ontology was accepted.
    assert events["events"][0]["ontology_sha256"] == result["ontology_sha256"]
    assert events["events"][0]["ontology_source"] == "FIXED_RUN_23_ACCEPTED_ONTOLOGY"
    assert events["events"][0]["ontology_authored_by"] == FIXED_ONTOLOGY_RUN
    assert events["events"][0]["non_claim"] == "STAGE_ACCEPTANCE_NOT_DOMAIN_ADEQUACY"


def test_the_binding_was_frozen_at_acceptance_and_executed_unchanged() -> None:
    accepted = json.loads((HERE / "results/query-binding.acceptance.json").read_bytes())
    executed = json.loads((HERE / "results/native-query-binding.json").read_bytes())
    result = json.loads((HERE / "results/run-result.json").read_bytes())
    log = json.loads((HERE / "results/launch-log.json").read_bytes())
    type_sets = json.loads((HERE / "results/query-type-sets.json").read_bytes())

    assert accepted["bound_at_stage"] == executed["bound_at_stage"] == "ONTOLOGY_ACCEPTANCE"
    assert executed["schema"] == {json.dumps(binding["schema"])}
    assert accepted["bound_after_replay_receipt_sha256"] == "PENDING"
    assert executed["bound_after_replay_receipt_sha256"] == result["replay_receipt_sha256"]
    assert accepted["cases_sha256"] == executed["cases_sha256"] == log["query"]["cases_sha256"]
    assert log["query"]["binding_at_acceptance_sha256"] == _digest(
        HERE / "results/query-binding.acceptance.json"
    )
    assert log["query"]["type_sets_sha256"] == _digest(HERE / "results/query-type-sets.json")
    assert log["query"]["bound_at"] < log["launches"][0]["phase_two"]["dispatched_at"]
    assert sorted(type_sets) == {json.dumps(question_ids)}
    assert sum(len(query["cases"]) for query in executed["queries"]) == {cases}
    assert log["query"]["rows_by_question"] == {json.dumps(rows)}
    # The type sets and the binding are run-23's, because the surface is.
    assert (HERE / "results/query-type-sets.json").read_bytes() == (
        RUN_23 / "results/query-type-sets.json"
    ).read_bytes()
    assert accepted["cases_sha256"] == json.loads(
        (RUN_23 / "results/query-binding.acceptance.json").read_bytes()
    )["cases_sha256"]


def test_the_v2_launch_log_and_the_derived_cost_record_agree() -> None:
    log = json.loads((HERE / "results/launch-log.json").read_bytes())
    usage = json.loads((HERE / "results/usage.json").read_bytes())
    launch = log["launches"][0]

    assert log["schema"] == "malleus.paper-v4.producer-launch-log/v2"
    assert log["protocol"] == {json.dumps(log["protocol"])}
    assert launch["condition"] == "FIXED_ONTOLOGY_CONTROL"
    assert launch["requested_model"] == {json.dumps(log["launches"][0]["requested_model"])}
    assert launch["model_id"] == {json.dumps(log["launches"][0]["model_id"])}
    assert launch["first_stage"] == "POPULATION"
    assert launch["phase"] == "POPULATION"
    assert [entry["status"] for entry in log["gate"]] == ["ACCEPTED"]
    assert log["gate"][-1]["citation_check"]["fabricated"] == 0
    assert log["gate"][-1]["gated_before_the_producer_was_spawned"] is True
    assert log["gate"][-1]["diagnostic_returns_used"] == 0
    assert [entry["status"] for entry in log["runner"]] == RUNNER_STATUSES
    assert log["runner"][-1]["status"] == "ADMITTED_AND_REPLAYED"
    assert log["runner"][-1]["execution_commit"] == EXECUTION_COMMIT
    assert [stage["stage"] for stage in usage["stages"]] == USAGE_STAGES
    assert sum(stage["tokens"] for stage in usage["stages"]) == usage["producer_total_tokens"]


def test_the_paper_ledger_entry_is_the_overseers_to_write() -> None:
    """This cell writes no ledger entry, and its contract does not claim an id."""

    ledger = PAPER_LEDGER.read_text(encoding="utf-8")

    assert _contract()["protocol"]["opening_ledger_entry"] == (
        "PENDING_THE_OVERSEER_WRITES_THE_PAPER_LEDGER"
    )
    assert "actor:overseer-run-25" not in ledger
'''


def evaluation_block() -> str:
    manifest = json.loads((PACKAGE / "review-input-manifest.json").read_bytes())
    summary = json.loads((PUBLIC / "query-trace-summary.json").read_bytes())
    materials = [item["name"] for item in manifest["materials"]]
    rows = manifest["rows_per_question"]
    return f'''
def test_the_evaluation_directory_carries_the_frozen_review_package() -> None:
    directory = EVALUATION / "run-25"
    present = {{path.name for path in directory.iterdir() if path.name != "__pycache__"}}

    assert {{
        "build_review_inputs.py",
        "review-input-manifest.json",
        "review-record.blank.md",
        "review-task.md",
    }} <= present
    manifest = json.loads((directory / "review-input-manifest.json").read_bytes())
    summary = json.loads((HERE / "results/query-trace-summary.json").read_bytes())
    assert manifest["run_id"] == "run-25"
    assert [item["name"] for item in manifest["materials"]] == {json.dumps(materials)}
    assert manifest["rows_per_question"] == {json.dumps(rows)}
    assert sum(manifest["rows_per_question"].values()) == {sum(rows.values())}
    assert summary["witnesses_traced"] == {summary["witnesses_traced"]}
    for name in ("review-task.md", "review-record.blank.md"):
        assert "{{{{" not in (directory / name).read_text(encoding="utf-8"), name
'''


def invert_placeholders(text: str) -> str:
    first = re.search(
        r"    # One row-count placeholder per question, plus the two totals, and nothing\n"
        r"    # else\. The builder refuses to write a package that carries any other\.\n"
        r"    surviving = sorted\(set\(re\.findall\(r\"\\\{\\\{\[A-Z_0-9\]\+\\\}\\\}\", task\)\)\)\n"
        r"    assert surviving == sorted\(\n.*?\n    \)\n",
        text,
        re.S,
    )
    assert first, "task placeholder block not found"
    text = (
        text[: first.start()]
        + '''    # Frozen: the builder filled every row-count placeholder and the two totals
    # from this cell's own query result and trace summary; none survives.
    manifest = json.loads((REVIEW_PACKAGE / "review-input-manifest.json").read_bytes())
    assert re.findall(r"\\{\\{[A-Z_0-9]+\\}\\}", task) == []
    for question_id in question_ids:
        assert str(manifest["rows_per_question"][question_id]) in task, question_id
    assert str(sum(manifest["rows_per_question"].values())) in task
    assert str(manifest["witnesses_traced"]) in task
'''
        + text[first.end() :]
    )
    second = re.search(
        r"    # The counts are the producer's and are not here yet; nothing else survives\.\n"
        r"    surviving = sorted\(set\(re\.findall\(r\"\\\{\\\{\[A-Z_0-9\]\+\\\}\\\}\", record\)\)\)\n"
        r"    assert \"\{\{ROWS_TOTAL\}\}\" in surviving\n"
        r"    assert \"\{\{WITNESSES_TOTAL\}\}\" in surviving\n"
        r"    assert all\(\n.*?\n    \)\n",
        text,
        re.S,
    )
    assert second, "blank placeholder block not found"
    text = (
        text[: second.start()]
        + '''    # Frozen: the builder filled the counts at freeze; no placeholder survives.
    assert re.findall(r"\\{\\{[A-Z_0-9]+\\}\\}", record) == []
'''
        + text[second.end() :]
    )
    return text.replace(
        """    they are figures of a producer that has not run, so they stay as
    placeholders and the builder fills them at freeze. Nothing else may survive.""",
        """    they are figures of a producer that has not run, so they stayed as
    placeholders until the builder filled them at freeze. Nothing survives now.""",
        1,
    )


def main() -> int:
    text = TEST.read_text(encoding="utf-8")
    old = re.search(
        r"\ndef test_the_result_directories_are_empty_until_the_producer_runs\(\) -> None:.*?\n\n\n",
        text,
        re.S,
    )
    assert old, "open-stage result-directory test not found"
    text = text[: old.start()] + "\n" + frozen_block().lstrip("\n") + "\n\n" + text[old.end() :]
    old = re.search(
        r"\ndef test_the_evaluation_directory_carries_the_open_package_and_nothing_yet\(\) -> None:.*?\n\n\n",
        text,
        re.S,
    )
    assert old, "open-stage evaluation test not found"
    text = text[: old.start()] + "\n" + evaluation_block().lstrip("\n") + "\n\n" + text[old.end() :]
    text = invert_placeholders(text)
    TEST.write_text(text, encoding="utf-8")
    print("test_contract.py rewritten from the frozen files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
