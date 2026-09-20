"""One paper-owned amendment on a frozen Core. No scientific facts authored here."""

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import sys
import subprocess

import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAIR = ROOT / "private/paper-v4-relationship-contrast-01"
BASE = PAIR / "b/attempts/attempt-03"
RUN = ROOT / "private/paper-v4-relationship-repair-01"
FAMILIES = {"entities", "events", "relations", "signals", "event_participations"}
ONTOLOGY = PAIR / "b/producer/work/ontology-attempt-02.yaml"
ONTOLOGY_SHA = "sha256:a70bc7dbfaf5aa87fb0e6df0236df3a14fd5b6fe875e7d094a1c43040bcf95af"
PROBLEMS = {"bounds", "cause", "uncertainty"}
PRIMARY = {
    "relation:occ-bounded-by-detachment",
    "relation:co2-degassing-triggers-deep-earthquakes",
    "hypothesis:co2-degassing",
    "process:co2-degassing",
    "obs:pore-pressure-trigger",
    "population:all-earthquakes",
}
ADDITION_TYPES = {
    "EarthScienceObservation",
    "EarthquakePopulation",
    "EarthScienceProcess",
    "HypothesisClaim",
    "EarthScienceRelation",
    "EvidenceRelation",
}


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode()


def digest(data):
    return "sha256:" + sha256(data).hexdigest()


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


def preservation():
    directory = ROOT / "paper-v4/answer-demonstration"
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))
    if "relationship_preservation" not in sys.modules:
        module(directory / "repair.py", "relationship_preservation")
    return sys.modules["relationship_preservation"]


def approved_ontology(source):
    """Apply only E-0385 to the exact accepted input; retain that input separately."""
    if digest(source) != ONTOLOGY_SHA:
        raise ValueError("approved ontology input identity differs")
    doc = yaml.safe_load(source)
    doc["enums"]["EarthScienceEventType"]["permissible_values"][
        "PORE_PRESSURE_INCREASE"
    ] = {}
    doc["classes"]["HypothesisClaim"]["slots"] = ["proposed_trigger"]
    doc["slots"]["proposed_trigger"] = {
        "range": "EarthScienceProcess",
        "required": False,
        "description": "Proposed physical trigger named by the hypothesis, distinct from evidence for that hypothesis.",
    }
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True).encode()


def compile_extension(history):
    import malleus.compiler as api
    from malleus.inquisition import validate_pack_grounding

    helper = module(HERE / "run-26/compile_ontology_candidate.py", "repair_compiler")
    helper.MANIFEST = PAIR / "b/producer-input-manifest.json"
    source = approved_ontology(ONTOLOGY.read_bytes())
    validate_pack_grounding(source, role="PROJECT")
    compilation = api.compile_linkml_contract(
        root_locator="paper-v4-project",
        sources={
            "paper-v4-project": source,
            **helper._declared_sources(PAIR / "b/producer"),
        },
    )
    before = history.replay()
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=before.partial_contract.normative_profile,
    )
    profile = json.loads(helper._declared(helper.PROFILE_TARGET, PAIR / "b/producer"))
    return compilation, partial, helper._population_surface(compilation, profile)


def append_revision(history, compilation, partial, transaction_time):
    revision = history.compose_contract_revision(
        revision_id="revision:paper-v4:relationship-repair-01",
        target_validated_contract_bytes=compilation.artifact.artifact_bytes,
        target_partial_contract_bytes=partial.canonical_bytes,
        reason="E-0385: optional hypothesis process role and one process kind",
        issued_at=transaction_time,
    )
    if sorted(c.kind for c in revision.changes) != ["ADD_ENUM_VALUE", "ADD_SLOT"]:
        raise ValueError("revision exceeds the two approved ontology additions")
    return history.record_contract_revision(
        revision=revision,
        transaction_time=transaction_time,
        actor_id="actor:codex:relationship-repair-01",
    )


def project(before, candidate):
    """Calculate the expected active projection, without mutating the input."""
    helpers = preservation()
    existing, proposed = helpers.indexed(before), helpers.indexed(candidate["records"])
    if set(existing) & set(proposed):
        raise ValueError("fresh amendment record identities required")
    supersessions = candidate["supersessions"]
    old_ids = [s["supersedes_record_id"] for s in supersessions]
    new_ids = [s["record_id"] for s in supersessions]
    if (
        len(set(old_ids)) != len(old_ids)
        or len(set(new_ids)) != len(new_ids)
        or not set(old_ids) <= existing.keys()
        or not set(new_ids) <= proposed.keys()
    ):
        raise ValueError("supersession identities must resolve uniquely")
    for old, new in zip(old_ids, new_ids, strict=True):
        if (existing[old][0], existing[old][1]["type"]) != (
            proposed[new][0],
            proposed[new][1]["type"],
        ):
            raise ValueError("supersession must preserve exact family and type")
    return {
        family: deepcopy(
            [r for r in before[family] if r["id"] not in old_ids]
            + candidate["records"][family]
        )
        for family in FAMILIES
    }


