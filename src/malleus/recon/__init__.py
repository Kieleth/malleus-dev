"""Evidence-first literature forensics for Malleus."""

import sysconfig
from pathlib import Path

from malleus.recon.analysis import (
    build_outputs,
    compare_subjects,
    current_graph,
    visualize,
)
from malleus.recon.import_v1 import LiteratureV1Importer, import_literature_kg_v1
from malleus.recon.store import (
    BUILD_DIRECTORY,
    LEDGER_FILE,
    PROJECT_FILE,
    ReconError,
    ReconProject,
    RecordCandidate,
    StoredRecord,
)


def bundled_contract_path() -> Path:
    """Return the Recon contract from a checkout or installed package."""

    source = Path(__file__).resolve().parents[3] / "docs" / "RECON_CONTRACT.md"
    if source.is_file():
        return source
    installed = (
        Path(sysconfig.get_path("data"))
        / "share"
        / "malleus"
        / "docs"
        / "RECON_CONTRACT.md"
    )
    if installed.is_file():
        return installed
    raise FileNotFoundError(
        "Bundled Recon contract not found in the source tree or installed data; "
        "reinstall malleus-dev or run from a checkout"
    )


__all__ = [
    "BUILD_DIRECTORY",
    "LEDGER_FILE",
    "LiteratureV1Importer",
    "PROJECT_FILE",
    "ReconError",
    "ReconProject",
    "RecordCandidate",
    "StoredRecord",
    "build_outputs",
    "bundled_contract_path",
    "compare_subjects",
    "current_graph",
    "import_literature_kg_v1",
    "visualize",
]
