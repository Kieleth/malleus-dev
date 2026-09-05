"""Public contract for the optional document-assertion population adapter."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from importlib import import_module
from inspect import signature
import json
from pathlib import Path
import tomllib

import pytest


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "inspection_note_capture_v1"
)


def _api():
    return import_module("malleus.compiler")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _load(name: str) -> object:
    return json.loads((EXAMPLES / name).read_bytes())


def _inputs() -> tuple[dict[str, object], ...]:
    reading = _load("reading.json")
    capture = _load("document-capture.json")
    plan = _load("document-plan.json")
    census = _load("document-census.json")
    assert isinstance(reading, dict)
    assert isinstance(capture, dict)
    assert isinstance(plan, dict)
    assert isinstance(census, dict)
    return reading, capture, plan, census


def _adapt(
    *,
    reading: dict[str, object] | None = None,
    capture: dict[str, object] | None = None,
):
    api = _api()
    fixture_reading, fixture_capture, plan, _ = _inputs()
    reading = fixture_reading if reading is None else reading
    capture = fixture_capture if capture is None else capture
    return api.adapt_document_assertions(
        reading_bytes=_canonical(reading),
        capture_bytes=_canonical(capture),
        capture_id="capture:inspection-note",
        plan_id=str(plan["plan_id"]),
        contract_identity=str(plan["contract_identity"]),
        records=plan["records"],
        supersessions=plan["supersessions"],
    )


def test_document_adapter_is_public_and_emits_the_exact_neutral_plan() -> None:
    api = _api()
    required = {
        "DOCUMENT_ASSERTION_ADAPTER",
        "DOCUMENT_CAPTURE_GRAMMAR",
        "DocumentAssertionCompilation",
        "DocumentAssertionRefusal",
        "DocumentAssertionRefusalReason",
        "adapt_document_assertions",
    }
    assert required <= set(api.__all__)
    package = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert (
        "/src/malleus/_contract_pipeline/document.py"
        in package["tool"]["hatch"]["build"]["include"]
    )

    reading, capture, expected_plan, expected_census = _inputs()
    reading_bytes = (EXAMPLES / "reading.json").read_bytes()
    capture_bytes = (EXAMPLES / "document-capture.json").read_bytes()
    assert reading_bytes == _canonical(reading)
    assert capture_bytes == _canonical(capture)
    result = api.adapt_document_assertions(
        reading_bytes=reading_bytes,
        capture_bytes=capture_bytes,
        capture_id="capture:inspection-note",
        plan_id=str(expected_plan["plan_id"]),
        contract_identity=str(expected_plan["contract_identity"]),
        records=expected_plan["records"],
        supersessions=expected_plan["supersessions"],
    )

    assert isinstance(result, api.DocumentAssertionCompilation)
    assert result.capture_id == "capture:inspection-note"
    assert result.capture_bytes == capture_bytes
    assert result.capture_identity == _digest(capture_bytes)
    assert result.reading_identity == _digest(_canonical(reading))
    assert result.canonical_plan_bytes == _canonical(expected_plan)
    assert result.canonical_census_bytes == _canonical(expected_census)
    assert (
        json.loads(result.canonical_plan_bytes)["records"] == expected_plan["records"]
    )
    assert not any(
        record["type"].endswith("Assertion")
        for records in expected_plan["records"].values()
        for record in records
    )


def test_document_adapter_derives_capture_batch_order_time() -> None:
    api = _api()
    assert "valid_time" not in signature(api.adapt_document_assertions).parameters
    reading, capture, plan, _ = _inputs()

    result = api.adapt_document_assertions(
        reading_bytes=_canonical(reading),
        capture_bytes=_canonical(capture),
        capture_id="capture:inspection-note",
        plan_id=str(plan["plan_id"]),
        contract_identity=str(plan["contract_identity"]),
        records=plan["records"],
        supersessions=plan["supersessions"],
    )

    assert json.loads(result.canonical_plan_bytes)["valid_time"] == {
        "kind": "ORDER_ONLY",
        "value": "capture:inspection-note",
    }


@pytest.mark.parametrize(
    ("case", "reason"),
    (
        ("reading-mismatch", "READING_MISMATCH"),
        ("unknown-block", "UNKNOWN_BLOCK"),
        ("not-verbatim", "NOT_VERBATIM"),
        ("unknown-modality", "UNKNOWN_MODALITY"),
        ("gap-required", "GAP_REQUIRED"),
        ("unknown-target", "UNKNOWN_FORMALIZATION_TARGET"),
        ("unknown-gap-kind", "UNKNOWN_GAP_KIND"),
    ),
)
def test_document_adapter_refuses_each_semantic_boundary(
    case: str, reason: str
) -> None:
    api = _api()
    reading, capture, _, _ = _inputs()
    if case == "reading-mismatch":
        capture["reading_sha256"] = "sha256:" + "0" * 64
    elif case == "unknown-block":
        capture["nothing_assertable"].append("page:9:block:999")
    elif case == "not-verbatim":
        capture["assertions"][0]["statement"] = "Pump P-7 was fine."
    elif case == "unknown-modality":
        capture["assertions"][0]["modality"] = "VIBES"
    elif case == "gap-required":
        capture["assertions"][1]["gaps"] = []
    elif case == "unknown-target":
        capture["assertions"][0]["formalized_by"].append(
            {"record_id": "asset:P-7", "path": ["properties", "mass"]}
        )
    elif case == "unknown-gap-kind":
        capture["assertions"][1]["gaps"][0]["kind"] = "SHRUG"

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt(reading=reading, capture=capture)

    assert refusal.value.reason is getattr(api.DocumentAssertionRefusalReason, reason)


def test_document_adapter_reports_every_locator_defect_in_one_refusal() -> None:
    """Paraphrases and phantom blocks are one refusal, not one return each.

    A fresh producer paraphrased all seven of its statements and named a block
    the reading does not carry. The adapter reported one defect per run, so a
    capture that was wrong throughout cost a structural return per statement.
    The reason stays the first defect's under the sort; every other defect is
    named inline, with the rule that closes them.
    """

    api = _api()
    reading, capture, _, _ = _inputs()
    capture["assertions"][0]["statement"] = "Pump P-7 was inspected."
    capture["assertions"][1]["statement"] = (
        "Vibration was approximately 4.3 mm/s on 2026-03-01."
    )
    capture["assertions"][2]["block"] = "page:9:block:999"
    capture["nothing_assertable"].append("page:3:block:007")

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt(reading=reading, capture=capture)

    assert refusal.value.reason is api.DocumentAssertionRefusalReason.NOT_VERBATIM
    assert refusal.value.detail == (
        "document capture locators are not accepted: "
        "assertion asr:001 is not verbatim in page:1:block:001 [NOT_VERBATIM]; "
        "assertion asr:002 is not verbatim in page:1:block:001 [NOT_VERBATIM]; "
        "assertion asr:003 names unknown block page:9:block:999 "
        "[UNKNOWN_BLOCK]; "
        "nothing_assertable names unknown block page:3:block:007 "
        "[UNKNOWN_BLOCK]; "
        "every block ID comes from the reading's inventory and every statement "
        "is copied from its block's own bytes, matching after whitespace "
        "collapse"
    )


def test_document_adapter_reports_locator_defects_before_other_semantics() -> None:
    """A defect later in the capture never hides a non-verbatim statement."""

    api = _api()
    reading, capture, _, _ = _inputs()
    capture["assertions"][0]["modality"] = "VIBES"
    capture["assertions"][2]["statement"] = "The technician suspects wear."

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt(reading=reading, capture=capture)

    assert refusal.value.reason is api.DocumentAssertionRefusalReason.NOT_VERBATIM
    assert "assertion asr:003 is not verbatim in page:1:block:002" in (
        refusal.value.detail
    )


def test_document_adapter_accepts_verbatim_text_after_whitespace_normalisation() -> (
    None
):
    reading, capture, _, _ = _inputs()
    capture["assertions"][0]["statement"] = "Pump  P-7 was\ninspected on 2026-03-02."

    result = _adapt(reading=reading, capture=capture)

    assert json.loads(result.canonical_plan_bytes)["derivations"][0]["locator"] == (
        "asr:001"
    )


@pytest.mark.parametrize(
    ("case", "reason"),
    (
        ("capture-field", "FIELDS_NOT_CLOSED"),
        ("capture-grammar", "UNSUPPORTED_GRAMMAR"),
        ("malformed-reading", "MALFORMED_READING"),
        ("malformed-capture", "MALFORMED_CAPTURE"),
    ),
)
def test_document_adapter_refuses_malformed_or_open_inputs(
    case: str, reason: str
) -> None:
    api = _api()
    reading, capture, plan, _ = _inputs()
    reading_bytes = _canonical(reading)
    capture_bytes = _canonical(capture)
    if case == "capture-field":
        capture["extra"] = True
        capture_bytes = _canonical(capture)
    elif case == "capture-grammar":
        capture["schema"] = "another-capture/v1"
        capture_bytes = _canonical(capture)
    elif case == "malformed-reading":
        reading_bytes = b"{"
    elif case == "malformed-capture":
        capture_bytes = b"[]"

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        api.adapt_document_assertions(
            reading_bytes=reading_bytes,
            capture_bytes=capture_bytes,
            capture_id="capture:inspection-note",
            plan_id=str(plan["plan_id"]),
            contract_identity=str(plan["contract_identity"]),
            records=plan["records"],
            supersessions=plan["supersessions"],
        )

    assert refusal.value.reason is getattr(api.DocumentAssertionRefusalReason, reason)


def test_document_census_keeps_review_and_formalisation_separate() -> None:
    reading, capture, _, _ = _inputs()
    capture["nothing_assertable"] = []

    result = _adapt(reading=reading, capture=capture)
    census = json.loads(result.canonical_census_bytes)

    assert census["blocks"] == {
        "page:1:block:001": "REVIEWED",
        "page:1:block:002": "REVIEWED",
        "page:1:block:003": "UNTOUCHED",
    }
    assert census["assertions"] == {
        "FULLY_FORMALIZED": 1,
        "PARTLY_FORMALIZED": 0,
        "UNFORMALIZED": 2,
    }


def test_document_adapter_can_emit_a_gaps_only_plan() -> None:
    reading, capture, plan, _ = _inputs()
    capture["assertions"] = [deepcopy(capture["assertions"][1])]
    capture["nothing_assertable"] = [
        "page:1:block:002",
        "page:1:block:003",
    ]

    api = _api()
    result = api.adapt_document_assertions(
        reading_bytes=_canonical(reading),
        capture_bytes=_canonical(capture),
        capture_id="capture:inspection-note:gaps-only",
        plan_id="plan:inspection-note:gaps-only",
        contract_identity=str(plan["contract_identity"]),
        records={"entities": [], "relations": []},
        supersessions=[],
    )
    emitted = json.loads(result.canonical_plan_bytes)

    assert emitted["records"] == {"entities": [], "relations": []}
    assert emitted["derivations"] == []
    assert emitted["gaps"] == [
        {
            "kind": "INTERVAL_NOT_EXPRESSIBLE",
            "locator": "asr:002",
            "source_id": "source:inspection-note",
            "statement": (
                "VibrationReading.vibration_mm_s is a single float; "
                "the source states a range"
            ),
        }
    ]


def _located(
    *,
    digest: str | None = None,
    locator: str = "asr:001",
) -> tuple[dict[str, object], dict[str, object]]:
    """The fixture capture and records with one located, digested claim."""

    _, capture, plan, _ = _inputs()
    records = deepcopy(plan["records"])
    statement = str(capture["assertions"][0]["statement"])
    properties = records["entities"][0]["properties"]
    properties["assertion_locator"] = locator
    properties["statement_sha256"] = (
        _digest(statement.encode("utf-8")) if digest is None else digest
    )
    return capture, records


def _adapt_records(
    capture: dict[str, object],
    records: dict[str, object],
    reading: dict[str, object] | None = None,
):
    api = _api()
    fixture_reading, _, plan, _ = _inputs()
    reading = fixture_reading if reading is None else reading
    return api.adapt_document_assertions(
        reading_bytes=_canonical(reading),
        capture_bytes=_canonical(capture),
        capture_id="capture:inspection-note",
        plan_id=str(plan["plan_id"]),
        contract_identity=str(plan["contract_identity"]),
        records=records,
        supersessions=plan["supersessions"],
    )


def test_document_adapter_recomputes_the_located_statement_digest() -> None:
    """A correct digest is the one the adapter computes from the statement."""

    capture, records = _located()

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_refuses_a_statement_digest_the_assertion_denies() -> None:
    """Run-04's 104 located claims all carried a correct digest; nothing checked one.

    The digest is the only field binding a claim record to the words behind
    it, and a producer that writes the digest of some other text passes
    admission untouched. The adapter now recomputes it from the located
    assertion's own statement bytes.
    """

    api = _api()
    wrong = "sha256:" + "0" * 64
    capture, records = _located(digest=wrong)
    statement = str(capture["assertions"][0]["statement"])

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is api.DocumentAssertionRefusalReason.DIGEST_MISMATCH
    assert refusal.value.detail == (
        "document capture derivations are not accepted: "
        f"record asset:P-7 names assertion asr:001 with statement digest "
        f"{wrong}, and that assertion's statement digests to "
        f"{_digest(statement.encode('utf-8'))} [DIGEST_MISMATCH]; "
        "a record's assertion_locator names an assertion of this capture, a "
        "statement_sha256 comes with the locator that checks it and is the "
        "SHA-256 of that assertion's statement bytes, "
        "a slot the contract declares evaluative is formalized by at "
        "least one assertion whose modality is not HYPOTHESISED, a name "
        "of a record's subject, its name or one of its tags, occurs as a "
        "word in the statement of an assertion that formalizes that subject, "
        "and a "
        "record's assertion_modality is the modality of an assertion that "
        "formalizes it"
    )


def test_document_adapter_refuses_a_locator_that_names_no_assertion() -> None:
    """A dangling locator is a different defect and carries its own reason."""

    api = _api()
    capture, records = _located(locator="asr:404")

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.UNKNOWN_ASSERTION_LOCATOR
    )
    assert (
        "record asset:P-7 names unknown assertion asr:404 "
        "[UNKNOWN_ASSERTION_LOCATOR]"
    ) in refusal.value.detail


def test_document_adapter_reports_every_digest_defect_in_one_refusal() -> None:
    """Both derivation defects arrive sorted, in one refusal, not one per run."""

    api = _api()
    wrong = "sha256:" + "1" * 64
    capture, records = _located(digest=wrong)
    records["entities"][1]["properties"]["assertion_locator"] = "asr:404"
    records["entities"][1]["properties"]["statement_sha256"] = wrong

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is api.DocumentAssertionRefusalReason.DIGEST_MISMATCH
    assert "record asset:P-7 names assertion asr:001" in refusal.value.detail
    assert (
        "record inspection:P-7:2026-03-02 names unknown assertion asr:404"
        in refusal.value.detail
    )
    assert refusal.value.detail.index("[DIGEST_MISMATCH]") < (
        refusal.value.detail.index("[UNKNOWN_ASSERTION_LOCATOR]")
    )


def test_document_adapter_leaves_an_undigested_locator_alone() -> None:
    """A locator with no digest still has to resolve; nothing else is claimed."""

    capture, records = _located()
    del records["entities"][0]["properties"]["statement_sha256"]

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_refuses_a_digest_no_locator_can_check() -> None:
    """Core-12 left a digest nobody can check passing admission.

    `statement_sha256` binds a record to the words behind it and the adapter
    recomputes it from the located assertion. With no `assertion_locator`
    there is no assertion to recompute from, so the digest asserts something
    the capture cannot deny: it is not a weaker binding, it is none.
    """

    api = _api()
    capture, records = _located()
    del records["entities"][0]["properties"]["assertion_locator"]

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.DIGEST_NOT_LOCATED
    )
    assert (
        "record asset:P-7 carries a statement digest and no assertion_locator "
        "[DIGEST_NOT_LOCATED]"
    ) in refusal.value.detail


def test_document_adapter_leaves_a_record_with_neither_field_alone() -> None:
    """A record that claims no assertion claims no digest either; nothing to check."""

    _, capture, plan, _ = _inputs()

    result = _adapt_records(capture, deepcopy(plan["records"]))

    assert json.loads(result.canonical_plan_bytes)["records"] == plan["records"]


def test_derivation_census_reads_only_what_it_is_handed() -> None:
    """The census counts derivations, blocks and record families; it never
    looked a record up by id, and the argument said it might."""

    document = import_module("malleus._contract_pipeline.document")

    assert tuple(signature(document._derivation_census).parameters) == (
        "derivations",
        "block_by_assertion",
        "record_data",
    )


def _research_view():
    """The compiled packs, whose `Evaluative` mixin declares the slot list."""

    from importlib.resources import files

    from malleus.ontology import bundled_ontology_path

    linkml_types = Path(
        str(
            files("linkml_runtime").joinpath(
                "linkml_model", "model", "schema", "types.yaml"
            )
        )
    )
    sources = {
        "linkml:types": linkml_types.read_bytes(),
        "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
        "metrology": bundled_ontology_path("packs", "metrology.yaml").read_bytes(),
        "chronology": bundled_ontology_path("packs", "chronology.yaml").read_bytes(),
        "research": bundled_ontology_path("packs", "research.yaml").read_bytes(),
    }
    return _api().compile_linkml_contract(
        root_locator="research", sources=sources
    ).view


def _disposed(
    *,
    modality: str = "HYPOTHESISED",
    formalized: bool = True,
) -> tuple[dict[str, object], dict[str, object]]:
    """The fixture with one claim disposition and the assertion behind it."""

    _, capture, plan, _ = _inputs()
    records = deepcopy(plan["records"])
    records["entities"][1]["properties"]["hypothesis_disposition"] = "NOT_SUPPORTED"
    capture["assertions"][2]["modality"] = modality
    if formalized:
        capture["assertions"][2]["formalized_by"] = [
            {
                "path": ["properties", "hypothesis_disposition"],
                "record_id": "inspection:P-7:2026-03-02",
            }
        ]
    return capture, records


def _adapt_with_contract(capture: dict[str, object], records: dict[str, object]):
    api = _api()
    reading, _, plan, _ = _inputs()
    return api.adapt_document_assertions(
        reading_bytes=_canonical(reading),
        capture_bytes=_canonical(capture),
        capture_id="capture:inspection-note",
        plan_id=str(plan["plan_id"]),
        contract_identity=str(plan["contract_identity"]),
        contract_view=_research_view(),
        records=records,
        supersessions=plan["supersessions"],
    )


def test_document_adapter_refuses_a_disposition_no_assertion_evaluates() -> None:
    """All five of run-04's dispositions derive from HYPOTHESISED assertions.

    The value was right and the evidence pointer was wrong: each disposition
    hung on the sentence that raises the hypothesis, never on the sentence
    that disposes of it. A slot the contract declares evaluative must be
    formalized by at least one assertion that evaluates.
    """

    api = _api()
    capture, records = _disposed()

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_with_contract(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.EVALUATIVE_SLOT_NOT_EVALUATED
    )
    assert refusal.value.detail == (
        "document capture derivations are not accepted: "
        "record inspection:P-7:2026-03-02 evaluative slot "
        "hypothesis_disposition is formalized by asr:003 HYPOTHESISED "
        "[EVALUATIVE_SLOT_NOT_EVALUATED]; "
        "a record's assertion_locator names an assertion of this capture, a "
        "statement_sha256 comes with the locator that checks it and is the "
        "SHA-256 of that assertion's statement bytes, "
        "a slot the contract declares evaluative is formalized by at "
        "least one assertion whose modality is not HYPOTHESISED, a name "
        "of a record's subject, its name or one of its tags, occurs as a "
        "word in the statement of an assertion that formalizes that subject, "
        "and a "
        "record's assertion_modality is the modality of an assertion that "
        "formalizes it"
    )


def test_document_adapter_accepts_a_disposition_an_evaluating_assertion_carries() -> (
    None
):
    """The sentence that declines the hypothesis is NEGATED, and it evaluates."""

    capture, records = _disposed(modality="NEGATED")

    result = _adapt_with_contract(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_refuses_a_disposition_nothing_formalizes() -> None:
    """No formalizing assertion at all fails the same rule and says so."""

    api = _api()
    capture, records = _disposed(formalized=False)

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_with_contract(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.EVALUATIVE_SLOT_NOT_EVALUATED
    )
    assert (
        "record inspection:P-7:2026-03-02 evaluative slot "
        "hypothesis_disposition is formalized by no assertion"
    ) in refusal.value.detail


def test_document_adapter_reads_the_evaluative_declaration_from_the_contract() -> None:
    """With no compiled contract the adapter knows no evaluative slot."""

    capture, records = _disposed()

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_keeps_the_six_capture_modalities() -> None:
    """The check reads the existing enum; no modality is added for it."""

    document = import_module("malleus._contract_pipeline.document")

    assert document._MODALITIES == {
        "CALCULATED",
        "CONTESTED",
        "HYPOTHESISED",
        "MEASURED",
        "NEGATED",
        "STATED",
    }


def _subjected(
    *,
    subject: str = "asset:P-7",
    name: str | None = None,
    tags: list[str] | None = None,
    locator: str = "asr:001",
) -> tuple[dict[str, object], dict[str, object]]:
    """The fixture with one record naming its subject, and the assertion for it.

    ``asr:001`` reads "Pump P-7 was inspected on 2026-03-02." and names the
    asset; ``asr:003`` reads "The technician suspects bearing wear." and names
    nothing the records carry.
    """

    _, capture, plan, _ = _inputs()
    records = deepcopy(plan["records"])
    records["entities"][1]["properties"]["subject"] = subject
    if name is not None:
        records["entities"][0]["properties"]["name"] = name
    if tags is not None:
        records["entities"][0]["properties"]["tags"] = tags
    index = {"asr:001": 0, "asr:002": 1, "asr:003": 2}[locator]
    capture["assertions"][index]["formalized_by"] = list(
        capture["assertions"][index]["formalized_by"]
    ) + [
        {
            "path": ["properties", "subject"],
            "record_id": "inspection:P-7:2026-03-02",
        }
    ]
    return capture, records


def test_document_adapter_accepts_a_subject_the_formalizing_statement_names() -> None:
    """Run-08 made 131 observations and attached none of them to a feature.

    The pack now carries the attachment, and the adapter accepts it when the
    sentence that formalizes it names the subject: the asset is called P-7 and
    asr:001 reads "Pump P-7 was inspected on 2026-03-02."
    """

    capture, records = _subjected()

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_refuses_a_subject_the_statement_does_not_name() -> None:
    """23 of run-08's observations put the feature inside quantity_kind text.

    A subject hung on a sentence that never mentions it is the same defect one
    layer up: the pointer exists and what it points at does not say so.
    """

    api = _api()
    capture, records = _subjected(locator="asr:003")

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.SUBJECT_NOT_NAMED
    )
    assert refusal.value.detail == (
        "document capture derivations are not accepted: "
        "record inspection:P-7:2026-03-02 names subject asset:P-7, whose name "
        "P-7 does not occur as a word in the statement of asr:003 "
        "[SUBJECT_NOT_NAMED]; "
        "a record's assertion_locator names an assertion of this capture, a "
        "statement_sha256 comes with the locator that checks it and is the "
        "SHA-256 of that assertion's statement bytes, "
        "a slot the contract declares evaluative is formalized by at "
        "least one assertion whose modality is not HYPOTHESISED, a name "
        "of a record's subject, its name or one of its tags, occurs as a "
        "word in the statement of an assertion that formalizes that subject, "
        "and a "
        "record's assertion_modality is the modality of an assertion that "
        "formalizes it"
    )


def test_document_adapter_refuses_a_subject_no_assertion_formalizes() -> None:
    """A subject nothing formalizes fails the same rule and says so."""

    api = _api()
    _, capture, plan, _ = _inputs()
    records = deepcopy(plan["records"])
    records["entities"][1]["properties"]["subject"] = "asset:P-7"

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.SUBJECT_NOT_NAMED
    )
    assert (
        "record inspection:P-7:2026-03-02 names subject asset:P-7, whose name "
        "P-7 does not occur as a word in the statement of no assertion"
    ) in refusal.value.detail


def test_document_adapter_matches_a_subject_name_past_spacing_and_case() -> None:
    """Both sides drop whitespace and case-fold; neither side is rewritten."""

    capture, records = _subjected(name="pump\n  p-7")

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records
    assert records["entities"][0]["properties"]["name"] == "pump\n  p-7"


def _broken() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    """The reading's text layer prints a space through the subject's name.

    Six of run-10's 35 refused subjects were this: the entity is named "CO2"
    and the page prints "CO 2". Here the asset is named "P-7" and the page
    prints "P- 7", so the statement stays verbatim in the block it came from.
    """

    reading, capture, plan, _ = _inputs()
    block = reading["pages"][0]["blocks"][0]
    block["text"] = str(block["text"]).replace("P-7", "P- 7")
    capture["assertions"][0]["statement"] = "Pump P- 7 was inspected on 2026-03-02."
    capture["reading_sha256"] = _digest(_canonical(reading))
    capture["assertions"][0]["formalized_by"] = list(
        capture["assertions"][0]["formalized_by"]
    ) + [
        {
            "path": ["properties", "subject"],
            "record_id": "inspection:P-7:2026-03-02",
        }
    ]
    records = deepcopy(plan["records"])
    records["entities"][1]["properties"]["subject"] = "asset:P-7"
    return reading, capture, records


def test_document_adapter_accepts_a_subject_one_of_its_tags_names() -> None:
    """Seven of run-10's 35 refused subjects were the source's short form.

    The entity is named "Mid-Atlantic Ridge" and the sentence writes "the
    MAR". The other forms the source uses for the same thing go in `tags`,
    which every Entity already carries, and the check accepts any of them.
    Here the asset is named "primary feed pump" and tagged "P-7", which is
    what asr:001 writes.
    """

    capture, records = _subjected(name="primary feed pump", tags=["P-7"])

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_accepts_a_subject_named_only_by_a_tag() -> None:
    """A subject with no `name` is named by a tag the statement writes."""

    capture, records = _subjected(tags=["P-7"])
    del records["entities"][0]["properties"]["name"]
    capture["assertions"][0]["formalized_by"] = [
        item
        for item in capture["assertions"][0]["formalized_by"]
        if item["record_id"] != "asset:P-7"
    ]

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_matches_a_name_the_text_layer_broke() -> None:
    """Eight of run-10's refusals were a name the page spells with a space.

    The comparison drops whitespace from both sides, so a name the text layer
    breaks still matches its own bytes. Neither side is rewritten.
    """

    reading, capture, records = _broken()

    result = _adapt_records(capture, records, reading=reading)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def _reworded(
    text: str,
    *,
    name: str | None = None,
    tags: list[str] | None = None,
) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    """The reading's second block reworded, and the record's subject on it.

    ``asr:003`` is the only assertion of ``page:1:block:002``, so replacing
    that block's text and that assertion's statement leaves every other
    locator of the fixture alone. With ``name`` absent the subject carries its
    tags and nothing else, and the derivation of its name goes with it.
    """

    reading, capture, plan, _ = _inputs()
    reading["pages"][0]["blocks"][1]["text"] = text
    capture["assertions"][2]["statement"] = text
    capture["reading_sha256"] = _digest(_canonical(reading))
    capture["assertions"][2]["formalized_by"] = [
        {
            "path": ["properties", "subject"],
            "record_id": "inspection:P-7:2026-03-02",
        }
    ]
    records = deepcopy(plan["records"])
    records["entities"][1]["properties"]["subject"] = "asset:P-7"
    properties = records["entities"][0]["properties"]
    if name is None:
        del properties["name"]
        capture["assertions"][0]["formalized_by"] = [
            item
            for item in capture["assertions"][0]["formalized_by"]
            if item["record_id"] != "asset:P-7"
        ]
    else:
        properties["name"] = name
    if tags is not None:
        properties["tags"] = tags
    return reading, capture, records


def test_document_adapter_refuses_a_form_found_inside_another_word() -> None:
    """Eight of run-12's fifteen projected subjects were a three-letter tag
    inside another word: RTI inside "vertical" and "portion", OCC inside
    "occur", MAR inside "mark", OBS inside "observations". A form names its
    entity where the sentence writes it as a word, and nowhere else."""

    api = _api()
    reading, capture, records = _reworded(
        "Vertical offset is under 4 mm.", tags=["RTI"]
    )

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records, reading=reading)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.SUBJECT_NOT_NAMED
    )
    assert (
        "record inspection:P-7:2026-03-02 names subject asset:P-7, whose name "
        "RTI does not occur as a word in the statement of asr:003"
    ) in refusal.value.detail


def test_document_adapter_matches_a_name_a_citation_number_is_glued_to() -> None:
    """The text layer prints a citation number against the word before it. A
    digit bounds a word, so "lithosphere13" still names the lithosphere."""

    reading, capture, records = _reworded(
        "The lithosphere13 is thin here.", name="lithosphere"
    )

    result = _adapt_records(capture, records, reading=reading)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_matches_a_form_the_text_layer_spaced_out() -> None:
    """Whitespace between a form's characters is still the same form: the page
    prints "R C 2" and the record is tagged "RC2"."""

    reading, capture, records = _reworded(
        "R C 2 was surveyed twice.", name="segment two", tags=["RC2"]
    )

    result = _adapt_records(capture, records, reading=reading)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_names_every_form_it_tried_for_a_subject() -> None:
    """The refusal says which forms were tried, in the order the record has
    them: its name first, then its tags."""

    api = _api()
    capture, records = _subjected(
        name="P-9", tags=["pump P-8", "P-6"], locator="asr:003"
    )

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.SUBJECT_NOT_NAMED
    )
    assert (
        "record inspection:P-7:2026-03-02 names subject asset:P-7, whose "
        "names P-9, pump P-8, P-6 do not occur as words in the statement of "
        "asr:003"
    ) in refusal.value.detail


def test_document_adapter_names_the_subject_in_one_collapsed_line() -> None:
    """The refusal is one aggregated line, so a name broken across two lines
    in the reading must reach the detail collapsed, not with the break in it."""

    api = _api()
    capture, records = _subjected(name="pump\n  p-9", locator="asr:003")

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert "\n" not in refusal.value.detail
    assert (
        "record inspection:P-7:2026-03-02 names subject asset:P-7, whose name "
        "pump p-9 does not occur as a word in the statement of asr:003"
    ) in refusal.value.detail


def test_document_adapter_refuses_a_subject_carrying_no_name() -> None:
    """A subject with no name is a subject no statement can be checked against."""

    api = _api()
    capture, records = _subjected()
    del records["entities"][0]["properties"]["name"]
    capture["assertions"][0]["formalized_by"] = [
        item
        for item in capture["assertions"][0]["formalized_by"]
        if item["record_id"] != "asset:P-7"
    ]

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.SUBJECT_NOT_NAMED
    )
    assert (
        "record inspection:P-7:2026-03-02 names subject asset:P-7, which "
        "carries no name"
    ) in refusal.value.detail


def test_document_adapter_leaves_a_subject_outside_this_change_set_alone() -> (
    None
):
    """The adapter is handed one change set and reads names from it alone.

    A subject that resolves in the base state has no name here to compare, and
    a subject that resolves nowhere is the plan compiler's DANGLING_SUBJECT,
    where the base state is in scope. The adapter claims neither.
    """

    capture, records = _subjected(subject="asset:P-9")

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def _moded(
    *,
    modality: str = "STATED",
    locator: str = "asr:001",
    formalized: bool = True,
    also: str | None = None,
) -> tuple[dict[str, object], dict[str, object]]:
    """The fixture with one record declaring its modality and the assertion for it.

    ``asr:001`` is STATED, ``asr:002`` is MEASURED and ``asr:003`` is
    HYPOTHESISED, so the three carry three different modalities to formalize
    the record's ``assertion_modality`` from.
    """

    _, capture, plan, _ = _inputs()
    records = deepcopy(plan["records"])
    records["entities"][1]["properties"]["assertion_modality"] = modality
    index = {"asr:001": 0, "asr:002": 1, "asr:003": 2}
    for name in ([locator] if formalized else []) + (
        [] if also is None else [also]
    ):
        position = index[name]
        capture["assertions"][position]["formalized_by"] = list(
            capture["assertions"][position]["formalized_by"]
        ) + [
            {
                "path": ["properties", "assertion_modality"],
                "record_id": "inspection:P-7:2026-03-02",
            }
        ]
    return capture, records


def test_document_adapter_accepts_a_modality_the_formalizing_assertion_carries() -> (
    None
):
    """A record's modality is its formalizing assertion's, so the two agree."""

    capture, records = _moded()

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_refuses_a_modality_no_formalizing_assertion_carries() -> (
    None
):
    """Twenty of run-09's 212 source-asserted records carried a modality the
    capture's own assertion denies: MEASURED in the capture, STATED on the
    record, twelve times. The record's modality was a second copy, set by the
    producer against the clause where the capture tagged the sentence. There
    is one source of truth for it, the assertion that formalizes it."""

    api = _api()
    capture, records = _moded(modality="MEASURED")

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.MODALITY_NOT_ASSERTED
    )
    assert refusal.value.detail == (
        "document capture derivations are not accepted: "
        "record inspection:P-7:2026-03-02 assertion_modality MEASURED is "
        "formalized by asr:001 STATED [MODALITY_NOT_ASSERTED]; "
        "a record's assertion_locator names an assertion of this capture, a "
        "statement_sha256 comes with the locator that checks it and is the "
        "SHA-256 of that assertion's statement bytes, "
        "a slot the contract declares evaluative is formalized by at "
        "least one assertion whose modality is not HYPOTHESISED, a name "
        "of a record's subject, its name or one of its tags, occurs as a "
        "word in the statement of an assertion that formalizes that subject, "
        "and a "
        "record's assertion_modality is the modality of an assertion that "
        "formalizes it"
    )


def test_document_adapter_accepts_a_modality_one_of_its_assertions_carries() -> None:
    """A record two assertions formalize takes the modality of either.

    A sentence carrying two modalities is captured as two assertions, and a
    record formalized from both is asserted under each of them.
    """

    capture, records = _moded(modality="MEASURED", locator="asr:002", also="asr:001")

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records


def test_document_adapter_refuses_a_modality_nothing_formalizes() -> None:
    """A modality no assertion formalizes fails the same rule and says so."""

    api = _api()
    capture, records = _moded(formalized=False)

    with pytest.raises(api.DocumentAssertionRefusal) as refusal:
        _adapt_records(capture, records)

    assert refusal.value.reason is (
        api.DocumentAssertionRefusalReason.MODALITY_NOT_ASSERTED
    )
    assert (
        "record inspection:P-7:2026-03-02 assertion_modality STATED is "
        "formalized by no assertion"
    ) in refusal.value.detail


def test_document_adapter_leaves_a_record_declaring_no_modality_alone() -> None:
    """The slot is optional; a record that does not set it is not checked."""

    _, capture, plan, _ = _inputs()

    result = _adapt_records(capture, deepcopy(plan["records"]))

    assert json.loads(result.canonical_plan_bytes)["records"] == plan["records"]


def test_document_census_reports_derivation_locality_and_fan_out() -> None:
    """Run-04's derivation rule bound every value to an assertion and never
    asked what the assertion said. One sentence on the data-acquisition
    paragraph carried 36 formalization targets for twelve relations it names
    no endpoint of, and the capture's largest hubs formalize 47, 23 and 12
    distinct records from single sentences on one reference-list block. The
    census reports both axes and refuses neither."""

    result = _adapt()
    census = json.loads(result.canonical_census_bytes)

    assert set(census) == {
        "assertions",
        "blocks",
        "blocks_reviewed",
        "blocks_total",
        "capture_sha256",
        "derivation",
        "gaps_by_kind",
        "subject_coverage",
    }
    assert census["derivation"] == {
        "assertion_fan_out": {"asr:001": 3, "asr:002": 0, "asr:003": 0},
        "fan_out_distribution": {"0": 2, "3": 1},
        "non_local_relations": 0,
        "relation_locality": {"inspection-of:P-7:2026-03-02": "LOCAL"},
        "top_hubs": [
            {
                "assertion": "asr:001",
                "block": "page:1:block:001",
                "records": 3,
            }
        ],
    }


def _subject_bearing() -> tuple[dict[str, object], dict[str, object]]:
    """Records typed against the research pack, one of which names its subject.

    ``Observation`` and ``Claim`` wear ``SourceAsserted`` and so carry the
    subject slot; ``Instrument`` does not, which is what the census population
    is the difference of.
    """

    _, capture, _, _ = _inputs()
    records = {
        "entities": [
            {
                "id": "instrument:ovg",
                "properties": {"name": "Pump P-7"},
                "type": "Instrument",
            },
            {
                "id": "obs:depth",
                "properties": {"name": "depth", "subject": "instrument:ovg"},
                "type": "Observation",
            },
            {
                "id": "obs:co2",
                "properties": {"name": "co2"},
                "type": "Observation",
            },
            {
                "id": "claim:mechanism",
                "properties": {"name": "mechanism"},
                "type": "Claim",
            },
        ],
        "relations": [],
    }
    capture["assertions"][0]["formalized_by"] = [
        {"path": ["properties", "subject"], "record_id": "obs:depth"}
    ]
    return capture, records


def test_document_census_reports_subject_coverage_per_bearing_type() -> None:
    """Run-08 held 131 observations and 85 claims and attached none of them to
    what they were about. Coverage of the attachment is the number that would
    have shown it at capture, so it joins the census as its own axis: per type
    the compiled contract declares as carrying `subject`, how many records name
    one and how many do not. Reported, never refused."""

    capture, records = _subject_bearing()

    result = _adapt_with_contract(capture, records)
    census = json.loads(result.canonical_census_bytes)

    assert census["subject_coverage"] == {
        "by_type": {
            "Claim": {
                "ambiguous": 0,
                "attachable": 0,
                "proposed": 0,
                "total": 1,
                "unnamed": 1,
                "with_subject": 0,
                "without_subject": 1,
            },
            "Observation": {
                "ambiguous": 0,
                "attachable": 0,
                "proposed": 1,
                "total": 2,
                "unnamed": 1,
                "with_subject": 1,
                "without_subject": 1,
            },
        },
        "ambiguous": 0,
        "attachable": 0,
        "proposed": 1,
        "total": 3,
        "unnamed": 2,
        "with_subject": 1,
        "without_subject": 2,
    }


def test_document_census_knows_no_subject_bearing_type_without_a_contract() -> None:
    """Which types may carry a subject is a contract question. With no compiled
    contract the adapter asks nothing and the axis is empty; the refusal still
    runs, because `subject` is one fixed name and needs no declaration."""

    capture, records = _subject_bearing()

    result = _adapt_records(capture, records)
    census = json.loads(result.canonical_census_bytes)

    assert census["subject_coverage"] == {
        "by_type": {},
        "ambiguous": 0,
        "attachable": 0,
        "proposed": 0,
        "total": 0,
        "unnamed": 0,
        "with_subject": 0,
        "without_subject": 0,
    }


def _attachable(
    *,
    sentence: str = "asr:001",
    named: tuple[tuple[str, str], ...] = (("instrument:ovg", "Pump P-7"),),
    subject: str | None = None,
) -> tuple[dict[str, object], dict[str, object]]:
    """One observation, and the entities the sentence formalizing it may name.

    ``asr:001`` reads "Pump P-7 was inspected on 2026-03-02." and ``asr:003``
    reads "The technician suspects bearing wear.". ``Instrument`` carries no
    subject slot and ``Observation`` does, so the instruments are what the
    census may count as named and the observation is what it counts.
    """

    _, capture, _, _ = _inputs()
    entities: list[object] = [
        {"id": record_id, "properties": {"name": name}, "type": "Instrument"}
        for record_id, name in named
    ]
    properties: dict[str, object] = {"name": "co2"}
    paths: list[list[str]] = [["properties", "name"]]
    if subject is not None:
        properties["subject"] = subject
        paths.append(["properties", "subject"])
    entities.append(
        {"id": "obs:co2", "properties": properties, "type": "Observation"}
    )
    index = {"asr:001": 0, "asr:002": 1, "asr:003": 2}[sentence]
    capture["assertions"][index]["formalized_by"] = [
        {"path": path, "record_id": "obs:co2"} for path in paths
    ]
    if index != 0:
        capture["assertions"][0]["formalized_by"] = [
            {"path": ["properties", "name"], "record_id": named[0][0]}
        ]
    return capture, {"entities": entities, "relations": []}


def test_document_census_counts_a_record_one_named_entity_could_attach() -> None:
    """Run-12 projected fifteen subjects and thirteen attached the record to
    its instrument, its database or its reference frame. A sentence naming
    exactly one entity names its tool as often as its subject, so nothing is
    set: the slot stays unset, no derivation is written for it, and the census
    counts the record `attachable` for the producer to read."""

    capture, records = _attachable()

    result = _adapt_with_contract(capture, records)
    plan = json.loads(result.canonical_plan_bytes)

    assert plan["records"] == records
    assert not [
        derivation
        for derivation in plan["derivations"]
        if derivation["path"] == ["properties", "subject"]
    ]
    census = json.loads(result.canonical_census_bytes)
    assert census["subject_coverage"]["by_type"]["Observation"] == {
        "ambiguous": 0,
        "attachable": 1,
        "proposed": 0,
        "total": 1,
        "unnamed": 0,
        "with_subject": 0,
        "without_subject": 1,
    }


def test_document_census_counts_a_sentence_two_named_entities_share() -> None:
    """A sentence naming two entities does not say which one the record is
    about, and the adapter makes no semantic judgment past the name. The slot
    stays unset, the census calls it ambiguous, and the producer sets it."""

    capture, records = _attachable(
        sentence="asr:003",
        named=(
            ("instrument:tech", "technician"),
            ("instrument:wear", "bearing wear"),
        ),
    )

    result = _adapt_with_contract(capture, records)
    plan = json.loads(result.canonical_plan_bytes)

    by_id = {record["id"]: record for record in plan["records"]["entities"]}
    assert "subject" not in by_id["obs:co2"]["properties"]
    assert not [
        derivation
        for derivation in plan["derivations"]
        if derivation["path"] == ["properties", "subject"]
    ]
    census = json.loads(result.canonical_census_bytes)
    assert census["subject_coverage"]["by_type"]["Observation"] == {
        "ambiguous": 1,
        "attachable": 0,
        "proposed": 0,
        "total": 1,
        "unnamed": 0,
        "with_subject": 0,
        "without_subject": 1,
    }


def test_document_adapter_keeps_the_subject_the_producer_set() -> None:
    """The subject is the producer's, checked as before: the census counts it
    proposed, and no derivation carries a field the grammar does not
    declare."""

    capture, records = _attachable(subject="instrument:ovg")

    result = _adapt_with_contract(capture, records)
    plan = json.loads(result.canonical_plan_bytes)

    assert plan["records"] == records
    assert not [
        derivation for derivation in plan["derivations"] if "origin" in derivation
    ]
    census = json.loads(result.canonical_census_bytes)
    assert census["subject_coverage"]["by_type"]["Observation"] == {
        "ambiguous": 0,
        "attachable": 0,
        "proposed": 1,
        "total": 1,
        "unnamed": 0,
        "with_subject": 1,
        "without_subject": 0,
    }


def test_document_census_counts_a_sentence_that_names_nothing() -> None:
    """A sentence naming no entity of the capture leaves the slot unset, which
    is the honest residue decision 18 named and the census counts."""

    capture, records = _attachable(named=(("instrument:mar", "Romanche"),))

    result = _adapt_with_contract(capture, records)
    plan = json.loads(result.canonical_plan_bytes)

    assert plan["records"] == records
    census = json.loads(result.canonical_census_bytes)
    assert census["subject_coverage"]["by_type"]["Observation"] == {
        "ambiguous": 0,
        "attachable": 0,
        "proposed": 0,
        "total": 1,
        "unnamed": 1,
        "with_subject": 0,
        "without_subject": 1,
    }


def test_document_census_counts_a_name_inside_another_word_unnamed() -> None:
    """A name inside another word names nothing: "ring" inside "bearing" is
    the shape of run-12's RTI inside "vertical". The only candidate entity is
    not named by the sentence, so the record is unnamed, not attachable."""

    capture, records = _attachable(
        sentence="asr:003", named=(("instrument:ring", "ring"),)
    )

    result = _adapt_with_contract(capture, records)

    census = json.loads(result.canonical_census_bytes)
    assert census["subject_coverage"]["by_type"]["Observation"] == {
        "ambiguous": 0,
        "attachable": 0,
        "proposed": 0,
        "total": 1,
        "unnamed": 1,
        "with_subject": 0,
        "without_subject": 1,
    }


def test_document_census_counts_nothing_without_a_compiled_contract() -> None:
    """Which types carry a subject is the contract's answer, so with no
    compiled contract the axis is empty and the plan is the producer's own."""

    capture, records = _attachable()

    result = _adapt_records(capture, records)

    assert json.loads(result.canonical_plan_bytes)["records"] == records
    census = json.loads(result.canonical_census_bytes)
    assert census["subject_coverage"]["by_type"] == {}


