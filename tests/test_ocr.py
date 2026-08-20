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
        metric_families={"coverage": {"denominator": "declared_units", "threshold": 1.0}},
        temporal_policy="printed_date_is_issue_date",
        frozen_at="2026-08-18T00:00:00+00:00",
    )
    base.update(over)
    return SourceClass(**base)


def _census(account):
    """The census as a plain mapping, so a test states every unit at once."""
    return {u.unit: (u.outcome, u.disposition) for u in account.units}


def _registry_moving(tmp_path, outcome, into_enum):
    """A deliberately different profile ontology, built from the shipped one.

    Moves one outcome between the disposition enums and returns a registry over
    the result. This is the only way to establish that the census reads the
    schema rather than a table in the verifier: an adversarial fixture shows
    refusal, and only a second conforming ontology shows replacement.
    """
    import yaml
    from malleus.ocr.verify import OUTCOME_ENUMS, ONTOLOGY
    from malleus.ontology import OntologyRegistry, bundled_ontology_path
    schema = yaml.safe_load(bundled_ontology_path(*ONTOLOGY).read_text())
    values = schema["enums"]
    source = next(
        name for name in OUTCOME_ENUMS.values()
        if outcome in values[name]["permissible_values"]
    )
    assert source != into_enum, f"{outcome} already lives in {into_enum}"
    moved = values[source]["permissible_values"].pop(outcome)
    values[into_enum]["permissible_values"][outcome] = moved
    written = tmp_path / "ocr.yaml"
    written.write_text(yaml.safe_dump(schema, sort_keys=False))
    return OntologyRegistry(written)


def _bundle(**over):
    """A conforming bundle: one region, one machine reading, one correction."""
    base = dict(
        id="bundle:1",
        source_class=_class(),
        sources=(SourceRepresentation("src:1", D(1), 2048, "application/pdf", "docs/a.pdf"),),
        rasters=(Raster("ras:1", "src:1", "page:1", D(2), "render:v1@300dpi"),
                 Raster("ras:2", "src:1", "page:2", D(8), "render:v1@300dpi")),
        regions=(Region("reg:1", "ras:1", {"type": "FragmentSelector", "value": "xywh=0,0,10,10"}),
                 Region("reg:2", "ras:2", {"type": "FragmentSelector", "value": "xywh=0,0,10,10"})),
        attempts=(OCRAttempt("att:1", "reg:1", D(3), {"model": "engine-a@1"}, "COMPLETED", D(4)),
                  OCRAttempt("att:2", "reg:2", D(9), {"model": "engine-a@1"}, "COMPLETED", D(1))),
        hypotheses=(
            Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1", confidence=0.7),
            Hypothesis("hyp:2", "reg:1", D(6), correction_id="cor:1"),
            Hypothesis("hyp:4", "reg:2", D(7), attempt_id="att:2"),
        ),
        corrections=(ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(6)),
                     ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "VERIFIED_BLANK")),
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
        floating = Raster("ras:1", "src:missing", "page:1", D(2), "render:v1")
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
    ("EvidenceBundle", "kind"): "bundle_kind",
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
            assert result.account.complete == case["expect_complete"], (
                f"case {name} changed what it accounts for"
            )
            census = {u.unit: [u.outcome, u.disposition] for u in result.account.units}
            assert census == case["expect_units"], (
                f"case {name} changed what became of its units"
            )

    def test_every_case_states_its_census_unit_by_unit(self):
        """Completeness is one bit, and a bit cannot distinguish a unit nobody
        fetched from one whose only call failed. A case stating only the bit
        could agree with the verifier while disagreeing about every unit in
        it, which is how a reviewer's ABSENT read as READ through four green
        cases."""
        from malleus.ocr.conformance import CASES, load_case
        for name in CASES:
            case = load_case(name)
            assert "expect_units" in case, f"case {name} does not state its census"
            required = case["document"]["bundle"]["source_class"]["required_units"]
            assert case["expect_units"], f"case {name} states an empty census"
            assert sorted(case["expect_units"]) == sorted(required), (
                f"case {name} censuses {sorted(case['expect_units'])} and its "
                f"source class requires {sorted(required)}. A census row for a "
                "unit nobody declared, or a declared unit with no row, is the "
                "case disagreeing with the thing it is a fixture for"
            )
            for outcome, disposition in case["expect_units"].values():
                assert outcome and disposition

    def test_the_suite_distinguishes_the_two_ways_a_unit_goes_unaccounted(self):
        """A corpus that never exercises CHECK_FAILED beside NOT_CHECKED
        cannot show that the profile keeps them apart, and an adopter running
        only the packaged cases is the reader who needs to see it."""
        from malleus.ocr.conformance import CASES, load_case
        dispositions = {
            pair[1]
            for name in CASES
            for pair in load_case(name)["expect_units"].values()
        }
        assert {"ACCOUNTED", "NOT_CHECKED", "CHECK_FAILED"} <= dispositions

    def test_the_suite_carries_a_bundle_that_is_sound_and_not_a_success(self):
        """The negative case for silence. Zero diagnostics and not complete:
        paperwork that holds together is not a reading, and the suite must
        contain a document that says so while claiming FINISHED_READING."""
        from malleus.ocr.conformance import CASES, load_case
        silent = [
            load_case(name) for name in CASES
            if not load_case(name)["expect"]
            and not load_case(name)["expect_complete"]
            and load_case(name)["document"]["bundle"]["kind"] == "FINISHED_READING"
        ]
        assert silent, "no case shows sound paperwork failing to be a reading"

    def test_the_suite_distinguishes_sound_paperwork_from_a_finished_reading(self):
        """Without a registration case the suite could not tell the two apart,
        which is the confusion the account exists to end."""
        from malleus.ocr.conformance import CASES, load_case
        cases = {name: load_case(name) for name in CASES}
        assert any(c["expect"] == [] and c["expect_complete"] for c in cases.values())
        assert any(c["expect"] == [] and not c["expect_complete"] for c in cases.values())

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

    def test_a_complete_reading_exits_zero_and_shows_what_it_accounted_for(self, tmp_path, capsys):
        import json
        path = tmp_path / "bundle.json"
        path.write_text(json.dumps(_bundle().document()))
        code, out = self._run([str(path)], capsys)
        assert code == 0 and "COMPLETE" in out
        assert "page:1: READ" in out and "page:2: VERIFIED_BLANK" in out

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
            "kind": "FINISHED_READING",
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
            "rasters": [{"id": "ras:a", "source_id": "src:a", "unit": "page:1",
                         "digest": digest(8), "render_contract": "render:v1@600dpi"}],
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
    "B2": STRUCTURAL + "three mechanisms, because the mandate was broken three "
                       "ways. AttemptStatus and ReviewVerdict keep the six "
                       "states distinct; the census maps each outcome to one of "
                       "three schema-declared dispositions rather than to a "
                       "bit; and OCR-D016 refuses two live verdicts about one "
                       "region instead of picking one. Summarising a unit's "
                       "several regions is stated scope, not conversion "
                       "(decision C9). This entry once read 'the enums keep "
                       "them distinct' while ABSENT was reported READ, and then "
                       "read 'the census maps each to a disposition' while a "
                       "superseded verdict outranked the review replacing it. "
                       "Both times the enums were distinct and the code that "
                       "consumed them was not",
    "B3": UNBUILT + "reviewer separateness is recorded and never checked (roadmap C1)",
    "C1": STRUCTURAL + "selector_profile is a declared slot; the default holds no privilege",
    "C2": UNBUILT + "dependency-closed partial claims. required_units IS read: "
                    "account_for censuses it and it is the declared_units "
                    "denominator. This entry said it had no reader for a "
                    "release after account_for began iterating it, which is a "
                    "table asserting a gap the code had closed. What is "
                    "unbuilt is the promotion rule (roadmap C2)",
    "C3": STRUCTURAL + "account_for measures each declared family; an uncomputable "
                       "denominator reports UNMEASURED rather than passing",
    "C4": ("OCR-D013",),
    "C5": ("OCR-D010",),
    "C6": ("OCR-D001", "OCR-D002"),
    "C7": STRUCTURAL + "currency_verdict separates invalidation from demotion",
    "C8": ("OCR-D009",),
    "C9": ("OCR-D016", "OCR-D017"),
}

