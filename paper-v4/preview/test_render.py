"""Review-copy fidelity and refusal checks, separate from the experiment gate."""

from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest

from pypdf import PdfReader

from render import render, table_rows


class ReviewRenderTests(unittest.TestCase):
    def test_question_tables_reserve_space_for_words_not_only_ids(self):
        from render import column_weights

        weights = column_weights(4)
        self.assertEqual(len(weights), 4)
        self.assertAlmostEqual(sum(weights), 1)
        self.assertGreaterEqual(weights[0], 0.25)
        self.assertGreaterEqual(weights[-1], 0.40)
        self.assertAlmostEqual(sum(column_weights(8)), 1)
        with self.assertRaises(ValueError):
            column_weights(3)

    def test_ragged_table_refuses(self):
        with self.assertRaisesRegex(ValueError, "equal-width"):
            table_rows("| A | B | C | D |\n| --- | --- | --- | --- |\n| 1 | 2 |")

    def test_invalid_separator_refuses(self):
        with self.assertRaisesRegex(ValueError, "separator"):
            table_rows(
                "| A | B | C | D |\n| --- | wrong | --- | --- |\n| 1 | 2 | 3 | 4 |"
            )

    def test_source_cannot_be_output(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source.md"
            source.write_text("# Title\n\nUnchanged.")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                render(source, source)
            self.assertEqual(source.read_text(), "# Title\n\nUnchanged.")

    def test_unsupported_markdown_refuses(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source.md"
            source.write_text("# Title\n\n```python\nprint(1)\n```")
            output = Path(directory) / "out.pdf"
            with self.assertRaisesRegex(ValueError, "Unsupported Markdown"):
                render(source, output)
            self.assertFalse(output.exists())

    def test_json_exhibit_and_appendix_start_survive_rendering(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source.md"
            source.write_text(
                '# Title\n\nMain text.\n\n## Appendix A. Evidence\n\n```json\n{\n  "rows": [],\n  "count": 19\n}\n```\n'
            )
            output = Path(directory) / "out.pdf"
            render(source, output)
            pages = PdfReader(output).pages
            self.assertEqual(len(pages), 2)
            self.assertIn("Appendix A. Evidence", pages[1].extract_text())
            self.assertIn('"count": 19', pages[1].extract_text())

    def test_malformed_or_oversized_json_exhibit_refuses(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source.md"
            output = Path(directory) / "out.pdf"
            for body in ('{"count": }', '{"value": "' + "x" * 200 + '"}'):
                source.write_text("# Title\n\n```json\n" + body + "\n```\n")
                with self.assertRaises(ValueError):
                    render(source, output)

    def test_every_draft_paragraph_and_table_cell_survives(self):
        source = Path(__file__).resolve().parents[1] / "manuscript-v4-working.md"
        with TemporaryDirectory() as directory:
            output = Path(directory) / "out.pdf"
            render(source, output)
            reader = PdfReader(output)
            appendix_page = next(
                i
                for i, p in enumerate(reader.pages)
                if "Appendix A. Evidence" in p.extract_text()
            )
            self.assertLessEqual(appendix_page, 5)
            self.assertLessEqual(len(reader.pages) - appendix_page, 6)
            bodies = []
            for index, page in enumerate(reader.pages, 1):
                lines = page.extract_text().splitlines()
                self.assertEqual(
                    lines[:2], ["Malleus | Author-review draft", str(index)]
                )
                bodies.append(" ".join(lines[2:]))
            actual = " ".join(" ".join(bodies).split())
            self.assertNotIn("\u25a0", actual)
            self.assertNotIn("\ufffd", actual)
            for exhibit in re.findall(r"```json\n(.*?)\n```", source.read_text(), re.S):
                self.assertTrue(
                    any(
                        " ".join(exhibit.split()) in " ".join(page.split())
                        for page in bodies
                    ),
                    "A record exhibit must not split across pages",
                )
            units = []
            blocks = re.split(r"\n\s*\n", source.read_text().strip())
            for index, block in enumerate(blocks):
                if block.startswith("#"):
                    title = re.sub(r"^#{1,3} ", "", block)
                    following = re.sub(r"^#{1,3} ", "", blocks[index + 1]).replace(
                        "*", ""
                    )
                    start = " ".join(following.split()[:6])
                    self.assertTrue(
                        any(
                            title in page and start in " ".join(page.split())
                            for page in bodies
                        ),
                        f"Orphan heading: {title}",
                    )
                if block.startswith("|"):
                    cells = [
                        " ".join(cell.replace("*", "").split())
                        for row in table_rows(block)
                        for cell in row
                    ]
                    self.assertTrue(
                        any(all(cell in page for cell in cells) for page in bodies),
                        "A paper table must remain on one page",
                    )
                    for line in block.splitlines():
                        if not re.fullmatch(r"[| :\-]+", line):
                            units.extend(line.strip("|").split("|"))
                else:
                    units.append(re.sub(r"^```json\n|\n```$", "", block))
            for unit in units:
                plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", unit)
                plain = re.sub(r"^#{1,3} ", "", plain).replace("*", "")
                self.assertIn(" ".join(plain.split()), actual)


if __name__ == "__main__":
    unittest.main()
