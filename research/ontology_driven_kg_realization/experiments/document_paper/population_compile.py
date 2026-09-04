"""Compile one exact D3 population into an aligned GraphRecipe plan."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any

from malleus._contract_pipeline import ValidatedContractCompilation
from malleus.ledger import canonical_json

from ..graph_recipe.assembly import AssemblyPlan, assemble_plan
from ..graph_recipe.model import (
    GraphRecipeDiagnostic,
    GraphRecipeFailure,
    LogicalGraphContract,
)
from ..graph_recipe.stottr import (
    RecipeTerm,
    compile_graph_recipe,
    expand_invocation,
    parse_stottr,
)
from .compiled_graph_recipe_contract import require_plan_contract_alignment


_INTERNAL_INVOCATION_NAMESPACE = (
    "https://malleus.dev/paper-v4/population/invocation/"
)
_XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema#"


class PopulationCompileRefusal(GraphRecipeFailure):
    """A deterministic refusal suitable for the one structural retry."""


@dataclass(frozen=True, slots=True)
class PopulationCompilation:
    """One immutable plan and its canonical block-to-emission map."""

    plan: AssemblyPlan
    provenance_map_bytes: bytes


@dataclass(frozen=True, slots=True)
class PopulationRecipeProfile:
    """All adopter-owned population and recipe binding choices."""

    population_schema: str
    selected_reading_schema: str
    provenance_schema: str
    graph_recipe_profile_iri: str
    recipe_namespace: str
    member_namespace: str
    record_type_templates: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        fields = (
            "population_schema",
            "selected_reading_schema",
            "provenance_schema",
            "graph_recipe_profile_iri",
            "recipe_namespace",
            "member_namespace",
        )
        for field in fields:
            value = getattr(self, field)
            if type(value) is not str or not value.strip():
                raise ValueError(f"{field} must be nonblank text")
        mappings = self.record_type_templates
        if type(mappings) is not tuple or not mappings:
            raise ValueError("record_type_templates must be a nonempty tuple")
        record_types = []
        for index, mapping in enumerate(mappings):
            if type(mapping) is not tuple or len(mapping) != 2:
                raise ValueError(
                    f"record_type_templates[{index}] must be a two-item tuple"
                )
            record_type, template_name = mapping
            if type(record_type) is not str or not record_type.strip():
                raise ValueError(
                    f"record_type_templates[{index}].record_type must be nonblank text"
                )
            if type(template_name) is not str or not template_name.strip():
                raise ValueError(
                    f"record_type_templates[{index}].template_name must be nonblank text"
                )
            record_types.append(record_type)
        duplicates = sorted(
            {item for item in record_types if record_types.count(item) > 1}
        )
        if duplicates:
            raise ValueError(
                "record_type_templates contains duplicate record types: "
                + ", ".join(duplicates)
            )


def _fail(code: str, subject: str, message: str, **evidence: Any) -> None:
    raise PopulationCompileRefusal(
        GraphRecipeDiagnostic(
            code,
            "population-compilation",
            subject,
            {"message": message},
            evidence,
        )
    )


def _text(value: object, subject: str) -> str:
    if type(value) is not str or not value.strip():
        _fail("POPULATION_TEXT_INVALID", subject, "Value must be nonblank text.")
    return value


def _digest(value: object, subject: str) -> str:
    text = _text(value, subject)
    if (
        not text.startswith("sha256:")
        or len(text) != 71
        or any(character not in "0123456789abcdef" for character in text[7:])
    ):
        _fail(
            "POPULATION_DIGEST_INVALID",
            subject,
            "Value must be a lowercase sha256 digest.",
        )
    return text


def _object(value: object, fields: set[str], subject: str) -> dict[str, Any]:
    if type(value) is not dict:
        _fail("POPULATION_SCHEMA_INVALID", subject, "Value must be an object.")
    actual = set(value)
    if actual != fields:
        _fail(
            "POPULATION_FIELDS_INVALID",
            subject,
            "Object fields do not match the closed D3 grammar.",
            missing_fields=sorted(fields - actual),
            unexpected_fields=sorted(actual - fields),
        )
    return value


def _pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in values:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValueError(f"nonstandard numeric constant: {value}")


def _load(source: bytes) -> dict[str, Any]:
    try:
        value = json.loads(
            source.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        _fail(
            "POPULATION_JSON_INVALID",
            "population",
            "Population must be one strict UTF-8 JSON value.",
            error_type=type(error).__name__,
        )
    return _object(
        value,
        {"schema", "ontology_sha256", "reading_sha256", "records"},
        "population",
    )


def _reading(
    source: object, *, selected_reading_schema: str
) -> tuple[str, frozenset[str]]:
    if type(source) is not bytes:
        _fail(
            "POPULATION_INPUT_INVALID",
            "selected_reading_bytes",
            "Input must be exact bytes.",
        )
    try:
        value = json.loads(
            source.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        _fail(
            "POPULATION_READING_INVALID",
            "selected_reading",
            "Selected reading must be strict UTF-8 JSON.",
            error_type=type(error).__name__,
        )
    reading = _object(
        value,
        {
            "schema",
            "source_sha256",
            "extractor",
            "projection",
            "page_count",
            "block_count",
            "pages",
        },
        "selected_reading",
    )
    if reading["schema"] != selected_reading_schema:
        _fail(
            "POPULATION_READING_INVALID",
            "selected_reading.schema",
            "Selected reading schema does not match the population recipe profile.",
        )
    pages = reading["pages"]
    if type(pages) is not list or not pages or reading["page_count"] != len(pages):
        _fail(
            "POPULATION_READING_INVALID",
            "selected_reading.pages",
            "Selected reading page count is invalid.",
        )
    block_ids = []
    for page_index, raw_page in enumerate(pages):
        page = _object(
            raw_page, {"page", "blocks"}, f"selected_reading.pages[{page_index}]"
        )
        blocks = page["blocks"]
        if type(blocks) is not list or not blocks:
            _fail(
                "POPULATION_READING_INVALID",
                f"selected_reading.pages[{page_index}].blocks",
                "Each selected-reading page must contain blocks.",
            )
        for block_index, raw_block in enumerate(blocks):
            block = _object(
                raw_block,
                {"id", "ordinal", "sha256", "text"},
                f"selected_reading.pages[{page_index}].blocks[{block_index}]",
            )
            block_ids.append(_text(block["id"], "selected_reading block id"))
    if reading["block_count"] != len(block_ids) or len(block_ids) != len(
        set(block_ids)
    ):
        _fail(
            "POPULATION_READING_INVALID",
            "selected_reading.block_count",
            "Selected reading block count or identity closure is invalid.",
        )
    return "sha256:" + sha256(source).hexdigest(), frozenset(block_ids)


def _locator(value: object, blocks: frozenset[str], subject: str) -> str:
    locator = _text(value, subject)
    if locator not in blocks:
        _fail(
            "POPULATION_LOCATOR_UNKNOWN",
            subject,
            "Block locator is absent from the selected reading.",
            block_id=locator,
        )
    return locator


def _endpoint(value: object, blocks: frozenset[str], subject: str) -> dict[str, str]:
    data = _object(value, {"record_id", "block_id"}, subject)
    return {
        "record_id": _text(data["record_id"], f"{subject}.record_id"),
        "block_id": _locator(data["block_id"], blocks, f"{subject}.block_id"),
    }


def _camel(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(item.title() for item in tail)


def _required_population_properties(record: Any) -> tuple[str, ...]:
    return tuple(
        slot.runtime_symbol
        for slot in record.operation_properties
        if slot.constraints.required and slot.constraints.equals_string is None
    )


def _validate_records(
    raw: object,
    blocks: frozenset[str],
    compilation: ValidatedContractCompilation,
    contract: LogicalGraphContract,
    templates: dict[str, str],
) -> tuple[dict[str, Any], ...]:
    if type(raw) is not list or not raw:
        _fail(
            "POPULATION_RECORDS_INVALID",
            "population.records",
            "Records must be a nonempty array.",
        )
    records: list[dict[str, Any]] = []
    for index, value in enumerate(raw):
        subject = f"population.records[{index}]"
        if type(value) is not dict:
            _fail("POPULATION_SCHEMA_INVALID", subject, "Record must be an object.")
        if "record_type" not in value:
            _fail(
                "POPULATION_FIELDS_INVALID",
                subject,
                "Record omits record_type.",
                missing_fields=["record_type"],
            )
        record_type = _text(value["record_type"], f"{subject}.record_type")
        if record_type not in templates:
            _fail(
                "POPULATION_RECORD_TYPE_UNMAPPED",
                f"{subject}.record_type",
                "Record type has no template in the population recipe profile.",
                mapped_record_types=sorted(templates),
            )
        try:
            record_contract = contract.record_for_symbol(record_type)
        except GraphRecipeFailure:
            _fail(
                "POPULATION_CONTRACT_DRIFT",
                f"{subject}.record_type",
                "Record type is absent from the logical contract.",
            )
        fields = {"record_id", "record_type", "record_block_id", "properties"}
        if record_contract.role == "RELATION":
            fields.update({"source", "target"})
        data = _object(value, fields, subject)
        property_names = _required_population_properties(record_contract)
        properties = _object(
            data["properties"],
            set(property_names),
            f"{subject}.properties",
        )
        normalized_properties = {}
        for name in property_names:
            wrapped = _object(
                properties[name],
                {"value", "block_id"},
                f"{subject}.properties.{name}",
            )
            scalar = wrapped["value"]
            if type(scalar) is str:
                _text(scalar, f"{subject}.properties.{name}.value")
            elif type(scalar) in {int, float}:
                try:
                    finite = math.isfinite(float(scalar))
                except OverflowError:
                    finite = False
                if not finite:
                    _fail(
                        "POPULATION_RECORD_INVALID",
                        f"{subject}.properties.{name}.value",
                        "Numeric values must be finite.",
                    )
            normalized_properties[name] = (
                scalar,
                _locator(
                    wrapped["block_id"],
                    blocks,
                    f"{subject}.properties.{name}.block_id",
                ),
            )
        record_id = _text(data["record_id"], f"{subject}.record_id")
        source = (
            _endpoint(data["source"], blocks, f"{subject}.source")
            if record_contract.role == "RELATION"
            else None
        )
        target = (
            _endpoint(data["target"], blocks, f"{subject}.target")
            if record_contract.role == "RELATION"
            else None
        )
        instance = {"id": record_id}
        instance.update({name: item[0] for name, item in normalized_properties.items()})
        instance.update(
            {
                slot.runtime_symbol: slot.constraints.equals_string
                for slot in record_contract.operation_properties
                if slot.constraints.equals_string is not None
            }
        )
        if source is not None and target is not None:
            instance.update(
                {"source_id": source["record_id"], "target_id": target["record_id"]}
            )
        errors = compilation.view.validate_instance(record_contract.type_iri, instance)
        if errors:
            _fail(
                "POPULATION_RECORD_INVALID",
                subject,
                "Record violates the compiled ontology.",
                errors=sorted(errors),
            )
        records.append(
            {
                "record_id": record_id,
                "record_type": record_type,
                "record_block_id": _locator(
                    data["record_block_id"], blocks, f"{subject}.record_block_id"
                ),
                "properties": normalized_properties,
                "source": source,
                "target": target,
            }
        )

    identifiers = [record["record_id"] for record in records]
    duplicates = sorted({item for item in identifiers if identifiers.count(item) > 1})
    if duplicates:
        _fail(
            "POPULATION_RECORD_ID_DUPLICATE",
            "population.records",
            "Record IDs must be unique.",
            duplicate_record_ids=duplicates,
        )
    by_id = {record["record_id"]: record for record in records}
    for record in records:
        if record["source"] is None:
            continue
        relation = contract.record_for_symbol(record["record_type"])
        assert relation.endpoint_constraints is not None
        for role, expected in (
            ("source", relation.endpoint_constraints.source),
            ("target", relation.endpoint_constraints.target),
        ):
            endpoint_id = record[role]["record_id"]
            endpoint = by_id.get(endpoint_id)
            if endpoint is None:
                _fail(
                    "POPULATION_ENDPOINT_DANGLING",
                    f"{record['record_id']}.{role}",
                    "Endpoint does not name a population record.",
                    endpoint_record_id=endpoint_id,
                )
            endpoint_contract = contract.record_for_symbol(endpoint["record_type"])
            if endpoint_contract.role != "ENTITY":
                _fail(
                    "POPULATION_ENDPOINT_NOT_ENTITY",
                    f"{record['record_id']}.{role}",
                    "Endpoint must name an entity record.",
                )
            if not compilation.view.is_subtype_of(endpoint_contract.type_iri, expected):
                _fail(
                    "POPULATION_ENDPOINT_TYPE_MISMATCH",
                    f"{record['record_id']}.{role}",
                    "Endpoint direction violates the compiled contract.",
                    actual_type=endpoint_contract.type_iri,
                    expected_type=expected,
                )
    return tuple(records)


def _iri(base: str, record_id: str) -> str:
    return base + sha256(record_id.encode("utf-8")).hexdigest()


def _term(value: bool | int | float | str) -> RecipeTerm:
    if type(value) is int:
        return RecipeTerm.integer(value)
    if type(value) is float:
        return RecipeTerm.literal(
            json.dumps(value, allow_nan=False), _XSD_NAMESPACE + "float"
        )
    return RecipeTerm.literal(value)


def _emission(
    emissions: tuple[dict[str, Any], ...],
    kind: str,
    subject: str,
    property_iri: str | None = None,
) -> dict[str, str]:
    matches = [
        item
        for item in emissions
        if item["fact"]["kind"] == kind
        and (property_iri is None or item["fact"].get("property") == property_iri)
    ]
    if len(matches) != 1:
        _fail(
            "POPULATION_RECIPE_PROVENANCE_INVALID",
            subject,
            "Assertion must map to exactly one recipe emission.",
            emission_count=len(matches),
        )
    return {
        "emission_id": matches[0]["emission_id"],
        "expansion_path_id": matches[0]["expansion_path_id"],
        "emitted_fact": matches[0]["fact"],
    }


def _provenance(
    record: dict[str, Any],
    contract: LogicalGraphContract,
    emissions: tuple[dict[str, Any], ...],
) -> list[dict[str, Any]]:
    record_id = record["record_id"]
    result = [
        {
            "assertion_kind": "RECORD",
            "block_id": record["record_block_id"],
            "record_id": record_id,
            **_emission(emissions, "Record", f"{record_id}.record"),
        }
    ]
    for name, (_, block_id) in record["properties"].items():
        result.append(
            {
                "assertion_kind": "PROPERTY",
                "block_id": block_id,
                "property": name,
                "record_id": record_id,
                **_emission(
                    emissions,
                    "Property",
                    f"{record_id}.{name}",
                    contract.symbol_bindings.property_iri(name),
                ),
            }
        )
    for role, kind in (("source", "RelationSource"), ("target", "RelationTarget")):
        if record[role] is not None:
            result.append(
                {
                    "assertion_kind": role.upper(),
                    "block_id": record[role]["block_id"],
                    "endpoint_record_id": record[role]["record_id"],
                    "record_id": record_id,
                    **_emission(emissions, kind, f"{record_id}.{role}"),
                }
            )
    return result


def compile_population(
    population_bytes: bytes,
    *,
    compiled_ontology: ValidatedContractCompilation,
    logical_contract: LogicalGraphContract,
    generic_recipe_bytes: bytes,
    selected_reading_bytes: bytes,
    recipe_profile: PopulationRecipeProfile,
) -> PopulationCompilation:
    """Validate, expand, assemble, and align one exact population."""

    if type(population_bytes) is not bytes:
        _fail(
            "POPULATION_INPUT_INVALID", "population_bytes", "Input must be exact bytes."
        )
    if type(compiled_ontology) is not ValidatedContractCompilation:
        _fail(
            "POPULATION_INPUT_INVALID",
            "compiled_ontology",
            "Input must be one exact ValidatedContractCompilation.",
        )
    if type(logical_contract) is not LogicalGraphContract:
        _fail(
            "POPULATION_INPUT_INVALID",
            "logical_contract",
            "Input must be one exact LogicalGraphContract.",
        )
    if type(recipe_profile) is not PopulationRecipeProfile:
        _fail(
            "POPULATION_INPUT_INVALID",
            "recipe_profile",
            "Input must be one exact PopulationRecipeProfile.",
        )
    if type(generic_recipe_bytes) is not bytes or not generic_recipe_bytes:
        _fail(
            "POPULATION_INPUT_INVALID",
            "generic_recipe_bytes",
            "Input must be nonempty exact bytes.",
        )
    ontology_digest = _digest(
        "sha256:" + compiled_ontology.source.sha256,
        "compiled_ontology.source.sha256",
    )
    templates = dict(recipe_profile.record_type_templates)
    for record_type in templates:
        try:
            record_contract = logical_contract.record_for_symbol(record_type)
        except GraphRecipeFailure:
            _fail(
                "POPULATION_PROFILE_RECORD_TYPE_UNKNOWN",
                f"recipe_profile.record_type_templates.{record_type}",
                "Mapped record type is absent from the logical contract.",
            )
        if (
            record_contract.abstract
            or record_contract.type_iri
            not in logical_contract.constructible_record_types
        ):
            _fail(
                "POPULATION_PROFILE_RECORD_TYPE_NONCONSTRUCTIBLE",
                f"recipe_profile.record_type_templates.{record_type}",
                "Mapped record type cannot produce a logical-contract operation.",
                abstract=record_contract.abstract,
                record_type_iri=record_contract.type_iri,
            )
    reading_digest, selected_reading_block_ids = _reading(
        selected_reading_bytes,
        selected_reading_schema=recipe_profile.selected_reading_schema,
    )

    population = _load(population_bytes)
    if population["schema"] != recipe_profile.population_schema:
        _fail(
            "POPULATION_SCHEMA_INVALID",
            "population.schema",
            "Population schema does not match the population recipe profile.",
        )
    for field, expected in (
        ("ontology_sha256", ontology_digest),
        ("reading_sha256", reading_digest),
    ):
        if population[field] != expected:
            _fail(
                "POPULATION_DIGEST_MISMATCH",
                f"population.{field}",
                "Population digest does not match the frozen input.",
                expected=expected,
                actual=population[field],
            )
    records = _validate_records(
        population["records"],
        selected_reading_block_ids,
        compiled_ontology,
        logical_contract,
        templates,
    )
    members = {
        record["record_id"]: _iri(
            recipe_profile.member_namespace, record["record_id"]
        )
        for record in records
    }

    try:
        document = parse_stottr(generic_recipe_bytes, "paper-v4:generic-recipes")
        declared_templates = {template.template_iri for template in document.templates}
        unknown_templates = sorted(
            recipe_profile.recipe_namespace + template
            for template in templates.values()
            if recipe_profile.recipe_namespace + template not in declared_templates
        )
        if unknown_templates:
            _fail(
                "POPULATION_PROFILE_TEMPLATE_UNKNOWN",
                "recipe_profile.record_type_templates",
                "Mapped recipe template is absent from the recipe document.",
                unknown_template_iris=unknown_templates,
            )
        recipes = {}
        all_emissions = []
        invocation_digests = []
        provenance = []
        for record in records:
            template = templates[record["record_type"]]
            root = recipe_profile.recipe_namespace + template
            if root not in recipes:
                recipes[root] = compile_graph_recipe(
                    (document,),
                    root_template=root,
                    contract_digest=logical_contract.contract_digest,
                    profile_id=recipe_profile.graph_recipe_profile_iri,
                    expansion_profile_id=recipe_profile.graph_recipe_profile_iri,
                )
            recipe = recipes[root]
            contract_record = logical_contract.record_for_symbol(record["record_type"])
            parameters = tuple(item.name for item in recipe.template(root).parameters)
            arguments = {
                "member": RecipeTerm.iri(members[record["record_id"]]),
                "recordId": RecipeTerm.literal(record["record_id"]),
            }
            if "recordType" in parameters:
                arguments["recordType"] = RecipeTerm.iri(contract_record.type_iri)
            for name in _required_population_properties(contract_record):
                arguments[_camel(name)] = _term(record["properties"][name][0])
            if record["source"] is not None:
                for role in ("source", "target"):
                    endpoint_id = record[role]["record_id"]
                    arguments[role + "Member"] = RecipeTerm.iri(members[endpoint_id])
                    arguments[role + "Id"] = RecipeTerm.literal(endpoint_id)
            if set(arguments) != set(parameters) or len(arguments) != len(parameters):
                _fail(
                    "POPULATION_RECIPE_BINDING_INVALID",
                    record["record_type"],
                    "Recipe parameters do not match the closed population mapping.",
                    missing_parameters=sorted(set(parameters) - set(arguments)),
                    unexpected_parameters=sorted(set(arguments) - set(parameters)),
                )
            expansion = expand_invocation(
                recipe,
                invocation_id=_iri(
                    _INTERNAL_INVOCATION_NAMESPACE, record["record_id"]
                ),
                arguments={name: arguments[name] for name in parameters},
            )
            all_emissions.extend(expansion.emissions)
            invocation_digests.append(expansion.invocation_digest)
            provenance.extend(
                _provenance(record, logical_contract, expansion.emissions)
            )

        plan = assemble_plan(
            logical_contract,
            all_emissions,
            invocation_digests=invocation_digests,
        )
        require_plan_contract_alignment(plan, logical_contract, compiled_ontology)
    except PopulationCompileRefusal:
        raise
    except GraphRecipeFailure as error:
        raise PopulationCompileRefusal(error.diagnostics) from error

    provenance_bytes = canonical_json(
        {
            "assertions": sorted(provenance, key=canonical_json),
            "ontology_sha256": ontology_digest,
            "plan_sha256": plan.plan_digest,
            "reading_sha256": reading_digest,
            "schema": recipe_profile.provenance_schema,
        }
    ).encode("utf-8")
    return PopulationCompilation(plan, provenance_bytes)


__all__ = [
    "PopulationCompilation",
    "PopulationCompileRefusal",
    "PopulationRecipeProfile",
    "compile_population",
]
