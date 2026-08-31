"""CC-001 documentation plumbing acceptance tests.

These tests cover presentation infrastructure only. Public compiler examples and
the themed corpus remain gated by CC-D09 and CC-D14.
"""

from __future__ import annotations

import ast
import doctest
import hashlib
import importlib.util
import inspect
import os
from pathlib import Path
import pickle
import subprocess
import sys
from types import ModuleType
from typing import Iterable

from markdown_it.renderer import RendererHTML
from markdown_it.token import Token
from myst_parser.config.main import MdParserConfig, TopmatterReadError, read_topmatter
from myst_parser.parsers.directives import (
    TestDirective as MystDirectiveGrammar,
    parse_directive_text,
)
from myst_parser.parsers.mdit import create_md_parser
import pytest

from scripts.contract_compiler_integration import IntegrationState

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 CI
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
EXTENSION = DOCS / "_ext" / "contract_manifest.py"
SPHINX_EXTENSIONS = {
    "contract_manifest",
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
}
INFRASTRUCTURE_DOCTEST = '>>> {"manifest": "validated"}["manifest"]'
PYTHON_ALIASES = {"py", "pycon", "python", "python3"}
SPHINX_TEST_DIRECTIVES = ("testcode", "testsetup", "testcleanup")
SPHINX_SKIPIF_DIRECTIVES = (
    "doctest",
    *SPHINX_TEST_DIRECTIVES,
    "testoutput",
)
SPHINX_AUTODOC_DIRECTIVES = (
    "autoattribute",
    "autoclass",
    "autodata",
    "autodecorator",
    "autoexception",
    "autofunction",
    "automethod",
    "automodule",
    "autoproperty",
)
PUBLIC_GUIDE_ROOT_IMPORTS = (
    "KnowledgeGraph",
    "LogicContract",
    "OntologyRegistry",
    "PrologVerifier",
    "ProposedOperation",
    "bundled_ontology_path",
    "stage_subgraph",
)
PUBLIC_IMPORT_TARGETS = {"malleus", "malleus.OntologyRegistry"}
PROTOCOL_BOUNDARY_ROLES = (
    "PROTOCOL_INVARIANT",
    "OPTIONAL_PROFILE",
    "REFERENCE_IMPLEMENTATION",
    "CONFORMANCE_FIXTURE",
    "ADOPTER_CHOICE",
)
MYST_CONFIG = MdParserConfig(enable_extensions=set(), fence_as_directive=set())
MYST_PARSER = create_md_parser(MYST_CONFIG, RendererHTML)
MYST_TOPMATTER_CONFIG_KEYS = {"html_meta", "myst", "substitutions"}
STATIC_EXAMPLE_POLICY_LIMITATION = (
    "This is a static policy for repository-controlled documentation, not a Python "
    "sandbox; reflection and deliberately obfuscated calls are outside its boundary."
)
PUBLIC_GUIDES = {
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
}
INTERNAL_CONTRACT_COMPILER_DOC_SOURCES = {
    "contract_compiler/index.md",
    "contract_compiler/manifests.md",
    "contract_compiler/support_profile.md",
}
PUBLIC_DOC_SOURCES = PUBLIC_GUIDES | {
    "index.md",
    "reference/index.md",
}
REPOSITORY_DOC_SOURCES = PUBLIC_DOC_SOURCES | INTERNAL_CONTRACT_COMPILER_DOC_SOURCES
SUPPORT_PROFILE_ROWS = (
    (
        "schema root",
        "`types`, `enums`, `slots`, `classes`, `imports`, `default_range`",
        "`id`, `prefixes`; each prefix key and value; each import reference; the `default_range` reference",
        "`name`, `version`, `title`, `description`",
        "every other field; every annotation",
    ),
    (
        "`types.<type>`",
        "`typeof`",
        "declaration map key; `typeof` reference",
        "`uri`, `description`",
        "every other field; every annotation",
    ),
    (
        "`enums.<enum>`",
        "`permissible_values`",
        "declaration map key",
        "`description`",
        "every other field; every annotation",
    ),
    (
        "`enums.<enum>.permissible_values.<value>`",
        "permissible-value map key",
        "none",
        "`description`",
        "every other field; every annotation",
    ),
    (
        "`slots.<slot>` global declaration",
        "`range`, `required`, `multivalued`, `identifier`, `inlined`, `equals_string`, `minimum_value`, `maximum_value`, `value_presence`",
        "declaration map key; `range` reference; `annotations.adopts` only for the exact imported global-slot redeclaration authorized by `OD-002`",
        "`description`",
        "every other field; every other annotation, including `annotations.retires`",
    ),
    (
        "`classes.<class>`",
        "`is_a`, `mixin`, `mixins`, `abstract`, `slots`, `attributes`, `slot_usage`, `exactly_one_of`",
        "declaration map key; references in `is_a`, `mixins`, and `slots`",
        "`class_uri`, `description`",
        "every other field; every annotation",
    ),
    (
        "`classes.<class>.attributes.<slot>`",
        "`range`, `required`, `multivalued`, `identifier`, `inlined`, `equals_string`, `minimum_value`, `maximum_value`, `value_presence`",
        "local declaration map key; `range` reference",
        "`description`",
        "every other field; every annotation",
    ),
    (
        "`classes.<class>.slot_usage.<slot>`",
        "`range`, `required`, `multivalued`, `identifier`, `inlined`, `equals_string`, `minimum_value`, `maximum_value`, `value_presence`",
        "authoritative slot reference map key; `range` reference",
        "`description`",
        "every other field; every annotation",
    ),
    (
        "`classes.<class>.exactly_one_of`",
        "flat nonempty alternative sequence",
        "none",
        "none",
        "empty sequence; `any_of`, `all_of`, `none_of`; nesting; every other expression field",
    ),
    (
        "one `exactly_one_of` alternative",
        "one nonempty `slot_conditions` map",
        "each `slot_conditions` map key is an authoritative qualified slot reference",
        "none",
        "empty alternative; every other field; every annotation",
    ),
    (
        "one `slot_conditions.<slot>` condition",
        "`required`, `equals_string`, `value_presence`, with at least one present",
        "the authoritative slot reference inherited from its map key",
        "none",
        "every other field; every annotation; nested expression",
    ),
)
EXPRESSION_EXTENSION_ROWS = (
    ("`ExactlyOneGroup`", "`rdf:type`", "exactly `ExactlyOneGroup`", "1"),
    ("`ExactlyOneGroup`", "`cf:onClass`", "`Class`", "1"),
    (
        "`ExactlyOneAlternative`",
        "`rdf:type`",
        "exactly `ExactlyOneAlternative`",
        "1",
    ),
    (
        "`ExactlyOneAlternative`",
        "`cf:inGroup`",
        "`ExactlyOneGroup`",
        "1",
    ),
    ("`SlotCondition`", "`rdf:type`", "exactly `SlotCondition`", "1"),
    (
        "`SlotCondition`",
        "`cf:inAlternative`",
        "`ExactlyOneAlternative`",
        "1",
    ),
    (
        "`SlotCondition`",
        "`cf:usesSlot`",
        "authoritative qualified `Slot`",
        "1",
    ),
    ("`SlotCondition`", "`cf:required`", "Boolean", "0..1"),
    ("`SlotCondition`", "`cf:equalsString`", "string", "0..1"),
    (
        "`SlotCondition`",
        "`cf:valuePresence`",
        "string `PRESENT` or `ABSENT`",
        "0..1",
    ),
)
INTERNAL_METAMODEL_IDENTITY_ROWS = (
    (
        "`ExactNonExpressionSeedContractMetamodel`",
        "4,819",
        "`urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:1c68a612f3e7a0f80c31965aa5525954921dfbee60d151552d10d61cb0aac71b`",
    ),
    (
        "`FlatExactlyOneExpressionExtensionV0`",
        "4,762",
        "`urn:malleus:contract-metamodel:flat-exactly-one-extension:v0:sha256:99527d21040cbdda9dd7c579af7f40af8645de9b5f4b1e8ba28b40ddff7d53e6`",
    ),
    (
        "`ExpressionCapableContractMetamodelV0`",
        "655",
        "`urn:malleus:contract-metamodel:expression-capable:v0:sha256:65aae23b7a0892a4d2ae2b5adc6888f1ddd39c94ce03f412d50a6a5ccd5d0964`",
    ),
)
APPROVED_REFERENCE_PATH = DOCS / "reference" / "index.md"
APPROVED_REFERENCE_SOURCE = (
    "# Current package-root reference\n"
    "\n"
    "This page exercises Sphinx autodoc and autosummary against the existing public\n"
    "package root. It does not promote contract-compiler stages.\n"
    "\n"
    "```{eval-rst}\n"
    ".. autosummary::\n"
    "\n"
    "   malleus.OntologyRegistry\n"
    "\n"
    ".. automodule:: malleus\n"
    "\n"
    ".. autoclass:: malleus.OntologyRegistry\n"
    "```\n"
).encode()


