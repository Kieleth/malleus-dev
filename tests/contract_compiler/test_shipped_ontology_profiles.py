"""Every shipped ontology loads under every profile it is declared to support.

Two loaders read the same shipped LinkML: ``OntologyRegistry``, the default
typed-graph profile, and ``compile_linkml_contract``, the compiler-enabled
profile. They are separate paths (docs/PRINCIPLES.md, principle 6) and they do
not accept the same schemas. Nothing in ``ontology/`` says which profile a
schema supports, so ``shipped_ontology_profiles.yaml`` beside this file says
it, and this test holds each declared pair to a load. A schema added under
``ontology/`` with no declaration fails here too.
"""

from __future__ import annotations

from importlib.resources import files
from pathlib import Path

import yaml

from malleus import OntologyRegistry, bundled_ontology_path
from malleus.compiler import compile_linkml_contract


DECLARATION = Path(__file__).with_name("shipped_ontology_profiles.yaml")
PROFILES = ("typed-graph", "compiler-enabled")
LINKML_TYPES = "linkml:types"


def _ontology_root() -> Path:
    return bundled_ontology_path("malleus.yaml").parent


def _declared() -> dict[str, list[str]]:
    return yaml.safe_load(DECLARATION.read_bytes())["schemas"]


def _shipped(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in root.rglob("*.yaml")}


def declaration_drift(root: Path, declared: dict[str, list[str]]) -> list[str]:
    """Every schema under ``root`` with no declaration, and every stale declaration."""
    shipped = _shipped(root)
    return [f"{path}: shipped with no declared profile" for path in sorted(shipped - set(declared))] + [
        f"{path}: declared but not shipped" for path in sorted(set(declared) - shipped)
    ]


def _sources(root: Path, relative: str) -> dict[str, bytes]:
    """The exact import closure of one shipped schema, keyed by import literal."""
    by_name = {path.stem: path for path in root.rglob("*.yaml")}
    types = files("linkml_runtime").joinpath("linkml_model", "model", "schema", "types.yaml")
    root_path = root / relative
    sources: dict[str, bytes] = {}
    pending = [(root_path.stem, root_path)]
    while pending:
        name, path = pending.pop()
        if name in sources:
            continue
        sources[name] = path.read_bytes()
        for literal in yaml.safe_load(sources[name]).get("imports", []):
            if literal == LINKML_TYPES:
                sources[literal] = types.read_bytes()
            else:
                pending.append((literal, by_name[literal]))
    return sources


def _refusal(root: Path, relative: str, profile: str) -> str | None:
    try:
        if profile == "typed-graph":
            OntologyRegistry(root / relative)
        elif profile == "compiler-enabled":
            compile_linkml_contract(
                root_locator=Path(relative).stem, sources=_sources(root, relative)
            )
        else:
            raise ValueError(f"unknown profile {profile!r}; known: {PROFILES}")
    except Exception as error:  # the test reports every refusal, of any kind
        return f"{relative} under {profile}: {type(error).__name__}: {error}"
    return None


def test_every_shipped_schema_declares_its_profiles() -> None:
    declared = _declared()
    drift = declaration_drift(_ontology_root(), declared)
    assert not drift, "\n".join(drift)
    assert {
        path: profiles
        for path, profiles in declared.items()
        if not profiles or set(profiles) - set(PROFILES) or len(set(profiles)) != len(profiles)
    } == {}


def test_every_shipped_schema_loads_under_every_declared_profile() -> None:
    root = _ontology_root()
    refusals = [
        refusal
        for relative, profiles in sorted(_declared().items())
        for profile in profiles
        if (refusal := _refusal(root, relative, profile)) is not None
    ]
    assert not refusals, "\n".join(refusals)


def test_a_pack_added_without_a_declaration_is_named(tmp_path: Path) -> None:
    root = tmp_path / "ontology"
    for relative in _shipped(_ontology_root()):
        (root / relative).parent.mkdir(parents=True, exist_ok=True)
        (root / relative).write_bytes((_ontology_root() / relative).read_bytes())
    (root / "packs" / "undeclared.yaml").write_text("id: undeclared\nname: undeclared\n")

    assert declaration_drift(root, _declared()) == [
        "packs/undeclared.yaml: shipped with no declared profile"
    ]
