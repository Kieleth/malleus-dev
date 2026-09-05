"""Pin run-14 to one Core commit and write the manifest and the gate block.

Core changes on main while a cell is open, so a run's declared inputs are the
bytes its producer consumed at one commit and nothing else. This script reads
the seven tracked declared inputs with ``git show <commit>:<path>`` and the
selected reading from its private path, writes ``producer-input-manifest.json``,
and fills the parts of ``run-contract.json`` that are facts about that commit:
the execution baseline, the governance head as the ledger renders it, every
verified piece's digests, the pack versions, the document adapter's refusal
reasons that are new since the v4.7 coordinate, the adapter's SUBJECT_NOT_NAMED
refusal messages, the subject census's own outcome keys, how the two subject
sites compare a name against a statement, and whether the adapter and the skill
moved.

Nothing here is typed by hand. A pack version that has not moved, or a Core-18
change that has not landed, is recorded as it stands and the change entry says
so; re-run the script after the Core work lands to re-pin.

Seven of the twenty-one change entries are Core's and carried from run-13.
Their landed facts are read at fixed commits, the v4.1 baseline for Core-12 and
the v4.2 to v4.7 coordinates for Core-11, Core-13, Core-14, Core-15, Core-16 and
Core-17, so a later Core change cannot be attributed to them:
CORE_18_NAME_AS_WORD owns everything the adapter and the skill gain or lose
after the v4.7 coordinate.

Core-18 is a clarification and adds no refusal reason either. The name-or-tag
comparison becomes word-bounded at the SUBJECT_NOT_NAMED check and in the
subject census, which narrows a condition the enum cannot see and leaves the
census keys where Core-17 left them. ``pin_status`` is therefore read from the
adapter's own two sites, by AST, beside the two byte comparisons against the
v4.7 coordinate: the pin refuses to call Core-18 LANDED unless both sites call
one module-level predicate that neither called at the v4.7 coordinate and
neither site still tests a name for membership in a statement. A predicate at
one site only, or a surviving substring test, reads PENDING.

The census reader resolves the adapter's own ``_SUBJECT_OUTCOMES`` tuple and
records what it finds. It is run-13's reader and not run-12's, whose scan of the
census function's body found none of the literals the adapter names by constant
and recorded an empty list at a commit where all four were declared. Run-12 and
run-13 are frozen and neither is edited.

    .venv/bin/python paper-v4/experiment-v4/run-14/pin.py --commit <sha>
"""

from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTRACT = HERE / "run-contract.json"
MANIFEST = HERE / "producer-input-manifest.json"

RUN_ID = "run-14"
PROTOCOL_VERSION = "v4.8"
INTERFACE_ORDINAL = "14"
PRODUCER_WORKSPACE = f"private/paper-v4-v4-{RUN_ID}/producer"

# The v4.1 to v4.7 coordinates the earlier cells ran at. All seven are fixed
# commits: the carried Core-12 entry reads what the enum gained between the
# first two, the carried Core-13 entry what it gained between the second and the
# third, the carried Core-14 entry what it gained between the third and the
# fourth, the carried Core-15 entry what the adapter and the skill gained
# between the fourth and the fifth, the carried Core-16 entry what they gained
# between the fifth and the sixth, the carried Core-17 entry what they gained
# between the sixth and the seventh, and Core-18 owns everything after the
# seventh, so no reason is attributed to the wrong Core task at a later pin.
V4_1_BASELINE_COMMIT = "8b806f7411e11b84e1156cea84b4b641d701db19"
V4_2_COMMIT = "f59477154a2b20f9ffbf6b1f72f6104ee2e1f6c5"
V4_3_COMMIT = "f6c8c71fd95711fd8f1bec811dff94cd61e535a0"
V4_4_COMMIT = "2026244516aa2c5bdc14ae0fea5c4242f5e7f31f"
V4_5_COMMIT = "9d789f2a2ab0d02d6de995acfd922e9a3e8eefd5"
V4_6_COMMIT = "90abc7916a92511e9c5202b591bc60fafab332d3"
V4_7_COMMIT = "12a04a9f033d890663398e1249b4e91c1ed6da7f"

SKILL_PATH = ".claude/skills/malleus-acolyte/SKILL.md"
GOVERNANCE_STATUS = "design/contract_compiler/overseer/status.md"
DOCUMENT_ADAPTER = "src/malleus/_contract_pipeline/document.py"
ELABORATOR = "src/malleus/_contract_pipeline/elaborate.py"
PLAN_COMPILER = "src/malleus/_contract_pipeline/population.py"
RITE_MODULE = "src/malleus/inquisition/pack_grounding.py"
GROUNDING_RITE = "src/malleus/inquisition/pack-grounding.json"
PROFILE_PATH = "src/malleus/profiles/source-assertion.json"

# The seed scalar ranges the elaborator binds. The v4.3 RCA's second ride-along
# asks the INVALID_RANGE refusal to name them. The pin records the refusal's
# message text verbatim, whether that text moved off the v4.3 coordinate, and
# whether one of these names is literally in it. Only the first two are facts
# about the change: a message that names the ranges through a joined constant
# reads false on the third, which is why the text itself is recorded beside it.
SEED_SCALAR_RANGES = ("Boolean", "DateTime", "Float", "Integer", "String")