def _load_module(path: Path) -> ModuleType:
    if not path.is_file():
        pytest.fail(f"required documentation module is missing: {path}")
    spec = importlib.util.spec_from_file_location("cc001_docs_module", path)
    if spec is None or spec.loader is None:
        pytest.fail(f"cannot load documentation module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_conf() -> ModuleType:
    return _load_module(DOCS / "conf.py")


def _public_doc_paths(root: Path = DOCS) -> list[Path]:
    paths = [root / relative for relative in sorted(PUBLIC_DOC_SOURCES)]
    missing = [path for path in paths if not path.is_file()]
    assert missing == [], f"required public documentation sources are missing: {missing}"
    return paths


def _repository_doc_paths(root: Path = DOCS) -> list[Path]:
    paths = [root / relative for relative in sorted(REPOSITORY_DOC_SOURCES)]
    missing = [path for path in paths if not path.is_file()]
    assert missing == [], f"required repository documentation sources are missing: {missing}"
    return paths


def _table_after(source: str, heading: str) -> tuple[tuple[str, ...], ...]:
    tail = source.split(heading, 1)[1]
    lines = tail.splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith("|"))
    rows: list[tuple[str, ...]] = []
    for line in lines[start + 2 :]:
        if not line.startswith("|"):
            break
        rows.append(tuple(cell.strip() for cell in line.strip("|").split("|")))
    return tuple(rows)


