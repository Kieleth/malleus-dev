"""Source preparation checks, not astronomy or model adequacy tests."""

import csv
import hashlib
import importlib.util
import json
import io
from pathlib import Path

import pytest


ROOT = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location(
    "exo_source_packet", ROOT / "source_packet.py"
)
packet = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(packet)


def test_pdf_identity_checks_title_author_version_and_table():
    spec = {
        "pages": 2,
        "first_page_markers": ["Example study", "A. Author", "arXiv:0000.00001v2"],
        "table": {"page": 2, "label": "Table B.3."},
    }
    pages = ["Example\nstudy A. Author arXiv:0000.00001v2", "Table B.3. Parameters"]
    packet.verify_pdf_identity(pages, spec)
    for original in ("Example\nstudy", "A. Author", "arXiv:0000.00001v2"):
        with pytest.raises(ValueError, match="first-page identity"):
            packet.verify_pdf_identity(
                [pages[0].replace(original, "Wrong"), pages[1]], spec
            )
    with pytest.raises(ValueError, match="table label"):
        packet.verify_pdf_identity([pages[0], "Table 5. Parameters"], spec)
    with pytest.raises(ValueError, match="page count"):
        packet.verify_pdf_identity(pages[:1], spec)


def test_exact_bytes_are_required(tmp_path):
    source = {
        "filename": "source.pdf",
        "sha256": hashlib.sha256(b"original").hexdigest(),
        "bytes": 8,
    }
    with pytest.raises(ValueError, match="missing source"):
        packet.verified_bytes(tmp_path, source)
    path = tmp_path / "source.pdf"
    path.write_bytes(b"changed!")
    with pytest.raises(ValueError, match="digest"):
        packet.verified_bytes(tmp_path, source)
    path.write_bytes(b"original")
    assert packet.verified_bytes(tmp_path, source) == b"original"


def test_csv_preserves_strings_missing_values_and_reference_identity():
    data = b"Source,Study A,Study B\nMass (unit),2.00,---\nRadius (unit),1.0,3.0\n"
    spec = {
        "references": ["Study A", "Study B"],
        "quantities": ["Mass (unit)", "Radius (unit)"],
    }
    rows = packet.verify_overview_csv(data, spec)
    assert rows[1] == ["Mass (unit)", "2.00", "---"]
    for malformed in (
        data.replace(b"Study B", b"Study A"),
        data.replace(b"Study B", b"Different study"),
        data.replace(b"Mass (unit)", b"Mass (other unit)"),
        data + b"Mass (unit),9,9\n",
        data.replace(b"2.00,---", b"2.00"),
    ):
        with pytest.raises(ValueError):
            packet.verify_overview_csv(malformed, spec)


def test_missing_required_manifest_data_is_not_defaulted():
    with pytest.raises(ValueError, match="missing required.*references"):
        packet.verify_overview_csv(b"Source,Study A\n", {"quantities": []})


