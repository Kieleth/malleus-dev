"""Ontology change as a recorded act.

A malleus migration never transforms a record. The ledger is append-only and
the fact that nobody can rewrite it is the whole value, so an ontology change
can only transform how an already-written record is READ. That is stricter,
not looser: a data migration succeeds once, on one Tuesday, and is then over. A
reading rule has to be total over every record ever written and has to keep
working on every future read.

A receipt is the record of one such change. It binds the outgoing identity, the
incoming identity, and the grade of the rule that reads the old records under
the new ontology. Receipts form a chain, and the chain is how a ledger anchored
under an earlier identity is still readable: not by a hand-passed list of
hashes anyone can widen, but by a path somebody wrote down.

The shape is borrowed rather than invented. Root rotation in the TUF
specification makes the switching record verifiable under both identities,
requires the position to be exactly the previous one incremented, and forbids
skipping intermediates. `did:webvh` makes the rules-version upgrade an entry in
the hash chain itself. Delta Lake puts the schema change in the same log as the
data. What none of them do, and what the append-only ledger here makes
possible, is make the record that cannot be interpreted addressable in the log
that holds it.

One honesty this module cannot escape: a receipt asserts what an ontology's
identity WAS, and those bytes are gone. `to_hash` can be checked against a live
registry. `from_hash` cannot be checked against anything, which is precisely
why it has to be recorded at the time rather than derived later.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from malleus.ledger import DIGEST_PATTERN, content_digest

# The grades of reading rule. A change is legitimate when it carries one and
# declares which. What malleus refuses is a break that is not declared: you may
# break history, you may not break it silently.
TOTAL = "TOTAL"
PARTIAL = "PARTIAL"
HARD_BREAK = "HARD_BREAK"
GRADES = (TOTAL, PARTIAL, HARD_BREAK)

RECEIPT_FIELDS = frozenset({
    "ontology", "from_hash", "to_hash", "grade", "reason",
    "issued_at", "previous_receipt", "delta_digest",
})


class MigrationError(ValueError):
    """A receipt or a chain of them cannot be read as a migration."""


def _digest(subject: str, value: Any, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str) or not DIGEST_PATTERN.fullmatch(value):
        raise MigrationError(f"{subject} must be sha256:<64 hex>, got {value!r}")
    return value


def _text(subject: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MigrationError(f"{subject} must be a nonblank string")
    return value


@dataclass(frozen=True)
class MigrationReceipt:
    """One recorded ontology change.

    `previous_receipt` is the digest of the receipt before this one, or None
    for the first. It is what makes the chain unskippable: a reader cannot jump
    from the oldest identity to the newest without walking every receipt
    between them, so a change nobody recorded cannot be stepped over.
    """

    ontology: str
    from_hash: str
    to_hash: str
    grade: str
    reason: str
    issued_at: str
    previous_receipt: str | None = None
    delta_digest: str | None = None

    def __post_init__(self) -> None:
        _text("receipt ontology", self.ontology)
        _text("receipt reason", self.reason)
        _text("receipt issued_at", self.issued_at)
        _digest("receipt from_hash", self.from_hash)
        _digest("receipt to_hash", self.to_hash)
        _digest("receipt previous_receipt", self.previous_receipt, optional=True)
        _digest("receipt delta_digest", self.delta_digest, optional=True)
        if self.grade not in GRADES:
            raise MigrationError(
                f"receipt grade must be one of {', '.join(GRADES)}, got {self.grade!r}. "
                f"A change with no declared grade is an undeclared break"
            )
        if self.from_hash == self.to_hash:
            raise MigrationError(
                "receipt from_hash equals to_hash: a change that changed no identity "
                "is not a migration and recording one would make the chain a liar"
            )

    @property
    def digest(self) -> str:
        """This receipt's own identity, over every field including its link."""
        return content_digest(asdict(self))

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, document: Mapping[str, Any]) -> "MigrationReceipt":
        if not isinstance(document, Mapping):
            raise MigrationError("a receipt must be a mapping")
        unknown = sorted(set(document) - RECEIPT_FIELDS)
        if unknown:
            raise MigrationError(f"receipt carries undeclared keys: {', '.join(unknown)}")
        missing = sorted(RECEIPT_FIELDS - set(document) - {"previous_receipt", "delta_digest"})
        if missing:
            raise MigrationError(f"receipt is missing: {', '.join(missing)}")
        return cls(**{name: document.get(name) for name in RECEIPT_FIELDS})