def _table_named(source: str, header: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
    lines = source.splitlines()
    matches: list[tuple[tuple[str, ...], ...]] = []
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = tuple(cell.strip() for cell in line.strip("|").split("|"))
        if cells != header:
            continue
        rows: list[tuple[str, ...]] = []
        for row in lines[index + 2 :]:
            if not row.startswith("|"):
                break
            rows.append(tuple(cell.strip() for cell in row.strip("|").split("|")))
        matches.append(tuple(rows))
    assert len(matches) == 1
    return matches[0]


def _assert_support_profile_guide(source: str) -> None:
    assert _table_after(source, "## Four exact classifications") == SUPPORT_PROFILE_ROWS
    assert _table_after(source, "## Exactly-one expression boundary") == (
        EXPRESSION_EXTENSION_ROWS
    )
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    for header in (
        ("Exact source member", "Required raw value"),
        ("Lexeme class", "Exact examples", "Result"),
        ("LinkML source name", "Neutral target", "Additional facts when referenced"),
        ("Effective location", "Omitted field", "Materialized result"),
        ("Governed source vector", "D08 outcome", "Exact reason"),
    ):
        assert _table_named(source, header) == _table_named(decisions, header)
    assert _table_named(
        source,
        ("Component", "Canonical byte length", "Internal content identity"),
    ) == INTERNAL_METAMODEL_IDENTITY_ROWS
    for phrase in (
        "Unknown input fails instead of acquiring hidden upstream semantics.",
        "The adapter emits deterministic, frontend-neutral facts.",
        "Another frontend can target the same neutral contract",
        "Parser acceptance is not compiler support.",
        "all explicit YAML tags, including core tags such as `!!str`",
        "Unlisted input is `REJECTED`.",
        "`annotations.adopts` is identity-only there, is rejected everywhere else, and never emits an adoption fact.",
        "A presentation-erasure change touching only those fields preserves facts, candidate fact identities, role-bound identity, and composition identity.",
        "Source indexes never enter identity.",
        "urn:malleus:contract-symbol-policy:linkml-v0-slash-qualified:v0",
        "Unicode general category is `Cc` or `Cs` refuses before format validation.",
        "linkml_runtime-1.11.1-py3-none-any.whl` with SHA-256 `b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da",
        "linkml_runtime/linkml_model/model/schema/types.yaml",
        "1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00",
        "Empty groups or branches, duplicate semantic alternatives, duplicate conditions, unknown or inapplicable slots, incompatible `equalsString` ranges, extra fields, wrong types, contradictions, nested expressions, and `any_of`, `all_of`, or `none_of` refuse atomically.",
        "Each class has at most one directly declared group, reified once on that class.",
        "Its operator makes active rules the exact closed union of both rule sets",
        "Bounds are legal for a direct `cf:Integer` or `cf:Float` range, or a Scalar chain terminating in one of them.",
        "Public namespace placement, public adapter docstrings, stable public fact identifiers, and public documentation remain blocked on `CC-D09` and `OD-009`.",
        "Unknown input remains rejected until all gates pass together.",
        "This decision does not design a plugin framework, discovery registry, lifecycle, or public injection API.",
        "declare its implementation and version plus its exact support, default, and resolver profiles",
        "neutral fact, metamodel, canonicalization, provenance, artifact, runtime, direct-fact, and independent-oracle conformance contract",
    ):
        assert phrase in " ".join(source.split())

    workflow = source.split("## How to expand the profile", 1)[1]
    steps = tuple(
        line.split(". ", 1)[1]
        for line in workflow.splitlines()
        if line[:1].isdigit() and ". " in line
    )
    assert len(steps) == 12
    for required in (
        "named Malleus use case or query",
        "operator decision",
        "exact location",
        "existing D05 seed",
        "defaulted",
        "smallest positive example",
        "independent source, direct-fact, and oracle parity",
        "metamorphic tests",
        "support-profile and metamodel-extension versions",
        "exact support matrix",
        "strict Sphinx HTML, doctest, and linkcheck",
        "independent evidence review",
    ):
        assert any(required in step for step in steps)


def _approved_eval_rst_island(path: Path) -> bool:
    if path != APPROVED_REFERENCE_PATH:
        return False
    if path.read_bytes() != APPROVED_REFERENCE_SOURCE:
        raise AssertionError(
            f"{path.relative_to(ROOT)}: approved eval-rst source bytes changed"
        )
    return True


def _public_source_captures(path: Path) -> list[dict[str, object]]:
    if _approved_eval_rst_island(path):
        return []
    location = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    return _captures_from_myst(
        path.read_text(encoding="utf-8"),
        location=location,
    )


def _public_source_python_blocks(path: Path) -> list[tuple[str, str]]:
    if _approved_eval_rst_island(path):
        return []
    return _python_blocks(path)


def _git_status() -> bytes:
    return subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout


def _inventory(root: Path) -> dict[str, tuple[int, str]]:
    return {
        path.relative_to(root).as_posix(): (
            len(source := path.read_bytes()),
            hashlib.sha256(source).hexdigest(),
        )
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def _build(
    builder: str,
    output: Path,
    *,
    source: Path = DOCS,
) -> subprocess.CompletedProcess[str]:
    try:
        output.resolve().relative_to(ROOT)
    except ValueError:
        pass
    else:
        raise AssertionError("documentation output must be outside the repository")
    before_status = _git_status()
    before_sources = _inventory(source)
    environment = os.environ.copy()
    environment.update(
        PYTHONDONTWRITEBYTECODE="1",
        PYTHONHASHSEED="0",
        SOURCE_DATE_EPOCH="0",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-W",
            "--keep-going",
            "-n",
            "-b",
            builder,
            str(source),
            str(output),
        ],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert _inventory(source) == before_sources
    assert _git_status() == before_status
    return result


def _assert_build(builder: str, output: Path) -> subprocess.CompletedProcess[str]:
    result = _build(builder, output)
    assert result.returncode == 0, result.stdout + result.stderr
    return result


def _isolated_docs(
    root: Path,
    *,
    extensions: Iterable[str],
    index: str,
    filename: str = "index.md",
) -> Path:
    source = root / "source"
    source.mkdir(parents=True)
    quoted = ", ".join(repr(item) for item in sorted({"myst_parser", *extensions}))
    (source / "conf.py").write_text(
        f"extensions = [{quoted}]\nnitpicky = True\n",
        encoding="utf-8",
    )
    (source / filename).write_text(index, encoding="utf-8")
    return source


def _hostile_state() -> IntegrationState:
    return IntegrationState(
        manifest={
            "program_id": "CC-PROGRAM-001",
            "authority": {
                "snapshot": {"state": "SEALED", "result_commit": "0" * 40}
            },
            "unused_absolute_path": str(ROOT),
        },
        workstreams={"CC-000": (), "CC-001": ("CC-000",)},
        cards={
            "CC-001": {
                "responsibility": "Render <script>alert('hostile')</script> safely.",
                "authorization": {"class": "FORMAL"},
                "assignment": {"state": "ASSIGNED", "owner_id": "overseer"},
                "candidate": {"state": "NONE"},
                "scopes": [{"kind": "FILE", "path": "docs/index.md"}],
            }
        },
        selections=("CC-000",),
    )


def _rendered_xml(module: ModuleType, state: IntegrationState) -> str:
    render = getattr(module, "render_integration", None)
    assert callable(render), "contract_manifest must expose render_integration"
    node = render(state)
    assert hasattr(node, "asdom"), "render_integration must return a docutils node"
    return node.asdom().toxml()


def _normalized_examples(
    block: str,
    *,
    location: str,
    doctest_block: bool,
) -> list[tuple[str, str]]:
    if doctest_block or any(
        line.lstrip().startswith(">>>") for line in block.splitlines()
    ):
        return [
            (f"{location} doctest {index}", example.source)
            for index, example in enumerate(
                doctest.DocTestParser().get_examples(block)
            )
        ]
    return [(location, block)]


_SAFE_NON_EXECUTABLE_DIRECTIVES = {
    "admonition",
    "contract-manifest",
    "note",
    "toctree",
}


def _target_block(
    raw_target: str,
    *,
    location: str,
    allow_tilde: bool,
) -> tuple[str, str]:
    raw = raw_target.strip()
    normalized = raw[1:] if raw.startswith("~") and allow_tilde else raw
    qualified = bool(normalized) and all(
        part.isidentifier() for part in normalized.split(".")
    )
    if not raw:
        category = "missing"
    elif raw.startswith("~") and not allow_tilde:
        category = "unsupported"
    elif not qualified:
        category = "unsupported"
    elif normalized not in PUBLIC_IMPORT_TARGETS and normalized.startswith(
        ("linkml", "malleus.", "tests")
    ):
        category = "forbidden"
    elif "." not in normalized and normalized != "malleus":
        category = "unsupported" if normalized[0].isupper() else "unknown"
    elif normalized not in PUBLIC_IMPORT_TARGETS:
        category = "unknown"
    else:
        source = (
            "import malleus\n"
            if normalized == "malleus"
            else "from malleus import OntologyRegistry\n"
        )
        return (f"{location} target {normalized}", source)
    raise AssertionError(
        f"{location}: {category} target {raw!r} normalized {normalized!r}"
    )


def _autosummary_blocks(body: str, *, location: str) -> list[tuple[str, str]]:
    return [
        _target_block(line, location=location, allow_tilde=True)
        for line in body.splitlines()
        if line.strip()
    ]


def _directive_blocks(
    directive: str,
    argument: str,
    body: str,
    *,
    location: str,
    options: dict[str, object],
) -> list[tuple[str, str]]:
    name = directive.casefold()
    language = argument.strip().casefold()
    if name in SPHINX_SKIPIF_DIRECTIVES and "skipif" in options:
        expression = options["skipif"]
        if not isinstance(expression, str):
            raise AssertionError(f"{location}: invalid skipif expression type")
        try:
            tree = ast.parse(expression, filename=location, mode="eval")
        except SyntaxError as error:
            raise AssertionError(
                f"{location}: invalid skipif expression: {error.msg}"
            ) from error
        forbidden = _forbidden_example_operations(tree)
        if forbidden:
            raise AssertionError(f"{location}: {forbidden}")
    if name in SPHINX_AUTODOC_DIRECTIVES:
        target = _target_block(argument, location=location, allow_tilde=False)
        if options:
            raise AssertionError(
                f"{location}: unsupported autodoc options {sorted(options)!r}"
            )
        return [target]
    if name == "autosummary":
        return _autosummary_blocks(body, location=location)
    if name == "doctest":
        return _normalized_examples(body, location=location, doctest_block=True)
    if name in SPHINX_TEST_DIRECTIVES:
        return _normalized_examples(body, location=location, doctest_block=False)
    if name == "testoutput":
        return []
    if name == "code" and (not language or language in PYTHON_ALIASES):
        raise AssertionError(f"{location}: unsupported executable directive {name!r}")
    if name == "code-block" and language in PYTHON_ALIASES:
        return _normalized_examples(body, location=location, doctest_block=False)
    if name in _SAFE_NON_EXECUTABLE_DIRECTIVES:
        return []
    raise AssertionError(f"{location}: unsupported directive {name!r}")


def _myst_info(info: str) -> tuple[str | None, str]:
    parts = info.strip().split(maxsplit=1)
    name = parts[0] if parts else ""
    argument = parts[1] if len(parts) > 1 else ""
    if name.startswith("{") and name.endswith("}") and len(name) > 2:
        return name[1:-1].casefold(), argument
    return None, name


def _myst_capture(
    directive: str,
    argument: str,
    body: str,
    *,
    location: str,
) -> dict[str, object]:
    parsed = parse_directive_text(
        MystDirectiveGrammar,
        argument,
        body,
    )
    if parsed.warnings:
        raise AssertionError(
            f"{location}: MyST directive parse warnings: {parsed.warnings!r}"
        )
    return {
        "directive": directive.casefold(),
        "argument": parsed.arguments[0] if parsed.arguments else "",
        "options": dict(parsed.options),
        "content": "\n".join(parsed.body) + ("\n" if parsed.body else ""),
    }


def _fence_blocks(
    info: str,
    body: str,
    *,
    location: str,
) -> list[tuple[str, str]]:
    directive, argument = _myst_info(info)
    if directive is None:
        language = argument.casefold()
        if language in PYTHON_ALIASES:
            return _normalized_examples(body, location=location, doctest_block=False)
        if language == "doctest":
            return _normalized_examples(body, location=location, doctest_block=True)
        return []
    if directive == "eval-rst":
        raise AssertionError(f"{location}: unsupported MyST directive 'eval-rst'")
    capture = _myst_capture(
        directive,
        argument,
        body,
        location=location,
    )
    if directive in _SAFE_NON_EXECUTABLE_DIRECTIVES:
        blocks = _directive_blocks(
            directive,
            capture["argument"],
            capture["content"],
            location=location,
            options=capture["options"],
        )
        if directive in {"admonition", "note"}:
            blocks.extend(
                _myst_python_blocks_from(
                    capture["content"],
                    location=location,
                )
            )
        return blocks
    if directive in {"code-cell", "jupyter-execute"}:
        raise AssertionError(f"{location}: unsupported executable fence {info!r}")
    return _directive_blocks(
        directive,
        capture["argument"],
        capture["content"],
        location=location,
        options=capture["options"],
    )


def _myst_tokens(source: str, *, location: str) -> list[Token]:
    try:
        topmatter = read_topmatter(source)
    except TopmatterReadError as error:
        raise AssertionError(
            f"{location}: malformed MyST topmatter: {error}"
        ) from error
    if topmatter:
        override = next(
            (key for key in topmatter if key in MYST_TOPMATTER_CONFIG_KEYS),
            None,
        )
        if override is not None:
            raise AssertionError(
                f"{location}: unsupported file-level MyST config {override!r}"
            )
    return MYST_PARSER.parse(source)


def _myst_python_blocks_from(
    source: str,
    *,
    location: str,
) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    for token in _myst_tokens(source, location=location):
        if token.type == "fence":
            blocks.extend(_fence_blocks(token.info, token.content, location=location))
    return blocks


def _captures_from_myst(
    source: str,
    *,
    location: str,
) -> list[dict[str, object]]:
    captures: list[dict[str, object]] = []
    for token in _myst_tokens(source, location=location):
        if token.type != "fence":
            continue
        directive, argument = _myst_info(token.info)
        if directive == "eval-rst":
            raise AssertionError(f"{location}: unsupported MyST directive 'eval-rst'")
        elif directive == "autosummary":
            captures.append(
                _myst_capture(
                    directive,
                    argument,
                    token.content,
                    location="autosummary inventory",
                )
            )
        elif directive in {"admonition", "note"}:
            captures.extend(
                _captures_from_myst(
                    token.content,
                    location=location,
                )
            )
    return captures


def _python_blocks(path: Path) -> list[tuple[str, str]]:
    try:
        location = str(path.relative_to(ROOT))
    except ValueError:
        location = str(path)
    if path.suffix != ".md":
        raise AssertionError(
            f"{location}: unsupported documentation source suffix {path.suffix!r}; "
            "authored docs must be MyST Markdown"
        )
    return _myst_python_blocks_from(
        path.read_text(encoding="utf-8"),
        location=location,
    )


def _import_bindings(tree: ast.AST) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                local = alias.asname or alias.name.split(".", maxsplit=1)[0]
                bindings[local] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                bindings[alias.asname or alias.name] = f"{node.module}.{alias.name}"
    return bindings


def _call_target(expression: ast.expr, bindings: dict[str, str]) -> str | None:
    parts: list[str] = []
    current = expression
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if not isinstance(current, ast.Name):
        return None
    root = bindings.get(current.id, current.id)
    return ".".join((root, *reversed(parts)))


def _forbidden_example_operations(tree: ast.AST) -> list[str]:
    found: list[str] = []
    bindings = _import_bindings(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
            if node.module == "malleus":
                found.extend(
                    f"private Malleus import {alias.name}"
                    for alias in node.names
                    if alias.name not in PUBLIC_GUIDE_ROOT_IMPORTS
                )
        else:
            names = []
        for name in names:
            if name == "pytest" or name.startswith(("linkml", "tests")):
                found.append(f"forbidden import {name}")
            if name.startswith("malleus."):
                found.append(f"private Malleus import {name}")
        if isinstance(node, ast.Call):
            function = node.func
            target = _call_target(function, bindings)
            if target in {"__import__", "builtins.__import__"}:
                found.append("forbidden dynamic import __import__")
            if target in {"import_module", "importlib.import_module"}:
                found.append("forbidden dynamic import import_module")
            for name in ("compile", "eval", "exec"):
                if target in {name, f"builtins.{name}"}:
                    found.append(f"forbidden dynamic execution {name}")
            if isinstance(function, ast.Name) and function.id == "open":
                found.append("fixture-file read through open")
            if isinstance(function, ast.Attribute) and function.attr in {
                "open",
                "read_bytes",
                "read_text",
            }:
                found.append(f"fixture-file read through {function.attr}")
    return found


def _refusal_from(source: str, *, location: str) -> str:
    try:
        blocks = _myst_python_blocks_from(source, location=location)
        for block_location, block in blocks:
            forbidden = _forbidden_example_operations(
                ast.parse(block, filename=block_location)
            )
            if forbidden:
                raise AssertionError(f"{block_location}: {forbidden}")
    except AssertionError as error:
        return str(error)
    pytest.fail(f"{location}: scanner accepted forbidden source")


def test_sphinx_configuration_is_strict_and_has_required_extensions() -> None:
    conf = _load_conf()

    assert set(conf.extensions) == SPHINX_EXTENSIONS
    assert conf.source_suffix == {".md": "markdown"}
    assert conf.myst_enable_extensions == []
    assert conf.myst_fence_as_directive == []
    assert conf.myst_substitutions == {}
    assert conf.myst_html_meta == {}
    assert conf.rst_prolog == ""
    assert conf.rst_epilog == ""
    assert conf.root_doc == "index"
    assert conf.autosummary_generate is False
    assert conf.autosummary_mock_imports == []
    assert conf.doctest_global_setup == ""
    assert conf.doctest_global_cleanup == ""
    assert conf.doctest_path == []
    assert conf.doctest_test_doctest_blocks == ""
    assert conf.nitpicky is True
    assert conf.suppress_warnings == []
    assert conf.nitpick_ignore == []
    assert conf.nitpick_ignore_regex == []
    assert conf.autodoc_mock_imports == []
    assert conf.autodoc_default_options == {}
    assert conf.linkcheck_ignore == []
    assert conf.linkcheck_exclude_documents == []
    assert conf.linkcheck_allowed_redirects == {}
    assert conf.linkcheck_anchors_ignore_for_url == []
    assert conf.linkcheck_request_headers == {}
    assert conf.linkcheck_anchors is True
    assert conf.linkcheck_allow_unauthorized is False
    assert conf.exclude_patterns == []
    conf_tree = ast.parse((DOCS / "conf.py").read_text(encoding="utf-8"))
    assert _forbidden_example_operations(conf_tree) == []
    assert set(conf.include_patterns) == REPOSITORY_DOC_SOURCES
    assert "COST_AWARE_MODEL_ARCHITECTURE_RECON.md" not in conf.include_patterns


def test_contract_compiler_support_profile_is_rendered_and_exact() -> None:
    index = (DOCS / "contract_compiler" / "index.md").read_text(encoding="utf-8")
    toctree = index.split("```{toctree}", 1)[1].split("```", 1)[0]
    assert tuple(line for line in toctree.splitlines() if line) == (
        ":maxdepth: 1",
        "manifests",
        "support_profile",
    )

    guide = (DOCS / "contract_compiler" / "support_profile.md").read_text(
        encoding="utf-8"
    )
    _assert_support_profile_guide(guide)
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    assert _table_after(decisions, "#### Exact location classification") == (
        SUPPORT_PROFILE_ROWS
    )
    assert _table_after(decisions, "#### Versioned exactly-one expression extension") == (
        EXPRESSION_EXTENSION_ROWS
    )
    assert "contract_compiler/support_profile.md" in INTERNAL_CONTRACT_COMPILER_DOC_SOURCES
    assert "contract_compiler/support_profile.md" not in PUBLIC_DOC_SOURCES
    assert "contract_compiler/index.md" not in PUBLIC_DOC_SOURCES
    assert "contract_compiler/manifests.md" not in PUBLIC_DOC_SOURCES
    assert set(_public_doc_paths()).isdisjoint(
        {DOCS / path for path in INTERNAL_CONTRACT_COMPILER_DOC_SOURCES}
    )


def test_contract_compiler_support_profile_refuses_semantic_drift() -> None:
    guide = (DOCS / "contract_compiler" / "support_profile.md").read_text(
        encoding="utf-8"
    )
    class_row = next(
        line
        for line in guide.splitlines()
        if line.startswith("| `classes.<class>` |")
    )
    condition_row = next(
        line
        for line in guide.splitlines()
        if line.startswith("| `SlotCondition` | `cf:valuePresence`")
    )
    mutations = (
        guide.replace(
            class_row,
            class_row.replace(
                "| `class_uri`, `description` |",
                "`class_uri`; | `description` |",
            ),
            1,
        ),
        guide.replace(
            "including `annotations.retires`",
            "excluding `annotations.retires`",
            1,
        ),
        guide.replace(
            "rejected everywhere else, and never emits an adoption fact.",
            "`annotations.adopts` emits an adoption fact.",
            1,
        ),
        guide.replace(
            class_row,
            class_row.replace("`exactly_one_of`", "`exactly_one_of`, `rules`"),
            1,
        ),
        guide.replace(condition_row, "", 1),
        guide.replace(
            condition_row,
            condition_row
            + "\n| `SlotCondition` | `cf:experimental` | string | 0..1 |",
            1,
        ),
        guide.replace("Source indexes never enter identity.", "", 1),
        guide.replace(
            "contradictions, nested expressions, and `any_of`,\n`all_of`, or `none_of` refuse atomically.",
            "nested expressions are accepted.",
            1,
        ),
        guide.replace(
            "| `minimum_value` and `maximum_value` | one finite JSON-number lexical scalar under the grammar below; retain the exact source lexeme |",
            "| `minimum_value` and `maximum_value` | any YAML number |",
            1,
        ),
        guide.replace(
            "| `date` | `https://w3id.org/linkml/types/date` | `rdf:type cf:Scalar`; `cf:typeof cf:String` |",
            "| `date` | `cf:String` | none |",
            1,
        ),
        guide.replace(
            "| supported `Slot` or `SlotUse` with non-Class range | `inlined` | `cf:inlined=false` |",
            "| supported `Slot` or `SlotUse` with non-Class range | `inlined` | `cf:inlined=true` |",
            1,
        ),
        guide.replace(
            "| `CC-X01/explicit_false` | REFUSE |",
            "| `CC-X01/explicit_false` | ACCEPT |",
            1,
        ),
        guide.replace(
            "65aae23b7a0892a4d2ae2b5adc6888f1ddd39c94ce03f412d50a6a5ccd5d0964",
            "07e6513939875ebff0b7495f202d49545e8b836aebe72befdd16a7684b982f59",
            1,
        ),
        guide.replace(
            "does not design a plugin framework, discovery registry, lifecycle,\nor public injection API",
            "defines a plugin registry",
            1,
        ),
        guide.replace(
            "provenance, artifact, runtime,\ndirect-fact",
            "provenance, direct-fact",
            1,
        ),
    )
    assert all(mutation != guide for mutation in mutations)
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _assert_support_profile_guide(mutation)


def test_dev_dependencies_pin_the_verified_docs_toolchain() -> None:
    manifest = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = set(manifest["project"]["optional-dependencies"]["dev"])

    assert "sphinx==8.1.3" in dependencies
    assert "myst-parser==4.0.1" in dependencies
    assert "docutils==0.21.2" in dependencies
    assert "markdown-it-py==3.0.0" in dependencies


def test_removed_rst_scanner_mechanism_stays_dead() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    forbidden_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            forbidden_imports.extend(
                alias.name for alias in node.names if alias.name.startswith("docutils")
            )
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith("docutils"):
                forbidden_imports.append(module)

    forbidden_names = {
        "Parser",
        "get_default_settings",
        "new_document",
        "publish_doctree",
        "roles",
        "states",
    }
    used_forbidden_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id in forbidden_names
    }
    forbidden_attributes = {"_directives", "_roles", "cache"}
    used_forbidden_attributes = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and node.attr in forbidden_attributes
    }
    rst_helpers = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("_rst")
    }

    assert forbidden_imports == []
    assert used_forbidden_names == set()
    assert used_forbidden_attributes == set()
    assert rst_helpers == set()