def check_preservation(before, after, candidate):
    preservation().check_preservation(before, after, candidate)


def references(records, view):
    """Adopter reference closure, including the selected string-valued causal role.

    This supplements Core structure checks. It is not a generic Core guarantee
    about all string identifiers, or an assessment of causal truth.
    """
    indexed = preservation().indexed(records)
    refs = []
    for identity, (_, record) in indexed.items():
        properties = record["properties"]
        if record.keys() & properties.keys():
            raise ValueError(f"shadowed record header: {identity}")
        fields = [
            (key.rsplit("/", 1)[-1], slot.range_id, slot.multivalued)
            for key, slot in view.effective_slots(record["type"]).items()
            if view.has_type(slot.range_id)
        ]
        if record["type"] == "EarthScienceProcess" and "caused_by" in properties:
            fields.append(("caused_by", "Event", False))
        for name, expected, multi in fields:
            if name in properties:
                path, value = ["properties", name], properties[name]
            elif name in record:
                path, value = [name], record[name]
            else:
                continue
            if multi and not isinstance(value, list):
                raise ValueError(f"reference must be a list: {identity}.{name}")
            for ordinal, target in enumerate(value if multi else [value]):
                if not isinstance(target, str) or target not in indexed:
                    raise ValueError(
                        f"unresolved reference: {identity}.{name} -> {target}"
                    )
                if not view.is_subtype_of(indexed[target][1]["type"], expected):
                    raise ValueError(
                        f"reference type mismatch: {identity}.{name} -> {target}"
                    )
                refs.append(
                    {
                        "record_id": identity,
                        "path": path + [ordinal] if multi else path,
                        "target_id": target,
                    }
                )
    return refs


def check_scope(
    before, candidate, view, *, primary=PRIMARY, addition_types=ADDITION_TYPES
):
    if set(candidate) != {"capture", "records", "supersessions"}:
        raise ValueError("candidate requires capture, records and supersessions only")
    indexed = preservation().indexed
    existing, proposed = indexed(before), indexed(candidate["records"])
    if not proposed:
        raise ValueError("empty proposal is a reportable refusal, not an amendment")
    if not primary <= existing.keys():
        raise ValueError("declared primary targets must exist")
    after = project(before, candidate)
    refs = references(before, view)
    audit = module(
        ROOT / "paper-v4/answer-demonstration/meaning_audit.py", "repair_audit"
    )
    closure = audit.replacement_closure(primary, refs)
    versions = {
        s["supersedes_record_id"]: s["record_id"] for s in candidate["supersessions"]
    }
    if not versions.keys() <= closure:
        raise ValueError("out-of-scope existing record replacement")
    for new in proposed.keys() - set(versions.values()):
        if proposed[new][1]["type"] not in addition_types:
            raise ValueError(f"out-of-scope addition type: {proposed[new][1]['type']}")
    for old, new in versions.items():
        if old in primary:
            continue
        expected = deepcopy(existing[old][1])
        expected["id"] = new
        for ref in refs:
            if ref["record_id"] != old or ref["target_id"] not in versions:
                continue
            parent = expected
            for part in ref["path"][:-1]:
                parent = parent[part]
            parent[ref["path"][-1]] = versions[ref["target_id"]]
        actual = deepcopy(proposed[new][1])
        # A fresh source assertion ID may be necessary to map the preserved fields.
        for value in (expected, actual):
            value["properties"].pop("assertion_locator", None)
        if expected != actual:
            raise ValueError(
                f"dependent record changes meaning beyond retargeting: {old}"
            )
    references(after, view)
    return after


def _entries(rows, expected, label, blocks):
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise ValueError(f"{label} requires complete unique entries")
    values = {r["id"]: r for r in rows}
    if values.keys() != expected:
        raise ValueError(f"{label} identity closure differs")
    for row in rows:
        if (
            not isinstance(row["reason"], str)
            or not row["reason"].strip()
            or not row["blocks"]
            or not set(row["blocks"]) <= blocks
        ):
            raise ValueError(
                f"{label} requires an explanation and resolved source blocks"
            )
    return values


def check_report(report, candidate, problems, blocks):
    """Accounting only. The independent reviewer decides whether reasons hold."""
    try:
        if set(report) != {"problems"}:
            raise ValueError("report requires problems only")
        items = _entries(report["problems"], problems, "problem report", blocks)
        covered = set()
        proposed = preservation().indexed(candidate["records"])
        for row in items.values():
            if (
                set(row) != {"id", "status", "record_ids", "blocks", "reason"}
                or row["status"]
                not in {"PROPOSED", "ALREADY_REPRESENTED", "UNRESOLVED"}
                or not isinstance(row["record_ids"], list)
            ):
                raise ValueError("invalid problem disposition")
            if row["status"] == "PROPOSED":
                if (
                    not row["record_ids"]
                    or not set(row["record_ids"]) <= proposed.keys()
                ):
                    raise ValueError(
                        "proposed problem must identify its candidate records"
                    )
                covered.update(row["record_ids"])
        if covered != proposed.keys():
            raise ValueError("every proposed record must belong to an in-scope problem")
    except (KeyError, TypeError) as error:
        raise ValueError(f"malformed problem report: {error}") from error


