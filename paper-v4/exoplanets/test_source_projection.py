"""Mechanical source projection tests. No astronomical population is authored."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

import source_projection as projection
import source_packet as packet


XML = b"""<VOTABLE xmlns="http://www.ivoa.net/xml/VOTable/v1.3" version="1.3">
<RESOURCE><INFO name="QUERY_STATUS" value="OK"/><TABLE>
<FIELD name="pl_name" datatype="char" arraysize="*"/>
<FIELD name="pl_refname" datatype="char" arraysize="*"/>
<FIELD name="pl_masse" datatype="double" unit="Mearth"><DESCRIPTION> Mass </DESCRIPTION></FIELD>
<FIELD name="rowupdate" datatype="char"/>
<DATA><TABLEDATA>
<TR><TD>Example b</TD><TD><![CDATA[<a refstr=EARLY href=url>Early</a>]]></TD><TD>2.000</TD><TD>current</TD></TR>
<TR><TD>Example b</TD><TD><![CDATA[<a refstr=LATER href=url>Later</a>]]></TD><TD/><TD>current</TD></TR>
</TABLEDATA></DATA></TABLE></RESOURCE></VOTABLE>"""
SPEC = {
    "sha256": sha256(XML).hexdigest(),
    "bytes": len(XML),
    "row_count": 2,
    "column_count": 4,
    "planet": "Example b",
    "required_columns": ["pl_name", "pl_refname", "pl_masse"],
    "reference_ids": ["EARLY", "LATER"],
    "field_units": {"pl_masse": "Mearth"},
}
SELECTION = {
    "stage": "initial",
    "reference_ids": ["EARLY"],
    "columns": ["pl_name", "pl_refname", "pl_masse"],
}


def test_exact_cells_definitions_and_nulls_are_preserved():
    rows, metadata = projection.project(XML, SPEC, SELECTION)
    assert projection.project(XML, SPEC, SELECTION) == (rows, metadata)
    record = json.loads(rows)
    assert record["pl_masse"] == "2.000"
    assert set(record) == set(SELECTION["columns"])
    detail = json.loads(metadata)
    assert detail["parent_sha256"] == SPEC["sha256"]
    assert detail["source_row_indices"] == [0]
    assert detail["fields"]["pl_masse"]["source_column_index"] == 2
    assert 'unit="Mearth"' in detail["fields"]["pl_masse"]["definition_xml"]
    assert b"LATER" not in rows + metadata
    assert b"rowupdate" not in rows + metadata
    later = {**SELECTION, "stage": "later", "reference_ids": ["LATER"]}
    later_rows, _ = projection.project(XML, SPEC, later)
    assert json.loads(later_rows)["pl_masse"] is None
    cell = projection.trace_cell(XML, SPEC, SELECTION, rows, metadata, "row:0:pl_masse")
    assert cell["value"] == "2.000"
    assert cell["source_row_index"] == 0 and cell["source_column_index"] == 2


@pytest.mark.parametrize(
    "selection",
    [
        {},
        {**SELECTION, "extra": True},
        {**SELECTION, "columns": []},
        {**SELECTION, "columns": ["pl_name", "pl_name"]},
        {**SELECTION, "columns": ["missing"]},
        {**SELECTION, "reference_ids": []},
        {**SELECTION, "reference_ids": ["EARLY", "EARLY"]},
        {**SELECTION, "reference_ids": ["absent"]},
        {**SELECTION, "stage": ""},
    ],
)
def test_missing_or_ambiguous_selection_refuses(selection):
    with pytest.raises(projection.ProjectionRefusal) as caught:
        projection.project(XML, SPEC, selection)
    assert caught.value.reason == "INVALID_SELECTION"


def test_parent_identity_is_checked_before_parsing_or_conversion():
    with pytest.raises(projection.ProjectionRefusal) as caught:
        projection.project(XML.replace(b"2.000", b"9.999"), SPEC, SELECTION)
    assert caught.value.reason == "PARENT_MISMATCH"


@pytest.mark.parametrize(
    "mutation",
    [
        lambda x: x.replace(b"<TD>2.000</TD>", b"<TD>2.<b>000</b></TD>"),
        lambda x: x.replace(b"<TD>2.000</TD>", b"<TD>2.000</TD><TD>extra</TD>"),
        lambda x: x.replace(b"<TD/>", b"<WRONG/>"),
        lambda x: x.replace(b'name="rowupdate"', b'name="pl_masse"'),
        lambda x: x.replace(b'value="OK"', b'value="OVERFLOW"'),
        lambda x: x.replace(b"VOTable/v1.3", b"VOTable/v1.4"),
        lambda x: x.replace(b' version="1.3"', b""),
        lambda x: x.replace(b' version="1.3"', b' version="1.4"'),
        lambda x: x.replace(b"</TABLEDATA>", b"<WRONG/></TABLEDATA>"),
    ],
)
def test_unsupported_or_ambiguous_source_shape_refuses(mutation):
    changed = mutation(XML)
    spec = {**SPEC, "sha256": sha256(changed).hexdigest(), "bytes": len(changed)}
    with pytest.raises(projection.ProjectionRefusal) as caught:
        projection.project(changed, spec, SELECTION)
    assert caught.value.reason == "SOURCE_INVALID"


@pytest.mark.parametrize(
    "target", ["number", "null", "unit", "parent_row", "extra_column", "later_stage"]
)
def test_verifier_rebuilds_from_external_selection_not_self_declared_metadata(target):
    rows, metadata = projection.project(XML, SPEC, SELECTION)
    detail = json.loads(metadata)
    if target == "number":
        rows = rows.replace(b"2.000", b"2.0")
        detail["rows_sha256"] = sha256(rows).hexdigest()
    elif target == "null":
        record = json.loads(rows)
        record["pl_masse"] = None
        rows = json.dumps(record).encode()
        detail["rows_sha256"] = sha256(rows).hexdigest()
    elif target == "unit":
        detail["fields"]["pl_masse"]["definition_xml"] = "changed unit"
    elif target == "parent_row":
        detail["source_row_indices"] = [1]
    else:
        other = deepcopy(SELECTION)
        if target == "extra_column":
            other["columns"].append("rowupdate")
        else:
            other.update(stage="later", reference_ids=["LATER"])
        rows, metadata = projection.project(XML, SPEC, other)
        detail = json.loads(metadata)
    with pytest.raises(projection.ProjectionRefusal) as caught:
        projection.verify(XML, SPEC, SELECTION, rows, projection.canonical(detail))
    assert caught.value.reason == "PROJECTION_MISMATCH"


@pytest.mark.parametrize(
    "locator",
    [
        "row:1:pl_masse",
        "row:-1:pl_masse",
        "row:0:absent",
        "row:0:pl_masse[0]",
        "page 1",
    ],
)
def test_bad_or_excluded_cell_locator_refuses(locator):
    rows, metadata = projection.project(XML, SPEC, SELECTION)
    with pytest.raises(projection.ProjectionRefusal) as caught:
        projection.trace_cell(XML, SPEC, SELECTION, rows, metadata, locator)
    assert caught.value.reason == "INVALID_LOCATOR"


def test_complete_output_is_published_once_without_overwrite(tmp_path, monkeypatch):
    rows, metadata = projection.project(XML, SPEC, SELECTION)
    destination = tmp_path / "new"
    real_write = Path.write_bytes

    def fail_metadata(path, data):
        if path.name == "derivation.json":
            raise OSError("simulated later write failure")
        return real_write(path, data)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "write_bytes", fail_metadata)
        with pytest.raises(OSError):
            projection.publish(destination, rows, metadata)
    assert not destination.exists()
    projection.publish(destination, rows, metadata)
    assert (destination / "rows.ndjson").read_bytes() == rows
    assert (destination / "derivation.json").read_bytes() == metadata
    with pytest.raises(FileExistsError):
        projection.publish(destination, b"changed", metadata)
    assert (destination / "rows.ndjson").read_bytes() == rows


CONFIG = {
    "schema": "exoplanet-table-selection/v1",
    "parent_sha256": SPEC["sha256"],
    "columns": SELECTION["columns"],
    "stages": {"initial": {"reference_ids": ["EARLY"]}},
}


@pytest.mark.parametrize(
    "config,stage",
    [
        ({}, "initial"),
        (CONFIG, "missing"),
        (CONFIG, ""),
        ({**CONFIG, "extra": True}, "initial"),
        ({**CONFIG, "parent_sha256": "bad"}, "initial"),
        ({**CONFIG, "columns": []}, "initial"),
        (
            {**CONFIG, "stages": {"initial": {"reference_ids": ["EARLY", "EARLY"]}}},
            "initial",
        ),
        (
            {
                **CONFIG,
                "stages": {"initial": {"reference_ids": ["EARLY"], "extra": True}},
            },
            "initial",
        ),
    ],
)
def test_missing_configuration_or_unselected_stage_refuses(config, stage):
    with pytest.raises(projection.ProjectionRefusal) as caught:
        projection.stage_selection(config, stage)
    assert caught.value.reason == "INVALID_SELECTION"


def test_preparation_requires_selection_bound_to_exact_single_manifest_source(tmp_path):
    spec = {**SPEC, "filename": "input.xml", "kind": "archive_ps_votable"}
    (tmp_path / "input.xml").write_bytes(XML)
    manifest = {"sources": [spec]}
    assert projection.prepare(
        manifest, tmp_path, CONFIG, "initial"
    ) == projection.project(XML, SPEC, SELECTION)
    for sources, config in (
        ([], CONFIG),
        ([spec, spec], CONFIG),
        ([spec], {**CONFIG, "parent_sha256": "0" * 64}),
    ):
        with pytest.raises(projection.ProjectionRefusal) as caught:
            projection.prepare({"sources": sources}, tmp_path, config, "initial")
        assert caught.value.reason == "PARENT_MISMATCH"


def test_actual_stage_rows_trace_to_exact_archive_cells():
    root = Path(__file__).parent
    manifest = json.loads((root / "source-manifest.json").read_text())
    spec = next(s for s in manifest["sources"] if s["kind"] == "archive_ps_votable")
    source_dir = root.parents[1] / "private/paper-v4-exoplanets-lhs1140-01/sources"
    data = packet.verified_bytes(source_dir, spec)
    config = json.loads((root / "table-selections.json").read_text())
    table = packet.verify_ps_votable(data, spec)
    assert config["parent_sha256"] == spec["sha256"]
    for stage in ("initial", "later"):
        selection = projection.stage_selection(config, stage)
        rows, metadata = projection.project(data, spec, selection)
        assert projection.project(data, spec, selection) == (rows, metadata)
        projection.verify(data, spec, selection, rows, metadata)
        row = json.loads(rows)
        assert len(rows.splitlines()) == 1
        assert set(row) == set(config["columns"])
        assert {"pl_masse", "pl_rade", "pl_dens", "pl_orbper", "pl_orbeccen"} <= set(
            row
        )
        assert not {
            "rowupdate",
            "releasedate",
            "sy_refname",
            "st_refname",
            "pl_controv_flag",
        } & set(row)
        for field in row:
            cell = projection.trace_cell(
                data, spec, selection, rows, metadata, f"row:0:{field}"
            )
            assert (
                cell["value"]
                == table[cell["source_row_index"] + 1][cell["source_column_index"]]
            )
        if stage == "initial":
            assert b"CADIEUX" not in rows + metadata
            assert b"2024" not in row["pl_refname"].encode()


def test_public_core_resolves_projected_cells_and_replays_their_retained_sources(
    tmp_path,
):
    from importlib.resources import files
    from malleus import bundled_ontology_path
    from malleus import compiler as api
    from test_history_feasibility import SCHEMA, TIME, ACTOR

    # Reuse the existing neutral diagnostic ontology, never build astronomy facts.
    compiled = api.compile_linkml_contract(
        root_locator="probe",
        sources={
            "probe": SCHEMA,
            "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model", "model", "schema", "types.yaml")
            .read_bytes(),
        },
    )
    path = tmp_path / "history.jsonl"
    history = api.create_structural_history(
        path, compilation=compiled, transaction_time=TIME, actor_id=ACTOR
    )
    rows, metadata = projection.project(XML, SPEC, SELECTION)
    profile = api.SOURCE_ASSERTION_PROFILE
    anchors = []
    for source_id, content, media_type in (
        ("native", XML, "application/xml"),
        ("rows", rows, "application/x-ndjson"),
    ):
        anchors.extend(
            api.structural_source_anchors(
                source_id=f"source:{source_id}",
                artifact_id=f"artifact:{source_id}",
                content=content,
                media_type=media_type,
            )
        )
    anchors.append(
        api.structural_evidence_anchor(
            record_id="evidence:projection",
            content=metadata,
            media_type="application/json",
        )
    )
    history.append_anchors(
        anchors=tuple(anchors), transaction_time=TIME, actor_id=ACTOR
    )
    plan = {
        "grammar": "malleus.population-plan/private-v0",
        "plan_id": "plan:projected-cell",
        "contract_identity": history.partial_contract.identity,
        "adapter": {"adapter_id": "synthetic-source-projection-probe", "version": "1"},
        "history_profile": {
            "profile_id": profile.profile_id,
            "sha256": profile.identity,
        },
        "sources": [
            {
                "source_id": f"source:{name}",
                "sha256": "sha256:" + sha256(content).hexdigest(),
            }
            for name, content in (("native", XML), ("rows", rows))
        ],
        "evidence": [
            {
                "evidence_id": "evidence:projection",
                "sha256": "sha256:" + sha256(metadata).hexdigest(),
            }
        ],
        "records": {
            "entities": [
                {
                    "id": "cell",
                    "type": "SourceStatement",
                    "properties": {"name": "2.000"},
                }
            ],
            "relations": [],
        },
        "derivations": [
            {
                "record_id": "cell",
                "path": ["properties", "name"],
                "source_id": "source:rows",
                "locator": "row:0:pl_masse",
            }
        ],
        "gaps": [],
        "supersessions": [],
        "valid_time": {"kind": "ORDER_ONLY", "value": "capture:synthetic"},
    }
    wrong_key = deepcopy(plan)
    wrong_key["evidence"][0]["record_id"] = wrong_key["evidence"][0].pop("evidence_id")
    before = path.read_bytes()
    with pytest.raises(api.PopulationPlanRefusal) as caught:
        api.compile_population_plan(
            wrong_key,
            partial_contract=history.partial_contract,
            contract_view=compiled.view,
            base_state=api.PopulationBaseState.from_replay(history.replay()),
            history_profile=profile,
        )
    assert (
        caught.value.reason
        is api.PopulationPlanRefusalReason.MALFORMED_EVIDENCE_REFERENCE
    )
    assert path.read_bytes() == before
    for locator in ("row:1:pl_masse", "row:0:rowupdate"):
        bad = deepcopy(plan)
        bad["derivations"][0]["locator"] = locator
        before = path.read_bytes()
        with pytest.raises(api.PopulationPlanRefusal) as caught:
            api.compile_population_plan(
                bad,
                partial_contract=history.partial_contract,
                contract_view=compiled.view,
                base_state=api.PopulationBaseState.from_replay(history.replay()),
                history_profile=profile,
            )
        assert (
            caught.value.reason
            is api.PopulationPlanRefusalReason.LOCATOR_NOT_RESOLVABLE
        )
        assert path.read_bytes() == before
    compilation = api.compile_population_plan(
        plan,
        partial_contract=history.partial_contract,
        contract_view=compiled.view,
        base_state=api.PopulationBaseState.from_replay(history.replay()),
        history_profile=profile,
    )
    preparation = api.prepare_population_change(
        history=history,
        plan=plan,
        profile=profile,
        retention_events=api.population_retention_events(
            history=history, compilation=compilation, profile=profile
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    admitted = api.admit_structural_change(
        history=history, preparation=preparation, transaction_time=TIME, actor_id=ACTOR
    )
    replayed = api.KnowledgeChangeHistory.reopen(path).replay()
    assert replayed.receipt == admitted.receipt
    assert replayed.graph.export_records() == admitted.graph.export_records()
    trace = api.trace_population_record(replayed, "cell")
    assert {source.content for source in trace.sources} == {XML, rows}
    assert metadata in {item.content for item in trace.evidence}
    cell = projection.trace_cell(
        XML, SPEC, SELECTION, rows, metadata, trace.derivations[0]["locator"]
    )
    assert cell["value"] == "2.000"
    assert (cell["source_row_index"], cell["source_column_index"]) == (0, 2)
