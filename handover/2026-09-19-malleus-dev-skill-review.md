# Review of the malleus-dev skill, 2026-09-19

Subject: `.claude/skills/malleus-dev/SKILL.md` at 471 lines, uncommitted working
tree, read together with its two references, the paper and acolyte skills,
`docs/PRINCIPLES.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/DELIMITATIONS.md`,
`ROADMAP.md` section F, paper ledger E-0430 to E-0489, and the five test files
that read skill text.

Proposals only. Nothing was edited, staged or committed. Line numbers are the
working-tree file as read on 2026-09-19.

Guard tests that can break on a malleus-dev sentence edit, established by
reading them:

| Test | What it holds |
|---|---|
| `tests/test_inquisition.py:883` `test_every_shipped_skill_carries_the_scope_gate` | `"## Before you build"`, `"smallest observation"`, `"exclude"` must stay |
| `tests/test_inquisition.py:894` `test_no_skill_sends_a_reader_to_a_path_that_will_not_exist` | any `src/malleus/...` mention needs `"import malleus"` or `"checkout"` within 700 characters |
| `tests/test_inquisition.py:840`, `:869`, `:938`, `:969`, `:981` | corpus-wide denial guards over every skill `.md` |
| `tests/test_inquisition.py:1645` `test_every_shipped_skill_has_valid_metadata` | frontmatter keys exactly `{name, description}`; `agents/openai.yaml` `short_description` 25 to 64 characters |
| `tests/test_inquisition.py:1685` `test_malleus_dev_skill_carries_the_accepted_modularity_doctrine` | three literals verbatim and unwrapped: `"LinkML is not the protocol"`, `"Any custom frontend may replace LinkML"`, `"must run without LinkML installed"` |
| `tests/test_inquisition.py:1723` `test_malleus_dev_skill_keeps_profiles_and_fixtures_in_their_roles` | the five role names, plus 11 phrases in whitespace-normalised text |
| `tests/test_status.py:265` `test_malleus_dev_skill_gates_research_and_projection_claims` | 12 typed labels must parse as `N. \`LABEL\`: text` or `- \`LABEL\`: text`, no duplicate label in the file, and body regexes per label |
| `tests/test_capability_declaration.py:206` | `"CAPABILITIES.md"` and `"before declaring a gap"` must stay in the file |
| `tests/test_contract_compiler_environment.py:901` | the `## MCP preflight` section's literals and the `](../../../.codex/README.md)` link, which must resolve |
| `tests/contract_compiler/pareto/test_adopter_completion_boundary.py:21` and `:81` | the heading `## Before you build: bind the slice` and the two acolyte links inside it |

Nothing under `paper-v4/` can break on a working-tree skill edit: those tests
read skills through `git show <pinned commit>:path`, never the working tree.

---

## 1. Facts against the code

### 1. Core does not run the rules at admission (must fix)

**Location.** "Rules and the ontology", lines 162 to 165.

**Current text.** "A `PolicyProgram` in the normative profile selects it by
contract id and contract identity. `PrologVerifier` runs it at admission over
the compiled facts of the candidate state."

**Problem.** The second sentence says Core runs the check. Core does not.
`grep -rn "PrologVerifier" src/malleus/` returns `runner.py:113`,
`session.py:118` and the `__init__` export, all on the Assent path. Nothing in
`src/malleus/_contract_pipeline/` imports it. What Core does at admission is
read *recorded* check outcomes and map them to verdicts:
`_contract_pipeline/machine.py:1156` `_require_policy_check` refuses a check the
policy does not require and an identity that does not match, and
`machine.py:1183` `_select_verdict` folds the recorded outcomes. Both live
consumers run the verifier themselves:
`private/shop-progressive-01/d0/runner.py:606`, inside `_check_and_admit`
(`:591`), reads `checked = PrologVerifier(logic).verify_candidate_subgraph(`;
`paper-v4/experiment-v4/content-rules-doc-02/admit.py:273` does the same.
`ROADMAP.md:1024` states it in the library's own words: "Today an adopter's
runner compiles a population plan, runs the PolicyProgram's Prolog check itself,
writes a check receipt, and only then calls `admit_with_anchors` ... the sequence
and the running of the rules live in adopter code". `docs/IMPLEMENTATION_STATUS.md:83`
agrees: the Shop episode "runs the existing Prolog checker", and "an explicitly
selected policy rejects the actual violated check".

The first sentence is correct. `PolicyProgram.required_checks` is a tuple of
(contract id, identity) pairs at `_contract_pipeline/machine.py:571`.

**Proposed text.** Replace the second sentence with: "The adopter's runner runs
it. The runner compiles the plan, calls `PrologVerifier` over the compiled facts
of the candidate state, writes a check receipt, and only then admits. Core reads
the receipt and never the rule: it refuses a check the policy does not require, a
wrong check identity and a violated verdict, and it runs no Prolog. Moving that
sequence into one Core call is ROADMAP F1, dispatched 2026-09-19 and not landed
(E-0486, E-0488, E-0489)."

**Guard.** None asserts this sentence. If the replacement names a
`src/malleus/...` path, `tests/test_inquisition.py:894` requires `"import
malleus"` or `"checkout"` within 700 characters; the wording above names no path.

**Priority.** Must fix. This is the load-bearing sentence of the section Luis
asked to be crystal clear, and it describes a capability Core does not have.

### 2. The Shop worked case has no `RESULTS.md` (must fix)

**Location.** "Choose an adopter rule", lines 150 to 152.

**Current text.** "Worked case, with mechanisms per refusal in each `RESULTS.md`:
`research/ontology_driven_kg_realization/experiments/small_shop/content_rules`
(Shop) and `paper-v4/experiment-v4/content-rules-doc-01` (document)."

**Problem.** That Shop directory holds `CORE_REQUIREMENT.md`, `fact_census.py`,
`logic.yaml`, `policy.json`, `README.md`, `rules.pl`, `run.py` and
`test_content_rules.py`. There is no `RESULTS.md`. The mechanisms per refusal
(62 mapping constants, 69 minted identities, 14 enum translations, recorded at
E-0406) are in that cell's `README.md`. The document cell does carry
`RESULTS.md`. A reader following the instruction as written finds nothing on the
Shop side.

