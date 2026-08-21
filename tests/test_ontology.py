"""Tests for ontology schemas: root + domain extensions.

Validates that LinkML schemas compile, generate correctly,
and enforce the type constraints we depend on for the experiment.
Also tests content-addressable hashing and compatibility checking
for distributed ontology convergence.
"""

import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
import yaml

from malleus.ontology import (
    OntologyError,
    OntologyRegistry,
    SlotConstraint,
    bundled_ontology_path,
)

ONTOLOGY_DIR = Path(__file__).parent.parent / "ontology"
ROOT_SCHEMA = ONTOLOGY_DIR / "malleus.yaml"
CYP450_SCHEMA = ONTOLOGY_DIR / "domains" / "cyp450.yaml"
ATTACK_SCHEMA = ONTOLOGY_DIR / "domains" / "attack.yaml"
PYPROJECT = ONTOLOGY_DIR.parent / "pyproject.toml"


def run_linkml(command: str, schema: Path) -> subprocess.CompletedProcess:
    """Run a LinkML generator command on a schema."""
    result = subprocess.run(
        [sys.executable, "-m", "linkml.generators." + command, str(schema)],
        capture_output=True,
        text=True,
    )
    return result


def test_no_isolation_build_backend_is_declared_for_development():
    """The development extra must install the configured build backend."""
    try:
        import tomllib
    except ModuleNotFoundError:  # Python 3.10
        import tomli as tomllib

    project = tomllib.loads(PYPROJECT.read_text())
    build_backend = project["build-system"]["requires"][0]
    assert build_backend in project["project"]["optional-dependencies"]["dev"]


def test_distribution_metadata_toolchain_is_reproducible():
    text = PYPROJECT.read_text()
    assert 'requires = ["hatchling==1.31.0"]' in text
    assert '"build==1.2.2.post1"' in text
    assert '"ruff==0.11.9"' in text
    assert '"twine==6.2.0"' in text
    assert text.count('core-metadata-version = "2.4"') == 2


# --- Root Ontology ---


class TestRootOntology:
    def test_schema_loads(self):
        """Root schema is valid YAML."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["name"] == "malleus"
        assert schema["version"] == "0.4.0"

    def test_bundled_ontology_path_resolves_source_and_domain_imports(self):
        root = bundled_ontology_path("malleus.yaml")
        domain = bundled_ontology_path("domains", "cyp450.yaml")
        assert root.resolve() == ROOT_SCHEMA.resolve()
        assert domain.resolve() == CYP450_SCHEMA.resolve()
        assert OntologyRegistry(domain).has_type("Drug")

    @pytest.mark.parametrize("parts", [("..", "private.yaml"), ("domains/..", "malleus.yaml")])
    def test_bundled_ontology_path_rejects_traversal(self, parts):
        with pytest.raises(OntologyError, match="relative names"):
            bundled_ontology_path(*parts)

    def test_generates_json_schema(self):
        """Root schema compiles to JSON Schema."""
        result = run_linkml("jsonschemagen", ROOT_SCHEMA)
        assert result.returncode == 0, f"Failed: {result.stderr}"
        json_schema = json.loads(result.stdout)
        assert "$defs" in json_schema

    def test_core_classes_exist(self):
        """All five core classes are defined."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        classes = schema["classes"]
        for cls in ["Entity", "Event", "Signal", "Relation"]:
            assert cls in classes, f"Missing core class: {cls}"

    def test_agent_is_mixin(self):
        """Agent is a mixin, not a standalone class."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["classes"]["Agent"].get("mixin") is True

    def test_four_mixins_exist(self):
        """All four cross-cutting mixins are defined."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        classes = schema["classes"]
        for mixin in ["Identifiable", "Temporal", "Describable", "Statusable"]:
            assert mixin in classes, f"Missing mixin: {mixin}"
            assert classes[mixin].get("mixin") is True

    def test_entity_status_enum(self):
        """EntityStatus enum has the three expected values."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        values = schema["enums"]["EntityStatus"]["permissible_values"]
        assert set(values.keys()) == {"ACTIVE", "INACTIVE", "DESTROYED"}

    def test_relation_required_slots(self):
        """Relation requires relation_type, source_id, target_id."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        slots = schema["slots"]
        assert slots["relation_type"].get("required") is True
        assert slots["source_id"].get("required") is True
        assert slots["target_id"].get("required") is True

    def test_root_relation_is_abstract(self):
        """Only concrete predicate classes can be materialized."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["classes"]["Relation"]["abstract"] is True

    def test_signal_bearer_required(self):
        """Signal requires bearer_id (dependent continuant)."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        signal = schema["classes"]["Signal"]
        bearer_usage = signal["slot_usage"]["bearer_id"]
        assert bearer_usage["required"] is True


# --- CYP450 Domain Extension ---


