# Native reading assessment

2026-09-15. EXO-011. Inspection only, not a selected reading or model run.

## Result

Keep the native-source route. It supplies structured equations, table cells and
figure files that avoid the diagnosed PDF font/traversal failures. It is not a
perfect substitute without verification: the later HTML visibly inserts `CLOSE`
into two formulas, and both editions require their own locators. A plain-text
dump of either page would again discard useful structure.

No source content was excluded, no transcription was hand-repaired and no
experiment input was replaced. The original PDFs remain the comparison sources.
The inspected HTML is live, not yet retained as a complete offline document.

## Inspected editions and coverage

- Earlier: <https://arxiv.org/html/2010.06928v1>, compared with retained PDF
  pages 6 and 21–22.
- Later: <https://arxiv.org/html/2310.15490v2>, compared with retained PDF
  pages 4–8, 19, 24 and 26.

Rendered PDF pages were inspected, not treated as equivalent to extracted text.
The browser inspection covered both full document structures, mathematical
annotations, duplicate identifiers, conversion-error elements and figure assets.
Visual and semantic comparisons were targeted to the known extraction failures,
the principal parameter tables and the passages explaining the interpretation.
This is not an exhaustive visual review of every equation, table or figure.

| Observed surface | Earlier edition | Later edition |
| --- | --- | --- |
| Figure containers | 17 | 18 |
| Table containers | 5 | 8 |
| Referenced scientific image files retained | 20 | 23 |
| MathML elements | 790 | 563 |
| MathML elements without a TeX annotation in `alttext` | 0 | 0 |
| Duplicate HTML identifiers | 0 | 0 |
| Explicit `ltx_ERROR` elements | 0 | 2 |

Counts describe the HTML, not completeness against the PDFs. Multi-panel figures
can use several files. All 43 discovered scientific assets downloaded through
the browser's asset tool. All 30 SVG files parsed; their `href` references were
either embedded data or resolved internal identifiers. This narrow check is not
full SVG resource closure or proof of pixel-level equivalence.

## Positive comparisons

| Earlier failure or required distinction | Native-source observation |
| --- | --- |
| Earlier page 6: missing second plot and damaged negative ticks | Figure 5's image retains negative phase ticks and both planet panels. Figure 6's image retains its period labels, including 24.7, and the peak-period legend. Both were compared visually with the PDF. |
| Earlier Table B.3: solar/planet units and column membership | HTML `A2.T5`, labelled Table 5, retains parameter, prior and posterior columns, solar/terrestrial unit symbols and signed uncertainties. Its continuation is part of the same table. Compared with both PDF pages. |
| Later Table D1: values must remain assigned to b or c | HTML `A4.T1` retains both planet columns, descriptions, units, uncertainties, limits and the albedo condition. Compared with the full PDF table. |
| Later page 19: missing delimiters and radical | TeX annotations for `A3.E1.m1`, `A3.E2.m1` and `A3.SS1.p2.m3` preserve the fraction/exponent scopes and square root visible in the PDF. |
| Later page 24: ordinary letter in place of square root | `A4.I2.i3.p1.m3` supplies `\sigma_{K}=\sigma_{\rm RV}\sqrt{2/N_{\rm RV}}`; its MathML contains `msqrt` over the same ratio. This agrees with the rendered PDF. |
| Meaning must include qualifications | Section IV.1 retains the explanation of the revised measurements. Figure 3 and its caption preserve the alternative composition curves and the inability to distinguish gas-rich from water-rich interiors using mass and radius alone. Checked against PDF pages 6–7. |

The later comparison table replaces PDF citation aliases with numbered links.
Those inspected links resolve to the corresponding bibliography entries for
Dittmann, Ment and Lillo-Box. Keep the link targets, not just the visible numbers.
Neither table renumbering nor citation-style changes justify reusing PDF locators.

## Defects and source issues, kept separate

**Two HTML-generated formula defects.** At `S4.SS2.p2.m1` and `A5.SS1.p3.m1`,
the later HTML inserts an actual MathML operator with the text `CLOSE`:

```html
<mo fence="true" lspace="0em">CLOSE</mo>
```

The TeX annotation ends before the closing parenthesis; the immediately following
ordinary text begins with that parenthesis. The rendered PDF shows the formula
and parenthesis without `CLOSE`, on pages 7 and 26 respectively. The browser
visibly displays the extra word in Section IV.2. Thus a successful error-class
scan or presence of TeX annotations does not prove faithful rendering.

The observed HTML/math boundary explains the immediate defect. The original TeX
archive and converter implementation were not inspected, so the upstream reason
for that boundary is not established. Keeping the exact TeX annotation together
with surrounding text is a candidate solution to test, not an implemented fix.
Do not globally delete `CLOSE`, invent a parenthesis or treat isolated math nodes
as self-contained propositions.

**Two explicit conversion warnings.** The later page retains the unsupported
`\tablenocomments` command beside Tables C1 and D1. D1's compared rows remain
present. This observation does not approve every C1 cell or all table metadata.
The earlier main kernel equation also carries TeX layout commands (`\penalty`)
in its annotation. Native markup still needs an explicitly tested delivery rule.

**Source issues, not extraction repairs.** The earlier Table B.3 continuation
contains the malformed upper uncertainty `0.001.8` in both PDF and HTML. The
later stellar-parameter prose gives the revised mass with a radius unit in both
surfaces, while nearby prose uses a mass unit. Preserve these statements and
their locations; any scientific interpretation or correction belongs to a
separate source-grounded decision. No values were corrected here.

## Smallest next step, still requiring a selected implementation

Prepare one complete, retained native reading per edition, with all figure
assets and original PDFs. Preserve paragraph order, TeX/MathML, table structure,
captions, bibliography links and edition-local locators. No answer-shaped subset.

Before selecting that reading, use failing tests for these observed error
classes: mathematical scope crossing a text boundary, visible converter tokens
outside `ltx_ERROR`, missing figure assets, loss of table units/column membership,
and accidental rewriting of source anomalies. A document-wide inventory is not
a substitute for the targeted visual/semantic comparisons. Then verify the
actual producer-facing delivery, including how it accesses images. Neither an
asset on disk nor its caption proves that a model can inspect it.

This keeps the original experiment about connected measurements, assumptions and
accepted interpretation changes. No generic Core runtime defect is established
by these HTML/PDF reading issues. Reusable acquisition changes belong with their
owner; no Core or OCR session was instructed during this assessment.

## Retained inspection evidence and limits

Scientific image files are private under
`private/paper-v4-exoplanets-lhs1140-01/native-html-inspection-v1/`, in
`earlier-figures/` and `later-figures/`. Their browser-generated manifests retain
original URLs and temporary acquisition paths. The corresponding retained file
is in the same folder as the copied manifest, with the basename of its original
`path`. Every retained file was checked byte-identical to its downloaded file.

Manifest SHA-256 values:

- Earlier: `6c1ea6fc3f92603bd5e63e0d8d9ecc9211fb9e3360155343448dc373df9a8b71`.
- Later: `7e383630c80b819bca932042718e4c8263711d87656e4e8b5704817977b09e1c`.

These identify acquisition manifests, not a frozen HTML reading or a digest of
all figure bytes. The browser supports asset retention but refused its advertised
whole-page export operation. No shell-network substitute or fabricated raw HTML
file was used. Whole-document byte retention remains part of the next step.
Both original PDF digests still match `source-manifest.json`. No code, model
input, source manifest, Core path, shared plan, branch, commit or push changed.
