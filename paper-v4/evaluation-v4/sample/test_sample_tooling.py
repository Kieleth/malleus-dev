"""Guards for the independent-judge sample tooling.

Everything here runs from fixtures this file writes into ``tmp_path``, shaped
like a protocol v3 document cell: a review record with one fenced JSON block and
one entry per distinct witness, a review input manifest binding its materials by
digest, a query result whose rows carry a ``witness`` and a ``record``, and a
selected reading of id-bearing text blocks. No private file of the repository is
opened, so the paper gate runs these without the private fixtures present.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sys

import pytest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import agreement  # noqa: E402
import build_packet  # noqa: E402
import sample_common  # noqa: E402
import sample_witnesses  # noqa: E402
import validate_judge_record  # noqa: E402

Refusal = sample_common.Refusal

LABELS = ("SUPPORTED", "PARTIAL", "UNSUPPORTED", "NOT_EVALUABLE")
BLOCK_TEXT = (
    "The instrument recorded a temperature of {value} degrees at station {index} "
    "during the second traverse of the survey line, and the operator logged it."
)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _write(path: Path, value: object) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    source = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(source)
    return source


def _block_id(index: int) -> str:
    return f"page:1:block:{index:03d}"


def _reading(blocks: int) -> dict:
    return {
        "schema": "malleus.paper-v4.selected-reading/v1",
        "source_sha256": "sha256:" + "0" * 64,
        "pages": [
            {
                "page": 1,
                "blocks": [
                    {
                        "id": _block_id(index),
                        "ordinal": index,
                        "text": BLOCK_TEXT.format(value=index, index=index),
                    }
                    for index in range(blocks)
                ],
            }
        ],
    }


def _witness_key(cell: str, index: int) -> str:
    return f"{cell}:entity:w{index:03d}"


def _review_record(cell: str, count: int) -> bytes:
    witnesses = [
        {
            "witness_key": _witness_key(cell, index),
            "source_support": LABELS[index % 4] if index % 7 == 0 else "SUPPORTED",
            "rationale": f"DIGEST_OK NO_SUBJECT_IN_ROW judged from block {index}.",
            "source_locators": [_block_id(index)],
        }
        for index in range(count)
    ]
    record = {
        "schema": "malleus.paper-v4.source-grounded-review/v3",
        "status": "PRELIMINARY_COMPLETE",
        "inputs": {},
        "preliminary": {"evaluator_kind": "CLAUDE_PRELIMINARY", "actor_id": f"actor:{cell}"},
        "questions": [],
        "ratification": {},
        "witnesses": witnesses,
    }
    text = (
        f"# synthetic {cell} review record\n\n```json\n"
        + json.dumps(record, ensure_ascii=False, indent=2)
        + "\n```\n"
    )
    return text.encode("utf-8")


def _query_result(cell: str, count: int) -> dict:
    return {
        "schema": "malleus.paper-v4.query-result/v3",
        "queries": [
            {
                "query_id": "q-01",
                "question_id": "CQ-T1-01",
                "rows": [
                    {
                        "case_ordinals": [index],
                        "kind": "ENTITY",
                        "record": {
                            "name": f"station {index}",
                            "assertion_locator": f"assertion:{index:03d}",
                        },
                        "witness": {"record_id": _witness_key(cell, index)},
                    }
                    for index in range(count)
                ],
            }
        ],
    }


@pytest.fixture
def repo(tmp_path: Path) -> dict:
    """A synthetic repository root with three cells of different sizes."""

    cells = {"run-a": 40, "run-b": 24, "run-c": 8}
    reading_path = tmp_path / "private/paper-v4-text-layer/selected-reading.json"
    reading_source = _write(reading_path, _reading(max(cells.values())))
    for cell, count in cells.items():
        base = tmp_path / "paper-v4/evaluation-v4" / cell
        base.mkdir(parents=True, exist_ok=True)
        (base / "review-record.preliminary.md").write_bytes(_review_record(cell, count))
        query_path = tmp_path / f"private/paper-v4-v4-{cell}/query/query-result.json"
        query_source = _write(query_path, _query_result(cell, count))
        _write(
            base / "review-input-manifest.json",
            {
                "run_id": cell,
                "evidence_surface": {"kind": "SELECTED_READING_TEXT_LAYER"},
                "fixed_identities": {"selected_reading_sha256": _digest(reading_source)},
                "materials": [
                    {
                        "name": "selected_reading",
                        "path": str(reading_path.relative_to(tmp_path)),
                        "sha256": _digest(reading_source),
                        "visibility": "PRIVATE",
                    },
                    {
                        "name": "query_result",
                        "path": str(query_path.relative_to(tmp_path)),
                        "sha256": _digest(query_source),
                        "visibility": "PRIVATE",
                    },
                ],
            },
        )
    return {"root": tmp_path, "cells": cells, "reading": _reading(max(cells.values()))}


def _sample(repo: dict, size: int = 12, seed: int = 4242, **kwargs) -> dict:
    if kwargs.get("all_label"):
        size = None
    return sample_witnesses.build(
        repo["root"], list(repo["cells"]), seed, size=size, **kwargs
    )


def _sample_file(repo: dict, size: int = 12, seed: int = 4242, **kwargs) -> tuple[Path, dict, bytes]:
    sample = _sample(repo, size, seed, **kwargs)
    name = sample_witnesses.target_name(
        seed, kwargs.get("only_label"), kwargs.get("all_label")
    )
    path = repo["root"] / "paper-v4/evaluation-v4/sample" / name
    source = sample_common.write_json(path, sample)
    return path, sample, source


# --- the two documents ---------------------------------------------------


def test_blank_record_is_the_shape_the_validator_expects() -> None:
    blank = sample_common.markdown_record(
        (HERE / "judge-record.blank.md").read_bytes(), "blank judge record"
    )
    assert blank["schema"] == sample_common.JUDGE_RECORD_SCHEMA
    assert set(blank) == {"schema", "sample_sha256", "judge", "judgements"}
    assert blank["judge"]["evaluator_kind"] == validate_judge_record.EVALUATOR_KIND
    assert set(blank["judge"]) == {
        "evaluator_kind",
        "model_id",
        "actor_id",
        "reasoning_effort",
    }
    assert set(blank["judgements"][0]) == {
        "cell",
        "witness_key",
        "source_support",
        "rationale",
    }


def test_task_template_never_hands_the_judge_the_sample() -> None:
    """The sample file carries the recorded labels and its name carries the stratum."""

    for name in ("judge-task.template.md", "judge-record.blank.md"):
        text = (HERE / name).read_text(encoding="utf-8")
        assert "<SAMPLE_PATH>" not in text
        assert "--sample" not in text
    template = (HERE / "judge-task.template.md").read_text(encoding="utf-8")
    used = set(re.findall(r"<([A-Z_]+)>", template))
    declared = set(re.findall(r"<([A-Z_]+)>", template.split("No placeholder")[0]))
    assert used == declared, f"undeclared or unused placeholders: {used ^ declared}"


def test_task_template_carries_the_frozen_label_definitions() -> None:
    """The four definitions are the frozen v3 task's, character for character."""

    frozen = (
        HERE.parent / "review-task-protocol-v3.template.md"
    ).read_text(encoding="utf-8")
    template = (HERE / "judge-task.template.md").read_text(encoding="utf-8")
    start = frozen.index("- `SUPPORTED`:")
    end = frozen.index("\n\n", start)
    assert frozen[start:end] in template
    for label in LABELS:
        assert f"`{label}`" in template
    # Protocol v3 carries the same four labels, and no fifth.
    protocol = json.loads(
        (HERE.parent / "review-protocol-v3.json").read_bytes()
    )
    assert tuple(protocol["judgments"]["source_support"]) == LABELS