class MigrationChain:
    """An ordered, gapless, unskippable sequence of receipts for one ontology.

    Validated whole at construction, because a chain that is checked lazily is
    a chain whose middle nobody has read.
    """

    def __init__(self, receipts: Iterable[MigrationReceipt]) -> None:
        self.receipts = tuple(receipts)
        self._validate()

    def _validate(self) -> None:
        if not self.receipts:
            return
        ontologies = {receipt.ontology for receipt in self.receipts}
        if len(ontologies) != 1:
            raise MigrationError(
                f"a chain covers one ontology; this one names {len(ontologies)}: "
                f"{', '.join(sorted(ontologies))}"
            )
        seen_identities: set[str] = set()
        previous: MigrationReceipt | None = None
        for position, receipt in enumerate(self.receipts, start=1):
            context = f"receipt {position}"
            if previous is None:
                if receipt.previous_receipt is not None:
                    raise MigrationError(
                        f"{context} is first and names a predecessor; the chain it "
                        f"belongs to is missing its earlier receipts"
                    )
                seen_identities.add(receipt.from_hash)
            else:
                if receipt.from_hash != previous.to_hash:
                    raise MigrationError(
                        f"{context} starts at {receipt.from_hash[:19]}… and the receipt "
                        f"before it ended at {previous.to_hash[:19]}…: a change between "
                        f"them was never recorded, and a chain with a gap in it cannot "
                        f"say what the records in that gap meant"
                    )
                if receipt.previous_receipt != previous.digest:
                    raise MigrationError(
                        f"{context} does not name the receipt before it; the link is "
                        f"what makes the chain unskippable"
                    )
            if receipt.to_hash in seen_identities:
                raise MigrationError(
                    f"{context} returns the ontology to an identity it already had. "
                    f"A cycle makes 'which rules governed this record' unanswerable"
                )
            seen_identities.add(receipt.to_hash)
            previous = receipt

    @property
    def head(self) -> str | None:
        """The identity the chain ends at, or None for an empty chain."""
        return self.receipts[-1].to_hash if self.receipts else None

    def accepted_hashes(self, current_hash: str) -> tuple[str, ...]:
        """Every identity a ledger may carry and still be read under `current_hash`.

        Walks backwards from the current identity and stops at a hard break,
        because a hard break is the author saying records before it cannot be
        read under the new ontology at all. Stopping there is the difference
        between a declared break and a silent one: the refusal still happens,
        and now it happens for a reason somebody wrote down.
        """
        _digest("current ontology hash", current_hash)
        accepted = [current_hash]
        for receipt in reversed(self.receipts):
            if receipt.to_hash != accepted[-1]:
                continue
            if receipt.grade == HARD_BREAK:
                break
            accepted.append(receipt.from_hash)
        return tuple(accepted)

    def explain(self, recorded_hash: str, current_hash: str) -> str:
        """Why a recorded identity is or is not readable now. For an operator."""
        accepted = self.accepted_hashes(current_hash)
        if recorded_hash in accepted:
            crossed = [r for r in self.receipts if r.to_hash in accepted]
            return (
                f"readable: {len(crossed)} recorded change(s) connect "
                f"{recorded_hash[:19]}… to the current ontology"
            )
        # If the walk back stopped at a hard break, that break is the answer,
        # whether the recorded identity is the one it broke from or an older
        # one behind it. Telling an operator "nothing connects this" when a
        # recorded decision is the reason sends them looking for a missing
        # receipt that was never missing.
        reached = accepted[-1]
        known = {h for r in self.receipts for h in (r.from_hash, r.to_hash)}
        for receipt in self.receipts:
            if recorded_hash not in known:
                break  # a stranger to this chain, not something a break excluded
            if receipt.to_hash == reached and receipt.grade == HARD_BREAK:
                return (
                    f"not readable: {receipt.reason}. The change recorded at "
                    f"{receipt.issued_at} was declared a hard break, so nothing before "
                    f"{receipt.from_hash[:19]}… is readable under the current ontology"
                )
        return (
            f"not readable: no recorded change connects {recorded_hash[:19]}… to the "
            f"current ontology. An unrecorded change cannot be stepped over"
        )

    def verified_against(self, registry: Any) -> "MigrationChain":
        """Check the chain actually ends where this registry is.

        Only the head can be checked. Every earlier identity describes bytes
        that no longer exist, which is why they are recorded rather than
        recomputed.
        """
        if self.receipts and not registry.verifies(f"sha256:{registry.content_hash()}") :
            raise MigrationError("registry cannot verify its own identity")
        head = self.head
        if head is not None and not registry.verifies(head):
            raise MigrationError(
                f"the chain ends at {head[:19]}… and this ontology is "
                f"sha256:{registry.content_hash()[:12]}…: the chain describes a "
                f"different ontology, or a change after its last receipt went "
                f"unrecorded"
            )
        return self

    @classmethod
    def load(cls, path: str | Path) -> "MigrationChain":
        """Read a chain from a JSON document, or refuse."""
        source = Path(path)
        try:
            document = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise MigrationError(f"cannot read migration chain '{source}': {error}") from error
        if not isinstance(document, list):
            raise MigrationError(f"migration chain '{source}' must be a JSON array")
        return cls(MigrationReceipt.from_dict(item) for item in document)

    def save(self, path: str | Path) -> Path:
        target = Path(path)
        target.write_text(
            json.dumps([r.as_dict() for r in self.receipts], indent=2) + "\n",
            encoding="utf-8",
        )
        return target


def migration_chain(registry: Any) -> MigrationChain:
    """The recorded changes for one bundled ontology, or an empty chain.

    A chain lives beside the schema it describes, named for it. Absent means
    no change was ever recorded, which is different from no change ever
    happening and is exactly why an unrecorded change cannot be stepped over.
    """
    schema_path = Path(registry.schema_path)
    chain_path = schema_path.with_name(f"{schema_path.stem}.migrations.json")
    if not chain_path.is_file():
        return MigrationChain(())
    return MigrationChain.load(chain_path).verified_against(registry)
