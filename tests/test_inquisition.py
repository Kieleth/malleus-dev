"""Rites of the Ordo Malleus: each mechanical rite proven on a real schema."""

from __future__ import annotations

import ast
import copy
import json
import re
import sys
import textwrap
from pathlib import Path

import pytest
import yaml

from malleus.inquisition import (
    EMITTED_RITES,
    HERESY,
    NOTE,
    SUSPICION,
    UNDISABLABLE_RITES,
    RiteContractError,
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

VACUOUS_ENDPOINT_SCHEMA = """
id: https://example.org/schema/vacuous
name: vacuous
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
        range: VacuousRelationType
        required: true
        equals_string: TAMES
enums:
  VacuousRelationType:
    permissible_values:
      TAMES: {}
"""

ROOTLESS_SCHEMA = """
id: https://example.org/schema/rootless
name: rootless
imports:
  - linkml:types
classes:
  Thing:
    attributes:
      label:
        range: string
"""

ROOT_MAP = {"malleus": str(bundled_ontology_path("malleus.yaml"))}


def _tuned_rubric(tmp_path, severities=None, disable=None, delete=None,
                  config=None, drop_keys=None, extra=None):
    """The shipped rubric with targeted edits, written to a temp file.

    Every test that claims the rubric drives something proves it by editing
    the rubric and observing the change, never by reading the code.
    """
    rubric = copy.deepcopy(_rubric())
    if config is not None:
        rubric["config"] = config
    for section in ("mechanical", "judgment"):
        kept = []
        for entry in rubric[section]:
            rite_id = entry["id"]
            if delete and rite_id in delete:
                continue
            if severities and rite_id in severities:
                entry["severity"] = severities[rite_id]
            if disable and rite_id in disable:
                entry["enabled"] = False
            if drop_keys and rite_id in drop_keys:
                entry.pop(drop_keys[rite_id], None)
            if extra and rite_id in extra:
                entry.update(extra[rite_id])
            kept.append(entry)
        rubric[section] = kept
    path = tmp_path / "tuned_rubric.yaml"
    path.write_text(yaml.safe_dump(rubric, sort_keys=False), encoding="utf-8")
    return path


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
    text_report = capsys.readouterr().out
    assert "ROOT ONTOLOGY PROFILE" in text_report
    assert "PURITY SEAL GRANTED" in text_report

    bad = tmp_path / "bad.yaml"
    bad.write_text((tmp_path / "domain.yaml").read_text())  # reuse, then break it
    bad.write_text(textwrap.dedent(LOOSE_SCHEMA))
    assert main([str(bad), "--map", map_arg, "--json"]) == 1
    out = capsys.readouterr().out
    parsed = json.loads(out)
    assert parsed["purity"] is False
    assert parsed["scope"] == "root-ontology-profile"


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

    def test_protocol_boundary_rites_are_heresies_with_false_positive_controls(self):
        rites = {rite["id"]: rite for rite in _rubric()["judgment"]}

        role = rites["protocol_role_is_explicit"]
        assert role["severity"] == HERESY
        role_text = f"{role['question']} {role['lesson']}".lower()
        for classification in (
            "protocol_invariant",
            "optional_profile",
            "reference_implementation",
            "conformance_fixture",
            "adopter_choice",
        ):
            assert classification in role_text
        assert "neither is itself" in role_text

        optional = rites["optional_profile_stays_optional"]
        assert optional["severity"] == HERESY
        optional_text = f"{optional['question']} {optional['lesson']}".lower()
        assert "lowest affected profile" in optional_text
        assert "within" in optional_text
        assert "compiler-enabled profile" in optional_text

        authority = rites["protocol_authority_is_data"]
        assert authority["severity"] == HERESY
        authority_text = f"{authority['question']} {authority['lesson']}".lower()
        for requirement in (
            "second conforming interpreter",
            "same accepted state or typed refusal",
            "profile-specific",
            "arbitrary-code escape hatch",
        ):
            assert requirement in authority_text

        change_set = rites["single_ledger_knowledge_change"]
        assert change_set["severity"] == HERESY
        change_set_text = (
            f"{change_set['question']} {change_set['lesson']}".lower()
        )
        for requirement in (
            "knowledgechangeset",
            "one authoritative ordered ledger",
            "replay-derived",
            "no independent accepted-state write path",
            "non-governed and non-accepted",
        ):
            assert requirement in change_set_text

    def test_rubric_version_records_protocol_boundary_instrument_change(self):
        assert int(_rubric()["version"]) == 12

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
        path = _tuned_rubric(tmp_path, config={"formula_slot_token": ["formula"]})
        with pytest.raises(RubricError, match="must be a list"):
            _formula_tokens(path)

    def test_missing_rite_section_refuses_with_rubric_error_not_keyerror(self, tmp_path):
        """R3 N3: the first hardening validated `config` and nothing else, so
        a rubric with a good config and no rites raised KeyError downstream."""
        path = tmp_path / "rubric.yaml"
        path.write_text("version: 1\nconfig:\n  formula_slot_tokens: []\njudgment: []\n")
        with pytest.raises(RubricError, match="`mechanical:` must be a non-empty list"):
            _rubric(path)

    def test_rite_missing_its_lesson_refuses(self, tmp_path):
        path = _tuned_rubric(tmp_path, drop_keys={"construction": "lesson"})
        with pytest.raises(RubricError, match="has no `lesson:`"):
            _rubric(path)

    def test_unknown_severity_refuses(self, tmp_path):
        path = _tuned_rubric(tmp_path, severities={"construction": "MILD_CONCERN"})
        with pytest.raises(RubricError, match="declares severity"):
            _rubric(path)

    def test_note_severity_must_say_why(self, tmp_path):
        """R3 N1: NOTE because the property is unproven and NOTE because it is
        minor read identically. The reason is data or the rubric refuses."""
        path = _tuned_rubric(tmp_path, severities={"construction": NOTE})
        with pytest.raises(RubricError, match="must say why in `status:`"):
            _rubric(path)

    def test_shipped_note_rites_all_declare_their_reason(self):
        rubric = _rubric()
        for rite in rubric["mechanical"] + rubric["judgment"]:
            if rite["severity"] == NOTE:
                assert rite.get("status") in ("open_question", "low_stakes"), rite["id"]

    def test_empty_token_list_is_an_explicit_disable(self, tmp_path):
        path = _tuned_rubric(tmp_path, config={"formula_slot_tokens": []})
        assert _formula_tokens(path) == ()


class TestTheRubricActuallyDrivesTheRites:
    """R3 H1. The rubric invited adopters to tune severities and disable
    rites while the CLI hardcoded both, so a rite raised to HERESY still
    printed as a suspicion and a deleted rite still fired. An adopter who
    believes a gate is closed while it is open is worse off than one whose
    tuning never existed."""

    def test_raising_a_severity_changes_the_verdict_and_denies_the_seal(self, tmp_path):
        schema = _write_schema(tmp_path, VACUOUS_ENDPOINT_SCHEMA)
        baseline = run_rites(schema, import_map=ROOT_MAP)
        assert _rites(baseline, "bound_endpoints")[0].severity == SUSPICION
        assert baseline.purity

        tuned = _tuned_rubric(tmp_path, severities={"bound_endpoints": HERESY})
        report = run_rites(schema, import_map=ROOT_MAP, rubric_path=tuned)
        assert _rites(report, "bound_endpoints")[0].severity == HERESY
        assert not report.purity

    def test_disabling_a_rite_silences_it(self, tmp_path):
        schema = _write_schema(tmp_path, VACUOUS_ENDPOINT_SCHEMA)
        assert _rites(run_rites(schema, import_map=ROOT_MAP), "bound_endpoints")
        tuned = _tuned_rubric(tmp_path, disable={"bound_endpoints"})
        assert not _rites(run_rites(schema, import_map=ROOT_MAP, rubric_path=tuned),
                          "bound_endpoints")

    def test_deleting_a_rite_breaks_the_instrument_rather_than_the_gate(self, tmp_path):
        """Absence is not consent. A mistyped id must never be the quiet way
        to switch a gate off; `enabled: false` is the only way."""
        schema = _write_schema(tmp_path, VACUOUS_ENDPOINT_SCHEMA)
        tuned = _tuned_rubric(tmp_path, delete={"bound_endpoints"})
        with pytest.raises(RubricError, match="declares no entry"):
            run_rites(schema, import_map=ROOT_MAP, rubric_path=tuned)

    def test_deletion_is_refused_before_any_rite_runs(self, tmp_path):
        """R4 H2. The check was lazy, at emit time, so deleting a rite that a
        given schema does not trip changed nothing and the schema took the
        seal from a rubric with a hole in it. Worse, deleting the last-firing
        rite refused only after eight findings had been computed and thrown
        away. A rite table is validated as a table, when it loads."""
        clean = _write_schema(tmp_path, GOOD_SCHEMA)
        tuned = _tuned_rubric(tmp_path, delete={"bound_endpoints", "inert_formula"})
        with pytest.raises(RubricError, match="declares no entry"):
            run_rites(clean, import_map=ROOT_MAP, rubric_path=tuned)

    def test_duplicate_rite_ids_are_refused(self, tmp_path):
        """A duplicate silently last-wins, so a second entry at NOTE quietly
        downgrades a heresy and the losing entry is a setting the operator can
        read and the instrument ignores."""
        rubric = copy.deepcopy(_rubric())
        clone = copy.deepcopy(rubric["mechanical"][0])
        clone["severity"] = NOTE
        clone["status"] = "low_stakes"
        clone["status_reason"] = "duplicate planted by a test"
        rubric["mechanical"].append(clone)
        path = tmp_path / "dupe.yaml"
        path.write_text(yaml.safe_dump(rubric, sort_keys=False), encoding="utf-8")
        with pytest.raises(RubricError, match="declared twice"):
            _rubric(path)


class TestASealIsOnlyAsWideAsItsRubric:
    """R4 H1. Making the rubric load-bearing turned a data file into a control
    surface with no floor: with every mechanical rite disabled, a schema
    carrying a known heresy printed an empty report and PURITY SEAL GRANTED at
    exit 0, and the JSON said `purity: true, findings: []`. Nothing named the
    rubric, its version, or how many rites had been skipped. That is this
    tool's own lesson turned against it: a rejection rate of zero is not
    evidence of a gate."""

    def _disable_all(self, tmp_path):
        disablable = set(EMITTED_RITES) - set(UNDISABLABLE_RITES)
        return _tuned_rubric(tmp_path, disable=disablable)

    def test_construction_can_never_be_disabled(self, tmp_path):
        tuned = _tuned_rubric(tmp_path, disable={"construction"})
        with pytest.raises(RubricError, match="cannot be disabled"):
            _rubric(tuned)

    def test_a_document_that_does_not_parse_can_never_take_the_seal(self, tmp_path):
        """The floor: `construction` is the precondition for judging anything."""
        broken = tmp_path / "broken.yaml"
        broken.write_text("classes: {Thing: {is_a: Entity")
        tuned = self._disable_all(tmp_path)
        assert main([str(broken), "--rubric", str(tuned)]) == 1

    def test_a_reduced_rubric_says_so_on_the_seal(self, tmp_path, capsys):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        tuned = self._disable_all(tmp_path)
        assert main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
                     "--rubric", str(tuned)]) == 0
        out = capsys.readouterr().out
        assert "TUNED RUBRIC" in out
        assert "rites disabled: " in out
        assert "bound_endpoints" in out

    def test_the_json_carries_the_coverage(self, tmp_path, capsys):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        tuned = _tuned_rubric(tmp_path, disable={"inert_formula"})
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
              "--rubric", str(tuned), "--json"])
        parsed = json.loads(capsys.readouterr().out)
        assert parsed["disabled"] == ["inert_formula"]
        assert parsed["rubric_version"] == _rubric()["version"]
        assert parsed["rubric"].endswith("tuned_rubric.yaml")

    def test_a_full_rubric_reports_zero_disabled(self, tmp_path, capsys):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}"])
        out = capsys.readouterr().out
        assert "0 mechanical and 0 judgment rites disabled" in out
        assert "REDUCED" not in out

    def test_a_downgraded_construction_cannot_seal_an_unparseable_file(self, tmp_path):
        """R5 H1. The floor went on `enabled:` and not on `severity:`, one
        word apart in the same entry. A rubric identical to the packaged one
        except `severity: NOTE` on `construction` sealed a file that is not
        valid YAML, at exit 0, under a header reading 0 rites disabled."""
        broken = tmp_path / "broken.yaml"
        broken.write_text("classes: {Thing: {is_a: Entity")
        for severity in (NOTE, SUSPICION):
            tuned = _tuned_rubric(
                tmp_path, severities={"construction": severity},
                extra={"construction": {"status": "open_question"}},
            )
            report = run_rites(broken, rubric_path=tuned)
            assert _rites(report, "construction")[0].severity == severity
            assert not report.purity, f"{severity} on construction sealed a non-schema"
            assert main([str(broken), "--rubric", str(tuned)]) == 1

    def test_a_downgraded_construction_cannot_seal_a_wrong_format_document(self, tmp_path):
        doc = tmp_path / "ontology.json"
        doc.write_text('{"name": "not a linkml schema"}')
        tuned = _tuned_rubric(tmp_path, severities={"construction": NOTE},
                              extra={"construction": {"status": "open_question"}})
        assert main([str(doc), "--rubric", str(tuned)]) == 1

    def test_disabled_judgment_rites_are_disclosed_too(self, tmp_path, capsys):
        """R5 H2. The disclosure counted the mechanical tier only, so all 24
        judgment rites could be switched off under "0 rites disabled"."""
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        tuned = _tuned_rubric(tmp_path, disable={"gate_integrity", "silent_drop"})
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
              "--rubric", str(tuned), "--json"])
        assert "gate_integrity" in json.loads(capsys.readouterr().out)["disabled"]
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
              "--rubric", str(tuned)])
        out = capsys.readouterr().out
        assert "2 judgment rites disabled" in out
        assert "gate_integrity" in out