**Proposed text.** "Worked case, with the mechanism of every refusal:
`research/ontology_driven_kg_realization/experiments/small_shop/content_rules/README.md`
(Shop) and `paper-v4/experiment-v4/content-rules-doc-01/RESULTS.md` (document)."

**Guard.** None. **Priority.** Must fix.

### 3. Two refusal names attributed to Core belong to the adopter's runner (must fix)

**Location.** "Rules and the ontology", lines 182 to 183; "Implementation
sequence", lines 434 to 436; "Architectural law", lines 315 to 317.

**Current text.** "The adopter retains the re-pinned contract in the same act, or
the next admission refuses `CHECK_CONTRACT_NOT_RETAINED` (E-0458, E-0465)." and
"the history requires a check contract it does not hold and the next admission
refuses `CHECK_CONTRACT_NOT_RETAINED`. That is not a Core defect" and "refused a
legitimate second anchor with `SOURCE_ALREADY_ANCHORED`".

**Problem.** Neither name exists in Core. `grep -rn "CHECK_CONTRACT_NOT_RETAINED"
src/` and `grep -rn "SOURCE_ALREADY_ANCHORED" src/` both return nothing. Core's
admission refusals are the closed `KnowledgeChangeRefusalReason` enum at
`src/malleus/_contract_pipeline/knowledge.py:125` to `:144`, and neither name is
in it. Both are `RunnerRefusal` values raised by the Shop's own runner:
`private/shop-progressive-01/d0/runner.py:330` and `:464`. E-0465 records them
under "Runner:" for that reason. The text says "not a Core defect" in one of the
three places, which is right, but a reader who greps Core for either name finds
nothing and concludes the skill is wrong about Core.

**Proposed text.** At line 182: "...or the adopter's runner refuses at the next
admission, `CHECK_CONTRACT_NOT_RETAINED` in the Shop's runner (E-0458, E-0465)."
At line 435: same treatment. At line 316: "a runner that named a retained source
after its packet file's stem refused a legitimate second anchor with its own
`SOURCE_ALREADY_ANCHORED`". One sentence somewhere in the section: "Both names
are the Shop runner's, not Core's closed refusal vocabulary."

**Guard.** None. **Priority.** Must fix.

### 4. The compiler-profile section names four abstractions the code does not have (should fix)

**Location.** "Accepted compiler-enabled profile boundary", lines 388 to 399.

**Current text.** "A `ContractFrontend` consumes retained source bytes, an
explicit resolver, and a support profile. It produces a
`ContractCompilationResult` containing canonical contract facts, annotations,
typed diagnostics, and complete lineage. Malleus validates and canonicalizes that
result into an `EffectiveContractArtifact`." and, at line 398, "runtime graph
construction, GraphRecipe, admission, replay, and migration consume the compiled
contract".

**Problem.** `grep -rln "ContractFrontend\|EffectiveContractArtifact\|ContractCompilationResult\|GraphRecipe" src/malleus/`
returns nothing. `docs/PRINCIPLES.md:247` says it outright: "There is no public
abstraction named `ContractFrontend` or `EffectiveContractArtifact`; the shipped
artifact is `ValidatedContractArtifact`." `docs/DELIMITATIONS.md:258`: "GE-000
through GE-020 are research-local; no GraphRecipe runtime ships." The four names
are design-graph objects, `design/PROTOCOL_FOUNDATION_GRAPH.ttl:296` and `:326`,
not Python surfaces. The section is titled "Accepted ... boundary" and its first
paragraph scopes it to a claimed profile, but the prose is in the present
indicative throughout and reads as shipped state.

**Proposed text.** Insert after line 385: "The names below are roles in the
accepted design, recorded in `design/PROTOCOL_FOUNDATION_GRAPH.ttl`, not Python
surfaces. The compiler ships `compile_linkml_contract`,
`ValidatedContractArtifact` and `ContractView`, the first two rows of
`references/CAPABILITIES.md`. There is no `ContractFrontend`,
`ContractCompilationResult` or `EffectiveContractArtifact` in the package, and no
GraphRecipe runtime ships (`docs/PRINCIPLES.md`, principle 6;
`docs/DELIMITATIONS.md`, Recipes)." Leave the rest of the section alone.

**Guard.** `tests/test_inquisition.py:1685` requires three literals verbatim and
unwrapped, at lines 394, 396 and 399: `"LinkML is not the protocol"`, `"Any
custom frontend may replace LinkML"`, `"must run without LinkML installed"`. An
inserted paragraph above them is safe; re-wrapping those three lines is not.

**Priority.** Should fix. The section is honest about profile scope and dishonest
about tense, and this skill's whole authority is that it does not do that.

### 5. The adopter-rule lesson carries a date and no ledger entry, and the date is half wrong (should fix)

**Location.** "Choose an adopter rule", lines 119 to 122.

**Current text.** "Choosing one wrongly cost two measurement cycles on
2026-09-16: 'every value must appear in the sentence it cites' refused 145 of 294
honest Shop derivations and 216 of 236 honest document records, because it was
designed from the fault it should catch and never read against the records it
would govern."

**Problem.** The counts check out: 145 of 294 is E-0406 (paper ledger line
14022), 216 of 236 is E-0426 (line 14144). The dates do not. E-0406 is
2026-09-16; E-0426 is 2026-09-17; the RCA and Luis's rulings are E-0430,
2026-09-17. The section carries no ledger entry at all, while "Rules and the
ontology" cites entries throughout. Luis's standing requirement is dated lessons
with their ledger entry.

**Proposed text.** "Choosing one wrongly cost two measurement cycles, 2026-09-16
on the Shop path and 2026-09-17 on the document path (E-0406, E-0426, E-0430):
'every value must appear in the sentence it cites' refused ..."

**Guard.** `tests/test_status.py:265` reads the labelled items under this heading
by label; the preamble is not asserted. **Priority.** Should fix.