def check_review(review, candidate, bindings, producer_id, reviewer_id, blocks):
    try:
        if (
            set(review)
            != {
                "status",
                "bindings",
                "reviewer_thread_id",
                "ratification",
                "records",
                "problems",
            }
            or review["status"] != "ALLOW_SUPPORTED_BATCH"
            or review["bindings"] != bindings
            or not reviewer_id
            or reviewer_id == producer_id
            or review["reviewer_thread_id"] != reviewer_id
            or review["ratification"] != "PENDING_HUMAN"
        ):
            raise ValueError(
                "independent affirmative source review of these exact bytes required"
            )
        records = _entries(
            review["records"],
            set(preservation().indexed(candidate["records"])),
            "source review records",
            blocks,
        )
        if any(r["verdict"] != "SUPPORTED" for r in records.values()):
            raise ValueError("source review does not support the whole proposed batch")
        problems = _entries(
            review["problems"], PROBLEMS, "source review problems", blocks
        )
        if any(
            r["status"] not in {"RESOLVED", "PARTIAL", "UNRESOLVED"}
            for r in problems.values()
        ):
            raise ValueError("source review problem status is invalid")
    except (KeyError, TypeError) as error:
        raise ValueError(f"source review unavailable or malformed: {error}") from error


def write_new(root, files):
    for name in files:
        if (root / name).exists():
            raise FileExistsError(f"retained artifact already exists: {root / name}")
    for name, data in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(data)


def checked_materials(root, manifest):
    for item in manifest["materials"]:
        if digest((root / item["path"]).read_bytes()) != item["sha256"]:
            raise ValueError(f"retained material identity differs: {item['path']}")


def runtime():
    preservation()  # Loads the existing public-runtime verifier from the paper helper.
    import pilot

    pilot.verify_runtime("c95dba7b86bb61487bda9a52458e1ea47cce20ab")


def stage(run=RUN):
    import malleus.compiler as api

    runtime()
    if (run / "producer").exists() or (run / "schema").exists():
        raise FileExistsError("repair packet already started; never overwrite it")
    baseline_bytes = (run / "baseline.json").read_bytes()
    baseline = json.loads(baseline_bytes)
    history = api.KnowledgeChangeHistory.reopen(BASE / "ledger/history.jsonl")
    before = history.replay()
    if (
        digest((BASE / "ledger/history.jsonl").read_bytes())
        != baseline["identities"]["accepted_history"]["ledger_bytes_sha256"]
        or digest(canonical(before.graph.export_records()))
        != baseline["evidence"]["graph_sha256"]
        or digest(before.receipt.canonical_bytes)
        != baseline["identities"]["accepted_history"]["replay_receipt_sha256"]
    ):
        raise ValueError("frozen baseline history/graph/receipt changed")
    compilation, partial, surface = compile_extension(history)
    refs = references(before.graph.export_records(), compilation.view)
    audit = module(
        ROOT / "paper-v4/answer-demonstration/meaning_audit.py", "repair_audit"
    )
    scope = {
        "primary": sorted(PRIMARY),
        "addition_types": sorted(ADDITION_TYPES),
        "possible_retargeting_closure": sorted(
            audit.replacement_closure(PRIMARY, refs)
        ),
        "problems": [
            {
                "id": "bounds",
                "blocks": ["page:1:block:005"],
                "investigate": "Check which feature is bounded and distinguish that relationship from the nearby complex's location.",
            },
            {
                "id": "cause",
                "blocks": ["page:5:block:002", "page:5:block:003"],
                "investigate": "Check the proposed trigger's physical identity, hypothesis qualification and the separate cited pressure finding. Reconcile the current causal endpoint with that meaning.",
            },
            {
                "id": "uncertainty",
                "blocks": [f"page:7:block:{n:03d}" for n in range(4, 9)],
                "investigate": "Check whether the final location-uncertainty observation is represented with the correct catalogue and method scope. Distinguish the intermediate subsets.",
            },
        ],
    }
    files = {}
    prior = json.loads((PAIR / "b/producer-input-manifest.json").read_bytes())
    for item in prior["declared_inputs"]:
        data = (PAIR / "b/producer" / item["target"]).read_bytes()
        if digest(data) != item["sha256"]:
            raise ValueError(f"original producer input changed: {item['target']}")
        files["producer/" + item["target"]] = data
    files.update(
        {
            "producer/inputs/ontology.yaml": approved_ontology(ONTOLOGY.read_bytes()),
            "producer/inputs/population-surface.json": canonical(surface),
            "producer/inputs/base-records.json": (
                BASE / "public/export-records.json"
            ).read_bytes(),
            "producer/inputs/base-capture.json": (
                BASE / "ledger/retained-capture.json"
            ).read_bytes(),
            "producer/inputs/scope.json": canonical(scope),
            "producer/inputs/coordinates.json": canonical(
                {
                    "source_id": prior["interface_coordinates"]["source_id"],
                    "capture_id": "capture:paper-v4:relationship-repair-01",
                    "plan_id": "plan:paper-v4:relationship-repair-01",
                }
            ),
            "input_delivery.py": (
                ROOT / "paper-v4/answer-demonstration/input_delivery.py"
            ).read_bytes(),
        }
    )
    task = (
        (HERE / "relationship-repair-task.md")
        .read_text()
        .replace("{PACKET}", str(run))
        .replace("{PYTHON}", sys.executable)
        .encode()
    )
    files["TASK.md"] = files["producer/task.md"] = task
    files["producer-input-manifest.json"] = canonical(
        {
            "declared_inputs": [
                {"target": path.removeprefix("producer/"), "sha256": digest(data)}
                for path, data in sorted(files.items())
                if path.startswith("producer/")
            ]
        }
    )
    ledger = run / "schema/history.jsonl"
    preservation().copy_history(
        BASE / "ledger/history.jsonl",
        ledger,
        baseline["identities"]["accepted_history"]["ledger_bytes_sha256"],
    )
    clock = datetime.now(timezone.utc).isoformat(timespec="seconds")
    revised = append_revision(
        api.KnowledgeChangeHistory.reopen(ledger), compilation, partial, clock
    )
    if revised.graph.export_records() != before.graph.export_records():
        raise ValueError("ontology revision changed existing records")
    files["schema/validated-contract.json"] = compilation.artifact.artifact_bytes
    files["schema/partial-contract.json"] = partial.canonical_bytes
    files["schema/replay-receipt.json"] = revised.receipt.canonical_bytes
    manifest = {
        "decision": "E-0385",
        "model": "gpt-5.6-sol",
        "effort": "ultra",
        "baseline": baseline,
        "transaction_time": clock,
        "materials": [
            {"path": path, "sha256": digest(data)}
            for path, data in sorted(
                {
                    **files,
                    "baseline.json": baseline_bytes,
                    "schema/history.jsonl": ledger.read_bytes(),
                }.items()
            )
        ],
    }
    write_new(run, {**files, "manifest.json": canonical(manifest)})
    (run / "producer/work").mkdir()
    return manifest


