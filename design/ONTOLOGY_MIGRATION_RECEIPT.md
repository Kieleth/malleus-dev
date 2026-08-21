# The migration receipt

What a malleus ontology change is, what records it, and what malleus refuses.

Status: the total grade is built and shipped (`src/malleus/migration.py`).
The partial and hard-break grades are declarable and their reading rules are
not yet executable. Two recons are open on the parts
this document marks unsettled. Nothing here authorises core implementation;
`ROADMAP.md` A8 and B3 still govern that.

---

## The correction that shapes everything else

A database migration **rewrites stored rows**. You alter the table, yesterday's
rows take today's shape, and the old shape stops existing.

Malleus cannot do that and the fact that it cannot is the entire value. The
ledger is append-only. A record written under one ontology stays exactly as
written, forever.

So a malleus migration never transforms a record. **It transforms how a record
is read.**

That is stricter, not looser. A data migration succeeds once, on one Tuesday,
and is then over. A reading rule must be total over every record ever written
and must keep working on every future read.

Everything below follows from that sentence.

---

## What a receipt is

A record, written into the same append-only log as the data, at the moment the
ontology changes. It says: before this line, ontology A. After it, ontology B.

The precedents are consistent about its shape. TUF root rotation makes the
switching record verifiable under both the old and the new identity, requires
the position to be exactly the previous one incremented, and forbids skipping
intermediate records. `did:webvh` makes the rules-version upgrade an entry in
the hash chain itself, with each entry hashed over its predecessor's version
id. Delta Lake puts the schema change in the same log as the data. Malleus
should look like these.

---

## Settled

### S1. A receipt is never revoked

Only superseded by another forward change. Crossing out a receipt makes every
record written between it and the correction unreadable, which trades three
days of history for one line of embarrassment. Every append-only precedent
inspected agrees.

### S2. Every ontology a receipt names stays readable forever

Accepted knowingly, and it has a bill that is not conceptual. Each named
grammar needs a live conformance fixture that exercises it, permanently, or
"readable forever" becomes a claim nobody measures and the reading code rots
until the day it is needed. This is the same defect as a guard nobody has seen
fail. The test suite grows a section that only ever gets longer.

One database refuses this property outright and says why: travelling back in
time does not take the schema back, because the machinery for the old schema
may no longer exist. RFC 7696 section 4 requires the opposite for stored data.
Malleus has an append-only ledger, so it has already chosen; it has not yet
paid.

### S3. The unit of guarantee is a bundled release, not a single ontology

What malleus guarantees to work together is a set: the ontologies plus the code
that reads them. Adopters take a bundle or stay on an older one, and the
migration tooling exists so moving between bundles is mechanical rather than
archaeological.

Consequence, and it corrects an earlier proposal: the receipt binds **bundle**
identities, not single-ontology identities.

### S4. Malleus consumes no external ontology bytes

Verified rather than assumed. `ontology/malleus.yaml` declares one import,
`linkml:types`, and `src/malleus/ontology.py` skips it explicitly. The `prov:`,
`bfo:` and `sosa:` prefixes are URI namespaces, not consumed bytes.

So the vendored-bytes problem is not ours to solve for ourselves. It remains
ours to supply downstream, because an adopter's vendored copy of our schema is
what got silently swapped in the incident that raised it.

### S5. The delta is recorded and checked, not recorded and trusted

Three layers, not three alternatives:

- **Prose.** What most systems ship. Unverifiable.
- **A typed delta.** KGCL already exists, is LinkML, and carries node and edge
  changes with `old_value`, `new_value` and `has_undo`. Do not invent one.
- **The reading rule.** Given a record written under A, what it means under B.
  KGCL does not supply this and binds no version identity at all.

The recorded delta is a convenience. The derivation from the two ontologies is
the authority. A test compares them, so the recorded delta cannot lie. This is
the pattern already used for the conformance projection, generated from the
registry and never hand-edited.

### S6. Three grades of reading rule, and silence is the only thing refused

A change is legitimate when it arrives with a rule of one of these grades, and
the grade is declared:

1. **Total.** Every record written under A has a meaning under B. The common
   case, and the default the tooling should make effortless.
