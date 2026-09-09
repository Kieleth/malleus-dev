# What the fresh graph actually says

2026-09-08. E-0329. Coordinator source assessment, not independent review.
Human ratification pending. No population, query, ontology or ledger change.

## Result

The fresh capture is not empty and its numbers have not disappeared. Its weak
point is the connection between a source passage and the meaning of a record.
Many claims identify where a statement came from without storing what it says.
Many quantities identify a value without enough of its scientific context.

This audit reads all eleven pages of the selected text layer, all 37
ScientificClaim records, and all 39 related quantitative records: 26
ScientificObservation, ten CountObservation and three RatioObservation. The last
three are not Observation subclasses. It follows declared references and all
formalization mappings, not just each record's preferred assertion locator.
There are 574 field-source mappings from 58 distinct assertions in this scope.
Those are accounting counts, not semantic coverage scores.

Four claims have cause/effect references that already express a coarse mechanism.
One has comparison subjects and a dimension but no comparison direction. The
other 32 have no statement, name, description or those proposition-specific
fields. Some have useful subjects and evidence links. They are not 32 false
claims, but their labels and citations do not reconstruct the source propositions.

I found no changed numerical value among the 39 records when compared with the
selected reading. That narrow finding does not certify their scope, attribution,
precision or completeness. The table below identifies those separate issues.
It also does not inventory all quantities omitted from the article.

## Corrections to the diagnosis

The deep-earthquake population already has an OBSERVED_AT relation to RC2 and a
LOCATED_BENEATH relation to the MAR axis. Its depth observations refer to that
population. Site and axis are therefore represented in the graph, although the
current answer view does not carry that traversal. They must not be generated
again and presented as capture gains. The explicit depth datum and the
observation-window limitation are different: the graph does not express them
on the observations or through a meaningful qualifying claim.

Five claims get fields from more than one source assertion. For example, the
preferred mechanism's cause/effect fields come from the abstract, while its
PREFERRED field comes from page 5. Looking only at its assertion_locator would
misdiagnose the preference as ungrounded. The audit helper now includes every
mapped assertion and tests this case.

The source distinguishes 19 deployed network instruments from 17 useful
instruments. This fresh graph contains the former number, without the network
role, but no count of 17. Do not carry the older repaired graph's separate useful
count into this run.

The source's proxy ratios are constants taken from cited work and used in the
authors' estimates. The graph marks them CALCULATED/ESTIMATED. Their numerical
values are correct, but the record does not distinguish an adopted input from a
result newly estimated in this study. This requires source assessment, not an
automatic enum substitution.

Two claim subjects need particular care. A general statement about earthquake
depth controls and a global ridge compilation both point to the population also
used for the local located catalogue. Generic aliases such as “earthquakes” do
not establish that identity. Adding a good sentence while retaining a misleading
subject would not complete their repair.

## All 37 claims

Locators abbreviate page:2:block:005 as p2b005. Record IDs below have the prefix
claim:. “Missing” describes meaning absent from graph fields or declared links,
not absent from the retained evidence. Assessments are not replacement values.

