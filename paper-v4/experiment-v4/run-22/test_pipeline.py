"""Drive the run-22 harness end to end on the neutral inspection-note fixture.

The fixture is Core's own synthetic document-capture conformance corpus. No paper
reading, ontology, capture or result enters this test, and no model runs.

The producer condition has no delta of any kind and the instruments have three.
Run-22's producer block is run-21's key for key, the three model fields
included, its spawn message is run-21's with the run id moved, and its eight
declared inputs are the same bytes at the same Core commit. What v4.12 moves is
the query and the staging: a fourth case kind that reaches a subject-less record
of a listed subject-bearing type, the closure check moved inside the binder, and
the history profile staged as canonical JSON.

Four files and the spawn message are run-21's with the run id substituted and
nothing else. Four more carry a change, and each of those is read through its
own table, stated once here and reversed, so everything outside a stated table
must reach run-21's bytes exactly and a second edit riding inside a run id move
fails here rather than travelling with the cell.

Core-19 and Core-20 are carried from run-21 and are not carried unread: the pin
still reads them at the commit run-21 pinned, against the same v4.8 baseline,
and both must come back LANDED. Their evidence is a commit and not a file in
this directory, so this file checks only that the pin can still refuse either
and that a pre-flight paragraph missing one refusal reason reads PENDING rather
than LANDED; what the adapter and the skill carry at the pinned commit is
``test_contract.py``'s.

``bind_from_surface.py`` is exercised end to end on a fixture that carries a
``subject`` reference, and that fixture is where the reachability change is
driven: the bearing type still gets no plain ENTITY case, a record of it that
carries a subject is reached through its subject alone, and a record of it that
carries none comes back as one ENTITY row from the new ENTITY_NO_SUBJECT case.
The fixture's subject entity carries ``tags``, so v4.7's carried
SUBJECT_TAGS_PROJECTED delta is exercised on the same run as everything else.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from hashlib import sha256
from importlib.resources import files
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Iterator

import pytest
import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_02 = HERE.parent / "run-02"
RUN_03 = HERE.parent / "run-03"
RUN_04 = HERE.parent / "run-04"
RUN_05 = HERE.parent / "run-05"
RUN_06 = HERE.parent / "run-06"
RUN_07 = HERE.parent / "run-07"
RUN_08 = HERE.parent / "run-08"
RUN_09 = HERE.parent / "run-09"
RUN_21 = HERE.parent / "run-21"
PRIVATE = ROOT / "private"
FIXTURE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "inspection_note_capture_v1"
)
LINKML_TYPES = Path(
    str(
        files("linkml_runtime").joinpath(
            "linkml_model", "model", "schema", "types.yaml"
        )
    )
)
TRANSACTION_TIME = "2026-09-04T00:00:00Z"
ACTOR = "actor:paper-v4-run-22"
SPAWN_MESSAGE = HERE / "spawn-message.md"
CONTRACT_PATH = HERE / "run-contract.json"
OFFLINE_VALIDATION = HERE / "offline-validation.json"

# The one sentence STOP_RULE_CLARIFIED adds to run-04's message.
STOP_RULE_SENTENCE = (
    "Reviewing the next block is not invention; stop only when every block is"
    " REVIEWED or listed in `nothing_assertable`, or when the next addition"
    " would require invention."
)

# The ten changes Core owns. Their evidence is a commit, not a file in this
# directory, so ``pin.py`` records what landed and test_contract recomputes it;
# there is nothing here to grep for. All ten are carried from run-21. Eight of
# them stop at the coordinate run-21 pinned Core-18 at and read
# CARRIED_FROM_RUN_21 and nothing else; Core-19 and Core-20 are carried too but
# are still read, at the commit run-21 pinned and against the same v4.8
# baseline, so those two read LANDED or PENDING_AT_PIN.
CORE_CHANGE_IDS = (
    "CORE_12_DERIVATION_CHECKS",
    "CORE_14_MODALITY_SOURCE_OF_TRUTH",
    "CORE_15_SUBJECT_ALIASES",
    "CORE_16_PROJECTED_SUBJECT",
    "CORE_17_PROJECTION_WITHDRAWN",
    "CORE_18_NAME_AS_WORD",
    "CORE_19_HONEST_REPORTING",
    "CORE_20_REFUSAL_LIST_PREFLIGHT",
    "PACKS_0_3_0",
    "SUBJECT_ELEMENT",
)
# The two the pin still reads rather than carries unread. They are run-18's
# entries, carried through run-19 and run-21, and carry ``carried_from:
# run-21``; what is not carried is the status, which the pin recomputes from the
# bytes at the pinned commit.
READ_AT_THE_PIN_CORE_CHANGE_IDS = (
    "CORE_19_HONEST_REPORTING",
    "CORE_20_REFUSAL_LIST_PREFLIGHT",
)
CARRIED_PIN_STATUS = "CARRIED_FROM_RUN_21"
READ_AT_THE_PIN_STATUSES = {"LANDED", "PENDING_AT_PIN"}
CORE_PIN_STATUSES = {CARRIED_PIN_STATUS} | READ_AT_THE_PIN_STATUSES

# The four files this cell carries with the run id moved and nothing else, read
# through RUN_ID_SUBSTITUTIONS, which reverse.
RUN_ID_SUBSTITUTIONS = (
    (
        "run-21",
        "run-22",
    ),
    (
        "Run-21",
        "Run-22",
    ),
    (
        "run_21",
        "run_22",
    ),
)
CARRIED_WITH_THE_RUN_ID = (
    "run.py",
    "compile_ontology_candidate.py",
    "usage_from_launch_log.py",
    "spawn-message.md",
)
# The four files v4.12 changes, and the one table each is read through after the
# run id move. Every one of them reverses: undo the change table and then the
# run id table and run-21's file comes back byte for byte, so an edit in neither
# table fails here rather than travelling with the cell.
#
# ``bind_from_surface.py`` gains the fourth case kind and the closure refusal,
# ``native_query.py`` gains the fourth case kind's rows, ``prepare_producer.py``
# gains the canonical staging, and ``offline_validation.py`` gains the third
# stage that measures the fourth kind on run-09's frozen record.
BINDER_V4_12 = (
    (
        'BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v4"',
        'BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v5"',
    ),
    (
        "import argparse\n"
        "from hashlib import sha256\n"
        "import json\n"
        "from pathlib import Path\n"
        "import sys\n",
        "import argparse\n"
        "from hashlib import sha256\n"
        "import importlib.util\n"
        "import json\n"
        "from pathlib import Path\n"
        "import sys\n",
    ),
    (
        "The expansion stays mechanical and the evaluator's one judgement stays the type\n"
        "set per question.",
        "What v4.12 adds is a fourth case kind and a refusal. ``ENTITY_NO_SUBJECT`` is\n"
        "emitted for every subject-bearing type in a question's set and returns the\n"
        "records of that type whose ``subject`` slot is absent, each of them an\n"
        "``ENTITY`` row witnessed by itself, so a record about nothing the producer\n"
        "stated is reached once instead of not at all. Run-21 carried 237 such records\n"
        "and CQ-01's answer, the instrument count, was two of them (E-0197). A record\n"
        "that does carry a subject is still reached through it and never here, so\n"
        "nothing the v4.4 restriction excluded on purpose comes back.\n"
        "\n"
        "The refusal is the closure check. ``type_set_closure.omissions`` runs against\n"
        "the gate's validated contract before the binding is written, so a set that\n"
        "lists a type without its surface subtypes is refused where the evaluator can\n"
        "still correct it. v4.11 shipped that check as a step the procedure ran by hand;\n"
        "a step run by hand is a step that can be skipped, and the artefact it guards is\n"
        "the one this script writes (E-0196, E-0198).\n"
        "\n"
        "The expansion stays mechanical and the evaluator's one judgement stays the type\n"
        "set per question.",
    ),
    (
        'BOUND_AT_STAGE = "ONTOLOGY_ACCEPTANCE"\n'
        'PENDING = "PENDING"\n',
        'BOUND_AT_STAGE = "ONTOLOGY_ACCEPTANCE"\n'
        'PENDING = "PENDING"\n'
        'CLOSURE_CHECK = "TYPE_SET_CLOSED_UNDER_THE_SURFACES_SUBTYPES_AT_BIND_TIME"\n',
    ),
    (
        "# The three case kinds, in the order the expansion emits them. All three are\n"
        "# type-only: a case names record types and projected field names and nothing\n"
        "# else.\n"
        'CASE_KINDS = ("ENTITY", "RELATION", "SUBJECT")\n',
        "# The four case kinds, sorted, which is also the order the expansion emits\n"
        "# them. All four are type-only: a case names record types and projected field\n"
        "# names and nothing else. ``ENTITY_NO_SUBJECT`` is v4.12's addition and is\n"
        "# emitted directly after ``ENTITY``, so a question's ordinals keep the two\n"
        "# entity kinds first and the rows keep their order.\n"
        'CASE_KINDS = ("ENTITY", "ENTITY_NO_SUBJECT", "RELATION", "SUBJECT")\n'
        'ENTITY_NO_SUBJECT = "ENTITY_NO_SUBJECT"\n',
    ),
    (
        "# ENTITY case at all: it is reached through its subject or it is not reached.\n",
        "# ENTITY case at all: it is reached through its subject or it is not reached.\n"
        "# From v4.12 the second half of that sentence has one exception. A record of a\n"
        "# bearing type whose ``subject`` is absent is reached by an ENTITY_NO_SUBJECT\n"
        "# case, which is the only case whose selection reads a record at all, and reads\n"
        "# exactly one thing: whether the slot is there.\n",
    ),
    (
        " question's type set; this script expands it into three kinds of case,\"\n"
        '    " every one of them type-only: one ENTITY case per type in the set that"\n'
        '    " carries no subject on the surface, one RELATION case per ordered pair of"',
        " question's type set; this script expands it into four kinds of case,\"\n"
        '    " every one of them type-only: one ENTITY case per type in the set that"\n'
        '    " carries no subject on the surface, one ENTITY_NO_SUBJECT case per type in"\n'
        '    " the set that does carry it, returning the records of that type whose"\n'
        '    " subject slot is absent, one RELATION case per ordered pair of"',
    ),
    (
        "    \"\"\"Every ENTITY, RELATION and SUBJECT case a question's type set expands to.\n"
        "\n"
        "    The v4.4 restriction is the first loop: a type that carries ``subject`` is\n"
        "    reached through its subject or not at all, and gets no ENTITY case.\n"
        '    """\n',
        "    \"\"\"Every case of the four kinds a question's type set expands to.\n"
        "\n"
        "    The v4.4 restriction is the first loop: a type that carries ``subject`` is\n"
        "    reached through its subject or not at all, and gets no ENTITY case. The\n"
        "    v4.12 addition is the second: the same type gets one ENTITY_NO_SUBJECT\n"
        "    case, which returns the records of it that carry no subject and nothing\n"
        "    else.\n"
        '    """\n',
    ),
    (
        "    for source_type in types:\n"
        "        for relation_type in relations:\n",
        "    for record_type in bearing:\n"
        "        cases.append(\n"
        "            {\n"
        '                "kind": ENTITY_NO_SUBJECT,\n'
        '                "ordinal": len(cases) + 1,\n'
        '                "output_fields": {"record": projections[record_type]},\n'
        '                "record_type": record_type,\n'
        "            }\n"
        "        )\n"
        "    for source_type in types:\n"
        "        for relation_type in relations:\n",
    ),
    (
        "    expected = (\n"
        "        len(unattached)\n"
        "        + len(types) * len(types) * len(relations)\n"
        "        + len(bearing) * len(entities)\n"
        "    )\n",
        "    expected = (\n"
        "        len(unattached)\n"
        "        + len(bearing)\n"
        "        + len(types) * len(types) * len(relations)\n"
        "        + len(bearing) * len(entities)\n"
        "    )\n",
    ),
    (
        "def build(\n"
        "    *, surface_source: bytes, type_sets: dict[str, list[str]], replay_receipt: str\n"
        ") -> dict[str, object]:\n",
        "def _type_set_closure():\n"
        '    """The shared closure reader, loaded by path from the experiment root.\n'
        "\n"
        "    It lives beside the cells and not inside one, because every cell from v4.11\n"
        "    on reads the same rule from the same file. Loading it by path is how the\n"
        "    procedure already runs it.\n"
        '    """\n'
        "\n"
        '    path = Path(__file__).resolve().parents[1] / "type_set_closure.py"\n'
        "    specification = importlib.util.spec_from_file_location(\n"
        '        "paper_v4_type_set_closure", path\n'
        "    )\n"
        "    if specification is None or specification.loader is None:\n"
        '        raise BindingRefusal(f"the closure reader is not readable: {path}")\n'
        "    module = importlib.util.module_from_spec(specification)\n"
        "    specification.loader.exec_module(module)\n"
        "    return module\n"
        "\n"
        "\n"
        "def refuse_unclosed(\n"
        "    *, surface: dict[str, object], contract: dict[str, object], type_sets: dict\n"
        ") -> None:\n"
        '    """Refuse a type set that lists a type without its surface subtypes.\n'
        "\n"
        "    The facade's typed query returns a type's records and its subtypes', and the\n"
        "    v4.9 executor projects every reached record by its own type and refuses a\n"
        "    type the binding never names. A set that lists a parent and not a surface\n"
        "    subtype therefore binds a query that is refused after the rows exist, which\n"
        "    is what run-21's first binding did (E-0196). Here it is refused before the\n"
        "    binding is written, with the reason and the omitted names the shared reader\n"
        "    returns.\n"
        '    """\n'
        "\n"
        "    closure = _type_set_closure()\n"
        "    found = closure.omissions(surface, contract, type_sets)\n"
        "    if found:\n"
        '        detail = "; ".join(\n'
        "            f\"{question} omits {', '.join(names)}\"\n"
        "            for question, names in sorted(found.items())\n"
        "        )\n"
        '        raise BindingRefusal(f"{closure.REASON}: {detail}")\n'
        "\n"
        "\n"
        "def build(\n"
        "    *,\n"
        "    surface_source: bytes,\n"
        "    type_sets: dict[str, list[str]],\n"
        "    replay_receipt: str,\n"
        "    contract_source: bytes,\n"
        ") -> dict[str, object]:\n",
    ),
    (
        "    return {\n"
        '        "schema": BINDING_SCHEMA,\n'
        '        "status": "FROZEN_AT_ONTOLOGY_ACCEPTANCE",\n',
        "    refuse_unclosed(\n"
        "        surface=json.loads(surface_source),\n"
        "        contract=json.loads(contract_source),\n"
        "        type_sets=resolved,\n"
        "    )\n"
        "    return {\n"
        '        "schema": BINDING_SCHEMA,\n'
        '        "status": "FROZEN_AT_ONTOLOGY_ACCEPTANCE",\n',
    ),
    (
        '            "case_kinds": list(CASE_KINDS),\n'
        '            "entity_case_scope": "TYPES_IN_THE_SET_THAT_CARRY_NO_SUBJECT",\n',
        '            "case_kinds": list(CASE_KINDS),\n'
        '            "closure_checked": CLOSURE_CHECK,\n'
        '            "entity_case_scope": "TYPES_IN_THE_SET_THAT_CARRY_NO_SUBJECT",\n'
        '            "entity_no_subject_case_scope": (\n'
        '                "TYPES_IN_THE_SET_THAT_CARRY_SUBJECT_RESTRICTED_TO_RECORDS"\n'
        '                "_WHOSE_SUBJECT_SLOT_IS_ABSENT"\n'
        "            ),\n",
    ),
    (
        '            "rule": (\n'
        "                \"one ENTITY case per type in a question's set that carries no\"\n"
        '                " subject on the surface; every ordered pair of those types"\n'
        '                " under every relation type on the surface as a RELATION case;"\n',
        '            "rule": (\n'
        "                \"one ENTITY case per type in a question's set that carries no\"\n"
        '                " subject on the surface; one ENTITY_NO_SUBJECT case per type"\n'
        '                " in the set that does carry subject, returning the records of"\n'
        '                " that type whose subject slot is absent; every ordered pair of"\n'
        "                \" the set's types\"\n"
        '                " under every relation type on the surface as a RELATION case;"\n',
    ),
    (
        "    binding = build(\n"
        "        surface_source=Path(arguments.surface).read_bytes(),\n"
        "        type_sets=type_sets,\n"
        "        replay_receipt=receipt,\n"
        "    )\n",
        "    binding = build(\n"
        "        surface_source=Path(arguments.surface).read_bytes(),\n"
        "        type_sets=type_sets,\n"
        "        replay_receipt=receipt,\n"
        "        contract_source=Path(arguments.contract).read_bytes(),\n"
        "    )\n",
    ),
    (
        '    parser.add_argument("--surface", required=True, help="accepted population surface")\n',
        '    parser.add_argument("--surface", required=True, help="accepted population surface")\n'
        "    parser.add_argument(\n"
        '        "--contract",\n'
        "        required=True,\n"
        "        help=\"the gate's validated contract, read for the surface's subtypes\",\n"
        "    )\n",
    ),
)
EXECUTOR_V4_12 = (
    (
        "(E-0138, and the v4.2 RCA sections 2 and 4).\n",
        "(E-0138, and the v4.2 RCA sections 2 and 4).\n"
        "\n"
        "v4.12 adds a fourth case kind and no fifth row kind. An ENTITY_NO_SUBJECT case\n"
        "names one subject-bearing record type and returns the records of it whose\n"
        "``subject`` slot is absent, each as an ``ENTITY`` row witnessed by itself and\n"
        "projected by its own type like every other row. It is the only case whose\n"
        "selection reads a record's fields at all, and the only field it reads is\n"
        "whether that slot is there. A record that carries a subject is returned by its\n"
        "SUBJECT case and by no case of this kind, so the addition reaches nothing twice;\n"
        "a record reached both here and through an ancestor's ENTITY case builds the same\n"
        "row and adds an ordinal to it (E-0197).\n",
    ),
    (
        'BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v4"',
        'BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v5"',
    ),
    (
        'CASE_KINDS = ("ENTITY", "RELATION", "SUBJECT")\n',
        'CASE_KINDS = ("ENTITY", "ENTITY_NO_SUBJECT", "RELATION", "SUBJECT")\n'
        "# The case kind v4.12 adds, and the row kind it writes. The case kind is new;\n"
        "# the row kind is not, because the row is one admitted record witnessed by\n"
        "# itself, which is what an ENTITY row already was.\n"
        'ENTITY_NO_SUBJECT = "ENTITY_NO_SUBJECT"\n'
        'ENTITY_ROW_KIND = "ENTITY"\n',
    ),
    (
        "_CASE_FIELDS = {\n"
        '    "ENTITY": {"kind", "ordinal", "output_fields", "record_type"},\n',
        "_CASE_FIELDS = {\n"
        '    "ENTITY": {"kind", "ordinal", "output_fields", "record_type"},\n'
        '    ENTITY_NO_SUBJECT: {"kind", "ordinal", "output_fields", "record_type"},\n',
    ),
    (
        "_OUTPUT_FIELDS = {\n"
        '    "ENTITY": {"record"},\n',
        "_OUTPUT_FIELDS = {\n"
        '    "ENTITY": {"record"},\n'
        '    ENTITY_NO_SUBJECT: {"record"},\n',
    ),
    (
        "_TYPE_FIELDS = {\n"
        '    "ENTITY": ("record_type",),\n',
        "_TYPE_FIELDS = {\n"
        '    "ENTITY": ("record_type",),\n'
        '    ENTITY_NO_SUBJECT: ("record_type",),\n',
    ),
    (
        "_PROJECTED_TYPES = {\n"
        '    "ENTITY": (("record_type", "record"),),\n',
        "_PROJECTED_TYPES = {\n"
        '    "ENTITY": (("record_type", "record"),),\n'
        '    ENTITY_NO_SUBJECT: (("record_type", "record"),),\n',
    ),
    (
        "def _relation_rows(\n",
        "def _entity_no_subject_rows(\n"
        "    graph,\n"
        "    case: dict[str, Any],\n"
        "    witnesses: list[str],\n"
        "    projections: dict[str, list[str]],\n"
        ") -> list[dict]:\n"
        '    """The records of one subject-bearing type that carry no subject.\n'
        "\n"
        "    Absent is the slot missing from the record and an explicit null alike: both\n"
        "    say the producer named nothing this record is about. Run-21 populated 237\n"
        "    such records and the v4.4 binder reached none of them, which is why its\n"
        "    CQ-01 came back without the instrument count that is stated twice in the\n"
        "    reading (E-0197). The row is an ENTITY row, witnessed by the record itself\n"
        "    and projected by the record's own type, so a reviewer reads it exactly as\n"
        "    any other ENTITY row and the row grammar does not move.\n"
        '    """\n'
        "\n"
        "    rows: list[dict[str, Any]] = []\n"
        '    for item in graph.query(case["record_type"]):\n'
        "        if item.get(SUBJECT_SLOT) is not None:\n"
        "            continue\n"
        "        rows.append(\n"
        "            {\n"
        '                "case_ordinals": [case["ordinal"]],\n'
        '                "kind": ENTITY_ROW_KIND,\n'
        '                "record": _project(item, _own_fields(item, projections)),\n'
        '                "witness": {"record_id": item["id"]},\n'
        "            }\n"
        "        )\n"
        '        witnesses.append(item["id"])\n'
        "    return rows\n"
        "\n"
        "\n"
        "def _relation_rows(\n",
    ),
    (
        "_ROWS_BY_KIND = {\n"
        '    "ENTITY": _entity_rows,\n',
        "_ROWS_BY_KIND = {\n"
        '    "ENTITY": _entity_rows,\n'
        "    ENTITY_NO_SUBJECT: _entity_no_subject_rows,\n",
    ),
)
PREPARE_V4_12 = (
    (
        "versions the paper environment lock names, and records that check in the\n"
        "receipt.\n"
        '"""\n',
        "versions the paper environment lock names, and records that check in the\n"
        "receipt.\n"
        "\n"
        "One declared input is not staged as the bytes its file carries. The history\n"
        "profile is staged as its canonical JSON, sorted keys, compact separators and no\n"
        "trailing newline, because that is the form Core digests to get the profile's\n"
        "identity. shop-01 staged the file's own bytes, the parent told the producer to\n"
        "write their digest into its plans, and the compiler refused all four with\n"
        "IDENTITY_MISMATCH (E-0203, cause B). From v4.12 the staged file's digest is the\n"
        "identity, so the producer reads it off its own declared input and the parent has\n"
        "nothing left to hand it. The manifest states a staging per input and carries the\n"
        "source bytes' digest beside the staged bytes'.\n"
        '"""\n',
    ),
    (
        'UNTRACKED_INPUTS = {"SELECTED_READING"}\n',
        'UNTRACKED_INPUTS = {"SELECTED_READING"}\n'
        "# The declared inputs staged as canonical JSON, and the two names a staging is\n"
        "# recorded under. The manifest states one per input and this set is checked\n"
        "# against it, so a manifest and a builder that disagree refuse rather than stage\n"
        "# bytes nobody declared.\n"
        'CANONICAL_JSON_INPUTS = {"SOURCE_ASSERTION_PROFILE"}\n'
        'CANONICAL_JSON = "CANONICAL_JSON"\n'
        'SOURCE_BYTES = "SOURCE_BYTES"\n',
    ),
    (
        "def _digest(data: bytes) -> str:\n"
        '    return "sha256:" + sha256(data).hexdigest()\n',
        "def _digest(data: bytes) -> str:\n"
        '    return "sha256:" + sha256(data).hexdigest()\n'
        "\n"
        "\n"
        "def _canonical(data: bytes) -> bytes:\n"
        "    \"\"\"A JSON document's canonical bytes: sorted keys, compact, no newline.\"\"\"\n"
        "    return json.dumps(\n"
        "        json.loads(data),\n"
        "        allow_nan=False,\n"
        "        ensure_ascii=False,\n"
        '        separators=(",", ":"),\n'
        "        sort_keys=True,\n"
        '    ).encode("utf-8")\n'
        "\n"
        "\n"
        "def staged_bytes(item: dict[str, object], data: bytes) -> bytes:\n"
        '    """What one declared input is written as, which the manifest states."""\n'
        '    staged_as = item["staged_as"]\n'
        "    if staged_as == CANONICAL_JSON:\n"
        "        return _canonical(data)\n"
        "    if staged_as != SOURCE_BYTES:\n"
        "        raise ProducerPreparationRefusal(\n"
        "            f\"declared input {item['name']} names an unknown staging: {staged_as}\"\n"
        "        )\n"
        "    return data\n",
    ),
    (
        "    manifest = json.loads(MANIFEST.read_bytes())\n"
        '    commit = manifest["core"]["commit"]\n',
        "    manifest = json.loads(MANIFEST.read_bytes())\n"
        "    canonical = {\n"
        '        item["name"]\n'
        '        for item in manifest["declared_inputs"]\n'
        '        if item["staged_as"] == CANONICAL_JSON\n'
        "    }\n"
        "    if canonical != CANONICAL_JSON_INPUTS:\n"
        "        raise ProducerPreparationRefusal(\n"
        '            f"the manifest stages {sorted(canonical)} as canonical JSON;"\n'
        '            f" this builder stages {sorted(CANONICAL_JSON_INPUTS)}"\n'
        "        )\n"
        '    commit = manifest["core"]["commit"]\n',
    ),
    (
        "    sources: dict[str, bytes] = {}\n"
        '    for item in manifest["declared_inputs"]:\n'
        "        data = (\n"
        "            reading.read_bytes()\n"
        '            if item["name"] in UNTRACKED_INPUTS\n'
        '            else _git_show(commit, item["source"])\n'
        "        )\n"
        '        if _digest(data) != item["sha256"]:\n'
        "            raise ProducerPreparationRefusal(\n"
        "                f\"declared input digest mismatch: {item['name']}\"\n"
        "            )\n"
        '        sources[item["name"]] = data\n',
        "    sources: dict[str, bytes] = {}\n"
        '    for item in manifest["declared_inputs"]:\n'
        "        read = (\n"
        "            reading.read_bytes()\n"
        '            if item["name"] in UNTRACKED_INPUTS\n'
        '            else _git_show(commit, item["source"])\n'
        "        )\n"
        '        if _digest(read) != item["source_sha256"]:\n'
        "            raise ProducerPreparationRefusal(\n"
        "                f\"declared input source digest mismatch: {item['name']}\"\n"
        "            )\n"
        "        data = staged_bytes(item, read)\n"
        '        if _digest(data) != item["sha256"]:\n'
        "            raise ProducerPreparationRefusal(\n"
        "                f\"declared input digest mismatch: {item['name']}\"\n"
        "            )\n"
        '        sources[item["name"]] = data\n',
    ),
)
OFFLINE_V4_12 = (
    (
        "\"\"\"Validate the v4.4 ENTITY restriction and the v4.9 removal on run-09's record.\n"
        "\n"
        "Both changes in the query surface are removals, so they can be measured before a\n"
        "producer runs: expand",
        '"""Validate the v4.4 restriction, the v4.9 removal and the v4.12 restoration.\n'
        "\n"
        "The first two changes in the query surface are removals and the third is an\n"
        "addition, and all three can be measured on one frozen record: expand",
    ),
    (
        "The two stages are reported separately. The first is the carried v4.4 rule, whose\n"
        "counts must not move because the binder did not; the second is this cell's, and\n"
        "the difference between them is what the removal takes out of run-09's record.\n",
        "The carried stages are reported first and their counts must not move, because\n"
        "neither the v4.4 rule nor the v4.9 removal moved under this cell. The third\n"
        "stage is v4.12's own. Run-09 ran under the v3 binding, which emitted a plain\n"
        "ENTITY case for every type in a question's set, so the rows an ENTITY_NO_SUBJECT\n"
        "case returns are already in run-09's result: they are the rows of the ENTITY\n"
        "case of a subject-bearing type whose projected record carries no subject. They\n"
        "are counted here with the labels run-09's reviewers gave them, which is what the\n"
        "addition brings back into reach and nothing more.\n",
    ),
    (
        'RECORD_SCHEMA = "malleus.paper-v4.run-22-offline-validation/v1"\n'
        'QUESTION_IDS = ("CQ-01", "CQ-02", "CQ-03", "CQ-04")\n',
        'RECORD_SCHEMA = "malleus.paper-v4.run-22-offline-validation/v2"\n'
        'QUESTION_IDS = ("CQ-01", "CQ-02", "CQ-03", "CQ-04")\n'
        "# v4.12's case kind. A v3 binding knows nothing of it, so its counterpart there\n"
        "# is the ENTITY case of the same type and the rows it would return are that\n"
        "# case's rows whose record carries no subject.\n"
        'ENTITY_NO_SUBJECT = "ENTITY_NO_SUBJECT"\n',
    ),
    (
        '    if kind == "SUBJECT":\n'
        '        return (kind, str(case["record_type"]), str(case["subject_record_type"]))\n'
        '    raise OfflineValidationRefusal(f"unknown case kind: {kind}")\n',
        '    if kind == "SUBJECT":\n'
        '        return (kind, str(case["record_type"]), str(case["subject_record_type"]))\n'
        "    if kind == ENTITY_NO_SUBJECT:\n"
        '        return (kind, str(case["record_type"]))\n'
        '    raise OfflineValidationRefusal(f"unknown case kind: {kind}")\n',
    ),
    (
        '        "rows_re_projected_under_another_label": 0,\n'
        "    }\n",
        '        "rows_re_projected_under_another_label": 0,\n'
        '        "rows_restored_by_entity_no_subject": 0,\n'
        '        "rows_restored_witnesses": 0,\n'
        '        "rows_restored_new_witnesses": 0,\n'
        "    }\n"
        "    restored_by_label_total: dict[str, int] = {}\n",
    ),
    (
        "        restricted = binder._cases(\n"
        "            types=types, relations=relations, by_name=by_name\n"
        "        )\n"
        "        kept_identities = {case_identity(case) for case in restricted}\n"
        "        frozen_cases = frozen[question_id]\n"
        "        frozen_identities = {case_identity(case) for case in frozen_cases}\n"
        "        if not kept_identities <= frozen_identities:\n"
        "            raise OfflineValidationRefusal(\n"
        '                f"the v4 expansion of {question_id} is not a subset of the v3 one"\n'
        "            )\n"
        "        kept_ordinals = {\n"
        '            int(case["ordinal"])\n'
        "            for case in frozen_cases\n"
        "            if case_identity(case) in kept_identities\n"
        "        }\n",
        "        expanded = binder._cases(\n"
        "            types=types, relations=relations, by_name=by_name\n"
        "        )\n"
        "        restricted = [\n"
        '            case for case in expanded if str(case["kind"]) != ENTITY_NO_SUBJECT\n'
        "        ]\n"
        "        restored_types = {\n"
        '            str(case["record_type"])\n'
        "            for case in expanded\n"
        '            if str(case["kind"]) == ENTITY_NO_SUBJECT\n'
        "        }\n"
        "        kept_identities = {case_identity(case) for case in restricted}\n"
        "        frozen_cases = frozen[question_id]\n"
        "        frozen_identities = {case_identity(case) for case in frozen_cases}\n"
        "        if not kept_identities <= frozen_identities:\n"
        "            raise OfflineValidationRefusal(\n"
        '                f"the v4 expansion of {question_id} is not a subset of the v3 one"\n'
        "            )\n"
        "        if restored_types != set(bearing):\n"
        "            raise OfflineValidationRefusal(\n"
        '                f"the ENTITY_NO_SUBJECT cases of {question_id} do not cover its"\n'
        '                " subject-bearing types"\n'
        "            )\n"
        "        kept_ordinals = {\n"
        '            int(case["ordinal"])\n'
        "            for case in frozen_cases\n"
        "            if case_identity(case) in kept_identities\n"
        "        }\n"
        "        # The v3 ENTITY case of each subject-bearing type. Its subject-less rows\n"
        "        # are the ones v4.4 took out of reach and v4.12 gives back.\n"
        "        restored_ordinals = {\n"
        '            int(case["ordinal"])\n'
        "            for case in frozen_cases\n"
        '            if str(case["kind"]) == "ENTITY"\n'
        '            and str(case["record_type"]) in restored_types\n'
        "        }\n",
    ),
    (
        "        kept = 0\n"
        "        relabelled = 0\n",
        "        kept = 0\n"
        "        relabelled = 0\n"
        "        restored = 0\n"
        "        restored_by_label: dict[str, int] = {}\n"
        "        restored_witnesses: set[str] = set()\n",
    ),
    (
        "        for index, row in enumerate(rows):\n"
        '            if int(row["case_ordinal"]) not in kept_ordinals:\n'
        "                continue\n"
        "            kept += 1\n",
        "        for index, row in enumerate(rows):\n"
        '            ordinal = int(row["case_ordinal"])\n'
        "            if (\n"
        "                ordinal in restored_ordinals\n"
        '                and row["record"].get(binder.SUBJECT_SLOT) is None\n'
        "            ):\n"
        "                restored += 1\n"
        "                restored_by_label[judged[index]] = (\n"
        "                    restored_by_label.get(judged[index], 0) + 1\n"
        "                )\n"
        "                restored_witnesses.add(witness_identity(row))\n"
        "            if ordinal not in kept_ordinals:\n"
        "                continue\n"
        "            kept += 1\n",
    ),
    (
        '                "rows_re_projected_under_another_label": relabelled,\n'
        "            }\n"
        "        )\n",
        '                "rows_re_projected_under_another_label": relabelled,\n'
        '                "rows_restored_by_entity_no_subject": restored,\n'
        '                "rows_restored_witnesses": len(restored_witnesses),\n'
        '                "rows_restored_new_witnesses": len(\n'
        "                    restored_witnesses - set(survivor_label)\n"
        "                ),\n"
        '                "rows_restored_by_label": dict(sorted(restored_by_label.items())),\n'
        "            }\n"
        "        )\n",
    ),
    (
        '        totals["rows_re_projected_under_another_label"] += relabelled\n',
        '        totals["rows_re_projected_under_another_label"] += relabelled\n'
        '        totals["rows_restored_by_entity_no_subject"] += restored\n'
        '        totals["rows_restored_witnesses"] += len(restored_witnesses)\n'
        '        totals["rows_restored_new_witnesses"] += len(\n'
        "            restored_witnesses - set(survivor_label)\n"
        "        )\n"
        "        for name, count in restored_by_label.items():\n"
        "            restored_by_label_total[name] = restored_by_label_total.get(name, 0) + count\n",
    ),
    (
        '    totals["rows_one_per_witness_by_label"] = dict(sorted(one_by_label.items()))\n',
        '    totals["rows_one_per_witness_by_label"] = dict(sorted(one_by_label.items()))\n'
        '    totals["rows_restored_by_label"] = dict(sorted(restored_by_label_total.items()))\n',
    ),
    (
        '        "and_change_id": "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION",\n',
        '        "and_change_id": "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION",\n'
        '        "third_change_id": "ENTITY_NO_SUBJECT_REACHABILITY",\n'
        '        "third_rule": (\n'
        "            \"one ENTITY_NO_SUBJECT case per subject-bearing type in a question's\"\n"
        '            " set, returning the records of that type whose subject slot is"\n'
        "            \" absent as ENTITY rows; measured here as the rows of run-09's v3\"\n"
        '            " ENTITY case of the same type whose record carries no subject"\n'
        "        ),\n",
    ),
)
CHANGED_BY_V4_12 = {
    "bind_from_surface.py": BINDER_V4_12,
    "native_query.py": EXECUTOR_V4_12,
    "offline_validation.py": OFFLINE_V4_12,
    "prepare_producer.py": PREPARE_V4_12,
}
# The three changes v4.12 states, and the files each one lands in. The list is
# closed: a fourth change, or a change in a file no entry names, fails the
# statement below rather than arriving unannounced.
V4_12_CHANGES = {
    "ENTITY_NO_SUBJECT_REACHABILITY": (
        "bind_from_surface.py",
        "native_query.py",
        "offline_validation.py",
    ),
    "TYPE_SET_CLOSURE_AT_BIND_TIME": ("bind_from_surface.py",),
    "CANONICAL_PROFILE_STAGING": ("prepare_producer.py", "pin.py"),
}
ENTITY_NO_SUBJECT = "ENTITY_NO_SUBJECT"
BINDING_SCHEMA_V5 = "malleus.paper-v4.native-query-binding/v5"
BINDING_SCHEMA_V4 = "malleus.paper-v4.native-query-binding/v4"
# ``pin.py`` is the one file that names the cell it carries from, so it takes a
# second table after the run id move: the reference cell steps from run-20 to
# run-21, the carried status with it, and the interface ordinal from 21 to 22.
# The protocol version steps too, from v4.10 to v4.12, because the harness moves
# under this cell even though Core does not; the gate status names the Core
# coordinate and stays where it is.
#
# Three passages are repaired after that step, because the blanket move would
# otherwise make them say something untrue: that v4.10 is the version this cell
# stays at, that this cell carries twenty-nine entries where it carries thirty,
# that the two entries reading past the v4.8 coordinate reached this cell
# through run-19 and run-21 alone, and that Core-18's carry chain skips run-20.
PIN_REFERENCE_CELL = (
    (
        "run-20",
        "run-21",
    ),
    (
        "RUN_20",
        "RUN_21",
    ),
    (
        'INTERFACE_ORDINAL = "21"',
        'INTERFACE_ORDINAL = "22"',
    ),
    (
        'PROTOCOL_VERSION = "v4.10"',
        'PROTOCOL_VERSION = "v4.12"',
    ),
    (
        "v4.10 does not move under this cell. It pins the commit run-21 pinned, so its\n"
        "twenty-nine carried entries still read at fixed coordinates, the v4.1 baseline\n",
        "Core does not move under this cell and the harness does: v4.12 is where it moves\n"
        "to. This pins the commit run-21 pinned, so its thirty carried entries still read\n"
        "at fixed coordinates, the v4.1 baseline\n",
    ),
    (
        "# the wrong Core task, and the two that do read past it are run-18's, carried\n"
        "# through run-19 and run-21 and read again at the commit run-21 pinned.\n",
        "# the wrong Core task, and the two that do read past it are run-18's, carried\n"
        "# through run-19, run-20 and run-21 and read again at the commit run-21\n"
        "# pinned.\n",
    ),
    (
        "    # Carried from run-21, and before that from run-19, run-18, run-17, run-16,\n"
        "    # run-15 and run-14, where it was the change under test.",
        "    # Carried from run-21, and before that from run-20, run-19, run-18, run-17,\n"
        "    # run-16, run-15 and run-14, where it was the change under test.",
    ),
)
# The pin gains code this cell, which it last did at run-18: the canonical
# staging table, the canonical bytes beside the canonical digest, the staged
# digest beside the source digest in every declared input, and the cause of
# every input that moved. Each block is delimited by its own run-22 marker pair
# and read through this third table, which reverses like the others.
PIN_V4_12_STAGING = (
    (
        "# Name, tracked source path, workspace target. The eight are run-04's, in\n"
        "# run-04's order, and the reading is the one input that is untracked.\n",
        "# run-22 addition begins: the canonical-staging table\n"
        "# The declared inputs whose staged bytes are not the file's bytes, and the two\n"
        "# names a staging is recorded under. v4.12's third change: the history profile\n"
        "# is staged as its canonical JSON, because that is the form Core digests to get\n"
        "# the profile's identity. shop-01 staged the file's own bytes, the producer\n"
        "# wrote their digest into four plans as the parent had told it to, and the\n"
        "# compiler refused every one of them (E-0203, cause B).\n"
        'CANONICAL_JSON_INPUTS = frozenset({"SOURCE_ASSERTION_PROFILE"})\n'
        'CANONICAL_JSON = "CANONICAL_JSON"\n'
        'SOURCE_BYTES = "SOURCE_BYTES"\n'
        "# Why each input that moved against the reference cell moved. An input that\n"
        "# moved for a reason this table does not name is Core moving under the cell,\n"
        "# which is a different fact and is recorded as one.\n"
        "MOVED_BY_THE_HARNESS = {\n"
        '    "SOURCE_ASSERTION_PROFILE": "STAGED_AS_CANONICAL_JSON_FROM_V4_12",\n'
        "}\n"
        "# run-22 addition ends: the canonical-staging table\n"
        "\n"
        "# Name, tracked source path, workspace target. The eight are run-04's, in\n"
        "# run-04's order, and the reading is the one input that is untracked.\n",
    ),
    (
        "def _canonical_digest(data: bytes) -> str:\n"
        '    """The identity Core gives a canonical JSON artifact, from its bytes."""\n'
        "    return _digest(\n"
        "        json.dumps(\n"
        "            json.loads(data),\n"
        "            allow_nan=False,\n"
        "            ensure_ascii=False,\n"
        '            separators=(",", ":"),\n'
        "            sort_keys=True,\n"
        '        ).encode("utf-8")\n'
        "    )\n",
        "# run-22 addition begins: the canonical bytes beside the canonical digest\n"
        "def _canonical(data: bytes) -> bytes:\n"
        "    \"\"\"A JSON document's canonical bytes: sorted keys, compact, no newline.\"\"\"\n"
        "    return json.dumps(\n"
        "        json.loads(data),\n"
        "        allow_nan=False,\n"
        "        ensure_ascii=False,\n"
        '        separators=(",", ":"),\n'
        "        sort_keys=True,\n"
        '    ).encode("utf-8")\n'
        "\n"
        "\n"
        "# run-22 addition ends: the canonical bytes beside the canonical digest\n"
        "\n"
        "\n"
        "def _canonical_digest(data: bytes) -> str:\n"
        '    """The identity Core gives a canonical JSON artifact, from its bytes."""\n'
        "    return _digest(_canonical(data))\n",
    ),
    (
        "    \"\"\"Which declared inputs carry other bytes than the v4.10 cell of record's.\n"
        "\n"
        "    A cell states what its producer read, and a cell that shares an input list\n"
        "    with an earlier one has to say which of those inputs actually moved. Core\n"
        "    does not move under this cell and neither does the skill: the manifest\n"
        "    records which inputs moved against run-21's, and none is expected to have.\n"
        '    """\n',
        '    """Which declared inputs carry other bytes than the cell this one replicates.\n'
        "\n"
        "    A cell states what its producer read, and a cell that shares an input list\n"
        "    with an earlier one has to say which of those inputs actually moved. Core\n"
        "    does not move under this cell and neither does the skill. One input does:\n"
        "    the history profile is staged as canonical JSON from v4.12, so the bytes\n"
        "    the producer reads are the profile's identity bytes and not the file's, and\n"
        "    the cause is recorded beside the name rather than left to be read as Core\n"
        "    having moved.\n"
        '    """\n',
    ),
    (
        "    return {\n"
        '        "reference_run": REFERENCE_RUN,\n'
        '        "reference_manifest": REFERENCE_MANIFEST,\n'
        '        "moved": sorted(\n'
        "            name for name in observed if observed[name] != reference[name]\n"
        "        ),\n"
        '        "unchanged": sorted(\n'
        "            name for name in observed if observed[name] == reference[name]\n"
        "        ),\n"
        "    }\n",
        "    moved = sorted(name for name in observed if observed[name] != reference[name])\n"
        "    return {\n"
        '        "reference_run": REFERENCE_RUN,\n'
        '        "reference_manifest": REFERENCE_MANIFEST,\n'
        '        "moved": moved,\n'
        "        # run-22 addition begins: the cause of every moved input\n"
        '        "moved_cause": {\n'
        '            name: MOVED_BY_THE_HARNESS.get(name, "CORE_MOVED_UNDER_THIS_CELL")\n'
        "            for name in moved\n"
        "        },\n"
        "        # run-22 addition ends: the cause of every moved input\n"
        '        "unchanged": sorted(\n'
        "            name for name in observed if observed[name] == reference[name]\n"
        "        ),\n"
        "    }\n",
    ),
    (
        "        declared.append(\n"
        "            {\n"
        '                "name": name,\n'
        '                "source": source,\n'
        '                "target": target,\n'
        '                "sha256": _digest(data),\n'
        "            }\n"
        "        )\n",
        "        # run-22 addition begins: the staged bytes beside the source bytes\n"
        "        staged_as = CANONICAL_JSON if name in CANONICAL_JSON_INPUTS else SOURCE_BYTES\n"
        "        staged = _canonical(data) if staged_as == CANONICAL_JSON else data\n"
        "        declared.append(\n"
        "            {\n"
        '                "name": name,\n'
        '                "source": source,\n'
        '                "target": target,\n'
        '                "staged_as": staged_as,\n'
        '                "source_sha256": _digest(data),\n'
        '                "sha256": _digest(staged),\n'
        "            }\n"
        "        )\n"
        "        # run-22 addition ends: the staged bytes beside the source bytes\n",
    ),
)
# The five blocks run-18 added to run-17's pin, each still delimited in
# ``pin.py`` by its own marker pair, and the four this cell adds. Run-18's are
# carried whole and their markers still name run-18, because run-18 wrote them.
PIN_ADDITION_MARKERS = (
    "the Core-19 and Core-20 constants",
    "the readers Core-19 and Core-20 are pinned by",
    "the Core-19 and Core-20 entries",
    "this cell's own entries in the gate status",
    "the Core-19 and Core-20 report keys",
)
PIN_RUN_22_ADDITION_MARKERS = (
    "the canonical-staging table",
    "the canonical bytes beside the canonical digest",
    "the cause of every moved input",
    "the staged bytes beside the source bytes",
)
ADDITION_BEGINS = "# run-18 addition begins: "
ADDITION_ENDS = "# run-18 addition ends: "
RUN_22_ADDITION_BEGINS = "# run-22 addition begins: "
RUN_22_ADDITION_ENDS = "# run-22 addition ends: "

