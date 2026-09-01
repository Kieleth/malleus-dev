"""Private deterministic qualification, binding, and explicit composition."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, auto
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from ._contract_linkml_adapter import (
    AuthoredField,
    AuthoredMapping,
    AuthoredScalar,
    AuthoredSequence,
    AuthoredSequenceItem,
    AuthoredValue,
    ClassifiedOccurrence,
    DeclaredContractClosure,
    DeclaredDeclaration,
    DeclaredModule,
)
from ._contract_source import (
    ModuleObservation,
    ResolvedImportEdge,
    ResolverSelection,
    RetainedSource,
    RootResolution,
    SourceClosure,
)


class BindingRefusalReason(Enum):
    """Closed refusal classes for the private binding boundary."""

    INVALID_PROFILE = auto()
    MALFORMED_INPUT = auto()
    QUALIFIED_IDENTIFIER_COLLISION = auto()
    BUILTIN_COLLISION = auto()
    NON_SLOT_DUPLICATE = auto()
    MULTIPLE_OWNERS = auto()
    ADOPTION_REQUIRED = auto()
    INVALID_ADOPTION = auto()
    ADOPTION_MISMATCH = auto()
    UNKNOWN_REFERENCE = auto()
    AMBIGUOUS_REFERENCE = auto()
    WRONG_REFERENCE_KIND = auto()


@dataclass(frozen=True, slots=True)
class BindingDiagnostic:
    """One deterministic reason the whole binding refused."""

    reason: BindingRefusalReason
    module_id: str
    source_identifier: str
    path: tuple[str | int, ...]
    reference: str | None
    candidates: tuple[str, ...]
    detail: str


class BindingRefusal(ValueError):
    """One typed atomic refusal without a partial composition result."""

    def __init__(self, diagnostics: tuple[BindingDiagnostic, ...]) -> None:
        if not diagnostics:
            raise ValueError("a binding refusal requires a diagnostic")
        self.diagnostics = diagnostics
        self.reason = diagnostics[0].reason
        super().__init__(self.reason.name)


@dataclass(frozen=True, slots=True)
class QualifiedDeclaration:
    """One exact declaration occurrence and its authoritative owner."""

    name: str
    identifier: str
    authoritative_identifier: str
    kind: str
    module_id: str
    schema_id: str
    source_sha256: str | None
    path: tuple[str, ...]
    body: AuthoredMapping
    trusted: bool


@dataclass(frozen=True, slots=True)
class ResolvedReference:
    """One declared reference bound to one exact authoritative target."""

    source_identifier: str
    source_module_id: str
    path: tuple[str | int, ...]
    literal: str
    target_identifier: str
    target_kind: str
    target_module_id: str


@dataclass(frozen=True, slots=True)
class ExplicitAdoption:
    """One accepted reuse marker that leaves the imported owner authoritative."""

    adopter_identifier: str
    adopter_module_id: str
    owner_identifier: str
    owner_module_id: str


@dataclass(frozen=True, slots=True)
class ContractBinding:
    """One deeply immutable qualified binding and composition result."""

    declared_closure: DeclaredContractClosure
    declarations: tuple[QualifiedDeclaration, ...]
    references: tuple[ResolvedReference, ...]
    adoptions: tuple[ExplicitAdoption, ...]
    profile_id: str
    profile_sha256: str


@dataclass(frozen=True, slots=True)
class _Builtin:
    name: str
    identifier: str
    kind: str


@dataclass(frozen=True, slots=True)
class _AdoptionPolicy:
    declaration_kind: str
    annotations_field: str
    marker_field: str
    marker_kind: str
    marker_lexeme: str
    marker_value: bool
    ignored_comparison_fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _ReferenceSite:
    source_kind: str
    selector: tuple[str, ...]
    extract: str
    target_kinds: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _QualificationPath:
    kind: str
    pattern: tuple[str, ...]
    identity: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _Profile:
    profile_id: str
    digest: str
    separator: str
    qualification_paths: tuple[_QualificationPath, ...]
    input_support_profile: str
    input_profile_sha256: str
    global_paths: tuple[str, ...]
    prefix_map_field: str
    trusted_module_id: str
    trusted_schema_id: str
    trusted_byte_length: int
    trusted_sha256: str
    builtins: tuple[_Builtin, ...]
    adoption: _AdoptionPolicy
    reference_sites: tuple[_ReferenceSite, ...]


_PROFILE_PATH = Path(__file__).with_name("_contract_binding_profile.json")
_PROFILE_SCHEMA = "malleus.contract-compiler.binding-profile/v0"
_CANONICALIZATION = "malleus.canonical-json/compact-sorted-key-utf8-no-newline/v0"
_EXTRACTORS = {"MAPPING_KEYS", "SCALAR", "SEQUENCE"}
_SOURCE_KINDS = {"Class", "Module", "Scalar", "Slot"}
_DECLARATION_KINDS = {"Class", "Enum", "Scalar", "Slot"}


def _path_key(path: tuple[str | int, ...]) -> tuple[tuple[int, str], ...]:
    return tuple(
        (0, item) if isinstance(item, str) else (1, str(item)) for item in path
    )


def _diagnostic_key(diagnostic: BindingDiagnostic) -> tuple[object, ...]:
    return (
        diagnostic.module_id,
        diagnostic.source_identifier,
        _path_key(diagnostic.path),
        diagnostic.reference or "",
        diagnostic.reason.name,
        diagnostic.candidates,
        diagnostic.detail,
    )


def _refuse(*diagnostics: BindingDiagnostic) -> BindingRefusal:
    return BindingRefusal(tuple(sorted(diagnostics, key=_diagnostic_key)))


def _diagnostic(
    reason: BindingRefusalReason,
    detail: str,
    *,
    module_id: str = "",
    source_identifier: str = "",
    path: tuple[str | int, ...] = (),
    reference: str | None = None,
    candidates: tuple[str, ...] = (),
) -> BindingDiagnostic:
    return BindingDiagnostic(
        reason=reason,
        module_id=module_id,
        source_identifier=source_identifier,
        path=path,
        reference=reference,
        candidates=tuple(sorted(candidates)),
        detail=detail,
    )


def _profile_refusal(detail: str) -> BindingRefusal:
    return _refuse(_diagnostic(BindingRefusalReason.INVALID_PROFILE, detail))


def _input_refusal(
    detail: str,
    *,
    module_id: str = "",
    source_identifier: str = "",
    path: tuple[str | int, ...] = (),
) -> BindingRefusal:
    return _refuse(
        _diagnostic(
            BindingRefusalReason.MALFORMED_INPUT,
            detail,
            module_id=module_id,
            source_identifier=source_identifier,
            path=path,
        )
    )


def _object_without_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate profile key {key}")
        result[key] = value
    return result


def _mapping(value: object, where: str) -> Mapping[str, Any]:
    if type(value) is not dict or not all(type(key) is str for key in value):
        raise _profile_refusal(f"profile {where} must be an object")
    return value


def _string(value: object, where: str) -> str:
    if type(value) is not str or not value:
        raise _profile_refusal(f"profile {where} must be a nonempty string")
    return value


def _strings(value: object, where: str) -> tuple[str, ...]:
    if type(value) is not list or any(
        type(item) is not str or not item for item in value
    ):
        raise _profile_refusal(f"profile {where} must be a string array")
    result = tuple(value)
    if len(result) != len(set(result)):
        raise _profile_refusal(f"profile {where} repeats a value")
    return result


def _exact_keys(value: Mapping[str, Any], expected: set[str], where: str) -> None:
    if set(value) != expected:
        raise _profile_refusal(f"profile {where} is not closed")


def _load_profile() -> _Profile:
    raw = _PROFILE_PATH.read_bytes()
    try:
        decoded = json.loads(raw, object_pairs_hook=_object_without_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise _profile_refusal("profile is not exact UTF-8 JSON") from error
    root = _mapping(decoded, "root")
    _exact_keys(
        root,
        {
            "adoption",
            "canonicalization",
            "declared_input",
            "global_declaration_paths",
            "prefix_map_field",
            "profile_id",
            "qualification",
            "reference_sites",
            "schema",
            "trusted_builtins",
            "trusted_module",
        },
        "root",
    )
    if (
        root["schema"] != _PROFILE_SCHEMA
        or root["canonicalization"] != _CANONICALIZATION
    ):
        raise _profile_refusal("profile identity or canonicalization is unsupported")

    qualification = _mapping(root["qualification"], "qualification")
    _exact_keys(
        qualification,
        {"declaration_paths", "operation", "separator"},
        "qualification",
    )
    if qualification["operation"] != "delimiter_join":
        raise _profile_refusal("profile qualification operation is unsupported")
    separator = _string(qualification["separator"], "qualification.separator")
    if separator != "/":
        raise _profile_refusal("profile qualification separator is unsupported")

    path_values = qualification["declaration_paths"]
    if type(path_values) is not list or not path_values:
        raise _profile_refusal("profile declaration_paths must be a nonempty array")
    qualification_paths: list[_QualificationPath] = []
    for index, value in enumerate(path_values):
        spec = _mapping(value, f"declaration_paths[{index}]")
        _exact_keys(
            spec,
            {"identity", "kind", "pattern"},
            f"declaration_paths[{index}]",
        )
        kind = _string(spec["kind"], f"declaration_paths[{index}].kind")
        pattern = _strings(spec["pattern"], f"declaration_paths[{index}].pattern")
        identity = _strings(spec["identity"], f"declaration_paths[{index}].identity")
        variables = {token for token in pattern if token.startswith("$")}
        if (
            kind not in _DECLARATION_KINDS
            or "$name" not in variables
            or not set(identity) <= variables
        ):
            raise _profile_refusal("profile declaration path is unsupported")
        qualification_paths.append(
            _QualificationPath(kind=kind, pattern=pattern, identity=identity)
        )

    declared_input = _mapping(root["declared_input"], "declared_input")
    _exact_keys(
        declared_input,
        {"profile_sha256", "support_profile"},
        "declared_input",
    )

    trusted = _mapping(root["trusted_module"], "trusted_module")
    _exact_keys(
        trusted,
        {"byte_length", "module_id", "schema_id", "sha256"},
        "trusted_module",
    )
    if type(trusted["byte_length"]) is not int or trusted["byte_length"] < 0:
        raise _profile_refusal("profile trusted byte_length is malformed")

    builtin_values = root["trusted_builtins"]
    if type(builtin_values) is not list or not builtin_values:
        raise _profile_refusal("profile trusted_builtins must be a nonempty array")
    builtins: list[_Builtin] = []
    for index, value in enumerate(builtin_values):
        spec = _mapping(value, f"trusted_builtins[{index}]")
        _exact_keys(spec, {"identifier", "kind", "name"}, f"trusted_builtins[{index}]")
        kind = _string(spec["kind"], f"trusted_builtins[{index}].kind")
        if kind not in _DECLARATION_KINDS:
            raise _profile_refusal("profile builtin kind is unsupported")
        builtins.append(
            _Builtin(
                name=_string(spec["name"], f"trusted_builtins[{index}].name"),
                identifier=_string(
                    spec["identifier"], f"trusted_builtins[{index}].identifier"
                ),
                kind=kind,
            )
        )
    if len({item.name for item in builtins}) != len(builtins) or len(
        {item.identifier for item in builtins}
    ) != len(builtins):
        raise _profile_refusal("profile trusted builtins collide")

    adoption_value = _mapping(root["adoption"], "adoption")
    _exact_keys(
        adoption_value,
        {
            "annotations_field",
            "declaration_kind",
            "ignored_comparison_fields",
            "marker_field",
            "marker_kind",
            "marker_lexeme",
            "marker_value",
        },
        "adoption",
    )
    marker_value = adoption_value["marker_value"]
    if type(marker_value) is not bool or marker_value is not True:
        raise _profile_refusal("profile adoption marker must be literal true")
    adoption = _AdoptionPolicy(
        declaration_kind=_string(adoption_value["declaration_kind"], "adoption.kind"),
        annotations_field=_string(
            adoption_value["annotations_field"], "adoption.annotations_field"
        ),
        marker_field=_string(adoption_value["marker_field"], "adoption.marker_field"),
        marker_kind=_string(adoption_value["marker_kind"], "adoption.marker_kind"),
        marker_lexeme=_string(
            adoption_value["marker_lexeme"], "adoption.marker_lexeme"
        ),
        marker_value=marker_value,
        ignored_comparison_fields=_strings(
            adoption_value["ignored_comparison_fields"],
            "adoption.ignored_comparison_fields",
        ),
    )
    if adoption.declaration_kind not in _DECLARATION_KINDS:
        raise _profile_refusal("profile adoption kind is unsupported")

    site_values = root["reference_sites"]
    if type(site_values) is not list or not site_values:
        raise _profile_refusal("profile reference_sites must be a nonempty array")
    sites: list[_ReferenceSite] = []
    for index, value in enumerate(site_values):
        spec = _mapping(value, f"reference_sites[{index}]")
        _exact_keys(
            spec,
            {"extract", "selector", "source_kind", "target_kinds"},
            f"reference_sites[{index}]",
        )
        source_kind = _string(spec["source_kind"], "reference source_kind")
        extract = _string(spec["extract"], "reference extract")
        target_kinds = _strings(spec["target_kinds"], "reference target_kinds")
        if (
            source_kind not in _SOURCE_KINDS
            or extract not in _EXTRACTORS
            or not set(target_kinds) <= _DECLARATION_KINDS
        ):
            raise _profile_refusal("profile reference operation is unsupported")
        sites.append(
            _ReferenceSite(
                source_kind=source_kind,
                selector=_strings(spec["selector"], "reference selector"),
                extract=extract,
                target_kinds=target_kinds,
            )
        )

    return _Profile(
        profile_id=_string(root["profile_id"], "profile_id"),
        digest=f"sha256:{sha256(raw).hexdigest()}",
        separator=separator,
        qualification_paths=tuple(qualification_paths),
        input_support_profile=_string(
            declared_input["support_profile"], "declared_input.support_profile"
        ),
        input_profile_sha256=_string(
            declared_input["profile_sha256"], "declared_input.profile_sha256"
        ),
        global_paths=_strings(root["global_declaration_paths"], "global paths"),
        prefix_map_field=_string(root["prefix_map_field"], "prefix_map_field"),
        trusted_module_id=_string(trusted["module_id"], "trusted module_id"),
        trusted_schema_id=_string(trusted["schema_id"], "trusted schema_id"),
        trusted_byte_length=trusted["byte_length"],
        trusted_sha256=_string(trusted["sha256"], "trusted sha256"),
        builtins=tuple(builtins),
        adoption=adoption,
        reference_sites=tuple(sites),
    )


def _validate_selection(value: object, where: str) -> None:
    if type(value) is not ResolverSelection or any(
        type(item) is not str or not item
        for item in (value.resolver_id, value.profile_version, value.configuration_id)
    ):
        raise _input_refusal(f"{where} resolver selection is malformed")


def _validate_authored(value: object, path: tuple[str | int, ...] = ()) -> None:
    if type(value) is AuthoredScalar:
        if (
            type(value.kind) is not str
            or not value.kind
            or type(value.lexeme) is not str
            or (value.value is not None and type(value.value) not in {bool, str})
        ):
            raise _input_refusal("authored scalar is malformed", path=path)
        return
    if type(value) is AuthoredSequence:
        if type(value.items) is not tuple:
            raise _input_refusal("authored sequence must be immutable", path=path)
        for index, item in enumerate(value.items):
            if type(item) is not AuthoredSequenceItem or type(item.ordinal) is not int:
                raise _input_refusal("authored sequence item is malformed", path=path)
            _validate_authored(item.value, path + (index,))
        return
    if type(value) is AuthoredMapping:
        if type(value.fields) is not tuple:
            raise _input_refusal("authored mapping must be immutable", path=path)
        names: set[str] = set()
        for field in value.fields:
            if (
                type(field) is not AuthoredField
                or type(field.name) is not str
                or not field.name
                or field.name in names
                or type(field.ordinal) is not int
                or type(field.classification) is not str
                or (
                    field.value_classification is not None
                    and type(field.value_classification) is not str
                )
            ):
                raise _input_refusal("authored mapping field is malformed", path=path)
            names.add(field.name)
            _validate_authored(field.value, path + (field.name,))
        return
    raise _input_refusal("authored value has an unsupported mutable shape", path=path)


def _qualified_identifier(
    schema_id: str, declaration: DeclaredDeclaration, profile: _Profile
) -> str:
    for path_spec in profile.qualification_paths:
        if path_spec.kind != declaration.kind or len(path_spec.pattern) != len(
            declaration.path
        ):
            continue
        variables: dict[str, str] = {}
        matched = True
        for expected, actual in zip(path_spec.pattern, declaration.path, strict=True):
            if expected.startswith("$"):
                prior = variables.setdefault(expected, actual)
                matched = matched and prior == actual
            else:
                matched = matched and expected == actual
        if not matched or variables.get("$name") != declaration.name:
            continue
        return profile.separator.join(
            (schema_id, *(variables[token] for token in path_spec.identity))
        )
    raise _input_refusal(
        "declaration path cannot be qualified",
        source_identifier=declaration.identifier,
        path=declaration.path,
    )


def _validate_source(source: object, module_id: str) -> None:
    if (
        type(source) is not RetainedSource
        or source.resolved_locator != module_id
        or type(source.source_bytes) is not bytes
        or type(source.byte_length) is not int
        or source.byte_length != len(source.source_bytes)
        or source.sha256 != f"sha256:{sha256(source.source_bytes).hexdigest()}"
        or type(source.media_type) is not str
        or not source.media_type
    ):
        raise _input_refusal(
            "retained source provenance is malformed", module_id=module_id
        )
    _validate_selection(source.resolver_selection, "retained source")


def _validate_input(closure: object, profile: _Profile) -> DeclaredContractClosure:
    if type(closure) is not DeclaredContractClosure:
        raise _input_refusal("binder input must be one exact DeclaredContractClosure")
    if (
        type(closure.modules) is not tuple
        or type(closure.source_closure) is not SourceClosure
    ):
        raise _input_refusal("binder input containers must be immutable")
    source_closure = closure.source_closure
    if (
        type(source_closure.modules) is not tuple
        or type(source_closure.import_edges) is not tuple
    ):
        raise _input_refusal("source closure containers must be immutable")
    _validate_selection(source_closure.selection, "source closure")
    if type(source_closure.root) is not RootResolution:
        raise _input_refusal("source closure root is malformed")
    _validate_selection(source_closure.root.resolver_selection, "source closure root")

    observations: dict[str, ModuleObservation] = {}
    for observation in source_closure.modules:
        if (
            type(observation) is not ModuleObservation
            or type(observation.module_id) is not str
            or not observation.module_id
            or type(observation.authored_imports) is not tuple
            or any(
                type(item) is not str or not item
                for item in observation.authored_imports
            )
            or observation.module_id in observations
        ):
            raise _input_refusal("source closure module is malformed")
        _validate_source(observation.source, observation.module_id)
        if observation.source.resolver_selection != source_closure.selection:
            raise _input_refusal(
                "retained module uses another resolver selection",
                module_id=observation.module_id,
            )
        observations[observation.module_id] = observation

    declared_ids: set[str] = set()
    for module in closure.modules:
        if (
            type(module) is not DeclaredModule
            or type(module.module_id) is not str
            or not module.module_id
            or module.module_id in declared_ids
            or type(module.schema_id) is not str
            or not module.schema_id
            or type(module.authored_imports) is not tuple
            or type(module.declarations) is not tuple
            or type(module.occurrences) is not tuple
            or type(module.trusted) is not bool
            or type(module.support_profile) is not str
            or type(module.profile_sha256) is not str
        ):
            raise _input_refusal("declared module is malformed")
        declared_ids.add(module.module_id)
        if (
            module.support_profile != profile.input_support_profile
            or module.profile_sha256 != profile.input_profile_sha256
        ):
            raise _input_refusal(
                "declared module was produced under another adapter profile",
                module_id=module.module_id,
            )
        if module.trusted:
            expected_declarations = tuple(
                (
                    builtin.name,
                    builtin.identifier,
                    builtin.kind,
                    index,
                    ("trusted_builtins", builtin.name),
                    AuthoredMapping(()),
                )
                for index, builtin in enumerate(profile.builtins)
            )
            observed_declarations = tuple(
                (
                    declaration.name,
                    declaration.identifier,
                    declaration.kind,
                    declaration.ordinal,
                    declaration.path,
                    declaration.body,
                )
                for declaration in module.declarations
            )
            if (
                module.module_id != profile.trusted_module_id
                or module.schema_id != profile.trusted_schema_id
                or module.source.byte_length != profile.trusted_byte_length
                or module.source.sha256 != profile.trusted_sha256
                or module.authored_imports
                or module.root != AuthoredMapping(())
                or observed_declarations != expected_declarations
            ):
                raise _input_refusal(
                    "trusted module does not match the exact profile authority",
                    module_id=module.module_id,
                )
        elif module.module_id == profile.trusted_module_id:
            raise _input_refusal(
                "trusted module identity cannot be treated as ordinary source",
                module_id=module.module_id,
            )
        observation = observations.get(module.module_id)
        if (
            observation is None
            or module.source != observation.source
            or module.authored_imports != observation.authored_imports
        ):
            raise _input_refusal(
                "declared module differs from retained source closure",
                module_id=module.module_id,
            )
        _validate_authored(module.root)
        for occurrence in module.occurrences:
            if (
                type(occurrence) is not ClassifiedOccurrence
                or type(occurrence.path) is not tuple
                or type(occurrence.ordinal_path) is not tuple
            ):
                raise _input_refusal("classified occurrence is malformed")
            _validate_authored(occurrence.value, occurrence.path)
        for declaration in module.declarations:
            if (
                type(declaration) is not DeclaredDeclaration
                or type(declaration.name) is not str
                or not declaration.name
                or type(declaration.identifier) is not str
                or not declaration.identifier
                or declaration.kind not in _DECLARATION_KINDS
                or type(declaration.ordinal) is not int
                or type(declaration.path) is not tuple
            ):
                raise _input_refusal(
                    "declared declaration is malformed", module_id=module.module_id
                )
            _validate_authored(declaration.body, declaration.path)
            if not module.trusted and declaration.identifier != _qualified_identifier(
                module.schema_id, declaration, profile
            ):
                raise _input_refusal(
                    "declaration identifier is not derived from its exact schema ID",
                    module_id=module.module_id,
                    source_identifier=declaration.identifier,
                    path=declaration.path,
                )

    if declared_ids != set(observations):
        raise _input_refusal("declared and retained module sets differ")
    root = source_closure.root
    root_observation = observations.get(root.resolved_locator)
    if (
        type(root.requested_locator) is not str
        or not root.requested_locator
        or type(root.resolved_locator) is not str
        or not root.resolved_locator
        or root_observation is None
        or root.source_sha256 != root_observation.source.sha256
        or root.resolver_selection != source_closure.selection
    ):
        raise _input_refusal("source closure root does not match its retained module")

    expected_edges = {
        (module.module_id, ordinal): literal
        for module in closure.modules
        for ordinal, literal in enumerate(module.authored_imports)
    }
    observed_edges: dict[tuple[str, int], ResolvedImportEdge] = {}
    children: dict[str, set[str]] = {module_id: set() for module_id in declared_ids}
    for edge in source_closure.import_edges:
        if (
            type(edge) is not ResolvedImportEdge
            or edge.parent_module_id not in declared_ids
            or edge.child_module_id not in declared_ids
            or type(edge.parent_import_ordinal) is not int
            or type(edge.literal_import) is not str
            or not edge.literal_import
            or edge.resolver_selection != source_closure.selection
        ):
            raise _input_refusal("source import edge is malformed")
        key = (edge.parent_module_id, edge.parent_import_ordinal)
        if key in observed_edges or expected_edges.get(key) != edge.literal_import:
            raise _input_refusal("source import edge differs from authored evidence")
        observed_edges[key] = edge
        children[edge.parent_module_id].add(edge.child_module_id)
    if set(observed_edges) != set(expected_edges):
        raise _input_refusal("source closure does not bind every authored import")

    reachable: set[str] = set()
    pending = [root.resolved_locator]
    while pending:
        module_id = pending.pop()
        if module_id in reachable:
            continue
        reachable.add(module_id)
        pending.extend(children[module_id])
    if reachable != declared_ids:
        raise _input_refusal("source closure contains a module outside the exact root")

    active: set[str] = set()
    completed: set[str] = set()

    def visit(module_id: str) -> None:
        if module_id in active:
            raise _input_refusal("source closure contains an import cycle")
        if module_id in completed:
            return
        active.add(module_id)
        for child in children[module_id]:
            visit(child)
        active.remove(module_id)
        completed.add(module_id)

    visit(root.resolved_locator)
    return closure


def _mapping_field(mapping: AuthoredMapping, name: str) -> AuthoredField | None:
    return next((field for field in mapping.fields if field.name == name), None)


def _marker(
    declaration: DeclaredDeclaration, policy: _AdoptionPolicy
) -> AuthoredScalar | None:
    annotations = _mapping_field(declaration.body, policy.annotations_field)
    if annotations is None:
        return None
    if type(annotations.value) is not AuthoredMapping:
        return AuthoredScalar("INVALID", "", None)
    marker = _mapping_field(annotations.value, policy.marker_field)
    if marker is None or type(marker.value) is not AuthoredScalar:
        return AuthoredScalar("INVALID", "", None)
    return marker.value


def _valid_marker(marker: AuthoredScalar | None, policy: _AdoptionPolicy) -> bool:
    return marker == AuthoredScalar(
        policy.marker_kind,
        policy.marker_lexeme,
        policy.marker_value,
    )


def _comparison_value(value: AuthoredValue) -> object:
    if type(value) is AuthoredScalar:
        return (
            "SCALAR",
            value.kind,
            value.lexeme,
            type(value.value).__name__,
            value.value,
        )
    if type(value) is AuthoredSequence:
        return (
            "SEQUENCE",
            tuple(_comparison_value(item.value) for item in value.items),
        )
    return (
        "MAPPING",
        tuple(
            sorted(
                (field.name, _comparison_value(field.value)) for field in value.fields
            )
        ),
    )


def _comparison_body(
    declaration: DeclaredDeclaration, policy: _AdoptionPolicy
) -> object:
    kept: list[AuthoredField] = []
    for field in declaration.body.fields:
        if field.name in policy.ignored_comparison_fields:
            continue
        if field.name != policy.annotations_field:
            kept.append(field)
            continue
        if type(field.value) is not AuthoredMapping:
            kept.append(field)
            continue
        annotations = tuple(
            item for item in field.value.fields if item.name != policy.marker_field
        )
        if annotations:
            kept.append(replace(field, value=AuthoredMapping(annotations)))
    return _comparison_value(AuthoredMapping(tuple(kept)))


def _imports(closure: DeclaredContractClosure) -> dict[str, frozenset[str]]:
    children: dict[str, set[str]] = {
        module.module_id: set() for module in closure.modules
    }
    for edge in closure.source_closure.import_edges:
        children[edge.parent_module_id].add(edge.child_module_id)
    result: dict[str, frozenset[str]] = {}
    for module_id in children:
        reached: set[str] = set()
        pending = list(children[module_id])
        while pending:
            child = pending.pop()
            if child in reached:
                continue
            reached.add(child)
            pending.extend(children[child])
        result[module_id] = frozenset(reached)
    return result


def _is_global(declaration: DeclaredDeclaration, profile: _Profile) -> bool:
    return len(declaration.path) == 2 and declaration.path[0] in profile.global_paths


def _qualified(
    closure: DeclaredContractClosure, profile: _Profile
) -> tuple[
    tuple[QualifiedDeclaration, ...],
    tuple[ExplicitAdoption, ...],
    dict[str, frozenset[str]],
]:
    reachable = _imports(closure)
    modules = {module.module_id: module for module in closure.modules}
    qualified: list[QualifiedDeclaration] = []
    originals: dict[str, DeclaredDeclaration] = {}
    for module in closure.modules:
        if module.trusted:
            continue
        for declaration in module.declarations:
            qualified.append(
                QualifiedDeclaration(
                    name=declaration.name,
                    identifier=declaration.identifier,
                    authoritative_identifier=declaration.identifier,
                    kind=declaration.kind,
                    module_id=module.module_id,
                    schema_id=module.schema_id,
                    source_sha256=module.source.sha256,
                    path=declaration.path,
                    body=declaration.body,
                    trusted=False,
                )
            )
            originals[declaration.identifier] = declaration

    identifier_groups: dict[str, list[QualifiedDeclaration]] = {}
    for declaration in qualified:
        identifier_groups.setdefault(declaration.identifier, []).append(declaration)
    collisions = [group for group in identifier_groups.values() if len(group) > 1]
    if collisions:
        diagnostics = tuple(
            _diagnostic(
                BindingRefusalReason.QUALIFIED_IDENTIFIER_COLLISION,
                "multiple declarations have the same qualified identifier",
                module_id=group[0].module_id,
                source_identifier=group[0].identifier,
                path=group[0].path,
                candidates=tuple(item.module_id for item in group),
            )
            for group in collisions
        )
        raise _refuse(*diagnostics)

    builtin_names = {item.name for item in profile.builtins}
    builtin_collisions = [item for item in qualified if item.name in builtin_names]
    if builtin_collisions:
        raise _refuse(
            *(
                _diagnostic(
                    BindingRefusalReason.BUILTIN_COLLISION,
                    "a source declaration collides with a trusted builtin name",
                    module_id=item.module_id,
                    source_identifier=item.identifier,
                    path=item.path,
                    reference=item.name,
                )
                for item in builtin_collisions
            )
        )

    groups: dict[str, list[QualifiedDeclaration]] = {}
    for declaration in qualified:
        original = originals[declaration.identifier]
        if _is_global(original, profile):
            groups.setdefault(declaration.name, []).append(declaration)

    owner_by_identifier = {item.identifier: item.identifier for item in qualified}
    adoptions: list[ExplicitAdoption] = []
    for name, group in groups.items():
        if len(group) == 1:
            only = group[0]
            marker = _marker(originals[only.identifier], profile.adoption)
            if marker is not None:
                raise _refuse(
                    _diagnostic(
                        BindingRefusalReason.INVALID_ADOPTION,
                        "an authoritative declaration cannot adopt without an ancestor owner",
                        module_id=only.module_id,
                        source_identifier=only.identifier,
                        path=only.path,
                        reference=name,
                    )
                )
            continue
        if any(item.kind != profile.adoption.declaration_kind for item in group):
            first = sorted(group, key=lambda item: item.identifier)[0]
            raise _refuse(
                _diagnostic(
                    BindingRefusalReason.NON_SLOT_DUPLICATE,
                    "only slot declarations can use explicit adoption",
                    module_id=first.module_id,
                    source_identifier=first.identifier,
                    path=first.path,
                    reference=name,
                    candidates=tuple(item.identifier for item in group),
                )
            )
        owners = [
            candidate
            for candidate in group
            if all(
                candidate.module_id == other.module_id
                or candidate.module_id in reachable[other.module_id]
                for other in group
            )
        ]
        if len(owners) != 1:
            first = sorted(group, key=lambda item: item.identifier)[0]
            raise _refuse(
                _diagnostic(
                    BindingRefusalReason.MULTIPLE_OWNERS,
                    "duplicate declarations do not have one imported ancestor owner",
                    module_id=first.module_id,
                    source_identifier=first.identifier,
                    path=first.path,
                    reference=name,
                    candidates=tuple(item.identifier for item in group),
                )
            )
        owner = owners[0]
        if _marker(originals[owner.identifier], profile.adoption) is not None:
            raise _refuse(
                _diagnostic(
                    BindingRefusalReason.INVALID_ADOPTION,
                    "the authoritative owner carries an adoption marker",
                    module_id=owner.module_id,
                    source_identifier=owner.identifier,
                    path=owner.path,
                    reference=name,
                )
            )
        for adopter in group:
            if adopter is owner:
                continue
            marker = _marker(originals[adopter.identifier], profile.adoption)
            if marker is None:
                reason = BindingRefusalReason.ADOPTION_REQUIRED
                detail = "an imported duplicate slot lacks the explicit adoption marker"
            elif not _valid_marker(marker, profile.adoption):
                reason = BindingRefusalReason.INVALID_ADOPTION
                detail = "the adoption marker is not exact literal Boolean true"
            elif _comparison_body(
                originals[adopter.identifier], profile.adoption
            ) != _comparison_body(originals[owner.identifier], profile.adoption):
                reason = BindingRefusalReason.ADOPTION_MISMATCH
                detail = "the adopting slot differs from its owner before elaboration"
            else:
                owner_by_identifier[adopter.identifier] = owner.identifier
                adoptions.append(
                    ExplicitAdoption(
                        adopter_identifier=adopter.identifier,
                        adopter_module_id=adopter.module_id,
                        owner_identifier=owner.identifier,
                        owner_module_id=owner.module_id,
                    )
                )
                continue
            raise _refuse(
                _diagnostic(
                    reason,
                    detail,
                    module_id=adopter.module_id,
                    source_identifier=adopter.identifier,
                    path=adopter.path,
                    reference=name,
                    candidates=(owner.identifier,),
                )
            )

    qualified = [
        replace(
            item,
            authoritative_identifier=owner_by_identifier[item.identifier],
        )
        for item in qualified
    ]
    existing_trusted = modules.get(profile.trusted_module_id)
    source_sha256 = existing_trusted.source.sha256 if existing_trusted else None
    for builtin in profile.builtins:
        qualified.append(
            QualifiedDeclaration(
                name=builtin.name,
                identifier=builtin.identifier,
                authoritative_identifier=builtin.identifier,
                kind=builtin.kind,
                module_id=profile.trusted_module_id,
                schema_id=profile.trusted_schema_id,
                source_sha256=source_sha256,
                path=("trusted_builtins", builtin.name),
                body=AuthoredMapping(()),
                trusted=True,
            )
        )
    return (
        tuple(
            sorted(
                qualified,
                key=lambda item: (item.identifier, item.module_id, item.path),
            )
        ),
        tuple(
            sorted(
                adoptions,
                key=lambda item: (item.adopter_identifier, item.owner_identifier),
            )
        ),
        reachable,
    )


def _selected(
    value: AuthoredValue,
    selector: tuple[str, ...],
    path: tuple[str | int, ...] = (),
) -> tuple[tuple[AuthoredValue, tuple[str | int, ...]], ...]:
    if not selector:
        return ((value, path),)
    token = selector[0]
    remaining = selector[1:]
    if token == "*":
        if type(value) is AuthoredSequence:
            return tuple(
                selected
                for item in value.items
                for selected in _selected(item.value, remaining, path + (item.ordinal,))
            )
        if type(value) is AuthoredMapping:
            return tuple(
                selected
                for field in value.fields
                for selected in _selected(field.value, remaining, path + (field.name,))
            )
        return ()
    if type(value) is not AuthoredMapping:
        return ()
    field = _mapping_field(value, token)
    return () if field is None else _selected(field.value, remaining, path + (token,))


def _raw_references(
    value: AuthoredValue, site: _ReferenceSite
) -> tuple[tuple[str, tuple[str | int, ...]], ...]:
    result: list[tuple[str, tuple[str | int, ...]]] = []
    for selected, path in _selected(value, site.selector):
        if site.extract == "SCALAR":
            if type(selected) is not AuthoredScalar or type(selected.value) is not str:
                raise _input_refusal("reference scalar is malformed", path=path)
            result.append((selected.value, path))
        elif site.extract == "SEQUENCE":
            if type(selected) is not AuthoredSequence:
                raise _input_refusal("reference sequence is malformed", path=path)
            for item in selected.items:
                if (
                    type(item.value) is not AuthoredScalar
                    or type(item.value.value) is not str
                ):
                    raise _input_refusal(
                        "reference sequence item is malformed", path=path
                    )
                result.append((item.value.value, path + (item.ordinal,)))
        else:
            if type(selected) is not AuthoredMapping:
                raise _input_refusal("reference mapping is malformed", path=path)
            result.extend(
                (field.name, path + (field.name,)) for field in selected.fields
            )
    return tuple(result)


def _prefixes(module: DeclaredModule, profile: _Profile) -> dict[str, str]:
    field = _mapping_field(module.root, profile.prefix_map_field)
    if field is None:
        return {}
    if type(field.value) is not AuthoredMapping:
        raise _input_refusal("prefix map is malformed", module_id=module.module_id)
    result: dict[str, str] = {}
    for item in field.value.fields:
        if type(item.value) is not AuthoredScalar or type(item.value.value) is not str:
            raise _input_refusal(
                "prefix value is malformed", module_id=module.module_id
            )
        result[item.name] = item.value.value
    return result


def _reference_candidates(
    *,
    literal: str,
    source: QualifiedDeclaration | None,
    module: DeclaredModule,
    declarations: tuple[QualifiedDeclaration, ...],
    reachable: Mapping[str, frozenset[str]],
    target_kinds: tuple[str, ...],
    profile: _Profile,
) -> tuple[tuple[QualifiedDeclaration, ...], tuple[QualifiedDeclaration, ...]]:
    visible_modules = reachable[module.module_id] | {module.module_id}
    visible = tuple(
        item
        for item in declarations
        if item.trusted or item.module_id in visible_modules
    )
    prefix, separator, local = literal.partition(":")
    if separator:
        base = _prefixes(module, profile).get(prefix)
        matches = (
            ()
            if base is None
            else tuple(
                item
                for item in visible
                if item.identifier == base + local
                or item.authoritative_identifier == base + local
            )
        )
    else:
        local_matches: tuple[QualifiedDeclaration, ...] = ()
        if source is not None and "Slot" in target_kinds:
            local_matches = tuple(
                item
                for item in visible
                if item.module_id == module.module_id
                and item.name == literal
                and item.identifier.startswith(source.identifier + profile.separator)
            )
        matches = local_matches or tuple(
            item for item in visible if item.name == literal
        )
    by_owner: dict[str, QualifiedDeclaration] = {}
    for item in sorted(matches, key=lambda candidate: candidate.identifier):
        owner = next(
            candidate
            for candidate in declarations
            if candidate.identifier == item.authoritative_identifier
        )
        by_owner[owner.identifier] = owner
    all_matches = tuple(by_owner.values())
    valid = tuple(item for item in all_matches if item.kind in target_kinds)
    return all_matches, valid


def _references(
    closure: DeclaredContractClosure,
    declarations: tuple[QualifiedDeclaration, ...],
    reachable: Mapping[str, frozenset[str]],
    profile: _Profile,
) -> tuple[ResolvedReference, ...]:
    modules = {module.module_id: module for module in closure.modules}
    originals = {
        (module.module_id, declaration.identifier): declaration
        for module in closure.modules
        for declaration in module.declarations
    }
    diagnostics: list[BindingDiagnostic] = []
    resolved: list[ResolvedReference] = []
    sources: list[
        tuple[DeclaredModule, QualifiedDeclaration | None, str, AuthoredValue]
    ] = []
    for module in closure.modules:
        if not module.trusted:
            sources.append((module, None, "Module", module.root))
    for declaration in declarations:
        if declaration.trusted:
            continue
        module = modules[declaration.module_id]
        original = originals[(declaration.module_id, declaration.identifier)]
        sources.append((module, declaration, declaration.kind, original.body))

    for module, source, source_kind, value in sources:
        source_id = module.schema_id if source is None else source.identifier
        for site in profile.reference_sites:
            if site.source_kind != source_kind:
                continue
            for literal, path in _raw_references(value, site):
                all_matches, valid = _reference_candidates(
                    literal=literal,
                    source=source,
                    module=module,
                    declarations=declarations,
                    reachable=reachable,
                    target_kinds=site.target_kinds,
                    profile=profile,
                )
                if len(valid) == 1:
                    target = valid[0]
                    resolved.append(
                        ResolvedReference(
                            source_identifier=source_id,
                            source_module_id=module.module_id,
                            path=path,
                            literal=literal,
                            target_identifier=target.identifier,
                            target_kind=target.kind,
                            target_module_id=target.module_id,
                        )
                    )
                    continue
                if len(valid) > 1:
                    reason = BindingRefusalReason.AMBIGUOUS_REFERENCE
                    detail = "reference resolves to multiple authoritative declarations"
                    candidates = tuple(item.identifier for item in valid)
                elif all_matches:
                    reason = BindingRefusalReason.WRONG_REFERENCE_KIND
                    detail = (
                        "reference resolves only to declarations of a forbidden kind"
                    )
                    candidates = tuple(item.identifier for item in all_matches)
                else:
                    reason = BindingRefusalReason.UNKNOWN_REFERENCE
                    detail = "reference has no target in the retained closure or trusted builtins"
                    candidates = ()
                diagnostics.append(
                    _diagnostic(
                        reason,
                        detail,
                        module_id=module.module_id,
                        source_identifier=source_id,
                        path=path,
                        reference=literal,
                        candidates=candidates,
                    )
                )
    if diagnostics:
        raise _refuse(*diagnostics)
    return tuple(
        sorted(
            resolved,
            key=lambda item: (
                item.source_identifier,
                _path_key(item.path),
                item.literal,
                item.target_identifier,
            ),
        )
    )


def bind_contract(closure: DeclaredContractClosure) -> ContractBinding:
    """Bind one exact declared closure or refuse without partial output."""

    profile = _load_profile()
    declared = _validate_input(closure, profile)
    declarations, adoptions, reachable = _qualified(declared, profile)
    references = _references(declared, declarations, reachable, profile)
    return ContractBinding(
        declared_closure=declared,
        declarations=declarations,
        references=references,
        adoptions=adoptions,
        profile_id=profile.profile_id,
        profile_sha256=profile.digest,
    )
