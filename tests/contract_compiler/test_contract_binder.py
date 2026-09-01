"""Fixed tests for private qualified contract binding and composition."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
from hashlib import sha256
from importlib.resources import files
from pathlib import Path

import pytest

import malleus._contract_binder as binder_module
from malleus._contract_binder import (
    BindingRefusal,
    BindingRefusalReason,
    ContractBinding,
    bind_contract,
)
from malleus._contract_linkml_adapter import (
    AuthoredField,
    AuthoredMapping,
    AuthoredScalar,
    AuthoredSequence,
    AuthoredSequenceItem,
    DeclaredContractClosure,
    DeclaredDeclaration,
    DeclaredModule,
    LinkMLImportReader,
    adapt_linkml_closure,
)
from malleus._contract_source import (
    CollaboratorRefusal,
    ImportRequest,
    ModuleObservation,
    RefusalReason,
    ResolvedImportEdge,
    ResolvedSource,
    ResolverSelection,
    RetainedSource,
    RootRequest,
    RootResolution,
    SourceBoundaryRefusal,
    SourceClosure,
    build_source_closure,
)


ROOT = Path(__file__).resolve().parents[2]
BINDER = ROOT / "src/malleus/_contract_binder.py"
PROFILE = ROOT / "src/malleus/_contract_binding_profile.json"
QUIET = ROOT / "conformance/contract_kernel/v0/themed_fixture/sources"
SELECTION = ResolverSelection(
    resolver_id="TEST_ONLY_CLOSED_RESOLVER",
    profile_version="TEST_ONLY_LINKML_V0",
    configuration_id="TEST_ONLY_NO_AMBIENT_IO",
)


def _retained(module_id: str, source: bytes) -> RetainedSource:
    return RetainedSource(
        resolved_locator=module_id,
        source_bytes=source,
        byte_length=len(source),
        sha256=f"sha256:{sha256(source).hexdigest()}",
        media_type="application/yaml",
        resolver_selection=SELECTION,
    )


def _observation(module_id: str, source: bytes) -> ModuleObservation:
    retained = _retained(module_id, source)
    return ModuleObservation(
        module_id=module_id,
        source=retained,
        authored_imports=LinkMLImportReader().read_imports(retained),
    )


def _declared(
    documents: dict[str, bytes],
    *,
    root: str,
    module_order: tuple[str, ...] | None = None,
) -> DeclaredContractClosure:
    observations = {
        module_id: _observation(module_id, source)
        for module_id, source in documents.items()
    }
    edges = tuple(
        ResolvedImportEdge(
            parent_module_id=module_id,
            parent_import_ordinal=ordinal,
            literal_import=literal,
            child_module_id=literal,
            resolver_selection=SELECTION,
        )
        for module_id, observation in observations.items()
        for ordinal, literal in enumerate(observation.authored_imports)
    )
    ordered = module_order or tuple(documents)
    root_source = observations[root].source
    closure = SourceClosure(
        selection=SELECTION,
        root=RootResolution(
            requested_locator=f"request:{root}",
            resolved_locator=root,
            source_sha256=root_source.sha256,
            resolver_selection=SELECTION,
        ),
        modules=tuple(observations[module_id] for module_id in ordered),
        import_edges=edges,
    )
    return adapt_linkml_closure(closure)


def _source(schema_id: str, body: str = "", imports: tuple[str, ...] = ()) -> bytes:
    import_text = ""
    if imports:
        import_text = "imports:\n" + "".join(f"  - {item}\n" for item in imports)
    return (
        f"id: {schema_id}\n"
        f"name: {schema_id.rsplit('/', 1)[-1].replace('-', '_')}\n"
        f"{import_text}{body}"
    ).encode()


def _mapping_field(mapping: AuthoredMapping, name: str) -> AuthoredField:
    return next(field for field in mapping.fields if field.name == name)


def _replace_mapping_field(
    mapping: AuthoredMapping,
    name: str,
    value: AuthoredMapping | AuthoredScalar | AuthoredSequence | None,
) -> AuthoredMapping:
    fields_out: list[AuthoredField] = []
    replaced = False
    for field in mapping.fields:
        if field.name != name:
            fields_out.append(field)
            continue
        replaced = True
        if value is not None:
            fields_out.append(replace(field, value=value))
    if not replaced and value is not None:
        fields_out.append(
            AuthoredField(
                name=name,
                ordinal=len(fields_out),
                classification="IDENTITY_ONLY",
                value=value,
            )
        )
    return AuthoredMapping(tuple(fields_out))


def _replace_declaration_body(
    closure: DeclaredContractClosure,
    *,
    module_id: str,
    name: str,
    body: AuthoredMapping,
) -> DeclaredContractClosure:
    modules: list[DeclaredModule] = []
    for module in closure.modules:
        if module.module_id != module_id:
            modules.append(module)
            continue
        declarations = tuple(
            replace(declaration, body=body) if declaration.name == name else declaration
            for declaration in module.declarations
        )
        modules.append(replace(module, declarations=declarations))
    return replace(closure, modules=tuple(modules))


def _declaration(
    closure: DeclaredContractClosure, module_id: str, name: str
) -> DeclaredDeclaration:
    module = next(item for item in closure.modules if item.module_id == module_id)
    return next(item for item in module.declarations if item.name == name)


def _assert_deeply_immutable(value: object) -> None:
    if is_dataclass(value):
        for field in fields(value):
            _assert_deeply_immutable(getattr(value, field.name))
        return
    if isinstance(value, tuple):
        for item in value:
            _assert_deeply_immutable(item)
        return
    assert value is None or type(value) in {bool, bytes, int, str}


def _reason(closure: object) -> BindingRefusal:
    with pytest.raises(BindingRefusal) as caught:
        bind_contract(closure)  # type: ignore[arg-type]
    return caught.value


def _owner_and_adopter() -> DeclaredContractClosure:
    owner_id = "https://example.test/owner"
    adopter_id = "https://example.test/adopter"
    return _declared(
        {
            adopter_id: _source(
                adopter_id,
                "slots:\n"
                "  shared_value:\n"
                "    annotations:\n"
                "      adopts: true\n"
                "    description: Adopter presentation.\n"
                "    range: string\n"
                "    required: true\n",
                (owner_id,),
            ),
            owner_id: _source(
                owner_id,
                "slots:\n"
                "  shared_value:\n"
                "    description: Owner presentation.\n"
                "    range: string\n"
                "    required: true\n",
            ),
        },
        root=adopter_id,
    )


def test_binding_boundary_is_closed_deeply_immutable_and_atomic() -> None:
    schema_id = "https://example.test/simple"
    declared = _declared(
        {
            schema_id: _source(
                schema_id,
                "slots:\n  value:\n    range: string\n"
                "classes:\n  Record:\n    slots:\n      - value\n",
            )
        },
        root=schema_id,
    )

    result = bind_contract(declared)

    assert type(result) is ContractBinding
    assert result.declared_closure is declared
    _assert_deeply_immutable(result)
    with pytest.raises(FrozenInstanceError):
        result.profile_id = "changed"  # type: ignore[misc]

    malformed = replace(declared, modules=list(declared.modules))  # type: ignore[arg-type]
    refusal = _reason(malformed)
    assert refusal.reason is BindingRefusalReason.MALFORMED_INPUT
    assert refusal.diagnostics == (refusal.diagnostics[0],)
    assert not hasattr(refusal, "partial_result")
    assert declared == result.declared_closure


def test_qualification_reference_resolution_and_trusted_builtins_are_exact() -> None:
    root = "https://example.test/root"
    child = "https://example.test/child"
    declared = _declared(
        {
            root: _source(
                root,
                "types:\n  Count:\n    typeof: integer\n"
                "slots:\n"
                "  local_value:\n    range: Count\n"
                "classes:\n"
                "  RootRecord:\n"
                "    is_a: ChildRecord\n"
                "    slots:\n      - child_value\n      - local_value\n",
                (child,),
            ),
            child: _source(
                child,
                "slots:\n  child_value:\n    range: string\nclasses:\n  ChildRecord:\n",
            ),
        },
        root=root,
    )

    result = bind_contract(declared)

    assert {
        (item.identifier, item.authoritative_identifier, item.kind)
        for item in result.declarations
        if not item.trusted
    } == {
        (f"{root}/Count", f"{root}/Count", "Scalar"),
        (f"{root}/local_value", f"{root}/local_value", "Slot"),
        (f"{root}/RootRecord", f"{root}/RootRecord", "Class"),
        (f"{child}/child_value", f"{child}/child_value", "Slot"),
        (f"{child}/ChildRecord", f"{child}/ChildRecord", "Class"),
    }
    assert {
        (item.source_identifier, item.path, item.literal, item.target_identifier)
        for item in result.references
    } == {
        (f"{root}/Count", ("typeof",), "integer", "urn:malleus:contract-facts/Integer"),
        (f"{root}/local_value", ("range",), "Count", f"{root}/Count"),
        (f"{root}/RootRecord", ("is_a",), "ChildRecord", f"{child}/ChildRecord"),
        (
            f"{root}/RootRecord",
            ("slots", 0),
            "child_value",
            f"{child}/child_value",
        ),
        (
            f"{root}/RootRecord",
            ("slots", 1),
            "local_value",
            f"{root}/local_value",
        ),
        (
            f"{child}/child_value",
            ("range",),
            "string",
            "urn:malleus:contract-facts/String",
        ),
    }
    integer = next(item for item in result.declarations if item.name == "integer")
    assert integer.trusted is True
    assert integer.module_id == "linkml:types"
    assert integer.identifier == "urn:malleus:contract-facts/Integer"


def test_literal_boolean_adoption_keeps_the_imported_owner() -> None:
    closure = _owner_and_adopter()

    result = bind_contract(closure)

    owner = "https://example.test/owner/shared_value"
    adopter = "https://example.test/adopter/shared_value"
    qualified = {item.identifier: item for item in result.declarations}
    assert qualified[owner].authoritative_identifier == owner
    assert qualified[adopter].authoritative_identifier == owner
    assert result.adoptions == (result.adoptions[0],)
    assert result.adoptions[0].adopter_identifier == adopter
    assert result.adoptions[0].owner_identifier == owner
    assert result.adoptions[0].owner_module_id == "https://example.test/owner"


@pytest.mark.parametrize(
    ("mutation", "expected"),
    (
        ("absent-marker", BindingRefusalReason.ADOPTION_REQUIRED),
        ("null-marker", BindingRefusalReason.INVALID_ADOPTION),
        ("false-marker", BindingRefusalReason.INVALID_ADOPTION),
        ("string-true-marker", BindingRefusalReason.INVALID_ADOPTION),
        ("different-value", BindingRefusalReason.ADOPTION_MISMATCH),
        ("different-presence", BindingRefusalReason.ADOPTION_MISMATCH),
        ("different-type", BindingRefusalReason.ADOPTION_MISMATCH),
        ("different-cardinality", BindingRefusalReason.ADOPTION_MISMATCH),
    ),
)
def test_full_explicit_adoption_marker_and_exact_equality_matrix(
    mutation: str, expected: BindingRefusalReason
) -> None:
    closure = _owner_and_adopter()
    module_id = "https://example.test/adopter"
    body = _declaration(closure, module_id, "shared_value").body
    annotations = _mapping_field(body, "annotations").value
    assert isinstance(annotations, AuthoredMapping)

    if mutation == "absent-marker":
        body = _replace_mapping_field(body, "annotations", None)
    elif mutation.endswith("marker"):
        scalar = {
            "null-marker": AuthoredScalar("NULL", "null", None),
            "false-marker": AuthoredScalar("BOOLEAN", "false", False),
            "string-true-marker": AuthoredScalar("STRING", "true", "true"),
        }[mutation]
        body = _replace_mapping_field(
            body,
            "annotations",
            _replace_mapping_field(annotations, "adopts", scalar),
        )
    elif mutation == "different-value":
        body = _replace_mapping_field(
            body, "range", AuthoredScalar("STRING", "integer", "integer")
        )
    elif mutation == "different-presence":
        body = _replace_mapping_field(body, "required", None)
    elif mutation == "different-type":
        body = _replace_mapping_field(
            body, "required", AuthoredScalar("STRING", "true", "true")
        )
    else:
        body = _replace_mapping_field(
            body,
            "range",
            AuthoredSequence(
                (AuthoredSequenceItem(0, AuthoredScalar("STRING", "string", "string")),)
            ),
        )
    closure = _replace_declaration_body(
        closure, module_id=module_id, name="shared_value", body=body
    )

    refusal = _reason(closure)

    assert refusal.reason is expected


def test_non_slot_duplicate_and_multiple_independent_owners_refuse() -> None:
    parent = "https://example.test/parent"
    root = "https://example.test/root"
    duplicate_class = _declared(
        {
            root: _source(root, "classes:\n  Record:\n", (parent,)),
            parent: _source(parent, "classes:\n  Record:\n"),
        },
        root=root,
    )
    assert _reason(duplicate_class).reason is BindingRefusalReason.NON_SLOT_DUPLICATE

    left = "https://example.test/left"
    right = "https://example.test/right"
    multiple = _declared(
        {
            root: _source(root, imports=(left, right)),
            left: _source(left, "slots:\n  value:\n    range: string\n"),
            right: _source(right, "slots:\n  value:\n    range: string\n"),
        },
        root=root,
    )
    assert _reason(multiple).reason is BindingRefusalReason.MULTIPLE_OWNERS


def test_collisions_unknown_ambiguous_and_wrong_kind_references_refuse() -> None:
    root = "https://example.test/root"
    child = "https://example.test/child"
    collision = _declared(
        {
            root: _source(root, imports=(child,)),
            child: _source(root, "classes:\n  Other:\n"),
        },
        root=root,
    )
    assert (
        _reason(collision).reason is BindingRefusalReason.QUALIFIED_IDENTIFIER_COLLISION
    )

    unknown = _declared(
        {root: _source(root, "classes:\n  Record:\n    is_a: Missing\n")},
        root=root,
    )
    assert _reason(unknown).reason is BindingRefusalReason.UNKNOWN_REFERENCE

    left = "https://example.test/left"
    right = "https://example.test/right"
    ambiguous = _declared(
        {
            root: _source(
                root,
                "classes:\n  Root:\n    slots:\n      - value\n",
                (left, right),
            ),
            left: _source(left, "classes:\n  Left:\n    attributes:\n      value:\n"),
            right: _source(
                right, "classes:\n  Right:\n    attributes:\n      value:\n"
            ),
        },
        root=root,
    )
    assert _reason(ambiguous).reason is BindingRefusalReason.AMBIGUOUS_REFERENCE

    wrong_kind = _declared(
        {
            root: _source(
                root,
                "slots:\n  NotAClass:\nclasses:\n  Record:\n    is_a: NotAClass\n",
            )
        },
        root=root,
    )
    assert _reason(wrong_kind).reason is BindingRefusalReason.WRONG_REFERENCE_KIND


def test_builtin_name_collision_refuses_instead_of_shadowing() -> None:
    root = "https://example.test/root"
    closure = _declared(
        {root: _source(root, "types:\n  string:\n    typeof: integer\n")},
        root=root,
    )

    refusal = _reason(closure)

    assert refusal.reason is BindingRefusalReason.BUILTIN_COLLISION


def test_diagnostic_order_ignores_import_module_and_declaration_order() -> None:
    root = "https://example.test/root"
    left = "https://example.test/left"
    right = "https://example.test/right"
    first = _declared(
        {
            root: _source(
                root,
                "classes:\n  Zed:\n    is_a: MissingZ\n  Alpha:\n    is_a: MissingA\n",
                (left, right),
            ),
            left: _source(left),
            right: _source(right),
        },
        root=root,
    )
    second = _declared(
        {
            root: _source(
                root,
                "classes:\n  Alpha:\n    is_a: MissingA\n  Zed:\n    is_a: MissingZ\n",
                (right, left),
            ),
            right: _source(right),
            left: _source(left),
        },
        root=root,
        module_order=(left, root, right),
    )

    left_refusal = _reason(first)
    right_refusal = _reason(second)

    assert left_refusal.diagnostics == right_refusal.diagnostics
    assert tuple(item.reference for item in left_refusal.diagnostics) == (
        "MissingA",
        "MissingZ",
    )


class _QuietResolver:
    def __init__(self) -> None:
        self.requests: list[RootRequest | ImportRequest] = []

    def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
        self.requests.append(request)
        if isinstance(request, RootRequest):
            return ResolvedSource(
                "modules/foundation.yaml",
                (QUIET / "modules/foundation.yaml").read_bytes(),
                "application/yaml",
            )
        if request.literal_import == "linkml:types":
            source = (
                files("linkml_runtime")
                .joinpath("linkml_model", "model", "schema", "types.yaml")
                .read_bytes()
            )
            return ResolvedSource("linkml:types", source, "application/yaml")
        raise CollaboratorRefusal("malleus has no governed retained source")


def test_quiet_bell_missing_import_refuses_before_binder(monkeypatch) -> None:
    resolver = _QuietResolver()
    called = False

    def forbidden(_closure: DeclaredContractClosure) -> ContractBinding:
        nonlocal called
        called = True
        raise AssertionError("binder must not run")

    monkeypatch.setattr(binder_module, "bind_contract", forbidden)

    with pytest.raises(SourceBoundaryRefusal) as caught:
        closure = build_source_closure(
            requested_locator="quiet-bell-root",
            selection=SELECTION,
            resolver=resolver,
            import_reader=LinkMLImportReader(),
        )
        binder_module.bind_contract(adapt_linkml_closure(closure))

    assert caught.value.reason is RefusalReason.RESOLUTION_REFUSED
    assert isinstance(caught.value.request, ImportRequest)
    assert caught.value.request.literal_import == "malleus"
    assert called is False


def test_retained_source_and_adapter_regressions_feed_the_binder_unchanged() -> None:
    schema_id = "https://example.test/regression"
    declared = _declared(
        {schema_id: _source(schema_id, "classes:\n  Record:\n")},
        root=schema_id,
    )

    result = bind_contract(declared)

    assert result.declared_closure is declared
    assert result.declared_closure.source_closure is declared.source_closure
    assert result.declarations[0].source_sha256 == declared.modules[0].source.sha256
    assert result.declarations[0].path == ("classes", "Record")


def test_binder_has_only_its_adjacent_profile_io_and_no_parser_fallback() -> None:
    tree = ast.parse(BINDER.read_text(encoding="utf-8"))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    }
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    } | {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    source = BINDER.read_text(encoding="utf-8")

    assert not {"re", "yaml", "linkml", "linkml_runtime"} & imported
    assert not {"open", "read_text", "resolve", "urlopen"} & calls
    assert source.count("_PROFILE_PATH.read_bytes()") == 1
    assert "OntologyRegistry" not in source
    assert "Quiet Bell" not in source
    assert "Greenhouse" not in source
    assert "Small Shop" not in source
    assert PROFILE.is_file()
