"""Rites of the Ordo Malleus: each mechanical rite proven on a real schema."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from malleus.inquisition import (
    HERESY,
    NOTE,
    SUSPICION,
    RubricError,
    _formula_tokens,
    _rubric,
    run_rites,
)
from malleus.inquisition.cli import main
from malleus.ontology import OntologyRegistry, bundled_ontology_path


def _rites(report, rite):
    return [f for f in report.findings if f.rite == rite]


def _write_schema(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "domain.yaml"
    path.write_text(textwrap.dedent(body))
    return path


GOOD_SCHEMA = """
id: https://example.org/schema/pure
name: pure
imports:
  - malleus
  - linkml:types
classes:
  Creature:
    is_a: Entity
  TamesRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: PureRelationType
        required: true
        equals_string: TAMES
      source_id:
        range: Creature
      target_id:
        range: Creature
enums:
  PureRelationType:
    permissible_values:
      TAMES: {}
"""

LOOSE_SCHEMA = """
id: https://example.org/schema/heretic
name: heretic
imports:
  - malleus
  - linkml:types
classes:
  ThingEvent:
    is_a: Event
  LinksRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: HereticRelationType
        required: true
        equals_string: LINKS
  StringSignal:
    is_a: Signal
    slot_usage:
      signal_type:
        range: PureSignalType
      bearer_id:
        required: false
    slots:
      - formal_expression
enums:
  HereticRelationType:
    permissible_values:
      LINKS: {}
  PureSignalType:
    permissible_values:
      SCORE: {}
slots:
  formal_expression:
    range: string
