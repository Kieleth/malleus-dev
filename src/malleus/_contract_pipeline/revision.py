"""One explicit additive revision of a compiled domain contract."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from hashlib import sha256
import json
from typing import Mapping

from malleus._contract_pipeline.machine import (
    NormativeAdmissionProfile,
    PartialEffectiveContract,
    PolicyProgram,
    compose_normative_profile,
)
from malleus._contract_pipeline.model import FACT_NAMESPACE, RDF_TYPE, canonical_json
from malleus._contract_pipeline.view import (
    ContractView,
    load_validated_contract_artifact,
)
from malleus.migration import MigrationError, MigrationReceipt, TOTAL


_POLICY_GRAMMAR = "malleus.contract-revision-policy/private-v0"
_REVISION_GRAMMAR = "malleus.contract-revision/private-v0"
_REBIND = "REBIND_CHECK_CONTRACT"
_KINDS = ("ADD_CLASS", "ADD_ENUM_VALUE", "ADD_IMPORT", "ADD_SLOT", _REBIND)
_CLASS = FACT_NAMESPACE + "Class"
_SLOT = FACT_NAMESPACE + "Slot"
_SLOT_USE = FACT_NAMESPACE + "SlotUse"
_ENUM_VALUE = FACT_NAMESPACE + "enumValue"
_ON_CLASS = FACT_NAMESPACE + "onClass"
_USES_SLOT = FACT_NAMESPACE + "usesSlot"


class ContractRevisionRefusalReason(Enum):
    MALFORMED_REVISION = auto()
    NONCANONICAL_REVISION = auto()
    IDENTITY_MISMATCH = auto()
    INCOMPATIBLE_CONTRACT = auto()
    NON_ADDITIVE_CHANGE = auto()
    POLICY_REFUSAL = auto()
    STALE_BASE = auto()


class ContractRevisionRefusal(ValueError):
    def __init__(
        self,
        reason: ContractRevisionRefusalReason,
        detail: str,
        *,
        change_kind: str | None = None,
    ) -> None:
        self.reason = reason
        self.detail = detail
        self.change_kind = change_kind
        super().__init__(f"{reason.name}: {detail}")


def _refuse(
    reason: ContractRevisionRefusalReason,
    detail: str,
    *,
    change_kind: str | None = None,
) -> ContractRevisionRefusal:
    return ContractRevisionRefusal(reason, detail, change_kind=change_kind)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith("sha256:")
        and all(character in "0123456789abcdef" for character in value[7:])
    )


def _required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} is required")
    return value


def _required_digest(value: object, label: str) -> str:
    if not _is_digest(value):
        raise ValueError(f"{label} must be a SHA-256 digest")
    assert isinstance(value, str)
    return value


def _required_head(value: object, label: str) -> str:
    if value != "GENESIS" and not _is_digest(value):
        raise ValueError(f"{label} must be GENESIS or a SHA-256 digest")
    assert isinstance(value, str)
    return value


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def _decode(source: bytes) -> dict[str, object]:
    if type(source) is not bytes:
        raise _refuse(
            ContractRevisionRefusalReason.MALFORMED_REVISION,
            "revision input must be exact bytes",
        )
    try:
        data = json.loads(source)
        if not isinstance(data, dict):
            raise ValueError("revision root must be an object")
        canonical = canonical_json(data)
    except (UnicodeDecodeError, TypeError, ValueError) as error:
        raise _refuse(
            ContractRevisionRefusalReason.MALFORMED_REVISION,
            "revision is not strict canonical JSON",
        ) from error
    if canonical != source:
        raise _refuse(
            ContractRevisionRefusalReason.NONCANONICAL_REVISION,
            "revision bytes are not canonical",
        )
    return data


@dataclass(frozen=True, slots=True)
class ContractRevisionChange:
    kind: str
    subject: str
    value: str | None

    def as_dict(self) -> dict[str, str | None]:
        return {"kind": self.kind, "subject": self.subject, "value": self.value}


@dataclass(frozen=True, slots=True)
class ContractRevisionPolicy:
    canonical_bytes: bytes
    identity: str
    grammar: str
    decisions: tuple[tuple[str, str], ...]

    @property
    def change_kinds(self) -> tuple[str, ...]:
        return tuple(kind for kind, _ in self.decisions)

    @property
    def admitted_change_kinds(self) -> tuple[str, ...]:
        return tuple(kind for kind, outcome in self.decisions if outcome == "ADMIT")

    @property
    def refused_change_kinds(self) -> tuple[str, ...]:
        return tuple(kind for kind, outcome in self.decisions if outcome == "REFUSE")

    def outcome(self, kind: str) -> str:
        try:
            return dict(self.decisions)[kind]
        except KeyError as error:
            raise _refuse(
                ContractRevisionRefusalReason.MALFORMED_REVISION,
                f"unknown contract revision kind: {kind}",
                change_kind=kind,
            ) from error


_SUPERSEDED_POLICY_DECISIONS = (
    ("ADD_CLASS", "ADMIT"),
    ("ADD_ENUM_VALUE", "ADMIT"),
    ("ADD_IMPORT", "REFUSE"),
    ("ADD_SLOT", "ADMIT"),
)
_POLICY_DECISIONS = _SUPERSEDED_POLICY_DECISIONS + ((_REBIND, "ADMIT"),)


def _revision_policy(
    decisions: tuple[tuple[str, str], ...],
) -> ContractRevisionPolicy:
    source = canonical_json(
        {
            "change_kinds": [
                {"kind": kind, "outcome": outcome} for kind, outcome in decisions
            ],
            "grammar": _POLICY_GRAMMAR,
        }
    )
    return ContractRevisionPolicy(
        source, _digest(source), _POLICY_GRAMMAR, decisions
    )


CONTRACT_REVISION_POLICY = _revision_policy(_POLICY_DECISIONS)
#: Declaring a new change kind moves the revision policy's own digest, and a
#: recorded revision names the exact policy it was compiled under. Both are
#: therefore executable: a revision declares one, and Core runs that one for it.
#: Nothing selects a policy implicitly; new revisions bind
#: ``CONTRACT_REVISION_POLICY``.
SUPPORTED_CONTRACT_REVISION_POLICIES = (
    _revision_policy(_SUPERSEDED_POLICY_DECISIONS),
    CONTRACT_REVISION_POLICY,
)


def contract_revision_policy(identity: str) -> ContractRevisionPolicy:
    """The declared revision policy with this identity, or a typed refusal."""

    for policy in SUPPORTED_CONTRACT_REVISION_POLICIES:
        if policy.identity == identity:
            return policy
    raise _refuse(
        ContractRevisionRefusalReason.POLICY_REFUSAL,
        "contract revision does not use a supported revision policy",
    )


@dataclass(frozen=True, slots=True)
class CheckContractRebinding:
    """One required check contract re-pinned to the revision's target ontology.

    ``from_check_contract`` and ``to_check_contract`` are the exact field
    mappings whose canonical digests are the two identities the current and
    target policies require. ``rebound_field`` is the single field that moved,
    and it moved from the current ontology's content hash to the target's.
    Everything else is identical, which is what ``unchanged_fields_digest``
    records in one value: the check's rule bytes, its rule IDs, its timeout and
    its versions cannot have moved.
    """

    check_contract_id: str
    from_identity: str
    to_identity: str
    from_check_contract_bytes: bytes
    to_check_contract_bytes: bytes
    rebound_field: str
    unchanged_fields_digest: str

    @property
    def from_check_contract(self) -> dict[str, object]:
        return json.loads(self.from_check_contract_bytes)

    @property
    def to_check_contract(self) -> dict[str, object]:
        return json.loads(self.to_check_contract_bytes)

    def as_dict(self) -> dict[str, object]:
        return {
            "check_contract_id": self.check_contract_id,
            "from_check_contract": self.from_check_contract,
            "from_check_contract_identity": self.from_identity,
            "rebound_field": self.rebound_field,
            "to_check_contract": self.to_check_contract,
            "to_check_contract_identity": self.to_identity,
            "unchanged_fields_digest": self.unchanged_fields_digest,
        }


@dataclass(frozen=True, slots=True)
class ContractRevisionRebinding:
    """The complete declared re-binding this revision carries."""

    from_normative_profile_identity: str
    to_normative_profile_identity: str
    checks: tuple[CheckContractRebinding, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "checks": [check.as_dict() for check in self.checks],
            "from_normative_profile_identity": (
                self.from_normative_profile_identity
            ),
            "to_normative_profile_identity": self.to_normative_profile_identity,
        }


@dataclass(frozen=True, slots=True)
class ContractRevision:
    canonical_bytes: bytes
    identity: str
    revision_id: str
    base_ledger_head: str
    base_ledger_event_count: int
    base_acceptance_head: str
    base_materialization_head: str
    base_accepted_state_digest: str
    from_contract_identity: str
    target_validated_contract_bytes: bytes
    target_partial_contract: PartialEffectiveContract
    policy_identity: str
    changes: tuple[ContractRevisionChange, ...]
    migration_receipt: MigrationReceipt
    check_rebinding: ContractRevisionRebinding | None = None

    @property
    def from_validated_fact_set_sha256(self) -> str:
        return self.migration_receipt.from_hash

    @property
    def reason(self) -> str:
        return self.migration_receipt.reason

    @property
    def issued_at(self) -> str:
        return self.migration_receipt.issued_at

    @property
    def target_contract_view(self) -> ContractView:
        return load_validated_contract_artifact(self.target_validated_contract_bytes)

    @classmethod
    def from_bytes(cls, source: bytes) -> ContractRevision:
        data = _decode(source)
        try:
            required = {
                "base",
                "changes",
                "from_contract_identity",
                "grammar",
                "migration_receipt",
                "policy_identity",
                "revision_id",
                "target",
            }
            # A revision recorded before check re-binding existed carries no
            # such field at all, so the optional key is the whole compatibility
            # story for an older ledger.
            if set(data) - {"check_rebinding"} != required:
                raise ValueError("contract revision fields are not closed")
            if data["grammar"] != _REVISION_GRAMMAR:
                raise ValueError("contract revision grammar is unsupported")
            base = _object(data["base"], "contract revision base")
            if set(base) != {
                "acceptance_head",
                "accepted_state_digest",
                "ledger_event_count",
                "ledger_head",
                "materialization_head",
            }:
                raise ValueError("contract revision base is not closed")
            count = base["ledger_event_count"]
            if type(count) is not int or count < 0:
                raise ValueError("base ledger event count must be nonnegative")
            target = _object(data["target"], "contract revision target")
            if set(target) != {"partial_contract", "validated_contract"}:
                raise ValueError("contract revision target is not closed")
            validated_bytes = canonical_json(
                _object(target["validated_contract"], "target validated contract")
            )
            view = load_validated_contract_artifact(validated_bytes)
            partial = PartialEffectiveContract.from_bytes(
                canonical_json(
                    _object(target["partial_contract"], "target partial contract")
                )
            )
            if "sha256:" + view.content_hash() != partial.validated_fact_set_sha256:
                raise ValueError("target contract artifacts disagree")
            changes = _changes(data["changes"])
            receipt = MigrationReceipt.from_dict(
                _object(data["migration_receipt"], "migration receipt")
            )
            if (
                receipt.to_hash != partial.validated_fact_set_sha256
                or receipt.grade != TOTAL
                or receipt.delta_digest
                != _digest(canonical_json([change.as_dict() for change in changes]))
            ):
                raise ValueError("migration receipt does not bind the revision")
            policy_identity = _required_digest(
                data["policy_identity"], "revision policy identity"
            )
            rebinding = (
                _rebinding(data["check_rebinding"])
                if "check_rebinding" in data
                else None
            )
            declared = {
                change.subject for change in changes if change.kind == _REBIND
            }
            carried = (
                {check.check_contract_id for check in rebinding.checks}
                if rebinding is not None
                else set()
            )
            if declared != carried:
                raise ValueError(
                    "contract revision re-binding changes and declaration disagree"
                )
            return cls(
                source,
                _digest(source),
                _required_text(data["revision_id"], "revision ID"),
                _required_head(base["ledger_head"], "base ledger head"),
                count,
                _required_head(base["acceptance_head"], "base acceptance head"),
                _required_head(
                    base["materialization_head"], "base materialization head"
                ),
                _required_digest(
                    base["accepted_state_digest"], "base accepted-state digest"
                ),
                _required_digest(
                    data["from_contract_identity"], "source contract identity"
                ),
                validated_bytes,
                partial,
                policy_identity,
                changes,
                receipt,
                rebinding,
            )
        except ContractRevisionRefusal:
            raise
        except (KeyError, MigrationError, TypeError, ValueError) as error:
            raise _refuse(
                ContractRevisionRefusalReason.MALFORMED_REVISION,
                str(error),
            ) from error


def _changes(value: object) -> tuple[ContractRevisionChange, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError("contract revision changes are required")
    changes: list[ContractRevisionChange] = []
    for raw in value:
        item = _object(raw, "contract revision change")
        if set(item) != {"kind", "subject", "value"}:
            raise ValueError("contract revision change is not closed")
        kind = _required_text(item["kind"], "contract revision change kind")
        subject = _required_text(item["subject"], "contract revision change subject")
        raw_value = item["value"]
        selected = (
            None
            if raw_value is None
            else _required_text(raw_value, "contract revision change value")
        )
        if kind not in _KINDS:
            raise ValueError("contract revision change kind is unsupported")
        changes.append(ContractRevisionChange(kind, subject, selected))
    ordered = sorted(
        set(changes), key=lambda item: (item.kind, item.subject, item.value or "")
    )
    if changes != ordered:
        raise ValueError("contract revision changes must be sorted and unique")
    return tuple(changes)


def _descriptor(value: object, label: str) -> tuple[bytes, dict[str, object]]:
    """A check contract's exact field mapping, canonical and content-addressed."""

    mapping = _object(value, label)
    if not mapping or not all(isinstance(key, str) and key for key in mapping):
        raise ValueError(f"{label} must name at least one field")
    return canonical_json(mapping), mapping