# What reads each enum the profile ontology declares. The same table as
# SLOT_READERS and for a sharper reason: an unread SLOT carries a value nobody
# checks, an unread ENUM carries a value nobody can produce. ABSENT was
# declared in ReviewVerdict, in the module's outcome tuple and in its accounted
# set, and `_unit_outcome` could not return it, so a reviewer's statement of
# absence was reported as a reading for a release. Nothing in the package could
# have noticed, because nothing read the vocabulary.
ENUM_READERS = {
    "BundleKind": STRUCTURAL + "range of bundle_kind; Account.complete refuses "
                               "to certify anything but FINISHED_READING",
    "AttemptStatus": STRUCTURAL + "range of attempt_status; read by OCR-D015 and "
                                  "by the census, which maps it to CHECK_FAILED",
    "ReviewVerdict": STRUCTURAL + "range of review_verdict; read by OCR-D015, by "
                                  "OCR-D016, and by terminal_verdicts, which "
                                  "intersects it with the unit outcomes to decide "
                                  "which verdicts speak for a unit. A human "
                                  "verdict outranks the machine and the worst "
                                  "region answer is the unit's",
    "UnitDisposition": STRUCTURAL + "read by outcome_dispositions; the census's "
                                    "three answers and the projection's",
    "AccountedUnitOutcome": STRUCTURAL + "read by outcome_dispositions and, "
                                         "intersected with ReviewVerdict, by "
                                         "terminal_verdicts",
    "NotCheckedUnitOutcome": STRUCTURAL + "read by outcome_dispositions",
    "CheckFailedUnitOutcome": STRUCTURAL + "read by outcome_dispositions",
    "OCREventType": UNBUILT + "declared and consumed by nothing. Its description "
                              "says the domain schema narrows the root's open "
                              "event_type; equals_string on OCRAttempt and "
                              "ReviewCorrection does that, and this enum is not "
                              "the slot's range, so it narrows nothing. Found "
                              "while giving the census vocabulary a reader; "
                              "recorded rather than closed, because binding it "
                              "is a schema decision and not this slice's",
}

