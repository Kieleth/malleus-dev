"""Conformance for the OCR evidence-integrity profile (OCR-D001, AUDIT_ONLY).

Each negative case names the decision it defends. A check with no case here is
a claim the profile cannot support.
"""

from __future__ import annotations

import pytest

from malleus.ocr import (
    Bundle,
    Hypothesis,
    OCRAttempt,
    Raster,
    Region,
    ReviewCorrection,
    Selection,
    SourceClass,
    SourceRepresentation,
    canonical_digest,
    verify_bundle,
)
from malleus.ocr.verify import currency_verdict

def D(n: int) -> str:
    """A distinct full-length digest per seed."""
    return "sha256:" + str(n) * 64


def _class(**over):
    base = dict(
        id="class:invoice",
        required_units=("page:1", "page:2"),
        metric_families={"coverage": {"denominator": "declared_units", "threshold": 1.0},
                         "semantics": {"denominator": "required_fields", "threshold": 0.9}},
        temporal_policy="printed_date_is_issue_date",
        frozen_at="2026-08-18T00:00:00+00:00",
    )
    base.update(over)
    return SourceClass(**base)


def _bundle(**over):
    """A conforming bundle: one region, one machine reading, one correction."""
    base = dict(
        id="bundle:1",
        source_class=_class(),
        sources=(SourceRepresentation("src:1", D(1), 2048, "application/pdf", "docs/a.pdf"),),
        rasters=(Raster("ras:1", "src:1", D(2), "render:v1@300dpi"),),
        regions=(Region("reg:1", "ras:1", {"type": "FragmentSelector", "value": "xywh=0,0,10,10"}),),
        attempts=(OCRAttempt("att:1", "reg:1", D(3), {"model": "engine-a@1"}, "COMPLETED", D(4)),),
        hypotheses=(
            Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1", confidence=0.7),
            Hypothesis("hyp:2", "reg:1", D(6), correction_id="cor:1"),
        ),
        corrections=(ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(6)),),
        selections=(Selection("sel:1", "reg:1", ("hyp:1", "hyp:2"), "hyp:2",
                              "human correction supersedes", human_verified=True),),
        observed_units=("page:1", "page:2"),
        data_handling_policy_id="policy:dh:1",
        hostile_content_policy_id="policy:hc:1",
    )
    base.update(over)
    return Bundle(**base)


def test_a_conforming_bundle_verifies():
    result = verify_bundle(_bundle())
    assert result.conforms, [str(d) for d in result.diagnostics]
    assert result.capability == "AUDIT_ONLY"


def test_the_digest_of_a_bundle_object_is_deterministic():
    assert canonical_digest(_class()) == canonical_digest(_class())
    assert canonical_digest(_class()) != canonical_digest(_class(id="class:other"))


class TestIntegrityValues:
    """C6. A truncated digest may be displayed and may never be stored."""

    def test_a_truncated_source_digest_refuses(self):
        bad = SourceRepresentation("src:1", "sha256:abc", 2048, "application/pdf", "d.pdf")
        assert "OCR-D001" in verify_bundle(_bundle(sources=(bad,))).codes()

    def test_an_untagged_digest_refuses(self):
        bad = SourceRepresentation("src:1", "f" * 64, 2048, "application/pdf", "d.pdf")
        assert "OCR-D001" in verify_bundle(_bundle(sources=(bad,))).codes()

    def test_a_truncated_hypothesis_digest_refuses(self):
        bad = Hypothesis("hyp:1", "reg:1", "sha256:dead", attempt_id="att:1")
        assert "OCR-D001" in verify_bundle(_bundle(hypotheses=(bad,))).codes()


class TestCredentialsNeverEnterTheBundle:
    """C6. Detected by construction, not redacted afterwards."""

    @pytest.mark.parametrize("key", ["authorization", "api_key", "X-API-Key", "Cookie"])
    def test_a_secret_in_transport_metadata_refuses(self, key):
        result = verify_bundle(_bundle(transport_metadata={key: "sk-live-1", "status": 200}))
        assert "OCR-D002" in result.codes()

    def test_a_secret_in_attempt_config_refuses(self):
        att = OCRAttempt("att:1", "reg:1", D(3), {"model": "e@1", "token": "t"}, "COMPLETED", D(4))
        assert "OCR-D002" in verify_bundle(_bundle(attempts=(att,))).codes()

    def test_ordinary_transport_metadata_passes(self):
        assert verify_bundle(_bundle(transport_metadata={"status": 200})).conforms