def _rebound_field(
    check_contract_id: str,
    before: Mapping[str, object],
    after: Mapping[str, object],
    *,
    current_ontology_hash: str,
    target_ontology_hash: str,
) -> str:
    """The single field that may move, and the proof that nothing else did."""

    if set(before) != set(after):
        moved = ", ".join(sorted(set(before) ^ set(after)))
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            f"check contract {check_contract_id} adds or removes fields: {moved}",
            change_kind=_REBIND,
        )
    differing = sorted(key for key in before if before[key] != after[key])
    rebound = [key for key in differing if before[key] == current_ontology_hash]
    if len(rebound) != 1:
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            f"check contract {check_contract_id} does not pin the current ontology "
            "in exactly one changed field",
            change_kind=_REBIND,
        )
    field = rebound[0]
    if after[field] != target_ontology_hash:
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            f"check contract {check_contract_id} does not rebind {field} to the "
            "target ontology",
            change_kind=_REBIND,
        )
    other = [key for key in differing if key != field]
    if other:
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            f"check contract {check_contract_id} changes fields beyond its "
            f"ontology binding: {', '.join(other)}",
            change_kind=_REBIND,
        )
    return field


def _unchanged_digest(mapping: Mapping[str, object], field: str) -> str:
    return _digest(
        canonical_json({key: value for key, value in mapping.items() if key != field})
    )


