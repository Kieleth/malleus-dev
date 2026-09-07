# Explicit absence of valid time

Luis approved this Core slice after the completed structured-source and locator
work. The evidence is the Shop source adapter's need to invent an ORDER_ONLY
token when no domain time was stated. This is not a paper or evaluator change.

## Bound contract before implementation

- Role: REFERENCE_IMPLEMENTATION of the optional compiler-enabled semantic
  history profile. The Shop case is a CONFORMANCE_FIXTURE; selecting domain
  time and replacement meaning remains an ADOPTER_CHOICE.
- Claim: an explicit `{"kind":"NONE_STATED","value":null}` survives plan
  compilation, change-set encoding, admission, reopen and record tracing.
  It asserts neither an instant nor relative domain order nor timeless truth.
  Ledger transaction order remains intact and means only recording order.
- Observation: admit the two retained supplier rows without supersession and
  recover both quantities, both source traces, and null valid-time values.
  An explicitly supplied same-kind replacement is separate from that case.
- Reuse: KnowledgeValidTime, the neutral PopulationPlan, the installed structural
  bundle, KnowledgeChangeHistory and the public record trace. One parser must
  serve the plan and change-set boundaries.
- Refusal: null or missing valid_time is not shorthand. NONE_STATED requires
  explicit null, INSTANT and ORDER_ONLY retain their required nonempty strings,
  and replacement across kinds continues to refuse before writes.
- Exclusions: no timestamp inference, new temporal query engine, cross-kind
  migration, changed document capture order, historical receipt rewrite, model
  comparison, package release, or Assent ValidTime change. Existing private-v0
  values keep their bytes and meaning; this is no stable-wire claim.

Pre-action check: local source/test/doc changes only; no server, endpoint or
dependency change. Required input stays explicit. Replace duplicated parsing
with one shared implementation, with hard tests at both consumers. No new
production mechanism or parallel ledger is introduced.

Evidence and final coordinates follow after RED and GREEN.