# The Core coordinate run-17 pinned, which is the baseline the two carried
# Core-19 and Core-20 entries are read against and the commit every other
# carried Core entry still stops at.
V4_9_COORDINATE = "dc5254795a78648591d3a1b0bcf602af8d443dc1"
# The producer block's three model fields. This cell moves none of them, and it
# moves no other key either: test_contract.py compares run-22's producer block
# to run-21's key by key and requires no difference at all. Run-21's own model
# entry, run-19's, run-18's and run-17's are carried beside this cell's as the
# closed cells' records, their subjects those cells' producer blocks and not
# this one's, so none is a harness marker and none is this cell's change.
MODEL_CHANGE_ID = "OPUS_5_REPLICATE_AT_V4_12"
PRIOR_MODEL_CHANGE_IDS = (
    "HAIKU_4_5_PRODUCER_AT_V4_9",
    "HAIKU_4_5_PRODUCER_AT_V4_10",
    "OPUS_5_PRODUCER_AT_V4_10",
    "OPUS_5_REPLICATE_AT_V4_10",
    "SONNET_5_PRODUCER_AT_V4_9",
    "SONNET_5_PRODUCER_AT_V4_10",
)
MODEL_FIELDS = {
    "requested_model": "opus",
    "model_family": "Claude Opus 5",
    "model_id": "claude-opus-5",
}
# Run-21's, and they are the same three. A replicate that moved one of them
# would be a matrix cell, not a replicate, and the equality below is where that
# would fail. The instruments move under this cell and the producer condition
# does not, which is the whole of what makes its rows comparable with run-20's
# and run-21's on the producer side and on nothing else.
PRIOR_MODEL_FIELDS = {
    "requested_model": "opus",
    "model_family": "Claude Opus 5",
    "model_id": "claude-opus-5",
}

