"""Conformance for the OCR evidence-integrity profile (OCR-D001, AUDIT_ONLY).

Each negative case names the decision it defends. A check with no case here is
a claim the profile cannot support.
"""

from __future__ import annotations

import dataclasses

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

D = lambda n: "sha256:" + str(n) * 64


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