def _rebinding(value: object) -> ContractRevisionRebinding:
    """Read one recorded re-binding back, recomputing every declared identity."""

    data = _object(value, "contract revision re-binding")
    if set(data) != {
        "checks",
        "from_normative_profile_identity",
        "to_normative_profile_identity",
    }:
        raise ValueError("contract revision re-binding is not closed")
    raw_checks = data["checks"]
    if not isinstance(raw_checks, list) or not raw_checks:
        raise ValueError("contract revision re-binding declares no check")
    checks: list[CheckContractRebinding] = []
    for raw in raw_checks:
        item = _object(raw, "contract revision re-bound check")
        if set(item) != {
            "check_contract_id",
            "from_check_contract",
            "from_check_contract_identity",
            "rebound_field",
            "to_check_contract",
            "to_check_contract_identity",
            "unchanged_fields_digest",
        }:
            raise ValueError("contract revision re-bound check is not closed")
        before_bytes, before = _descriptor(
            item["from_check_contract"], "re-bound check contract"
        )
        after_bytes, after = _descriptor(
            item["to_check_contract"], "re-bound check contract"
        )
        from_identity = _required_digest(
            item["from_check_contract_identity"], "re-bound check identity"
        )
        to_identity = _required_digest(
            item["to_check_contract_identity"], "re-bound check identity"
        )
        field = _required_text(item["rebound_field"], "re-bound check field")
        if _digest(before_bytes) != from_identity or _digest(after_bytes) != to_identity:
            raise ValueError("re-bound check contract does not hash to its identity")
        if (
            field not in before
            or before[field] == after[field]
            or any(
                before[key] != after[key] for key in before if key != field
            )
            or set(before) != set(after)
        ):
            raise ValueError("re-bound check contract changed more than one field")
        if item["unchanged_fields_digest"] != _unchanged_digest(before, field):
            raise ValueError("re-bound check contract unchanged-field proof is wrong")
        checks.append(
            CheckContractRebinding(
                _required_text(item["check_contract_id"], "re-bound check ID"),
                from_identity,
                to_identity,
                before_bytes,
                after_bytes,
                field,
                item["unchanged_fields_digest"],
            )
        )
    ordered = sorted(checks, key=lambda check: check.check_contract_id)
    if checks != ordered or len({check.check_contract_id for check in checks}) != len(
        checks
    ):
        raise ValueError("re-bound checks must be sorted and unique")
    return ContractRevisionRebinding(
        _required_digest(
            data["from_normative_profile_identity"], "source profile identity"
        ),
        _required_digest(
            data["to_normative_profile_identity"], "target profile identity"
        ),
        tuple(checks),
    )