# The seventeen changes the harness owns, each with the file that carries it
# and one string that cannot be there unless the change is. Fourteen are carried
# from run-21 and their markers are in bytes this cell copied; the last three
# are v4.12's own and their markers are in the bytes it wrote. The producer sees
# none of them except the canonical profile bytes, which it reads as its own
# declared input and is told nothing about.
DELTA_MARKERS = {
    "BINDING_FROZEN_AT_ACCEPTANCE": (
        "paper-v4/experiment-v4/run-22/bind_from_surface.py",
        '"bound_at_stage": BOUND_AT_STAGE,',
    ),
    "GATE_SURFACES_CHAINED_CAUSE": (
        "paper-v4/experiment-v4/run-22/compile_ontology_candidate.py",
        '"cause_chain": chain,',
    ),
    "INTERPRETER_PREFLIGHT": (
        "paper-v4/experiment-v4/run-22/prepare_producer.py",
        "def preflight() -> dict[str, object]:",
    ),
    "LAUNCH_LOG_V2": (
        "paper-v4/experiment-v4/run-22/usage_from_launch_log.py",
        'LOG_SCHEMA = "malleus.paper-v4.producer-launch-log/v2"',
    ),
    "PUBLIC_COST_RECORD": (
        "paper-v4/experiment-v4/run-22/usage_from_launch_log.py",
        'USAGE_SCHEMA = "malleus.paper-v4.producer-usage/v1"',
    ),
    "QUERY_CASE_KINDS_V3": (
        "paper-v4/experiment-v4/run-22/native_query.py",
        "_ROWS_BY_KIND = {",
    ),
    "REVIEW_PROTOCOL_V2": (
        "paper-v4/evaluation-v4/review-protocol-v2.json",
        '"query_trace_summary"',
    ),
    "REVIEW_TASK_V2": (
        "paper-v4/evaluation-v4/review-task.template.md",
        "{{WITNESS_COUNT}}",
    ),
    "REVIEW_TASK_V3": (
        "paper-v4/evaluation-v4/review-task-v3.template.md",
        "SUBJECT_IN_BLOCK",
    ),
    "REVIEW_TASK_V4": (
        "paper-v4/evaluation-v4/review-task-v4.template.md",
        "**Derivation locality, `RELATION` rows only.**",
    ),
    "STOP_RULE_CLARIFIED": (
        "paper-v4/experiment-v4/run-22/spawn-message.md",
        "Reviewing the next block is",
    ),
    "SUBJECT_TAGS_PROJECTED": (
        "paper-v4/experiment-v4/run-22/native_query.py",
        'SUBJECT_TAGS_SLOT = "tags"',
    ),
    "ENTITY_KIND_RESTRICTED": (
        "paper-v4/experiment-v4/run-22/bind_from_surface.py",
        "unattached = [name for name in types if name not in set(bearing)]",
    ),
    "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION": (
        "paper-v4/experiment-v4/run-22/native_query.py",
        "def surface_projections(binding: dict[str, object])"
        " -> dict[str, list[str]]:",
    ),
    "ENTITY_NO_SUBJECT_REACHABILITY": (
        "paper-v4/experiment-v4/run-22/native_query.py",
        "def _entity_no_subject_rows(",
    ),
    "TYPE_SET_CLOSURE_AT_BIND_TIME": (
        "paper-v4/experiment-v4/run-22/bind_from_surface.py",
        "def refuse_unclosed(",
    ),
    "CANONICAL_PROFILE_STAGING": (
        "paper-v4/experiment-v4/run-22/prepare_producer.py",
        "def staged_bytes(item: dict[str, object], data: bytes) -> bytes:",
    ),
}
CAPTURE_ID = "capture:inspection-note"
PLAN_ID = "plan:inspection-note:1"
SOURCE_ID = "source:inspection-note"
ARTIFACT_ID = "artifact:inspection-note"

# Core owns the governed-history machine, its policy, its binding, its check
# outcome and its event bytes. Paper code that names any of them has stopped
# being an adopter and started hand-assembling Core's protocol. The tokens are
# spelled in halves so this guard cannot match itself.
FORBIDDEN_SYMBOLS = (
    "Protocol" + "MachineProgram",
    "Policy" + "Program",
    "KnowledgeChange" + "HistoryBinding",
    "CHECK_" + "RECORDED",
    "machine_" + "events",
)

# The Event half of this test. The shared fixture declares no Event type, so the
# test adds one to its own ontology bytes and never edits the fixture.
EVENT_TYPE = "MaintenanceEvent"
EVENT_RECORD_ID = "maintenance-event:P-7:2026-03-02"

# The SUBJECT half. The fixture declares no subject reference, so the test adds
# one to its own ontology bytes and never edits the fixture.
SUBJECT_SLOT = "subject"
# The closure half. The fixture declares no subclass of a project class, so the
# test declares one on its own copy of the ontology and never edits the fixture.
SUBTYPE = "ProbeInspection"
SUBJECT_RECORD_ID = "inspection:P-7:2026-03-02"
# The reachability half. A second record of the same bearing type that names no
# subject: v4.4 reached it with no case at all and v4.12 reaches it once, as an
# ENTITY row of its own type.
UNATTACHED_RECORD_ID = "inspection:P-9:2026-03-04"
UNATTACHED_INSPECTED_ON = "2026-03-04"
SUBJECT_TARGET_ID = "asset:P-7"
# The carried v4.7 delta needs a subject that carries ``tags``. The fixture's asset does
# not, and the fixture is Core's and is read, never written, so the test writes
# the slot on its own copy of the records exactly as it writes the subject.
SUBJECT_TAGS_SLOT = "tags"
SUBJECT_TARGET_TAGS = ["P-7", "Pump 7"]
ROOT_PARENTS = ("Entity", "Event", "Relation", "Signal")
GROUNDING = {
    "tag": "grounding",
    "value": {
        "area": "Industrial maintenance and reliability",
        "taxonomy": "DDC 620.0046",
        "vocabularies": [
            {
                "vocabulary": (
                    "ISO 14224:2016 Collection and exchange of reliability and"
                    " maintenance data for equipment"
                ),
                "vocabulary_url": "https://www.iso.org/standard/64076.html",
                "borrowed_terms": ["equipment unit", "maintenance action"],
            }
        ],
        "invented_terms": [],
    },
}


def _module(name: str):
    path = HERE / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"paper_v4_run_22_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _binder_of(cell: Path, name: str, module: str = "bind_from_surface"):
    """An earlier cell's module, read and never written."""
    path = cell / f"{module}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_21_binder():
    """Run-21's binder: this cell has no delta, so it is the same expansion."""
    return _binder_of(RUN_21, "paper_v4_run_21_binder")


def _run_09_binder():
    """Run-09's binder, the cell before the carried ENTITY restriction."""
    return _binder_of(RUN_09, "paper_v4_run_09_binder")


def _identity(case: dict) -> tuple[str, ...]:
    """A case's kind and its types, which is all a type-only case is."""
    if case["kind"] in {"ENTITY", ENTITY_NO_SUBJECT}:
        return (case["kind"], case["record_type"])
    if case["kind"] == "RELATION":
        return (
            "RELATION",
            case["source_record_type"],
            case["relation_record_type"],
            case["target_record_type"],
        )
    return ("SUBJECT", case["record_type"], case["subject_record_type"])


def _identities(cases: list[dict]) -> set[tuple[str, ...]]:
    return {_identity(case) for case in cases}


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _plain(text: str) -> str:
    return " ".join(text.split())


def _span(text: str, start: str, end: str) -> str:
    """The inclusive span from ``start`` to the first ``end`` after it."""
    assert text.count(start) == 1, start
    begin = text.index(start)
    return text[begin : text.index(end, begin) + len(end)]


def _carried(name: str) -> tuple[str, str]:
    """This cell's copy of a run-21 file, beside run-21's with the run id moved."""
    return (
        (HERE / name).read_text(encoding="utf-8"),
        (RUN_21 / name).read_text(encoding="utf-8")
        .replace("run-21", "run-22")
        .replace("Run-21", "Run-22")
        .replace("run_21", "run_22"),
    )


@pytest.fixture()
def private_workspace() -> Iterator[Path]:
    PRIVATE.mkdir(exist_ok=True)
    path = Path(tempfile.mkdtemp(dir=PRIVATE, prefix="run-22-test-"))
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _source_arguments(ontology: Path | None = None) -> list[str]:
    return [
        "--root",
        "inspection-note",
        "--source",
        "inspection-note",
        str(ontology if ontology is not None else FIXTURE / "inspection-note.yaml"),
        "--source",
        "malleus",
        str(ROOT / "ontology/malleus.yaml"),
        "--source",
        "linkml:types",
        str(LINKML_TYPES),
    ]


def _population_file(directory: Path) -> Path:
    plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    path = directory / "document-population.json"
    path.write_bytes(
        _canonical(
            {
                "capture": json.loads((FIXTURE / "document-capture.json").read_bytes()),
                "records": plan["records"],
                "supersessions": plan["supersessions"],
            }
        )
    )
    return path


def _event_ontology(directory: Path) -> Path:
    """The neutral fixture ontology plus one grounded Event subclass.

    The fixture is Core's and is read, never written. It declares no Event type
    and carries no grounding block, and the PROJECT rite needs one on every class
    whose ``is_a`` is a Malleus root, so the test writes its own bytes.
    """
    document = yaml.safe_load((FIXTURE / "inspection-note.yaml").read_bytes())
    document["classes"][EVENT_TYPE] = {"is_a": "Event"}
    for body in document["classes"].values():
        if body.get("is_a") in ROOT_PARENTS:
            body["annotations"] = {"grounding": deepcopy(GROUNDING)}
    path = directory / "inspection-note-with-event.yaml"
    path.write_bytes(yaml.safe_dump(document, sort_keys=True).encode("utf-8"))
    return path


def _event_population_file(directory: Path) -> Path:
    """The fixture capture and records with one Event record and its derivation.

    Every ``properties`` key needs a formalization target, so the event's
    ``event_type`` is named by the same assertion that already carries the
    inspection.
    """
    plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    capture = json.loads((FIXTURE / "document-capture.json").read_bytes())
    capture["assertions"][0]["formalized_by"].append(
        {"path": ["properties", "event_type"], "record_id": EVENT_RECORD_ID}
    )
    records = dict(plan["records"])
    records["events"] = [
        {
            "id": EVENT_RECORD_ID,
            "properties": {"event_type": "INSPECTION"},
            "type": EVENT_TYPE,
        }
    ]
    path = directory / "document-population-with-event.json"
    path.write_bytes(
        _canonical(
            {
                "capture": capture,
                "records": records,
                "supersessions": plan["supersessions"],
            }
        )
    )
    return path


def _binding_file(directory: Path) -> Path:
    path = directory / "native-query-binding.json"
    path.write_bytes(
        _canonical(
            {
                "schema": "malleus.paper-v4.native-query-binding/v5",
                "status": "FROZEN_AFTER_REPLAY",
                "queries": [
                    {
                        "id": "NQ-FIXTURE-01",
                        "question_id": "FIXTURE-01",
                        "cases": [
                            {
                                "kind": "RELATION",
                                "ordinal": 1,
                                "source_record_type": "Inspection",
                                "relation_record_type": "InspectionOfRelation",
                                "target_record_type": "Asset",
                                "output_fields": {
                                    "source": ["inspected_on"],
                                    "relation": ["relation_type"],
                                    "target": ["name"],
                                },
                            }
                        ],
                    }
                ],
            }
        )
    )
    return path


def _subject_ontology(directory: Path) -> Path:
    """The neutral fixture ontology plus a grounded ``subject`` reference.

    Core-13 puts ``subject`` on the research pack's SourceAsserted mixin, single,
    optional and Entity-ranged. The fixture is Core's and is read, never written,
    and it imports no pack, so the test declares the same shape on its own bytes:
    one entity type carries an entity-ranged ``subject`` slot, which is what a
    SUBJECT case binds against.
    """
    document = yaml.safe_load((FIXTURE / "inspection-note.yaml").read_bytes())
    document["slots"][SUBJECT_SLOT] = {"range": "Asset"}
    document["classes"]["Inspection"]["slots"].append(SUBJECT_SLOT)
    for body in document["classes"].values():
        if body.get("is_a") in ROOT_PARENTS:
            body["annotations"] = {"grounding": deepcopy(GROUNDING)}
    path = directory / "inspection-note-with-subject.yaml"
    path.write_bytes(yaml.safe_dump(document, sort_keys=True).encode("utf-8"))
    return path


def _subtype_ontology(directory: Path) -> Path:
    """The neutral fixture ontology plus one subtype of an entity type.

    The fixture declares no subclass of a project class, and the closure rule
    is about exactly that: the facade's typed query returns a type's records
    and its subtypes', so a set that lists the parent and not the child binds a
    query the executor refuses after the rows exist (E-0196). The fixture is
    Core's and is read, never written, so the subtype is declared on the test's
    own bytes.
    """

    document = yaml.safe_load((FIXTURE / "inspection-note.yaml").read_bytes())
    for body in document["classes"].values():
        if body.get("is_a") in ROOT_PARENTS:
            body["annotations"] = {"grounding": deepcopy(GROUNDING)}
    document["classes"][SUBTYPE] = {"is_a": "Inspection"}
    path = directory / "inspection-note-with-subtype.yaml"
    path.write_bytes(yaml.safe_dump(document, sort_keys=True).encode("utf-8"))
    return path


