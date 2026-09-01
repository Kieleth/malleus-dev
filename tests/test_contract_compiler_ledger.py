from __future__ import annotations

import hashlib
import json
import shlex
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from unicodedata import category
from urllib.parse import urlsplit

import pytest
import yaml
from jsonschema import FormatChecker
from markdown_it import MarkdownIt
from rdflib import Graph, Literal, URIRef
from rdflib.exceptions import ParserError
from rdflib.plugins.parsers.notation3 import BadSyntax

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.contract_compiler_ledger import (  # noqa: E402
    LedgerValidationError,
    _superseded_entries,
    canonical_json,
    entry_hash,
    load_ledger,
    render_status,
    verify_evidence_snapshot,
)
from scripts.contract_compiler_integration import (  # noqa: E402
    validate_candidate_history,
)
from scripts.ci import plan as ci_plan  # noqa: E402


OVERSEER = ROOT / "design" / "contract_compiler" / "overseer"
STEADY_STATE_WORKFLOWS = (
    ROOT / ".github" / "workflows" / "tests.yml",
    ROOT / ".github" / "workflows" / "release.yml",
)
CC002_CARD = (
    ROOT / "design" / "contract_compiler" / "workstreams" / "CC-002" / "manifest.json"
)
INTEGRATION = ROOT / "design" / "contract_compiler" / "integration.json"
GOVERNANCE_BASE_COMMIT = "6325bd962ecfd00bd4ca62b1d9febd07e3737357"
R3_GOVERNANCE_BASE_COMMIT = "a3d2d644fa92ae6d59bff0cc5a422557d35afe85"
CC002_CHECKPOINT_LINEAGE = (
    "a7a65ccfdd7afd7d42a40509631fcdfef49f135e",
    "4cbf79c287b7fdc3c21beda3869bd45b3835d8f4",
    "a48c754ae6a7aa904c3317d3cdde06de6db8ff98",
    GOVERNANCE_BASE_COMMIT,
)
CC002_SELECTION_COMMIT = "fc23888e012b0771289b5006ccd9a74945db2220"
CC002_LINEAGE_CONTRACT = (
    "Bind the four governed historical worker checkpoints as final-byte evidence "
    "only: a7a65ccfdd7afd7d42a40509631fcdfef49f135e, "
    "4cbf79c287b7fdc3c21beda3869bd45b3835d8f4, "
    "a48c754ae6a7aa904c3317d3cdde06de6db8ff98, and "
    "6325bd962ecfd00bd4ca62b1d9febd07e3737357."
)
FOUNDATION_PROJECTIONS = (
    ROOT / "design" / "PROTOCOL_FOUNDATION_GRAPH.md",
    ROOT / "design" / "ONTOLOGY_DRIVEN_KG_REALIZATION.md",
    ROOT / "design" / "GRAPH_RECIPE_OTTR_PROFILE.md",
    ROOT / "design" / "GRAPH_REALIZATION_SESSION_CHECKPOINT.md",
    ROOT / "design" / "GRAPH_RECIPE_TDD_EXPERIMENTS.md",
)
HISTORICAL_CCD12_PATHS = (
    "design/contract_compiler/overseer/entries/OVR-000050.json",
    "design/contract_compiler/overseer/entries/OVR-000053.json",
    "design/contract_compiler/overseer/entries/OVR-000054.json",
    "design/contract_compiler/overseer/evidence/CC-D12.json",
    "design/contract_compiler/workstreams/CC-D12/manifest.json",
)
HISTORICAL_R3_PATHS = (
    *(
        f"design/contract_compiler/overseer/entries/OVR-{sequence:06d}.json"
        for sequence in range(58, 69)
    ),
    "design/contract_compiler/overseer/evidence/CC-D12-R2.json",
    "design/contract_compiler/overseer/evidence/CC-002-progress-01.json",
)
OD005_HEADING = "### OD-005: logical fact record and canonical bytes"
OD005_NEXT_HEADING = "### OD-006: closed contract roles and composition"
OD006_HEADING = OD005_NEXT_HEADING
OD006_NEXT_HEADING = "### OD-007: protected governance partition topology"
OD007_HEADING = OD006_NEXT_HEADING
OD007_NEXT_HEADING = "### OD-008: closed LinkML v0 support profile"
OD008_HEADING = OD007_NEXT_HEADING
OD008_NEXT_HEADING = "### OD-010: contextual graph references and endpoints"
OD010_HEADING = OD008_NEXT_HEADING
OD010_NEXT_HEADING = "### OD-011: resolver and import policy"
OD005_SEED_TABLE_HEADER = (
    "Subject kind",
    "Predicate",
    "Object type or target",
    "Cardinality",
)
OD005_SEED_ROWS = (
    ("`Class`", "`rdf:type`", "exactly `Class`", "1"),
    ("`Class`", "`rdfs:subClassOf`", "`Class`", "0..1"),
    ("`Class`", "`cf:isMixin`", "Boolean", "1"),
    (
        "`Class`",
        "`cf:usesMixin`",
        "distinct `Class` with `isMixin=true`",
        "0..*",
    ),
    ("`Class`", "`cf:abstract`", "Boolean", "1"),
    ("`Slot`", "`rdf:type`", "exactly `Slot`", "1"),
    (
        "`Slot`, `SlotUse`",
        "`cf:valueRange`",
        "`Class`, `Enum`, `Scalar`, or `SeedPrimitive`",
        "1",
    ),
    ("`Slot`, `SlotUse`", "`cf:required`", "Boolean", "1"),
    ("`Slot`, `SlotUse`", "`cf:multivalued`", "Boolean", "1"),
    ("`Slot`, `SlotUse`", "`cf:identifier`", "Boolean", "1"),
    ("`Slot`, `SlotUse`", "`cf:inlined`", "Boolean", "1"),
    ("`Slot`, `SlotUse`", "`cf:equalsString`", "string", "0..1"),
    (
        "`Slot`, `SlotUse`",
        "`cf:minimum`",
        "canonical decimal lexical string",
        "0..1",
    ),
    (
        "`Slot`, `SlotUse`",
        "`cf:maximum`",
        "canonical decimal lexical string",
        "0..1",
    ),
    (
        "`Slot`, `SlotUse`",
        "`cf:valuePresence`",
        "string `PRESENT` or `ABSENT`",
        "0..1",
    ),
    ("`SlotUse`", "`rdf:type`", "exactly `SlotUse`", "1"),
    ("`SlotUse`", "`cf:onClass`", "`Class`", "1"),
    ("`SlotUse`", "`cf:usesSlot`", "`Slot`", "1"),
    ("`Enum`", "`rdf:type`", "exactly `Enum`", "1"),
    ("`Enum`", "`cf:enumValue`", "distinct string", "0..*"),
    ("`Scalar`", "`rdf:type`", "exactly `Scalar`", "1"),
    ("`Scalar`", "`cf:typeof`", "`Scalar` or `SeedPrimitive`", "1"),
)
OD005_SEED_PRIMITIVES = ("String", "Integer", "Float", "Boolean", "DateTime")
OD006_ROLE_TABLE = (
    ("Fixed role", "Complete contract governed by the role"),
    (
        "`ProtocolRecordContract`",
        "Protocol records, events, transitions, and ledger-facing protocol semantics",
    ),
    (
        "`GovernedGraphContract`",
        "Governed domain records, relations, fields, and structural graph semantics",
    ),
    (
        "`GovernanceContract`",
        "Authorization and governance-policy semantics",
    ),
)
OD006_DELTA_TABLE = (
    (
        "Change",
        "Protocol role",
        "Governed-graph role",
        "Governance role",
        "Composition",
        "Accepted-temporal epoch",
    ),
    ("Presentation or provenance only", "same", "same", "same", "same", "same"),
    ("Protocol semantic edit", "changed", "same", "same", "changed", "new"),
    ("Domain semantic edit", "same", "changed", "same", "changed", "new"),
    ("Governance semantic edit", "same", "same", "changed", "changed", "new"),
)
OD008_PROFILE_HEADER = (
    "Exact source location",
    "ENFORCED",
    "IDENTITY_ONLY",
    "ANNOTATION_ONLY",
    "REJECTED",
)
OD010_REFERENCE_ROWS = (
    ("Case", "Outcome", "Reason"),
    (
        "present scalar target or every multivalue target exists in the same role and partition and has the declared class or subclass",
        "ACCEPT",
        "the complete strong-reference obligation is satisfied",
    ),
    (
        "inlined class-valued SlotUse",
        "ACCEPT AS CONTAINED VALUE",
        "it is not a graph reference",
    ),
    (
        "missing target, wrong concrete type, or mixin-only match",
        "REFUSE CANDIDATE",
        "existence and class ancestry are mandatory; usesMixin is not subClassOf",
    ),
    (
        "target in another contract role or replay-derived partition",
        "REFUSE CANDIDATE",
        "D06 forbids borrowing another role's registry or facts",
    ),
    (
        "target admitted earlier in dependency order",
        "ACCEPT",
        "earlier candidate state is visible",
    ),
    (
        "target admitted later, self-reference through the same create, or reference cycle",
        "REFUSE CANDIDATE",
        "runtime does not search, reorder, or solve a fixed point",
    ),
    (
        "primitive ID or hash scalar outside a class-valued SlotUse",
        "SCALAR CONTENT",
        "it does not masquerade as a contextual graph reference",
    ),
)
OD010_CONTEXT_ROWS = (
    ("Contextual rule", "Accept", "Refuse"),
    (
        "Relation endpoint",
        "existing same-role and same-partition Entity of the declared class or subclass",
        "missing, Event, Signal, Relation, protocol, governance, cross-role, cross-partition, or wrong Entity type",
    ),
    (
        "Signal bearer",
        "existing same-role and same-partition Entity or Relation",
        "missing, Event, Signal, cross-role, or cross-partition target",
    ),
    (
        "Record identity",
        "one unused ID",
        "reuse across any graph category or partition",
    ),
    (
        "Selected temporal view",
        "every visible strong reference, endpoint, and bearer has its visible target",
        "any visible referrer with an omitted target",
    ),
)
OD008_PROFILE_ROWS = (
    (
        "schema root",
        "types, enums, slots, classes, imports, default_range",
        "id, prefixes; each prefix key and value; each import reference; the default_range reference",
        "name, version, title, description",
        "every other field; every annotation",
    ),
    (
        "types.<type>",
        "typeof",
        "declaration map key; typeof reference",
        "uri, description",
        "every other field; every annotation",
    ),
    (
        "enums.<enum>",
        "permissible_values",
        "declaration map key",
        "description",
        "every other field; every annotation",
    ),
    (
        "enums.<enum>.permissible_values.<value>",
        "permissible-value map key",
        "none",
        "description",
        "every other field; every annotation",
    ),
    (
        "slots.<slot> global declaration",
        "range, required, multivalued, identifier, inlined, equals_string, minimum_value, maximum_value, value_presence",
        "declaration map key; range reference; annotations.adopts only for the exact imported global-slot redeclaration authorized by OD-002",
        "description",
        "every other field; every other annotation, including annotations.retires",
    ),
    (
        "classes.<class>",
        "is_a, mixin, mixins, abstract, slots, attributes, slot_usage, exactly_one_of",
        "declaration map key; references in is_a, mixins, and slots",
        "class_uri, description",
        "every other field; every annotation",
    ),
    (
        "classes.<class>.attributes.<slot>",
        "range, required, multivalued, identifier, inlined, equals_string, minimum_value, maximum_value, value_presence",
        "local declaration map key; range reference",
        "description",
        "every other field; every annotation",
    ),
    (
        "classes.<class>.slot_usage.<slot>",
        "range, required, multivalued, identifier, inlined, equals_string, minimum_value, maximum_value, value_presence",
        "authoritative slot reference map key; range reference",
        "description",
        "every other field; every annotation",
    ),
    (
        "classes.<class>.exactly_one_of",
        "flat nonempty alternative sequence",
        "none",
        "none",
        "empty sequence; any_of, all_of, none_of; nesting; every other expression field",
    ),
    (
        "one exactly_one_of alternative",
        "one nonempty slot_conditions map",
        "each slot_conditions map key is an authoritative qualified slot reference",
        "none",
        "empty alternative; every other field; every annotation",
    ),
    (
        "one slot_conditions.<slot> condition",
        "required, equals_string, value_presence, with at least one present",
        "the authoritative slot reference inherited from its map key",
        "none",
        "every other field; every annotation; nested expression",
    ),
)
OD008_SOURCE_VALUE_ROWS = (
    (
        "document and every declaration, attribute, slot-usage, alternative, condition, annotation, or description-bearing body",
        "mapping; never null",
    ),
    ("schema id and name", "required nonempty strings"),
    (
        "version, title, every description, class_uri, type uri, and equals_string",
        "string when present",
    ),
    (
        "prefixes",
        "mapping from an ASCII identifier key to a nonempty absolute-IRI string",
    ),
    (
        "imports, class mixins, and class slots",
        "sequence of nonempty reference strings; a scalar is not promoted to a sequence",
    ),
    (
        "types, enums, slots, classes, attributes, slot_usage, permissible_values, and slot_conditions",
        "mapping with the location-specific key and body rules",
    ),
    (
        "default_range, typeof, range, and is_a",
        "one nonempty reference string",
    ),
    (
        "mixin, abstract, required, multivalued, identifier, and inlined",
        "raw lowercase true or false; quoted, title-case, and YAML-only Boolean spellings refuse",
    ),
    (
        "minimum_value and maximum_value",
        "one finite JSON-number lexical scalar under the grammar below; retain the exact source lexeme",
    ),
    ("value_presence", "string exactly PRESENT or ABSENT"),
    ("exactly_one_of", "nonempty sequence of alternative mappings"),
    (
        "annotations at the one adopted-slot location",
        "mapping exactly adopts: true, with literal Boolean true",
    ),
    (
        "one permissible-value body",
        "raw empty scalar or lowercase null, empty mapping, or mapping exactly description: <string>",
    ),
)
OD008_BUILTIN_ROWS = (
    ("string", "cf:String", "none; trusted D05 seed target"),
    ("integer", "cf:Integer", "none; trusted D05 seed target"),
    ("float", "cf:Float", "none; trusted D05 seed target"),
    ("boolean", "cf:Boolean", "none; trusted D05 seed target"),
    ("datetime", "cf:DateTime", "none; trusted D05 seed target"),
    (
        "date",
        "https://w3id.org/linkml/types/date",
        "rdf:type cf:Scalar; cf:typeof cf:String",
    ),
    (
        "uri",
        "https://w3id.org/linkml/types/uri",
        "rdf:type cf:Scalar; cf:typeof cf:String",
    ),
)
OD008_CORPUS_ROWS = (
    (
        "ontology/malleus.yaml",
        "ACCEPT",
        "closed non-expression profile and trusted seven-name builtin map",
    ),
    (
        "ontology/assent.yaml",
        "ACCEPT",
        "closed profile plus flat exactly_one_of ValidTime evidence",
    ),
    (
        "ontology/domains/attack.yaml",
        "ACCEPT",
        "closed non-expression profile",
    ),
    (
        "ontology/domains/cyp450.yaml",
        "ACCEPT",
        "closed non-expression profile",
    ),
    (
        "ontology/domains/ocr.yaml",
        "ACCEPT",
        "closed non-expression profile",
    ),
    (
        "ontology/domains/recon.yaml",
        "ACCEPT",
        "closed non-expression profile",
    ),
    ("CC-X01/simple_parity", "ACCEPT", "supported direct slot use"),
    (
        "CC-X01/parent_mixin_precedence",
        "ACCEPT",
        "exact pinned ancestor traversal",
    ),
    (
        "CC-X01/repeated_mixin",
        "REFUSE",
        "repeated authored mixin reference",
    ),
    (
        "CC-X01/conflicting_mixins_ab",
        "REFUSE",
        "conflicting ENFORCED mixin values",
    ),
    (
        "CC-X01/conflicting_mixins_ba",
        "REFUSE",
        "same conflict after source-order reversal",
    ),
    ("CC-X01/numeric_bounds", "ACCEPT", "supported numeric-bound intersection"),
    (
        "CC-X01/explicit_false",
        "REFUSE",
        "measured SlotUse remains EQUAL, but global String Slot has illegal inlined=true",
    ),
    (
        "CC-X01/default_range",
        "ACCEPT",
        "supported default_range materialization with provenance",
    ),
    (
        "CC-X01/attribute_slot_usage",
        "ACCEPT",
        "supported local attribute plus applicable slot_usage",
    ),
    (
        "D08/valid_explicit_false",
        "ACCEPT",
        "separate valid String Slot and SlotUse with four explicit false values",
    ),
)
OD008_DEFAULT_ROWS = (
    ("class declaration", "mixin", "cf:isMixin=false"),
    ("class declaration", "abstract", "cf:abstract=false"),
    (
        "global slot, local attribute, or effective SlotUse",
        "range",
        "schema default_range; if that is absent, seed String",
    ),
    (
        "global slot, local attribute, or effective SlotUse",
        "required",
        "cf:required=false",
    ),
    (
        "global slot, local attribute, or effective SlotUse",
        "multivalued",
        "cf:multivalued=false",
    ),
    (
        "global slot, local attribute, or effective SlotUse",
        "identifier",
        "cf:identifier=false",
    ),
    ("supported Slot or SlotUse with non-Class range", "inlined", "cf:inlined=false"),
    (
        "supported Slot or SlotUse with Class range whose target has exactly one effective identifier slot",
        "inlined",
        "cf:inlined=false",
    ),
    (
        "supported Slot or SlotUse with Class range whose target has no effective identifier slot",
        "inlined",
        "cf:inlined=true",
    ),
    ("type declaration", "typeof", "no default; refuse incomplete Scalar"),
    (
        "any supported constraint location",
        "equals_string, minimum_value, maximum_value, value_presence",
        "no fact",
    ),
    (
        "class declaration",
        "is_a, mixins, slots, attributes, slot_usage, exactly_one_of",
        "no relation or expression fact",
    ),
)
OD008_EXPRESSION_ROWS = (
    ("ExactlyOneGroup", "rdf:type", "exactly ExactlyOneGroup", "1"),
    ("ExactlyOneGroup", "cf:onClass", "Class", "1"),
    (
        "ExactlyOneAlternative",
        "rdf:type",
        "exactly ExactlyOneAlternative",
        "1",
    ),
    ("ExactlyOneAlternative", "cf:inGroup", "ExactlyOneGroup", "1"),
    ("SlotCondition", "rdf:type", "exactly SlotCondition", "1"),
    ("SlotCondition", "cf:inAlternative", "ExactlyOneAlternative", "1"),
    ("SlotCondition", "cf:usesSlot", "authoritative qualified Slot", "1"),
    ("SlotCondition", "cf:required", "Boolean", "0..1"),
    ("SlotCondition", "cf:equalsString", "string", "0..1"),
    (
        "SlotCondition",
        "cf:valuePresence",
        "string PRESENT or ABSENT",
        "0..1",
    ),
)
OD008_SEED_INVARIANTS = (
    (
        "absent-conflicts-with-required-true-or-equals-string",
        "valuePresence=ABSENT refuses when required=true or equalsString is present on the same Slot or SlotUse.",
    ),
    (
        "atomic-whole-fact-set-validation",
        "Validation accepts or refuses the complete supplied fact set atomically; it never returns or accepts a valid subset after any violation.",
    ),
    (
        "class-parent-and-mixin-graph-acyclic",
        "The union of rdfs:subClassOf and cf:usesMixin edges between Class subjects is acyclic.",
    ),
    (
        "enforced-kind-predicate-cardinality-and-whole-set-completeness",
        "Every fact subject has exactly one rdf:type kind fact and exactly the closed kind-specific predicate cardinalities in the active metamodel's rules; no other kind or predicate is legal.",
    ),
    (
        "equals-string-only-string-resolving-or-enum-range",
        "On a Slot or SlotUse subject, cf:equalsString is legal only when cf:valueRange directly names cf:String or an Enum, or resolves through a Scalar chain terminating in cf:String.",
    ),
    (
        "every-non-seed-identifier-target-resolves-in-fact-set",
        "Every object of rdfs:subClassOf, cf:usesMixin, cf:typeof, cf:valueRange, cf:onClass, or cf:usesSlot resolves to a fact subject in the same whole fact set, except an allowed SeedPrimitive object of cf:typeof or cf:valueRange.",
    ),
    (
        "exact-duplicate-fact-record-refuses",
        "An exact duplicate subject-predicate-object fact record refuses the whole fact set; convergent derivation provenance remains outside the fact set.",
    ),
    (
        "inlined-true-only-class-range",
        "cf:inlined=true is legal only when cf:valueRange names Class.",
    ),
    (
        "numeric-bounds-only-integer-or-float-and-minimum-not-greater-than-maximum",
        "cf:minimum and cf:maximum are legal only when cf:valueRange directly names cf:Integer or cf:Float, or resolves through a Scalar chain terminating in cf:Integer or cf:Float, and minimum cannot exceed maximum.",
    ),
    (
        "scalar-typeof-acyclic-and-terminates-in-seed-primitive",
        "The Scalar cf:typeof graph is acyclic and every path terminates in exactly one of the five SeedPrimitive targets.",
    ),
    (
        "seed-primitives-are-targets-not-fact-subjects",
        "The five SeedPrimitive IRIs are trusted targets and cannot occur as fact subjects.",
    ),
    (
        "uses-mixin-target-has-is-mixin-true",
        "Every cf:usesMixin object resolves to a Class subject in the same whole fact set whose cf:isMixin object is true.",
    ),
)
OD008_SEED_STRUCTURAL_IDENTITY_PROFILES = (
    {
        "digest_encoding": "lowercase-hex",
        "domain": "malleus.contract-structure.slot-use/v0",
        "hash": "sha256",
        "members": ["class", "domain", "slot"],
        "output_prefix": "urn:malleus:contract-structure:slot-use:v0:sha256:",
    },
)
OD008_EXPRESSION_INVARIANTS = (
    (
        "alternative-has-one-or-more-conditions",
        "Every ExactlyOneAlternative belongs to one ExactlyOneGroup and has one or more SlotCondition subjects.",
    ),
    (
        "condition-equals-string-uses-d05-effective-slot-use-range-rule",
        "SlotCondition cf:equalsString is legal only when the declaring-class effective SlotUse range directly names cf:String or an Enum, or resolves through a Scalar chain terminating in cf:String.",
    ),
    (
        "condition-has-one-or-more-enforcing-members",
        "Every SlotCondition has at least one of cf:required, cf:equalsString, or cf:valuePresence.",
    ),
    (
        "condition-slot-has-applicable-effective-slot-use-on-declaring-class",
        "Every SlotCondition cf:usesSlot target has an applicable effective SlotUse on the ExactlyOneGroup declaring Class.",
    ),
    (
        "declaring-class-group-reified-once-and-inherited-conjunctively-without-copy",
        "Each Class has at most one directly declared ExactlyOneGroup; that group is reified once on its declaring Class; descendants apply ancestor and local groups conjunctively without copied or reidentified groups.",
    ),
    (
        "duplicate-semantic-alternatives-and-conditions-refuse",
        "Duplicate semantic alternatives in one group and duplicate authoritative-slot conditions in one alternative refuse the whole fact set.",
    ),
    (
        "group-has-one-or-more-alternatives",
        "Every ExactlyOneGroup names one Class and has one or more ExactlyOneAlternative subjects.",
    ),
    (
        "group-and-alternative-structural-targets-resolve-in-whole-fact-set",
        "Every cf:inGroup object resolves in the same whole fact set to ExactlyOneGroup, and every cf:inAlternative object resolves there to ExactlyOneAlternative.",
    ),
    (
        "only-flat-class-exactly-one-of",
        "Only flat class exactly_one_of is legal; nested, any_of, all_of, and none_of forms refuse, and no cross-branch or cross-group satisfiability analysis occurs.",
    ),
    (
        "semantic-order-independent-structural-identities",
        "Branch, condition, and member order does not change structural envelopes, subjects, or canonical facts; source indexes never enter identity.",
    ),
    (
        "value-presence-absent-conflicts-with-required-true-or-equals-string",
        "Within one SlotCondition, cf:valuePresence ABSENT refuses with cf:required true or any cf:equalsString.",
    ),
)
OD008_EXPRESSION_STRUCTURAL_IDENTITY_PROFILES = (
    {
        "digest_encoding": "lowercase-hex",
        "domain": "malleus.exactly-one-alternative-semantics/v0",
        "hash": "sha256",
        "members": ["conditions", "domain"],
        "output_prefix": "sha256:",
        "sorted_arrays": {
            "conditions": "canonical-json-object-bytes-ascending",
        },
    },
    {
        "digest_encoding": "lowercase-hex",
        "domain": "malleus.contract-structure.exactly-one-group/v0",
        "hash": "sha256",
        "members": ["alternative_semantic_digests", "class", "domain"],
        "output_prefix": (
            "urn:malleus:contract-structure:exactly-one-group:v0:sha256:"
        ),
        "sorted_arrays": {
            "alternative_semantic_digests": "canonical-json-string-bytes-ascending",
        },
    },
    {
        "digest_encoding": "lowercase-hex",
        "domain": "malleus.contract-structure.exactly-one-alternative/v0",
        "hash": "sha256",
        "members": [
            "alternative_semantic_digest",
            "domain",
            "group",
        ],
        "output_prefix": (
            "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:"
        ),
    },
    {
        "digest_encoding": "lowercase-hex",
        "domain": "malleus.contract-structure.slot-condition/v0",
        "hash": "sha256",
        "members": ["alternative", "domain", "slot"],
        "output_prefix": (
            "urn:malleus:contract-structure:slot-condition:v0:sha256:"
        ),
    },
)
OD008_EXPRESSION_SEMANTIC_MEMBER_PROFILES = (
    {
        "minimum_optional_members": 1,
        "name": "slot-condition-semantics",
        "optional_members": ["equalsString", "required", "valuePresence"],
        "required_members": ["slot"],
    },
)
OD008_SEED_METAMODEL_ID = (
    "urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:"
    "1c68a612f3e7a0f80c31965aa5525954921dfbee60d151552d10d61cb0aac71b"
)
OD008_EXPRESSION_METAMODEL_ID = (
    "urn:malleus:contract-metamodel:flat-exactly-one-extension:v0:sha256:"
    "99527d21040cbdda9dd7c579af7f40af8645de9b5f4b1e8ba28b40ddff7d53e6"
)
OD008_COMPOSITION_OPERATOR = (
    "The active rules are the exact closed union of base.rules and extension.rules; "
    "duplicate kind-predicate rows refuse composition; both invariant sets apply "
    "with their literal subject and whole-set quantifiers; every invariant reference "
    "to active rules means that union; no other kind or predicate is legal."
)
OD008_COMBINED_METAMODEL_ID = (
    "urn:malleus:contract-metamodel:expression-capable:v0:sha256:"
    "65aae23b7a0892a4d2ae2b5adc6888f1ddd39c94ce03f412d50a6a5ccd5d0964"
)
OD008_SYMBOL_POLICY_ID = (
    "urn:malleus:contract-symbol-policy:linkml-v0-slash-qualified:v0"
)
OD008_ANCESTOR_FENCE = """ancestors = [class]
stack = [class]
visited = []
while stack is not empty:
  current = stack.pop_last()
  visited.append(current)
  for parent in authored_mixins_then_is_a(current):
    if parent is absent from visited and ancestors:
      stack.append(parent)
      ancestors.append(parent)
apply slot_usage for each class in reverse(ancestors)"""
OD008_NUMBER_FENCE = """number = ["-"] integer [fraction] [exponent]
integer = "0" | nonzero-digit {digit}
fraction = "." digit {digit}
exponent = ("e" | "E") ["+" | "-"] digit {digit}"""
OD006_CONSTRUCTOR_FENCES = (
    """RoleBoundContractIdentity(
  fixed logical token: malleus.contract-role-bound-identity/v0,
  fixed_role_name,
  exact_effective_contract_identity
)""",
    """ContractCompositionIdentity(
  fixed logical token: malleus.contract-composition-identity/v0,
  ProtocolRecordContract_role_identity,
  GovernedGraphContract_role_identity,
  GovernanceContract_role_identity
)""",
)
OD006_REFUSAL_PARAGRAPHS = (
    (
        "Composition refuses atomically when a role is missing, duplicated, "
        "unknown, or supplied more than once; when protocol and governed-graph "
        "slots are swapped; when a role tag, version, or identity domain is "
        "wrong; when an already-bound epoch is continued with a valid replacement "
        "role identity but no new composition is constructed and bound; when "
        "roles from different compositions are mixed without constructing a new "
        "composition; or when equal payload is treated as proof that two roles "
        "are interchangeable."
    ),
    (
        "It also refuses an incomplete role closure that relies on ambient "
        "declarations or another role, a protocol contract used to validate "
        "governed domain state, a governed-graph contract used to validate "
        "protocol records, an independently advanced or borrowed role head, "
        "continuation of a ledger after composition change, and any inferred "
        "latest or current composition. A structural-only graph refuses protocol "
        "or governance roles, a composition identity, or a protocol ledger. An "
        "accepted-temporal graph refuses a structural-only binding. "
        "Whole-composition validation refuses atomically; no subset is accepted."
    ),
)
OD006_ORDERED_REFUSAL_CLAIMS = (
    "a role is missing",
    "duplicated",
    "unknown",
    "supplied more than once",
    "protocol and governed-graph slots are swapped",
    "a role tag, version, or identity domain is wrong",
    (
        "an already-bound epoch is continued with a valid replacement role "
        "identity but no new composition is constructed and bound"
    ),
    "roles from different compositions are mixed without constructing a new composition",
    "equal payload is treated as proof that two roles are interchangeable",
    "an incomplete role closure that relies on ambient declarations or another role",
    "a protocol contract used to validate governed domain state",
    "a governed-graph contract used to validate protocol records",
    "an independently advanced or borrowed role head",
    "continuation of a ledger after composition change",
    "any inferred latest or current composition",
    (
        "A structural-only graph refuses protocol or governance roles, a "
        "composition identity, or a protocol ledger"
    ),
    "An accepted-temporal graph refuses a structural-only binding",
)
IMMUTABLE_R3_REFINEMENT_INPUTS = {
    "design/contract_compiler/overseer/entries/OVR-000069.json": "3f1f72dbb437fbbf2e1aad2dfaeec213884228f169330361e513c6af700ad910",
    "design/contract_compiler/overseer/entries/OVR-000070.json": "011f1ccef652b5299b23aa4588edd66dacc2802a0ed2fb0370669a6b5c1747ce",
    "design/contract_compiler/overseer/entries/OVR-000071.json": "62c93ddd39554c47af605923c4ab7f428ed87f5694c4600d834fbe70f31396e3",
    "design/contract_compiler/overseer/entries/OVR-000072.json": "095ceccda8ddc22a29cb3481da41bce52a9f53ea2a61b61c361db0a7ebcef0bb",
    "design/contract_compiler/overseer/entries/OVR-000073.json": "b5867998fafe3dc2649b251819145f032d456d7b54c07ee807de57c67e4694eb",
    "design/contract_compiler/overseer/entries/OVR-000074.json": "30de0203fee9a3c6ae25a0ede22b573e70c19f73b1bdd6601f88cab6a74cbc8f",
    "design/contract_compiler/overseer/entries/OVR-000075.json": "64b4d744cfe491df70dfa3c4d18d9944654a620eeb05ac888475cd2ab3a07da2",
    "design/contract_compiler/overseer/entries/OVR-000076.json": "fbac3bceeee378bd2f5fe5c9633fabedfc636170c2d212a9ce717ae09d4fdf41",
    "design/contract_compiler/overseer/entries/OVR-000077.json": "b57a83e46bb2e015a62715a02c251a763ec1c3ed4aace4394f9e85b320ab0cef",
    "design/contract_compiler/overseer/evidence/CC-D12-R3.json": "1f4e71eb7c0f3dac0be5bf6bd8e633dfc6975979e5756796631cf014320c3bd9",
}