class TestReadingsReachTheirPixels:
    """A reading with no path to source bytes is not evidence of anything."""

    def test_a_hypothesis_over_an_unknown_region_refuses(self):
        orphan = Hypothesis("hyp:9", "reg:missing", D(5), attempt_id="att:1")
        assert "OCR-D003" in verify_bundle(_bundle(hypotheses=(orphan,))).codes()

    def test_a_region_over_an_unknown_raster_refuses(self):
        detached = Region("reg:1", "ras:missing", {"value": "xywh=0,0,1,1"})
        assert "OCR-D003" in verify_bundle(_bundle(regions=(detached,))).codes()

    def test_a_raster_over_an_unknown_source_refuses(self):
        floating = Raster("ras:1", "src:missing", D(2), "render:v1")
        assert "OCR-D003" in verify_bundle(_bundle(rasters=(floating,))).codes()


class TestIdentityPlanesStaySeparate:
    def test_a_correction_may_not_move_the_region(self):
        """Same pixels, corrected text: the region identity survives."""
        moved = (
            Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),
            Hypothesis("hyp:2", "reg:2", D(6), correction_id="cor:1"),
        )
        regions = (*_bundle().regions, Region("reg:2", "ras:1", {"value": "xywh=0,0,9,9"}))
        assert "OCR-D004" in verify_bundle(_bundle(hypotheses=moved, regions=regions)).codes()

    def test_a_hypothesis_with_two_origins_refuses(self):
        both = Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1", correction_id="cor:1")
        assert "OCR-D007" in verify_bundle(_bundle(hypotheses=(both,))).codes()

    def test_a_hypothesis_with_no_origin_refuses(self):
        orphan = Hypothesis("hyp:1", "reg:1", D(5))
        assert "OCR-D007" in verify_bundle(_bundle(hypotheses=(orphan,))).codes()

    def test_retries_do_not_collapse(self):
        """Two attempts on one region are two records, never one."""
        twice = (
            OCRAttempt("att:1", "reg:1", D(3), {"model": "e@1"}, "FAILED"),
            OCRAttempt("att:2", "reg:1", D(3), {"model": "e@1"}, "COMPLETED", D(4)),
        )
        assert verify_bundle(_bundle(attempts=twice)).conforms

    def test_two_attempts_sharing_an_identity_refuse(self):
        collapsed = (
            OCRAttempt("att:1", "reg:1", D(3), {"model": "e@1"}, "FAILED"),
            OCRAttempt("att:1", "reg:1", D(3), {"model": "e@1"}, "COMPLETED", D(4)),
        )
        assert "OCR-D005" in verify_bundle(_bundle(attempts=collapsed)).codes()

    def test_a_correction_must_retain_what_it_reviewed(self):
        only_child = (Hypothesis("hyp:2", "reg:1", D(6), correction_id="cor:1"),)
        assert "OCR-D006" in verify_bundle(_bundle(hypotheses=only_child)).codes()


class TestHumanVerificationCannotBeClaimed:
    """An unreviewed transcript may not present itself as reviewed."""

    def test_a_selection_claiming_review_without_one_refuses(self):
        result = verify_bundle(_bundle(
            corrections=(),
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),),
            selections=(Selection("sel:1", "reg:1", ("hyp:1",), "hyp:1", "legacy",
                                  human_verified=True),),
        ))
        assert "OCR-D008" in result.codes()

    def test_the_same_selection_without_the_claim_passes(self):
        result = verify_bundle(_bundle(
            corrections=(),
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),),
            selections=(Selection("sel:1", "reg:1", ("hyp:1",), "hyp:1", "legacy"),),
        ))
        assert result.conforms, [str(d) for d in result.diagnostics]

    def test_a_selection_may_not_select_what_it_did_not_consider(self):
        sel = (Selection("sel:1", "reg:1", ("hyp:1",), "hyp:2", "unconsidered"),)
        assert "OCR-D011" in verify_bundle(_bundle(selections=sel)).codes()


class TestPrecommitmentAndPolicy:
    """C3, C4, C5, C8."""

    def test_an_unfrozen_source_class_refuses(self):
        assert "OCR-D009" in verify_bundle(_bundle(source_class=_class(frozen_at=" "))).codes()

    def test_no_declared_metric_family_refuses(self):
        assert "OCR-D012" in verify_bundle(_bundle(source_class=_class(metric_families={}))).codes()

    @pytest.mark.parametrize("field", ["data_handling_policy_id", "hostile_content_policy_id"])
    def test_an_unbound_policy_declaration_refuses(self, field):
        assert "OCR-D010" in verify_bundle(_bundle(**{field: None})).codes()

    def test_the_profile_enforces_that_policy_exists_never_what_it_says(self):
        """C5: the declaration is mandatory, its content is the adopter's."""
        assert verify_bundle(_bundle(data_handling_policy_id="policy:anything")).conforms