@pytest.mark.parametrize("workflow", ["tests.yml", "release.yml"])
def test_ci_and_release_run_one_exact_docs_gate(workflow: str) -> None:
    source = (ROOT / ".github" / "workflows" / workflow).read_text(encoding="utf-8")
    step = source.split("- name: Build strict documentation", 1)[1].split(
        "\n      - name:", 1
    )[0]

    assert "if: matrix.python-version == '3.12'" in step
    assert "run: python scripts/ci.py docs --require-clean" in step
    assert source.count("python scripts/ci.py docs --require-clean") == 1
    assert "python -m sphinx" not in source


def test_strict_html_build_is_source_pure(tmp_path: Path) -> None:
    _assert_build("html", tmp_path / "html")


def test_autodoc_and_autosummary_render_the_existing_package_root(
    tmp_path: Path,
) -> None:
    assert _approved_eval_rst_island(APPROVED_REFERENCE_PATH)

    output = tmp_path / "html"
    _assert_build("html", output)
    environment = pickle.loads(
        (output / ".doctrees" / "environment.pickle").read_bytes()
    )
    objects = environment.domaindata["py"]["objects"]
    assert set(objects) == {
        "malleus",
        "malleus.OntologyRegistry",
        "malleus.ontology.OntologyRegistry",
    }
    assert objects["malleus"].objtype == "module"
    assert objects["malleus"].node_id == "module-malleus"
    assert objects["malleus"].aliased is False
    assert objects["malleus.OntologyRegistry"].objtype == "class"
    assert objects["malleus.OntologyRegistry"].node_id == "malleus.OntologyRegistry"
    assert objects["malleus.OntologyRegistry"].aliased is False
    assert objects["malleus.ontology.OntologyRegistry"].aliased is True
    modules = environment.domaindata["py"]["modules"]
    assert set(modules) == {"malleus"}
    assert modules["malleus"].docname == "reference/index"
    assert modules["malleus"].node_id == "module-malleus"

    doctree = pickle.loads(
        (output / ".doctrees" / "reference" / "index.doctree").read_bytes()
    )
    descriptions = [
        node
        for node in doctree.findall()
        if type(node).__name__ == "desc" and node.get("domain") == "py"
    ]
    signatures = [
        node
        for node in doctree.findall()
        if type(node).__name__ == "desc_signature"
    ]
    assert [(node.get("objtype"), node.get("classes")) for node in descriptions] == [
        ("class", ["py", "class"])
    ]
    assert [node.get("ids") for node in signatures] == [
        ["malleus.OntologyRegistry"]
    ]

    rendered = (output / "reference" / "index.html").read_text(encoding="utf-8")
    assert 'id="module-malleus"' in rendered
    assert '<table class="autosummary longtable docutils align-default">' in rendered
    assert 'href="#malleus.OntologyRegistry"' in rendered
    assert 'class="py class"' in rendered
    assert 'class="sig sig-object py" id="malleus.OntologyRegistry"' in rendered
    assert ':py:obj:' not in rendered
    assert ".. py:" not in rendered
    assert (output / "py-modindex.html").is_file()