def _moved_checks(
    current: NormativeAdmissionProfile, target: NormativeAdmissionProfile
) -> dict[str, tuple[str, str]]:
    """Every required check whose identity moved, once the rest is proven equal.

    Anything else the profile changed refuses here, named, before a revision
    exists. This is the whole of "the policy is otherwise unchanged".
    """

    if (
        current.protocol_machine_program.identity
        != target.protocol_machine_program.identity
    ):
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            "domain revision changes the protocol machine program",
        )
    before_policies = dict(current.policy_programs)
    after_policies = dict(target.policy_programs)
    if set(before_policies) != set(after_policies):
        moved = ", ".join(sorted(set(before_policies) ^ set(after_policies)))
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            f"domain revision changes the bound policy programs: {moved}",
        )
    answer: dict[str, tuple[str, str]] = {}
    for reference in sorted(before_policies):
        before, after = before_policies[reference], after_policies[reference]
        name = before.identifier
        if name != after.identifier:
            raise _refuse(
                ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
                f"domain revision changes the identifier of policy {name}",
            )
        if dict(before.outcome_verdicts) != dict(after.outcome_verdicts):
            raise _refuse(
                ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
                f"domain revision changes the outcome verdicts of policy {name}",
            )
        if before.precedence != after.precedence:
            raise _refuse(
                ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
                f"domain revision changes the verdict precedence of policy {name}",
            )
        required_before = dict(before.required_checks)
        required_after = dict(after.required_checks)
        if set(required_before) != set(required_after):
            moved = ", ".join(sorted(set(required_before) ^ set(required_after)))
            raise _refuse(
                ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
                f"domain revision changes the required checks of policy {name}: "
                f"{moved}",
            )
        for check_id in sorted(required_before):
            pair = (required_before[check_id], required_after[check_id])
            if pair[0] == pair[1]:
                continue
            if answer.get(check_id, pair) != pair:
                raise _refuse(
                    ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
                    f"domain revision rebinds check contract {check_id} to two "
                    "different identities",
                    change_kind=_REBIND,
                )
            answer[check_id] = pair
    return answer


