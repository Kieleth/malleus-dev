"""Pin shop-01 to one Core commit and write the manifest and the gate block.

This is run-21's pin with the readers carried whole and the cell's own facts
written around them. The readers are what makes a Core entry a fact rather than
a recollection: they resolve the governance head, the pack versions, the two
refusal enums, the adapter's subject sites by AST, the block census labels and
the skill's pre-flight paragraph, all at the commit this cell pins.
``test_pipeline.py`` holds the whole span against run-21's bytes under one table
that reverses, so a reader that drifts fails there rather than travelling here.

What is not carried is everything that names the document cell's inputs. This
cell declares twelve inputs, not eight: the five Small Shop source files replace
the selected reading, and the bound history profile is the shipped
``state-version`` profile the Small Shop fixture itself declares, not
``source-assertion``. Every one of the twelve is tracked, so nothing is read
from a private path and ``--reading`` is gone.

Two gate pieces move with the source shape. ``DERIVATION_CONTENT_CHECKS`` is the
document adapter's, and it does not bind a run whose plans are written by the
producer: what binds is the plan compiler, so the piece this cell requires is
``PLAN_DERIVATION_CHECKS`` and the reasons it records are the plan compiler's
own. ``STRUCTURAL_HISTORY_BUNDLE`` is new: the runner admits through the shipped
bundle rather than through a fixture's assembled machine, and the four files
that bundle is built from are pinned here by digest.

Nothing here is typed by hand. A pack version that has not moved is recorded as
it stands and the change entry says so.

    .venv/bin/python paper-v4/experiment-v4/shop-01/pin.py --commit <sha>
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

RUN_ID = "shop-01"
PROTOCOL_VERSION = "v4.10"
INTERFACE_ORDINAL = "1"
PRODUCER_WORKSPACE = f"private/paper-v4-v4-{RUN_ID}/producer"

# The v4.1 to v4.8 coordinates the document cells ran at. This cell reads Core
# at two of them only: the v4.8 coordinate, which is the baseline the two
# carried entries are read against, and the commit it pins, which is the commit
# run-21 pinned. No entry here reads what the document adapter gained between
# the earlier coordinates, because no entry here claims one.
V4_8_COMMIT = "dc5254795a78648591d3a1b0bcf602af8d443dc1"

SKILL_PATH = ".claude/skills/malleus-acolyte/SKILL.md"
GOVERNANCE_STATUS = "design/contract_compiler/overseer/status.md"
DOCUMENT_ADAPTER = "src/malleus/_contract_pipeline/document.py"
PLAN_COMPILER = "src/malleus/_contract_pipeline/population.py"
RITE_MODULE = "src/malleus/inquisition/pack_grounding.py"
GROUNDING_RITE = "src/malleus/inquisition/pack-grounding.json"
PROFILE_PATH = "src/malleus/profiles/state-version.json"
# The four shipped files ``STRUCTURAL_HISTORY_BUNDLE`` is composed from. The
# runner admits through that bundle, so a cell that did not pin them would be
# reporting an admission path it never fixed.
BUNDLE_PATHS = (
    "src/malleus/profiles/structural-admission-check.json",
    "src/malleus/profiles/structural-admission-policy.json",
    "src/malleus/profiles/structural-history-binding.json",
    "src/malleus/profiles/structural-history-machine.json",
)

# The five Small Shop source files, verbatim, at the paths the fixture reads
# them from. They are the evidence surface of this cell and they are tracked, so
# the producer's inputs are reproducible from the commit alone.
SOURCE_FILES = (
    (
        "SOURCE_WAREHOUSE",
        "source:small-shop:warehouse",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment"
        "/input/sources/warehouse.jsonl",
        "inputs/sources/warehouse.jsonl",
        "application/x-ndjson",
    ),
    (
        "SOURCE_INVENTORY",
        "source:small-shop:inventory",
        "research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment"
        "/input/sources/inventory-units.csv",
        "inputs/sources/inventory-units.csv",
        "text/csv",
    ),
    (
        "SOURCE_INVOICES",
        "source:small-shop:invoices",
        "research/ontology_driven_kg_realization/fixtures"
        "/small_shop_fulfilment_settlement_v1/input/sources/invoices.csv",
        "inputs/sources/invoices.csv",
        "text/csv",
    ),
    (
        "SOURCE_PAYMENTS",
        "source:small-shop:payments",
        "research/ontology_driven_kg_realization/fixtures"
        "/small_shop_fulfilment_settlement_v1/input/sources/payments.jsonl",
        "inputs/sources/payments.jsonl",
        "application/x-ndjson",
    ),
    (
        "SOURCE_SUPPLIER_ORDERS",
        "source:small-shop:supplier-orders",
        "research/ontology_driven_kg_realization/fixtures"
        "/small_shop_fulfilment_correction_v1/input/sources"
        "/supplier-order-history.jsonl",
        "inputs/sources/supplier-order-history.jsonl",
        "application/x-ndjson",
    ),
)

# Name, tracked source path, workspace target. Twelve, in run-21's order with
# the five source files where the reading was.
DECLARED_INPUTS = (
    ("MALLEUS_NASCENT_PROJECT_SKILL", SKILL_PATH, SKILL_PATH),
    *((name, source, target) for name, _, source, target, _ in SOURCE_FILES),
    ("MALLEUS_ROOT", "ontology/malleus.yaml", "inputs/malleus.yaml"),
    (
        "LINKML_TYPES",
        "paper-v4/experiment-v2/run-inputs/linkml-types.yaml",
        "inputs/linkml-types.yaml",
    ),
    ("METROLOGY_PACK", "ontology/packs/metrology.yaml", "inputs/metrology.yaml"),
    ("CHRONOLOGY_PACK", "ontology/packs/chronology.yaml", "inputs/chronology.yaml"),
    ("RESEARCH_PACK", "ontology/packs/research.yaml", "inputs/research.yaml"),
    ("STATE_VERSION_PROFILE", PROFILE_PATH, "inputs/profile-state-version.json"),
)
UNTRACKED_INPUTS: frozenset[str] = frozenset()
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
# run-18 addition begins: the Core-19 and Core-20 constants

# Core-19's reporting shapes, all read by AST at the pinned commit and at the
# v4.8 coordinate. The three block labels are string constants inside the
# block census, which declares no module-level tuple the way the subject axis
# does, so the pin walks that function and records every label-shaped constant
# it finds rather than looking for the three it expects. ``provenance_coverage``
# is the key the adapter writes beside them. The aggregation of GAP_REQUIRED
# cannot be read from the enum, which carries that reason at both coordinates:
# what the AST can see is the pre-pass that collects every empty assertion and
# the refusal that renders them as one, both module-level functions, and that is
# what the entry records and says it records.
BLOCK_CENSUS_NAME = "_block_census"
BLOCK_CENSUS_LABELS = ("ASSERTED", "DECLARED_NOTHING_ASSERTABLE", "UNTOUCHED")
LABEL_SHAPE = re.compile(r"[A-Z][A-Z0-9_]*$")
PROVENANCE_CENSUS_KEY = "provenance_coverage"
GAP_AGGREGATION_NAMES = ("_empty_assertion_defects", "_refuse_gaps")
REHYDRATION_REASON = "RECORDS_NOT_REHYDRATABLE"
POPULATION_ENUM_BLOCK = re.compile(
    r"class PopulationPlanRefusalReason\(str, Enum\):\n(?P<body>(?:    .*\n|\n)*)"
)

# Core-20's pre-flight. The skill gains one paragraph between two marker
# comments, one line per refusal reason with the check in plain words, and
# ``tests/test_inquisition.py`` derives the names from the two enums so the
# paragraph cannot drift from Core. Neither enum gains a member, so neither can
# report the change; the paragraph and the guard are the whole of what is
# readable. The pin reads the marker from the skill and records whether the
# guard names the same one, so a rename is a recorded fact and not a silent
# PENDING.
PREFLIGHT_MARKER = "malleus-preflight-refusals"
PREFLIGHT_TOKEN = re.compile(r"[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+")
INQUISITION_GUARD = "tests/test_inquisition.py"
REFUSAL_ENUM_NAMES = (
    "DocumentAssertionRefusalReason",
    "PopulationPlanRefusalReason",
)

# The two statuses the Core entries carried from run-21 can read. Both landed
# before that cell closed and are read again here at the same commit.
LANDED = "LANDED"
PENDING = "PENDING_AT_PIN"
# run-18 addition ends: the Core-19 and Core-20 constants

# The status of every entry this cell carries unchanged from run-21. Two of them
# are Core-19 and Core-20, which read LANDED or PENDING_AT_PIN instead, off the
# bytes between the v4.8 coordinate and the commit run-21 pinned, which is the
# commit this cell pins.
CARRIED = "CARRIED_FROM_RUN_21"


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
# run-18 addition begins: the readers Core-19 and Core-20 are pinned by


def _optional_text(commit: str, path: str) -> str:
    """``path`` at ``commit``, or the empty string when it is not there yet.

    Core-20's guard landed before this cell opened, and the reader stays
    tolerant: an absent file is a fact about the change's status and not a
    reason to refuse the pin, which is why this reader does not raise.
    """
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"], capture_output=True, cwd=ROOT
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.decode("utf-8")


def population_refusal_reasons(commit: str) -> list[str]:
    """Every member of the plan compiler's refusal enum at ``commit``."""
    block = POPULATION_ENUM_BLOCK.search(_text(commit, PLAN_COMPILER))
    if block is None:
        raise PinRefusal(f"{PLAN_COMPILER} declares no refusal enum at {commit}")
    names = sorted(
        match.group("name") for match in ENUM_MEMBER.finditer(block.group("body"))
    )
    if not names:
        raise PinRefusal(f"the population refusal enum at {commit} is empty")
    return names