### 6. CC-002 is a codename with no gloss (should fix)

**Location.** "MCP preflight", line 36.

**Current text.** "Before CC-002 work, confirm that server `cc002` and tools
`cc002_acquire` and `cc002_verify_offline` are loaded in the current task."

**Problem.** CC-002 is never explained. It is the "Reproducible selected compiler
environment" workstream, `design/contract_compiler/program.md:390`, with its
manifest at `design/contract_compiler/workstreams/CC-002/manifest.json`. A reader
who has not met it cannot tell what "CC-002 work" is, and Luis's standing
requirement is explicit names, no codenames. The `.codex/README.md` pointer and
both tool names check out against `.codex/README.md:22` and `:57`.

**Proposed text.** "Before work on CC-002, the reproducible compiler-environment
workstream (`design/contract_compiler/program.md`), confirm that server `cc002`
and tools ..."

**Guard.** `tests/test_contract_compiler_environment.py:901` slices on `"## MCP
preflight\n"` and asserts `"server \`cc002\`"`, both tool names,
`"](../../../.codex/README.md)"` with the link resolving, `"If any are absent,
stop"`, the four words `shell`, `package-manager`, `direct-network`, `legacy`,
`"Any change that adds an MCP dependency"` and `"regression test"`. A gloss
touches none of them. **Priority.** Should fix.

### 7. `ShipmentRuleClaim` and one of the two live rule layers have no reachable path (could fix)

**Location.** "Rules and the ontology", lines 168 to 170 and lines 205 to 207.

**Current text.** "Read the two live rule layers before designing here, with
their `logic.yaml` files: `private/shop-progressive-01/producer/workspace-stage-c/inputs/rules.pl`
and `paper-v4/experiment-v4/content-rules-doc-02/rules.pl`." and "The Shop's
`ShipmentRuleClaim` is that already, a rule held as a typed record with its
threshold as a slot, stored and not run."

**Problem.** Both paths exist on this machine and both `logic.yaml` files check
out (Shop `rule_ids: [NO_CONFLICTING_QUANTITY, NO_EMPTY_RECORD]`, document
`rule_ids: [NO_CONFLICTING_QUANTITY, INTERVAL_SANITY, NUMBER_IN_CITED_TEXT,
FORMULA_IN_SOURCE]`). But `/private/` is gitignored at `.gitignore:51`, so a
reader in a fresh clone cannot open the Shop layer and the skill does not say so.
`ShipmentRuleClaim` is given no path at all; it is at
`private/shop-progressive-01/producer/workspace-stage-c/inputs/context.yaml:33`,
admitted at E-0451.

**Proposed text.** Add "the first is local only, `private/` never enters git" to
the first, and the path plus "(E-0451)" to the second.

**Guard.** None. **Priority.** Could fix.

### 8. One of the six live rules is named by description, not by its id (could fix)

**Location.** "Rules and the ontology", lines 193 to 196.

**Current text.** "The six are the census any proposal is read against: the
Shop's `NO_CONFLICTING_QUANTITY` and `NO_EMPTY_RECORD`, and the document path's
conflict-with-modality rule, `INTERVAL_SANITY`, `NUMBER_IN_CITED_TEXT` and
`FORMULA_IN_SOURCE`."

**Problem.** Five rules are named by id and one is described. Its id is
`NO_CONFLICTING_QUANTITY`, the same id the Shop uses for a different rule body,
which is presumably why the writer avoided it
(`paper-v4/experiment-v4/content-rules-doc-02/logic.yaml` and
`private/shop-progressive-01/producer/workspace-stage-c/inputs/logic.yaml`). A
reader cannot grep for "the conflict-with-modality rule".

**Proposed text.** "...and the document path's own `NO_CONFLICTING_QUANTITY`,
which reads `assertion_modality` and is a different rule body under the same id,
plus `INTERVAL_SANITY`, `NUMBER_IN_CITED_TEXT` and `FORMULA_IN_SOURCE`."

**Guard.** None. **Priority.** Could fix, but it is exactly the kind of thing
that makes "one read is enough" fail.

---

## 2. Consistency inside the skill

### 9. Two sections define "adopter rule" differently (must fix)

**Location.** "Choose an adopter rule", lines 117 to 118, against "Rules and the
ontology", lines 160 to 165.

**Current text.** "An adopter rule is a `PolicyProgram` check that runs at
admission over the compiled facts. It is `ADOPTER_CHOICE`." against "A rule layer
is a `LogicContract`: a small YAML file naming a Prolog rules file and pinned to
the hash of the ontology those rules were written against. A `PolicyProgram` in
the normative profile selects it by contract id and contract identity."

**Problem.** The same noun gets two answers 45 lines apart. A `PolicyProgram` is
not a check; its `required_checks` field names (contract id, identity) pairs
(`src/malleus/_contract_pipeline/machine.py:571`). A rule is a clause in the
pinned Prolog file, the `LogicContract` pins the file, and the `PolicyProgram`
requires the contract by identity. The first definition also repeats the "runs at
admission" error of proposal 1.

**Proposed text.** "An adopter rule is one clause in a pinned Prolog rule file,
required by the admission policy and run over the compiled facts of the candidate
state. 'Rules and the ontology' below says exactly what carries it and what moves
when the ontology does. It is `ADOPTER_CHOICE`."

**Guard.** `tests/test_status.py:265` parses the labelled items under this
heading; the preamble is not asserted. **Priority.** Must fix, it is a
contradiction.

### 10. A reader meets every rule term before anything defines it (should fix)

**Location.** Section order: "Choose an adopter rule" at line 115, "Rules and the
ontology" at line 152.

**Problem.** `PolicyProgram`, "admission" and "compiled facts" first appear at
lines 117 and 118; Prolog at line 126. All four are defined at lines 160 to 170,
in the following section. E-0489 records that "Rules and the ontology" was placed
"between 'Choose an adopter rule' and 'Architectural law'", which put the
definition after the use.

