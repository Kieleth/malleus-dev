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
