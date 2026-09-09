"""Candidate source fidelity and archive boundaries, not experimental claims."""

import importlib.util
import json
from pathlib import Path
import re
import unittest


HERE = Path(__file__).resolve().parent


class CandidateTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "candidate_prepare", HERE / "prepare.py"
        )
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_every_json_exhibit_is_byte_preserved(self):
        source = (HERE.parent / "manuscript-v4-working.md").read_text()
        files = self.module.convert(source)
        actual = re.findall(
            r"\\begin\{lstlisting\}\n(.*?)\n\\end\{lstlisting\}",
            files["appendix.tex"],
            re.S,
        )
        expected = re.findall(r"```json\n(.*?)\n```", source, re.S)
        self.assertEqual(actual, expected)
        self.assertGreater(len(actual), 6)

    def test_unknown_markdown_and_malformed_table_refuse(self):
        for block in (
            "- silently lost list",
            "```python\npass\n```",
            "| A | B |\n| --- | --- |\n| 1 |",
        ):
            with self.assertRaises(ValueError):
                self.module.block_tex(block)

    def test_all_citations_have_bibliography_entries(self):
        files = self.module.convert(
            (HERE.parent / "manuscript-v4-working.md").read_text()
        )
        keys = set(re.findall(r"\\cite\{([^}]+)\}", files["body.tex"]))
        entries = set(
            re.findall(r"@\w+\{([^,]+),", (HERE / "references.bib").read_text())
        )
        self.assertEqual(keys, entries)
        self.assertEqual(len(keys), 8)

    def test_archive_is_exact_source_allowlist(self):
        config = json.loads((HERE / "build-config.json").read_text())
        self.assertEqual(
            set(config["archive_files"]),
            {"main.tex", "body.tex", "appendix.tex", "references.bib", "main.bbl"},
        )
        self.assertFalse(
            any(
                "private" in path or path.endswith(".pdf")
                for path in config["archive_files"]
            )
        )

    def test_font_package_uses_installed_outline_fonts(self):
        config = json.loads((HERE / "build-config.json").read_text())
        self.assertIn("lmodern", config["tex_packages"])
        self.assertIn(r"\usepackage{lmodern}", (HERE / "template.tex").read_text())

    def test_bold_lead_in_stays_inside_exhibit_container(self):
        source = '# Title\n\nLuis Guzman Lorenzo. Author-review draft.\n\n## Abstract\n\nText.\n\n## Appendix A. Evidence\n\n**Quantity:** the record is:\n\n```json\n{"count": 19}\n```'
        appendix = self.module.convert(source)["appendix.tex"]
        self.assertIn(
            "\\begin{minipage}{\\linewidth}\n\\textbf{Quantity:} the record is:",
            appendix,
        )

    def test_archive_refuses_any_extra_material(self):
        files = {
            name: b"source"
            for name in (
                "main.tex",
                "body.tex",
                "appendix.tex",
                "references.bib",
                "main.bbl",
            )
        }
        with self.assertRaises(ValueError):
            self.module.archive_bytes(
                {**files, "private/selected-reading.json": b"secret"}
            )

    def test_required_evidence_and_ratification_limits_survive(self):
        files = self.module.convert(
            (HERE.parent / "manuscript-v4-working.md").read_text()
        )
        all_text = " ".join(files.values())
        for phrase in (
            "Source-bearing artifacts remain private",
            "HUMAN RATIFICATION PENDING",
            "not a statistical comparison",
            "Robotics simulation is a candidate application",
        ):
            self.assertIn(phrase, all_text)

    def test_every_printed_experiment_report_has_an_access_entry(self):
        source = (HERE.parent / "manuscript-v4-working.md").read_text()
        required = set(re.findall(r"\]\((answer-demonstration/[^)]+\.md)\)", source))
        access = (HERE / "EVIDENCE-ACCESS.md").read_text()
        mapped = set(re.findall(r"\]\(\.\./(answer-demonstration/[^)]+\.md)\)", access))
        self.assertTrue(required, "The manuscript must identify its result reports")
        self.assertFalse(
            required - mapped, f"Unmapped result reports: {required - mapped}"
        )
        for relative in mapped:
            self.assertTrue((HERE.parent / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
