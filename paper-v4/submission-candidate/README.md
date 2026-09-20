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
the declared literature links with citations, and removes local link targets from
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

Open the [current PDF](../../output/pdf/malleus-paper-v4-submission-candidate.pdf).
The current page count and hashes are in QA.md and build-receipt.json. Read
the abstract, the comparison and reuse results in Section 4, and Appendix A. Every figure in the
main text is bound to a frozen public file by
`paper-v4/answer-demonstration/test_manuscript.py`, and the Small Shop figures
are bound to fresh runs by `paper-v4/test_shop_connected_calibration.py`, which
rebuilds the connected history from empty, and by
`paper-v4/test_shop_calibration.py` for the shipment-policy fixture. `EVIDENCE-ACCESS.md` maps each printed
claim to the file behind it.

First, ratify or challenge both baseline/reuse assessments. The graph reviews of
run-22 through run-26 were read in full and ratified by the author on 2026-09-16
(`paper-v4/evaluation-v4/author-ratification-2026-09-16.md`), and run-20 and
run-21 under the earlier protocol; the records keep their `preliminary` file
names and the manuscript states the ratification. Second, choose the publication evidence route: the public files
establish pins, isolation, compilation, admission, replay and every review
judgement with its locator, and they do not replay a document ledger without
the article's text. The source carries CC BY-NC-ND 4.0; redistribution of a
derived text layer is a rights decision, not a legal conclusion made here.

Then choose final title and author metadata, subject category, licence and
whether to replace the historical `arxiv/` sources. Endorsement and actual
submission remain with Luis. Robotics is not part of this document and is not
a prerequisite for it.

Luis approved including the bounded reuse result on 13 September. Its defective
absence controls are excluded from comparative conclusions; producer-only and
producer-plus-review costs are both reported. No measured break-even point,
cross-surface precision advantage or cross-session learning benefit is claimed.
Committing and uploading remain separate author decisions. The current working
changes have not been committed by this task.

Checks: `python3 -m unittest discover -s paper-v4/submission-candidate -p test_prepare.py`.
`verify_pdf.py` additionally checks every printed paragraph, heading and table
cell, intact exhibits and archive bytes; its dependency is declared in
requirements-qa.txt. The whole paper gate is `python paper-v4/run_active_tests.py`
under the locked interpreter. Tests establish transcription, archive and
figure-to-file consistency, not scientific truth.
