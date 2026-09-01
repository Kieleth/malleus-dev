# Malleus core: overseer review and handover

Reviewed 2026-09-01 against `bb56848`. Main moved to `4fabab2` during the review;
a second session was committing throughout. Every number below was measured, not
recalled. Where a claim could not be verified it says so.

---

## 1. The state in six numbers

| | |
|---|---|
| Commits since the program base `c410f11` | **204** |
| Of those, touching `src/malleus/` | **12** |
| New library lines | 3,314, of which **3,018 are excluded from the wheel** |
| Design + tests + scripts + conformance | ~93,000 lines |
| Workstreams integrated | **4 of 72** (rig, docs, environment, inventory) |
| Production / wire / packaging workstreams begun | **0 of 33** |

Package version is `0.13.3`, unchanged since 2026-08-20. HEAD is 213 commits past
that tag. `CHANGELOG.md` has no `[Unreleased]` section. **An adopter installing
from PyPI today gets none of it.**

---

## 2. What actually shipped

Wheel diffed at both ends of the range: same 38 files, zero added, five changed.

**One real capability: the lean review protocol** (`21577f8`, 2026-08-26).
`REVIEW_REQUESTED`, `REVIEW_RECORDED`, `REVIEW_DISPOSITIONED` with handlers, seven
projection fields, five new classes, assent ontology 0.9.0 -> 0.10.0, eight tests.
This is the ledger door for human review. It is not part of the contract-compiler
program.

**From the contract compiler: nothing ships.** No public name reaches it, no module
under `src/malleus/` imports it, and the wheel `exclude` keeps all of it out. Its
only consumers are `tests/` and `scripts/ci.py`.

---

## 3. Defects, most severe first

Each one verified. `file:line` given where it exists.

### D1. `status.py` denies a capability that shipped six days ago
`src/malleus/status.py:112` lists `review-report-recording` as pending. The door
exists: `EventType.REVIEW_RECORDED` with `PAYLOAD_FIELDS == {'findings','report'}`
and a bound handler. `docs/IMPLEMENTATION_STATUS.md:318` still calls it "the type
exists in the schema with no protocol door", and `:199` says OCR is blocked on it.

This is the machine-readable boundary the maintainer skill mandates reading before
any capability claim, and it is wrong about the only capability this program
shipped. `tests/test_inquisition.py:939` checks that named gaps appear in the
pending list; nothing checks the converse.

**Fix:** move it to `implemented_capabilities`, correct both prose sites, and add
the converse census so a shipped capability cannot stay listed as pending.

### D2. `tests/contract_compiler/` is not collected
`pyproject.toml` `testpaths` names three governance test files individually and
omits the directory holding the behavioural tests. Default suite collects 1,948
tests; the directory holds **371** that are never run. Only `scripts/ci.py:74`
picks them up, as a separate command.

Run directly under the repo's own `[dev]` install: **28 fail**, all from D3.

**Fix:** add `"tests/contract_compiler"` to `testpaths`. It will go red. That is
the point.

### D3. The LinkML pin is hard-coded in the executor and undeclared as a dependency
`src/malleus/_contract_compiler.py:1171` refuses anything that is not exactly
`linkml == 1.11.1`. `pyproject.toml:28` declares `linkml>=1.10`. With 1.11.1
installed, 284 of 285 conformance tests pass, so the code is right and the
declaration is wrong. CI passes only because 1.11.1 is currently newest on PyPI;
it goes red on the next LinkML release with no code change.

**The lock already exists.**
`conformance/contract_compiler/v0/compiler_environment/requirements.lock` carries
`linkml==1.11.1 --hash=sha256:d1bbb97a...`. It is simply not wired to `pyproject`.

**Fix:** wire it. This is the highest value-per-line change in the list.

### D4. Version 0.13.3 names two different artifacts
`pyproject.toml:7` has not moved since the 0.13.3 release. Since then: eight
commits including `migration.py` and the slot promotion, then 204 more, plus the
assent ontology bump. A wheel built from main today is labelled `0.13.3` and is not
the released 0.13.3.