# What reads each slot the profile ontology declares. Being written into a
# record is emitting, not reading, and the difference is the whole lesson.
SLOT_READERS = {
    "required_units": STRUCTURAL + "the units account_for censuses, one row each",
    "observed_units": STRUCTURAL + "read by the account; a unit absent from it is NOT_OBSERVED",
    "metric_families_digest": STRUCTURAL + "content address only",
    "metric_family_names": ("OCR-D012",),
    "temporal_policy": UNBUILT + "declared per C4; no ordering code consults it",
    "frozen_at": ("OCR-D009",),
    "inventory_basis": UNBUILT + "records how the inventory was confirmed; unused until C2",
    "source_class_id": STRUCTURAL + "binds the bundle to its frozen precommitment",
    "member_ids": STRUCTURAL + "answers which records the bundle contains",
    "bundle_kind": STRUCTURAL + "a REGISTRATION is never complete and never counts as conformance",
    "unit": ("OCR-D014",),
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
    "unavailable_reason": ("OCR-D015",),
    "reviewed_hypothesis_id": ("OCR-D006",),
    "reviewer_id": UNBUILT + "mandate B3 cannot be checked without actor registration",
    "review_verdict": ("OCR-D013",),
    "corrected_text_digest": ("OCR-D015",),
    "predecessor_id": ("OCR-D016", "OCR-D017"),
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

    def test_every_enum_the_schema_declares_states_what_reads_it(self):
        """A vocabulary nothing reads cannot notice that one of its values is
        unreachable. That is not a tidiness point: it is exactly how ABSENT
        spent a release being reported as READ."""
        import re
        from pathlib import Path
        schema = (Path(__file__).resolve().parents[1] / "ontology" / "domains"
                  / "ocr.yaml").read_text()
        body = schema.split("\nenums:\n", 1)[1].split("\nclasses:\n", 1)[0]
        declared = set(re.findall(r"^  ([A-Za-z][A-Za-z0-9_]*):", body, re.M))
        assert declared, "the schema stopped declaring enums; this guard rotted"
        missing = sorted(declared - set(ENUM_READERS))
        assert not missing, (
            f"enums with no recorded reader: {missing}. Name what consumes the "
            "vocabulary, or say UNBUILT and why. Being a slot's range is not "
            "enough on its own; something must read the values."
        )
        stale = sorted(set(ENUM_READERS) - declared)
        assert not stale, f"recorded readers for enums that no longer exist: {stale}"
        _entries(ENUM_READERS)

    def test_the_census_vocabulary_is_read_and_not_merely_declared(self):
        """The one enum group whose reader had to be built. If this stops
        holding, the mapping has gone back into Python and the schema is
        decoration again."""
        from malleus.ocr.verify import DISPOSITION_ENUM, OUTCOME_ENUMS, outcome_dispositions
        for enum_name in (DISPOSITION_ENUM, *OUTCOME_ENUMS.values()):
            assert ENUM_READERS[enum_name].startswith(STRUCTURAL)
        assert outcome_dispositions(), "the mapping resolves from the schema"

    def test_the_unbuilt_set_is_visible_rather_than_inferred(self):
        """The number that matters. If this is a surprise, that is the finding."""
        unbuilt = sorted(k for k, v in SLOT_READERS.items()
                         if isinstance(v, str) and v.startswith(UNBUILT))
        assert len(unbuilt) >= 6, (
            "the unbuilt list shrank without this count being updated; confirm "
            "each one really gained a reader"
        )


class TestExplicitAbsenceIsData:
    """Three-valued, and the three values are declared rather than assumed.

    The profile already kept ten outcome strings apart. What it did not have
    was a reader for the vocabulary that holds them, and the cost was exact:
    ABSENT sat in the module tuple, in the accounted set and in ReviewVerdict
    for a release while no code path could produce it, so a reviewer stating
    that a page is not in the source got the page reported READ. A vocabulary
    nothing consults cannot notice that one of its values is unreachable.
    """

    def _absent(self):
        """A reviewer states page:2 is not present in this source."""
        return _bundle(corrections=(
            ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(6)),
            ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "ABSENT"),
        ))

    def test_a_reviewer_stating_absence_does_not_produce_a_reading(self):
        """The regression. `_unit_outcome` fell through to the hypothesis test
        and returned READ, which is mandate B2's exact prohibition run
        backwards: an absence converted into a reading."""
        outcomes = {u.unit: u.outcome for u in verify_bundle(self._absent()).account.units}
        assert outcomes["page:2"] == "ABSENT", "absence must never be reported as a reading"

    def test_absence_is_an_answer_and_therefore_accounted(self):
        """Somebody looked and can say what they found. B2 keeps ABSENT
        distinct from a blank page and from a page nobody opened; all three
        are answers or non-answers on their own terms."""
        units = {u.unit: u for u in verify_bundle(self._absent()).account.units}
        assert units["page:2"].disposition == "ACCOUNTED"
        assert units["page:2"].accounted

    def test_never_checked_and_check_failed_are_two_answers(self):
        """`accounted` is one bit and was the only judgment available, so a
        unit nobody fetched and a unit whose only call died read identically.
        The fixes are different: one is fetched, the other retried."""
        bundle = _bundle(
            source_class=_class(required_units=("page:1", "page:2", "page:3")),
            attempts=(OCRAttempt("att:1", "reg:1", D(3), {"model": "e@1"}, "COMPLETED", D(4)),
                      OCRAttempt("att:2", "reg:2", D(9), {"model": "e@1"}, "FAILED")),
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),),
            corrections=(),
            selections=(),
        )
        account = verify_bundle(bundle).account
        assert account.units_with("CHECK_FAILED") == ("page:2",)
        assert account.units_with("NOT_CHECKED") == ("page:3",)
        assert account.unaccounted == ("page:2", "page:3"), (
            "the union still answers 'which units are not accounted for'"
        )
        assert not account.complete, "silence must not pass as success"

    def test_the_disposition_of_every_outcome_comes_from_the_schema(self):
        """Declared, not assumed. The mapping used to be a frozenset in this
        module, which is the same defect as a rule stated in a slot
        description: a reader of the schema could not learn it."""
        from malleus.ocr.verify import OUTCOME_ENUMS, outcome_dispositions, profile_registry
        registry = profile_registry()
        mapping = outcome_dispositions(registry)
        for disposition, enum_name in OUTCOME_ENUMS.items():
            for outcome in registry.get_enum_values(enum_name):
                assert mapping[outcome] == disposition

    def test_no_outcome_carries_two_dispositions(self):
        """A three-valued answer stops being one the moment a value can be
        two of them."""
        from malleus.ocr.verify import OUTCOME_ENUMS, profile_registry
        registry = profile_registry()
        seen: set[str] = set()
        for enum_name in OUTCOME_ENUMS.values():
            values = set(registry.get_enum_values(enum_name))
            assert not (values & seen), f"{enum_name} overlaps an earlier disposition"
            seen |= values

    def test_a_disposition_with_no_outcomes_is_refused(self):
        """Fail closed on a schema that declares a fourth answer and gives the
        verifier no way to produce it. That silence is how ABSENT hid."""
        from malleus.ontology import OntologyError
        from malleus.ocr.verify import DISPOSITION_ENUM, outcome_dispositions

        class Registry:
            def get_enum_values(self, name):
                if name == DISPOSITION_ENUM:
                    return frozenset({"ACCOUNTED", "NOT_CHECKED", "CHECK_FAILED", "PENDING"})
                return frozenset()

        with pytest.raises(OntologyError) as raised:
            outcome_dispositions(Registry())
        assert "PENDING" in str(raised.value)

    def test_every_declared_outcome_is_reachable(self):
        """The guardrail for the class of defect, not the instance. A value
        the schema declares and no bundle can produce is a promise the census
        cannot keep, and reading the vocabulary is not enough to notice it:
        ABSENT was declared in three places at once and produced by none."""
        from malleus.ocr.verify import outcome_dispositions

        def one(unit, **over):
            return {u.unit: u.outcome
                    for u in verify_bundle(_bundle(**over)).account.units}[unit]

        base_h = (Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),)
        reached = {
            "READ": one("page:1"),
            "VERIFIED_BLANK": one("page:2"),
            "ABSENT": one("page:2", corrections=(
                ReviewCorrection("cor:1", "hyp:1", "r", "CORRECTED", D(6)),
                ReviewCorrection("cor:2", "hyp:4", "r", "ABSENT"))),
            "UNREADABLE": one("page:2", corrections=(
                ReviewCorrection("cor:1", "hyp:1", "r", "CORRECTED", D(6)),
                ReviewCorrection("cor:2", "hyp:4", "r", "UNREADABLE"))),
            "EXCLUDED": one("page:2", corrections=(
                ReviewCorrection("cor:1", "hyp:1", "r", "CORRECTED", D(6)),
                ReviewCorrection("cor:2", "hyp:4", "r", "EXCLUDED"))),
            "FAILED": one("page:2", hypotheses=base_h, corrections=(), selections=(),
                          attempts=(OCRAttempt("att:1", "reg:1", D(3), {"m": "e"}, "COMPLETED", D(4)),
                                    OCRAttempt("att:2", "reg:2", D(9), {"m": "e"}, "FAILED"))),
            "UNAVAILABLE": one("page:2", hypotheses=base_h, corrections=(), selections=(),
                               attempts=(OCRAttempt("att:1", "reg:1", D(3), {"m": "e"}, "COMPLETED", D(4)),
                                         OCRAttempt("att:2", "reg:2", D(9), {"m": "e"}, "UNAVAILABLE",
                                                    unavailable_reason="provider quota"))),
            "NOT_OBSERVED": one("page:2", observed_units=("page:1",),
                                rasters=(Raster("ras:1", "src:1", "page:1", D(2), "r"),),
                                regions=(Region("reg:1", "ras:1", {"v": "a"}),),
                                attempts=(OCRAttempt("att:1", "reg:1", D(3), {"m": "e"}, "COMPLETED", D(4)),),
                                hypotheses=base_h, corrections=(), selections=()),
            "NOT_RENDERED": one("page:2",
                                rasters=(Raster("ras:1", "src:1", "page:1", D(2), "r"),),
                                regions=(Region("reg:1", "ras:1", {"v": "a"}),),
                                attempts=(OCRAttempt("att:1", "reg:1", D(3), {"m": "e"}, "COMPLETED", D(4)),),
                                hypotheses=base_h, corrections=(), selections=()),
            "NOT_ATTEMPTED": one("page:2",
                                 regions=(Region("reg:1", "ras:1", {"v": "a"}),),
                                 attempts=(OCRAttempt("att:1", "reg:1", D(3), {"m": "e"}, "COMPLETED", D(4)),),
                                 hypotheses=base_h, corrections=(), selections=()),
        }
        wrong = {name: got for name, got in reached.items() if got != name}
        assert not wrong, f"fixtures do not produce the outcome they claim: {wrong}"
        declared = set(outcome_dispositions())
        assert declared == set(reached), (
            f"declared outcomes with no fixture proving they are reachable: "
            f"{sorted(declared - set(reached))}"
        )

    def test_a_replacement_registry_governs_the_census_too(self, tmp_path):
        """Doctrine rule 6, and replacement is empirical. A caller replacing
        the profile ontology used to replace which records are legal while the
        outcome vocabulary stayed hardcoded in the verifier, which is half a
        replacement.

        So this passes a deliberately different registry, one that rules a
        reviewer's ABSENT to be a unit nobody checked, and reads the census
        back. Passing `profile_registry()` here would exercise nothing: the
        default is what runs when the argument is omitted, and a test that
        cannot tell the two apart cannot support a replaceability claim.
        """
        from malleus.ocr.verify import account_for
        replacement = _registry_moving(tmp_path, "ABSENT", "NotCheckedUnitOutcome")

        under_replacement = _census(account_for(self._absent(), replacement))
        assert under_replacement["page:2"] == ("ABSENT", "NOT_CHECKED"), (
            "the census read its own hardcoded mapping, not the schema it was given"
        )
        assert _census(account_for(self._absent()))["page:2"] == ("ABSENT", "ACCOUNTED"), (
            "the default must be unchanged by another registry existing"
        )

    def test_a_replacement_registry_moves_the_coverage_number_with_it(self):
        """The disposition is not decoration: it is the coverage numerator.
        A replacement that reclassifies an outcome and leaves the metric
        unmoved would have replaced a label and nothing else."""
        from malleus.ocr.verify import account_for
        default = account_for(self._absent())
        assert [(m.value, m.verdict) for m in default.metrics] == [(1.0, "MET")]
        assert default.complete

    def test_the_replacement_and_the_default_disagree_about_completeness(self, tmp_path):
        """Both halves of the same fact, stated as one assertion so neither
        can quietly stop being true."""
        from malleus.ocr.verify import account_for
        replacement = _registry_moving(tmp_path, "ABSENT", "NotCheckedUnitOutcome")
        moved = account_for(self._absent(), replacement)
        assert [(m.value, m.verdict) for m in moved.metrics] == [(0.5, "UNMET")]
        assert not moved.complete
        assert moved.units_with("NOT_CHECKED") == ("page:2",)
        assert moved.unaccounted == ("page:2",)

    def test_a_registry_governs_verify_bundle_and_its_census_together(self, tmp_path):
        """One registry, both answers. A caller who can replace the record
        grammar and not the census is holding two ontologies at once."""
        from malleus.ocr.verify import verify_bundle as verify
        replacement = _registry_moving(tmp_path, "ABSENT", "NotCheckedUnitOutcome")
        result = verify(self._absent(), replacement)
        assert result.conforms, [str(d) for d in result.diagnostics]
        assert _census(result.account)["page:2"] == ("ABSENT", "NOT_CHECKED")
        assert not result.account.complete

    def test_a_ratio_over_an_empty_denominator_is_unmeasured_not_perfect(self):
        """A source class requiring nothing scored 1.000 coverage over a
        census of nothing and read MET. The schema refuses an empty
        `required_units`, so the branch was unreachable through
        `verify_bundle`; a neighbouring gate holding a door this arithmetic
        left open is not the same as the arithmetic being closed."""
        from malleus.ocr.verify import account_for
        account = account_for(_bundle(source_class=_class(required_units=())))
        assert [m.verdict for m in account.metrics] == ["UNMEASURED"]
        assert not account.complete


