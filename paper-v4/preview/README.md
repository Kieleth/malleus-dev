# Review PDF

This renders manuscript-v4-working.md without editing the arXiv sources.
It supports only the heading, paragraph, table and JSON-exhibit forms used by
this draft. Appendix headings start a new page. JSON exhibits are kept intact
with their lead-in, validated as JSON, and limited to 100 characters per line.
External citations remain clickable; repository evidence links are available
in the companion Markdown, not portable links in the PDF.

From the repository root, using a dedicated preview environment:

```sh
pip install -r paper-v4/preview/requirements.txt
python paper-v4/preview/render.py paper-v4/manuscript-v4-working.md output/pdf/malleus-paper-v4-evidence-appendix-review.pdf
python -m unittest discover -s paper-v4/preview -p 'test_render.py'
```

The authoring task used the existing bundled runtime with these package versions,
without installing dependencies. Generated PDFs are review artifacts, not
source evidence or frozen publication bundles. Inspect rendered pages after
changes; text extraction alone cannot validate layout.