class TestTheDisclosureCannotBeForged:
    """R5 S1, S2. The version is the operator's own word in a file they
    control, and a downgrade narrows the gate exactly as much as a disable."""

    def test_the_digest_is_reported_and_tracks_the_bytes(self, tmp_path, capsys):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        tuned = _tuned_rubric(tmp_path, severities={"bound_endpoints": HERESY})
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
              "--rubric", str(tuned), "--json"])
        first = json.loads(capsys.readouterr().out)
        assert len(first["rubric_sha256"]) == 64
        assert first["rubric"] == "tuned_rubric.yaml"  # a name, not an install path

        again = _tuned_rubric(tmp_path, severities={"bound_endpoints": SUSPICION})
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
              "--rubric", str(again), "--json"])
        assert json.loads(capsys.readouterr().out)["rubric_sha256"] != first["rubric_sha256"]

    def test_a_non_scalar_version_is_refused(self, tmp_path):
        rubric = copy.deepcopy(_rubric())
        rubric["version"] = {"pretend": "7"}
        path = tmp_path / "forged.yaml"
        path.write_text(yaml.safe_dump(rubric, sort_keys=False), encoding="utf-8")
        with pytest.raises(RubricError, match="scalar `version:`"):
            _rubric(path)

    def test_a_downgrade_is_disclosed_like_a_disable(self, tmp_path, capsys):
        schema = _write_schema(tmp_path, LOOSE_SCHEMA)
        tuned = _tuned_rubric(tmp_path, severities={"constrained_tongues": NOTE},
                              extra={"constrained_tongues": {"status": "low_stakes",
                                                             "status_reason": "test"}})
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
              "--rubric", str(tuned), "--json"])
        assert "constrained_tongues" in json.loads(capsys.readouterr().out)["downgraded"]
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}", "--rubric", str(tuned)])
        out = capsys.readouterr().out
        assert "downgraded: constrained_tongues" in out
        assert "TUNED RUBRIC" in out

    def test_the_packaged_rubric_reports_no_tuning(self, tmp_path, capsys):
        main([str(_write_schema(tmp_path, GOOD_SCHEMA)),
              "--map", f"malleus={ROOT_MAP['malleus']}", "--json"])
        parsed = json.loads(capsys.readouterr().out)
        assert parsed["downgraded"] == [] and parsed["disabled"] == []

    def test_the_two_rite_constants_cannot_drift(self):
        """R5 S4: a floor named against a rite the code never emits would be
        enforced on an entry nothing checks."""
        assert set(UNDISABLABLE_RITES) <= set(EMITTED_RITES)
        declared = {r["id"] for r in _rubric()["mechanical"]}
        assert set(EMITTED_RITES) == declared


class TestTheReferenceRootIsJudgedToo:
    """R5 H3. A reference root that parses and declares no classes has an
    empty fingerprint, which makes every subject a trivial superset, so the
    rite answered "root is current" precisely when it knew least. The subject
    side already refuses this exact shape fourteen lines earlier."""

    def test_an_empty_reference_root_denies_the_seal(self, tmp_path):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        empty = tmp_path / "truncated.yaml"
        empty.write_text("id: https://example.org/schema/x\nname: x\n")
        report = run_rites(schema, import_map=ROOT_MAP, root_path=str(empty))
        assert not report.purity
        assert not [f for f in _rites(report, "root_currency")
                    if f.severity == "COMMENDATION"]
        assert _rites(report, "root_currency_answerable")[0].severity == HERESY

    def test_a_json_reference_root_denies_the_seal(self, tmp_path):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        doc = tmp_path / "root.json"
        doc.write_text('{"name": "not a root"}')
        assert main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
                     "--root", str(doc)]) == 1

    def test_the_other_rites_still_run_on_a_good_subject(self, tmp_path):
        """The fault is in the reference; the subject is fine and still judged."""
        schema = _write_schema(tmp_path, LOOSE_SCHEMA)
        empty = tmp_path / "truncated.yaml"
        empty.write_text("id: https://example.org/schema/x\nname: x\n")
        report = run_rites(schema, import_map=ROOT_MAP, root_path=str(empty))
        assert _rites(report, "constrained_tongues")
        assert _rites(report, "inert_formula")


class TestTheTuningContractIsReachable:
    """R4 H3. The rubric and PRINCIPLES.md both told the adopter to tune
    "your own copy of the rubric". There was no flag, so the only operator
    path was editing site-packages, which the next upgrade silently reverts,
    taking every raised severity with it. The heal had moved round 3's
    failure out of the code and into the packaging."""

    def test_the_cli_accepts_a_tuned_rubric_without_monkeypatching(self, tmp_path, capsys):
        schema = _write_schema(tmp_path, VACUOUS_ENDPOINT_SCHEMA)
        tuned = _tuned_rubric(tmp_path, severities={"bound_endpoints": HERESY})
        assert main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
                     "--rubric", str(tuned)]) == 1
        assert "HERESY" in capsys.readouterr().out

    def test_a_broken_tuned_rubric_is_still_a_broken_instrument(self, tmp_path, capsys):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        broken = tmp_path / "bad.yaml"
        broken.write_text("config: {formula_slot_tokens: [oops")
        assert main([str(schema), "--rubric", str(broken)]) == 2
        assert "Traceback" not in capsys.readouterr().err


class TestUnknownConditionsRefuse:
    """R4 S1. `root_currency` is a HERESY rite, and the case where its
    question could not be answered at all carried a hardcoded suspicion: with
    an unreadable reference root the schema took the seal at exit 0."""

    def test_an_unreadable_reference_root_denies_the_seal(self, tmp_path):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        corrupt = tmp_path / "corrupt_root.yaml"
        corrupt.write_text("classes: {Entity: {is_a: ")
        assert main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}",
                     "--root", str(corrupt)]) == 1

    def test_a_missing_reference_root_denies_the_seal(self, tmp_path):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        report = run_rites(schema, import_map=ROOT_MAP,
                           root_path=str(tmp_path / "nowhere.yaml"))
        assert _rites(report, "root_currency_answerable")[0].severity == HERESY
        assert not report.purity


