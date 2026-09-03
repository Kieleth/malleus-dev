"""Manifest-driven paper-v4 document runs for several proposal producers.

One run manifest names every frozen coordinate of one document experiment: the
selected ontology, the constructible record types the query binding closes over,
the generic recipes derived from them, the population, and the identities the
v2 driver hard-codes. The v2 run is expressed as one such manifest so that this
module can be proven to reproduce its bytes before any other producer is run.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Sequence

import yaml

from .compiled_graph_recipe_contract import derive_compiled_logical_contract
from .experiment_run import PaperExperimentConfiguration
from .frozen_experiment import FrozenExperimentPaths, run_frozen_experiment
from .ontology_compile import ExactSource, compile_exact_ontology
from .population_acquisition import (
    PopulationCandidateKind,
    classify_population_candidate,
)
from .population_compile import PopulationRecipeProfile
from .query_replay import run_query_replay, write_query_result


MANIFEST_SCHEMA = "malleus.paper-v4.multimodel-run-manifest/v1"
_TEMPLATE_VERSION = "-1.0.0"
_NUMERIC_RANGES = {"integer", "float", "double", "decimal"}
_BASE_TEMPLATES = """\
mgrp:Record [
  ! ottr:IRI ?member,
  ! ottr:IRI ?operationKind,
  ! ottr:IRI ?recordType,
  ! xsd:string ?recordId
] :: BASE .

mgrp:Property [
  ! ottr:IRI ?member,
  ! ottr:IRI ?property,
  ?value
] :: BASE .

mgrp:RelationSource [
  ! ottr:IRI ?member,
  ! xsd:string ?recordId
] :: BASE .

mgrp:RelationTarget [
  ! ottr:IRI ?member,
  ! xsd:string ?recordId
] :: BASE .

mgrp:DependsOn [
  ! ottr:IRI ?member,
  ! ottr:IRI ?prerequisiteMember
] :: BASE .
"""


class MultimodelRefusal(ValueError):
    """A manifest coordinate is missing, malformed, or contradicts its bytes."""


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(item.title() for item in tail)


# --- ontology structure -----------------------------------------------------


def load_ontology(source: bytes) -> dict[str, Any]:
    """Parse the selected ontology YAML; the compiler remains the validity gate."""

    document = yaml.safe_load(source)
    if type(document) is not dict or "classes" not in document:
        raise MultimodelRefusal("ontology must be one YAML mapping with classes")
    return document


def domain_iri(ontology: dict[str, Any]) -> str:
    """LinkML expands class names under the schema id when no default prefix exists."""

    schema_id = ontology.get("id")
    if type(schema_id) is not str or not schema_id.strip():
        raise MultimodelRefusal("ontology id must be nonblank text")
    return schema_id if schema_id.endswith(("/", "#")) else schema_id + "/"


def domain_prefix(ontology: dict[str, Any]) -> str:
    """The prefix the ontology itself declares for its own namespace."""

    expansion = domain_iri(ontology)
    prefixes = ontology.get("prefixes") or {}
    matches = [
        name
        for name, value in prefixes.items()
        if (value if type(value) is str else (value or {}).get("prefix_reference"))
        == expansion
    ]
    if len(matches) > 1:
        raise MultimodelRefusal(
            f"ontology declares several prefixes for {expansion}: {matches}"
        )
    return matches[0] if matches else "domain"


def class_chain(ontology: dict[str, Any], name: str) -> list[str]:
    """The class followed by its is_a ancestors inside the ontology."""

    classes = ontology["classes"]
    chain: list[str] = []
    current: str | None = name
    while current is not None and current in classes:
        if current in chain:
            raise MultimodelRefusal(f"is_a cycle at {current}")
        chain.append(current)
        current = (classes[current] or {}).get("is_a")
    return chain


def declared_slot_order(ontology: dict[str, Any], name: str) -> list[str]:
    """Own slots in declaration order, then inherited ones, each once."""

    order: list[str] = []
    for cls in class_chain(ontology, name):
        for slot in (ontology["classes"][cls] or {}).get("slots") or []:
            if slot not in order:
                order.append(slot)
    return order


def slot_range(ontology: dict[str, Any], class_name: str, slot: str) -> str | None:
    for cls in class_chain(ontology, class_name):
        usage = ((ontology["classes"][cls] or {}).get("slot_usage") or {}).get(slot)
        if usage and usage.get("range"):
            return usage["range"]
    declared = (ontology.get("slots") or {}).get(slot) or {}
    return declared.get("range")


def is_relation(record: Any) -> bool:
    """The compiled contract, not the domain YAML, knows the imported roots."""

    return record.role == "RELATION"


def population_properties(
    ontology: dict[str, Any], record: Any, class_name: str
) -> list[str]:
    """Required population properties: ``name`` first, then declaration order."""

    required = {
        slot.runtime_symbol
        for slot in record.operation_properties
        if slot.constraints.required and slot.constraints.equals_string is None
    }
    ordered = ["name"] if "name" in required else []
    for slot in declared_slot_order(ontology, class_name):
        if slot in required and slot not in ordered:
            ordered.append(slot)
    missing = required - set(ordered)
    if missing:
        raise MultimodelRefusal(
            f"{class_name} requires undeclared population properties {sorted(missing)}"
        )
    return ordered


def relation_type_value(record: Any) -> str:
    for slot in record.operation_properties:
        if slot.runtime_symbol == "relation_type":
            if slot.constraints.equals_string is None:
                raise MultimodelRefusal(
                    f"{record.runtime_symbol} does not fix relation_type"
                )
            return slot.constraints.equals_string
    raise MultimodelRefusal(f"{record.runtime_symbol} has no relation_type slot")


# --- derived artifacts ------------------------------------------------------


def binding_closure(binding: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Entity and relation record types the binding names, in first appearance."""

    entities: list[str] = []
    relations: list[str] = []
    for query in binding["queries"]:
        for case in query["cases"]:
            for name in (case["source_record_type"], case["target_record_type"]):
                if name not in entities:
                    entities.append(name)
            if case["relation_record_type"] not in relations:
                relations.append(case["relation_record_type"])
    return entities, relations


