"""Render the sealed CC-000 state without becoming a second authority."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from docutils import nodes
from docutils.parsers.rst import Directive

from scripts.contract_compiler_integration import IntegrationState, validate_integration


REPOSITORY = Path(__file__).resolve().parents[2]


def _item(text: str) -> nodes.list_item:
    item = nodes.list_item()
    item += nodes.paragraph(text=text)
    return item


def render_integration(state: IntegrationState) -> nodes.container:
    """Return a deterministic presentation of one already validated state."""
    manifest = state.manifest
    snapshot = manifest["authority"]["snapshot"]
    projection = nodes.container(classes=["contract-manifest"])
    projection += nodes.paragraph(
        text="Non-authoritative projection. Validated manifests remain authoritative."
    )
    projection += nodes.paragraph(
        text=(
            f"Program {manifest['program_id']}; snapshot {snapshot['state']}; "
            f"result commit {snapshot['result_commit']}."
        )
    )
    projection += nodes.paragraph(
        text="Selected workstreams: " + ", ".join(state.selections)
    )
    workstreams = nodes.bullet_list()
    for workstream_id in sorted(state.workstreams):
        dependencies = state.workstreams[workstream_id]
        card = state.cards.get(workstream_id)
        if card is None:
            text = f"{workstream_id}: no registered card"
        else:
            text = (
                f"{workstream_id}: {card['responsibility']} "
                f"Authorization {card['authorization']['class']}; "
                f"candidate {card['candidate']['state']}; "
                f"dependencies {', '.join(dependencies) if dependencies else 'none'}."
            )
        workstreams += _item(text)
    projection += workstreams
    return projection


def manifest_projection(repository: Path) -> nodes.container:
    """Validate the fixed sealed repository manifest, then render its state."""
    return render_integration(validate_integration(repository, require_sealed=True))


class ContractManifestDirective(Directive):
    """Render the repository's fixed sealed integration state."""

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec: dict[str, Any] = {}
    has_content = False

    def run(self) -> list[nodes.Node]:
        return [manifest_projection(REPOSITORY)]


def setup(app: Any) -> dict[str, bool]:
    """Register the zero-input manifest directive."""
    app.add_directive("contract-manifest", ContractManifestDirective)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
