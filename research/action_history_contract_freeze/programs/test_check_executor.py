"""Actual pure checks and existing output records, not applied ledger evidence."""

from copy import deepcopy
from importlib import import_module
import json

import pytest

from malleus.assent import make_record
from malleus.control import monitor_specification_digest
from malleus.ledger import canonical_json, content_digest, record_hash
from research.action_history_contract_freeze.programs.test_input_preflight import (
    specimen,
)
from research.action_history_contract_freeze.programs.test_input_carrier import (
    candidate,
    source_record,
)
from tests.contract_compiler.pareto.test_assent_contract_compatibility import _compile


def api():
    return import_module(
        "research.action_history_contract_freeze.programs.check_executor"
    )


@pytest.fixture(scope="module")
def compiled():
    return _compile()


def inputs(compiled, kind):
    engine = api().load_check_executor()
    args = specimen(compiled, kind)
    invocation, records, blobs = (
        args["invocation"],
        args["records"],
        args["retained_bytes"],
    )
    invocation["implementation"] = engine.implementation_reference
    static = []
    for role, content in [
        ("implementation", engine.implementation_bytes),
        ("definition", engine.definition_bytes),
    ]:
        value = source_record(candidate(), role, content)
        records[value["id"]] = {"record_type": "SourceArtifact", "record": value}
        blobs[value["id"]] = content
        static.append(value)
    static.sort(key=lambda r: r["id"])
    fields = dict(
        artifact_kind="MONITOR_SPECIFICATION",
        artifact_version="check-v1",
        monitor_schema_version="1",
        assessment_kind="TYPE" if kind == "TYPE" else "AUTHORITY",
        monitor_implementation_hash=invocation["implementation"]["bytes_sha256"],
        input_artifact_ids=[r["id"] for r in static],
        input_artifact_record_hashes=[r["content_hash"] for r in static],
    )
    fields["artifact_hash"] = monitor_specification_digest(
        schema_version=fields["monitor_schema_version"],
        monitor_id="monitor:actual",
        monitor_version=fields["artifact_version"],
        assessment_kind=fields["assessment_kind"],
        implementation_hash=fields["monitor_implementation_hash"],
        input_artifact_ids=fields["input_artifact_ids"],
        input_artifact_record_hashes=fields["input_artifact_record_hashes"],
    )
    monitor = make_record(
        "MonitorSpecificationArtifact",
        id="monitor:actual",
        event_id="event:monitor",
        generated_at="2026-09-07T00:00:00Z",
        actor_id="actor:registrar",
        role="registrar",
        source_record_ids=fields["input_artifact_ids"],
        **fields,
    )
    records[monitor["id"]] = {
        "record_type": "MonitorSpecificationArtifact",
        "record": monitor,
    }
    invocation["monitor"] = {
        "id": monitor["id"],
        "record_hash": monitor["content_hash"],
    }
    if kind == "DIRECT_GRANT":
        records["grant:shape"]["record"]["grantee_actor_id"] = "actor:executor"
        records["grant:shape"]["record"]["scope_record_id"] = "scope:local"
        records["grant:shape"]["record"]["content_hash"] = record_hash(
            "AuthorityGrant", records["grant:shape"]["record"]
        )
        next(r for r in invocation["inputs"] if r["role"] == "grant")["value"][
            "record_hash"
        ] = records["grant:shape"]["record"]["content_hash"]
    return engine, args


@pytest.mark.parametrize("kind", ["TYPE", "DIRECT_GRANT"])
def test_real_checks_produce_full_deterministic_assessments_without_caller_outcome(
    compiled, kind
):
    engine, args = inputs(compiled, kind)
    before = deepcopy(args)
    result = engine.execute(**args)
    assert result == engine.execute(**args)
    output = result.data["records"][0]
    assert output["record"]["assessment_outcome"] == "SATISFIED"
    assert output["record_type"] == (
        "TypeAssessment" if kind == "TYPE" else "AuthorityAssessment"
    )
    assert (
        compiled.view.validate_instance(output["record_type"], output["record"]) == []
    )
    assert output["record"]["content_hash"] == record_hash(
        output["record_type"], output["record"]
    )
    assert output["record"]["monitor_version"] == "check-v1"
    assert result.data["runtime_executed"] is True
    assert result.data["history_authenticated"] is False
    assert args == before