class TestStalenessIsTwoProperties:
    """C7. Collapsing these would make engine comparison impossible."""

    def test_changed_bytes_invalidate(self):
        assert currency_verdict({"source_digest": D(1)}, {"source_digest": D(2)}) == "INVALIDATED"

    @pytest.mark.parametrize("key", ["prompt", "model", "ontology", "mapping", "policy"])
    def test_changed_configuration_demotes_without_voiding(self, key):
        before = {"source_digest": D(1), key: "a"}
        assert currency_verdict(before, {**before, key: "b"}) == "DEMOTED"

    def test_two_engines_over_the_same_bytes_remain_comparable(self):
        """The older reading is demoted, not void, so it can still be scored."""
        before = {"source_digest": D(1), "model": "engine-a@1"}
        after = {"source_digest": D(1), "model": "engine-b@1"}
        assert currency_verdict(before, after) == "DEMOTED"

    def test_an_unchanged_configuration_stays_current(self):
        assert currency_verdict({"source_digest": D(1)}, {"source_digest": D(1)}) == "CURRENT"


def test_every_diagnostic_code_has_a_case():
    """A check with no negative case is a claim the profile cannot support."""
    from malleus.ocr.verify import CODES
    source = open(__file__).read()
    missing = [code for code in CODES if code not in source]
    assert not missing, f"diagnostics with no conformance case: {missing}"


def test_the_profile_declares_what_it_cannot_prove():
    """Proof boundaries are part of the contract, not a disclaimer."""
    import malleus.ocr as pkg
    for phrase in ("does not perform OCR", "AUDIT_ONLY"):
        assert phrase in pkg.__doc__
    import malleus.ocr.verify as v
    assert "does not prove source authenticity" in v.__doc__


def test_the_conformance_projection_is_current():
    """Doctrine: generate repetitive projections from the authoritative
    contract, and never promote a projection into authority. If this fails,
    run `conformance/ocr/v0/generate.py` rather than editing JSON."""
    import json
    from pathlib import Path
    from malleus.ocr.verify import profile_projection
    root = Path(__file__).resolve().parents[1]
    shipped = json.loads((root / "conformance" / "ocr" / "v0" / "profile.json").read_text())
    assert shipped == profile_projection(), (
        "conformance projection is stale; run conformance/ocr/v0/generate.py"
    )


def test_the_projection_states_both_sides_of_the_boundary():
    import json
    from pathlib import Path
    shipped = json.loads(
        (Path(__file__).resolve().parents[1] / "conformance" / "ocr" / "v0" / "profile.json").read_text()
    )
    assert shipped["does_not_prove"], "a profile that claims no limits claims too much"
    assert shipped["selector_profile_replaceable"] is True


class TestOntologyGovernance:
    """The planes are typed records under the root primitives, not loose
    dataclasses. Every case below was granted a purity seal by 0.11.0, whose
    verifier had no schema to consult: the dataclass proved a field was a
    string and nothing proved the string meant anything."""

    def test_an_attempt_status_outside_the_enum_is_refused(self):
        bundle = _bundle(attempts=(
            OCRAttempt("att:1", "reg:1", D(3), {"model": "engine-a@1"}, "banana", D(4)),
        ))
        result = verify_bundle(bundle)
        assert "OCR-D013" in result.codes()
        assert "attempt_status" in str(result.diagnostics[0])

    def test_a_review_verdict_outside_the_enum_is_refused(self):
        bundle = _bundle(corrections=(
            ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "looks fine", D(6)),
        ))
        assert "OCR-D013" in verify_bundle(bundle).codes()

    def test_a_byte_count_that_is_not_an_integer_is_refused(self):
        bundle = _bundle(sources=(
            SourceRepresentation("src:1", D(1), "2048", "application/pdf", "docs/a.pdf"),
        ))
        assert "OCR-D013" in verify_bundle(bundle).codes()

    def test_a_human_verified_flag_that_is_not_a_boolean_is_refused(self):
        bundle = _bundle(selections=(
            Selection("sel:1", "reg:1", ("hyp:1", "hyp:2"), "hyp:2", "r", human_verified="yes"),
        ))
        assert "OCR-D013" in verify_bundle(bundle).codes()

    def test_a_freeze_timestamp_that_is_not_a_timestamp_is_refused(self):
        """OCR-D009 only ever asked whether frozen_at was non-blank, so
        'last tuesday' froze a source class for a whole release."""
        assert "OCR-D013" in verify_bundle(_bundle(source_class=_class(frozen_at="last tuesday"))).codes()

    def test_the_profile_registry_is_replaceable(self):
        """Doctrine rule 6: the default implementation is ordinary. A caller
        supplying its own registry gets the same path, not a lesser one."""
        from malleus.ocr.verify import profile_registry
        assert verify_bundle(_bundle(), registry=profile_registry()).conforms


