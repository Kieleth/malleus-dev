"""End-to-end tests for the first GraphRecipe conformance slice."""

from __future__ import annotations

import json
from pathlib import Path
import shutil

import pytest
import yaml

from malleus.kg import KnowledgeGraph
from malleus.ledger import content_digest
from malleus.ontology import OntologyRegistry
from malleus.source import source_bytes_digest

from research.ontology_driven_kg_realization.experiments.graph_recipe.assembly import (
    assemble_plan,
    stage_and_materialize,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.case_harness import (
    CaseHarnessError,
    ReceiptMismatch,
    assert_receipt,
    run_experiment,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.contract import (
    derive_logical_contract,
    load_ontology_symbol_bindings,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.model import (
    GraphRecipeFailure,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.stottr import (
    RecipeTerm,
    compile_graph_recipe,
    expand_invocation,
    parse_stottr,
)


ROOT = Path(__file__).resolve().parents[4]
CORPUS_ROOT = ROOT / "conformance" / "graph_recipe" / "v0"
CORPUS = CORPUS_ROOT / "corpus.json"
CHECKSUMS = CORPUS_ROOT / "checksums.json"
REPORT = Path(__file__).with_name("FIRST_SLICE_CONFORMANCE_REPORT.json")

EXPECTED_CASES = {
    ("GE-000-ONTOLOGY-IS-NOT-POPULATION", "baseline"),
    ("GE-000-ONTOLOGY-IS-NOT-POPULATION", "recipe-selection-missing"),
    ("GE-010-ONE-ENTITY", "alice"),
    ("GE-010-ONE-ENTITY", "mandatory-recipe-value-missing"),
    ("GE-010-ONE-ENTITY", "recipe-argument-type-mismatch"),
    ("GE-010-ONE-ENTITY", "forbidden-blank-node"),
    ("GE-020-TWO-NODES-ONE-RELATION", "alice-works-for-acme-relation-first"),
    ("GE-020-TWO-NODES-ONE-RELATION", "local-reference-dependency-missing"),
    ("GE-020-TWO-NODES-ONE-RELATION", "wrong-endpoint-role"),
    ("GE-020-TWO-NODES-ONE-RELATION", "construction-dependency-cycle"),
}

METAMORPHIC_TESTS = {
    (
        "GE-000-ONTOLOGY-IS-NOT-POPULATION",
        "repeated-execution-preserves-all-semantic-artifacts",
    ): "test_case_receipt_is_repeatable",
    (
        "GE-000-ONTOLOGY-IS-NOT-POPULATION",
        "ontology-formatting-only-change-preserves-logical-contract-and-graph",
    ): "test_ontology_formatting_preserves_the_logical_contract_and_empty_graph",
    (
        "GE-010-ONE-ENTITY",
        "alpha-rename-variables",
    ): "test_person_alpha_rename_alone_is_semantically_invariant",
    (
        "GE-010-ONE-ENTITY",
        "formatting-and-safe-prefix-aliases",
    ): "test_person_formatting_and_prefix_aliases_alone_are_semantically_invariant",
    (
        "GE-010-ONE-ENTITY",
        "pattern-permutation",
    ): "test_person_pattern_permutation_alone_is_semantically_invariant",
    (
        "GE-020-TWO-NODES-ONE-RELATION",
        "pattern-permutation",
    ): "test_relation_first_and_node_first_patterns_produce_the_same_plan",
    (
        "GE-020-TWO-NODES-ONE-RELATION",
        "formatting-safe-prefix-alias-and-alpha-renaming",
    ): "test_employment_formatting_prefix_and_alpha_changes_are_semantically_invariant",
}


def _load_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def _load_yaml(path: Path):
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def _declared_cases():
    corpus = _load_json(CORPUS)
    cases = []
    for experiment in corpus["experiments"]:
        manifest = CORPUS_ROOT / experiment["manifest"]
        declaration = _load_yaml(manifest)
        cases.append((manifest, experiment["experiment_id"], declaration["case_id"]))
        for negative in declaration["negative_cases"]:
            cases.append((manifest, experiment["experiment_id"], negative["case_id"]))
    return tuple(cases)


DECLARED_CASES = _declared_cases()
CASE_IDS = [f"{experiment_id}::{case_id}" for _, experiment_id, case_id in DECLARED_CASES]


def test_corpus_declares_exact_first_slice():
    declared = {(experiment_id, case_id) for _, experiment_id, case_id in DECLARED_CASES}
    assert declared == EXPECTED_CASES


def test_every_declared_metamorphic_obligation_has_an_executable_test():
    corpus = _load_json(CORPUS)
    declared = set()
    for experiment in corpus["experiments"]:
        manifest = _load_yaml(CORPUS_ROOT / experiment["manifest"])
        for obligation in manifest["metamorphic_obligations"]:
            transform = obligation if isinstance(obligation, str) else obligation["transform"]
            declared.add((experiment["experiment_id"], transform))

    assert declared == set(METAMORPHIC_TESTS)
    missing_tests = sorted(
        name for name in METAMORPHIC_TESTS.values() if not callable(globals().get(name))
    )
    assert missing_tests == []


@pytest.mark.parametrize(
    "manifest,experiment_id,case_id",
    DECLARED_CASES,
    ids=CASE_IDS,
)
def test_frozen_case_matches_every_expected_artifact(manifest, experiment_id, case_id):
    receipt = run_experiment(manifest, case_id)
    assert receipt.experiment_id == experiment_id
    assert_receipt(receipt)


@pytest.mark.parametrize(
    "manifest,experiment_id,case_id",
    DECLARED_CASES,
    ids=CASE_IDS,
)
def test_case_receipt_is_repeatable(manifest, experiment_id, case_id):
    first = run_experiment(manifest, case_id)
    second = run_experiment(manifest, case_id)
    assert first.as_dict() == second.as_dict()


def test_digest_red_obligation_is_closed():
    corpus = _load_json(CORPUS)
    assert corpus["digest_gate"]["status"] == "complete"
    pending = []
    for path in sorted(CORPUS_ROOT.rglob("*")):
        if path.suffix not in {".json", ".yaml"}:
            continue
        value = _load_json(path) if path.suffix == ".json" else _load_yaml(path)
        stack = [("$", value)]
        while stack:
            location, item = stack.pop()
            if isinstance(item, dict):
                if item.get("status") == "pending":
                    pending.append(f"{path.relative_to(CORPUS_ROOT)}:{location}")
                stack.extend((f"{location}.{key}", member) for key, member in item.items())
            elif isinstance(item, list):
                stack.extend(
                    (f"{location}[{index}]", member) for index, member in enumerate(item)
                )
    assert pending == []


def test_checksum_set_and_report_bind_the_current_executable_snapshot():
    checksums = _load_json(CHECKSUMS)
    assert checksums["algorithm"] == "source-bytes-sha256-v1"
    declared = {item["path"]: item for item in checksums["files"]}
    actual_paths = {
        path.relative_to(CORPUS_ROOT).as_posix()
        for path in CORPUS_ROOT.rglob("*")
        if path.is_file() and path != CHECKSUMS
    }
    assert set(declared) == actual_paths
    assert checksums["file_count"] == len(actual_paths)
    for relative_path, identity in declared.items():
        source = (CORPUS_ROOT / relative_path).read_bytes()
        assert identity["size_bytes"] == len(source)
        assert identity["sha256"] == source_bytes_digest(source)

    report = _load_json(REPORT)
    assert report["corpus_identities"]["corpus"]["sha256"] == source_bytes_digest(
        CORPUS.read_bytes()
    )
    assert report["corpus_identities"]["profile"]["sha256"] == source_bytes_digest(
        (CORPUS_ROOT / "profile.json").read_bytes()
    )
    assert report["corpus_identities"]["checksum_set"]["sha256"] == source_bytes_digest(
        CHECKSUMS.read_bytes()
    )
    assert report["corpus_identities"]["checksum_set"]["covered_file_count"] == len(
        actual_paths
    )
    for group in report["bound_file_identities"].values():
        if not isinstance(group, dict):
            continue
        for relative_path, expected_digest in group.items():
            assert source_bytes_digest((ROOT / relative_path).read_bytes()) == expected_digest, (
                f"{relative_path} drifted from its binding; rebind with "
                f"research/ontology_driven_kg_realization/experiments/graph_recipe/"
                f"rebind_report.py rather than editing a digest by hand"
            )

    receipt_identities = {
        (item["experiment_id"], item["case_id"]): item
        for item in report["case_receipt_identities"]["cases"]
    }
    assert set(receipt_identities) == EXPECTED_CASES
    for manifest, experiment_id, case_id in DECLARED_CASES:
        receipt = run_experiment(manifest, case_id)
        identity = receipt_identities[(experiment_id, case_id)]
        assert identity["selected_manifest_identity"]["sha256"] == receipt.manifest_digest
        assert identity["canonical_receipt_digest"] == content_digest(receipt.as_dict())


def test_report_public_snapshot_boundary_is_classified_and_non_enumerating():
    snapshot = _load_json(REPORT)["repository_snapshot"]
    assert "dirty_worktree_boundary" not in snapshot

    boundary = snapshot["working_tree_boundary"]
    assert boundary["enumeration"] == "non-enumerating"
    assert boundary["classification"]
    assert boundary["private_or_excluded_path_names_disclosed"] is False
    assert not {"command", "entries", "files", "paths"}.intersection(boundary)

    path_suffixes = (".json", ".md", ".py", ".toml", ".ttl", ".yaml", ".yml")
    for value in boundary.values():
        if not isinstance(value, str):
            continue
        assert "/" not in value and "\\" not in value and "\n" not in value
        tokens = (token.strip("`'\"()[]{}.,:;") for token in value.split())
        assert not any(token.endswith(path_suffixes) for token in tokens)


def test_execution_never_opens_expected_artifacts(monkeypatch):
    original_open = Path.open

    def guarded_open(path, *args, **kwargs):
        if "expected" in path.resolve(strict=False).parts:
            raise AssertionError(f"execution opened assertion oracle: {path}")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    for manifest, _, case_id in DECLARED_CASES:
        receipt = run_experiment(manifest, case_id)
        assert all("expected" not in Path(locator).parts for locator in receipt.execution_reads)


def test_expected_pin_tampering_is_assertion_only(tmp_path):
    corpus = tmp_path / "v0"
    shutil.copytree(CORPUS_ROOT, corpus)
    manifest = corpus / "experiments" / "ge-010-one-entity" / "experiment.yaml"
    expected = manifest.parent / "expected" / "diagnostics.json"
    expected.write_bytes(expected.read_bytes() + b"\n")

    receipt = run_experiment(manifest, "alice")
    with pytest.raises(ReceiptMismatch, match="artifact pin mismatch.*expected/diagnostics.json"):
        assert_receipt(receipt)


def test_receipt_binds_the_exact_assertion_manifest_bytes(tmp_path):
    corpus = tmp_path / "v0"
    shutil.copytree(CORPUS_ROOT, corpus)
    manifest = corpus / "experiments" / "ge-010-one-entity" / "experiment.yaml"
    receipt = run_experiment(manifest, "alice")
    manifest.write_bytes(manifest.read_bytes() + b"\n# mutated after execution\n")

    with pytest.raises(ReceiptMismatch, match="manifest bytes differ"):
        assert_receipt(receipt)


def test_input_pin_tampering_fails_before_execution(tmp_path):
    corpus = tmp_path / "v0"
    shutil.copytree(CORPUS_ROOT, corpus)
    manifest = corpus / "experiments" / "ge-010-one-entity" / "experiment.yaml"
    prior_graph = manifest.parent / "input" / "prior-graph.json"
    prior_graph.write_bytes(prior_graph.read_bytes() + b"\n")

    with pytest.raises(CaseHarnessError, match="artifact pin mismatch.*input/prior-graph.json"):
        run_experiment(manifest, "alice")


@pytest.mark.parametrize(
    "mutation,match",
    (
        ("missing", "missing required fields: input/prior-graph.json"),
        ("extra", "unknown fields: input/not-declared.json"),
    ),
)
def test_artifact_pin_map_is_an_exact_declaration_closure(tmp_path, mutation, match):
    corpus = tmp_path / mutation / "v0"
    shutil.copytree(CORPUS_ROOT, corpus)
    manifest = corpus / "experiments" / "ge-010-one-entity" / "experiment.yaml"
    declaration = _load_yaml(manifest)
    if mutation == "missing":
        del declaration["artifact_digests"]["input/prior-graph.json"]
    else:
        declaration["artifact_digests"]["input/not-declared.json"] = "sha256:" + "0" * 64
    manifest.write_text(yaml.safe_dump(declaration, sort_keys=False), encoding="utf-8")

    with pytest.raises(CaseHarnessError, match=match):
        run_experiment(manifest, "alice")


def _compile_recipe(source: bytes, contract_digest: str, root_template: str, source_id: str):
    base_path = CORPUS_ROOT / "base" / "malleus-base-v0.stottr"
    base = parse_stottr(base_path.read_bytes(), "base/malleus-base-v0.stottr")
    recipe = parse_stottr(source, source_id)
    return compile_graph_recipe(
        (base, recipe),
        root_template=root_template,
        contract_digest=contract_digest,
        profile_id="https://malleus.dev/graph-recipe/profile/v0",
        expansion_profile_id="https://malleus.dev/graph-recipe/profile/v0",
    )


def _compile_person(source: bytes, contract_digest: str):
    return _compile_recipe(
        source,
        contract_digest,
        "https://fixtures.malleus.dev/graph-recipe/v0/recipe/Person-1.0.0",
        "experiments/ge-010-one-entity/input/recipe.stottr",
    )


def _semantic_paths(paths):
    return [
        {key: value for key, value in path.items() if key != "source_pattern_index"}
        for path in paths
    ]


def test_ontology_formatting_preserves_the_logical_contract_and_empty_graph(tmp_path):
    case_root = CORPUS_ROOT / "experiments" / "ge-000-ontology-is-not-population"
    ontology_path = case_root / "input" / "ontology.yaml"
    original_bytes = ontology_path.read_bytes()
    reformatted_bytes = yaml.safe_dump(
        yaml.safe_load(original_bytes),
        explicit_start=True,
        sort_keys=True,
    ).encode("utf-8")
    assert reformatted_bytes != original_bytes

    reformatted_path = tmp_path / "ontology.yaml"
    reformatted_path.write_bytes(reformatted_bytes)
    bindings = load_ontology_symbol_bindings(
        case_root / "input" / "ontology-symbol-bindings.json"
    )
    contract_id = "https://fixtures.malleus.dev/graph-recipe/v0/contract/person-only"
    original_registry = OntologyRegistry(ontology_path)
    reformatted_registry = OntologyRegistry(reformatted_path)
    original_contract = derive_logical_contract(original_registry, bindings, contract_id)
    reformatted_contract = derive_logical_contract(reformatted_registry, bindings, contract_id)

    assert original_contract.as_dict() == reformatted_contract.as_dict()
    assert original_contract.contract_digest == reformatted_contract.contract_digest
    prior = _load_json(case_root / "input" / "prior-graph.json")
    original_graph = KnowledgeGraph.from_records(original_registry, prior)
    reformatted_graph = KnowledgeGraph.from_records(reformatted_registry, prior)
    assert original_graph.snapshot() == reformatted_graph.snapshot()
    assert original_graph.state_digest() == reformatted_graph.state_digest()


def _assert_person_variant(
    variant_bytes: bytes,
    variant_parameter_names: tuple[str, str, str],
) -> None:
    case_root = CORPUS_ROOT / "experiments" / "ge-010-one-entity"
    registry = OntologyRegistry(case_root / "input" / "ontology.yaml")
    bindings = load_ontology_symbol_bindings(
        case_root / "input" / "ontology-symbol-bindings.json"
    )
    contract = derive_logical_contract(
        registry,
        bindings,
        "https://fixtures.malleus.dev/graph-recipe/v0/contract/person-only",
    )
    original_bytes = (case_root / "input" / "recipe.stottr").read_bytes()
    assert variant_bytes != original_bytes
    original = _compile_person(original_bytes, contract.contract_digest)
    variant = _compile_person(variant_bytes, contract.contract_digest)
    assert original.source_digests != variant.source_digests
    assert original.effective_recipe_digest == variant.effective_recipe_digest

    values = (
        RecipeTerm.iri("https://fixtures.malleus.dev/graph-recipe/v0/member/ge-010/01-person"),
        RecipeTerm.literal("person:alice"),
        RecipeTerm.literal("Alice"),
    )
    invocation_id = "https://fixtures.malleus.dev/graph-recipe/v0/invocation/ge-010-alice"
    first = expand_invocation(
        original,
        invocation_id=invocation_id,
        arguments=dict(zip(("personMember", "personId", "personName"), values, strict=True)),
    )
    second = expand_invocation(
        variant,
        invocation_id=invocation_id,
        arguments=dict(zip(variant_parameter_names, values, strict=True)),
    )
    assert first.invocation_digest == second.invocation_digest
    assert first.emissions == second.emissions
    assert _semantic_paths(first.expansion_paths) == _semantic_paths(second.expansion_paths)

    first_plan = assemble_plan(
        contract,
        first.emissions,
        invocation_digests=(first.invocation_digest,),
    )
    second_plan = assemble_plan(
        contract,
        second.emissions,
        invocation_digests=(second.invocation_digest,),
    )
    assert first_plan.member_graph_artifact() == second_plan.member_graph_artifact()
    assert first_plan.proposed_operations_artifact() == second_plan.proposed_operations_artifact()
    assert first_plan.operation_lineage() == second_plan.operation_lineage()
    assert first_plan.plan_digest == second_plan.plan_digest

    records = _load_json(case_root / "input" / "prior-graph.json")
    first_graph = KnowledgeGraph.from_records(registry, records)
    second_graph = KnowledgeGraph.from_records(registry, records)
    first_result = stage_and_materialize(first_graph, first_plan)
    second_result = stage_and_materialize(second_graph, second_plan)
    assert first_result.candidate_digest == second_result.candidate_digest
    assert first_result.as_dict() == second_result.as_dict()


def test_person_alpha_rename_alone_is_semantically_invariant():
    source = (
        CORPUS_ROOT / "experiments" / "ge-010-one-entity" / "input" / "recipe.stottr"
    ).read_bytes()
    variant = source.replace(b"personMember", b"member")
    variant = variant.replace(b"personId", b"identifier")
    variant = variant.replace(b"personName", b"label")
    _assert_person_variant(variant, ("member", "identifier", "label"))


def test_person_formatting_and_prefix_aliases_alone_are_semantically_invariant():
    source = (
        CORPUS_ROOT / "experiments" / "ge-010-one-entity" / "input" / "recipe.stottr"
    ).read_text(encoding="utf-8")
    variant = source.replace("mgrp:", "core:")
    variant = variant.replace("ottr:", "t:")
    variant = variant.replace("ont:", "domain:")
    variant = variant.replace("recipe:", "r:")
    variant = variant.replace("xsd:", "x:")
    variant = variant.replace("\n  ", "\n    ").encode("utf-8")
    _assert_person_variant(variant, ("personMember", "personId", "personName"))


def test_person_pattern_permutation_alone_is_semantically_invariant():
    source = (
        CORPUS_ROOT / "experiments" / "ge-010-one-entity" / "input" / "recipe.stottr"
    ).read_text(encoding="utf-8")
    first, second = source.index("  mgrp:Record"), source.index("  mgrp:Property")
    prefix = source[:first]
    record = source[first:second].rstrip(",\n")
    suffix_start = source.index("\n} .", second)
    prop = source[second:suffix_start].rstrip(",\n")
    variant = f"{prefix}{prop},\n{record}\n{source[suffix_start:]}".encode("utf-8")
    _assert_person_variant(variant, ("personMember", "personId", "personName"))


def test_effective_recipe_identity_binds_selected_root():
    source_path = CORPUS_ROOT / "experiments" / "ge-010-one-entity" / "input" / "recipe.stottr"
    source = source_path.read_bytes()
    alias = b"""
<https://fixtures.malleus.dev/graph-recipe/v0/recipe/Person-Alias> [
  ! <http://ns.ottr.xyz/0.4/IRI> ?member,
  ! <http://www.w3.org/2001/XMLSchema#string> ?recordId,
  ! <http://www.w3.org/2001/XMLSchema#string> ?name
] :: {
  <https://malleus.dev/graph-recipe/base/Record>(
    ?member,
    <https://malleus.dev/graph-recipe/base/CreateEntity>,
    <https://fixtures.malleus.dev/graph-recipe/v0/ontology/Person>,
    ?recordId
  ),
  <https://malleus.dev/graph-recipe/base/Property>(
    ?member,
    <https://fixtures.malleus.dev/graph-recipe/v0/ontology/name>,
    ?name
  )
} .
"""
    base_path = CORPUS_ROOT / "base" / "malleus-base-v0.stottr"
    documents = (
        parse_stottr(base_path.read_bytes(), "base/malleus-base-v0.stottr"),
        parse_stottr(source + alias, "two-roots.stottr"),
    )
    common = {
        "contract_digest": "sha256:" + "0" * 64,
        "profile_id": "https://malleus.dev/graph-recipe/profile/v0",
        "expansion_profile_id": "https://malleus.dev/graph-recipe/profile/v0",
    }
    person = compile_graph_recipe(
        documents,
        root_template="https://fixtures.malleus.dev/graph-recipe/v0/recipe/Person-1.0.0",
        **common,
    )
    alias_recipe = compile_graph_recipe(
        documents,
        root_template="https://fixtures.malleus.dev/graph-recipe/v0/recipe/Person-Alias",
        **common,
    )
    assert person.effective_recipe_digest != alias_recipe.effective_recipe_digest


def test_terminal_base_signature_is_closed():
    base_path = CORPUS_ROOT / "base" / "malleus-base-v0.stottr"
    invalid = base_path.read_bytes().replace(
        b"! xsd:string ?recordId",
        b"! xsd:integer ?recordId",
        1,
    )
    recipe_path = CORPUS_ROOT / "experiments" / "ge-010-one-entity" / "input" / "recipe.stottr"
    with pytest.raises(GraphRecipeFailure) as refusal:
        compile_graph_recipe(
            (
                parse_stottr(invalid, "invalid-base.stottr"),
                parse_stottr(recipe_path.read_bytes(), "person.stottr"),
            ),
            root_template="https://fixtures.malleus.dev/graph-recipe/v0/recipe/Person-1.0.0",
            contract_digest="sha256:" + "0" * 64,
            profile_id="https://malleus.dev/graph-recipe/profile/v0",
            expansion_profile_id="https://malleus.dev/graph-recipe/profile/v0",
        )
    assert [item.code for item in refusal.value.diagnostics] == ["TERMINAL_ABI_MISMATCH"]


def test_alpha_prefix_format_and_pattern_permutation_are_semantically_invariant():
    case_root = CORPUS_ROOT / "experiments" / "ge-010-one-entity"
    registry = OntologyRegistry(case_root / "input" / "ontology.yaml")
    bindings = load_ontology_symbol_bindings(case_root / "input" / "ontology-symbol-bindings.json")
    contract = derive_logical_contract(
        registry,
        bindings,
        "https://fixtures.malleus.dev/graph-recipe/v0/contract/person-only",
    )
    original_bytes = (case_root / "input" / "recipe.stottr").read_bytes()
    variant_bytes = b"""@prefix m: <https://malleus.dev/graph-recipe/base/> .
@prefix t: <http://ns.ottr.xyz/0.4/> .
@prefix domain: <https://fixtures.malleus.dev/graph-recipe/v0/ontology/> .
@prefix r: <https://fixtures.malleus.dev/graph-recipe/v0/recipe/> .
@prefix x: <http://www.w3.org/2001/XMLSchema#> .
r:Person-1.0.0 [ ! t:IRI ?m, ! x:string ?i, ! x:string ?n ] :: {
  m:Property(?m, domain:name, ?n),
  m:Record(?m, m:CreateEntity, domain:Person, ?i)
} .
"""
    original = _compile_person(original_bytes, contract.contract_digest)
    variant = _compile_person(variant_bytes, contract.contract_digest)
    assert original.source_digests != variant.source_digests
    assert original.effective_recipe_digest == variant.effective_recipe_digest

    identity = RecipeTerm.iri(
        "https://fixtures.malleus.dev/graph-recipe/v0/member/ge-010/01-person"
    )
    record_id = RecipeTerm.literal("person:alice")
    name = RecipeTerm.literal("Alice")
    invocation_id = "https://fixtures.malleus.dev/graph-recipe/v0/invocation/ge-010-alice"
    first = expand_invocation(
        original,
        invocation_id=invocation_id,
        arguments={"personMember": identity, "personId": record_id, "personName": name},
    )
    second = expand_invocation(
        variant,
        invocation_id=invocation_id,
        arguments={"m": identity, "i": record_id, "n": name},
    )
    assert first.invocation_digest == second.invocation_digest
    assert first.emissions == second.emissions
    assert _semantic_paths(first.expansion_paths) == _semantic_paths(second.expansion_paths)

    first_plan = assemble_plan(
        contract,
        first.emissions,
        invocation_digests=(first.invocation_digest,),
    )
    second_plan = assemble_plan(
        contract,
        second.emissions,
        invocation_digests=(second.invocation_digest,),
    )
    assert first_plan.plan_digest == second_plan.plan_digest
    assert first_plan.proposed_operations_artifact() == second_plan.proposed_operations_artifact()

    records = _load_json(case_root / "input" / "prior-graph.json")
    first_graph = KnowledgeGraph.from_records(registry, records)
    second_graph = KnowledgeGraph.from_records(registry, records)
    first_result = stage_and_materialize(first_graph, first_plan)
    second_result = stage_and_materialize(second_graph, second_plan)
    assert first_result.candidate_digest == second_result.candidate_digest
    assert first_result.as_dict() == second_result.as_dict()


def _assert_employment_variant(
    variant_bytes: bytes,
    variant_parameter_names: tuple[str, ...],
) -> None:
    case_root = CORPUS_ROOT / "experiments" / "ge-020-two-nodes-one-relation"
    registry = OntologyRegistry(case_root / "input" / "ontology.yaml")
    bindings = load_ontology_symbol_bindings(case_root / "input" / "ontology-symbol-bindings.json")
    contract = derive_logical_contract(
        registry,
        bindings,
        "https://fixtures.malleus.dev/graph-recipe/v0/contract/employment",
    )
    source = (case_root / "input" / "recipe.stottr").read_bytes()
    assert variant_bytes != source
    root_template = "https://fixtures.malleus.dev/graph-recipe/v0/recipe/Employment-1.0.0"
    original = _compile_recipe(
        source,
        contract.contract_digest,
        root_template,
        "experiments/ge-020-two-nodes-one-relation/input/recipe.stottr",
    )
    variant = _compile_recipe(
        variant_bytes,
        contract.contract_digest,
        root_template,
        "variant-employment.stottr",
    )
    assert original.source_digests != variant.source_digests
    assert original.effective_recipe_digest == variant.effective_recipe_digest

    original_names = (
        "personMember",
        "personId",
        "personName",
        "organizationMember",
        "organizationId",
        "organizationName",
        "employmentMember",
        "employmentId",
    )
    values = (
        RecipeTerm.iri(
            "https://fixtures.malleus.dev/graph-recipe/v0/member/ge-020/01-person"
        ),
        RecipeTerm.literal("person:alice"),
        RecipeTerm.literal("Alice"),
        RecipeTerm.iri(
            "https://fixtures.malleus.dev/graph-recipe/v0/member/ge-020/02-organization"
        ),
        RecipeTerm.literal("org:acme"),
        RecipeTerm.literal("Acme"),
        RecipeTerm.iri(
            "https://fixtures.malleus.dev/graph-recipe/v0/member/ge-020/03-employment"
        ),
        RecipeTerm.literal("employment:alice-acme"),
    )
    invocation_id = "https://fixtures.malleus.dev/graph-recipe/v0/invocation/ge-020-employment"
    first = expand_invocation(
        original,
        invocation_id=invocation_id,
        arguments=dict(zip(original_names, values, strict=True)),
    )
    second = expand_invocation(
        variant,
        invocation_id=invocation_id,
        arguments=dict(zip(variant_parameter_names, values, strict=True)),
    )
    assert first.invocation_digest == second.invocation_digest
    assert first.emissions == second.emissions
    assert _semantic_paths(first.expansion_paths) == _semantic_paths(second.expansion_paths)

    first_plan = assemble_plan(
        contract,
        first.emissions,
        invocation_digests=(first.invocation_digest,),
    )
    second_plan = assemble_plan(
        contract,
        second.emissions,
        invocation_digests=(second.invocation_digest,),
    )
    assert first_plan.topological_order == second_plan.topological_order
    assert first_plan.member_graph_artifact() == second_plan.member_graph_artifact()
    assert first_plan.plan_digest == second_plan.plan_digest
    assert first_plan.proposed_operations_artifact() == second_plan.proposed_operations_artifact()
    assert first_plan.operation_lineage() == second_plan.operation_lineage()

    records = _load_json(case_root / "input" / "prior-graph.json")
    first_graph = KnowledgeGraph.from_records(registry, records)
    second_graph = KnowledgeGraph.from_records(registry, records)
    first_result = stage_and_materialize(first_graph, first_plan)
    second_result = stage_and_materialize(second_graph, second_plan)
    assert first_result.candidate_digest == second_result.candidate_digest
    assert first_result.as_dict() == second_result.as_dict()


def test_relation_first_and_node_first_patterns_produce_the_same_plan():
    source = (
        CORPUS_ROOT
        / "experiments"
        / "ge-020-two-nodes-one-relation"
        / "input"
        / "recipe.stottr"
    ).read_text(encoding="utf-8")
    header, remainder = source.split("] :: {", 1)
    body, suffix = remainder.split("} .", 1)
    patterns = [line.strip().removesuffix(",") for line in body.splitlines() if line.strip()]
    permuted = (
        header
        + "] :: {\n  "
        + ",\n  ".join(reversed(patterns))
        + "\n} ."
        + suffix
    ).encode("utf-8")
    _assert_employment_variant(
        permuted,
        (
            "personMember",
            "personId",
            "personName",
            "organizationMember",
            "organizationId",
            "organizationName",
            "employmentMember",
            "employmentId",
        ),
    )


def test_employment_formatting_prefix_and_alpha_changes_are_semantically_invariant():
    source = (
        CORPUS_ROOT
        / "experiments"
        / "ge-020-two-nodes-one-relation"
        / "input"
        / "recipe.stottr"
    ).read_text(encoding="utf-8")
    replacements = {
        "mgrp:": "core:",
        "ottr:": "t:",
        "ont:": "domain:",
        "recipe:": "r:",
        "xsd:": "x:",
        "personMember": "pm",
        "personId": "pi",
        "personName": "pn",
        "organizationMember": "om",
        "organizationId": "oi",
        "organizationName": "on",
        "employmentMember": "em",
        "employmentId": "ei",
    }
    for before, after in replacements.items():
        source = source.replace(before, after)
    variant = source.replace("\n  ", "\n    ").encode("utf-8")
    _assert_employment_variant(
        variant,
        ("pm", "pi", "pn", "om", "oi", "on", "em", "ei"),
    )