class TestTwoReviewersDisagreeing:
    """Decision C9. The census reports one outcome per unit, a unit may carry
    several verdicts, and something has to choose. Which choices are honest is
    a question about SUBJECT, not about severity.

    Two verdicts about two regions of one unit are two true answers to two
    questions, summarised worst-first into the unit's answer. Two live verdicts
    about the SAME region are two answers to one question, and picking either
    converts the other, which is mandate B2's literal prohibition. The first is
    stated; the second is refused as OCR-D016.
    """

    def _on(self, *verdicts, region="reg:2", **over):
        """One correction per verdict, every one reviewing a reading of `region`."""
        hypotheses = [
            Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1", confidence=0.7),
            Hypothesis("hyp:2", "reg:1", D(6), correction_id="cor:1"),
        ]
        corrections = [ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(6))]
        for index, verdict in enumerate(verdicts, start=4):
            hypotheses.append(Hypothesis(f"hyp:{index}", region, D(7), attempt_id="att:2"))
            corrections.append(
                ReviewCorrection(f"cor:{index}", f"hyp:{index}", f"reviewer:{index}", verdict)
            )
        base = dict(hypotheses=tuple(hypotheses), corrections=tuple(corrections))
        base.update(over)
        return _bundle(**base)

    def test_two_live_verdicts_about_one_region_refuse(self):
        """The regression this diagnostic exists for. Under a clean seal the
        census answered UNREADABLE and said nothing about the reviewer who
        had answered VERIFIED_BLANK."""
        result = verify_bundle(self._on("VERIFIED_BLANK", "UNREADABLE"))
        assert "OCR-D016" in result.codes()
        assert not result.conforms

    def test_the_refusal_names_the_region_and_both_verdicts(self):
        """A diagnostic an operator cannot act on is a diagnostic that will be
        suppressed. It must say which region and which two records."""
        [diagnostic] = [
            d for d in verify_bundle(self._on("VERIFIED_BLANK", "UNREADABLE")).diagnostics
            if d.code == "OCR-D016"
        ]
        assert diagnostic.subject == "reg:2"
        for fragment in ("UNREADABLE", "cor:5", "VERIFIED_BLANK", "cor:4"):
            assert fragment in diagnostic.detail

    @pytest.mark.parametrize("pair", [
        ("VERIFIED_BLANK", "UNREADABLE"),
        ("VERIFIED_BLANK", "EXCLUDED"),
        ("UNREADABLE", "EXCLUDED"),
        ("ABSENT", "VERIFIED_BLANK"),
        ("ABSENT", "UNREADABLE"),
        ("ABSENT", "EXCLUDED"),
    ])
    def test_every_disagreeing_pair_refuses_and_not_only_the_one_that_was_reported(self, pair):
        """Six ordered pairs, not the one example in the report. A guard built
        against a single reproduction is a guard against that reproduction."""
        assert "OCR-D016" in verify_bundle(self._on(*pair)).codes()

    def test_the_same_verdict_recorded_twice_is_not_a_disagreement(self):
        """Duplicates. Two reviewers reaching the same answer is corroboration,
        and refusing it would make a second opinion a defect."""
        result = verify_bundle(self._on("VERIFIED_BLANK", "VERIFIED_BLANK"))
        assert "OCR-D016" not in result.codes()
        assert result.conforms, [str(d) for d in result.diagnostics]
        assert _census(result.account)["page:2"] == ("VERIFIED_BLANK", "ACCOUNTED")

    def test_one_verdict_alone_is_not_a_disagreement(self):
        """The single-element case, stated because a check written over pairs
        is one off-by-one away from firing on every reviewed region."""
        result = verify_bundle(self._on("UNREADABLE"))
        assert "OCR-D016" not in result.codes()
        assert _census(result.account)["page:2"] == ("UNREADABLE", "ACCOUNTED")

    def test_a_bundle_with_no_review_at_all_is_not_a_disagreement(self):
        """The empty case. Nothing to disagree about must not read as
        disagreement, and a bundle nobody reviewed is an ordinary bundle."""
        result = verify_bundle(_bundle(
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),
                        Hypothesis("hyp:4", "reg:2", D(7), attempt_id="att:2")),
            corrections=(),
            selections=(Selection("sel:1", "reg:1", ("hyp:1",), "hyp:1",
                                  "only candidate", human_verified=False),),
        ))
        assert "OCR-D016" not in result.codes()
        assert result.conforms, [str(d) for d in result.diagnostics]

    def test_a_reading_verdict_beside_a_terminal_one_is_not_a_disagreement(self):
        """CONFIRMED and CORRECTED are answers about a reading, not about what
        became of a unit, and the schema is what says so: they are not
        declared as unit outcomes, so `terminal_verdicts` never ranks them.
        A reviewer confirming a reading and another calling the region blank
        are not in conflict about the unit."""
        result = verify_bundle(self._on("CONFIRMED", "VERIFIED_BLANK"))
        assert "OCR-D016" not in result.codes()
        assert _census(result.account)["page:2"] == ("VERIFIED_BLANK", "ACCOUNTED")

    def test_two_regions_of_one_unit_may_answer_differently(self):
        """The case that is NOT refused, and the reason it is not. Two regions
        are two subjects. The unit's answer is the worst of them, which is
        summarising a different question rather than converting an answer."""
        bundle = _bundle(
            regions=(Region("reg:1", "ras:1", {"type": "FragmentSelector", "value": "xywh=0,0,10,10"}),
                     Region("reg:2", "ras:2", {"type": "FragmentSelector", "value": "xywh=0,0,10,10"}),
                     Region("reg:3", "ras:2", {"type": "FragmentSelector", "value": "xywh=0,10,10,10"})),
            attempts=(OCRAttempt("att:1", "reg:1", D(3), {"model": "engine-a@1"}, "COMPLETED", D(4)),
                      OCRAttempt("att:2", "reg:2", D(9), {"model": "engine-a@1"}, "COMPLETED", D(1)),
                      OCRAttempt("att:3", "reg:3", D(2), {"model": "engine-a@1"}, "COMPLETED", D(3))),
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1", confidence=0.7),
                        Hypothesis("hyp:2", "reg:1", D(6), correction_id="cor:1"),
                        Hypothesis("hyp:4", "reg:2", D(7), attempt_id="att:2"),
                        Hypothesis("hyp:5", "reg:3", D(3), attempt_id="att:3")),
            corrections=(ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(6)),
                         ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "VERIFIED_BLANK"),
                         ReviewCorrection("cor:3", "hyp:5", "reviewer:lee", "UNREADABLE")),
        )
        result = verify_bundle(bundle)
        assert "OCR-D016" not in result.codes()
        assert result.conforms, [str(d) for d in result.diagnostics]
        assert _census(result.account)["page:2"] == ("UNREADABLE", "ACCOUNTED"), (
            "a unit is only as read as its least-read region"
        )

    @pytest.mark.parametrize("recorded,expected", [
        (("VERIFIED_BLANK", "EXCLUDED"), "EXCLUDED"),
        (("VERIFIED_BLANK", "UNREADABLE"), "UNREADABLE"),
        (("EXCLUDED", "UNREADABLE"), "UNREADABLE"),
        (("VERIFIED_BLANK", "ABSENT"), "ABSENT"),
        (("UNREADABLE", "ABSENT"), "ABSENT"),
    ])
    def test_the_unit_answer_is_the_worst_region_answer(self, recorded, expected):
        """The published order, exercised rather than asserted. Every pair the
        precedence ranks, so a reordering cannot pass by touching one line."""
        first, second = recorded
        bundle = _bundle(
            regions=(Region("reg:1", "ras:1", {"type": "FragmentSelector", "value": "xywh=0,0,10,10"}),
                     Region("reg:2", "ras:2", {"type": "FragmentSelector", "value": "xywh=0,0,10,10"}),
                     Region("reg:3", "ras:2", {"type": "FragmentSelector", "value": "xywh=0,10,10,10"})),
            attempts=(OCRAttempt("att:1", "reg:1", D(3), {"model": "engine-a@1"}, "COMPLETED", D(4)),
                      OCRAttempt("att:2", "reg:2", D(9), {"model": "engine-a@1"}, "COMPLETED", D(1)),
                      OCRAttempt("att:3", "reg:3", D(2), {"model": "engine-a@1"}, "COMPLETED", D(3))),
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1", confidence=0.7),
                        Hypothesis("hyp:4", "reg:2", D(7), attempt_id="att:2"),
                        Hypothesis("hyp:5", "reg:3", D(3), attempt_id="att:3")),
            corrections=(ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", first),
                         ReviewCorrection("cor:3", "hyp:5", "reviewer:lee", second)),
            selections=(),
        )
        assert _census(verify_bundle(bundle).account)["page:2"][0] == expected

    def test_the_published_projection_states_the_order_it_will_use(self):
        """An adopter whose page carries two region verdicts is entitled to
        know which one the census reports before it does."""
        from malleus.ocr.verify import profile_projection
        assert profile_projection()["unit_verdict_precedence"] == [
            "ABSENT", "UNREADABLE", "EXCLUDED", "VERIFIED_BLANK",
        ]