def module_functions(commit: str, path: str) -> set[str]:
    """The module-level functions ``path`` declares at ``commit``."""
    return {
        node.name
        for node in ast.parse(_text(commit, path)).body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def block_census_labels(commit: str) -> list[str]:
    """The labels the block census writes at ``commit``, read from its body.

    The subject axis declares ``_SUBJECT_OUTCOMES`` at module level; the block
    census names its labels as string constants inside the function instead.
    The pin resolves the function by name and records every label-shaped
    constant in it, so a fourth label is reported rather than hidden by a check
    for the three this cell expects. A commit with no such function has no
    labels, which is what the coordinate before Core-19 reads.
    """
    tree = ast.parse(_text(commit, DOCUMENT_ADAPTER))
    node = next(
        (
            candidate
            for candidate in tree.body
            if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef))
            and candidate.name == BLOCK_CENSUS_NAME
        ),
        None,
    )
    if node is None:
        return []
    return sorted(
        {
            child.value
            for child in ast.walk(node)
            if isinstance(child, ast.Constant)
            and isinstance(child.value, str)
            and LABEL_SHAPE.match(child.value)
        }
    )


def census_key_written(commit: str, key: str) -> bool:
    """Whether the adapter writes ``key`` as a literal at ``commit``."""
    return any(
        isinstance(node, ast.Constant) and node.value == key
        for node in ast.walk(ast.parse(_text(commit, DOCUMENT_ADAPTER)))
    )