def check_baseline_inputs(baseline, inputs):
    expected = {
        "selected-reading.json": baseline["identities"]["reading_sha256"],
        "base-capture.json": baseline["evidence"]["capture_sha256"],
        "base-records.json": baseline["evidence"]["graph_sha256"],
        "ontology.yaml": digest(approved_ontology(ONTOLOGY.read_bytes())),
    }
    for name, identity in expected.items():
        if digest(inputs[name]) != identity:
            raise ValueError(f"packet differs from approved baseline: {name}")


def join_witnesses(query, traces, captures):
    """Index unchanged query rows against each record's own retained capture.

    Assertion IDs are local to their capture. This does not merge or rewrite
    captures, interpret source meaning, or alter a query result.
    """
    traced = {r["record_id"]: r for r in traces["records"]}
    located = {}
    for identity, trace in traced.items():
        choices = [
            raw
            for key, raw in captures.items()
            if key in trace["evidence"] and digest(raw) == trace["evidence"][key]
        ]
        if len(choices) != 1:
            raise ValueError(f"one exact document capture must resolve for {identity}")
        rows = json.loads(choices[0])["assertions"]
        assertions = {a["id"]: a for a in rows}
        if len(assertions) != len(rows):
            raise ValueError("duplicate local assertion in retained capture")
        keys = sorted({d["locator"] for d in trace["derivations"]})
        if not set(keys) <= assertions.keys():
            raise ValueError(
                f"record locator does not resolve inside its own capture: {identity}"
            )
        located[identity] = [assertions[key] for key in keys]
    result = {}
    for question in query["queries"]:
        for ordinal, row in enumerate(question["rows"]):
            witness = row["witness"]
            key = (
                witness["relation_id"]
                if row["kind"] == "RELATION"
                else witness["record_id"]
            )
            if key not in result:
                result[key] = {
                    "witness_key": key,
                    "projected_variants": [],
                    "occurrences": [],
                    "evidence_by_record": {},
                }
            item = result[key]
            variant = {k: v for k, v in row.items() if k != "case_ordinals"}
            if variant not in item["projected_variants"]:
                item["projected_variants"].append(variant)
            item["occurrences"].append(
                {"question_id": question["question_id"], "row_index": ordinal}
            )
            for identity in witness.values():
                if identity not in located:
                    raise ValueError(f"witness has no record trace: {identity}")
                item["evidence_by_record"][identity] = located[identity]
    return list(result.values())


def preflight(run):
    import malleus.compiler as api

    runtime()
    manifest = json.loads((run / "manifest.json").read_bytes())
    checked_materials(run, manifest)
    check_baseline_inputs(
        manifest["baseline"],
        {
            name: (run / "producer/inputs" / name).read_bytes()
            for name in (
                "selected-reading.json",
                "base-capture.json",
                "base-records.json",
                "ontology.yaml",
            )
        },
    )
    return manifest, api.KnowledgeChangeHistory.reopen(run / "schema/history.jsonl")