def _subtype_gate_surface(workspace: Path) -> Path:
    """Compile the fixture-plus-subtype ontology and return its accepted surface."""

    producer = workspace / "producer"
    if not producer.exists():
        _module("prepare_producer").prepare(
            ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
        )
    gate = workspace / "gate-subtype"
    assert _module("compile_ontology_candidate").compile_candidate(
        ontology_path=_subtype_ontology(workspace),
        producer_root=producer,
        output=gate,
        attempt=1,
    )
    return gate / "population-surface.json"


def _subject_population_file(directory: Path) -> Path:
    """The fixture records with one naming its subject and one naming none.

    Both are of the bearing type. The first is what the v4.4 restriction was
    written for and is reached through its subject; the second is what E-0197
    found run-21 carrying 237 of and what v4.12's fourth case kind reaches.
    """

    plan = json.loads((FIXTURE / "document-plan.json").read_bytes())
    capture = json.loads((FIXTURE / "document-capture.json").read_bytes())
    capture["assertions"][0]["formalized_by"].extend(
        (
            {"path": ["properties", SUBJECT_SLOT], "record_id": SUBJECT_RECORD_ID},
            {
                "path": ["properties", SUBJECT_TAGS_SLOT],
                "record_id": SUBJECT_TARGET_ID,
            },
            {
                "path": ["properties", "inspected_on"],
                "record_id": UNATTACHED_RECORD_ID,
            },
        )
    )
    records = deepcopy(plan["records"])
    records["entities"].append(
        {
            "id": UNATTACHED_RECORD_ID,
            "properties": {"inspected_on": UNATTACHED_INSPECTED_ON},
            "type": "Inspection",
        }
    )
    for entity in records["entities"]:
        if entity["id"] == SUBJECT_RECORD_ID:
            entity["properties"][SUBJECT_SLOT] = SUBJECT_TARGET_ID
        if entity["id"] == SUBJECT_TARGET_ID:
            entity["properties"][SUBJECT_TAGS_SLOT] = list(SUBJECT_TARGET_TAGS)
    path = directory / "document-population-with-subject.json"
    path.write_bytes(
        _canonical(
            {
                "capture": capture,
                "records": records,
                "supersessions": plan["supersessions"],
            }
        )
    )
    return path


