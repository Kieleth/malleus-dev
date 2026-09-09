"""Follow-up staging must not mix fixed ontology or query bytes with live state."""

from hashlib import sha256

import pytest


def identity(value):
    return "sha256:" + sha256(value).hexdigest()


def test_unchanged_input_bytes_are_required_before_staging():
    from followup import checked_bytes

    assert checked_bytes(b"fixed", identity(b"fixed"), "ontology") == b"fixed"
    with pytest.raises(ValueError, match="ontology"):
        checked_bytes(b"changed", identity(b"fixed"), "ontology")


def test_material_check_refuses_drift_and_path_escape(tmp_path):
    from followup import verify_materials

    material = tmp_path / "input.txt"
    material.write_bytes(b"fixed")
    entries = [{"path": "input.txt", "sha256": identity(b"fixed")}]
    verify_materials(tmp_path, entries)
    material.write_bytes(b"changed")
    with pytest.raises(ValueError, match="input.txt"):
        verify_materials(tmp_path, entries)
    with pytest.raises(ValueError, match="escapes"):
        verify_materials(tmp_path, [{"path": "../outside", "sha256": identity(b"")}])


def test_materials_cannot_omit_required_identity(tmp_path):
    from followup import verify_materials

    (tmp_path / "input.txt").write_bytes(b"fixed")
    with pytest.raises(KeyError):
        verify_materials(tmp_path, [{"path": "input.txt"}])


def test_fixed_population_condition_requires_known_ontology_and_safe_identity():
    from followup import population_condition

    base, run_id = population_condition("run-21", "overnight-sol-01")
    assert base.name == "run-21" and run_id == "overnight-sol-01"
    for base_run, identity in (
        ("../run-21", "overnight-sol-01"),
        ("run-22", "overnight-sol-01"),
        ("run-21", "../other"),
        ("run-21", ""),
    ):
        with pytest.raises(ValueError):
            population_condition(base_run, identity)