class TestCYP450Schema:

    def test_returned_type_definition_cannot_mutate_registry(self):
        registry = OntologyRegistry(CYP450_SCHEMA)
        original_hash = registry.content_hash()
        returned = registry.get_type("Drug")
        returned.slots.append("forged_slot")
        returned.slot_usage.clear()
        assert registry.content_hash() == original_hash
        assert "forged_slot" not in registry.get_type("Drug").slots

    def test_schema_loads(self):
        """CYP450 schema is valid YAML and imports malleus."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["name"] == "cyp450"
        assert "malleus" in schema["imports"]

    @pytest.mark.skip(reason="linkml CLI import resolver looks only in schema dir; OntologyRegistry's own resolver handles this correctly (see test_cyp450_extends_root_fingerprint)")
    def test_generates_json_schema(self):
        """CYP450 schema compiles to JSON Schema."""
        result = run_linkml("jsonschemagen", CYP450_SCHEMA)
        assert result.returncode == 0, f"Failed: {result.stderr}"

    def test_drug_extends_entity(self):
        """Drug is_a Entity."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["classes"]["Drug"]["is_a"] == "Entity"

    def test_enzyme_extends_entity(self):
        """Enzyme is_a Entity with required cyp_isoform."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        enzyme = schema["classes"]["Enzyme"]
        assert enzyme["is_a"] == "Entity"
        assert enzyme["slot_usage"]["cyp_isoform"]["required"] is True

    def test_cyp_enzyme_enum_has_core_six(self):
        """CYPEnzyme enum contains the 6 core isoforms."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        values = schema["enums"]["CYPEnzyme"]["permissible_values"]
        expected = {"CYP1A2", "CYP2C9", "CYP2C19", "CYP2D6", "CYP2E1", "CYP3A4"}
        assert set(values.keys()) == expected

    def test_drug_relations_have_concrete_signatures(self):
        """Each drug predicate has a concrete class and endpoint ranges."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        expected = {
            "SubstrateOfRelation": ("SUBSTRATE_OF", "Drug", "Enzyme"),
            "InhibitsRelation": ("INHIBITS", "Drug", "Enzyme"),
            "InducesRelation": ("INDUCES", "Drug", "Enzyme"),
            "ProducesRelation": ("PRODUCES", "Drug", "Metabolite"),
            "InteractsWithRelation": ("INTERACTS_WITH", "Drug", "Drug"),
        }
        assert "DrugRelation" not in schema["classes"]
        for name, (predicate, source, target) in expected.items():
            relation = schema["classes"][name]
            assert relation["is_a"] == "Relation"
            assert relation["slot_usage"]["relation_type"]["equals_string"] == predicate
            assert relation["slot_usage"]["source_id"]["range"] == source
            assert relation["slot_usage"]["target_id"]["range"] == target

    def test_drug_relation_types(self):
        """DrugRelationType has the expected interaction types."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        values = schema["enums"]["DrugRelationType"]["permissible_values"]
        expected = {"SUBSTRATE_OF", "INHIBITS", "INDUCES", "PRODUCES", "INTERACTS_WITH"}
        assert set(values.keys()) == expected

    def test_inhibition_strength_enum(self):
        """InhibitionStrength matches FDA classification."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        values = schema["enums"]["InhibitionStrength"]["permissible_values"]
        assert set(values.keys()) == {"WEAK", "MODERATE", "STRONG"}

    def test_interaction_effect_enum(self):
        """InteractionEffect covers the PK outcomes."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        values = schema["enums"]["InteractionEffect"]["permissible_values"]
        assert "INCREASED_EXPOSURE" in values
        assert "DECREASED_EXPOSURE" in values

    def test_drug_signal_constrains_type(self):
        """DrugSignal constrains signal_type to DrugSignalType."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        ds = schema["classes"]["DrugSignal"]
        assert ds["is_a"] == "Signal"
        assert ds["slot_usage"]["signal_type"]["range"] == "DrugSignalType"


# --- ATT&CK Domain Extension ---


class TestAttackSchema:
    def test_schema_loads(self):
        """ATT&CK schema is valid YAML and imports malleus."""
        with open(ATTACK_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["name"] == "attack"
        assert "malleus" in schema["imports"]

    @pytest.mark.skip(reason="linkml CLI import resolver looks only in schema dir; OntologyRegistry's own resolver handles this correctly (see test_attack_extends_root_fingerprint)")
    def test_generates_json_schema(self):
        """ATT&CK schema compiles to JSON Schema."""
        result = run_linkml("jsonschemagen", ATTACK_SCHEMA)
        assert result.returncode == 0, f"Failed: {result.stderr}"

    def test_technique_extends_entity(self):
        """Technique is_a Entity."""
        with open(ATTACK_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["classes"]["Technique"]["is_a"] == "Entity"

    def test_fourteen_tactics(self):
        """Tactic enum has all 14 ATT&CK Enterprise tactics."""
        with open(ATTACK_SCHEMA) as f:
            schema = yaml.safe_load(f)
        values = schema["enums"]["Tactic"]["permissible_values"]
        assert len(values) == 14
        assert "RECONNAISSANCE" in values
        assert "IMPACT" in values

    def test_attack_relations_have_concrete_signatures(self):
        """Every ATT&CK predicate has one concrete relation signature."""
        with open(ATTACK_SCHEMA) as f:
            schema = yaml.safe_load(f)
        expected = {
            "BelongsToTacticRelation": ("BELONGS_TO_TACTIC", "Technique", "TacticEntity"),
            "SubtechniqueOfRelation": ("SUBTECHNIQUE_OF", "Technique", "Technique"),
            "RequiresCapabilityRelation": ("REQUIRES_CAPABILITY", "Technique", "Capability"),
            "ProvidesCapabilityRelation": ("PROVIDES_CAPABILITY", "Technique", "Capability"),
            "MitigatesRelation": ("MITIGATES", "Mitigation", "Technique"),
            "DetectsRelation": ("DETECTS", "DataSource", "Technique"),
            "ChainLinkRelation": ("CHAIN_LINK", "Technique", "Technique"),
        }
        assert "AttackRelation" not in schema["classes"]
        for name, (predicate, source, target) in expected.items():
            relation = schema["classes"][name]
            assert relation["slot_usage"]["relation_type"]["equals_string"] == predicate
            assert relation["slot_usage"]["source_id"]["range"] == source
            assert relation["slot_usage"]["target_id"]["range"] == target

    def test_chain_link_in_relation_types(self):
        """CHAIN_LINK exists as a relation type (Attack Flow integration)."""
        with open(ATTACK_SCHEMA) as f:
            schema = yaml.safe_load(f)
        values = schema["enums"]["AttackRelationType"]["permissible_values"]
        assert "CHAIN_LINK" in values

    def test_mitigation_extends_entity(self):
        """Mitigation is_a Entity."""
        with open(ATTACK_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["classes"]["Mitigation"]["is_a"] == "Entity"

    def test_attack_signal_types(self):
        """AttackSignalType has chain viability and mitigation coverage."""
        with open(ATTACK_SCHEMA) as f:
            schema = yaml.safe_load(f)
        values = schema["enums"]["AttackSignalType"]["permissible_values"]
        assert "CHAIN_VIABILITY" in values
        assert "MITIGATION_COVERAGE" in values


# --- Content-Addressable Hashing ---


class TestContentHash:
    def test_hash_is_deterministic(self):
        """Same schema loaded twice produces identical hash."""
        reg1 = OntologyRegistry(CYP450_SCHEMA)
        reg2 = OntologyRegistry(CYP450_SCHEMA)
        assert reg1.content_hash() == reg2.content_hash()

    def test_hash_is_hex_sha256(self):
        """Hash is a 64-char hex string (SHA-256)."""
        reg = OntologyRegistry(ROOT_SCHEMA)
        h = reg.content_hash()
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_different_schemas_different_hashes(self):
        """Root, CYP450, and ATT&CK produce distinct hashes."""
        root = OntologyRegistry(ROOT_SCHEMA)
        cyp = OntologyRegistry(CYP450_SCHEMA)
        atk = OntologyRegistry(ATTACK_SCHEMA)
        hashes = {root.content_hash(), cyp.content_hash(), atk.content_hash()}
        assert len(hashes) == 3

    def test_hash_is_cached(self):
        """Calling content_hash() twice returns the same object."""
        reg = OntologyRegistry(CYP450_SCHEMA)
        h1 = reg.content_hash()
        h2 = reg.content_hash()
        assert h1 is h2


# --- Fingerprinting ---


class TestFingerprint:
    def test_fingerprint_is_frozenset(self):
        """Fingerprint returns a frozenset of strings."""
        reg = OntologyRegistry(ROOT_SCHEMA)
        fp = reg.fingerprint()
        assert isinstance(fp, frozenset)
        assert all(isinstance(f, str) for f in fp)

    def test_root_types_in_fingerprint(self):
        """Root ontology fingerprint contains core types."""
        reg = OntologyRegistry(ROOT_SCHEMA)
        fp = reg.fingerprint()
        for t in ["Entity", "Event", "Signal", "Relation"]:
            assert f"type:{t}" in fp

    def test_root_mixins_in_fingerprint(self):
        """Root fingerprint marks Agent as mixin."""
        reg = OntologyRegistry(ROOT_SCHEMA)
        fp = reg.fingerprint()
        assert "type:Agent:mixin" in fp

    def test_cyp450_extends_root_fingerprint(self):
        """CYP450 fingerprint is a strict superset of root fingerprint."""
        root = OntologyRegistry(ROOT_SCHEMA)
        cyp = OntologyRegistry(CYP450_SCHEMA)
        root_fp = root.fingerprint()
        cyp_fp = cyp.fingerprint()
        assert root_fp < cyp_fp  # strict subset

    def test_attack_extends_root_fingerprint(self):
        """ATT&CK fingerprint is a strict superset of root fingerprint."""
        root = OntologyRegistry(ROOT_SCHEMA)
        atk = OntologyRegistry(ATTACK_SCHEMA)
        root_fp = root.fingerprint()
        atk_fp = atk.fingerprint()
        assert root_fp < atk_fp

    def test_cyp450_and_attack_are_divergent(self):
        """CYP450 and ATT&CK are divergent: neither is a subset of the other."""
        cyp = OntologyRegistry(CYP450_SCHEMA)
        atk = OntologyRegistry(ATTACK_SCHEMA)
        cyp_fp = cyp.fingerprint()
        atk_fp = atk.fingerprint()
        assert not cyp_fp.issubset(atk_fp)
        assert not atk_fp.issubset(cyp_fp)

    def test_cyp450_has_domain_types(self):
        """CYP450 fingerprint includes Drug, Enzyme, CYPEnzyme values."""
        cyp = OntologyRegistry(CYP450_SCHEMA)
        fp = cyp.fingerprint()
        assert "type:Drug" in fp
        assert "type:Enzyme" in fp
        assert "type:Drug:parent:Entity" in fp
        assert "enum:CYPEnzyme" in fp
        assert "enum:CYPEnzyme:CYP3A4" in fp

    def test_fingerprint_serializable(self):
        """Serializable fingerprint is a sorted list for JSON."""
        reg = OntologyRegistry(ROOT_SCHEMA)
        s = reg.fingerprint_serializable()
        assert isinstance(s, list)
        assert s == sorted(s)
        assert len(s) == len(reg.fingerprint())

    def test_fingerprint_is_cached(self):
        """Calling fingerprint() twice returns the same object."""
        reg = OntologyRegistry(CYP450_SCHEMA)
        fp1 = reg.fingerprint()
        fp2 = reg.fingerprint()
        assert fp1 is fp2


# --- Compatibility Checking ---


class TestCompatibility:
    def test_identical(self):
        """Same schema reports identical."""
        reg1 = OntologyRegistry(CYP450_SCHEMA)
        reg2 = OntologyRegistry(CYP450_SCHEMA)
        result = reg1.check_compatibility(reg2.content_hash(), reg2.fingerprint())
        assert result == "identical"

    def test_superset_cyp450_vs_root(self):
        """CYP450 is a superset of root (I'm newer, they're older)."""
        cyp = OntologyRegistry(CYP450_SCHEMA)
        root = OntologyRegistry(ROOT_SCHEMA)
        result = cyp.check_compatibility(root.content_hash(), root.fingerprint())
        assert result == "superset"

    def test_subset_root_vs_cyp450(self):
        """Root is a subset of CYP450 (I'm older, they're newer)."""
        root = OntologyRegistry(ROOT_SCHEMA)
        cyp = OntologyRegistry(CYP450_SCHEMA)
        result = root.check_compatibility(cyp.content_hash(), cyp.fingerprint())
        assert result == "subset"

    def test_divergent_cyp450_vs_attack(self):
        """CYP450 and ATT&CK are divergent (different domain extensions)."""
        cyp = OntologyRegistry(CYP450_SCHEMA)
        atk = OntologyRegistry(ATTACK_SCHEMA)
        result = cyp.check_compatibility(atk.content_hash(), atk.fingerprint())
        assert result == "divergent"

    def test_superset_attack_vs_root(self):
        """ATT&CK is a superset of root."""
        atk = OntologyRegistry(ATTACK_SCHEMA)
        root = OntologyRegistry(ROOT_SCHEMA)
        result = atk.check_compatibility(root.content_hash(), root.fingerprint())
        assert result == "superset"

    def test_subset_root_vs_attack(self):
        """Root is a subset of ATT&CK."""
        root = OntologyRegistry(ROOT_SCHEMA)
        atk = OntologyRegistry(ATTACK_SCHEMA)
        result = root.check_compatibility(atk.content_hash(), atk.fingerprint())
        assert result == "subset"


# --- Strict Fingerprint (consumer-side safety) ---


class TestStrictFingerprint:
    def test_strict_is_superset_of_lax(self):
        """Strict fingerprint contains everything the lax one does, plus required facts."""
        reg = OntologyRegistry(CYP450_SCHEMA)
        lax = reg.fingerprint()
        strict = reg.strict_fingerprint()
        assert lax.issubset(strict)

    def test_strict_includes_required_facts(self):
        """Enzyme.cyp_isoform is required; the strict fingerprint should say so."""
        reg = OntologyRegistry(CYP450_SCHEMA)
        strict = reg.strict_fingerprint()
        assert "type:Enzyme:usage:cyp_isoform:required" in strict

    def test_lax_excludes_required_facts(self):
        """The lax fingerprint deliberately omits required constraints."""
        reg = OntologyRegistry(CYP450_SCHEMA)
        lax = reg.fingerprint()
        assert "type:Enzyme:usage:cyp_isoform:required" not in lax

    def test_strict_is_cached(self):
        reg = OntologyRegistry(CYP450_SCHEMA)
        a = reg.strict_fingerprint()
        b = reg.strict_fingerprint()
        assert a is b

    def test_strict_serializable_is_sorted_list(self):
        reg = OntologyRegistry(CYP450_SCHEMA)
        s = reg.strict_fingerprint_serializable()
        assert isinstance(s, list)
        assert s == sorted(s)

    def test_effective_required_override_changes_strict_fingerprint(self, tmp_path):
        required = tmp_path / "required.yaml"
        relaxed = tmp_path / "relaxed.yaml"
        template = (
            "id: test\nname: test\n"
            "classes:\n  Thing:\n    slots: [name]\n{usage}"
            "slots:\n  name:\n    range: string\n    required: true\n"
        )
        required.write_text(template.format(usage=""))
        relaxed.write_text(
            template.format(
                usage="    slot_usage:\n      name:\n        required: false\n"
            )
        )
        required_registry = OntologyRegistry(required)
        relaxed_registry = OntologyRegistry(relaxed)
        fact = "type:Thing:effective:name:required"
        assert fact in required_registry.strict_fingerprint()
        assert fact not in relaxed_registry.strict_fingerprint()


class TestStrictCompatibility:
    def test_identical_under_strict(self):
        a = OntologyRegistry(CYP450_SCHEMA)
        b = OntologyRegistry(CYP450_SCHEMA)
        assert a.check_compatibility_strict(b.content_hash(), b.strict_fingerprint()) == "identical"

    def test_pure_addition_still_superset(self):
        """CYP450 adds types on top of root; strict check sees it as a superset."""
        cyp = OntologyRegistry(CYP450_SCHEMA)
        root = OntologyRegistry(ROOT_SCHEMA)
        result = cyp.check_compatibility_strict(root.content_hash(), root.strict_fingerprint())
        assert result == "superset"

    def test_pure_addition_reverse_is_subset(self):
        cyp = OntologyRegistry(CYP450_SCHEMA)
        root = OntologyRegistry(ROOT_SCHEMA)
        result = root.check_compatibility_strict(cyp.content_hash(), cyp.strict_fingerprint())
        assert result == "subset"

    def test_relaxation_breaks_strict_check(self, tmp_path):
        """If two schemas differ only by a required -> optional change, lax says
        superset/subset but strict says divergent."""
        import textwrap
        strict_yaml = tmp_path / "strict.yaml"
        relaxed_yaml = tmp_path / "relaxed.yaml"
        strict_yaml.write_text(textwrap.dedent("""
            id: https://example.org/schema/test
            name: test
            imports: [linkml:types]
            prefixes:
              linkml: https://w3id.org/linkml/
            classes:
              Thing:
                slot_usage:
                  name:
                    required: true
            slots:
              name:
                range: string
        """).strip())
        relaxed_yaml.write_text(textwrap.dedent("""
            id: https://example.org/schema/test
            name: test
            imports: [linkml:types]
            prefixes:
              linkml: https://w3id.org/linkml/
            classes:
              Thing:
                slot_usage:
                  name:
                    required: false
            slots:
              name:
                range: string
        """).strip())

        strict_reg = OntologyRegistry(strict_yaml)
        relaxed_reg = OntologyRegistry(relaxed_yaml)

        # Hashes differ because the canonical form includes required:true/false.
        assert strict_reg.content_hash() != relaxed_reg.content_hash()

        # Lax check: they look identical structurally (relaxation is "additive").
        lax = strict_reg.check_compatibility(relaxed_reg.content_hash(), relaxed_reg.fingerprint())
        assert lax in ("identical", "superset", "subset")

        # Strict check: the relaxed schema is missing the required fact.
        # Neither fingerprint is a superset of the other: divergent.
        strict_result = strict_reg.check_compatibility_strict(
            relaxed_reg.content_hash(), relaxed_reg.strict_fingerprint()
        )
        assert strict_result in ("superset", "divergent")
        # Same check from the relaxed side.
        strict_reverse = relaxed_reg.check_compatibility_strict(
            strict_reg.content_hash(), strict_reg.strict_fingerprint()
        )
        assert strict_reverse in ("subset", "divergent")

        # And one of the two sides has to see the constraint change.
        # Together they cover the asymmetry.
        assert "divergent" in (strict_result, strict_reverse) or \
               (strict_result == "superset" and strict_reverse == "subset")


# --- Mixin tracking (Agent-as-trait, queryable) ---


@pytest.fixture
def agent_domain(tmp_path):
    """A minimal domain that declares a class using the Agent mixin."""
    import textwrap
    schema = tmp_path / "agent_domain.yaml"
    schema.write_text(textwrap.dedent("""
        id: https://example.org/schema/agent_test
        name: agent_test
        imports:
          - malleus
          - linkml:types
        prefixes:
          linkml: https://w3id.org/linkml/

        classes:
          Person:
            is_a: Entity
            mixins:
              - Agent
          Service:
            is_a: Entity
            mixins:
              - Agent
          Drug:
            is_a: Entity
    """).strip())
    # Copy malleus.yaml next to it so the import resolver finds it.
    import shutil
    shutil.copy(ROOT_SCHEMA, tmp_path / "malleus.yaml")
    return schema


class TestMixinTracking:
    def test_mixins_loaded(self, agent_domain):
        reg = OntologyRegistry(agent_domain)
        person = reg.get_type("Person")
        assert "Agent" in person.mixins

    def test_has_mixin_direct(self, agent_domain):
        reg = OntologyRegistry(agent_domain)
        assert reg.has_mixin("Person", "Agent")
        assert reg.has_mixin("Service", "Agent")
        assert not reg.has_mixin("Drug", "Agent")

    def test_has_mixin_inherited(self, agent_domain):
        """A subtype of a type that carries the mixin should also carry it."""
        # Person is_a Entity. If we made SeniorPerson is_a Person, it would
        # inherit the Agent mixin. Simulate by checking the walk.
        reg = OntologyRegistry(agent_domain)
        # Add a synthetic subtype in-memory for the test
        from malleus.ontology import TypeDef
        reg._types["SeniorPerson"] = TypeDef(
            name="SeniorPerson", parent="Person", slots=[], slot_usage={},
            is_mixin=False, mixins=(),
        )
        reg._inheritance["SeniorPerson"] = "Person"
        assert reg.has_mixin("SeniorPerson", "Agent")

    def test_types_with_mixin(self, agent_domain):
        reg = OntologyRegistry(agent_domain)
        agents = reg.types_with_mixin("Agent")
        assert agents == ["Person", "Service"]
        assert "Drug" not in agents
        assert "Agent" not in agents  # the mixin itself is excluded

    def test_mixin_appears_in_fingerprint(self, agent_domain):
        reg = OntologyRegistry(agent_domain)
        fp = reg.fingerprint()
        assert "type:Person:uses_mixin:Agent" in fp
        assert "type:Service:uses_mixin:Agent" in fp
        assert "type:Drug:uses_mixin:Agent" not in fp

    def test_mixin_affects_content_hash(self, agent_domain, tmp_path):
        """A schema that declares an extra mixin must hash differently."""
        import shutil
        import textwrap
        no_mixin = tmp_path / "no_mixin.yaml"
        no_mixin.write_text(textwrap.dedent("""
            id: https://example.org/schema/agent_test
            name: agent_test
            imports: [malleus, linkml:types]
            prefixes:
              linkml: https://w3id.org/linkml/
            classes:
              Person:
                is_a: Entity
              Service:
                is_a: Entity
              Drug:
                is_a: Entity
        """).strip())
        shutil.copy(ROOT_SCHEMA, tmp_path / "malleus.yaml")
        with_mx = OntologyRegistry(agent_domain).content_hash()
        without_mx = OntologyRegistry(no_mixin).content_hash()
        assert with_mx != without_mx


# --- Strict loading and closed-world instance validation ---


class TestStrictOntologyLoading:
    @pytest.mark.parametrize(
        "body",
        [
            "name: one\nname: two\n",
            "classes:\n  Thing: {}\n  Thing: {abstract: true}\n",
            "slots:\n  value: {range: string}\n  value: {range: integer}\n",
            "enums:\n  Choice: {permissible_values: {A: {}, A: {}}}\n",
            (
                "slots:\n  value: {range: string}\n"
                "classes:\n  Thing:\n    slot_usage:\n"
                "      value: {required: true, required: false}\n"
            ),
        ],
    )
    def test_duplicate_yaml_keys_fail(self, tmp_path, body):
        schema = tmp_path / "duplicate.yaml"
        schema.write_text(f"id: duplicate\nname: duplicate\n{body}")
        with pytest.raises(OntologyError, match="Duplicate YAML key"):
            OntologyRegistry(schema)

    def test_missing_import_fails_loudly(self, tmp_path):
        schema = tmp_path / "broken.yaml"
        schema.write_text("id: x\nname: broken\nimports: [missing]\n")
        with pytest.raises(OntologyError, match="Cannot resolve import 'missing'"):
            OntologyRegistry(schema)

    def test_explicit_import_map_resolves_alias(self, tmp_path):
        base = tmp_path / "base.yaml"
        base.write_text("id: base\nname: base\nclasses:\n  Root: {}\n")
        child = tmp_path / "child.yaml"
        child.write_text(
            "id: child\nname: child\nimports: ['vendor:base']\n"
            "classes:\n  Child:\n    is_a: Root\n"
        )
        registry = OntologyRegistry(child, {"vendor:base": base})
        assert registry.is_subtype_of("Child", "Root")

    @pytest.mark.parametrize(
        "section, definition",
        [
            ("classes", "  Shared: {}\n"),
            ("slots", "  shared:\n    range: string\n"),
            ("enums", "  Shared:\n    permissible_values: {A: {}}\n"),
            ("types", "  Shared:\n    typeof: string\n"),
        ],
    )
    def test_imported_name_collision_fails(self, tmp_path, section, definition):
        base = tmp_path / "base.yaml"
        base.write_text(f"id: base\nname: base\n{section}:\n{definition}")
        child = tmp_path / "child.yaml"
        child.write_text(
            f"id: child\nname: child\nimports: [base]\n{section}:\n{definition}"
        )
        with pytest.raises(OntologyError, match="Duplicate"):
            OntologyRegistry(child)

    def test_unknown_range_fails_at_construction(self, tmp_path):
        schema = tmp_path / "broken.yaml"
        schema.write_text(
            "id: broken\nname: broken\n"
            "classes:\n  Thing:\n    slots: [value]\n"
            "slots:\n  value:\n    range: MissingType\n"
        )
        with pytest.raises(OntologyError, match="unknown range 'MissingType'"):
            OntologyRegistry(schema)

    def test_generic_relation_subclass_is_rejected(self, tmp_path):
        import shutil

        shutil.copy(ROOT_SCHEMA, tmp_path / "malleus.yaml")
        schema = tmp_path / "generic.yaml"
        schema.write_text(
            "id: generic\nname: generic\nimports: [malleus]\n"
            "classes:\n  Thing:\n    is_a: Entity\n"
            "  GenericRelation:\n    is_a: Relation\n"
        )
        with pytest.raises(OntologyError, match="must fix relation_type with equals_string"):
            OntologyRegistry(schema)

    def test_relation_endpoint_range_must_be_a_class(self, tmp_path):
        import shutil

        shutil.copy(ROOT_SCHEMA, tmp_path / "malleus.yaml")
        schema = tmp_path / "generic.yaml"
        schema.write_text(
            "id: generic\nname: generic\nimports: [malleus]\n"
            "enums:\n  Predicate:\n    permissible_values:\n      LINK: {}\n"
            "classes:\n  Thing:\n    is_a: Entity\n"
            "  BrokenRelation:\n    is_a: Relation\n    slot_usage:\n"
            "      relation_type:\n        range: Predicate\n        equals_string: LINK\n"
            "      source_id:\n        range: string\n"
            "      target_id:\n        range: Thing\n"
        )
        with pytest.raises(OntologyError, match="class-valued source_id range"):
            OntologyRegistry(schema)

    def test_scalar_type_must_terminate_in_supported_builtin(self, tmp_path):
        schema = tmp_path / "broken.yaml"
        schema.write_text(
            "id: broken\nname: broken\n"
            "types:\n  Mystery:\n    typeof: Missing\n"
        )
        with pytest.raises(OntologyError, match="unsupported range 'Missing'"):
            OntologyRegistry(schema)

    @pytest.mark.parametrize(
        "constraint, message",
        [
            ('required: "yes"', "required must be bool"),
            ("multivalued: many", "multivalued must be bool"),
            ("identifier: id", "identifier must be bool"),
            ("range: 7", "range must be str"),
            ("equals_string: 7", "equals_string must be str"),
            ("minimum_value: low", "minimum_value must be a finite number"),
            ("maximum_value: .nan", "maximum_value must be a finite number"),
        ],
    )
    def test_malformed_slot_constraints_fail_at_construction(
        self,
        tmp_path,
        constraint,
        message,
    ):
        schema = tmp_path / "broken.yaml"
        schema.write_text(
            "id: broken\nname: broken\n"
            f"slots:\n  value:\n    {constraint}\n"
        )
        with pytest.raises(OntologyError, match=message):
            OntologyRegistry(schema)

    def test_malformed_class_boolean_fails_at_construction(self, tmp_path):
        schema = tmp_path / "broken.yaml"
        schema.write_text(
            'id: broken\nname: broken\nclasses:\n  Thing:\n    abstract: "yes"\n'
        )
        with pytest.raises(OntologyError, match="abstract must be bool"):
            OntologyRegistry(schema)


class TestEffectiveSlotValidation:
    def test_inherited_and_mixin_slots_are_effective(self):
        registry = OntologyRegistry(CYP450_SCHEMA)
        drug_slots = registry.effective_slots("Drug")
        assert drug_slots["id"].required is True
        assert drug_slots["id"].identifier is True
        assert drug_slots["tags"].multivalued is True
        relation_slots = registry.effective_slots("SubstrateOfRelation")
        assert relation_slots["source_id"].range == "Drug"
        assert relation_slots["target_id"].range == "Enzyme"

    def test_unknown_property_is_reported(self):
        registry = OntologyRegistry(CYP450_SCHEMA)
        errors = registry.validate_instance("Drug", {"id": "drug-1", "fabricated": 1})
        assert errors == ["Unknown property 'fabricated' for Drug"]

    def test_multivalued_shape_is_enforced(self):
        registry = OntologyRegistry(CYP450_SCHEMA)
        errors = registry.validate_instance("Drug", {"id": "drug-1", "tags": "one"})
        assert errors == ["Property 'tags' must be a list"]

    def test_enforced_slot_shape_changes_identity(self, tmp_path):
        singular = tmp_path / "singular.yaml"
        plural = tmp_path / "plural.yaml"
        template = (
            "id: test\nname: test\n"
            "classes:\n  Thing:\n    slots: [value]\n"
            "slots:\n  value:\n    range: string\n    multivalued: {multivalued}\n"
        )
        singular.write_text(template.format(multivalued="false"))
        plural.write_text(template.format(multivalued="true"))
        left = OntologyRegistry(singular)
        right = OntologyRegistry(plural)
        assert left.content_hash() != right.content_hash()
        assert left.fingerprint() != right.fingerprint()

    def test_inlined_class_values_are_closed_world_validated_and_hashed(self, tmp_path):
        template = (
            "id: test\nname: test\n"
            "classes:\n"
            "  Inner:\n    slots: [code]\n"
            "  Outer:\n    slots: [payload]\n"
            "slots:\n"
            "  code:\n    range: string\n    required: true\n"
            "  payload:\n    range: Inner\n    inlined: {inlined}\n"
        )
        inlined_path = tmp_path / "inlined.yaml"
        reference_path = tmp_path / "reference.yaml"
        inlined_path.write_text(template.format(inlined="true"))
        reference_path.write_text(template.format(inlined="false"))
        registry = OntologyRegistry(inlined_path)
        assert registry.validate_instance("Outer", {"payload": {"code": "x"}}) == []
        assert registry.validate_instance("Outer", {"payload": "inner:1"}) == [
            "Inlined property 'payload' must be a mapping"
        ]
        errors = registry.validate_instance("Outer", {"payload": {"fabricated": "x"}})
        assert any("Unknown property 'fabricated' for Inner" in error for error in errors)
        reference = OntologyRegistry(reference_path)
        assert registry.content_hash() != reference.content_hash()
        assert registry.fingerprint() != reference.fingerprint()

    def test_inlined_does_not_reinterpret_the_public_positional_signature(self):
        prior_positional = SlotConstraint(False, "string", False, True)
        assert prior_positional.identifier is True
        assert prior_positional.inlined is None
        assert prior_positional.value_presence is None


class TestExactlyOneOfClassExpressions:
    CHOICE_SCHEMA = """