def test_native_myst_autodoc_fences_render_literal_rst_not_domain_objects(
    tmp_path: Path,
) -> None:
    index = (
        "# Broken native reference\n\n"
        "```{autosummary}\nmalleus.OntologyRegistry\n```\n\n"
        "```{automodule} malleus\n```\n\n"
        "```{autoclass} malleus.OntologyRegistry\n```\n"
    )
    source = _isolated_docs(
        tmp_path,
        extensions=("myst_parser", "sphinx.ext.autodoc", "sphinx.ext.autosummary"),
        index=index,
    )
    output = tmp_path / "html"
    result = _build("html", output, source=source)
    assert result.returncode == 0, result.stdout + result.stderr
    rendered = (output / "index.html").read_text(encoding="utf-8")
    assert ":py:obj:" in rendered
    assert ".. py:module::" in rendered
    assert ".. py:class::" in rendered
    environment = pickle.loads(
        (output / ".doctrees" / "environment.pickle").read_bytes()
    )
    assert environment.domaindata["py"]["objects"] == {}
    assert environment.domaindata["py"]["modules"] == {}
    assert 'class="py class"' not in rendered
    assert 'id="module-malleus"' not in rendered
    assert 'id="malleus.OntologyRegistry"' not in rendered
    assert not (output / "py-modindex.html").exists()


def test_doctest_builder_executes_an_infrastructure_only_example(
    tmp_path: Path,
) -> None:
    index = (DOCS / "index.md").read_text(encoding="utf-8")
    assert INFRASTRUCTURE_DOCTEST in index

    _assert_build("doctest", tmp_path / "doctest")
    report = (tmp_path / "doctest" / "output.txt").read_text(encoding="utf-8")
    assert "1 passed" in report


@pytest.mark.parametrize(
    ("builder", "extensions", "index", "expected"),
    [
        (
            "doctest",
            ("sphinx.ext.doctest",),
            "# Broken doctest\n\n```{doctest}\n>>> 1 + 1\n3\n```\n",
            "1 failures",
        ),
        (
            "linkcheck",
            (),
            "# Broken link\n\nSee [missing](missing.md).\n",
            "missing",
        ),
        (
            "html",
            ("sphinx.ext.autodoc",),
            "# Broken API\n\n```{autofunction} no_such_package.symbol\n```\n",
            "no_such_package",
        ),
    ],
)
def test_broken_docs_are_mechanically_refused(
    tmp_path: Path,
    builder: str,
    extensions: tuple[str, ...],
    index: str,
    expected: str,
) -> None:
    source = _isolated_docs(tmp_path, extensions=extensions, index=index)
    result = _build(builder, tmp_path / "output", source=source)

    assert result.returncode != 0
    assert expected in result.stdout + result.stderr


def test_linkcheck_policy_has_no_silent_exclusion() -> None:
    conf = _load_conf()
    assert conf.linkcheck_ignore == []
    assert conf.linkcheck_exclude_documents == []
    assert conf.linkcheck_allowed_redirects == {}
    assert conf.linkcheck_anchors_ignore_for_url == []
    assert conf.linkcheck_request_headers == {}
    assert conf.linkcheck_anchors is True
    assert conf.linkcheck_allow_unauthorized is False


def test_manifest_projection_uses_only_the_fixed_sealed_validator_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_module(EXTENSION)
    state = _hostile_state()
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

    def validate(*args: object, **kwargs: object) -> IntegrationState:
        calls.append((args, kwargs))
        return state

    monkeypatch.setattr(module, "validate_integration", validate)
    signature = inspect.signature(module.manifest_projection)
    assert tuple(signature.parameters) == ("repository",)
    assert _rendered_xml(module, state) == module.manifest_projection(ROOT).asdom().toxml()
    assert calls == [((ROOT,), {"require_sealed": True})]

    def refuse(*args: object, **kwargs: object) -> IntegrationState:
        raise RuntimeError("validator refusal propagated")

    monkeypatch.setattr(module, "validate_integration", refuse)
    with pytest.raises(RuntimeError, match="validator refusal propagated"):
        module.manifest_projection(ROOT)


def test_manifest_renderer_is_deterministic_escaped_and_non_authoritative() -> None:
    module = _load_module(EXTENSION)
    state = _hostile_state()
    first = _rendered_xml(module, state)

    assert first == _rendered_xml(module, state)
    assert "Non-authoritative projection" in first
    assert "CC-PROGRAM-001" in first
    assert "CC-001" in first
    assert "<script>" not in first
    assert "&lt;script&gt;" in first
    assert str(ROOT) not in first


def test_manifest_directive_has_no_user_selected_input_or_raw_fallback() -> None:
    module = _load_module(EXTENSION)
    directive = module.ContractManifestDirective
    assert directive.required_arguments == 0
    assert directive.optional_arguments == 0
    assert directive.final_argument_whitespace is False
    assert directive.option_spec == {}
    assert callable(getattr(module, "setup", None))

    tree = ast.parse(EXTENSION.read_text(encoding="utf-8"))
    forbidden_calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            forbidden_calls.append("open")
        if isinstance(node.func, ast.Attribute) and node.func.attr in {
            "load",
            "loads",
            "read_bytes",
            "read_text",
        }:
            forbidden_calls.append(node.func.attr)
    assert forbidden_calls == [], f"raw governance fallback calls: {forbidden_calls}"