def contract_only_types(
    ontology: dict[str, Any], constructible: Sequence[str]
) -> list[str]:
    """Abstract classes that constructible types reach through slot ranges."""

    classes = ontology["classes"]
    selected = list(constructible)
    extra: list[str] = []
    frontier = list(selected)
    while frontier:
        name = frontier.pop(0)
        for cls in class_chain(ontology, name):
            usages = (classes[cls] or {}).get("slot_usage") or {}
            slots = list(usages) + list((classes[cls] or {}).get("slots") or [])
            for slot in slots:
                rng = slot_range(ontology, name, slot)
                if rng in classes and rng not in selected and rng not in extra:
                    extra.append(rng)
                    frontier.append(rng)
    return extra


def recipe_document(
    ontology: dict[str, Any],
    logical_contract: Any,
    constructible: Sequence[str],
    *,
    recipe_namespace: str,
) -> bytes:
    """Value-generic construction templates in the exact v2 layout."""

    prefix = domain_prefix(ontology)
    lines = [
        "@prefix mgrp: <https://malleus.dev/graph-recipe/base/> .",
        "@prefix ottr: <http://ns.ottr.xyz/0.4/> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix malleus: <https://malleus.dev/schema/> .",
        f"@prefix {prefix}: <{domain_iri(ontology)}> .",
        f"@prefix recipe: <{recipe_namespace}> .",
        "",
        _BASE_TEMPLATES,
    ]
    for name in constructible:
        record = logical_contract.record_for_symbol(name)
        head = f"recipe:{name}{_TEMPLATE_VERSION} ["
        if is_relation(record):
            params = [
                "! ottr:IRI ?member",
                "! xsd:string ?recordId",
                "! ottr:IRI ?sourceMember",
                "! xsd:string ?sourceId",
                "! ottr:IRI ?targetMember",
                "! xsd:string ?targetId",
            ]
            body = [
                f"mgrp:Record(?member, mgrp:CreateRelation, {prefix}:{name}, ?recordId)",
                f'mgrp:Property(?member, malleus:relation_type, "{relation_type_value(record)}")',
                "mgrp:RelationSource(?member, ?sourceId)",
                "mgrp:RelationTarget(?member, ?targetId)",
                "mgrp:DependsOn(?member, ?sourceMember)",
                "mgrp:DependsOn(?member, ?targetMember)",
            ]
        else:
            params = ["! ottr:IRI ?member", "! xsd:string ?recordId"]
            body = [
                f"mgrp:Record(?member, mgrp:CreateEntity, {prefix}:{name}, ?recordId)"
            ]
            for slot in population_properties(ontology, record, name):
                typed = (
                    "" if slot_range(ontology, name, slot) in _NUMERIC_RANGES
                    else "xsd:string "
                )
                params.append(f"! {typed}?{_camel(slot)}")
                owner = "malleus" if slot == "name" else prefix
                body.append(f"mgrp:Property(?member, {owner}:{slot}, ?{_camel(slot)})")
        lines.append(head)
        lines.append(",\n".join("  " + item for item in params))
        lines.append("] :: {")
        lines.append(",\n".join("  " + item for item in body))
        lines.append("} .")
        lines.append("")
    return ("\n".join(lines).rstrip("\n") + "\n").encode("utf-8")