class TestOnlyAVerdictMayDenyTheSeal:
    """R4 S2. The invariant that severity is data was guarded by a regex over
    the source file, which sees one call shape and no other."""

    def test_add_refuses_to_raise_a_heresy(self, tmp_path):
        report = run_rites(_write_schema(tmp_path, GOOD_SCHEMA), import_map=ROOT_MAP)
        with pytest.raises(RiteContractError, match="only verdict"):
            report.add("root", HERESY, "x", "y")

    def test_the_plural_is_spelled_correctly(self, tmp_path, capsys):
        """R4 N2: the suffix was appended to 'heresy', printing 'heresyies'."""
        schema = _write_schema(tmp_path, LOOSE_SCHEMA)
        main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}"])
        out = capsys.readouterr().out
        assert "heresyies" not in out
        assert re.search(r"\d+ heres(y|ies) recorded", out)

    def test_primary_verdict_severity_is_the_declared_one(self, tmp_path):
        """R3 H2: rubric.yaml declared `root` at NOTE while the code emitted
        HERESY. Reading the severity from the rubric makes that unrepresentable."""
        schema = _write_schema(tmp_path, ROOTLESS_SCHEMA)
        assert _rites(run_rites(schema), "root")[0].severity == HERESY
        tuned = _tuned_rubric(tmp_path, severities={"root": SUSPICION})
        assert _rites(run_rites(schema, rubric_path=tuned), "root")[0].severity == SUSPICION

    # The source-grep guard that used to live here is gone: it saw one call
    # shape and nothing else. The invariant is enforced at runtime instead,
    # in Report.add. See TestOnlyAVerdictMayDenyTheSeal.


class TestBrokenInstrumentIsNeverABrokenSubject:
    """R3 H6. A corrupt rubric produced a 40-line traceback headed by a YAML
    parser error and exit 1, the same code that means 'your schema has
    heresies'. An operator who just edited their schema reads that as their
    fault, and a CI gate cannot tell the two apart."""

    def test_cli_reports_a_broken_rubric_as_exit_two_without_a_traceback(
        self, tmp_path, capsys, monkeypatch
    ):
        import malleus.inquisition as inq
        broken = tmp_path / "rubric.yaml"
        broken.write_text("config: {formula_slot_tokens: [oops")
        monkeypatch.setattr(inq, "RUBRIC_PATH", broken)
        schema = _write_schema(tmp_path, GOOD_SCHEMA)

        assert main([str(schema), "--map", f"malleus={ROOT_MAP['malleus']}"]) == 2
        captured = capsys.readouterr()
        assert "Traceback" not in captured.err
        assert "rubric" in captured.err
        assert "PURITY SEAL" not in captured.out

    def test_a_broken_rubric_refuses_before_any_rite_runs(self, tmp_path):
        """The refusal must precede the work, or a half-built report is
        discarded and the operator sees nothing that was already known."""
        broken = tmp_path / "rubric.yaml"
        broken.write_text("config: {}\n")
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        with pytest.raises(RubricError):
            run_rites(schema, import_map=ROOT_MAP, rubric_path=broken)


class TestTheDiagnosticIsNeverDiscarded:
    """R3 S3. When a schema fails to construct, the tool tries to explain it
    as version skew. Every failure of that diagnostic was swallowed by
    `except ...: pass`, and the likeliest cause of the failure is exactly the
    case where the hint vanished."""

    def test_unusable_mapped_root_is_reported_not_swallowed(self, tmp_path):
        schema = _write_schema(tmp_path, GOOD_SCHEMA)
        report = run_rites(schema, import_map={"malleus": str(tmp_path / "absent.yaml")})
        assert _rites(report, "construction")[0].severity == HERESY
        skew = _rites(report, "root_currency")
        assert skew and "could not be attributed" in skew[0].message


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


class TestShippedGuidanceSaysWhatTheCodeDoes:
    """Rites applied to the rite-givers. Every finding below was a real
    divergence between what this repository shipped and what it did."""

    ROOT = Path(__file__).parent.parent

    def _docs(self):
        """Every prose surface that ships. The wheel and the sdist both carry
        the CHANGELOG, and a false claim there is as shipped as one in a doc."""
        paths = [self.ROOT / "README.md",
                 self.ROOT / "CHANGELOG.md",
                 self.ROOT / "src" / "malleus" / "inquisition" / "rubric.yaml"]
        paths += sorted((self.ROOT / "docs").glob("*.md"))
        paths += sorted((self.ROOT / ".claude" / "skills").rglob("*.md"))
        return [(p, p.read_text(encoding="utf-8")) for p in paths]

    def test_no_shipped_document_claims_a_capability_the_library_lacks(self):
        """R4 H4. `RECIPES.md` presented "malleus's own loop: ... roll back
        both graph and log, returning the violated rule and proof trace" in a
        list of production examples. Zero hits for either in `src/`; staging
        never mutates the base graph, so there is nothing to roll back; and
        four other shipped documents go out of their way to deny the proof
        trace. Five documents, one disagreeing, is `single_source` scored."""
        absent = {
            "proof trace": "malleus records execution attestations, not proofs",
            "rollback": "staging never mutates the base graph",
            "roll back": "staging never mutates the base graph",
        }
        offenders = []
        for path, text in self._docs():
            if path.name in ("CHANGELOG.md", "DELIMITATIONS.md"):
                continue  # history and prior-art comparison, not capability claims
            for phrase, why in absent.items():
                for match in re.finditer(re.escape(phrase), text, re.I):
                    # The denial must be in the SAME sentence. A 300-character
                    # window let "cannot drift" in the neighbouring list item
                    # clear all three claims in this very document.
                    sentence = _sentence_around(text, match.start(), match.end())
                    if re.search(r"\b(not|never|no|without|cannot|denies|neither)\b",
                                 sentence, re.I):
                        continue
                    line = text.count("\n", 0, match.start()) + 1
                    offenders.append(f"{path.name}:{line} ({phrase}: {why})")
        assert not offenders, f"capability claimed that src/ cannot support: {offenders}"

    def test_currency_guidance_never_names_the_producer_side_check(self):
        """R3 H5. The producer-side check is blind to a dropped `required`
        constraint. Naming it for the currency question hands the adopter a
        green test over a root the rite should condemn, which is the
        confusion `the_rite_survives_its_subject` warns about by name."""
        offenders = [f"{p.name}:{line}" for p, text in self._docs()
                     for line in _producer_check_for_currency(text)]
        assert not offenders, (
            "the producer-side check is named as the answer to a currency, "
            f"staleness, or drift question at: {offenders}. Documenting the "
            "producer-side API itself is fine; prescribing it for the "
            "consumer question is the drift it cannot see."
        )

    def test_every_shipped_skill_carries_the_scope_gate(self):
        """R3 H7. The CHANGELOG claimed both skills received the gate. One
        did. A claim about a shipped artifact is checkable, so check it."""
        skills = sorted((self.ROOT / ".claude" / "skills").glob("*/SKILL.md"))
        assert len(skills) >= 2
        for path in skills:
            text = path.read_text(encoding="utf-8")
            assert "## Before you build" in text, path
            assert "smallest observation" in text, path
            assert "exclude" in text.lower(), path

    def test_no_skill_sends_a_reader_to_a_path_that_will_not_exist(self):
        """R4 S5. The inquisitor skill's only instruction for finding the
        rubric named `src/malleus/inquisition/rubric.yaml` "in the malleus
        repo". The skill installs into projects with no checkout, where that
        path never exists and the rubric lives in site-packages. An assistant
        following step 3 literally finds nothing and is forced into exactly
        the paraphrase-from-memory the same sentence forbids."""
        for path in sorted((self.ROOT / ".claude" / "skills").glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"`?src/malleus/[\w/.]+`?", text):
                window = text[max(0, match.start() - 700):match.end() + 700]
                assert "import malleus" in window or "checkout" in window, (
                    f"{path.name} names {match.group()} with no installed-package "
                    "resolution nearby; that path does not exist where this skill installs"
                )

    # R6 H2. The prior guard checked that a pending capability was NAMED in
    # the document. It was, and three sentences above the naming the same
    # paragraph asserted the capability exists. Naming is not disclaiming, and
    # a guard that cannot tell them apart is the criterion tested instead of
    # the property. This table is data: when a capability joins the pending
    # list, add the words a document would use to claim it.
    UNIMPLEMENTED_CLAIMS = {
        "citation-byte-verification": (
            ("evidence binding", "quoted span", "registered bytes", "source bytes",
             "byte identity"),
            ("invalidates", "verifies", "proves", "guarantees", "enforces", "detects"),
        ),
        "deferral-queue-aging": (
            ("deferral", "deferred proposal", "review queue"),
            ("ages", "expires", "blocks past", "escalates"),
        ),
        "action-execution": (
            ("the action", "authorized action"),
            ("executes", "performs", "carries out"),
        ),
    }
    # A denial clears a sentence, and so does a modal: `PRINCIPLES.md` states
    # norms ("a tuple SHOULD point at bytes") beside boundaries, and a norm is
    # not a capability claim. Only the present indicative claims.
    _DENIAL = re.compile(
        r"\b(not|never|no|nor|without|cannot|does not|neither|declares no"
        r"|should|must|would|ought|belongs to)\b", re.I)

    def test_no_document_asserts_a_capability_on_the_pending_list(self):
        from malleus.status import IMPLEMENTATION_STATUS
        offenders = []
        for capability, (subjects, verbs) in self.UNIMPLEMENTED_CLAIMS.items():
            assert capability in IMPLEMENTATION_STATUS.pending_capabilities, (
                f"{capability} is no longer pending; move it out of this table "
                "and prove the capability with a test instead"
            )
            for path, text in self._docs():
                if path.name == "CHANGELOG.md":
                    continue  # history records what was claimed, including wrongly
                for verb in verbs:
                    for match in re.finditer(rf"\b{re.escape(verb)}\b", text, re.I):
                        sentence = _sentence_around(text, match.start(), match.end())
                        if not any(s in sentence.lower() for s in subjects):
                            continue
                        # The exemption must govern the CLAUSE that carries the
                        # verb, not merely appear somewhere in the sentence:
                        # "Evidence must cite the record, so changing the bytes
                        # invalidates the binding" is a requirement followed by
                        # a capability claim, and the first cleared the second.
                        clause = _clause_around(sentence, verb)
                        if self._DENIAL.search(clause):
                            continue
                        line = text.count("\n", 0, match.start()) + 1
                        offenders.append(f"{path.name}:{line} ({capability}: '{verb}')")
        assert not offenders, (
            "a shipped document asserts a capability that is on the "
            f"not-implemented list: {offenders}"
        )

    def test_the_two_doctrines_name_their_tiebreaker(self):
        """R3 S2. No half measures says cut an open gate now; the scope gate
        says do not widen the slice. They meet on an out-of-scope open gate
        found mid-work, and an unresolved standing order is resolved
        arbitrarily by whoever reads it."""
        for path in sorted((self.ROOT / ".claude" / "skills").glob("*/SKILL.md")):
            text = _flat(path.read_text(encoding="utf-8"))
            if "no half measures" not in text.lower():
                continue
            assert "not closed silently, not deferred silently" in text, path
            assert "The human decides whether it enters this slice" in text, path

    def test_principles_name_the_capabilities_they_do_not_have(self):
        """R3 H3, H4. Principles 2 and 3 asserted byte-exact citation and an
        aging deferral queue as properties of malleus. Malleus has neither.
        The capability boundary is the one document that must know."""
        from malleus.status import IMPLEMENTATION_STATUS
        surfaces = [self.ROOT / "docs" / "PRINCIPLES.md",
                    self.ROOT / "docs" / "ADOPTION_GUIDE.md"]
        # R4: the first version of this guard read only the two documents the
        # finding named, so the same claim relapsed one file over, in the
        # skill that ships to every adopting project. Every prose surface that
        # states the property must also state its tense.
        surfaces += sorted((self.ROOT / ".claude" / "skills").glob("*/SKILL.md"))
        for capability in ("citation-byte-verification", "deferral-queue-aging"):
            assert capability in IMPLEMENTATION_STATUS.pending_capabilities
        claims = {"byte-exact": "citation-byte-verification",
                  "age is measured": "deferral-queue-aging"}
        for path in surfaces:
            text = _flat(path.read_text(encoding="utf-8"))
            for claim, capability in claims.items():
                if claim in text:
                    assert capability in text, (
                        f"{path.name} states '{claim}' without naming {capability}, "
                        "so a reader takes it for a property malleus provides"
                    )

    def test_load_bearing_is_reserved_for_checkable_properties(self):
        """R3 N2. This repo names a HERESY-severity rite
        `encoding_is_load_bearing`. Calling the biological analogy load
        bearing two paragraphs before saying it is never support for a claim
        is a reader trap in the one document about what supports what."""
        principles = (self.ROOT / "docs" / "PRINCIPLES.md").read_text(encoding="utf-8")
        for match in re.finditer(r"load[ -]bearing", principles):
            window = principles[max(0, match.start() - 200):match.end() + 200]
            assert "analogy" not in window.lower(), (
                "'load bearing' used of the biological analogy at offset "
                f"{match.start()}"
            )

    def test_public_and_private_doctrine_do_not_diverge(self):
        """R3 S4. The thesis and the working rule exist in two copies, one of
        them gitignored. `single_source` predicts one is already wrong, and
        one was: the public copy had lost two of the completion rule's three
        conditions and the whole exclusion list."""
        principles = _flat((self.ROOT / "docs" / "PRINCIPLES.md").read_text(encoding="utf-8"))
        thesis = ("typed subgraphs as composable epistemic modules whose")
        # R5 N3: half this guard needs no private file, and that half must
        # run in CI and on every adopter's machine, not on one laptop.
        assert thesis in principles
        for condition in _SHARED_DOCTRINE:
            assert condition in principles, f"public copy is weaker: {condition}"

        private = self.ROOT / "malleus-moving" / "design" / "CLAIM_AND_EXECUTION_DOCTRINE.md"
        if not private.is_file():
            pytest.skip("the paper-program doctrine is not present in this tree")
        doctrine = private.read_text(encoding="utf-8")
        assert thesis in _flat(doctrine)
        for condition in ("the relevant guardrails pass",
                          "new databases, orchestration layers",
                          "stop before implementation and obtain a decision",
                          # R4 N5: the drift restarted in the other direction
                          # the moment the public copy gained a paragraph.
                          "not closed silently, not deferred silently",
                          "The human decides whether it enters this slice"):
            assert condition in _flat(doctrine), f"doctrine lost: {condition}"


