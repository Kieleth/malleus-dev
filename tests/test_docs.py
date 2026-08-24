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
import re
import subprocess
import sys
import textwrap
from types import ModuleType
from typing import Iterable

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
DOCS_COMMANDS = (
    "python -m sphinx -W --keep-going -n -b html docs /tmp/malleus-docs/html",
    "python -m sphinx -W --keep-going -n -b doctest docs /tmp/malleus-docs/doctest",
    "python -m sphinx -W --keep-going -n -b linkcheck docs /tmp/malleus-docs/linkcheck",
)
INFRASTRUCTURE_DOCTEST = '>>> {"manifest": "validated"}["manifest"]'
PYTHON_ALIASES = {"py", "python", "python3"}
RST_EXECUTABLE = re.compile(r"^\.\. (code|code-block|doctest|jupyter-execute)::(?:\s+(\S+))?\s*$")


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


def _isolated_docs(root: Path, *, extensions: Iterable[str], index: str) -> Path:
    source = root / "source"
    source.mkdir(parents=True)
    quoted = ", ".join(repr(item) for item in extensions)
    (source / "conf.py").write_text(
        f"extensions = [{quoted}]\nnitpicky = True\n",
        encoding="utf-8",
    )
    (source / "index.rst").write_text(index, encoding="utf-8")
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