**Proposed change.** Swap the two sections: "Rules and the ontology" first (what
a rule is, what carries it, what moves), "Choose an adopter rule" second (how to
pick one). Neither section refers forward to the other today except proposal 9's
new sentence, which would then point backwards. `CORE_PROMOTION` at line 241
points backwards to line 109 and is unaffected.

**Guard.** No test asserts section order in malleus-dev. The ordering assertions
at `tests/test_inquisition.py:2078` to `:2101` are for malleus-acolyte's ten
numbered steps only. The two pareto tests slice malleus-dev by heading name, not
position. **Priority.** Should fix.

### 11. Two rules about what a rule reads, 80 lines apart, with no pointer (should fix)

**Location.** `DECLARED_DISTINCTIONS_ONLY`, lines 135 to 139, against
`RULE_DECLARES_ITS_READS`, lines 212 to 224.

**Current text.** "A rule reads only what the compiled ontology declares. If it
needs a distinction the ontology lacks ... the rule is out of reach." against
"every rule declares the classes and slots it reads, with an explicit
reads-all-types marker for a rule that quantifies over every type."

**Problem.** The first says what a rule may read; the second says what a rule must
say it reads. They are complementary and a first-time reader will read the second
as a restatement or a contradiction of the first. Nothing connects them.

**Proposed text.** One sentence at the end of `DECLARED_DISTINCTIONS_ONLY`: "That
is what a rule may read. What a rule must declare it reads is
`RULE_DECLARES_ITS_READS` under 'Rules and the ontology', adopted 2026-09-19 and
not yet built."

**Guard.** `tests/test_status.py:265` parses `DECLARED_DISTINCTIONS_ONLY` through
`_labelled_skill_items` but asserts nothing about its body. The live constraints
are that it keeps the `N. \`LABEL\`: text` form and that no label name repeats in
the file. **Priority.** Should fix.

### 12. The second-consumer rule is stated three ways (should fix)

**Location.** `CORE_PROMOTION` line 111, `CENSUS_FIRST` line 126, "Rules and the
ontology" line 240.

**Current text.** "waits for a second independent consumer" / "on at least two
consumers with different shapes" / "until a second consumer with a different
shape exists".

**Problem.** One rule, three phrasings, and the difference between "independent"
and "different shape" is not decorative: E-0488 named "the Shop runner and the
document path as the two consumers of different shape" for exactly this reason,
and Luis's 2026-09-03 rule is about shape.

**Proposed text.** Add "with a different shape" to `CORE_PROMOTION` without
removing its existing words, and make the other two read the same way.

**Guard.** `tests/test_status.py:265` asserts the regex `generic core waits for a
second independent consumer` inside `CORE_PROMOTION`, lowercased. That phrase
must survive verbatim; "a second independent consumer with a different shape"
still matches. **Priority.** Should fix.

### 13. `LITERATURE_INHERITANCE` is not an architectural law (could fix)

**Location.** "Architectural law" point 11, lines 273 to 277.

**Current text.** "`LITERATURE_INHERITANCE`: Treat independently convergent
literature and products as inherited foundations ... Locate contribution claims
in the composed protocol, component interactions, and measured results."

**Problem.** The section opens "Build Malleus as small, replaceable stages
connected by versioned artifact contracts", and points 1 to 10 and 12 to 14 are
about stages, artifacts and effects. Point 11 is about where novelty claims live,
which is the subject of "Research-to-core promotion gate" at lines 87 to 113 and
of `docs/PRINCIPLES.md` principle 8. It sits between the extension-point rule and
the integrity rule and stops the list.

**Proposed change.** Move the item into "Research-to-core promotion gate" as a
seventh numbered item, text unchanged, renumbering points 12 to 14 to 11 to 13.

**Guard.** `tests/test_status.py:265` requires the label to parse as
`N. \`LITERATURE_INHERITANCE\`: ` or `- \`LITERATURE_INHERITANCE\`: `, and its
body to contain, lowercased, "inherited foundations", "empirical corroboration",
"sources of techniques and baselines", the regex `do not organize.*being first
to.*ingredient`, and "composed protocol", "component interactions", "measured
results". Moving the item is safe if the line keeps that shape and the body is
not reworded. **Priority.** Could fix.

---

## 3. Consistency with the other two skills

### 14. malleus-dev does not route to malleus-paper (must fix)

**Location.** Lines 8 to 10.

**Current text.** "Work on the library and protocol, not on one adopter. Route
adopter-side schema and graph work to `malleus-acolyte`, repository audits to
`malleus-inquisitor`, and literature forensics to `malleus-recon`."

**Problem.** The paper front is missing. `.claude/skills/malleus-paper/SKILL.md:8`
says "Read `.claude/skills/malleus-dev/SKILL.md` first; its rules bind here", and
line 97 says "Every agent reads malleus-dev first". The binding runs one way.
E-0460 already found the paper skill "unwired from Core's skill rites" and that
was fixed in the packaging; the same hole is still in the prose. The paper front
is also one of the two live rule consumers this skill's census depends on.

**Proposed text.** "... literature forensics to `malleus-recon`, and the paper
front, its cells, manuscript and gate to `malleus-paper`, whose work these rules
bind."

**Guard.** None asserts the routing sentence.
`tests/test_capability_declaration.py:206` only requires "CAPABILITIES.md" and
"before declaring a gap" in each of the three skills. **Priority.** Must fix.

### 15. malleus-paper's pointer predates the rules section (should fix)

**Location.** `.claude/skills/malleus-paper/SKILL.md`, lines 8 to 9. This
proposal edits the paper skill, not malleus-dev.

**Current text.** "Read `.claude/skills/malleus-dev/SKILL.md` first; its rules
bind here, including 'Choose an adopter rule'."

**Problem.** Since E-0489 the rule doctrine lives in "Rules and the ontology",
which the paper skill does not name, and
`paper-v4/experiment-v4/content-rules-doc-02` is one of the two live rule layers
that section is written from.

**Proposed text.** "...its rules bind here, including 'Rules and the ontology'
and 'Choose an adopter rule'."