"""

ROOT_MAP = {"malleus": str(bundled_ontology_path("malleus.yaml"))}


def test_pure_schema_earns_the_seal(tmp_path):
    report = run_rites(_write_schema(tmp_path, GOOD_SCHEMA), import_map=ROOT_MAP)
    assert report.purity, [f.message for f in report.heresies]
    assert any(f.severity == "COMMENDATION" for f in _rites(report, "root_currency"))


def test_unloadable_schema_is_a_construction_heresy(tmp_path):
    path = tmp_path / "broken.yaml"
    path.write_text("id: x\nname: broken\nimports: [does-not-exist]\n")
    report = run_rites(path)
    assert not report.purity
    assert _rites(report, "construction")[0].severity == HERESY


def test_loose_event_type_is_a_heresy(tmp_path):
    report = run_rites(_write_schema(tmp_path, LOOSE_SCHEMA), import_map=ROOT_MAP)
    subjects = {f.subject for f in _rites(report, "constrained_tongues")}
    assert "ThingEvent" in subjects
    assert not report.purity


def test_unbound_endpoints_raise_suspicion(tmp_path):
    report = run_rites(_write_schema(tmp_path, LOOSE_SCHEMA), import_map=ROOT_MAP)
    subjects = {f.subject for f in _rites(report, "bound_endpoints")}
    messages = [f.message for f in _rites(report, "bound_endpoints")]
    assert "LinksRelation" in subjects
    assert any("source_id" in m for m in messages)


def test_optional_bearer_and_formula_slot_raise_suspicion(tmp_path):
    report = run_rites(_write_schema(tmp_path, LOOSE_SCHEMA), import_map=ROOT_MAP)
    assert any(f.severity == SUSPICION for f in _rites(report, "derived_signals"))
    formula = _rites(report, "inert_formula")
    assert formula and formula[0].subject == "StringSignal.formal_expression"


def test_stale_root_is_divergent(tmp_path):
    root_text = bundled_ontology_path("malleus.yaml").read_text()
    aged = tmp_path / "old_malleus.yaml"
    aged.write_text(root_text.replace("DESTROYED:", "OBLITERATED:"))
    report = run_rites(
        _write_schema(tmp_path, GOOD_SCHEMA),
        import_map={"malleus": str(aged)},
    )
    currency = _rites(report, "root_currency")
    assert currency and currency[0].severity == HERESY
    assert "divergent" in currency[0].message


def test_cli_exit_codes_and_json(tmp_path, capsys):
    good = _write_schema(tmp_path, GOOD_SCHEMA)
    map_arg = f"malleus={ROOT_MAP['malleus']}"
    assert main([str(good), "--map", map_arg]) == 0
    assert "PURITY SEAL GRANTED" in capsys.readouterr().out

    bad = tmp_path / "bad.yaml"
    bad.write_text((tmp_path / "domain.yaml").read_text())  # reuse, then break it
    bad.write_text(textwrap.dedent(LOOSE_SCHEMA))
    assert main([str(bad), "--map", map_arg, "--json"]) == 1
    out = capsys.readouterr().out
    assert '"purity": false' in out


REQUIRED_LINES = [
    index
    for index, line in enumerate(
        bundled_ontology_path("malleus.yaml").read_text().splitlines()
    )
    if line.strip() == "required: true"
]


class TestRootCurrencyIsConsumerSide:
    """A vendored root that dropped ANY required constraint must lose the
    seal (second self-inquisition H1). No occurrence exempt."""

    @pytest.mark.parametrize("line_index", REQUIRED_LINES)
    def test_dropping_any_required_line_is_a_heresy(self, tmp_path, line_index):
        lines = bundled_ontology_path("malleus.yaml").read_text().splitlines()
        del lines[line_index]
        aged = tmp_path / "malleus.yaml"
        aged.write_text("\n".join(lines) + "\n")
        report = run_rites(
            _write_schema(tmp_path, GOOD_SCHEMA), import_map={"malleus": str(aged)}
        )
        currency = _rites(report, "root_currency")
        assert currency and currency[0].severity == HERESY
        assert not report.purity


class TestMalformedSchemaIsAFindingNotACrash:
    """Every way the subject can be malformed becomes a recorded finding
    (second self-inquisition H4)."""

    @pytest.mark.parametrize("content", [
        "classes: {Thing: {is_a: Entity",          # parser error
        "a:\n\t- tab-indent scanner error",         # scanner error
    ])
    def test_yaml_errors_are_construction_heresies(self, tmp_path, content):
        path = tmp_path / "broken.yaml"
        path.write_text(content)
        report = run_rites(path)
        construction = _rites(report, "construction")
        assert construction and construction[0].severity == HERESY
        assert not report.purity

    def test_non_utf8_bytes_are_a_construction_heresy(self, tmp_path):
        path = tmp_path / "binary.yaml"
        path.write_bytes(b"\xff\xfe\x00broken")
        report = run_rites(path)
        assert _rites(report, "construction")[0].severity == HERESY

    def test_cli_reports_broken_yaml_as_json(self, tmp_path, capsys):
        path = tmp_path / "broken.yaml"
        path.write_text("classes: {Thing: {is_a: Entity")
        assert main([str(path), "--json"]) == 1
        parsed = json.loads(capsys.readouterr().out)
        assert parsed["purity"] is False


class TestFormulaTokensAreData:
    """The inert_formula name set lives in rubric.yaml and matches
    substrings (second self-inquisition S5)."""

    def test_equation_slot_is_flagged(self, tmp_path):
        schema = tmp_path / "eq.yaml"
        schema.write_text(
            "id: https://example.org/schema/eq\n"
            "name: eq\n"
            "imports:\n"
            "  - malleus\n"
            "  - linkml:types\n"
            "classes:\n"
            "  Model:\n"
            "    is_a: Entity\n"
            "    slots: [growth_equation]\n"
            "slots:\n"
            "  growth_equation:\n"
            "    range: string\n"
        )
        report = run_rites(schema, import_map=ROOT_MAP)
        formula = [f for f in report.findings if f.rite == "inert_formula"]
        assert formula and formula[0].subject == "Model.growth_equation"


class TestRubricIsWellFormedAndFailsLoud:
    """The rubric is shipped data adopters tune. A malformed rubric must
    refuse, never degrade to built-in defaults: silent fallback is the
    silent_drop rite firing on the inspector's own instrument."""

    def test_every_rite_declares_question_severity_and_lesson(self):
        rubric = _rubric()
        rites = rubric["mechanical"] + rubric["judgment"]
        assert len(rites) > 25
        for rite in rites:
            assert rite["question"].strip(), rite
            assert rite["severity"] in (HERESY, SUSPICION, NOTE), rite
            assert rite["lesson"].strip(), rite

    def test_rite_ids_are_unique(self):
        rubric = _rubric()
        ids = [r["id"] for r in rubric["mechanical"] + rubric["judgment"]]
        assert len(ids) == len(set(ids))

    def test_principles_rites_are_present(self):
        """docs/PRINCIPLES.md names these; a rite named in prose and absent
        from the rubric is a remediation that exists only in documentation."""
        ids = {r["id"] for r in _rubric()["judgment"]}
        assert {
            "encoding_is_load_bearing",
            "quotation_is_byte_exact",
            "arbiter_is_accountable",
            "evidence_does_not_transfer",
            "module_declares_its_interface",
        } <= ids

    def test_unparseable_rubric_refuses(self, tmp_path):
        path = tmp_path / "rubric.yaml"
        path.write_text("config: {formula_slot_tokens: [oops")
        with pytest.raises(RubricError, match="could not be read"):
            _formula_tokens(path)

    def test_missing_config_refuses(self, tmp_path):
        path = tmp_path / "rubric.yaml"
        path.write_text("judgment: []\n")
        with pytest.raises(RubricError, match="no `config:` mapping"):
            _formula_tokens(path)

    def test_mistyped_token_list_refuses_instead_of_defaulting(self, tmp_path):
        path = tmp_path / "rubric.yaml"
        path.write_text("config:\n  formula_slot_token: [formula]\n")
        with pytest.raises(RubricError, match="must be a list"):
            _formula_tokens(path)

    def test_empty_token_list_is_an_explicit_disable(self, tmp_path):
        path = tmp_path / "rubric.yaml"
        path.write_text("config:\n  formula_slot_tokens: []\n")
        assert _formula_tokens(path) == ()


