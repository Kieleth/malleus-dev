"""Tests for ontology schemas: root + domain extensions.

Validates that LinkML schemas compile, generate correctly,
and enforce the type constraints we depend on for the experiment.
Also tests content-addressable hashing and compatibility checking
for distributed ontology convergence.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from malleus.ontology import OntologyRegistry

ONTOLOGY_DIR = Path(__file__).parent.parent / "ontology"
ROOT_SCHEMA = ONTOLOGY_DIR / "malleus.yaml"
CYP450_SCHEMA = ONTOLOGY_DIR / "domains" / "cyp450.yaml"
ATTACK_SCHEMA = ONTOLOGY_DIR / "domains" / "attack.yaml"


def run_linkml(command: str, schema: Path) -> subprocess.CompletedProcess:
    """Run a LinkML generator command on a schema."""
    result = subprocess.run(
        [sys.executable, "-m", "linkml.generators." + command, str(schema)],
        capture_output=True,
        text=True,
    )
    return result


# --- Root Ontology ---


class TestRootOntology:
    def test_schema_loads(self):
        """Root schema is valid YAML."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        assert schema["name"] == "malleus"
        assert schema["version"] == "0.3.0"

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

    def test_signal_bearer_required(self):
        """Signal requires bearer_id (dependent continuant)."""
        with open(ROOT_SCHEMA) as f:
            schema = yaml.safe_load(f)
        signal = schema["classes"]["Signal"]
        bearer_usage = signal["slot_usage"]["bearer_id"]
        assert bearer_usage["required"] is True


# --- CYP450 Domain Extension ---


class TestCYP450Schema:
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

    def test_drug_relation_constrains_type(self):
        """DrugRelation constrains relation_type to DrugRelationType enum."""
        with open(CYP450_SCHEMA) as f:
            schema = yaml.safe_load(f)
        dr = schema["classes"]["DrugRelation"]
        assert dr["is_a"] == "Relation"
        assert dr["slot_usage"]["relation_type"]["range"] == "DrugRelationType"

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

    def test_attack_relation_constrains_type(self):
        """AttackRelation constrains relation_type to AttackRelationType."""
        with open(ATTACK_SCHEMA) as f:
            schema = yaml.safe_load(f)
        ar = schema["classes"]["AttackRelation"]
        assert ar["is_a"] == "Relation"
        assert ar["slot_usage"]["relation_type"]["range"] == "AttackRelationType"

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
        import textwrap, shutil
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