def test_document_census_names_a_relation_derived_away_from_its_endpoints() -> None:
    """A relation hung on a neighbouring sentence is reported, never refused."""

    reading, capture, _, _ = _inputs()
    moved = [
        item
        for item in capture["assertions"][0]["formalized_by"]
        if item["record_id"] == "inspection-of:P-7:2026-03-02"
    ]
    capture["assertions"][0]["formalized_by"] = [
        item
        for item in capture["assertions"][0]["formalized_by"]
        if item["record_id"] != "inspection-of:P-7:2026-03-02"
    ]
    capture["assertions"][2]["formalized_by"] = moved

    result = _adapt(reading=reading, capture=capture)
    derivation = json.loads(result.canonical_census_bytes)["derivation"]

    assert derivation["relation_locality"] == {
        "inspection-of:P-7:2026-03-02": "NON_LOCAL"
    }
    assert derivation["non_local_relations"] == 1
    assert derivation["assertion_fan_out"] == {"asr:001": 2, "asr:002": 0, "asr:003": 1}
    assert derivation["fan_out_distribution"] == {"0": 1, "1": 1, "2": 1}
    assert derivation["top_hubs"] == [
        {"assertion": "asr:001", "block": "page:1:block:001", "records": 2},
        {"assertion": "asr:003", "block": "page:1:block:002", "records": 1},
    ]


def test_document_census_calls_an_underived_relation_underived() -> None:
    """A relation no assertion formalizes is neither local nor non-local."""

    reading, capture, plan, _ = _inputs()
    capture["assertions"][0]["formalized_by"] = [
        item
        for item in capture["assertions"][0]["formalized_by"]
        if item["record_id"] != "inspection-of:P-7:2026-03-02"
    ]

    result = _adapt(reading=reading, capture=capture)
    derivation = json.loads(result.canonical_census_bytes)["derivation"]

    assert derivation["relation_locality"] == {
        "inspection-of:P-7:2026-03-02": "UNDERIVED"
    }
    assert derivation["non_local_relations"] == 0
