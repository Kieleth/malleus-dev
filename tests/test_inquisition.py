"""Rites of the Ordo Malleus: each mechanical rite proven on a real schema."""

from __future__ import annotations

import copy
import json
import re
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
                  config=None, drop_keys=None):
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
        path = _tuned_rubric(tmp_path, config={"formula_slot_token": ["formula"]})
        with pytest.raises(RubricError, match="must be a list"):
            _formula_tokens(path)

    def test_missing_rite_section_refuses_with_rubric_error_not_keyerror(self, tmp_path):
        """R3 N3: the first hardening validated `config` and nothing else, so
        a rubric with a good config and no rites raised KeyError downstream."""
        path = tmp_path / "rubric.yaml"
        path.write_text("config:\n  formula_slot_tokens: []\njudgment: []\n")
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
        assert "REDUCED RUBRIC" in out
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
        assert "0 rites disabled" in out
        assert "REDUCED" not in out


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
        with pytest.raises(RubricError, match="only verdict"):
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
        paths += sorted((self.ROOT / ".claude" / "skills").glob("*/SKILL.md"))
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
        private = self.ROOT / "malleus-moving" / "design" / "CLAIM_AND_EXECUTION_DOCTRINE.md"
        if not private.is_file():
            pytest.skip("the paper-program doctrine is not present in this tree")
        doctrine = private.read_text(encoding="utf-8")
        principles = (self.ROOT / "docs" / "PRINCIPLES.md").read_text(encoding="utf-8")
        thesis = ("typed subgraphs as composable epistemic modules whose")
        assert thesis in _flat(doctrine) and thesis in _flat(principles)
        for condition in ("the relevant guardrails pass",
                          "new databases, orchestration layers",
                          "stop before implementation and obtain a decision",
                          # R4 N5: the drift restarted in the other direction
                          # the moment the public copy gained a paragraph.
                          "not closed silently, not deferred silently",
                          "The human decides whether it enters this slice"):
            assert condition in _flat(doctrine), f"doctrine lost: {condition}"
            assert condition in _flat(principles), f"public copy is weaker: {condition}"


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
