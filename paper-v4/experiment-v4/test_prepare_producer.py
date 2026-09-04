from __future__ import annotations

import importlib.util
from pathlib import Path


SUBJECT_PATH = Path(__file__).with_name("prepare_producer.py")
SPEC = importlib.util.spec_from_file_location("paper_v4_prepare_producer", SUBJECT_PATH)
assert SPEC is not None and SPEC.loader is not None
SUBJECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SUBJECT)


def test_installer_output_is_reduced_to_the_declared_skill_file(tmp_path: Path) -> None:
    skill_root = tmp_path / ".codex" / "skills"
    allowed = skill_root / "malleus-acolyte" / "SKILL.md"
    extra_metadata = skill_root / "malleus-acolyte" / "agents" / "openai.yaml"
    extra_skill = skill_root / "malleus-recon" / "SKILL.md"
    for path in (allowed, extra_metadata, extra_skill):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(path.name, encoding="utf-8")

    SUBJECT._prune_skill_tree(skill_root, {allowed.resolve()})

    assert allowed.read_text(encoding="utf-8") == "SKILL.md"
    assert {path.resolve() for path in skill_root.rglob("*") if path.is_file()} == {
        allowed.resolve()
    }