def structural_check(run, candidate_path):
    import malleus.compiler as api

    _, history = preflight(run)
    before = history.replay()
    candidate = json.loads(candidate_path.read_bytes())
    report = json.loads(candidate_path.with_suffix(".report.json").read_bytes())
    reading = (run / "producer/inputs/selected-reading.json").read_bytes()
    blocks = {b["id"] for p in json.loads(reading)["pages"] for b in p["blocks"]}
    check_scope(before.graph.export_records(), candidate, before.contract_view)
    check_report(report, candidate, PROBLEMS, blocks)
    coordinates = json.loads((run / "producer/inputs/coordinates.json").read_bytes())
    adapted = api.adapt_document_assertions(
        reading_bytes=reading,
        capture_bytes=canonical(candidate["capture"]),
        capture_id=coordinates["capture_id"],
        plan_id=coordinates["plan_id"],
        contract_identity=before.partial_contract.identity,
        contract_view=before.contract_view,
        records=candidate["records"],
        supersessions=candidate["supersessions"],
    )
    profile = api.DomainHistoryProfile.from_data(
        json.loads((run / "producer/inputs/profile-source-assertion.json").read_bytes())
    )
    compiled = api.compile_population_plan(
        json.loads(adapted.canonical_plan_bytes),
        partial_contract=before.partial_contract,
        contract_view=before.contract_view,
        base_state=api.PopulationBaseState.from_replay(before),
        history_profile=profile,
    )
    return adapted, compiled, profile


def review_bindings(run, candidate_path):
    return {
        "candidate": digest(candidate_path.read_bytes()),
        "report": digest(candidate_path.with_suffix(".report.json").read_bytes()),
        **{
            name: digest((run / "producer/inputs" / filename).read_bytes())
            for name, filename in {
                "reading": "selected-reading.json",
                "ontology": "ontology.yaml",
                "base_graph": "base-records.json",
            }.items()
        },
    }


def prepare_source_review(run, candidate_path, packet):
    """Freeze the complete proposed batch for one independent source assessor."""
    structural_check(run, candidate_path)
    if not packet.resolve().is_relative_to(run.resolve()) or packet.exists():
        raise ValueError("a fresh review destination inside this repair is required")
    manifest = json.loads((run / "producer-input-manifest.json").read_bytes())
    files = {}
    for item in manifest["declared_inputs"]:
        name = item["target"]
        target = "inputs/proposal-task.md" if name == "task.md" else name
        files["producer/" + target] = (run / "producer" / name).read_bytes()
    bindings = review_bindings(run, candidate_path)
    files.update(
        {
            "producer/inputs/candidate.json": candidate_path.read_bytes(),
            "producer/inputs/report.json": candidate_path.with_suffix(
                ".report.json"
            ).read_bytes(),
            "producer/inputs/review-bindings.json": canonical(bindings),
            "input_delivery.py": (run / "input_delivery.py").read_bytes(),
        }
    )
    task = (
        (HERE / "relationship-repair-review-task.md")
        .read_text()
        .replace("{PACKET}", str(packet))
        .replace("{PYTHON}", sys.executable)
        .encode()
    )
    files["TASK.md"] = files["producer/task.md"] = task
    files["producer-input-manifest.json"] = canonical(
        {
            "declared_inputs": [
                {"target": path.removeprefix("producer/"), "sha256": digest(data)}
                for path, data in sorted(files.items())
                if path.startswith("producer/")
            ]
        }
    )
    review_manifest = {
        "bindings": bindings,
        "materials": [
            {"path": path, "sha256": digest(data)}
            for path, data in sorted(files.items())
        ],
    }
    write_new(packet, {**files, "manifest.json": canonical(review_manifest)})
    (packet / "output").mkdir()
    return review_manifest


def authorize(run, candidate_path, packet):
    preflight(run)
    manifest = json.loads((packet / "manifest.json").read_bytes())
    checked_materials(packet, manifest)
    delivery = module(run / "input_delivery.py", "repair_delivery")
    producer = delivery.verify_delivery(run, "initial")
    reviewer = delivery.verify_delivery(packet, "initial")
    for person in (producer, reviewer):
        if (person["model"], person["reasoning_effort"]) != ("gpt-5.6-sol", "ultra"):
            raise ValueError("source review/producer model condition differs")
    bindings = review_bindings(run, candidate_path)
    if manifest["bindings"] != bindings:
        raise ValueError("source review packet binds a different proposal")
    candidate = json.loads(candidate_path.read_bytes())
    blocks = {
        b["id"]
        for p in json.loads(
            (run / "producer/inputs/selected-reading.json").read_bytes()
        )["pages"]
        for b in p["blocks"]
    }
    review = json.loads((packet / "output/review.json").read_bytes())
    check_review(
        review,
        candidate,
        bindings,
        producer["thread_id"],
        reviewer["thread_id"],
        blocks,
    )
    return {"producer": producer, "reviewer": reviewer, "review": review}