def _endpoint_text(
    ontology: dict[str, Any], constructible_entities: Sequence[str], rng: str
) -> str:
    if rng in constructible_entities:
        return f"`{rng}`"
    descendants = [
        name
        for name in constructible_entities
        if rng in class_chain(ontology, name)
    ]
    if descendants == list(constructible_entities):
        return "any constructible entity"
    if not descendants:
        raise MultimodelRefusal(f"endpoint range {rng} has no constructible type")
    return " or ".join(f"`{name}`" for name in descendants)


def population_brief_sections(
    ontology: dict[str, Any],
    logical_contract: Any,
    entities: Sequence[str],
    relations: Sequence[str],
    *,
    root_ontology: dict[str, Any] | None = None,
) -> str:
    """The two constructible-type lists of the population brief.

    A required property whose enum is declared only in the imported root
    ontology gets one extra line naming its permissible values, because the
    population producer does not receive the root file.
    """

    lines = ["## Constructible entity types", ""]
    root_enum_lines: list[str] = []
    for name in entities:
        record = logical_contract.record_for_symbol(name)
        props = population_properties(ontology, record, name)
        lines.append(f"- `{name}`: " + ", ".join(f"`{slot}`" for slot in props))
        for slot in props:
            if slot in (ontology.get("slots") or {}) or slot_range(ontology, name, slot):
                continue
            root_slots = (root_ontology or {}).get("slots") or {}
            root_enums = (root_ontology or {}).get("enums") or {}
            rng = (root_slots.get(slot) or {}).get("range")
            if rng in root_enums:
                values = ", ".join(f"`{v}`" for v in root_enums[rng]["permissible_values"])
                line = f"- `{slot}` is the imported Malleus root slot; its permissible values are {values}."
                if line not in root_enum_lines:
                    root_enum_lines.append(line)
    lines += root_enum_lines
    lines += ["", "## Constructible relation types", ""]
    for name in relations:
        source = _endpoint_text(ontology, entities, slot_range(ontology, name, "source_id"))
        target = _endpoint_text(ontology, entities, slot_range(ontology, name, "target_id"))
        lines.append(f"- `{name}`: source {source}, target {target}")
    return "\n".join(lines) + "\n"


# --- acquisition staging ----------------------------------------------------

BEGIN_ONTOLOGY = "BEGIN_ONTOLOGY_YAML"
END_ONTOLOGY = "END_ONTOLOGY_YAML"
ACCEPTANCE_SCHEMA = "malleus.paper-v4.ontology-decision/v1"
EVALUATOR_ACTOR_ID = "actor:paper-v4-evaluator"