def _od005_section(decisions: str) -> str:
    assert decisions.count(OD005_HEADING) == 1
    assert decisions.count(OD005_NEXT_HEADING) == 1
    before, section_and_after = decisions.split(OD005_HEADING, 1)
    section, after = section_and_after.split(OD005_NEXT_HEADING, 1)
    assert OD005_NEXT_HEADING not in before
    assert OD005_HEADING not in after
    return section


def _od006_section(decisions: str) -> str:
    assert decisions.count(OD006_HEADING) == 1
    assert decisions.count(OD006_NEXT_HEADING) == 1
    before, section_and_after = decisions.split(OD006_HEADING, 1)
    section, after = section_and_after.split(OD006_NEXT_HEADING, 1)
    assert OD006_NEXT_HEADING not in before
    assert OD006_HEADING not in after
    return section


def _od007_section(decisions: str) -> str:
    assert decisions.count(OD007_HEADING) == 1
    assert decisions.count(OD007_NEXT_HEADING) == 1
    before, section_and_after = decisions.split(OD007_HEADING, 1)
    section, after = section_and_after.split(OD007_NEXT_HEADING, 1)
    assert OD007_NEXT_HEADING not in before
    assert OD007_HEADING not in after
    return section


def _od008_section(decisions: str) -> str:
    assert decisions.count(OD008_HEADING) == 1
    assert decisions.count(OD008_NEXT_HEADING) == 1
    before, section_and_after = decisions.split(OD008_HEADING, 1)
    section, after = section_and_after.split(OD008_NEXT_HEADING, 1)
    assert OD008_NEXT_HEADING not in before
    assert OD008_HEADING not in after
    return section


def _od010_section(decisions: str) -> str:
    assert decisions.count(OD010_HEADING) == 1
    assert decisions.count(OD010_NEXT_HEADING) == 1
    before, section_and_after = decisions.split(OD010_HEADING, 1)
    section, after = section_and_after.split(OD010_NEXT_HEADING, 1)
    assert OD010_NEXT_HEADING not in before
    assert OD010_HEADING not in after
    return section


def _markdown_tables(section: str) -> tuple[tuple[tuple[str, ...], ...], ...]:
    tables: list[tuple[tuple[str, ...], ...]] = []
    rows: list[tuple[str, ...]] | None = None
    row: list[str] | None = None
    for token in MarkdownIt("commonmark").enable("table").parse(section):
        if token.type == "table_open":
            assert rows is None
            rows = []
        elif token.type == "tr_open" and rows is not None:
            assert row is None
            row = []
        elif token.type == "inline" and row is not None:
            row.append(token.content)
        elif token.type == "tr_close" and rows is not None:
            assert row is not None
            rows.append(tuple(row))
            row = None
        elif token.type == "table_close":
            assert rows is not None and row is None
            tables.append(tuple(rows))
            rows = None
    assert rows is None and row is None
    return tuple(tables)