**Guard.** The corpus guards at `tests/test_inquisition.py:840`, `:869`, `:883`,
`:894`, `:938`, `:969`, `:981` and `:1645` apply to malleus-paper; none is
touched. **Priority.** Should fix.

### 16. The adopter's re-binding step is in the library skill and not in the adopter skill (should fix)

**Location.** malleus-dev "Implementation sequence", lines 430 to 436; the gap is
in `.claude/skills/malleus-acolyte/SKILL.md` step 9.

**Current text (malleus-dev).** "A contract revision that declares a re-bound
check contract records an identity; it does not retain bytes. Retain the
re-pinned contract in the same act, and have the act load it back through the
history's own selector before it returns."

**Problem.** That is an adopter step, and the adopter skill does not have it.
`grep -n "REBIND\|re-pin\|re-bound\|check contract"
.claude/skills/malleus-acolyte/SKILL.md` returns one hit, line 494, about the
bootstrap bundle. The acolyte's step 9, "Grow only from recorded gaps", is where
an adopter meets `compile_contract_revision` and it says nothing about re-binding
or retention. The Shop paid for this once (E-0458, E-0465). Both entry points are
declared in `references/CAPABILITIES.md`: `compose_contract_revision` with
`check_contract_descriptors=...` and `KnowledgeHistoryReplay.required_checks`.

**Proposed change.** Keep the lesson in malleus-dev, where it tells the library
what its adopters miss, and add the step to malleus-acolyte step 9, naming those
two entry points and the retention obligation.

**Guard (acolyte side, and it is tight).**
`tests/contract_compiler/pareto/test_adopter_completion_boundary.py:81` slices
step 9 between the literals `9. **Grow only from recorded gaps.**` and
`10. **Stop honestly.**` and requires `](#maintaining-interpretations-as-evidence-accumulates)`
and "structural schema growth, not the scope of interpretation review" to stay
inside it. `tests/test_inquisition.py:1772` requires roughly 290 exact substrings
in the "## Starting a project with no schema" section, holds index ordering over
the ten step headings at `:2078` to `:2101` (including "at most two additive
revision rounds" before "compile_contract_revision"), and enforces a
case-insensitive leak blacklist at `:2102` to `:2117` that forbids the substrings
"paper", "brief" and "small shop" anywhere in that section. Any added sentence
must avoid those words and must not move the step headings.

**Priority.** Should fix.

### 17. Nothing in malleus-dev belongs to the paper skill (negative finding, no action)

Checked and recorded so the question is not re-asked. The two `paper-v4/` paths
the skill cites (lines 152 and 170) are cited as the census and the worked case,
which is what `CENSUS_FIRST` requires of any rule proposal. They are evidence for
a library rule, not paper business. No proposal.

---

## 4. Missing decisions

### 18. ROADMAP F1 is named twice and never stated (must fix)

**Location.** Line 224, "Sequenced after the one-call admission (ROADMAP F1)",
and line 245, "the open work is ROADMAP items F1, F3, F4 and F5".

**Problem.** The skill never says what F1 is, that it is in flight, or that it
blocks every model run. E-0486: "compile-check-admit becomes one Core operation,
designed with Luis and built before any further run". E-0488 ruling 1 gives its
shape, its RED-first condition, its two consumers of different shape (the Shop
runner and the document path), and "no model run until it lands". E-0489: the
Core agent was stopped by a session limit before any change and was resumed;
nothing has landed. `ROADMAP.md:1022` to `:1034`. This is the most consequential
open item for the library and a reader of the skill cannot find it. It is also
the fix for proposal 1.

**Proposed text.** A short paragraph in "Rules and the ontology", beside the
corrected sentence from proposal 1: "**What is being built.** ROADMAP F1,
dispatched 2026-09-19 and not landed: one Core call takes the semantic ledger and
a plan, compiles against the contract the ledger requires, runs the check
contract the ledger requires, and appends the retained plan, gaps, change set,
receipt and the three protocol events in one transaction, or writes nothing and
returns a typed refusal naming the stage and the witness records. Until it lands
the sequence is adopter code, roughly 700 lines of it in the Shop, and what Core
does when an adopter never runs the check is unverified. No model run happens
until it lands (E-0486, E-0488, E-0489)."

**Guard.** None. Watch `tests/test_inquisition.py:938`: the sentence must not pair
a pending-capability subject with a verb like "enforces" or "guarantees" outside
a denial clause. The wording above does not.

**Priority.** Must fix.

### 19. What a declared gap does today is decided and absent (should fix)

**Location.** "What Core can do", lines 12 to 32.

**Problem.** E-0486 records the answer as a fact, not a design: "nothing consumes
a declared gap today (it is retained as an artifact, event 44 in the third round's
ledger)". `references/CAPABILITIES.md` line 35 declares the six gap kinds as a
shipped capability and says nothing about what happens after one is declared.
`ROADMAP.md:1036` F2 is open and marked investigate, so the mechanism is not
decided and must not be written. The fact is decided and is the one Luis asked
for ("a declared gap should've triggered the ontology growth").

**Proposed text.** One sentence in "What Core can do": "A declared typed gap is
retained as an artifact and nothing consumes it: no revision proposal, no report
of open gaps against open proposals. That is today's behaviour, not a design.
Whether a declared gap should trigger ontology growth is ROADMAP F2, open
(E-0486)."

**Guard.** `tests/test_capability_declaration.py:206` requires "CAPABILITIES.md"
and "before declaring a gap" to stay in the file; unaffected.
`tests/test_inquisition.py:938` does not cover gap kinds. **Priority.** Should
fix.

### 20. The design constraint's scope stops short of what was ruled (should fix)

**Location.** Line 224.

**Current text.** "Sequenced after the one-call admission (ROADMAP F1)."

**Problem.** E-0488 ruling 2 says more: "Option B of E-0487 is the design
constraint for ROADMAP F5 and F3: every rule declares the classes and slots it
reads, Core checks the declaration against the compiled contract and derives
re-binding from the intersection with the revision diff; sequenced after F1." The
skill states the mechanism and the sequence and never says the constraint governs
F3 and F5, which is why F3 and F5 arrive in the last line as loose "open work"
with no connection to the constraint two paragraphs above.

**Proposed text.** "Sequenced after the one-call admission (ROADMAP F1). It is
the design constraint for F3, the impact of a revision, and for F5, re-binding
derived instead of decided (E-0488)."

**Guard.** None. **Priority.** Should fix.

### 21. The packet-reachability lesson is only in the paper skill (should fix, and it is a judgement)

**Location.** "Before you build: bind the slice", after line 86. The rule
currently lives only at `.claude/skills/malleus-paper/SKILL.md:120` to `:126`.

**Current text (paper skill).** "An instruction may only name what the addressee
can reach. A producer session is fresh by design and exposure forbids it any
other stage's workspace, so 'as before', or a filename from an earlier stage,
names something it cannot open."

**Problem.** The rule is about instructions to a fresh session, not about the
paper. This skill dispatches too: lines 77 to 86 govern dispatching bounded
capture, reconciliation and repair, and E-0488 dispatched a Core agent into an
isolated worktree where a sibling worktree's path names nothing the addressee can
open. The skill has no equivalent sentence.

**Proposed text.** After line 86: "A dispatched agent reads only what its own
worktree and its brief carry. 'As before', or a path from another agent's
worktree, names something it cannot open. State the shape you want where you ask
for it, every time (E-0477)."

**Guard.** `tests/contract_compiler/pareto/test_adopter_completion_boundary.py:21`
and `:81` slice `## Before you build: bind the slice` up to the next `## ` and
require both acolyte links to stay inside it. An added sentence inside the section
is safe.

**Priority.** Should fix, stated honestly: E-0483 wrote the day's lessons into
both skills, but the ledger does not record this particular one for malleus-dev.
It is my judgement that it generalises, not a ruling.

### 22. Nothing was found that is in the skill and undecided (negative finding, no action)

Every typed label and every dated lesson in the skill traces to a ledger entry or
to a file in the repository. `RULE_DECLARES_ITS_READS` is correctly marked as
adopted and sequenced, the rule grammar is correctly held at `PROPOSED`, and the
second check engine is correctly marked `EXPLICIT_EXCLUSION` (E-0487, E-0488).
No proposal.

---

## 5. Stale or dead text

### 23. "For v0" scopes a rule the skill never scopes (should fix)

**Location.** "Accepted compiler-enabled profile boundary", line 383.

**Current text.** "For v0, LinkML is the sole first-party human-authored ontology
frontend."

**Problem.** The claim is right, `docs/PRINCIPLES.md:236` says "the accepted v0
design selects official, execution-pinned LinkML as the sole first-party
human-authored frontend". But "v0" appears nowhere else in the skill and is
defined nowhere in it, so the only version-scoped sentence in the file is the one
a reader cannot date. Combined with proposal 4, the section reads as shipped.

**Proposed text.** "Under the accepted v0 design (`docs/PRINCIPLES.md`,
'Contracts are stable; implementations are replaceable'), LinkML is the sole
first-party human-authored ontology frontend."