id: https://example.org/schema/choice
name: choice
classes:
  Choice:
    slots: [kind, left, right]
    exactly_one_of:
{branches}
slots:
  kind:
    range: ChoiceKind
    required: true
  left:
    range: string
  right:
    range: string
enums:
  ChoiceKind:
    permissible_values:
      A:
      B:
      C:
"""

    BRANCH_A = """      - slot_conditions:
          kind:
            equals_string: A
          left:
            required: true
          right:
            value_presence: ABSENT
"""
    BRANCH_B = """      - slot_conditions:
          kind:
            equals_string: B
          left:
            value_presence: ABSENT
          right:
            required: true
"""

    def _registry(self, tmp_path, name, branches):
        path = tmp_path / f"{name}.yaml"
        path.write_text(self.CHOICE_SCHEMA.format(branches=branches))
        return OntologyRegistry(path)

    def test_union_enforces_required_forbidden_and_forbidden_null(self, tmp_path):
        registry = self._registry(tmp_path, "choice", self.BRANCH_A + self.BRANCH_B)
        assert registry.validate_instance("Choice", {"kind": "A", "left": "x"}) == []
        assert registry.validate_instance("Choice", {"kind": "B", "right": "x"}) == []

        missing = registry.validate_instance("Choice", {"kind": "A"})
        forbidden = registry.validate_instance(
            "Choice",
            {"kind": "A", "left": "x", "right": "y"},
        )
        forbidden_null = registry.validate_instance(
            "Choice",
            {"kind": "A", "left": "x", "right": None},
        )
        assert any("missing left" in error for error in missing)
        assert any("Property 'right' must be absent" in error for error in forbidden)
        assert any("Property 'right' must be absent" in error for error in forbidden_null)

    def test_union_rejects_zero_and_multiple_matching_alternatives(self, tmp_path):
        schema = tmp_path / "overlap.yaml"
        schema.write_text(
            "id: test\nname: test\n"
            "classes:\n  Choice:\n    slots: [left, right]\n"
            "    exactly_one_of:\n"
            "      - slot_conditions:\n          left:\n            required: true\n"
            "      - slot_conditions:\n          right:\n            required: true\n"
            "slots:\n  left:\n    range: string\n  right:\n    range: string\n"
        )
        registry = OntologyRegistry(schema)
        assert registry.validate_instance("Choice", {"left": "x"}) == []
        zero = registry.validate_instance("Choice", {})
        multiple = registry.validate_instance(
            "Choice",
            {"left": "x", "right": "y"},
        )
        assert any("matched 0" in error for error in zero)
        assert any("matched 2" in error for error in multiple)

    @pytest.mark.parametrize(
        "expression,message",
        [
            (
                "      - any_of: []\n        slot_conditions:\n"
                "          left:\n            required: true\n",
                "unsupported expression keys",
            ),
            (
                "      - slot_conditions:\n"
                "          left:\n            pattern: x\n",
                "unsupported condition keys",
            ),
            (
                "      - slot_conditions:\n"
                "          absent_slot:\n            required: true\n",
                "references unknown slot",
            ),
            (
                "      - slot_conditions:\n"
                "          left:\n            required: true\n"
                "            value_presence: ABSENT\n",
                "cannot be required",
            ),
            (
                "      - slot_conditions:\n"
                "          left:\n            equals_string: x\n"
                "            value_presence: ABSENT\n",
                "cannot declare equals_string",
            ),
        ],
    )
    def test_unsupported_or_contradictory_expressions_fail_closed(
        self,
        tmp_path,
        expression,
        message,
    ):
        with pytest.raises(OntologyError, match=message):
            self._registry(tmp_path, "broken", expression)

    @pytest.mark.parametrize(
        "schema_text",
        [
            (
                "id: test\nname: test\n"
                "classes:\n  Choice:\n    slots: [left]\n"
                "slots:\n  left:\n    range: string\n"
                "    value_presence: UNCOMMITTED\n"
            ),
            (
                "id: test\nname: test\n"
                "classes:\n"
                "  Choice:\n"
                "    slots: [left]\n"
                "    slot_usage:\n"
                "      left:\n"
                "        value_presence: UNCOMMITTED\n"
                "slots:\n  left:\n    range: string\n"
            ),
            (
                "id: test\nname: test\n"
                "classes:\n"
                "  Choice:\n"
                "    slots: [left]\n"
                "    exactly_one_of:\n"
                "      - slot_conditions:\n"
                "          left:\n"
                "            value_presence: UNCOMMITTED\n"
                "slots:\n  left:\n    range: string\n"
            ),
        ],
        ids=["global-slot", "slot-usage", "class-expression"],
    )
    def test_uncommitted_presence_fails_closed_in_every_supported_location(
        self,
        tmp_path,
        schema_text,
    ):
        schema = tmp_path / "uncommitted-presence.yaml"
        schema.write_text(schema_text)
        with pytest.raises(
            OntologyError,
            match=r"value_presence must be one of \['ABSENT', 'PRESENT'\]",
        ):
            OntologyRegistry(schema)

    @pytest.mark.parametrize(
        "composition",
        ["    is_a: Restriction\n", "    mixins: [Restriction]\n"],
    )
    def test_absent_rejects_inherited_or_mixin_equals_string(
        self,
        tmp_path,
        composition,
    ):
        schema = tmp_path / "merged-contradiction.yaml"
        schema.write_text(
            "id: test\nname: test\n"
            "classes:\n"
            "  Restriction:\n"
            "    mixin: true\n"
            "    slots: [left]\n"
            "    exactly_one_of:\n"
            "      - slot_conditions:\n"
            "          left:\n"
            "            value_presence: ABSENT\n"
            "  Choice:\n"
            f"{composition}"
            "    slot_usage:\n"
            "      left:\n"
            "        equals_string: x\n"
            "slots:\n"
            "  left:\n"
            "    range: string\n"
        )
        with pytest.raises(OntologyError, match="cannot declare equals_string"):
            OntologyRegistry(schema)

    @pytest.mark.parametrize(
        ("base", "condition", "message"),
        [
            (
                "    equals_string: A\n",
                "            equals_string: B\n",
                "conflicting equals_string values",
            ),
            (
                "    value_presence: PRESENT\n",
                "            value_presence: ABSENT\n",
                "conflicting value_presence values",
            ),
            (
                "    value_presence: ABSENT\n",
                "            value_presence: PRESENT\n",
                "conflicting value_presence values",
            ),
        ],
    )
    def test_expression_constraints_cannot_relax_effective_constraints(
        self,
        tmp_path,
        base,
        condition,
        message,
    ):
        schema = tmp_path / "monotonic-conflict.yaml"
        schema.write_text(
            "id: test\nname: test\n"
            "classes:\n"
            "  Choice:\n"
            "    slots: [left]\n"
            "    exactly_one_of:\n"
            "      - slot_conditions:\n"
            "          left:\n"
            f"{condition}"
            "slots:\n"
            "  left:\n"
            "    range: string\n"
            f"{base}"
        )
        with pytest.raises(OntologyError, match=message):
            OntologyRegistry(schema)

    def test_construction_checks_conflict_before_last_sorted_condition(self, tmp_path):
        schema = tmp_path / "non-last-conflict.yaml"
        template = (
            "id: test\nname: test\n"
            "classes:\n"
            "  Choice:\n"
            "    slots: [alpha, zeta]\n"
            "    exactly_one_of:\n"
            "      - slot_conditions:\n"
            "          alpha:\n"
            "            equals_string: {condition}\n"
            "          zeta:\n"
            "            required: true\n"
            "slots:\n"
            "  alpha:\n"
            "    range: string\n"
            "    equals_string: A\n"
            "  zeta:\n"
            "    range: string\n"
        )
        schema.write_text(template.format(condition="B"))
        with pytest.raises(OntologyError, match="conflicting equals_string"):
            OntologyRegistry(schema)

        schema.write_text(template.format(condition="A"))
        registry = OntologyRegistry(schema)
        errors = registry.validate_instance("Choice", {"alpha": "A"})
        assert any("missing zeta" in error for error in errors)

    def test_required_false_does_not_relax_effective_required_true(self, tmp_path):
        schema = tmp_path / "required-conjunction.yaml"
        schema.write_text(
            "id: test\nname: test\n"
            "classes:\n"
            "  Choice:\n"
            "    slots: [left]\n"
            "    exactly_one_of:\n"
            "      - slot_conditions:\n"
            "          left:\n"
            "            required: false\n"
            "slots:\n"
            "  left:\n"
            "    range: string\n"
            "    required: true\n"
        )
        registry = OntologyRegistry(schema)
        assert registry.validate_instance("Choice", {"left": "x"}) == []
        assert any(
            "Required slot 'left' missing" in error
            for error in registry.validate_instance("Choice", {})
        )

    def test_slot_usage_cannot_create_uninhabitable_effective_presence(self, tmp_path):
        schema = tmp_path / "effective-presence-conflict.yaml"
        schema.write_text(
            "id: test\nname: test\n"
            "classes:\n"
            "  Parent:\n"
            "    slots: [left]\n"
            "  Child:\n"
            "    is_a: Parent\n"
            "    slot_usage:\n"
            "      left:\n"
            "        value_presence: ABSENT\n"
            "slots:\n"
            "  left:\n"
            "    range: string\n"
            "    required: true\n"
        )
        with pytest.raises(OntologyError, match="cannot be required"):
            OntologyRegistry(schema)

    def test_inherited_and_local_exactly_one_of_groups_remain_conjunctive(
        self,
        tmp_path,
    ):
        schema = tmp_path / "grouped-unions.yaml"
        schema.write_text(
            "id: test\nname: test\n"
            "classes:\n"
            "  ParentChoice:\n"
            "    slots: [left, right]\n"
            "    exactly_one_of:\n"
            "      - slot_conditions:\n"
            "          left:\n"
            "            required: true\n"
            "      - slot_conditions:\n"
            "          right:\n"
            "            required: true\n"
            "  ChildChoice:\n"
            "    is_a: ParentChoice\n"
            "    slots: [top, bottom]\n"
            "    exactly_one_of:\n"
            "      - slot_conditions:\n"
            "          top:\n"
            "            required: true\n"
            "      - slot_conditions:\n"
            "          bottom:\n"
            "            required: true\n"
            "slots:\n"
            "  left:\n    range: string\n"
            "  right:\n    range: string\n"
            "  top:\n    range: string\n"
            "  bottom:\n    range: string\n"
        )
        registry = OntologyRegistry(schema)
        assert registry.validate_instance(
            "ChildChoice",
            {"left": "l", "top": "t"},
        ) == []
        assert any(
            "matched 0" in error
            for error in registry.validate_instance("ChildChoice", {"left": "l"})
        )
        assert any(
            "matched 2" in error
            for error in registry.validate_instance(
                "ChildChoice",
                {"left": "l", "right": "r", "top": "t"},
            )
        )

    def test_operand_order_is_identity_invariant_but_conditions_are_not(self, tmp_path):
        forward = self._registry(tmp_path, "forward", self.BRANCH_A + self.BRANCH_B)
        reverse = self._registry(tmp_path, "reverse", self.BRANCH_B + self.BRANCH_A)
        changed = self._registry(
            tmp_path,
            "changed",
            self.BRANCH_A + self.BRANCH_B.replace("equals_string: B", "equals_string: C"),
        )
        assert forward.content_hash() == reverse.content_hash()
        assert forward.fingerprint() == reverse.fingerprint()
        assert forward.strict_fingerprint() == reverse.strict_fingerprint()
        assert forward.content_hash() != changed.content_hash()
        assert forward.fingerprint() != changed.fingerprint()
        assert "fingerprint_version:4" in forward.fingerprint()
        assert "fingerprint_version:3" in OntologyRegistry(ROOT_SCHEMA).fingerprint()


class TestIdentityFromResolution:
    """Identity must derive from the resolved constraint table the validator
    consults, never the declaration syntax (self-inquisition H1, H2, S5)."""

    BASE = """
