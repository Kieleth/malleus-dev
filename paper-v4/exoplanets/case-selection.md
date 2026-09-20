# Case recommendation: LHS 1140 b

Date: 2026-09-14
Status: LHS 1140 b selected by Luis; experiment inputs not yet complete.
Evaluator-facing research notes. Do not deliver this file to a question-blind producer.

## Recommendation

Use LHS 1140 b, comparing Lillo-Box et al. (2020) with Cadieux et al. (2024).
It offers a bounded change in interpretation, explicit numerical solutions and
identifiable observing material. Retain planet c where necessary to understand
the system, but focus the demonstration on b.

Luis accepted this recommendation with "ok, go". This permits preparation, not
execution or a claim that either study establishes the planet's true composition.

## Three candidates compared

| Candidate | Verified material | Assessment for this experiment |
| --- | --- | --- |
| LHS 1140 b | Two studies and reference-specific archive solutions; a later reanalysis revises mass, radius and composition interpretation. | Recommended. Clear before/after evidence and identifiable methods. |
| TOI-561 b | Lacedelli et al. (2021) reports density 3.0 ± 0.8 g/cm³; Brinkman et al. (2023) reports 4.8 ± 0.5 g/cm³ and competing composition explanations. Both use TESS and radial velocities. | Strong reserve. The earlier paper also revises the outer system's architecture, adding scope beyond the focal calculation. |
| K2-18 b | Cloutier et al. (2017, 2019) reports masses 8.0 ± 1.9 and 8.63 ± 1.35 Earth masses. The later paper investigates a disputed signal associated with planet c. | Reserve. The stronger change story concerns another planet's detection rather than b's composition. |

Primary sources: [LHS 1140 archive](https://exoplanetarchive.ipac.caltech.edu/overview/LHS%201140%20b),
[Lacedelli](https://arxiv.org/abs/2009.02332),
[Brinkman](https://arxiv.org/abs/2210.06665),
[Cloutier 2017](https://arxiv.org/abs/1707.04292),
[Cloutier 2019](https://arxiv.org/abs/1810.04731).
These are bounded historical comparisons, not surveys of all later work.
Full product-access and redistribution checks were not performed for the reserves.

## What differs for LHS 1140 b

These are published estimates, not Malleus outputs or calculations performed here.
NASA presents them under separate reference columns:

| Quantity | Lillo-Box 2020, joint fit | Cadieux 2024, joint fit |
| --- | --- | --- |
| Mass, Earth masses | 6.38, +0.46 / -0.44 | 5.60 ± 0.19 |
| Radius, Earth radii | 1.635 ± 0.046 | 1.730 ± 0.025 |
| Bulk density, g/cm³ | 8.04, +0.84 / -0.80 | 5.9 ± 0.3 |

[NASA's reference-specific values](https://exoplanetarchive.ipac.caltech.edu/overview/LHS%201140%20b).
Do not mix columns and call the result a published solution. Recomputing density
from central mass and radius estimates need not exactly reproduce a reported
posterior median. Propagated uncertainty requires a justified method.

The earlier paper interprets b as rocky, possibly iron-enriched. Its section 6
and joint-fit table supply the coherent set above. The downloaded v1 PDF labels
that table B.3 on PDF page 21. The earlier HTML inspection called it Table 5;
that rendering's label must not be used as a PDF locator. The abstract's mass is
not that joint-fit estimate;
the prose radius uncertainty also differs from the table. Preserve fit and
source-version identity instead of silently repairing discrepancies.
[Lillo-Box full text](https://ar5iv.labs.arxiv.org/html/2010.06928).

The later paper reprocesses the same 117 ESPRESSO spectra and combines additional
transits. Its interpretation allows a small gas envelope or a water-rich
interior. Sections II.3, II.4 and III explain method/data changes; Table D1 gives
the joint solution; section IV discusses alternatives. An ocean is not established.
[Cadieux full text](https://ar5iv.labs.arxiv.org/html/2310.15490).

This is suitable for testing what justifies changing an accepted interpretation.
It does not establish that one isolated method caused the entire difference,
or that a later publication should automatically replace an older claim.

## Proposed input packet

| Material | Located source | Check before freezing |
| --- | --- | --- |
| Earlier paper | Lillo-Box et al., A&A 642 A121 (2020); arXiv 2010.06928v1. | Select publisher or named preprint bytes; bind locators to that edition. |
| Later paper | Cadieux et al., ApJL 960 L3 (2024); arXiv 2310.15490v2, posted December 2023. | Select bytes; distinguish journal year from preprint date. |
| Parameter rows | NASA solutions attributed to these references. | Retrieve exact rows and column definitions. The live overview is not a frozen export. |
| Observation product | TIC 92226327; TESS Sectors 3/30, two-minute PDCSAP light curves, identified in Cadieux II.3. | Resolve a product identifier, processing version and exact bytes. |
| Alternative measurement product | Machine-readable ESPRESSO velocity table, Cadieux Appendix B. | Resolve the supplementary file; a rendered sample is not the full table. |

The later study reports reprocessing Sector 3 with SPOC 5.0.20. Do not label a
current light curve as the earlier study's exact input without verifying its
processing history. [Cadieux II.3](https://ar5iv.labs.arxiv.org/html/2310.15490).

The study-to-observation connection is documented. Actual product-byte access
remains unchecked: direct archive-directory requests were not retrievable with
the web tool. This does not establish that the data are unavailable.

If historical bytes cannot be recovered, present the author with either a
clearly labelled later product used only as linked evidence or the published
measurement-table route. Do not silently substitute one. The first experiment
will not refit spectra or transits; it tests source connection and justified
use of published estimates, not scientific reproduction from raw observations.

## Access and evidence safeguards

Both papers have accessible arXiv text. Cadieux's record links CC BY 4.0;
Lillo-Box's links the arXiv non-exclusive distribution licence. Neither PDF will
be committed here. Public acquisition instructions and any redistributed source
content need separate review.
[Cadieux record](https://arxiv.org/abs/2310.15490),
[Lillo-Box record](https://arxiv.org/abs/2010.06928).

NASA also flags a stellar-luminosity typo in the older paper. Record relevant
source discrepancies; do not turn the demonstration into repairing every field.
[Archive notes](https://exoplanetarchive.ipac.caltech.edu/overview/LHS%201140%20b).

Before freeze, mechanically verify identifier/title/author/version agreement
and numeric locator/object/fit/unit agreement. Test mismatched identities and
cross-fit binding in the preparation code. A correctly shaped URL is not proof
of the correct paper. No new validator has been implemented in this investigation.

## Selection and next boundary

LHS 1140 b is selected for milestone 2 preparation. TOI-561 b and K2-18 b remain
in reserve. [source-packet.md](source-packet.md) supersedes the access status in
this earlier comparison. Model execution, another experiment's Core pin and
manuscript claims remain outside this approval.