# Name, tracked source path, workspace target. The eight are run-04's, in
# run-04's order, and the reading is the one input that is untracked.
DECLARED_INPUTS = (
    ("MALLEUS_NASCENT_PROJECT_SKILL", SKILL_PATH, SKILL_PATH),
    (
        "SELECTED_READING",
        "private/paper-v4-text-layer/selected-reading.json",
        "inputs/selected-reading.json",
    ),
    ("MALLEUS_ROOT", "ontology/malleus.yaml", "inputs/malleus.yaml"),
    (
        "LINKML_TYPES",
        "paper-v4/experiment-v2/run-inputs/linkml-types.yaml",
        "inputs/linkml-types.yaml",
    ),
    ("METROLOGY_PACK", "ontology/packs/metrology.yaml", "inputs/metrology.yaml"),
    ("CHRONOLOGY_PACK", "ontology/packs/chronology.yaml", "inputs/chronology.yaml"),
    ("RESEARCH_PACK", "ontology/packs/research.yaml", "inputs/research.yaml"),
    (
        "SOURCE_ASSERTION_PROFILE",
        PROFILE_PATH,
        "inputs/profile-source-assertion.json",
    ),
)
UNTRACKED_INPUTS = {"SELECTED_READING"}
PACKS = ("chronology", "metrology", "research")

HEAD_LINE = re.compile(
    r"^Ledger head: `(?P<entry>OVR-\d+)` / `(?P<hash>sha256:[0-9a-f]{64})`", re.M
)
VERSION_LINE = re.compile(r"^version: (?P<version>\S+)\s*$", re.M)
ENUM_MEMBER = re.compile(r"^    (?P<name>[A-Z][A-Z0-9_]*) = \"(?P=name)\"$", re.M)
ENUM_BLOCK = re.compile(
    r"class DocumentAssertionRefusalReason\(str, Enum\):\n(?P<body>(?:    .*\n|\n)*)"
)
INVALID_RANGE_REFUSAL = re.compile(
    r"ElaborationRefusalReason\.INVALID_RANGE,\n(?P<message>(?:[^\n]*\n)*?)\s*\)\n"
)
SUBJECT_NOT_NAMED_REFUSAL = re.compile(
    r"DocumentAssertionRefusalReason\.SUBJECT_NOT_NAMED,\n"
    r"(?P<message>(?:[^\n]*\n)*?)\s*\)\n"
)

# The four dispositions Core-17 leaves on the subject axis. A subject the
# producer set is ``proposed``; a record whose formalizing statement names
# exactly one capture entity and whose subject is unset is ``attachable``, which
# is a report and not an attachment; ``ambiguous`` is a statement naming more
# than one and ``unnamed`` one naming none. ``projected`` is the outcome Core-16
# added and Core-17 withdraws, so the pin records its absence beside the four.
CENSUS_KEYS = ("ambiguous", "attachable", "proposed", "unnamed")
WITHDRAWN_CENSUS_KEY = "projected"
# What the census carried at the v4.6 coordinate, which the carried Core-16
# entry is read against.
PROJECTED_CENSUS_KEYS = ("ambiguous", "projected", "proposed", "unnamed")
# The adapter declares its census outcomes as one module-level tuple and names
# them by constant inside the census function, so the tuple is what the pin
# resolves.
CENSUS_OUTCOMES_NAME = "_SUBJECT_OUTCOMES"

# The two places the adapter asks whether a statement names a form: the
# SUBJECT_NOT_NAMED check and the subject census. Core-18 makes both
# word-bounded through one predicate. The pin resolves each function by AST and
# records which module-level helpers it calls and whether it still tests a form
# for membership in something whose source text names a statement, which is what
# the substring comparison of Core-15 looks like at both sites.
SUBJECT_SITES = ("_subject_defects", "_subject_outcomes")
STATEMENT_TOKEN = "statement"

LANDED = "LANDED"
PENDING = "PENDING_AT_PIN"
CARRIED = "CARRIED_FROM_RUN_13"


class PinRefusal(ValueError):
    """The commit does not carry something the pin must record."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _canonical_digest(data: bytes) -> str:
    """The identity Core gives a canonical JSON artifact, from its bytes."""
    return _digest(
        json.dumps(
            json.loads(data),
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    )


def _git(*arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments], capture_output=True, cwd=ROOT, text=True
    )
    if completed.returncode != 0:
        raise PinRefusal(
            f"git {' '.join(arguments)} refused: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def _git_show(commit: str, path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"], capture_output=True, cwd=ROOT
    )
    if completed.returncode != 0:
        raise PinRefusal(
            f"declared input is not readable at {commit}: {path}"
            f" ({completed.stderr.decode(errors='replace').strip()})"
        )
    return completed.stdout


def _text(commit: str, path: str) -> str:
    return _git_show(commit, path).decode("utf-8")


def governance_head(commit: str) -> dict[str, str]:
    """The ledger head as the overseer status page renders it at ``commit``."""
    match = HEAD_LINE.search(_text(commit, GOVERNANCE_STATUS))
    if match is None:
        raise PinRefusal(f"{GOVERNANCE_STATUS} renders no ledger head at {commit}")
    return {"entry_id": match.group("entry"), "head_hash": match.group("hash")}


def pack_versions(commit: str) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in PACKS:
        match = VERSION_LINE.search(_text(commit, f"ontology/packs/{name}.yaml"))
        if match is None:
            raise PinRefusal(f"pack {name} declares no version at {commit}")
        versions[name] = match.group("version")
    return versions


def refusal_reasons(commit: str) -> list[str]:
    """Every member of the document adapter's refusal enum at ``commit``."""
    block = ENUM_BLOCK.search(_text(commit, DOCUMENT_ADAPTER))
    if block is None:
        raise PinRefusal(f"{DOCUMENT_ADAPTER} declares no refusal enum at {commit}")
    names = sorted(match.group("name") for match in ENUM_MEMBER.finditer(block.group("body")))
    if not names:
        raise PinRefusal(f"the refusal enum at {commit} is empty")
    return names