# --- sampling ------------------------------------------------------------


def test_sampling_is_deterministic_for_a_seed(repo: dict) -> None:
    first = _sample(repo, 12, 7)
    second = _sample(repo, 12, 7)
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert [entry["witness_key"] for entry in first["witnesses"]] == [
        entry["witness_key"] for entry in second["witnesses"]
    ]


def test_another_seed_draws_another_sample(repo: dict) -> None:
    first = {entry["witness_key"] for entry in _sample(repo, 12, 7)["witnesses"]}
    second = {entry["witness_key"] for entry in _sample(repo, 12, 8)["witnesses"]}
    assert first != second


def test_stratification_sums_and_is_proportional(repo: dict) -> None:
    sample = _sample(repo, 12, 7)
    per_cell = {entry["cell"]: entry["sampled"] for entry in sample["cells"]}
    assert sum(per_cell.values()) == 12 == len(sample["witnesses"])
    # 40, 24 and 8 of 72 witnesses at a size of 12 gives quotas of 6.67, 4.00 and
    # 1.33; the floors are 6, 4 and 1 and the one remaining seat goes to the
    # largest fraction.
    assert per_cell == {"run-a": 7, "run-b": 4, "run-c": 1}
    drawn = {cell: 0 for cell in per_cell}
    for entry in sample["witnesses"]:
        drawn[entry["cell"]] += 1
    assert drawn == per_cell


