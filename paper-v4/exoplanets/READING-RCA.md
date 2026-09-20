# Reading RCA: lost extraction, not unreadable science

2026-09-14. EXO-009. Diagnosis requested by Luis. No reader selected or repaired.

## Conclusion

The inspected pages render legibly. The observed failures do not establish that
the papers, equations or figures are damaged or unrecoverable. They establish
several specific extractor failures and an error in our own diagnostic checker.
Calling all of them "damaged equations and figure regions" was inaccurate.
Proposing source-scope narrowing before testing recoverability was premature.

The original requirement remains: preserve supported source meaning, including
figures and tables. An unresolved extraction problem is a gap to investigate,
not permission to remove that source content from the experiment. No source,
question set, ontology, population, Core runtime or experiment scope changed.

## What the causal tests established

### 1. Pypdf plain skips the second figure after counting drawing markers

Earlier paper, PDF page 6. The page invokes two figure forms, `/Im6` (object 421)
and `/Im7` (object 432). Across their nested content it invokes 14,396 forms,
with 11 distinct objects. The first figure alone makes 14,386 nested calls to
seven marker forms. Those seven forms contain drawing operations, no text-show
operations. Repeated plot markers exhaust the plain reader's 5,000-call guard
before the second figure is visited.

One isolated process changed only the in-memory traversal limit, then restored
it. The source PDF and installed pypdf files were not changed.

| Observation | Default 5,000 | Diagnostic 20,000 |
| --- | --- | --- |
| `Peak periods (d)` | Absent | Present |
| `24.7` | Absent | Present |
| `Normalized ﬂux` | Present | Present |
| Correct minus sign in `−0.006` | Absent | Absent |
| Traversal warning | Present | Absent |
| Extracted characters | 3,933 | 4,106 |

Plain extraction before/after SHA-256:
`ee742fc72821e96ded1daead61417e89ead3aca8c52f552dba6e2ee3397e7121`
and `57d3be412f8f608e4ee919e0d3086dde5bbedf65c4e2d14ef889effa2e62fd75`.

The cap explains the second figure's missing labels, not every failed page-6
probe. Raising a safety limit is a causal test, not an approved production fix.
A repair must preserve bounded work and cycle protection.

### 2. Layout mode does not traverse embedded figure forms

This is a different mechanism. In installed pypdf 6.16.2, `_layout_mode_text`
passes the page's own content stream to `text_show_operations`. Neither that
function nor `recurse_to_target_op` follows the `Do` operation into a form.
The remaining operation handler ignores it. Font collection likewise visits
page/parent resources, not nested form resources.

Both figures therefore disappear from this page's layout-mode text without a
form-omission warning. Presenting `/Im7`'s unchanged content and resources as an
isolated in-memory page makes the same layout extractor return `Peak periods
(d)` and `24.7`. This confirms that the figure contains extractable text; the
page-level traversal does not reach it. Rotated-text layout warnings remain.
This isolated test does not establish correct full-page layout reconstruction.

Code locations in the installed dependency:

- `pypdf/_page.py`: `_extract_text__xform`, `_layout_mode_fonts`, `_layout_mode_text`.
- `pypdf/_text_extraction/_layout_mode/_fixed_width_page.py`:
  `text_show_operations`, `recurse_to_target_op`.
- `pypdf/_text_extraction/_layout_mode/_text_state_manager.py`:
  `set_state_param` ignores unsupported operations, including `Do`.

### 3. The missing minus signs are a font-decoding precedence problem

Earlier page 6, `/Im6`, font `/F3`, `/USNJQB+HFBRSY10`. Its explicit PDF
`/Encoding /Differences` maps character 0 to `/minus`. Pypdf's first decoding
step correctly resolves that to `−`. But the embedded Type1 font program has
an internal encoding entry `dup 0 /.notdef put`.

Because there is no ToUnicode map, pypdf invokes `_type1_alternative`, then
overwrites its already-correct explicit encoding with the built-in `.notdef`
entry. Its glyph table converts `.notdef` to `□`. The rendered PDF shows minus
signs, and Poppler's extraction preserves them.