| Record | Source context | Represented and missing meaning |
| --- | --- | --- |
| axis-relocation | p2b005 | Axis subject and hypothetical interpretation retained. Proposed relocation from the OCC termination east under the faulted dome is missing. |
| co2-mechanism | p1b001, p5b002, p5b003 | Hypothesized cause/effect and source preference survive, with two SUPPORTS links. Volume-change reasoning and full contextual explanation do not. Already improved by the event reader. |
| cold-lithosphere | p3b001 | Hypothesis status, deep-earthquake subject, declined disposition and an incoming challenge survive. The cold, thick lithosphere proposition is missing. |
| competing | p10b047 | NEGATED/NEGATIVE_FINDING survives. No statement says whose competing interests are denied. |
| depth-factors | p1b004 | BACKGROUND category survives, but controls on maximum depth do not. Local-catalogue subject is not established for this general statement. |
| forced-depth-test | p7b010, p8b001 | Deep-earthquake subject survives. The test design, constrained-depth comparisons and result are missing from the claim. A separate count records the subset size. |
| geochemical-assumption | p5b004 | LIMITATION category survives. The mantle-source and absence-of-secondary-processes assumption is missing. |
| global-depth-compilation | p8b004 | CHARACTERIZATION category survives. Global coverage, maximum-depth selection and accompanying factors are missing. Subject conflates the compilation with a local population. |
| hot-magmatic-rc2 | p3b002 | RC2 subject and CHALLENGES edge survive. Magmatic accretion, hot mantle and the supporting observations are not stated. |
| hot-mantle | p3b001 | CALCULATED interpretation and challenge to the cold hypothesis survive. Separate temperature record exists, but no edge associates that result with this claim; site and depth conditions are missing there. |
| hydrothermal | p3b002 | Declined hypothetical status and incoming challenge survive. Rapid cooling by robust hydrothermal circulation is missing. |
| knowledge-limit | p1b003 | Melt subject and LIMITATION category survive. The unresolved migration process is missing. |
| lab-influence | p1b001 | LAB subject and hypothetical prediction survive. The proposed CO2 influence on subsolidus melt is missing. |
| lab-volatiles | p5b010, p6b001 | LAB subject and hypothetical interpretation survive. The combined CO2/water explanation and prior-work attribution are missing. |
| magtect | p4b002, p4b003, p5b001 | Declined hypothesis and two challenges survive. The magmatic-tectonic proposition and the source's comparison with other sites are missing. |
| melt-focus | p1b002 | Ascending-melt subject survives. Broad-source melting and focusing into a narrow ridge zone are missing. |
| melt-movement-rejected | p4b003, p5b001 | Negative-finding category and challenge to magmatic-tectonic activity survive. The authors' qualified rejection and its observations are missing. Preserve the authors' “suggest” status in any new statement. |
| migration-prediction | p5b009 | Melt subject and hypothetical prediction survive. Continuing degassing and predicted mantle seismicity during ascent are missing. |
| model-five-selection | p6b003, p6b004 | Model 5 subject and its separate method-use relation survive. Selection tradeoff and subsequent checks are missing. |
| no-detachment | p3b003, p4b001 | RC2 subject and challenge to the shear-zone account survive. Absence of evidence for detachment faults is not stated; do not turn that into universal absence. |
| no-eruption | p4b002, p4b003 | Axial-valley subject and challenge survive. Lack of current-eruption evidence and the observations supporting that judgment are missing. |
| no-over-20 | p5b007 | MEASURED/NEGATIVE_FINDING survives. No explicit threshold, population, site or observation-limited absence is expressed. |
| nonlinloc-method | p7b004 | NonLinLoc subject survives. Oct-tree search and preferred maximum-likelihood solution are missing. |
| ocean-crust-formation | p1b002 | Crust subject survives. Formation from mantle melt at spreading centres is missing. |
| pressure-trigger | p5b003 | Hypothesized degassing/earthquake event pair survives. The pressure mechanism and separation of cited triggering examples from the RC2 proposal are missing. |
| quality-ab | p2b003, p7b008 | METHOD_JUSTIFICATION survives. A/B selection for interpretation and its population are missing. |
| rc2-more-volatile | p5b004, p5b005, p8b007 | RC2, RC3 and comparison dimension survive. Direction and material stage are missing from the claim. Site-specific quantitative records exist separately. |
| schematic-interpretation | p7b011, p7b012 | Degassing/earthquake event pair survives. Caption-specific depth, seafloor datum and volume-change interpretation are missing. STATED marks a reported interpretation, not demonstrated causation. |
| shear-zone | p3b003, p4b001 | Declined hypothesis, population and incoming challenge survive. High-strain, hot-mylonite explanation and its geographic distinction are missing. |
| snapshot-limit | p2b004 | LIMITATION and citation survive. Brief recording window and variability over years are missing, with no semantic link to the observations. |
| spectrum | p5b008 | Measured interpretation and deep-earthquake subject survive. “Some” events and the missing high-frequency energy are not expressed. The adjacent long-period interpretation is only possible, not established. |
| spectrum-limit | p5b008 | LIMITATION survives. Not all events have low-frequency character and more events are needed; neither qualification is expressed. |
| station-corrections | p7b005 | METHOD_JUSTIFICATION survives. Iterative corrections, removal of 3-D effects and RMS criterion are missing. |
| supplementary | p11b001 | DATA_AVAILABILITY survives. What is available and where are missing. |
| tests-robust | p7b009, p7b010, p8b001 | Population and SUPPORTS link to the depth observation survive. What was varied and why the locations are considered robust are missing. |
| volume-trigger | p5b003 | Hypothesized degassing/earthquake event pair survives. Volume change, extensional stress and strain are collapsed into the same coarse pair used by the pressure claim. |
| vpvs-justification | p7b002, p7b003 | METHOD_JUSTIFICATION survives. Lowest RMS and largest located-event count are missing; the ratio exists separately without a link to this justification. |

## All 39 quantitative records

