"""Explicit text-slot binding for the accepted ontology, not semantic inference.

The question programs and row projections are unchanged. Unknown string slots
refuse until classified; no graph values participate in this classification.
"""

STRING = "https://malleus.dev/contract-facts/String"
CONTENT = frozenset(
    "name description statement tags quantity_kind count_scope claim_kind "
    "observation_kind object_kind spreading_regime feature_kind orientation "
    "layer_kind material_kind chemical_formula selection_basis dataset_kind "
    "numerator_kind denominator_kind event_type temporal_reference_system".split()
)
EXCLUDED = frozenset(
    "id assertion_locator statement_sha256 resource_locator software_version doi "
    "licence duration unit order_key caused_by locator source_digest".split()
)


def text_binding(surface):
    bound = {}
    for item in surface["record_types"]:
        name = item["name"]
        if name in bound:
            raise ValueError(f"duplicate type: {name}")
        selected, seen = [], set()
        for slot in item["slots"]:
            key = slot["name"]
            if key in seen:
                raise ValueError(f"duplicate slot: {name}.{key}")
            seen.add(key)
            kind = slot["range_id"]
            identifier, many = slot["identifier"], slot["multivalued"]
            if type(identifier) is not bool or type(many) is not bool:
                raise ValueError(f"invalid slot flags: {name}.{key}")
            if key in CONTENT and (kind != STRING or identifier):
                raise ValueError(f"content slot is not declared text: {name}.{key}")
            if kind != STRING or identifier:
                continue
            if key in CONTENT:
                selected.append(key)
            elif key not in EXCLUDED:
                raise ValueError(f"unclassified string slot: {name}.{key}")
        bound[name] = sorted(selected)
    return bound


def GraphReads(graph, surface, *, program):
    """Compose with the exact selected base program, never an ambient import."""

    class BoundReads(TextSelection, program.GraphReads):
        pass

    reads = BoundReads(graph, surface)
    reads.text_slots = text_binding(surface)
    reads.contains = program.contains
    return reads


class TextSelection:
    def matching(self, *groups, nodes=None):
        candidates = self.nodes() if nodes is None else nodes
        selected = []
        for node in candidates:
            declarations = {s["name"]: s for s in self.types[node["type"]]["slots"]}
            texts = []
            for key in self.text_slots[node["type"]]:
                if key not in node:
                    continue  # Optional declared field, no substitute value.
                value = node[key]
                if declarations[key]["multivalued"]:
                    if not isinstance(value, list) or any(
                        type(x) is not str for x in value
                    ):
                        raise ValueError(
                            f"text value shape differs: {node['id']}.{key}"
                        )
                    texts.extend(value)
                else:
                    if type(value) is not str:
                        raise ValueError(
                            f"text value shape differs: {node['id']}.{key}"
                        )
                    texts.append(value)
            text = " ".join(texts)
            if all(
                any(self.contains(text, term) for term in group) for group in groups
            ):
                selected.append(node)
        return selected