In a temporary in-memory test, preventing only that built-in-font override
restored five minus signs in the first figure. The resulting text differed only
at those five `□` to `−` substitutions. No source text was supplied by an
evaluator. The correct mapping was already explicitly declared in the PDF.

### 4. Incomplete character maps hide usable equation glyph names

The later PDF contains two relevant embedded Type1 fonts:

- `/IWHZYN+CMEX10`, font object 1755.
- `/FBKLIZ+CMEX9`, font object 1985.

Their ToUnicode maps omit codes used by the document for parentheses, brackets
and square roots. Their embedded font programs still identify these glyphs:

| Source character code | Embedded glyph name | Existing pypdf glyph interpretation |
| --- | --- | --- |
| 0 | `parenleftbig` | `(` |
| 1 | `parenrightbig` | `)` |
| 18 | `parenleftbigg` | `(` |
| 19 | `parenrightbigg` | `)` |
| 20 | `bracketleftbigg` | `[` |
| 21 | `bracketrightbigg` | `]` |
| 112 | `radicalbig` | `√` |

In `pypdf/_cmap.py`, `_parse_to_unicode` uses `_type1_alternative` only if the
ToUnicode object is absent, not when it exists but omits a used character.
The unmapped delimiter codes become control characters; code 112 becomes the
ordinary letter `p`. These are not legitimate mathematical transcriptions.

A second causal test extracted all 31 pages, removed only those two ToUnicode
entries from the in-memory reader, then extracted all pages again. It reused
pypdf's existing font-program decoder and glyph-name table. No output was saved
as a candidate reading and no PDF was rewritten.

| PDF page | Only changes in plain extracted text |
| --- | --- |
| 19 | Four control characters become parentheses; one `p` becomes `√`. |
| 22 | Two control characters become parentheses. |
| 23 | Six control characters become parentheses/brackets. |
| 24 | One `p` becomes `√` in the noise-test formula below Table D1. |
| 25 | Eighteen control characters become parentheses. |
| 27 | One `p` becomes `√`. |

The other 25 page strings remain identical. All 30 reported delimiter control
characters disappear. Three previously unflagged letter substitutions are also
corrected. On page 24, the visible noise-test formula contains a square root of
`2/N_RV`; the original extracted string instead contains a standalone `p`.
That page had no audit issue despite the mathematical error. The five passing
Table D1 probes never established faithfulness of the entire page.

This demonstrates recoverability of these glyphs from retained source data.
It does not justify deleting all ToUnicode maps in production. A real repair
must preserve valid explicit mappings, use font-local evidence for missing
entries, and report contradictions or unknowns. Decoding glyphs also does not
reconstruct fraction scope, superscripts, matrix layout or scientific meaning.

### 5. Our own checker called a ligature a missing label

The retained plain output already contains `Normalized ﬂux`. Our probe expects
`Normalized flux`. `reading_audit.check` removes whitespace but compares the
remaining characters literally, so it labels the probe missing. This is a false
alarm, not a lost scientific label. The exact frozen report remains unchanged.

Conversely, a plausible wrong letter such as `p` instead of `√` passes a screen
for control characters. The checker also does not flag the open square `□`
used for `.notdef`; the specific minus-sign probe caught that problem. A larger
blacklist alone cannot establish faithful decoding.

Any repair should define the narrow equivalences used for comparison without
rewriting the retained reading. Blanket compatibility normalization is not a
safe mathematical repair: it can erase distinctions such as superscripts.
Tests must keep ligature equivalence separate from signs, units and exponents.

## What remains unproved

Poppler's loss of the solar-unit symbol in earlier Table B.3 is reproduced.
The font program names character 12 `/circledot`, which pypdf resolves as `⊙`;
the original page visibly contains it. Absence of a ToUnicode object does not
mean the information is absent. The precise Poppler-internal decision that
drops this glyph was not traced, so it remains a specific open diagnostic,
not a reason to describe the PDF as corrupt.

