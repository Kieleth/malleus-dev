"""Strict, repository-only Sphinx configuration for Malleus."""

from __future__ import annotations

from pathlib import Path
import sys


DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(DOCS / "_ext"))

project = "Malleus"
copyright = "2026, Malleus contributors"
extensions = [
    "contract_manifest",
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
]
source_suffix = {".md": "markdown"}
root_doc = "index"
myst_enable_extensions = []
myst_fence_as_directive = []
myst_substitutions = {}
myst_html_meta = {}
rst_prolog = ""
rst_epilog = ""
autosummary_generate = False
autosummary_mock_imports = []
doctest_global_setup = ""
doctest_global_cleanup = ""
doctest_path = []
doctest_test_doctest_blocks = ""
nitpicky = True
suppress_warnings = []
nitpick_ignore = []
nitpick_ignore_regex = []
autodoc_mock_imports = []
autodoc_default_options = {}
autodoc_typehints = "none"
exclude_patterns = []
include_patterns = [
    "index.md",
    "ADOPTION_GUIDE.md",
    "ARCHITECTURE.md",
    "ASSENT_PLAN.md",
    "ASSENT_PROTOCOL.md",
    "DELIMITATIONS.md",
    "EFFECT_PROTOCOL.md",
    "IMPLEMENTATION_STATUS.md",
    "KNOWLEDGE_GRAPH_PROTOCOL.md",
    "ONTOLOGY_PROTOCOL.md",
    "PRINCIPLES.md",
    "RECIPES.md",
    "RECON_CONTRACT.md",
    "contract_compiler/index.md",
    "contract_compiler/manifests.md",
    "contract_compiler/support_profile.md",
    "reference/index.md",
]
linkcheck_ignore = []
linkcheck_exclude_documents = []
linkcheck_allowed_redirects = {}
linkcheck_anchors_ignore_for_url = []
linkcheck_request_headers = {}
linkcheck_anchors = True
linkcheck_allow_unauthorized = False
html_theme = "alabaster"