def preflight_paragraph(skill_text: str) -> str | None:
    """The skill's pre-flight paragraph, or None when the markers are absent."""
    start = f"<!-- {PREFLIGHT_MARKER}:start -->"
    end = f"<!-- {PREFLIGHT_MARKER}:end -->"
    if start not in skill_text or end not in skill_text:
        return None
    return skill_text.split(start, 1)[1].split(end, 1)[0]


def preflight_observation(
    skill_text: str, guard_text: str, reasons: list[str]
) -> dict[str, object]:
    """What the skill's paragraph and Core's guard carry of the refusal list."""
    paragraph = preflight_paragraph(skill_text)
    named = sorted(set(PREFLIGHT_TOKEN.findall(paragraph or "")))
    missing = sorted(set(reasons) - set(named))
    invented = sorted(set(named) - set(reasons))
    enums = sorted(name for name in REFUSAL_ENUM_NAMES if name in guard_text)
    return {
        "marker": PREFLIGHT_MARKER,
        "paragraph_present": paragraph is not None,
        "reasons_at_pin": sorted(reasons),
        "reasons_named_in_the_paragraph": named,
        "reasons_absent_from_the_paragraph": missing,
        "reasons_the_paragraph_invents": invented,
        "every_reason_named": paragraph is not None and missing == [],
        "no_other_reason_named": paragraph is not None and invented == [],
        "guard_path": INQUISITION_GUARD,
        "guard_names_the_marker": PREFLIGHT_MARKER in guard_text,
        "enums_named_in_the_guard": enums,
        "guard_derives_from_both_enums": enums == sorted(REFUSAL_ENUM_NAMES),
    }