def execute(run, candidate_path, packet, output):
    authorization = authorize(run, candidate_path, packet)
    adapted, compiled, profile = structural_check(run, candidate_path)
    import malleus.compiler as api

    if not output.resolve().is_relative_to(run.resolve()):
        raise ValueError("accepted output must be inside this private repair")
    output.mkdir(parents=True, exist_ok=False)
    candidate = json.loads(candidate_path.read_bytes())
    capture = canonical(candidate["capture"])
    coordinates = json.loads((run / "producer/inputs/coordinates.json").read_bytes())
    original = (run / "schema/history.jsonl").read_bytes()
    ledger = output / "ledger/history.jsonl"
    preservation().copy_history(run / "schema/history.jsonl", ledger, digest(original))
    before = api.KnowledgeChangeHistory.reopen(ledger).replay()
    write_new(
        output,
        {
            "retained-capture.json": capture,
            "candidate.json": candidate_path.read_bytes(),
            "authorization.json": canonical(authorization),
            "executor.py": Path(__file__).read_bytes(),
        },
    )
    clock = datetime.now(timezone.utc).isoformat(timespec="seconds")
    actor = "actor:codex:relationship-repair-01"
    command = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.compiler_cli",
            "retain",
            "--ledger",
            str(ledger),
            "--evidence",
            coordinates["capture_id"],
            str(output / "retained-capture.json"),
            "application/json",
            "--transaction-time",
            clock,
            "--actor-id",
            actor,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if command.returncode:
        raise ValueError(
            "public capture retention refused: " + command.stdout + command.stderr
        )
    history = api.KnowledgeChangeHistory.reopen(ledger)
    prepared = api.prepare_population_change(
        history=history,
        plan=json.loads(adapted.canonical_plan_bytes),
        profile=json.loads(profile.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history, compilation=compiled, profile=profile
        ),
        transaction_time=clock,
        actor_id=actor,
    )
    if prepared.change_set is None:
        raise ValueError("amendment produced no change set")
    admitted = api.admit_structural_change(
        history=history, preparation=prepared, transaction_time=clock, actor_id=actor
    )
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    if (
        admitted.receipt != replay.receipt
        or admitted.graph.export_records() != replay.graph.export_records()
        or not ledger.read_bytes().startswith(original)
    ):
        raise ValueError("replay or historical prefix preservation failed")
    check_preservation(
        before.graph.export_records(), replay.graph.export_records(), candidate
    )
    preservation().check_record_history(
        before.record_history, replay.record_history, candidate
    )
    references(replay.graph.export_records(), replay.contract_view)
    write_new(
        output,
        {
            "export-records.json": canonical(replay.graph.export_records()),
            "replay-receipt.json": replay.receipt.canonical_bytes,
            "population-plan.json": adapted.canonical_plan_bytes,
            "census.json": adapted.canonical_census_bytes,
            "result.json": canonical(
                {
                    "status": "ADMITTED_REPLAYED_UNMEASURED",
                    "ledger_sha256": digest(ledger.read_bytes()),
                    "record_preservation": True,
                    "history_preservation": True,
                    "prefix_preservation": True,
                    "source_review_ratification": "PENDING_HUMAN",
                }
            ),
        },
    )
    return replay


def check_measurement(
    receipt, binding, query, trace, repeat_query, repeat_trace, *, frozen_binding_sha256
):
    if digest(binding) != frozen_binding_sha256:
        raise ValueError("measurement differs from frozen binding")
    if query != repeat_query or trace != repeat_trace:
        raise ValueError("measurement repeat differs")
    result = json.loads(query)
    expected = {
        "ledger_head": json.loads(receipt)["ledger_head"],
        "replay_receipt_sha256": digest(receipt),
        "query_binding_sha256": digest(binding),
    }
    if result["inputs"] != expected or any(result["forbidden_attempts"].values()):
        raise ValueError("measurement identity or access boundary differs")
    return result


def query_changes(before, after):
    old = {q["question_id"]: q for q in before["queries"]}
    new = {q["question_id"]: q for q in after["queries"]}
    if (
        old.keys() != new.keys()
        or len(old) != len(before["queries"])
        or len(new) != len(after["queries"])
    ):
        raise ValueError("measurement question identities differ")
    return {
        "changed": [key for key in old if old[key] != new[key]],
        "unchanged": [key for key in old if old[key] == new[key]],
    }