def extract_delimited(report: str, begin: str, end: str) -> bytes:
    """The producer's document between two marker lines, with one trailing newline."""

    def is_marker(line: str, marker: str) -> bool:
        return line.strip().strip("`") == marker

    lines = report.splitlines()
    starts = [i for i, line in enumerate(lines) if is_marker(line, begin)]
    ends = [i for i, line in enumerate(lines) if is_marker(line, end)]
    if len(starts) != 1 or len(ends) != 1 or ends[0] <= starts[0]:
        raise MultimodelRefusal(
            f"report must contain exactly one {begin} ... {end} block, "
            f"found {len(starts)} and {len(ends)}"
        )
    body = "\n".join(lines[starts[0] + 1 : ends[0]]).strip("\n")
    if not body:
        raise MultimodelRefusal("delimited block is empty")
    return (body + "\n").encode("utf-8")


def acceptance_event(ontology_sha256: str, *, ordinal: int = 1) -> bytes:
    """One recorded evaluator acceptance of a compiled ontology digest."""

    from malleus.ledger import canonical_json

    return (
        canonical_json(
            {
                "actor_id": EVALUATOR_ACTOR_ID,
                "decision": "ACCEPT_FOR_POPULATION",
                "event_type": "ONTOLOGY_DECISION",
                "ontology_sha256": ontology_sha256,
                "ordinal": ordinal,
                "schema": ACCEPTANCE_SCHEMA,
            }
        )
        + "\n"
    ).encode("utf-8")


def render_population_brief(
    template: str,
    *,
    ontology_sha256: str,
    reading_path: str,
    sections: str,
    write_tool: str = "`apply_patch`",
) -> bytes:
    """The v2 population brief with only its ontology-specific parts replaced.

    ``write_tool`` names the harness facility that creates ``population.json``;
    the v2 producer had ``apply_patch``, a Claude Code producer has the Write tool.
    """

    lines = [
        line.replace("Use `apply_patch` to create it.", f"Use {write_tool} to create it.")
        for line in template.splitlines()
    ]
    fixed = [line for line in lines if line.startswith("Every enum-valued property")]
    if len(fixed) != 1:
        raise MultimodelRefusal("template must carry exactly one enum-value paragraph")
    head, sep, tail = sections.partition("## Constructible relation types")
    if not sep:
        raise MultimodelRefusal("sections must contain both constructible headers")
    spliced = head + fixed[0] + "\n\n" + sep + tail
    start = next(i for i, line in enumerate(lines) if line == "## Constructible entity types")
    end = next(
        i for i, line in enumerate(lines)
        if line.startswith("Every relation has an empty `properties` object")
    )
    out: list[str] = []
    for i, line in enumerate(lines[:start]):
        if line.endswith("selected-reading.json`") and line.lstrip().startswith("5. `"):
            line = f"5. `{reading_path}`"
        if line.startswith("- `ontology_sha256`: exactly `"):
            line = f"- `ontology_sha256`: exactly `{ontology_sha256}`"
        out.append(line)
    out.extend(spliced.rstrip("\n").splitlines())
    out.append("")
    out.extend(lines[end:])
    return ("\n".join(out) + "\n").encode("utf-8")


