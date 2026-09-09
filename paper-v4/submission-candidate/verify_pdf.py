"""Check built candidate transcription and source archive. Visual QA is separate."""

from hashlib import sha256
import json
import re
import tarfile
import unicodedata

from pypdf import PdfReader

from prepare import HERE, ROOT, convert


def normalized(value):
    return "".join(
        char.lower() for char in unicodedata.normalize("NFKD", value) if char.isalnum()
    )


def verify():
    receipt = json.loads((HERE / "build-receipt.json").read_text())
    source = (HERE.parent / "manuscript-v4-working.md").read_bytes()
    pdf = ROOT / "output/pdf/malleus-paper-v4-submission-candidate.pdf"
    assert sha256(source).hexdigest() == receipt["manuscript_sha256"], (
        "Manuscript changed after build"
    )
    assert sha256(pdf.read_bytes()).hexdigest() == receipt["pdf_sha256"], (
        "PDF bytes differ"
    )
    for name, identity in receipt["files"].items():
        assert sha256((HERE / name).read_bytes()).hexdigest() == identity, (
            f"Source drift: {name}"
        )
    for name, value in convert(source.decode()).items():
        assert (HERE / name).read_text() == value, f"Conversion drift: {name}"
    archive = HERE / "candidate-source.tar"
    assert sha256(archive.read_bytes()).hexdigest() == receipt["archive_sha256"]
    with tarfile.open(archive) as handle:
        assert sorted(handle.getnames()) == receipt["archive_files"]
        for member in handle.getmembers():
            assert member.isfile() and "/" not in member.name
            assert (
                handle.extractfile(member).read() == (HERE / member.name).read_bytes()
            )
    reader = PdfReader(pdf)
    pages = []
    for index, page in enumerate(reader.pages, 1):
        lines = page.extract_text().splitlines()
        assert lines[-1] == str(index), f"Unexpected footer on page {index}"
        pages.append("\n".join(lines[:-1]))
    text = normalized(re.sub(r"\[\d+\]", "", "\n".join(pages)))
    normalized_pages = [normalized(page) for page in pages]
    blocks = re.split(r"\n\s*\n", source.decode().strip())
    units_checked = 0
    for block in blocks:
        if (
            block.startswith("# ")
            or block == "Luis Guzman Lorenzo. Author-review draft."
        ):
            continue
        if block.startswith("|"):
            units = [
                cell.strip()
                for line in block.splitlines()
                if not re.fullmatch(r"[| :\-]+", line)
                for cell in line.strip("|").split("|")
            ]
            assert any(
                all(normalized(cell) in page for cell in units)
                for page in normalized_pages
            ), "Table split across pages"
        else:
            units = [re.sub(r"^#{1,3} |^```json\n|\n```$", "", block)]
        for unit in units:
            plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", unit).replace("*", "")
            assert normalized(plain) in text, f"Missing printed unit: {plain[:90]}"
            units_checked += 1
    exhibits = re.findall(r"```json\n(.*?)\n```", source.decode(), re.S)
    for exhibit in exhibits:
        assert any(normalized(exhibit) in page for page in normalized_pages), (
            "JSON exhibit split"
        )
    return {
        "status": "TRANSCRIPTION_AND_ARCHIVE_PASS",
        "pages": len(pages),
        "paragraph_heading_cell_units": units_checked,
        "intact_json_exhibits": len(exhibits),
        "archive_files": receipt["archive_files"],
        "pdf_sha256": receipt["pdf_sha256"],
        "visual_review": "SEPARATE_REQUIRED_CHECK",
        "human_ratification": "PENDING",
    }


if __name__ == "__main__":
    result = verify()
    (HERE / "transcription-check.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