2. **Partial, declaring its own gaps.** The rule names the records it cannot
   interpret and refuses to answer for them, rather than guessing or dropping
   them. Those records are addressable, countable, and consumable by nothing
   that computes an answer. This is the same mechanism as the provisional
   concept and the pointer frontier: a known unknown with a name.
3. **A hard break.** Records before the receipt cannot be read under B at all,
   and the receipt says so in those words.

Some changes have no total rule and this is not laziness. Removing a required
field leaves no meaning for records that carry it. Narrowing text to number
leaves `"abc"` with no image. Splitting one class in two leaves an old record
with no answer to which it belongs to. These need judgment per record and no
rule supplies it.

**What malleus refuses is a break that is not declared.** You may break
history. You may not break it silently.

Posture: the default handles the common case without thought, and the rest is a
declared extension point rather than a special case in the engine.

---

## Built

`MigrationReceipt` binds one ontology, the outgoing identity, the incoming
identity, the grade, a reason, a timestamp, the digest of the receipt before
it, and optionally the digest of a declared delta. `MigrationChain` validates
the whole sequence at construction, because a chain checked lazily is a chain
whose middle nobody has read.

Four refusals, each closing a way the chain could lie. A gap, where one
receipt does not start where the previous ended, because a chain with a hole
cannot say what the records in the hole meant. A broken link, since naming the
predecessor by digest is what makes the chain unskippable. A cycle, which makes
"which rules governed this record" unanswerable. And a chain whose head is not
the ontology it claims to describe.

A hard break truncates what is readable, and the refusal that follows carries
the recorded reason instead of silence. An identity the chain never mentions is
told it is missing a receipt, not told it hit a break, because sending an
operator to hunt for a decision nobody made is its own defect.

Only the head can be verified against a live registry. Every earlier identity
describes bytes that no longer exist, which is exactly why they are recorded at
the time rather than derived later.

The first customer is real: promoting `reviewer_id` into the root grew recon's
slot closure by a name it never used and shut all ten recon projects. The
receipt, graded TOTAL because no record means anything different, reopens them.
Removing it shuts them again.

## Not settled

### U1. Branch and merge of ontology versions

The motivating case is real and named: a domain close to the core, `ocr` or
`recon`, needs a concept the root does not offer or needs a root concept
changed. Today the moves are to change the root and force every importer to
absorb it, or to invent a local answer and diverge permanently. The second is
how a domain quietly reinvents a mechanism the root should have owned, which
has already happened here.

The wanted third move is a domain evolving its own extension and merging it
back upstream once it proves itself, without rebuilding the domain ontology.

Against doing it now: of everything the first recon inspected, nothing performs
branch and merge for schema versions. TUF requires strictly sequential and
unskippable. `did:webvh` chains each entry to its predecessor. Git can merge
because it merges text and a human resolves the conflict, and a text merge of
two schemas can load cleanly while meaning something nobody intended. Merging
two divergent ontologies properly is ontology alignment, an open research
problem rather than an engineering task.

Position: identified, not urgent. A linear chain first, with the DAG left
possible rather than foreclosed. A recon is open on the extension and promotion
patterns that would make the third move cheap without a merge at all.

### U2. What authorises a receipt

Malleus owns the root, so malleus authorises root changes and each project
authorises its own. That answers who and not how. The mechanism that records
the authorisation is unexamined, and malleus already has one candidate in the
epistemic decision path, which currently has no consumer outside the paper.

The knot to resolve before designing: the receipt is about changing the
ontology, so which ontology is the receipt itself written under. TUF's answer
is that the switching record is valid under both and is signed twice.

### U3. Granularity below the bundle

S3 fixes the unit of guarantee. It does not decide whether a receipt records
one change per bundle, per ontology, or per element. Prior art points three
ways: per module, per field with stable identifiers, or whole-document
rotation.

---

## What the recons are for

`research/ontology_migration_recon/` is complete and established the shape of
the record: identifier beside the digest, two identities bound in a chained
unskippable entry, KGCL as the delta language, and a negative audit showing
nobody binds an outgoing and incoming digest in one record.

Two are open. One on how a reading rule is expressed, executed and authorised,
which decides S6's mechanics and U2. One on downstream extension and upstream
promotion, which decides whether U1 needs a merge at all.

The stage contract is not written until the reading-rule question is answered,
because it decides what the receipt has to carry.