def invalid_range_messages(commit: str) -> list[str]:
    """The elaborator's INVALID_RANGE refusal messages at ``commit``, verbatim.

    The message text is what a producer reads when its first ontology attempt is
    returned. The pin records it; whether it names the bound ranges is a fact
    about those bytes and not a judgement this script makes.
    """
    source = _text(commit, ELABORATOR)
    messages = [
        " ".join(match.group("message").split())
        for match in INVALID_RANGE_REFUSAL.finditer(source)
    ]
    if not messages:
        raise PinRefusal(f"{ELABORATOR} raises no INVALID_RANGE refusal at {commit}")
    return messages


def subject_not_named_messages(commit: str) -> list[str]:
    """The adapter's SUBJECT_NOT_NAMED refusal messages at ``commit``, verbatim.

    Core-15 widens the check and moves this text; it adds no enum member, so
    the message is the only thing in the adapter that says the change landed.
    The pin records it and compares it against the v4.4 coordinate's; whether a
    given wording is the right wording is not a judgement this script makes.
    """
    source = _text(commit, DOCUMENT_ADAPTER)
    messages = [
        " ".join(match.group("message").split())
        for match in SUBJECT_NOT_NAMED_REFUSAL.finditer(source)
    ]
    if not messages:
        raise PinRefusal(
            f"{DOCUMENT_ADAPTER} raises no SUBJECT_NOT_NAMED refusal at {commit}"
        )
    return messages


def subject_census_keys(commit: str) -> list[str]:
    """The outcomes the subject census files a record under at ``commit``.

    Core-16 added no refusal reason and Core-17 removes none, so the enum
    cannot report either. What is readable in the file is the set of outcomes
    the census counts, declared as one module-level tuple whose members are
    string constants. The pin resolves that tuple and records what it finds;
    it refuses rather than guessing if the declaration is not there.

    Run-12's pin scanned the census function's body for the literals instead
    and found none of them, because the function names the outcomes by
    constant, so its frozen contract records an empty list at a commit where
    Core-16 had landed. Run-12 is frozen and is not edited; this reads the
    declaration.
    """

    tree = ast.parse(_text(commit, DOCUMENT_ADAPTER))
    constants: dict[str, str] = {}
    declared: ast.expr | None = None
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            constants[target.id] = node.value.value
        if target.id == CENSUS_OUTCOMES_NAME:
            declared = node.value
    if not isinstance(declared, (ast.Tuple, ast.List)):
        raise PinRefusal(
            f"{DOCUMENT_ADAPTER} declares no {CENSUS_OUTCOMES_NAME} at {commit}"
        )
    keys: list[str] = []
    for element in declared.elts:
        if isinstance(element, ast.Constant) and isinstance(element.value, str):
            keys.append(element.value)
        elif isinstance(element, ast.Name) and element.id in constants:
            keys.append(constants[element.id])
        else:
            raise PinRefusal(
                f"{CENSUS_OUTCOMES_NAME} at {commit} names an outcome the pin"
                " cannot resolve to a string"
            )
    return sorted(keys)


def subject_site_predicates(commit: str) -> dict[str, dict[str, list[str]]]:
    """How each subject site compares a name against a statement at ``commit``.

    Core-18 adds no refusal reason and removes none, and it declares no new
    constant either: what moves is the predicate the two sites use. For each
    site the pin records the module-level helpers it calls and every membership
    test it still makes against something whose source text names a statement.
    At the v4.7 coordinate each site makes exactly one such test, ``form in
    statement`` in the census and ``form in _compact(statements[assertion_id])
    .casefold()`` in the check; a word-bounded predicate leaves neither. The pin
    refuses rather than guessing if a site is not there to read.
    """

    source = _text(commit, DOCUMENT_ADAPTER)
    tree = ast.parse(source)
    module_functions = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    sites: dict[str, dict[str, list[str]]] = {}
    for name in SUBJECT_SITES:
        node = next(
            (
                candidate
                for candidate in ast.walk(tree)
                if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef))
                and candidate.name == name
            ),
            None,
        )
        if node is None:
            raise PinRefusal(f"{DOCUMENT_ADAPTER} declares no {name} at {commit}")
        sites[name] = {
            "calls": sorted(
                {
                    child.func.id
                    for child in ast.walk(node)
                    if isinstance(child, ast.Call)
                    and isinstance(child.func, ast.Name)
                    and child.func.id in module_functions
                }
            ),
            "statement_membership_tests": sorted(
                {
                    " ".join((ast.get_source_segment(source, child) or "").split())
                    for child in ast.walk(node)
                    if isinstance(child, ast.Compare)
                    and len(child.ops) == 1
                    and isinstance(child.ops[0], ast.In)
                    and STATEMENT_TOKEN
                    in (ast.get_source_segment(source, child.comparators[0]) or "")
                }
            ),
        }
    return sites