def test_every_cell_keeps_at_least_one_witness() -> None:
    share = sample_witnesses.allocate({"big": 1000, "tiny": 3}, 10)
    assert share["tiny"] >= 1
    assert sum(share.values()) == 10


def test_allocation_refuses_a_size_it_cannot_meet() -> None:
    with pytest.raises(Refusal, match="below one per cell"):
        sample_witnesses.allocate({"a": 10, "b": 10, "c": 10}, 2)
    with pytest.raises(Refusal, match="exceeds the 30 witnesses"):
        sample_witnesses.allocate({"a": 10, "b": 10, "c": 10}, 31)


def test_sample_carries_the_recorded_label_and_the_record_digest(repo: dict) -> None:
    sample = _sample(repo, 12, 7)
    record = (repo["root"] / "paper-v4/evaluation-v4/run-a/review-record.preliminary.md").read_bytes()
    by_cell = {entry["cell"]: entry for entry in sample["cells"]}
    assert by_cell["run-a"]["record_sha256"] == _digest(record)
    for entry in sample["witnesses"]:
        assert entry["recorded_source_support"] in LABELS
        assert entry["source_locators"]


# --- label strata --------------------------------------------------------
#
# The synthetic records label index%7==0 with LABELS[index%4] and everything else
# SUPPORTED, which gives run-a 36 SUPPORTED and 1 PARTIAL of 40, run-b 21 and 1
# of 24, and run-c 7 SUPPORTED and no PARTIAL of 8.


def test_only_label_draws_inside_that_label(repo: dict) -> None:
    sample = _sample(repo, 12, 7, only_label="SUPPORTED")
    assert sample["stratum"] == {"label": "SUPPORTED", "population": "RECORDED_SUPPORTED"}
    assert {entry["recorded_source_support"] for entry in sample["witnesses"]} == {
        "SUPPORTED"
    }
    per_cell = {entry["cell"]: entry for entry in sample["cells"]}
    assert {cell: entry["witnesses_in_stratum"] for cell, entry in per_cell.items()} == {
        "run-a": 36,
        "run-b": 21,
        "run-c": 7,
    }
    # 36, 21 and 7 of 64 at a size of 12: floors 6, 3 and 1, two seats left over.
    assert {cell: entry["sampled"] for cell, entry in per_cell.items()} == {
        "run-a": 7,
        "run-b": 4,
        "run-c": 1,
    }
    assert len(sample["witnesses"]) == 12


def test_only_label_is_deterministic_and_its_own_stream(repo: dict) -> None:
    first = _sample(repo, 12, 7, only_label="SUPPORTED")
    second = _sample(repo, 12, 7, only_label="SUPPORTED")
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    unfiltered = {entry["witness_key"] for entry in _sample(repo, 12, 7)["witnesses"]}
    filtered = {entry["witness_key"] for entry in first["witnesses"]}
    assert filtered != unfiltered


def test_only_label_refuses_a_cell_that_holds_none_of_it(repo: dict) -> None:
    with pytest.raises(Refusal, match="run-c holds no witness recorded PARTIAL"):
        _sample(repo, 3, 7, only_label="PARTIAL")