Record IDs have the prefix observation:. Values below describe existing graph
fields, not proposed population facts. A correct value can still be unsafe to use
without the qualifications listed. No blanket “fully captured” judgment follows.

| Record | Existing value and source | Context finding |
| --- | --- | --- |
| co2-ba-ratio | 81.3 ± 23; p8b006 | CO2/Ba roles and pre-eruptive subject exist. Adopted constant and cited-study origin are not explicit. |
| co2-rb-ratio | 991 ± 129; p8b006 | CO2/Rb roles and pre-eruptive subject exist. Same input/result distinction as the Ba ratio. |
| crust-thickness | Approx. 5.4 ± 0.3 km; p7b011, p2b006 | Crust subject exists, but generic. Caption's RC2 scope and body text's cited western-flank/age context are not represented. Do not silently identify the measurement with a new on-axis observation. |
| deep-16-19 | 16 to 19 km; p2b006 | Population links already supply RC2 and axis. Explicit depth datum and observation-window qualification are missing. |
| deep-depth | 10 to 20 km; p1b001, p2b004 | Population, measured status and SUPPORTS link exist. RC2/axis context is reachable. Explicit seafloor datum and short-window warning are missing. |
| depth-resolution | 10 to 20 km; p7b009 | Site is reachable through the population. Model-variation context, “most” and distinction from a separate new measurement are not expressed. |
| depth-uncertainty | Approx. 2.6 km; p7b009 | Deep-population subject exists. Uncertainty is recorded; the specific velocity-sensitivity comparison is not. |
| focal-new | 3; p8b003 | Count scope explicitly says new, well-constrained focal mechanisms. Method, criteria and study attribution are not linked. |
| focal-total | 6; p8b003 | Count scope explicitly combines new and previous solutions. No false claim that all six are new; constituent evidence is not linked. |
| forced-depth-subset | 45; p7b010 | Forced-depth-test role and deep-population subject exist. Cross-section and subset depth conditions are missing. |
| half-spreading | 16 mm/yr; p1b005 | Half-rate is explicit. Subject is the entire named MAR, without the source's local “here” scope. |
| horizontal-error | Approx. 2.8 km; p6b005, p7b001 | Correct earlier error, not final catalogue uncertainty. The stage and antecedent catalogue are missing. The separate later 2.1 km result is not captured. |
| identified-760 | 760; p6b002 | Explicit identification/SEISAN scope and identified population exist. Study acquisition context is not linked. |
| instrument-spacing | Approx. 30 km; p2b002 | OBS subject and campaign instrument-use relation exist elsewhere. Study year and full spatial coverage are missing. |
| located-514 | 514; p2b003 | Location role, Romanche RTI scope and population exist. Catalogue stages and acquisition context are not linked. |
| mantle-temperature | 1100 to 1200 °C; p3b001 | MODELLED status survives. Generic mantle subject loses RC2, depth range and cited thermal model. |
| mar-317 | 317; p7b007 | MAR location scope exists. Final-catalogue partition and complement are separate records, not linked as one partition. |
| obs-count | 19; p2b002, p6b002 | Instrument kind survives. Deployed network role does not. A campaign uses the instrument, but that alone does not assign this count to deployment. |
| primary-co2 | Approx. 0.4 to 3 wt%; p1b001, p5b004, p5b005 | Primary-melt subject, estimated status and SUPPORTS link exist. RC2 scope is not linked to this abstract synthesis. |
| quality-78 | Approx. 78%; p7b008 | Located-catalogue subject and at-least-two-criteria meaning survive. It is not the percentage of the deep subset. Criteria and category mapping are missing. |
| rc2-calculated-co2 | 0.4 to 3 wt%; p5b005 | RC2 and calculated status exist. Primary stage is not explicit; the paired RC3 record exists separately. |
| rc2-pre-ba | 0.7 to 4.6 wt%; p8b006 | RC2 and Ba proxy survive. Pre-eruptive stage is only in the ID/source, not a meaningful field or link. |
| rc2-pre-rb | 0.9 to 4.3 wt%; p8b006 | RC2 and Rb proxy survive. Same missing stage. |
| rc2-primary-ba90 | 0.4 to 3 wt%; p8b007 | RC2 and Ba90 proxy survive. Explicit primary-stage meaning and correction context are missing. |
| rc2-primary-rb90 | 0.5 to 2.8 wt%; p8b007 | RC2 and Rb90 proxy survive. Same missing stage and correction context. |
| rc3-calculated-co2 | 0.04 to 0.7 wt%; p5b005 | RC3 and calculated status exist. Stage and comparative role are missing. |
| rc3-pre-ba | 0.06 to 0.8 wt%; p8b006 | RC3 and Ba proxy survive. Pre-eruptive stage is missing. |
| rc3-pre-rb | 0.07 to 1 wt%; p8b006 | RC3 and Rb proxy survive. Pre-eruptive stage is missing. |
| rc3-primary-ba90 | 0.04 to 0.5 wt%; p8b007 | RC3 and Ba90 proxy survive. Explicit primary stage and correction context are missing. |
| rc3-primary-rb90 | 0.05 to 0.7 wt%; p8b007 | RC3 and Rb90 proxy survive. Same missing stage and correction context. |
| recording-duration | Approx. 21 days; p2b002 | SMARTIES subject exists. Campaign's USED_INSTRUMENT link exists but is not the frozen duration reader's OBSERVED_WITH relation. Year and continuous-recording meaning are absent. |
| relocated-276 | 276; p7b007 | “Well relocated” distinguishes this count from initial input. Replacement of initial locations in the final catalogue is not linked. |
| relocated-364 | 364; p7b006 | Count refers to the well-constrained relocation input/process. Do not confuse it with the later successful 276. Stage relation and selection criteria are missing. |
| romanche-197 | 197; p7b007 | Romanche TF scope exists. Final-catalogue partition is not explicit as a relation. |
| saturation-depth | Approx. 25 km; p5b006 | MODELLED status survives. Model condition, melt composition and association with the pressure/temperature records are missing. |
| saturation-pressure | Approx. 0.7 GPa; p5b006 | MODELLED status survives. Same missing joint conditions. This is not a measured pressure. |
| saturation-temperature | 1250 °C; p5b006 | MODELLED status survives. Same missing joint conditions and threshold on initial CO2 content. |
| vertical-error | Approx. 2.9 km; p6b005, p7b001 | Correct earlier error, but no stage or catalogue antecedent. Do not attach it to the later horizontal-error result by proximity. |
| vpvs | 1.7; p7b002, p7b003 | Numerator and denominator survive. The source's approximation, Wadati-method origin and use as an inversion setting are not explicit. |