def rehash(args, role):
    reference = next(
        item for item in args["invocation"]["inputs"] if item["role"] == role
    )["value"]
    wrapper = args["records"][reference["id"]]
    value = wrapper["record"]
    value["content_hash"] = record_hash(wrapper["record_type"], value)
    reference["record_hash"] = value["content_hash"]


def replace_content(args, role, mutate):
    reference = next(
        item for item in args["invocation"]["inputs"] if item["role"] == role
    )["value"]
    value = json.loads(args["retained_bytes"][reference["id"]])
    mutate(value)
    content = canonical_json(value).encode()
    record = source_record(candidate(), role, content)
    args["records"][record["id"]] = {"record_type": "SourceArtifact", "record": record}
    args["retained_bytes"][record["id"]] = content
    reference["bytes_sha256"] = record["source_content_digest"]


@pytest.mark.parametrize(
    "fault,violated",
    [
        ("actor", "GRANTEE_MATCH"),
        ("type", "ACTION_TYPE_PERMITTED"),
        ("scope_id", "EXACT_SCOPE"),
        ("scope_hash", "EXACT_SCOPE"),
        ("grant_scope", "GRANT_SCOPE_BINDING"),
        ("delegation", "NO_SUBDELEGATION"),
        ("interval", "GRANT_INTERVAL"),
    ],
)
def test_direct_grant_computes_violations_instead_of_assuming_permission(
    compiled, fault, violated
):
    engine, args = inputs(compiled, "DIRECT_GRANT")
    grant = args["records"]["grant:shape"]["record"]
    if fault == "actor":
        grant["grantee_actor_id"] = "another:actor"
    elif fault == "type":
        grant["permitted_action_types"] = ["OTHER"]
    elif fault == "grant_scope":
        grant["scope_record_id"] = "another:scope"
    elif fault == "delegation":
        grant["may_subdelegate"] = True
    elif fault == "interval":
        grant["grant_valid_from"] = "2026-09-07T01:00:00Z"
    else:
        field = "id" if fault == "scope_id" else "record_hash"
        replace_content(
            args,
            "scope_association",
            lambda v: v["action_scope"].update({field: content_digest("another")}),
        )
    rehash(args, "grant")
    before = deepcopy(args)
    value = engine.execute(**args).data["records"][0]["record"]
    assert value["assessment_outcome"] == "VIOLATED"
    assert value["violated_policy_predicates"] == [violated]
    assert value["evaluated_authority_grant_hash"] == grant["content_hash"]
    assert value["evaluated_authority_grant_id"] == grant["id"]
    assert args == before


def test_type_check_evaluates_actual_compiled_record_shape(compiled):
    engine, args = inputs(compiled, "TYPE")
    args["records"]["action:shape"]["record"]["revision"] = True
    rehash(args, "action")
    value = engine.execute(**args).data["records"][0]["record"]
    assert value["assessment_outcome"] == "VIOLATED"
    assert value["reason_codes"] == ["ACTION_TYPE"]


@pytest.mark.parametrize(
    "fault",
    [
        "outcome",
        "implementation",
        "monitor",
        "static_bytes",
        "source_bytes",
        "duplicate_output_id",
    ],
)
def test_check_invocation_and_implementation_binding_refuse_before_output(
    compiled, fault
):
    engine, args = inputs(compiled, "TYPE")
    if fault == "outcome":
        args["invocation"]["outcome"] = "SATISFIED"
    elif fault in {"implementation", "monitor"}:
        key = "bytes_sha256" if fault == "implementation" else "record_hash"
        args["invocation"][fault][key] = content_digest("not-the-implementation")
    elif fault == "static_bytes":
        args["retained_bytes"]["input:implementation:shape-only"] += b" "
    elif fault == "source_bytes":
        args["retained_bytes"]["input:record_contract:shape-only"] += b" "
    else:
        args["invocation"]["output_ids"]["failure"] = args["invocation"]["output_ids"][
            "assessment"
        ]
    before = deepcopy(args)
    with pytest.raises(api().CheckRefusal):
        engine.execute(**args)
    assert args == before


