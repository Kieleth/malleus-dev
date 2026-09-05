"""The run-13 ontology gate the parent runs between producer attempts.

The compiler sources come from the producer workspace and are checked against
run-13's own frozen manifest. Refusals are written through unchanged: ``detail``
is the exception's own text, so the aggregated grounding diagnostic reaches the
producer with its complete sorted defect set, not one subject at a time.

A refusal also records ``cause_chain``, every link of the raised error's
``__cause__`` chain with its reason and its detail. The diagnostic file is the
artifact returned to the producer, so a refusal whose sentence lives in a
chained cause is complete in the file rather than recoverable from two others
(deep sweep D-14, run-05's attempt 01).

The population surface is at ``/v2``. Run-02's ``/v1`` surface classed a record
type as ``RELATION`` or ``ENTITY`` and dropped everything else, so the Event
subclass the accepted ontology declared never reached the producer and seven
assertions became ``TYPE_ABSENT`` gaps (E-0122 finding 3). The surface now
carries every concrete type that subtypes the Malleus ``Event`` root, and
``EventParticipation`` types when the compiled contract declares that type, and
it states which families the bound history profile admits.
"""

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
PROFILE_TARGET = "inputs/profile-source-assertion.json"
SURFACE_SCHEMA = "malleus.paper-v4.population-surface/v2"

# Core's own record-family order (``kg.RECORD_FAMILIES``), minus the families no
# document capture may carry. The surface reports admission in this order rather
# than alphabetically, so it reads the way the plan compiler applies operations.
FAMILY_ORDER = ("entities", "events", "event_participations", "relations")

# The population family each root ancestor gives a concrete type, in the order
# the surface tests them. ``is_subtype_of`` answers False for an ancestor the
# compiled contract does not declare, so the EventParticipation branch is inert
# unless that type is present. Signal reaches no branch: it has no population
# family and is left out of the surface.
FAMILY_BY_ROOT = (
    ("Relation", "RELATION"),
    ("EventParticipation", "EVENT_PARTICIPATION"),
    ("Event", "EVENT"),
    ("Entity", "ENTITY"),
)


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


def _reason(error: BaseException) -> str:
    reason = getattr(error, "reason", None)
    return str(getattr(reason, "name", reason))


def _cause_chain(error: BaseException) -> list[dict[str, str]]:
    """Every link of the raised error's ``__cause__`` chain, head first.

    Run-05's attempt 01 refused with ``IMPORT_READER_REFUSED`` and nothing else;
    the sentence that named the offending field lived in the chained cause and
    had to be recovered from two other files after the fact (deep sweep D-14).
    The diagnostic file is the artifact returned to the producer, so the chain
    is recorded in it rather than beside it.
    """
    chain: list[dict[str, str]] = []
    seen: set[int] = set()
    link: BaseException | None = error
    while link is not None and id(link) not in seen:
        seen.add(id(link))
        chain.append(
            {
                "detail": str(link),
                "error_type": type(link).__name__,
                "reason": _reason(link),
            }
        )
        link = link.__cause__
    return chain


def _declared(target: str, producer_root: Path) -> bytes:
    manifest = json.loads(MANIFEST.read_bytes())
    item = next(
        entry for entry in manifest["declared_inputs"] if entry["target"] == target
    )
    source = (producer_root / target).read_bytes()
    if _digest(source) != item["sha256"]:
        raise ValueError(f"declared input digest mismatch: {target}")
    return source


def _declared_sources(producer_root: Path) -> dict[str, bytes]:
    return {
        locator: _declared(target, producer_root)
        for locator, target in SOURCE_TARGETS.items()
    }


def _families_admitted(view, profile: dict[str, object]) -> list[str]:
    """The record families the bound history profile admits, in Core's order.

    This mirrors the plan compiler: a profile whose Event ontology role is
    nonempty admits ``events``, and ``event_participations`` on top of that only
    when the compiled contract declares an ``EventParticipation`` type.
    """
    admitted = {"entities", "relations"}
    if profile["ontology_roles"]["event"]:
        admitted.add("events")
        if view.has_type("EventParticipation"):
            admitted.add("event_participations")
    return [family for family in FAMILY_ORDER if family in admitted]


def _family(view, qualified_name: str) -> str | None:
    for ancestor, family in FAMILY_BY_ROOT:
        if view.is_subtype_of(qualified_name, ancestor):
            return family
    return None


def _population_surface(compilation, profile: dict[str, object]) -> dict[str, object]:
    view = compilation.view
    record_types: list[dict[str, object]] = []
    for qualified_name in view.type_names():
        definition = view.get_type(qualified_name)
        if definition.abstract or definition.is_mixin:
            continue
        family = _family(view, qualified_name)
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
        "schema": SURFACE_SCHEMA,
        "families_admitted": _families_admitted(view, profile),
        "history_profile_id": profile["profile_id"],
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
        profile = json.loads(_declared(PROFILE_TARGET, producer_root))
        grounding = validate_pack_grounding(ontology, role="PROJECT")
        compilation = compiler.compile_linkml_contract(
            root_locator="paper-v4-project",
            sources={"paper-v4-project": ontology, **sources},
        )
    except (OSError, TypeError, ValueError) as error:
        chain = _cause_chain(error)
        diagnostic.update(
            {
                "cause_chain": chain,
                "chained_cause": (
                    None if len(chain) == 1 else "; ".join(
                        f"{link['reason']}: {link['detail']}" for link in chain[1:]
                    )
                ),
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
    surface = _population_surface(compilation, profile)
    surface_bytes = _canonical(surface)
    diagnostic.update(
        {
            "fact_count": compilation.artifact.fact_count,
            "families_admitted": surface["families_admitted"],
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
