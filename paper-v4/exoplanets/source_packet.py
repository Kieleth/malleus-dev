"""Verify retained exoplanet sources. This neither extracts facts nor launches a run."""

import csv
import hashlib
import io
import json
import re
from xml.etree import ElementTree
from pathlib import Path

import pypdf


def required(record, key):
    if key not in record:
        raise ValueError(f"missing required field: {key}")
    return record[key]


def verified_bytes(source_dir, source):
    filename = required(source, "filename")
    if not filename or Path(filename).name != filename:
        raise ValueError("source filename must be a single relative filename")
    path = source_dir / filename
    if not path.is_file():
        raise ValueError(
            f"missing source: {path}; retrieve the manifest's exact source"
        )
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != required(source, "sha256"):
        raise ValueError(f"source digest mismatch: {filename}")
    if len(data) != required(source, "bytes"):
        raise ValueError(f"source byte count mismatch: {filename}")
    return data


def verify_pdf_identity(pages, spec):
    """Check selected identity surfaces, never imply a complete PDF reading."""
    if len(pages) != required(spec, "pages"):
        raise ValueError("PDF page count mismatch")

    def compact(page):
        text = page if isinstance(page, str) else page.extract_text()
        if not text:
            raise ValueError("required PDF identity surface has no text")
        return "".join(text.split()).casefold()

    first = compact(pages[0])
    for marker in required(spec, "first_page_markers"):
        if "".join(marker.split()).casefold() not in first:
            raise ValueError(f"PDF first-page identity mismatch: {marker}")
    table = required(spec, "table")
    page_number = required(table, "page")
    if not 1 <= page_number <= len(pages):
        raise ValueError("table page outside PDF")
    label = required(table, "label")
    if "".join(label.split()).casefold() not in compact(pages[page_number - 1]):
        raise ValueError(f"PDF table label mismatch: {label}")


def verify_overview_csv(data, spec):
    """Return original cell strings, with no numeric conversion or gap filling."""
    references = required(spec, "references")
    quantities = required(spec, "quantities")
    rows = list(csv.reader(io.StringIO(data.decode("utf-8")), strict=True))
    if not rows or rows[0][0] != "Source":
        raise ValueError("archive CSV requires its Source header")
    headers = rows[0][1:]
    if len(headers) != len(set(headers)) or not set(references) <= set(headers):
        raise ValueError("archive reference identity is missing or duplicated")
    if any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("archive CSV has a ragged row")
    labels = [row[0] for row in rows[1:]]
    if len(labels) != len(set(labels)) or not set(quantities) <= set(labels):
        raise ValueError("archive quantity/unit identity is missing or duplicated")
    return rows


def read_ps_votable(data, spec):
    """Return verified rows, FIELD elements and reference IDs without coercion."""
    ns = {"v": "http://www.ivoa.net/xml/VOTable/v1.3"}
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError as exc:
        raise ValueError("PS VOTable is malformed XML") from exc
    namespace = "{" + ns["v"] + "}"
    if root.tag != namespace + "VOTABLE" or root.attrib.get("version") != "1.3":
        raise ValueError("PS requires the declared VOTable 1.3 surface")
    statuses = root.findall(".//v:INFO[@name='QUERY_STATUS']", ns)
    if not statuses or any(required(s.attrib, "value") != "OK" for s in statuses):
        raise ValueError("PS query did not report complete success")
    tables = root.findall(".//v:TABLE", ns)
    if len(tables) != 1:
        raise ValueError("PS response requires one table")
    fields = tables[0].findall("v:FIELD", ns)
    headers = [required(f.attrib, "name") for f in fields]
    data_tables = tables[0].findall("v:DATA/v:TABLEDATA", ns)
    if len(data_tables) != 1:
        raise ValueError("PS requires one inline TABLEDATA surface")
    rows = [headers]
    for row in data_tables[0]:
        if row.tag != namespace + "TR":
            raise ValueError("PS TABLEDATA requires TR elements only")
        if any(cell.tag != namespace + "TD" or len(cell) for cell in row):
            raise ValueError("PS rows require text-only TD cells")
        rows.append([cell.text for cell in row])
    if len(rows) != required(spec, "row_count") + 1:
        raise ValueError("PS row count mismatch")
    if (
        len(headers) != required(spec, "column_count")
        or len(headers) != len(set(headers))
        or not set(required(spec, "required_columns")) <= set(headers)
        or not {"pl_name", "pl_refname"} <= set(headers)
    ):
        raise ValueError("PS column identity is missing or duplicated")
    if any(len(row) != len(headers) for row in rows[1:]):
        raise ValueError("PS table has a ragged row")
    for name, unit in required(spec, "field_units").items():
        if (
            name not in headers
            or required(fields[headers.index(name)].attrib, "unit") != unit
        ):
            raise ValueError(f"PS field unit mismatch: {name}")
    references = []
    for row in rows[1:]:
        if row[headers.index("pl_name")] != required(spec, "planet"):
            raise ValueError("PS planet identity mismatch")
        reference = row[headers.index("pl_refname")]
        if not isinstance(reference, str):
            raise ValueError("PS row has no reference identity")
        matches = re.findall(r"\brefstr=([A-Z0-9_]+)\s", reference)
        if len(matches) != 1:
            raise ValueError("PS row requires one reference identity")
        references.append(matches[0])
    expected = required(spec, "reference_ids")
    if (
        len(references) != len(set(references))
        or len(expected) != len(set(expected))
        or set(references) != set(expected)
    ):
        raise ValueError("PS reference identity is missing or duplicated")
    return rows, fields, references