# Every dataclass field either reaches a graph slot under its own name or is
# named here with the slot it is content-addressed into. A field in neither
# column is governed by nothing, which is the defect this whole class exists
# to prevent recurring. Keep it a countable set of argued exceptions rather
# than a silence (rite `unread_declared`).
CONTENT_ADDRESSED = {
    ("SourceClass", "metric_families"): "metric_families_digest",
    ("Region", "selector"): "selector_digest",
    ("OCRAttempt", "config_identity"): "config_identity_digest",
    ("EvidenceBundle", "transport_metadata"): "transport_metadata_digest",
}
CONTAINED = {
    ("EvidenceBundle", name): "member_ids"
    for name in ("sources", "rasters", "regions", "attempts",
                 "hypotheses", "corrections", "selections")
}
RENAMED = {
    ("Raster", "source_id"): "source_representation_id",
    ("OCRAttempt", "status"): "attempt_status",
    ("ReviewCorrection", "verdict"): "review_verdict",
    ("EvidenceBundle", "source_class"): "source_class_id",
}


class TestTheCarrierAndTheSchemaCannotDrift:
    """The checking thing and the checked thing must be compared by something.
    bundle.py is a carrier; ontology/domains/ocr.yaml is the authority. This
    is the only thing that notices when they stop agreeing."""

    def _planes(self):
        from dataclasses import fields
        from malleus.ocr.verify import PLANES, profile_registry
        bundle = _bundle()
        registry = profile_registry()
        for attribute, type_name, _family in PLANES:
            obj = bundle if attribute == "bundle" else (
                bundle.source_class if attribute == "source_class"
                else getattr(bundle, attribute)[0]
            )
            yield type_name, obj, fields(obj), registry

    def test_every_record_key_is_a_slot_the_schema_declares(self):
        for type_name, obj, _fields, registry in self._planes():
            declared = set(registry.effective_slots(type_name))
            unknown = set(obj.record()) - declared
            assert not unknown, f"{type_name} records undeclared slots {sorted(unknown)}"

    def test_every_required_slot_is_produced_by_a_conforming_object(self):
        for type_name, obj, _fields, registry in self._planes():
            record = obj.record()
            missing = [
                name for name, slot in registry.effective_slots(type_name).items()
                if slot.required and name not in record
            ]
            assert not missing, f"{type_name} never produces required {missing}"

    def test_every_dataclass_field_reaches_the_graph_or_is_declared(self):
        """Reaching the graph means the schema declares a slot for it, not
        that this fixture happened to populate it: an unset optional field is
        absent from one record and still governed."""
        for type_name, _obj, dataclass_fields, registry in self._planes():
            declared = set(registry.effective_slots(type_name))
            for field_ in dataclass_fields:
                name = field_.name
                if name in declared:
                    continue
                target = (
                    CONTENT_ADDRESSED.get((type_name, name))
                    or RENAMED.get((type_name, name))
                    or CONTAINED.get((type_name, name))
                )
                assert target, (
                    f"{type_name}.{name} reaches no slot and is not declared as "
                    f"content-addressed or renamed"
                )
                assert target in declared, (
                    f"{type_name}.{name} declares {target}, which the schema does not"
                )

    def test_the_declared_exceptions_are_all_real(self):
        """An exception list that outlives its exceptions is a lie that passes."""
        from dataclasses import fields
        from malleus.ocr.verify import PLANES
        import malleus.ocr.bundle as mod
        by_type = {t: a for a, t, _ in PLANES}
        for (type_name, field_name) in {**CONTENT_ADDRESSED, **RENAMED, **CONTAINED}:
            assert type_name in by_type, f"{type_name} is not a plane"
            cls = getattr(mod, "Bundle" if type_name == "EvidenceBundle" else type_name)
            assert field_name in {f.name for f in fields(cls)}, (
                f"{type_name}.{field_name} is declared as an exception and does not exist"
            )


