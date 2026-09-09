# Independent source-scope probe

E-0250 diagnostic, three existing records. Read-only model-assisted assessment
by /root/source_scope_probe. No prior reviews, manuscript, questions, calibration
outputs or network sources supplied. Human ratification is pending. This does
not replace a frozen thirty-question evaluation.

The reviewer resolved retained traces, checked the selected-reading digest and
read the accepted ontology/import definitions. The census ontology path came
from the accepted manifest and was verified as
sha256:96b9b75ccf7a935b0d9b89f4aa5ae13d0f9c530fc4276fc18ccc0e94f22ec8ff.
The first dispatch incorrectly assumed an accepted/ontology.yaml path. The
reviewer stopped at that missing input; the correct accepted attempt was then
supplied without changing any source or record. The diagnostic fixture now
checks the manifest-selected definition path and digest.

## Census quality claim: correct statement, unsupported subject narrowing

In sol-census-01, claim:location-quality preserves the source's approximately
78% location-quality statement, the threshold of at least two criteria, its
STATED modality and an appropriate descriptive claim kind. Its derivation is
assertion:location-quality, page:7:block:008.

Its subject is earthquakes:deep-mantle, explicitly selected as earthquakes at
10–20 km mantle depth. That set's own description is source-supported. But the
quality passage discusses located earthquakes more broadly; neither that block
nor the inspected context establishes the percentage for this deep subset.
Generic earthquakes/events tags do not remove the set's explicit selection.

The independent finding is an unsupported scope assignment. This is not proof
that the subset's actual percentage differs. The exact percentage denominator
cannot be reconstructed independently without the referenced supplementary
table, outside the selected reading. Relevant context: page:7:block:007–008,
page:2:block:003; deep-set evidence includes page:1:block:001.

This record was not returned by the earlier thirty-query view. Its error shows
why checking only returned witnesses cannot certify the entire populated graph.
No capture repair or historical label change was performed.

## Segment CO2 observations: supported values, incomplete stage representation

In followup-sol-01, obs:rc2-melt-co2 and obs:rc3-melt-co2 retain respectively
0.4–3.0 and 0.04–0.7 wt%, CO2(calculated), MassFraction, CALCULATED and DERIVED.
The independent assessment supports those quantities and their association
with RC2 and RC3. The cited source is assertion:segment-co2-comparison,
page:5:block:005, with context in page:5:block:004 and page:8:block:007.

That context identifies primary-melt estimates after fractional-crystallization
correction. RC3's aggregate range spans the two proxy-derived estimates in the
methods. Neither record identifies the proxies separately or carries an explicit
primary-melt stage. Their graph subjects identify ridge segments, not material
populations. This is supported geographical association with underqualified
material/stage scope, not evidence that the numbers themselves are wrong.

Absent uncertainty/value_qualification fields do not assert exactness under
the accepted metrology definitions. Assumptions and uncertainty remain incompletely
represented. Source context distinguishes the pre-eruptive ranges in
page:8:block:006; relabelling these stored values as pre-eruptive or directly
measured concentrations would be unsupported.

The useful distinction is concrete: lexical selection hides existing values;
source context resolves their meaning; the graph still lacks some of that
meaning. A wider reader alone cannot claim that the missing stage is now stored.

## Completed calibration b: negative dispositions and retained scope

A second read-only probe by the same diagnostic agent examined calibration b
after submission. It is separate from its fresh thirty-question reviewer and
was not supplied to that reviewer. No population or formal label was changed.

The capture assigns page:5:block:005 and page:7:block:003 to nothing_assertable.
Neither has an assertion or typed gap. Both are scientific prose. The first
reports calculated segment CO2 ranges, comparative enrichment and a prior
partial-melting interpretation. The second reports relative RMS residual and
located-event performance across Vp/Vs settings, a reasonableness conclusion
and tomographic corroboration. Claim and quantitative types are available in
the fixed surface. These are unsupported negative dispositions, not proof of
an inability to represent any of their content.

Some numerical content is duplicated elsewhere. assertion:074-primary-estimates
on page:8:block:007 supports four primary-melt observations. Their exact IDs are
observation:rc2-primary-rb90, observation:rc2-primary-ba90,
observation:rc3-primary-rb90 and observation:rc3-primary-ba90. They retain,
respectively, 0.5–2.8, 0.4–3.0, 0.05–0.7 and 0.04–0.5 wt%, with ESTIMATED
determination. quantity_kind retains Rb90/Ba90 labels. Each subject is a MeltPhase
named primary melts with a segment RC2 or segment RC3 tag. Thus site, stage and
proxy basis are in graph properties, not only record IDs. There is no explicit
site relation or full Fo90 procedure. CALCULATED remains on the retained
assertion, not these exported observations.

The RC3 summary range is reconstructable as the envelope of its two estimates,
not a separately stored aggregate. The full volatile comparison and geological
interpretation remain absent. ratio:vp-vs, from assertion:061-vpvs on
page:7:block:002, stores the approximate Wadati estimate of 1.7. It does not
capture the following block's comparative test results or corroboration.

The producer session-log.md says all 129 negative blocks are navigation,
figure-only or reference material without separately admissible facts. These
two blocks contradict that universal explanation. Exact accounting of 57 asserted
plus 129 negative blocks establishes a partition of the 186 source IDs, not
semantic completeness or the correctness of any negative label.

The bounded next probe is an audit of negative dispositions, including duplicate
coverage versus absent content, followed only by explicitly authorized,
preservation-checked amendments. No internal model cause is established by
these artifacts, and no generic Core capability defect was found.