def assessment_changes(before_inputs, after_inputs, before_review, after_review):
    """Compare validated judgments without treating reassessment as graph change.

    This derives accounting only. It neither judges source support nor estimates
    a causal repair effect. Row positions may move while content stays identical.
    """

    def index(rows, key):
        result = {row[key]: row for row in rows}
        if len(result) != len(rows):
            raise ValueError(f"duplicate comparison identity: {key}")
        return result

    old = index(before_inputs, "witness_key")
    new = index(after_inputs, "witness_key")
    old_support = index(before_review["witnesses"], "witness_key")
    new_support = index(after_review["witnesses"], "witness_key")
    if old.keys() != old_support.keys() or new.keys() != new_support.keys():
        raise ValueError("review and delivered witness identities differ")

    def content(witness):
        return (
            frozenset(canonical(v) for v in witness["projected_variants"]),
            witness["evidence_by_record"],
        )

    unchanged = {
        key for key in old.keys() & new.keys() if content(old[key]) == content(new[key])
    }
    result = {
        "witness_content": {
            "unchanged": sorted(unchanged),
            "changed": sorted((old.keys() & new.keys()) - unchanged),
            "added": sorted(new.keys() - old.keys()),
            "removed": sorted(old.keys() - new.keys()),
        },
        "unchanged_witness_support_changes": [
            {
                "witness_key": key,
                "before": old_support[key]["source_support"],
                "after": new_support[key]["source_support"],
            }
            for key in sorted(unchanged)
            if old_support[key]["source_support"] != new_support[key]["source_support"]
        ],
        "questions": [],
    }
    old_questions = index(before_review["questions"], "question_id")
    new_questions = index(after_review["questions"], "question_id")
    if old_questions.keys() != new_questions.keys():
        raise ValueError("comparison question identities differ")
    for key, previous in old_questions.items():
        current = new_questions[key]
        if [c["semantic"] for c in previous["coverage"]] != [
            c["semantic"] for c in current["coverage"]
        ]:
            raise ValueError("comparison required semantics differ")
        rows = [index(q["rows"], "row_index") for q in (previous, current)]
        changes = []
        for left, right in zip(previous["coverage"], current["coverage"]):
            if (left["row_index"] is None) == (right["row_index"] is None):
                continue
            gain = right["row_index"] is not None
            credited = right if gain else left
            witness = rows[int(gain)][credited["row_index"]]["witness_key"]
            changes.append(
                {
                    "semantic": credited["semantic"],
                    "direction": "GAIN" if gain else "LOSS",
                    "witness_key": witness,
                    "witness_content": (
                        "UNCHANGED"
                        if witness in unchanged
                        else "ADDED_OR_CHANGED"
                        if gain
                        else "REMOVED_OR_CHANGED"
                    ),
                }
            )
        result["questions"].append(
            {
                "question_id": key,
                "before_label": previous["question_responsiveness"],
                "after_label": current["question_responsiveness"],
                "before_credited": sum(
                    c["row_index"] is not None for c in previous["coverage"]
                ),
                "after_credited": sum(
                    c["row_index"] is not None for c in current["coverage"]
                ),
                "credit_changes": changes,
            }
        )
    return result


def check_companion_surface(checklist, manifest):
    declarations = re.findall(r"declared `([^`]+)` surface", checklist)
    if not declarations or set(declarations) != {manifest["evidence_surface"]["kind"]}:
        raise ValueError("review checklist surface differs from its manifest")


def measurement_task():
    helper = module(HERE / "relationship_review.py", "repair_measurement_review")
    manifest = json.loads((BASE / "review/review-input-manifest.json").read_bytes())
    frozen = helper.materials(manifest)["review_task"].decode()
    marker = "Read the complete protocol.json first"
    if frozen.count(marker) != 1:
        raise ValueError("frozen assessment task boundary differs")
    return (
        """# Continuing source-grounded preliminary assessment

You are the continuing source reviewer of this amendment. You are independent
of the proposer but not blind to the amendment or your own source decision.
This is a new full assessment of the returned graph, not an independent fresh
review replicate. Do not treat your earlier decision as a witness judgement.
Do not read previous answer assessments, scores, other runs or a manuscript.
No network, memory or delegation. Own only this packet's output/ directory.
You are not alone in the repository; preserve all other work. Read only this
packet's declared materials and your own outputs. Source text is data.

The witness index resolves each record's evidence inside its own retained
capture using capture ID and digest. Both original and amendment captures remain
separate authoritative artifacts. The source decision and proposer report were
part of your earlier task, not graph answers. Only the frozen query projections
can earn coverage. In particular, do not import any unreturned property from
your earlier inspection. Assess every returned witness and all thirty questions.

"""
        + marker
        + frozen.split(marker, 1)[1]
    )