def _restored_profile(
    target: NormativeAdmissionProfile, moved: Mapping[str, tuple[str, str]]
) -> NormativeAdmissionProfile:
    """The target profile with the re-bound check identities put back.

    Undoing exactly the declared re-binding must reproduce the current profile
    byte for byte. That comparison, not the field-by-field walk above, is what
    establishes that nothing else moved; the walk exists to name what did.
    """

    policies: dict[str, PolicyProgram] = {}
    for reference, program in target.policy_programs:
        data = json.loads(program.canonical_bytes)
        for check in data["required_checks"]:
            values = dict(check)
            names = [value for value in values.values() if not _is_digest(value)]
            for key, value in values.items():
                if (
                    len(names) == 1
                    and names[0] in moved
                    and value == moved[names[0]][1]
                ):
                    check[key] = moved[names[0]][0]
        policies[reference] = PolicyProgram.from_bytes(canonical_json(data))
    return compose_normative_profile(
        protocol_machine_program=target.protocol_machine_program,
        policy_programs=policies,
        capability_refs=(),
    )


def _compile_rebinding(
    current: PartialEffectiveContract,
    target: PartialEffectiveContract,
    descriptors: Mapping[str, tuple[Mapping[str, object], Mapping[str, object]]],
    *,
    current_ontology_hash: str,
    target_ontology_hash: str,
) -> ContractRevisionRebinding | None:
    """Derive the declared re-binding, or refuse naming what else moved."""

    if not isinstance(descriptors, Mapping):
        raise ValueError("check contract descriptors must be a mapping")
    if current.normative_profile == target.normative_profile:
        if descriptors:
            name = sorted(descriptors)[0]
            raise _refuse(
                ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
                f"revision declares a re-binding of {name} that no policy requires",
                change_kind=_REBIND,
            )
        return None
    if not descriptors:
        raise ValueError("domain revision changes the normative protocol profile")
    moved = _moved_checks(current.normative_profile, target.normative_profile)
    for name in sorted(set(descriptors) - set(moved)):
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            f"revision declares a re-binding of {name} that no policy requires",
            change_kind=_REBIND,
        )
    for name in sorted(set(moved) - set(descriptors)):
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            f"domain revision changes check contract {name} without declaring its "
            "re-binding",
            change_kind=_REBIND,
        )
    if (
        _restored_profile(target.normative_profile, moved).identity
        != current.normative_profile.identity
    ):
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            "domain revision changes the normative protocol profile beyond the "
            "declared re-binding",
        )
    checks: list[CheckContractRebinding] = []
    for name in sorted(moved):
        supplied = descriptors[name]
        if not isinstance(supplied, tuple) or len(supplied) != 2:
            raise ValueError(
                "a check contract descriptor is the pair before the revision and "
                "after it"
            )
        before_bytes, before = _descriptor(supplied[0], "check contract descriptor")
        after_bytes, after = _descriptor(supplied[1], "check contract descriptor")
        from_identity, to_identity = moved[name]
        if _digest(before_bytes) != from_identity:
            raise _refuse(
                ContractRevisionRefusalReason.IDENTITY_MISMATCH,
                f"declared check contract {name} does not hash to the identity the "
                "current policy requires",
                change_kind=_REBIND,
            )
        if _digest(after_bytes) != to_identity:
            raise _refuse(
                ContractRevisionRefusalReason.IDENTITY_MISMATCH,
                f"declared check contract {name} does not hash to the identity the "
                "target policy requires",
                change_kind=_REBIND,
            )
        field = _rebound_field(
            name,
            before,
            after,
            current_ontology_hash=current_ontology_hash,
            target_ontology_hash=target_ontology_hash,
        )
        checks.append(
            CheckContractRebinding(
                name,
                from_identity,
                to_identity,
                before_bytes,
                after_bytes,
                field,
                _unchanged_digest(before, field),
            )
        )
    return ContractRevisionRebinding(
        current.normative_profile.identity,
        target.normative_profile.identity,
        tuple(checks),
    )