def test_repository_python_examples_are_ast_checked() -> None:
    assert list(DOCS.rglob("*.rst")) == []
    public_paths = _repository_doc_paths()
    autosummaries = [
        (path, capture)
        for path in public_paths
        for capture in _public_source_captures(path)
        if capture["directive"] == "autosummary"
    ]
    for path, capture in autosummaries:
        assert "toctree" not in capture["options"], path
    blocks = [
        block
        for path in public_paths
        for block in _public_source_python_blocks(path)
    ]
    assert blocks, "documentation has no executable Python or doctest blocks"
    for location, source in blocks:
        tree = ast.parse(source, filename=location)
        forbidden = _forbidden_example_operations(tree)
        assert forbidden == [], f"{location}: {forbidden}"


@pytest.mark.parametrize(
    "mutation",
    [
        lambda source: source.replace(b"package root", b"package-root", 1),
        lambda source: source.replace(b"OntologyRegistry", b"KnowledgeGraph", 1),
        lambda source: source.replace(
            b".. automodule:: malleus\n",
            b".. automodule:: malleus\n   :members:\n",
        ),
        lambda source: source.replace(
            b"```{eval-rst}", b"````{note}\n```{eval-rst}"
        ).replace(b"```\n", b"```\n````\n", 1),
        lambda source: source + b"\n```{eval-rst}\n.. automodule:: malleus\n```\n",
    ],
)
def test_approved_eval_rst_island_refuses_every_byte_change(
    monkeypatch: pytest.MonkeyPatch,
    mutation,
) -> None:
    changed = mutation(APPROVED_REFERENCE_SOURCE)
    original_read_bytes = Path.read_bytes

    def changed_reference(path: Path) -> bytes:
        if path == APPROVED_REFERENCE_PATH:
            return changed
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", changed_reference)
    with pytest.raises(AssertionError, match="approved eval-rst source bytes changed"):
        _public_source_captures(APPROVED_REFERENCE_PATH)


def test_eval_rst_permission_cannot_be_spoofed_by_path_or_location(
    tmp_path: Path,
) -> None:
    copied = tmp_path / "reference" / "index.md"
    copied.parent.mkdir(parents=True)
    copied.write_bytes(APPROVED_REFERENCE_SOURCE)
    with pytest.raises(AssertionError, match="unsupported MyST directive 'eval-rst'"):
        _public_source_captures(copied)
    with pytest.raises(AssertionError, match="unsupported MyST directive 'eval-rst'"):
        _public_source_python_blocks(copied)
    assert _refusal_from(
        APPROVED_REFERENCE_SOURCE.decode(),
        location="docs/reference/index.md",
    ) == "docs/reference/index.md: unsupported MyST directive 'eval-rst'"


def test_repository_scan_excludes_unrendered_markdown_but_rst_stays_refused(
    tmp_path: Path,
) -> None:
    copied_docs = tmp_path / "docs"
    for relative in REPOSITORY_DOC_SOURCES:
        path = copied_docs / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Rendered repository source\n", encoding="utf-8")
    excluded = copied_docs / "COST_AWARE_MODEL_ARCHITECTURE_RECON.md"
    excluded.write_text("```python\nimport linkml\n```\n", encoding="utf-8")
    forbidden_rst = copied_docs / "excluded.rst"
    forbidden_rst.write_text("content\n", encoding="utf-8")

    selected = _repository_doc_paths(copied_docs)
    assert excluded not in selected
    assert forbidden_rst not in selected
    with pytest.raises(AssertionError, match="authored docs must be MyST Markdown"):
        _python_blocks(forbidden_rst)


@pytest.mark.parametrize(
    "source",
    [
        "```python\nimport linkml\n```\n",
        "```{code-block} python\nimport linkml\n```\n",
        "```{doctest}\n>>> import linkml\n```\n",
        "```{doctest} *\n>>> import linkml\n```\n",
        "```pycon\n>>> import linkml\n```\n",
        "```{code-block} pycon\n>>> import linkml\n```\n",
    ],
)
def test_supported_executable_markup_cannot_bypass_ast_guard(source: str) -> None:
    blocks = _myst_python_blocks_from(
        source,
        location="focused-example",
    )
    assert blocks
    for location, block in blocks:
        forbidden = _forbidden_example_operations(ast.parse(block, filename=location))
        assert "forbidden import linkml" in forbidden


@pytest.mark.parametrize("language", ["python", "pycon"])
def test_myst_code_directive_for_python_is_refused(language: str) -> None:
    source = f"```{{code}} {language}\nimport linkml\n```\n"
    refusal = _refusal_from(
        source,
        location=f"myst-code-{language}",
    )
    assert refusal.startswith(f"myst-code-{language}: unsupported executable")


@pytest.mark.parametrize("directive", SPHINX_TEST_DIRECTIVES)
def test_myst_doctest_python_directives_cannot_bypass_ast_guard(
    directive: str,
) -> None:
    source = f"```{{{directive}}} *\nimport linkml\n```\n"
    blocks = _myst_python_blocks_from(
        source,
        location=f"myst-{directive}",
    )
    assert blocks
    for location, block in blocks:
        forbidden = _forbidden_example_operations(ast.parse(block, filename=location))
        assert "forbidden import linkml" in forbidden


@pytest.mark.parametrize("directive", SPHINX_AUTODOC_DIRECTIVES)
def test_myst_autodoc_targets_cannot_bypass_ast_guard(directive: str) -> None:
    source = f"```{{{directive}}} linkml_runtime.forbidden\n```\n"
    location = f"myst-{directive}"
    target = "linkml_runtime.forbidden"
    assert _refusal_from(source, location=location) == (
        f"{location}: forbidden target {target!r} normalized {target!r}"
    )


def test_allowed_autodoc_target_cannot_expand_unapproved_members() -> None:
    source = "```{automodule} malleus\n:members:\n```\n"
    assert _refusal_from(source, location="autodoc-members") == (
        "autodoc-members: unsupported autodoc options ['members']"
    )


def test_real_autodoc_members_expands_unapproved_public_objects(tmp_path: Path) -> None:
    index = "# Expanded module\n\n```{automodule} malleus\n:members:\n```\n"
    source = _isolated_docs(
        tmp_path,
        extensions=("myst_parser", "sphinx.ext.autodoc"),
        index=index,
    )
    result = _build("html", tmp_path / "output", source=source)
    assert result.returncode == 0, result.stdout + result.stderr
    html = (tmp_path / "output" / "index.html").read_text(encoding="utf-8")
    assert "KnowledgeGraph" in html
    assert "LogicContract" in html
    assert "ProposedOperation" in html
    assert _refusal_from(index, location="real-autodoc-members") == (
        "real-autodoc-members: unsupported autodoc options ['members']"
    )


@pytest.mark.parametrize(
    ("source", "target"),
    [
        ("```{autosummary}\nlinkml_runtime.forbidden\n```\n", "linkml_runtime.forbidden"),
        ("```{autosummary}\n:nosignatures:\n\nlinkml_runtime.forbidden\n```\n", "linkml_runtime.forbidden"),
    ],
)
def test_autosummary_targets_cannot_bypass_ast_guard(
    source: str,
    target: str,
) -> None:
    assert _refusal_from(
        source,
        location="autosummary-target",
    ) == (
        f"autosummary-target: forbidden target {target!r} normalized {target!r}"
    )


@pytest.mark.parametrize(
    "source",
    ["```{automodule} malleus\n```\n\n```{autosummary}\n"
     "malleus.OntologyRegistry\n```\n"],
)
def test_public_root_autodoc_and_autosummary_targets_remain_allowed(source: str) -> None:
    blocks = _myst_python_blocks_from(
        source,
        location="public-root-target",
    )
    assert len(blocks) == 2
    for location, block in blocks:
        forbidden = _forbidden_example_operations(ast.parse(block, filename=location))
        assert forbidden == []


@pytest.mark.parametrize(
    "source",
    [
        "```{eval-rst}\ncontent\n```\n",
        "````{note}\n```{eval-rst}\ncontent\n```\n````\n",
        "> ```{eval-rst}\n> content\n> ```\n",
        "- item\n\n  ```{eval-rst}\n  content\n  ```\n",
        "~~~{eval-rst}\ncontent\n~~~\n",
        "```{EVAL-RST}\ncontent\n```\n",
    ],
)
def test_eval_rst_is_refused_at_every_nesting_depth(source: str) -> None:
    refusal = _refusal_from(source, location="eval-rst-refusal")
    assert refusal == "eval-rst-refusal: unsupported MyST directive 'eval-rst'"


