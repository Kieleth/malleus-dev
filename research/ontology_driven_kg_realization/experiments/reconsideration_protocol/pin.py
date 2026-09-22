"""The two coordinates a run is reproducible from: Core's export, and this code.

Core is pinned by export. A runner searches upward from its own file, reads the
export's own markers, and refuses unless they name the Core it is pinned to.
That mechanism stays in the runner, which is staged standalone into a producer
workspace and imports nothing from here.

This package is pinned by digest. It is tracked code in a checkout, not an
export, so the launch receipt records a digest over its module bytes and the
run is reproducible from its receipt without the export carrying a copy. A
receipt written before this pin existed carries none, and no launched run is
re-pinned: its receipt is that run's record.

The pinned set is every module at the package root. Tests are excluded because
no producer session runs them, and caches are excluded because they are not
source.
"""

from __future__ import annotations

from pathlib import Path

from .digests import canonical, digest


GRAMMAR = "malleus.reconsideration-protocol.package-pin/private-v0"


class PinRefusal(ValueError):
    """The pinned package or export is absent, or is not what it declares."""


def module_digests(package) -> dict:
    """Every module of this package at its root, by file name."""
    package = Path(package)
    if not package.is_dir():
        raise PinRefusal(f"{package} is not a directory; there is no package to pin")
    found = {
        path.name: digest(path.read_bytes())
        for path in sorted(package.glob("*.py"))
        if path.is_file()
    }
    if not found:
        raise PinRefusal(f"{package} holds no module; there is nothing to pin")
    return found


def package_pin(package) -> dict:
    """The digest of this package's modules, and the digest over all of them."""
    modules = module_digests(package)
    return {
        "grammar": GRAMMAR,
        "package": Path(package).name,
        "modules": modules,
        "module_count": len(modules),
        "sha256": digest(canonical(modules)),
    }


def verify_package(package, recorded) -> dict:
    """Refuse when this package's bytes are not the ones a receipt recorded."""
    found = package_pin(package)
    if found["sha256"] != recorded.get("sha256"):
        raise PinRefusal(
            f"the protocol package is {found['sha256']}, not the recorded"
            f" {recorded.get('sha256')}"
        )
    moved = sorted(
        name
        for name, value in found["modules"].items()
        if recorded.get("modules", {}).get(name) != value
    )
    if moved:
        raise PinRefusal(f"these modules moved: {', '.join(moved)}")
    return found
