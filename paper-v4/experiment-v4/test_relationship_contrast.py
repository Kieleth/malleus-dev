"""One instruction change, no producer dispatch or historical input mutation."""

import importlib.util
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def subject():
    path = Path(__file__).with_name("relationship_contrast.py")
    spec = importlib.util.spec_from_file_location("relationship_contrast", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def pair(subject):
    return subject.build_pair()


def test_exact_input_contrast_preserves_seven_other_inputs(subject, pair):
    old, new = pair
    assert len(old) == len(new) == 8
    assert {key for key in old if old[key] != new[key]} == {subject.SKILL}
    assert subject.OLD_BLOCK in old[subject.SKILL]
    assert subject.OLD_BLOCK not in new[subject.SKILL]
    assert b"do not require both endpoint" in new[subject.SKILL]
    assert b"Semantic completeness is not assessed." not in new[subject.SKILL]
    subject.check_pair(old, new)


@pytest.mark.parametrize("change", ["extra", "missing", "empty", "reading", "skill"])
def test_input_pollution_or_unrelated_drift_refuses(subject, pair, change):
    old, new = pair
    candidate = dict(new)
    if change == "extra":
        candidate["inputs/prior-ontology.yaml"] = b"forbidden"
    elif change == "missing":
        del candidate["inputs/research.yaml"]
    elif change == "empty":
        candidate["inputs/research.yaml"] = b""
    elif change == "reading":
        candidate["inputs/selected-reading.json"] += b" "
    else:
        candidate[subject.SKILL] += b"\nAn unrelated extra instruction.\n"
    with pytest.raises(ValueError):
        subject.check_pair(old, candidate)


@pytest.mark.parametrize("copies", [0, 2])
def test_missing_or_repeated_replacement_marker_refuses(subject, pair, copies):
    old, _ = pair
    modified = old[subject.SKILL].replace(subject.OLD_BLOCK, subject.OLD_BLOCK * copies)
    with pytest.raises(ValueError, match="exactly once"):
        subject.replace_guidance(modified)


def test_old_input_identity_cannot_drift_in_both_arms(subject, pair):
    old, new = map(dict, pair)
    for arm in (old, new):
        arm["inputs/selected-reading.json"] += b" "
    with pytest.raises(ValueError, match="historical input"):
        subject.check_pair(old, new)


def test_staged_pair_is_fresh_and_differs_only_in_guidance(
    subject, tmp_path, monkeypatch
):
    monkeypatch.setattr(subject, "PRIVATE", tmp_path)
    root = tmp_path / "contrast"
    subject.prepare_pair(root)
    import json

    loaded = []
    tasks = []
    for arm in ("a", "b"):
        run = root / arm
        manifest = json.loads((run / "producer-input-manifest.json").read_bytes())
        assert manifest["producer"]["model_id"] == "gpt-5.6-sol"
        assert manifest["producer"]["reasoning_effort"] == "ultra"
        assert not list((run / "producer/work").iterdir())
        files = {
            str(p.relative_to(run / "producer")): p.read_bytes()
            for p in (run / "producer").rglob("*")
            if p.is_file()
        }
        assert set(files) == {item["target"] for item in manifest["declared_inputs"]}
        for item in manifest["declared_inputs"]:
            assert subject.digest(files[item["target"]]) == item["sha256"]
        loaded.append(files)
        tasks.append((run / "task.md").read_text().replace(str(run), "<RUN>"))
    subject.check_pair(*loaded)
    assert tasks[0] == tasks[1]
    assert "accepted/population-surface.json" not in loaded[0]
    assert "input_delivery.py" in tasks[0]
    before = {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    with pytest.raises(ValueError, match="exists"):
        subject.prepare_pair(root)
    assert before == {str(p): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_staging_outside_private_refuses(subject, tmp_path, monkeypatch):
    monkeypatch.setattr(subject, "PRIVATE", tmp_path / "private")
    with pytest.raises(ValueError, match="private"):
        subject.prepare_pair(tmp_path / "elsewhere")
    assert not (tmp_path / "elsewhere").exists()