@pytest.mark.parametrize("inner", ["testcode", "automodule"])
def test_nested_myst_container_import_forms_are_checked(inner: str) -> None:
    location = f"nested-myst-{inner}"
    if inner == "testcode":
        myst_inner = "```{testcode}\nimport linkml\n```\n"
        expected_target = None
    else:
        myst_inner = "```{automodule} linkml\n```\n"
        expected_target = (
            f"{location}: forbidden target 'linkml' normalized 'linkml'"
        )
    source = f"````{{note}}\n{myst_inner}````\n"

    refusal = _refusal_from(source, location=location)
    if expected_target is None:
        assert location in refusal
        assert "forbidden import linkml" in refusal
    else:
        assert refusal == expected_target


@pytest.mark.parametrize("option", ["platform: any", "synopsis: x"])
def test_valid_myst_autodoc_options_cannot_hide_import_targets(option: str) -> None:
    source = f"```{{automodule}} linkml\n:{option}\n```\n"
    assert _refusal_from(
        source,
        location="valid-myst-option",
    ) == (
        "valid-myst-option: forbidden target 'linkml' normalized 'linkml'"
    )


def test_authored_rst_source_is_refused_with_actionable_path(tmp_path: Path) -> None:
    source = tmp_path / "forbidden.rst"
    source.write_text("content\n", encoding="utf-8")
    with pytest.raises(AssertionError, match="forbidden.rst"):
        _python_blocks(source)


@pytest.mark.parametrize(
    "source",
    [
        "```Python\nimport linkml\n```\n",
        "```{CODE-BLOCK} Python\nimport linkml\n```\n",
        "```{testcode}\n:hide:\n\nimport linkml\n```\n",
        "```{testcode}\n:skipif: False\n\nimport linkml\n```\n",
    ],
)
def test_parser_native_case_and_options_are_checked(source: str) -> None:
    refusal = _refusal_from(
        source,
        location="parser-native-myst",
    )
    assert "parser-native-myst" in refusal
    assert "forbidden import linkml" in refusal


@pytest.mark.parametrize("language", ["Python", "PyCon"])
def test_case_varied_myst_code_directive_is_refused(language: str) -> None:
    refusal = _refusal_from(
        f"```{{code}} {language}\nimport linkml\n```\n",
        location="case-varied-code",
    )
    assert refusal.startswith("case-varied-code: unsupported executable")


def test_unknown_directive_is_captured_then_refused() -> None:
    refusal = _refusal_from(
        "```{run-python} payload\nimport linkml\n```\n",
        location="unknown-directive",
    )
    assert refusal == "unknown-directive: unsupported directive 'run-python'"


@pytest.mark.parametrize(
    ("key", "configuration"),
    [
        ("myst", "myst:\n  enable_extensions:\n    - colon_fence\n"),
        ("substitutions", "substitutions:\n  project: malleus\n"),
        ("html_meta", "html_meta:\n  description: malleus\n"),
    ],
)
def test_file_level_myst_parser_override_is_refused_before_scanning(
    key: str,
    configuration: str,
) -> None:
    source = f"---\n{configuration}---\n# File-local parser override\n"
    assert _refusal_from(
        source,
        location="myst-topmatter",
    ) == f"myst-topmatter: unsupported file-level MyST config {key!r}"


def test_real_myst_builder_executes_topmatter_enabled_directive(
    tmp_path: Path,
) -> None:
    source_text = (
        "---\n"
        "myst:\n"
        "  enable_extensions:\n"
        "    - colon_fence\n"
        "---\n"
        "# File-local executable bypass\n\n"
        ":::{testcode}\n"
        "import linkml\n"
        "assert linkml\n"
        ":::\n"
    )
    source = _isolated_docs(
        tmp_path,
        extensions=("myst_parser", "sphinx.ext.doctest"),
        index=source_text,
        filename="index.md",
    )
    result = _build("doctest", tmp_path / "output", source=source)
    assert result.returncode == 0, result.stdout + result.stderr
    report = (tmp_path / "output" / "output.txt").read_text(encoding="utf-8")
    assert "1 passed" in report
    assert _refusal_from(
        source_text,
        location="real-myst-topmatter",
    ) == "real-myst-topmatter: unsupported file-level MyST config 'myst'"


@pytest.mark.parametrize(
    ("container", "directive", "source", "filename", "extensions"),
    [
        (
            "blockquote",
            "testcode",
            "> ```{testcode}\n> import linkml\n> ```\n",
            "index.md",
            ("myst_parser", "sphinx.ext.doctest"),
        ),
        (
            "blockquote",
            "automodule",
            "> ```{automodule} linkml\n> ```\n",
            "index.md",
            (),
        ),
        (
            "list-item",
            "testcode",
            "- item\n\n  ```{testcode}\n  import linkml\n  ```\n",
            "index.md",
            ("myst_parser", "sphinx.ext.doctest"),
        ),
        (
            "list-item",
            "automodule",
            "- item\n\n  ```{automodule} linkml\n  ```\n",
            "index.md",
            (),
        ),
        (
            "tilde-fence",
            "testcode",
            "~~~{testcode}\nimport linkml\n~~~\n",
            "index.md",
            ("myst_parser", "sphinx.ext.doctest"),
        ),
        (
            "tilde-fence",
            "automodule",
            "~~~{automodule} linkml\n~~~\n",
            "index.md",
            (),
        ),
    ],
)
def test_commonmark_container_import_forms_are_checked(
    tmp_path: Path,
    container: str,
    directive: str,
    source: str,
    filename: str,
    extensions: tuple[str, ...],
) -> None:
    location = f"container-{container}-{directive}"
    if directive == "testcode":
        docs = _isolated_docs(
            tmp_path,
            extensions=extensions,
            index=source,
            filename=filename,
        )
        result = _build("doctest", tmp_path / "output", source=docs)
        assert result.returncode == 0, result.stdout + result.stderr
        expected_target = None
    else:
        expected_target = (
            f"{location}: forbidden target 'linkml' normalized 'linkml'"
        )

    refusal = _refusal_from(source, location=location)
    if expected_target is None:
        assert location in refusal
        assert "forbidden import linkml" in refusal
    else:
        assert refusal == expected_target


@pytest.mark.parametrize(
    ("source", "category", "target", "normalized"),
    [
        ("```{automodule}\n```\n", "missing", "", ""),
        ("```{automodule} pathlib\n```\n", "unknown", "pathlib", "pathlib"),
        (
            "```{autoclass} ~malleus.OntologyRegistry\n```\n",
            "unsupported",
            "~malleus.OntologyRegistry",
            "~malleus.OntologyRegistry",
        ),
        (
            "```{autoclass} malleus.Registry\n```\n",
            "forbidden",
            "malleus.Registry",
            "malleus.Registry",
        ),
        ("```{automodule} tests\n```\n", "forbidden", "tests", "tests"),
        (
            "```{autosummary}\nOntologyRegistry\n```\n",
            "unsupported",
            "OntologyRegistry",
            "OntologyRegistry",
        ),
        (
            "```{autosummary}\nmalleus.OntologyRegistry extra\n```\n",
            "unsupported",
            "malleus.OntologyRegistry extra",
            "malleus.OntologyRegistry extra",
        ),
    ],
)
def test_autodoc_and_autosummary_refuse_targets_outside_exact_allowlist(
    source: str,
    category: str,
    target: str,
    normalized: str,
) -> None:
    assert _refusal_from(
        source,
        location="exact-target-guard",
    ) == (
        f"exact-target-guard: {category} target {target!r} "
        f"normalized {normalized!r}"
    )


def test_autosummary_normalizes_only_a_leading_tilde() -> None:
    allowed = _myst_python_blocks_from(
        "```{autosummary}\n~malleus.OntologyRegistry\n```\n",
        location="tilde-allowed",
    )
    assert len(allowed) == 1
    assert _forbidden_example_operations(ast.parse(allowed[0][1])) == []

    assert _refusal_from(
        "```{autosummary}\n~linkml.SchemaView\n```\n",
        location="tilde-forbidden",
    ) == (
        "tilde-forbidden: forbidden target '~linkml.SchemaView' "
        "normalized 'linkml.SchemaView'"
    )


def test_from_malleus_import_allows_only_the_current_guide_root_objects() -> None:
    allowed_names = ", ".join(PUBLIC_GUIDE_ROOT_IMPORTS)
    allowed = ast.parse(f"from malleus import {allowed_names}")
    assert _forbidden_example_operations(allowed) == []

    forbidden = ast.parse("from malleus import ContractCompiler, ontology")
    assert _forbidden_example_operations(forbidden) == [
        "private Malleus import ContractCompiler",
        "private Malleus import ontology",
    ]


