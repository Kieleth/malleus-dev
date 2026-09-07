"""Two closed typed capabilities reusing existing Assent control semantics.

These functions compute over supplied records. They do not authenticate history
or attest that a producer ran. No handler import, dynamic callable or I/O.
"""

from dataclasses import asdict

from malleus.control import evaluate_authorization_policy, evaluate_epistemic_policy


COMMON = {"proposal_id", "proposal_content_hash", "base_acceptance_head"}
AUTHORITY = {
    "action_proposal_id",
    "action_content_hash",
    "evaluated_actor_id",
    "authority_policy_id",
    "authority_policy_hash",
}
CAPABILITIES = {
    "ASSENT_EPISTEMIC_CONTROL_V1": (evaluate_epistemic_policy, COMMON),
    "ASSENT_AUTHORIZATION_CONTROL_V1": (
        evaluate_authorization_policy,
        COMMON | AUTHORITY,
    ),
}


def require_coverage(required, outputs, context):
    """Require one exact output per required monitor and all context bindings."""
    if set(context) != {"recipe", "monitors", "bindings"}:
        raise ValueError("closed control context required")
    if context["recipe"] not in CAPABILITIES:
        raise ValueError("unknown typed control recipe")
    fields = CAPABILITIES[context["recipe"]][1]
    if set(context["bindings"]) != fields:
        raise ValueError("complete exact control bindings required")
    if not required or any(
        set(r) != {"monitor_id", "monitor_record_hash"} for r in required
    ):
        raise ValueError("nonempty exact required monitor pairs required")
    ids = [r["monitor_id"] for r in required]
    if any(type(i) is not str or not i.strip() for i in ids) or ids != sorted(set(ids)):
        raise ValueError("required monitor IDs must be canonical and unique")
    monitors = {m["id"]: m for m in context["monitors"]}
    by_monitor = {a["monitor_id"]: a for a in outputs}
    if (
        len(monitors) != len(context["monitors"])
        or len(by_monitor) != len(outputs)
        or set(monitors) != set(ids)
        or set(by_monitor) != set(ids)
        or len({a["id"] for a in outputs}) != len(outputs)
    ):
        raise ValueError("one distinct output and specification per required monitor")
    for requirement in required:
        monitor, output = (
            monitors[requirement["monitor_id"]],
            by_monitor[requirement["monitor_id"]],
        )
        if monitor["content_hash"] != requirement["monitor_record_hash"]:
            raise ValueError("required monitor record hash differs")
        for field, expected in {
            **context["bindings"],
            "monitor_hash": monitor["content_hash"],
            "monitor_version": monitor["artifact_version"],
            "assessment_kind": monitor["assessment_kind"],
        }.items():
            if output[field] != expected:
                raise ValueError(f"check binding differs: {field}")


def select_control(policy, outputs, context):
    """Recompute the existing policy result, with no supplied verdict shortcut."""
    required = [
        {"monitor_id": i, "monitor_record_hash": h}
        for i, h in zip(
            policy["required_monitor_ids"],
            policy["required_monitor_record_hashes"],
            strict=True,
        )
    ]
    require_coverage(required, outputs, context)
    evaluator, fields = CAPABILITIES[context["recipe"]]
    bindings = context["bindings"]
    arguments = {name: bindings[name] for name in COMMON}
    if fields == COMMON | AUTHORITY:
        if (
            bindings["authority_policy_id"] != policy["id"]
            or bindings["authority_policy_hash"] != policy["content_hash"]
        ):
            raise ValueError("context authority policy differs from selected policy")
        arguments.update(
            action_id=bindings["action_proposal_id"],
            action_content_hash=bindings["action_content_hash"],
            evaluated_actor_id=bindings["evaluated_actor_id"],
        )
    return asdict(
        evaluator(
            policy, {m["id"]: m for m in context["monitors"]}, outputs, **arguments
        )
    )