_SHARED_DOCTRINE = (
    "the relevant guardrails pass",
    "new databases, orchestration layers",
    "stop before implementation and obtain a decision",
    "not closed silently, not deferred silently",
    "The human decides whether it enters this slice",
)


def _flat(text: str) -> str:
    """Markdown wraps at different columns in different files; compare words."""
    return " ".join(text.split())


_CURRENCY_WORDS = re.compile(
    r"\b(current|currency|stale|staleness|drift|drifted|diverged|divergence"
    r"|out.of.date|outdated|up.to.date|in.sync|behind|newer|older|upgrade[ds]?"
    r"|vendored|re.?vendor)\b",
    re.I,
)


def _sentence_around(text: str, start: int, end: int) -> str:
    """The sentence containing [start:end). Sentence ends at `. ` or a blank
    line or a list-item boundary; markdown lists break sentences too."""
    left = max((m.end() for m in re.finditer(r"(?:\.\s|\n\s*\n|\n\s*\d+\.\s|\n\s*[-*]\s)",
                                             text[:start])), default=0)
    tail = re.search(r"(?:\.\s|\n\s*\n|\n\s*\d+\.\s|\n\s*[-*]\s)", text[end:])
    right = end + (tail.start() if tail else len(text) - end)
    return text[left:right]


_CLAUSE_BREAK = re.compile(r"\bso that\b|\bso\b|\bwhich\b|\btherefore\b|\bthus\b|;", re.I)


def _clause_around(sentence: str, verb: str) -> str:
    """The clause of `sentence` containing `verb`.

    A modal or a denial in one clause does not govern the next: the sentence
    that relapsed read "Evidence must cite the exact record, so changing the
    registered bytes invalidates the old evidence binding", and a
    sentence-wide exemption let the second half through on the strength of
    the first half's "must".
    """
    pieces, last = [], 0
    for brk in _CLAUSE_BREAK.finditer(sentence):
        pieces.append(sentence[last:brk.start()])
        last = brk.start()
    pieces.append(sentence[last:])
    for piece in pieces:
        if re.search(rf"\b{re.escape(verb)}\b", piece, re.I):
            return piece
    return sentence


def _sections(text: str) -> list[tuple[int, str]]:
    """(offset, body) per markdown/comment section, split on headings."""
    bounds = [m.start() for m in re.finditer(r"^#{1,6} ", text, re.M)] or [0]
    if bounds[0] != 0:
        bounds.insert(0, 0)
    bounds.append(len(text))
    return [(bounds[i], text[bounds[i]:bounds[i + 1]]) for i in range(len(bounds) - 1)]


def _producer_check_for_currency(text: str) -> list[int]:
    """Line numbers where the producer-side check is offered as the answer to
    a currency question.

    Two things clear an occurrence, and both are semantic rather than
    positional, because the first version of this guard used a 500-character
    window and six ordinary rewordings walked straight past it. A passage
    clears if it also names `check_compatibility_strict` anywhere in the same
    section, or if it calls the check producer-side at the point of use.
    Either way the reader has been told which question it answers.
    """
    hits = []
    for offset, section in _sections(text):
        contrasted = "check_compatibility_strict" in section
        for match in re.finditer(r"check_compatibility(?!_strict)", section):
            if contrasted:
                continue
            near = section[max(0, match.start() - 250):match.end() + 250]
            if re.search(r"producer[ -]side", near, re.I):
                continue
            if _CURRENCY_WORDS.search(near):
                hits.append(text.count("\n", 0, offset + match.start()) + 1)
    return hits