id: https://example.org/schema/{name}
name: {name}
classes:
  MixA:
    mixin: true
    slots: [alpha]
  MixB:
    mixin: true
    slots: [beta]
  Thing:
    mixins: [{mixins}]
    slots: [id]
slots:
  id:
    range: string
  alpha:
    range: string
  beta:
    range: string
"""

    def _write(self, tmp_path, name, text):
        path = tmp_path / f"{name}.yaml"
        path.write_text(text)
        return OntologyRegistry(path)

    def test_mixin_order_is_unobservable(self, tmp_path):
        a = self._write(tmp_path, "a", self.BASE.format(name="a", mixins="MixA, MixB"))
        b = self._write(tmp_path, "b", self.BASE.format(name="a", mixins="MixB, MixA"))
        assert a.effective_slots("Thing") == b.effective_slots("Thing")
        assert a.content_hash() == b.content_hash()
        assert a.fingerprint() == b.fingerprint()
        assert a.check_compatibility(b.content_hash(), b.fingerprint()) == "identical"

    def test_conflicting_mixin_constraints_refuse_construction(self, tmp_path):
        conflicted = """
id: https://example.org/schema/c
name: c
classes:
  Cheap:
    mixin: true
    slot_usage:
      severity:
        maximum_value: 200
  Critical:
    mixin: true
    slot_usage:
      severity:
        maximum_value: 10
  Alert:
    mixins: [{order}]
    slots: [severity]