### D5. The ownership gate does not inspect `main`
`scripts/contract_compiler_integration.py:760-830` enforces scope only over a
declared `base..head` candidate range. `program.md` claims "CC-000 inspects every
commit's touched paths". It inspects candidate commits only.

Concrete instance: `e0e72d9` landed 2,613 lines into `_contract_compiler.py` and
its profile, both CC-R02 scopes, **more than a day before CC-R02 was activated**
and before CC-R01 completed. Both checks pass. Of 41 files in `src/malleus/`,
three are inside any card scope.

### D6. The overseer ledger is hand-rewritable
Only 32 of 297 entries are pinned outside the ledger directory. A forged entry with
a recomputed chain and updated head passes both checks clean. The external anchor
in `integration.json` sits at `entry_count: 119` against a head of 297, and the
validator explicitly permits a behind anchor: **178 entries past the checkpoint**.

The README acknowledges this and promises CC-000 will bind the values. That promise
is roughly 40% delivered.

### D7. The domain-neutrality test blanks the field it checks
`tests/contract_compiler/test_greenhouse_compiler.py:224`,
`test_compiler_policy_is_machine_readable_and_domain_neutral`, asserts `"greenhouse"`
is absent from the profile and one line earlier sets `support_profile = ""`. The
real value was `malleus.linkml/greenhouse-bootstrap-v0`, copied into the shipped
compilation attestation, so a conformance fixture held normative identity.

Value fixed in `4fabab2`. **The blanking line is still there.**

### D8. Mandatory ATTEST content is missing and nothing checks for it
`program.md:497` requires every implementation workstream to record exact commits,
file digests, dependency lock, commands, results and a mutation inventory naming
each operator and survivor disposition. CC-R01's ATTEST block has no mutation
inventory and no dependency lock. `conformance/contract_compiler/v0/evidence/CC-R01.json`
contains zero occurrences of "mutation". Neither governance script greps for it.

The one completed implementation workstream passed COMPLETE on evidence the program
declares insufficient.

### D9. The `test:` / `feat:` sequence is not TDD evidence
`6428dc1` added 378 implementation lines. 70 seconds later a `test:` commit deleted
all 378 to manufacture a RED. 65 seconds after that a `feat:` commit restored them
with two trivial changes. The worker ledger discloses and supersedes its own bad
claim, which is to its credit. The tests were still written against code that
already existed.

### D10. The compiler cannot compile any malleus ontology
All six bundled schemas refuse at the first root field:
`schema root contains unsupported field 'prefixes'`. It compiles one thing, the
Greenhouse fixture authored to fit it. The program is explicit that general LinkML
support is deferred (OD-008), so this is scope, not a lie. Worth stating out loud
because D7 made it easy to miss.

### D11. `ruff` excludes seven files that have never existed
`pyproject.toml:236` lists `conditions.py`, `evaluator.py`, `llm_client.py`,
`runner.py`, `session.py`, `static_loader.py`, `tools.py`. `git log` returns nothing
for any of them. Ten commits in the range touched `pyproject.toml` without noticing.

### D12. A HERESY rite ships that the shipping library fails
`rubric.yaml` went v9 -> v12 and added `single_ledger_knowledge_change` at HERESY,
asking whether every governed change uses one `KnowledgeChangeSet` with no
independent accepted-state write path. `docs/PRINCIPLES.md` §7 states Malleus itself
"does not yet expose a generic `KnowledgeChangeSet` artifact."

---

## 4. Documents that are now false