def _run(script: str, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    environment = {
        "PATH": "/usr/bin:/bin",
        "PYTHONPATH": f"{ROOT}:{ROOT / 'src'}",
    }
    return subprocess.run(
        [sys.executable, str(HERE / f"{script}.py"), *arguments],
        capture_output=True,
        cwd=ROOT,
        env=environment,
        text=True,
    )


def _executed(workspace: Path) -> tuple[Path, dict[str, object]]:
    results = workspace / "results"
    completed = _run(
        "run",
        [
            *_source_arguments(),
            "--reading",
            str(FIXTURE / "reading.json"),
            "--population",
            str(_population_file(workspace)),
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            PLAN_ID,
            "--source-id",
            SOURCE_ID,
            "--artifact-id",
            ARTIFACT_ID,
            "--ledger",
            str(workspace / "history.jsonl"),
            "--results",
            str(results),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    assert completed.returncode == 0, completed.stderr
    return results, json.loads((results / "run-result.json").read_bytes())


def test_no_paper_module_names_a_core_protocol_internal() -> None:
    scripts = sorted(path.name for path in HERE.glob("*.py"))

    assert scripts == [
        "bind_from_surface.py",
        "compile_ontology_candidate.py",
        "native_query.py",
        "offline_validation.py",
        "pin.py",
        "prepare_producer.py",
        "run.py",
        "test_contract.py",
        "test_pipeline.py",
        "usage_from_launch_log.py",
    ]
    for name in scripts:
        text = (HERE / name).read_text(encoding="utf-8")
        for symbol in FORBIDDEN_SYMBOLS:
            assert symbol not in text, f"{name} names {symbol}"


def test_the_four_carried_harness_files_are_run_21s_bytes() -> None:
    """The runner, the gate, the deriver and the message.

    Every one of them is run-21's file with the run id substituted and nothing
    else: neither how the run executes, nor how the gate refuses, nor what the
    producer is told moves under v4.12. The other five files in this directory
    each carry a change and each has its own table and its own test, and the
    file list is closed, so a tenth file or a second edit inside any of these
    four fails here rather than travelling with the cell.
    """

    assert set(CARRIED_WITH_THE_RUN_ID) == {
        "compile_ontology_candidate.py",
        "run.py",
        "spawn-message.md",
        "usage_from_launch_log.py",
    }
    assert set(CARRIED_WITH_THE_RUN_ID) & set(CHANGED_BY_V4_12) == set()
    assert sorted(
        path.name
        for path in HERE.iterdir()
        if path.suffix in {".py", ".md"} and not path.name.startswith("test_")
    ) == sorted(
        CARRIED_WITH_THE_RUN_ID + tuple(CHANGED_BY_V4_12) + ("pin.py",)
    )
    for name in CARRIED_WITH_THE_RUN_ID:
        here, expected = _carried(name)
        assert here == expected, name
        assert "run-21" not in here, name
        assert "run_21" not in here, name
        # The table reverses: undo the substitutions and run-21's file comes
        # back, so a second edit cannot ride along inside the run id move.
        reversed_text = here
        for before, after in RUN_ID_SUBSTITUTIONS:
            reversed_text = reversed_text.replace(after, before)
        assert reversed_text == (RUN_21 / name).read_text(encoding="utf-8"), name

    runner = (HERE / "run.py").read_text(encoding="utf-8")
    # Once for the plan compiler and once for the document adapter, so Core-12's
    # evaluative-slot check stays in force; a runner that dropped the second
    # would skip EVALUATIVE_SLOT_NOT_EVALUATED in silence.
    assert runner.count("contract_view=retention.contract_view") == 2
    assert STOP_RULE_SENTENCE in _plain(SPAWN_MESSAGE.read_text(encoding="utf-8"))
    assert STOP_RULE_SENTENCE not in _plain(
        (RUN_04 / "spawn-message.md").read_text(encoding="utf-8")
    )
    # The spawn message is run-21's with the run id moved and nothing else, so
    # the producer is told exactly what run-21's producer was told. This is the
    # producer-side half of the replicate claim and it is byte-exact.
    message, expected_message = _carried("spawn-message.md")
    assert message == expected_message
    assert message == (
        (RUN_21 / "spawn-message.md")
        .read_text(encoding="utf-8")
        .replace("run-21", "run-22")
    )


def test_the_four_changed_files_reverse_through_their_tables_to_run_21s_bytes() -> None:
    """v4.12's whole edit surface, stated as four tables and reversed.

    A cell that changes a file has to say what it changed in it, and saying it
    in prose is what lets a second edit ride along. Each of these four files is
    read as run-21's bytes with the run id moved and then its own table applied;
    reversing both tables must give run-21's file back byte for byte. Every
    entry of every table is required to appear exactly once, so an anchor that
    matched twice, or a change made outside a table, fails here.
    """

    assert set(CHANGED_BY_V4_12) == {
        "bind_from_surface.py",
        "native_query.py",
        "offline_validation.py",
        "prepare_producer.py",
    }
    # The three changes and the files they land in. Every file a change names
    # is a file with a table or is the pin, and every changed file is named by
    # at least one change: v4.12 has no edit that no entry accounts for.
    named = {name for files in V4_12_CHANGES.values() for name in files}
    assert named == set(CHANGED_BY_V4_12) | {"pin.py"}
    assert set(V4_12_CHANGES) == {
        "CANONICAL_PROFILE_STAGING",
        "ENTITY_NO_SUBJECT_REACHABILITY",
        "TYPE_SET_CLOSURE_AT_BIND_TIME",
    }

    for name, table in sorted(CHANGED_BY_V4_12.items()):
        here = (HERE / name).read_text(encoding="utf-8")
        prior = (RUN_21 / name).read_text(encoding="utf-8")
        assert here != prior, name
        carried = prior
        for before, after in RUN_ID_SUBSTITUTIONS:
            carried = carried.replace(before, after)
        built = carried
        for before, after in table:
            assert built.count(before) == 1, (name, before[:60])
            built = built.replace(before, after)
        assert built == here, name
        reversed_text = here
        for before, after in reversed(table):
            assert here.count(after) == 1, (name, after[:60])
            reversed_text = reversed_text.replace(after, before)
        for before, after in RUN_ID_SUBSTITUTIONS:
            reversed_text = reversed_text.replace(after, before)
        assert reversed_text == prior, name


def test_native_query_is_run_21s_executor_with_a_fourth_case_kind() -> None:
    """The executor gains one kind and no row kind, and nothing else.

    Run-21's executor carries the v4.9 removal and names no cell, so run-22's
    differs from it only by the ENTITY_NO_SUBJECT table above, which the
    previous test reverses. What this one holds is the shape of the addition:
    a fourth case kind in every one of the four maps that key on a kind, one
    more row builder, and three row kinds still, because the new kind writes an
    ENTITY row. The spans hold the rest of the file against run-08's bytes, so
    it cannot drift away from the executor every cell from run-02 onward ran.
    """

    text = (HERE / "native_query.py").read_text(encoding="utf-8")
    prior = (RUN_21 / "native_query.py").read_text(encoding="utf-8")

    # The executor still names no cell of its own; what it names is the cells
    # the carried removal and this cell's addition were measured on.
    assert "run-22" not in text
    assert "run_22" not in text
    assert text.count("Run-13's 515 rows") == 1
    assert text.count("run-14's 919 carried 44") == 1
    assert text.count("Run-21 populated 237") == 1
    assert text.count(BINDING_SCHEMA_V5) == 1
    assert BINDING_SCHEMA_V4 not in text
    assert prior.count(BINDING_SCHEMA_V4) == 1
    assert text.count('RESULT_SCHEMA = "malleus.paper-v4.query-result/v3"') == 1
    assert "malleus.paper-v4.query-result/v2" not in text
    # The carried v4.7 delta is still exactly one edit, on the own-type fields.
    assert text.count('SUBJECT_TAGS_SLOT = "tags"') == 1
    assert (
        text.count(
            '                "subject": _project(\n'
            "                    subject,\n"
            "                    [*_own_fields(subject, projections),"
            " SUBJECT_TAGS_SLOT],\n"
            "                ),\n"
        )
        == 1
    )
    assert "SUBJECT_TAGS_SLOT" not in (
        RUN_09 / "native_query.py"
    ).read_text(encoding="utf-8")
    # No row carries the singular field, at any kind, and the fourth kind
    # writes its ordinals the same way the other three do.
    assert '"case_ordinal":' not in text
    assert text.count('"case_ordinals": [case["ordinal"]],') == 4

    # The bytes every cell from run-02 to run-08 ran are still one file.
    for prior_cell in (RUN_02, RUN_03, RUN_04, RUN_05, RUN_06, RUN_07):
        assert (prior_cell / "native_query.py").read_bytes() == (
            RUN_08 / "native_query.py"
        ).read_bytes(), prior_cell.name
    # Every region run-08 already had and neither the carried removal nor this
    # cell's addition touches is still run-08's, ``_project`` included.
    for start, end in (
        ("class _SourceFreeGuard:", "        self._stack.close()\n"),
        (
            "def trace_witnesses(",
            "    return [traced[record_id] for record_id in sorted(traced)]\n",
        ),
        ("def execute(arguments: argparse.Namespace)", "    return result\n"),
        ("def _project(", "    return {name: record[name] for name in fields if name in record}\n"),
        ("FORBIDDEN_ATTEMPTS = ", "    }\n)\n"),
    ):
        assert _span(text, start, end) == _span(
            (RUN_08 / "native_query.py").read_text(encoding="utf-8"), start, end
        ), start

    subject = _module("native_query")
    prior_module = _binder_of(
        RUN_21, "paper_v4_run_21_native_query", "native_query"
    )
    assert subject.RESULT_SCHEMA == "malleus.paper-v4.query-result/v3"
    assert subject.BINDING_SCHEMA == BINDING_SCHEMA_V5
    assert subject.SUBJECT_TAGS_SLOT == "tags"
    assert subject.SUBJECT_SLOT == "subject"
    assert subject.RECORD_TYPE_SLOT == "type"
    assert subject.ENTITY_NO_SUBJECT == ENTITY_NO_SUBJECT
    # The row kind the new case writes is the one an ENTITY case already wrote.
    assert subject.ENTITY_ROW_KIND == "ENTITY"
    assert subject.CASE_KINDS == (
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
    )
    assert prior_module.CASE_KINDS == ("ENTITY", "RELATION", "SUBJECT")
    assert set(subject.CASE_KINDS) - set(prior_module.CASE_KINDS) == {
        ENTITY_NO_SUBJECT
    }
    assert sorted(subject._ROWS_BY_KIND) == list(subject.CASE_KINDS)
    assert sorted(subject._CASE_FIELDS) == sorted(subject._OUTPUT_FIELDS)
    assert sorted(subject._CASE_FIELDS) == list(subject.CASE_KINDS)
    # The new kind's grammar is the ENTITY kind's, which is what makes its row
    # an ENTITY row rather than a fourth shape the reviewer has to learn.
    for mapping in (
        subject._CASE_FIELDS,
        subject._OUTPUT_FIELDS,
        subject._TYPE_FIELDS,
        subject._PROJECTED_TYPES,
    ):
        assert mapping[ENTITY_NO_SUBJECT] == mapping["ENTITY"]
    # The three carried kinds do not move at all.
    for kind in prior_module.CASE_KINDS:
        assert subject._CASE_FIELDS[kind] == prior_module._CASE_FIELDS[kind], kind
        assert subject._OUTPUT_FIELDS[kind] == prior_module._OUTPUT_FIELDS[kind], kind
        assert subject._TYPE_FIELDS[kind] == prior_module._TYPE_FIELDS[kind], kind
        assert (
            subject._PROJECTED_TYPES[kind] == prior_module._PROJECTED_TYPES[kind]
        ), kind
    assert subject.RESULT_SCHEMA == prior_module.RESULT_SCHEMA
    # The carried removal reads a case's projected fields per declared type, so
    # every kind's output fields are covered and no key outside the grammar is.
    assert sorted(subject._PROJECTED_TYPES) == list(subject.CASE_KINDS)
    for kind, pairs in subject._PROJECTED_TYPES.items():
        assert {field for _, field in pairs} == subject._OUTPUT_FIELDS[kind], kind
        assert {key for key, _ in pairs} <= subject._CASE_FIELDS[kind], kind


def test_pin_is_run_21s_bytes_with_the_reference_cell_and_the_staging_table() -> None:
    """The one file that names the cell it carries from, and gains code here.

    ``pin.py`` writes ``pin_status`` on every Core entry and reads the declared
    inputs against a reference run, so carrying it means moving two things: the
    run id, and the cell of record. Run-18 had to move a third because Core did
    not stand still under it; this cell has to add a fourth of its own, because
    v4.12 stages one declared input as canonical JSON and the manifest the pin
    writes has to say so. The four blocks it adds carry run-22's own markers,
    the five run-18 added are here as bytes with run-18's markers, and the file
    reverses through all three tables to run-21's byte for byte with nothing
    removed first. An edit in no table fails.
    """

    here = (HERE / "pin.py").read_text(encoding="utf-8")
    prior = (RUN_21 / "pin.py").read_text(encoding="utf-8")

    assert here != prior
    reversed_text = here
    for before, after in reversed(PIN_V4_12_STAGING):
        assert here.count(after) == 1, after[:60]
        reversed_text = reversed_text.replace(after, before)
    for before, after in reversed(PIN_REFERENCE_CELL):
        assert here.count(after) >= 1, after[:60]
        reversed_text = reversed_text.replace(after, before)
    for before, after in RUN_ID_SUBSTITUTIONS:
        reversed_text = reversed_text.replace(after, before)
    assert reversed_text == prior
    # Run-18's five marked blocks are carried whole, markers included, and both
    # files carry every one of them exactly once.
    for label in PIN_ADDITION_MARKERS:
        for text, name in ((here, "run-22"), (prior, "run-21")):
            assert text.count(f"{ADDITION_BEGINS}{label}\n") == 1, (label, name)
            assert text.count(f"{ADDITION_ENDS}{label}\n") == 1, (label, name)
    assert here.count(ADDITION_BEGINS) == len(PIN_ADDITION_MARKERS)
    assert here.count(ADDITION_ENDS) == len(PIN_ADDITION_MARKERS)
    assert here.count(ADDITION_BEGINS) == prior.count(ADDITION_BEGINS)
    # This cell's own four are marked with its own run id and are in no earlier
    # cell's pin, so what run-22 added to the pin can be read off the file.
    for label in PIN_RUN_22_ADDITION_MARKERS:
        assert here.count(f"{RUN_22_ADDITION_BEGINS}{label}\n") == 1, label
        assert here.count(f"{RUN_22_ADDITION_ENDS}{label}\n") == 1, label
    assert here.count(RUN_22_ADDITION_BEGINS) == len(PIN_RUN_22_ADDITION_MARKERS)
    assert here.count(RUN_22_ADDITION_ENDS) == len(PIN_RUN_22_ADDITION_MARKERS)
    assert RUN_22_ADDITION_BEGINS not in prior

    # What the three tables are for, read off the module rather than the text.
    pin = _module("pin")
    assert pin.RUN_ID == "run-22"
    assert pin.PROTOCOL_VERSION == "v4.12"
    assert pin.INTERFACE_ORDINAL == "22"
    assert pin.CARRIED == CARRIED_PIN_STATUS
    assert pin.REFERENCE_RUN == "run-21"
    assert pin.REFERENCE_MANIFEST == (
        "paper-v4/experiment-v4/run-21/producer-input-manifest.json"
    )
    assert (ROOT / pin.REFERENCE_MANIFEST).is_file()
    assert pin.CARRIED in CORE_PIN_STATUSES
    # The protocol version does move, and Core does not: this cell is the first
    # of v4.12 at the coordinate run-21 pinned.
    prior_pin = _binder_of(RUN_21, "paper_v4_run_21_pin", "pin")
    assert prior_pin.PROTOCOL_VERSION == "v4.10"
    assert pin.PROTOCOL_VERSION != prior_pin.PROTOCOL_VERSION
    assert prior_pin.INTERFACE_ORDINAL == "21"
    assert prior_pin.CARRIED == "CARRIED_FROM_RUN_20"
    assert prior_pin.REFERENCE_RUN == "run-20"
    # The staging table, read off the module. One input is staged canonical and
    # the cause of a moved input is named rather than left to be guessed at.
    assert pin.CANONICAL_JSON_INPUTS == frozenset({"SOURCE_ASSERTION_PROFILE"})
    assert pin.CANONICAL_JSON == "CANONICAL_JSON"
    assert pin.SOURCE_BYTES == "SOURCE_BYTES"
    assert pin.MOVED_BY_THE_HARNESS == {
        "SOURCE_ASSERTION_PROFILE": "STAGED_AS_CANONICAL_JSON_FROM_V4_12"
    }
    assert not hasattr(prior_pin, "CANONICAL_JSON_INPUTS")
    # Both statuses exist at run-21 too, because the two entries they belong to
    # are run-18's and are carried through it rather than rewritten.
    assert pin.LANDED == "LANDED"
    assert pin.PENDING == "PENDING_AT_PIN"
    assert {pin.LANDED, pin.PENDING} == READ_AT_THE_PIN_STATUSES
    assert prior_pin.LANDED == pin.LANDED
    assert prior_pin.PENDING == pin.PENDING
    # The baseline the two carried entries are read against is the coordinate
    # run-17 pinned, which is still where every other carried entry stops.
    assert pin.V4_8_COMMIT == prior_pin.V4_8_COMMIT == V4_9_COORDINATE


def test_the_pin_refuses_landed_for_core_20_unless_the_paragraph_carries_every_reason() -> None:
    """The guard the carried Core-20 entry needs, driven on synthetic text.

    Core-20's whole content is that the skill's pre-flight paragraph carries the
    two enums' refusal reasons, each of them and no other. A pin that recorded
    LANDED off a paragraph missing one would say a producer had a list to check
    against when it did not, and this cell's whole subject is what that list
    does for a producer that reads it. The decision is a pure function of three
    strings, so it is driven here with a paragraph built to be wrong in one way
    at a time; no commit is read.
    """

    pin = _module("pin")
    reasons = ["ALPHA_ONE", "BETA_TWO", "GAMMA_THREE"]
    marker = pin.PREFLIGHT_MARKER
    guard = (
        "DocumentAssertionRefusalReason PopulationPlanRefusalReason"
        f" {marker}"
    )

    def skill(body: str) -> str:
        return (
            "before\n"
            f"<!-- {marker}:start -->\n{body}\n<!-- {marker}:end -->\n"
            "after\n"
        )

    complete = skill("\n".join(f"- {reason}: check it." for reason in reasons))
    observed = pin.preflight_observation(complete, guard, reasons)
    assert observed["paragraph_present"] is True
    assert observed["reasons_absent_from_the_paragraph"] == []
    assert observed["reasons_the_paragraph_invents"] == []
    assert pin.preflight_status(observed) == pin.LANDED

    # One reason missing: PENDING, and the entry names which one.
    short = skill("\n".join(f"- {reason}: check it." for reason in reasons[:-1]))
    observed = pin.preflight_observation(short, guard, reasons)
    assert observed["reasons_absent_from_the_paragraph"] == ["GAMMA_THREE"]
    assert observed["every_reason_named"] is False
    assert pin.preflight_status(observed) == pin.PENDING

    # One reason neither enum carries: PENDING too, because a producer told to
    # check for a refusal that cannot happen is being told something untrue.
    invented = skill(
        "\n".join(f"- {reason}: check it." for reason in [*reasons, "DELTA_FOUR"])
    )
    observed = pin.preflight_observation(invented, guard, reasons)
    assert observed["reasons_the_paragraph_invents"] == ["DELTA_FOUR"]
    assert pin.preflight_status(observed) == pin.PENDING

    # No markers at all: PENDING, and no reason counted as named.
    observed = pin.preflight_observation("no paragraph here", guard, reasons)
    assert observed["paragraph_present"] is False
    assert observed["reasons_named_in_the_paragraph"] == []
    assert pin.preflight_status(observed) == pin.PENDING

    # The paragraph is complete but the guard does not derive it from the enums:
    # PENDING, because a hand-written list is what drifts.
    for weak in ("", "DocumentAssertionRefusalReason", f"{marker} only"):
        observed = pin.preflight_observation(complete, weak, reasons)
        assert observed["every_reason_named"] is True
        assert pin.preflight_status(observed) == pin.PENDING, weak


def test_the_carried_delta_projects_tags_only_on_the_subject_side_and_only_when_present() -> None:
    """The carried v4.7 delta at the row level, on rows built in isolation.

    A subject that carries ``tags`` projects them beside its own type's fields;
    one that does not projects exactly what run-09 projected. The record side
    never gains the field and the two other kinds are untouched. Run-09's
    executor is the comparison because it is the last one without the tags
    delta, and it is driven with the same projections the case names, so the
    only difference the comparison can show is the delta itself.
    """

    subject = _module("native_query")
    prior = _binder_of(
        RUN_09, "paper_v4_run_09_native_query_rows", "native_query"
    )
    assert "SUBJECT_TAGS_SLOT" not in (
        RUN_09 / "native_query.py"
    ).read_text(encoding="utf-8")

    class _Graph:
        def __init__(self, records: dict[str, list[dict]]) -> None:
            self._records = records

        def query(self, record_type: str) -> list[dict]:
            return list(self._records.get(record_type, ()))

    tagged = {
        "id": "asset:P-7",
        "type": "Asset",
        "name": "Pump P-7",
        "tags": ["P-7", "P7"],
    }
    bare = {"id": "asset:P-8", "type": "Asset", "name": "Pump P-8"}
    records = [
        {
            "id": "inspection:1",
            "type": "Inspection",
            "inspected_on": "2026-03-02",
            "subject": "asset:P-7",
        },
        {
            "id": "inspection:2",
            "type": "Inspection",
            "inspected_on": "2026-03-03",
            "subject": "asset:P-8",
        },
    ]
    graph = _Graph({"Asset": [tagged, bare], "Inspection": records})
    case = {
        "kind": "SUBJECT",
        "ordinal": 1,
        "output_fields": {"record": ["inspected_on", "subject"], "subject": ["name"]},
        "record_type": "Inspection",
        "subject_record_type": "Asset",
    }
    projections = {"Asset": ["name"], "Inspection": ["inspected_on", "subject"]}

    witnesses: list[str] = []
    rows = subject._subject_rows(graph, case, witnesses, projections)
    prior_rows = prior._subject_rows(graph, dict(case), [])

    assert [row["subject"] for row in rows] == [
        {"name": "Pump P-7", "tags": ["P-7", "P7"]},
        {"name": "Pump P-8"},
    ]
    # Run-09's executor on the same graph and the same projection: the tagged
    # subject is the only difference, and it is an addition.
    assert [row["subject"] for row in prior_rows] == [
        {"name": "Pump P-7"},
        {"name": "Pump P-8"},
    ]
    # The record side, the witnesses and the row order are untouched.
    assert [row["record"] for row in rows] == [row["record"] for row in prior_rows]
    assert [row["witness"] for row in rows] == [row["witness"] for row in prior_rows]
    assert witnesses == ["inspection:1", "asset:P-7", "inspection:2", "asset:P-8"]
    for row in rows:
        assert "tags" not in row["record"]
        assert "type" not in row["record"]
        assert row["case_ordinals"] == [1]

    # The other two kinds project the same fields either way; only the ordinal
    # field's name moves, which is this cell's delta and not the tags one.
    entity_case = {
        "kind": "ENTITY",
        "ordinal": 1,
        "output_fields": {"record": ["name"]},
        "record_type": "Asset",
    }
    here_rows = subject._entity_rows(graph, entity_case, [], projections)
    there_rows = prior._entity_rows(graph, dict(entity_case), [])
    assert [row["record"] for row in here_rows] == [
        {"name": "Pump P-7"},
        {"name": "Pump P-8"},
    ]
    assert [row["record"] for row in here_rows] == [
        row["record"] for row in there_rows
    ]
    assert [row["witness"] for row in here_rows] == [
        row["witness"] for row in there_rows
    ]
    assert [row["case_ordinals"] for row in here_rows] == [[1], [1]]
    assert [row["case_ordinal"] for row in there_rows] == [1, 1]


def test_two_cases_reaching_one_witness_are_one_row_of_the_records_own_type() -> None:
    """The v4.9 removal at the row level, and the two refusals that guard it.

    A question whose type set names a type and one of its ancestors expands to
    an ENTITY case for each, and the graph returns the same record under both.
    Run-14, the last executor without the removal, wrote two rows, the
    ancestor's with fewer fields; this writes one,
    projected through the record's own type and carrying both ordinals. The
    projections come out of the binding, so a type the binding projects two ways
    and a record whose own type it never names are both refused rather than
    guessed past.
    """

    subject = _module("native_query")

    class _Graph:
        """A two-level hierarchy: ``query`` on the parent returns the child."""

        def __init__(self, records: list[dict], subtypes: dict[str, list[str]]):
            self._records = records
            self._subtypes = subtypes

        def query(self, record_type: str) -> list[dict]:
            wanted = {record_type, *self._subtypes.get(record_type, ())}
            return [item for item in self._records if item["type"] in wanted]

        def query_relations(self, relation_type: str | None = None) -> list[dict]:
            return []

    class _Replay:
        def __init__(self, graph) -> None:
            self.graph = graph

    pump = {
        "id": "asset:P-7",
        "type": "Pump",
        "name": "Pump P-7",
        "serial": "SN-7",
    }
    graph = _Graph([pump], {"Asset": ["Pump"]})
    binding = {
        "queries": [
            {
                "id": "NQ-CQ-01",
                "question_id": "CQ-01",
                "cases": [
                    {
                        "kind": "ENTITY",
                        "ordinal": 1,
                        "output_fields": {"record": ["name"]},
                        "record_type": "Asset",
                    },
                    {
                        "kind": "ENTITY",
                        "ordinal": 2,
                        "output_fields": {"record": ["name", "serial"]},
                        "record_type": "Pump",
                    },
                ],
            }
        ]
    }

    results, witnesses = subject.run_queries(_Replay(graph), binding)
    rows = results[0]["rows"]

    assert len(rows) == 1
    assert rows[0]["case_ordinals"] == [1, 2]
    # The own type's fields, not the ancestor case's fewer ones. Run-14, before
    # the removal, returned {"name": "Pump P-7"} here as well as this, in that
    # order.
    assert rows[0]["record"] == {"name": "Pump P-7", "serial": "SN-7"}
    assert rows[0]["witness"] == {"record_id": "asset:P-7"}
    assert "case_ordinal" not in rows[0]
    # The witness list is unchanged: it is what the tracer dedupes by id.
    assert witnesses == ["asset:P-7", "asset:P-7"]

    # The map the projection comes from is the binding's own per-type fields.
    assert subject.surface_projections(binding) == {
        "Asset": ["name"],
        "Pump": ["name", "serial"],
    }

    # A type projected two ways is refused rather than chosen between.
    conflicting = deepcopy(binding)
    conflicting["queries"][0]["cases"][1]["record_type"] = "Asset"
    with pytest.raises(subject.NativeQueryRefusal) as refusal:
        subject.surface_projections(conflicting)
    assert "projects Asset two ways" in str(refusal.value)

    # A record whose own type the binding never names is refused too: the
    # executor does not fall back to the case's type.
    orphan = {"id": "asset:P-9", "type": "Valve", "name": "Valve P-9"}
    with pytest.raises(subject.NativeQueryRefusal) as refusal:
        subject.run_queries(
            _Replay(_Graph([orphan], {"Asset": ["Valve"]})), binding
        )
    assert "no projection for the record's own type: Valve" in str(refusal.value)


def test_bind_from_surface_keeps_the_v4_4_restriction_and_adds_the_fourth_kind() -> None:
    """The two v4.12 changes in the binder, and the carried ones still in place.

    The reversal test above already holds every byte of this file against
    run-21's; what this one holds is what the two changes mean. The v4.4
    restriction is unchanged and is still read against run-09's
    pre-restriction bytes: a subject-bearing type gets no plain ENTITY case.
    What v4.12 adds beside it is one ENTITY_NO_SUBJECT case for exactly those
    types, and a refusal that runs before the binding is written. v4.7's tags
    delta is in the executor, not here, so the binder's housekeeping set still
    drops ``tags`` from every projection it writes.
    """

    here = (HERE / "bind_from_surface.py").read_text(encoding="utf-8")
    prior = (RUN_09 / "bind_from_surface.py").read_text(encoding="utf-8")
    run_21 = (RUN_21 / "bind_from_surface.py").read_text(encoding="utf-8")

    assert here != prior
    for start, end in (
        ("class BindingRefusal(ValueError):", "def _cases(\n"),
        ("    if len(cases) != expected:", "    return cases\n"),
        (
            '        "population_surface_sha256": _digest(surface_source),',
            "def execute(arguments: argparse.Namespace) -> dict[str, object]:\n",
        ),
        (
            "    type_sets = json.loads(Path(arguments.type_sets).read_bytes())",
            "    binding = build(\n",
        ),
        (
            "    output.parent.mkdir(parents=True, exist_ok=True)",
            '    parser.add_argument("--surface", required=True,'
            ' help="accepted population surface")\n',
        ),
        (
            '    parser.add_argument(\n        "--type-sets", required=True,'
            ' help="question id to surface type list"\n    )',
            "raise SystemExit(main())\n",
        ),
        ("HOUSEKEEPING_SLOTS = frozenset(", "BOUND_BY = ("),
    ):
        assert _span(here, start, end) == _span(prior, start, end), start

    # The carried v4.4 delta, line for line, against the cell before it.
    assert "unattached = [name for name in types if name not in set(bearing)]" in here
    assert "unattached = " not in prior
    assert "    for record_type in unattached:\n" in here
    assert "    for record_type in types:\n" in prior
    assert "    for record_type in types:\n" not in here
    assert "        len(unattached)\n" in here
    assert "entity_case_scope" in here
    assert "entity_case_scope" not in prior
    # The SUBJECT loop is untouched: subject-bearing types are still reached
    # through their subject, and the v4.12 addition does not replace that.
    assert _span(
        here, "    for record_type in bearing:\n        for subject_type", "    expected = (\n"
    ) == _span(
        prior, "    for record_type in bearing:\n        for subject_type", "    expected = (\n"
    )

    # v4.12, change one: the fourth kind, emitted for the bearing types alone.
    assert here.count('"kind": ENTITY_NO_SUBJECT,') == 1
    assert "ENTITY_NO_SUBJECT" not in run_21
    assert "        + len(bearing)\n" in here
    assert "        + len(bearing)\n" not in run_21
    assert "entity_no_subject_case_scope" in here
    # v4.12, change two: the closure refusal, before the binding is written.
    assert "def refuse_unclosed(" in here
    assert "refuse_unclosed(" not in run_21
    assert here.index("    refuse_unclosed(") < here.index('        "schema": BINDING_SCHEMA,')
    assert "type_set_closure.py" in here

    binder = _module("bind_from_surface")
    assert binder.BINDING_SCHEMA == BINDING_SCHEMA_V5
    assert _run_21_binder().BINDING_SCHEMA == BINDING_SCHEMA_V4
    assert binder.CASE_KINDS == (
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
    )
    assert binder.CASE_KINDS == tuple(sorted(binder.CASE_KINDS))
    assert _run_21_binder().CASE_KINDS == ("ENTITY", "RELATION", "SUBJECT")
    assert binder.ENTITY_NO_SUBJECT == ENTITY_NO_SUBJECT
    assert binder.SUBJECT_SLOT == "subject"
    assert binder.CLOSURE_CHECK == (
        "TYPE_SET_CLOSED_UNDER_THE_SURFACES_SUBTYPES_AT_BIND_TIME"
    )
    # The closure reader is the shared file every cell from v4.11 reads, loaded
    # by path and not copied into the cell.
    closure = binder._type_set_closure()
    assert closure.REASON == "TYPE_SET_NOT_CLOSED_UNDER_SUBTYPES"
    assert (HERE.parent / "type_set_closure.py").is_file()
    # The v4.7 delta is not here: the binder still calls ``tags`` housekeeping
    # and names it in no projection it writes.
    assert "https://malleus.dev/schema/tags" in binder.HOUSEKEEPING_SLOTS
    assert binder.HOUSEKEEPING_SLOTS == _run_21_binder().HOUSEKEEPING_SLOTS
    assert "SUBJECT_TAGS_SLOT" not in here


def test_the_binder_refuses_a_type_set_that_omits_a_surface_subtype(
    private_workspace: Path,
) -> None:
    """v4.12, change two, driven on a surface that carries a subtype.

    Run-21's first binding listed a parent and not its surface subtype; the
    facade returned the subtype's records and the executor refused a type the
    binding never named, after the rows existed (E-0196). v4.11 answered that
    with a reader the procedure ran by hand between writing the sets and binding
    them. Here the binder runs it, so the refusal happens where the evaluator
    can still correct the set and there is no binding file to skip it with.
    """

    subject = _module("bind_from_surface")
    surface_path = _subtype_gate_surface(private_workspace)
    contract_path = _gate_contract(surface_path)
    output = private_workspace / "binding-unclosed.json"

    # The parent alone: the surface carries a subtype of it, so the set is not
    # closed and no binding is written.
    with pytest.raises(subject.BindingRefusal) as refusal:
        subject.build(
            surface_source=surface_path.read_bytes(),
            type_sets={"CQ-01": ["Asset", "Inspection"]},
            replay_receipt="PENDING",
            contract_source=contract_path.read_bytes(),
        )
    assert "TYPE_SET_NOT_CLOSED_UNDER_SUBTYPES" in str(refusal.value)
    assert "CQ-01 omits ProbeInspection" in str(refusal.value)

    completed = _run(
        "bind_from_surface",
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(contract_path),
            "--type-sets",
            str(
                _type_set_file(
                    private_workspace, {"CQ-01": ["Asset", "Inspection"]}
                )
            ),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(output),
        ],
    )
    assert completed.returncode == 2
    assert "TYPE_SET_NOT_CLOSED_UNDER_SUBTYPES" in completed.stderr
    assert not output.exists()

    # The closed set binds, and the binding it writes is the one the executor
    # can project: every reached record's own type is named.
    closed = subject.build(
        surface_source=surface_path.read_bytes(),
        type_sets={"CQ-01": ["Asset", "Inspection", "ProbeInspection"]},
        replay_receipt="PENDING",
        contract_source=contract_path.read_bytes(),
    )
    assert closed["type_sets"]["CQ-01"] == ["Asset", "Inspection", "ProbeInspection"]
    assert closed["expansion"]["closure_checked"] == subject.CLOSURE_CHECK
    # The contract is required: a binding cannot be written without one.
    assert _run(
        "bind_from_surface",
        [
            "--surface",
            str(surface_path),
            "--type-sets",
            str(_type_set_file(private_workspace, {"CQ-02": ["Asset"]})),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(private_workspace / "binding-no-contract.json"),
        ],
    ).returncode == 2
    assert not (private_workspace / "binding-no-contract.json").exists()


def test_offline_validation_is_run_21s_with_the_run_id_moved() -> None:
    """Carried whole, and the record it writes still recomputes to run-21's counts.

    ``offline_validation.py`` computes the carried v4.4 restriction and the
    carried v4.9 collapse on run-09's frozen record, and from v4.12 a third
    stage beside them. Neither the v4.4 rule nor the v4.9 collapse moved this
    cell, so those two stages must return run-21's numbers exactly, key for
    key; a rule that returns other numbers is a different rule and this test
    fails rather than the record being adjusted to match. The third stage is
    the addition, measured on the same frozen record because run-09 ran under
    the v3 binding and its result already carries the rows the new kind
    returns.
    """

    here = (HERE / "offline_validation.py").read_text(encoding="utf-8")
    prior = (RUN_21 / "offline_validation.py").read_text(encoding="utf-8")

    for carried in (
        "def witness_identity(",
        '"rows_one_per_witness"',
        '"rows_re_projected"',
        '"rows_re_projected_under_another_label"',
        '"and_change_id": "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION"',
    ):
        assert carried in here, carried
        assert carried in prior, carried

    record = json.loads(OFFLINE_VALIDATION.read_bytes())
    prior_record = json.loads((RUN_21 / "offline-validation.json").read_bytes())
    contract = json.loads(CONTRACT_PATH.read_bytes())["offline_validation"]
    totals = record["totals"]
    prior_totals = prior_record["totals"]

    assert record["run_id"] == "run-22"
    assert prior_record["run_id"] == "run-21"
    assert record["schema"] == "malleus.paper-v4.run-22-offline-validation/v2"
    assert prior_record["schema"] == "malleus.paper-v4.run-21-offline-validation/v1"
    assert record["change_id"] == "ENTITY_KIND_RESTRICTED"
    assert record["and_change_id"] == "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION"
    assert record["third_change_id"] == "ENTITY_NO_SUBJECT_REACHABILITY"
    assert "third_change_id" not in prior_record
    assert record["measured_on"] == "run-09"

    # The two carried stages, unchanged against run-21's record, key by key.
    assert {
        name: value for name, value in totals.items() if "restored" not in name
    } == prior_totals
    assert [
        {name: value for name, value in question.items() if "restored" not in name}
        for question in record["questions"]
    ] == prior_record["questions"]
    # The third stage is the addition and is not in run-21's record at all.
    assert totals["rows_restored_by_entity_no_subject"] == 429
    assert totals["rows_restored_witnesses"] == 373
    assert totals["rows_restored_new_witnesses"] == 373
    assert totals["rows_restored_by_label"] == {"PARTIAL": 2, "SUPPORTED": 427}
    assert sum(totals["rows_restored_by_label"].values()) == (
        totals["rows_restored_by_entity_no_subject"]
    )
    # Every restored row is a row the v4.4 restriction removed, and every
    # restored witness is one no kept case reaches: the addition gives back
    # what that removal took and reaches nothing the other kinds already did.
    assert totals["rows_restored_by_entity_no_subject"] <= totals["rows_removed"]
    assert totals["rows_restored_new_witnesses"] == (
        totals["rows_restored_witnesses"]
    )
    assert sum(
        question["rows_restored_by_entity_no_subject"]
        for question in record["questions"]
    ) == totals["rows_restored_by_entity_no_subject"]
    assert totals["rows_v3"] == 1466
    assert totals["rows_kept"] == 630
    assert totals["rows_kept_by_label"] == {"PARTIAL": 12, "SUPPORTED": 618}
    assert totals["rows_one_per_witness"] == 463
    assert totals["rows_re_projected"] == 167
    assert totals["rows_one_per_witness"] + totals["rows_re_projected"] == (
        totals["rows_kept"]
    )
    assert totals["rows_re_projected_under_another_label"] == 0
    assert sum(totals["rows_one_per_witness_by_kind"].values()) == (
        totals["rows_one_per_witness"]
    )
    assert sum(totals["rows_one_per_witness_by_label"].values()) == (
        totals["rows_one_per_witness"]
    )
    for question in record["questions"]:
        assert question["rows_one_per_witness"] + question["rows_re_projected"] == (
            question["rows_kept"]
        )
    assert sum(
        question["rows_one_per_witness"] for question in record["questions"]
    ) == totals["rows_one_per_witness"]

    # The record is what the script returns today, not a copy of run-21's.
    assert _module("offline_validation").validate() == record
    assert record["inputs"]["binder"]["path"] == (
        "paper-v4/experiment-v4/run-22/bind_from_surface.py"
    )
    assert record["inputs"]["binder"]["sha256"] == _digest(
        (HERE / "bind_from_surface.py").read_bytes()
    )

    # The contract carries the same four numbers, so neither can drift alone.
    assert contract["rows_kept"] == totals["rows_kept"]
    assert contract["rows_one_per_witness"] == totals["rows_one_per_witness"]
    assert contract["rows_re_projected"] == totals["rows_re_projected"]
    assert contract["rows_re_projected_under_another_label"] == 0
    assert contract["and_change_id"] == record["and_change_id"]
    assert contract["third_change_id"] == record["third_change_id"]
    assert contract["rows_restored_by_entity_no_subject"] == (
        totals["rows_restored_by_entity_no_subject"]
    )
    assert contract["rows_restored_witnesses"] == totals["rows_restored_witnesses"]
    assert contract["rows_restored_new_witnesses"] == (
        totals["rows_restored_new_witnesses"]
    )
    assert contract["carried_from"] == "run-21"


def test_every_v4_12_change_is_present_in_the_file_that_carries_it() -> None:
    """One marker per harness change id, read from the contract, found in its
    subject.

    Every one of the thirty entries run-21 closed with is carried, the fourteen
    harness ones included, and four are added: v4.12's three and this cell's own
    producer record. That leaves seven entries with no file in this directory to
    grep for, the six closed cells' producer records and this cell's own. The
    two Core entries the pin still reads are carried too, and their evidence is
    the pinned commit rather than a file here. The sets are disjoint and
    together they are the whole change list, so an entry added or dropped fails
    here.
    """

    changes = {
        str(item["id"]): item
        for item in json.loads(CONTRACT_PATH.read_bytes())["protocol"]["changes"]
    }

    assert set(changes) == set(DELTA_MARKERS) | set(CORE_CHANGE_IDS) | {
        MODEL_CHANGE_ID,
        *PRIOR_MODEL_CHANGE_IDS,
    }
    assert set(DELTA_MARKERS) & set(CORE_CHANGE_IDS) == set()
    for change_id in (MODEL_CHANGE_ID, *PRIOR_MODEL_CHANGE_IDS):
        assert change_id not in set(DELTA_MARKERS) | set(CORE_CHANGE_IDS)
    assert set(READ_AT_THE_PIN_CORE_CHANGE_IDS) <= set(CORE_CHANGE_IDS)
    assert len(changes) == 34
    # The three v4.12 entries are the only harness entries that are not carried,
    # and the set of them is the set the tables above declare.
    v4_12 = {
        change_id
        for change_id, entry in changes.items()
        if entry.get("carried_since") == "run-22" and entry.get("kind") == "HARNESS"
    }
    assert v4_12 == set(V4_12_CHANGES)
    for change_id, (relative, marker) in DELTA_MARKERS.items():
        text_of = (ROOT / relative).read_text(encoding="utf-8")
        assert marker in text_of, change_id
        entry = json.dumps(changes[change_id])
        assert Path(relative).name in entry, change_id
        assert changes[change_id]["detail"].strip()
        assert changes[change_id]["why"].strip()
        if change_id in v4_12:
            assert "carried_from" not in changes[change_id], change_id
            # Every file a v4.12 entry names is a file with a table or the pin,
            # and the entry's subject names each of them.
            for name in V4_12_CHANGES[change_id]:
                assert name in changes[change_id]["subject"], (change_id, name)
        else:
            assert changes[change_id]["carried_from"] == "run-21", change_id
    for change_id in CORE_CHANGE_IDS:
        entry = changes[change_id]
        assert entry["pin_status"] in CORE_PIN_STATUSES
        assert entry["core_task"].startswith("Core-")
        # Every Core entry is carried this cell, the two the pin still reads
        # included: Core does not move, so no entry here is this cell's own.
        assert entry["carried_from"] == "run-21", change_id
        if change_id in READ_AT_THE_PIN_CORE_CHANGE_IDS:
            # Carried, and still read: the pin recomputes the status at the
            # commit run-21 pinned against the same v4.8 baseline. Both were
            # written at run-18 and carried since, so ``carried_since`` stays
            # there and only ``carried_from`` steps.
            assert entry["pin_status"] in READ_AT_THE_PIN_STATUSES, change_id
            assert entry["carried_since"] == "run-18", change_id
            assert entry["baseline_commit"] == V4_9_COORDINATE, change_id
            assert entry["carried"] == (
                "READ_AGAIN_AT_THE_SAME_COMMIT_NOT_CARRIED_UNREAD"
            ), change_id
        else:
            assert entry["pin_status"] == CARRIED_PIN_STATUS, change_id
    # This cell's own producer entry has no harness file at all. Core does not
    # move and neither does the producer condition; the harness does, and the
    # entry says so and points at the three entries that carry it rather than
    # restating them.
    model = changes[MODEL_CHANGE_ID]
    assert "carried_from" not in model
    assert model["kind"] == "MODEL_CELL"
    assert model["core_delta"] == "NONE"
    assert model["harness_delta"] == "THREE_CHANGES_STATED_AS_THEIR_OWN_ENTRIES"
    assert model["producer_delta"] == "NONE_EXCEPT_THE_CANONICAL_PROFILE_BYTES"
    assert model["replicates"] == ["run-20", "run-21"]
    assert model["producer_matched_cells"] == ["run-20", "run-21"]
    assert model["model_fields_moved"] == []
    assert model["subject_block"] == "producer"
    assert model["carried_since"] == "run-22"
    assert "core_task" not in model
    # The comparability statement, which is the one thing this cell must not
    # leave to a reader's inference: the producer side and nothing else.
    assert model["comparability"] == (
        "ROWS_AND_REVIEWS_ARE_COMPARABLE_WITH_RUN_20_AND_RUN_21_ON_THE"
        "_PRODUCER_SIDE_ONLY"
    )
    assert "thirty questions" in model["comparability_detail"]
    for name in (*CARRIED_WITH_THE_RUN_ID, *CHANGED_BY_V4_12, "pin.py"):
        assert name not in model["subject"], name
    # The six closed cells' records keep their own subjects and their own model
    # fields; none may be read as this cell's producer. Run-20's and run-21's
    # are among them and carry the same three model fields this cell runs,
    # which is what makes this a replicate on the producer side: the entries
    # that name them are those cells', and this cell's own is the one above.
    for change_id, cell in (
        ("HAIKU_4_5_PRODUCER_AT_V4_9", "run-17"),
        ("HAIKU_4_5_PRODUCER_AT_V4_10", "run-18"),
        ("OPUS_5_PRODUCER_AT_V4_10", "run-20"),
        ("OPUS_5_REPLICATE_AT_V4_10", "run-21"),
        ("SONNET_5_PRODUCER_AT_V4_9", "run-16"),
        ("SONNET_5_PRODUCER_AT_V4_10", "run-19"),
    ):
        entry = changes[change_id]
        assert entry["kind"] == "MODEL_CELL"
        assert entry["carried_from"] == "run-21", change_id
        assert entry["subject_cell"] == cell, change_id
        assert entry["subject"] == (
            f"paper-v4/experiment-v4/{cell}/run-contract.json#producer"
        ), change_id


def test_the_producer_block_is_run_21s_key_for_key_with_nothing_moved() -> None:
    """The whole of what a replicate is, read off the contract and the manifest.

    Run-22 moves nothing. The producer block is run-21's key for key, the three
    model fields included, and the comparison below is the whole guard: one key
    that differed would make this a matrix cell and would be read later as the
    cause of whatever the two cells do not share. Run-21 moved these three
    fields off run-19's and was admitted at its second runner attempt after one
    defect; holding them here is what makes the pair two draws of one condition.
    """

    contract = json.loads(CONTRACT_PATH.read_bytes())
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    producer = contract["producer"]
    prior = json.loads((RUN_21 / "run-contract.json").read_bytes())["producer"]

    assert set(producer) == set(prior)
    assert {
        key: value for key, value in producer.items() if prior[key] != value
    } == {}
    assert producer == prior
    assert {key: producer[key] for key in MODEL_FIELDS} == MODEL_FIELDS
    assert {key: prior[key] for key in MODEL_FIELDS} == PRIOR_MODEL_FIELDS
    assert MODEL_FIELDS == PRIOR_MODEL_FIELDS
    assert manifest["producer"] == producer
    # The manifest is the file the workspace is built from, so the model fields
    # have to be the same three there too.
    assert {key: manifest["producer"][key] for key in MODEL_FIELDS} == MODEL_FIELDS
    # And the harness the model runs under is the same harness.
    assert producer["harness"] == prior["harness"]
    assert producer["kind"] == prior["kind"] == "CLAUDE_CODE_FRESH_SUBAGENT"
    assert producer["session"] == prior["session"] == "FRESH_SINGLE_SESSION"
    assert producer["reasoning_effort"] == prior["reasoning_effort"]
    assert producer["max_compiler_diagnostic_returns"] == 2
    assert producer["max_ontology_revision_rounds"] == 2
    assert producer["fallback"] == "FORBIDDEN"
    assert producer["network"] == "FORBIDDEN"
    assert producer["delegation"] == "FORBIDDEN"


def test_producer_preparation_refuses_output_outside_private() -> None:
    subject = _module("prepare_producer")

    with pytest.raises(subject.ProducerPreparationRefusal):
        subject.prepare(ROOT / "ontology/malleus.yaml", ROOT / "tmp-producer")


def test_producer_preparation_installs_the_claude_layout_and_exact_closure(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    output = private_workspace / "producer"

    receipt = subject.prepare(ROOT / manifest["declared_inputs"][1]["source"], output)

    installed = {
        str(path.relative_to(output))
        for path in output.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    assert installed == {item["target"] for item in manifest["declared_inputs"]}
    assert len(installed) == 8
    assert ".claude/skills/malleus-acolyte/SKILL.md" in installed
    assert not (output / ".codex").exists()
    assert receipt["status"] == "FROZEN"
    assert receipt["core"] == manifest["core"]
    assert (private_workspace / "producer-input-receipt.json").exists()


def test_the_history_profile_is_staged_as_its_canonical_bytes(
    private_workspace: Path,
) -> None:
    """v4.12, change three: the staged file's digest is the profile identity.

    shop-01's producer wrote the staged profile file's digest into four
    population plans, as the parent's phase-two message told it to, and the
    compiler refused every one with IDENTITY_MISMATCH because it digests the
    profile's canonical bytes and not the file's (E-0203, cause B). From here
    the two are the same bytes, so a producer can read the identity off its own
    declared input and the parent has nothing left to hand it.
    """

    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    contract = json.loads(CONTRACT_PATH.read_bytes())
    declared = {item["name"]: item for item in manifest["declared_inputs"]}
    profile = declared["SOURCE_ASSERTION_PROFILE"]
    output = private_workspace / "producer"

    # The manifest states a staging per input, and exactly one is canonical.
    assert subject.CANONICAL_JSON_INPUTS == {"SOURCE_ASSERTION_PROFILE"}
    assert {
        name: item["staged_as"] for name, item in declared.items()
    } == {
        name: (
            subject.CANONICAL_JSON
            if name in subject.CANONICAL_JSON_INPUTS
            else subject.SOURCE_BYTES
        )
        for name in declared
    }
    # The source bytes and the staged bytes are stated separately, and they
    # differ for the profile and for nothing else.
    for name, item in declared.items():
        moved = item["sha256"] != item["source_sha256"]
        assert moved == (name in subject.CANONICAL_JSON_INPUTS), name

    receipt = subject.prepare(ROOT / declared["SELECTED_READING"]["source"], output)
    staged = (output / profile["target"]).read_bytes()
    source = subject._git_show(manifest["core"]["commit"], profile["source"])

    assert staged != source
    assert staged == subject._canonical(source)
    assert json.loads(staged) == json.loads(source)
    assert not staged.endswith(b"\n")
    assert staged == json.dumps(
        json.loads(source),
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    # The staged file's digest is the profile identity the manifest, the
    # contract and the pin all record, and it is not the file's own.
    assert _digest(staged) == profile["sha256"]
    assert _digest(source) == profile["source_sha256"]
    assert _digest(staged) == manifest["history_profile"]["profile_identity"]
    assert _digest(staged) == contract["history"]["profile_sha256"]
    assert _digest(source) == contract["history"]["profile_file_sha256"]
    assert contract["history"]["profile_staging"] == (
        "CANONICAL_JSON_THE_STAGED_FILES_DIGEST_IS_THE_IDENTITY"
    )
    assert {
        item["name"]: item["sha256"] for item in receipt["files"]
    }["SOURCE_ASSERTION_PROFILE"] == profile["sha256"]
    # Run-21 staged the file's bytes, and that is the whole of what moved
    # against its manifest.
    prior = {
        item["name"]: item["sha256"]
        for item in json.loads(
            (RUN_21 / "producer-input-manifest.json").read_bytes()
        )["declared_inputs"]
    }
    assert prior["SOURCE_ASSERTION_PROFILE"] == profile["source_sha256"]
    assert manifest["moved_since"]["moved"] == ["SOURCE_ASSERTION_PROFILE"]
    assert manifest["moved_since"]["moved_cause"] == {
        "SOURCE_ASSERTION_PROFILE": "STAGED_AS_CANONICAL_JSON_FROM_V4_12"
    }
    assert manifest["moved_since"]["reference_run"] == "run-21"
    assert sorted(manifest["moved_since"]["unchanged"]) == sorted(
        name for name in declared if name != "SOURCE_ASSERTION_PROFILE"
    )
    # Every other declared input is staged as the bytes the commit carries.
    for name, item in declared.items():
        if name in subject.CANONICAL_JSON_INPUTS or name == "SELECTED_READING":
            continue
        assert (output / item["target"]).read_bytes() == subject._git_show(
            manifest["core"]["commit"], item["source"]
        ), name


def test_producer_preparation_refuses_a_staging_the_manifest_does_not_declare(
    monkeypatch: pytest.MonkeyPatch, private_workspace: Path
) -> None:
    """The builder and the manifest have to agree on what is staged how.

    A manifest that stages another input canonical, or none, is a manifest this
    builder did not write, and staging bytes nobody declared is exactly the
    class of defect E-0203 turned up. The check is on the set, so both
    directions refuse.
    """

    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    reading = ROOT / "private/paper-v4-text-layer/selected-reading.json"

    for name, staging in (
        ("SOURCE_ASSERTION_PROFILE", subject.SOURCE_BYTES),
        ("RESEARCH_PACK", subject.CANONICAL_JSON),
    ):
        drifted = deepcopy(manifest)
        for item in drifted["declared_inputs"]:
            if item["name"] == name:
                item["staged_as"] = staging
        path = private_workspace / f"manifest-{name}.json"
        path.write_bytes(_canonical(drifted))
        monkeypatch.setattr(subject, "MANIFEST", path)
        with pytest.raises(subject.ProducerPreparationRefusal) as refusal:
            subject.prepare(reading, private_workspace / f"producer-{name}")
        assert "canonical JSON" in str(refusal.value), name

    # An unknown staging name is refused by the writer rather than guessed at.
    with pytest.raises(subject.ProducerPreparationRefusal) as refusal:
        subject.staged_bytes({"name": "X", "staged_as": "RAW"}, b"{}")
    assert "unknown staging" in str(refusal.value)


def test_producer_preparation_refuses_a_drifted_declared_input(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")

    with pytest.raises(subject.ProducerPreparationRefusal):
        subject.prepare(FIXTURE / "reading.json", private_workspace / "producer")


def test_producer_preparation_reads_every_tracked_input_from_the_commit(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    commit = manifest["core"]["commit"]
    seen: list[tuple[str, str]] = []
    real = subject._git_show

    def recording(requested: str, path: str) -> bytes:
        seen.append((requested, path))
        return real(requested, path)

    subject._git_show = recording
    receipt = subject.prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json",
        private_workspace / "producer",
    )

    tracked = [
        item["source"]
        for item in manifest["declared_inputs"]
        if item["name"] != "SELECTED_READING"
    ]
    assert sorted(seen) == sorted((commit, source) for source in tracked)
    assert len(tracked) == 7
    assert receipt["core"]["commit"] == commit


def test_the_installed_skill_is_the_bytes_at_the_commit_not_the_live_tree(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())
    output = private_workspace / "producer"

    subject.prepare(ROOT / "private/paper-v4-text-layer/selected-reading.json", output)

    skill = output / ".claude/skills/malleus-acolyte/SKILL.md"
    frozen = subprocess.run(
        ["git", "show", f"{manifest['core']['commit']}:{skill.relative_to(output)}"],
        capture_output=True,
        check=True,
        cwd=ROOT,
    ).stdout
    assert skill.read_bytes() == frozen
    assert _digest(frozen) == next(
        item["sha256"]
        for item in manifest["declared_inputs"]
        if item["name"] == "MALLEUS_NASCENT_PROJECT_SKILL"
    )
    assert "install-skills" not in (HERE / "prepare_producer.py").read_text(
        encoding="utf-8"
    )


def test_producer_preparation_refuses_an_input_absent_at_the_recorded_commit() -> None:
    subject = _module("prepare_producer")
    manifest = json.loads((HERE / "producer-input-manifest.json").read_bytes())

    with pytest.raises(subject.ProducerPreparationRefusal):
        subject._git_show(manifest["core"]["commit"], "ontology/no-such-pack.yaml")


def test_ontology_gate_returns_one_aggregate_grounding_diagnostic(
    private_workspace: Path,
) -> None:
    subject = _module("compile_ontology_candidate")
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    output = private_workspace / "gate-01"

    assert not subject.compile_candidate(
        ontology_path=FIXTURE / "inspection-note.yaml",
        producer_root=producer,
        output=output,
        attempt=1,
    )

    diagnostic = json.loads((output / "diagnostic.json").read_bytes())
    assert diagnostic["status"] == "REFUSED"
    assert diagnostic["stage"] == "PACK_GROUNDING"
    assert diagnostic["reason"] == "DIRECT_ROOT_GROUNDING_REQUIRED"
    assert diagnostic["detail"] == (
        "DIRECT_ROOT_GROUNDING_REQUIRED: project classes extend Malleus roots"
        " without grounding: Asset extends Entity; Inspection extends Entity;"
        " InspectionOfRelation extends Relation; VibrationReading extends Entity"
    )
    assert {path.name for path in output.iterdir()} == {"diagnostic.json"}


def test_ontology_gate_accepts_a_pack_derived_project(
    private_workspace: Path,
) -> None:
    subject = _module("compile_ontology_candidate")
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    ontology = private_workspace / "candidate.yaml"
    ontology.write_text(
        """id: https://example.org/gate-probe
name: gate_probe
imports: [linkml:types, malleus, research]
classes:
  ProbeObservation:
    is_a: Observation
""",
        encoding="utf-8",
    )
    output = private_workspace / "gate-02"

    assert subject.compile_candidate(
        ontology_path=ontology,
        producer_root=producer,
        output=output,
        attempt=2,
    )

    diagnostic = json.loads((output / "diagnostic.json").read_bytes())
    surface = json.loads((output / "population-surface.json").read_bytes())
    assert diagnostic["status"] == "ACCEPTED"
    assert diagnostic["stage"] == "COMPLETE"
    assert surface["schema"] == "malleus.paper-v4.population-surface/v2"
    assert surface["families_admitted"] == ["entities", "events", "relations"]
    assert any(
        item["name"] == "ProbeObservation" and item["family"] == "ENTITY"
        for item in surface["record_types"]
    )
    assert {path.name for path in output.iterdir()} == {
        "diagnostic.json",
        "grounding-receipt.json",
        "population-surface.json",
        "validated-contract.json",
    }


def test_an_event_type_reaches_the_surface_and_one_event_record_is_admitted(
    private_workspace: Path,
) -> None:
    """The run-02 defect, closed at both ends.

    Run-02's surface listed no Event type although the bound profile admits
    events and the accepted ontology declared one, so the producer wrote typed
    gaps instead of Event records (E-0122 finding 3). Here the surface lists the
    Event subclass under family EVENT, and a capture whose ``records`` carry an
    ``events`` envelope with a full derivation admits, replays and exports it.
    """
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    ontology = _event_ontology(private_workspace)
    gate = private_workspace / "gate-event"

    assert _module("compile_ontology_candidate").compile_candidate(
        ontology_path=ontology,
        producer_root=producer,
        output=gate,
        attempt=1,
    )

    surface = json.loads((gate / "population-surface.json").read_bytes())
    families = {item["name"]: item["family"] for item in surface["record_types"]}
    assert surface["schema"] == "malleus.paper-v4.population-surface/v2"
    assert surface["families_admitted"] == ["entities", "events", "relations"]
    assert families[EVENT_TYPE] == "EVENT"
    assert families["Event"] == "EVENT"
    assert families["Asset"] == "ENTITY"
    assert families["InspectionOfRelation"] == "RELATION"
    assert "EVENT_PARTICIPATION" not in set(families.values())
    event_type = next(
        item for item in surface["record_types"] if item["name"] == EVENT_TYPE
    )
    assert "event_type" in {slot["name"] for slot in event_type["slots"]}

    results = private_workspace / "event-results"
    completed = _run(
        "run",
        [
            *_source_arguments(ontology),
            "--reading",
            str(FIXTURE / "reading.json"),
            "--population",
            str(_event_population_file(private_workspace)),
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            PLAN_ID,
            "--source-id",
            SOURCE_ID,
            "--artifact-id",
            ARTIFACT_ID,
            "--ledger",
            str(private_workspace / "event-history.jsonl"),
            "--results",
            str(results),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    assert completed.returncode == 0, completed.stderr

    result = json.loads((results / "run-result.json").read_bytes())
    export = json.loads((results / "export-records.json").read_bytes())
    summary = json.loads((results / "trace-summary.json").read_bytes())
    traces = {item["record_id"]: item for item in summary["records"]}

    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["reopen_matches_admitted"] == {
        "receipt": True,
        "export_records": True,
    }
    assert result["graph"]["events"] == 1
    assert result["graph"]["entities"] == 2
    assert result["graph"]["relations"] == 1
    assert result["graph"]["event_participations"] == 0
    assert result["records_traced"] == 4
    assert export["events"] == [
        {
            "id": EVENT_RECORD_ID,
            "properties": {"event_type": "INSPECTION"},
            "type": EVENT_TYPE,
        }
    ]
    assert traces[EVENT_RECORD_ID]["record_type"] == EVENT_TYPE
    assert [item["path"] for item in traces[EVENT_RECORD_ID]["derivations"]] == [
        ["properties", "event_type"]
    ]


def test_run_admits_replays_and_reproduces_the_same_receipt(
    private_workspace: Path,
) -> None:
    results, result = _executed(private_workspace)

    assert result["schema"] == "malleus.paper-v4.run-22-result/v1"
    assert result["run_id"] == "run-22"
    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["reopen_matches_admitted"] == {
        "receipt": True,
        "export_records": True,
    }
    assert result["replay_receipt_sha256"] == _digest(
        (results / "replay-receipt.json").read_bytes()
    )
    assert result["capture"]["capture_id"] == CAPTURE_ID
    assert result["capture"]["capture_sha256"] == _digest(
        (FIXTURE / "document-capture.json").read_bytes()
    )
    assert result["reading_sha256"] == _digest((FIXTURE / "reading.json").read_bytes())
    assert result["plan"]["plan_id"] == PLAN_ID
    assert result["plan"]["status"] == "CHANGE_SET"
    assert result["graph"]["entities"] == 2
    assert result["graph"]["relations"] == 1
    assert result["graph"]["events"] == 0
    assert result["gaps_by_kind"] == {
        "INTERVAL_NOT_EXPRESSIBLE": 1,
        "MODALITY_NOT_EXPRESSIBLE": 1,
        "TYPE_ABSENT": 1,
    }
    assert sorted(path.name for path in results.iterdir()) == [
        "census.json",
        "export-records.json",
        "gaps.json",
        "paper-events.json",
        "population-plan.json",
        "replay-receipt.json",
        "run-result.json",
        "trace-summary.json",
    ]


def test_run_records_exactly_one_paper_owned_stage_acceptance(
    private_workspace: Path,
) -> None:
    results, result = _executed(private_workspace)
    events = json.loads((results / "paper-events.json").read_bytes())

    assert [event["event"] for event in events["events"]] == [
        "ONTOLOGY_ACCEPTED_FOR_POPULATION"
    ]
    event = events["events"][0]
    assert event["ontology_sha256"] == _digest(
        (FIXTURE / "inspection-note.yaml").read_bytes()
    )
    assert event["non_claim"] == "STAGE_ACCEPTANCE_NOT_DOMAIN_ADEQUACY"
    assert event["actor_id"] == ACTOR
    assert event["transaction_time"] == TRANSACTION_TIME
    assert event["ontology_sha256"] == result["ontology_sha256"]


def test_run_traces_every_admitted_record_to_retained_inputs(
    private_workspace: Path,
) -> None:
    results, _ = _executed(private_workspace)
    summary = json.loads((results / "trace-summary.json").read_bytes())
    traces = {item["record_id"]: item for item in summary["records"]}

    assert set(traces) == {
        "asset:P-7",
        "inspection:P-7:2026-03-02",
        "inspection-of:P-7:2026-03-02",
    }
    for trace in traces.values():
        assert trace["plan_id"] == PLAN_ID
        assert trace["history_profile"]["profile_id"] == "source-assertion"
        assert isinstance(trace["evidence"], dict)
        assert trace["evidence"][CAPTURE_ID] == _digest(
            (FIXTURE / "document-capture.json").read_bytes()
        )
        assert trace["sources"][SOURCE_ID] == _digest(
            (FIXTURE / "reading.json").read_bytes()
        )
    assert "statement" not in json.dumps(summary)


def test_native_query_reads_only_the_replayed_graph(
    private_workspace: Path,
) -> None:
    _executed(private_workspace)
    binding = _binding_file(private_workspace)
    query_results = private_workspace / "query"

    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "history.jsonl"),
            "--binding",
            str(binding),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr

    result = json.loads((query_results / "query-result.json").read_bytes())
    assert result["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert result["inputs"]["query_binding_sha256"] == _digest(binding.read_bytes())
    rows = result["queries"][0]["rows"]
    assert len(rows) == 1
    assert rows[0]["source"] == {"inspected_on": "2026-03-02"}
    assert rows[0]["target"] == {"name": "P-7"}
    assert rows[0]["relation"] == {"relation_type": "INSPECTION_OF"}
    assert rows[0]["witness"] == {
        "relation_id": "inspection-of:P-7:2026-03-02",
        "source_id": "inspection:P-7:2026-03-02",
        "target_id": "asset:P-7",
    }


def test_native_query_traces_every_witness_and_selects_evidence_by_id(
    private_workspace: Path,
) -> None:
    _executed(private_workspace)
    query_results = private_workspace / "query"
    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "history.jsonl"),
            "--binding",
            str(_binding_file(private_workspace)),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr

    summary = json.loads((query_results / "trace-summary.json").read_bytes())
    traced = {item["record_id"]: item for item in summary["records"]}

    assert set(traced) == {
        "asset:P-7",
        "inspection:P-7:2026-03-02",
        "inspection-of:P-7:2026-03-02",
    }
    assert summary["witnesses_traced"] == 3
    assert summary["evidence_selection"] == "BY_RECORD_ID_NEVER_BY_POSITION"
    for trace in traced.values():
        assert trace["declared_evidence_resolved"] is True
        assert trace["evidence"][CAPTURE_ID] == _digest(
            (FIXTURE / "document-capture.json").read_bytes()
        )


def test_the_source_free_guard_refuses_and_counts_a_file_read() -> None:
    subject = _module("native_query")
    guard = subject._SourceFreeGuard()

    with pytest.raises(subject.NativeQueryRefusal):
        with guard:
            open(FIXTURE / "reading.json", "rb")

    assert guard.attempts == {"embedding_import": 0, "file_read": 1, "network": 0}


def test_native_query_refuses_a_binding_naming_an_absent_type(
    private_workspace: Path,
) -> None:
    _executed(private_workspace)
    binding = private_workspace / "bad-binding.json"
    binding.write_bytes(
        _canonical(
            {
                "schema": "malleus.paper-v4.native-query-binding/v5",
                "status": "FROZEN_AFTER_REPLAY",
                "queries": [
                    {
                        "id": "NQ-FIXTURE-02",
                        "question_id": "FIXTURE-02",
                        "cases": [
                            {
                                "kind": "RELATION",
                                "ordinal": 1,
                                "source_record_type": "Inspection",
                                "relation_record_type": "AbsentRelation",
                                "target_record_type": "Asset",
                                "output_fields": {
                                    "source": [],
                                    "relation": [],
                                    "target": [],
                                },
                            }
                        ],
                    }
                ],
            }
        )
    )

    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "history.jsonl"),
            "--binding",
            str(binding),
            "--results",
            str(private_workspace / "query-refused"),
        ],
    )

    assert completed.returncode == 2
    assert "AbsentRelation" in completed.stderr
    assert not (private_workspace / "query-refused").exists()


# ---------------------------------------------------------------------------
# The carried v4.2 and v4.3 deltas, exercised rather than asserted.
# ---------------------------------------------------------------------------


LAUNCH_LOG = {
    "schema": "malleus.paper-v4.producer-launch-log/v2",
    "run": "run-22",
    "protocol": "v4.9",
    "launches": [
        {
            "ordinal": 1,
            "role": "PRODUCER",
            "phase": "ONTOLOGY",
            "first_stage": "ONTOLOGY_ATTEMPT_01",
            "harness": "Claude Code Agent tool, subagent_type general-purpose",
            "requested_model": "opus",
            "model_family": "Claude Opus 5",
            "model_id": "claude-opus-5",
            "usage_cumulative": {
                "tokens": 185877,
                "tool_uses": 17,
                "duration_ms": 1007660,
            },
            "usage_by_resume": [
                {
                    "after": "ONTOLOGY_ATTEMPT_02",
                    "tokens": 203752,
                    "tool_uses": 23,
                    "duration_ms": 1194022,
                },
                {
                    "after": "POPULATION",
                    "tokens": 371026,
                    "tool_uses": 72,
                    "duration_ms": 2696310,
                },
            ],
        }
    ],
    "gate": [{"attempt": 1, "status": "ACCEPTED"}],
    "runner": [
        {
            "attempt": 1,
            "status": "ADMITTED_AND_REPLAYED",
            "execution_commit": "0000000",
            "structural_diagnostic_returns_used": 0,
        }
    ],
    "query": {"rows_by_question": {}},
    "review": {"model_id": "claude-opus-5", "tokens": 322049},
}


def _gate_contract(surface: Path) -> Path:
    """The validated contract the gate wrote beside the surface it accepted.

    v4.12's binder reads it: the surface carries no ancestry and the closure
    check needs the contract's ``rdfs:subClassOf`` facts.
    """

    return surface.parent / "validated-contract.json"


def _gate_surface(workspace: Path) -> Path:
    """Compile the fixture-plus-Event ontology and return its accepted surface."""

    producer = workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    gate = workspace / "gate-binding"
    assert _module("compile_ontology_candidate").compile_candidate(
        ontology_path=_event_ontology(workspace),
        producer_root=producer,
        output=gate,
        attempt=1,
    )
    return gate / "population-surface.json"


def _subject_gate_surface(workspace: Path) -> Path:
    """Compile the fixture-plus-subject ontology and return its accepted surface."""

    producer = workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    gate = workspace / "gate-subject"
    assert _module("compile_ontology_candidate").compile_candidate(
        ontology_path=_subject_ontology(workspace),
        producer_root=producer,
        output=gate,
        attempt=1,
    )
    return gate / "population-surface.json"


def _type_set_file(directory: Path, type_sets: dict[str, list[str]]) -> Path:
    path = directory / "query-type-sets.json"
    path.write_bytes(_canonical(type_sets))
    return path


def test_the_gate_records_every_link_of_a_chained_cause(
    private_workspace: Path,
) -> None:
    """Run-05's attempt 01, with the cause in the file instead of beside it."""

    subject = _module("compile_ontology_candidate")
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    ontology = private_workspace / "rejected-field.yaml"
    ontology.write_text(
        """id: https://example.org/gate-probe
name: gate_probe
comments: [a note the source boundary rejects]
imports: [linkml:types, malleus, research]
classes:
  ProbeObservation:
    is_a: Observation
""",
        encoding="utf-8",
    )
    output = private_workspace / "gate-chained"

    assert not subject.compile_candidate(
        ontology_path=ontology,
        producer_root=producer,
        output=output,
        attempt=1,
    )

    diagnostic = json.loads((output / "diagnostic.json").read_bytes())
    chain = diagnostic["cause_chain"]

    assert diagnostic["status"] == "REFUSED"
    assert diagnostic["reason"] == "IMPORT_READER_REFUSED"
    assert diagnostic["detail"] == "IMPORT_READER_REFUSED"
    assert len(chain) >= 2
    assert chain[0]["reason"] == diagnostic["reason"]
    assert chain[0]["detail"] == diagnostic["detail"]
    assert "rejected field 'comments'" in json.dumps(chain[1:])
    assert "rejected field 'comments'" in diagnostic["chained_cause"]
    assert all(set(link) == {"detail", "error_type", "reason"} for link in chain)


def test_an_unchained_refusal_records_one_link_and_no_chained_cause(
    private_workspace: Path,
) -> None:
    subject = _module("compile_ontology_candidate")
    producer = private_workspace / "producer"
    _module("prepare_producer").prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json", producer
    )
    output = private_workspace / "gate-unchained"

    assert not subject.compile_candidate(
        ontology_path=FIXTURE / "inspection-note.yaml",
        producer_root=producer,
        output=output,
        attempt=1,
    )

    diagnostic = json.loads((output / "diagnostic.json").read_bytes())

    assert diagnostic["reason"] == "DIRECT_ROOT_GROUNDING_REQUIRED"
    assert len(diagnostic["cause_chain"]) == 1
    assert diagnostic["chained_cause"] is None


def test_the_preflight_records_the_interpreter_and_the_locked_versions(
    private_workspace: Path,
) -> None:
    subject = _module("prepare_producer")

    receipt = subject.prepare(
        ROOT / "private/paper-v4-text-layer/selected-reading.json",
        private_workspace / "producer",
    )
    interpreter = receipt["interpreter"]

    assert interpreter["status"] == "VERIFIED"
    assert interpreter["checked"] == "INTERPRETER_AND_LOCKED_COMPILER_VERSIONS"
    assert interpreter["prefix"] == interpreter["required_prefix"]
    assert interpreter["prefix"] == str((ROOT / ".venv").resolve())
    assert interpreter["locked_versions"] == interpreter["installed_versions"]
    assert set(interpreter["locked_versions"]) == {"linkml", "linkml-runtime"}
    assert interpreter["environment_lock_sha256"] == _digest(
        (ROOT / interpreter["environment_lock"]).read_bytes()
    )


def test_the_preflight_refuses_an_interpreter_that_is_not_the_repository_venv(
    monkeypatch: pytest.MonkeyPatch, private_workspace: Path
) -> None:
    subject = _module("prepare_producer")
    monkeypatch.setattr(subject.sys, "prefix", "/usr")

    with pytest.raises(subject.ProducerPreparationRefusal, match="interpreter is"):
        subject.prepare(
            ROOT / "private/paper-v4-text-layer/selected-reading.json",
            private_workspace / "producer",
        )

    assert not (private_workspace / "producer").exists()


def test_the_preflight_refuses_a_version_the_environment_lock_does_not_name(
    monkeypatch: pytest.MonkeyPatch, private_workspace: Path
) -> None:
    subject = _module("prepare_producer")
    monkeypatch.setattr(subject.metadata, "version", lambda name: "1.10.0")

    with pytest.raises(subject.ProducerPreparationRefusal, match="1.10.0"):
        subject.prepare(
            ROOT / "private/paper-v4-text-layer/selected-reading.json",
            private_workspace / "producer",
        )

    assert not (private_workspace / "producer").exists()


def test_the_binding_is_the_exhaustive_expansion_of_the_surface(
    private_workspace: Path,
) -> None:
    """One ENTITY case per type, the RELATION cross product, no SUBJECT case.

    This surface carries no subject reference, so no type is restricted, the
    SUBJECT kind expands to nothing and says so rather than being absent, and
    v4.12's ENTITY_NO_SUBJECT kind expands to nothing for the same reason: it
    is emitted for the subject-bearing types of a set and this set has none.
    The expansion is v4.3's for this surface.
    """

    subject = _module("bind_from_surface")
    surface_path = _gate_surface(private_workspace)
    surface = json.loads(surface_path.read_bytes())
    relations = sorted(
        item["name"] for item in surface["record_types"] if item["family"] == "RELATION"
    )
    types = ["Asset", "Inspection"]
    output = private_workspace / "binding-acceptance.json"

    subject.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(_type_set_file(private_workspace, {"CQ-01": types})),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(output),
        ]
    )

    binding = json.loads(output.read_bytes())
    query = binding["queries"][0]
    kinds = Counter(case["kind"] for case in query["cases"])
    asset = next(
        item for item in surface["record_types"] if item["name"] == "Asset"
    )
    expected_projection = [
        slot["name"]
        for slot in asset["slots"]
        if slot["qualified_name"] not in subject.HOUSEKEEPING_SLOTS
    ]

    assert binding["schema"] == "malleus.paper-v4.native-query-binding/v5"
    assert binding["bound_at_stage"] == "ONTOLOGY_ACCEPTANCE"
    assert binding["bound_after_replay_receipt_sha256"] == "PENDING"
    assert binding["population_surface_sha256"] == _digest(surface_path.read_bytes())
    assert binding["type_sets"] == {"CQ-01": types}
    assert binding["expansion"]["case_kinds"] == [
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
    ]
    assert binding["expansion"]["subject_bearing_record_types"] == []
    assert binding["expansion"]["closure_checked"] == subject.CLOSURE_CHECK
    assert binding["expansion"]["subject_slot"] == SUBJECT_SLOT
    assert binding["expansion"]["entity_case_scope"] == (
        "TYPES_IN_THE_SET_THAT_CARRY_NO_SUBJECT"
    )
    assert binding["expansion"]["entity_no_subject_case_scope"] == (
        "TYPES_IN_THE_SET_THAT_CARRY_SUBJECT_RESTRICTED_TO_RECORDS"
        "_WHOSE_SUBJECT_SLOT_IS_ABSENT"
    )
    assert ENTITY_NO_SUBJECT not in kinds
    assert query["id"] == "NQ-CQ-01"
    assert query["question_id"] == "CQ-01"
    assert kinds == Counter(
        {"ENTITY": len(types), "RELATION": len(types) * len(types) * len(relations)}
    )
    assert len(query["cases"]) == len(types) + len(types) * len(types) * len(relations)
    assert [case["ordinal"] for case in query["cases"]] == list(
        range(1, len(query["cases"]) + 1)
    )
    relation_cases = [case for case in query["cases"] if case["kind"] == "RELATION"]
    entity_cases = [case for case in query["cases"] if case["kind"] == "ENTITY"]
    assert {case["relation_record_type"] for case in relation_cases} == set(relations)
    assert [case["record_type"] for case in entity_cases] == types
    assert expected_projection
    assert "id" not in expected_projection
    for case in entity_cases:
        if case["record_type"] == "Asset":
            assert case["output_fields"]["record"] == expected_projection
    for case in relation_cases:
        if case["source_record_type"] == "Asset":
            assert case["output_fields"]["source"] == expected_projection
        assert not set(case["output_fields"]["relation"]) & {
            "id",
            "source_id",
            "target_id",
        }

    # The binding the query executes is the binding the launch log pinned.
    _module("native_query").load_binding(output.read_bytes())


def test_a_subject_bearing_surface_gets_no_entity_case_for_the_bearing_type(
    private_workspace: Path,
) -> None:
    """The carried v4.4 restriction and v4.12's addition beside it.

    ``Inspection`` bears ``subject`` and ``Asset`` does not, so the expansion
    emits one plain ENTITY case for ``Asset`` and none for ``Inspection``, and
    reaches an attached ``Inspection`` through its SUBJECT cases. What v4.12
    adds is one ENTITY_NO_SUBJECT case for ``Inspection`` and for no other
    type: the restriction stands for every record it was written for, and the
    records it left unreachable are reached by the new kind alone.
    """

    binder = _module("bind_from_surface")
    surface_path = _subject_gate_surface(private_workspace)
    surface = json.loads(surface_path.read_bytes())
    relations = sorted(
        item["name"] for item in surface["record_types"] if item["family"] == "RELATION"
    )
    types = ["Asset", "Inspection"]
    output = private_workspace / "binding-subject.json"

    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(_type_set_file(private_workspace, {"CQ-01": types})),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(output),
        ]
    )

    binding = json.loads(output.read_bytes())
    query = binding["queries"][0]
    kinds = Counter(case["kind"] for case in query["cases"])
    subject_cases = [case for case in query["cases"] if case["kind"] == "SUBJECT"]
    entity_cases = [case for case in query["cases"] if case["kind"] == "ENTITY"]
    inspection = next(
        item for item in surface["record_types"] if item["name"] == "Inspection"
    )
    bearing = ["Inspection"]
    unattached = ["Asset"]

    assert SUBJECT_SLOT in {slot["name"] for slot in inspection["slots"]}
    assert binding["expansion"]["subject_bearing_record_types"] == bearing
    assert binding["expansion"]["entity_case_scope"] == (
        "TYPES_IN_THE_SET_THAT_CARRY_NO_SUBJECT"
    )
    assert [case["record_type"] for case in entity_cases] == unattached
    assert "Inspection" not in {case["record_type"] for case in entity_cases}
    assert kinds == Counter(
        {
            "ENTITY": len(unattached),
            ENTITY_NO_SUBJECT: len(bearing),
            "RELATION": len(types) * len(types) * len(relations),
            "SUBJECT": len(types),
        }
    )
    # v4.12's kind is emitted for the bearing types and for nothing else, and
    # it is emitted directly after the ENTITY cases, so the ordinals keep the
    # two entity kinds first.
    no_subject_cases = [
        case for case in query["cases"] if case["kind"] == ENTITY_NO_SUBJECT
    ]
    assert [case["record_type"] for case in no_subject_cases] == bearing
    assert [case["ordinal"] for case in no_subject_cases] == [2]
    for case in no_subject_cases:
        assert set(case["output_fields"]) == {"record"}
        assert set(case) == {"kind", "ordinal", "output_fields", "record_type"}
        # The projection is the type's own, the same list its SUBJECT case
        # projects for the same type: the kind selects, it does not project.
        assert case["output_fields"]["record"] == (
            subject_cases[0]["output_fields"]["record"]
        )
    # The declared count rule, recomputed here rather than restated.
    assert len(query["cases"]) == (
        len(unattached)
        + len(bearing)
        + len(types) * len(types) * len(relations)
        + len(bearing) * len(types)
    )
    assert [
        (case["record_type"], case["subject_record_type"]) for case in subject_cases
    ] == [("Inspection", "Asset"), ("Inspection", "Inspection")]
    for case in subject_cases:
        assert SUBJECT_SLOT in case["output_fields"]["record"]
        assert set(case["output_fields"]) == {"record", "subject"}
    assert [case["ordinal"] for case in query["cases"]] == list(
        range(1, len(query["cases"]) + 1)
    )
    _module("native_query").load_binding(output.read_bytes())

    # Against run-21's binder on the same surface: exactly one case more, and
    # every case run-21 emitted still emitted, in the same order and with the
    # same types. The digest moves because a case was added and for no other
    # reason, which is what a schema step is for.
    run_21 = _run_21_binder()
    prior_binding = run_21.build(
        surface_source=surface_path.read_bytes(),
        type_sets={"CQ-01": types},
        replay_receipt="PENDING",
    )
    prior = prior_binding["queries"][0]["cases"]
    assert len(query["cases"]) == len(prior) + len(bearing)
    assert _identities(prior) < _identities(query["cases"])
    assert _identities(query["cases"]) - _identities(prior) == {
        (ENTITY_NO_SUBJECT, "Inspection")
    }
    # Case for case, ignoring the ordinals the insertion shifts.
    assert [
        {name: value for name, value in case.items() if name != "ordinal"}
        for case in query["cases"]
        if case["kind"] != ENTITY_NO_SUBJECT
    ] == [
        {name: value for name, value in case.items() if name != "ordinal"}
        for case in prior
    ]
    assert binding["cases_sha256"] != prior_binding["cases_sha256"]
    assert prior_binding["schema"] == BINDING_SCHEMA_V4
    assert binding["schema"] == BINDING_SCHEMA_V5

    # And against run-09's, the cell before the restriction: the same type is
    # reached, and it is reached by a case that selects on the absent slot
    # instead of by one that returns every record of the type.
    before = _run_09_binder().build(
        surface_source=surface_path.read_bytes(),
        type_sets={"CQ-01": types},
        replay_receipt="PENDING",
    )["queries"][0]["cases"]
    assert Counter(case["kind"] for case in before) == Counter(
        {
            "ENTITY": len(types),
            "RELATION": len(types) * len(types) * len(relations),
            "SUBJECT": len(types),
        }
    )
    assert ("ENTITY", "Inspection") in _identities(before)
    assert ("ENTITY", "Inspection") not in _identities(query["cases"])
    assert (ENTITY_NO_SUBJECT, "Inspection") not in _identities(before)


