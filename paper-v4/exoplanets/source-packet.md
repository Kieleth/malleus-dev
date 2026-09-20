# LHS 1140 b: source preparation

Date: 2026-09-14. Preparation only. No model has received these sources.

The source downloads are complete: two papers, the reference-specific archive
rows and definitions, and one TESS observation product. Six files pass their
identity checks. A seventh, malformed archive CSV, is retained as a rejected
input. Candidate initial/later table projections now pass their separation tests.
The model packet is **not ready**: PDF reading, complete staged delivery, history
semantics and execution method remain open.
[source-manifest.json](source-manifest.json) records exact identities once.
[READING-FINDINGS.md](READING-FINDINGS.md) records the complete four-condition
extraction comparison. [READING-RCA.md](READING-RCA.md) corrects its causal
interpretation and withdraws the premature scope-narrowing recommendation.
Neither selects an extractor, changes source scope or approves a model run.

## What is on disk

Sources live under `private/paper-v4-exoplanets-lhs1140-01/sources/`, covered by
the repository's existing `/private/` ignore rule. No PDF or source CSV was
committed. Downloads used the browser tool, not a shell network client.

| Source | Retained file | Verified scope |
| --- | --- | --- |
| Lillo-Box et al. 2020 | `2010.06928v1.pdf` | Exact version on the first page, title and lead author, 22 pages. Joint-fit Table B.3 is on PDF page 21. |
| Cadieux et al. 2024 | `2310.15490v2.pdf` | Exact version on the first page, title and lead author, 31 pages. Joint-fit Table D1 is on PDF page 24. This preprint version was posted in December 2023. |
| NASA LHS 1140 b overview | `LHS_1140_b_planet_params.csv` | Original browser export: 20 quantity rows, seven reference columns. Values, uncertainty strings and missing-value markers are unchanged. This is not a raw Planetary Systems export. |
| NASA Planetary Systems | `LHS_1140_b_PS.xml` | Original VOTable response: seven reference-specific rows, 355 columns, successful query status, explicit units. Decimal text and empty cells are preserved. |
| NASA column definitions | `API_PS_columns.html` | Browser-saved HTML, with mass/radius/density units, reference and uncertainty fields. Page states last update 4 June 2026. |
| TESS Sector 3 light curve | `tess2018263035959-s0003-0000000092226327-0123-s_lc.fits` | Target TIC 92226327, processing version `spoc-5.0.20-20201120`, data release 42. Header declares 19,692 rows and 20 fields. No scientific fit or sample-level analysis. |

The source URLs, byte counts and SHA-256 digests are in the manifest. Both table
pages were rendered and visually inspected, alongside their text layers. The
mass, radius and reported-density entries agree with the two corresponding
NASA reference columns. This is investigator source verification, not model
capture, ontology adequacy or a Malleus result.

## Findings that affect the experiment

The older PDF's table label is B.3, not the Table 5 label seen in the HTML
rendering. Citations must use the selected file's coordinates. Its joint-fit
mass also differs from its abstract, and its prose radius uncertainty differs
from the table. Preserve attribution to the fit and location. Do not silently
repair either source or combine different estimates.

Both archive exports contain later references and ExoFOP data. They are
investigator-only. Before production, source-derived subsets must be made
mechanically from the VOTable, with exact parent/row/column locators. Inspect all
selected columns, not just the planet-reference cell: current system fields and
archive maintenance dates are not historical source snapshots. The first
producer must not receive the second study's values or our comparison notes.
Candidate table subsets now exist as described below. No astronomy population
or complete producer packet has been authored.

A per-page rerun of `pypdf==6.16.2` over all 53 pages localizes the 5,000-form
invocation warning to page 6 of the older paper. It emitted no warning on the
other 52 pages. Page 6's Figure 6 plot labels are absent from that output; some
negative Figure 5 axis labels appear with square glyphs. Both captions and the
surrounding prose remain visible. The warning comes from the extractor's form
traversal limit, not Malleus. This identifies a reader defect surface, not proof
that all other text is complete.