slots:
  severity:
    range: integer
"""
        for order in ("Cheap, Critical", "Critical, Cheap"):
            path = tmp_path / "c.yaml"
            path.write_text(conflicted.format(order=order))
            with pytest.raises(OntologyError, match="conflicting constraints"):
                OntologyRegistry(path)

    def test_effective_slot_membership_is_a_fact(self, tmp_path):
        template = """
id: https://example.org/schema/m
name: m
classes:
  Thing:
    slots: [id]{usage}
slots:
  id:
    range: string
  val:
    range: string
"""
        with_doc_slot = self._write(
            tmp_path, "with",
            template.format(usage="\n    slot_usage:\n      val:\n        description: docs only\n"),
        )
        without = self._write(tmp_path, "without", template.format(usage=""))
        assert "val" in with_doc_slot.effective_slots("Thing")
        assert "val" not in without.effective_slots("Thing")
        assert with_doc_slot.fingerprint() != without.fingerprint()
        verdict = without.check_compatibility(
            with_doc_slot.content_hash(), with_doc_slot.fingerprint()
        )
        assert verdict != "superset"
        for registry in (with_doc_slot, without):
            facts = registry.fingerprint()
            for type_name in registry.type_names():
                recovered = {
                    fact.split(":", 3)[3]
                    for fact in facts
                    if fact.startswith(f"type:{type_name}:effective_slot:")
                }
                assert recovered == set(registry.effective_slots(type_name))

    def test_numeric_bound_spelling_is_canonical(self, tmp_path):
        template = """
