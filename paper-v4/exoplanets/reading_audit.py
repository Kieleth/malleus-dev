"""Screen candidate PDF readings. Passing probes never approves a reading."""

from hashlib import sha256
import re


class ReadingAuditRefusal(ValueError):
    pass


def _closed(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ReadingAuditRefusal(f"expected exactly these fields: {sorted(keys)}")


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def check(candidate, expected):
    _closed(candidate, {"source_sha256", "pages"})
    _closed(expected, {"source_sha256", "page_count", "probes"})
    if (
        not isinstance(expected["source_sha256"], str)
        or not re.fullmatch(r"[0-9a-f]{64}", expected["source_sha256"])
        or candidate["source_sha256"] != expected["source_sha256"]
        or type(expected["page_count"]) is not int
        or expected["page_count"] <= 0
        or not isinstance(candidate["pages"], list)
        or not isinstance(expected["probes"], list)
        or not expected["probes"]
    ):
        raise ReadingAuditRefusal(
            "bind source identity, page count and nonempty visual probes"
        )
    ids = []
    for probe in expected["probes"]:
        _closed(probe, {"id", "page", "text"})
        if (
            not _text(probe["id"])
            or not _text(probe["text"])
            or type(probe["page"]) is not int
            or not 1 <= probe["page"] <= expected["page_count"]
        ):
            raise ReadingAuditRefusal(
                "probe needs an ID, source page and expected text"
            )
        ids.append(probe["id"])
    if len(ids) != len(set(ids)):
        raise ReadingAuditRefusal("probe IDs must be unique")
    pages = candidate["pages"]
    for page in pages:
        _closed(page, {"page", "text", "warnings"})
        if (
            type(page["page"]) is not int
            or not isinstance(page["text"], str)
            or not isinstance(page["warnings"], list)
            or not all(_text(w) for w in page["warnings"])
        ):
            raise ReadingAuditRefusal(
                "page requires an integer, exact text and explicit warnings"
            )
    issues = []
    expected_order = list(range(1, expected["page_count"] + 1))
    if [p["page"] for p in pages] != expected_order:
        issues.append(
            {
                "kind": "PAGE_ACCOUNTING",
                "detail": "missing, duplicate, extra or reordered pages",
            }
        )
    for page in pages:
        number, text = page["page"], page["text"]
        if not text.strip():
            issues.append({"kind": "EMPTY_PAGE", "page": number})
        if page["warnings"]:
            issues.append(
                {
                    "kind": "EXTRACTOR_WARNING",
                    "page": number,
                    "messages": page["warnings"],
                }
            )
        controls = sorted(
            {f"U+{ord(c):04X}" for c in text if ord(c) < 32 and c not in "\t\r\n\f"}
        )
        if controls:
            issues.append(
                {"kind": "CONTROL_CHARACTER", "page": number, "codepoints": controls}
            )
        suspect = sorted(
            {
                f"U+{ord(c):04X}"
                for c in text
                if (ord(c) < 32 and c not in "\t\r\n\f")
                or c in "\ufffd\u25a0"
                or 0xE000 <= ord(c) <= 0xF8FF
            }
        )
        if suspect or re.search(r"\(cid:\d+\)", text):
            issues.append(
                {"kind": "GLYPH_REVIEW_REQUIRED", "page": number, "codepoints": suspect}
            )
    probes = []
    for probe in expected["probes"]:
        matches = [page for page in pages if page["page"] == probe["page"]]
        present = len(matches) == 1 and "".join(probe["text"].split()) in "".join(
            matches[0]["text"].split()
        )
        probes.append({"id": probe["id"], "page": probe["page"], "present": present})
        if not present:
            issues.append(
                {
                    "kind": "MISSING_PROBE",
                    "page": probe["page"],
                    "probe_id": probe["id"],
                }
            )
    return {
        "status": (
            "DEFECTS_FOUND"
            if any(i["kind"] != "GLYPH_REVIEW_REQUIRED" for i in issues)
            else "REVIEW_REQUIRED"
            if issues
            else "CHECKS_PASS_REVIEW_REQUIRED"
        ),
        "launch_ready": False,
        "pages_received": len(pages),
        "page_text_sha256": [sha256(p["text"].encode()).hexdigest() for p in pages],
        "probes_passed": sum(probe["present"] for probe in probes),
        "probes": probes,
        "issues": issues,
    }
