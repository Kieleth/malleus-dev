# Candidate QA, 7 September 2026

Local source build passes with TeX Live 2026. Five main pages, one bibliography
page and seven appendix pages. The working manuscript is at SHA-256
7d24ff8ff821db6316f03756ee505bf5c285c1c3c0f48ddfbd344553875dabe0.
Its 3,016-word main includes one separate paragraph reporting both new Sol
reviews without changing the original result table.
The earlier composition review PDF remains byte-identical.

All thirteen candidate pages were inspected as rendered PNGs. After adding the
supplementary result paragraph, twelve pages remain byte-identical to the
inspected render and the changed fifth page was inspected again. No clipped text, missing glyph, split JSON exhibit,
split table or orphan exhibit lead-in remains. The source archive was unpacked
into a new directory and compiled independently. All thirteen rendered pages
match the candidate byte-for-byte; bibliography bytes also match. PDF container
bytes differ with build metadata, so no byte-identical PDF claim is made.

`verify_pdf.py` checks all 234 paragraph, heading and table-cell units, twelve
intact JSON exhibits, generated TeX fidelity, the five-member archive closure
and file digests. Source JSON is byte-preserved in TeX; printed text is checked
with typography-normalized characters, not treated as a new evidence source.
The final TeX log has no unresolved citations, overflow or missing characters.
Minor underfull spacing warnings were inspected, not suppressed.

The first build stopped before producing a deliverable because the default T1
font required an unavailable generated font in a nonwritable cache. A RED test
preceded selecting the already installed Latin Modern outline fonts in the
template and dependency configuration. No install was performed. Visual review
then caught a bold exhibit lead-in split from its JSON block. A RED test preceded
fixing the paragraph grouping rule for formatted lead-ins. No evidence changed.
The first QA pass reported four missing paragraphs because page-number text
interrupted them at page breaks. After explicit footer checking and removal,
all units matched. The checker still refuses actual missing text. Ruff caught
one unused import in that checker; it was removed and the check passes.

Focused paper/query/review/candidate gate: 251 passed after the evidence-access
index check. Existing preview layout gate: eight passed at the preceding build.
Candidate source tests: nine of the 251. This is not a full
repository or Core CI claim. All source-only build files remain candidate-owned;
historical arXiv sources, Core, other tasks and shared refs were not changed.

The access index had not caught up with the printed supplementary conditions.
A new test first failed for the seven result reports named by the manuscript,
then passed after each received an explicit access entry. Every linked report
must exist. This checks report discoverability, not the truth of its content.
The index now distinguishes typeset-paper reproduction, retained-result checking
and fresh model generation. No full evidence package was exported. The working
manuscript, PDF and source tar retain the exact hashes below; no render changed.

PDF SHA-256:
c55ebc609b27b6be2f2d02254cd582ff9b29eec41cf3d0ae5f00726964f98e3a.
Source tar SHA-256:
98552f79c3ffdc1cd9c8a4653ac47b554f4607f4d1b8f0ac92b8d437d7ce763f.
arXiv server processing, public full-evidence access and human ratification
remain unperformed. This is ready for author inspection, not an upload verdict.
