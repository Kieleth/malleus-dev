"""What a producer may see, checked over every byte of its workspace.

The frame, which both consumers hold identically:

1. A closure check. Every file in the workspace is declared and every declared
   file is present. Nothing else runs until this passes.
2. Every ``DATA`` file's digest is one the run froze, so the evidence cannot be
   swapped or edited.
3. Every file, and every text the producer reads that is not a file, is handed
   to the adapter's measure.
4. One report naming each file, its role, its bytes and its digest, the total,
   and the checks that ran.

``extra`` is text the producer reads that is not a file in its workspace: the
spawn message, which arrives as the dispatch prompt. It gets the same measure
and is listed in the report, and it is outside the closure check because it is
not in the workspace to be closed over.

**The measure is the adapter's**, because the two consumers measure different
things and record different refusals. One refuses evaluator-only files by name,
digest and substring, withheld passages outside the stage that was given them,
and case identifiers and thresholds in instruction text. The other refuses any
60-character normalised run the later document carries and the earlier one
lacks, plus an answer-key term, and exempts the one stage whose evidence *is*
the later document. A union of the two would be an adapter wearing an
interface, so the measure is a callable taking ``(where, role, data, stage)``
and raising its own refusal.
"""

from __future__ import annotations

from pathlib import Path

from .adapter import ROLES
from .digests import digest


class ExposureRefusal(ValueError):
    """The producer would see something it must not see."""


def refuse_undeclared_roles(declared, roles=ROLES):
    unknown = sorted(role for role in set(declared.values()) if role not in roles)
    if unknown:
        raise ExposureRefusal(f"undeclared role: {', '.join(unknown)}")


def refuse_closure_break(root, declared):
    """Every file declared, every declared file present. Symlinks count."""
    root = Path(root)
    present = {
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    for relative in sorted(present - set(declared)):
        raise ExposureRefusal(f"{relative}: in the workspace and not declared")
    for relative in sorted(set(declared) - present):
        raise ExposureRefusal(f"{relative}: declared and not in the workspace")
    return present


def check(
    root,
    declared,
    stage,
    *,
    stages,
    frozen_digests,
    measure,
    report_schema,
    report_extras=None,
    roles=ROLES,
    extra=None,
):
    """Every byte the producer can see, and what it is not allowed to contain."""
    stages = tuple(stages)
    if stage not in stages:
        raise ExposureRefusal(f"unknown stage: {stage!r}; expected one of {stages}")
    root = Path(root)
    refuse_undeclared_roles(declared, roles)
    refuse_closure_break(root, declared)

    files = []
    for relative in sorted(declared):
        data = (root / relative).read_bytes()
        role = declared[relative]
        if role == "DATA" and digest(data) not in frozen_digests:
            raise ExposureRefusal(f"{relative}: DATA that is not a frozen packet")
        measure(relative, role, data, stage)
        files.append(
            {
                "path": relative,
                "role": role,
                "bytes": len(data),
                "sha256": digest(data),
                "in_workspace": True,
            }
        )
    for name, (role, data) in sorted((extra or {}).items()):
        if role not in roles:
            raise ExposureRefusal(f"undeclared role: {role}")
        measure(name, role, data, stage)
        files.append(
            {
                "path": name,
                "role": role,
                "bytes": len(data),
                "sha256": digest(data),
                "in_workspace": False,
            }
        )
    return {
        "schema": report_schema,
        "stage": stage,
        "files": files,
        "total_bytes": sum(item["bytes"] for item in files),
        **(report_extras or {}),
        "status": "CLEAN",
    }