def test_ps_rows_keep_one_reference_per_solution_and_empty_cells():
    data = b"""<VOTABLE xmlns="http://www.ivoa.net/xml/VOTable/v1.3" version="1.3">
    <RESOURCE type="results"><INFO name="QUERY_STATUS" value="OK"/><TABLE>
    <FIELD name="pl_name"/><FIELD name="pl_refname"/>
    <FIELD name="pl_masse" unit="Mearth"/><FIELD name="pl_masseerr2" unit="Mearth"/>
    <DATA><TABLEDATA>
    <TR><TD>Planet b</TD><TD><![CDATA[<a refstr=STUDY_A href=url>A</a>]]></TD><TD>2.000</TD><TD>-0.100</TD></TR>
    <TR><TD>Planet b</TD><TD><![CDATA[<a refstr=STUDY_B href=url>B</a>]]></TD><TD/><TD/></TR>
    </TABLEDATA></DATA></TABLE></RESOURCE></VOTABLE>"""
    spec = {
        "row_count": 2,
        "column_count": 4,
        "required_columns": ["pl_name", "pl_refname", "pl_masse", "pl_masseerr2"],
        "planet": "Planet b",
        "reference_ids": ["STUDY_A", "STUDY_B"],
        "field_units": {"pl_masse": "Mearth", "pl_masseerr2": "Mearth"},
    }
    rows = packet.verify_ps_votable(data, spec)
    assert rows[1][2:] == ["2.000", "-0.100"]
    assert rows[2][2:] == [None, None]
    for malformed in (
        data.replace(b"STUDY_B", b"STUDY_A"),
        data.replace(b"STUDY_B", b"UNKNOWN"),
        data.replace(b"Planet b", b"Planet c", 1),
        data.replace(b"pl_masseerr2", b"pl_masse"),
        data.replace(b"<TD>-0.100</TD>", b""),
        data.replace(b'value="OK"', b'value="OVERFLOW"'),
        data.replace(b'<INFO name="QUERY_STATUS" value="OK"/>', b""),
        data.replace(b"Mearth", b"Mjup"),
        b"\n",
    ):
        with pytest.raises(ValueError):
            packet.verify_ps_votable(malformed, spec)
    assert not hasattr(packet, "verify_ps_csv")


def test_malformed_archive_csv_is_retained_but_never_repaired_or_selected():
    manifest = json.loads((ROOT / "source-manifest.json").read_text())
    source_dir = ROOT.parents[1] / "private/paper-v4-exoplanets-lhs1140-01/sources"
    rejected = manifest["rejected_sources"][0]
    data = packet.verified_bytes(source_dir, rejected)
    assert rejected["filename"] not in {s["filename"] for s in manifest["sources"]}
    with pytest.raises(csv.Error):
        list(csv.reader(io.StringIO(data.decode("utf-8")), strict=True))


def fits_header(*cards):
    raw = b"".join(card.encode("ascii").ljust(80) for card in (*cards, "END"))
    return raw.ljust(((len(raw) + 2879) // 2880) * 2880, b" ")


def test_fits_identity_checks_version_target_and_header_location():
    cards = [
        "SIMPLE  =                    T / conforms to FITS standards",
        "TICID   =                 1234 / target identifier",
        "PROCVER = 'pipeline-v2' / processing version",
    ]
    data = fits_header(*cards)
    spec = {"headers": [{"offset": 0, "cards": cards}]}
    packet.verify_fits_headers(data, spec)
    for malformed in (
        data.replace(b"pipeline-v2", b"pipeline-v1"),
        data.replace(b"1234", b"9999"),
        fits_header(cards[0], cards[1]),
        fits_header(*cards, cards[2]),
        data.replace(b"END" + b" " * 77, b" " * 80),
        data[:-1],
    ):
        with pytest.raises(ValueError):
            packet.verify_fits_headers(malformed, spec)
    with pytest.raises(ValueError):
        packet.verify_fits_headers(data, {"headers": [{"offset": 1, "cards": cards}]})


def test_documentation_requires_units_and_reference_definitions():
    spec = {"required_markers": ["Planet Mass [Earth Mass]", "pl_refname"]}
    data = b"<html>Planet Mass [Earth Mass] pl_refname</html>"
    packet.verify_text_markers(data, spec)
    for malformed in (b"", data.replace(b"Earth Mass", b"Jupiter Mass")):
        with pytest.raises(ValueError, match="documentation marker"):
            packet.verify_text_markers(malformed, spec)


def test_retained_real_sources_match_manifest():
    manifest = json.loads((ROOT / "source-manifest.json").read_text())
    source_dir = ROOT.parents[1] / "private/paper-v4-exoplanets-lhs1140-01/sources"
    result = packet.verify_packet(manifest, source_dir)
    assert result["verified_source_count"] == 6
    assert result["launch_ready"] is False
    assert result["pdf_pages"] == [22, 31]