@pytest.mark.parametrize(
    ("expression", "operation"),
    [
        ("__import__('linkml')", "forbidden dynamic import __import__"),
        ("builtins.__import__('linkml')", "forbidden dynamic import __import__"),
        (
            "importlib.import_module('linkml')",
            "forbidden dynamic import import_module",
        ),
        ("import_module('linkml')", "forbidden dynamic import import_module"),
        ("exec('import linkml')", "forbidden dynamic execution exec"),
        ("eval(\"__import__('linkml')\")", "forbidden dynamic execution eval"),
        (
            "compile('import linkml', '<docs>', 'exec')",
            "forbidden dynamic execution compile",
        ),
    ],
)
def test_dynamic_import_and_execution_calls_are_ast_refused(
    expression: str,
    operation: str,
) -> None:
    source = f"```{{testcode}}\n{expression}\n```\n"
    refusal = _refusal_from(
        source,
        location="dynamic-execution",
    )
    assert refusal == f"dynamic-execution: ['{operation}']"


@pytest.mark.parametrize("directive", SPHINX_SKIPIF_DIRECTIVES)
def test_myst_skipif_expressions_use_the_bounded_ast_policy(directive: str) -> None:
    source = (
        f"```{{{directive}}}\n"
        ":skipif: __import__('linkml') and False\n\n"
        "pass\n"
        "```\n"
    )
    assert _refusal_from(
        source,
        location=f"myst-skipif-{directive}",
    ) == f"myst-skipif-{directive}: ['forbidden dynamic import __import__']"


def test_myst_yaml_skipif_uses_the_bounded_ast_policy() -> None:
    source = (
        "```{testcode}\n"
        "---\n"
        "skipif: __import__('linkml') and False\n"
        "---\n"
        "pass\n"
        "```\n"
    )
    assert _refusal_from(
        source,
        location="myst-yaml-skipif",
    ) == "myst-yaml-skipif: ['forbidden dynamic import __import__']"


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            "```{testcode}\n---\nhide: true\n---\nimport linkml\n```\n",
            "myst-yaml-import: ['forbidden import linkml']",
        ),
        (
            "```{automodule} linkml\n---\nplatform: any\n---\n```\n",
            "myst-yaml-import: forbidden target 'linkml' normalized 'linkml'",
        ),
    ],
)
def test_myst_yaml_options_cannot_hide_imports(source: str, expected: str) -> None:
    assert _refusal_from(source, location="myst-yaml-import") == expected


def test_invalid_skipif_expression_fails_closed_with_location() -> None:
    source = "```{testcode}\n:skipif: if broken\n\npass\n```\n"
    assert _refusal_from(
        source,
        location="skipif-syntax",
    ).startswith("skipif-syntax: invalid skipif expression")


def test_real_doctest_evaluates_skipif_that_guard_refuses(tmp_path: Path) -> None:
    index = (
        "# Executable option bypass\n\n"
        "```{testcode}\n"
        ":skipif: __import__('linkml') and False\n\n"
        "pass\n"
        "```\n"
    )
    source = _isolated_docs(
        tmp_path,
        extensions=("myst_parser", "sphinx.ext.doctest"),
        index=index,
        filename="index.md",
    )
    result = _build("doctest", tmp_path / "output", source=source)
    assert result.returncode == 0, result.stdout + result.stderr
    report = (tmp_path / "output" / "output.txt").read_text(encoding="utf-8")
    assert "1 passed" in report
    assert _refusal_from(
        index,
        location="real-skipif",
    ) == "real-skipif: ['forbidden dynamic import __import__']"


def test_static_example_policy_states_its_non_sandbox_boundary() -> None:
    assert "repository-controlled" in STATIC_EXAMPLE_POLICY_LIMITATION
    assert "not a Python sandbox" in STATIC_EXAMPLE_POLICY_LIMITATION
    assert "reflection" in STATIC_EXAMPLE_POLICY_LIMITATION


@pytest.mark.parametrize(
    ("body", "operation"),
    [
        (
            "import importlib as loader\nloader.import_module('linkml')",
            "forbidden dynamic import import_module",
        ),
        (
            "from importlib import import_module as load\nload('linkml')",
            "forbidden dynamic import import_module",
        ),
        (
            "import builtins as runtime\nruntime.__import__('linkml')",
            "forbidden dynamic import __import__",
        ),
        (
            "from builtins import exec as run\nrun('import linkml')",
            "forbidden dynamic execution exec",
        ),
    ],
)
def test_ordinary_import_aliases_cannot_hide_dynamic_calls(
    body: str,
    operation: str,
) -> None:
    source = "```{testcode}\n" + body + "\n```\n"
    refusal = _refusal_from(
        source,
        location="dynamic-alias",
    )
    assert refusal == f"dynamic-alias: ['{operation}']"


def test_real_doctest_executes_dynamic_import_that_guard_refuses(
    tmp_path: Path,
) -> None:
    index = (
        "# Dynamic import bypass\n\n"
        "```{testcode}\n"
        "__import__('linkml')\n"
        "```\n"
    )
    source = _isolated_docs(
        tmp_path,
        extensions=("myst_parser", "sphinx.ext.doctest"),
        index=index,
        filename="index.md",
    )
    result = _build("doctest", tmp_path / "output", source=source)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _refusal_from(
        index,
        location="real-dynamic-import",
    ) == "real-dynamic-import: ['forbidden dynamic import __import__']"


@pytest.mark.parametrize(
    ("builder", "extensions", "index", "target"),
    [
        (
            "doctest",
            ("myst_parser", "sphinx.ext.doctest"),
            "# Executable bypass\n\n```{testcode}\nimport linkml\n```\n",
            "linkml",
        ),
        (
            "html",
            ("myst_parser", "sphinx.ext.autodoc"),
            "# Import bypass\n\n```{automodule} linkml\n```\n",
            "linkml",
        ),
    ],
)
def test_real_builders_execute_import_forms_that_the_guard_refuses(
    tmp_path: Path,
    builder: str,
    extensions: tuple[str, ...],
    index: str,
    target: str,
) -> None:
    source = _isolated_docs(
        tmp_path,
        extensions=extensions,
        index=index,
        filename="index.md",
    )
    result = _build(builder, tmp_path / "output", source=source)
    assert result.returncode == 0, result.stdout + result.stderr
    refusal = _refusal_from(
        index,
        location=f"real-{builder}",
    )
    if builder == "html":
        assert refusal == (
            "real-html: forbidden target 'linkml' normalized 'linkml'"
        )
    else:
        assert f"real-{builder}" in refusal
        assert f"forbidden import {target}" in refusal


def test_unrecognized_executable_markup_is_refused() -> None:
    with pytest.raises(AssertionError, match="unsupported executable"):
        _myst_python_blocks_from(
            "```{code-cell} python\nfrom malleus import OntologyRegistry\n```\n",
            location="focused-example",
        )

    root_import = ast.parse("from malleus import OntologyRegistry")
    assert _forbidden_example_operations(root_import) == []


def test_protocol_boundary_taxonomy_is_closed_and_separates_capability_status() -> None:
    principles = (DOCS / "PRINCIPLES.md").read_text(encoding="utf-8")
    normalized = " ".join(principles.split())

    assert "## Protocol boundary taxonomy" in principles
    assert all(role in principles for role in PROTOCOL_BOUNDARY_ROLES)
    assert "Capability status is a separate axis" in normalized
    assert "One document or module may contain several roles" in normalized


def test_public_guides_do_not_present_root_types_as_the_whole_protocol() -> None:
    for path in (ROOT / "README.md", DOCS / "ADOPTION_GUIDE.md"):
        text = path.read_text(encoding="utf-8")
        assert "Everything in malleus is one of five things" not in text


def test_semantic_history_is_an_optional_profile() -> None:
    design = (
        ROOT / "design" / "SEMANTIC_LOG_KNOWLEDGE_PROJECTION.md"
    ).read_text(encoding="utf-8")

    assert "The semantic-history and replay profile is optional." in design


def test_graph_realization_separates_structure_governance_and_fixture_authority() -> None:
    design = (
        ROOT / "design" / "ONTOLOGY_DRIVEN_KG_REALIZATION.md"
    ).read_text(encoding="utf-8")

    assert "StructuralGraphRealization" in design
    assert "GovernedAcceptedRealization" in design
    assert "No fixture has protocol authority." in design
    assert "structurally independent fixture" in design
    assert "`PROTOCOL_INVARIANT`" in design


def test_architecture_does_not_call_a_domain_example_ground_truth() -> None:
    architecture = (DOCS / "ARCHITECTURE.md").read_text(encoding="utf-8")

    assert "## Layer 2: The Ground Truth (Static Data)" not in architecture