class TestNoPrivateMaterialCanReachARelease:
    """R6 H1. A branch un-gitignored the private research directory, and the
    build silently absorbed it: main's sdist held 49 files and zero private
    ones, the branch's held 70 and sixteen, because `pyproject.toml`'s bare
    `README.md` include matches at every depth. The wheel stayed clean, which
    is why nothing noticed: `twine check` validates metadata and never reads
    content, and CI smoke-tests only the wheel.

    The instance was one `.gitignore` line. The property is that every archive
    member belongs to a declared public root and every sdist source is tracked.
    That is what this test holds, so the next broad glob fails here rather than
    after publication.
    """

    ROOT = Path(__file__).parent.parent
    SDIST_ALLOWED_FILES = {
        ".gitignore",
        "CHANGELOG.md",
        "LICENSE",
        "PKG-INFO",
        "README.md",
        "pyproject.toml",
    }
    SDIST_ALLOWED_ROOTS = (
        ".claude/skills/",
        "conformance/ocr/v0/corpus/",
        "docs/",
        "ontology/",
        "prolog/",
        "src/malleus/",
        "tests/",
    )
    WHEEL_SHARED_ROOTS = ("docs", "ontology", "prolog", "skills")

    def _ocr_fixture_sources(self):
        corpus = self.ROOT / "conformance" / "ocr" / "v0" / "corpus"
        return {
            path.relative_to(self.ROOT).as_posix()
            for path in corpus.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        } | {"docs/OCR_FIXTURE_CORPUS.md", "tests/test_ocr_corpus.py"}

    def _build(self, tmp_path):
        import subprocess
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "build",
                "--no-isolation",
                "--sdist",
                "--wheel",
                "--outdir",
                str(tmp_path),
                str(self.ROOT),
            ],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, (
            "release artifact build failed:\n"
            f"{result.stdout[-1000:]}\n{result.stderr[-1000:]}"
        )
        return sorted(tmp_path.iterdir())

    def _members(self, artifact):
        if artifact.suffix == ".whl":
            import zipfile
            with zipfile.ZipFile(artifact) as archive:
                return archive.namelist()
        import tarfile
        with tarfile.open(artifact) as archive:
            # strip the leading "malleus_dev-X.Y.Z/" component
            return [
                member.name.partition("/")[2]
                for member in archive.getmembers()
                if member.isfile()
            ]

    def _unexpected_members(self, artifact, members):
        if artifact.suffix != ".whl":
            return sorted(
                name
                for name in members
                if name
                and name not in self.SDIST_ALLOWED_FILES
                and not name.startswith(self.SDIST_ALLOWED_ROOTS)
            )

        dist_info_roots = {
            name.partition("/")[0]
            for name in members
            if name.partition("/")[0].endswith(".dist-info")
        }
        assert len(dist_info_roots) == 1, (
            f"{artifact.name} has ambiguous metadata roots: {sorted(dist_info_roots)}"
        )
        dist_info_root = next(iter(dist_info_roots))
        distribution_root = dist_info_root.removesuffix(".dist-info")
        shared_root = f"{distribution_root}.data/data/share/malleus/"
        allowed_shared = tuple(
            f"{shared_root}{root}/" for root in self.WHEEL_SHARED_ROOTS
        )
        return sorted(
            name
            for name in members
            if not name.startswith("malleus/")
            and not name.startswith(f"{dist_info_root}/")
            and not name.startswith(allowed_shared)
        )

    def _untracked_sdist_members(self, members):
        import subprocess

        if not (self.ROOT / ".git").exists():
            pytest.skip("not a git checkout")
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=self.ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        tracked = set(result.stdout.rstrip("\0").split("\0"))
        generated = {"PKG-INFO"}
        return sorted(
            name
            for name in members
            if name and name not in generated and name not in tracked
        )

    def test_release_artifacts_are_bounded_and_carry_every_skill(self, tmp_path):
        skill_root = self.ROOT / ".claude" / "skills"
        skill_files = sorted(
            path.relative_to(skill_root).as_posix()
            for path in skill_root.rglob("*")
            if path.is_file()
        )
        assert skill_files
        for artifact in self._build(tmp_path):
            members = self._members(artifact)
            fixture_sources = self._ocr_fixture_sources()
            unexpected = self._unexpected_members(artifact, members)
            assert not unexpected, (
                f"{artifact.name} carries files outside allowed roots: "
                f"{unexpected[:10]}. "
                "A release artifact is irrevocable once published."
            )
            if artifact.suffix != ".whl":
                missing_fixtures = sorted(fixture_sources - set(members))
                assert not missing_fixtures, (
                    f"{artifact.name} omits OCR fixture sources: {missing_fixtures[:10]}"
                )
                untracked = self._untracked_sdist_members(members)
                assert not untracked, (
                    f"{artifact.name} carries untracked source files: {untracked[:10]}. "
                    "Build and publish from one committed source identity."
                )
            if artifact.suffix == ".whl":
                leaked_fixtures = sorted(fixture_sources & set(members))
                assert not leaked_fixtures, (
                    f"{artifact.name} carries development-only OCR fixtures: "
                    f"{leaked_fixtures[:10]}"
                )
                missing = [
                    path
                    for path in skill_files
                    if not any(
                        member.endswith(f"share/malleus/skills/{path}")
                        for member in members
                    )
                ]
            else:
                missing = [
                    path
                    for path in skill_files
                    if f".claude/skills/{path}" not in members
                ]
            assert not missing, (
                f"{artifact.name} omits shipped skill files: {missing}"
            )

    def test_the_guard_would_catch_a_planted_file(self, tmp_path):
        """A guard nobody has seen fail is a guard nobody should trust."""
        planted = tmp_path / "malleus_dev-1.0.0.tar.gz"
        assert self._unexpected_members(
            planted,
            ["README.md", "src/malleus/kg.py", "research/private/README.md"],
        ) == ["research/private/README.md"]

    def test_execution_bundle_names_only_public_python_namespaces(self):
        """Public design notes must not publish adopter-local module names."""
        import re

        text = (self.ROOT / "design" / "EXECUTION_BUNDLE.md").read_text(
            encoding="utf-8"
        )
        code_spans = re.findall(r"(?<!`)`([^`\n]+)`(?!`)", text)
        module_names = {
            value
            for value in code_spans
            if value[0].islower()
            and len(value.split(".")) >= 3
            and all(part.isidentifier() for part in value.split("."))
        }
        non_public = sorted(
            name for name in module_names if not name.startswith("malleus.")
        )
        assert not non_public, (
            "execution-bundle design names a non-public Python namespace: "
            f"{non_public}"
        )


class TestPackagingTargetsAreTracked:
    """Every declared packaging target must exist AND be tracked by git;
    hatchling builds a smaller wheel instead of failing (second
    self-inquisition H3, N3). This test is a deliberate tripwire: it stays
    red until the manifest and its targets are committed together."""

    def test_declared_targets_exist_and_are_tracked(self):
        import subprocess
        try:
            import tomllib
        except ModuleNotFoundError:  # Python 3.10
            import tomli as tomllib
        root = Path(__file__).parent.parent
        if not (root / ".git").exists():
            pytest.skip("not a git checkout")
        config = tomllib.loads((root / "pyproject.toml").read_text())
        declared = list(config["tool"]["hatch"]["build"]["include"])
        declared += config["tool"]["pytest"]["ini_options"]["testpaths"]
        missing, untracked = [], []
        for entry in declared:
            filesystem_entry = entry.removeprefix("/")
            if any(char in entry for char in "*?["):
                targets = sorted(root.glob(filesystem_entry))
                if not targets:
                    missing.append(entry)
            else:
                targets = [root / filesystem_entry]
                if not targets[0].exists():
                    missing.append(entry)
                    continue
            for target in targets:
                relative = target.relative_to(root).as_posix()
                probe = subprocess.run(
                    ["git", "ls-files", "--error-unmatch", relative],
                    cwd=root,
                    capture_output=True,
                )
                if probe.returncode != 0:
                    untracked.append(relative)
        assert not missing, f"declared but absent: {missing}"
        assert not untracked, (
            f"declared in pyproject but not committed: {untracked}. "
            "Commit the manifest and its targets as one unit."
        )


class TestReleaseWorkflowIsFailClosed:
    """Publishing can start only from the exact version tag on main history."""

    ROOT = Path(__file__).parent.parent
    RELEASE = ROOT / ".github" / "workflows" / "release.yml"
    CI = ROOT / ".github" / "workflows" / "tests.yml"

    def _jobs(self):
        return yaml.safe_load(self.RELEASE.read_text(encoding="utf-8"))["jobs"]

    def _validation_script(self):
        return "\n".join(
            step.get("run", "")
            for step in self._jobs()["validate-release"]["steps"]
        )

    def test_release_has_no_manual_publish_path(self):
        workflow = self.RELEASE.read_text(encoding="utf-8")
        assert "workflow_dispatch" not in workflow
        assert re.search(
            r'^on:\n  push:\n    tags:\n      - "v\*"$',
            workflow,
            re.MULTILINE,
        )

    def test_validation_precedes_every_release_consumer(self):
        jobs = self._jobs()
        validation = self._validation_script()
        assert '"$GITHUB_REF_TYPE" != "tag"' in validation
        assert 'EXPECTED_TAG="v${FILE_VERSION}"' in validation
        assert '"$GITHUB_REF_NAME" != "$EXPECTED_TAG"' in validation
        assert (
            'git fetch --no-tags origin "+refs/heads/main:refs/remotes/origin/main"'
            in validation
        )
        assert 'git rev-parse "${GITHUB_REF_NAME}^{commit}"' in validation
        assert 'git merge-base --is-ancestor "$TAG_COMMIT" refs/remotes/origin/main' in validation
        for job_name in ("test", "build"):
            assert jobs[job_name]["needs"] == "validate-release"
        assert set(jobs["publish-pypi"]["needs"]) == {"build", "test"}

    def test_release_gate_refuses_non_tags_and_commits_outside_main(self, tmp_path):
        import os
        import subprocess

        origin = tmp_path / "origin.git"
        checkout = tmp_path / "checkout"

        def git(*arguments):
            result = subprocess.run(
                ["git", *arguments],
                cwd=checkout if checkout.exists() else tmp_path,
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, result.stderr

        subprocess.run(
            ["git", "init", "--bare", str(origin)],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "init", "--initial-branch=main", str(checkout)],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )
        git("config", "user.name", "Release Gate Test")
        git("config", "user.email", "release-gate@example.invalid")
        (checkout / "pyproject.toml").write_text(
            '[project]\nname = "fixture"\nversion = "1.2.3"\n',
            encoding="utf-8",
        )
        git("add", "pyproject.toml")
        git("commit", "-m", "main")
        git("remote", "add", "origin", str(origin))
        git("push", "-u", "origin", "main")
        git("switch", "-c", "feature")
        (checkout / "feature.txt").write_text("outside main\n", encoding="utf-8")
        git("add", "feature.txt")
        git("commit", "-m", "feature")
        git("tag", "v1.2.3")

        def run_gate(ref_type, ref_name):
            environment = os.environ.copy()
            environment.update(
                GITHUB_REF_TYPE=ref_type,
                GITHUB_REF_NAME=ref_name,
            )
            return subprocess.run(
                ["bash", "-e", "-o", "pipefail", "-c", self._validation_script()],
                cwd=checkout,
                env=environment,
                capture_output=True,
                text=True,
            )

        assert run_gate("branch", "main").returncode != 0
        assert run_gate("tag", "v9.9.9").returncode != 0
        off_main = run_gate("tag", "v1.2.3")
        assert off_main.returncode != 0
        assert "is not on origin/main" in off_main.stdout

        git("tag", "-f", "v1.2.3", "main")
        assert run_gate("tag", "v1.2.3").returncode == 0

    def test_release_runs_every_supported_python_and_the_research_gate(self):
        from scripts import ci as ci_runner

        jobs = self._jobs()
        supported = [
            "3.10",
            "3.11",
            "3.12",
            "3.13",
        ]
        assert jobs["test"]["strategy"]["matrix"]["python-version"] == supported
        ci_jobs = yaml.safe_load(self.CI.read_text(encoding="utf-8"))["jobs"]
        assert ci_jobs["test"]["strategy"]["matrix"]["python-version"] == supported
        plan = ci_runner.plan("test")
        by_name = {command.name: command.argv for command in plan}
        assert by_name["quality"][1:4] == ("-m", "ruff", "check")
        assert "src/malleus" in by_name["quality"]
        assert str(ci_runner.GRAPH_RECIPE) in by_name["quality"]
        assert by_name["graph-recipe"][1:] == (
            "-m",
            "pytest",
            "-q",
            str(ci_runner.GRAPH_RECIPE / "test_cases.py"),
        )
        for workflow_path in (self.RELEASE, self.CI):
            workflow = workflow_path.read_text(encoding="utf-8")
            assert workflow.count(
                "python scripts/ci.py test --require-clean"
            ) == 1

    def test_workflows_cannot_invoke_undeclared_ruff(self):
        from scripts import ci as ci_runner

        try:
            import tomllib
        except ModuleNotFoundError:  # Python 3.10
            import tomli as tomllib

        config = tomllib.loads((self.ROOT / "pyproject.toml").read_text())
        declared = {
            re.split(r"[<>=!~;\[\s]", dependency, maxsplit=1)[0].lower()
            for dependency in config["project"]["optional-dependencies"]["dev"]
        }
        invokers = [
            command.name
            for command in ci_runner.plan("all")
            if command.argv[1:3] == ("-m", "ruff")
        ]
        assert invokers == ["quality"]
        assert "ruff" in declared


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
    # Nothing was judged, so nothing may be reported as judged. The only
    # other finding permitted here is the coverage note saying so.
    judged = [f for f in report.findings if f.severity != NOTE]
    assert len(judged) == 1
    coverage = [f for f in report.findings if f.subject == "coverage"]
    assert coverage and "did not run" in coverage[0].message