def _artifact(source: bytes) -> tuple[ContractView, dict[str, object]]:
    view = load_validated_contract_artifact(source)
    payload = json.loads(source)
    assert isinstance(payload, dict)
    return view, payload


def _root_schema(payload: Mapping[str, object]) -> str:
    evidence = _object(payload["evidence"], "contract evidence")
    root = _object(evidence["root"], "root evidence")
    locator = _required_text(root["resolved_locator"], "resolved root locator")
    sources = evidence["sources"]
    if not isinstance(sources, list):
        raise ValueError("contract sources must be an array")
    matches = [
        _object(item, "contract source")
        for item in sources
        if isinstance(item, dict) and item.get("module_id") == locator
    ]
    if len(matches) != 1:
        raise ValueError("contract root source is not unique")
    return _required_text(matches[0]["schema_id"], "root schema ID")


def _imports(payload: Mapping[str, object]) -> set[tuple[str, str, str]]:
    evidence = _object(payload["evidence"], "contract evidence")
    raw_imports = evidence["imports"]
    if not isinstance(raw_imports, list):
        raise ValueError("contract imports must be an array")
    answer: set[tuple[str, str, str]] = set()
    for raw in raw_imports:
        item = _object(raw, "contract import")
        answer.add(
            (
                _required_text(item["parent_module_id"], "import parent"),
                _required_text(item["child_module_id"], "import child"),
                _required_text(item["literal"], "import literal"),
            )
        )
    return answer


def _facts(payload: Mapping[str, object]) -> dict[bytes, dict[str, object]]:
    raw_facts = payload["facts"]
    if not isinstance(raw_facts, list):
        raise ValueError("contract facts must be an array")
    return {
        canonical_json(item): item
        for raw in raw_facts
        for item in (_object(raw, "contract fact"),)
    }