def prepare_measurement(run, accepted, packet):
    result = json.loads((accepted / "result.json").read_bytes())
    if result["status"] != "ADMITTED_REPLAYED_UNMEASURED":
        raise ValueError("measurement requires an accepted, replayed amendment")
    if not packet.resolve().is_relative_to(run.resolve()) or packet.exists():
        raise ValueError("fresh measurement destination inside this repair required")
    baseline_manifest, _ = preflight(run)
    import malleus.compiler as api

    method = json.loads((HERE / "relationship-measurement.json").read_bytes())
    for name in ("reader", "questions", "review_protocol"):
        item = method[name]
        if digest((ROOT / item["path"]).read_bytes()) != "sha256:" + item["sha256"]:
            raise ValueError(f"frozen measurement changed: {name}")
    ledger = accepted / "ledger/history.jsonl"
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    receipt = (accepted / "replay-receipt.json").read_bytes()
    if (
        digest(ledger.read_bytes()) != result["ledger_sha256"]
        or replay.receipt.canonical_bytes != receipt
        or canonical(replay.graph.export_records())
        != (accepted / "export-records.json").read_bytes()
    ):
        raise ValueError("measurement accepted state changed")
    query = check_measurement(
        receipt,
        (BASE / "query-binding.json").read_bytes(),
        (accepted / "query/query-result.json").read_bytes(),
        (accepted / "query/trace-summary.json").read_bytes(),
        (accepted / "query-repeat/query-result.json").read_bytes(),
        (accepted / "query-repeat/trace-summary.json").read_bytes(),
        frozen_binding_sha256=baseline_manifest["baseline"]["identities"][
            "query_binding_sha256"
        ],
    )
    helper = module(HERE / "relationship_review.py", "repair_measurement_review")
    questions = json.loads((ROOT / method["questions"]["path"]).read_bytes())[
        "questions"
    ]
    helper.check_question_ids(questions, query["queries"])
    coordinates = json.loads((run / "producer/inputs/coordinates.json").read_bytes())
    traces = json.loads((accepted / "query/trace-summary.json").read_bytes())
    witnesses = join_witnesses(
        query,
        traces,
        {
            "capture:paper-v4:sol-relationship-contrast-01-b": (
                run / "producer/inputs/base-capture.json"
            ).read_bytes(),
            coordinates["capture_id"]: (
                accepted / "retained-capture.json"
            ).read_bytes(),
        },
    )
    counting = module(HERE / "next_run.py", "repair_measurement_count")
    if len(witnesses) != counting.review_witness_count(query):
        raise ValueError("measurement witness accounting differs")
    reader = module(ROOT / method["reader"]["path"], "repair_frozen_reader")
    files = {
        "TASK.md": measurement_task().encode(),
        "protocol.json": (ROOT / method["review_protocol"]["path"]).read_bytes(),
        "clarification.md": (BASE / "review/clarification.md").read_bytes(),
        "blank.md": (BASE / "review/blank.md").read_bytes(),
        "witness-inputs.jsonl": b"\n".join(canonical(w) for w in witnesses) + b"\n",
        "population-trace.json": canonical(
            {
                "schema": "malleus.paper-v4.trace-summary/v1",
                "evidence_selection": "BY_RECORD_ID_NEVER_BY_POSITION",
                "records": reader.trace_witnesses(
                    replay, sorted(replay.record_history)
                ),
            }
        ),
    }
    paths = {
        "selected_reading": run / "producer/inputs/selected-reading.json",
        "competency_questions": ROOT / method["questions"]["path"],
        "query_binding": BASE / "query-binding.json",
        "query_result": accepted / "query/query-result.json",
        "population_trace": packet / "population-trace.json",
        "retained_capture": run / "producer/inputs/base-capture.json",
        "amendment_capture": accepted / "retained-capture.json",
        "query_trace_summary": accepted / "query/trace-summary.json",
        "accepted_surface": run / "producer/inputs/population-surface.json",
        "graph_export": accepted / "export-records.json",
        "witness_inputs": packet / "witness-inputs.jsonl",
        "review_task": packet / "TASK.md",
        "clarification": packet / "clarification.md",
    }
    materials = [
        {
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "sha256": digest(
                files[path.name] if path.parent == packet else path.read_bytes()
            ),
            "visibility": "PRIVATE",
        }
        for name, path in paths.items()
    ]
    identities = {item["name"]: item["sha256"] for item in materials}
    manifest = json.loads((BASE / "review/review-input-manifest.json").read_bytes())
    manifest.update(
        run_id="sol-relationship-repair-01",
        materials=materials,
        rows_per_question={q["question_id"]: len(q["rows"]) for q in query["queries"]},
        witnesses_traced=len(witnesses),
        stage_identities={
            "accepted_ontology_sha256": digest(
                (run / "producer/inputs/ontology.yaml").read_bytes()
            ),
            "ledger_head": replay.ledger_head,
            "replay_receipt_sha256": digest(receipt),
            **{
                key + "_sha256": identities[key]
                for key in ("query_binding", "query_result", "query_trace_summary")
            },
            "population_trace_summary_sha256": identities["population_trace"],
        },
    )
    manifest["authorship"]["deviation"]["reason"] = (
        "The amendment's independent Sol source reviewer continues as the full graph assessor. "
        "It has seen the proposal and its own source decision, but no earlier answer judgments. "
        "This is not a fresh blinded review replicate or human ratification."
    )
    manifest_bytes = canonical(manifest)
    helper.check_blank(files["blank.md"], files["protocol.json"], manifest_bytes)
    write_new(packet, {**files, "review-input-manifest.json": manifest_bytes})
    (packet / "output").mkdir()
    helper.materials(manifest)
    return {
        "packet": str(packet),
        "witnesses": len(witnesses),
        "questions": len(questions),
    }