**Guard.** `tests/test_inquisition.py:1685`'s three verbatim literals are at lines
394, 396 and 399, not here. **Priority.** Should fix.

### 24. F4 is listed as open work and it is answered (should fix)

**Location.** Lines 243 to 245.

**Current text.** "The research is
`handover/2026-09-19-rules-inside-the-ontology-findings.md`, sha256
`88c9e30a...`; the open work is ROADMAP items F1, F3, F4 and F5."

**Problem.** F4 is the research item. E-0487 delivered the findings, E-0488 ruled
on them (Option B adopted, Option D excluded with reason, Option C held at
`PROPOSED`), and this very section is the result. Sending a reader to F4 as open
work sends them to re-run research the paragraph above already reports.
`ROADMAP.md:1057` still carries only the brief, so the roadmap is stale on this
too, but the skill does not have to inherit it.

**Proposed text.** "The research is
`handover/2026-09-19-rules-inside-the-ontology-findings.md`, sha256 `88c9e30a...`.
It answers ROADMAP F4 and this section is its result. The open work is ROADMAP
F1, F3 and F5."

**Guard.** None. **Priority.** Should fix.

### 25. "Represent the dependency in the design graph" names no graph (should fix)

**Location.** "Specify every stage", lines 363 to 372.

**Current text.** "Represent the dependency in the design graph. At minimum,
record tuples equivalent to: `Stage implements ProtocolRole` ..."

**Problem.** The graph is never named. It is
`design/PROTOCOL_FOUNDATION_GRAPH.ttl`, with a Markdown projection beside it, and
it uses exactly this vocabulary (`implements`, `consumes`, `produces`,
`governedBy`, `conformsTo`, `derivedFrom`; see `.ttl:126`, `:154`, `:296`).
Without the path, the instruction is unfollowable. The file's own header records
"Design graph revision: 26" and "Evidence cutoff: 2026-09-01", which is before
every decision from E-0430 onward, so a reader should also be told the graph lags
the ledger.

**Proposed text.** "Represent the dependency in the design graph,
`design/PROTOCOL_FOUNDATION_GRAPH.ttl`, whose Markdown tuple blocks are
projections of it. Its recorded evidence cutoff is 2026-09-01, so it does not yet
carry the rule decisions of this skill. At minimum, record tuples equivalent to:"

**Guard.** None. **Priority.** Should fix.

### 26. `OVR-000466` is used twice and never glossed (could fix)

**Location.** Lines 177 and 222.

**Current text.** "broke frozen evidence three layers away (OVR-000466)" and
"which is the OVR-000466 blast radius".

**Problem.** The skill glosses KG, LinkML, SHACL, SPARQL and RDF and leaves this
one. It is an overseer ledger entry id, sealed at commit `ff1c6931`, and a reader
cannot resolve it from the repository without already knowing the overseer ledger
exists. Luis's standing requirement is explicit names.

**Proposed text.** At the first use: "broke frozen evidence three layers away
(overseer entry OVR-000466, sealed at commit `ff1c6931`; the re-baseline is
E-0467)". Leave the second use as the short form.

