"""Focused guard for the dependency failure found during D1."""

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper.text_layer_reading import (
    PINNED_PYPDF_VERSION,
    TextLayerReadingError,
    _blocks,
    _require_pypdf_version,
)


def test_unpinned_pypdf_version_refuses() -> None:
    with pytest.raises(TextLayerReadingError, match="pypdf version drift"):
        _require_pypdf_version("6.16.1")

    _require_pypdf_version(PINNED_PYPDF_VERSION)


def test_wrapped_sentence_stays_in_one_locator_block() -> None:
    blocks = _blocks("A value wraps\nonto the next line.\nAnother value.\n", 2)

    assert [(block["id"], block["text"]) for block in blocks] == [
        ("page:2:block:001", "A value wraps\nonto the next line.\n"),
        ("page:2:block:002", "Another value.\n"),
    ]