def test_all_four_case_kinds_execute_against_the_replayed_graph(
    private_workspace: Path,
) -> None:
    """The carried change and v4.12's, end to end, on one replayed graph.

    Run-08's binding could return the RELATION row and nothing else. Run-09
    returned both records as ENTITY rows and the subject link as a SUBJECT row,
    so the inspection came back twice. Under the v4.4 restriction the attached
    inspection arrives only through its subject and the asset still arrives as
    an ENTITY row because it bears no subject. What that restriction left
    unreachable is the second inspection, which names no subject: v4.12's fourth
    case kind returns it, once, as an ENTITY row of its own type. Every row is
    witnessed and traced and the row kinds are still three.
    """

    binder = _module("bind_from_surface")
    surface_path = _subject_gate_surface(private_workspace)
    ontology = private_workspace / "inspection-note-with-subject.yaml"
    results = private_workspace / "subject-results"
    completed = _run(
        "run",
        [
            *_source_arguments(ontology),
            "--reading",
            str(FIXTURE / "reading.json"),
            "--population",
            str(_subject_population_file(private_workspace)),
            "--capture-id",
            CAPTURE_ID,
            "--plan-id",
            PLAN_ID,
            "--source-id",
            SOURCE_ID,
            "--artifact-id",
            ARTIFACT_ID,
            "--ledger",
            str(private_workspace / "subject-history.jsonl"),
            "--results",
            str(results),
            "--transaction-time",
            TRANSACTION_TIME,
            "--actor-id",
            ACTOR,
        ],
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads((results / "run-result.json").read_bytes())

    binding = private_workspace / "binding-executed.json"
    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(_type_set_file(private_workspace, {"CQ-01": ["Asset", "Inspection"]})),
            "--replay-receipt",
            result["replay_receipt_sha256"],
            "--output",
            str(binding),
        ]
    )
    query_results = private_workspace / "subject-query"
    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "subject-history.jsonl"),
            "--binding",
            str(binding),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr

    query_result = json.loads((query_results / "query-result.json").read_bytes())
    summary = json.loads((query_results / "trace-summary.json").read_bytes())
    rows = query_result["queries"][0]["rows"]
    by_kind: dict[str, list[dict]] = {}
    for row in rows:
        by_kind.setdefault(row["kind"], []).append(row)

    assert query_result["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    # Four case kinds and three row kinds: the fourth kind writes ENTITY rows.
    assert sorted(by_kind) == ["ENTITY", "RELATION", "SUBJECT"]
    binding_cases = [
        case
        for query in json.loads(binding.read_bytes())["queries"]
        for case in query["cases"]
    ]
    assert sorted({case["kind"] for case in binding_cases}) == [
        "ENTITY",
        ENTITY_NO_SUBJECT,
        "RELATION",
        "SUBJECT",
    ]
    # The asset through its own ENTITY case, ordinal 1, and the subject-less
    # inspection through the ENTITY_NO_SUBJECT case, ordinal 2. The attached
    # inspection is in neither: the v4.4 restriction still holds for it.
    assert [row["witness"]["record_id"] for row in by_kind["ENTITY"]] == [
        SUBJECT_TARGET_ID,
        UNATTACHED_RECORD_ID,
    ]
    assert SUBJECT_RECORD_ID not in {
        row["witness"]["record_id"] for row in by_kind["ENTITY"]
    }
    unattached_row = by_kind["ENTITY"][1]
    assert unattached_row["case_ordinals"] == [
        next(
            case["ordinal"]
            for case in binding_cases
            if case["kind"] == ENTITY_NO_SUBJECT
        )
    ]
    # Projected by its own type, and the absent slot is simply not there.
    assert unattached_row["record"] == {"inspected_on": UNATTACHED_INSPECTED_ON}
    assert SUBJECT_SLOT not in unattached_row["record"]
    assert len(by_kind["RELATION"]) == 1
    assert by_kind["RELATION"][0]["witness"] == {
        "relation_id": "inspection-of:P-7:2026-03-02",
        "source_id": SUBJECT_RECORD_ID,
        "target_id": SUBJECT_TARGET_ID,
    }
    assert len(by_kind["SUBJECT"]) == 1
    subject_row = by_kind["SUBJECT"][0]
    assert subject_row["witness"] == {
        "record_id": SUBJECT_RECORD_ID,
        "subject_id": SUBJECT_TARGET_ID,
    }
    assert subject_row["record"][SUBJECT_SLOT] == SUBJECT_TARGET_ID
    # The carried v4.7 delta, end to end: the binder called ``tags`` housekeeping and
    # named only ``name`` for the subject side, and the executor projected the
    # subject's tags beside it because the record carries them.
    assert subject_row["subject"] == {
        "name": "P-7",
        SUBJECT_TAGS_SLOT: list(SUBJECT_TARGET_TAGS),
    }
    subject_case = next(
        case
        for query in json.loads(binding.read_bytes())["queries"]
        for case in query["cases"]
        if case["kind"] == "SUBJECT"
    )
    assert subject_case["output_fields"]["subject"] == ["description", "name"]
    assert SUBJECT_TAGS_SLOT not in subject_case["output_fields"]["subject"]
    # The record side never gains the field, and the ENTITY row of the same
    # entity is what run-21 returned.
    assert SUBJECT_TAGS_SLOT not in subject_row["record"]
    assert by_kind["ENTITY"][0]["record"] == {"name": "P-7"}
    # v4.9, end to end on the fixture: the rows of a question are ordered by the
    # first case that produced them, no witness appears twice, and every key a
    # row projects is a slot the witness record's own type declares on the
    # accepted surface. The surface is the file the binder read, so this reads
    # the projection against its source rather than against the case.
    assert [row["case_ordinals"][0] for row in rows] == sorted(
        row["case_ordinals"][0] for row in rows
    )
    for row in rows:
        assert row["case_ordinals"] == sorted(row["case_ordinals"])
        assert row["case_ordinals"]
        assert "case_ordinal" not in row
    seen = [(row["kind"], _canonical(row["witness"])) for row in rows]
    assert len(seen) == len(set(seen))
    surface_slots = {
        str(record_type["name"]): {
            str(slot["name"]) for slot in record_type["slots"]
        }
        for record_type in json.loads(surface_path.read_bytes())["record_types"]
    }
    population = json.loads(
        (private_workspace / "document-population-with-subject.json").read_bytes()
    )
    own_type = {
        item["id"]: item["type"]
        for group in population["records"].values()
        for item in group
    }
    assert own_type[SUBJECT_RECORD_ID] == "Inspection"
    assert own_type[UNATTACHED_RECORD_ID] == "Inspection"
    assert own_type[SUBJECT_TARGET_ID] == "Asset"
    for row in rows:
        if row["kind"] == "ENTITY":
            sides = [(row["record"], own_type[row["witness"]["record_id"]])]
        elif row["kind"] == "SUBJECT":
            sides = [
                (row["record"], own_type[row["witness"]["record_id"]]),
                (row["subject"], own_type[row["witness"]["subject_id"]]),
            ]
        else:
            sides = [
                (row["source"], own_type[row["witness"]["source_id"]]),
                (row["target"], own_type[row["witness"]["target_id"]]),
                (row["relation"], own_type[row["witness"]["relation_id"]]),
            ]
        for projected, type_name in sides:
            assert set(projected) <= surface_slots[type_name] | {
                SUBJECT_TAGS_SLOT
            }, (row["kind"], type_name)

    # Every witness of every kind resolves to a retained input, by record id.
    traced = {item["record_id"] for item in summary["records"]}
    assert traced == {
        SUBJECT_RECORD_ID,
        SUBJECT_TARGET_ID,
        UNATTACHED_RECORD_ID,
        "inspection-of:P-7:2026-03-02",
    }
    assert summary["evidence_selection"] == "BY_RECORD_ID_NEVER_BY_POSITION"


def test_the_binding_refuses_a_case_of_an_unknown_kind_or_open_fields() -> None:
    subject = _module("native_query")
    case = {
        "kind": "ENTITY",
        "ordinal": 1,
        "record_type": "Asset",
        "output_fields": {"record": ["name"]},
    }

    def binding(mutated: dict[str, object]) -> bytes:
        return _canonical(
            {
                "schema": "malleus.paper-v4.native-query-binding/v5",
                "queries": [
                    {"id": "NQ-X", "question_id": "X", "cases": [mutated]}
                ],
            }
        )

    assert subject.load_binding(binding(dict(case)))
    for mutate, expected in (
        (lambda item: item.__setitem__("kind", "SUMMARY"), "kind is unknown"),
        (lambda item: item.__setitem__("relation_record_type", "R"), "not closed"),
        (
            lambda item: item.__setitem__("output_fields", {"source": []}),
            "output_fields must name",
        ),
    ):
        mutated = dict(case)
        mutate(mutated)
        with pytest.raises(subject.NativeQueryRefusal, match=expected):
            subject.load_binding(binding(mutated))


def test_only_the_receipt_field_moves_between_acceptance_and_query(
    private_workspace: Path,
) -> None:
    subject = _module("bind_from_surface")
    surface_path = _gate_surface(private_workspace)
    type_sets = _type_set_file(private_workspace, {"CQ-01": ["Asset", "Inspection"]})
    at_acceptance = private_workspace / "binding-acceptance.json"
    after_replay = private_workspace / "binding-query.json"
    receipt = "sha256:" + "0" * 64

    for output, value in ((at_acceptance, "PENDING"), (after_replay, receipt)):
        subject.main(
            [
                "--surface",
                str(surface_path),
                "--contract",
                str(_gate_contract(surface_path)),
                "--type-sets",
                str(type_sets),
                "--replay-receipt",
                value,
                "--output",
                str(output),
            ]
        )

    first = json.loads(at_acceptance.read_bytes())
    second = json.loads(after_replay.read_bytes())

    assert first["cases_sha256"] == second["cases_sha256"]
    assert first["queries"] == second["queries"]
    assert {
        key for key in first if first[key] != second.get(key)
    } == {"bound_after_replay_receipt_sha256"}
    assert second["bound_after_replay_receipt_sha256"] == receipt


def test_the_binding_refuses_a_type_the_surface_does_not_carry(
    private_workspace: Path,
) -> None:
    subject = _module("bind_from_surface")
    surface_path = _gate_surface(private_workspace)

    with pytest.raises(subject.BindingRefusal, match="AbsentType"):
        subject.build(
            surface_source=surface_path.read_bytes(),
            type_sets={"CQ-01": ["Asset", "AbsentType"]},
            replay_receipt="PENDING",
            contract_source=_gate_contract(surface_path).read_bytes(),
        )


def test_the_binding_frozen_at_acceptance_executes_after_the_replay(
    private_workspace: Path,
) -> None:
    """The whole point of the change: bound before rows, run after them."""

    binder = _module("bind_from_surface")
    surface_path = _gate_surface(private_workspace)
    type_sets = _type_set_file(private_workspace, {"CQ-01": ["Asset", "Inspection"]})
    at_acceptance = private_workspace / "binding-acceptance.json"
    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(type_sets),
            "--replay-receipt",
            "PENDING",
            "--output",
            str(at_acceptance),
        ]
    )
    frozen_cases = json.loads(at_acceptance.read_bytes())["cases_sha256"]

    results, result = _executed(private_workspace)
    after_replay = private_workspace / "binding-query.json"
    binder.main(
        [
            "--surface",
            str(surface_path),
            "--contract",
            str(_gate_contract(surface_path)),
            "--type-sets",
            str(type_sets),
            "--replay-receipt",
            result["replay_receipt_sha256"],
            "--output",
            str(after_replay),
        ]
    )

    assert json.loads(after_replay.read_bytes())["cases_sha256"] == frozen_cases

    query_results = private_workspace / "query"
    completed = _run(
        "native_query",
        [
            "--ledger",
            str(private_workspace / "history.jsonl"),
            "--binding",
            str(after_replay),
            "--results",
            str(query_results),
        ],
    )
    assert completed.returncode == 0, completed.stderr

    query_result = json.loads((query_results / "query-result.json").read_bytes())
    rows = query_result["queries"][0]["rows"]

    assert query_result["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert query_result["inputs"]["query_binding_sha256"] == _digest(
        after_replay.read_bytes()
    )
    relation_rows = [row for row in rows if row["kind"] == "RELATION"]
    assert Counter(row["kind"] for row in rows) == Counter(
        {"ENTITY": 2, "RELATION": 1}
    )
    assert len(relation_rows) == 1
    assert relation_rows[0]["witness"] == {
        "relation_id": "inspection-of:P-7:2026-03-02",
        "source_id": "inspection:P-7:2026-03-02",
        "target_id": "asset:P-7",
    }
    assert relation_rows[0]["target"]["name"] == "P-7"


