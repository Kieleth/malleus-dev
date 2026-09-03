"""Mechanical guards for claims duplicated across the paper-v4 publications."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper-v4"
MANUSCRIPT = PAPER / "manuscript.md"
TEX = PAPER / "arxiv/main.tex"
README = PAPER / "arxiv/README.md"
QUERY_RESULT = PAPER / "experiment-v2/results/query-result.json"
BUILD_RESULT = PAPER / "experiment-v2/results/experiment-result.json"
COMPILE_RECEIPT = PAPER / "experiment-v2/ontology-run/compilation/compile-receipt.json"
REPRODUCER_COMMIT = "8e818103e6867e326544123a30abe756bdd45117"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_publication_claims_match_frozen_v2_results() -> None:
    query = json.loads(QUERY_RESULT.read_bytes())
    build = json.loads(BUILD_RESULT.read_bytes())
    compile_receipt = json.loads(COMPILE_RECEIPT.read_bytes())

    assert [len(item["rows"]) for item in query["queries"]] == [0, 2, 4, 0]
    assert query["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert (build["entity_count"], build["relation_count"]) == (7, 6)
    assert compile_receipt["fact_count"] == 4146
    assert {item["module_id"] for item in compile_receipt["sources"]} == {
        "linkml:types",
        "malleus",
        "paper-v4:mid-ocean-ridge-geodynamics",
    }

    for publication in (MANUSCRIPT, TEX):
        body = _text(publication)
        assert "4,146-fact validated import closure" in body
        assert "seven entities and six relations" in body
        assert "Eighteen prerequisite anchors plus a five-event atomic admission batch" in body
        assert REPRODUCER_COMMIT in body
        for stale in (
            "UNSCORABLE_ORACLE_SCHEMA_MISMATCH",
            "Admission produced a 23-event history",
            "24-event history",
            "eight entities and six relations",
        ):
            assert stale not in body


def test_arxiv_citations_and_reproduction_coordinate_are_closed() -> None:
    tex = _text(TEX)
    bibliography = _text(PAPER / "arxiv/references.bib")
    keys = set(re.findall(r"@\w+\{([^,]+),", bibliography))
    citations = {
        key
        for group in re.findall(r"\\citep\{([^}]+)\}", tex)
        for key in group.split(",")
    }

    assert citations == keys
    assert REPRODUCER_COMMIT in _text(README)
    for path in (MANUSCRIPT, TEX, README):
        body = _text(path)
        assert "TODO" not in body
        assert "TBD" not in body
        assert "PLACEHOLDER" not in body