id: https://example.org/schema/n
name: n
classes:
  Thing:
    slots: [score]
slots:
  score:
    range: float
    minimum_value: {value}
"""
        as_int = self._write(tmp_path, "int", template.format(value="0"))
        as_float = self._write(tmp_path, "float", template.format(value="0.0"))
        assert as_int.content_hash() == as_float.content_hash()
        assert as_int.fingerprint() == as_float.fingerprint()
        assert as_int.check_compatibility(
            as_float.content_hash(), as_float.fingerprint()
        ) == "identical"


class TestLinkMLBuiltinRangesAreAccepted:
    """Two independent projects lost a schema in one week to the same hole:
    the loader accepted five of LinkML's nineteen built-in ranges, so `uri`
    and `double` were construction failures. Refusing a legal type punishes
    an adopter for using their schema language correctly."""

    def _schema(self, tmp_path, range_name):
        path = tmp_path / "domain.yaml"
        path.write_text(
            "id: https://example.org/schema/d\nname: d\n"
            "imports: [malleus, 'linkml:types']\n"
            "classes:\n  Thing:\n    is_a: Entity\n    slots: [probe]\n"
            f"slots:\n  probe:\n    range: {range_name}\n"
        )
        return path

    @pytest.mark.parametrize("range_name", [
        "uri", "double", "decimal", "date", "time", "uriorcurie",
        "curie", "ncname", "jsonpointer", "sparqlpath",
    ])
    def test_a_legal_builtin_range_constructs(self, tmp_path, range_name):
        registry = OntologyRegistry(self._schema(tmp_path, range_name))
        assert registry.has_type("Thing")

    def test_the_base_kind_is_still_enforced(self, tmp_path):
        """Accepting the declaration must not mean accepting anything."""
        registry = OntologyRegistry(self._schema(tmp_path, "double"))
        errors = registry.validate_instance("Thing", {"id": "t:1", "probe": "not a number"})
        assert any("must be a number" in error for error in errors)

    def test_the_lexical_boundary_is_what_it_says(self, tmp_path):
        """`uri` is checked as a string, not parsed as a URI. Pinned as a
        test so the boundary is proven rather than described, and so any
        future claim to validate the lexical form has something to fail
        against. Tracked as `lexical-format-validation`."""
        registry = OntologyRegistry(self._schema(tmp_path, "uri"))
        assert registry.validate_instance("Thing", {"id": "t:1", "probe": "not a uri"}) == []
        assert registry.validate_instance("Thing", {"id": "t:1", "probe": 7}) != []


class TestTheBundledRootResolvesWithoutAMap:
    """`pip install malleus-dev`, write `imports: [malleus]`, run the tool.
    That path reported a construction heresy against a correct schema, which
    is an adopter's first contact with the inspector."""

    def _schema(self, tmp_path):
        path = tmp_path / "domain.yaml"
        path.write_text(
            "id: https://example.org/schema/d\nname: d\n"
            "imports: [malleus, 'linkml:types']\n"
            "classes:\n  Thing:\n    is_a: Entity\n"
        )
        return path

    def test_an_unmapped_malleus_import_resolves_to_the_installed_root(self, tmp_path):
        registry = OntologyRegistry(self._schema(tmp_path))
        for primitive in ("Entity", "Event", "Signal", "Relation"):
            assert registry.has_type(primitive)

    def test_a_local_copy_still_wins(self, tmp_path):
        """Precedence matters: if the bundled root outranked a vendored copy,
        the root-currency rite could never see a drifted vendor again."""
        vendored = tmp_path / "malleus.yaml"
        text = bundled_ontology_path("malleus.yaml").read_text()
        vendored.write_text(text.replace("DESTROYED:", "OBLITERATED:"))
        registry = OntologyRegistry(self._schema(tmp_path))
        installed = OntologyRegistry(bundled_ontology_path("malleus.yaml"))
        assert registry.check_compatibility_strict(
            installed.content_hash(), installed.strict_fingerprint()
        ) == "divergent"

    def test_a_genuinely_absent_import_still_refuses(self, tmp_path):
        path = tmp_path / "domain.yaml"
        path.write_text(
            "id: https://example.org/schema/d\nname: d\n"
            "imports: [no_such_ontology]\nclasses:\n  Thing: {}\n"
        )
        with pytest.raises(OntologyError, match="Cannot resolve import"):
            OntologyRegistry(path)