def test_a_construction_failure_names_the_rites_it_skipped(tmp_path):
    """A report showing one heresy and nothing else invites the reader to
    conclude the rest passed. In the field a construction failure left seven
    of eight rites unexecuted across a repository, and the report was
    silent about it."""
    path = tmp_path / "broken.yaml"
    path.write_text("classes: {Thing: {is_a: Entity")
    report = run_rites(path)
    coverage = [f for f in report.findings if f.subject == "coverage"]
    assert coverage, "a construction failure reported no coverage"
    for rite in ("constrained_tongues", "bound_endpoints", "inert_formula"):
        assert rite in coverage[0].message
    assert "Their silence is not a pass." in coverage[0].message


def test_the_coverage_note_respects_disabled_rites(tmp_path):
    """A disabled rite did not run because it was switched off, not because
    the schema stopped it. Naming it here would double-count the loss."""
    path = tmp_path / "broken.yaml"
    path.write_text("classes: {Thing: {is_a: Entity")
    tuned = _tuned_rubric(tmp_path, disable={"inert_formula"})
    report = run_rites(path, rubric_path=tuned)
    coverage = [f for f in report.findings if f.subject == "coverage"]
    assert coverage and "inert_formula" not in coverage[0].message


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
    """Any project gets every shipped procedure; releases refresh them so
    generic learnings flow back."""

    ROOT = Path(__file__).parent.parent
    SKILL_ROOT = ROOT / ".claude" / "skills"
    SKILL_DIRS = tuple(
        path.parent for path in sorted(SKILL_ROOT.glob("*/SKILL.md"))
    )
    SKILL_NAMES = tuple(path.name for path in SKILL_DIRS)

    def _assert_installed_tree(self, target_root):
        for source in self.SKILL_DIRS:
            target = target_root / source.name
            source_files = sorted(
                path for path in source.rglob("*") if path.is_file()
            )
            for source_file in source_files:
                relative = source_file.relative_to(source)
                target_file = target / relative
                assert target_file.is_file(), target_file
                assert target_file.read_bytes() == source_file.read_bytes(), target_file

    def test_every_shipped_skill_has_valid_metadata(self):
        assert self.SKILL_NAMES
        assert len(self.SKILL_NAMES) == len(set(self.SKILL_NAMES))
        for skill_dir in self.SKILL_DIRS:
            skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            assert skill_text.startswith("---\n"), skill_dir
            _, frontmatter, _ = skill_text.split("---", 2)
            metadata = yaml.safe_load(frontmatter)
            assert metadata["name"] == skill_dir.name
            assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["name"])
            assert isinstance(metadata["description"], str)
            assert metadata["description"].strip()
            assert set(metadata) == {"name", "description"}

            agent_path = skill_dir / "agents" / "openai.yaml"
            agent = yaml.safe_load(agent_path.read_text(encoding="utf-8"))["interface"]
            assert isinstance(agent["display_name"], str) and agent["display_name"].strip()
            assert isinstance(agent["short_description"], str)
            assert 25 <= len(agent["short_description"]) <= 64
            assert f"${skill_dir.name}" in agent["default_prompt"]

    def test_skill_files_are_explicit_packaging_targets(self):
        try:
            import tomllib
        except ModuleNotFoundError:  # Python 3.10
            import tomli as tomllib
        config = tomllib.loads((self.ROOT / "pyproject.toml").read_text())
        included = {
            entry.removeprefix("/")
            for entry in config["tool"]["hatch"]["build"]["include"]
        }
        expected = {
            path.relative_to(self.ROOT).as_posix()
            for skill_dir in self.SKILL_DIRS
            for path in skill_dir.rglob("*")
            if path.is_file()
        }
        missing = sorted(expected - included)
        assert not missing, f"skill files absent from package allowlist: {missing}"

    def test_malleus_dev_skill_carries_the_accepted_modularity_doctrine(self):
        skill_dir = self.SKILL_ROOT / "malleus-dev"
        skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        normalized_skill = " ".join(skill.split())
        doctrine = (
            skill_dir / "references" / "UNIX_DESIGN_DOCTRINE.md"
        ).read_text(encoding="utf-8")
        assert "LinkML is not the protocol" in skill
        assert "Any custom frontend may replace LinkML" in skill
        assert "must run without LinkML installed" in skill
        assert (
            "a second implementation passes the same conformance suite"
            in normalized_skill
        )
        rules = {
            "Modularity",
            "Clarity",
            "Composition",
            "Separation",
            "Simplicity",
            "Parsimony",
            "Transparency",
            "Robustness",
            "Representation",
            "Least surprise",
            "Silence",
            "Repair",
            "Economy",
            "Generation",
            "Optimization",
            "Diversity",
            "Extensibility",
        }
        missing_rules = sorted(
            rule for rule in rules if f"| {rule} |" not in doctrine
        )
        assert not missing_rules, f"Unix doctrine omits rules: {missing_rules}"

    def test_malleus_dev_skill_keeps_profiles_and_fixtures_in_their_roles(self):
        skill = (
            self.SKILL_ROOT / "malleus-dev" / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(skill.split())
        for classification in (
            "PROTOCOL_INVARIANT",
            "OPTIONAL_PROFILE",
            "REFERENCE_IMPLEMENTATION",
            "CONFORMANCE_FIXTURE",
            "ADOPTER_CHOICE",
        ):
            assert classification in skill
        for requirement in (
            "lowest affected profile",
            "guarantees omitted",
            "compiler-enabled profile",
            "EXECUTOR_ONLY",
            "SINGLE_LEDGER_CHANGE_SET",
            "KnowledgeChangeSet",
            "genesis change set",
            "non-governed and non-accepted",
            "second conforming interpreter",
            "self-inquisition",
            "not repository or protocol conformance",
        ):
            assert requirement in normalized

    def test_inquisitor_scopes_schema_rites_and_has_a_malleus_self_branch(self):
        skill = (
            self.SKILL_ROOT / "malleus-inquisitor" / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(skill.split())
        for requirement in (
            "Locate claimed profiles before schemas",
            "only for the root ontology profile",
            "## Malleus-self branch",
            "protocol_role_is_explicit",
            "optional_profile_stays_optional",
            "protocol_authority_is_data",
            "single_ledger_knowledge_change",
            "Never treat its purity seal as repository conformance",
            "Quiet Bell, Neutral Greenhouse, Small Shop, and CYP450",
            "Only a bounded, frozen test input, answer key, or scenario",
            "| claim | role | evidence | unsupported transfer | verdict |",
        ):
            assert requirement in normalized
        assert "every future example as conformance fixtures" not in normalized

    def test_acolyte_carries_the_nascent_project_playbook(self):
        skill = (
            self.SKILL_ROOT / "malleus-acolyte" / "SKILL.md"
        ).read_text(encoding="utf-8")
        section = " ".join(
            skill.split("## Starting a project with no schema", 1)[1]
            .split("\n## ", 1)[0]
            .split()
        )
        required = (
            "proposal, not accepted knowledge",
            "Downstream assessment material is not an input",
            "malleus-inquisitor install-skills --agent codex --project .",
            "supersedes the earlier capability probe and ADOPTION_GUIDE.md pre-read",
            "Do not inspect home directories, local checkouts, the network, or undeclared repository documentation",
            "required capability or artifact is absent",
            "Model only concepts, properties, relations, values, and distinctions materially supported",
            "Never invent a missing value, count, record, relation, or epistemic status",
            "Do not collapse two source concepts",
            "metrology`, `chronology`, and `research",
            "pack-grounding",
            "pack-conformance",
            "extend a pack concept before extending root",
            (
                "the rite reads only classes whose `is_a` is a Malleus root "
                "directly"
            ),
            "DIRECT_ROOT_GROUNDING_REQUIRED",
            (
                "it reports every ill-formed block and entry in one refusal "
                "too, sorted, each item naming its subject, its entry index "
                "and the closed field set that position requires"
            ),
            "annotations: grounding: tag: grounding value: area:",
            "vocabulary_url:",
            "borrowed_terms:",
            "invented_terms: []",
            "must equal one of three closed forms exactly",
            "requires `invention_search` beside it",
            "`none_found: true` and `search`",
            (
                "each entry carries exactly `vocabulary`, `vocabulary_url` "
                "and `borrowed_terms`"
            ),
            "state-version`, `source-assertion`, or `object-event",
            "Event admissibility follows the profile's declared Event role",
            "Steps 6 through 9 are the governed-history branch",
            "choose an exact history profile before proposing the ontology",
            "For schema-only adoption, stop after step 5",
            "For typed-graph-only adoption",
            "OntologyRegistry",
            "KnowledgeGraph.from_records",
            "stop before step 6",
            "malleus-compiler contract",
            "malleus-compiler history create",
            "malleus-compiler retain",
            "malleus-compiler capture",
            "malleus-compiler populate",
            "malleus-compiler admit",
            "malleus-compiler replay",
            "malleus-compiler query",
            "malleus-compiler trace",
            "population_retention_events",
            "Keep instances out of schema vocabulary",
            "Keep protocol, provenance, ledger, policy, and query machinery out",
            (
                "provenance locators, meaning block IDs, assertion IDs, and "
                "retained-input IDs, belong to the capture and the ledger, "
                "never to a domain slot"
            ),
            (
                "Identifiers the source reports as facts about the domain are "
                "domain slots and belong in the ontology: a DOI, a dataset "
                "URL, a grant number, an accession"
            ),
            (
                "a claim-bearing record carries `assertion_locator`, the "
                "opaque route back to the retained assertion, and "
                "`statement_sha256`, the digest of its exact text, and "
                "`statement` stays empty unless the record's `Source` "
                "declares a licence that permits reproducing the sentence"
            ),
            "Labels identify records",
            "document capture",
            "coverage of the retained reading is the objective",
            "never the smallest query- or answer-changing subset",
            (
                'overrides the global "smallest observation", "Build only what '
                'changes the answer", and "Build less" rules for document capture'
            ),
            (
                "locate the span in the named block by a "
                "whitespace-insensitive anchor and copy the block's own bytes"
            ),
            "never retype the text and never clean it up",
            (
                "verify every statement is a substring of its block after "
                "whitespace collapse"
            ),
            (
                "Every block ID in `assertions` and in `nothing_assertable` is "
                "taken from the reading's own block inventory; never construct "
                "one"
            ),
            "neutral population plan",
            "every concrete Entity and Relation type",
            (
                "The `records` object carries an `events` envelope beside "
                "`entities` and `relations`"
            ),
            (
                "the bound profile's `ontology_roles.event` is nonempty and "
                "the accepted ontology declares the type"
            ),
            (
                "`event_participations` additionally need an "
                "`EventParticipation` type"
            ),
            "FAMILY_NOT_ADMITTED",
            "canonical_census_bytes",
            "REVIEWED` or `UNTOUCHED",
            "FULLY_FORMALIZED`, `PARTLY_FORMALIZED`, or `UNFORMALIZED",
            "A reviewed block is not thereby formalized",
            "uncaptured assertions remain invisible",
            "UNTOUCHED",
            "Preserve source units and values",
            (
                "set `quantity_kind_class` to it and keep the source's own "
                "wording in `quantity_kind`, which stays open and is never "
                "rewritten to fit the class"
            ),
            "explicit evidence-bearing operation",
            "typed gaps",
            "NO_DOMAIN_CHANGE",
            "compile_population_plan",
            "prepare_population_change",
            "PopulationPreparation",
            "STRUCTURAL_HISTORY_BUNDLE",
            "create_structural_history",
            "prepared.change_set is not None",
            "admit_structural_change",
            "does not establish source truth, domain adequacy, or epistemic correctness",
            "Never write a `CHECK_RECORDED` outcome by hand",
            "prepared.change_set is None",
            "do not call `history.admit`",
            "KnowledgeChangeHistory.reopen",
            "trace_population_record",
            "compile_contract_revision",
            "one working session by default",
            "at most two additive revision rounds",
            "Stop when another addition would require invention",
            "incomplete captures, gaps, and typed refusals as results",
            "query-shaped vocabulary",
            (
                "The producer writes one file, `document-population.json`, "
                "with exactly three top-level keys: `capture`, `records`, and "
                "`supersessions`"
            ),
            "the producer never writes a contract identity",
            (
                "the parent or `malleus-compiler capture` computes "
                "`contract_identity` from the compiled contract"
            ),
            "current private-v0 shape, not a stable wire",
            "reading object is illustrative input, not a live grammar or closed shape",
            "reading_bytes`, `capture_bytes`, `capture_id`, `plan_id`, `contract_identity`, `records`, and `supersessions",
            "canonical JSON bytes",
            "after whitespace normalization",
            "must name a known reading block",
            "If `formalized_by` is empty, at least one typed gap is required",
            "Every formalization `record_id` and `path` must resolve",
            "raw bytes of the declared reading input exactly as supplied",
            (
                "`capture.reading_sha256` is `sha256:` followed by the "
                "SHA-256 of those same bytes"
            ),
            "READING_MISMATCH",
            (
                "every key under a record's `properties`, and both endpoints "
                "of a relation record, must be named by at least one "
                "assertion's formalization target"
            ),
            "`type` and `id` are not derived",
            (
                "UNDERIVED_FIELD` once, naming every such field in one sorted "
                "detail with the rule that closes them"
            ),
            "Every `nothing_assertable` block ID must exist",
            (
                "naming every non-verbatim assertion with its block and every "
                "unknown block ID from `assertions` and from "
                "`nothing_assertable` in one sorted detail"
            ),
            "it does not stop at the first such defect",
            "CALCULATED`, `CONTESTED`, `HYPOTHESISED`, `MEASURED`, `NEGATED`, or `STATED",
            "INTERVAL_NOT_EXPRESSIBLE",
            "AGGREGATE_ONLY",
            "MODALITY_NOT_EXPRESSIBLE",
            "REQUIRED_FIELD_ABSENT_IN_SOURCE",
            "TYPE_ABSENT",
            "RELATION_ABSENT",
        )
        for phrase in required:
            assert phrase in section
        assert "The command-line compiler stops at contract compilation" not in section
        assert "stops at the first block whose shape is wrong" not in section
        assert "naming the first such field it meets" not in section
        assert "replace-with-PartialEffectiveContract.identity" not in skill
        assert "stops at the first such defect" not in section
        steps = (
            "Retain the source boundary",
            "Choose the Malleus level",
            "Look for vocabulary before inventing it",
            "Propose the project ontology",
            "Run the structural gates and compile exact sources",
            "Capture before formalising",
            "Compile, then admit",
            "Reopen, replay, and inspect",
            "Grow only from recorded gaps",
            "Stop honestly",
        )
        assert [section.index(step) for step in steps] == sorted(
            section.index(step) for step in steps
        )
        assert section.index("Choose the Malleus level") < section.index(
            "Look for vocabulary before inventing it"
        ) < section.index("Propose the project ontology")
        assert section.index("one working session by default") < section.index(
            "compile_contract_revision"
        )
        assert section.index("at most two additive revision rounds") < section.index(
            "compile_contract_revision"
        )
        for leaked in (
            "paper",
            "brief",
            "gpt-5.6-sol",
            "sonnet",
            "opus",
            "small shop",
            "quiet bell",
            "neutral greenhouse",
            "cyp450",
            "answer key",
            "answer value",
            "query binding",
            "evaluation criter",
        ):
            assert leaked not in section.lower()

    def test_acolyte_grounding_block_passes_the_live_rite(self):
        """The block the skill tells a project to copy is run through the
        checker it must satisfy. A prose example is wrong until proven
        otherwise, and this one cost a fresh producer two ontology attempts
        when the skill named the rite and showed no block."""
        from malleus.inquisition.pack_grounding import validate_pack_grounding

        skill = (
            self.SKILL_ROOT / "malleus-acolyte" / "SKILL.md"
        ).read_text(encoding="utf-8")
        section = skill.split("## Starting a project with no schema", 1)[1].split(
            "\n## ", 1
        )[0]
        blocks = re.findall(r"```yaml\n(.*?)```", section, re.S)
        assert len(blocks) == 1, "the section carries exactly one grounding block"
        schema = textwrap.dedent(
            """
            id: https://example.org/schema/acolyte-grounding-block
            name: acolyte_grounding_block
            prefixes:
              linkml: https://w3id.org/linkml/
              malleus: https://malleus.dev/schema/
            imports:
              - linkml:types
              - malleus
            """
        ).strip() + "\n" + textwrap.dedent(blocks[0])
        receipt = validate_pack_grounding(schema.encode("utf-8"), role="PROJECT")
        assert receipt.role == "PROJECT"
        assert receipt.grounded_subjects == ("ProjectSensorReading",)

    def test_installed_acolyte_keeps_the_nascent_project_playbook(
        self, tmp_path, capsys
    ):
        assert main(
            ["install-skills", "--project", str(tmp_path), "--agent", "codex"]
        ) == 0
        capsys.readouterr()
        installed = (
            tmp_path / ".codex" / "skills" / "malleus-acolyte" / "SKILL.md"
        ).read_text(encoding="utf-8")
        assert "## Starting a project with no schema" in installed
        assert "malleus-compiler contract" in installed
        assert "malleus-compiler populate" in installed
        assert "malleus-compiler trace" in installed
        assert "neutral population plan" in installed

    def test_nascent_document_template_runs_through_the_public_adapter(
        self, tmp_path, capsys
    ):
        from hashlib import sha256
        from importlib import import_module
        from inspect import signature

        assert main(
            ["install-skills", "--agent", "codex", "--project", str(tmp_path)]
        ) == 0
        capsys.readouterr()
        installed_skill = (
            tmp_path / ".codex" / "skills" / "malleus-acolyte" / "SKILL.md"
        )
        source_skill = self.SKILL_ROOT / "malleus-acolyte" / "SKILL.md"
        assert installed_skill.read_bytes() == source_skill.read_bytes()
        skill = installed_skill.read_text(encoding="utf-8")
        def _block(marker):
            region = skill.split(f"<!-- {marker}:start -->", 1)[1].split(
                f"<!-- {marker}:end -->", 1
            )[0]
            return json.loads(region.split("```json", 1)[1].split("```", 1)[0])

        template = _block("malleus-nascent-document-template")
        harness = _block("malleus-nascent-document-harness")
        assert "schema" not in template
        assert "documentation_example" not in template
        assert "schema" not in harness["reading"]
        assert set(template) == {"capture", "records", "supersessions"}
        assert set(harness) == {
            "accepted_gap_kinds",
            "accepted_modalities",
            "adapter_call",
            "reading",
        }
        assert tuple(harness["adapter_call"]) == (
            "capture_bytes",
            "capture_id",
            "contract_identity",
            "plan_id",
            "reading_bytes",
            "records",
            "supersessions",
        )
        modalities = [
            "CALCULATED",
            "CONTESTED",
            "HYPOTHESISED",
            "MEASURED",
            "NEGATED",
            "STATED",
        ]
        assert harness["accepted_modalities"] == modalities
        gap_kinds = [
            "INTERVAL_NOT_EXPRESSIBLE",
            "AGGREGATE_ONLY",
            "MODALITY_NOT_EXPRESSIBLE",
            "REQUIRED_FIELD_ABSENT_IN_SOURCE",
            "TYPE_ABSENT",
            "RELATION_ABSENT",
        ]
        assert harness["accepted_gap_kinds"] == gap_kinds

        reading_bytes = json.dumps(
            harness["reading"],
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
        capture = template["capture"]
        capture["assertions"][0]["gaps"] = [
            {"kind": kind, "statement": f"Example gap: {kind}"}
            for kind in gap_kinds
        ]
        assert capture["reading_sha256"] == "sha256:" + sha256(
            reading_bytes
        ).hexdigest()
        assertion = capture["assertions"][0]
        assert set(assertion) == {
            "assertion_time",
            "block",
            "domain_time",
            "formalized_by",
            "gaps",
            "id",
            "modality",
            "statement",
        }
        assert set(assertion["gaps"][0]) == {"kind", "statement"}
        assert set(template["records"]) == {"entities", "events", "relations"}
        assert set(template["records"]["entities"][0]) == {
            "id",
            "properties",
            "type",
        }
        assert set(template["records"]["events"][0]) == {
            "id",
            "properties",
            "type",
        }
        assert set(template["records"]["relations"][0]) == {
            "id",
            "properties",
            "source_id",
            "target_id",
            "type",
        }

        compiler = import_module("malleus.compiler")
        assert capture["schema"] == compiler.DOCUMENT_CAPTURE_GRAMMAR
        assert tuple(signature(compiler.adapt_document_assertions).parameters) == (
            "reading_bytes",
            "capture_bytes",
            "capture_id",
            "plan_id",
            "contract_identity",
            "records",
            "supersessions",
        )
        by_modality = {}
        for modality in modalities:
            candidate_capture = copy.deepcopy(capture)
            candidate_capture["assertions"][0]["modality"] = modality
            by_modality[modality] = compiler.adapt_document_assertions(
                reading_bytes=reading_bytes,
                capture_bytes=json.dumps(
                    candidate_capture,
                    allow_nan=False,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode(),
                capture_id=harness["adapter_call"]["capture_id"],
                plan_id=harness["adapter_call"]["plan_id"],
                contract_identity=harness["adapter_call"]["contract_identity"],
                records=template["records"],
                supersessions=template["supersessions"],
            )
        result = by_modality["STATED"]
        assert {
            json.loads(compilation.capture_bytes)["assertions"][0]["modality"]
            for compilation in by_modality.values()
        } == set(modalities)
        plan = json.loads(result.canonical_plan_bytes)
        census = json.loads(result.canonical_census_bytes)
        assert plan["records"] == template["records"]
        assert [gap["kind"] for gap in plan["gaps"]] == gap_kinds
        assert census["gaps_by_kind"] == {kind: 1 for kind in gap_kinds}
        assert census["blocks"] == {
            "block:1": "REVIEWED",
            "block:2": "UNTOUCHED",
            "block:3": "REVIEWED",
        }
        assert census["blocks_reviewed"] == 2
        assert census["blocks_total"] == 3
        assert census["assertions"] == {
            "FULLY_FORMALIZED": 1,
            "PARTLY_FORMALIZED": 1,
            "UNFORMALIZED": 0,
        }

    def test_nascent_playbook_names_live_python_and_cli_surfaces(
        self, tmp_path, capsys
    ):
        from importlib import import_module

        compiler = import_module("malleus.compiler")
        malleus = import_module("malleus")
        required = {
            "DOCUMENT_CAPTURE_GRAMMAR",
            "KnowledgeChangeHistory",
            "PopulationPreparation",
            "STRUCTURAL_HISTORY_BUNDLE",
            "adapt_document_assertions",
            "admit_structural_change",
            "compile_contract_revision",
            "compile_population_plan",
            "create_structural_history",
            "prepare_population_change",
            "trace_population_record",
        }
        assert required <= set(compiler.__all__)
        assert all(hasattr(compiler, name) for name in required)
        assert callable(compiler.KnowledgeChangeHistory.admit)
        assert callable(compiler.KnowledgeChangeHistory.reopen)
        assert {"KnowledgeGraph", "OntologyRegistry"} <= set(malleus.__all__)
        assert callable(malleus.KnowledgeGraph.from_records)

        schema = _write_schema(
            tmp_path,
            """
            id: https://example.org/schema/nascent-typed-graph
            name: nascent_typed_graph
            imports:
              - malleus
              - linkml:types
            classes:
              ProjectObject:
                is_a: Entity
            """,
        )
        registry = malleus.OntologyRegistry(schema, import_map=ROOT_MAP)
        graph = malleus.KnowledgeGraph.from_records(
            registry,
            {
                "entities": [
                    {
                        "type": "ProjectObject",
                        "id": "object:1",
                        "properties": {},
                    }
                ]
            },
        )
        assert graph.node_count == 1
        assert graph.get_node("object:1")["type"] == "ProjectObject"

        assert main(
            ["install-skills", "--agent", "codex", "--project", str(tmp_path)]
        ) == 0
        capsys.readouterr()
        pack = bundled_ontology_path("packs", "metrology.yaml")
        assert main(["pack-grounding", str(pack), "--role", "PACK"]) == 0
        capsys.readouterr()
        assert main(["pack-conformance", str(pack), "--against", str(pack)]) == 0
        capsys.readouterr()

        compiler_cli = import_module("malleus.compiler_cli")
        arguments = compiler_cli._parser().parse_args(
            [
                "contract",
                "--root",
                "project",
                "--source",
                "project",
                str(tmp_path / "project.yaml"),
            ]
        )
        assert arguments.command == "contract"

    def test_install_skills_into_a_project(self, tmp_path, capsys):
        assert main(["install-skills", "--project", str(tmp_path)]) == 0
        out = capsys.readouterr().out
        self._assert_installed_tree(tmp_path / ".claude" / "skills")
        for name in self.SKILL_NAMES:
            assert name in out
        # Idempotent refresh: a second run overwrites without error.
        assert main(["install-skills", "--project", str(tmp_path)]) == 0

    def test_install_skills_for_codex(self, tmp_path, capsys):
        assert main(
            ["install-skills", "--project", str(tmp_path), "--agent", "codex"]
        ) == 0
        out = capsys.readouterr().out
        self._assert_installed_tree(tmp_path / ".codex" / "skills")
        for name in self.SKILL_NAMES:
            assert f"installed codex skill: {name}" in out
        assert not (tmp_path / ".claude").exists()

    def test_install_skills_for_both_agents(self, tmp_path):
        assert main(
            ["install-skills", "--project", str(tmp_path), "--agent", "all"]
        ) == 0
        for directory in (".claude", ".codex"):
            self._assert_installed_tree(tmp_path / directory / "skills")


class TestProtocolProfileBoundaries:
    """Mechanical tripwires for the protocol/profile/fixture boundary."""

    ROOT = Path(__file__).parent.parent

    @staticmethod
    def _imported_modules(path: Path) -> set[str]:
        relative = path.relative_to(TestProtocolProfileBoundaries.ROOT / "src")
        package = list(relative.parent.parts)
        modules: set[str] = set()
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
                continue
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.level:
                base = package[: len(package) - node.level + 1]
                if node.module:
                    modules.add(".".join(base + node.module.split(".")))
                else:
                    modules.update(".".join(base + [alias.name]) for alias in node.names)
            elif node.module:
                modules.add(node.module)
        return modules

    def test_core_runtime_does_not_import_research_conformance_or_tests(self):
        forbidden = {"research", "conformance", "tests"}
        offenders = []
        for path in sorted((self.ROOT / "src" / "malleus").rglob("*.py")):
            for module in self._imported_modules(path):
                parts = module.split(".")
                if parts and parts[0] == "malleus":
                    parts = parts[1:]
                if parts and parts[0] in forbidden:
                    offenders.append(f"{path.relative_to(self.ROOT)} -> {module}")
        assert not offenders, (
            "core runtime imports must not depend on research, conformance, "
            f"or test trees: {offenders}"
        )

    def test_root_ontology_does_not_import_domain_or_fixture_ontologies(self):
        root = self.ROOT / "ontology" / "malleus.yaml"
        document = yaml.safe_load(root.read_text(encoding="utf-8"))
        imports = document.get("imports")
        assert imports == ["linkml:types"], (
            "the root ontology profile has one reviewed language-level import; "
            "any added dependency needs an explicit boundary review, got "
            f"{imports!r}"
        )


def test_every_rite_accepted_on_the_roadmap_exists_in_the_rubric():
    """The loop is only closed when an accepted rite ships.

    Five rites were accepted on the roadmap and sat there through a release
    while their code fixes shipped without them, so the lessons an adopter
    paid for never reached anyone else. This reads the roadmap's own `Rite:`
    lines rather than a list maintained beside it, so a rite accepted
    tomorrow is covered without anyone remembering to add it here.
    """
    root = Path(__file__).parent.parent
    roadmap = (root / "ROADMAP.md").read_text(encoding="utf-8")
    declared = set(re.findall(r"^Rite: `(\w+)`", roadmap, re.M))
    assert declared, "no roadmap section declares a rite id; the link rotted"
    rubric = _rubric()
    shipped = {entry["id"] for entry in rubric["mechanical"] + rubric["judgment"]}
    missing = sorted(declared - shipped)
    assert not missing, (
        f"accepted on the roadmap and absent from the rubric: {missing}. "
        "An accepted rite that does not ship never reaches the adopter who "
        "paid for the next one."
    )


def test_the_release_gate_reads_the_same_version_a_parser_would():
    """The gate extracts the version with sed, because a policy gate that
    dies on a missing stdlib module reports a traceback where it owes an
    actionable refusal: `tomllib` is stdlib only from 3.11 and the 3.10 CI
    matrix caught it. This holds the shortcut to the manifest so it cannot
    drift."""
    import subprocess
    try:
        import tomllib
    except ModuleNotFoundError:  # pragma: no cover - 3.10 path
        import tomli as tomllib
    root = Path(__file__).parent.parent
    parsed = tomllib.loads((root / "pyproject.toml").read_text())["project"]["version"]
    extracted = subprocess.run(
        ["sed", "-n", r's/^version = "\(.*\)"$/\1/p', "pyproject.toml"],
        cwd=root, capture_output=True, text=True,
    ).stdout.splitlines()
    assert extracted and extracted[0] == parsed, (
        f"gate would read {extracted[:1]} where the manifest says {parsed!r}"
    )


def test_the_release_gate_step_runs_locally():
    """Run the complete research slice from the shared CI plan.

    The v0.11.0 tag was cut three times. The third failure was this guard's
    own fault: it executed the Ruff half but omitted GraphRecipe. Both fixed
    commands now come from the same plan that release and pull-request CI call.
    """
    import subprocess
    from scripts import ci as ci_runner

    root = Path(__file__).parent.parent
    research_commands = [
        command
        for command in ci_runner.plan("test")
        if command.name in {"quality", "graph-recipe"}
    ]
    assert [command.name for command in research_commands] == [
        "quality",
        "graph-recipe",
    ]
    for command in research_commands:
        result = subprocess.run(
            command.argv,
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, (
            f"shared CI command {command.name!r} fails locally:\n"
            f"{result.stdout[-3000:]}{result.stderr[-2000:]}"
        )