## Why this happens at the current boundary

The ontology makes proposition text and contextual fields optional. Its claim
description asks for traceability, which the producer supplies. The adapter
checks exact source locations and field mappings. Admission checks the supplied
records. None of those contracts requires the statement's substantive content
to be recoverable from the graph.

That is an observed contract allowance and an observed producer choice, not a
proved causal account of the model's behavior. There is still one fresh sample.
Nothing in this audit establishes a Core persistence or query-API defect. It
does establish that the adopter's capture completion condition is too weak for
the useful graph we want.

The next capture requirement should be simple: for each represented assertion,
point to the graph fields and links that express its proposition, participants,
conditions and qualification, or declare what remains retained-only. A citation
is evidence for that account, not the account itself. A typed predicate with
resolved arguments can suffice; duplicate prose is not universally required.
Shared subjects need source-supported identity. Correct numbers do not authorize
merging populations, sites, stages or cited-study results.

## Bounded repair and comparison

The [repair specification](MEANING-REPAIR-PLAN.md) uses this inventory, not answer
values, to ask for one source-grounded amendment. It preserves the fresh run as a
first-pass result. Any gains belong to the amendment, not to regenerated capture.
Do not combine a reader repair with the population change: run the same frozen
event-query method before and after, then report any remaining reader limitation.

The 76 records are an audit scope, not a required replacement count. Replacing
all of them would also require retargeting nine existing relations. The typed
reverse-reference check finds no other dependants for that full set. A smaller
proposal must compute its own exact closure. New scientific relations, missing
catalogue values and funding records are separate work, not silently added here.

## Evidence and checks

Baseline is sol-fresh-comparison-01/attempt-02, Core 160878cf14c0d27b11a440e26688708e9b7a7e2b.
The exact retained inputs and existing identities are in EVENT-QUERY-RESULTS.md
and FRESH-COMPARISON-RESULTS.md. No additional identity system is introduced.
Read the graph at public/export-records.json, retained-capture.json under ledger/,
the producer's accepted population-surface.json and complete selected-reading.json.

meaning_audit.py is only an accounting aid. It keeps source passages separate
from graph fields, includes all mappings, and walks declared references instead
of interpreting strings as IDs. It assigns no adequacy label and writes no
population. Its tests discriminate dropped secondary evidence, missing paths,
duplicate identities, unresolved references, scalar/list mismatches, header
shadowing and transitive replacement dependencies. Source judgments in this
document remain mine, not output from those tests.