def test_the_profile_ontology_is_packaged():
    """A schema the wheel does not carry is a schema the adopter cannot load."""
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    pyproject = (root / "pyproject.toml").read_text()
    assert '"/ontology/domains/ocr.yaml"' in pyproject, "not in the build include list"
    assert 'share/malleus/ontology/domains/ocr.yaml' in pyproject, "not in shared data"


def test_every_plane_is_governed():
    """No identity plane may be carried by a dataclass alone."""
    from dataclasses import fields
    from malleus.ocr.verify import PLANES
    import malleus.ocr.bundle as mod
    planes = {t for _a, t, _f in PLANES}
    carriers = {
        name for name in dir(mod)
        if isinstance(getattr(mod, name), type)
        and hasattr(getattr(mod, name), "__dataclass_fields__")
    }
    ungoverned = {c for c in carriers if c not in planes and c != "Bundle"}
    assert not ungoverned, f"dataclasses governed by no schema: {sorted(ungoverned)}"
    for plane in planes:
        cls = getattr(mod, "Bundle" if plane == "EvidenceBundle" else plane)
        assert fields(cls), f"{plane} carries no fields"


class TestThePortableDocument:
    """The artifact is the document, not the Python object. An adapter in
    another language conforms by emitting one of these; the dataclasses are
    one carrier for the records and were, for a release, the only one."""

    def test_a_document_round_trips_through_json(self):
        import json
        from malleus.ocr.bundle import Bundle
        bundle = _bundle()
        assert Bundle.from_document(json.loads(json.dumps(bundle.document()))) == bundle

    def test_a_document_names_its_profile_and_version(self):
        from malleus.ocr.bundle import DOCUMENT_VERSION, PROFILE_ID, PROFILE_VERSION
        document = _bundle().document()
        assert document["profile"] == PROFILE_ID
        assert document["profile_version"] == PROFILE_VERSION
        assert document["document_version"] == DOCUMENT_VERSION

    @pytest.mark.parametrize("mutate,fragment", [
        (lambda d: d.update(profile="somebody.else"), "will not guess"),
        (lambda d: d.update(profile_version="v1"), "will not guess"),
        (lambda d: d.update(document_version=2), "will not guess"),
        (lambda d: d.update(extra=1), "undeclared keys"),
        (lambda d: d.pop("profile"), "does not declare"),
        (lambda d: d["bundle"]["regions"][0].update(rotation=90), "undeclared keys"),
        (lambda d: d["bundle"]["sources"][0].pop("digest"), "missing required keys"),
        (lambda d: d["bundle"].update(pages=[]), "undeclared keys"),
        (lambda d: d["bundle"].update(regions={}), "must be an array"),
        (lambda d: d["bundle"].pop("source_class"), "no source class"),
    ])
    def test_a_document_this_reader_cannot_verify_is_refused(self, mutate, fragment):
        """Fail closed on both directions of version drift. A newer document
        is refused for the same reason an older one is: a reader that repairs
        what it does not understand reports on something nobody wrote."""
        import json
        from malleus.ocr.bundle import Bundle, BundleError
        document = json.loads(json.dumps(_bundle().document()))
        mutate(document)
        with pytest.raises(BundleError) as raised:
            Bundle.from_document(document)
        assert fragment in str(raised.value)

    def test_reading_a_document_is_all_or_nothing(self):
        """No partial bundle escapes a refusal."""
        import json
        from malleus.ocr.bundle import Bundle, BundleError
        document = json.loads(json.dumps(_bundle().document()))
        document["bundle"]["hypotheses"][1].pop("region_id")
        with pytest.raises(BundleError):
            Bundle.from_document(document)


