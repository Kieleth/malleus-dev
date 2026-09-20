"""Retain a local four-condition reading comparison. This selects no reader."""

import argparse
from hashlib import sha256
import io
import json
import logging
import os
from pathlib import Path
import platform
import subprocess
from tempfile import TemporaryDirectory

import pypdf

import reading_audit
import source_packet


def publish_report(path, data):
    """Publish one complete diagnostic, exclusively, without modifying old files."""
    with TemporaryDirectory(prefix=".reading-audit-", dir=path.parent) as scratch:
        staged = Path(scratch) / "report.json"
        staged.write_bytes(data)
        os.link(staged, path)


class Warnings(logging.Handler):
    def __init__(self):
        super().__init__(logging.WARNING)
        self.messages = []

    def emit(self, record):
        self.messages.append(record.getMessage())


def collect_pypdf(data, mode):
    reader = pypdf.PdfReader(io.BytesIO(data), strict=True)
    logger = logging.getLogger("pypdf")
    pages = []
    for number, page in enumerate(reader.pages, 1):
        handler = Warnings()
        logger.addHandler(handler)
        try:
            text = page.extract_text(
                extraction_mode=mode, layout_mode_strip_rotated=False
            )
        finally:
            logger.removeHandler(handler)
        pages.append({"page": number, "text": text, "warnings": handler.messages})
    return pages


def collect_poppler(path, executable, count, layout):
    pages = []
    for number in range(1, count + 1):
        command = [
            str(executable),
            "-f",
            str(number),
            "-l",
            str(number),
            "-enc",
            "UTF-8",
        ]
        if layout:
            command.append("-layout")
        result = subprocess.run(
            [*command, str(path), "-"], capture_output=True, check=True, timeout=30
        )
        pages.append(
            {
                "page": number,
                "text": result.stdout.decode("utf-8"),
                "warnings": result.stderr.decode("utf-8").splitlines(),
            }
        )
    return pages


def run(root, private, executable):
    tools = json.loads((root / "reading-audit-tools.json").read_bytes())
    if pypdf.__version__ != tools["python_package"]["version"]:
        raise ValueError("pypdf differs from the declared diagnostic dependency")
    version = subprocess.run(
        [str(executable), "-v"], capture_output=True, check=True, timeout=10
    ).stderr.decode()
    if (
        version.splitlines()[0]
        != "pdftotext version " + tools["external_tool"]["version"]
    ):
        raise ValueError("pdftotext differs from the declared diagnostic version")
    manifest = json.loads((root / "source-manifest.json").read_bytes())
    specifications = json.loads((private / "reading-probes-v1.json").read_bytes())
    pdfs = [source for source in manifest["sources"] if source["kind"] == "pdf"]
    if set(specifications) != {source["filename"] for source in pdfs}:
        raise ValueError(
            "reading probes must account for every selected PDF exactly once"
        )
    cases = []
    for source in pdfs:
        data = source_packet.verified_bytes(private / "sources", source)
        expected = specifications[source["filename"]]
        if (
            expected["source_sha256"] != source["sha256"]
            or expected["page_count"] != source["pages"]
        ):
            raise ValueError(
                "probe source identity/page count differs from the retained PDF"
            )
        for name in (
            "pypdf-plain",
            "pypdf-layout",
            "poppler-default",
            "poppler-layout",
        ):
            if name.startswith("pypdf-"):
                pages = collect_pypdf(data, name.split("-")[1])
            else:
                pages = collect_poppler(
                    private / "sources" / source["filename"],
                    executable,
                    source["pages"],
                    name == "poppler-layout",
                )
            candidate = {"source_sha256": source["sha256"], "pages": pages}
            cases.append(
                {
                    "source": source["filename"],
                    "method": name,
                    "candidate": candidate,
                    "assessment": reading_audit.check(candidate, expected),
                }
            )
    return {
        "schema": "exoplanet-reading-investigation/v1",
        "selected_reader": None,
        "python": platform.python_version(),
        "pypdf_version": pypdf.__version__,
        "pdftotext_version": version,
        "pdftotext_binary_sha256": sha256(executable.read_bytes()).hexdigest(),
        "probe_bytes_sha256": sha256(
            (private / "reading-probes-v1.json").read_bytes()
        ).hexdigest(),
        "code_sha256": {
            name: sha256((root / name).read_bytes()).hexdigest()
            for name in ("reading_audit.py", "inspect_pdf_readings.py")
        },
        "cases": cases,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdftotext", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    private = root.parents[1] / "private/paper-v4-exoplanets-lhs1140-01"
    if args.output.exists():
        raise FileExistsError("use a new result path, never overwrite an investigation")
    result = run(root, private, args.pdftotext)
    data = json.dumps(
        result,
        ensure_ascii=False,
        sort_keys=True,
        allow_nan=False,
        separators=(",", ":"),
    ).encode()
    # One completed diagnostic artifact, no proposed or accepted reading is published.
    publish_report(args.output, data)
    print(
        json.dumps(
            {
                "output_sha256": sha256(data).hexdigest(),
                "cases": [
                    {
                        "source": c["source"],
                        "method": c["method"],
                        "pages": c["assessment"]["pages_received"],
                        "status": c["assessment"]["status"],
                        "probes_passed": c["assessment"]["probes_passed"],
                    }
                    for c in result["cases"]
                ],
            },
            indent=2,
        )
    )
