# Candidate QA, 16 September 2026

Seventeen pages: ten main-text pages, two references pages and five appendix
pages. Main text is 7,979 whitespace-separated words; including appendices,
9,341. The earlier 3,500-word target is an author-approved guideline.

Two finished results entered the manuscript in this revision and nothing else
changed: the connected Small Shop history as Section 3 and Appendix B, and the
injected-fault control as a new Section 4.6, with one abstract sentence for
each and one added measurement in the closing paragraph of Section 7. The old
4.6 to 4.9 became 4.7 to 4.10 and the two cross-references that named them were
moved with them.

Every page this revision changed was rendered at 75 dpi and inspected: the
abstract on page 1, the connected Small Shop section and its three-row stage
table on pages 2 and 3, Section 4.6 and its eleven-row fault table on pages 6
and 7, the closing paragraph of Section 7 on page 10, and the rebuilt Appendix
B with its three exhibits on pages 16 and 17. No clipping, overlapping text,
missing glyph, split table or split JSON exhibit was observed. Both new tables
have four columns. The fault table's catcher column wraps to three lines on
"admission structural check" and the fault names break at their underscores;
both stay inside their cells.

verify_pdf.py passes all 366 paragraph/heading/table-cell units, eleven intact
JSON exhibits, generated source fidelity and the five-member archive closure.
TeX Live 2026 reports no unresolved citation, overflow or missing character.
The bibliography has twenty entries.

Manuscript SHA-256:
f3165c9b64edce94bca14b78fce4b11d6c374c394321f7ee4cf35d8c08f164a3.
PDF SHA-256:
5c686da44ccdf4ada50e36ea2f3be88b4fcfcf5635e031bff132d1af72a300a8.
Source archive SHA-256:
62d5a63e9fd622bac8fa0d4639623c18cc049dff558c26ee4671192cfcaafc9e.

After the agent's build, the overseer made three edits and rebuilt: the pinned
private-fixture list in test_gate_integration.py was extended with
`private/paper-v4-relationship-repair-01` (added to the manifest on 14 September
without the pin, so the whole gate had been red since then) and with
`private/paper-v4-fault-injection-01`, which was also registered in the
manifest so the isolated-clone gate declares the fault cell's private input;
and Section 7's "The Small Shop is synthetic" became "The Small Shop
transcribes a published example; its shipment cohort is synthetic and labelled
so, and its rules are an adopter's choice, not a Malleus invariant", which the
new Section 3 made necessary. Page 10 was re-rendered and inspected after that
edit; no clipping or overlap.

A further edit followed: the author stated he had read the five later
graph-result review records in full, and the manuscript now says so at 4.4,
in Section 7 and in the Appendix A identities, bound by a new test to
`paper-v4/evaluation-v4/author-ratification-2026-09-16.md`, which carries the
digest of each record read. The baseline and reuse assessments stay unratified
and the appendix keeps HUMAN RATIFICATION PENDING for them. The candidate was
rebuilt again, and pages 4, 10 and 15, which carry the three edited
sentences, were rendered at 75 dpi and inspected: no clipping, overlap or
split exhibit. The 4.4 link to the ratification record prints as the plain
word "record", as the builder prints every local link.

One later change re-cut two strings in Appendix B. Core moved on main to
ff1c6931, and with it the content-addressed identity of the contract revision
policy, so the connected Small Shop chain's warehouse and synthetic ledgers
digest differently. The warehouse ledger is now
32798a67f4b2d5b6fab2de102ae6c4b41087f04ae794547517497232256ac333 and the
synthetic ledger 15c7c1eff28ff59496fd937de19181f649e9c8c9c4c1e895cf56252f434bd204;
the Table 1 ledger is unchanged. No domain value, count, exhibit or sentence
moved with them: the three stage rows, the three Appendix B exhibits and the
abstract sentence all still match a chain rebuilt from empty. The candidate was
rebuilt and verify_pdf.py rerun over it: 17 pages again, the same 366
paragraph, heading and table-cell units and the same eleven intact exhibits.
Both changed strings sit in the closing paragraph of Appendix B on page 17. No
new visual inspection was made for this rebuild.

Those two strings were re-cut again on 19 September 2026, when the paper's
Core pins moved to d89a0c4718654249ad678eaff62e7b1daba30b6f, and neither
moved. `test_shop_connected_calibration.py` rebuilt the chain from empty
against the checkout's Core at that commit and all fifteen passed, including
the one that compares the three printed ledger digests with a fresh run. The
mechanism is readable and was checked rather than assumed: the chain's ledger
digests hang off the validated contract's producer digest, which
`_contract_pipeline/elaborate.py` computes over five Core source files,
`_contract_compiler.py`, `_contract_pipeline/__init__.py`, `elaborate.py`,
`model.py` and `view.py`. The one-call atomic admission changed `compiler.py`,
`logic.py` and `_contract_pipeline/population.py` and added
`_contract_pipeline/admission.py`, none of those five, so the producer digest
stays sha256:683df284eaf8bb20d8872583bb2f73a9ea316b37d13f5282be934702e846d0da
and the warehouse and synthetic ledgers stay where E-0468 left them. A Core
change is expected to move a replay receipt by the producer digest alone; this
one did not move it at all.

