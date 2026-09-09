# Submission candidate, not a submission

This directory renders the current working manuscript without replacing the
historical `arxiv/` sources. It does not select an arXiv category, licence,
affiliation, ratification status or submission date. Nothing has been uploaded.

Run `python3 paper-v4/submission-candidate/prepare.py` from the repository.
`build-config.json` declares Python, the TeX distribution packages, executable
lookup and all build commands. No Python package installation is needed for
the builder. It uses a new local scratch directory, disables shell escape,
builds the bibliography, checks the final log and emits the candidate PDF plus
an explicit five-file source archive. Missing tools fail with their names.
No fonts or packages are downloaded by the builder.

`manuscript-v4-working.md` is the sole prose and exhibit source. `prepare.py`
converts its supported Markdown, preserves each JSON exhibit verbatim, replaces
the eight literature links with citations, and removes local link targets from
the printed text. Unknown list/code/table forms refuse. The candidate therefore
prints the evidence report names but does not pretend that private reports are
available from hyperlinks in the PDF. `EVIDENCE-ACCESS.md` maps those materials.

`candidate-source.tar` contains only main.tex, body.tex, appendix.tex,
references.bib and main.bbl. It is an uncompressed tar, not a full experiment
archive. It contains selected source excerpts already printed in the manuscript,
but no publisher PDF, full reading, capture, ledger, credentials, cache or
development history. Extra files refuse archive construction. The bibliography
is regenerated locally; the retained bbl also supports a source-only build.

Local TeX Live 2026 succeeds. arXiv's documented default is TeX Live 2025;
server processing has not been tested. The source uses distribution packages
and no shell escape, custom fonts, scripts or external assets. arXiv requires
the submitting author to inspect its processed PDF before completing submission.
See [arXiv TeX preparation](https://info.arxiv.org/help/submit_tex.html), checked
7 September 2026. A successful local build does not certify that later step.

## Remaining author decisions

For a short first pass, open the [current PDF](../../output/pdf/malleus-paper-v4-submission-candidate.pdf).
Read the abstract, the six worked answers, then Appendix A.3 and Appendix B.
Those distinguish a supported hypothesis, an insufficient evidence link and
the one question covered after a task-directed amendment. The primary counts
remain eight and eleven covered questions, not amended totals. In particular,
do not read the composition result as a question-blind extraction improvement.

Next inspect the [two new Sol results](../answer-demonstration/OVERNIGHT-RESULTS.md).
Their weaker coverage is retained. One covered answer resides in prose despite
zero graph edges; this is not typed composition. The [optional robotics note](../robotics-evidence-assessment.md)
and [Re-entry conformance note](../reentry-paper-plan.md#later-conformance-result-the-graph-is-not-the-whole-history)
are separate proposals for inclusion, not part of this PDF. Neither establishes
an external action loop. No additional capture is needed to make this review.

First, inspect and accept or challenge the model-assisted support and coverage
judgments. No file marks them human-ratified. Second, choose the publication
evidence route: the current appendix is inspectable but the private full inputs
prevent public reproduction. Confirm redistribution permissions before releasing
any additional source-bearing material. The source article carries CC BY-NC-ND
4.0; this note is not a legal conclusion about a derived artifact.

Then choose final title/author metadata, subject category, licence and whether
to replace the historical formal sources. Endorsement and actual submission
remain with Luis. Robotics and further Re-entry results are not prerequisites
for this document case study. Both new overnight captures and their complete
reviews are reported separately in answer-demonstration/OVERNIGHT-RESULTS.md;
the candidate's short supplementary paragraph does not replace primary results.

Checks: `python3 -m unittest discover -s paper-v4/submission-candidate -p test_prepare.py`.
`verify_pdf.py` additionally checks every printed paragraph/heading/table cell,
intact exhibits and archive bytes; its dependency is declared in
requirements-qa.txt and is available in the bundled artifact runtime. The PDF
also has a render-and-inspect step, recorded separately. Tests establish
transcription and archive boundaries, not scientific truth.