class TestThePackagedConformanceCases:
    """An adopter with only the wheel must be able to run something. Until
    these shipped, 'passes the conformance suite' meant 'cloned our repo'."""

    def test_every_declared_case_is_installed_and_expects_what_it_gets(self):
        from malleus.ocr.bundle import Bundle
        from malleus.ocr.conformance import CASES, load_case
        assert CASES, "a conformance suite with no cases is a claim with no evidence"
        for name in CASES:
            case = load_case(name)
            assert case["case"] == name
            assert case["description"].strip()
            result = verify_bundle(Bundle.from_document(case["document"]))
            assert sorted(set(result.codes())) == sorted(case["expect"]), (
                f"case {name} no longer means what it says"
            )

    def test_the_suite_contains_a_refusal(self):
        """A verifier that refuses nothing is indistinguishable from one that
        is not running, so a corpus of only accepted bundles proves nothing."""
        from malleus.ocr.conformance import CASES, load_case
        assert any(load_case(name)["expect"] for name in CASES)
        assert any(not load_case(name)["expect"] for name in CASES)

    def test_an_undeclared_case_is_refused_rather_than_read(self):
        from malleus.ocr.conformance import load_case
        with pytest.raises(KeyError):
            load_case("../../../etc/passwd")

    def test_the_cases_and_the_cli_are_packaged(self):
        from pathlib import Path
        pyproject = (Path(__file__).resolve().parents[1] / "pyproject.toml").read_text()
        from malleus.ocr.conformance import CASES
        for name in CASES:
            assert f'"/src/malleus/ocr/cases/{name}.json"' in pyproject, f"{name} is not packaged"
        for module in ("cli.py", "conformance.py", "__main__.py"):
            assert f'"/src/malleus/ocr/{module}"' in pyproject, f"{module} is not packaged"
        assert 'malleus-ocr = "malleus.ocr.cli:main"' in pyproject


class TestTheCommandLine:
    """The operator's path. Verified by running it, not by reading it."""

    def _run(self, argv, capsys):
        from malleus.ocr.cli import main
        code = main(argv)
        return code, capsys.readouterr().out

    def test_a_conforming_document_exits_zero(self, tmp_path, capsys):
        import json
        path = tmp_path / "bundle.json"
        path.write_text(json.dumps(_bundle().document()))
        code, out = self._run([str(path)], capsys)
        assert code == 0 and "CONFORMS" in out

    def test_a_refused_document_exits_one_and_names_every_diagnostic(self, tmp_path, capsys):
        import json
        path = tmp_path / "bundle.json"
        bundle = _bundle(attempts=(
            OCRAttempt("att:1", "reg:1", D(3), {"model": "engine-a@1"}, "banana", D(4)),
        ))
        path.write_text(json.dumps(bundle.document()))
        code, out = self._run([str(path)], capsys)
        assert code == 1 and "OCR-D013" in out and "REFUSED" in out

    def test_an_unreadable_document_exits_two_and_is_not_confused_with_a_refusal(
        self, tmp_path, capsys
    ):
        """A malformed file and a non-conforming bundle are different answers.
        Collapsing them tells an adopter their evidence failed when their JSON
        did."""
        path = tmp_path / "bundle.json"
        path.write_text("{not json")
        code, out = self._run([str(path)], capsys)
        assert code == 2 and "cannot read" in out
        missing = tmp_path / "absent.json"
        code, _ = self._run([str(missing)], capsys)
        assert code == 2

    def test_the_packaged_suite_passes_from_the_command_line(self, capsys):
        code, out = self._run(["--conformance"], capsys)
        assert code == 0 and "conformance suite passed" in out

    def test_the_header_states_what_is_running(self, capsys):
        """`guidance_newer_than_runtime`: one command answers which profile,
        which malleus and which ontology bytes produced this verdict."""
        import malleus
        _code, out = self._run(["--conformance"], capsys)
        assert malleus.__version__ in out
        assert "AUDIT_ONLY" in out and "ocr.yaml" in out

    def test_exactly_one_input_is_required(self, capsys):
        from malleus.ocr.cli import main
        for argv in ([], ["--conformance", "--case", "conforming"]):
            with pytest.raises(SystemExit):
                main(argv)