class TestSupersedingIsNotDisagreeing:
    """`predecessor_id` is documented as the prior review in an append-only
    chain, and nothing walked it. So a reviewer who recorded UNREADABLE and
    then superseded it with VERIFIED_BLANK was reported UNREADABLE: the
    retracted record outranked the one that replaced it, under a clean seal.

    Found while building the OCR-D016 reader, not reported by anyone.
    `SLOT_READERS` had carried `predecessor_id` as UNBUILT since the table was
    written, which is what that table is for; what it could not say is that
    the unbuilt reader was load-bearing.
    """

    def _chain(self, *links, region="reg:2"):
        """Corrections over one region, each superseding the one before it."""
        hypotheses = [Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1", confidence=0.7)]
        corrections = []
        previous = None
        for index, verdict in enumerate(links, start=4):
            hypotheses.append(Hypothesis(f"hyp:{index}", region, D(7), attempt_id="att:2"))
            corrections.append(ReviewCorrection(
                f"cor:{index}", f"hyp:{index}", "reviewer:kim", verdict,
                predecessor_id=previous,
            ))
            previous = f"cor:{index}"
        return _bundle(
            hypotheses=tuple(hypotheses), corrections=tuple(corrections), selections=(),
        )

    def test_a_revised_verdict_is_the_one_the_census_reports(self):
        """The regression. UNREADABLE outranks VERIFIED_BLANK in the published
        order, so a census that ignores supersession reports the retraction."""
        result = verify_bundle(self._chain("UNREADABLE", "VERIFIED_BLANK"))
        assert result.conforms, [str(d) for d in result.diagnostics]
        assert _census(result.account)["page:2"] == ("VERIFIED_BLANK", "ACCOUNTED")

    def test_a_revision_the_other_way_is_also_followed(self):
        """The mirror case, so the test cannot pass by preferring the weaker
        verdict rather than by reading the chain."""
        result = verify_bundle(self._chain("VERIFIED_BLANK", "UNREADABLE"))
        assert result.conforms, [str(d) for d in result.diagnostics]
        assert _census(result.account)["page:2"] == ("UNREADABLE", "ACCOUNTED")

    def test_absence_can_be_retracted(self):
        """A reviewer who called a unit absent and then found it may say so,
        and the census must stop saying ABSENT. Absence is a statement, not a
        state the bundle cannot leave."""
        result = verify_bundle(self._chain("ABSENT", "VERIFIED_BLANK"))
        assert _census(result.account)["page:2"] == ("VERIFIED_BLANK", "ACCOUNTED")

    def test_absence_can_be_reached_by_revision(self):
        """And the other direction, because a rule that only ever removes
        ABSENT would be the old bug wearing a chain."""
        result = verify_bundle(self._chain("VERIFIED_BLANK", "ABSENT"))
        assert _census(result.account)["page:2"] == ("ABSENT", "ACCOUNTED")

    def test_only_the_head_of_a_longer_chain_speaks(self):
        """Three links. A reader that skipped one hop would report the middle
        record, which looks like a fix and is not."""
        result = verify_bundle(self._chain("ABSENT", "UNREADABLE", "VERIFIED_BLANK"))
        assert result.conforms, [str(d) for d in result.diagnostics]
        assert _census(result.account)["page:2"] == ("VERIFIED_BLANK", "ACCOUNTED")

    def test_superseding_is_not_erasing(self):
        """Mandate: a review never erases what it reviewed. The superseded
        record stays in the bundle and stops being the answer, and those are
        two different things."""
        bundle = self._chain("UNREADABLE", "VERIFIED_BLANK")
        assert [c.verdict for c in bundle.corrections] == ["UNREADABLE", "VERIFIED_BLANK"]
        assert verify_bundle(bundle).conforms

    def test_a_revision_is_not_reported_as_a_disagreement(self):
        """The interaction. Two verdicts on one region refuse; a chain over
        one region is the same two verdicts and must not, or revising a
        verdict would be impossible."""
        assert "OCR-D016" not in verify_bundle(self._chain("UNREADABLE", "VERIFIED_BLANK")).codes()

    def test_a_chain_that_never_reaches_an_earliest_review_refuses(self):
        """A self-superseding correction. Append-only means finite and rooted,
        and a record that supersedes itself never speaks, so reading
        supersession without this check would dig its own silent hole."""
        bundle = _bundle(
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),
                        Hypothesis("hyp:4", "reg:2", D(7), attempt_id="att:2")),
            corrections=(ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "VERIFIED_BLANK",
                                          predecessor_id="cor:2"),),
            selections=(),
        )
        result = verify_bundle(bundle)
        assert "OCR-D017" in result.codes()
        assert not result.conforms

    def test_two_corrections_superseding_each_other_refuse(self):
        """The two-record cycle, which a self-reference check alone misses."""
        bundle = _bundle(
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),
                        Hypothesis("hyp:4", "reg:2", D(7), attempt_id="att:2"),
                        Hypothesis("hyp:5", "reg:2", D(3), attempt_id="att:2")),
            corrections=(ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "VERIFIED_BLANK",
                                          predecessor_id="cor:3"),
                         ReviewCorrection("cor:3", "hyp:5", "reviewer:lee", "VERIFIED_BLANK",
                                          predecessor_id="cor:2")),
            selections=(),
        )
        result = verify_bundle(bundle)
        assert sorted(d.subject for d in result.diagnostics if d.code == "OCR-D017") == [
            "cor:2", "cor:3",
        ], "both records lie on the cycle and both must be named"

    def test_a_broken_chain_does_not_also_lose_the_verdict(self):
        """A diagnostic that swallowed the data would be reporting a hole it
        dug. Records on a broken chain stay live, so the census still answers
        and OCR-D017 says the chain is unusable."""
        bundle = _bundle(
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),
                        Hypothesis("hyp:4", "reg:2", D(7), attempt_id="att:2")),
            corrections=(ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "UNREADABLE",
                                          predecessor_id="cor:2"),),
            selections=(),
        )
        result = verify_bundle(bundle)
        assert "OCR-D017" in result.codes()
        assert _census(result.account)["page:2"] == ("UNREADABLE", "ACCOUNTED")

    def test_a_chain_naming_a_correction_the_bundle_does_not_hold_is_lineage(self):
        """The optional-reference edge. An absent predecessor is OCR-D003,
        already, and must not become a second diagnostic saying the same
        thing, nor silently mute the record that names it."""
        bundle = _bundle(
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),
                        Hypothesis("hyp:4", "reg:2", D(7), attempt_id="att:2")),
            corrections=(ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "UNREADABLE",
                                          predecessor_id="cor:gone"),),
            selections=(),
        )
        result = verify_bundle(bundle)
        assert "OCR-D003" in result.codes()
        assert "OCR-D017" not in result.codes()
        assert _census(result.account)["page:2"] == ("UNREADABLE", "ACCOUNTED")