| File | Wrong how |
|---|---|
| `src/malleus/status.py` | D1; version 0.13.3; stage 8c |
| `docs/IMPLEMENTATION_STATUS.md` | D1; `:291` says "Not implemented: a migration receipt" while `migration.py` implements and ships it; zero mentions of the compiler |
| `ROADMAP.md` | `:264` "Still open, and the smaller half: a migration receipt" |
| `CHANGELOG.md` | Last entry 0.13.3; nothing for 204 commits |
| `docs/KNOWLEDGE_GRAPH_PROTOCOL.md` | Correct as of 2026-08-31, and directly contradicts `IMPLEMENTATION_STATUS.md:291` |
| `design/contract_compiler/decisions.md:380` | "CC-002 materialization remains pending"; the overseer records CC-002 COMPLETE |
| `docs/ARCHITECTURE.md:495` | Calls it "the future contract compiler"; the only adopter-facing mention anywhere |

---

## 5. Vendored wheels: removed

`conformance/contract_compiler/v0/compiler_environment/wheelhouse/` held **90 wheels,
33 MB**, including Babel 9.7 MB, Sphinx 3.7 MB, SQLAlchemy 3.2 MB. Removed from
index and working tree on 2026-09-01.

Kept, and defensible under retained-input policy: `roots/` (LinkML source tarballs,
3.7 MB), `build-inputs/` (1.1 MB), the JSON records and `requirements.lock` (732 KB).

**Six tests now fail**, in `test_contract_compiler_environment.py` and
`test_contract_compiler_divergence.py`. Seven ledger entries pin wheel digests.
Those must be reconciled: either the tests drop the wheelhouse requirement, or the
CC-002 evidence is restated to bind the lock rather than the binaries.

**The 33 MB remains in git history.** `.git` is 76 MB. Removing it from history
requires a rewrite (`git filter-repo`), which invalidates every commit hash after
the first wheel commit, breaks the two paper repositories that are worktrees of this
object database, and breaks every digest the overseer ledger pins to a commit.
**Not attempted. It is a separate decision with a large blast radius.**

---

## 6. What was done well, and should not be re-litigated

`_contract_compiler.py` is not scaffolding. Under the correct LinkML it compiles the
baseline into 90 canonical subject-predicate-object facts with content-addressed
structural URNs, a stable digest and an implementation attestation.

`_validate_profile` refuses any profile member that no code path consumes
(`_contract_compiler.py:472` and fifteen siblings). That is a stronger version of
the `tests/test_ocr.py` census pattern, enforced at load rather than by a
hand-maintained table.

The CC-X04 historic-wire corpus measured the current reader **before** the decision
it fed. OD-004 then chose a typed hard break and stated the cost in its own text:
"This deliberately gives up new-reader replay of the two inputs that the current
Recon reader accepts through its receipt."
`docs/KNOWLEDGE_GRAPH_PROTOCOL.md:163-167` reconciles it in public.

That is measure-then-decide, done correctly, and it answers the question of whether
OD-004 orphaned the migration receipt: it did not. It cut the receipt's data path
knowingly and said so. The only gap is that **no workstream owns `migration.py`'s
retirement**; grep of the whole `design/contract_compiler/` tree for `migration.py`,
`MigrationChain`, `MigrationReceipt` returns zero hits.

---

## 7. Do these first

1. Add `"tests/contract_compiler"` to `testpaths` and pin `linkml==1.11.1` from the
   existing `requirements.lock`. **D2 and D3, and D3's fix is already written.**
2. Fix `status.py` and the two prose sites for `review-report-recording`. **D1.**
3. Reconcile the six wheel failures and the seven ledger digest pins. **§5.**
4. Cut a release with an honest changelog, or set `version` to something that is not
   a released tag. **D4.**
5. Delete the blanking line in the domain-neutrality test. **D7.**
6. Remove the seven phantom ruff excludes. **D11.**

---

## 8. Not determined

- Whether CI is currently green on `main`. Not queried.
- What is published on PyPI as 0.13.3. Inferred from `b5a72a6`, not fetched.
- Whether CC-002's MCP acquisition replay happened. `FakeServices` is defined in the
  test; the retained wheel digests were not verified against the recorded ones.
- Whether the four new HERESY rites fire. They are judgment tier, read but not run.
- Whether the independently authored oracles were independent. All 204 commits are
  authored by one identity, so git provides no evidence either way.
