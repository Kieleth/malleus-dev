# Finite control execution

This instantiates the already approved REQUIRE_COVERAGE and SELECT_CONTROL
meanings. It adds no instruction, evaluator language, callback or new policy.
The two typed capabilities select the existing `malleus.control` epistemic
and authorization evaluators, including their existing evaluation-hash recipes.
They are reference implementations, not a portability claim.

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
