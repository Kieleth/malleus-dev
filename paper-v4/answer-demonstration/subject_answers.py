"""Query revision: match an existing subject's identity text, one hop only.

All question programs, projections, numeric reads and relation traversals remain
the frozen implementation. This changes candidate selection, not stored facts.
"""

from answers import GraphReads, contains, text_of


class SubjectGraphReads(GraphReads):
    def matching(self, *groups, nodes=None):
        candidates = self.nodes() if nodes is None else nodes
        selected = []
        for node in candidates:
            texts = [text_of(node)]
            if "subject" in node:
                subject = self.graph.get_node(node["subject"])
                if subject is None:
                    raise ValueError(
                        f"missing subject {node['subject']} for {node['id']}"
                    )
                fields = self.row_without_subject(subject)
                texts.extend(
                    fields[key] for key in ("name", "description") if key in fields
                )
                if "tags" in fields:
                    texts.extend(fields["tags"])
            if all(
                any(contains(text, term) for text in texts for term in group)
                for group in groups
            ):
                selected.append(node)
        return selected