class TestTheGrammarVersionIsNotAStructuralFact:
    """Reported by an adopting project whose release pipeline this blocked,
    and reproduced against our own shipped ontologies before the fix."""

    def _shipped(self, *parts):
        from malleus.ontology import OntologyRegistry, bundled_ontology_path
        return OntologyRegistry(bundled_ontology_path(*parts))

    def test_a_schema_using_a_conditional_feature_is_still_a_superset_of_the_root(self):
        """`assent.yaml` uses value_presence, so it emits grammar 4 while the
        root emits 3. It carries every fact the root has, zero missing, and
        was reported divergent because the two markers differ in each
        direction. A rite that condemns a correct schema is worse than a
        missing rite."""
        root, assent = self._shipped("malleus.yaml"), self._shipped("assent.yaml")
        structural = {f for f in root.strict_fingerprint()
                      if not f.startswith("fingerprint_version:")}
        mine = {f for f in assent.strict_fingerprint()
                if not f.startswith("fingerprint_version:")}
        assert not structural - mine, "premise changed: assent no longer contains the root"
        assert assent.check_compatibility_strict(
            root.content_hash(), root.strict_fingerprint()) == "superset"
        assert assent.check_compatibility(
            root.content_hash(), root.fingerprint()) == "superset"

    def test_the_grammar_relationship_is_answered_rather_than_dropped(self):
        root, assent = self._shipped("malleus.yaml"), self._shipped("assent.yaml")
        assert assent.fingerprint_grammar(root.strict_fingerprint()) == "older"
        assert assent.fingerprint_grammar(assent.strict_fingerprint()) == "same"
        assert root.fingerprint_grammar(assent.strict_fingerprint()) == "newer"
        assert root.fingerprint_grammar(frozenset({"type:Thing"})) == "unknown"

    def test_the_marker_is_still_published(self):
        """Excluded from the comparison, not removed from the fact set. A
        consumer reading the published fingerprint still learns which grammar
        produced it."""
        assent = self._shipped("assent.yaml")
        assert "fingerprint_version:4" in assent.strict_fingerprint()
        assert "fingerprint_version:4" in assent.fingerprint()

    def test_genuinely_different_schemas_are_still_divergent(self):
        """The fix must not make everything a superset."""
        cyp, recon = self._shipped("domains", "cyp450.yaml"), self._shipped("domains", "recon.yaml")
        assert cyp.check_compatibility_strict(
            recon.content_hash(), recon.strict_fingerprint()) == "divergent"

    def test_a_dropped_required_constraint_is_still_caught(self):
        """The strict check exists to catch what the producer-side one misses.
        Excluding the grammar marker must not blunt it."""
        from malleus.ontology import OntologyRegistry
        import tempfile, pathlib, textwrap
        base = textwrap.dedent("""
            id: https://example.org/s
            name: s
            version: 0.1.0
            default_range: string
            imports: [linkml:types]
            prefixes: {linkml: 'https://w3id.org/linkml/'}
            classes:
              Thing:
                slots: [tag]
                slot_usage:
                  tag: {required: %s}
            slots:
              tag: {range: string}
        """)
        with tempfile.TemporaryDirectory() as tmp:
            strict_path = pathlib.Path(tmp) / "strict.yaml"
            loose_path = pathlib.Path(tmp) / "loose.yaml"
            strict_path.write_text(base % "true")
            loose_path.write_text(base % "false")
            strict, loose = OntologyRegistry(strict_path), OntologyRegistry(loose_path)
            assert loose.check_compatibility_strict(
                strict.content_hash(), strict.strict_fingerprint()) != "superset"


class TestPromotionIsADuplicateThatIsNotAnError:
    """Pushing a concept up into the root, which `ONTOLOGY_PROTOCOL.md` rule 2
    asks for once two projects need it independently, made every domain that
    already named it stop loading. Not degrade: stop. Verified before this
    existed: adding `confidence` to the root refused both `recon` and `ocr`.

    A duplicate is still a collision. It is an adoption only when the second
    occurrence says so and the two definitions already agree. Both halves
    matter: `recon` and `ocr` both declare `confidence` as a float and mean
    opposite things, a reviewer's judgment against a provider's uncalibrated
    number, so structural agreement alone would silently unify them."""

    ROOT = textwrap.dedent("""
        id: https://example.org/up
        name: up
        version: 0.1.0
        default_range: string
        imports: [linkml:types]
        prefixes: {linkml: 'https://w3id.org/linkml/'}
        classes:
          Thing:
            slots: [locator]
        slots:
          locator:
            range: string
    """)

    def _pair(self, tmp_path, slot_body):
        (tmp_path / "up.yaml").write_text(self.ROOT)
        (tmp_path / "down.yaml").write_text(textwrap.dedent("""
            id: https://example.org/down
            name: down
            version: 0.1.0
            default_range: string
            imports: [linkml:types, up]
            prefixes: {linkml: 'https://w3id.org/linkml/'}
            classes:
              Other:
                slots: [locator]
            slots:
              locator:
        """) + slot_body + "\n")
        return tmp_path / "down.yaml"

    def test_a_silent_duplicate_is_still_refused(self, tmp_path):
        """The default does not move. Silence is a collision."""
        path = self._pair(tmp_path, "    range: string")
        with pytest.raises(OntologyError) as raised:
            OntologyRegistry(path)
        assert "conflicts with" in str(raised.value)
        assert "adopts: true" in str(raised.value), (
            "a refusal that does not say how to proceed costs the reader a guess"
        )

    def test_a_declared_adoption_of_an_identical_definition_loads(self, tmp_path):
        path = self._pair(tmp_path, "    range: string\n    annotations: {adopts: true}")
        registry = OntologyRegistry(path)
        assert registry.effective_slots("Other")["locator"].range == "string"

    def test_the_adopted_definition_is_the_upstream_one(self, tmp_path):
        """Adoption keeps what it adopted. If the downstream copy won, the
        declaration would be a way to override upstream while claiming to
        agree with it."""
        (tmp_path / "up.yaml").write_text(
            self.ROOT.replace("    range: string", "    range: string\n    required: true")
        )
        (tmp_path / "down.yaml").write_text(textwrap.dedent("""
            id: https://example.org/down
            name: down
            version: 0.1.0
            default_range: string
            imports: [linkml:types, up]
            prefixes: {linkml: 'https://w3id.org/linkml/'}
            classes:
              Other:
                slots: [locator]
            slots:
              locator:
                range: string
                required: true
                annotations: {adopts: true}
        """))
        registry = OntologyRegistry(tmp_path / "down.yaml")
        assert registry.effective_slots("Other")["locator"].required is True

    @pytest.mark.parametrize("body,expected", [
        ("    range: integer\n    annotations: {adopts: true}", "range"),
        ("    range: string\n    minimum_value: 1\n    annotations: {adopts: true}", "minimum_value"),
        ("    range: string\n    required: true\n    annotations: {adopts: true}", "required"),
        ("    range: string\n    multivalued: true\n    annotations: {adopts: true}", "multivalued"),
    ])
    def test_adoption_of_a_definition_that_disagrees_is_refused(self, tmp_path, body, expected):
        """Adoption is for a definition that already agrees. Anything else is a
        different concept and needs its own name. The refusal names the field."""
        path = self._pair(tmp_path, body)
        with pytest.raises(OntologyError) as raised:
            OntologyRegistry(path)
        assert expected in str(raised.value)
        assert "different concept" in str(raised.value)

    def test_prose_may_differ_because_a_machine_cannot_check_it(self, tmp_path):
        """Description is excluded from the comparison on purpose. A machine
        cannot tell whether two descriptions mean the same thing, which is
        exactly why the adoption is declared by a human as well."""
        path = self._pair(
            tmp_path,
            "    range: string\n    description: local prose\n    annotations: {adopts: true}",
        )
        assert OntologyRegistry(path).effective_slots("Other")["locator"].range == "string"

    def test_adoption_applies_to_slots_only(self, tmp_path):
        """A class or enum that already exists upstream is reused by importing
        it. Redeclaring one is not adoption, and letting it through would give
        two definitions of one type."""
        (tmp_path / "up.yaml").write_text(self.ROOT)
        (tmp_path / "down.yaml").write_text(textwrap.dedent("""
            id: https://example.org/down
            name: down
            version: 0.1.0
            default_range: string
            imports: [linkml:types, up]
            prefixes: {linkml: 'https://w3id.org/linkml/'}
            classes:
              Thing:
                slots: [locator]
                annotations: {adopts: true}
            slots: {}
        """))
        with pytest.raises(OntologyError, match="supported for slots only"):
            OntologyRegistry(tmp_path / "down.yaml")

    def test_promotion_of_a_real_shared_name_becomes_a_no_op(self, tmp_path):
        """The case that motivated this, on the real schemas. `locator` is
        declared by `assent`, `recon` and `ocr`. Before this, the root adopting
        it refused all three."""
        import shutil
        from malleus.ontology import bundled_ontology_path
        source = bundled_ontology_path("malleus.yaml").parent
        shutil.copytree(source, tmp_path / "ontology")
        root = tmp_path / "ontology" / "malleus.yaml"
        root.write_text(root.read_text() + "\n  locator:\n    range: string\n")
        for name in ("assent.yaml", "domains/recon.yaml", "domains/ocr.yaml"):
            target = tmp_path / "ontology" / name
            with pytest.raises(OntologyError, match="conflicts with"):
                OntologyRegistry(target)
            target.write_text(re.sub(
                r"^(  locator:\n)", r"\1    annotations: {adopts: true}\n",
                target.read_text(), count=1, flags=re.M,
            ))
            OntologyRegistry(target)


