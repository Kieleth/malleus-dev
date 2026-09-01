from __future__ import annotations


def test_retained_source_boundary_exposes_the_authorized_private_api() -> None:
    from malleus._contract_source import (
        CollaboratorRefusal,
        ImportReader,
        ImportRequest,
        ModuleObservation,
        RefusalReason,
        ResolvedImportEdge,
        ResolvedSource,
        Resolver,
        ResolverSelection,
        RetainedSource,
        RootRequest,
        RootResolution,
        SourceBoundaryRefusal,
        SourceClosure,
        build_source_closure,
    )

    assert all(
        value is not None
        for value in (
            CollaboratorRefusal,
            ImportReader,
            ImportRequest,
            ModuleObservation,
            RefusalReason,
            ResolvedImportEdge,
            ResolvedSource,
            Resolver,
            ResolverSelection,
            RetainedSource,
            RootRequest,
            RootResolution,
            SourceBoundaryRefusal,
            SourceClosure,
            build_source_closure,
        )
    )