def _table_named(
    section: str,
    header: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    matches = tuple(table[1:] for table in _markdown_tables(section) if table[0] == header)
    assert len(matches) == 1
    return tuple(tuple(cell.replace("`", "") for cell in row) for row in matches[0])


def _assert_od008_closed_profile(section: str) -> None:
    assert _table_named(section, OD008_PROFILE_HEADER) == OD008_PROFILE_ROWS
    assert _table_named(section, ("Exact source member", "Required raw value")) == (
        OD008_SOURCE_VALUE_ROWS
    )
    assert _table_named(
        section,
        ("LinkML source name", "Neutral target", "Additional facts when referenced"),
    ) == OD008_BUILTIN_ROWS
    assert _table_named(
        section,
        ("Governed source vector", "D08 outcome", "Exact reason"),
    ) == OD008_CORPUS_ROWS
    assert _table_named(
        section,
        ("Effective location", "Omitted field", "Materialized result"),
    ) == OD008_DEFAULT_ROWS
    assert _table_named(
        section,
        ("Subject kind", "Predicate", "Object type or target", "Cardinality"),
    ) == OD008_EXPRESSION_ROWS
    prose = " ".join(section.split())
    for phrase in (
        "Anything absent from the exact table at its exact location is `REJECTED`.",
        "A parser branch alone cannot expand this profile.",
        "V0 accepts exactly one mapping document and no YAML directive or document-boundary marker.",
        "all explicit YAML tags, including core tags such as `!!str`",
        "implicit LinkML coercion refuse",
        "qualified symbol `schema-id + \"/\" + K`",
        "qualified symbol `C + \"/\" + A`",
        "There is no escaping, case folding, Unicode normalization, path normalization",
        "The exact authored import `linkml:types` selects one trusted builtin lookup map.",
        "It does not admit upstream `types.yaml` as ordinary user source.",
        "`linkml_runtime-1.11.1-py3-none-any.whl` with SHA-256 `b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da`",
        "`linkml_runtime/linkml_model/model/schema/types.yaml`",
        "`1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00`",
        "exactly 7,296 member bytes",
        "Null means an empty value declaration, not a semantic null.",
        "`name` and `version` remain module metadata only",
        "Each permissible-value key is `ENFORCED` because it emits one `cf:enumValue` fact.",
        "Effective `identifier=true` forces effective `required=true`",
        "pinned LinkML identifier-based `inlined` derivation",
        "Annotation-only differences never cause that refusal.",
        "A `slot_usage` key must resolve to an already applicable slot",
        "authoritative slot owner and emits no adoption fact",
        "The immutable `ExactNonExpressionSeedContractMetamodel` from D05 is not edited.",
        "`FlatExactlyOneExpressionExtensionV0` is composed with that exact seed",
        "`ExpressionCapableContractMetamodelV0` identity",
        "applicable effective `SlotUse` on the group's declaring class",
        "inherited groups are not copied or reidentified",
        "no other base-slot or branch narrowing is declared contradictory",
        OD008_SEED_METAMODEL_ID,
        OD008_EXPRESSION_METAMODEL_ID,
        OD008_COMBINED_METAMODEL_ID,
        OD008_SYMBOL_POLICY_ID,
        "These are internal candidate structural IDs, not published stable IDs.",
        "Source indexes never enter identity.",
        "D08 does not design a plugin framework",
        "declare its implementation and version plus its exact support, default, and resolver profiles",
        "public support claims remain blocked on `OD-009`.",
    ):
        assert phrase in prose
    for rejected in (
        "`annotations.retires`",
        "`range_expression`",
        "`rules`",
        "`unique_keys`",
        "`any_of`",
        "`all_of`",
        "`none_of`",
    ):
        assert rejected in section

    od005 = _od005_section(
        (ROOT / "design" / "contract_compiler" / "decisions.md").read_text(
            encoding="utf-8"
        )
    )
    assert _od005_seed_table_rows(od005) == OD005_SEED_ROWS
    assert _od005_seed_primitives(od005) == OD005_SEED_PRIMITIVES
    assert {row[0] for row in OD008_EXPRESSION_ROWS}.isdisjoint(
        {row[0] for row in OD005_SEED_ROWS}
    )
    text_fences = tuple(
        token.content.removesuffix("\n")
        for token in MarkdownIt("commonmark").parse(section)
        if token.type == "fence" and token.info.strip() == "text"
    )
    assert text_fences == (
        OD008_NUMBER_FENCE,
        OD008_ANCESTOR_FENCE,
        "urn:malleus:contract-structure:exactly-one-group:v0:sha256:<hex>\n"
        "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:<hex>\n"
        "urn:malleus:contract-structure:slot-condition:v0:sha256:<hex>",
    )
    yaml_fences = tuple(
        token.content
        for token in MarkdownIt("commonmark").parse(section)
        if token.type == "fence" and token.info.strip() == "yaml"
    )
    assert len(yaml_fences) == 1
    explicit_false = _od008_assert_raw_source_grammar(yaml_fences[0])
    _od008_assert_exact_value_types(explicit_false)
    assert explicit_false["slots"]["value"] == {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "range": "string",
        "required": False,
    }
    assert explicit_false["classes"]["Record"]["slot_usage"]["value"] == {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "required": False,
    }


def _od008_source_shape_inventory(
    documents: list[dict[str, object]],
) -> tuple[dict[str, set[str]], set[type[object]], int]:
    observed = {
        name: set()
        for name in (
            "schema",
            "type",
            "enum",
            "permissible_value",
            "slot",
            "class",
            "attribute",
            "slot_usage",
            "alternative",
            "condition",
            "slot_annotation",
        )
    }
    permissible_body_types: set[type[object]] = set()
    null_permissible_values = 0

    def mapping(value: object, location: str) -> dict[str, object]:
        assert isinstance(value, dict), f"{location} body must be a map"
        assert all(isinstance(key, str) for key in value), f"{location} keys must be strings"
        return value

    for document_index, document in enumerate(documents):
        root = mapping(document, f"document[{document_index}]")
        observed["schema"].update(root)
        for kind, observed_name in (
            ("types", "type"),
            ("enums", "enum"),
            ("slots", "slot"),
            ("classes", "class"),
        ):
            declarations = mapping(root.get(kind, {}), f"document[{document_index}].{kind}")
            for name, raw_declaration in declarations.items():
                declaration = mapping(
                    raw_declaration,
                    f"document[{document_index}].{kind}.{name}",
                )
                observed[observed_name].update(declaration)
                if kind == "enums":
                    values = mapping(
                        declaration.get("permissible_values", {}),
                        f"document[{document_index}].enums.{name}.permissible_values",
                    )
                    for value_name, body in values.items():
                        permissible_body_types.add(type(body))
                        if body is None:
                            null_permissible_values += 1
                            continue
                        value = mapping(
                            body,
                            f"document[{document_index}].enums.{name}.permissible_values.{value_name}",
                        )
                        assert set(value) <= {"description"}
                        if "description" in value:
                            assert isinstance(value["description"], str)
                        observed["permissible_value"].update(value)
                elif kind == "slots":
                    if "annotations" in declaration:
                        annotations = mapping(
                            declaration["annotations"],
                            f"document[{document_index}].slots.{name}.annotations",
                        )
                        observed["slot_annotation"].update(annotations)
                elif kind == "classes":
                    for field, observed_field in (
                        ("attributes", "attribute"),
                        ("slot_usage", "slot_usage"),
                    ):
                        nested = mapping(
                            declaration.get(field, {}),
                            f"document[{document_index}].classes.{name}.{field}",
                        )
                        for nested_name, nested_body in nested.items():
                            body = mapping(
                                nested_body,
                                f"document[{document_index}].classes.{name}.{field}.{nested_name}",
                            )
                            observed[observed_field].update(body)
                    alternatives = declaration.get("exactly_one_of", [])
                    assert isinstance(alternatives, list)
                    for alternative_index, alternative_body in enumerate(alternatives):
                        alternative = mapping(
                            alternative_body,
                            f"document[{document_index}].classes.{name}.exactly_one_of[{alternative_index}]",
                        )
                        observed["alternative"].update(alternative)
                        conditions = mapping(
                            alternative.get("slot_conditions", {}),
                            f"document[{document_index}].classes.{name}.exactly_one_of[{alternative_index}].slot_conditions",
                        )
                        for slot, condition_body in conditions.items():
                            condition = mapping(
                                condition_body,
                                f"document[{document_index}].classes.{name}.exactly_one_of[{alternative_index}].slot_conditions.{slot}",
                            )
                            observed["condition"].update(condition)
    return observed, permissible_body_types, null_permissible_values


def _od008_is_json_number_lexeme(value: str) -> bool:
    index = 0
    if value.startswith("-"):
        index = 1
    if index == len(value):
        return False
    if value[index] == "0":
        index += 1
        if index < len(value) and "0" <= value[index] <= "9":
            return False
    elif "1" <= value[index] <= "9":
        index += 1
        while index < len(value) and "0" <= value[index] <= "9":
            index += 1
    else:
        return False
    if index < len(value) and value[index] == ".":
        index += 1
        start = index
        while index < len(value) and "0" <= value[index] <= "9":
            index += 1
        if index == start:
            return False
    if index < len(value) and value[index] in "eE":
        index += 1
        if index < len(value) and value[index] in "+-":
            index += 1
        start = index
        while index < len(value) and "0" <= value[index] <= "9":
            index += 1
        if index == start:
            return False
    return index == len(value)


def _od008_assert_raw_source_grammar(source: str) -> dict[str, object]:
    forbidden_tokens = (
        yaml.tokens.AliasToken,
        yaml.tokens.AnchorToken,
        yaml.tokens.DirectiveToken,
        yaml.tokens.DocumentEndToken,
        yaml.tokens.DocumentStartToken,
        yaml.tokens.TagToken,
    )
    tokens = tuple(yaml.scan(source))
    assert not any(isinstance(token, forbidden_tokens) for token in tokens)
    documents = tuple(yaml.compose_all(source, Loader=yaml.SafeLoader))
    assert len(documents) == 1
    root = documents[0]
    assert isinstance(root, yaml.nodes.MappingNode)
    boolean_fields = {
        "abstract",
        "adopts",
        "identifier",
        "inlined",
        "mixin",
        "multivalued",
        "required",
    }
    bound_fields = {"maximum_value", "minimum_value"}

    def visit(node: yaml.nodes.Node, *, permissible_body: bool = False) -> None:
        if isinstance(node, yaml.nodes.ScalarNode):
            if node.tag == "tag:yaml.org,2002:null":
                assert permissible_body
                assert node.style is None
                assert node.value in {"", "null"}
            return
        if isinstance(node, yaml.nodes.SequenceNode):
            for item in node.value:
                visit(item)
            return
        assert isinstance(node, yaml.nodes.MappingNode)
        keys: set[str] = set()
        for key, value in node.value:
            assert isinstance(key, yaml.nodes.ScalarNode)
            assert key.tag == "tag:yaml.org,2002:str"
            assert key.value and key.value not in keys
            keys.add(key.value)
            if key.value in boolean_fields:
                assert isinstance(value, yaml.nodes.ScalarNode)
                assert value.style is None
                assert value.value in {"true", "false"}
            elif key.value in bound_fields:
                assert isinstance(value, yaml.nodes.ScalarNode)
                assert value.style is None
                assert _od008_is_json_number_lexeme(value.value)
            elif key.value == "permissible_values":
                assert isinstance(value, yaml.nodes.MappingNode)
                permissible_keys: set[str] = set()
                for pv_key, pv_body in value.value:
                    assert isinstance(pv_key, yaml.nodes.ScalarNode)
                    assert pv_key.tag == "tag:yaml.org,2002:str"
                    assert pv_key.value and pv_key.value not in permissible_keys
                    permissible_keys.add(pv_key.value)
                    visit(pv_body, permissible_body=True)
                continue
            visit(value)

    visit(root)
    loaded = yaml.safe_load(source)
    assert isinstance(loaded, dict)

    def retain_numbers(node: yaml.nodes.Node, value: object) -> object:
        if isinstance(node, yaml.nodes.SequenceNode):
            assert isinstance(value, list) and len(node.value) == len(value)
            return [
                retain_numbers(item_node, item_value)
                for item_node, item_value in zip(node.value, value)
            ]
        if not isinstance(node, yaml.nodes.MappingNode):
            return value
        assert isinstance(value, dict)
        result = dict(value)
        for key_node, value_node in node.value:
            assert isinstance(key_node, yaml.nodes.ScalarNode)
            key = key_node.value
            if key in bound_fields:
                assert isinstance(value_node, yaml.nodes.ScalarNode)
                result[key] = Decimal(value_node.value)
            else:
                result[key] = retain_numbers(value_node, result[key])
        return result

    loaded = retain_numbers(root, loaded)
    assert isinstance(loaded, dict)
    return loaded


def _od008_assert_exact_value_types(document: dict[str, object]) -> None:
    prefix_names: set[str] = set()
    root_fields = {
        "classes",
        "default_range",
        "description",
        "enums",
        "id",
        "imports",
        "name",
        "prefixes",
        "slots",
        "title",
        "types",
        "version",
    }
    constraint_fields = {
        "description",
        "equals_string",
        "identifier",
        "inlined",
        "maximum_value",
        "minimum_value",
        "multivalued",
        "range",
        "required",
        "value_presence",
    }

    def ascii_key(value: object) -> bool:
        if not isinstance(value, str) or not value:
            return False
        first = value[0]
        if not ("A" <= first <= "Z" or "a" <= first <= "z" or first == "_"):
            return False
        return all(
            "A" <= char <= "Z"
            or "a" <= char <= "z"
            or "0" <= char <= "9"
            or char == "_"
            for char in value[1:]
        )

    def mapping(value: object) -> dict[str, object]:
        assert isinstance(value, dict)
        assert all(isinstance(key, str) and key for key in value)
        return value

    def string(value: object) -> None:
        assert isinstance(value, str) and value

    def absolute_iri(value: object, *, schema_id: bool = False) -> None:
        string(value)
        assert all(category(char) not in {"Cc", "Cs"} for char in value)
        assert FormatChecker().conforms(value, "iri")
        parsed = urlsplit(value)
        assert parsed.scheme
        if schema_id:
            assert not parsed.query and not parsed.fragment
            assert not value.endswith("/")

    def reference(value: object) -> None:
        string(value)
        if ":" not in value:
            assert ascii_key(value)
            return
        prefix, separator, suffix = value.partition(":")
        assert separator and prefix in prefix_names and ascii_key(suffix)

    def optional_string(body: dict[str, object], field: str) -> None:
        if field in body:
            assert isinstance(body[field], str)

    def string_sequence(value: object) -> None:
        assert isinstance(value, list) and all(
            isinstance(item, str) and item for item in value
        )

    def constraints(body: dict[str, object], *, annotations: bool = False) -> None:
        allowed = constraint_fields | ({"annotations"} if annotations else set())
        assert set(body) <= allowed
        if "range" in body:
            reference(body["range"])
        optional_string(body, "equals_string")
        for field in (
            "required",
            "multivalued",
            "identifier",
            "inlined",
        ):
            if field in body:
                assert type(body[field]) is bool
        for field in ("minimum_value", "maximum_value"):
            if field in body:
                value = body[field]
                assert isinstance(value, Decimal) and value.is_finite()
        if "value_presence" in body:
            assert body["value_presence"] in {"PRESENT", "ABSENT"}
        optional_string(body, "description")
        if "annotations" in body:
            assert annotations
            assert mapping(body["annotations"]) == {"adopts": True}

    root = mapping(document)
    assert set(root) <= root_fields
    assert "id" in root and "name" in root
    absolute_iri(root["id"], schema_id=True)
    string(root["name"])
    for field in ("version", "title", "description"):
        optional_string(root, field)
    if "prefixes" in root:
        prefixes = mapping(root["prefixes"])
        assert all(ascii_key(key) for key in prefixes)
        prefix_names.update(prefixes)
        for value in prefixes.values():
            absolute_iri(value)
    if "imports" in root:
        string_sequence(root["imports"])
    if "default_range" in root:
        reference(root["default_range"])

    for container in ("types", "enums", "slots", "classes"):
        assert all(ascii_key(key) for key in mapping(root.get(container, {})))

    for body in mapping(root.get("types", {})).values():
        declaration = mapping(body)
        assert set(declaration) <= {"description", "typeof", "uri"}
        assert "typeof" in declaration
        reference(declaration["typeof"])
        optional_string(declaration, "uri")
        optional_string(declaration, "description")
    for body in mapping(root.get("enums", {})).values():
        declaration = mapping(body)
        assert set(declaration) <= {"description", "permissible_values"}
        optional_string(declaration, "description")
        for pv_body in mapping(declaration.get("permissible_values", {})).values():
            if pv_body is None:
                continue
            value = mapping(pv_body)
            assert set(value) <= {"description"}
            optional_string(value, "description")
    for body in mapping(root.get("slots", {})).values():
        constraints(mapping(body), annotations=True)
    for body in mapping(root.get("classes", {})).values():
        declaration = mapping(body)
        assert set(declaration) <= {
            "abstract",
            "attributes",
            "class_uri",
            "description",
            "exactly_one_of",
            "is_a",
            "mixin",
            "mixins",
            "slot_usage",
            "slots",
        }
        if "is_a" in declaration:
            reference(declaration["is_a"])
        for field in ("class_uri", "description"):
            optional_string(declaration, field)
        for field in ("mixin", "abstract"):
            if field in declaration:
                assert type(declaration[field]) is bool
        for field in ("mixins", "slots"):
            if field in declaration:
                string_sequence(declaration[field])
                for item in declaration[field]:
                    reference(item)
        for field in ("attributes", "slot_usage"):
            nested_declarations = mapping(declaration.get(field, {}))
            if field == "attributes":
                assert all(ascii_key(key) for key in nested_declarations)
            else:
                for key in nested_declarations:
                    reference(key)
            for nested in nested_declarations.values():
                constraints(mapping(nested))
        if "exactly_one_of" in declaration:
            alternatives = declaration["exactly_one_of"]
            assert isinstance(alternatives, list) and alternatives
            for raw_alternative in alternatives:
                alternative = mapping(raw_alternative)
                assert set(alternative) == {"slot_conditions"}
                conditions = mapping(alternative["slot_conditions"])
                assert conditions
                for slot_reference, raw_condition in conditions.items():
                    reference(slot_reference)
                    condition = mapping(raw_condition)
                    assert condition and set(condition) <= {
                        "equals_string",
                        "required",
                        "value_presence",
                    }
                    for field in ("equals_string",):
                        optional_string(condition, field)
                    if "required" in condition:
                        assert type(condition["required"]) is bool
                    if "value_presence" in condition:
                        assert condition["value_presence"] in {"PRESENT", "ABSENT"}


def _od006_constructor_fences(section: str) -> tuple[str, ...]:
    return tuple(
        token.content.removesuffix("\n")
        for token in MarkdownIt("commonmark").parse(section)
        if token.type == "fence" and token.info.strip() == "text"
    )


def _od006_refusal_paragraphs(section: str) -> tuple[str, ...]:
    heading = "#### Refusal examples"
    boundary = "`OD-006` defines role and composition structure only."
    assert section.count(heading) == 1
    assert section.count(boundary) == 1
    before, refusal_and_after = section.split(heading, 1)
    refusal, after = refusal_and_after.split(boundary, 1)
    assert heading not in after and boundary not in before
    return tuple(
        " ".join(paragraph.split())
        for paragraph in refusal.strip().split("\n\n")
        if paragraph.strip()
    )


def _od005_seed_table_rows(section: str) -> tuple[tuple[str, ...], ...]:
    tokens = MarkdownIt("commonmark").enable("table").parse(section)
    assert sum(token.type == "table_open" for token in tokens) == 1
    rows: list[tuple[str, ...]] = []
    row: list[str] | None = None
    in_table = False
    for token in tokens:
        if token.type == "table_open":
            in_table = True
        elif token.type == "table_close":
            in_table = False
        elif in_table and token.type == "tr_open":
            assert row is None
            row = []
        elif in_table and token.type == "inline":
            assert row is not None
            row.append(token.content)
        elif in_table and token.type == "tr_close":
            assert row is not None
            rows.append(tuple(row))
            row = None
    assert not in_table and row is None
    assert rows[0] == OD005_SEED_TABLE_HEADER
    assert all(len(current) == len(OD005_SEED_TABLE_HEADER) for current in rows)
    return tuple(rows[1:])


def _od005_seed_primitives(section: str) -> tuple[str, ...]:
    lead = "The five trusted `SeedPrimitive` target IRIs are exactly "
    tail = " under the seed namespace."
    paragraphs = tuple(" ".join(part.split()) for part in section.split("\n\n"))
    declarations = tuple(part for part in paragraphs if part.startswith(lead))
    assert len(declarations) == 1
    declaration = declarations[0].split(tail, 1)
    assert len(declaration) == 2
    assert declaration[1] == (
        " They are not XSD aliases and are not fact subjects requiring kind facts."
    )
    names_source = declaration[0].removeprefix(lead)
    assert names_source == "`String`, `Integer`, `Float`, `Boolean`, and `DateTime`"
    inline = MarkdownIt("commonmark").parseInline(names_source)[0]
    return tuple(
        child.content for child in inline.children or () if child.type == "code_inline"
    )


def _assert_od005_closed_seed(section: str) -> None:
    assert _od005_seed_table_rows(section) == OD005_SEED_ROWS
    assert _od005_seed_primitives(section) == OD005_SEED_PRIMITIVES


def _assert_od006_closed_contract(section: str) -> None:
    assert _markdown_tables(section) == (OD006_ROLE_TABLE, OD006_DELTA_TABLE)
    assert _od006_constructor_fences(section) == OD006_CONSTRUCTOR_FENCES
    refusal_paragraphs = _od006_refusal_paragraphs(section)
    assert refusal_paragraphs == OD006_REFUSAL_PARAGRAPHS
    refusal_text = " ".join(refusal_paragraphs)
    refusal_positions = tuple(
        refusal_text.index(claim) for claim in OD006_ORDERED_REFUSAL_CLAIMS
    )
    assert refusal_positions == tuple(sorted(refusal_positions))
    assert len(set(refusal_positions)) == len(OD006_ORDERED_REFUSAL_CLAIMS)
    prose = " ".join(section.split())
    for exact in (
        "exactly these fixed slots, each with cardinality `1..1`",
        "fixed logical token: malleus.contract-role-bound-identity/v0",
        "fixed logical token: malleus.contract-composition-identity/v0",
        "The two versioned domain tokens are fixed by this decision and are not caller parameters.",
        "There is no fourth role, extension role, unknown-member preservation, inferred current role, or optional slot in the v0 full composition.",
        "A change to any one role-bound identity changes the composition identity and starts a new epoch.",
        "V0 has no independently advancing role heads, synchronization protocol, cross-head replay, mixed-epoch recovery, migration machinery, or compatibility relaxation.",
        "This does not make any slot optional in a full composition.",
        "On the accepted-temporal path, a new role value is legal only through a newly constructed composition and a new epoch.",
    ):
        assert exact in prose


def _assert_od010_contract(section: str) -> None:
    assert _markdown_tables(section) == (OD010_REFERENCE_ROWS, OD010_CONTEXT_ROWS)
    prose = " ".join(section.split())
    for exact in (
        "Every non-inlined class-valued `SlotUse` is a strong graph reference.",
        "A present scalar value and every member of a present multivalue must resolve.",
        "D10 runs after the active general missing-value, null, presence, and cardinality evaluation and validates only surviving non-null scalar or list members.",
        "It neither changes nor owns missing, null, presence, or cardinality outcomes.",
        "The concrete target type must equal the declared class range or be its `subClassOf` descendant.",
        "`usesMixin` alone never satisfies the declared class range.",
        "Admission reads accepted prestate plus earlier dependency-ordered candidate writes.",
        "Later writes, self-reference through the same create, forward lookup, fixed-point search, and reference cycles refuse the whole candidate.",
        "The runtime performs no topological sort.",
        "Cross-partition and cross-role strong references refuse in v0.",
        "Relation endpoints remain existing `Entity` records matching the declared endpoint class or subtype.",
        "Signal bearer remains an explicit contextual admission rule",
        "one global record-ID namespace across graph categories and logical partitions",
        "Every selected temporal view must be referentially closed",
        "Admission does not cascade, repair, delete, infer reverse dependencies, propagate uncertainty, or prove interval containment.",
        "One query surface remains; these admission rules create no confidentiality, read-authorization, filtering, or ACL policy.",
        "This decision creates no production implementation, ontology YAML, dependency, package, API, storage, migration, deletion, cascade, repair, or public diagnostic grammar.",
    ):
        assert exact in prose


class _Od007Refusal(ValueError):
    pass


class _Od007ReplayProjection:
    """Abstract replay trace, never a wire, API, record, or operation schema.

    The accepted-event sequence is the test-only lineage projection. It does
    not replace or collapse SourceProtocolLedgerHead, AcceptanceHead, or
    MaterializationHead. The methods consume validated conceptual ledger events.
    They are not graph-write entry points.
    """

    def __init__(
        self,
        bootstrap_authorities: tuple[tuple[str, str], ...],
        governance_contract_identity: str,
        composition_epoch_identity: str,
    ) -> None:
        if len(bootstrap_authorities) != 1:
            raise _Od007Refusal("genesis requires exactly one bootstrap authority root")
        bootstrap_actor, bootstrap_source_identity = bootstrap_authorities[0]
        self.governance_contract_identity = governance_contract_identity
        self.composition_epoch_identity = composition_epoch_identity
        self._bootstrap_actor = bootstrap_actor
        self._bootstrap_source_identity = bootstrap_source_identity
        self._authority_sources = {bootstrap_actor: bootstrap_source_identity}
        self._events: list[tuple[str, tuple[object, ...]]] = []
        self._records: dict[str, tuple[str, object]] = {}

    @classmethod
    def replay(
        cls,
        events: tuple[tuple[str, tuple[object, ...]], ...],
        bootstrap_authorities: tuple[tuple[str, str], ...],
        governance_contract_identity: str,
        composition_epoch_identity: str,
    ) -> _Od007ReplayProjection:
        graph = cls(
            bootstrap_authorities,
            governance_contract_identity,
            composition_epoch_identity,
        )
        for path, arguments in events:
            if path == "domain":
                graph.consume_domain_event(*arguments)
            elif path == "governance":
                graph.consume_governance_event(*arguments)
            else:
                raise AssertionError(f"unknown abstract trace path: {path}")
        return graph

    def accepted_events(self) -> tuple[tuple[str, tuple[object, ...]], ...]:
        return tuple(self._events)

    def query(self, record_id: str) -> tuple[str, object] | None:
        return self._records.get(record_id)

    def _check_role(self, admitted_role: str, expected_role: str) -> None:
        if admitted_role != expected_role:
            raise _Od007Refusal("operation used the wrong contract admission path")

    def consume_domain_event(
        self,
        record_id: str,
        value: object,
        admitted_role: str,
    ) -> None:
        """Apply one abstract ordinary-path transition."""
        self._check_role(admitted_role, "GovernedGraphContract")
        if record_id == self._bootstrap_source_identity:
            raise _Od007Refusal("graph transition cannot mutate the external bootstrap root")
        if self._records.get(record_id, (None, None))[0] == "governance":
            raise _Od007Refusal("ordinary transition cannot touch governance records")
        self._records[record_id] = ("domain", value)
        self._events.append(
            (
                "domain",
                (record_id, value, admitted_role),
            )
        )

    def consume_governance_event(
        self,
        record_id: str,
        value: object,
        actor: str,
        authority_source_identity: str,
        authority_additions: tuple[str, ...],
        admitted_role: str,
        governance_contract_identity: str,
    ) -> None:
        """Apply one abstract governance-path transition against prior state."""
        self._check_role(admitted_role, "GovernanceContract")
        if governance_contract_identity != self.governance_contract_identity:
            raise _Od007Refusal("GovernanceContract semantic change requires a new epoch")
        if actor not in self._authority_sources:
            raise _Od007Refusal("governance transition lacks pre-event authority")
        if authority_source_identity != self._authority_sources[actor]:
            raise _Od007Refusal("governance transition names the wrong prior authority")
        if record_id == self._bootstrap_source_identity:
            raise _Od007Refusal("graph transition cannot mutate the external bootstrap root")
        if authority_source_identity == record_id:
            raise _Od007Refusal("governance policy cannot authorize its own amendment")
        if self._bootstrap_actor in authority_additions:
            raise _Od007Refusal("governance event cannot replace external root binding")
        if any(added_actor in self._authority_sources for added_actor in authority_additions):
            raise AssertionError(
                "abstract D07 trace does not model authority-source replacement"
            )
        if self._records.get(record_id, (None, None))[0] == "domain":
            raise _Od007Refusal("governance transition cannot reclassify a domain record")
        self._records[record_id] = ("governance", value)
        for added_actor in authority_additions:
            self._authority_sources[added_actor] = record_id
        self._events.append(
            (
                "governance",
                (
                    record_id,
                    value,
                    actor,
                    authority_source_identity,
                    authority_additions,
                    admitted_role,
                    governance_contract_identity,
                ),
            )
        )


def _od007_state(graph: _Od007ReplayProjection) -> tuple[object, ...]:
    return (
        graph.governance_contract_identity,
        graph.composition_epoch_identity,
        graph._bootstrap_source_identity,
        tuple(sorted(graph._authority_sources.items())),
        tuple(sorted(graph._records.items())),
        tuple(graph._events),
    )


class _Od010Refusal(ValueError):
    pass


_Od010Record = tuple[str, str, str, tuple[str, ...]]
_Od010Admission = tuple[
    str,
    str,
    str,
    str,
    tuple[tuple[str, str], ...],
    tuple[tuple[str, str], ...],
    str | None,
]
_OD010_ROLE = "GovernedGraphContract"
_OD010_PARTITION = "domain"
_OD010_PARENTS = {
    "ArchiveExaminer": "Entity",
    "InquiryDossier": "Entity",
    "EvidenceFolio": "Entity",
    "EvidenceAttachment": "Entity",
    "Work": "Entity",
    "MixinCarrier": "Entity",
    "CitesFolioRelation": "Relation",
    "SealReviewEvent": "Event",
    "SealDiscrepancySignal": "Signal",
}
_OD010_MIXINS = {"MixinCarrier": {"EvidenceAttachment"}}


def _od010_obligation(
    record_id: str,
    record_type: str = "Work",
    *,
    role: str = _OD010_ROLE,
    partition: str = _OD010_PARTITION,
    refs: tuple[tuple[str, str], ...] = (),
    endpoints: tuple[tuple[str, str], ...] = (),
    bearer: str | None = None,
) -> _Od010Admission:
    """Build a test-only proof tuple, never a record, wire, or public API."""
    return record_id, record_type, role, partition, refs, endpoints, bearer


def _od010_is_subclass(actual: str, expected: str) -> bool:
    seen = set()
    while actual not in seen:
        if actual == expected:
            return True
        seen.add(actual)
        parent = _OD010_PARENTS.get(actual)
        if parent is None:
            return False
        actual = parent
    return False


def _od010_contextual_targets(
    *,
    class_valued: bool,
    inlined: bool,
    surviving_values: tuple[str, ...],
) -> tuple[str, ...]:
    """Classify already-shaped values without defining source or wire fields."""
    if not class_valued or inlined:
        return ()
    return surviving_values


def _od010_resolve(
    records: dict[str, _Od010Record],
    target_id: str,
    expected_type: str,
    role: str,
    partition: str,
) -> None:
    target = records.get(target_id)
    if target is None:
        raise _Od010Refusal("strong reference target is absent from visible state")
    target_type, target_role, target_partition, _ = target
    if target_role != role or target_partition != partition:
        raise _Od010Refusal("strong reference crosses role or partition")
    if not _od010_is_subclass(target_type, expected_type):
        raise _Od010Refusal("strong reference target does not satisfy class ancestry")


def _od010_admit_candidate(
    prestate: dict[str, _Od010Record],
    admissions: tuple[_Od010Admission, ...],
) -> dict[str, _Od010Record]:
    """Evaluate abstract proof obligations, never candidate or wire fields."""
    overlay = dict(prestate)
    for record_id, record_type, role, partition, refs, endpoints, bearer in admissions:
        if record_id in overlay:
            raise _Od010Refusal("record ID already exists in the global namespace")
        for target_id, expected_type in refs:
            _od010_resolve(overlay, target_id, expected_type, role, partition)
        for target_id, expected_type in endpoints:
            if not _od010_is_subclass(expected_type, "Entity"):
                raise _Od010Refusal("relation endpoint range is not Entity")
            _od010_resolve(overlay, target_id, expected_type, role, partition)
        if bearer is not None:
            target = overlay.get(bearer)
            if target is None:
                raise _Od010Refusal("signal bearer is absent from visible state")
            target_type, target_role, target_partition, _ = target
            if target_role != role or target_partition != partition:
                raise _Od010Refusal("signal bearer crosses role or partition")
            if not any(
                _od010_is_subclass(target_type, allowed)
                for allowed in ("Entity", "Relation")
            ):
                raise _Od010Refusal("signal bearer is not Entity or Relation")
        targets = tuple(
            target_id for target_id, _ in refs + endpoints
        ) + (() if bearer is None else (bearer,))
        overlay[record_id] = (record_type, role, partition, targets)
    return overlay


def _od010_select_temporal_view(
    records: dict[str, _Od010Record],
    visible_ids: frozenset[str],
) -> dict[str, _Od010Record]:
    if not visible_ids <= records.keys():
        raise _Od010Refusal("temporal view selects an absent record")
    for record_id in visible_ids:
        if any(target not in visible_ids for target in records[record_id][3]):
            raise _Od010Refusal("temporal view is not referentially closed")
    return {record_id: records[record_id] for record_id in sorted(visible_ids)}


def _copy_ledger(tmp_path: Path) -> Path:
    copied = tmp_path / "overseer"
    shutil.copytree(OVERSEER, copied)
    return copied


def _rewrite_entry(path: Path, mutate, *, rehash: bool) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    if rehash:
        value["entry_hash"] = entry_hash(value)
    path.write_text(canonical_json(value, indent=2) + "\n", encoding="utf-8")


def _reseal(root: Path) -> None:
    previous = "GENESIS"
    paths = sorted((root / "entries").glob("*.json"))
    for sequence, path in enumerate(paths, start=1):
        value = json.loads(path.read_text(encoding="utf-8"))
        value["sequence"] = sequence
        value["entry_id"] = f"OVR-{sequence:06d}"
        value["previous_entry_hash"] = previous
        value["entry_hash"] = entry_hash(value)
        path.write_text(canonical_json(value, indent=2) + "\n", encoding="utf-8")
        previous = value["entry_hash"]
    head = json.loads((root / "head.json").read_text(encoding="utf-8"))
    head.update(
        entry_count=len(paths),
        head_entry_id=f"OVR-{len(paths):06d}",
        head_hash=previous,
    )
    (root / "head.json").write_text(
        canonical_json(head, indent=2) + "\n",
        encoding="utf-8",
    )


def _append_correction(
    root: Path,
    *,
    target_id: str,
    actor_type: str,
    replacement_required: bool,
) -> str:
    paths = sorted((root / "entries").glob("*.json"))
    sequence = len(paths) + 1
    entry_id = f"OVR-{sequence:06d}"
    target = json.loads(
        (root / "entries" / f"{target_id}.json").read_text(encoding="utf-8")
    )
    prior = json.loads(paths[-1].read_text(encoding="utf-8"))["recorded_at"]
    recorded_at = (
        (
            datetime.fromisoformat(prior.removesuffix("Z") + "+00:00")
            + timedelta(minutes=1)
        )
        .isoformat()
        .replace("+00:00", "Z")
    )
    subject = target["subject"]
    references = [{"relation": "SUPERSEDES", "target": target_id, "type": "ENTRY"}]
    if subject["type"] != "PROGRAM":
        references.append(
            {"relation": "AFFECTS", "target": subject["id"], "type": subject["type"]}
        )
    entry = {
        "actor": {
            "id": "operator" if actor_type == "OPERATOR" else "overseer",
            "type": actor_type,
        },
        "data": {
            "affected_subject_ids": [subject["id"]],
            "replacement_required": replacement_required,
            "supersedes_entry_id": target_id,
        },
        "entry_hash": "sha256:" + "0" * 64,
        "entry_id": entry_id,
        "entry_type": "CORRECTION",
        "ledger": "overseer",
        "previous_entry_hash": "sha256:" + "0" * 64,
        "recorded_at": recorded_at,
        "references": references,
        "schema": "malleus.contract-compiler.ledger-entry/v1",
        "sequence": sequence,
        "subject": subject,
        "summary": f"Correct the recorded {subject['id']} entry.",
        "why": "Synthetic validation case for append-only correction authority.",
    }
    path = root / "entries" / f"{entry_id}.json"
    path.write_text(canonical_json(entry, indent=2) + "\n", encoding="utf-8")
    _reseal(root)
    return entry_id


def _append_replacement_workstream(root: Path, source_id: str) -> str:
    paths = sorted((root / "entries").glob("*.json"))
    sequence = len(paths) + 1
    entry_id = f"OVR-{sequence:06d}"
    source = json.loads(
        (root / "entries" / f"{source_id}.json").read_text(encoding="utf-8")
    )
    prior = json.loads(paths[-1].read_text(encoding="utf-8"))["recorded_at"]
    recorded_at = (
        (
            datetime.fromisoformat(prior.removesuffix("Z") + "+00:00")
            + timedelta(minutes=1)
        )
        .isoformat()
        .replace("+00:00", "Z")
    )
    source.update(
        entry_id=entry_id,
        sequence=sequence,
        recorded_at=recorded_at,
        summary="Replace the corrected workstream state.",
        why="Synthetic positive case for an active typed replacement.",
    )
    path = root / "entries" / f"{entry_id}.json"
    path.write_text(canonical_json(source, indent=2) + "\n", encoding="utf-8")
    _reseal(root)
    return entry_id


def _workflow_run_blocks(path: Path) -> list[str]:
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [
        step["run"]
        for job in workflow["jobs"].values()
        for step in job["steps"]
        if isinstance(step.get("run"), str)
    ]


def _workflow_commands(run_blocks: list[str]) -> list[list[str]]:
    return [
        shlex.split(line)
        for run_block in run_blocks
        for line in run_block.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def test_steady_state_workflows_do_not_revalidate_retained_overseer_evidence() -> None:
    plan = ci_plan("test")
    assert [command.name for command in plan] == [
        "quality",
        "tests",
        "compiler-tests",
        "ledger",
        "integration",
        "graph-recipe",
    ]
    commands_by_name = {command.name: command.argv for command in plan}
    assert commands_by_name["tests"][1:] == ("-m", "pytest")
    assert commands_by_name["ledger"][1:] == (
        "scripts/contract_compiler_ledger.py",
        "check",
    )
    assert all(
        "verify-evidence" not in argument
        for command in plan
        for argument in command.argv
    )
    for workflow in STEADY_STATE_WORKFLOWS:
        run_blocks = _workflow_run_blocks(workflow)
        assert all("verify-evidence" not in run_block for run_block in run_blocks)
        commands = _workflow_commands(run_blocks)
        assert ["python", "scripts/ci.py", "test", "--require-clean"] in commands


def test_cc002_integrated_candidate_binds_governed_checkpoint_lineage() -> None:
    card_source = CC002_CARD.read_bytes()
    card = json.loads(card_source)
    responsibility = card["responsibility"]
    assert CC002_LINEAGE_CONTRACT in responsibility
    assert "do not omit those paths from later candidate history" not in responsibility
    for checkpoint in CC002_CHECKPOINT_LINEAGE:
        assert responsibility.count(checkpoint) == 1

    resolved = [
        subprocess.run(
            ["git", "rev-parse", f"{checkpoint}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        for checkpoint in CC002_CHECKPOINT_LINEAGE
    ]
    assert resolved == list(CC002_CHECKPOINT_LINEAGE)
    for earlier, later in zip(resolved, resolved[1:], strict=False):
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", earlier, later],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        assert ancestry.returncode == 0, ancestry.stderr.decode(errors="replace")

    evidence_path = "conformance/contract_compiler/v0/evidence/CC-002.json"
    checkpoint_scopes = {
        scope["path"]
        for scope in card["scopes"]
        if scope["kind"] == "FILE" and scope["path"] != evidence_path
    }
    assert len(checkpoint_scopes) == 7
    changed_paths = {
        path
        for checkpoint in resolved
        for path in subprocess.run(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", checkpoint],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    }
    assert changed_paths == checkpoint_scopes

    candidate = card["candidate"]
    assert candidate["state"] == "INTEGRATED"
    completion = json.loads(
        (OVERSEER / "evidence" / "CC-002-completion.json").read_text(
            encoding="utf-8"
        )
    )
    assert completion["base_commit"] == candidate["head_commit"]
    worker_entries = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((CC002_CARD.parent / "ledger" / "entries").glob("*.json"))
    ]
    candidate_committed_at = datetime.fromisoformat(
        subprocess.run(
            ["git", "show", "-s", "--format=%cI", candidate["head_commit"]],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
    worker_recorded_at = [
        datetime.fromisoformat(
            entry["recorded_at"].removesuffix("Z") + "+00:00"
        )
        for entry in worker_entries
    ]
    completion_recorded_at = datetime.fromisoformat(
        completion["recorded_at"].removesuffix("Z") + "+00:00"
    )
    completion_revision = json.loads(
        (OVERSEER / "entries" / "OVR-000099.json").read_text(encoding="utf-8")
    )
    completion_fact = json.loads(
        (OVERSEER / "entries" / "OVR-000100.json").read_text(encoding="utf-8")
    )
    revision_recorded_at = datetime.fromisoformat(
        completion_revision["recorded_at"].removesuffix("Z") + "+00:00"
    )
    assert candidate_committed_at < worker_recorded_at[0]
    assert worker_recorded_at == sorted(worker_recorded_at)
    assert worker_recorded_at[-1] < completion_recorded_at
    assert completion_recorded_at < revision_recorded_at
    assert {
        entry["data"]["phase"]: entry["data"]["result"]
        for entry in worker_entries
        if entry["entry_type"] == "TDD_RESULT"
    } == {
        "RED": "EXPECTED_FAILURE",
        "GREEN": "PASS",
        "SLICE": "PASS",
        "DISPROOF": "PASS",
        "REGRESSION": "PASS",
        "PACKAGE": "NOT_APPLICABLE",
        "ATTEST": "PASS",
    }
    worker_tdd_check = next(
        check
        for check in completion["checks"]
        if check["check_id"] == "cc002-worker-tdd"
    )
    assert "PACKAGE not applicable" in worker_tdd_check["observed"]
    assert any(
        "PACKAGE not applicable" in claim for claim in completion_fact["data"]["claims"]
    )
    validate_candidate_history(
        ROOT,
        candidate,
        allowed_scopes=tuple(card["scopes"]),
        workstream_id="CC-002",
    )
    artifacts = {record["path"]: record for record in candidate["artifacts"]}
    retained_identity_paths = {
        "conformance/contract_compiler/v0/compiler_environment/manifest.json",
        "conformance/contract_compiler/v0/compiler_environment/requirements.lock",
        "conformance/contract_compiler/v0/compiler_environment/resolution-report.json",
        "conformance/contract_compiler/v0/compiler_environment/build-record.json",
        "conformance/contract_compiler/v0/compiler_environment/derivation-record.json",
        "conformance/contract_compiler/v0/compiler_environment/verification.json",
    }
    assert len(artifacts) == 13
    assert retained_identity_paths <= artifacts.keys()
    assert checkpoint_scopes <= artifacts.keys()
    for path in checkpoint_scopes:
        source = subprocess.run(
            ["git", "show", f"{candidate['head_commit']}:{path}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert artifacts[path] == {
            "byte_length": len(source),
            "path": path,
            "sha256": "sha256:" + hashlib.sha256(source).hexdigest(),
        }

    evidence_reference = next(
        record for record in candidate["evidence"] if record["path"] == evidence_path
    )
    evidence_source = subprocess.run(
        ["git", "show", f"{candidate['head_commit']}:{evidence_path}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    assert evidence_reference == {
        "byte_length": len(evidence_source),
        "path": evidence_path,
        "result": "PASS",
        "sha256": "sha256:" + hashlib.sha256(evidence_source).hexdigest(),
    }
    evidence = json.loads(evidence_source)
    lineage_limitation = next(
        limitation
        for limitation in evidence["limitations"]
        if "candidate range" in limitation.casefold()
    )
    assert all(
        checkpoint in lineage_limitation for checkpoint in CC002_CHECKPOINT_LINEAGE
    )
    assert any(
        check["result"] == "PASS"
        and all(
            checkpoint in canonical_json(check)
            for checkpoint in CC002_CHECKPOINT_LINEAGE
        )
        for check in evidence["checks"]
    )

    ledger = load_ledger(OVERSEER)
    superseded = {
        entry["data"]["supersedes_entry_id"]
        for entry in ledger.entries
        if entry["entry_type"] == "CORRECTION"
    }
    cc002_state = next(
        entry
        for entry in reversed(ledger.entries)
        if entry["entry_id"] not in superseded
        and entry["entry_type"] == "WORKSTREAM_STATE"
        and entry["data"]["workstream_id"] == "CC-002"
    )
    integration = json.loads(INTEGRATION.read_text(encoding="utf-8"))
    assert cc002_state["entry_id"] == "OVR-000101"
    assert cc002_state["data"]["new_state"] == "COMPLETE"
    assert card["ledger"]["state"] == "RECORDED"
    selected_integration = json.loads(
        subprocess.run(
            [
                "git",
                "show",
                f"{CC002_SELECTION_COMMIT}:design/contract_compiler/integration.json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    assert selected_integration["authority"]["overseer_ledger"] == {
        "entry_count": 101,
        "head_entry_id": "OVR-000101",
        "head_hash": "sha256:e0eaf379e6f5b708952d63510fa0a98b16b05f457304244ac4cec20501f51c4d",
        "path": "design/contract_compiler/overseer",
    }
    assert integration["selections"] == ["CC-000", "CC-001", "CC-X00", "CC-002"]
    row = next(
        item for item in integration["workstreams"] if item["workstream_id"] == "CC-002"
    )
    assert row["depends_on"] == ["CC-000", "CC-D12"]
    selection_positions = {
        workstream_id: position
        for position, workstream_id in enumerate(integration["selections"])
    }
    assert selection_positions["CC-000"] < selection_positions["CC-002"]
    assert "CC-D12" not in selection_positions
    assert row["card"] == {
        "byte_length": len(card_source),
        "path": "workstreams/CC-002/manifest.json",
        "sha256": "sha256:" + hashlib.sha256(card_source).hexdigest(),
        "state": "PRESENT",
    }
    assert card["authorization"]["dependency_bindings"] == [
        {
            "card_sha256": "sha256:4943b94cad90eeecac92944bd1bdca80618658b75744aec267bcbe13678f93b9",
            "completion_entry_hash": "sha256:d37f9eb77f572ee648f640171d9481800aaa6bc33f6f6553f21cd177188099b3",
            "completion_entry_id": "OVR-000016",
            "integrated_head": "09265cb4af2cec5ea8e1d3b063dce811952fcfe6",
            "workstream_id": "CC-000",
        },
        {
            "card_sha256": "sha256:46c8ee073c2d9537f512c579915ee49bc67c15d19c665c84df9d736deb9b3bd7",
            "completion_entry_hash": "sha256:089705dd93e3f892ae03a93896b44171f333e0d2cea0110c763d7f19a5f7795a",
            "completion_entry_id": "OVR-000084",
            "integrated_head": "d0eb42d42d5d4bd3f18d883eb26b2eb3806e2c72",
            "workstream_id": "CC-D12",
        },
    ]

    completion_commit = "1ae83e49ef1ae2432400978ffd77cde525719cbe"
    completion_tree = "3128b1d5155a0a71d7311f5c5b3968811c0bba4c"
    assert (
        subprocess.run(
            ["git", "rev-parse", f"{completion_commit}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        == completion_commit
    )
    assert (
        subprocess.run(
            ["git", "rev-parse", f"{completion_commit}^{{tree}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        == completion_tree
    )
    selection_report_path = OVERSEER / "evidence" / "CC-002.json"
    selection_report_source = subprocess.run(
        [
            "git",
            "show",
            f"{CC002_SELECTION_COMMIT}:design/contract_compiler/overseer/evidence/CC-002.json",
        ],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    assert selection_report_path.read_bytes() == selection_report_source
    selection_report = json.loads(selection_report_source)
    for artifact in selection_report["artifacts"]:
        source = subprocess.run(
            ["git", "show", f"{CC002_SELECTION_COMMIT}:{artifact['path']}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert artifact["byte_length"] == len(source)
        assert artifact["sha256"] == "sha256:" + hashlib.sha256(source).hexdigest()
    assert selection_report["base_commit"] == completion_commit
    selection_claims = canonical_json(selection_report)
    assert completion_commit in selection_claims
    assert completion_tree in selection_claims
    completion_committed_at = datetime.fromisoformat(
        subprocess.run(
            ["git", "show", "-s", "--format=%cI", completion_commit],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
    selection_recorded_at = datetime.fromisoformat(
        selection_report["recorded_at"].removesuffix("Z") + "+00:00"
    )
    assert completion_committed_at < selection_recorded_at

    selection_revision = next(
        entry for entry in ledger.entries if entry["entry_id"] == "OVR-000102"
    )
    assert selection_revision["entry_id"] == "OVR-000102"
    assert selection_revision["entry_type"] == "DOCUMENT_REVISION"
    selection_fact = next(
        entry for entry in ledger.entries if entry["entry_id"] == "OVR-000103"
    )
    assert selection_fact["entry_id"] == "OVR-000103"
    assert selection_fact["entry_type"] == "VERIFIED_FACT"
    selection_revision_at = datetime.fromisoformat(
        selection_revision["recorded_at"].removesuffix("Z") + "+00:00"
    )
    selection_fact_at = datetime.fromisoformat(
        selection_fact["recorded_at"].removesuffix("Z") + "+00:00"
    )
    assert selection_recorded_at < selection_revision_at < selection_fact_at
    selection_entries = [
        entry
        for entry in ledger.entries
        if selection_revision["sequence"]
        <= entry["sequence"]
        <= selection_fact["sequence"]
    ]
    assert [entry["entry_id"] for entry in selection_entries] == [
        "OVR-000102",
        "OVR-000103",
    ]
    assert all(
        entry["entry_type"] != "WORKSTREAM_STATE" for entry in selection_entries
    )
    assert {
        "relation": "EVIDENCES",
        "target": completion_commit,
        "type": "COMMIT",
    } in selection_fact["references"]


def test_ccd12_r3_exact_wheel_derivation_authority_is_active() -> None:
    state = load_ledger(OVERSEER)
    active_corrections = [
        entry for entry in state.entries if entry["entry_type"] == "CORRECTION"
    ]
    superseded = {entry["data"]["supersedes_entry_id"] for entry in active_corrections}
    assert {
        "OVR-000050",
        "OVR-000053",
        "OVR-000054",
        "OVR-000061",
        "OVR-000064",
        "OVR-000065",
        "OVR-000072",
        "OVR-000075",
        "OVR-000076",
    } <= superseded
    for target in (
        "OVR-000050",
        "OVR-000053",
        "OVR-000054",
        "OVR-000061",
        "OVR-000064",
        "OVR-000065",
        "OVR-000072",
        "OVR-000075",
        "OVR-000076",
    ):
        correction = next(
            entry
            for entry in active_corrections
            if entry["data"]["supersedes_entry_id"] == target
        )
        assert correction["data"]["replacement_required"] is True
    decision_correction = next(
        entry
        for entry in active_corrections
        if entry["data"]["supersedes_entry_id"] == "OVR-000072"
    )
    assert decision_correction["actor"] == {"id": "operator", "type": "OPERATOR"}

    active_entries = [
        entry for entry in state.entries if entry["entry_id"] not in superseded
    ]
    decision = next(
        entry
        for entry in reversed(active_entries)
        if entry["entry_type"] == "DECISION"
        and entry["data"]["decision_id"] == "OD-012"
    )
    assert decision["entry_id"] == "OVR-000097"
    assert decision["actor"] == {"id": "operator", "type": "OPERATOR"}
    assert decision["data"]["supersedes_entry_id"] == "OVR-000081"
    assert decision["data"]["selected_option"] == (
        "Internal provisional CC-002 use of one exact embedded CFGraph 0.2.1 wheel"
    )
    assert decision["data"]["canonical_record_uris"] == []
    assert decision["data"]["satisfies_workstreams"] == ["CC-002"]
    assert {
        (reference["relation"], reference["type"], reference["target"])
        for reference in decision["references"]
    } >= {
        ("EVIDENCES", "ENTRY", "OVR-000081"),
        ("EVIDENCES", "ENTRY", "OVR-000093"),
        ("EVIDENCES", "ENTRY", "OVR-000095"),
        ("SATISFIES", "WORKSTREAM", "CC-002"),
    }

    exception_policy = canonical_json(decision["data"]).casefold()
    for required in (
        "cfgraph-0.2.1-py3-none-any.whl",
        "2256 bytes",
        "sha256:28a5bc1292af3c7de137c500da2f9607d66ed27fe787f15ce33e5698fa828f13",
        "name: cfgraph",
        "version: 0.2.1",
        "requires-dist: rdflib>=0.4.2",
        "generator: setuptools 83.0.0",
        "internal, non-release",
        "exact bytes and selected semantics fail closed",
        "wheel-only offline closure",
        "behavior smoke",
        "no reproducible-build",
        "license-sufficiency",
        "security",
        "vulnerability",
        "distribution",
        "public-release claim",
    ):
        assert required in exception_policy
    for deferred in (
        "deterministic double-build from exact source in the selected container",
        "authoritative license and notice bytes",
        "release-grade supply-chain, security, and vulnerability attestation",
        "retire this exception before any public or external release",
    ):
        assert deferred in exception_policy

    r3_refinement = next(
        entry for entry in state.entries if entry["entry_id"] == "OVR-000081"
    )
    assert r3_refinement["data"]["supersedes_entry_id"] == "OVR-000072"
    base_decision = next(
        entry for entry in state.entries if entry["entry_id"] == "OVR-000072"
    )
    policy = canonical_json(
        [base_decision["data"], r3_refinement["data"]]
    ).casefold()
    for required in (
        "antlr4-python3-runtime-4.9.3.tar.gz",
        "117034",
        "f224469b4168294902bb1efa80a8bf7855f24c99aef99cbefc1bcd3cce77881b",
        "https://files.pythonhosted.org/packages/3e/38/7859ff46355f76f8d19459005ca000b6e7012f2f1ca597746cbcd1fbfe5e/antlr4-python3-runtime-4.9.3.tar.gz",
        "setuptools-83.0.0-py3-none-any.whl",
        "1008090",
        "29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3",
        "https://files.pythonhosted.org/packages/5d/40/e1e72872c6354b306daef1703549e8e83b4d43cfea356311bf722a043752/setuptools-83.0.0-py3-none-any.whl",
        "source_date_epoch=315532800",
        "setuptools.build_meta:__legacy__",
        "two fresh",
        "byte-identical",
        "network denied",
        "wheel-only",
        "not rebuilt",
        "prefixcommons-0.1.12-py3-none-any.whl",
        "29482",
        "16dbc0a1f775e003c724f19a694fcfa3174608f5c8b0e893d494cf8098ac7f8b",
        "https://files.pythonhosted.org/packages/31/e8/715b09df3dab02b07809d812042dc47a46236b5603d9d3a2572dbd1d8a97/prefixcommons-0.1.12-py3-none-any.whl",
        "0.1.12+malleus.1",
        "requires-dist: pytest-logging (>=2015.11.4,<2016.0.0)",
        "pytest-logging>=2015.11.4,<2016.0.0",
        "14 members",
        "109044 expanded bytes",
        "ten package code or data",
        "1500-byte",
        "3a9b5b0d46996cdfd82b65429e189904e4ab1908014ce408cbecde9f591f37b4",
        "1960 bytes",
        "4c6cf90de54fa4ce46d1235551f75c021bacab34b8c9894fd50a8096441a5303",
        "83 bytes",
        "cb778389a15548d4cf6e0cdf367d27627e6d127d5c5fa5ab75eb43950338c56c",
        "generator: poetry 1.0.7",
        "every package code, resource, and license payload byte exactly",
        "generator: malleus-cc002 (wheel-derivation-v1)",
        "zip_stored",
        "two fresh",
        "stdlib-only",
        "derivative-inputs/prefixcommons-0.1.12-py3-none-any.whl",
        "prefixcommons-0.1.12+malleus.1-py3-none-any.whl",
        "/built/prefixcommons-0.1.12+malleus.1-py3-none-any.whl",
        "retain the derived wheel under built/",
        "build-record.json",
        "derivation-record.json",
        "malleus.cc002.wheel-derivation/v1",
        "malleus.cc002.acquire-result/v3",
        "malleus.cc002.verify-result/v3",
        "malleus.cc002.compiler-environment/v3",
        "malleus.cc002.internal-verification/v3",
        "malleus.cc002.container-verification/v1",
        "malleus.cc002.source-build/v1",
        "retain malleus.cc002.container-verification/v1 and malleus.cc002.source-build/v1 unchanged",
        "derivation_record_sha256",
        "eight retained inputs",
        "two produced artifacts",
        "1980-01-01 00:00:00",
        "unix create-system identity",
        "regular-file mode 0644",
        "empty archive/member comments and extra fields",
        "record is generated from the final member payloads and names",
        "its own hash/size cells stay empty",
        "never imports, extracts, or executes prefixcommons",
        "validate the exact input record",
        "exact whole-wheel identity",
        "duplicate/unsafe member names",
        "non-regular member types",
        "bsd 3-clause license",
        "no separate extracted license file",
        "direct resolver input",
        "official prefixcommons wheel absent",
        "pip check",
        "go:0008150",
        "http://purl.obolibrary.org/obo/go_0008150",
        "strict mode",
        "exactly [go:0008150]",
        "linkml_runtime.utils.namespaces.namespaces",
        "https://example.org/",
        "ex:item",
        "pytest, pytest-logging, and py",
        "maintenance and security review",
        "non-allowlisted payload change",
        "license loss",
        "unequal transform",
        "resolver substitution",
        "smoke that requires the removed plugin",
    ):
        assert required in policy

    refinement_policy = canonical_json(r3_refinement["data"]).casefold()
    for required in (
        "ovr-000072 unchanged",
        "ascending unicode code point",
        "final posix member names",
        "including the record member and its row",
        "every final zip filename is ascii",
        "utf-8 without bom",
        "exactly three fields",
        "comma delimiter",
        "ascii double-quote quotechar",
        "doublequote true",
        "quote_minimal",
        "no escapechar",
        "lf line terminator",
        "terminal lf",
        "url-safe base64 of the raw sha-256 digest",
        "without '=' padding",
        "decimal byte length",
        "record row's own hash and size fields empty",
        "date_time to 1980-01-01 00:00:00",
        "compress_type to zip_stored",
        "create_system=3",
        "create_version=20",
        "extract_version=20",
        "reserved=0",
        "flag_bits=0",
        "volume=0",
        "internal_attr=0",
        "external_attr=(0o100644 << 16)",
        "extra/comment empty",
        "archive comment empty",
        "disable zip64",
        "reject every input or output requiring it",
        "crc32, compressed and uncompressed sizes, and local-header offsets",
        "consequences of the exact payloads and member order",
        "set every selected record, zipinfo, and archive field explicitly",
        "reopen the written wheel and validate every selected field and byte",
        "must not rely on cpython defaults",
        "https://packaging.python.org/en/latest/specifications/recording-installed-packages/",
        "https://docs.python.org/3.12/library/zipfile.html",
        "complete canonical grammar above is a malleus choice",
        "do not claim those sources mandate every selected value",
    ):
        assert required in refinement_policy

    workstream_states = {
        entry["data"]["workstream_id"]: entry
        for entry in active_entries
        if entry["entry_type"] == "WORKSTREAM_STATE"
    }
    ccd12 = workstream_states["CC-D12"]
    cc002 = workstream_states["CC-002"]
    assert ccd12["entry_id"] != "OVR-000053"
    assert ccd12["data"]["new_state"] == "COMPLETE"
    assert cc002["entry_id"] != "OVR-000054"
    assert cc002["entry_id"] == "OVR-000101"
    assert cc002["data"]["new_state"] == "COMPLETE"

    card = json.loads(CC002_CARD.read_text(encoding="utf-8"))
    binding = next(
        item
        for item in card["authorization"]["dependency_bindings"]
        if item["workstream_id"] == "CC-D12"
    )
    assert binding["completion_entry_id"] == ccd12["entry_id"]
    assert binding["completion_entry_hash"] == ccd12["entry_hash"]
    responsibility = card["responsibility"].casefold()
    for required in (
        "malleus.cc002.acquire-result/v4",
        "malleus.cc002.verify-result/v4",
        "malleus.cc002.compiler-environment/v4",
        "malleus.cc002.internal-verification/v4",
        "nine governed inputs",
        "two produced artifacts",
        "406 adapter tests",
        "74 governance tests",
        "internal, non-release",
        "cfgraph-0.2.1-py3-none-any.whl",
        "sha256:28a5bc1292af3c7de137c500da2f9607d66ed27fe787f15ce33e5698fa828f13",
        "retire the exception before public or external release",
    ):
        assert required in responsibility
    for obsolete in (
        "malleus.cc002.acquire-result/v3",
        "malleus.cc002.verify-result/v3",
        "formal cfgraph gate",
        "keep candidate state none",
        "ledger state not_started",
    ):
        assert obsolete not in responsibility

    for relative in HISTORICAL_CCD12_PATHS:
        historical = subprocess.run(
            ["git", "show", f"{GOVERNANCE_BASE_COMMIT}:{relative}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert (ROOT / relative).read_bytes() == historical
    for relative in HISTORICAL_R3_PATHS:
        historical = subprocess.run(
            ["git", "show", f"{R3_GOVERNANCE_BASE_COMMIT}:{relative}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert (ROOT / relative).read_bytes() == historical
    for relative, expected in IMMUTABLE_R3_REFINEMENT_INPUTS.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_revision_23_graph_is_generated_from_all_turtle_projections() -> None:
    blocks = [
        token.content
        for path in FOUNDATION_PROJECTIONS
        for token in MarkdownIt("commonmark").parse(path.read_text(encoding="utf-8"))
        if token.type == "fence" and token.info.strip() == "turtle"
    ]
    assert len(blocks) == 29
    canonical_path = ROOT / "design" / "PROTOCOL_FOUNDATION_GRAPH.ttl"
    source = canonical_path.read_bytes()
    body = [
        line
        for line in source.decode("utf-8").splitlines()
        if line and not line.startswith("#")
    ]
    projected = Graph().parse(data="\n".join(blocks), format="turtle")
    canonical = Graph().parse(data=source, format="nt")
    assert set(projected) == set(canonical)
    assert len(canonical) == 1852

    digest = hashlib.sha256(source).hexdigest()
    assert source.decode("utf-8").splitlines()[:9] == [
        "# Canonical Malleus protocol foundation design graph.",
        "#",
        "# Design graph revision: 23",
        "# Evidence cutoff: 2026-09-01",
        "# Authority: candidate and accepted design states recorded by author decisions.",
        "# Shipped capability remains controlled by src/malleus/status.py and tests.",
        "#",
        "# The Markdown tuple blocks are explanatory projections of this graph.",
        "# Semantic changes create new object revisions and supersedes edges.",
    ]
    marker = (
        "Canonical design graph: "
        "[`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl),"
    )
    for path in FOUNDATION_PROJECTIONS:
        lines = path.read_text(encoding="utf-8").splitlines()
        index = lines.index(marker)
        assert lines[index : index + 3] == [
            marker,
            "revision 23,",
            f"`sha256:{digest}`",
        ]
    assert body == sorted(set(body))

    cc = "https://malleus.dev/contract-compiler/"
    mfg = "https://malleus.dev/foundation-graph/"
    okg = "https://malleus.dev/ontology-kg-realization/"
    selects = URIRef(f"{mfg}selects")
    decision_date = URIRef(f"{mfg}decisionDate")
    assert set(canonical.objects(URIRef(f"{cc}OD-012"), decision_date)) == {
        Literal("2026-08-25")
    }
    assert set(canonical.objects(URIRef(f"{cc}OD-012"), selects)) == {
        URIRef(f"{mfg}LinkMLV1_11_1ReleaseCompilerBaselineR3")
    }
    accepted = {
        "OD-002": "ExactSlotOnlyExplicitAdoptionProfile",
        "OD-003": "LinkML1_11_1ReplaceableDefaultFrontendAdapterProfile",
        "OD-004": "TypedPersistedWireEpochHardBreakProfile",
        "OD-005": "AtomicOntologyPoweredCanonicalFactContract",
        "OD-006": "ThreeRoleClosedContractCompositionProfile",
        "OD-008": "MalleusLinkMLSupportProfileV0",
        "OD-011": "ExplicitSingleResolverProfileSelection",
        "OD-013": "SingleDistributionCompilerIncludedPackagingTopology",
        "OD-014": "QuietBellArchiveFixturePublicationBoundary",
    }
    for decision, selected in accepted.items():
        subject = URIRef(f"{cc}{decision}")
        assert set(canonical.objects(subject, decision_date)) == {
            Literal("2026-08-26")
        }
        assert set(canonical.objects(subject, selects)) == {URIRef(f"{mfg}{selected}")}
    od007 = URIRef(f"{cc}OD-007")
    assert set(canonical.objects(od007, decision_date)) == {Literal("2026-08-27")}
    assert set(canonical.objects(od007, selects)) == {
        URIRef(f"{mfg}ProtectedReplayDerivedGovernancePartitionTopologyV0")
    }
    od010 = URIRef(f"{cc}OD-010")
    assert set(canonical.objects(od010, decision_date)) == {Literal("2026-08-27")}
    assert set(canonical.objects(od010, selects)) == {
        URIRef(f"{mfg}StrongLocalContextualReferenceAdmissionProfileV0")
    }
    od015 = URIRef(f"{cc}OD-015")
    architecture = URIRef(f"{mfg}ExecutorOnlyProtocolMachineArchitecture")
    assert set(canonical.objects(od015, decision_date)) == {
        Literal("2026-08-31")
    }
    assert set(canonical.objects(od015, selects)) == {architecture}
    od016 = URIRef(f"{cc}OD-016")
    kcs_architecture = URIRef(f"{mfg}SingleLedgerKnowledgeChangeSetArchitecture")
    assert set(canonical.objects(od016, decision_date)) == {
        Literal("2026-09-01")
    }
    assert set(canonical.objects(od016, selects)) == {kcs_architecture}
    rdf_type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    status = URIRef(f"{mfg}status")
    decided_by = URIRef(f"{mfg}decidedBy")
    od008 = URIRef(f"{cc}OD-008")
    assert set(canonical.objects(od008, rdf_type)) == {
        URIRef(f"{mfg}DecisionRecord")
    }
    assert set(canonical.objects(od008, decided_by)) == {URIRef(f"{mfg}Author")}
    assert set(canonical.objects(od008, status)) == {URIRef(f"{mfg}AcceptedDesign")}
    assert set(canonical.objects(od007, rdf_type)) == {
        URIRef(f"{mfg}DecisionRecord")
    }
    assert set(canonical.objects(od007, decided_by)) == {URIRef(f"{mfg}Author")}
    assert set(canonical.objects(od007, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }
    assert set(canonical.objects(od010, rdf_type)) == {
        URIRef(f"{mfg}DecisionRecord")
    }
    assert set(canonical.objects(od010, decided_by)) == {URIRef(f"{mfg}Author")}
    assert set(canonical.objects(od010, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }
    assert set(canonical.objects(od015, rdf_type)) == {
        URIRef(f"{mfg}DecisionRecord")
    }
    assert set(canonical.objects(od015, decided_by)) == {URIRef(f"{mfg}Author")}
    assert set(canonical.objects(od015, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }
    assert set(canonical.objects(od016, rdf_type)) == {
        URIRef(f"{mfg}DecisionRecord")
    }
    assert set(canonical.objects(od016, decided_by)) == {URIRef(f"{mfg}Author")}
    assert set(canonical.objects(od016, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }
    assert set(canonical.objects(kcs_architecture, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }
    assert set(canonical.objects(architecture, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }
    composed_of = URIRef(f"{mfg}composedOf")
    implements = URIRef(f"{mfg}implements")
    assert set(
        canonical.objects(URIRef(f"{mfg}NormativeAdmissionProfile"), composed_of)
    ) == {URIRef(f"{mfg}ProtocolMachineProgram")}
    assert set(
        canonical.objects(URIRef(f"{mfg}ProtocolMachineProgram"), composed_of)
    ) == {URIRef(f"{mfg}AdmissionRuleSet")}
    assert set(
        canonical.objects(URIRef(f"{mfg}AdmissionImplementation"), implements)
    ) == {URIRef(f"{mfg}ProtocolMachineInterpreterContract")}
    for node in ("ProtocolMachineProgram", "PolicyProgram", "ProjectionProgram"):
        subject = URIRef(f"{mfg}{node}")
        assert set(canonical.objects(subject, rdf_type)) == {
            URIRef("http://www.w3.org/2000/01/rdf-schema#Class")
        }
        assert set(canonical.objects(subject, status)) == {URIRef(f"{mfg}Candidate")}

    okg_d013 = URIRef(f"{okg}OKG-D013")
    okg_fx001 = URIRef(f"{okg}OKG-FX001")
    architecture = URIRef(
        f"{okg}DeterministicCompilerOptionalProposalProducerArchitecture"
    )
    assert set(canonical.objects(okg_d013, rdf_type)) == {
        URIRef(f"{mfg}DecisionRecord")
    }
    assert set(canonical.objects(okg_d013, decided_by)) == {URIRef(f"{mfg}Author")}
    assert set(canonical.objects(okg_d013, decision_date)) == {
        Literal("2026-08-28")
    }
    assert set(canonical.objects(okg_d013, selects)) == {okg_fx001}
    assert set(canonical.objects(okg_d013, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }
    assert set(canonical.objects(okg_fx001, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }
    assert set(canonical.objects(architecture, status)) == {
        URIRef(f"{mfg}AcceptedDesign")
    }

    od008_node_types = {
        "MalleusLinkMLSupportProfileV0": "SupportProfile",
        "FlatExactlyOneExpressionExtensionV0": "ContractMetamodel",
        "ExpressionCapableContractMetamodelV0": "ContractMetamodel",
        "ExactlyOneGroupFactRule": "Boundary",
        "ExactlyOneAlternativeFactRule": "Boundary",
        "SlotConditionFactRule": "Boundary",
        "FlatExactlyOneWholeSetInvariant": "Invariant",
        "ClosedSeedExpressionRuleUnionCompositionV0": "Boundary",
        "ClosedExactLocationClassificationV0": "Boundary",
        "StrictJSONShapedYAMLSourceGrammarV0": "SupportProfile",
        "TrustedLinkML1_11_1SevenBuiltinMapV0": "SupportProfile",
        "LinkML1_11_1ElaborationAndDefaultProfileV0": "SupportProfile",
        "LosslessSourceDeclarationAndProvenanceProfileV0": "Boundary",
        "LinkMLV0SlashQualifiedSymbolPolicy": "SymbolIdentityPolicy",
        "RetainedCorpusWholeSourceClosureV0": "Boundary",
        "FrontendAdapterConstructionInjectionDeferredBoundary": "Boundary",
        "NoGeneralLinkMLSupportClaimBoundary": "Boundary",
        "StablePublicFactIdentityStillOD009Boundary": "Boundary",
        "PublicCompilerPromotionStillOD009Boundary": "Boundary",
    }
    od007_node_types = {
        "ProtectedReplayDerivedGovernancePartitionTopologyV0": "DesignObject",
        "ProtocolLedgerSoleWriteAuthorityBoundary": "Boundary",
        "NoSeparateGovernanceGraphHeadSnapshotDigestSynchronizationOrQueryBoundary": "Boundary",
        "GovernanceMembershipAdmissionPathOnlyNoCallerTypeNameNamespaceOrStorageInferenceBoundary": "Boundary",
        "PriorAuthoritySingleExternalRootNoSameEventOrDirectPolicySelfAmendmentFollowingEventVisibilityBoundary": "Boundary",
        "OrdinaryPathCannotDirectlyMutateGovernanceIdentityBoundary": "Boundary",
        "SameGovernanceContractPolicyUpdateSameEpochSemanticContractChangeNewEpochBoundary": "Boundary",
        "GovernanceRepresentationAndD10SemanticsDeferredBoundary": "Boundary",
        "ProtectedWriteAdmissionNotReadConfidentialityBoundary": "Boundary",
        "GovernanceTopologyQuestionR2": "OpenQuestion",
    }
    od010_node_types = {
        "StrongLocalContextualReferenceAdmissionProfileV0": "NormativeAdmissionProfile",
        "SurvivingNonInlinedClassValuesStrongReferenceBoundary": "Boundary",
        "ClassOrSubclassTargetNoMixinOnlyMatchBoundary": "Boundary",
        "SameRoleSamePartitionNoRegistryFactBorrowingBoundary": "Boundary",
        "AcceptedPrestateEarlierOrderedWritesWholeCandidateAtomicNoRuntimeSortBoundary": "Boundary",
        "EntityOnlyRelationEndpointsEntityOrRelationSignalBearersBoundary": "Boundary",
        "GlobalRecordIDNamespaceReferentiallyClosedTemporalViewsBoundary": "Boundary",
        "InlinedValuesAndPrimitiveIDHashScalarsNotContextualReferencesBoundary": "Boundary",
        "NoCascadeRepairDeletionMigrationReadAccessOrImplementationBoundary": "Boundary",
        "GovernanceRepresentationAndReadPolicyRemainDeferredAfterOD010Boundary": "Boundary",
    }
    for node, node_type in (
        od008_node_types | od007_node_types | od010_node_types
    ).items():
        subject = URIRef(f"{mfg}{node}")
        assert set(canonical.objects(subject, rdf_type)) == {
            URIRef(f"{mfg}{node_type}")
        }
        assert set(canonical.objects(subject, status)) == {
            URIRef(f"{mfg}AcceptedDesign")
        }
    binds = URIRef(f"{mfg}binds")
    assert {
        str(value).removeprefix(okg)
        for value in canonical.objects(architecture, binds)
    } == {
        "DeterministicCompilerExactOutputOrTypedRefusalBoundary",
        "OntologyBuilderCorrectorOutsideTrustedCompilerBoundary",
        "OntologyBuilderCorrectorProtocolReviewBoundary",
        "ReplayNeverCallsOntologyBuilderCorrectorBoundary",
    }
    required_bindings = {
        "SingleLedgerKnowledgeChangeSetArchitecture": {
            "OneAuthoritativeSemanticHistoryBoundary",
            "ReplayDerivedAcceptedTemporalGraphOnlyBoundary",
            "RetainedGenesisKnowledgeChangeSetBoundary",
            "LifecycleSharedKnowledgeChangeSetIdentityBoundary",
            "MachineEffectsAdmitKnowledgeChangeSetOnlyBoundary",
            "NoIndependentAcceptedGraphMutationBoundary",
            "TransitionLocalOperationDependencyPlanBoundary",
            "PersistedStructuralCandidateNonGovernedBoundary",
            "AtomicAcceptApplicationEventBoundary",
            "CrossContractKnowledgeChangeSetMigrationFutureBoundary",
        },
        "ExecutorOnlyProtocolMachineArchitecture": {
            "StrictNeutralContractIRBoundary",
            "StrictProtocolMachineIRBoundary",
            "SeparateExactIdentityPolicyAndProjectionProgramsBoundary",
            "GenericInterpreterNoProtocolAuthorityBoundary",
            "NoArbitraryCodeEscapeHatchBoundary",
            "CrossImplementationReplayParityBoundary",
        },
        "ExactSlotOnlyExplicitAdoptionProfile": {
            "SlotDeclarationsOnlyAdoptionBoundary",
            "LiteralBooleanAdoptsTrueRequiredBoundary",
            "ImportedAncestorOwnerAuthoritativeBoundary",
            "ExactTypedSourceStructureBeforeDefaultsBoundary",
            "RemoveOnlyDescriptionAdoptsAndEmptyAnnotationsComparisonBoundary",
            "AdoptionDifferenceOrInvalidMarkerRefusalBoundary",
            "SourceOrderNeverCompositionWinnerBoundary",
        },
        "LinkML1_11_1ReplaceableDefaultFrontendAdapterProfile": {
            "ReplaceableAdapterNeutralOutputContract",
            "GenericNeutralResultConformanceBoundary",
            "SourceLanguageSpecificNamedVersionedProfileAndCorpusBoundary",
            "LinkMLCorpusOnlyForLinkMLCompatibilityClaimBoundary",
            "NamedVersionedAdapterSupportAndDefaultProfileBoundary",
            "AppliedDefaultsExplicitWithProvenanceBoundary",
            "RuntimeNeverInfersFrontendDefaultsBoundary",
            "NoLegacyOntologyRegistryEmulationV0Boundary",
            "CCX01SimpleParityEqual",
            "CCX01ParentMixinPrecedenceLinkML",
            "CCX01RepeatedMixinRefused",
            "CCX01ConflictingMixinsABRefused",
            "CCX01ConflictingMixinsBARefused",
            "CCX01NumericBoundsLinkML",
            "CCX01ExplicitFalseEqual",
            "CCX01DefaultRangeLinkMLExplicit",
            "CCX01AttributeSlotUsageLinkML",
        },
        "TypedPersistedWireEpochHardBreakProfile": {
            "PersistedWireEpochCheckedBeforeSemanticDecodeBoundary",
            "ExactPublicDiagnosticIdentifierDeferredToCCW01Boundary",
            "LegacyOntologyHashNeverReinterpretedBoundary",
            "NoPersistedWireFallbackReceiptMigrationTranslationOrRewriteBoundary",
            "ReconProjectTypedHardBreak",
            "ReconRecordTypedHardBreak",
            "KnowledgeGraphSnapshotTypedHardBreak",
            "ProtocolEnvelopeTypedHardBreakBeforeReplay",
            "EmbeddedGraphBaseAndCandidateNotReached",
        },
        "AtomicOntologyPoweredCanonicalFactContract": {
            "ExactNonExpressionSeedContractMetamodel",
            "AtomicCanonicalJSONFactProfileV0",
            "AbsoluteIdentifierExactUnicodeSymbolPolicyV0",
            "LinkMLV0SlashQualifiedSymbolPolicy",
            "ContractMetamodelSemanticAuthorityOverJSONBoundary",
            "ClosedThreeMemberCanonicalJSONFactWireBoundary",
            "CanonicalDecimalLexicalNumericObjectBoundary",
            "InternalCandidateDigestNotPublicIdentityBoundary",
            "StructuralIdentityAndExternalProvenanceBoundary",
            "FrontendDirectFactConformanceOnlyParityBoundary",
            "ExactSeedMetamodelBootstrapTrustBoundary",
            "ExpressionCapableContractMetamodelV0",
            "AdmissionArtifactBundleAndPromotionSeparateAuthorityBoundary",
            "NoGenericDefaultValueOrRuntimeDefaultBoundary",
        },
        "ThreeRoleClosedContractCompositionProfile": {
            "ExactThreeNamedRoleCardinalityBoundary",
            "RoleBoundIdentityDomainSeparationBoundary",
            "CompleteRoleClosureNoAmbientBorrowingBoundary",
            "ClosedCompositionIdentityBoundary",
            "OneAcceptedTemporalCompositionEpochV0Boundary",
            "StandaloneStructuralGraphGovernedRoleOnlyBoundary",
            "OneArtifactMayPackageThreeRolesBoundary",
            "IndependentRoleHeadsAndRecoveryDeferredBoundary",
            "ArtifactBundleAndWireGrammarDeferredBoundary",
            "StablePublicFactIdentityStillOD009Boundary",
        },
        "ExactNonExpressionSeedContractMetamodel": {
            "ExactClassSeedFactRule",
            "ExactSlotAndSlotUseSeedFactRule",
            "ExactEnumSeedFactRule",
            "ExactScalarAndSeedPrimitiveFactRule",
            "ExactWholeSetSeedFactInvariant",
            "SourceToFactCompletenessSeparateConformanceBoundary",
        },
        "FlatExactlyOneExpressionExtensionV0": {
            "ExactlyOneGroupFactRule",
            "ExactlyOneAlternativeFactRule",
            "SlotConditionFactRule",
            "FlatExactlyOneWholeSetInvariant",
        },
        "ExpressionCapableContractMetamodelV0": {
            "ExactNonExpressionSeedContractMetamodel",
            "FlatExactlyOneExpressionExtensionV0",
            "ClosedSeedExpressionRuleUnionCompositionV0",
        },
        "MalleusLinkMLSupportProfileV0": {
            "ClosedExactLocationClassificationV0",
            "StrictJSONShapedYAMLSourceGrammarV0",
            "TrustedLinkML1_11_1SevenBuiltinMapV0",
            "LinkML1_11_1ElaborationAndDefaultProfileV0",
            "LosslessSourceDeclarationAndProvenanceProfileV0",
            "LinkMLV0SlashQualifiedSymbolPolicy",
            "ExpressionCapableContractMetamodelV0",
            "RetainedCorpusWholeSourceClosureV0",
            "FrontendAdapterConstructionInjectionDeferredBoundary",
            "NoGeneralLinkMLSupportClaimBoundary",
            "StablePublicFactIdentityStillOD009Boundary",
            "PublicCompilerPromotionStillOD009Boundary",
        },
        "ProtectedReplayDerivedGovernancePartitionTopologyV0": {
            "AcceptedTemporalGraphVersion",
            "AcceptedTemporalGraphVersionHash",
            "GovernedGraphContract",
            "GovernanceContract",
            "GovernanceBootstrap",
            "ProtocolLedgerSoleWriteAuthorityBoundary",
            "NoSeparateGovernanceGraphHeadSnapshotDigestSynchronizationOrQueryBoundary",
            "GovernanceMembershipAdmissionPathOnlyNoCallerTypeNameNamespaceOrStorageInferenceBoundary",
            "PriorAuthoritySingleExternalRootNoSameEventOrDirectPolicySelfAmendmentFollowingEventVisibilityBoundary",
            "OrdinaryPathCannotDirectlyMutateGovernanceIdentityBoundary",
            "SameGovernanceContractPolicyUpdateSameEpochSemanticContractChangeNewEpochBoundary",
            "StandaloneStructuralGraphGovernedRoleOnlyBoundary",
            "GovernanceRepresentationAndD10SemanticsDeferredBoundary",
            "ProtectedWriteAdmissionNotReadConfidentialityBoundary",
        },
        "StrongLocalContextualReferenceAdmissionProfileV0": {
            "SurvivingNonInlinedClassValuesStrongReferenceBoundary",
            "ClassOrSubclassTargetNoMixinOnlyMatchBoundary",
            "SameRoleSamePartitionNoRegistryFactBorrowingBoundary",
            "AcceptedPrestateEarlierOrderedWritesWholeCandidateAtomicNoRuntimeSortBoundary",
            "EntityOnlyRelationEndpointsEntityOrRelationSignalBearersBoundary",
            "GlobalRecordIDNamespaceReferentiallyClosedTemporalViewsBoundary",
            "InlinedValuesAndPrimitiveIDHashScalarsNotContextualReferencesBoundary",
            "NoCascadeRepairDeletionMigrationReadAccessOrImplementationBoundary",
            "GovernanceRepresentationAndReadPolicyRemainDeferredAfterOD010Boundary",
        },
        "ExplicitSingleResolverProfileSelection": {
            "StrictMalleusResolverDefaultBoundary",
            "ExplicitNamedVersionedResolverAndConfigurationBoundary",
            "ResolverSoleByteSourceAdapterNoHiddenIOBoundary",
            "ResolverFileAndNetworkCapabilitiesDefaultDenyBoundary",
            "ResolverNeverTryNextFallbackBoundary",
            "ExactResolvedSourceAndImportEdgeProvenanceBoundary",
            "ExactResolvedLocatorStringModuleInstanceIdentityBoundary",
            "NoUniversalLocatorNormalizationBoundary",
            "RootRetainedSourceSeparateFromImportEdgeBoundary",
            "ImportEdgeCarriesParentOrdinalLiteralAndChildResolvedLocatorBoundary",
            "ResolvedIdentityDifferentBytesRefusalBoundary",
            "DifferentLocatorSameBytesDistinctObservationBoundary",
            "ImportOrderProvenanceOnlyBoundary",
            "AllImportCyclesRefusedWithLineageBoundary",
        },
        "SingleDistributionCompilerIncludedPackagingTopology": {
            "NormalMalleusInstallIncludesCompilerAndLinkMLBoundary",
            "NoCoreCompilerExtraOrSecondDistributionV0Boundary",
            "LeanInstallDeferredGovernedRevisionBoundary",
            "ArtifactBackedRuntimeLinkMLImportBlockedBoundary",
            "TargetTopologyNotCurrentPackagingClaimBoundary",
        },
        "QuietBellArchiveFixturePublicationBoundary": {
            "QuietBellVocabularyFixtureOnlyCoreNeutralBoundary",
            "QuietBellAttestationExcludesVisualAssetsBoundary",
            "FuturePublicAssetExactManifestBoundary",
            "CCPUB01ReviewBindsExactManifestDigestBoundary",
            "AssetOrManifestChangeInvalidatesPublicReviewBoundary",
            "DecisionCreatesNoFixtureAssetOrPublicationBoundary",
        },
    }
    for selected, expected in required_bindings.items():
        assert {
            str(value).removeprefix(mfg)
            for value in canonical.objects(URIRef(f"{mfg}{selected}"), binds)
        } == expected

    knowledge_change_set = URIRef(f"{mfg}KnowledgeChangeSet")
    knowledge_change_set_hash = URIRef(f"{mfg}KnowledgeChangeSetHash")
    identified_by = URIRef(f"{mfg}identifiedBy")
    governed_by = URIRef(f"{mfg}governedBy")
    assert set(canonical.objects(knowledge_change_set, rdf_type)) == {
        URIRef("http://www.w3.org/2000/01/rdf-schema#Class")
    }
    assert set(canonical.objects(knowledge_change_set, status)) == {
        URIRef(f"{mfg}Candidate")
    }
    assert set(canonical.objects(knowledge_change_set, identified_by)) == {
        knowledge_change_set_hash
    }
    assert set(canonical.objects(knowledge_change_set, governed_by)) == {
        URIRef(f"{mfg}EffectiveContract")
    }
    assert {
        str(value).removeprefix(mfg)
        for value in canonical.objects(knowledge_change_set_hash, binds)
    } == {
        "EffectiveContractHash",
        "KnowledgeChangeSetSourceEvidenceClosureHash",
        "KnowledgeChangeSetBaseLedgerHead",
        "KnowledgeChangeSetBaseStateHash",
        "KnowledgeChangeSetOrderedOperationManifestHash",
        "KnowledgeChangeSetValidTimeCoordinateHash",
        "KnowledgeChangeSetSupersessionHash",
        "KnowledgeChangeSetLocalDependencyHash",
    }

    operation_plan = URIRef(f"{okg}OperationDependencyPlan")
    construction_member_graph = URIRef(f"{okg}ConstructionMemberGraph")
    supersedes = URIRef(f"{mfg}supersedes")
    assert set(canonical.objects(operation_plan, status)) == {
        URIRef(f"{mfg}Candidate")
    }
    assert set(canonical.objects(operation_plan, supersedes)) == {
        construction_member_graph
    }
    assert set(canonical.objects(construction_member_graph, status)) == {
        URIRef(f"{mfg}Excluded")
    }
    transition_plan_boundary = URIRef(
        f"{mfg}TransitionLocalOperationDependencyPlanBoundary"
    )
    assert set(canonical.objects(transition_plan_boundary, binds)) == {
        URIRef(f"{okg}PopulationPlan"),
        URIRef(f"{okg}GraphConstructionPlan"),
        operation_plan,
    }
    assert not any("SemanticTransition" in str(node) for node in canonical.all_nodes())

    identified_by = URIRef(f"{mfg}identifiedBy")
    metamodel_identities = {
        "ExactNonExpressionSeedContractMetamodel": OD008_SEED_METAMODEL_ID,
        "FlatExactlyOneExpressionExtensionV0": OD008_EXPRESSION_METAMODEL_ID,
        "ExpressionCapableContractMetamodelV0": OD008_COMBINED_METAMODEL_ID,
        "LinkMLV0SlashQualifiedSymbolPolicy": OD008_SYMBOL_POLICY_ID,
    }
    for subject, identity in metamodel_identities.items():
        assert set(canonical.objects(URIRef(f"{mfg}{subject}"), identified_by)) == {
            URIRef(identity)
        }
    supersedes = URIRef(f"{mfg}supersedes")
    assert set(
        canonical.objects(
            URIRef(f"{mfg}ClosedSeedExpressionRuleUnionCompositionV0"), supersedes
        )
    ) == {URIRef(f"{mfg}ExpressionVocabularyDeferredToOD008Boundary")}
    assert set(
        canonical.objects(
            URIRef(f"{mfg}StablePublicFactIdentityStillOD009Boundary"), supersedes
        )
    ) == {URIRef(f"{mfg}StablePublicFactIdentityStillOD008Boundary")}
    assert set(
        canonical.objects(URIRef(f"{mfg}GovernanceTopologyQuestionR2"), supersedes)
    ) == {URIRef(f"{mfg}GovernanceTopology")}
    assert set(
        canonical.objects(
            URIRef(
                f"{mfg}GovernanceRepresentationAndReadPolicyRemainDeferredAfterOD010Boundary"
            ),
            supersedes,
        )
    ) == {URIRef(f"{mfg}GovernanceRepresentationAndD10SemanticsDeferredBoundary")}
    assert set(
        canonical.objects(URIRef(f"{mfg}GovernanceTopologyQuestionR2"), selects)
    ) == {
        URIRef(f"{mfg}ProtectedReplayDerivedGovernancePartitionTopologyV0")
    }
    rejects = URIRef(f"{mfg}rejects")
    assert set(canonical.objects(od007, rejects)) == {
        URIRef(f"{mfg}GovernancePolicyGraphR2")
    }
    endpoint_expansion = URIRef(f"{mfg}EntityEventSignalRelationEndpointExpansionV0")
    assert set(canonical.objects(od010, rejects)) == {endpoint_expansion}
    assert set(canonical.objects(endpoint_expansion, rdf_type)) == {
        URIRef(f"{mfg}DesignObject")
    }
    assert set(canonical.objects(endpoint_expansion, status)) == {
        URIRef(f"{mfg}Excluded")
    }
    depends_on = URIRef(f"{mfg}dependsOn")
    assert set(
        canonical.objects(
            URIRef(f"{mfg}StrongLocalContextualReferenceAdmissionProfileV0"),
            depends_on,
        )
    ) == {
        URIRef(f"{mfg}ThreeRoleClosedContractCompositionProfile"),
        URIRef(f"{mfg}ProtectedReplayDerivedGovernancePartitionTopologyV0"),
        URIRef("https://malleus.dev/ontology-kg-realization/LocalReferenceDependencyRule"),
    }
    historical_graph = URIRef(f"{mfg}GovernancePolicyGraph")
    rejected_graph = URIRef(f"{mfg}GovernancePolicyGraphR2")
    assert set(canonical.objects(historical_graph, rdf_type)) == {
        URIRef(f"{mfg}DesignObject")
    }
    assert set(canonical.objects(historical_graph, status)) == {URIRef(f"{mfg}Open")}
    assert set(canonical.objects(rejected_graph, rdf_type)) == {
        URIRef(f"{mfg}DesignObject")
    }
    assert set(canonical.objects(rejected_graph, status)) == {
        URIRef(f"{mfg}Excluded")
    }
    assert set(canonical.objects(rejected_graph, supersedes)) == {historical_graph}
    selected_topology = URIRef(
        f"{mfg}ProtectedReplayDerivedGovernancePartitionTopologyV0"
    )
    assert set(canonical.objects(selected_topology, supersedes)) == set()
    assert set(
        canonical.objects(URIRef(f"{mfg}GovernanceTopology"), rdf_type)
    ) == {URIRef(f"{mfg}OpenQuestion")}
    assert set(
        canonical.objects(URIRef(f"{mfg}GovernanceTopology"), status)
    ) == {URIRef(f"{mfg}Open")}
    for retired in (
        "ExpressionVocabularyDeferredToOD008Boundary",
        "StablePublicFactIdentityStillOD008Boundary",
    ):
        assert set(canonical.subjects(binds, URIRef(f"{mfg}{retired}"))) == set()

    assert {
        str(value).removeprefix(mfg)
        for value in canonical.objects(
            URIRef(f"{mfg}AcceptedTemporalGraphVersionHash"), binds
        )
    } == {
        "ContractCompositionHash",
        "CanonicalStructuralStateHash",
        "TemporalMetadataDigest",
        "SourceProtocolLedgerHead",
        "AcceptanceHead",
        "MaterializationHead",
    }

    role_hash_bindings = {
        "ProtocolRecordContractHash": {
            "RoleBoundContractIdentityV0",
            "ProtocolRecordContractRoleTag",
            "EffectiveContractHash",
        },
        "GovernedGraphContractHash": {
            "RoleBoundContractIdentityV0",
            "GovernedGraphContractRoleTag",
            "EffectiveContractHash",
        },
        "GovernanceContractHash": {
            "RoleBoundContractIdentityV0",
            "GovernanceContractRoleTag",
            "EffectiveContractHash",
        },
        "ContractCompositionHash": {
            "ContractCompositionIdentityV0",
            "ProtocolRecordContractHash",
            "GovernedGraphContractHash",
            "GovernanceContractHash",
        },
    }
    for identity, expected in role_hash_bindings.items():
        assert {
            str(value).removeprefix(mfg)
            for value in canonical.objects(URIRef(f"{mfg}{identity}"), binds)
        } == expected
    accepted_status = URIRef(f"{mfg}AcceptedDesign")
    status = URIRef(f"{mfg}status")
    for subject in (
        "ProtocolRecordContract",
        "GovernedGraphContract",
        "GovernanceContract",
        "ContractComposition",
    ):
        assert set(canonical.objects(URIRef(f"{mfg}{subject}"), status)) == {
            accepted_status
        }
    quiet_bell = URIRef(f"{mfg}QuietBellArchiveFixturePublicationBoundary")
    assert set(canonical.objects(quiet_bell, URIRef(f"{mfg}workingName"))) == {
        Literal("Quiet Bell Archive")
    }
    assert set(canonical.objects(quiet_bell, URIRef(f"{mfg}attestationText"))) == {
        Literal(
            "Luis Guzman Lorenzo is the author and rights holder for the original "
            "Quiet Bell text/data, licensed Apache-2.0"
        )
    }
    r3 = URIRef(f"{mfg}LinkMLV1_11_1ReleaseCompilerBaselineR3")
    assert (
        r3,
        URIRef(f"{mfg}supersedes"),
        URIRef(f"{mfg}LinkMLV1_11_1ReleaseCompilerBaselineR2"),
    ) in canonical
    for selected in (
        "Antlr4Python3Runtime4_9_3DeterministicWheelBuildProfile",
        "Prefixcommons0_1_12Malleus1WheelDerivationProfile",
        "CC002CompilerEnvironmentMaterializationAndAttestationBoundaryR3",
        "RootSourceRetentionSeparateFromTransitiveBuildInputBoundary",
        "DerivativeInputSeparateFromBuildAndRuntimeBoundary",
        "TwoFreshBuildsByteIdenticalBoundary",
        "TwoFreshTransformsByteIdenticalBoundary",
        "FinalRuntimeClosureRemainsWheelOnlyBoundary",
        "RuntimeClosureExcludesPytestPytestLoggingAndPyBoundary",
        "MalleusDerivedPackagingMaintenanceAndSecurityOwnershipBoundary",
    ):
        assert (r3, binds, URIRef(f"{mfg}{selected}")) in canonical

    statuses: dict[object, set[object]] = {}
    for subject, _, object_ in canonical.triples((None, status, None)):
        statuses.setdefault(subject, set()).add(object_)
    assert len(statuses) == 395
    assert all(len(values) == 1 for values in statuses.values())
    realization = (
        ROOT / "design" / "ONTOLOGY_DRIVEN_KG_REALIZATION.md"
    ).read_text(encoding="utf-8")
    assert (
        "4. All 357 subjects carrying `mfg:status` have exactly one distinct status."
    ) in realization

    edges = {
        (subject, object_)
        for subject, _, object_ in canonical.triples((None, depends_on, None))
    }
    nodes = {node for edge in edges for node in edge}
    assert len(nodes) == 109
    assert len(edges) == 109
    successors = {node: set() for node in nodes}
    indegree = {node: 0 for node in nodes}
    for dependent, prerequisite in edges:
        successors[prerequisite].add(dependent)
        indegree[dependent] += 1
    ready = [node for node, count in indegree.items() if count == 0]
    visited = 0
    while ready:
        node = ready.pop()
        visited += 1
        for successor in successors[node]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
    assert visited == len(nodes)

    checkpoint = (
        ROOT / "design" / "GRAPH_REALIZATION_RUNNING_DOMAIN_CHECKPOINT.md"
    ).read_text(encoding="utf-8")
    for exact in (
        "Create `O1`, distinct physical item\n   `X1`, and fixture-defined `OrderContainsUnit(O1, X1)`",
        "After `I1` and `I2` exist, create\n   `P1` and two `PaymentSettlesInvoiceRelation` records.",
        "supplier-order `B` change from\n   `1Y` at `e4` to `2Y` at `e7`, then retain the bounded `I2` update at `e9`.",
        "e27 correlates with O1, X1, X2, Y1, and R4",
        "`Y1` and `Y2` are distinct physical items.",
        "Exact, closed input bytes produce\nexact compiled artifacts or an exact typed refusal.",
        "The skill is an untrusted proposal producer outside the\ncompiler.",
        "Its bytes enter ordinary evidence, review, and decision handling.",
        "Replay uses retained bytes and\nrecorded artifacts and never calls the skill.",
    ):
        assert exact in checkpoint


def test_knowledge_change_set_target_has_one_state_authority() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    program = (ROOT / "design" / "contract_compiler" / "program.md").read_text(
        encoding="utf-8"
    )
    projection = (
        ROOT / "design" / "SEMANTIC_LOG_KNOWLEDGE_PROJECTION.md"
    ).read_text(encoding="utf-8")
    recipe = (ROOT / "design" / "GRAPH_RECIPE_TDD_EXPERIMENTS.md").read_text(
        encoding="utf-8"
    )
    combined = " ".join((decisions + program + projection).split())

    for phrase in (
        "KnowledgeChangeSet is the one frontend-neutral immutable state-change artifact",
        "one authoritative ordered semantic and protocol history",
        "one evolving temporal domain-KG projection",
        "initial accepted domain state is the empty graph",
        "same immutable KnowledgeChangeSet identity",
        "ACCEPT decision event may contain the atomic application",
        "persisted structural candidate remains non-governed and non-accepted",
        "cross-contract KnowledgeChangeSet or migration change set",
        "machine effects may produce, validate, or admit exact change-set and receipt data",
        "must not mutate the accepted temporal graph directly",
    ):
        assert phrase in combined

    assert "Three graphs must remain distinct" not in recipe
    assert "Three artifacts must remain distinct" in recipe
    assert "`OperationDependencyPlan` is not a knowledge graph" in recipe
    assert "retained v0 research wire labels" in recipe
    assert "`OperationDependencyPlan` data, not another knowledge graph" in recipe
    assert "Member-graph assembly and operation ordering." not in recipe
    assert "member graphs, proposed operations" not in (
        ROOT / "design" / "ONTOLOGY_DRIVEN_KG_REALIZATION.md"
    ).read_text(encoding="utf-8")


def test_od005_seed_vocabulary_and_canonical_example_are_mechanical() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od005_section(decisions)
    prose = " ".join(section.split())

    assert "JSON and any future JSON Schema define syntax only." in prose
    assert "wire facts always carry the full absolute IRI" in prose
    assert "`OD-008` now maps source fields to this exact seed" in prose
    assert "final predicate inventory" not in prose
    assert "There is no generic `defaultValue` fact" in prose
    assert "not a public or second first-party authoring language" in prose
    assert "never the normative runtime wire" in prose
    assert "stable public identifiers still require the promotion decision at `od-009`" in prose.casefold()
    assert "stable public fact ids remain blocked on `od-006`" not in prose.casefold()
    for rule in (
        "The parent-plus-`usesMixin` graph is acyclic.",
        "Every `usesMixin` target has `isMixin=true`",
        "The Scalar `typeof` graph is acyclic and terminates in exactly one seed primitive.",
        "Every non-seed identifier target resolves in the same fact set.",
        "Bounds are legal only when `valueRange` directly names `Integer` or `Float`, or resolves through a Scalar chain terminating there",
        "`valuePresence=ABSENT` conflicts with `required=true` and with `equalsString`.",
        "deterministic qualified class-local declaration",
        "Source-to-fact completeness is separately proven by support-profile conformance and independent oracles.",
    ):
        assert rule in prose
    for forbidden in (
        "example.malleus.dev/archive",
        "ReviewState",
        "Shelfmark",
        "Quiet Bell",
        "NinthQuire",
        "http://www.w3.org/2001/XMLSchema",
    ):
        assert forbidden not in section

    _assert_od005_closed_seed(section)

    json_blocks = [
        token.content.removesuffix("\n")
        for token in MarkdownIt("commonmark").parse(section)
        if token.type == "fence" and token.info.strip() == "json"
    ]
    fact_source = next(block for block in json_blocks if block.startswith("["))
    assert "\n" not in fact_source
    facts = json.loads(fact_source)
    assert len(facts) == 38
    assert canonical_json(facts) == fact_source
    records = [canonical_json(fact) for fact in facts]
    assert records == sorted(records)
    assert len(records) == len(set(records))
    assert all(set(fact) == {"subject", "predicate", "object"} for fact in facts)
    assert all(isinstance(fact["object"], (str, bool)) for fact in facts)
    source_bytes = fact_source.encode("utf-8")
    source_digest = hashlib.sha256(source_bytes).hexdigest()
    assert len(source_bytes) == 6244
    assert source_digest == (
        "31db4d651f7a90f86466141193d806a5af58f8e09afa20dba838224b9361ca74"
    )
    assert (
        f"The array contains {len(facts)} facts and {len(source_bytes):,} bytes. "
        "Its SHA-256 is"
    ) in section
    assert f"`{source_digest}`" in section
    assert f"produce the same {len(facts)} metamodel-valid facts" in section

    envelope_source = next(
        block
        for block in json_blocks
        if block.startswith('{"class":')
        and "malleus.contract-structure.slot-use/v0" in block
    )
    envelope = json.loads(envelope_source)
    assert canonical_json(envelope) == envelope_source
    slot_use = (
        "urn:malleus:contract-structure:slot-use:v0:sha256:"
        + hashlib.sha256(envelope_source.encode("utf-8")).hexdigest()
    )
    assert slot_use == (
        "urn:malleus:contract-structure:slot-use:v0:sha256:"
        "5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"
    )
    slot_use_facts = {
        fact["predicate"]: fact["object"]
        for fact in facts
        if fact["subject"] == slot_use
    }
    assert slot_use_facts == {
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": (
            "https://malleus.dev/contract-facts/SlotUse"
        ),
        "https://malleus.dev/contract-facts/identifier": False,
        "https://malleus.dev/contract-facts/inlined": False,
        "https://malleus.dev/contract-facts/multivalued": False,
        "https://malleus.dev/contract-facts/onClass": (
            "https://example.malleus.dev/domain/Record"
        ),
        "https://malleus.dev/contract-facts/required": True,
        "https://malleus.dev/contract-facts/usesSlot": (
            "https://example.malleus.dev/domain/value"
        ),
        "https://malleus.dev/contract-facts/valuePresence": "PRESENT",
        "https://malleus.dev/contract-facts/valueRange": (
            "https://malleus.dev/contract-facts/String"
        ),
    }
    seed_primitives = {
        f"https://malleus.dev/contract-facts/{name}"
        for name in ("String", "Integer", "Float", "Boolean", "DateTime")
    }
    assert not seed_primitives & {fact["subject"] for fact in facts}
    assert not any(
        fact["predicate"] == "https://malleus.dev/contract-facts/defaultValue"
        for fact in facts
    )
    evidence_source = (
        ROOT
        / "design"
        / "contract_compiler"
        / "overseer"
        / "evidence"
        / "CC-D05.json"
    ).read_text(encoding="utf-8")
    evidence = json.loads(evidence_source)
    assert {check["check_id"] for check in evidence["checks"]} == {
        "ccd05-dependencies",
        "ccd05-seed-metamodel",
        "ccd05-canonical-bytes",
        "ccd05-graph",
        "ccd05-boundaries",
        "ccd05-zero-scope",
    }
    for forbidden in (
        "Quiet Bell",
        "NinthQuire",
        "ReviewState",
        "Shelfmark",
        "example.malleus.dev/archive",
    ):
        assert forbidden not in evidence_source


def test_od005_closed_seed_guard_rejects_adversarial_drift() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od005_section(decisions)
    row = "| `Scalar` | `cf:typeof` | `Scalar` or `SeedPrimitive` | 1 |"
    assert section.count(row) == 1
    mutations = (
        section.replace(
            row,
            row + "\n| `Scalar` | `cf:experimental` | string | 0..1 |",
            1,
        ),
        section.replace(row, "", 1),
        section.replace(row, row + "\n" + row, 1),
        section.replace(
            "and `DateTime` under the seed namespace",
            "`DateTime`, and `Decimal` under the seed namespace",
            1,
        ),
    )
    assert all(mutation != section for mutation in mutations)
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _assert_od005_closed_seed(mutation)


def test_od006_closed_three_role_composition_is_mechanical() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od006_section(decisions)
    prose = " ".join(section.split())

    _assert_od006_closed_contract(section)
    for phrase in (
        "Each slot binds one complete `EffectiveContract` identity.",
        "not a namespace label, overlay, patch, or partial view",
        "Two roles remain non-interchangeable even when their underlying effective-contract payloads or identities are equal.",
        "One physical artifact may package all three complete role contracts.",
        "semantic modularity, not three packages, installations, processes, ledgers, or compiler invocations",
        "The only narrower case is a standalone structural graph.",
        "An accepted-temporal graph bound only to the governed-graph role refuses",
        "when an already-bound epoch is continued with a valid replacement role identity but no new composition is constructed and bound",
        "Whole-composition validation refuses atomically",
        "`OD-007` owns governance storage topology",
        "`OD-010` owns endpoint, reference, context, and stateful admission semantics",
        "`OD-008` completes the candidate fact-identity inputs; `OD-009` still owns public promotion and identifier publication.",
        "This decision creates no implementation, ontology YAML, package, artifact, bundle, public API, or migration mechanism.",
    ):
        assert phrase in prose
    for forbidden in (
        "example.malleus.dev/archive",
        "Quiet Bell",
        "NinthQuire",
        "Shelfmark",
    ):
        assert forbidden not in section

    conformance = (
        ROOT / "design" / "contract_compiler" / "conformance.md"
    ).read_text(encoding="utf-8")
    assert "OD-010 now supplies their outcomes" in conformance
    assert "Cross-partition references, read authorization" not in conformance
    row = next(line.casefold() for line in conformance.splitlines() if line.startswith("| AT-008 "))
    for phrase in (
        "complete p/d/g role closures",
        "fixed conceptual v0 role tags and constructors",
        "standalone d-only structural graph",
        "wrong fixed role tag, domain, version, or composition constructor",
        "new composition and epoch for any semantic role change",
        "exact atomic refusal",
    ):
        assert phrase in row
    for forbidden in ("single-artifact", "wrong grammar"):
        assert forbidden not in row

    program = (
        ROOT / "design" / "contract_compiler" / "program.md"
    ).read_text(encoding="utf-8")
    cc_d06 = next(line.casefold() for line in program.splitlines() if line.startswith("| CC-D06 "))
    for phrase in (
        "exact three-role closure",
        "fixed conceptual v0 identity constructors",
        "structural-only exception",
        "deferred wire boundaries",
    ):
        assert phrase in cc_d06


def test_od006_closed_composition_guard_rejects_adversarial_drift() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od006_section(decisions)
    role_row = (
        "| `GovernanceContract` | Authorization and governance-policy semantics |"
    )
    assert section.count(role_row) == 1
    mutations = (
        section.replace(
            role_row,
            role_row + "\n| `ExtensionContract` | Unapproved fourth role |",
            1,
        ),
        section.replace(role_row, "", 1),
        section.replace(role_row, role_row + "\n" + role_row, 1),
        section.replace("cardinality `1..1`", "cardinality `0..1`", 1),
        section.replace(
            "  fixed_role_name,\n  exact_effective_contract_identity",
            "  fixed_role_name,\n  unapproved_input,\n  exact_effective_contract_identity",
            1,
        ),
        section.replace("  fixed_role_name,\n", "", 1),
        section.replace(
            "  ProtocolRecordContract_role_identity,\n"
            "  GovernedGraphContract_role_identity,",
            "  GovernedGraphContract_role_identity,\n"
            "  ProtocolRecordContract_role_identity,",
            1,
        ),
        section.replace(
            "RoleBoundContractIdentity(",
            "CallerSelectedRoleIdentity(",
            1,
        ),
        section.replace(
            "malleus.contract-role-bound-identity/v0",
            "malleus.contract-role-bound-identity/v1",
            1,
        ),
        section.replace(
            "malleus.contract-composition-identity/v0",
            "malleus.contract-composition-identity/v1",
            1,
        ),
        section.replace("There is no fourth role", "A fourth role is allowed", 1),
        section.replace(
            "when protocol and governed-graph slots are\nswapped; ",
            "",
            1,
        ),
        section.replace(
            "when roles from different\ncompositions are mixed without constructing a new composition; ",
            "",
            1,
        ),
        section.replace(
            "Whole-composition validation refuses atomically; no subset is accepted.",
            "An unapproved refusal is accepted.\n\n"
            "Whole-composition validation refuses atomically; no subset is accepted.",
            1,
        ),
    )
    assert all(mutation != section for mutation in mutations)
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _assert_od006_closed_contract(mutation)


def test_od007_protected_partition_contract_is_exact() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od007_section(decisions)
    prose = " ".join(section.split())

    for phrase in (
        "`SourceProtocolLedgerHead`, `AcceptanceHead`, and `MaterializationHead` identity components remain unchanged",
        "no governance-specific head, snapshot, or digest",
        "The `ProtocolLedger` is the sole write authority.",
        "not a third partition or the same physical store as the accepted graph",
        "Membership never comes from a caller-supplied partition field, record-type guess, namespace, or storage convention",
        "pre-event authority state, seeded at genesis by the external root and otherwise derived from accepted governance state",
        "exactly one explicit bootstrap authority root at genesis",
        "Domain and governance graph writes cannot create, replace, or delete that root.",
        "cannot authorize itself",
        "When the authority source is a governance policy, its identity must differ from the directly mutated governance-policy identity",
        "cannot directly create, change, or delete a governance record identity",
        "Cross-partition references, endpoints, and reads remain with D10",
        "same accepted-graph lineage and existing state-identity components",
        "same `GovernanceContract` identity stays in the current composition epoch",
        "semantic change to the `GovernanceContract` changes its role-bound identity",
        "As current shipped behavior, existing typed policy artifacts remain protocol-ledger artifacts",
        "D07 does not materialize current artifacts",
        "D07 selects no read authorization, filtering, query-access, or secrecy policy.",
        "A standalone structural graph has no governance role and refuses governance records.",
        "logical partition is not an RDF named graph, database, namespace, caller flag, or public wire field",
        "`OD-010` retains exact endpoint, class-reference, context, and stateful admission semantics",
        "This decision creates no production implementation, ontology YAML, record schema, operation vocabulary, API, storage layout, migration, or second graph.",
    ):
        assert phrase in prose

    conformance = (
        ROOT / "design" / "contract_compiler" / "conformance.md"
    ).read_text(encoding="utf-8")
    row = next(
        line.casefold()
        for line in conformance.splitlines()
        if line.startswith("| AT-008a ")
    )
    for phrase in (
        "protected replay-derived governance partition",
        "single external bootstrap root",
        "pre-event authority",
        "same-contract policy update",
        "no type/name/namespace/storage inference",
        "no governance-specific head or query surface",
        "atomic refusal",
    ):
        assert phrase in row

    program = (
        ROOT / "design" / "contract_compiler" / "program.md"
    ).read_text(encoding="utf-8")
    d07 = next(line.casefold() for line in program.splitlines() if line.startswith("| CC-D07 "))
    for phrase in ("protected replay-derived governance partition", "epoch boundary"):
        assert phrase in d07
    remaining = decisions.split("## Remaining decisions after revision 23", 1)[1]
    assert "| OD-007 |" not in remaining


def test_od007_replay_uses_prior_state_and_shared_graph_lineage() -> None:
    contract = "urn:malleus:test:governance-contract:v0"
    epoch = "urn:opaque:composition-epoch"
    bootstrap = (("actor:root", "urn:opaque:bootstrap-root"),)
    graph = _Od007ReplayProjection(bootstrap, contract, epoch)
    graph.consume_domain_event(
        "policy:looks-protected",
        "ordinary",
        "GovernedGraphContract",
    )
    assert graph.query("policy:looks-protected") == ("domain", "ordinary")

    before_refusal = _od007_state(graph)
    with pytest.raises(_Od007Refusal, match="pre-event authority"):
        graph.consume_governance_event(
            "policy:self-grant",
            "self-grant",
            "actor:reviewer",
            "policy:self-grant",
            ("actor:reviewer",),
            "GovernanceContract",
            contract,
        )
    assert _od007_state(graph) == before_refusal

    graph.consume_governance_event(
        "domain:looks-ordinary",
        "grant",
        "actor:root",
        graph._bootstrap_source_identity,
        ("actor:reviewer",),
        "GovernanceContract",
        contract,
    )
    assert graph.query("domain:looks-ordinary") == ("governance", "grant")

    graph.consume_governance_event(
        "policy:reviewer-update",
        "accepted only after grant",
        "actor:reviewer",
        "domain:looks-ordinary",
        (),
        "GovernanceContract",
        contract,
    )
    assert graph.query("policy:reviewer-update") == (
        "governance",
        "accepted only after grant",
    )
    graph.consume_governance_event(
        "domain:looks-ordinary",
        "revised policy instance",
        "actor:root",
        graph._bootstrap_source_identity,
        (),
        "GovernanceContract",
        contract,
    )
    assert graph.query("domain:looks-ordinary") == (
        "governance",
        "revised policy instance",
    )
    assert graph.composition_epoch_identity == epoch
    assert len(graph.accepted_events()) == 4
    replayed = _Od007ReplayProjection.replay(
        graph.accepted_events(),
        bootstrap,
        contract,
        epoch,
    )
    assert _od007_state(replayed) == _od007_state(graph)


@pytest.mark.parametrize(
    "roots",
    [(), (("actor:one", "root:one"), ("actor:two", "root:two"))],
)
def test_od007_genesis_requires_one_bootstrap_authority(
    roots: tuple[tuple[str, str], ...],
) -> None:
    with pytest.raises(_Od007Refusal, match="exactly one bootstrap authority root"):
        _Od007ReplayProjection(
            roots,
            "urn:malleus:test:governance-contract:v0",
            "urn:opaque:composition-epoch",
        )


def test_od007_protected_partition_refusals_are_atomic() -> None:
    contract = "urn:malleus:test:governance-contract:v0"
    graph = _Od007ReplayProjection(
        (("actor:root", "urn:opaque:bootstrap-root"),),
        contract,
        "urn:opaque:composition-epoch",
    )
    graph.consume_governance_event(
        "policy:base",
        "base policy instance",
        "actor:root",
        graph._bootstrap_source_identity,
        ("actor:reviewer",),
        "GovernanceContract",
        contract,
    )
    graph.consume_domain_event(
        "domain:base",
        "base domain record",
        "GovernedGraphContract",
    )
    accepted = _od007_state(graph)
    assert graph.query(graph._bootstrap_source_identity) is None
    with pytest.raises(_Od007Refusal, match="cannot authorize its own amendment"):
        graph.consume_governance_event(
            "policy:base",
            "forbidden self-amendment",
            "actor:reviewer",
            "policy:base",
            (),
            "GovernanceContract",
            contract,
        )
    assert _od007_state(graph) == accepted
    with pytest.raises(_Od007Refusal, match="ordinary transition cannot touch"):
        graph.consume_domain_event(
            "policy:base",
            "forbidden direct mutation",
            "GovernedGraphContract",
        )
    assert _od007_state(graph) == accepted
    with pytest.raises(_Od007Refusal, match="external bootstrap root"):
        graph.consume_domain_event(
            graph._bootstrap_source_identity,
            "forbidden bootstrap mutation",
            "GovernedGraphContract",
        )
    assert _od007_state(graph) == accepted
    with pytest.raises(_Od007Refusal, match="external bootstrap root"):
        graph.consume_governance_event(
            graph._bootstrap_source_identity,
            "forbidden bootstrap mutation",
            "actor:root",
            graph._bootstrap_source_identity,
            (),
            "GovernanceContract",
            contract,
        )
    assert _od007_state(graph) == accepted
    with pytest.raises(_Od007Refusal, match="wrong prior authority"):
        graph.consume_governance_event(
            "policy:wrong-source",
            "wrong source",
            "actor:reviewer",
            "policy:not-authoritative",
            (),
            "GovernanceContract",
            contract,
        )
    assert _od007_state(graph) == accepted
    with pytest.raises(_Od007Refusal, match="replace external root binding"):
        graph.consume_governance_event(
            "policy:authority-overwrite",
            "forbidden root replacement",
            "actor:root",
            graph._bootstrap_source_identity,
            ("actor:root",),
            "GovernanceContract",
            contract,
        )
    assert _od007_state(graph) == accepted
    with pytest.raises(_Od007Refusal, match="wrong contract admission path"):
        graph.consume_governance_event(
            "policy:wrong-role",
            "wrong role",
            "actor:root",
            graph._bootstrap_source_identity,
            (),
            "GovernedGraphContract",
            contract,
        )
    assert _od007_state(graph) == accepted
    with pytest.raises(_Od007Refusal, match="requires a new epoch"):
        graph.consume_governance_event(
            "policy:new-contract",
            "requires new epoch",
            "actor:root",
            graph._bootstrap_source_identity,
            (),
            "GovernanceContract",
            "urn:malleus:test:governance-contract:v1",
        )
    assert _od007_state(graph) == accepted
    with pytest.raises(_Od007Refusal, match="cannot reclassify a domain record"):
        graph.consume_governance_event(
            "domain:base",
            "forbidden reclassification",
            "actor:root",
            graph._bootstrap_source_identity,
            (),
            "GovernanceContract",
            contract,
        )
    assert _od007_state(graph) == accepted


def test_od010_contextual_reference_contract_is_exact() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od010_section(decisions)
    _assert_od010_contract(section)
    integration = json.loads(INTEGRATION.read_text(encoding="utf-8"))
    row = next(
        item
        for item in integration["workstreams"]
        if item["workstream_id"] == "CC-D10"
    )
    assert row["card"] == {
        "byte_length": (
            ROOT
            / "design"
            / "contract_compiler"
            / "workstreams"
            / "CC-D10"
            / "manifest.json"
        ).stat().st_size,
        "path": "workstreams/CC-D10/manifest.json",
        "sha256": "sha256:"
        + hashlib.sha256(
            (
                ROOT
                / "design"
                / "contract_compiler"
                / "workstreams"
                / "CC-D10"
                / "manifest.json"
            ).read_bytes()
        ).hexdigest(),
        "state": "PRESENT",
    }
    program = (
        ROOT / "design" / "contract_compiler" / "program.md"
    ).read_text(encoding="utf-8")
    d10 = next(line.casefold() for line in program.splitlines() if line.startswith("| CC-D10 "))
    for phrase in (
        "strong same-role and same-partition class references",
        "entity-only endpoints",
        "entity-or-relation bearer",
        "ordered candidate visibility",
        "referentially closed temporal views",
    ):
        assert phrase in d10
    remaining = decisions.split("## Remaining decisions after revision 23", 1)[1]
    assert "| OD-010 |" not in remaining

    conformance = (
        ROOT / "design" / "contract_compiler" / "conformance.md"
    ).read_text(encoding="utf-8")
    context = next(line.casefold() for line in conformance.splitlines() if line.startswith("| AT-011 "))
    staging = next(line.casefold() for line in conformance.splitlines() if line.startswith("| AT-012 "))
    for phrase in (
        "generic class reference",
        "entity-only relation endpoint",
        "entity-or-relation signal bearer",
        "same role and partition",
        "mixin-only",
        "referential closure",
    ):
        assert phrase in context
    for phrase in (
        "earlier dependency-ordered target",
        "later target",
        "self-reference",
        "cycle",
        "whole-candidate refusal",
        "no runtime topological sort",
    ):
        assert phrase in staging


def test_od010_quiet_bell_and_recon_strong_references_accept() -> None:
    admission = _od010_obligation
    admissions = (
        admission("Vella", "ArchiveExaminer"),
        admission("TheQuietBell", "InquiryDossier"),
        admission("NinthQuire", "EvidenceFolio"),
        admission(
            "CitesFolioRelation",
            "CitesFolioRelation",
            endpoints=(
                ("TheQuietBell", "InquiryDossier"),
                ("NinthQuire", "EvidenceFolio"),
            ),
        ),
        admission(
            "SealReviewEvent",
            "SealReviewEvent",
            refs=(("CitesFolioRelation", "Relation"),),
        ),
        admission(
            "SealDiscrepancySignal",
            "SealDiscrepancySignal",
            bearer="CitesFolioRelation",
        ),
        admission("evidence:one", "EvidenceAttachment"),
        admission("evidence:two", "EvidenceAttachment"),
        admission(
            "work:one",
            refs=(
                ("evidence:one", "EvidenceAttachment"),
                ("evidence:two", "EvidenceAttachment"),
            ),
        ),
        admission(
            "entity-bearer-signal",
            "SealDiscrepancySignal",
            bearer="TheQuietBell",
        ),
    )
    accepted = _od010_admit_candidate({}, admissions)
    assert tuple(accepted) == tuple(item[0] for item in admissions)
    assert _od010_select_temporal_view(accepted, frozenset(accepted)) == accepted


def test_od010_inlined_values_never_become_contextual_targets() -> None:
    missing = ("not-a-graph-record",)
    assert _od010_contextual_targets(
        class_valued=True,
        inlined=True,
        surviving_values=missing,
    ) == ()
    assert _od010_contextual_targets(
        class_valued=False,
        inlined=False,
        surviving_values=missing,
    ) == ()
    assert _od010_contextual_targets(
        class_valued=True,
        inlined=False,
        surviving_values=("target",),
    ) == ("target",)


def test_od010_contextual_refusals_preserve_the_complete_prestate() -> None:
    admission = _od010_obligation
    prestate = _od010_admit_candidate(
        {},
        (
            admission("entity", "InquiryDossier"),
            admission("attachment", "EvidenceAttachment"),
            admission("carrier", "MixinCarrier"),
            admission("event", "SealReviewEvent"),
            admission("signal", "SealDiscrepancySignal"),
            admission("relation", "CitesFolioRelation"),
        ),
    )
    accepted_prestate_reference = _od010_admit_candidate(
        prestate,
        (admission("prestate-ref", refs=(("attachment", "EvidenceAttachment"),)),),
    )
    assert accepted_prestate_reference["prestate-ref"][3] == ("attachment",)
    # Opaque foreign-state probes exercise lookup refusal. They are not admitted
    # combinations and make no D06 or D07 validity claim.
    prestate["other-role"] = (
        "EvidenceAttachment",
        "GovernanceContract",
        _OD010_PARTITION,
        (),
    )
    prestate["other-partition"] = (
        "EvidenceAttachment",
        _OD010_ROLE,
        "governance",
        (),
    )
    assert "EvidenceAttachment" in _OD010_MIXINS["MixinCarrier"]
    def assert_refuses(
        case: str,
        message: str,
        admissions: tuple[_Od010Admission, ...],
    ) -> None:
        before = dict(prestate)
        with pytest.raises(_Od010Refusal) as error:
            _od010_admit_candidate(prestate, admissions)
        assert message in str(error.value), case
        assert prestate == before, case

    generic_cases = (
        ("missing", "absent", "EvidenceAttachment", "absent from visible state"),
        ("wrong-type", "entity", "EvidenceAttachment", "class ancestry"),
        ("mixin-only", "carrier", "EvidenceAttachment", "class ancestry"),
        ("cross-role", "other-role", "EvidenceAttachment", "crosses role or partition"),
        ("cross-partition", "other-partition", "EvidenceAttachment", "crosses role or partition"),
    )
    for case, target, expected, message in generic_cases:
        assert_refuses(
            case,
            message,
            (admission(case, refs=((target, expected),)),),
        )

    sequence_cases = (
        (
            "forward",
            (
                admission("forward", refs=(("later", "EvidenceAttachment"),)),
                admission("later", "EvidenceAttachment"),
            ),
        ),
        ("self", (admission("self", refs=(("self", "Work"),)),)),
        (
            "cycle",
            (
                admission("cycle:a", refs=(("cycle:b", "Work"),)),
                admission("cycle:b", refs=(("cycle:a", "Work"),)),
            ),
        ),
        (
            "rollback after staged write",
            (
                admission("staged", "EvidenceAttachment"),
                admission("invalid", refs=(("absent", "EvidenceAttachment"),)),
            ),
        ),
    )
    for case, admissions in sequence_cases:
        assert_refuses(case, "absent from visible state", admissions)

    endpoint_cases = (
        ("Event endpoint", "event", "Entity", "class ancestry"),
        ("Relation endpoint", "relation", "Entity", "class ancestry"),
        (
            "non-Entity endpoint range",
            "relation",
            "Relation",
            "relation endpoint range is not Entity",
        ),
        ("Signal endpoint", "signal", "Entity", "class ancestry"),
        ("wrong Entity subtype", "entity", "EvidenceFolio", "class ancestry"),
        (
            "cross-role endpoint",
            "other-role",
            "Entity",
            "crosses role or partition",
        ),
        (
            "cross-partition endpoint",
            "other-partition",
            "Entity",
            "crosses role or partition",
        ),
        ("missing endpoint", "absent", "Entity", "absent from visible state"),
    )
    for case, target, expected, message in endpoint_cases:
        assert_refuses(
            case,
            message,
            (admission(case, "CitesFolioRelation", endpoints=((target, expected),)),),
        )

    bearer_cases = (
        ("Event bearer", "event", "not Entity or Relation"),
        ("Signal bearer", "signal", "not Entity or Relation"),
        ("missing bearer", "absent", "absent from visible state"),
        ("cross-role bearer", "other-role", "crosses role or partition"),
        ("cross-partition bearer", "other-partition", "crosses role or partition"),
    )
    for case, bearer, message in bearer_cases:
        assert_refuses(
            case,
            message,
            (admission(case, "SealDiscrepancySignal", bearer=bearer),),
        )

    duplicate_id_cases = (
        ("cross-category duplicate ID", admission("relation")),
        (
            "cross-partition duplicate ID",
            admission("attachment", "EvidenceAttachment", partition="governance"),
        ),
    )
    for case, duplicate in duplicate_id_cases:
        assert_refuses(case, "global namespace", (duplicate,))
    assert_refuses(
        "one bad multivalue member",
        "absent from visible state",
        (
            admission(
                "one-bad-multivalue",
                refs=(
                    ("attachment", "EvidenceAttachment"),
                    ("absent", "EvidenceAttachment"),
                ),
            ),
        ),
    )


def test_od010_temporal_views_refuse_incomplete_reference_closure() -> None:
    admission = _od010_obligation
    records = _od010_admit_candidate(
        {},
        (
            admission("dossier", "InquiryDossier"),
            admission("folio", "EvidenceFolio"),
            admission(
                "citation",
                "CitesFolioRelation",
                endpoints=(
                    ("dossier", "InquiryDossier"),
                    ("folio", "EvidenceFolio"),
                ),
            ),
            admission(
                "review",
                "SealReviewEvent",
                refs=(("citation", "Relation"),),
            ),
            admission(
                "discrepancy",
                "SealDiscrepancySignal",
                bearer="citation",
            ),
        ),
    )
    incomplete_views = (
        ("missing dossier", frozenset(records) - {"dossier"}),
        ("missing folio", frozenset(records) - {"folio"}),
        ("missing citation", frozenset(records) - {"citation"}),
        ("isolated generic reference", frozenset({"review"})),
        ("isolated signal bearer", frozenset({"discrepancy"})),
    )
    before = dict(records)
    for case, visible in incomplete_views:
        with pytest.raises(_Od010Refusal, match="referentially closed"):
            _od010_select_temporal_view(records, visible)
        assert records == before, case


def test_od010_contract_guard_rejects_semantic_drift() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od010_section(decisions)
    mutations = (
        section.replace(
            "REFUSE CANDIDATE | runtime does not search, reorder, or solve a fixed point",
            "ACCEPT | runtime searches the batch",
            1,
        ),
        section.replace(
            "Relation endpoints remain existing `Entity` records",
            "Relation endpoints may be any record",
            1,
        ),
        section.replace("`usesMixin` alone never satisfies", "`usesMixin` satisfies", 1),
        section.replace("Every selected temporal view must be referentially closed", "Temporal views may dangle", 1),
    )
    assert all(mutation != section for mutation in mutations)
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _assert_od010_contract(mutation)


def test_od008_closed_profile_and_expression_identity_are_mechanical() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od008_section(decisions)
    _assert_od008_closed_profile(section)

    blocks = [
        token.content.removesuffix("\n")
        for token in MarkdownIt("commonmark").parse(section)
        if token.type == "fence" and token.info.strip() == "json"
    ]
    assert len(blocks) == 8
    values = [json.loads(block) for block in blocks]
    assert all(canonical_json(value) == block for value, block in zip(values, blocks))

    def one(domain: str) -> tuple[str, dict[str, object]]:
        matches = [
            (block, value)
            for block, value in zip(blocks, values)
            if value.get("domain") == domain
        ]
        assert len(matches) == 1
        return matches[0]

    predicate_iris = {
        "rdf:type": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
        "rdfs:subClassOf": "http://www.w3.org/2000/01/rdf-schema#subClassOf",
    }

    def expanded_rule(row: tuple[str, ...]) -> list[str]:
        cells = [cell.replace("`", "") for cell in row]
        predicate = cells[1]
        cells[1] = predicate_iris.get(
            predicate,
            (
                "https://malleus.dev/contract-facts/" + predicate.removeprefix("cf:")
                if predicate.startswith("cf:")
                else predicate
            ),
        )
        return cells

    seed_block, seed = one("malleus.contract-metamodel/non-expression-seed/v0")
    assert len(seed_block.encode("utf-8")) == 4819
    assert seed == {
        "domain": "malleus.contract-metamodel/non-expression-seed/v0",
        "invariants": sorted(
            [
                {"id": identifier, "rule": rule}
                for identifier, rule in OD008_SEED_INVARIANTS
            ],
            key=canonical_json,
        ),
        "primitives": sorted(OD005_SEED_PRIMITIVES),
        "rules": sorted(
            [expanded_rule(row) for row in OD005_SEED_ROWS],
            key=canonical_json,
        ),
        "seed_namespace": "https://malleus.dev/contract-facts/",
        "structural_identity_canonicalization": (
            "malleus.canonical-json/d05-compact-sorted-key-utf8-no-newline/v0"
        ),
        "structural_identity_profiles": sorted(
            OD008_SEED_STRUCTURAL_IDENTITY_PROFILES,
            key=canonical_json,
        ),
    }
    seed_id = (
        "urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:"
        + hashlib.sha256(seed_block.encode("utf-8")).hexdigest()
    )
    assert seed_id == OD008_SEED_METAMODEL_ID

    extension_block, extension = one(
        "malleus.contract-metamodel/flat-exactly-one-extension/v0"
    )
    assert len(extension_block.encode("utf-8")) == 4762
    assert extension == {
        "domain": "malleus.contract-metamodel/flat-exactly-one-extension/v0",
        "invariants": sorted(
            [
                {"id": identifier, "rule": rule}
                for identifier, rule in OD008_EXPRESSION_INVARIANTS
            ],
            key=canonical_json,
        ),
        "rules": sorted(
            [expanded_rule(row) for row in OD008_EXPRESSION_ROWS],
            key=canonical_json,
        ),
        "semantic_member_profiles": sorted(
            OD008_EXPRESSION_SEMANTIC_MEMBER_PROFILES,
            key=canonical_json,
        ),
        "seed_namespace": "https://malleus.dev/contract-facts/",
        "structural_identity_canonicalization": (
            "malleus.canonical-json/d05-compact-sorted-key-utf8-no-newline/v0"
        ),
        "structural_identity_profiles": sorted(
            OD008_EXPRESSION_STRUCTURAL_IDENTITY_PROFILES,
            key=canonical_json,
        ),
    }
    extension_id = (
        "urn:malleus:contract-metamodel:flat-exactly-one-extension:v0:sha256:"
        + hashlib.sha256(extension_block.encode("utf-8")).hexdigest()
    )
    assert extension_id == OD008_EXPRESSION_METAMODEL_ID

    def assert_absolute_rule_predicates(component: dict[str, object]) -> None:
        rules = component["rules"]
        assert isinstance(rules, list)
        for rule in rules:
            assert isinstance(rule, list) and len(rule) == 4
            predicate = rule[1]
            assert isinstance(predicate, str) and urlsplit(predicate).scheme

    assert_absolute_rule_predicates(seed)
    assert_absolute_rule_predicates(extension)
    relative_predicate = json.loads(json.dumps(seed))
    relative_predicate["rules"][0][1] = "relative-predicate"
    with pytest.raises(AssertionError):
        assert_absolute_rule_predicates(relative_predicate)

    combined_block, combined = one("malleus.contract-metamodel/composition/v0")
    assert len(combined_block.encode("utf-8")) == 655
    assert combined == {
        "base": seed_id,
        "operator": OD008_COMPOSITION_OPERATOR,
        "domain": "malleus.contract-metamodel/composition/v0",
        "extension": extension_id,
    }
    combined_id = (
        "urn:malleus:contract-metamodel:expression-capable:v0:sha256:"
        + hashlib.sha256(combined_block.encode("utf-8")).hexdigest()
    )
    assert combined_id == OD008_COMBINED_METAMODEL_ID

    seed_prefix = "urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:"
    extension_prefix = (
        "urn:malleus:contract-metamodel:flat-exactly-one-extension:v0:sha256:"
    )

    def content_id(prefix: str, component: dict[str, object]) -> str:
        return prefix + hashlib.sha256(
            canonical_json(component).encode("utf-8")
        ).hexdigest()

    def composed_id(base: str, expression: str) -> str:
        envelope = {
            "base": base,
            "operator": OD008_COMPOSITION_OPERATOR,
            "domain": "malleus.contract-metamodel/composition/v0",
            "extension": expression,
        }
        return (
            "urn:malleus:contract-metamodel:expression-capable:v0:sha256:"
            + hashlib.sha256(canonical_json(envelope).encode("utf-8")).hexdigest()
        )

    seed_mutations: list[dict[str, object]] = []
    for path, replacement in (
        (("domain",), "malleus.contract-metamodel/non-expression-seed/v1"),
        (("invariants", 0, "rule"), "changed invariant proposition"),
        (("primitives", 0), "ChangedPrimitive"),
        (("rules", 0, 1), "https://example.test/changed-predicate"),
        (("rules", 0, 2), "changed object type"),
        (("rules", 0, 3), "0..1"),
        (("seed_namespace",), "https://example.test/changed-seed/"),
        (("structural_identity_canonicalization",), "changed-canonicalization"),
        (("structural_identity_profiles", 0, "domain"), "changed-domain"),
        (("structural_identity_profiles", 0, "members", 0), "changed-member"),
        (("structural_identity_profiles", 0, "hash"), "sha512"),
        (("structural_identity_profiles", 0, "digest_encoding"), "uppercase-hex"),
        (("structural_identity_profiles", 0, "output_prefix"), "changed-prefix"),
    ):
        changed = json.loads(json.dumps(seed))
        target: object = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = replacement
        seed_mutations.append(changed)

    extension_mutations: list[dict[str, object]] = []
    for path, replacement in (
        (("domain",), "malleus.contract-metamodel/flat-exactly-one-extension/v1"),
        (("invariants", 0, "rule"), "changed invariant proposition"),
        (("rules", 0, 1), "https://example.test/changed-predicate"),
        (("rules", 0, 2), "changed object type"),
        (("rules", 0, 3), "0..1"),
        (("semantic_member_profiles", 0, "minimum_optional_members"), 2),
        (("semantic_member_profiles", 0, "optional_members", 0), "changedMember"),
        (("semantic_member_profiles", 0, "required_members", 0), "changedMember"),
        (("seed_namespace",), "https://example.test/changed-seed/"),
        (("structural_identity_canonicalization",), "changed-canonicalization"),
        (("structural_identity_profiles", 0, "domain"), "changed-domain"),
        (("structural_identity_profiles", 0, "members", 0), "changed-member"),
        (("structural_identity_profiles", 0, "hash"), "sha512"),
        (("structural_identity_profiles", 0, "digest_encoding"), "uppercase-hex"),
        (("structural_identity_profiles", 0, "output_prefix"), "changed-prefix"),
        (
            (
                "structural_identity_profiles",
                1,
                "sorted_arrays",
                "alternative_semantic_digests",
            ),
            "source-order",
        ),
    ):
        changed = json.loads(json.dumps(extension))
        target = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = replacement
        extension_mutations.append(changed)

    for changed in seed_mutations:
        changed_seed_id = content_id(seed_prefix, changed)
        assert changed_seed_id != seed_id
        assert composed_id(changed_seed_id, extension_id) != combined_id
    for changed in extension_mutations:
        changed_extension_id = content_id(extension_prefix, changed)
        assert changed_extension_id != extension_id
        assert composed_id(seed_id, changed_extension_id) != combined_id
    assert composed_id(extension_id, seed_id) != combined_id
    combined_prefix = (
        "urn:malleus:contract-metamodel:expression-capable:v0:sha256:"
    )
    for member, replacement in (
        ("domain", "malleus.contract-metamodel/composition/v1"),
        ("operator", "changed composition operator"),
    ):
        changed_combined = dict(combined)
        changed_combined[member] = replacement
        assert content_id(combined_prefix, changed_combined) != combined_id

    alternative_pairs = [
        (block, value)
        for block, value in zip(blocks, values)
        if value.get("domain") == "malleus.exactly-one-alternative-semantics/v0"
    ]
    assert len(alternative_pairs) == 2
    alternative_pairs.sort(key=lambda pair: pair[1]["conditions"][0]["slot"])
    alternative_blocks = [pair[0] for pair in alternative_pairs]
    alternative_semantics = [pair[1] for pair in alternative_pairs]
    assert [value["conditions"][0]["slot"] for value in alternative_semantics] == [
        "https://example.malleus.dev/domain/left_value",
        "https://example.malleus.dev/domain/right_value",
    ]
    alternative_digests = [
        "sha256:" + hashlib.sha256(block.encode("utf-8")).hexdigest()
        for block in alternative_blocks
    ]
    assert alternative_digests == [
        "sha256:10f5b3992c471304ed0382e000f93ff6ef2aa0240bc1501dfae25e834267016a",
        "sha256:1c8099c0364055a950dd2ff3eaecfbd4554fb8199ff3f0af2be0679d25d1bbb9",
    ]

    group_block, group_envelope = one(
        "malleus.contract-structure.exactly-one-group/v0"
    )
    alternative_block, alternative_envelope = one(
        "malleus.contract-structure.exactly-one-alternative/v0"
    )
    condition_block, condition_envelope = one(
        "malleus.contract-structure.slot-condition/v0"
    )
    assert group_envelope == {
        "alternative_semantic_digests": sorted(alternative_digests),
        "class": "https://example.malleus.dev/domain/ChoiceCarrier",
        "domain": "malleus.contract-structure.exactly-one-group/v0",
    }
    group = (
        "urn:malleus:contract-structure:exactly-one-group:v0:sha256:"
        + hashlib.sha256(group_block.encode("utf-8")).hexdigest()
    )
    assert group == (
        "urn:malleus:contract-structure:exactly-one-group:v0:sha256:"
        "7c7fff294828d255018a04f67dfd0d2f86307867882e07866a25c1bfc7cca1f1"
    )
    assert alternative_envelope == {
        "alternative_semantic_digest": alternative_digests[0],
        "domain": "malleus.contract-structure.exactly-one-alternative/v0",
        "group": group,
    }
    alternative = (
        "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:"
        + hashlib.sha256(alternative_block.encode("utf-8")).hexdigest()
    )
    assert alternative == (
        "urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:"
        "15c008ee7b1dc89621e92acf93bb0f2d572102aa5430569af899e656da375b81"
    )
    assert condition_envelope == {
        "alternative": alternative,
        "domain": "malleus.contract-structure.slot-condition/v0",
        "slot": "https://example.malleus.dev/domain/left_value",
    }
    condition = (
        "urn:malleus:contract-structure:slot-condition:v0:sha256:"
        + hashlib.sha256(condition_block.encode("utf-8")).hexdigest()
    )
    assert condition == (
        "urn:malleus:contract-structure:slot-condition:v0:sha256:"
        "7c973812ba4ba438f046cf89fd3038fe41a218c2fc4ebb0dd67b578a5a681e7a"
    )

    reversed_group = dict(group_envelope)
    reversed_group["alternative_semantic_digests"] = sorted(
        reversed(group_envelope["alternative_semantic_digests"])
    )
    assert canonical_json(reversed_group) == group_block


def test_od008_composition_is_one_closed_mixed_rule_union() -> None:
    rdf_type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    cf = "https://malleus.dev/contract-facts/"

    def rule_pairs(rows: tuple[tuple[str, ...], ...]) -> tuple[tuple[str, str], ...]:
        pairs: list[tuple[str, str]] = []
        for kind_cell, predicate_cell, _, _ in rows:
            predicate = predicate_cell.replace("`", "")
            if predicate == "rdf:type":
                predicate = rdf_type
            elif predicate == "rdfs:subClassOf":
                predicate = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
            elif predicate.startswith("cf:"):
                predicate = cf + predicate.removeprefix("cf:")
            pairs.extend(
                (kind.strip(), predicate)
                for kind in kind_cell.replace("`", "").split(",")
            )
        return tuple(pairs)

    base_pairs = rule_pairs(OD005_SEED_ROWS)
    extension_pairs = rule_pairs(OD008_EXPRESSION_ROWS)

    def compose(
        base: tuple[tuple[str, str], ...],
        extension: tuple[tuple[str, str], ...],
    ) -> set[tuple[str, str]]:
        rows = (*base, *extension)
        if len(set(rows)) != len(rows):
            raise ValueError("duplicate kind-predicate composition row")
        return set(rows)

    active = compose(base_pairs, extension_pairs)
    assert set(base_pairs).isdisjoint(extension_pairs)
    with pytest.raises(ValueError, match="duplicate kind-predicate"):
        compose(base_pairs, (*extension_pairs, base_pairs[0]))

    facts = [
        ("C", "Class", rdf_type, cf + "Class"),
        ("C", "Class", cf + "abstract", False),
        ("C", "Class", cf + "isMixin", False),
        ("S", "Slot", rdf_type, cf + "Slot"),
        ("S", "Slot", cf + "valueRange", cf + "String"),
        ("S", "Slot", cf + "required", False),
        ("S", "Slot", cf + "multivalued", False),
        ("S", "Slot", cf + "identifier", False),
        ("S", "Slot", cf + "inlined", False),
        ("SU", "SlotUse", rdf_type, cf + "SlotUse"),
        ("SU", "SlotUse", cf + "valueRange", cf + "String"),
        ("SU", "SlotUse", cf + "required", False),
        ("SU", "SlotUse", cf + "multivalued", False),
        ("SU", "SlotUse", cf + "identifier", False),
        ("SU", "SlotUse", cf + "inlined", False),
        ("SU", "SlotUse", cf + "onClass", "C"),
        ("SU", "SlotUse", cf + "usesSlot", "S"),
        ("G", "ExactlyOneGroup", rdf_type, cf + "ExactlyOneGroup"),
        ("G", "ExactlyOneGroup", cf + "onClass", "C"),
        ("A", "ExactlyOneAlternative", rdf_type, cf + "ExactlyOneAlternative"),
        ("A", "ExactlyOneAlternative", cf + "inGroup", "G"),
        ("K", "SlotCondition", rdf_type, cf + "SlotCondition"),
        ("K", "SlotCondition", cf + "inAlternative", "A"),
        ("K", "SlotCondition", cf + "usesSlot", "S"),
        ("K", "SlotCondition", cf + "required", True),
        ("K", "SlotCondition", cf + "equalsString", "LEFT"),
    ]

    def assert_unique_declared_groups(
        group_class_pairs: list[tuple[object, object]],
    ) -> None:
        classes = [class_id for _, class_id in group_class_pairs]
        assert len(set(classes)) == len(classes)

    assert_unique_declared_groups([("G", "C"), ("G2", "C2")])
    with pytest.raises(AssertionError):
        assert_unique_declared_groups([("G", "C"), ("G2", "C")])

    def assert_closed_mixed_fact_set(rows: list[tuple[str, str, str, object]]) -> None:
        assert all((kind, predicate) in active for _, kind, predicate, _ in rows)
        subjects = {subject: kind for subject, kind, _, _ in rows}
        type_counts = {
            subject: sum(1 for fact in rows if fact[0] == subject and fact[2] == rdf_type)
            for subject in subjects
        }
        assert set(type_counts.values()) == {1}

        def targets(subject: str, predicate: str) -> list[object]:
            return [obj for sub, _, pred, obj in rows if sub == subject and pred == predicate]

        groups = [subject for subject, kind in subjects.items() if kind == "ExactlyOneGroup"]
        alternatives = [
            subject
            for subject, kind in subjects.items()
            if kind == "ExactlyOneAlternative"
        ]
        conditions = [
            subject for subject, kind in subjects.items() if kind == "SlotCondition"
        ]
        declaring_classes: list[object] = []
        for group in groups:
            on_class = targets(group, cf + "onClass")
            assert len(on_class) == 1 and subjects.get(on_class[0]) == "Class"
            declaring_classes.extend(on_class)
        assert_unique_declared_groups(list(zip(groups, declaring_classes)))
        for alternative in alternatives:
            in_group = targets(alternative, cf + "inGroup")
            assert len(in_group) == 1
            assert subjects.get(in_group[0]) == "ExactlyOneGroup"
        for condition in conditions:
            in_alternative = targets(condition, cf + "inAlternative")
            assert len(in_alternative) == 1
            assert subjects.get(in_alternative[0]) == "ExactlyOneAlternative"
            group = targets(in_alternative[0], cf + "inGroup")
            assert len(group) == 1
            declaring_class = targets(group[0], cf + "onClass")
            assert len(declaring_class) == 1
            slot = targets(condition, cf + "usesSlot")
            assert len(slot) == 1 and subjects.get(slot[0]) == "Slot"
            applicable_uses = [
                subject
                for subject, kind in subjects.items()
                if kind == "SlotUse"
                and targets(subject, cf + "onClass") == declaring_class
                and targets(subject, cf + "usesSlot") == slot
            ]
            assert len(applicable_uses) == 1
            if targets(condition, cf + "equalsString"):
                value_range = targets(applicable_uses[0], cf + "valueRange")
                assert len(value_range) == 1
                current = value_range[0]
                visited: set[object] = set()
                while subjects.get(current) == "Scalar":
                    assert current not in visited
                    visited.add(current)
                    typeof = targets(current, cf + "typeof")
                    assert len(typeof) == 1
                    current = typeof[0]
                assert current == cf + "String" or subjects.get(current) == "Enum"
        assert all(any(targets(alt, cf + "inGroup") == [group] for alt in alternatives) for group in groups)
        assert all(
            any(targets(condition, cf + "inAlternative") == [alternative] for condition in conditions)
            for alternative in alternatives
        )

    assert_closed_mixed_fact_set(facts)
    with pytest.raises(AssertionError):
        assert_closed_mixed_fact_set(
            [*facts, ("X", "FourthKind", rdf_type, cf + "FourthKind")]
        )
    with pytest.raises(AssertionError):
        assert_closed_mixed_fact_set(
            [*facts, ("K", "SlotCondition", cf + "experimental", "x")]
        )
    for predicate, replacement in (
        (cf + "inGroup", "missing-group"),
        (cf + "inAlternative", "missing-alternative"),
        (cf + "usesSlot", "missing-slot"),
    ):
        dangling = [
            (subject, kind, pred, replacement if pred == predicate else obj)
            for subject, kind, pred, obj in facts
        ]
        with pytest.raises(AssertionError):
            assert_closed_mixed_fact_set(dangling)
    wrong_class = [
        (subject, kind, predicate, "missing-class" if subject == "SU" and predicate == cf + "onClass" else obj)
        for subject, kind, predicate, obj in facts
    ]
    with pytest.raises(AssertionError):
        assert_closed_mixed_fact_set(wrong_class)
    with pytest.raises(AssertionError):
        assert_closed_mixed_fact_set(
            [
                *facts,
                ("G2", "ExactlyOneGroup", rdf_type, cf + "ExactlyOneGroup"),
                ("G2", "ExactlyOneGroup", cf + "onClass", "C"),
            ]
        )


def test_od008_constraint_ranges_preserve_direct_primitives_and_scalar_chains() -> None:
    scalar_terminal = {
        "StringScalar": "String",
        "IntegerScalar": "Integer",
        "FloatScalar": "Float",
        "BooleanScalar": "Boolean",
    }

    def terminal(range_name: str) -> str:
        return scalar_terminal.get(range_name, range_name)

    def admits_equals_string(range_name: str) -> bool:
        return range_name.startswith("Enum:") or terminal(range_name) == "String"

    def admits_bound(range_name: str) -> bool:
        return terminal(range_name) in {"Integer", "Float"}

    assert all(
        admits_equals_string(name) for name in ("String", "StringScalar", "Enum:State")
    )
    assert not any(
        admits_equals_string(name) for name in ("Integer", "BooleanScalar")
    )
    assert all(
        admits_bound(name)
        for name in ("Integer", "Float", "IntegerScalar", "FloatScalar")
    )
    assert not any(admits_bound(name) for name in ("String", "BooleanScalar"))


def test_od008_expression_identity_ignores_branch_condition_and_member_order() -> None:
    rdf_type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    cf = "https://malleus.dev/contract-facts/"
    class_id = "https://example.malleus.dev/domain/ChoiceCarrier"

    def structural_id(prefix: str, envelope: dict[str, object]) -> str:
        digest = hashlib.sha256(canonical_json(envelope).encode("utf-8")).hexdigest()
        return f"urn:malleus:contract-structure:{prefix}:v0:sha256:{digest}"

    def compile_expression(
        alternatives: list[list[dict[str, object]]],
    ) -> tuple[str, tuple[str, ...], tuple[str, ...], str]:
        semantic_alternatives: list[tuple[str, list[dict[str, object]]]] = []
        for conditions in alternatives:
            normalized = sorted(
                (dict(condition) for condition in conditions),
                key=canonical_json,
            )
            semantic = {
                "conditions": normalized,
                "domain": "malleus.exactly-one-alternative-semantics/v0",
            }
            digest = "sha256:" + hashlib.sha256(
                canonical_json(semantic).encode("utf-8")
            ).hexdigest()
            semantic_alternatives.append((digest, normalized))
        semantic_alternatives.sort(key=lambda item: item[0])
        group = structural_id(
            "exactly-one-group",
            {
                "alternative_semantic_digests": [
                    digest for digest, _ in semantic_alternatives
                ],
                "class": class_id,
                "domain": "malleus.contract-structure.exactly-one-group/v0",
            },
        )
        facts: list[dict[str, object]] = [
            {"subject": group, "predicate": rdf_type, "object": cf + "ExactlyOneGroup"},
            {"subject": group, "predicate": cf + "onClass", "object": class_id},
        ]
        alternative_ids: list[str] = []
        condition_ids: list[str] = []
        for semantic_digest, conditions in semantic_alternatives:
            alternative = structural_id(
                "exactly-one-alternative",
                {
                    "alternative_semantic_digest": semantic_digest,
                    "domain": "malleus.contract-structure.exactly-one-alternative/v0",
                    "group": group,
                },
            )
            alternative_ids.append(alternative)
            facts.extend(
                (
                    {
                        "subject": alternative,
                        "predicate": rdf_type,
                        "object": cf + "ExactlyOneAlternative",
                    },
                    {
                        "subject": alternative,
                        "predicate": cf + "inGroup",
                        "object": group,
                    },
                )
            )
            for semantics in conditions:
                slot = semantics["slot"]
                assert isinstance(slot, str)
                condition = structural_id(
                    "slot-condition",
                    {
                        "alternative": alternative,
                        "domain": "malleus.contract-structure.slot-condition/v0",
                        "slot": slot,
                    },
                )
                condition_ids.append(condition)
                facts.extend(
                    (
                        {
                            "subject": condition,
                            "predicate": rdf_type,
                            "object": cf + "SlotCondition",
                        },
                        {
                            "subject": condition,
                            "predicate": cf + "inAlternative",
                            "object": alternative,
                        },
                        {
                            "subject": condition,
                            "predicate": cf + "usesSlot",
                            "object": slot,
                        },
                    )
                )
                for member, predicate in (
                    ("required", "required"),
                    ("equalsString", "equalsString"),
                    ("valuePresence", "valuePresence"),
                ):
                    if member in semantics:
                        facts.append(
                            {
                                "subject": condition,
                                "predicate": cf + predicate,
                                "object": semantics[member],
                            }
                        )
        return (
            group,
            tuple(sorted(alternative_ids)),
            tuple(sorted(condition_ids)),
            canonical_json(sorted(facts, key=canonical_json)),
        )

    left = {
        "slot": "https://example.malleus.dev/domain/left_value",
        "required": True,
        "equalsString": "LEFT",
    }
    right = {
        "slot": "https://example.malleus.dev/domain/right_value",
        "valuePresence": "PRESENT",
    }
    fallback = {
        "slot": "https://example.malleus.dev/domain/fallback_value",
        "valuePresence": "PRESENT",
    }
    baseline = compile_expression([[left, right], [fallback]])
    reordered_left = {
        "equalsString": "LEFT",
        "required": True,
        "slot": "https://example.malleus.dev/domain/left_value",
    }
    permuted = compile_expression([[fallback], [right, reordered_left]])
    assert baseline == permuted


def test_od008_default_and_identifier_truth_tables_are_exact() -> None:
    def effective_inlined(
        *, explicit: bool | None, range_kind: str, target_identifiers: int
    ) -> bool:
        if range_kind == "Class" and target_identifiers > 1:
            raise ValueError("multiple effective identifiers")
        if explicit is not None:
            if explicit and range_kind != "Class":
                raise ValueError("D05 Class-only inlined guard")
            return explicit
        if range_kind != "Class":
            return False
        return target_identifiers == 0

    assert effective_inlined(
        explicit=None, range_kind="String", target_identifiers=0
    ) is False
    assert effective_inlined(
        explicit=None, range_kind="Class", target_identifiers=1
    ) is False
    assert effective_inlined(
        explicit=None, range_kind="Class", target_identifiers=0
    ) is True
    assert effective_inlined(
        explicit=False, range_kind="String", target_identifiers=0
    ) is False
    with pytest.raises(ValueError, match="multiple effective identifiers"):
        effective_inlined(explicit=None, range_kind="Class", target_identifiers=2)
    with pytest.raises(ValueError, match="multiple effective identifiers"):
        effective_inlined(explicit=False, range_kind="Class", target_identifiers=2)
    with pytest.raises(ValueError, match="multiple effective identifiers"):
        effective_inlined(explicit=True, range_kind="Class", target_identifiers=2)
    with pytest.raises(ValueError, match="Class-only"):
        effective_inlined(explicit=True, range_kind="String", target_identifiers=0)

    def effective_required(
        *, identifier: bool, required: bool | None
    ) -> bool:
        if identifier and required is False:
            raise ValueError("explicit required=false conflicts with identifier=true")
        return identifier if required is None else required

    assert effective_required(identifier=False, required=None) is False
    assert effective_required(identifier=True, required=None) is True
    assert effective_required(identifier=False, required=False) is False
    with pytest.raises(ValueError, match="conflicts"):
        effective_required(identifier=True, required=False)


def test_od008_expression_admission_and_inheritance_are_exact() -> None:
    def admit_condition(
        *,
        applicable: bool,
        range_kind: str,
        required: bool | None = None,
        equals_string: str | None = None,
        value_presence: str | None = None,
    ) -> tuple[tuple[str, object], ...]:
        if not applicable:
            raise ValueError("slot has no declaring-class effective SlotUse")
        if equals_string is not None and range_kind not in {"String", "Enum"}:
            raise ValueError("equalsString range")
        if value_presence == "ABSENT" and (
            required is True or equals_string is not None
        ):
            raise ValueError("condition contradiction")
        members = {
            "equalsString": equals_string,
            "required": required,
            "valuePresence": value_presence,
        }
        result = tuple(sorted((key, value) for key, value in members.items() if value is not None))
        if not result:
            raise ValueError("empty condition")
        return result

    assert admit_condition(applicable=True, range_kind="String", equals_string="A")
    assert admit_condition(applicable=True, range_kind="Enum", equals_string="OPEN")
    assert admit_condition(applicable=True, range_kind="Integer", required=True)
    with pytest.raises(ValueError, match="effective SlotUse"):
        admit_condition(applicable=False, range_kind="String", required=True)
    with pytest.raises(ValueError, match="range"):
        admit_condition(applicable=True, range_kind="Integer", equals_string="1")
    with pytest.raises(ValueError, match="contradiction"):
        admit_condition(
            applicable=True,
            range_kind="String",
            equals_string="A",
            value_presence="ABSENT",
        )

    # Separate branches may narrow differently. V0 performs no cross-branch analysis.
    assert admit_condition(applicable=True, range_kind="String", equals_string="A")
    assert admit_condition(applicable=True, range_kind="String", equals_string="B")

    ancestor_group = "urn:malleus:contract-structure:exactly-one-group:v0:sha256:ancestor"
    local_group = "urn:malleus:contract-structure:exactly-one-group:v0:sha256:local"
    applied_on_child = (ancestor_group, local_group)
    assert applied_on_child[0] == ancestor_group
    assert len(set(applied_on_child)) == 2


def test_od008_annotation_only_mixin_changes_preserve_semantics() -> None:
    enforced_fields = {
        "equals_string",
        "identifier",
        "inlined",
        "maximum_value",
        "minimum_value",
        "multivalued",
        "range",
        "required",
        "value_presence",
    }

    def project(mixins: list[dict[str, object]]) -> tuple[str, str]:
        semantic: dict[str, object] = {}
        for mixin in mixins:
            for field in enforced_fields & mixin.keys():
                if field in semantic and semantic[field] != mixin[field]:
                    raise ValueError("conflicting ENFORCED values")
                semantic[field] = mixin[field]
        source_attestation = hashlib.sha256(
            canonical_json(mixins).encode("utf-8")
        ).hexdigest()
        semantic_identity = hashlib.sha256(
            canonical_json(semantic).encode("utf-8")
        ).hexdigest()
        return source_attestation, semantic_identity

    baseline = [
        {"description": "first prose", "required": True},
        {"description": "second prose", "required": True},
    ]
    edited = [
        {"description": "changed prose", "required": True},
        {"required": True},
    ]
    baseline_source, baseline_semantics = project(baseline)
    edited_source, edited_semantics = project(edited)
    assert baseline_source != edited_source
    assert baseline_semantics == edited_semantics
    with pytest.raises(ValueError, match="ENFORCED"):
        project([{"required": True}, {"required": False}])


def test_od008_symbol_metadata_erasure_and_schema_identity_are_mechanical() -> None:
    def projection(schema: dict[str, str]) -> tuple[str, str, str]:
        class_id = schema["id"] + "/Record"
        slot_id = schema["id"] + "/value"
        fact = {
            "object": "https://malleus.dev/contract-facts/Class",
            "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "subject": class_id,
        }
        envelope = {
            "canonicalization_profile": (
                "malleus.canonical-json/d05-compact-sorted-key-utf8-no-newline/v0"
            ),
            "domain": "malleus.contract-fact/candidate-v0",
            "fact": fact,
            "metamodel": OD008_COMBINED_METAMODEL_ID,
            "symbol_policy": OD008_SYMBOL_POLICY_ID,
        }
        source_attestation = hashlib.sha256(
            canonical_json(schema).encode("utf-8")
        ).hexdigest()
        candidate = hashlib.sha256(canonical_json(envelope).encode("utf-8")).hexdigest()
        return canonical_json((class_id, slot_id, fact)), candidate, source_attestation

    baseline = {
        "id": "https://example.test/schema",
        "name": "one",
        "version": "1",
    }
    metadata_edit = {**baseline, "name": "two", "version": "2"}
    identity_edit = {**baseline, "id": "https://example.test/other"}
    baseline_projection, baseline_candidate, baseline_source = projection(baseline)
    metadata_projection, metadata_candidate, metadata_source = projection(metadata_edit)
    identity_projection, identity_candidate, _ = projection(identity_edit)
    assert metadata_projection == baseline_projection
    assert metadata_candidate == baseline_candidate
    assert metadata_source != baseline_source
    assert identity_projection != baseline_projection
    assert identity_candidate != baseline_candidate


def test_od008_closed_profile_rejects_adversarial_drift() -> None:
    decisions = (
        ROOT / "design" / "contract_compiler" / "decisions.md"
    ).read_text(encoding="utf-8")
    section = _od008_section(decisions)
    class_row = next(
        line for line in section.splitlines() if line.startswith("| `classes.<class>` |")
    )
    expression_row = next(
        line
        for line in section.splitlines()
        if line.startswith("| `SlotCondition` | `cf:valuePresence`")
    )
    mutations = (
        section.replace(
            class_row,
            class_row.replace("`class_uri`, `description`", "`description`"),
            1,
        ),
        section.replace(
            "including `annotations.retires`",
            "excluding `annotations.retires`",
            1,
        ),
        section.replace(
            "emits no adoption fact",
            "emits one adoption fact",
            1,
        ),
        section.replace(
            class_row,
            class_row.replace("`exactly_one_of`", "`exactly_one_of`, `rules`"),
            1,
        ),
        section.replace(expression_row, "", 1),
        section.replace(
            expression_row,
            expression_row
            + "\n| `SlotCondition` | `cf:experimental` | string | 0..1 |",
            1,
        ),
        section.replace("Source indexes never enter identity.", "", 1),
        section.replace("current = stack.pop_last()", "current = stack.pop_first()", 1),
        section.replace(
            "no other base-slot or branch narrowing is declared\ncontradictory",
            "All base-slot narrowing is contradictory",
            1,
        ),
        section.replace(
            "public docstrings,\nnamespace placement, stable public fact identifiers, and public support claims\nremain blocked on `OD-009`.",
            "public support is promoted now.",
            1,
        ),
    )
    assert all(mutation != section for mutation in mutations)
    for mutation in mutations:
        with pytest.raises(AssertionError):
            _assert_od008_closed_profile(mutation)


def test_od008_profile_covers_retained_source_shapes_exactly() -> None:
    bundled = (
        ROOT / "ontology" / "malleus.yaml",
        ROOT / "ontology" / "assent.yaml",
        *sorted((ROOT / "ontology" / "domains").glob("*.yaml")),
    )
    assert len(bundled) == 6
    sources = [path.read_text(encoding="utf-8") for path in bundled]
    cases = json.loads(
        (
            ROOT
            / "conformance"
            / "contract_compiler"
            / "v0"
            / "linkml_legacy_divergence"
            / "cases.json"
        ).read_text(encoding="utf-8")
    )["cases"]
    assert len(cases) == 9
    sources.extend(case["source_text"] for case in cases)
    documents = [_od008_assert_raw_source_grammar(source) for source in sources]
    for document in documents:
        _od008_assert_exact_value_types(document)

    outcomes = {vector: outcome for vector, outcome, _ in OD008_CORPUS_ROWS}
    bundled_relatives = tuple(path.relative_to(ROOT).as_posix() for path in bundled)
    assert {path: outcomes[path] for path in bundled_relatives} == {
        path: "ACCEPT" for path in bundled_relatives
    }
    case_outcomes = {
        vector.removeprefix("CC-X01/"): outcome
        for vector, outcome in outcomes.items()
        if vector.startswith("CC-X01/")
    }
    assert case_outcomes == {
        "attribute_slot_usage": "ACCEPT",
        "conflicting_mixins_ab": "REFUSE",
        "conflicting_mixins_ba": "REFUSE",
        "default_range": "ACCEPT",
        "explicit_false": "REFUSE",
        "numeric_bounds": "ACCEPT",
        "parent_mixin_precedence": "ACCEPT",
        "repeated_mixin": "REFUSE",
        "simple_parity": "ACCEPT",
    }
    case_documents = {
        case["case_id"]: document for case, document in zip(cases, documents[6:])
    }
    repeated = case_documents["repeated_mixin"]
    assert repeated["classes"]["Child"]["mixins"] == ["MixinA", "MixinA"]
    for case_id, order in (
        ("conflicting_mixins_ab", ["MixinA", "MixinB"]),
        ("conflicting_mixins_ba", ["MixinB", "MixinA"]),
    ):
        conflicting = case_documents[case_id]
        assert conflicting["classes"]["Child"]["mixins"] == order
        assert {
            conflicting["classes"][name]["slot_usage"]["value"]["range"]
            for name in order
        } == {"integer", "float"}
    measured_false = case_documents["explicit_false"]
    assert measured_false["slots"]["value"]["range"] == "string"
    assert measured_false["slots"]["value"]["inlined"] is True
    assert measured_false["classes"]["Thing"]["slot_usage"]["value"] == {
        "identifier": False,
        "inlined": False,
        "multivalued": False,
        "required": False,
    }

    builtin_names = {row[0] for row in OD008_BUILTIN_ROWS}
    observed_range_references: set[str] = set()

    def collect_builtins(value: object, field: str | None = None) -> None:
        if isinstance(value, dict):
            for key, member in value.items():
                collect_builtins(member, key)
        elif isinstance(value, list):
            for member in value:
                collect_builtins(member, field)
        elif field in {"default_range", "range", "typeof"}:
            assert isinstance(value, str)
            observed_range_references.add(value)

    for document in documents:
        collect_builtins(document)
    retained_wheel = (
        ROOT
        / "conformance"
        / "contract_compiler"
        / "v0"
        / "compiler_environment"
        / "roots"
        / "linkml_runtime-1.11.1-py3-none-any.whl"
    )
    wheel_bytes = retained_wheel.read_bytes()
    assert hashlib.sha256(wheel_bytes).hexdigest() == (
        "b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da"
    )
    member_path = "linkml_runtime/linkml_model/model/schema/types.yaml"
    with zipfile.ZipFile(retained_wheel) as archive:
        member = archive.read(member_path)
        assert archive.namelist().count(member_path) == 1
    assert len(member) == 7296
    assert hashlib.sha256(member).hexdigest() == (
        "1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00"
    )
    upstream_types = set(yaml.safe_load(member)["types"])

    def upstream_references(references: set[str]) -> set[str]:
        return references & upstream_types

    assert upstream_references(observed_range_references) == builtin_names
    assert upstream_references(observed_range_references | {"decimal"}) != builtin_names

    observed, permissible_body_types, null_permissible_values = (
        _od008_source_shape_inventory(documents)
    )

    assert observed == {
        "schema": {
            "classes",
            "default_range",
            "description",
            "enums",
            "id",
            "imports",
            "name",
            "prefixes",
            "slots",
            "title",
            "types",
            "version",
        },
        "type": {"description", "typeof", "uri"},
        "enum": {"description", "permissible_values"},
        "permissible_value": {"description"},
        "slot": {
            "annotations",
            "description",
            "identifier",
            "inlined",
            "maximum_value",
            "minimum_value",
            "multivalued",
            "range",
            "required",
        },
        "class": {
            "abstract",
            "attributes",
            "class_uri",
            "description",
            "exactly_one_of",
            "is_a",
            "mixin",
            "mixins",
            "slot_usage",
            "slots",
        },
        "attribute": {"range", "required"},
        "slot_usage": {
            "description",
            "equals_string",
            "identifier",
            "inlined",
            "maximum_value",
            "minimum_value",
            "multivalued",
            "range",
            "required",
        },
        "alternative": {"slot_conditions"},
        "condition": {"equals_string", "required", "value_presence"},
        "slot_annotation": {"adopts"},
    }
    assert permissible_body_types == {dict, type(None)}
    assert null_permissible_values > 0

    allowed = {
        "schema": {
            "id",
            "name",
            "version",
            "prefixes",
            "imports",
            "default_range",
            "title",
            "description",
            "types",
            "enums",
            "slots",
            "classes",
        },
        "type": {"typeof", "uri", "description"},
        "enum": {"permissible_values", "description"},
        "permissible_value": {"description"},
        "slot": {
            "range",
            "required",
            "multivalued",
            "identifier",
            "inlined",
            "equals_string",
            "minimum_value",
            "maximum_value",
            "value_presence",
            "description",
            "annotations",
        },
        "class": {
            "is_a",
            "mixin",
            "mixins",
            "abstract",
            "slots",
            "attributes",
            "slot_usage",
            "exactly_one_of",
            "class_uri",
            "description",
        },
        "attribute": {
            "range",
            "required",
            "multivalued",
            "identifier",
            "inlined",
            "equals_string",
            "minimum_value",
            "maximum_value",
            "value_presence",
            "description",
        },
        "slot_usage": {
            "range",
            "required",
            "multivalued",
            "identifier",
            "inlined",
            "equals_string",
            "minimum_value",
            "maximum_value",
            "value_presence",
            "description",
        },
        "alternative": {"slot_conditions"},
        "condition": {"required", "equals_string", "value_presence"},
        "slot_annotation": {"adopts"},
    }
    assert all(observed[location] <= keys for location, keys in allowed.items())

    for document in documents:
        for declaration in (document.get("slots") or {}).values():
            annotations = (declaration or {}).get("annotations")
            if annotations is not None:
                assert annotations == {"adopts": True}


@pytest.mark.parametrize(
    "document",
    (
        {"types": {"T": None}},
        {"enums": {"E": None}},
        {"slots": {"s": None}},
        {"classes": {"C": None}},
        {"classes": {"C": {"attributes": {"a": None}}}},
        {"classes": {"C": {"slot_usage": {"s": None}}}},
        {"classes": {"C": {"exactly_one_of": [None]}}},
        {
            "classes": {
                "C": {
                    "exactly_one_of": [
                        {"slot_conditions": {"s": None}},
                    ]
                }
            }
        },
        {"enums": {"E": {"permissible_values": {"X": "not-a-map"}}}},
        {
            "enums": {
                "E": {"permissible_values": {"X": {"description": None}}}
            }
        },
    ),
)
def test_od008_source_shape_guard_rejects_null_or_wrong_bodies(
    document: dict[str, object],
) -> None:
    with pytest.raises(AssertionError):
        _od008_source_shape_inventory([document])


def test_od008_null_permissible_value_is_one_exact_empty_declaration() -> None:
    observed, body_types, null_count = _od008_source_shape_inventory(
        [{"enums": {"E": {"permissible_values": {"EMPTY": None}}}}]
    )
    assert body_types == {type(None)}
    assert null_count == 1
    assert observed["permissible_value"] == set()


@pytest.mark.parametrize(
    "lexeme",
    ("0", "-0", "5", "5.0", "5e0", "5E-2", "1e+3", "-12.34"),
)
def test_od008_exact_source_number_grammar_accepts_json_numbers(lexeme: str) -> None:
    assert _od008_is_json_number_lexeme(lexeme)
    document = _od008_assert_raw_source_grammar(
        "id: https://example.test/schema\n"
        "name: numeric\n"
        "slots:\n"
        "  count:\n"
        "    minimum_value: "
        + lexeme
        + "\n"
    )
    _od008_assert_exact_value_types(document)
    bound = document["slots"]["count"]["minimum_value"]
    assert bound == Decimal(lexeme)


@pytest.mark.parametrize(
    "lexeme",
    (
        "+1",
        "01",
        "0x10",
        "1_0",
        "1:20",
        ".5",
        "1.",
        ".inf",
        ".nan",
        "1١",
        '"1"',
    ),
)
def test_od008_exact_source_number_grammar_refuses_non_json_numbers(
    lexeme: str,
) -> None:
    assert not _od008_is_json_number_lexeme(lexeme.strip('"')) or lexeme == '"1"'
    with pytest.raises(AssertionError):
        _od008_assert_raw_source_grammar(
            "id: https://example.test/schema\n"
            "name: numeric\n"
            "slots:\n"
            "  count:\n"
            "    minimum_value: "
            + lexeme
            + "\n"
        )


@pytest.mark.parametrize("lexeme", ("true", "false"))
def test_od008_raw_boolean_grammar_accepts_lowercase_only(lexeme: str) -> None:
    document = _od008_assert_raw_source_grammar(
        "id: https://example.test/schema\n"
        "name: boolean\n"
        "slots:\n"
        "  value:\n"
        "    required: "
        + lexeme
        + "\n"
    )
    _od008_assert_exact_value_types(document)


@pytest.mark.parametrize(
    "lexeme",
    ('"false"', "False", "FALSE", "yes", "on"),
)
def test_od008_raw_boolean_grammar_refuses_quoted_or_yaml_spellings(
    lexeme: str,
) -> None:
    with pytest.raises(AssertionError):
        _od008_assert_raw_source_grammar(
            "id: https://example.test/schema\n"
            "name: boolean\n"
            "slots:\n"
            "  value:\n"
            "    required: "
            + lexeme
            + "\n"
        )


@pytest.mark.parametrize("body", ("", "null"))
def test_od008_raw_permissible_value_empty_forms_are_exact(body: str) -> None:
    source = (
        "id: https://example.test/schema\n"
        "name: enum\n"
        "enums:\n"
        "  State:\n"
        "    permissible_values:\n"
        "      OPEN:"
        + ("\n" if not body else f" {body}\n")
    )
    document = _od008_assert_raw_source_grammar(source)
    _od008_assert_exact_value_types(document)


@pytest.mark.parametrize("body", ("~", "Null", "NULL"))
def test_od008_raw_permissible_value_refuses_yaml_only_nulls(body: str) -> None:
    with pytest.raises(AssertionError):
        _od008_assert_raw_source_grammar(
            "id: https://example.test/schema\n"
            "name: enum\n"
            "enums:\n"
            "  State:\n"
            "    permissible_values:\n"
            f"      OPEN: {body}\n"
        )


@pytest.mark.parametrize(
    "source",
    (
        "id: https://example.test/schema\nname: one\nname: two\n",
        "id: https://example.test/schema\nname: &name one\ntitle: *name\n",
        "id: https://example.test/schema\nname: one\nclasses:\n  C:\n    <<: {}\n",
        "id: https://example.test/schema\nname: !custom one\n",
        "1: value\nid: https://example.test/schema\nname: one\n",
        "---\nid: https://example.test/schema\nname: one\n",
        "%YAML 1.2\n---\nid: https://example.test/schema\nname: one\n",
        "id: https://example.test/schema\nname: one\n...\n",
        "id: https://example.test/schema\nname: one\n---\nid: https://example.test/other\nname: two\n",
        "id: https://example.test/schema\nname: null\n",
        "scalar\n",
        "- item\n",
    ),
)
def test_od008_raw_source_guard_refuses_yaml_expansion_and_nulls(source: str) -> None:
    with pytest.raises(AssertionError):
        _od008_assert_raw_source_grammar(source)


@pytest.mark.parametrize(
    ("source", "token_type"),
    (
        (
            "id: https://example.test/schema\nname: &name one\n",
            yaml.tokens.AnchorToken,
        ),
        (
            "id: https://example.test/schema\nname: *missing\n",
            yaml.tokens.AliasToken,
        ),
        (
            "%YAML 1.2\n---\nid: https://example.test/schema\nname: one\n",
            yaml.tokens.DirectiveToken,
        ),
        (
            "id: https://example.test/schema\nname: !!str one\n",
            yaml.tokens.TagToken,
        ),
    ),
)
def test_od008_raw_source_guard_refuses_each_yaml_structure_token(
    source: str, token_type: type[yaml.tokens.Token]
) -> None:
    assert any(isinstance(token, token_type) for token in yaml.scan(source))
    with pytest.raises(AssertionError):
        _od008_assert_raw_source_grammar(source)


@pytest.mark.parametrize(
    "source",
    (
        "id: https://example.test/schema\nname: one\nclasses:\n  C: null\n",
        "id: https://example.test/schema\nname: one\nclasses:\n  C:\n    exactly_one_of:\n      - null\n",
        "id: https://example.test/schema\nname: one\nslots:\n  s: {}\nclasses:\n  C:\n    slots: [s]\n    exactly_one_of:\n      - slot_conditions:\n          s: null\n",
        "id: https://example.test/schema\nname: one\nenums:\n  E:\n    permissible_values:\n      V: text\n",
    ),
)
def test_od008_raw_source_bytes_refuse_wrong_body_shapes(source: str) -> None:
    with pytest.raises(AssertionError):
        document = _od008_assert_raw_source_grammar(source)
        _od008_assert_exact_value_types(document)


@pytest.mark.parametrize(
    "source",
    (
        "id: https://example.test/schema\nname: one\nimports: linkml:types\n",
        "id: https://example.test/schema\nname: one\nclasses:\n  C:\n    mixins: M\n",
        'id: https://example.test/schema\nname: one\nslots:\n  s:\n    required: "false"\n',
    ),
)
def test_od008_exact_value_types_refuse_linkml_coercions(source: str) -> None:
    with pytest.raises(AssertionError):
        document = _od008_assert_raw_source_grammar(source)
        _od008_assert_exact_value_types(document)


@pytest.mark.parametrize(
    "source",
    (
        "id: relative\nname: one\n",
        "id: https://example.test/schema\n",
        "name: one\n",
        "id: urn:foo bar\nname: one\n",
        "id: https://example.test/a b\nname: one\n",
        'id: "https://example.test/schema\\n"\nname: one\n',
        "id: https://example.test/schema?query\nname: one\n",
        "id: https://example.test/schema#fragment\nname: one\n",
        "id: https://example.test/schema/\nname: one\n",
        "id: https://example.test/schema\nname: one\nbogus: x\n",
        "id: https://example.test/schema\nname: one\nclasses:\n  É: {}\n",
        "id: https://example.test/schema\nname: one\nclasses:\n  bad-key: {}\n",
        "id: https://example.test/schema\nname: one\nclasses:\n  C:\n    bogus: x\n",
        "id: https://example.test/schema\nname: one\ntypes:\n  T:\n    typeof: string\n    bogus: x\n",
        "id: https://example.test/schema\nname: one\nenums:\n  E:\n    bogus: x\n",
        "id: https://example.test/schema\nname: one\nenums:\n  E:\n    permissible_values:\n      V:\n        bogus: x\n",
        "id: https://example.test/schema\nname: one\nprefixes:\n  É: https://example.test/\n",
        "id: https://example.test/schema\nname: one\nprefixes:\n  ex: relative\n",
        "id: https://example.test/schema\nname: one\nprefixes:\n  ex: https://example.test/a b/\n",
        'id: https://example.test/schema\nname: one\nslots:\n  s:\n    range: ""\n',
        "id: https://example.test/schema\nname: one\nslots:\n  s:\n    bogus: x\n",
        "id: https://example.test/schema\nname: one\nslots:\n  s:\n    annotations:\n      adopts: true\n      bogus: true\n",
        "id: https://example.test/schema\nname: one\nslots:\n  s:\n    range: ex:Thing\n",
        "id: https://example.test/schema\nname: one\nprefixes:\n  ex: https://example.test/\nslots:\n  s:\n    range: ex:Thing:Extra\n",
        "id: https://example.test/schema\nname: one\nslots:\n  s:\n    range: Thíng\n",
        "id: https://example.test/schema\nname: one\nslots:\n  s: {}\nclasses:\n  C:\n    slots: [s]\n    exactly_one_of:\n      - slot_conditions:\n          s:\n            bogus: true\n",
        "id: https://example.test/schema\nname: one\nclasses:\n  C:\n    attributes:\n      a:\n        bogus: x\n",
        "id: https://example.test/schema\nname: one\nslots:\n  s: {}\nclasses:\n  C:\n    slots: [s]\n    slot_usage:\n      s:\n        bogus: x\n",
        "id: https://example.test/schema\nname: one\nslots:\n  s: {}\nclasses:\n  C:\n    slots: [s]\n    exactly_one_of:\n      - slot_conditions:\n          s:\n            required: true\n        bogus: x\n",
    ),
)
def test_od008_exact_location_symbol_and_iri_guards_refuse_drift(source: str) -> None:
    document = _od008_assert_raw_source_grammar(source)
    with pytest.raises(AssertionError):
        _od008_assert_exact_value_types(document)


def test_od008_absolute_iri_guard_preserves_valid_unicode_iris() -> None:
    document = _od008_assert_raw_source_grammar(
        "id: https://example.test/café\n"
        "name: unicode\n"
        "prefixes:\n"
        "  ex: https://example.test/résumé/\n"
        "slots:\n"
        "  value:\n"
        "    range: ex:Text\n"
    )
    _od008_assert_exact_value_types(document)
    _od008_assert_exact_value_types(
        _od008_assert_raw_source_grammar("id: http:foo\nname: generic_iri\n")
    )
    _od008_assert_exact_value_types(
        _od008_assert_raw_source_grammar('id: "foo:"\nname: empty_hier_part\n')
    )
    _od008_assert_exact_value_types(
        _od008_assert_raw_source_grammar(
            'id: "https://example.test/a\u00a0b"\nname: rfc_iri_separator\n'
        )
    )


def test_revision_18_conformance_rows_guard_closed_decisions() -> None:
    rows = {
        cells[0]: line.casefold()
        for line in (
            ROOT / "design" / "contract_compiler" / "conformance.md"
        ).read_text(encoding="utf-8").splitlines()
        if line.startswith("| AT-")
        and (cells := [cell.strip() for cell in line.strip("|").split("|")])
    }

    for phrase in (
        "resolver failure never tries another profile",
        "same locator with different bytes",
        "different locators with identical bytes",
        "distinct module observations",
        "directed cycle refuse with retained lineage",
    ):
        assert phrase in rows["AT-001"]
    for phrase in (
        "adoption marker/equality refusal matrix",
        "literal boolean adoption marker",
        "exact pre-default equality",
        "every other matrix cell refuses",
    ):
        assert phrase in rows["AT-003"]
    for phrase in ("every applied default", "materialized", "provenance"):
        assert phrase in rows["AT-005"]
    for phrase in (
        "immutable d05 seed plus exact expression extension",
        "complete reified slotuse",
        "seed subject",
        "invalid bound or range",
        "identical metamodel-valid atomic facts",
        "refuse atomically",
    ):
        assert phrase in rows["AT-007"]

    program = (
        ROOT / "design" / "contract_compiler" / "program.md"
    ).read_text(encoding="utf-8").casefold()
    cc_r01 = next(line for line in program.splitlines() if line.startswith("| cc-r01 "))
    for phrase in (
        "no try-next profile",
        "same-locator/different-bytes refusal",
        "different-locator/same-bytes distinction",
        "directed-cycle lineage refusal",
    ):
        assert phrase in cc_r01


def test_contract_compiler_docs_keep_public_adapter_promotion_gated() -> None:
    index = (ROOT / "docs" / "contract_compiler" / "index.md").read_text(
        encoding="utf-8"
    )
    prose = " ".join(index.split())

    assert "No public frontend adapter or adapter docstring exists yet." in prose
    assert "Pinned LinkML 1.11.1 is the selected v0 target adapter." in prose
    assert "CC-R02 may implement and characterize" in prose
    assert "it cannot authorize public exposure." in prose
    assert "remain governed by open CC-D09/OD-009." in prose
    assert "If CC-D09/OD-009 permits promotion," in prose
    assert "When CC-R02 exposes a public adapter," not in prose
    assert "CC-R02 owns future public adapter docstrings" not in prose
    assert "Each public frontend adapter documents" not in prose
    assert "The default first-party adapter is" not in prose


def test_rdf_guard_dependency_is_an_exact_direct_dev_pin() -> None:
    try:
        import tomllib
    except ModuleNotFoundError:  # pragma: no cover - Python 3.10
        import tomli as tomllib

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    rdf_dependencies = [
        dependency
        for dependency in project["project"]["optional-dependencies"]["dev"]
        if dependency.casefold().startswith("rdflib")
    ]
    assert rdf_dependencies == ["rdflib==7.6.0"]


def test_rdf_guard_rejects_invalid_iri_and_literal_escape() -> None:
    with pytest.raises(ParserError):
        Graph().parse(
            data="<https://example/s> <https://example/p> <bad iri> .",
            format="nt",
        )
    with pytest.raises(BadSyntax):
        Graph().parse(
            data='@prefix ex: <https://example/> . ex:s ex:p "\\q" .',
            format="turtle",
        )


def test_verified_facts_do_not_claim_future_artifact_bytes() -> None:
    state = load_ledger(OVERSEER)
    superseded: set[str] = set()
    for entry in state.entries:
        if entry["entry_id"] not in superseded and entry["entry_type"] == "CORRECTION":
            superseded.add(entry["data"]["supersedes_entry_id"])
    active = [entry for entry in state.entries if entry["entry_id"] not in superseded]
    test_path = Path(__file__).relative_to(ROOT).as_posix()
    chronology_boundary = min(
        entry["sequence"]
        for entry in active
        if entry["entry_type"] == "DOCUMENT_REVISION"
        and any(
            document["path"] == test_path and document["change"] == "MODIFIED"
            for document in entry["data"]["documents"]
        )
        and any(
            document["change"] == "CREATED"
            and any(
                reference["type"] == "EVIDENCE"
                and reference["target"] == document["path"]
                for reference in entry["references"]
            )
            for document in entry["data"]["documents"]
        )
    )

    provenance: dict[str, list[tuple[int, str]]] = {}
    entry_root = OVERSEER.relative_to(ROOT) / "entries"
    for entry in state.entries:
        entry_path = entry_root / f"{entry['entry_id']}.json"
        entry_source = (ROOT / entry_path).read_bytes()
        provenance.setdefault(entry_path.as_posix(), []).append(
            (entry["sequence"], "sha256:" + hashlib.sha256(entry_source).hexdigest())
        )
        if entry["entry_type"] == "DOCUMENT_REVISION":
            for document in entry["data"]["documents"]:
                provenance.setdefault(document["path"], []).append(
                    (entry["sequence"], document["after_digest"])
                )

    facts = [
        entry
        for entry in active
        if entry["entry_type"] == "VERIFIED_FACT"
        and entry["sequence"] > chronology_boundary
    ]
    assert facts
    for fact in facts:
        evidence = [
            reference
            for reference in fact["references"]
            if reference["type"] == "EVIDENCE"
        ]
        assert evidence
        for reference in evidence:
            prior_report = [
                sequence
                for sequence, digest in provenance.get(reference["target"], [])
                if sequence < fact["sequence"] and digest == reference["digest"]
            ]
            assert prior_report, (
                f"{fact['entry_id']} claims evidence bytes before a prior "
                f"document revision: {reference['target']}"
            )
            report = json.loads(
                (ROOT / reference["target"]).read_text(encoding="utf-8")
            )
            for artifact in report["artifacts"]:
                prior_artifact = [
                    sequence
                    for sequence, digest in provenance.get(artifact["path"], [])
                    if sequence < fact["sequence"] and digest == artifact["sha256"]
                ]
                assert prior_artifact, (
                    f"{fact['entry_id']} claims artifact bytes before their active "
                    f"create/revision entry: {artifact['path']}"
                )


def test_overseer_ledger_and_projection_are_current() -> None:
    state = load_ledger(OVERSEER)

    assert state.head["entry_count"] == len(state.entries)
    assert state.head["head_entry_id"] == state.entries[-1]["entry_id"]
    assert state.head["head_hash"] == state.entries[-1]["entry_hash"]
    rendered = render_status(state)
    assert rendered == (OVERSEER / "status.md").read_text(encoding="utf-8")
    assert all(not line.endswith(" ") for line in rendered.splitlines())


def test_suffix_truncation_is_caught_by_separate_local_head(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    (copied / "entries" / "OVR-000006.json").unlink()

    with pytest.raises(LedgerValidationError, match="entry_count"):
        load_ledger(copied)


def test_entry_tampering_breaks_the_hash_chain(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(target, lambda value: value.update(summary="tampered"), rehash=False)

    with pytest.raises(LedgerValidationError, match="entry_hash"):
        load_ledger(copied)


def test_duplicate_json_keys_fail_closed(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    text = target.read_text(encoding="utf-8")
    target.write_text(
        text.replace(
            '"ledger": "overseer"', '"ledger": "overseer",\n  "ledger": "overseer"'
        ),
        encoding="utf-8",
    )

    with pytest.raises(LedgerValidationError, match="duplicate JSON key"):
        load_ledger(copied)


def test_unknown_fields_fail_schema_validation(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    _rewrite_entry(
        target, lambda value: value.update(notes="unbounded escape hatch"), rehash=True
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_only_the_operator_can_record_a_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["actor"].update(type="WORKER", id="worker:test"),
        rehash=True,
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_completed_workstream_requires_decision_evidence(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(
        target,
        lambda value: value["data"].update(evidence_entry_ids=[]),
        rehash=True,
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_entry_type_and_payload_are_discriminated(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target, lambda value: value.update(entry_type="OBSERVATION"), rehash=True
    )

    with pytest.raises(LedgerValidationError, match="schema"):
        load_ledger(copied)


def test_workstream_subject_must_match_payload(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000005.json"
    _rewrite_entry(
        target,
        lambda value: value["subject"].update(id="CC-X03"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="workstream subject and payload"):
        load_ledger(copied, repository=ROOT)


def test_decision_subject_must_match_payload(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["subject"].update(id="OD-002"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="decision subject and payload"):
        load_ledger(copied, repository=ROOT)


def test_document_reference_cannot_escape_repository(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000001.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(target="/etc/hosts"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="repository-relative"):
        load_ledger(copied, repository=ROOT)


def test_canonical_reference_must_exist_in_graph(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000002.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][1].update(
            target="https://malleus.dev/not-a-canonical-record"
        ),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="absent from the canonical graph"):
        load_ledger(copied, repository=ROOT)


def test_entry_reference_must_point_backward(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000003.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(target="OVR-000003"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="point backward"):
        load_ledger(copied, repository=ROOT)


def test_observation_cannot_complete_a_workstream(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"

    def make_observation(value: dict) -> None:
        value["entry_type"] = "OBSERVATION"
        value["data"] = {
            "as_of": value["recorded_at"],
            "basis": ["Unverified reviewer observation."],
            "limitations": ["No retained mechanical evidence."],
        }

    _rewrite_entry(target, make_observation, rehash=False)
    _reseal(copied)

    with pytest.raises(
        LedgerValidationError, match="OBSERVATION cannot satisfy a gate"
    ):
        load_ledger(copied, repository=ROOT)


def test_nonbootstrap_transition_requires_projected_prior_state(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000006.json"
    _rewrite_entry(
        target,
        lambda value: value["data"].update(bootstrap=False),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="previous_state"):
        load_ledger(copied, repository=ROOT)


def test_only_operator_can_correct_a_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_only_operator_can_correct_the_program_decision(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000001",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_decision_correction_requires_operator_identity(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=False,
    )
    _rewrite_entry(
        copied / "entries" / f"{correction_id}.json",
        lambda value: value["actor"].update(id="overseer"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="only the operator"):
        load_ledger(copied, repository=ROOT)


def test_correction_subject_must_equal_target_subject(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=False,
    )
    _rewrite_entry(
        copied / "entries" / f"{correction_id}.json",
        lambda value: value.update(subject={"id": "CC-X03", "type": "WORKSTREAM"}),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="same subject"):
        load_ledger(copied, repository=ROOT)


def test_correction_that_requires_replacement_fails_without_one(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000002",
        actor_type="OPERATOR",
        replacement_required=True,
    )

    with pytest.raises(LedgerValidationError, match="replacement entry is absent"):
        load_ledger(copied, repository=ROOT)


def test_projected_state_correction_cannot_waive_replacement(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=False,
    )

    with pytest.raises(
        LedgerValidationError, match="projected state requires a replacement"
    ):
        load_ledger(copied, repository=ROOT)


def test_required_replacement_must_remain_active(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    replacement_id = _append_replacement_workstream(copied, "OVR-000006")
    _append_correction(
        copied,
        target_id=replacement_id,
        actor_type="OVERSEER",
        replacement_required=True,
    )

    with pytest.raises(LedgerValidationError, match="replacement entry is absent"):
        load_ledger(copied, repository=ROOT)


def test_correction_of_correction_restores_the_original_projection(
    tmp_path: Path,
) -> None:
    copied = _copy_ledger(tmp_path)
    correction_id = _append_correction(
        copied,
        target_id="OVR-000006",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    _append_correction(
        copied,
        target_id=correction_id,
        actor_type="OVERSEER",
        replacement_required=False,
    )

    state = load_ledger(copied, repository=ROOT)

    assert "| `CC-X03` | `COMPLETE` |" in render_status(state)


def test_active_typed_replacement_projects_normally(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    _append_correction(
        copied,
        target_id="OVR-000122",
        actor_type="OVERSEER",
        replacement_required=True,
    )
    _append_replacement_workstream(copied, "OVR-000122")

    state = load_ledger(copied, repository=ROOT)

    assert "| `CC-X03` | `COMPLETE` |" in render_status(state)


def test_evidence_reference_must_target_immutable_evidence_area(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target,
        lambda value: value["references"][0].update(
            target="design/PROTOCOL_FOUNDATION_GRAPH.ttl"
        ),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="immutable evidence"):
        load_ledger(copied, repository=ROOT)


def test_verified_fact_requires_immutable_evidence(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000004.json"
    _rewrite_entry(
        target,
        lambda value: value["references"].pop(0),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="requires immutable EVIDENCE"):
        load_ledger(copied, repository=ROOT)


def test_failed_verification_report_cannot_satisfy_a_gate(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    copied = repository / "design" / "contract_compiler" / "overseer"
    shutil.copytree(OVERSEER, copied)
    for relative in (
        "design/contract_compiler/program.md",
        "design/contract_compiler/decisions.md",
        "design/PROTOCOL_FOUNDATION_GRAPH.ttl",
    ):
        target = repository / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    for path in sorted((copied / "entries").glob("OVR-*.json"))[6:]:
        path.unlink()
    report_path = copied / "evidence" / "CC-D01.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["checks"][0]["result"] = "FAIL"
    report_path.write_text(canonical_json(report, indent=2) + "\n", encoding="utf-8")
    report_digest = "sha256:" + hashlib.sha256(report_path.read_bytes()).hexdigest()
    _rewrite_entry(
        copied / "entries" / "OVR-000004.json",
        lambda value: value["references"][0].update(digest=report_digest),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(
        LedgerValidationError, match="failed check cannot satisfy a gate"
    ):
        load_ledger(copied, repository=repository)


def test_evidence_sealing_checks_source_bytes(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("verified bytes\n", encoding="utf-8")
    digest = "sha256:" + hashlib.sha256(artifact.read_bytes()).hexdigest()
    report = {
        "artifacts": [
            {
                "byte_length": len(artifact.read_bytes()),
                "path": "artifact.txt",
                "sha256": digest,
            }
        ],
        "base_commit": "0" * 40,
        "checks": [
            {
                "check_id": "fixture",
                "method": "Compare exact source bytes.",
                "observed": "Fixture matched.",
                "result": "PASS",
            }
        ],
        "limitations": [],
        "recorded_at": "2026-08-24T19:30:00Z",
        "schema": "malleus.contract-compiler.verification-report/v1",
        "workstream_id": "CC-D01",
    }
    report_path = tmp_path / "report.json"
    report_path.write_text(canonical_json(report, indent=2) + "\n", encoding="utf-8")

    verify_evidence_snapshot(
        report_path,
        tmp_path,
        schema_path=OVERSEER / "ledger.schema.json",
    )
    artifact.write_text("tampered bytes\n", encoding="utf-8")
    with pytest.raises(
        LedgerValidationError, match="byte length mismatch|digest mismatch"
    ):
        verify_evidence_snapshot(
            report_path,
            tmp_path,
            schema_path=OVERSEER / "ledger.schema.json",
        )


def test_latest_document_revision_must_match_current_bytes(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target_path = ".gitignore"
    entry_paths = sorted((copied / "entries").glob("*.json"))
    entries = [json.loads(path.read_text(encoding="utf-8")) for path in entry_paths]
    superseded = _superseded_entries(entries)
    active_revisions = [
        path
        for path, entry in zip(entry_paths, entries, strict=True)
        if entry["entry_id"] not in superseded
        and entry["entry_type"] == "DOCUMENT_REVISION"
        and any(document["path"] == target_path for document in entry["data"]["documents"])
    ]
    assert active_revisions
    target = active_revisions[-1]

    def corrupt_latest_revision(value) -> None:
        document = next(
            document
            for document in value["data"]["documents"]
            if document["path"] == target_path
        )
        document["after_digest"] = "sha256:" + "0" * 64

    _rewrite_entry(
        target,
        corrupt_latest_revision,
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="latest document digest mismatch"):
        load_ledger(copied, repository=ROOT)


def test_document_revision_path_cannot_escape_repository(tmp_path: Path) -> None:
    copied = _copy_ledger(tmp_path)
    target = copied / "entries" / "OVR-000007.json"
    _rewrite_entry(
        target,
        lambda value: value["data"]["documents"][0].update(path="../../etc/hosts"),
        rehash=False,
    )
    _reseal(copied)

    with pytest.raises(LedgerValidationError, match="schema violation"):
        load_ledger(copied, repository=ROOT)
