# Roadmap

Candidates for later grooming. Nothing here is committed work. Each item
records what earned it, so that grooming can weigh evidence rather than
enthusiasm.

Two standing rules govern promotion into this file and out of it:

- **A concept promotes on the second consumer, not the first.** One project
  wanting something is a local solution; two independent projects wanting it
  is shared vocabulary. Designing a general API from a single example
  produces an API shaped by that example's accidents.
- **Rites for capabilities malleus does not provide enter at NOTE with
  `status: open_question`, never at HERESY.** Condemning adopters for lacking
  what we do not offer is the defect three self-inquisitions removed from our
  own documents.

---

## A. From adopters, via the upstream channel

Lessons sent up by an adopting project, already written project-free. Source
document held locally by that project; only the generic lesson travels.

### A1. Per-instance reader coverage (refines `reader_census`)

A reader census is satisfied by one reader touching one instance, so a type
can be read once, extended with a hundred new instances, and stay green while
none of the hundred is reached. Reported case: two dozen rows, every row
cited to its source and counted by an invariant, referenced by exactly one
thing in the repository, which was the generator that wrote them. A
neighbouring path reached the same content through a side door, so the type
had a reader and the census was clean. Found by auditing output; no gate saw
it.

Proposed severity is conditional, and the condition is good: SUSPICION where
unread data means wasted storage, HERESY where the graph is the program,
because unread rules are absent behaviour rather than dead weight.

Two mechanical discharges, catching different amounts: a static walk from
entry points (cheap, blind to side doors, which was 17 of 23 in the reported
case), and a runtime journal of touched ids plus a sweep (complete, costs a
journal).

**Verdict: accept as a rite.** Groom the severity condition.

### A2. Fidelity, coherence and consequence are three claims

Projects conflate them because they are all "the checks pass". Fidelity: the
data matches its source. Coherence: the assembled graph is well-formed.
Consequence: the system acts on it. A project can hold the first two to an
unusually high standard and have no vocabulary for the third, and the
strength of the first two is what makes the absence invisible.

**Verdict: accept at NOTE.** Needs a `status:` field to load under rubric v7.

### A3. A declared-unread annotation

Schemas commonly have a slot for a partially expressed rule. There is no
mirror for a record that is fully expressed and never invoked. Without a
declared-exception slot a coverage gate has two settings, pass and nuisance,
and the second gets it switched off. With one, the gap is a countable set of
argued exceptions instead of a silence.

**Verdict: accept at NOTE.** Pairs with A1; groom them together.

### A4. Guidance newer than runtime

A resolution order that tries the installed package first and a local
checkout second degrades in the dangerous direction: the fallback is not
equivalent, it is newer. The adopter reads the current rubric and protocol
docs while running a package several minor versions old. Reported as an
`ImportError` from a bootstrap step against an installed 0.1.0 with a 0.6.0
checkout beside it, the symbol having been added in between. This is
`root_currency` inverted, and worse, because that rite compares two copies of
the root while this compares documentation against code and nothing diffs
them.

Concrete fix, small: make the version a first-class output of the bootstrap
step. `malleus-inquisitor` already prints the rubric path, version and
digest; it should also print the installed malleus version and the resolved
bundled root, so one command answers "which root am I actually running
against" and a stale install announces itself.

**Verdict: accept the rite, and do the CLI line soon.** It is one line and it
closes a confusing first-contact failure.

### A5. Unknown-range blast radius (highest value in this batch)

Three defects, one root:

1. The loader's range allowlist is five names where the schema language
   defines nineteen. The missing fourteen include the double-precision float,
   the decimal, the date and the URI, which are the ones an adopter reaching
   for precision uses first. Rejecting a legal built-in punishes an adopter
   for using their tools correctly.
2. Construction is rite one and a failed rite one short-circuits the run, so
   one unrecognised name silently blinds every later rite on that file and on
   every file importing it. Reported: five files of thirteen failed to
   construct, and seven of eight mechanical rites had therefore never
   executed anywhere in that repository, with nothing in the report saying so.
   Construction failure should report the rites it prevented.
3. **The tool manufactures findings against correct schemas.** Run without
   `--map` on a schema importing a sibling, it reports "does not construct",
   indistinguishable in the output from a real failure. Twelve schemas
   appeared broken and none were. Either resolve sibling imports relative to
   the inspected file by default, or say `CANNOT INSPECT` rather than
   `HERESY`.

**Independently corroborated.** A second, unrelated project lost its schema
to the same allowlist gap on `uri` in the same week. Two projects, one hole,
found separately.

**Verdict: accept all three, highest priority in this file.** (3) first: an
adopter's first run is exactly when they cannot tell a manufactured finding
from a real one.

### A6. Provisional concepts (feature, not just a rite)

Documents introduce terms before defining them; that is normal prose, not a
defect in the source. A knowledge system with no provisional state offers its
writers three moves and all three are bad: invent the definition, refuse the
passage, or store an unresolved string and promise to fix it later. The third
gets chosen because it is the only one that lets the ingest continue, and it
reintroduces magic strings under a name nobody is watching.

The proposal: a typed provisional status that is addressable and
referenceable, that names the source location forcing it, that no executable
path may consume, and that is cleared only by a definition being found and
judged. Lewis's rule of accommodation is the formal ancestor, and the
objection clause is the part a knowledge system has to supply.

The trap, correctly identified by the proposer: reference counting may rank
the backlog and must never settle a concept. A concept referenced forty times
and never defined is the most important open question in the ingest, not
thereby defined. Promotion by accumulated weight rebuilds a half-open gate on
precisely the entities the graph leans on hardest.

Distinct from staging: staging asks whether a claim has been assented to;
accommodation asks whether a concept is fully known. A staged claim about a
settled concept and a committed claim about a half-known concept are
different states.

**Verdict: the design deserves real consideration; the rite does not enter at
HERESY.** As proposed it would condemn every adopter for lacking a capability
malleus does not offer, which is the exact defect rounds three through six
removed from our own documents. Either the capability lands first, or the
rite enters at NOTE with `status: open_question` like
`module_declares_its_interface`.

---

## B. From our own use

### B1. A commitment-lifecycle facade

Measured on a real adapter that drives one proposal through the full
lifecycle: **644 lines of generic lifecycle against 105 lines of domain
content.** The generic part is artifact, source, graph-base, candidate,
monitor-specification and policy construction, proposal-member assembly,
state transitions, and accepted-graph application. `AssentPlan` (0.8.0)
orchestrates the monitoring step and leaves the stages either side of it to
the caller.

The pain is real and it is the same class that earned `get_relation`,
`export_records`, `from_records` and `schema_version`. It is also the class
our own doctrine lists under default exclusions ("orchestration layers"), and
promotion needs a second consumer.

**Verdict: do not build in core yet.** Let the pattern be extracted locally by
its user, and revisit when three adapters exist and the shape has stopped
moving. Design the facade from three examples or not at all.

### B2. Make a construction failure report its blast radius

Same as A5 (2), reached independently: a report that shows one heresy per
file and says nothing about the seven rites it skipped invites the reader to
conclude that everything else passed.

**Verdict: accept, groom with A5.**
