"""The obligation grammar, its freeze check, and the binding step.

An obligation is one declared interpretation that must be reviewed exactly once
at a declared boundary, with one of the four declared outcomes. It says what must be
looked at again and in what vocabulary; it never says what the answer is.

``load_frozen`` reads a boundary's obligations back against the freeze record
that names their digests and refuses on drift. ``bind`` maps them onto the
producer's own record ids and writes the boundary declaration
``malleus.acquisition.check_review_coverage`` consumes, with the identity
Core computes for it beside the boundary and never inside it, so adding the
identity cannot change the bytes it identifies.

**The selector is the adapter's.** Both consumers select records by type and
role and never by identifier, but the two grammars have nothing in common: one
declares event and entity types and matches an export's own type strings; the
other declares pack types and walks the compiled contract for a subtype or a
mixin, then filters by reading block, unit and slot. So ``bind`` takes a
``select`` callable and an ``obligations`` list and knows neither grammar.

**An obligation that binds nothing is still an obligation.** The producer
reviews it and may answer that the matter is unresolved. That is why the
boundary carries every interpretation whatever the binding found.
"""

from __future__ import annotations

import json

from .adapter import EXPORT_GROUPS, BOUNDARY_GRAMMAR
from .digests import canonical, digest, reference


class BindingRefusal(ValueError):
    """The frozen bytes moved, or the export is not a graph export."""


def freeze_record(body, obligations, *, schema, path):
    """The record that holds one boundary's frozen bytes to their digests."""
    return {
        "schema": schema,
        "frozen_before": "ANY_MODEL_OUTPUT_EXISTS",
        "sha256": digest(body),
        "path": path,
        "obligations": [
            {"id": item["id"], "sha256": digest(canonical(item))}
            for item in obligations
        ],
    }


def load_frozen(body, record, *, per_obligation=False):
    """One boundary's obligations, checked against the record that froze them.

    ``per_obligation`` additionally checks each obligation's own digest, which
    is what catches an edit that leaves the body's own digest re-computed.
    """
    if digest(body) != record["sha256"]:
        raise BindingRefusal(
            f"the frozen obligations are {digest(body)}, not the bytes they"
            f" declare, {record['sha256']}"
        )
    declared = json.loads(body)
    if per_obligation:
        recorded = {item["id"]: item["sha256"] for item in record["obligations"]}
        for item in declared["obligations"]:
            if digest(canonical(item)) != recorded.get(item["id"]):
                raise BindingRefusal(f"{item['id']} is not the bytes it declares")
    return declared


def check_export(export, *, forbidden_record_ids=(), noun="a withheld record"):
    """The export's own shape, and that it carries none of the withheld ids."""
    if not isinstance(export, dict) or set(export) != set(EXPORT_GROUPS):
        raise BindingRefusal(
            f"not a graph export: expected exactly {', '.join(EXPORT_GROUPS)}"
        )
    for group in EXPORT_GROUPS:
        if not isinstance(export[group], list):
            raise BindingRefusal(f"{group} is not a list of records")
        for item in export[group]:
            if item.get("id") in tuple(forbidden_record_ids):
                raise BindingRefusal(f"the export carries {noun} {item['id']}")


def records_by_id(export):
    """Every record of an export, by id, for the dependency references."""
    return {
        item["id"]: item
        for group in EXPORT_GROUPS
        for item in export[group]
        if isinstance(item, dict) and "id" in item
    }


def bind(
    export,
    knowledge,
    *,
    declared,
    select,
    evidence,
    ontology,
    boundary_schema=None,
    bound_schema,
    binding_extras=(),
    result_extras=None,
    carry_identity=True,
):
    """Map every obligation onto the producer's own record ids.

    ``declared`` is the loaded obligation declaration; ``select`` takes one
    obligation's ``subject`` and returns the sorted record ids it binds.
    ``knowledge`` is the reference the producer's replay receipt or export
    digest gives, pinned so the boundary names the knowledge position it was
    declared at. ``binding_extras`` names obligation fields to copy into each
    binding, which is how a consumer hands the producer the question in words
    beside the ids.

    ``carry_identity=False`` reproduces a boundary frozen before the identity
    was carried beside it, and is used for nothing else.
    """
    by_id = records_by_id(export)
    bindings, dependencies, interpretations = [], {}, []
    for item in declared["obligations"]:
        found = select(item["subject"])
        bindings.append(
            {
                "obligation": item["id"],
                "subject": item["subject"],
                **{key: item[key] for key in binding_extras},
                "records": found,
                "matched": len(found),
                "must_review": True,
                "may_answer": list(item["permitted_outcomes"]),
            }
        )
        for identifier in found:
            dependencies[identifier] = reference(
                identifier, canonical(by_id[identifier])
            )
        interpretations.append(reference(item["id"], canonical(item)))
    boundary = {
        "schema": boundary_schema or BOUNDARY_GRAMMAR,
        "id": declared["boundary_id"],
        "evidence": list(evidence),
        "ontology": ontology,
        "knowledge": knowledge,
        "dependencies": [dependencies[key] for key in sorted(dependencies)],
        "interpretations": interpretations,
    }
    result = {
        "schema": bound_schema,
        "boundary": boundary,
        "bindings": bindings,
        "note": "An obligation that bound no record is still reviewed. UNRESOLVED"
        " is a complete review outcome, not a failure to answer.",
        **(result_extras or {}),
    }
    if carry_identity:
        from malleus.acquisition import review_boundary_identity

        result["boundary_identity"] = review_boundary_identity(
            boundary_bytes=canonical(boundary)
        )
    return result