def _shared_calls(sites: dict[str, dict[str, list[str]]]) -> set[str]:
    """The module-level helpers both subject sites call."""
    return set.intersection(*(set(site["calls"]) for site in sites.values()))


def _names_a_seed_scalar(messages: list[str]) -> bool:
    return any(name in message for message in messages for name in SEED_SCALAR_RANGES)


REFERENCE_RUN = "run-13"
REFERENCE_MANIFEST = f"paper-v4/experiment-v4/{REFERENCE_RUN}/producer-input-manifest.json"


def _moved_since_reference(declared: list[dict[str, str]]) -> dict[str, object]:
    """Which declared inputs carry other bytes than the v4.7 cell of record's.

    A cell states what its producer read, and a cell that shares an input list
    with an earlier one has to say which of those inputs actually moved. The
    skill moves by design in v4.8; anything else that moved is a fact this run
    records rather than a change it claims.
    """
    reference = {
        item["name"]: item["sha256"]
        for item in json.loads((ROOT / REFERENCE_MANIFEST).read_bytes())[
            "declared_inputs"
        ]
    }
    observed = {item["name"]: item["sha256"] for item in declared}
    if set(observed) != set(reference):
        raise PinRefusal("the declared input set differs from the reference run's")
    return {
        "reference_run": REFERENCE_RUN,
        "reference_manifest": REFERENCE_MANIFEST,
        "moved": sorted(
            name for name in observed if observed[name] != reference[name]
        ),
        "unchanged": sorted(
            name for name in observed if observed[name] == reference[name]
        ),
    }


def build_manifest(commit: str, tree: str, reading: Path) -> dict[str, object]:
    contract = json.loads(CONTRACT.read_bytes())
    declared: list[dict[str, str]] = []
    for name, source, target in DECLARED_INPUTS:
        data = (
            reading.read_bytes()
            if name in UNTRACKED_INPUTS
            else _git_show(commit, source)
        )
        declared.append(
            {
                "name": name,
                "source": source,
                "target": target,
                "sha256": _digest(data),
            }
        )
    return {
        "schema": "malleus.paper-v4.producer-input-manifest/v1",
        "run_id": RUN_ID,
        "status": "FROZEN",
        "producer_workspace": PRODUCER_WORKSPACE,
        "core": {"commit": commit, "tree": tree},
        "interface_coordinates": {
            "capture_id": f"capture:paper-v4:yu-2025:v4:{INTERFACE_ORDINAL}",
            "plan_id": f"plan:paper-v4:yu-2025:v4:{INTERFACE_ORDINAL}",
            "source_id": contract["source"]["source_id"],
        },
        "history_profile": {
            "profile_id": "source-assertion",
            "profile_identity": _canonical_digest(_git_show(commit, PROFILE_PATH)),
            "semantic_unit": "COMPOSITION",
            "origin": "PARTIAL_IMPORT",
        },
        "producer": contract["producer"],
        "input_bytes": {
            "tracked": "GIT_SHOW_AT_CORE_COMMIT",
            "untracked": "PRIVATE_PATH",
            "untracked_inputs": sorted(UNTRACKED_INPUTS),
        },
        "interpreter_preflight": {
            "checked_by": "paper-v4/experiment-v4/run-14/prepare_producer.py",
            "lock": "paper-v4/environment/requirements-cp312-macos-arm64.lock",
            "packages": ["linkml", "linkml-runtime"],
            "recorded_in": "producer-input-receipt.json under interpreter",
        },
        "skill_installer": {
            "method": "WRITE_DECLARED_BYTES_AT_CORE_COMMIT",
            "reason": (
                "the live skill tree is expected to move; the run consumes the"
                " bytes recorded in this manifest"
            ),
            "installed_tree": ".claude/skills",
            "target": SKILL_PATH,
        },
        "declared_inputs": declared,
        "moved_since": _moved_since_reference(declared),
        "forbidden_inputs": contract["producer"]["forbidden_inputs"],
        "session": {
            "fresh": True,
            "single_session": True,
            "delegation": "FORBIDDEN",
            "max_compiler_diagnostic_returns": 2,
            "max_additive_revision_rounds": 2,
            "fallback": "FORBIDDEN",
        },
        "outputs": {
            "ontology_pattern": "work/ontology-attempt-NN.yaml",
            "population": "work/document-population.json",
            "session_log": "work/session-log.md",
            "status": "work/status.json",
        },
    }