The earlier PDFium/pdfplumber spot checks remain limited observations, not
evidence that either engine cannot be configured usefully. No new extractor,
OCR route, model, dependency or runtime was selected. The full mathematical and
visual reading remains unverified even if these isolated glyph repairs work.
No historical known-good extraction was compared, so this is not a demonstrated
version regression.

## Smallest proposed prevention and repair boundary

This is adopter-side source reading, before ontology construction or Malleus
admission. These reproductions demonstrate no failure of Core's ledger/replay.
Do not ask Core to invent astronomy facts or to compensate for missing input.
Any runtime change must be routed to its owning task after an agreed cut.

Proposed TDD requirements, not implemented or authorized by this RCA:

1. A page with repeated non-text drawing forms followed by a text-bearing form
   must return that text or explicitly refuse completeness. Preserve bounded
   traversal and cycle protection. No silent form omission in layout mode.
2. Explicit font encoding must not be replaced by a `.notdef` fallback. A partial
   Unicode map must not turn a source-identified radical into an ordinary letter.
   Test missing, valid and conflicting mappings separately with synthetic fonts.
3. A ligature-only difference is not missing content. A lost minus, unit or
   exponent remains a real failure. Comparison must not rewrite evidence bytes.
4. Recheck these exact PDFs after a selected repair. Retain complete outputs,
   account for changed regions, and visually verify equations, table structure
   and figure labels. Passing the glyph cases is not whole-document approval.

The recommended next action is to agree that bounded reading repair, not shrink
the experiment. Until then the extraction gaps stay recorded as unresolved;
their current status must not be mistaken for evidence that recovery is impossible.

## Reproduction notes

All causal tests used repository `.venv/bin/python`, pypdf 6.16.2, with
`PYTHONDONTWRITEBYTECODE=1`. Exact source names, versions and digests are in
`source-manifest.json`. The earlier and later digests were checked before the
causal tests; the later source was checked again after the in-memory experiment.
Private source root: `private/paper-v4-exoplanets-lhs1140-01/sources/`.

The retained unmodified four-condition report is `reading-investigation-v2.json`,
SHA-256 `4a05200d6057932c8b1e7554a5a28de3ac3656676faa24ecac6859dff6d62eef`.
It contains original page strings and warnings, including the false ligature
alarm. It was not rewritten to make the diagnosis look better.

The existing preparation suite still passes 74 tests. Those tests do not cover
all the newly identified failures and no repair is claimed. Source PDFs, retained
comparison and both audit implementation hashes were verified unchanged after
the investigation. Only this front's diagnosis/status documents were updated.

To reproduce the key font counterfactual without editing any file, open the
later PDF with `PdfReader(..., strict=True)`, retain `extract_text()` for every
page, and remove `/ToUnicode` only from the in-memory `/CMEX9` and `/CMEX10`
font dictionaries. Extract all pages again and compare strings with
`difflib.SequenceMatcher(..., autojunk=False)`. The exact subset font names
are listed above. Expect the six changed pages and 33 changed characters listed
in the table, with the other page strings unchanged. Do not write this modified
reader back to a PDF or treat its output as an approved reading.

The traversal counterfactual sets
`pypdf._page.MAX_XFORM_INVOCATIONS_PER_EXTRACTION` to 5,000 then 20,000 in one
temporary process, extracting earlier page index 5 from a fresh reader for each
condition and restoring the original constant in `finally`. Expected text
hashes are listed above. The separate form-isolation test supplies `/Im7` and
its own `/Resources` as `/Contents` and `/Resources` of an in-memory `PageObject`
and uses layout extraction with `layout_mode_strip_rotated=False`.

The source/reader distinction also agrees with pypdf's own discussion of
ligatures, nested mathematics and positioned PDF text. That documentation is
background, not evidence for the version-specific causal findings above.
[pypdf text extraction documentation](https://pypdf.readthedocs.io/en/stable/user/extract-text.html).
