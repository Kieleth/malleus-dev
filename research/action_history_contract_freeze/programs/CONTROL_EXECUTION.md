# Finite control execution

This instantiates the already approved REQUIRE_COVERAGE and SELECT_CONTROL
meanings. It adds no instruction, evaluator language, callback or new policy.
The two typed capabilities select the existing `malleus.control` epistemic
and authorization evaluators, including their existing evaluation-hash recipes.
They are reference implementations, not a portability claim.

Authorization outcome mapping, precedence and trigger membership now come from
the fixed packaged `authorization-control-v1.json` resource. The shared evaluator
uses a generic lookup/selection interpreter for these rules. Policy and
evaluation hashes remain unchanged; the default resource is pinned, not a
caller-selectable rule override. Record and history validation remain separate.
The [implementation record](../../../handover/2026-09-08-authorization-rule-artifact.md)
states the exact identity, compatibility proof and remaining Python boundary.

The [authorization answer table](authorization_conformance_cases.json) records
independently written verdict and trigger expectations for all nine pairs of
two authority outcomes. Its test runs both control entry points, checks input
order independence and typed refusals, and injects wrong shared rules to prove
that agreement alone cannot satisfy the table. The table is test evidence, not
an executable policy or a public wire. The
[bounded comparison](../../../handover/2026-09-08-authorization-conformance.md)
separates this control check from full history admission and Assent replacement.

Context is exactly `{recipe, monitors, bindings}`. `recipe` is
`ASSENT_EPISTEMIC_CONTROL_V1` or `ASSENT_AUTHORIZATION_CONTROL_V1`, explicitly
required by the program. `monitors` is the complete finite list of resolved
MonitorSpecificationArtifact records. `bindings` contains proposal_id,
proposal_content_hash and base_acceptance_head. Authorization additionally
requires action_proposal_id, action_content_hash, evaluated_actor_id,
authority_policy_id and authority_policy_hash. No extra binding is ignored.

REQUIRE_COVERAGE consumes the required ordered list of
`{monitor_id, monitor_record_hash}` pairs. It matches exactly one output to
each pair and checks monitor version/kind, proposal, action, actor, policy and
head bindings. It does not decide the verdict. SELECT_CONTROL independently
derives that required list from the supplied policy and repeats coverage before
calling the selected existing evaluator. Its result contains verdict,
assessment_ids, triggered_assessment_ids and evaluation_hash. Input order
cannot change policy order. Output values are not accepted from the caller.

Full record introduction, record/source hashes, actual producer execution and
applied-prefix authentication remain separate owning-history obligations. A
standalone control invocation computes over supplied records, not authenticated
checks. The later retained execution bundle must bind the exact executor,
control implementation and policy bytes before admitting any result.

The optional ARTIFACT hash variant remains refused unless its specific semantic
projection is instantiated. The selected registration programs already use
explicit field-bound preimages and HASH VALUE, so no generic artifact mapper
is needed for this milestone.