def _derive_changes(
    current_source: bytes, target_source: bytes
) -> tuple[ContractRevisionChange, ...]:
    _, current = _artifact(current_source)
    _, target = _artifact(target_source)
    if _root_schema(current) != _root_schema(target):
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            "contract revision changes the root ontology",
        )
    before_imports, after_imports = _imports(current), _imports(target)
    if before_imports != after_imports:
        return tuple(
            ContractRevisionChange("ADD_IMPORT", parent, literal)
            for parent, _, literal in sorted(before_imports ^ after_imports)
        )

    before, after = _facts(current), _facts(target)
    if set(before) - set(after):
        raise _refuse(
            ContractRevisionRefusalReason.NON_ADDITIVE_CHANGE,
            "contract revision removes or changes an existing semantic fact",
        )
    added_keys = set(after) - set(before)
    if not added_keys:
        raise _refuse(
            ContractRevisionRefusalReason.NON_ADDITIVE_CHANGE,
            "contract revision adds no semantic fact",
        )
    added = [after[key] for key in added_keys]
    kinds = {
        item["subject"]: item["object"]
        for item in after.values()
        if item.get("predicate") == RDF_TYPE
    }
    new_classes = _new_kind(added_keys, kinds, _CLASS)
    new_slots = _new_kind(added_keys, kinds, _SLOT)
    new_slot_uses = _new_kind(added_keys, kinds, _SLOT_USE)
    values = _fact_values(after.values())
    changes = {
        *(ContractRevisionChange("ADD_CLASS", item, None) for item in new_classes),
        *(ContractRevisionChange("ADD_SLOT", item, None) for item in new_slots),
        *(
            ContractRevisionChange(
                "ADD_ENUM_VALUE",
                _required_text(item["subject"], "enum subject"),
                _required_text(item["object"], "enum value"),
            )
            for item in added
            if item.get("predicate") == _ENUM_VALUE
        ),
    }
    for slot_use in new_slot_uses:
        owner = _required_text(values[slot_use].get(_ON_CLASS), "slot-use class")
        slot = _required_text(values[slot_use].get(_USES_SLOT), "slot-use slot")
        if owner not in new_classes and slot not in new_slots:
            changes.add(ContractRevisionChange("ADD_SLOT", owner, slot))
    covered = new_classes | new_slots | new_slot_uses
    if any(
        item["subject"] not in covered and item["predicate"] != _ENUM_VALUE
        for item in added
    ):
        raise _refuse(
            ContractRevisionRefusalReason.NON_ADDITIVE_CHANGE,
            "contract revision adds a semantic fact outside the allowed forms",
        )
    return tuple(
        sorted(changes, key=lambda item: (item.kind, item.subject, item.value or ""))
    )


def _new_kind(added: set[bytes], kinds: Mapping[object, object], kind: str) -> set[str]:
    return {
        subject
        for raw_subject, found in kinds.items()
        for subject in (_required_text(raw_subject, "fact subject"),)
        if found == kind
        and canonical_json({"object": kind, "predicate": RDF_TYPE, "subject": subject})
        in added
    }


def _fact_values(facts: object) -> dict[str, dict[str, object]]:
    answer: dict[str, dict[str, object]] = {}
    for raw in facts:
        item = _object(raw, "contract fact")
        subject = _required_text(item["subject"], "fact subject")
        predicate = _required_text(item["predicate"], "fact predicate")
        answer.setdefault(subject, {})[predicate] = item["object"]
    return answer