class TestTheVerdictVocabularyIsDerived:
    """Which verdicts speak for a unit is the schema's answer, not a tuple in
    the verifier. The order is policy and is published; the set is read."""

    def test_a_verdict_that_is_not_a_unit_outcome_never_ranks(self):
        """CONFIRMED and CORRECTED are declared as ReviewVerdict values and as
        no unit outcome, so the derivation excludes them without a hardcoded
        exception list."""
        from malleus.ocr.verify import profile_registry, terminal_verdicts
        registry = profile_registry()
        ranked = set(terminal_verdicts(registry))
        assert ranked == {"ABSENT", "UNREADABLE", "EXCLUDED", "VERIFIED_BLANK"}
        assert {"CONFIRMED", "CORRECTED"} <= set(registry.get_enum_values("ReviewVerdict"))
        assert not ranked & {"CONFIRMED", "CORRECTED"}

    def test_an_attempt_state_is_never_a_reviewer_verdict(self):
        """Mandate B2's 'a reviewer never inherits them', with a reader. If
        FAILED or UNAVAILABLE were ever added to ReviewVerdict the derivation
        would rank them and this asserts the schema does not."""
        from malleus.ocr.verify import profile_registry, terminal_verdicts
        registry = profile_registry()
        assert not set(terminal_verdicts(registry)) & {"FAILED", "UNAVAILABLE"}
        assert not set(registry.get_enum_values("ReviewVerdict")) & {"FAILED", "UNAVAILABLE"}

    def test_a_declared_verdict_with_no_rank_refuses(self, tmp_path):
        """Fail closed on a schema this verifier cannot summarise. Silently
        dropping it would put an unreportable verdict back in a closed enum,
        which is the defect this release removes."""
        import yaml
        from malleus.ontology import OntologyError, OntologyRegistry
        from malleus.ocr.verify import ONTOLOGY, terminal_verdicts
        from malleus.ontology import bundled_ontology_path
        schema = yaml.safe_load(bundled_ontology_path(*ONTOLOGY).read_text())
        note = {"description": "A reviewer states the unit is illegible in part."}
        schema["enums"]["ReviewVerdict"]["permissible_values"]["PARTIAL"] = dict(note)
        schema["enums"]["AccountedUnitOutcome"]["permissible_values"]["PARTIAL"] = dict(note)
        written = tmp_path / "ocr.yaml"
        written.write_text(yaml.safe_dump(schema, sort_keys=False))
        with pytest.raises(OntologyError) as raised:
            terminal_verdicts(OntologyRegistry(written))
        assert "PARTIAL" in str(raised.value)

    def test_a_rank_for_a_verdict_the_schema_does_not_declare_refuses(self, tmp_path):
        """The other direction, and the one that matters historically: a rule
        for a value nothing can record is how ABSENT spent a release
        unreachable. Removing EXCLUDED from ReviewVerdict must be refused,
        not quietly skipped."""
        import yaml
        from malleus.ontology import OntologyError, OntologyRegistry
        from malleus.ocr.verify import ONTOLOGY, terminal_verdicts
        from malleus.ontology import bundled_ontology_path
        schema = yaml.safe_load(bundled_ontology_path(*ONTOLOGY).read_text())
        schema["enums"]["ReviewVerdict"]["permissible_values"].pop("EXCLUDED")
        written = tmp_path / "ocr.yaml"
        written.write_text(yaml.safe_dump(schema, sort_keys=False))
        with pytest.raises(OntologyError) as raised:
            terminal_verdicts(OntologyRegistry(written))
        assert "EXCLUDED" in str(raised.value)

    def test_moving_a_verdict_between_dispositions_keeps_it_ranked(self, tmp_path):
        """Which disposition an outcome carries and whether it speaks for a
        unit are two questions. A replacement answering the first differently
        must not silently answer the second."""
        from malleus.ocr.verify import terminal_verdicts
        replacement = _registry_moving(tmp_path, "ABSENT", "NotCheckedUnitOutcome")
        assert "ABSENT" in terminal_verdicts(replacement)