def test_all_label_takes_every_one_and_tolerates_an_empty_cell(repo: dict) -> None:
    sample = _sample(repo, seed=7, all_label="PARTIAL")
    assert sample["stratification"] == "COMPLETE_STRATUM_NOT_SAMPLED"
    assert {entry["recorded_source_support"] for entry in sample["witnesses"]} == {
        "PARTIAL"
    }
    per_cell = {entry["cell"]: entry["sampled"] for entry in sample["cells"]}
    assert per_cell == {"run-a": 1, "run-b": 1, "run-c": 0}
    assert sample["size"] == len(sample["witnesses"]) == 2
    # Every PARTIAL witness of every cell, not a draw from them.
    everything = set()
    for cell, count in repo["cells"].items():
        record = sample_common.markdown_record(
            (
                repo["root"] / "paper-v4/evaluation-v4" / cell / "review-record.preliminary.md"
            ).read_bytes(),
            cell,
        )
        everything |= {
            (cell, witness["witness_key"])
            for witness in record["witnesses"]
            if witness["source_support"] == "PARTIAL"
        }
    assert {
        (entry["cell"], entry["witness_key"]) for entry in sample["witnesses"]
    } == everything


def test_all_label_is_not_a_seeded_draw(repo: dict) -> None:
    """The seed is recorded, and it changes nothing: a complete stratum is complete."""

    first = _sample(repo, seed=1, all_label="PARTIAL")
    second = _sample(repo, seed=99, all_label="PARTIAL")
    assert first["seed"] == 1 and second["seed"] == 99
    assert first["witnesses"] == second["witnesses"]
    assert first["cells"] == second["cells"]


def test_default_draw_is_unchanged_by_the_new_options(repo: dict) -> None:
    sample = _sample(repo, 12, 7)
    assert sample["stratum"] == {"label": None, "population": "EVERY_WITNESS"}
    assert {entry["cell"]: entry["sampled"] for entry in sample["cells"]} == {
        "run-a": 7,
        "run-b": 4,
        "run-c": 1,
    }
    for entry in sample["cells"]:
        assert entry["witnesses_in_stratum"] == entry["witnesses_in_record"]


def test_build_refuses_conflicting_or_missing_options(repo: dict) -> None:
    with pytest.raises(Refusal, match="run the script twice"):
        sample_witnesses.build(
            repo["root"],
            list(repo["cells"]),
            7,
            size=12,
            only_label="SUPPORTED",
            all_label="PARTIAL",
        )
    with pytest.raises(Refusal, match="is not one of"):
        sample_witnesses.build(
            repo["root"], list(repo["cells"]), 7, size=12, only_label="MOSTLY"
        )
    with pytest.raises(Refusal, match="a complete stratum has no size"):
        sample_witnesses.build(
            repo["root"], list(repo["cells"]), 7, size=12, all_label="PARTIAL"
        )
    with pytest.raises(Refusal, match="needs --size"):
        sample_witnesses.build(repo["root"], list(repo["cells"]), 7)


def test_cells_must_be_named_every_time(repo: dict, tmp_path: Path) -> None:
    """No default cell set: one would go stale the moment a cell is rebound."""

    assert not hasattr(sample_witnesses, "DEFAULT_CELLS")
    with pytest.raises(SystemExit) as exit_code:
        sample_witnesses.main(
            ["--seed", "7", "--size", "12", "--root", str(repo["root"])]
        )
    assert exit_code.value.code == 2
    assert (
        sample_witnesses.main(
            [
                "--cells",
                *repo["cells"],
                "--seed",
                "7",
                "--size",
                "12",
                "--root",
                str(repo["root"]),
                "--output",
                str(tmp_path / "out"),
            ]
        )
        == 0
    )
    assert (tmp_path / "out" / "sample-7.json").exists()


def test_strata_at_one_seed_get_their_own_file_names() -> None:
    assert sample_witnesses.target_name(5, None, None) == "sample-5.json"
    assert sample_witnesses.target_name(5, "SUPPORTED", None) == "sample-5-supported.json"
    assert sample_witnesses.target_name(5, None, "PARTIAL") == "sample-5-partial-all.json"