# --- manifest and run -------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RunManifest:
    """Every coordinate of one document run, all paths relative to the repo root."""

    run_id: str
    root_locator: str
    contract_id: str
    recipe_namespace: str
    member_namespace: str
    entity_types: tuple[str, ...]
    relation_types: tuple[str, ...]
    contract_only_types: tuple[str, ...]
    paths: dict[str, str]
    sha256: dict[str, str]

    @classmethod
    def load(cls, path: Path) -> "RunManifest":
        try:
            raw = json.loads(path.read_bytes())
        except (OSError, ValueError) as error:
            raise MultimodelRefusal(f"cannot read run manifest {path}: {error}") from error
        if raw.get("schema") != MANIFEST_SCHEMA:
            raise MultimodelRefusal("run manifest schema differs")
        expected = {
            "schema", "run_id", "root_locator", "contract_id", "recipe_namespace",
            "member_namespace", "entity_types", "relation_types",
            "contract_only_types", "paths", "sha256",
        }
        if set(raw) != expected:
            raise MultimodelRefusal(
                f"run manifest fields differ: {sorted(set(raw) ^ expected)}"
            )
        roles = {
            "source", "ontology", "malleus", "linkml", "reading", "population",
            "recipes", "acceptance", "machine", "binding",
        }
        if set(raw["paths"]) != roles or set(raw["sha256"]) != roles:
            raise MultimodelRefusal("run manifest paths and sha256 must cover every role")
        return cls(
            run_id=raw["run_id"],
            root_locator=raw["root_locator"],
            contract_id=raw["contract_id"],
            recipe_namespace=raw["recipe_namespace"],
            member_namespace=raw["member_namespace"],
            entity_types=tuple(raw["entity_types"]),
            relation_types=tuple(raw["relation_types"]),
            contract_only_types=tuple(raw["contract_only_types"]),
            paths=dict(raw["paths"]),
            sha256=dict(raw["sha256"]),
        )

    @property
    def constructible(self) -> tuple[str, ...]:
        return (*self.entity_types, *self.relation_types)


def _read_exact(root: Path, manifest: RunManifest, role: str) -> bytes:
    path = root / manifest.paths[role]
    try:
        source = path.read_bytes()
    except OSError as error:
        raise MultimodelRefusal(f"cannot read {role} at {path}: {error}") from error
    if _digest(source) != manifest.sha256[role]:
        raise MultimodelRefusal(
            f"{role} drifted: expected {manifest.sha256[role]}, observed {_digest(source)}"
        )
    return source


def recipe_profile(manifest: RunManifest) -> PopulationRecipeProfile:
    return PopulationRecipeProfile(
        population_schema="malleus.paper-v4.population/v2",
        selected_reading_schema="malleus.paper-v4.text-layer-reading/v1",
        provenance_schema="malleus.paper-v4.population-provenance/v2",
        graph_recipe_profile_iri="https://malleus.dev/graph-recipe/profile/v0",
        recipe_namespace=manifest.recipe_namespace,
        member_namespace=manifest.member_namespace,
        record_type_templates=tuple(
            (name, name + _TEMPLATE_VERSION) for name in manifest.constructible
        ),
    )


def configuration(
    manifest: RunManifest, domain: str, transaction_time: str
) -> PaperExperimentConfiguration:
    return PaperExperimentConfiguration(
        result_schema="malleus.paper-v4.knowledge-build-result/v2",
        source_sha256=manifest.sha256["source"],
        ontology_sha256=manifest.sha256["ontology"],
        reading_sha256=manifest.sha256["reading"],
        malleus_import_sha256=manifest.sha256["malleus"],
        linkml_types_sha256=manifest.sha256["linkml"],
        population_sha256=manifest.sha256["population"],
        generic_recipe_sha256=manifest.sha256["recipes"],
        ontology_acceptance_sha256=manifest.sha256["acceptance"],
        protocol_machine_sha256=manifest.sha256["machine"],
        population_recipe_profile=recipe_profile(manifest),
        record_type_iris=tuple(
            domain + name
            for name in (*manifest.constructible, *manifest.contract_only_types)
        ),
        contract_id=manifest.contract_id,
        transaction_time=transaction_time,
        ontology_locator=manifest.root_locator,
        malleus_import_locator="malleus",
        linkml_types_locator="linkml:types",
    )