Poppler 26.03.0 diagnostic extracts and page renders are retained under
`inspection/`. The page-6 render confirms the missing plot labels; Poppler's
reading-order text includes them, though its displayed equation is awkward.
No reader is selected yet. Check full prose order, tables, captions and missing
glyphs before freezing locators. A successful extraction is not a completeness
assessment; figures remain outside a text-only scientific interpretation claim.

## Observation identity and the later study

The MAST portal search for `TIC 92226327`, restricted to SPOC and sequence 3,
returns the two-minute observation
`tess2018263035959-s0003-0000000092226327-0123-s`. Its downloaded FITS file confirms
the target, sector and `spoc-5.0.20-20201120` processing version. Cadieux section
II.3, PDF page 4, names that target, sector and SPOC 5.0.20. This is a supported
study connection at that level, not proof of byte equality to the authors'
working file. The columns include time, processed flux, flux uncertainty and
quality flags. Bulk samples remain in the native file, not individual graph nodes.

Observation dates are 20 September to 17 October 2018. The file creation date
is 26 November 2020, after the older paper's selected October version. The file
is therefore marked as a **later-stage candidate**. Do not present it as the
earlier study's exact input merely because its observing sector matches.

## Acquisition failures and the chosen source format

The in-app browser blocked direct downloads. Chrome's browser-extension surface
was unavailable, but its native app interface worked. It delivered the raw
archive responses, definition page and FITS. No shell network client, browser
security change or dependency installation was used. The temporary tab was
closed; existing user tabs were preserved.

NASA's `select * from ps` CSV response contains unescaped double quotes inside
HTML display fields, for example `class="supersubNumber"`. Strict CSV parsing
refuses the first data row. A permissive parser's seven rows of 355 cells did
not establish correct decoding. The original CSV is retained unchanged in the
manifest's `rejected_sources`, excluded from selected sources and covered by a
test proving the refusal.

The identical query using NASA's documented `format=votable` returns valid XML
with seven rows and 355 fields. VOTable also carries units and a query status,
so there is no need to repair CSV quoting or infer units from field names. The
CSV path was removed, with no permissive fallback. This is an explicit source
format choice for the same data, not a new scientific input or Core request.
[NASA TAP formats](https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html).

## Mechanical checks added in TDD

The initial five tests were extended in TDD. Nine now pass, including real-file
checks and the rejected CSV. They cover exact bytes, PDF identity and table
coordinates, table shape, reference closure, units, empty values, incomplete
query status, and missing, duplicated or changed FITS header identities. Table
numbers remain source strings; empty XML cells remain explicitly empty. The
FITS check compares declared header cards at known offsets, not a general FITS
parser or scientific validity check. These tests do not establish faithful model
capture, compatible scientific assumptions, source truth or launch approval.