class TestTheAccount:
    """Integrity and coverage are two answers. A bundle that read nothing used
    to take the same word as one that read everything, which is what made
    "passed" mean "passed what"."""

    def test_a_page_read_and_found_blank_is_accounted_for(self):
        """The objection that produced this design. Blank is an answer, not a
        failure, and mandate B2 forbids converting it into one."""
        account = verify_bundle(_bundle()).account
        outcomes = {u.unit: u.outcome for u in account.units}
        assert outcomes == {"page:1": "READ", "page:2": "VERIFIED_BLANK"}
        assert all(u.accounted for u in account.units)
        assert account.complete

    def test_a_bundle_that_read_nothing_is_sound_and_not_complete(self):
        from malleus.ocr.bundle import Bundle, SourceRepresentation
        bundle = Bundle(id="b:2", source_class=_class(),
                        sources=(SourceRepresentation("src:1", D(1), 2048, "application/pdf", "a.pdf"),),
                        data_handling_policy_id="p", hostile_content_policy_id="p")
        result = verify_bundle(bundle)
        assert result.conforms, "the paperwork holds together and that is all it means"
        assert not result.account.complete
        assert result.account.unaccounted == ("page:1", "page:2")

    def test_a_registration_is_never_complete_and_never_counts(self):
        from malleus.ocr.bundle import Bundle, SourceRepresentation
        bundle = Bundle(id="b:3", source_class=_class(), kind="REGISTRATION",
                        sources=(SourceRepresentation("src:1", D(1), 2048, "application/pdf", "a.pdf"),),
                        data_handling_policy_id="p", hostile_content_policy_id="p")
        result = verify_bundle(bundle)
        assert result.conforms and not result.account.complete
        assert result.account.kind == "REGISTRATION"

    @pytest.mark.parametrize("unit,expected", [
        ("page:2", "NOT_OBSERVED"),
    ])
    def test_a_unit_never_fetched_is_distinct_from_one_never_rendered(self, unit, expected):
        """Three ways to go unaccounted, kept apart: never fetched, held and
        never rendered, rendered and never looked at. Different fixes."""
        from malleus.ocr.bundle import Raster
        not_observed = _bundle(observed_units=("page:1",))
        assert {u.unit: u.outcome for u in verify_bundle(not_observed).account.units}[unit] == expected
        not_rendered = _bundle(rasters=(Raster("ras:1", "src:1", "page:1", D(2), "r"),))
        assert {u.unit: u.outcome for u in verify_bundle(not_rendered).account.units}["page:2"] == "NOT_RENDERED"

    def test_a_failed_attempt_is_not_a_blank_page(self):
        from malleus.ocr.bundle import OCRAttempt
        bundle = _bundle(
            attempts=(OCRAttempt("att:1", "reg:1", D(3), {"model": "e@1"}, "COMPLETED", D(4)),
                      OCRAttempt("att:2", "reg:2", D(9), {"model": "e@1"}, "FAILED")),
            hypotheses=(Hypothesis("hyp:1", "reg:1", D(5), attempt_id="att:1"),
                        Hypothesis("hyp:2", "reg:1", D(6), correction_id="cor:1")),
            corrections=(ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(6)),),
        )
        outcomes = {u.unit: u.outcome for u in verify_bundle(bundle).account.units}
        assert outcomes["page:2"] == "FAILED", "a failed call must never read as a blank page"

    def test_a_metric_we_cannot_compute_does_not_read_as_a_pass(self):
        """Fail closed. An unmeasured metric reported as met is worse than a
        missing one, because it certifies something nobody measured."""
        bundle = _bundle(source_class=_class(metric_families={
            "coverage": {"denominator": "declared_units", "threshold": 1.0},
            "semantics": {"denominator": "required_fields", "threshold": 0.9},
        }))
        account = verify_bundle(bundle).account
        verdicts = {m.family: m.verdict for m in account.metrics}
        assert verdicts == {"coverage": "MET", "semantics": "UNMEASURED"}
        assert not account.complete, "an unmeasured declaration blocks completeness"

    def test_the_threshold_is_the_adopters_own(self):
        """Frozen before ingest, so it cannot be lowered after seeing the scan."""
        lenient = _bundle(observed_units=("page:1",), source_class=_class(
            metric_families={"coverage": {"denominator": "declared_units", "threshold": 0.5}}))
        assert verify_bundle(lenient).account.complete
        strict = _bundle(observed_units=("page:1",), source_class=_class(
            metric_families={"coverage": {"denominator": "declared_units", "threshold": 1.0}}))
        assert not verify_bundle(strict).account.complete