def verify_ps_votable(data, spec):
    """Read the declared VOTable surface, preserving decimal text and empty TDs."""
    rows, _, _ = read_ps_votable(data, spec)
    return rows


def verify_fits_headers(data, spec):
    """Compare exact 80-byte header cards at known offsets. Not a FITS reader."""
    if not data or len(data) % 2880:
        raise ValueError("FITS source must contain complete 2880-byte blocks")
    for header in required(spec, "headers"):
        offset = required(header, "offset")
        if (
            type(offset) is not int
            or offset < 0
            or offset % 2880
            or offset >= len(data)
        ):
            raise ValueError("FITS header offset must identify a retained block")
        cards = []
        for start in range(offset, len(data), 80):
            try:
                card = data[start : start + 80].decode("ascii").rstrip()
            except UnicodeDecodeError as exc:
                raise ValueError("FITS header has invalid ASCII before END") from exc
            if card == "END":
                break
            cards.append(card)
        else:
            raise ValueError("FITS header END is missing")
        for expected in required(header, "cards"):
            key = expected[:8].strip()
            matches = [card for card in cards if card[:8].strip() == key]
            if matches != [expected]:
                raise ValueError(f"FITS header identity mismatch or duplicate: {key}")


def verify_text_markers(data, spec):
    text = data.decode("utf-8")
    for marker in required(spec, "required_markers"):
        if marker not in text:
            raise ValueError(f"documentation marker missing: {marker}")


def verify_packet(manifest, source_dir):
    if pypdf.__version__ != required(manifest, "identity_checker_pypdf"):
        raise ValueError(
            "use the declared pypdf version in the project's research dependencies"
        )
    sources = required(manifest, "sources")
    names = [required(source, "filename") for source in sources]
    if len(names) != len(set(names)):
        raise ValueError("duplicate source filename")
    pdf_pages = []
    for source in sources:
        data = verified_bytes(source_dir, source)
        kind = required(source, "kind")
        if kind == "pdf":
            reader = pypdf.PdfReader(io.BytesIO(data), strict=True)
            verify_pdf_identity(reader.pages, source)
            pdf_pages.append(len(reader.pages))
        elif kind == "archive_overview_csv":
            verify_overview_csv(data, source)
        elif kind == "archive_ps_votable":
            verify_ps_votable(data, source)
        elif kind == "fits_observation":
            verify_fits_headers(data, source)
        elif kind == "html_documentation":
            verify_text_markers(data, source)
        else:
            raise ValueError(f"unsupported source kind: {kind}")
    return {
        "verified_source_count": len(sources),
        "pdf_pages": pdf_pages,
        "launch_ready": False,
    }


if __name__ == "__main__":
    root = Path(__file__).parent
    manifest = json.loads((root / "source-manifest.json").read_text())
    source_dir = root.parents[1] / "private/paper-v4-exoplanets-lhs1140-01/sources"
    print(json.dumps(verify_packet(manifest, source_dir), sort_keys=True))
