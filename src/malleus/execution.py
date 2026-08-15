"""Generic execution and externally observed outcome contracts."""

from __future__ import annotations

from malleus.ledger import LedgerError, content_digest, require_digest


class ExecutionError(ValueError):
    """An execution or outcome contract field is invalid."""


def outcome_contract_digest(
    *,
    schema_version: str,
    contract_id: str,
    contract_version: str,
    observation_type: str,
    observer_implementation_hash: str,
) -> str:
    """Hash the replay-visible semantics of one external outcome check."""
    if schema_version != "1":
        raise ExecutionError("outcome_contract_schema_version must be '1'")
    for name, value in (
        ("contract_id", contract_id),
        ("contract_version", contract_version),
        ("observation_type", observation_type),
    ):
        if not isinstance(value, str) or not value.strip():
            raise ExecutionError(f"{name} must be a nonblank string")
    try:
        require_digest(
            observer_implementation_hash,
            "observer_implementation_hash",
        )
    except LedgerError as error:
        raise ExecutionError(str(error)) from error
    return content_digest({
        "outcome_contract_schema_version": schema_version,
        "contract_id": contract_id,
        "contract_version": contract_version,
        "observation_type": observation_type,
        "observer_implementation_hash": observer_implementation_hash,
    })
