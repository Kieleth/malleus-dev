"""Reuse exact static definitions, never input validation or execution results."""

from copy import deepcopy
import json

import pytest

from malleus._contract_pipeline import finite_executor as runtime
from research.action_history_contract_freeze.programs.test_packet_validator import (
    HERE,
    specimen,
    profile,
)


def test_definition_reuse_is_bounded_and_keys_every_definition_byte(monkeypatch):
    check = runtime.validate_program_definition
    runtime._validated_definition.cache_clear()
    assert runtime._validated_definition.cache_info().maxsize == 32
    calls = []
    actual = runtime.validate_program

    def counted(program, **kwargs):
        calls.append(deepcopy((program, kwargs)))
        return actual(program, **kwargs)

    monkeypatch.setattr(runtime, "validate_program", counted)
    program = specimen()
    kwargs = {
        "profile": profile(),
        "instruction_schema": json.loads(
            (HERE.parent / "instructions.schema.json").read_bytes()
        ),
    }
    check(program, **kwargs)
    check(deepcopy(program), **deepcopy(kwargs))
    assert len(calls) == 1
    # Every source of static meaning participates, not only a declared name.
    program["name"] += "-other"
    check(program, **kwargs)
    kwargs["profile"]["capabilities"] = []
    check(program, **kwargs)
    kwargs["instruction_schema"]["title"] = "Different exact declaration"
    check(program, **kwargs)
    assert len(calls) == 4
    program["steps"][0]["value"]["name"] = "absent"
    for _ in range(2):
        with pytest.raises(runtime.PacketRefusal):
            check(program, **kwargs)
    assert len(calls) == 6
    runtime._validated_definition.cache_clear()