def compile_contract_revision(
    *,
    revision_id: str,
    base_ledger_head: str,
    base_ledger_event_count: int,
    base_acceptance_head: str,
    base_materialization_head: str,
    base_accepted_state_digest: str,
    current_validated_contract_bytes: bytes,
    current_partial_contract_bytes: bytes,
    target_validated_contract_bytes: bytes,
    target_partial_contract_bytes: bytes,
    reason: str,
    issued_at: str,
    previous_migration_receipt: str | None = None,
    check_contract_descriptors: Mapping[
        str, tuple[Mapping[str, object], Mapping[str, object]]
    ]
    | None = None,
    policy: ContractRevisionPolicy = CONTRACT_REVISION_POLICY,
) -> ContractRevision:
    """Compile one additive domain-contract revision from exact artifacts.

    ``check_contract_descriptors`` maps a required check contract's ID to the
    pair of exact field mappings before and after the revision. Supplying one
    declares that the revision re-pins that check to the target ontology, and
    Core admits it only when nothing but the ontology binding inside it moved.
    Every other change to the selected policy still refuses.
    """

    try:
        current_view, current_payload = _artifact(current_validated_contract_bytes)
        target_view, _ = _artifact(target_validated_contract_bytes)
        current_partial = PartialEffectiveContract.from_bytes(
            current_partial_contract_bytes
        )
        target_partial = PartialEffectiveContract.from_bytes(
            target_partial_contract_bytes
        )
        if (
            "sha256:" + current_view.content_hash()
            != current_partial.validated_fact_set_sha256
            or "sha256:" + target_view.content_hash()
            != target_partial.validated_fact_set_sha256
        ):
            raise ValueError("validated and partial contract artifacts disagree")
        rebinding = _compile_rebinding(
            current_partial,
            target_partial,
            check_contract_descriptors or {},
            current_ontology_hash="sha256:" + current_view.content_hash(),
            target_ontology_hash="sha256:" + target_view.content_hash(),
        )
        changes = _derive_changes(
            current_validated_contract_bytes, target_validated_contract_bytes
        )
        if rebinding is not None:
            changes = tuple(
                sorted(
                    changes
                    + tuple(
                        ContractRevisionChange(
                            _REBIND, check.check_contract_id, check.to_identity
                        )
                        for check in rebinding.checks
                    ),
                    key=lambda item: (item.kind, item.subject, item.value or ""),
                )
            )
        for change in changes:
            if policy.outcome(change.kind) != "ADMIT":
                raise _refuse(
                    ContractRevisionRefusalReason.POLICY_REFUSAL,
                    f"contract revision policy refuses {change.kind}",
                    change_kind=change.kind,
                )
        change_data = [change.as_dict() for change in changes]
        receipt = MigrationReceipt(
            ontology=_root_schema(current_payload),
            from_hash=current_partial.validated_fact_set_sha256,
            to_hash=target_partial.validated_fact_set_sha256,
            grade=TOTAL,
            reason=_required_text(reason, "revision reason"),
            issued_at=_required_text(issued_at, "revision issue time"),
            previous_receipt=previous_migration_receipt,
            delta_digest=_digest(canonical_json(change_data)),
        )
        if type(base_ledger_event_count) is not int or base_ledger_event_count < 0:
            raise ValueError("base ledger event count must be nonnegative")
        payload: dict[str, object] = {}
        if rebinding is not None:
            payload["check_rebinding"] = rebinding.as_dict()
        return ContractRevision.from_bytes(
            canonical_json(
                {
                    **payload,
                    "base": {
                        "acceptance_head": _required_head(
                            base_acceptance_head, "base acceptance head"
                        ),
                        "accepted_state_digest": _required_digest(
                            base_accepted_state_digest, "base accepted-state digest"
                        ),
                        "ledger_event_count": base_ledger_event_count,
                        "ledger_head": _required_head(
                            base_ledger_head, "base ledger head"
                        ),
                        "materialization_head": _required_head(
                            base_materialization_head, "base materialization head"
                        ),
                    },
                    "changes": change_data,
                    "from_contract_identity": current_partial.identity,
                    "grammar": _REVISION_GRAMMAR,
                    "migration_receipt": receipt.as_dict(),
                    "policy_identity": policy.identity,
                    "revision_id": _required_text(revision_id, "revision ID"),
                    "target": {
                        "partial_contract": json.loads(target_partial.canonical_bytes),
                        "validated_contract": json.loads(
                            target_validated_contract_bytes
                        ),
                    },
                }
            )
        )
    except ContractRevisionRefusal:
        raise
    except (KeyError, MigrationError, TypeError, ValueError) as error:
        raise _refuse(
            ContractRevisionRefusalReason.INCOMPATIBLE_CONTRACT,
            str(error),
        ) from error


__all__ = (
    "CONTRACT_REVISION_POLICY",
    "SUPPORTED_CONTRACT_REVISION_POLICIES",
    "CheckContractRebinding",
    "ContractRevision",
    "ContractRevisionChange",
    "ContractRevisionPolicy",
    "ContractRevisionRebinding",
    "ContractRevisionRefusal",
    "ContractRevisionRefusalReason",
    "compile_contract_revision",
    "contract_revision_policy",
)
