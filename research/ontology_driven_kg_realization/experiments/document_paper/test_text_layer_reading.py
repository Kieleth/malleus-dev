"""Focused guard for the dependency failure found during D1."""

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper.text_layer_reading import (
    PINNED_PYPDF_VERSION,
    TextLayerReadingError,
    _require_pypdf_version,
)


def test_unpinned_pypdf_version_refuses() -> None:
    with pytest.raises(TextLayerReadingError, match="pypdf version drift"):
        _require_pypdf_version("6.16.1")

    _require_pypdf_version(PINNED_PYPDF_VERSION)