def compile_manifest_ontology(root: Path, manifest: RunManifest):
    """Compile the frozen ontology and derive its logical contract."""

    ontology_bytes = _read_exact(root, manifest, "ontology")
    ontology = load_ontology(ontology_bytes)
    domain = domain_iri(ontology)
    result = compile_exact_ontology(
        root=ExactSource(manifest.root_locator, ontology_bytes, manifest.sha256["ontology"]),
        malleus=ExactSource("malleus", _read_exact(root, manifest, "malleus"), manifest.sha256["malleus"]),
        linkml_types=ExactSource("linkml:types", _read_exact(root, manifest, "linkml"), manifest.sha256["linkml"]),
    )
    contract = derive_compiled_logical_contract(
        result.compilation,
        record_type_iris=tuple(
            domain + name
            for name in (*manifest.constructible, *manifest.contract_only_types)
        ),
        contract_id=manifest.contract_id,
    )
    return ontology, domain, result, contract


def derive_run_artifacts(root: Path, manifest: RunManifest) -> dict[str, bytes]:
    """Recipes and brief sections implied by the manifest's ontology and types."""

    ontology, _, _, contract = compile_manifest_ontology(root, manifest)
    root_ontology = yaml.safe_load(_read_exact(root, manifest, "malleus"))
    return {
        "recipes": recipe_document(
            ontology, contract, manifest.constructible,
            recipe_namespace=manifest.recipe_namespace,
        ),
        "brief_sections": population_brief_sections(
            ontology, contract, manifest.entity_types, manifest.relation_types,
            root_ontology=root_ontology,
        ).encode("utf-8"),
    }


def run_manifest_experiment(
    root: Path,
    manifest_path: Path,
    *,
    private_run_dir: Path,
    results_dir: Path,
    transaction_time: str,
) -> bytes:
    """Build, admit, replay and query one manifest's run; return query result bytes."""

    manifest = RunManifest.load(manifest_path)
    ontology, domain, _, _ = compile_manifest_ontology(root, manifest)
    derived = derive_run_artifacts(root, manifest)
    if derived["recipes"] != _read_exact(root, manifest, "recipes"):
        raise MultimodelRefusal("frozen recipes differ from those derived from the ontology")
    population = _read_exact(root, manifest, "population")
    kind = classify_population_candidate(
        population,
        success_schema="malleus.paper-v4.population/v2",
        refusal_schema="malleus.paper-v4.population-refusal/v2",
        record_id_prefix="urn:malleus:paper-v4:v2:record:",
        ordinal_width=3,
    )
    if kind is PopulationCandidateKind.MODEL_REFUSAL:
        raise MultimodelRefusal("model population refusal is terminal")
    binding = _read_exact(root, manifest, "binding")
    for role in ("reading", "acceptance", "machine", "source"):
        _read_exact(root, manifest, role)
    paths = {role: root / rel for role, rel in manifest.paths.items()}
    inputs = FrozenExperimentPaths(
        selected_ontology=paths["ontology"],
        malleus_import=paths["malleus"],
        linkml_types=paths["linkml"],
        selected_reading=paths["reading"],
        population=paths["population"],
        generic_recipes=paths["recipes"],
        ontology_acceptance=paths["acceptance"],
        protocol_machine=paths["machine"],
    )
    build = run_frozen_experiment(
        root,
        configuration=configuration(manifest, domain, transaction_time),
        inputs=inputs,
        private_run_dir=private_run_dir,
        results_dir=results_dir,
    )
    query_result = run_query_replay(
        build.replay_receipt_bytes,
        binding,
        ontology_path=paths["ontology"],
        ontology_source=paths["ontology"].read_bytes(),
        malleus_path=paths["malleus"],
        malleus_source=paths["malleus"].read_bytes(),
    )
    write_query_result(results_dir / "query-result.json", query_result)
    return query_result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--private-run", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--transaction-time", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    run_manifest_experiment(
        args.repository_root,
        args.manifest,
        private_run_dir=args.private_run,
        results_dir=args.results,
        transaction_time=args.transaction_time,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


__all__ = [
    "MANIFEST_SCHEMA",
    "MultimodelRefusal",
    "RunManifest",
    "binding_closure",
    "compile_manifest_ontology",
    "contract_only_types",
    "derive_run_artifacts",
    "domain_iri",
    "load_ontology",
    "population_brief_sections",
    "recipe_document",
    "run_manifest_experiment",
]