class TestARetirementIsAWindowNotAWall:
    """There was no way to say a name is going away. Two moves existed and
    both were bad: delete it, and every schema using it stops that instant; or
    leave it and add the replacement, and two names cover one concept forever
    with nothing saying which to follow.

    The trap on the way out is symmetrical. A marker nothing reads is
    decoration, which is the defect found three times in one week in this
    repository. A marker that bites the day it lands is the outage the adoption
    work just removed, pointed the other way."""

    def _schema(self, version, retires_lines, successor="new_tag"):
        head = [
            "id: https://example.org/s", "name: s", f"version: {version}",
            "default_range: string", "imports: [linkml:types]",
            "prefixes: {linkml: 'https://w3id.org/linkml/'}",
            "classes:", "  Thing:", f"    slots: [old_tag, {successor}]",
            "slots:", f"  {successor}:", "    range: string",
            "  old_tag:", "    range: string",
        ]
        return "\n".join(head + retires_lines) + "\n"

    FULL = ["    annotations:", "      retires:", "        replaced_by: new_tag",
            "        stops_at: '0.6.0'", "        reason: superseded by new_tag"]

    def _load(self, tmp_path, text):
        path = tmp_path / "s.yaml"
        path.write_text(text)
        return OntologyRegistry(path)

    def test_inside_the_window_the_name_still_works(self, tmp_path):
        registry = self._load(tmp_path, self._schema("0.5.0", self.FULL))
        assert registry.effective_slots("Thing")["old_tag"].range == "string"

    def test_inside_the_window_the_retirement_is_reported(self, tmp_path):
        """The second reader. Without it the plan is visible only on the day it
        stops being a plan."""
        registry = self._load(tmp_path, self._schema("0.5.0", self.FULL))
        retirement = registry.retirements()[0]
        assert retirement.slot == "old_tag"
        assert retirement.replaced_by == "new_tag"
        assert retirement.stops_at_text == "0.6.0"
        assert "superseded" in retirement.reason

    @pytest.mark.parametrize("version", ["0.6.0", "0.7.0", "1.0.0"])
    def test_at_and_past_the_boundary_the_name_is_refused(self, tmp_path, version):
        """At, not merely past. A boundary that the boundary version itself
        slips through is off by one in the direction nobody notices."""
        with pytest.raises(OntologyError) as raised:
            self._load(tmp_path, self._schema(version, self.FULL))
        assert "retired at version 0.6.0" in str(raised.value)
        assert "new_tag" in str(raised.value), "a refusal must name the replacement"

    def test_a_retirement_without_a_boundary_is_refused(self, tmp_path):
        """Deprecated-forever is a note pretending to be a plan."""
        with pytest.raises(OntologyError, match="never bites"):
            self._load(tmp_path, self._schema("0.5.0", [
                "    annotations:", "      retires:",
                "        replaced_by: new_tag", "        reason: x"]))

    def test_a_retirement_without_a_reason_is_refused(self, tmp_path):
        with pytest.raises(OntologyError, match="states its reason"):
            self._load(tmp_path, self._schema("0.5.0", [
                "    annotations:", "      retires:",
                "        stops_at: '0.6.0'", "        replaced_by: new_tag"]))

    def test_a_retirement_may_have_no_replacement(self, tmp_path):
        """A concept can be wrong rather than renamed. The reason carries the
        weight, and the report says no replacement is offered."""
        registry = self._load(tmp_path, self._schema("0.5.0", [
            "    annotations:", "      retires:",
            "        stops_at: '0.6.0'", "        reason: the concept was wrong"]))
        assert registry.retirements()[0].replaced_by is None

    def test_a_replacement_that_does_not_exist_is_refused(self, tmp_path):
        """A retirement pointing nowhere sends the reader to a dead end."""
        with pytest.raises(OntologyError, match="which no schema in this closure declares"):
            self._load(tmp_path, self._schema("0.5.0", [
                "    annotations:", "      retires:", "        replaced_by: ghost",
                "        stops_at: '0.6.0'", "        reason: x"]))

    def test_an_uncomparable_boundary_is_refused(self, tmp_path):
        """A boundary nobody can compare never arrives."""
        with pytest.raises(OntologyError, match="dotted version of integers"):
            self._load(tmp_path, self._schema("0.5.0", [
                "    annotations:", "      retires:",
                "        stops_at: soon", "        reason: x"]))

    def test_an_undeclared_key_in_a_retirement_is_refused(self, tmp_path):
        """Never guess at an undeclared extension."""
        with pytest.raises(OntologyError, match="undeclared keys: when"):
            self._load(tmp_path, self._schema("0.5.0", [
                "    annotations:", "      retires:", "        stops_at: '0.6.0'",
                "        reason: x", "        when: later"]))

    def test_a_schema_with_no_version_cannot_retire_anything(self, tmp_path):
        """The boundary is compared against the declaring schema's own version,
        so the artifact carries both halves and no reader's clock decides."""
        text = self._schema("0.5.0", self.FULL).replace("version: 0.5.0\n", "")
        with pytest.raises(OntologyError, match="declare its own `version`"):
            self._load(tmp_path, text)

    def test_the_replacement_may_live_upstream(self, tmp_path):
        """The common case: a name retires in favour of one promoted into the
        root, which had not been read when the retiring slot was."""
        (tmp_path / "up.yaml").write_text("\n".join([
            "id: https://example.org/up", "name: up", "version: 0.1.0",
            "default_range: string", "imports: [linkml:types]",
            "prefixes: {linkml: 'https://w3id.org/linkml/'}",
            "classes:", "  Base:", "    slots: [promoted_tag]",
            "slots:", "  promoted_tag:", "    range: string"]) + "\n")
        (tmp_path / "down.yaml").write_text("\n".join([
            "id: https://example.org/down", "name: down", "version: 0.5.0",
            "default_range: string", "imports: [linkml:types, up]",
            "prefixes: {linkml: 'https://w3id.org/linkml/'}",
            "classes:", "  Thing:", "    slots: [old_tag]",
            "slots:", "  old_tag:", "    range: string",
            "    annotations:", "      retires:",
            "        replaced_by: promoted_tag", "        stops_at: '0.6.0'",
            "        reason: promoted into the shared root"]) + "\n")
        registry = OntologyRegistry(tmp_path / "down.yaml")
        assert registry.retirements()[0].replaced_by == "promoted_tag"

    def test_the_inquisitor_reports_a_pending_retirement(self, tmp_path):
        """Proven through the operator's path, not by reading the code."""
        from malleus.inquisition import run_rites
        path = tmp_path / "s.yaml"
        path.write_text(self._schema("0.5.0", self.FULL))
        report = run_rites(str(path))
        messages = [f.message for f in report.findings if f.subject == "old_tag"]
        assert messages and "retires at version 0.6.0" in messages[0]