@pytest.mark.parametrize("kind", ["TYPE", "DIRECT_GRANT"])
def test_actual_checker_failure_produces_paired_unknown_not_satisfied(
    compiled, monkeypatch, kind
):
    engine, args = inputs(compiled, kind)

    def unavailable(*args, **kwargs):
        raise RuntimeError("engine unavailable")

    monkeypatch.setattr(api(), "execute_program", unavailable)
    result = engine.execute(**args).data
    failure, assessment = result["records"]
    assert failure["record_type"] == "MonitorFailure"
    assert assessment["record_type"] == (
        "UnavailableAssessment" if kind == "TYPE" else "UnavailableAuthorityAssessment"
    )
    assert assessment["record"]["assessment_outcome"] == "UNKNOWN"
    assert assessment["record"]["monitor_failure_id"] == failure["record"]["id"]
    assert failure["record"]["id"] in assessment["record"]["source_record_ids"]
    assert failure["record"]["id"] not in failure["record"]["source_record_ids"]


def test_implementation_claim_must_name_this_loaded_implementation():
    engine = api().load_check_executor()
    with pytest.raises(api().CheckRefusal, match="implementation"):
        api().CheckExecutor(engine.definition_bytes, b"not executable producer bytes")


def test_implementation_capsule_retains_the_core_kernel_not_only_import_shims():
    from importlib import import_module
    from pathlib import Path

    capsule = json.loads(api().load_check_executor().implementation_bytes)
    for name in ("finite_program", "finite_executor", "finite_control"):
        module = import_module(f"malleus._contract_pipeline.{name}")
        assert capsule[f"core/{name}.py"] == Path(module.__file__).read_text()


def test_unknown_check_instruction_is_not_misreported_as_a_violated_predicate(compiled):
    engine, args = inputs(compiled, "TYPE")
    definition = json.loads(engine.definition_bytes)
    definition["rules"]["TYPE"][0]["steps"][0]["opcode"] = "UNSUPPORTED_CHECK"
    changed = api().CheckExecutor(
        canonical_json(definition).encode(), engine.implementation_bytes
    )
    source = source_record(candidate(), "definition", changed.definition_bytes)
    args["records"][source["id"]] = {"record_type": "SourceArtifact", "record": source}
    args["retained_bytes"][source["id"]] = changed.definition_bytes
    monitor = args["records"]["monitor:actual"]["record"]
    index = monitor["input_artifact_ids"].index(source["id"])
    monitor["input_artifact_record_hashes"][index] = source["content_hash"]
    monitor["artifact_hash"] = monitor_specification_digest(
        schema_version=monitor["monitor_schema_version"],
        monitor_id=monitor["id"],
        monitor_version=monitor["artifact_version"],
        assessment_kind=monitor["assessment_kind"],
        implementation_hash=monitor["monitor_implementation_hash"],
        input_artifact_ids=monitor["input_artifact_ids"],
        input_artifact_record_hashes=monitor["input_artifact_record_hashes"],
    )
    monitor["content_hash"] = record_hash("MonitorSpecificationArtifact", monitor)
    args["invocation"]["monitor"]["record_hash"] = monitor["content_hash"]
    with pytest.raises(api().CheckRefusal, match="instruction"):
        changed.execute(**args)


def test_pure_check_has_no_clock_source_store_writer_or_io(compiled, monkeypatch):
    engine, args = inputs(compiled, "TYPE")

    def forbidden(*args, **kwargs):
        raise AssertionError("unexpected I/O")

    monkeypatch.setattr("builtins.open", forbidden)
    monkeypatch.setattr("pathlib.Path.open", forbidden)
    assert (
        engine.execute(**args).data["records"][0]["record"]["assessment_outcome"]
        == "SATISFIED"
    )