Two of the three Core pins moved on 19 September 2026, under E-0436: when Core
changes, the paper's pin moves to the new commit, the cells re-run on it and
the new fingerprints are the baseline. The new pin is
d89a0c4718654249ad678eaff62e7b1daba30b6f, the sealed commit carrying Core's
one-call atomic admission `malleus.compiler.check_and_admit_population_plan`,
governance head OVR-000468. The rule cells moved from e7937b89 and the Shop
reconsideration cell from d5d014ba. Three fingerprints moved with them, all
three for the same reason, which is that Core's own bytes moved: the census
cell and the rule-adoption cell each pinned 52 modules
sha256:d57f3cc9b8af9dcd1245e92e956f23b7d63351d4a9bbce2100909ab5949b1355 and
now pin 53 modules
sha256:340196130e1820e9a4f9979223f40dcf6b8c1227d8805d812fd08ca529a3ed04; the
Shop reconsideration cell pinned 52 modules
sha256:f2fd444d09072c02575e64d6e918b30599b2ccb5823639188d76dabb72a3e73c and
now pins the same new value. The one module added is
`_contract_pipeline/admission.py`. No measurement moved: the two groups read
184 and 32, the counts they read on the old pins, and every domain artifact,
count and digest the cells bind is byte-identical. The Core each run was
produced on is a separate coordinate and did not move; the Shop
reconsideration cell now keeps the two apart by name, and the manuscript still
states d5d014ba for the third boundary.

The first pin did not move, and that is a measured refusal rather than a
choice. Against a `git archive` of d89a0c47 the answer-demonstration group
reads 30 failed, 631 passed, 2 subtests passed. Twenty-nine of the failures
are `pilot.verify_runtime` refusing before any Core work happens: each frozen
run's own manifest declares its `core_commit` as
160878cf14c0d27b11a440e26688708e9b7a7e2b, and the harness compares the
installed package against that tree before it will reproduce anything. The
thirtieth gets past that guard and is refused by Core itself with
SOURCE_BINDING_REQUIRED when a retained population plan is recompiled:
records of that lineage carry types that declare `assertion_locator` without
setting it, and every Core from e7937b89 onward refuses that under the
source-assertion profile. How many of the twenty-nine would also be refused on
content is not established, because the runtime guard stops them first. Moving
this pin therefore needs either the frozen run manifests rewritten or those
populations produced again, and neither is a gate decision. The pin stays at
160878cf and the group reads 661 passed plus 2 subtests there.

The full active paper gate was rerun after the pins moved and exited 0. The
command:

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python paper-v4/run_active_tests.py \
      -p no:cacheprovider

It runs four partitions. 661 tests plus two subtests passed against the Core
pinned at 160878cf, 184 tests passed against the Core pinned at d89a0c47 for
the four rule-cell modules, 32 tests passed against the same pin for the Shop
reconsideration cell, and 2,547 tests passed in the unpinned partition, which
imports the checkout's Core at d89a0c47: 3,424 tests plus two subtests in
total, including the 56 manuscript bindings, the fifteen connected Small Shop
calibrations and the thirty fault-injection contract tests. Each pinned group
imports its own export in process as well as in subprocesses, and a cell named
by a pin is collected once, in that group. Two pin entries name the same
commit and stay two groups, because a group is a commit plus an import path
and only the commit is shared.

The Small Shop figures are now bound by two files. `test_shop_connected_calibration.py`
rebuilds the connected history from empty and compares every stage row, the
ordering comparison, the abstract sentence and both new Appendix B exhibits;
it takes about two and a half minutes. `test_shop_calibration.py` was reduced
to the shipment-policy fixture, which is the only Small Shop history whose
refusal comes from a retained domain rule, and it still binds that fixture's
prose figures and its Appendix B exhibit.

Every public file this revision changed was measured against the selected
reading at the sixty-character window. The manuscript's forty-nine windows, the
fourteen in body.tex and the thirty-five in appendix.tex are the article title
in Section 4.1 and the Appendix A source excerpts, unchanged in count by this
revision; every changed region, and every other changed file, shares nothing.

The revised draft reports reuse with both cost accounts and excludes defective
controls from comparative conclusions. It no longer claims comparative
precision, a measured break-even point or a reasoning budget from aggregate
token totals. Frozen experiment results and judgements are unchanged.

E-0373 corrects the global claim that no reported graph used evidence
predicates: run-26 has two positively reviewed SUPPORTS links about depth
reliability. Its two question-specific scientific argument links remain
missing.

The candidate was not rebuilt on 19 September 2026, because the build refused.
`prepare.py` treats any Overfull hbox in the TeX log as a layout failure and
raises before it writes anything, so `build-receipt.json`,
`transcription-check.json`, the five source files, `candidate-source.tar` and
the PDF are still the 18 September build described above and still describe a
manuscript without Section 3.2. That build's manuscript was
f3165c9b64edce94bca14b78fce4b11d6c374c394321f7ee4cf35d8c08f164a3; the working
manuscript is now
2e678a945153d47185b36f7d0fe16a44b7e2e03d80e8a669eae5cb83daf55594. The two overflows are both in the Section 3.2
boundary table, an eight-column table the converter lays out at scriptsize:
the header "Obligations" is 2.67532pt too wide for its 0.1 linewidth column
and "Correctly" is 4.87267pt too wide for its 0.08 linewidth column. The log
reports no undefined citation, no undefined reference and no missing
character. Nothing else blocks the build. Making it fit means either shorter
column headers in the manuscript or a change to how the converter allocates
table column widths, and both are author decisions, not a re-cut. Section 3.2
also still contradicts the abstract, which describes the Small Shop as
model-free, so a rebuild before that sentence is settled would print the
contradiction.

No Core change, new producer/reviewer, commit, upload or arXiv server
processing. The fault-injection control changed nothing in Core: four
constructions it admits are recorded with reproducers and left alone. Human
ratification and the public full-evidence access decision remain open.
