"""Shop-owned JSONL mapping. No history, graph, or admission authority."""

from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import quote

import malleus.compiler as api


MAPPING_BYTES = Path(__file__).with_name("mapping.json").read_bytes()


def canonical(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(content: bytes) -> str:
    return "sha256:" + sha256(content).hexdigest()


class SupplierImportRefusal(ValueError):
    """A supplier-file shape error, not a Core protocol refusal."""

    reason = "MALFORMED_SUPPLIER_ROWS"


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise SupplierImportRefusal(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def adapt_supplier_rows(
    *, source_bytes: bytes, source_id: str, plan_id: str, contract_identity: str
) -> dict:
    """Map all nonempty lines using the exact sibling mapping loaded at import.

    The call performs no I/O. Values are copied, never normalized or inferred.
    Mapping identity is retained in the plan; the coordinator also binds these
    implementation bytes before preparation.
    """
    mapping = json.loads(MAPPING_BYTES)
    try:
        rows = [
            json.loads(line, object_pairs_hook=_unique_object)
            for line in source_bytes.decode("utf-8").splitlines()
            if line.strip()
        ]
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SupplierImportRefusal(f"expected UTF-8 JSONL objects: {error}") from error
    if not rows:
        raise SupplierImportRefusal("supplier file contains no data rows")
    records, derivations, seen = [], [], set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != set(mapping["fields"]):
            raise SupplierImportRefusal(
                f"row {index} requires exactly {sorted(mapping['fields'])}"
            )
        for field, rule in mapping["fields"].items():
            value = row[field]
            if rule == "NONEMPTY_STRING":
                valid = isinstance(value, str) and bool(value.strip())
            elif rule == "NONNEGATIVE_INTEGER":
                valid = type(value) is int and value >= 0
            else:
                raise ValueError(f"unsupported declared mapping rule: {rule}")
            if not valid:
                raise SupplierImportRefusal(
                    f"row {index} field {field} requires {rule}"
                )
        occurrence = row[mapping["identity_field"]]
        if occurrence in seen:
            raise SupplierImportRefusal(f"row {index} repeats occurrence {occurrence}")
        seen.add(occurrence)
        record_id = mapping["record_id_prefix"] + quote(occurrence, safe="")
        records.append(
            {"id": record_id, "type": mapping["record_type"], "properties": row}
        )
        derivations.extend(
            {
                "locator": f"row:{index}:{field}",
                "path": ["properties", field],
                "record_id": record_id,
                "source_id": source_id,
            }
            for field in sorted(row)
        )
    return {
        "adapter": mapping["adapter"],
        "contract_identity": contract_identity,
        "derivations": derivations,
        "evidence": [
            {"evidence_id": mapping["evidence_id"], "sha256": digest(MAPPING_BYTES)}
        ],
        "gaps": [],
        "grammar": mapping["plan_grammar"],
        "history_profile": {
            "profile_id": "state-version",
            "sha256": api.STATE_VERSION_PROFILE.identity,
        },
        "plan_id": plan_id,
        "records": {"entities": records, "relations": []},
        "sources": [{"source_id": source_id, "sha256": digest(source_bytes)}],
        "supersessions": [],
        "valid_time": mapping["valid_time"],
    }