def build_verified_pieces(commit: str, tree: str) -> dict[str, object]:
    profile_bytes = _git_show(commit, PROFILE_PATH)
    profile = json.loads(profile_bytes)
    event_role = list(profile["ontology_roles"]["event"])
    base = {"core_commit": commit, "core_tree": tree, "paper_audit": "DIGEST_PINNED"}
    plan_compiler_sha256 = _digest(_git_show(commit, PLAN_COMPILER))
    return {
        "AGGREGATE_REFUSAL_DIAGNOSTICS": {
            **base,
            "governance_entry": "OVR-000395",
            "shape": "ONE_SORTED_DEFECT_SET_PER_REFUSAL",
            "plan_compiler_sha256": plan_compiler_sha256,
            "rite_module_sha256": _digest(_git_show(commit, RITE_MODULE)),
        },
        "DERIVATION_CONTENT_CHECKS": {
            **base,
            "document_adapter_path": DOCUMENT_ADAPTER,
            "document_adapter_sha256": _digest(_git_show(commit, DOCUMENT_ADAPTER)),
            "refusal_reasons": refusal_reasons(commit),
        },
        "EVENT_FAMILY_ADMISSION": {
            **base,
            "profile_id": profile["profile_id"],
            "event_role": event_role,
            "admitted_families": (
                ["entities", "events", "relations"]
                if event_role
                else ["entities", "relations"]
            ),
            "event_participations": (
                "ONLY_WHEN_THE_COMPILED_CONTRACT_DECLARES_EventParticipation"
            ),
            "plan_compiler_sha256": plan_compiler_sha256,
        },
        "FULL_DOMAIN_HISTORY_PROFILE": {
            **base,
            "profile_id": profile["profile_id"],
            "profile_path": PROFILE_PATH,
            "profile_file_sha256": _digest(profile_bytes),
            "profile_sha256": _canonical_digest(profile_bytes),
        },
        "GROUNDED_PACKS_AND_PACK_GROUNDING": {
            **base,
            "grounding_rite_sha256": _digest(_git_show(commit, GROUNDING_RITE)),
            "pack_sha256": {
                name: _digest(_git_show(commit, f"ontology/packs/{name}.yaml"))
                for name in PACKS
            },
            "pack_version": pack_versions(commit),
        },
        "NASCENT_PROJECT_PLAYBOOK": {
            **base,
            "skill_path": SKILL_PATH,
            "skill_sha256": _digest(_git_show(commit, SKILL_PATH)),
        },
    }