**Guard.** None. **Priority.** Could fix.

---

## 6. Readability

Only cases where meaning is at stake. No style-only proposals.

### 27. The MCP preflight is the narrowest section in the file and sits third (should fix)

**Location.** Lines 34 to 44, between "What Core can do" and "Before you build".

**Problem.** A first-time reader meets, in order: Core's capabilities, then an MCP
registration check for one workstream, then the slice gate. The preflight is
correct and it binds nothing a reader needs before the doctrine. It interrupts the
path from "what exists" to "how to bind work".

**Proposed change.** Move `## MCP preflight` and its body, unchanged, to sit just
before `## Completion gate`. No text edit.

**Guard.** `tests/test_contract_compiler_environment.py:901` slices on `"## MCP
preflight\n"` up to the next `"\n## "` and asserts only the literals inside;
position is not asserted. The link `](../../../.codex/README.md)` must stay inside
the section and must still resolve from `.claude/skills/malleus-dev/`, which it
does from anywhere in the file. **Priority.** Should fix.

### 28. `DERIVATION_CLOSURE` is one eight-line noun phrase (could fix, high guard risk)

**Location.** "Qualify a projection", lines 326 to 333.

**Current text.** "`DERIVATION_CLOSURE`: Bind the accepted canonical graph-state
identity; exact initial-empty-state identity and retained genesis change-set-set
digest; verified selected-prefix identity and checkpoint; effective contract and
composition; reader identity; projector implementation and projection profile;
interpretation profile; declared side inputs; transaction-time and valid-time
coordinates; and output digest."

**Problem.** Ten commitments in one sentence with no verbs after the first. It is
the hardest paragraph in the skill and it is a checklist, which is a list.

**Proposed change.** Keep the label line and turn the ten commitments into an
indented sub-list under it, each on its own line, wording unchanged.

**Guard.** This is the tightest guard in the file and the risk is real.
`tests/test_status.py:265` requires all ten commitment strings to appear,
lowercased, in the *item body* that `_labelled_skill_items` (`tests/test_status.py:19`)
assembles from the label line plus its indented continuation lines, together with
two regexes, the phrase "keep them distinct", and the absence of "initial-base
identity". Whether an indented `- ` line counts as a continuation or is dropped
depends on that helper and was not verified by execution here. Run
`tests/test_status.py::...::test_malleus_dev_skill_gates_research_and_projection_claims`
before and after. **Priority.** Could fix. Modest gain, real risk.

### 29. Line 212 runs 99 characters where the file wraps at 80 (could fix)

**Location.** Line 212.

**Current text.** "constraint, in that order). `RULE_DECLARES_ITS_READS`: every
rule declares the classes and slots it"

**Problem.** Mechanical only; it is the one line in the body that breaks the
file's wrap and it sits at the start of the newest and most important clause.

**Proposed change.** Re-wrap, and start `RULE_DECLARES_ITS_READS` on its own line.

**Guard.** The sentence is asserted nowhere. `RULE_DECLARES_ITS_READS` is not in
the `- \`LABEL\`: ` form, so `_labelled_skill_items` does not parse it and there is
no duplicate-label risk either way. **Priority.** Could fix.

### 30. "Rules and the ontology" is 92 lines and carries seven bolded claims (no action)

Checked against Luis's "one read should be enough". The section is dense but its
seven bolded lead-ins ("What a rule is today", "The hash chain that must travel
together", "What already lives inside the ontology", "What was decided before",
"What was decided on 2026-09-19", "What is excluded", "The target, held") are the
best structure in the file and each is one answerable question. With proposals 1,
9, 10, 18 and 20 applied it reads in one pass. No length proposal.

---

## 7. The frontmatter description

### 31. The description does not name rules, binding or capabilities, and names one abstraction that does not exist (must fix)

**Location.** Line 3.

**Current text.** "Maintain and evolve the Malleus library itself. Use for
malleus-dev architecture, protocol stages, contract frontends, graph backends,
adapters, generated projections, artifact formats, dependency boundaries, public
APIs, research-to-core promotion, and decisions about modularity, composability,
replaceability, or conformance."