def test_an_emitter_that_never_touches_the_carrier_conforms():
    """Replacement is empirical. This emitter builds the document as literal
    JSON, imports no plane class and knows nothing about dataclasses, which is
    the position an adapter written in another language is in. If it can only
    be produced by constructing nine Python objects, the profile is a module
    with a schema attached, not a portable contract."""
    from malleus.ocr.bundle import Bundle
    digest = lambda seed: "sha256:" + str(seed) * 64  # noqa: E731
    document = {
        "profile": "malleus.ocr.evidence_integrity",
        "profile_version": "v0",
        "document_version": 1,
        "bundle": {
            "id": "bundle:hand-written",
            "source_class": {
                "id": "class:receipt",
                "required_units": ["page:1"],
                "metric_families": {"coverage": {"denominator": "declared_units",
                                                 "threshold": 1.0}},
                "temporal_policy": "undated_class_carries_no_timeline",
                "frozen_at": "2026-08-19T00:00:00+00:00",
                "inventory_basis": "derived_then_confirmed",
            },
            "sources": [{"id": "src:a", "digest": digest(7), "byte_length": 91,
                         "media_type": "image/tiff", "locator": "scans/a.tiff"}],
            "rasters": [{"id": "ras:a", "source_id": "src:a", "digest": digest(8),
                         "render_contract": "render:v1@600dpi"}],
            "regions": [{"id": "reg:a", "raster_id": "ras:a",
                         "selector": {"type": "FragmentSelector", "value": "xywh=1,1,4,4"},
                         "selector_profile": "w3c-web-annotation+iiif"}],
            "attempts": [{"id": "att:a", "region_id": "reg:a", "request_digest": digest(9),
                          "config_identity": {"model": "engine-b@2"},
                          "status": "COMPLETED", "response_digest": digest(1),
                          "unavailable_reason": None}],
            "hypotheses": [{"id": "hyp:a", "region_id": "reg:a", "text_digest": digest(2),
                            "attempt_id": "att:a", "correction_id": None,
                            "confidence": 0.9}],
            "corrections": [],
            "selections": [{"id": "sel:a", "region_id": "reg:a", "candidate_ids": ["hyp:a"],
                            "selected_id": "hyp:a", "reason": "only candidate",
                            "human_verified": False}],
            "observed_units": ["page:1"],
            "data_handling_policy_id": "policy:local-only",
            "hostile_content_policy_id": "policy:isolate",
            "transport_metadata": {},
        },
    }
    result = verify_bundle(Bundle.from_document(document))
    assert result.conforms, [str(d) for d in result.diagnostics]


# Two tables that exist because of one mistake. The coverage machinery was in
# the schema, complete and unread: required_units as denominator,
# observed_units as numerator, metric_families carrying each measure's divisor
# and threshold. A pass/fail rule was designed to replace it while it sat
# there. `docs/IMPLEMENTATION_STATUS.md` already said "no coverage measurement
# exists" and `verify.py` already said "a decision with no check is prose".
# Both statements were true, neither was enforced, and the author of both did
# not consult either. These tables make the answer a lookup instead of a
# recollection.

UNBUILT = "UNBUILT: "
STRUCTURAL = "STRUCTURAL: "

# What discharges each decision in the record. A diagnostic code, or an honest
# statement that nothing does.
DECISION_DISCHARGE = {
    "A1": STRUCTURAL + "capability is AUDIT_ONLY; nothing here writes to a ledger",
    "A2": STRUCTURAL + "the profile ontology imports the root and adds nothing to it",
    "A3": STRUCTURAL + "no portability claim is made anywhere in the package",
    "B1": STRUCTURAL + "no code path reads confidence, so it cannot control acceptance",
    "B2": STRUCTURAL + "AttemptStatus and ReviewVerdict keep the six states distinct",
    "B3": UNBUILT + "reviewer separateness is recorded and never checked (roadmap C1)",
    "C1": STRUCTURAL + "selector_profile is a declared slot; the default holds no privilege",
    "C2": UNBUILT + "dependency-closed partial claims; required_units has no reader",
    "C3": UNBUILT + "coverage is declared and never measured; only emptiness is checked",
    "C4": ("OCR-D013",),
    "C5": ("OCR-D010",),
    "C6": ("OCR-D001", "OCR-D002"),
    "C7": STRUCTURAL + "currency_verdict separates invalidation from demotion",
    "C8": ("OCR-D009",),
}