def preflight_status(observation: dict[str, object]) -> str:
    """LANDED only when the paragraph carries the whole list and the guard derives it.

    A paragraph that omits one reason of either enum is the defect Core-20 is
    for: a producer reading it has nothing to check that reason against before
    it stops. The pin refuses to record such a paragraph as landed, and the
    entry names the reasons that are missing.
    """
    return (
        LANDED
        if all(
            observation[key]
            for key in (
                "paragraph_present",
                "every_reason_named",
                "no_other_reason_named",
                "guard_derives_from_both_enums",
                "guard_names_the_marker",
            )
        )
        else PENDING
    )
# run-18 addition ends: the readers Core-19 and Core-20 are pinned by


REFERENCE_RUN = "run-21"
REFERENCE_MANIFEST = f"paper-v4/experiment-v4/{REFERENCE_RUN}/producer-input-manifest.json"
# The six inputs this cell shares with the document cell it is translated from.
# The other six are this cell's own: the five source files and the state-version
# profile, which no document cell declared, so no earlier manifest can say
# whether they moved and the manifest does not pretend one can.
SHARED_WITH_REFERENCE = (
    "CHRONOLOGY_PACK",
    "LINKML_TYPES",
    "MALLEUS_NASCENT_PROJECT_SKILL",
    "MALLEUS_ROOT",
    "METROLOGY_PACK",
    "RESEARCH_PACK",
)


def _moved_since_reference(declared: list[dict[str, str]]) -> dict[str, object]:
    """Which shared inputs carry other bytes than run-21's producer read.

    A cell states what its producer read, and a cell that shares inputs with an
    earlier one has to say which of those actually moved. Six of the twelve are
    run-21's; the pin compares those six and names the other six as this cell's
    own rather than reporting them as unchanged against a manifest that never
    carried them.
    """
    reference = {
        item["name"]: item["sha256"]
        for item in json.loads((ROOT / REFERENCE_MANIFEST).read_bytes())[
            "declared_inputs"
        ]
    }
    observed = {item["name"]: item["sha256"] for item in declared}
    absent = sorted(set(SHARED_WITH_REFERENCE) - set(reference))
    if absent:
        raise PinRefusal(
            f"the reference run declares none of: {', '.join(absent)}"
        )
    shared = sorted(SHARED_WITH_REFERENCE)
    return {
        "reference_run": REFERENCE_RUN,
        "reference_manifest": REFERENCE_MANIFEST,
        "shared_with_reference": shared,
        "moved": sorted(
            name for name in shared if observed[name] != reference[name]
        ),
        "unchanged": sorted(
            name for name in shared if observed[name] == reference[name]
        ),
        "not_in_the_reference": sorted(set(observed) - set(SHARED_WITH_REFERENCE)),
    }