# --- packet --------------------------------------------------------------


def test_packet_is_blind_and_carries_the_cited_text(repo: dict) -> None:
    path, sample, source = _sample_file(repo)
    packet = build_packet.build(repo["root"], sample, _digest(source))
    text = json.dumps(packet)
    assert "recorded_source_support" not in text
    assert "rationale\": \"DIGEST_OK" not in text
    for entry in packet["witnesses"]:
        assert entry["judgement"] == {"source_support": None, "rationale": None}
        assert entry["cited_blocks"]
        for block in entry["cited_blocks"]:
            assert block["text"]
        assert entry["returned"]["witness"]["record_id"] == entry["witness_key"]
        assert "case_ordinals" not in entry["returned"]
    assert len(packet["witnesses"]) == len(sample["witnesses"])
    assert path.exists()


def test_packet_of_a_label_stratum_does_not_name_the_label(repo: dict) -> None:
    """The stratum is the recorded label of every witness in it. The judge sees neither."""

    path, sample, source = _sample_file(repo, 12, 7, only_label="SUPPORTED")
    packet = build_packet.build(repo["root"], sample, _digest(source))
    text = json.dumps(packet)
    assert "recorded_source_support" not in text
    assert "stratum" not in packet
    for entry in packet["witnesses"]:
        assert entry["judgement"] == {"source_support": None, "rationale": None}
        assert "recorded_source_support" not in entry
    # No label word at all in this fixture. On real data a record field may hold a
    # domain value that contains one (run-25 carries hypothesis_disposition
    # NOT_SUPPORTED), so this is a fixture check, not the rule; the rule is the
    # structural assertions above.
    for label in LABELS:
        assert label not in text
    name = build_packet.packet_name(sample["seed"], _digest(source))
    assert name.startswith("packet-7-") and name.endswith(".json")
    for label in LABELS:
        assert label.lower() not in name
    # The sample file may say which stratum it is; only the parent reads it.
    assert path.name == "sample-7-supported.json"


def test_two_strata_at_one_seed_write_two_packets(repo: dict) -> None:
    _, supported, supported_source = _sample_file(repo, 12, 7, only_label="SUPPORTED")
    _, partial, partial_source = _sample_file(repo, seed=7, all_label="PARTIAL")
    first = build_packet.packet_name(7, _digest(supported_source))
    second = build_packet.packet_name(7, _digest(partial_source))
    assert first != second
    assert len(partial["witnesses"]) == 2
    packet = build_packet.build(repo["root"], partial, _digest(partial_source))
    assert len(packet["witnesses"]) == 2