def _python_blocks_from(source: str, *, location: str) -> list[tuple[str, str]]:
    lines = source.splitlines()
    blocks: list[tuple[str, str]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("```"):
            label = line[3:].strip()
            end = index + 1
            while end < len(lines) and not lines[end].startswith("```"):
                end += 1
            if end == len(lines):
                raise AssertionError(f"{location}: unclosed fenced block {label!r}")
            body = "\n".join(lines[index + 1 : end]) + "\n"
            words = label.split()
            doctest_block = label in {"doctest", "{doctest}"}
            python_block = bool(words and words[0] in PYTHON_ALIASES)
            if len(words) == 2 and words[0] == "{code-block}":
                python_block = words[1] in PYTHON_ALIASES
            if label.startswith(("{code-cell}", "{jupyter-execute}")):
                raise AssertionError(
                    f"{location}: unsupported executable fence {label!r}"
                )
            if python_block or doctest_block:
                blocks.extend(
                    _normalized_examples(
                        body,
                        location=location,
                        doctest_block=doctest_block,
                    )
                )
            elif label == "{eval-rst}":
                blocks.extend(_python_blocks_from(body, location=location))
            index = end + 1
            continue

        match = RST_EXECUTABLE.match(line)
        if match:
            directive, language = match.groups()
            end = index + 1
            while end < len(lines) and (
                not lines[end].strip() or lines[end].lstrip().startswith(":")
            ):
                end += 1
            body_start = end
            while end < len(lines) and (
                not lines[end].strip() or lines[end].startswith((" ", "\t"))
            ):
                end += 1
            body = textwrap.dedent("\n".join(lines[body_start:end])) + "\n"
            doctest_block = directive == "doctest"
            python_block = directive == "code-block" and language in PYTHON_ALIASES
            if directive in {"code", "jupyter-execute"} and (
                language is None or language in PYTHON_ALIASES
            ):
                raise AssertionError(
                    f"{location}: unsupported executable directive {line!r}"
                )
            if python_block or doctest_block:
                blocks.extend(
                    _normalized_examples(
                        body,
                        location=location,
                        doctest_block=doctest_block,
                    )
                )
            index = end
            continue
        index += 1
    return blocks


def _python_blocks(path: Path) -> list[tuple[str, str]]:
    return _python_blocks_from(
        path.read_text(encoding="utf-8"),
        location=str(path.relative_to(ROOT)),
    )


def _forbidden_example_operations(tree: ast.AST) -> list[str]:
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            names = []
        for name in names:
            if name == "pytest" or name.startswith(("linkml", "tests")):
                found.append(f"forbidden import {name}")
            if name.startswith("malleus."):
                found.append(f"private Malleus import {name}")
        if isinstance(node, ast.Call):
            function = node.func
            if isinstance(function, ast.Name) and function.id == "open":
                found.append("fixture-file read through open")
            if isinstance(function, ast.Attribute) and function.attr in {
                "open",
                "read_bytes",
                "read_text",
            }:
                found.append(f"fixture-file read through {function.attr}")
    return found


def test_sphinx_configuration_is_strict_and_has_required_extensions() -> None:
    conf = _load_conf()

    assert SPHINX_EXTENSIONS <= set(conf.extensions)
    assert conf.source_suffix[".md"] == "markdown"
    assert conf.root_doc == "index"
    assert conf.autosummary_generate is False
    assert conf.nitpicky is True
    assert conf.suppress_warnings == []
    assert conf.nitpick_ignore == []
    assert conf.nitpick_ignore_regex == []
    assert conf.autodoc_mock_imports == []
    assert conf.linkcheck_ignore == []
    assert conf.linkcheck_exclude_documents == []
    assert conf.linkcheck_allowed_redirects == {}
    assert conf.linkcheck_anchors_ignore_for_url == []
    assert conf.linkcheck_request_headers == {}
    assert conf.linkcheck_anchors is True
    assert conf.linkcheck_allow_unauthorized is False
    assert conf.exclude_patterns == []


def test_autosummary_cannot_generate_authored_stubs() -> None:
    for path in sorted((*DOCS.rglob("*.md"), *DOCS.rglob("*.rst"))):
        source = path.read_text(encoding="utf-8")
        autosummary_blocks = re.findall(
            r"(?:```\{autosummary\}|\.\. autosummary::)(.*?)(?:```|\n\S|\Z)",
            source,
            re.DOTALL,
        )
        assert all(":toctree:" not in block for block in autosummary_blocks), path


def test_dev_dependencies_pin_the_verified_docs_toolchain() -> None:
    manifest = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = set(manifest["project"]["optional-dependencies"]["dev"])

    assert "sphinx==8.1.3" in dependencies
    assert "myst-parser==4.0.1" in dependencies


@pytest.mark.parametrize("workflow", ["tests.yml", "release.yml"])
def test_ci_and_release_run_one_exact_docs_gate(workflow: str) -> None:
    source = (ROOT / ".github" / "workflows" / workflow).read_text(encoding="utf-8")
    step = source.split("- name: Build strict documentation", 1)[1].split(
        "\n      - name:", 1
    )[0]

    assert "if: matrix.python-version == '3.12'" in step
    assert 'PYTHONDONTWRITEBYTECODE: "1"' in step
    assert 'PYTHONHASHSEED: "0"' in step
    assert 'SOURCE_DATE_EPOCH: "0"' in step
    assert "git diff --exit-code" in step
    assert 'test -z "$(git status --porcelain=v1)"' in step
    for command in DOCS_COMMANDS:
        assert source.count(command) == 1


def test_strict_html_build_is_source_pure(tmp_path: Path) -> None:
    _assert_build("html", tmp_path / "html")


def test_autodoc_and_autosummary_render_the_existing_package_root(
    tmp_path: Path,
) -> None:
    reference = (DOCS / "reference" / "index.md").read_text(encoding="utf-8")
    assert "automodule:: malleus" in reference
    assert "autosummary::" in reference
    assert "malleus.OntologyRegistry" in reference

    output = tmp_path / "html"
    _assert_build("html", output)
    rendered = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(output.rglob("*.html"))
    )
    assert "OntologyRegistry" in rendered
    assert (
        "Malleus: root ontology + ontology-typed knowledge graph with distributed "
        "convergence."
    ) in rendered


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
            "Broken doctest\n==============\n\n.. doctest::\n\n   >>> 1 + 1\n   3\n",
            "1 failures",
        ),
        (
            "linkcheck",
            (),
            "Broken link\n===========\n\nSee :doc:`missing`.\n",
            "missing",
        ),
        (
            "html",
            ("sphinx.ext.autodoc",),
            "Broken API\n==========\n\n.. autofunction:: no_such_package.symbol\n",
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


def test_public_python_examples_are_ast_checked() -> None:
    blocks = [
        block
        for path in sorted((*DOCS.rglob("*.md"), *DOCS.rglob("*.rst")))
        for block in _python_blocks(path)
    ]
    assert blocks, "documentation has no executable Python or doctest blocks"
    for location, source in blocks:
        tree = ast.parse(source, filename=location)
        forbidden = _forbidden_example_operations(tree)
        assert forbidden == [], f"{location}: {forbidden}"


@pytest.mark.parametrize(
    "source",
    [
        "```python\nimport linkml\n```\n",
        "```{code-block} python\nimport linkml\n```\n",
        "```{doctest}\n>>> import linkml\n```\n",
        ".. code-block:: python\n\n   import linkml\n",
        ".. doctest::\n\n   >>> import linkml\n",
    ],
)
def test_supported_executable_markup_cannot_bypass_ast_guard(source: str) -> None:
    blocks = _python_blocks_from(source, location="focused-example")
    assert blocks
    for location, block in blocks:
        forbidden = _forbidden_example_operations(ast.parse(block, filename=location))
        assert "forbidden import linkml" in forbidden


def test_unrecognized_executable_markup_is_refused() -> None:
    with pytest.raises(AssertionError, match="unsupported executable"):
        _python_blocks_from(
            "```{code-cell} python\nfrom malleus import OntologyRegistry\n```\n",
            location="focused-example",
        )

    root_import = ast.parse("from malleus import OntologyRegistry")
    assert _forbidden_example_operations(root_import) == []