def test_usage_is_differenced_from_the_cumulative_launch_log_figures() -> None:
    subject = _module("usage_from_launch_log")

    usage = subject.derive(deepcopy(LAUNCH_LOG))

    assert usage["schema"] == "malleus.paper-v4.producer-usage/v1"
    assert usage["run"] == "run-22"
    assert usage["model_id"] == "claude-opus-5"
    assert [item["stage"] for item in usage["stages"]] == [
        "ONTOLOGY_ATTEMPT_01",
        "ONTOLOGY_ATTEMPT_02",
        "POPULATION",
    ]
    assert [item["tokens"] for item in usage["stages"]] == [185877, 17875, 167274]
    assert sum(item["tokens"] for item in usage["stages"]) == 371026
    assert usage["producer_total_tokens"] == 371026
    assert usage["review"] == {"model_id": "claude-opus-5", "tokens": 322049}
    assert "ADMITTED_AND_REPLAYED at runner attempt 1" in usage["population"]
    assert "0000000" in usage["population"]


def test_the_usage_record_refuses_a_launch_log_of_another_shape() -> None:
    subject = _module("usage_from_launch_log")

    for mutate, expected in (
        (lambda log: log.__setitem__("schema", "malleus.paper-v4.producer-launch-log/v1"), "v2"),
        (lambda log: log.pop("review"), "review"),
        (lambda log: log["runner"][0].pop("execution_commit"), "execution_commit"),
        (lambda log: log["launches"][0].pop("first_stage"), "first_stage"),
        (lambda log: log.__setitem__("drafts", []), "undeclared"),
    ):
        log = deepcopy(LAUNCH_LOG)
        mutate(log)
        with pytest.raises(subject.UsageRefusal, match=expected):
            subject.derive(log)


def test_the_usage_record_refuses_a_cumulative_figure_that_decreases() -> None:
    subject = _module("usage_from_launch_log")
    log = deepcopy(LAUNCH_LOG)
    log["launches"][0]["usage_by_resume"][0]["tokens"] = 1

    with pytest.raises(subject.UsageRefusal, match="decreases"):
        subject.derive(log)
