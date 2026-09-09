"""Read-only field/source inventory. This does not decide semantic adequacy."""

from copy import deepcopy


def unique(rows, key):
    result = {}
    for row in rows:
        identity = row[key]
        if identity in result:
            raise ValueError(f"duplicate {key}: {identity}")
        result[identity] = row
    return result


def indexed(graph):
    return unique((r for rows in graph.values() for r in rows), "id")


def references(graph, surface):
    """Declared record references only. Core remains the type validator."""
    records = indexed(graph)
    types = unique(surface["record_types"], "name")
    ranges = {t["qualified_name"] for t in types.values()}
    result = []
    for record in records.values():
        if record["type"] not in types:
            raise ValueError(f"unknown record type: {record['type']}")
        properties = record["properties"]
        if record.keys() & properties.keys():
            raise ValueError(f"shadowed record header: {record['id']}")
        for slot in types[record["type"]]["slots"]:
            name = slot["name"]
            if slot["range_id"] not in ranges:
                continue
            if name in properties:
                value, path = properties[name], ["properties", name]
            elif name in record:
                value, path = record[name], [name]
            else:
                continue
            multi = slot["multivalued"]
            if type(multi) is not bool or (multi and type(value) is not list):
                raise ValueError(f"invalid reference shape: {record['id']}.{name}")
            for ordinal, target in enumerate(value if multi else [value]):
                if type(target) is not str or target not in records:
                    raise ValueError(f"unresolved reference: {record['id']}.{name}")
                result.append(
                    {
                        "record_id": record["id"],
                        "path": path + [ordinal] if multi else path,
                        "target_id": target,
                    }
                )
    return result


def replacement_closure(targets, refs):
    """Find records that would need retargeting when IDs are superseded."""
    closure = set(targets)
    while True:
        expanded = closure | {r["record_id"] for r in refs if r["target_id"] in closure}
        if expanded == closure:
            return closure
        closure = expanded


def inventory(graph, surface, capture, reading, *, targets):
    try:
        return _inventory(graph, surface, capture, reading, targets)
    except (KeyError, TypeError, IndexError) as error:
        raise ValueError(f"missing or malformed audit input: {error}") from error


def _inventory(graph, surface, capture, reading, targets):
    records = indexed(graph)
    if not targets or not set(targets) <= records.keys():
        raise ValueError("explicit, existing audit targets required")
    refs = references(graph, surface)
    blocks = unique((b for p in reading["pages"] for b in p["blocks"]), "id")
    assertions = unique(capture["assertions"], "id")
    sources = {key: [] for key in records}
    for assertion in assertions.values():
        statement = " ".join(assertion["statement"].split())
        block = blocks[assertion["block"]]
        if not statement or statement not in " ".join(block["text"].split()):
            raise ValueError(f"assertion text not located: {assertion['id']}")
        mapped = {}
        for field in assertion["formalized_by"]:
            key, path = field["record_id"], field["path"]
            if not path:
                raise ValueError("empty field path")
            value = records[key]
            for component in path:
                value = value[component]
            if key not in mapped:
                mapped[key] = []
            mapped[key].append({"path": path, "value": value})
        # Retain all derivations, not only the record's preferred locator.
        for key, fields in mapped.items():
            sources[key].append(
                {
                    "assertion_id": assertion["id"],
                    "block": assertion["block"],
                    "statement": assertion["statement"],
                    "modality": assertion["modality"],
                    "fields": fields,
                }
            )
    result = []
    for key in sorted(targets):
        if not sources[key]:
            raise ValueError(f"audit target has no source mapping: {key}")
        outgoing = [r for r in refs if r["record_id"] == key]
        incoming = [r for r in refs if r["target_id"] == key]
        neighbors = {r["record_id"] for r in incoming} | {
            r["target_id"] for r in outgoing
        }
        result.append(
            {
                "record": records[key],
                "sources": sources[key],
                "outgoing": outgoing,
                "incoming": incoming,
                "neighbors": {other: records[other] for other in sorted(neighbors)},
            }
        )
    return deepcopy(result)