**Problem.** Two defects. First, the skill now covers rule design ("Choose an
adopter rule"), rule binding and what an ontology revision does to rules ("Rules
and the ontology", added at E-0489 on Luis's instruction), and Core's declared
capability surface. None of those words is in the description, so a session asking
"where should this rule live?", "how do rules survive an ontology revision?" or
"does Core already do this?" does not trigger the skill. Second, "contract
frontends" is the one trigger term naming an abstraction the package does not
have (proposal 4).

**Proposed text.** "Maintain and evolve the Malleus library itself. Use for
Malleus architecture and protocol stages, ontology contracts and their
compilation, rule design and rule binding (adopter rules, check contracts,
re-binding across an ontology revision), graph backends, adapters, generated
projections, artifact formats, dependency boundaries, public APIs, Core's declared
capabilities, research-to-core promotion, and decisions about modularity,
composability, replaceability, or conformance."

**Guard.** `tests/test_inquisition.py:1645` requires the frontmatter to parse as
YAML with keys exactly `{name, description}`, `name == "malleus-dev"`, and a
nonempty string description. Any wording passes. **Priority.** Must fix.

### 32. The agent manifest's one-line description is silent on rules too (could fix)

**Location.** `.claude/skills/malleus-dev/agents/openai.yaml`, line 3.

**Current text.** `short_description: "Build Malleus through replaceable protocol
stages"`

**Problem.** Second description surface, same gap as proposal 31.

**Proposed text.** `"Build and bind Malleus protocol stages and rules"`, 48
characters.

**Guard.** `tests/test_inquisition.py:1645` requires
`25 <= len(short_description) <= 64` and `"$malleus-dev"` in `default_prompt`.
**Priority.** Could fix.

---

## Counts

| Priority | Count | Proposals |
|---|---|---|
| Must fix | 7 | 1, 2, 3, 9, 14, 18, 31 |
| Should fix | 15 | 4, 5, 6, 10, 11, 12, 15, 16, 19, 20, 21, 23, 24, 25, 27 |
| Could fix | 7 | 7, 8, 13, 26, 28, 29, 32 |
| Negative findings, no action | 3 | 17, 22, 30 |

32 numbered entries, 29 of them proposals.

---

## Overall read

The skill is in sync with the decisions and out of sync with the code in one
place that matters and several that do not. Everything Luis ruled between E-0430
and E-0489 that belongs to the library is in it, correctly dated and correctly
attributed, with two exceptions: ROADMAP F1 is named twice and never stated even
though it is in flight and blocking every model run, and the fact that nothing
consumes a declared gap is recorded in the ledger and nowhere in the skill. The
counts, the hash chain, the six live rules, the exclusion of a second check engine
and the closed `LogicContract` field set all check out against the code and the
ledger; `LogicContract.load` really does close its fields against
`CONTRACT_FIELDS`, so the mechanical argument for Prolog is sound. What does not
check out is the sentence that says Core runs the check at admission. It does not,
and F1 exists precisely because it does not, so the skill states as shipped
behaviour the thing the library is currently building. Around that sit three
smaller factual defects of the same family: a worked case pointing at a file that
is not there, two adopter-runner refusal names presented as Core's, and a whole
section written in the present indicative about abstractions that live only in the
design graph. The internal contradiction between the two definitions of "adopter
rule" and the section order that puts every rule term before its definition are
the reasons a first read does not stick.

The three changes that matter most:

1. Fix the claim that `PrologVerifier` runs at admission, and say in the same
   breath what F1 is and that it has not landed (proposals 1 and 18). One
   sentence is wrong and the correction is the missing decision.
2. Make "adopter rule" mean one thing, and put the definition before the use by
   swapping the two rule sections (proposals 9 and 10). This is what "crystal
   clear on a re-read" costs.
3. Add malleus-paper to the routing line and fix the frontmatter description so
   the skill fires on rules, binding and capabilities (proposals 14 and 31).
   Today the paper skill binds to this one and this one does not know it exists,
   and the description does not name half of what the skill now carries.

---

## OVR-000467 draft, unsealed (added by the Overlord, 2026-09-19)

All 29 proposals above were applied (E-0491, E-0492) and committed as 3b8d49f4 with ROADMAP section F. The skills are governed documents; this entry records their new digests. The Overlord seals.

```json
{
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "ledger": "overseer",
  "entry_type": "DOCUMENT_REVISION",
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "subject": {
    "id": "skills-in-sync-2026-09-19",
    "type": "DOCUMENT"
  },
  "entry_id": "OVR-000467",
  "sequence": 467,
  "previous_entry_hash": "sha256:0eb70a735e843fe9d22bf3032e3efe8be49deea4cc6c8b7678449461f89aaa7b",
  "recorded_at": "<sealing moment, UTC>",
  "summary": "Record the skill and ROADMAP edits of 2026-09-18 and 2026-09-19 so the governed documents match the tree again.",
  "why": "The three skills are governed documents under this ledger, and their working-tree bytes had moved from the digests recorded at OVR-000463 without an entry, which blocked every later seal at render (2026-09-19). This entry records the edits made on 2026-09-18 and 2026-09-19 under the paper Overlord session: malleus-dev gains 'Rules and the ontology' (E-0488, E-0489), the 29 applied proposals of the skill review (E-0490 to E-0492) and the F1 landing sentences (E-0493); malleus-paper carries the 2026-09-18 launch-packet lessons and the protocol supersession rule (E-0483); malleus-acolyte step 9 carries the re-binding step (E-0492). ROADMAP.md gains section F, items F1 to F6, from the Shop reconsideration experiment. The review handover holding this block is created. Commit 3b8d49f4 carries the document bytes; the agent manifest and the rules findings file in that commit are not governed and are not listed.",
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "path": ".claude/skills/malleus-dev/SKILL.md",
        "change": "MODIFIED",
        "before_digest": "sha256:67197a1c5d1ad9b2f1c7c66fa200ba8afe07d825eea77cd10f4fbb3ac3a987b2",
        "after_digest": "sha256:a135c1634771ed2a81d1562cbee8b092c51f254f5224f14fed21622bf5abfbb5"
      },
      {
        "path": ".claude/skills/malleus-paper/SKILL.md",
        "change": "MODIFIED",
        "before_digest": "sha256:5c43070ad7c170df78013cc7932fa8e410d3683c58d18e1c57dd1f31d49b2b5a",
        "after_digest": "sha256:4ebd7fd961ac13be6e0f0f498135689551cf81771a6dfc96198d41a2ee928b5b"
      },
      {
        "path": ".claude/skills/malleus-acolyte/SKILL.md",
        "change": "MODIFIED",
        "before_digest": "sha256:5b050ba92c9849d9377b51a82c01e67ed2549a6e3ec9b4f9967a8113c573a1d4",
        "after_digest": "sha256:4e457d697a79e091f5b86be39b736e678f511f145ee0bc3c1b8062c6c040a9fb"
      },
      {
        "path": "ROADMAP.md",
        "change": "MODIFIED",
        "before_digest": "sha256:891c9529a77a0cd999c55e42f63ab9f3ce39fa46c46be63024dd6f7af01733aa",
        "after_digest": "sha256:ac3e4f66eea1f700ae144b33886314b416c877ea4847450ec70e7090c6733867"
      },
      {
        "path": "handover/2026-09-19-malleus-dev-skill-review.md",
        "change": "CREATED",
        "after_digest": "<digest of this file once final>"
      }
    ]
  },
  "references": [
    {
      "relation": "EVIDENCES",
      "type": "COMMIT",
      "target": "3b8d49f41690702de0f9cbaa8a666fd638474090"
    },
    {
      "relation": "AFFECTS",
      "type": "WORKSTREAM",
      "target": "CC-R11"
    }
  ]
}
```

## Sealing note for OVR-000467, 2026-09-19

`entries/OVR-000467.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment,
the previous entry hash and this file's digest filled in.