class TestPinnedContractMatchesLiveOntology:
    """Editing cyp450.yaml must orphan the contract at build time, not at
    runtime (second self-inquisition, C12 residual)."""

    def test_contract_pin_equals_live_hash(self):
        import yaml as _yaml
        contract = _yaml.safe_load(
            (Path(__file__).parent.parent / "prolog" / "cyp450_logic.yaml").read_text()
        )
        live = OntologyRegistry(bundled_ontology_path("domains", "cyp450.yaml"))
        assert contract["ontology_hash"] == "sha256:" + live.content_hash()


class TestPackagingTargetsAreTracked:
    """Every declared packaging target must exist AND be tracked by git;
    hatchling builds a smaller wheel instead of failing (second
    self-inquisition H3, N3). This test is a deliberate tripwire: it stays
    red until the manifest and its targets are committed together."""

    def test_declared_targets_exist_and_are_tracked(self):
        import subprocess
        import tomllib
        root = Path(__file__).parent.parent
        if not (root / ".git").exists():
            pytest.skip("not a git checkout")
        config = tomllib.loads((root / "pyproject.toml").read_text())
        declared = list(config["tool"]["hatch"]["build"]["include"])
        declared += config["tool"]["pytest"]["ini_options"]["testpaths"]
        missing, untracked = [], []
        for entry in declared:
            if any(char in entry for char in "*?["):
                if not list(root.glob(entry)):
                    missing.append(entry)
                continue
            if not (root / entry).exists():
                missing.append(entry)
                continue
            probe = subprocess.run(
                ["git", "ls-files", "--error-unmatch", entry],
                cwd=root, capture_output=True,
            )
            if probe.returncode != 0:
                untracked.append(entry)
        assert not missing, f"declared but absent: {missing}"
        assert not untracked, (
            f"declared in pyproject but not committed: {untracked}. "
            "Commit the manifest and its targets as one unit."
        )


def test_wrong_format_document_is_refused_not_judged(tmp_path):
    """JSON is valid YAML; a JSON ontology must be refused as not-my-format,
    never certified as an empty schema (fleet inquisition lesson)."""
    path = tmp_path / "ontology.json"
    path.write_text('{"node_types": {"server": {}}, "edge_types": {}}')
    report = run_rites(path)
    construction = _rites(report, "construction")
    assert construction[0].severity == HERESY
    assert "not a schema" in construction[0].message
    assert not report.purity
    assert len(report.findings) == 1


def test_construction_failure_still_explains_root_skew(tmp_path):
    """When a schema fails to construct, the report names probable version
    skew of the mapped root instead of hiding it (fleet inquisition lesson)."""
    root_text = bundled_ontology_path("malleus.yaml").read_text()
    aged = tmp_path / "old_malleus.yaml"
    aged.write_text(root_text.replace("DESTROYED:", "OBLITERATED:"))
    unpinned = tmp_path / "domain.yaml"
    unpinned.write_text(
        "id: https://example.org/schema/skew\n"
        "name: skew\n"
        "imports:\n"
        "  - malleus\n"
        "  - linkml:types\n"
        "classes:\n"
        "  LooseRelation:\n"
        "    is_a: Relation\n"
    )
    report = run_rites(unpinned, import_map={"malleus": str(aged)})
    assert _rites(report, "construction")[0].severity == HERESY
    skew = _rites(report, "root_currency")
    assert skew and "version skew" in skew[0].message


class TestSkillsAreInstallable:
    """Any project gets its acolyte at fingertips; releases refresh it
    (the learnings flow back)."""

    def test_install_skills_into_a_project(self, tmp_path, capsys):
        assert main(["install-skills", "--project", str(tmp_path)]) == 0
        out = capsys.readouterr().out
        for name in ("malleus-acolyte", "malleus-inquisitor"):
            assert (tmp_path / ".claude" / "skills" / name / "SKILL.md").is_file()
            assert name in out
        # Idempotent refresh: a second run overwrites without error.
        assert main(["install-skills", "--project", str(tmp_path)]) == 0
