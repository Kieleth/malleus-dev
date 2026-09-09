# Separate faithful evidence from sufficient evidence

E-0272 update: Luis approved the recommended separation and the bounded repair
sequence. It applies prospectively only. E-0271's pending selection is superseded;
the historical proposal below and frozen reviews remain evidence. The executable
cut is specified in QUALIFICATION-PLAN.md. No historical grades are rewritten.

E-0271. Decision proposal, not a changed evaluation rule. Luis acknowledged the
sequence: clarify this boundary, then repair missing observation qualifications.
The current graph, frozen criteria and historical reviews remain unchanged.

## Evidence behind the decision

The earlier argument review judged the asserted quantities and relations
source-supported, while recording missing context under coverage. The scoped
review instead judged some whole rows PARTIAL because qualifications were absent,
then withheld additional coverage credits through that support judgment.
The second packet also uses the corrected endpoint-context projection, so this
is not an identical-packet repeat. Neither set of historical grades is replaced.

The scoped review agrees that both new SUPPORTS connections represent the
authors' argument. The seismic observation has its RC2 subject and approximate
depth range, but no determination property. Its original assertion explicitly
retains MEASURED without mapping it into that property. Core and the reader did
not discard an authored determination. This is an incomplete representation.

## Recommended prospective rule

Assess faithfulness against what the representation actually claims under its
declared ontology. Assess sufficiency against the requirements fixed for the
question. A missing field does not by itself assert a false value, a universal
scope or certainty. Conversely, an omission that changes the represented meaning
can be a faithfulness defect. The reviewer must identify that unsupported claim
or implication, not merely list additional context that could have been returned.

| Representation | Faithfulness issue | Coverage issue |
| --- | --- | --- |
| Correct depth and site, determination absent | No incorrect determination asserted; inspect other claims separately | Required evidential status missing |
| An estimate explicitly labelled a direct measurement | Status contradicts the source | Cannot fulfil the status requirement faithfully |
| A modelled saturation depth presented as an earthquake observation | Quantity meaning and status contradict the source | Does not supply observed seismic evidence |
| Supported evidence link, endpoint missing a requested qualification | Judge the asserted link and endpoint claims separately | Link exists; qualified evidence requirement remains incomplete |

This preserves the three author-endorsed promises in ../acceptance-promises.md.
It is not permission to credit unsupported fields or import absent content from
source into an answer. Any change to the current whole-witness coverage rule
must be explicit and prospective, with mechanical evidence-binding tests; no
automatic semantic scorer is proposed.

The alternative is to retain the newer review's holistic gate: a whole row
must carry every declared qualification before any of its semantics receives
credit. That requires an explicit qualification checklist too. The recommendation
above keeps the cause of failure more legible and matches the existing separation
of faithfulness and sufficiency. The author selects the rule.

## Smallest subsequent graph repair

The current export has exactly one relation incident on
observation:rc2-deep-depth: its new SUPPORTS relation to claim:co2-degassing.
The fixed ontology already permits determination. No new ontology or Core
capability is indicated by this inspection.

1. Freeze the chosen rule and the exact qualification requirements before a new
   producer runs. Clarify any required axial or observation-window scope rather
   than adding requirements after seeing an answer.
2. In TDD, prepare an atomic same-type replacement of the observation and a
   replacement of its incident relation pointing to the new observation ID.
   Preserve existing quantities, units, approximation, subject and predicate.
   Preserve the old versions in history and every unrelated current record.
   Retiring an observation must not leave an active dangling relation.
3. A fresh producer must derive any added qualification from retained source
   evidence, not receive an evaluator-authored replacement or expected enum.
   Reuse the existing public admission/replay path and corrected reader.
4. Reproduce, trace and assess before and after under the same chosen rule.
   Adding determination alone does not guarantee full coverage: unresolved
   source scope remains visible, never silently waived.

This is a proposal for two versioned replacements, not two new independent
observations. No population bytes, test implementation, model dispatch, Core
request, manuscript edit, dependency or Git mutation is part of this note.

Evidence: SCOPED-LINKS-RESULTS.md; the two retained review.md files under
sol-argument-01 and sol-argument-scope-01; the latter run's baseline capture,
current export, ontology closure and query result. Core remains 160878c.