def build_manifest(commit: str, tree: str) -> dict[str, object]:
    contract = json.loads(CONTRACT.read_bytes())
    declared = [
        {
            "name": name,
            "source": source,
            "target": target,
            "sha256": _digest(_git_show(commit, source)),
        }
        for name, source, target in DECLARED_INPUTS
    ]
    return {
        "schema": "malleus.paper-v4.producer-input-manifest/v1",
        "run_id": RUN_ID,
        "status": "FROZEN",
        "producer_workspace": PRODUCER_WORKSPACE,
        "core": {"commit": commit, "tree": tree},
        "interface_coordinates": {
            "capture_id": f"capture:paper-v4:small-shop:shop:{INTERFACE_ORDINAL}",
            "capture_id_role": (
                "RESERVED_THE_PLAN_PATH_PRODUCES_NO_CAPTURE_RECORD"
            ),
            "plan_id": f"plan:paper-v4:small-shop:shop:{INTERFACE_ORDINAL}",
            "plan_id_role": "PREFIX_EVERY_PLAN_ID_SITS_UNDER_IT",
            "source_ids": [source_id for _, source_id, _, _, _ in SOURCE_FILES],
            "contract_identity": (
                "SUPPLIED_AT_PHASE_TWO_FROM"
                " paper-v4/experiment-v4/shop-01/contract_identity.py"
            ),
        },
        "history_profile": {
            "profile_id": "state-version",
            "profile_identity": _canonical_digest(_git_show(commit, PROFILE_PATH)),
            "semantic_unit": "STATE_VERSION",
            "origin": "EMPTY",
        },
        "producer": contract["producer"],
        "input_bytes": {
            "tracked": "GIT_SHOW_AT_CORE_COMMIT",
            "untracked": "NONE_EVERY_DECLARED_INPUT_OF_THIS_CELL_IS_TRACKED",
            "untracked_inputs": sorted(UNTRACKED_INPUTS),
        },
        "interpreter_preflight": {
            "checked_by": "paper-v4/experiment-v4/shop-01/prepare_producer.py",
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
            "population": "work/population-plans/",
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
        "PLAN_DERIVATION_CHECKS": {
            **base,
            "plan_compiler_path": PLAN_COMPILER,
            "plan_compiler_sha256": plan_compiler_sha256,
            "refusal_reasons": population_refusal_reasons(commit),
            "field_level_checks": [
                "ABSENT_PATH",
                "UNDERIVED_FIELD",
                "UNLISTED_SOURCE",
                "UNRETAINED_SOURCE",
            ],
            "not_checked_by_core": "THE_LOCATOR_IS_FREE_TEXT_AND_IS_NOT_RESOLVED"
            "_AGAINST_THE_SOURCE_BYTES",
            "document_adapter_note": (
                "the document adapter's derivation content checks are"
                " DIGEST_MISMATCH, NOT_VERBATIM and their kin; they bind a"
                " document capture and not a plan the producer wrote, so this"
                " cell does not carry them as a verified piece"
            ),
            "document_adapter_sha256": _digest(_git_show(commit, DOCUMENT_ADAPTER)),
        },
        "STRUCTURAL_HISTORY_BUNDLE": {
            **base,
            "admission_path": "CREATE_STRUCTURAL_HISTORY_THEN_ADMIT_STRUCTURAL_CHANGE",
            "file_sha256": {
                path: _digest(_git_show(commit, path)) for path in BUNDLE_PATHS
            },
        },
    }


def pin(commit_argument: str) -> dict[str, object]:
    commit = _git("rev-parse", f"{commit_argument}^{{commit}}")
    tree = _git("rev-parse", f"{commit}^{{tree}}")
    contract = json.loads(CONTRACT.read_bytes())

    profile_bytes = _git_show(commit, PROFILE_PATH)
    contract["history"]["profile_sha256"] = _canonical_digest(profile_bytes)
    contract["source"]["source_sha256"] = {
        source_id: _digest(_git_show(commit, source))
        for _, source_id, source, _, _ in SOURCE_FILES
    }

    gate = contract["core_gate"]
    gate["execution_baseline"] = {"core_commit": commit, "core_tree": tree}
    gate["governance_head"] = governance_head(commit)
    gate["verified_pieces"] = build_verified_pieces(commit, tree)
    absent = sorted(set(gate["required_pieces"]) - set(gate["verified_pieces"]))
    if absent:
        raise PinRefusal(f"required pieces are unverified: {', '.join(absent)}")

    changes = {item["id"]: item for item in contract["protocol"]["changes"]}
    observed = pack_versions(commit)

    # Carried from run-21, itself carried from run-08. The entry records what
    # v4.2 landed and what the pinned commit now carries, never an expectation
    # of this cell.
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

    # Carried from run-21 and not carried unread: the pin recomputes both
    # statuses at the commit run-21 pinned, against the same v4.8 baseline.
    reporting = changes["CORE_19_HONEST_REPORTING"]
    at_v4_8_population = set(population_refusal_reasons(V4_8_COMMIT))
    at_commit_population = set(population_refusal_reasons(commit))
    reporting["reasons"] = sorted(at_commit_population - at_v4_8_population)
    reporting["block_census_labels_at_pin"] = block_census_labels(commit)
    reporting["gap_aggregation_at_pin"] = sorted(
        module_functions(commit, DOCUMENT_ADAPTER) & set(GAP_AGGREGATION_NAMES)
    )
    reporting["observed"] = {
        "document_adapter_moved": (
            _digest(_git_show(commit, DOCUMENT_ADAPTER))
            != _digest(_git_show(V4_8_COMMIT, DOCUMENT_ADAPTER))
        ),
        "plan_compiler_moved": (
            _digest(_git_show(commit, PLAN_COMPILER))
            != _digest(_git_show(V4_8_COMMIT, PLAN_COMPILER))
        ),
        "block_census_declares_the_three_labels": (
            block_census_labels(commit) == sorted(BLOCK_CENSUS_LABELS)
        ),
        "provenance_coverage_written": census_key_written(
            commit, PROVENANCE_CENSUS_KEY
        ),
        "rehydration_reason_present": REHYDRATION_REASON in at_commit_population,
        "gap_aggregation_present": (
            set(GAP_AGGREGATION_NAMES)
            <= module_functions(commit, DOCUMENT_ADAPTER)
        ),
    }
    reporting["pin_status"] = (
        LANDED if all(reporting["observed"].values()) else PENDING
    )
    reporting["binds_this_cell"] = [
        "RECORDS_NOT_REHYDRATABLE_IS_THE_PLAN_COMPILERS_AND_BINDS_THIS_CELL",
        "THE_BLOCK_CENSUS_AND_PROVENANCE_COVERAGE_ARE_THE_DOCUMENT_ADAPTERS"
        "_AND_DO_NOT",
    ]

    preflight = changes["CORE_20_REFUSAL_LIST_PREFLIGHT"]
    document_at_commit = set(refusal_reasons(commit))
    preflight["reasons"] = []
    preflight["document_reasons_at_pin"] = sorted(document_at_commit)
    preflight["population_reasons_at_pin"] = sorted(at_commit_population)
    preflight["skill"] = {
        "path": SKILL_PATH,
        "sha256": _digest(_git_show(commit, SKILL_PATH)),
        "baseline_sha256": _digest(_git_show(V4_8_COMMIT, SKILL_PATH)),
        "moved": _digest(_git_show(commit, SKILL_PATH))
        != _digest(_git_show(V4_8_COMMIT, SKILL_PATH)),
    }
    preflight["observed"] = preflight_observation(
        _text(commit, SKILL_PATH),
        _optional_text(commit, INQUISITION_GUARD),
        sorted(document_at_commit | at_commit_population),
    )
    preflight["expectation"] = "EMPTY_NO_ENUM_CHECK_IS_POSSIBLE"
    preflight["pin_status"] = preflight_status(preflight["observed"])
    # The governance entry is recorded beside the status and never decides it.
    preflight["governance_head_at_pin"] = gate["governance_head"]["entry_id"]
    preflight["governance_entry_landed"] = (
        gate["governance_head"]["entry_id"] != reporting["governance_entry"]
    )

    pending = [
        item["core_task"]
        for item in (reporting, preflight)
        if item["pin_status"] != LANDED
    ]
    if pending:
        gate["status"] = f"PENDING_AT_PIN_{'_AND_'.join(sorted(pending))}"

    manifest = build_manifest(commit, tree)
    MANIFEST.write_bytes(
        json.dumps(manifest, indent=2, sort_keys=False).encode("utf-8") + b"\n"
    )
    CONTRACT.write_bytes(
        json.dumps(contract, indent=2, sort_keys=False).encode("utf-8") + b"\n"
    )
    return {
        "core_commit": commit,
        "core_tree": tree,
        "governance_head": gate["governance_head"],
        "declared_inputs": len(manifest["declared_inputs"]),
        "declared_input_digests": {
            item["name"]: item["sha256"] for item in manifest["declared_inputs"]
        },
        "moved_since_reference": manifest["moved_since"],
        "history_profile": manifest["history_profile"],
        "pack_versions": observed,
        "packs_moved_since_run_08": packs["moved_since_run_08"],
        "plan_refusal_reasons": len(
            gate["verified_pieces"]["PLAN_DERIVATION_CHECKS"]["refusal_reasons"]
        ),
        "structural_bundle_files": sorted(
            gate["verified_pieces"]["STRUCTURAL_HISTORY_BUNDLE"]["file_sha256"]
        ),
        "core_19_pin_status": reporting["pin_status"],
        "core_19_reasons": reporting["reasons"],
        "core_19_observed": reporting["observed"],
        "core_20_pin_status": preflight["pin_status"],
        "core_20_paragraph_present": preflight["observed"]["paragraph_present"],
        "core_20_reasons_absent_from_the_paragraph": preflight["observed"][
            "reasons_absent_from_the_paragraph"
        ],
        "core_20_guard_derives_from_both_enums": preflight["observed"][
            "guard_derives_from_both_enums"
        ],
        "core_20_governance_entry_landed": preflight["governance_entry_landed"],
        "core_gate_status": gate["status"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True, help="the Core commit to pin to")
    arguments = parser.parse_args(argv)
    try:
        report = pin(arguments.commit)
    except (OSError, TypeError, ValueError) as error:
        print(f"pin: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