No dependency was installed. The identity checker uses the existing research
dependency `pypdf==6.16.2` declared in `pyproject.toml`. It reads only the identity
and table-label pages, not the full PDF. Poppler is an inspection tool here;
its reproducible installation has not been added to an execution environment.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider paper-v4/exoplanets/test_source_packet.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python paper-v4/exoplanets/source_packet.py
```

## Next dependency order

1. Finish and test the deterministic source reading, including table locations,
   missing values and strict separation of initial and later sources. Resolve
   the PDF reading defect. EXO-007 resolves VOTable source-to-cell binding through
   a tested projection; FITS still has no selected row projection. Retaining
   native files alone does not verify a graph value's cell locator. No semantic
   mapping or population facts are supplied by the evaluator.
2. Define the history profile and scientific-selection semantics before ontology
   generation. The document adapter's import order is not observation time, and
   adding a later publication must not silently retire the earlier claim.
3. Verify a public Core coordinate in a reproducible environment and freeze the
   proposed execution/evaluation method for Luis's approval. The current editable
   installation is a diagnostic environment, not a selected experimental pin.
   Only after approval launch one fresh producer.

The intended demonstration is unchanged: connect the papers' numbers to their
methods and qualified interpretations, use one accepted history for calculation
and explanation, then introduce the later study while retaining the old result.
There is no new manuscript claim, Core implementation request, Core rebind,
commit or push. Core's EXO-008 reply confirms that profile composition needs an
explicit decision; mechanical mixed-profile replay does not settle it.

## Converted archive rows, EXO-007

The converter copies source cells into one JSON object per line (NDJSON), which
Core already knows how to address. It does not create graph facts. A location
such as `row:0:pl_masse` identifies the mass cell in the first projected row.
`derivation.json` links it to the unchanged XML, original row/column and FIELD
definition, including the unit. All indices are zero-based; FIELD declarations
are not data rows.

[table-selections.json](table-selections.json) explicitly lists 151 planet fields,
including uncertainties, limits, alternate units and display strings. This is
not a mass/radius-only selection. It excludes non-planet fields, including
maintenance dates and independently referenced stellar/system parameters, and
five archive-wide counters/flags: `pl_controv_flag`, `pl_nespec`, `pl_ntranspec`,
`pl_ndispec`, `pl_nnotes`. This is a candidate scope for review before delivery,
not a claim that excluded fields lack scientific value or that the current
archive row is a historical snapshot.

| Private output directory | Selected reference | Fields | Nulls | Original row |
| --- | --- | ---: | ---: | ---: |
| `table-initial-v1/` | `LILLO_BOX_ET_AL__2020` | 151 | 52 | 5 |
| `table-later-v1/` | `CADIEUX_ET_AL__2024` | 151 | 57 | 3 |

Directories are under `private/paper-v4-exoplanets-lhs1140-01/`. All 302 projected
cells match their original coordinates. Empty cells remain null, not zero;
decimal strings are not rounded or converted to floats. Standard XML entity
and line-ending decoding applies. FIELD definitions are parsed serializations,
not literal byte spans; the unchanged native XML remains authoritative.

Both outputs rebuild byte-for-byte. Verification reconstructs the expected
output from the external selection, not its own metadata. Changed numbers,
units, coordinates, columns and stages refuse. A second-file write failure
exposes no output directory, and existing directories cannot be overwritten.
Publishing assumes a single writer.

The full XML and two-stage selection file remain investigator-only. Initial
output rows and metadata exclude the later reference and unselected columns.
This tests a table boundary, not the complete delivery boundary. In particular,
giving the first consumer a trace containing the full native XML would expose
later rows. Resolve that evidence-access design before launch.

A synthetic public-API test retains XML, projected rows and conversion metadata,
accepts one source-statement record and reopens an identical graph and receipt.
Core returns the retained evidence and row locator; the adopter checker then
resolves the original XML cell. Missing rows and excluded fields refuse with
unchanged history bytes. Core does not check this XML conversion or semantic
faithfulness. No astronomical record was used in that test.

SHA-256 output identities:

| File | Initial | Later |
| --- | --- | --- |
| `rows.ndjson` | `1d4a9e3b01adc83719905cc21821fd61c63f09f1b73c282c3ff4d6904ad672b3` | `b109eb1da83477a4cb0f3d3d9509b3d2373a03af7bce9efb40688d0498cc1d5b` |
| `derivation.json` | `87734543b1d3bded29b1f21caa79b42bec802ba4cfda57d4a2617a42efc70eda` | `26e16c00bc8b30c5a542d9ac7b240376eb2f2afc91df8e6eb56ecfa730523420` |

The metadata names `source_projection.project/v1`. At generation, the converter
SHA-256 was `3493bcc97445ee8560ab3820908cc8549718f93b16be6d7cc193a6613745a499`,
the reused source checker was `0d6a9859a99193f34975720a3d50a7cc51cab99c4fb8695845164aa7aa70aaec`,
and selection configuration was `2664c6b5ef7913c9783489a31df7af3980ff8b0f83bed0d75f69e68ced981739`.
No dependency was added or installed. This is working preparation, not a frozen
Core execution environment or a model result.

Run the full local preparation suite with:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider paper-v4/exoplanets
```

Generate with `.venv/bin/python paper-v4/exoplanets/source_projection.py --stage initial --output <new-directory>`;
use `--stage later` for the second selection. The output must be absent and its
parent must exist. The retained directories already exist and refuse overwrite.
Use a new directory and compare both files for an independent rebuild.