def test_a_source_class_declaring_no_measure_is_never_complete():
    """With nothing declared there is no bar, and an empty all() would
    otherwise certify a bundle nobody measured."""
    account = verify_bundle(_bundle(source_class=_class(metric_families={}))).account
    assert not account.metrics and not account.complete


class TestEveryReferenceIsWalked:
    """Lineage was traced outward from readings, so a plane nothing referenced
    was never examined. A region over a missing raster and a raster over a
    missing source both took a purity seal. The bundle is the unit of
    verification, not the reading."""

    def test_a_region_over_a_missing_raster_is_refused_even_when_unread(self):
        from malleus.ocr.bundle import Region
        bundle = _bundle(regions=(*_bundle().regions, Region("reg:orphan", "ras:absent", {"t": "F"})))
        result = verify_bundle(bundle)
        assert "OCR-D003" in result.codes()
        assert any("reg:orphan" in d.subject for d in result.diagnostics)

    def test_a_raster_over_a_missing_source_is_refused_even_when_unread(self):
        from malleus.ocr.bundle import Raster
        bundle = _bundle(rasters=(*_bundle().rasters,
                                  Raster("ras:orphan", "src:absent", "page:1", D(9), "r")))
        assert "OCR-D003" in verify_bundle(bundle).codes()

    def test_an_attempt_over_a_missing_region_is_refused(self):
        from malleus.ocr.bundle import OCRAttempt
        bundle = _bundle(attempts=(*_bundle().attempts,
                                   OCRAttempt("att:9", "reg:absent", D(3), {"m": "e"}, "COMPLETED", D(4))))
        assert "OCR-D003" in verify_bundle(bundle).codes()

    def test_a_selection_over_a_missing_region_is_refused(self):
        from malleus.ocr.bundle import Selection
        bundle = _bundle(selections=(Selection("sel:1", "reg:absent", ("hyp:1", "hyp:2"),
                                               "hyp:2", "r", True),))
        assert "OCR-D003" in verify_bundle(bundle).codes()

    def test_a_correction_chain_naming_a_missing_predecessor_is_refused(self):
        bundle = _bundle(corrections=(
            ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(6),
                             predecessor_id="cor:absent"),
            ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "VERIFIED_BLANK"),
        ))
        assert "OCR-D003" in verify_bundle(bundle).codes()

    def test_a_rendering_of_a_unit_the_bundle_does_not_observe_is_refused(self):
        """A typo in a unit name would otherwise report the page as never
        rendered, which reads as an honest gap rather than a mistake."""
        from malleus.ocr.bundle import Raster
        bundle = _bundle(rasters=(Raster("ras:1", "src:1", "page:7", D(2), "r"),
                                  Raster("ras:2", "src:1", "page:2", D(8), "r")))
        assert "OCR-D014" in verify_bundle(bundle).codes()

    def test_the_complete_example_is_still_clean(self):
        """The wider walk must not condemn a sound bundle."""
        assert verify_bundle(_bundle()).conforms


class TestAStateAgreesWithTheDetailItRequires:
    """The schema can say a slot is required. It cannot say "required when the
    status is UNAVAILABLE", and LinkML's exactly_one_of cannot express the
    implication without also accepting the case it exists to refuse. The slot
    description said it anyway and nothing performed it."""

    def test_an_unavailable_attempt_must_say_why(self):
        bundle = _bundle(attempts=(
            OCRAttempt("att:1", "reg:1", D(3), {"m": "e"}, "COMPLETED", D(4)),
            OCRAttempt("att:2", "reg:2", D(9), {"m": "e"}, "UNAVAILABLE"),
        ))
        assert "OCR-D015" in verify_bundle(bundle).codes()

    def test_an_attempt_that_was_made_carries_no_unavailable_reason(self):
        """The mirror. A reason on a completed call means one of the two is
        wrong, and neither may be assumed to be the mistake."""
        bundle = _bundle(attempts=(
            OCRAttempt("att:1", "reg:1", D(3), {"m": "e"}, "COMPLETED", D(4),
                       unavailable_reason="provider quota"),
            OCRAttempt("att:2", "reg:2", D(9), {"m": "e"}, "COMPLETED", D(1)),
        ))
        assert "OCR-D015" in verify_bundle(bundle).codes()

    def test_a_correction_that_says_corrected_must_carry_the_correction(self):
        bundle = _bundle(corrections=(
            ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED"),
            ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "VERIFIED_BLANK"),
        ))
        assert "OCR-D015" in verify_bundle(bundle).codes()

    def test_the_corrected_text_must_be_the_reading_it_produced(self):
        """The stronger of the two available discharges. Presence alone would
        let the correction record and the hypothesis plane disagree about what
        the corrected text is, with nothing preferring either."""
        bundle = _bundle(corrections=(
            ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(3)),
            ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "VERIFIED_BLANK"),
        ))
        result = verify_bundle(bundle)
        assert "OCR-D015" in result.codes()
        assert "disagrees with the reading it produced" in str(result.diagnostics[0])

    def test_a_blank_page_carries_no_corrected_text(self):
        """B2 keeps the verdicts distinct. A page verified blank that also
        carries corrected text is claiming both at once."""
        bundle = _bundle(corrections=(
            ReviewCorrection("cor:1", "hyp:1", "reviewer:kim", "CORRECTED", D(6)),
            ReviewCorrection("cor:2", "hyp:4", "reviewer:kim", "VERIFIED_BLANK", D(2)),
        ))
        assert "OCR-D015" in verify_bundle(bundle).codes()
