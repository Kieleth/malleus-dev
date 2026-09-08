"""The accepted nonblank census is enforced at actual prerequisite admission."""

from copy import deepcopy
import json

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs.lifecycle.test_prerequisites import (
    HERE,
    KINDS,
    packet,
    specimen,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    api,
    append,
    draft,
    prerequisites,
    setup,
)


CENSUS = json.loads((HERE / "registration-nonblank-gap.json").read_bytes())[
    "affected_fields"
]
CASES = [(name, field) for name, kind in KINDS.items() for field in CENSUS[kind]]


@pytest.fixture(scope="module")
def registered_prefix(tmp_path_factory):
    history, _ = setup(tmp_path_factory.mktemp("registration-nonblank"))
    prerequisites(history)
    return history.path.read_bytes()


def candidate(history, name):
    if name == "grant":
        value = specimen(name)
    else:
        identifier = "monitor:epistemic:0" if name == "monitor" else "policy:" + name
        value = history.replay().protocol_replay.data["records"][identifier]["record"]
    value["id"] = "candidate:" + name
    value["generation_event_id"] = "event:candidate:" + name
    return value


def event(name, value):
    preimage = None
    if name != "grant":
        mapping = packet(name)["semantic_preimage"]
        preimage = deepcopy(mapping["template"])
        for binding in mapping["bindings"]:
            source = value
            for part in binding["record_path"]:
                source = source[part]
            target = preimage
            for part in binding["preimage_path"][:-1]:
                target = target[part]
            target[binding["preimage_path"][-1]] = source
        # Deliberately do not call the existing semantic digest helper: it
        # already refuses blanks. The owning program must check these values.
        value["artifact_hash"] = content_digest(preimage)
    value["content_hash"] = record_hash(KINDS[name], value)
    return draft(KINDS[name], value, preimage=preimage)


def reopen(tmp_path, content):
    path = tmp_path / "history.jsonl"
    path.write_bytes(content)
    return KnowledgeChangeHistory.reopen(path)


@pytest.mark.parametrize("name,field", CASES)
def test_each_nonblank_census_field_refuses_atomically_at_real_admission(
    tmp_path, registered_prefix, name, field
):
    history = reopen(tmp_path, registered_prefix)
    value = candidate(history, name)
    if field.endswith("[]"):
        value[field[:-2]][0] = " \t\u2003"
    else:
        value[field] = " \t\u2003"
    before = history.path.read_bytes()
    before_replay = history.replay()
    with pytest.raises(api().ProtocolProgramRefusal, match="INPUT_SHAPE.*nonblank"):
        append(history, name, event(name, value))
    assert history.path.read_bytes() == before
    assert (
        KnowledgeChangeHistory.reopen(history.path).replay().receipt
        == before_replay.receipt
    )


@pytest.mark.parametrize("name", KINDS)
def test_nonblank_registration_preserves_supplied_nonblank_values_on_reopen(
    tmp_path, registered_prefix, name
):
    history = reopen(tmp_path, registered_prefix)
    value = candidate(history, name)
    field = "scope_record_id" if name == "grant" else "artifact_version"
    value[field] = " value with surrounding space "
    if name == "grant":
        value["permitted_action_types"] = [" AMEND "]
    append(history, name, event(name, value))
    replay = KnowledgeChangeHistory.reopen(history.path).replay()
    assert replay.protocol_replay.data["records"][value["id"]]["record"] == value


def test_census_has_exact_accepted_field_closure():
    assert CENSUS == {
        "AuthorityGrant": ["scope_record_id", "permitted_action_types[]"],
        "MonitorSpecificationArtifact": [
            "id",
            "artifact_version",
            "input_artifact_ids[]",
        ],
        "EpistemicPolicyArtifact": [
            "id",
            "artifact_version",
            "ruleset_id",
            "required_monitor_ids[]",
        ],
        "AuthorizationPolicyArtifact": [
            "id",
            "artifact_version",
            "required_monitor_ids[]",
        ],
    }
