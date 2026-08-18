"""Strict, offline harness for the frozen GraphRecipe v0 case corpus.

Execution consumes only manifests and declared inputs. Golden artifacts are
opened exclusively by :func:`assert_receipt` and
:func:`propose_pending_digests`; they are never inputs to realization.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

import yaml

from malleus.kg import KnowledgeGraph
from malleus.ledger import canonical_json
from malleus.ontology import OntologyRegistry
from malleus.source import source_bytes_digest

from .assembly import (
    AssemblyFailure,
    StagingFailure,
    assemble_plan,
    stage_and_materialize,
)
from .contract import derive_logical_contract
from .model import (
    GraphRecipeDiagnostic,
    GraphRecipeFailure,
    IdentityBinding,
    IdentityPolicy,
    InvocationPlan,
    OntologySymbolBindings,
    load_json_object,
)
from .stottr import RecipeTerm, compile_graph_recipe, expand_invocation, parse_stottr


SCHEMA_VERSION = "1"
ARTIFACT_LAYERS = (
    "logical_contract",
    "terminal_facts",
    "member_graph",
    "proposed_operations",
    "graph",
    "lineage",
    "diagnostics",
)
DIGEST_NAMES = (
    "source",
    "effective_recipe",
    "invocation",
    "plan",
    "candidate",
    "final_state",
)
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_EXPECTED_FILENAMES = {
    "logical_contract": "logical-contract.json",
    "terminal_facts": "terminal-facts.json",
    "member_graph": "member-graph.json",
    "proposed_operations": "proposed-operations.json",
    "graph": "graph.json",
    "lineage": "lineage.json",
    "diagnostics": "diagnostics.json",
}
_MANIFEST_REQUIRED = {
    "schema_version",
    "experiment_id",
    "case_id",
    "contract_id",
    "profile",
    "artifact_digests",
    "input",
    "expected",
    "expected_outcome",
    "digest_expectations",
}
_MANIFEST_OPTIONAL = {
    "purpose",
    "population_input_mode",
    "staging",
    "metamorphic_obligations",
    "negative_cases",
    "expected_diagnostic",
    "retained_endpoint_diagnostic",
}
_INPUT_FIELDS = {
    "ontology",
    "ontology_symbol_bindings",
    "recipe",
    "recipe_lock",
    "invocations",
    "identity_policy",
    "prior_graph",
}
_CONTRACT_SUGGESTIONS = {
    "GE-000-ONTOLOGY-IS-NOT-POPULATION": (
        "https://fixtures.malleus.dev/graph-recipe/v0/contract/person-only"
    ),
    "GE-010-ONE-ENTITY": "https://fixtures.malleus.dev/graph-recipe/v0/contract/person-only",
    "GE-020-TWO-NODES-ONE-RELATION": (
        "https://fixtures.malleus.dev/graph-recipe/v0/contract/employment"
    ),
}
_INVOCATION_FAILURES = {
    "MANDATORY_RECIPE_VALUE_MISSING": (
        "Mandatory argument binding failed.",
        "not-produced-binding-failed",
    ),
    "RECIPE_ARGUMENT_TYPE_MISMATCH": (
        "Typed argument binding failed.",
        "not-produced-binding-failed",
    ),
    "FORBIDDEN_BLANK_NODE": (
        "Profile validation rejected identity binding.",
        "not-produced-profile-validation-failed",
    ),
}
_FAILURE_COMPLETED_LAYER = {
    "RECIPE_SELECTION_MISSING": "logical-contract",
    "MANDATORY_RECIPE_VALUE_MISSING": "effective-recipe",
    "RECIPE_ARGUMENT_TYPE_MISMATCH": "effective-recipe",
    "FORBIDDEN_BLANK_NODE": "effective-recipe",
    "LOCAL_REFERENCE_DEPENDENCY_MISSING": "terminal-facts",
    "CONSTRUCTION_DEPENDENCY_CYCLE": "member-graph",
    "PLAN_GATE_REJECTION": "proposed-operations",
}


class CaseHarnessError(ValueError):
    """A corpus declaration or harness boundary is invalid."""


class ReceiptMismatch(AssertionError):
    """Actual execution does not match the frozen assertion oracle."""


class PendingDigestObligation(ReceiptMismatch):
    """A digest is deliberately unfrozen and requires proposal review."""


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise CaseHarnessError("YAML object keys must be strings")
        if key in result:
            raise CaseHarnessError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _json_copy(value: Any) -> Any:
    return json.loads(canonical_json(value))


def _require_object(value: Any, subject: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise CaseHarnessError(f"{subject} must be an object with string keys")
    return value


def _require_array(value: Any, subject: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise CaseHarnessError(f"{subject} must be an array")
    return value


def _require_text(value: Any, subject: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CaseHarnessError(f"{subject} must be a nonblank string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise CaseHarnessError(f"{subject} must be valid UTF-8") from error
    return value


def _require_iri(value: Any, subject: str) -> str:
    iri = _require_text(value, subject)
    parsed = urlsplit(iri)
    if not parsed.scheme or any(character.isspace() for character in iri):
        raise CaseHarnessError(f"{subject} must be an absolute IRI")
    return iri


def _exact_fields(
    value: Mapping[str, Any],
    required: set[str] | Sequence[str],
    subject: str,
    optional: set[str] | Sequence[str] = (),
) -> None:
    required_set = set(required)
    allowed = required_set | set(optional)
    missing = sorted(required_set - set(value))
    unknown = sorted(set(value) - allowed)
    if missing or unknown:
        parts = []
        if missing:
            parts.append(f"missing required fields: {', '.join(missing)}")
        if unknown:
            parts.append(f"unknown fields: {', '.join(unknown)}")
        raise CaseHarnessError(f"{subject} has {'; '.join(parts)}")


def _find_corpus_root(manifest_path: Path) -> Path:
    candidate = manifest_path.expanduser()
    if candidate.is_symlink():
        candidate = candidate.resolve(strict=True)
    else:
        candidate = candidate.resolve(strict=True)
    if not candidate.is_file():
        raise CaseHarnessError(f"manifest is not a regular file: {candidate}")
    for ancestor in candidate.parents:
        if (ancestor / "corpus.json").is_file() and (ancestor / "profile.json").is_file():
            return ancestor.resolve(strict=True)
    raise CaseHarnessError(f"manifest is not inside a GraphRecipe v0 corpus: {candidate}")


def _relative_name(path: Path, corpus_root: Path) -> str:
    return path.relative_to(corpus_root).as_posix()


def _contains_expected(path: Path, corpus_root: Path) -> bool:
    return "expected" in path.relative_to(corpus_root).parts


def _local_file(
    locator: Any,
    *,
    base: Path,
    corpus_root: Path,
    subject: str,
    execution: bool,
) -> Path:
    text = _require_text(locator, subject)
    raw = Path(text)
    if raw.is_absolute() or urlsplit(text).scheme:
        raise CaseHarnessError(f"{subject} must be a relative local path")
    try:
        resolved = (base / raw).resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise CaseHarnessError(f"{subject} cannot be resolved: {text}") from error
    try:
        resolved.relative_to(corpus_root)
    except ValueError as error:
        raise CaseHarnessError(f"{subject} escapes the corpus root: {text}") from error
    if not resolved.is_file():
        raise CaseHarnessError(f"{subject} is not a regular file: {text}")
    if execution and _contains_expected(resolved, corpus_root):
        raise CaseHarnessError(
            f"oracle boundary violation: execution input {subject} resolves inside expected/: {text}"
        )
    return resolved


def _assertion_locator(
    locator: Any,
    *,
    base: Path,
    corpus_root: Path,
    subject: str,
) -> Path:
    return _local_file(
        locator,
        base=base,
        corpus_root=corpus_root,
        subject=subject,
        execution=False,
    )


def _mark_read(path: Path, corpus_root: Path, reads: set[str]) -> None:
    if _contains_expected(path, corpus_root):
        raise CaseHarnessError(
            f"oracle boundary violation: execution attempted to read {_relative_name(path, corpus_root)}"
        )
    reads.add(_relative_name(path, corpus_root))


def _load_yaml_object(
    path: Path,
    corpus_root: Path,
    reads: set[str],
) -> tuple[Mapping[str, Any], str]:
    source = _read_input_bytes(path, corpus_root, reads)
    try:
        value = yaml.load(source.decode("utf-8"), Loader=_UniqueKeyLoader)
    except (OSError, UnicodeError, yaml.YAMLError, CaseHarnessError) as error:
        raise CaseHarnessError(f"cannot load YAML object {path}: {error}") from error
    return _require_object(value, str(path)), source_bytes_digest(source)


def _load_input_json(path: Path, corpus_root: Path, reads: set[str]) -> Mapping[str, Any]:
    _mark_read(path, corpus_root, reads)
    return load_json_object(path)


def _read_input_bytes(path: Path, corpus_root: Path, reads: set[str]) -> bytes:
    _mark_read(path, corpus_root, reads)
    try:
        return path.read_bytes()
    except OSError as error:
        raise CaseHarnessError(f"cannot read input artifact {path}: {error}") from error


def _validate_digest_spec(value: Any, subject: str, algorithm: str | None = None) -> None:
    if isinstance(value, str):
        _require_text(value, subject)
        return
    data = _require_object(value, subject)
    status = data.get("status")
    if status == "pending":
        _exact_fields(data, {"status", "algorithm", "obligation_id"}, subject)
        _require_text(data["obligation_id"], f"{subject}.obligation_id")
    elif status == "complete":
        _exact_fields(data, {"status", "algorithm", "value"}, subject)
        if not isinstance(data["value"], str) or _DIGEST.fullmatch(data["value"]) is None:
            raise CaseHarnessError(f"{subject}.value must be a sha256 digest")
    else:
        raise CaseHarnessError(f"{subject}.status must be pending or complete")
    actual_algorithm = _require_text(data["algorithm"], f"{subject}.algorithm")
    if algorithm is not None and actual_algorithm != algorithm:
        raise CaseHarnessError(f"{subject}.algorithm must be {algorithm!r}")


def _validate_manifest(data: Mapping[str, Any], path: Path) -> None:
    if "contract_id" not in data:
        experiment = data.get("experiment_id")
        suggestion = _CONTRACT_SUGGESTIONS.get(experiment)
        patch = f" Add exactly: contract_id: {suggestion}" if suggestion else ""
        raise CaseHarnessError(f"{path}: missing required field contract_id.{patch}")
    _exact_fields(data, _MANIFEST_REQUIRED, str(path), _MANIFEST_OPTIONAL)
    if data["schema_version"] != SCHEMA_VERSION:
        raise CaseHarnessError(f"{path}.schema_version must be {SCHEMA_VERSION!r}")
    _require_text(data["experiment_id"], f"{path}.experiment_id")
    _require_text(data["case_id"], f"{path}.case_id")
    _require_iri(data["contract_id"], f"{path}.contract_id")
    _require_text(data["profile"], f"{path}.profile")
    outcome = data["expected_outcome"]
    if outcome not in {"success", "success-with-no-population", "rejected"}:
        raise CaseHarnessError(f"{path}.expected_outcome is unsupported: {outcome!r}")

    inputs = _require_object(data["input"], f"{path}.input")
    unknown_inputs = sorted(set(inputs) - _INPUT_FIELDS)
    common = {"ontology", "ontology_symbol_bindings", "prior_graph"}
    missing_common = sorted(common - set(inputs))
    if unknown_inputs or missing_common:
        raise CaseHarnessError(
            f"{path}.input has missing fields {missing_common} and unknown fields {unknown_inputs}"
        )
    recipe_fields = {"recipe", "recipe_lock", "identity_policy"}
    if set(inputs) & recipe_fields and not recipe_fields | {"invocations"} <= set(inputs):
        missing = sorted((recipe_fields | {"invocations"}) - set(inputs))
        raise CaseHarnessError(f"{path}.input has incomplete recipe inputs, missing: {missing}")
    if "recipe" in inputs and data.get("population_input_mode") != "direct-typed-invocation":
        raise CaseHarnessError(
            f"{path}.population_input_mode must be 'direct-typed-invocation' when recipe exists"
        )

    expected = _require_object(data["expected"], f"{path}.expected")
    _exact_fields(expected, set(ARTIFACT_LAYERS), f"{path}.expected")
    for layer, locator in expected.items():
        text = _require_text(locator, f"{path}.expected.{layer}")
        if Path(text).name != _EXPECTED_FILENAMES[layer]:
            raise CaseHarnessError(
                f"{path}.expected.{layer} must name {_EXPECTED_FILENAMES[layer]!r}"
            )
        if Path(text).is_absolute() or urlsplit(text).scheme:
            raise CaseHarnessError(f"{path}.expected.{layer} must be a relative local path")

    declared_locators = [data["profile"], *inputs.values(), *expected.values()]
    for index, locator in enumerate(declared_locators):
        _require_text(locator, f"{path}.declared_artifacts[{index}]")
    if len(set(declared_locators)) != len(declared_locators):
        raise CaseHarnessError(f"{path} repeats a profile, input, or expected artifact locator")
    artifact_digests = _require_object(data["artifact_digests"], f"{path}.artifact_digests")
    _exact_fields(artifact_digests, set(declared_locators), f"{path}.artifact_digests")
    for locator, digest in artifact_digests.items():
        if not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None:
            raise CaseHarnessError(
                f"{path}.artifact_digests[{locator!r}] must be a sha256 digest"
            )

    digests = _require_object(data["digest_expectations"], f"{path}.digest_expectations")
    _exact_fields(digests, set(DIGEST_NAMES), f"{path}.digest_expectations")
    for name, value in digests.items():
        algorithm = "source-bytes-sha256-v1" if name == "source" else "canonical-json-sha256-v1"
        _validate_digest_spec(value, f"{path}.digest_expectations.{name}", algorithm)

    obligations = _require_array(
        data.get("metamorphic_obligations", []),
        f"{path}.metamorphic_obligations",
    )
    seen_obligations: set[str] = set()
    legal_artifacts = {
        "logical-contract",
        "terminal-facts",
        "member-graph",
        "proposed-operations",
        "graph",
        "lineage-semantics",
        "diagnostics",
    }
    for index, value in enumerate(obligations):
        subject = f"{path}.metamorphic_obligations[{index}]"
        if isinstance(value, str):
            transform = _require_text(value, subject)
        else:
            obligation = _require_object(value, subject)
            _exact_fields(
                obligation,
                {"transform"},
                subject,
                {"source_digest", "invariant_digests", "invariant_artifacts"},
            )
            transform = _require_text(obligation["transform"], f"{subject}.transform")
            if "source_digest" in obligation and obligation["source_digest"] not in {
                "changes",
                "preserved",
            }:
                raise CaseHarnessError(f"{subject}.source_digest must be changes or preserved")
            if "invariant_digests" in obligation:
                invariant_digests = _require_array(
                    obligation["invariant_digests"],
                    f"{subject}.invariant_digests",
                )
                digest_names = {
                    _require_text(item, f"{subject}.invariant_digests[{item_index}]")
                    for item_index, item in enumerate(invariant_digests)
                }
                unknown_digests = sorted(digest_names - set(DIGEST_NAMES))
                if unknown_digests:
                    raise CaseHarnessError(
                        f"{subject}.invariant_digests has unknown values: {unknown_digests}"
                    )
            if "invariant_artifacts" in obligation:
                invariant_artifacts = _require_array(
                    obligation["invariant_artifacts"],
                    f"{subject}.invariant_artifacts",
                )
                artifact_names = {
                    _require_text(item, f"{subject}.invariant_artifacts[{item_index}]")
                    for item_index, item in enumerate(invariant_artifacts)
                }
                unknown_artifacts = sorted(artifact_names - legal_artifacts)
                if unknown_artifacts:
                    raise CaseHarnessError(
                        f"{subject}.invariant_artifacts has unknown values: {unknown_artifacts}"
                    )
        if transform in seen_obligations:
            raise CaseHarnessError(f"{path} repeats metamorphic obligation {transform!r}")
        seen_obligations.add(transform)

    negatives = data.get("negative_cases", [])
    values = _require_array(negatives, f"{path}.negative_cases")
    seen: set[str] = set()
    for index, item in enumerate(values):
        declaration = _require_object(item, f"{path}.negative_cases[{index}]")
        _exact_fields(declaration, {"case_id", "manifest"}, f"{path}.negative_cases[{index}]")
        case_id = _require_text(declaration["case_id"], f"{path}.negative_cases[{index}].case_id")
        _require_text(declaration["manifest"], f"{path}.negative_cases[{index}].manifest")
        if case_id in seen:
            raise CaseHarnessError(f"{path} repeats negative case {case_id!r}")
        seen.add(case_id)


def _load_selected_manifest(
    manifest_path: str | Path,
    case_id: str,
    reads: set[str],
) -> tuple[Path, Path, Mapping[str, Any], str]:
    requested = _require_text(case_id, "case_id")
    supplied = Path(manifest_path)
    corpus_root = _find_corpus_root(supplied)
    root_path = supplied.expanduser().resolve(strict=True)
    if _contains_expected(root_path, corpus_root):
        raise CaseHarnessError("a case manifest cannot reside inside expected/")
    root, root_digest = _load_yaml_object(root_path, corpus_root, reads)
    _validate_manifest(root, root_path)
    if root["case_id"] == requested:
        return corpus_root, root_path, root, root_digest
    matches = [
        item for item in root.get("negative_cases", []) if item["case_id"] == requested
    ]
    if len(matches) != 1:
        declared = [root["case_id"], *(item["case_id"] for item in root.get("negative_cases", []))]
        raise CaseHarnessError(
            f"case {requested!r} is not declared by {root_path}; declared cases: {declared}"
        )
    selected_path = _local_file(
        matches[0]["manifest"],
        base=root_path.parent,
        corpus_root=corpus_root,
        subject=f"{root_path}.negative_cases[{requested}].manifest",
        execution=True,
    )
    selected, selected_digest = _load_yaml_object(selected_path, corpus_root, reads)
    _validate_manifest(selected, selected_path)
    if selected["case_id"] != requested or selected["experiment_id"] != root["experiment_id"]:
        raise CaseHarnessError(
            f"negative manifest {selected_path} does not match its declaration in {root_path}"
        )
    return corpus_root, selected_path, selected, selected_digest


def _load_profile(
    path: Path,
    corpus_root: Path,
    reads: set[str],
) -> Mapping[str, Any]:
    profile = _load_input_json(path, corpus_root, reads)
    fields = {
        "schema_version",
        "profile_id",
        "status",
        "authored_language",
        "namespaces",
        "accepted_decisions",
        "terminal_abi",
        "assembly",
        "ontology_symbol_binding",
        "lineage_identity",
        "fixture_limits",
        "artifact_contract",
        "digest_contract",
        "network_policy",
        "excluded_scope",
    }
    _exact_fields(profile, fields, str(path))
    _require_text(profile["schema_version"], f"{path}.schema_version")
    _require_iri(profile["profile_id"], f"{path}.profile_id")
    if profile["network_policy"] != "forbidden":
        raise CaseHarnessError(f"{path}.network_policy must be 'forbidden'")
    limits = _require_object(profile["fixture_limits"], f"{path}.fixture_limits")
    limit_fields = {
        "maximum_template_depth",
        "maximum_invocation_count",
        "maximum_list_size",
        "maximum_cross_product_size",
        "maximum_terminal_member_count",
        "maximum_output_bytes",
    }
    _exact_fields(limits, limit_fields, f"{path}.fixture_limits")
    for name, value in limits.items():
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise CaseHarnessError(f"{path}.fixture_limits.{name} must be a positive integer")
    return profile


def _verify_source_digest(spec: Any, actual: str, subject: str) -> None:
    _validate_digest_spec(spec, subject, "source-bytes-sha256-v1")
    if isinstance(spec, Mapping) and spec["status"] == "complete" and spec["value"] != actual:
        raise CaseHarnessError(
            f"{subject} does not match exact source bytes: expected {spec['value']}, got {actual}"
        )


def _verify_execution_artifact_pin(
    *,
    manifest: Mapping[str, Any],
    locator: str,
    path: Path,
    corpus_root: Path,
    reads: set[str],
) -> None:
    actual = source_bytes_digest(_read_input_bytes(path, corpus_root, reads))
    expected = manifest["artifact_digests"][locator]
    if actual != expected:
        raise CaseHarnessError(
            f"artifact pin mismatch for {locator!r}: expected {expected}, got {actual}"
        )


def _verify_assertion_artifact_pin(
    *,
    manifest: Mapping[str, Any],
    locator: str,
    path: Path,
) -> None:
    try:
        actual = source_bytes_digest(path.read_bytes())
    except OSError as error:
        raise ReceiptMismatch(f"cannot read pinned assertion artifact {path}: {error}") from error
    expected = manifest["artifact_digests"][locator]
    if actual != expected:
        raise ReceiptMismatch(
            f"artifact pin mismatch for {locator!r}: expected {expected}, got {actual}"
        )


@dataclass(frozen=True)
class _LockedRecipe:
    root_template: str
    root_source_digest: str
    documents: tuple[Any, ...]
    source_digests: tuple[tuple[str, str], ...]


def _load_locked_recipe(
    *,
    lock_path: Path,
    declared_recipe: Path,
    corpus_root: Path,
    reads: set[str],
) -> _LockedRecipe:
    lock = _load_input_json(lock_path, corpus_root, reads)
    fields = {
        "schema_version",
        "lock_id",
        "root_template",
        "root_artifact",
        "root_source_digest",
        "network_access",
        "libraries",
    }
    _exact_fields(lock, fields, str(lock_path))
    if lock["schema_version"] != SCHEMA_VERSION:
        raise CaseHarnessError(f"{lock_path}.schema_version must be {SCHEMA_VERSION!r}")
    _require_iri(lock["lock_id"], f"{lock_path}.lock_id")
    root_template = _require_iri(lock["root_template"], f"{lock_path}.root_template")
    if lock["network_access"] != "forbidden":
        raise CaseHarnessError(f"{lock_path}.network_access must be 'forbidden'")
    root_path = _local_file(
        lock["root_artifact"],
        base=lock_path.parent,
        corpus_root=corpus_root,
        subject=f"{lock_path}.root_artifact",
        execution=True,
    )
    if root_path != declared_recipe:
        raise CaseHarnessError(
            f"{lock_path}.root_artifact must resolve to declared recipe input {declared_recipe}"
        )

    root_bytes = _read_input_bytes(root_path, corpus_root, reads)
    root_digest = source_bytes_digest(root_bytes)
    _verify_source_digest(lock["root_source_digest"], root_digest, f"{lock_path}.root_source_digest")
    documents = [
        parse_stottr(root_bytes, _relative_name(root_path, corpus_root))
    ]
    sources = [(_relative_name(root_path, corpus_root), root_digest)]

    libraries = _require_array(lock["libraries"], f"{lock_path}.libraries")
    if not libraries:
        raise CaseHarnessError(f"{lock_path}.libraries cannot be empty")
    library_ids: set[str] = set()
    library_paths: set[Path] = set()
    for index, item in enumerate(libraries):
        subject = f"{lock_path}.libraries[{index}]"
        library = _require_object(item, subject)
        _exact_fields(
            library,
            {"library_id", "version", "media_type", "path", "source_digest"},
            subject,
        )
        library_id = _require_iri(library["library_id"], f"{subject}.library_id")
        _require_text(library["version"], f"{subject}.version")
        if library["media_type"] != "text/stottr":
            raise CaseHarnessError(f"{subject}.media_type must be 'text/stottr'")
        path = _local_file(
            library["path"],
            base=lock_path.parent,
            corpus_root=corpus_root,
            subject=f"{subject}.path",
            execution=True,
        )
        if library_id in library_ids or path in library_paths:
            raise CaseHarnessError(f"{lock_path} repeats a locked library identity or path")
        library_ids.add(library_id)
        library_paths.add(path)
        source_bytes = _read_input_bytes(path, corpus_root, reads)
        digest = source_bytes_digest(source_bytes)
        _verify_source_digest(library["source_digest"], digest, f"{subject}.source_digest")
        source_id = _relative_name(path, corpus_root)
        documents.append(parse_stottr(source_bytes, source_id))
        sources.append((source_id, digest))
    return _LockedRecipe(root_template, root_digest, tuple(documents), tuple(sorted(sources)))


@dataclass(frozen=True)
class _IdentityResolver:
    policy_id: str
    values: Mapping[str, Mapping[str, str]]

    def resolve(self, binding: IdentityBinding) -> str:
        identity = self.values.get(binding.identity_key)
        if identity is None:
            raise GraphRecipeFailure(
                GraphRecipeDiagnostic(
                    "IDENTITY_BINDING_UNRESOLVED",
                    "invocation-binding",
                    binding.identity_key,
                    {"message": f"Identity key '{binding.identity_key}' is not declared."},
                    {"identity_key": binding.identity_key, "policy_id": self.policy_id},
                )
            )
        return identity[binding.field]


def _load_identity_resolver(
    path: Path,
    corpus_root: Path,
    reads: set[str],
) -> _IdentityResolver:
    raw = _load_input_json(path, corpus_root, reads)
    identities = _require_array(raw.get("identities"), f"{path}.identities")
    contains_blank = any(
        isinstance(item, Mapping)
        and isinstance(item.get("member_iri"), str)
        and item["member_iri"].startswith("_:")
        for item in identities
    )
    if not contains_blank:
        policy = IdentityPolicy.from_dict(raw, subject=str(path))
        return _IdentityResolver(
            policy.policy_id,
            {
                item.identity_key: {
                    "member_iri": item.member_iri,
                    "record_id": item.record_id,
                }
                for item in policy.identities
            },
        )

    _exact_fields(raw, {"schema_version", "policy_id", "collision_policy", "identities"}, str(path))
    if raw["schema_version"] != SCHEMA_VERSION:
        raise CaseHarnessError(f"{path}.schema_version must be {SCHEMA_VERSION!r}")
    policy_id = _require_iri(raw["policy_id"], f"{path}.policy_id")
    if raw["collision_policy"] != "reject":
        raise CaseHarnessError(f"{path}.collision_policy must be 'reject'")
    values: dict[str, dict[str, str]] = {}
    record_ids: set[str] = set()
    member_ids: set[str] = set()
    for index, item in enumerate(identities):
        subject = f"{path}.identities[{index}]"
        identity = _require_object(item, subject)
        _exact_fields(identity, {"identity_key", "member_iri", "record_id"}, subject)
        key = _require_text(identity["identity_key"], f"{subject}.identity_key")
        member = _require_text(identity["member_iri"], f"{subject}.member_iri")
        record_id = _require_text(identity["record_id"], f"{subject}.record_id")
        if member.startswith("_:"):
            if len(member) == 2 or any(character.isspace() for character in member):
                raise CaseHarnessError(f"{subject}.member_iri is not a valid blank-node label")
        else:
            _require_iri(member, f"{subject}.member_iri")
        if key in values or member in member_ids or record_id in record_ids:
            raise CaseHarnessError(f"{path} violates collision_policy 'reject'")
        values[key] = {"member_iri": member, "record_id": record_id}
        member_ids.add(member)
        record_ids.add(record_id)
    return _IdentityResolver(policy_id, values)


def _recipe_term(binding: IdentityBinding, value: str) -> RecipeTerm:
    if binding.field == "member_iri":
        if value.startswith("_:"):
            return RecipeTerm("blank", value)
        return RecipeTerm.iri(value)
    return RecipeTerm.literal(value)


def _graph_artifact(graph: KnowledgeGraph, *, staging: str, materialization: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "complete",
        "staging": staging,
        "materialization": materialization,
        "snapshot": graph.snapshot(),
        "canonical_operations": list(graph.canonical_operations()),
        "state_digest": graph.state_digest(),
    }


def _diagnostics_artifact(diagnostics: Sequence[GraphRecipeDiagnostic]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "diagnostics": [item.as_dict() for item in diagnostics],
    }


def _not_produced_member(code: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "not-produced",
        "blocked_by": code,
        "members": [],
        "dependencies": [],
        "acyclic": None,
        "topological_order": [],
    }


def _not_produced_operations(code: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "not-produced",
        "blocked_by": code,
        "operations": [],
    }


def _lineage_failure(diagnostic: GraphRecipeDiagnostic) -> dict[str, Any]:
    failure: dict[str, Any] = {
        "code": diagnostic.code,
        "subject": diagnostic.subject,
    }
    parameter = diagnostic.evidence.get("parameter")
    if isinstance(parameter, str):
        failure["argument"] = parameter
    failure["completed_layer"] = _FAILURE_COMPLETED_LAYER.get(
        diagnostic.code,
        diagnostic.phase,
    )
    return failure


def _lineage(
    *,
    expansion_paths: Sequence[Mapping[str, Any]],
    operations: Sequence[Mapping[str, Any]],
    diagnostics: Sequence[GraphRecipeDiagnostic] = (),
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "complete",
        "expansion_paths": _json_copy(expansion_paths),
        "operations": _json_copy(operations),
        "failures": [_lineage_failure(item) for item in diagnostics],
    }


def _failed_operation_lineage(emissions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[tuple[str, str]]] = {}
    for emission in emissions:
        member = emission["fact"]["member"]
        grouped.setdefault(member, []).append(
            (emission["emission_id"], emission["expansion_path_id"])
        )
    return [
        {
            "member": member,
            "operation_index": None,
            "emission_ids": [item[0] for item in sorted(grouped[member])],
            "expansion_path_ids": [item[1] for item in sorted(grouped[member])],
        }
        for member in sorted(grouped)
    ]


def _selection_missing(
    path: Path,
    corpus_root: Path,
    reads: set[str],
) -> GraphRecipeDiagnostic:
    data = _load_input_json(path, corpus_root, reads)
    _exact_fields(
        data,
        {"schema_version", "request_id", "realization_requested", "recipe_set", "invocations"},
        str(path),
    )
    if (
        data["schema_version"] != SCHEMA_VERSION
        or data["realization_requested"] is not True
        or data["recipe_set"] is not None
        or data["invocations"] != []
    ):
        raise CaseHarnessError(f"{path} is not a recipe-selection-missing request")
    request_id = _require_iri(data["request_id"], f"{path}.request_id")
    return GraphRecipeDiagnostic(
        "RECIPE_SELECTION_MISSING",
        "population-plan",
        request_id,
        {"message": "Realization was requested without a selected GraphRecipeSet."},
        {"request_id": request_id},
    )


@dataclass(frozen=True, init=False)
class ConformanceReceipt:
    """Defensive record of actual execution only, never golden contents."""

    schema_version: str
    experiment_id: str
    case_id: str
    manifest_digest: str
    actual_outcome: str
    completed_layers: tuple[str, ...]
    _artifacts_json: str = field(repr=False)
    _digests_json: str = field(repr=False)
    _reads_json: str = field(repr=False)
    _manifest_path: Path = field(repr=False, compare=False)
    _corpus_root: Path = field(repr=False, compare=False)

    def __init__(
        self,
        *,
        experiment_id: str,
        case_id: str,
        manifest_digest: str,
        actual_outcome: str,
        artifacts: Mapping[str, Any],
        semantic_digests: Mapping[str, Any],
        execution_reads: Sequence[str],
        manifest_path: Path,
        corpus_root: Path,
    ) -> None:
        _exact_fields(artifacts, set(ARTIFACT_LAYERS), "receipt.artifacts")
        _exact_fields(semantic_digests, set(DIGEST_NAMES), "receipt.semantic_digests")
        if _DIGEST.fullmatch(manifest_digest) is None:
            raise ValueError("receipt.manifest_digest must be a sha256 digest")
        completed = tuple(
            layer
            for layer in ARTIFACT_LAYERS
            if layer == "diagnostics" or artifacts[layer].get("status") == "complete"
        )
        object.__setattr__(self, "schema_version", SCHEMA_VERSION)
        object.__setattr__(self, "experiment_id", experiment_id)
        object.__setattr__(self, "case_id", case_id)
        object.__setattr__(self, "manifest_digest", manifest_digest)
        object.__setattr__(self, "actual_outcome", actual_outcome)
        object.__setattr__(self, "completed_layers", completed)
        object.__setattr__(self, "_artifacts_json", canonical_json(artifacts))
        object.__setattr__(self, "_digests_json", canonical_json(semantic_digests))
        object.__setattr__(self, "_reads_json", canonical_json(sorted(set(execution_reads))))
        object.__setattr__(self, "_manifest_path", manifest_path)
        object.__setattr__(self, "_corpus_root", corpus_root)

    @property
    def artifacts(self) -> dict[str, Any]:
        return json.loads(self._artifacts_json)

    @property
    def semantic_digests(self) -> dict[str, Any]:
        return json.loads(self._digests_json)

    @property
    def execution_reads(self) -> tuple[str, ...]:
        return tuple(json.loads(self._reads_json))

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "experiment_id": self.experiment_id,
            "case_id": self.case_id,
            "manifest_digest": self.manifest_digest,
            "actual_outcome": self.actual_outcome,
            "completed_layers": list(self.completed_layers),
            "artifacts": self.artifacts,
            "semantic_digests": self.semantic_digests,
            "execution_reads": list(self.execution_reads),
        }


def _receipt(
    *,
    manifest: Mapping[str, Any],
    manifest_path: Path,
    manifest_digest: str,
    corpus_root: Path,
    reads: set[str],
    artifacts: Mapping[str, Any],
    digests: Mapping[str, Any],
) -> ConformanceReceipt:
    diagnostics = artifacts["diagnostics"]["diagnostics"]
    if diagnostics:
        outcome = "rejected"
    elif "recipe" not in manifest["input"]:
        outcome = "success-with-no-population"
    else:
        outcome = "success"
    encoded = canonical_json(artifacts).encode("utf-8")
    profile_path = _local_file(
        manifest["profile"],
        base=manifest_path.parent,
        corpus_root=corpus_root,
        subject=f"{manifest_path}.profile",
        execution=True,
    )
    _verify_execution_artifact_pin(
        manifest=manifest,
        locator=manifest["profile"],
        path=profile_path,
        corpus_root=corpus_root,
        reads=reads,
    )
    profile = _load_profile(profile_path, corpus_root, reads)
    maximum = profile["fixture_limits"]["maximum_output_bytes"]
    if len(encoded) > maximum:
        raise CaseHarnessError(
            f"case output is {len(encoded)} bytes, above profile maximum_output_bytes {maximum}"
        )
    return ConformanceReceipt(
        experiment_id=manifest["experiment_id"],
        case_id=manifest["case_id"],
        manifest_digest=manifest_digest,
        actual_outcome=outcome,
        artifacts=artifacts,
        semantic_digests=digests,
        execution_reads=tuple(reads),
        manifest_path=manifest_path,
        corpus_root=corpus_root,
    )


def run_experiment(manifest_path: str | Path, case_id: str) -> ConformanceReceipt:
    """Execute one declared case without opening any expected artifact."""

    reads: set[str] = set()
    corpus_root, selected_path, manifest, manifest_digest = _load_selected_manifest(
        manifest_path,
        case_id,
        reads,
    )
    input_paths = {
        name: _local_file(
            locator,
            base=selected_path.parent,
            corpus_root=corpus_root,
            subject=f"{selected_path}.input.{name}",
            execution=True,
        )
        for name, locator in manifest["input"].items()
    }
    profile_path = _local_file(
        manifest["profile"],
        base=selected_path.parent,
        corpus_root=corpus_root,
        subject=f"{selected_path}.profile",
        execution=True,
    )
    _verify_execution_artifact_pin(
        manifest=manifest,
        locator=manifest["profile"],
        path=profile_path,
        corpus_root=corpus_root,
        reads=reads,
    )
    for name, locator in manifest["input"].items():
        _verify_execution_artifact_pin(
            manifest=manifest,
            locator=locator,
            path=input_paths[name],
            corpus_root=corpus_root,
            reads=reads,
        )
    profile = _load_profile(profile_path, corpus_root, reads)

    ontology_path = input_paths["ontology"]
    _mark_read(ontology_path, corpus_root, reads)
    registry = OntologyRegistry(ontology_path)
    bindings_path = input_paths["ontology_symbol_bindings"]
    bindings_data = _load_input_json(bindings_path, corpus_root, reads)
    bindings = OntologySymbolBindings.from_dict(bindings_data, subject=str(bindings_path))
    bound_ontology = _local_file(
        bindings.ontology_artifact,
        base=bindings_path.parent,
        corpus_root=corpus_root,
        subject=f"{bindings_path}.ontology_artifact",
        execution=True,
    )
    if bound_ontology != ontology_path:
        raise CaseHarnessError(
            f"{bindings_path}.ontology_artifact must resolve to declared ontology input {ontology_path}"
        )
    contract = derive_logical_contract(registry, bindings, manifest["contract_id"])

    prior_path = input_paths["prior_graph"]
    prior = _load_input_json(prior_path, corpus_root, reads)
    _exact_fields(prior, {"entities", "relations", "signals", "events"}, str(prior_path))
    for family, records in prior.items():
        _require_array(records, f"{prior_path}.{family}")
    graph = KnowledgeGraph.from_records(registry, dict(prior))

    if "recipe" not in input_paths:
        logical = contract.as_dict()
        if "invocations" not in input_paths:
            artifacts = {
                "logical_contract": logical,
                "terminal_facts": {
                    "schema_version": SCHEMA_VERSION,
                    "status": "complete",
                    "invocation_digest": {
                        "status": "not-applicable",
                        "reason": "No recipe invocation exists.",
                    },
                    "emissions": [],
                },
                "member_graph": {
                    "schema_version": SCHEMA_VERSION,
                    "status": "complete",
                    "members": [],
                    "dependencies": [],
                    "acyclic": True,
                    "topological_order": [],
                },
                "proposed_operations": {
                    "schema_version": SCHEMA_VERSION,
                    "status": "complete",
                    "operations": [],
                },
                "graph": _graph_artifact(
                    graph,
                    staging="skipped-empty-operation-sequence",
                    materialization="skipped-empty-operation-sequence",
                ),
                "lineage": _lineage(expansion_paths=(), operations=()),
                "diagnostics": _diagnostics_artifact(()),
            }
            digests = {
                "source": "not-applicable-no-recipe",
                "effective_recipe": "not-applicable-no-recipe",
                "invocation": "not-applicable-no-invocation",
                "plan": "not-applicable-no-population-plan",
                "candidate": "not-applicable-empty-operation-sequence",
                "final_state": graph.state_digest(),
            }
            return _receipt(
                manifest=manifest,
                manifest_path=selected_path,
                manifest_digest=manifest_digest,
                corpus_root=corpus_root,
                reads=reads,
                artifacts=artifacts,
                digests=digests,
            )

        diagnostic = _selection_missing(input_paths["invocations"], corpus_root, reads)
        code = diagnostic.code
        artifacts = {
            "logical_contract": logical,
            "terminal_facts": {
                "schema_version": SCHEMA_VERSION,
                "status": "not-produced",
                "blocked_by": code,
                "invocation_digest": {
                    "status": "not-applicable",
                    "reason": "Recipe selection failed before invocation binding.",
                },
                "emissions": [],
            },
            "member_graph": _not_produced_member(code),
            "proposed_operations": _not_produced_operations(code),
            "graph": _graph_artifact(graph, staging="not-entered", materialization="not-entered"),
            "lineage": _lineage(
                expansion_paths=(),
                operations=(),
                diagnostics=(diagnostic,),
            ),
            "diagnostics": _diagnostics_artifact((diagnostic,)),
        }
        digests = {
            "source": "not-applicable-no-recipe",
            "effective_recipe": "not-applicable-recipe-selection-failed",
            "invocation": "not-applicable-recipe-selection-failed",
            "plan": "not-applicable-recipe-selection-failed",
            "candidate": "not-applicable-recipe-selection-failed",
            "final_state": graph.state_digest(),
        }
        return _receipt(
            manifest=manifest,
            manifest_path=selected_path,
            manifest_digest=manifest_digest,
            corpus_root=corpus_root,
            reads=reads,
            artifacts=artifacts,
            digests=digests,
        )

    locked = _load_locked_recipe(
        lock_path=input_paths["recipe_lock"],
        declared_recipe=input_paths["recipe"],
        corpus_root=corpus_root,
        reads=reads,
    )
    compiled = compile_graph_recipe(
        locked.documents,
        root_template=locked.root_template,
        contract_digest=contract.contract_digest,
        profile_id=profile["profile_id"],
        expansion_profile_id=profile["profile_id"],
    )
    invocation_path = input_paths["invocations"]
    invocation_data = _load_input_json(invocation_path, corpus_root, reads)
    invocation_plan = InvocationPlan.from_dict(invocation_data, subject=str(invocation_path))
    maximum_invocations = profile["fixture_limits"]["maximum_invocation_count"]
    if len(invocation_plan.invocations) != 1:
        raise CaseHarnessError(
            f"{invocation_path} must contain exactly one invocation for this slice, "
            f"received {len(invocation_plan.invocations)}"
        )
    if len(invocation_plan.invocations) > maximum_invocations:
        raise CaseHarnessError(f"{invocation_path} exceeds maximum_invocation_count")
    invocation = invocation_plan.invocations[0]
    if invocation.template != locked.root_template:
        raise CaseHarnessError(
            f"{invocation_path} invocation.template must equal lock root_template "
            f"{locked.root_template!r}"
        )
    resolver = _load_identity_resolver(input_paths["identity_policy"], corpus_root, reads)
    arguments: dict[str, RecipeTerm] = {}
    for argument in invocation.arguments:
        if argument.identity_binding is not None:
            value = resolver.resolve(argument.identity_binding)
            arguments[argument.parameter] = _recipe_term(argument.identity_binding, value)
        else:
            arguments[argument.parameter] = RecipeTerm.from_artifact(
                argument.term.as_dict(),
                f"{invocation.invocation_id}.{argument.parameter}",
            )

    try:
        expansion = expand_invocation(
            compiled,
            invocation_id=invocation.invocation_id,
            arguments=arguments,
        )
    except GraphRecipeFailure as error:
        if any(item.code not in _INVOCATION_FAILURES for item in error.diagnostics):
            raise
        diagnostic = error.diagnostics[0]
        reason, digest_state = _INVOCATION_FAILURES[diagnostic.code]
        code = diagnostic.code
        artifacts = {
            "logical_contract": contract.as_dict(),
            "terminal_facts": {
                "schema_version": SCHEMA_VERSION,
                "status": "not-produced",
                "blocked_by": code,
                "invocation_digest": {"status": "not-produced", "reason": reason},
                "emissions": [],
            },
            "member_graph": _not_produced_member(code),
            "proposed_operations": _not_produced_operations(code),
            "graph": _graph_artifact(graph, staging="not-entered", materialization="not-entered"),
            "lineage": _lineage(
                expansion_paths=(),
                operations=(),
                diagnostics=error.diagnostics,
            ),
            "diagnostics": _diagnostics_artifact(error.diagnostics),
        }
        digests = {
            "source": locked.root_source_digest,
            "effective_recipe": compiled.effective_recipe_digest,
            "invocation": digest_state,
            "plan": digest_state,
            "candidate": digest_state,
            "final_state": graph.state_digest(),
        }
        return _receipt(
            manifest=manifest,
            manifest_path=selected_path,
            manifest_digest=manifest_digest,
            corpus_root=corpus_root,
            reads=reads,
            artifacts=artifacts,
            digests=digests,
        )

    terminal = expansion.terminal_artifact()
    emissions = list(expansion.emissions)
    paths = list(expansion.expansion_paths)
    try:
        plan = assemble_plan(
            contract,
            emissions,
            invocation_digests=(expansion.invocation_digest,),
        )
    except AssemblyFailure as error:
        artifacts = {
            "logical_contract": contract.as_dict(),
            "terminal_facts": terminal,
            "member_graph": error.member_graph_artifact,
            "proposed_operations": error.proposed_operations_artifact,
            "graph": _graph_artifact(graph, staging="not-entered", materialization="not-entered"),
            "lineage": _lineage(
                expansion_paths=paths,
                operations=_failed_operation_lineage(emissions),
                diagnostics=error.diagnostics,
            ),
            "diagnostics": _diagnostics_artifact(error.diagnostics),
        }
        digests = {
            "source": locked.root_source_digest,
            "effective_recipe": compiled.effective_recipe_digest,
            "invocation": expansion.invocation_digest,
            "plan": "not-produced-member-graph-rejected",
            "candidate": "not-produced-member-graph-rejected",
            "final_state": graph.state_digest(),
        }
        return _receipt(
            manifest=manifest,
            manifest_path=selected_path,
            manifest_digest=manifest_digest,
            corpus_root=corpus_root,
            reads=reads,
            artifacts=artifacts,
            digests=digests,
        )

    try:
        realization = stage_and_materialize(graph, plan)
    except StagingFailure as error:
        artifacts = {
            "logical_contract": contract.as_dict(),
            "terminal_facts": terminal,
            "member_graph": error.member_graph_artifact,
            "proposed_operations": error.proposed_operations_artifact,
            "graph": error.graph_artifact,
            "lineage": _lineage(
                expansion_paths=paths,
                operations=plan.operation_lineage(),
                diagnostics=error.diagnostics,
            ),
            "diagnostics": _diagnostics_artifact(error.diagnostics),
        }
        digests = {
            "source": locked.root_source_digest,
            "effective_recipe": compiled.effective_recipe_digest,
            "invocation": expansion.invocation_digest,
            "plan": plan.plan_digest,
            "candidate": error.candidate_digest,
            "final_state": graph.state_digest(),
        }
        return _receipt(
            manifest=manifest,
            manifest_path=selected_path,
            manifest_digest=manifest_digest,
            corpus_root=corpus_root,
            reads=reads,
            artifacts=artifacts,
            digests=digests,
        )

    artifacts = {
        "logical_contract": contract.as_dict(),
        "terminal_facts": terminal,
        "member_graph": plan.member_graph_artifact(),
        "proposed_operations": plan.proposed_operations_artifact(),
        "graph": realization.as_dict(),
        "lineage": _lineage(
            expansion_paths=paths,
            operations=plan.operation_lineage(),
        ),
        "diagnostics": _diagnostics_artifact(()),
    }
    digests = {
        "source": locked.root_source_digest,
        "effective_recipe": compiled.effective_recipe_digest,
        "invocation": expansion.invocation_digest,
        "plan": plan.plan_digest,
        "candidate": realization.candidate_digest or "not-applicable-empty-operation-sequence",
        "final_state": graph.state_digest(),
    }
    return _receipt(
        manifest=manifest,
        manifest_path=selected_path,
        manifest_digest=manifest_digest,
        corpus_root=corpus_root,
        reads=reads,
        artifacts=artifacts,
        digests=digests,
    )


def _load_assertion_manifest(
    receipt: ConformanceReceipt,
    manifest_path: str | Path | None,
    case_id: str | None,
) -> tuple[Path, Path, Mapping[str, Any]]:
    supplied = receipt._manifest_path if manifest_path is None else Path(manifest_path)
    requested = receipt.case_id if case_id is None else case_id
    assertion_reads: set[str] = set()
    corpus_root, selected_path, manifest, manifest_digest = _load_selected_manifest(
        supplied,
        requested,
        assertion_reads,
    )
    if corpus_root != receipt._corpus_root:
        raise ReceiptMismatch("receipt and assertion manifest belong to different corpora")
    if manifest["experiment_id"] != receipt.experiment_id or manifest["case_id"] != receipt.case_id:
        raise ReceiptMismatch("receipt identity does not match assertion manifest")
    if manifest_digest != receipt.manifest_digest:
        raise ReceiptMismatch(
            "assertion manifest bytes differ from the manifest used during execution: "
            f"expected {receipt.manifest_digest}, got {manifest_digest}"
        )
    return corpus_root, selected_path, manifest


def _compare_value(
    expected: Any,
    actual: Any,
    pointer: str,
    pending: list[str],
) -> str | None:
    if isinstance(expected, Mapping) and expected.get("status") == "pending":
        pending.append(pointer or "/")
        return None
    if isinstance(expected, Mapping):
        if not isinstance(actual, Mapping):
            return f"{pointer or '/'} expected object, got {type(actual).__name__}"
        if set(expected) != set(actual):
            return (
                f"{pointer or '/'} object fields differ, expected {sorted(expected)}, "
                f"got {sorted(actual)}"
            )
        for key in expected:
            result = _compare_value(
                expected[key],
                actual[key],
                f"{pointer}/{key.replace('~', '~0').replace('/', '~1')}",
                pending,
            )
            if result is not None:
                return result
        return None
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return f"{pointer or '/'} expected array, got {type(actual).__name__}"
        if len(expected) != len(actual):
            return f"{pointer or '/'} array length differs, expected {len(expected)}, got {len(actual)}"
        for index, item in enumerate(expected):
            result = _compare_value(item, actual[index], f"{pointer}/{index}", pending)
            if result is not None:
                return result
        return None
    if expected != actual or type(expected) is not type(actual):
        return f"{pointer or '/'} expected {expected!r}, got {actual!r}"
    return None


def _assert_digest_expectations(
    manifest: Mapping[str, Any],
    actual: Mapping[str, Any],
    pending: list[str],
    manifest_path: Path,
) -> None:
    for name in DIGEST_NAMES:
        expected = manifest["digest_expectations"][name]
        pointer = f"{manifest_path}#/digest_expectations/{name}"
        if isinstance(expected, Mapping) and expected["status"] == "pending":
            pending.append(pointer)
            continue
        if isinstance(expected, Mapping):
            if actual[name] != expected["value"]:
                raise ReceiptMismatch(
                    f"semantic digest {name} differs, expected {expected['value']}, got {actual[name]}"
                )
        elif actual[name] != expected:
            raise ReceiptMismatch(
                f"semantic digest state {name} differs, expected {expected!r}, got {actual[name]!r}"
            )


def assert_receipt(
    receipt: ConformanceReceipt,
    manifest_path: str | Path | None = None,
    case_id: str | None = None,
) -> None:
    """Compare actual artifacts against goldens, outside the execution path."""

    if not isinstance(receipt, ConformanceReceipt):
        raise TypeError("receipt must be a ConformanceReceipt")
    corpus_root, selected_path, manifest = _load_assertion_manifest(
        receipt,
        manifest_path,
        case_id,
    )
    if receipt.actual_outcome != manifest["expected_outcome"]:
        raise ReceiptMismatch(
            f"outcome differs, expected {manifest['expected_outcome']!r}, "
            f"got {receipt.actual_outcome!r}"
        )
    pending: list[str] = []
    actual_artifacts = receipt.artifacts
    for layer in ARTIFACT_LAYERS:
        locator = manifest["expected"][layer]
        path = _assertion_locator(
            locator,
            base=selected_path.parent,
            corpus_root=corpus_root,
            subject=f"{selected_path}.expected.{layer}",
        )
        _verify_assertion_artifact_pin(
            manifest=manifest,
            locator=locator,
            path=path,
        )
        expected = load_json_object(path)
        mismatch = _compare_value(expected, actual_artifacts[layer], "", pending)
        if mismatch is not None:
            raise ReceiptMismatch(f"{receipt.experiment_id}/{receipt.case_id} {layer}: {mismatch}")
    diagnostics = actual_artifacts["diagnostics"]["diagnostics"]
    expected_code = manifest.get("expected_diagnostic")
    if expected_code is not None:
        actual_codes = [item["code"] for item in diagnostics]
        if actual_codes != [expected_code]:
            raise ReceiptMismatch(
                f"expected diagnostic {expected_code!r}, got {actual_codes!r}"
            )
    _assert_digest_expectations(
        manifest,
        receipt.semantic_digests,
        pending,
        selected_path,
    )
    if pending:
        joined = "\n  ".join(sorted(pending))
        raise PendingDigestObligation(
            "pending digest obligations remain; run the explicit --propose-digests mode:\n  "
            + joined
        )


def _replacement(path: Path, corpus_root: Path, pointer: str, value: Any) -> dict[str, Any]:
    return {
        "path": _relative_name(path, corpus_root),
        "json_pointer": pointer,
        "proposed": _json_copy(value),
    }


def propose_pending_digests(
    receipt: ConformanceReceipt,
    manifest_path: str | Path | None = None,
    case_id: str | None = None,
) -> dict[str, Any]:
    """Return reviewed-patch candidates without writing any corpus file."""

    corpus_root, selected_path, manifest = _load_assertion_manifest(
        receipt,
        manifest_path,
        case_id,
    )
    replacements: list[dict[str, Any]] = []
    algorithms = {
        "source": "source-bytes-sha256-v1",
        **{name: "canonical-json-sha256-v1" for name in DIGEST_NAMES if name != "source"},
    }
    actual_digests = receipt.semantic_digests
    for name in DIGEST_NAMES:
        spec = manifest["digest_expectations"][name]
        if isinstance(spec, Mapping) and spec.get("status") == "pending":
            replacements.append(
                _replacement(
                    selected_path,
                    corpus_root,
                    f"/digest_expectations/{name}",
                    {
                        "status": "complete",
                        "algorithm": algorithms[name],
                        "value": actual_digests[name],
                    },
                )
            )

    terminal_locator = manifest["expected"]["terminal_facts"]
    terminal_path = _assertion_locator(
        terminal_locator,
        base=selected_path.parent,
        corpus_root=corpus_root,
        subject=f"{selected_path}.expected.terminal_facts",
    )
    _verify_assertion_artifact_pin(
        manifest=manifest,
        locator=terminal_locator,
        path=terminal_path,
    )
    terminal = load_json_object(terminal_path)
    invocation_spec = terminal.get("invocation_digest")
    actual_invocation = receipt.artifacts["terminal_facts"].get("invocation_digest")
    if isinstance(invocation_spec, Mapping) and invocation_spec.get("status") == "pending":
        replacements.append(
            _replacement(terminal_path, corpus_root, "/invocation_digest", actual_invocation)
        )

    inputs = manifest["input"]
    if "recipe_lock" in inputs:
        lock_path = _assertion_locator(
            inputs["recipe_lock"],
            base=selected_path.parent,
            corpus_root=corpus_root,
            subject=f"{selected_path}.input.recipe_lock",
        )
        _verify_assertion_artifact_pin(
            manifest=manifest,
            locator=inputs["recipe_lock"],
            path=lock_path,
        )
        lock = load_json_object(lock_path)
        recipe_path = _assertion_locator(
            inputs["recipe"],
            base=selected_path.parent,
            corpus_root=corpus_root,
            subject=f"{selected_path}.input.recipe",
        )
        _verify_assertion_artifact_pin(
            manifest=manifest,
            locator=inputs["recipe"],
            path=recipe_path,
        )
        root_spec = lock["root_source_digest"]
        if isinstance(root_spec, Mapping) and root_spec.get("status") == "pending":
            replacements.append(
                _replacement(
                    lock_path,
                    corpus_root,
                    "/root_source_digest",
                    {
                        "status": "complete",
                        "algorithm": "source-bytes-sha256-v1",
                        "value": source_bytes_digest(recipe_path.read_bytes()),
                    },
                )
            )
        for index, library in enumerate(lock["libraries"]):
            spec = library["source_digest"]
            if not isinstance(spec, Mapping) or spec.get("status") != "pending":
                continue
            library_path = _assertion_locator(
                library["path"],
                base=lock_path.parent,
                corpus_root=corpus_root,
                subject=f"{lock_path}.libraries[{index}].path",
            )
            replacements.append(
                _replacement(
                    lock_path,
                    corpus_root,
                    f"/libraries/{index}/source_digest",
                    {
                        "status": "complete",
                        "algorithm": "source-bytes-sha256-v1",
                        "value": source_bytes_digest(library_path.read_bytes()),
                    },
                )
            )
    replacements.sort(key=lambda item: (item["path"], item["json_pointer"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "mode": "proposal-only",
        "experiment_id": receipt.experiment_id,
        "case_id": receipt.case_id,
        "writes_performed": False,
        "replacements": replacements,
    }