def pin(commit_argument: str, reading: Path) -> dict[str, object]:
    commit = _git("rev-parse", f"{commit_argument}^{{commit}}")
    tree = _git("rev-parse", f"{commit}^{{tree}}")
    contract = json.loads(CONTRACT.read_bytes())

    contract["source"]["selected_reading_sha256"] = _digest(reading.read_bytes())
    profile_bytes = _git_show(commit, PROFILE_PATH)
    contract["history"]["profile_sha256"] = _canonical_digest(profile_bytes)

    gate = contract["core_gate"]
    gate["execution_baseline"] = {"core_commit": commit, "core_tree": tree}
    gate["governance_head"] = governance_head(commit)
    gate["verified_pieces"] = build_verified_pieces(commit, tree)
    absent = sorted(set(gate["required_pieces"]) - set(gate["verified_pieces"]))
    if absent:
        raise PinRefusal(f"required pieces are unverified: {', '.join(absent)}")

    changes = {item["id"]: item for item in contract["protocol"]["changes"]}
    observed = pack_versions(commit)
    at_commit = set(refusal_reasons(commit))
    at_v4_2 = set(refusal_reasons(V4_2_COMMIT))
    at_v4_3 = set(refusal_reasons(V4_3_COMMIT))
    at_v4_4 = set(refusal_reasons(V4_4_COMMIT))
    at_v4_5 = set(refusal_reasons(V4_5_COMMIT))
    at_v4_6 = set(refusal_reasons(V4_6_COMMIT))
    at_v4_7 = set(refusal_reasons(V4_7_COMMIT))

    # Carried from run-13, itself carried from run-08. The entry records what
    # v4.2 landed and what the pinned commit now carries, never an expectation
    # of this iteration.
    packs = changes["PACKS_0_3_0"]
    packs["versions"] = {
        name: observed[name] for name in sorted(packs["expected_versions"])
    }
    packs["moved_since_run_08"] = sorted(
        name
        for name, version in packs["versions"].items()
        if version != packs["expected_versions"][name]
    )
    packs["pin_status"] = CARRIED

    # Carried. Its reasons are what the enum gained between its own baseline and
    # the v4.2 coordinate, both fixed commits; the pin only checks that they are
    # still in force here.
    derivation = changes["CORE_12_DERIVATION_CHECKS"]
    derivation["reasons"] = sorted(
        at_v4_2 - set(refusal_reasons(derivation["baseline_commit"]))
    )
    derivation["still_present_at_pin"] = (
        set(derivation["expected_reasons"]) <= at_commit
    )
    derivation["pin_status"] = CARRIED

    # Carried from run-13, where run-09 had it as the change under test. Its
    # reasons are what the enum gained between the v4.2 and the v4.3
    # coordinates, both fixed commits, so nothing Core-18 lands can be read as
    # Core-13's.
    subject = changes["SUBJECT_ELEMENT"]
    subject["versions"] = {
        name: observed[name] for name in sorted(subject["expected_versions"])
    }
    subject["reasons"] = sorted(at_v4_3 - at_v4_2)
    subject["still_present_at_pin"] = set(subject["expected_reasons"]) <= at_commit
    subject["pin_status"] = CARRIED

    # Carried from run-13, where run-10 had it as the change under test. Its
    # reason and both of its ride-alongs are read between the v4.3 and the v4.4
    # coordinates, all fixed commits, so nothing Core-18 lands can be read as
    # Core-14's; the pin only checks that the reason is still in force here.
    modality = changes["CORE_14_MODALITY_SOURCE_OF_TRUTH"]
    modality["reasons"] = sorted(at_v4_4 - at_v4_3)
    messages = invalid_range_messages(V4_4_COMMIT)
    baseline_messages = invalid_range_messages(V4_3_COMMIT)
    modality["invalid_range"] = {
        "path": ELABORATOR,
        "sha256": _digest(_git_show(V4_4_COMMIT, ELABORATOR)),
        "baseline_sha256": _digest(_git_show(V4_3_COMMIT, ELABORATOR)),
        "moved": _digest(_git_show(V4_4_COMMIT, ELABORATOR))
        != _digest(_git_show(V4_3_COMMIT, ELABORATOR)),
        "messages": messages,
        "baseline_messages": baseline_messages,
        "messages_moved": messages != baseline_messages,
        "seed_scalar_name_literal_in_message": _names_a_seed_scalar(messages),
    }
    modality["skill"] = {
        "path": SKILL_PATH,
        "sha256": _digest(_git_show(V4_4_COMMIT, SKILL_PATH)),
        "baseline_sha256": _digest(_git_show(V4_3_COMMIT, SKILL_PATH)),
        "moved": _digest(_git_show(V4_4_COMMIT, SKILL_PATH))
        != _digest(_git_show(V4_3_COMMIT, SKILL_PATH)),
    }
    modality["ride_alongs_observed"] = {
        "ELABORATOR_MOVED_SINCE_THE_V4_3_COORDINATE": modality["invalid_range"][
            "moved"
        ],
        "SKILL_MOVED_SINCE_THE_V4_3_COORDINATE": modality["skill"]["moved"],
    }
    modality["ride_alongs_landed"] = all(
        modality["ride_alongs_observed"].values()
    )
    modality["still_present_at_pin"] = (
        set(modality["expected_reasons"]) <= at_commit
    )
    modality["pin_status"] = CARRIED

    # Carried from run-13, where run-11 had it as the change under test. Its
    # two byte comparisons stay between the v4.4 and the v4.5 coordinates, both
    # fixed commits, because every Core task after it touches the same two
    # files and a comparison against the pin would report their bytes as
    # Core-15's. Its expectation is empty, so no enum check is possible either
    # way and the entry says so instead of carrying a vacuous subset result.
    aliases = changes["CORE_15_SUBJECT_ALIASES"]
    aliases["reasons"] = sorted(at_v4_5 - at_v4_4)
    aliases_messages = subject_not_named_messages(V4_5_COMMIT)
    aliases_baseline = subject_not_named_messages(V4_4_COMMIT)
    aliases["adapter"] = {
        "path": DOCUMENT_ADAPTER,
        "sha256": _digest(_git_show(V4_5_COMMIT, DOCUMENT_ADAPTER)),
        "baseline_sha256": _digest(_git_show(V4_4_COMMIT, DOCUMENT_ADAPTER)),
        "moved": _digest(_git_show(V4_5_COMMIT, DOCUMENT_ADAPTER))
        != _digest(_git_show(V4_4_COMMIT, DOCUMENT_ADAPTER)),
        "messages": aliases_messages,
        "baseline_messages": aliases_baseline,
        "messages_moved": aliases_messages != aliases_baseline,
    }
    aliases["skill"] = {
        "path": SKILL_PATH,
        "sha256": _digest(_git_show(V4_5_COMMIT, SKILL_PATH)),
        "baseline_sha256": _digest(_git_show(V4_4_COMMIT, SKILL_PATH)),
        "moved": _digest(_git_show(V4_5_COMMIT, SKILL_PATH))
        != _digest(_git_show(V4_4_COMMIT, SKILL_PATH)),
    }
    aliases["observed"] = {
        "ADAPTER_MOVED_SINCE_THE_V4_4_COORDINATE": aliases["adapter"]["moved"],
        "SKILL_MOVED_SINCE_THE_V4_4_COORDINATE": aliases["skill"]["moved"],
    }
    aliases["landed_at_the_v4_5_coordinate"] = all(aliases["observed"].values())
    aliases["expectation"] = "EMPTY_NO_ENUM_CHECK_IS_POSSIBLE"
    aliases["reasons_added"] = aliases["reasons"] != []
    aliases["pin_status"] = CARRIED

    # Carried from run-13, where run-12 had it as the change under test. Its
    # two byte comparisons stay between the v4.5 and the v4.6 coordinates, both
    # fixed commits, because every Core task after it rewrites the same adapter
    # and the same skill and a comparison against the pin would report their
    # bytes as Core-16's. Its census keys stay at the v4.6 coordinate for the
    # same reason: the four it added are what v4.6 carried, not what this pin
    # does.
    projected = changes["CORE_16_PROJECTED_SUBJECT"]
    projected["reasons"] = sorted(at_v4_6 - at_v4_5)
    projected_messages = subject_not_named_messages(V4_6_COMMIT)
    projected_baseline = subject_not_named_messages(V4_5_COMMIT)
    projected["adapter"] = {
        "path": DOCUMENT_ADAPTER,
        "sha256": _digest(_git_show(V4_6_COMMIT, DOCUMENT_ADAPTER)),
        "baseline_sha256": _digest(_git_show(V4_5_COMMIT, DOCUMENT_ADAPTER)),
        "moved": _digest(_git_show(V4_6_COMMIT, DOCUMENT_ADAPTER))
        != _digest(_git_show(V4_5_COMMIT, DOCUMENT_ADAPTER)),
        "messages": projected_messages,
        "baseline_messages": projected_baseline,
        "messages_moved": projected_messages != projected_baseline,
    }
    projected["skill"] = {
        "path": SKILL_PATH,
        "sha256": _digest(_git_show(V4_6_COMMIT, SKILL_PATH)),
        "baseline_sha256": _digest(_git_show(V4_5_COMMIT, SKILL_PATH)),
        "moved": _digest(_git_show(V4_6_COMMIT, SKILL_PATH))
        != _digest(_git_show(V4_5_COMMIT, SKILL_PATH)),
    }
    projected["observed"] = {
        "ADAPTER_MOVED_SINCE_THE_V4_5_COORDINATE": projected["adapter"]["moved"],
        "SKILL_MOVED_SINCE_THE_V4_5_COORDINATE": projected["skill"]["moved"],
    }
    projected["census_keys"] = list(PROJECTED_CENSUS_KEYS)
    projected["census_keys_at_the_v4_6_coordinate"] = subject_census_keys(
        V4_6_COMMIT
    )
    projected["census_keys_present"] = projected[
        "census_keys_at_the_v4_6_coordinate"
    ] == list(PROJECTED_CENSUS_KEYS)
    projected["landed_at_the_v4_6_coordinate"] = all(projected["observed"].values())
    projected["expectation"] = "EMPTY_NO_ENUM_CHECK_IS_POSSIBLE"
    projected["reasons_added"] = projected["reasons"] != []
    projected["pin_status"] = CARRIED

    # Carried from run-13, where it was the change under test. Its two byte
    # comparisons are now read between the v4.6 and the v4.7 coordinates, both
    # fixed commits, because Core-18 rewrites the same adapter and the same
    # skill and a comparison against the pin would report Core-18's bytes as
    # Core-17's. Its census keys are read at the v4.7 coordinate for the same
    # reason: the four that survive the withdrawal are what v4.7 carried, not
    # what this pin does.
    withdrawn = changes["CORE_17_PROJECTION_WITHDRAWN"]
    withdrawn["reasons"] = sorted(at_v4_7 - at_v4_6)
    withdrawn_messages = subject_not_named_messages(V4_7_COMMIT)
    withdrawn_baseline = subject_not_named_messages(V4_6_COMMIT)
    withdrawn["adapter"] = {
        "path": DOCUMENT_ADAPTER,
        "sha256": _digest(_git_show(V4_7_COMMIT, DOCUMENT_ADAPTER)),
        "baseline_sha256": _digest(_git_show(V4_6_COMMIT, DOCUMENT_ADAPTER)),
        "moved": _digest(_git_show(V4_7_COMMIT, DOCUMENT_ADAPTER))
        != _digest(_git_show(V4_6_COMMIT, DOCUMENT_ADAPTER)),
        "messages": withdrawn_messages,
        "baseline_messages": withdrawn_baseline,
        "messages_moved": withdrawn_messages != withdrawn_baseline,
    }
    withdrawn["skill"] = {
        "path": SKILL_PATH,
        "sha256": _digest(_git_show(V4_7_COMMIT, SKILL_PATH)),
        "baseline_sha256": _digest(_git_show(V4_6_COMMIT, SKILL_PATH)),
        "moved": _digest(_git_show(V4_7_COMMIT, SKILL_PATH))
        != _digest(_git_show(V4_6_COMMIT, SKILL_PATH)),
    }
    withdrawn["observed"] = {
        "ADAPTER_MOVED_SINCE_THE_V4_6_COORDINATE": withdrawn["adapter"]["moved"],
        "SKILL_MOVED_SINCE_THE_V4_6_COORDINATE": withdrawn["skill"]["moved"],
    }
    withdrawn["census_keys"] = list(CENSUS_KEYS)
    withdrawn["withdrawn_census_key"] = WITHDRAWN_CENSUS_KEY
    withdrawn["census_keys_at_the_v4_7_coordinate"] = subject_census_keys(
        V4_7_COMMIT
    )
    withdrawn["census_keys_present"] = withdrawn[
        "census_keys_at_the_v4_7_coordinate"
    ] == list(CENSUS_KEYS)
    withdrawn["projection_withdrawn_at_the_v4_7_coordinate"] = (
        WITHDRAWN_CENSUS_KEY
        not in withdrawn["census_keys_at_the_v4_7_coordinate"]
    )
    withdrawn["landed_at_the_v4_7_coordinate"] = all(withdrawn["observed"].values())
    withdrawn["expectation"] = "EMPTY_NO_ENUM_CHECK_IS_POSSIBLE"
    withdrawn["reasons_added"] = withdrawn["reasons"] != []
    withdrawn["pin_status"] = CARRIED

    # This cell's Core change, and a clarification. Everything the adapter and
    # the skill gain or lose after the v4.7 coordinate belongs to it. It adds no
    # refusal reason, removes none and declares no new constant, so neither the
    # enum nor the census keys can report it: what moves is the predicate the
    # two subject sites use. The pin resolves both sites by AST at the pinned
    # commit and at the v4.7 coordinate, and LANDED requires all four of the
    # adapter moved, the skill moved, one module-level predicate called at both
    # sites that neither called at the v4.7 coordinate, and no membership test
    # against a statement left at either site. Anything less reads PENDING.
    bounded = changes["CORE_18_NAME_AS_WORD"]
    bounded["reasons"] = sorted(at_commit - at_v4_7)
    bounded_messages = subject_not_named_messages(commit)
    bounded_baseline = subject_not_named_messages(V4_7_COMMIT)
    bounded["adapter"] = {
        "path": DOCUMENT_ADAPTER,
        "sha256": _digest(_git_show(commit, DOCUMENT_ADAPTER)),
        "baseline_sha256": _digest(_git_show(V4_7_COMMIT, DOCUMENT_ADAPTER)),
        "moved": _digest(_git_show(commit, DOCUMENT_ADAPTER))
        != _digest(_git_show(V4_7_COMMIT, DOCUMENT_ADAPTER)),
        "messages": bounded_messages,
        "baseline_messages": bounded_baseline,
        "messages_moved": bounded_messages != bounded_baseline,
    }
    bounded["skill"] = {
        "path": SKILL_PATH,
        "sha256": _digest(_git_show(commit, SKILL_PATH)),
        "baseline_sha256": _digest(_git_show(V4_7_COMMIT, SKILL_PATH)),
        "moved": _digest(_git_show(commit, SKILL_PATH))
        != _digest(_git_show(V4_7_COMMIT, SKILL_PATH)),
    }
    sites = subject_site_predicates(commit)
    baseline_sites = subject_site_predicates(V4_7_COMMIT)
    added = sorted(_shared_calls(sites) - _shared_calls(baseline_sites))
    substring_left = sorted(
        name
        for name, site in sites.items()
        if site["statement_membership_tests"]
    )
    bounded["sites_at_pin"] = sites
    bounded["sites_at_the_v4_7_coordinate"] = baseline_sites
    bounded["bounded_predicate"] = added
    bounded["bounded_predicate_at_both_sites"] = added != []
    bounded["substring_test_left_at"] = substring_left
    bounded["substring_test_absent"] = substring_left == []
    bounded["census_keys"] = list(CENSUS_KEYS)
    bounded["census_keys_at_pin"] = subject_census_keys(commit)
    bounded["census_keys_present"] = bounded["census_keys_at_pin"] == list(
        CENSUS_KEYS
    )
    bounded["observed"] = {
        "ADAPTER_MOVED_SINCE_THE_V4_7_COORDINATE": bounded["adapter"]["moved"],
        "SKILL_MOVED_SINCE_THE_V4_7_COORDINATE": bounded["skill"]["moved"],
        "ONE_PREDICATE_AT_BOTH_SUBJECT_SITES": bounded[
            "bounded_predicate_at_both_sites"
        ],
        "NO_SUBSTRING_TEST_LEFT_AT_EITHER_SITE": bounded["substring_test_absent"],
    }
    bounded["pin_status"] = LANDED if all(bounded["observed"].values()) else PENDING
    bounded["reasons_added"] = bounded["reasons"] != []

    pending = [bounded["core_task"]] if bounded["pin_status"] != LANDED else []
    for carried in (derivation, subject, modality):
        if not carried["still_present_at_pin"]:
            pending.append(carried["core_task"])
    gate["status"] = (
        "PINNED_TO_THE_V4_8_CORE_COORDINATE"
        if not pending
        else "PROVISIONALLY_PINNED_PENDING_"
        + "_AND_".join(task.upper().replace("-", "_") for task in pending)
    )

    manifest = build_manifest(commit, tree, reading)
    MANIFEST.write_bytes(
        json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )
    CONTRACT.write_bytes(
        json.dumps(contract, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )
    return {
        "commit": commit,
        "tree": tree,
        "governance_head": gate["governance_head"],
        "pack_versions": observed,
        "core_12_reasons": derivation["reasons"],
        "core_13_reasons": subject["reasons"],
        "core_14_reasons": modality["reasons"],
        "core_14_pin_status": modality["pin_status"],
        "core_15_reasons": aliases["reasons"],
        "core_15_pin_status": aliases["pin_status"],
        "core_15_landed_at_the_v4_5_coordinate": aliases[
            "landed_at_the_v4_5_coordinate"
        ],
        "core_16_reasons": projected["reasons"],
        "core_16_pin_status": projected["pin_status"],
        "core_16_landed_at_the_v4_6_coordinate": projected[
            "landed_at_the_v4_6_coordinate"
        ],
        "core_16_census_keys_at_the_v4_6_coordinate": projected[
            "census_keys_at_the_v4_6_coordinate"
        ],
        "core_17_reasons": withdrawn["reasons"],
        "core_17_pin_status": withdrawn["pin_status"],
        "core_17_landed_at_the_v4_7_coordinate": withdrawn[
            "landed_at_the_v4_7_coordinate"
        ],
        "core_17_census_keys_at_the_v4_7_coordinate": withdrawn[
            "census_keys_at_the_v4_7_coordinate"
        ],
        "core_18_reasons": bounded["reasons"],
        "core_18_pin_status": bounded["pin_status"],
        "core_18_adapter_moved": bounded["adapter"]["moved"],
        "core_18_adapter_messages_moved": bounded["adapter"]["messages_moved"],
        "core_18_skill_moved": bounded["skill"]["moved"],
        "core_18_bounded_predicate": bounded["bounded_predicate"],
        "core_18_substring_test_left_at": bounded["substring_test_left_at"],
        "core_18_census_keys_at_pin": bounded["census_keys_at_pin"],
        "core_gate_status": gate["status"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True, help="the Core commit to pin to")
    parser.add_argument(
        "--reading",
        type=Path,
        default=ROOT / "private/paper-v4-text-layer/selected-reading.json",
        help="the untracked selected reading",
    )
    arguments = parser.parse_args(argv)
    try:
        report = pin(arguments.commit, arguments.reading)
    except (OSError, TypeError, ValueError) as error:
        print(f"pin: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