# What reads each slot the profile ontology declares. Being written into a
# record is emitting, not reading, and the difference is the whole lesson.
SLOT_READERS = {
    "required_units": UNBUILT + "the C2 denominator; nothing computes with it",
    "observed_units": UNBUILT + "the C3 numerator; nothing computes with it",
    "metric_families_digest": STRUCTURAL + "content address only",
    "metric_family_names": ("OCR-D012",),
    "temporal_policy": UNBUILT + "declared per C4; no ordering code consults it",
    "frozen_at": ("OCR-D009",),
    "inventory_basis": UNBUILT + "records how the inventory was confirmed; unused until C2",
    "source_class_id": STRUCTURAL + "binds the bundle to its frozen precommitment",
    "member_ids": STRUCTURAL + "answers which records the bundle contains",
    "data_handling_policy_id": ("OCR-D010",),
    "hostile_content_policy_id": ("OCR-D010",),
    "transport_metadata_digest": ("OCR-D002",),
    "digest": ("OCR-D001",),
    "byte_length": ("OCR-D013",),
    "media_type": STRUCTURAL + "declares what the bytes are; not otherwise consumed",
    "locator": STRUCTURAL + "where the bytes came from; never treated as authentication",
    "source_representation_id": ("OCR-D003",),
    "render_contract": UNBUILT + "no check compares two renderings of one source",
    "raster_id": ("OCR-D003",),
    "selector_digest": STRUCTURAL + "content address only",
    "selector_profile": STRUCTURAL + "declares which selector spec applies",
    "region_id": ("OCR-D003", "OCR-D004"),
    "text_digest": ("OCR-D001",),
    "attempt_id": ("OCR-D003", "OCR-D007"),
    "correction_id": ("OCR-D003", "OCR-D007"),
    "confidence": UNBUILT + "deliberately unread: mandate B1 bars it from acceptance",
    "candidate_ids": ("OCR-D011",),
    "selected_id": ("OCR-D008", "OCR-D011"),
    "reason": UNBUILT + "why a reading was selected; recorded, never judged",
    "human_verified": ("OCR-D008",),
    "request_digest": ("OCR-D001",),
    "config_identity_digest": STRUCTURAL + "content address; drives currency_verdict",
    "attempt_status": ("OCR-D013",),
    "response_digest": ("OCR-D001",),
    "unavailable_reason": UNBUILT + "required reading per the slot's own description; unenforced",
    "reviewed_hypothesis_id": ("OCR-D006",),
    "reviewer_id": UNBUILT + "mandate B3 cannot be checked without actor registration",
    "review_verdict": ("OCR-D013",),
    "corrected_text_digest": UNBUILT + "not compared to the hypothesis it produced",
    "predecessor_id": UNBUILT + "correction chains are recorded and never walked",
}


def _entries(table):
    from malleus.ocr.verify import CODES
    for key, value in table.items():
        if isinstance(value, tuple):
            for code in value:
                assert code in CODES, f"{key} names {code}, which is not a diagnostic"
        else:
            assert value.startswith((UNBUILT, STRUCTURAL)), f"{key} has no honest discharge"
            assert value.split(": ", 1)[1].strip(), f"{key} gives no reason"


class TestNothingIsDischargedByAssertion:
    """A decision with no check is prose, and a slot with no reader is
    decoration. Both sentences were already written in this package. Neither
    was enforced, so a coverage design was invented on top of a coverage
    design that was already there."""

    def test_every_decision_in_the_record_states_what_discharges_it(self):
        import re
        from pathlib import Path
        record = (Path(__file__).resolve().parents[1] / "design"
                  / "OCR_EVIDENCE_INTEGRITY_DECISIONS.md").read_text()
        declared = set(re.findall(r"\*\*([ABC][0-9])[.*]", record))
        assert declared, "the decision record stopped declaring ids; this guard rotted"
        missing = sorted(declared - set(DECISION_DISCHARGE))
        assert not missing, (
            f"decisions with nothing recorded about their discharge: {missing}. "
            "Name the diagnostic, or say UNBUILT and why."
        )
        _entries(DECISION_DISCHARGE)

    def test_every_slot_the_schema_declares_states_what_reads_it(self):
        import re
        from pathlib import Path
        schema = (Path(__file__).resolve().parents[1] / "ontology" / "domains"
                  / "ocr.yaml").read_text()
        body = schema.split("\nslots:\n", 1)[1]
        declared = set(re.findall(r"^  ([a-z_]+):", body, re.M))
        assert declared, "the schema stopped declaring slots; this guard rotted"
        missing = sorted(declared - set(SLOT_READERS))
        assert not missing, (
            f"slots with no recorded reader: {missing}. Name the diagnostic that "
            "consumes it, or say UNBUILT and why. Being written into a record is "
            "emitting, not reading."
        )
        stale = sorted(set(SLOT_READERS) - declared)
        assert not stale, f"recorded readers for slots that no longer exist: {stale}"
        _entries(SLOT_READERS)

    def test_the_unbuilt_set_is_visible_rather_than_inferred(self):
        """The number that matters. If this is a surprise, that is the finding."""
        unbuilt = sorted(k for k, v in SLOT_READERS.items()
                         if isinstance(v, str) and v.startswith(UNBUILT))
        assert len(unbuilt) >= 10, (
            "the unbuilt list shrank without this count being updated; confirm "
            "each one really gained a reader"
        )
