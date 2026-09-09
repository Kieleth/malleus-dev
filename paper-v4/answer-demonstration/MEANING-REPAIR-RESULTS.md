# Source-context repair: one proposed batch withheld

The graph has not improved in this attempt. Independent model-assisted source
review withheld Sol's three-record amendment before any retention or admission.
The original history, graph and all thirty existing answers still reproduce.
Human ratification is pending. No corrected proposal or passing subset was made.

## What the proposal got right and wrong

Sol proposed adding the modeled material and its CO2-content condition to three
existing quantities. The numbers and units remained exact. But it copied one
description, calling the quantity a model result, onto all three records.

| Quantity | Source-review finding |
| --- | --- |
| Approximately 0.7 GPa pressure | The added modeled-melt and composition context is supported. |
| Approximately 25 km depth | The added context is supported; this modeled depth remains distinct from observed earthquake depths. |
| 1250 °C temperature | The source gives a saturation condition. It does not establish that the model calculated the temperature itself. The new output claim is unresolved. |

The source passage is selected-reading `page:5:block:006`. It also discusses
measured seafloor basalts, which must not be confused with ascending modeled melt.
The separate Methods calculation at `page:8:block:007` uses 1200 °C and a different
cited model. Sol correctly kept that calculation separate. Neither passage proves
that the 1250 °C value was an adopted input; the review did not make that opposite
inference either.

## Located cause, not a guess about model ability

The submitted builder defines one `DESCRIPTION` constant and applies it to depth,
pressure and temperature. That is the exact point where potentially different
quantity roles receive the same output claim. The incorrect implication exists
in the submitted JSON, before Core sees it. Numeric preservation and an exact
source locator cannot prevent this kind of meaning change.

The original temperature record already says MODELLED and CALCULATED. Those
fields were frozen by this experiment. The amendment repeated and strengthened
their unresolved interpretation rather than identifying it as a limitation.
The prompt explicitly requested input-versus-result checks, but the report did
not account for this distinction. Full input delivery is verified for both
sessions, so missing delivery is not an explanation here. We do not know why
the model chose this interpretation.

Core's public adapter and population compiler accepted the structure. The
paper-owned source-review gate then withheld it. A real-executor regression test
confirms that this decision refuses before creating an attempt directory. No new
ledger was created. No Core source-truth capability or Core regression is claimed.

## Why this did not complete the wider repair

The packet permitted changes across 76 targets. Sol selected three and reported
73 as NO_CHANGE. Its builder generates generic property inventories for those
unchanged records. All 37 claims remain unchanged, with their existing useful
causal/comparison links preserved and much proposition detail still source-only.

The independent review instead accounts for all 76 targets and 119 report
contexts. It separates omissions from inherited defects, including local subjects
incorrectly attached to background/global claims, missing melt-processing stages,
and calibration ratios confused with their application material. A complete list
of IDs and present fields is not a complete source reconciliation. The current
task required an account for every target, not a justified repair or a specific
obstacle for every acknowledged gap. We must not call the submitted partial
account completion of the broader objective.

## Next correction, proposed only

Revisit the temperature's meaning before another wording-only repair. The frozen
schema already makes `determination` and `assertion_modality` optional; it does
not force the unresolved classifications. A narrow author decision could reopen
those two fields on this temperature only, while keeping all values, units,
other records and the reader fixed. The model must not guess an input role in
place of an unsupported output role.

If approved, return the exact diagnostic once to Sol, retain a new whole
candidate, and use the same independent source reviewer. This would be a declared
semantic correction, not a fresh blind replicate. No such return is authorized
or launched. The remaining claim/context repair remains separate unfinished work.

## Evidence

Private run: `private/paper-v4-answer-demonstration/sol-meaning-repair-01`.
It retains the frozen inputs, candidate, report, builder, source-review packet,
review, decision and outcome. See the [full source review](../../private/paper-v4-answer-demonstration/sol-meaning-repair-01/source-review-01/review.md).
Exact identities and settings are recorded in paper-ledger.md, E-0334/E-0335.
Producer: fresh Sol/ultra, 92 verified input frames. Reviewer: fresh Astra/xhigh,
80 verified frames. The reviewer's initial count of 82 was an arithmetic error,
corrected without changing any delivered frame or source judgment.

Validation: full answer-demonstration selection passed 609 tests and two subtests
before the final actual-refusal regression was added. The later focused staging,
audit, scope and actual-refusal selection passes 48 tests. The new regression
also reproduces the original thirty answers and checks unchanged history, graph
and receipt. These are execution safeguards, not an automated source assessment
or a new answer score. Core, manuscript, dependencies and shared refs are unchanged.