def test_packet_refuses_a_record_that_changed_after_the_draw(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    record = repo["root"] / "paper-v4/evaluation-v4/run-b/review-record.preliminary.md"
    record.write_bytes(record.read_bytes() + b"\n<!-- edited -->\n")
    with pytest.raises(Refusal, match="changed after the sample was drawn"):
        build_packet.build(repo["root"], sample, _digest(source))


def test_packet_refuses_a_material_that_differs_from_its_digest(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    query = repo["root"] / "private/paper-v4-v4-run-c/query/query-result.json"
    query.write_bytes(query.read_bytes().replace(b"station 0", b"station zero"))
    with pytest.raises(Refusal, match="query result differs from the digest"):
        build_packet.build(repo["root"], sample, _digest(source))


def test_packet_cli_refuses_a_public_destination(repo: dict) -> None:
    path, _, _ = _sample_file(repo)
    status = build_packet.main(
        [
            "--sample",
            str(path),
            "--root",
            str(repo["root"]),
            "--output",
            str(repo["root"] / "paper-v4/evaluation-v4/sample"),
        ]
    )
    assert status == 2


# --- judge record --------------------------------------------------------


def _judge_record(sample: dict, source: bytes, **overrides) -> bytes:
    judgements = overrides.pop(
        "judgements",
        [
            {
                "cell": entry["cell"],
                "witness_key": entry["witness_key"],
                "source_support": "SUPPORTED",
                "rationale": "The cited block names the station this record projects.",
            }
            for entry in sample["witnesses"]
        ],
    )
    record = {
        "schema": "malleus.paper-v4.independent-judge-record/v1",
        "sample_sha256": overrides.pop("sample_sha256", _digest(source)),
        "judge": overrides.pop(
            "judge",
            {
                "evaluator_kind": "INDEPENDENT_MODEL_JUDGE",
                "model_id": "fable",
                "actor_id": "actor:fable-judge",
                "reasoning_effort": "high",
            },
        ),
        "judgements": judgements,
    }
    record.update(overrides)
    text = "# synthetic judge record\n\n```json\n" + json.dumps(record, indent=2) + "\n```\n"
    return text.encode("utf-8")


def test_validator_accepts_a_complete_record(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    record = validate_judge_record.validate(
        _judge_record(sample, source), source, repo["reading"]
    )
    assert len(record["judgements"]) == len(sample["witnesses"])


def test_validator_refuses_a_short_record(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    full = json.loads(
        _judge_record(sample, source).decode("utf-8").split("```json\n")[1].split("\n```")[0]
    )
    with pytest.raises(Refusal, match="sampled witnesses are unjudged"):
        validate_judge_record.validate(
            _judge_record(sample, source, judgements=full["judgements"][:-1]),
            source,
            repo["reading"],
        )


def test_validator_refuses_an_extra_witness(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    extra = {
        "cell": "run-a",
        "witness_key": "run-a:entity:w999",
        "source_support": "SUPPORTED",
        "rationale": "A witness the sample never drew.",
    }
    judgements = [
        {
            "cell": entry["cell"],
            "witness_key": entry["witness_key"],
            "source_support": "SUPPORTED",
            "rationale": "The cited block names the station this record projects.",
        }
        for entry in sample["witnesses"]
    ] + [extra]
    with pytest.raises(Refusal, match="which the sample did not draw"):
        validate_judge_record.validate(
            _judge_record(sample, source, judgements=judgements), source, repo["reading"]
        )


def test_validator_refuses_a_duplicate_witness(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    judgements = [
        {
            "cell": entry["cell"],
            "witness_key": entry["witness_key"],
            "source_support": "SUPPORTED",
            "rationale": "The cited block names the station this record projects.",
        }
        for entry in sample["witnesses"]
    ]
    judgements[-1] = dict(judgements[0])
    with pytest.raises(Refusal, match="a second time"):
        validate_judge_record.validate(
            _judge_record(sample, source, judgements=judgements), source, repo["reading"]
        )


def test_validator_refuses_a_label_outside_the_four(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    judgements = [
        {
            "cell": entry["cell"],
            "witness_key": entry["witness_key"],
            "source_support": "MOSTLY_SUPPORTED",
            "rationale": "A label the protocol does not carry.",
        }
        for entry in sample["witnesses"]
    ]
    with pytest.raises(Refusal, match="a label outside"):
        validate_judge_record.validate(
            _judge_record(sample, source, judgements=judgements), source, repo["reading"]
        )


def test_validator_refuses_an_empty_rationale(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    judgements = [
        {
            "cell": entry["cell"],
            "witness_key": entry["witness_key"],
            "source_support": "SUPPORTED",
            "rationale": "  ",
        }
        for entry in sample["witnesses"]
    ]
    with pytest.raises(Refusal, match="carries no rationale"):
        validate_judge_record.validate(
            _judge_record(sample, source, judgements=judgements), source, repo["reading"]
        )


def test_validator_refuses_a_sample_digest_mismatch(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    with pytest.raises(Refusal, match="binds a different sample"):
        validate_judge_record.validate(
            _judge_record(sample, source, sample_sha256="sha256:" + "0" * 64),
            source,
            repo["reading"],
        )


def test_validator_refuses_reading_text_in_a_rationale(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    leak = BLOCK_TEXT.format(value=0, index=0)[:80]
    assert len(sample_common.normalized(leak)) >= sample_common.SHARED_RUN_CHARS
    judgements = [
        {
            "cell": entry["cell"],
            "witness_key": entry["witness_key"],
            "source_support": "SUPPORTED",
            "rationale": leak,
        }
        for entry in sample["witnesses"]
    ]
    with pytest.raises(Refusal, match="reproduces a 60-character run"):
        validate_judge_record.validate(
            _judge_record(sample, source, judgements=judgements), source, repo["reading"]
        )


def test_validator_refuses_a_wrong_evaluator_kind(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    with pytest.raises(Refusal, match="evaluator_kind must be"):
        validate_judge_record.validate(
            _judge_record(
                sample,
                source,
                judge={
                    "evaluator_kind": "CLAUDE_PRELIMINARY",
                    "model_id": "fable",
                    "actor_id": "actor:fable-judge",
                    "reasoning_effort": "high",
                },
            ),
            source,
            repo["reading"],
        )


# --- agreement -----------------------------------------------------------


def test_kappa_on_a_hand_computed_case() -> None:
    # Six SUPPORTED and four PARTIAL on each side, two of them crossed over.
    pairs = (
        [("SUPPORTED", "SUPPORTED")] * 5
        + [("SUPPORTED", "PARTIAL")]
        + [("PARTIAL", "PARTIAL")] * 3
        + [("PARTIAL", "SUPPORTED")]
    )
    agree, total, fraction = agreement.percent_agreement(pairs)
    assert (agree, total) == (8, 10)
    assert fraction == pytest.approx(0.8)
    kappa, expected = agreement.cohen_kappa(pairs)
    assert expected == pytest.approx(0.52)
    assert kappa == pytest.approx((0.8 - 0.52) / (1 - 0.52))
    assert kappa == pytest.approx(0.5833333333333334)


def test_kappa_is_undefined_when_one_label_is_used_everywhere() -> None:
    kappa, expected = agreement.cohen_kappa([("SUPPORTED", "SUPPORTED")] * 9)
    assert kappa is None
    assert expected == pytest.approx(1.0)


def test_report_counts_agreement_against_the_recorded_labels(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    record = validate_judge_record.validate(
        _judge_record(sample, source), source, repo["reading"]
    )
    lines = agreement.report(sample, [("judge-record-fable.md", record)])
    text = "\n".join(lines)
    recorded = [entry["recorded_source_support"] for entry in sample["witnesses"]]
    agree = sum(1 for label in recorded if label == "SUPPORTED")
    assert f"overall: {agree}/{len(recorded)}" in text
    assert "recorded vs judge" in text
    assert "confusion, differing" in text


def test_composition_prints_prevalence_without_a_judge(repo: dict) -> None:
    _, sample, _ = _sample_file(repo, 12, 7, only_label="SUPPORTED")
    lines = agreement.composition(sample)
    text = "\n".join(lines)
    assert "stratum: RECORDED_SUPPORTED" in text
    assert "prevalence of SUPPORTED: 12/12 = 1.000" in text
    assert "run-a: 7 drawn of 36 in the stratum, 40 in the record" in text
    assert "kappa" not in text


def test_composition_cli_runs_with_no_judge_record(repo: dict) -> None:
    path, _, _ = _sample_file(repo, seed=7, all_label="PARTIAL")
    assert agreement.main(["--sample", str(path)]) == 0


def test_report_compares_two_judges(repo: dict) -> None:
    _, sample, source = _sample_file(repo)
    first = validate_judge_record.validate(_judge_record(sample, source), source, repo["reading"])
    other = [
        {
            "cell": entry["cell"],
            "witness_key": entry["witness_key"],
            "source_support": "PARTIAL" if index == 0 else "SUPPORTED",
            "rationale": "The cited block names the station this record projects.",
        }
        for index, entry in enumerate(sample["witnesses"])
    ]
    second = validate_judge_record.validate(
        _judge_record(sample, source, judgements=other), source, repo["reading"]
    )
    lines = agreement.report(
        sample, [("judge-a.md", first), ("judge-b.md", second)]
    )
    text = "\n".join(lines)
    assert "judge-a.md vs judge-b.md" in text
    assert "judge vs judge" in text
    assert f"overall: {len(sample['witnesses']) - 1}/{len(sample['witnesses'])}" in text
