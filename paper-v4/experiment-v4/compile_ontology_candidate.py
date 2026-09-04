from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

import malleus.compiler as compiler
from malleus.inquisition import validate_pack_grounding


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "producer-input-manifest.json"
SOURCE_TARGETS = {
    "malleus": "inputs/malleus.yaml",
    "linkml:types": "inputs/linkml-types.yaml",
    "metrology": "inputs/metrology.yaml",
    "chronology": "inputs/chronology.yaml",
    "research": "inputs/research.yaml",
}


def _canonical(value: object) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        + b"\n"
    )


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _reason(error: Exception) -> str:
    reason = getattr(error, "reason", None)
    return str(getattr(reason, "name", reason))


def _declared_sources(producer_root: Path) -> dict[str, bytes]:
    manifest = json.loads(MANIFEST.read_bytes())
    by_target = {item["target"]: item for item in manifest["declared_inputs"]}
    sources: dict[str, bytes] = {}
    for locator, target in SOURCE_TARGETS.items():
        item = by_target[target]
        source = (producer_root / target).read_bytes()
        if _digest(source) != item["sha256"]:
            raise ValueError(f"declared compiler input digest mismatch: {target}")
        sources[locator] = source
    return sources


def _population_surface(compilation) -> dict[str, object]:
    view = compilation.view
    record_types: list[dict[str, object]] = []
    for qualified_name in view.type_names():
        definition = view.get_type(qualified_name)
        if definition.abstract or definition.is_mixin:
            continue
        family = (
            "RELATION"
            if view.is_subtype_of(qualified_name, "Relation")
            else "ENTITY"
            if view.is_subtype_of(qualified_name, "Entity")
            else None
        )
        if family is None:
            continue
        slots = []
        for slot_name, constraints in view.effective_slots(qualified_name).items():
            slot = asdict(constraints)
            slot["name"] = slot_name.rsplit("/", 1)[-1]
            slot["qualified_name"] = slot_name
            if view.has_enum(constraints.range_id):
                slot["enum_values"] = sorted(view.get_enum_values(constraints.range_id))
            slots.append(slot)
        record_types.append(
            {
                "family": family,
                "name": qualified_name.rsplit("/", 1)[-1],
                "qualified_name": qualified_name,
                "slots": sorted(slots, key=lambda value: value["qualified_name"]),
            }
        )
    return {
        "schema": "malleus.paper-v4.population-surface/v1",
        "validated_fact_set_sha256": compilation.artifact.validated_fact_set_sha256,
        "record_types": record_types,
    }


def compile_candidate(
    *, ontology_path: Path, producer_root: Path, output: Path, attempt: int
) -> bool:
    ontology = ontology_path.read_bytes()
    output.mkdir(parents=True, exist_ok=False)
    diagnostic: dict[str, object] = {
        "attempt": attempt,
        "ontology_sha256": _digest(ontology),
        "schema": "malleus.paper-v4.ontology-compile-attempt/v1",
    }
    try:
        sources = _declared_sources(producer_root)
        grounding = validate_pack_grounding(ontology, role="PROJECT")
        compilation = compiler.compile_linkml_contract(
            root_locator="paper-v4-project",
            sources={"paper-v4-project": ontology, **sources},
        )
    except (OSError, TypeError, ValueError) as error:
        diagnostic.update(
            {
                "detail": str(error),
                "error_type": type(error).__name__,
                "reason": _reason(error),
                "stage": (
                    "PACK_GROUNDING"
                    if type(error).__module__.endswith("pack_grounding")
                    else "CONTRACT_COMPILATION"
                ),
                "status": "REFUSED",
            }
        )
        (output / "diagnostic.json").write_bytes(_canonical(diagnostic))
        return False

    grounding_bytes = grounding.canonical_bytes + b"\n"
    contract_bytes = compilation.artifact.artifact_bytes
    surface_bytes = _canonical(_population_surface(compilation))
    diagnostic.update(
        {
            "fact_count": compilation.artifact.fact_count,
            "grounding_receipt_sha256": _digest(grounding_bytes),
            "population_surface_sha256": _digest(surface_bytes),
            "stage": "COMPLETE",
            "status": "ACCEPTED",
            "validated_contract_sha256": _digest(contract_bytes),
            "validated_fact_set_sha256": (
                compilation.artifact.validated_fact_set_sha256
            ),
        }
    )
    (output / "grounding-receipt.json").write_bytes(grounding_bytes)
    (output / "population-surface.json").write_bytes(surface_bytes)
    (output / "validated-contract.json").write_bytes(contract_bytes)
    (output / "diagnostic.json").write_bytes(_canonical(diagnostic))
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ontology", type=Path, required=True)
    parser.add_argument("--producer-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--attempt", type=int, required=True)
    args = parser.parse_args(argv)
    accepted = compile_candidate(
        ontology_path=args.ontology,
        producer_root=args.producer_root,
        output=args.output,
        attempt=args.attempt,
    )
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
