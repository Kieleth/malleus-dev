# Core population piece 8: nascent-project adoption playbook

Status: implemented in Core, awaiting independent overseer verification.

## Coordinates

- RED: `d29c7b1b146420106a9bd4e2aab36519099b0533`
- RED tree: `9da90627329bdb048164d4927432412bb69fdace`
- GREEN: `321da76e8a8b523d7f51d1263c81860bf3daca6c`
- GREEN tree: `46ea71aa47181f45fa489e8d3d85d50217c5a5cb`
- Sequence guard: `77f9f5cb44596fed8990b63d898959439bc9c3c5`
- Sequence-guard tree: `da9ccb69819665ba2ea44138fb4c5e1d835b4d02`
- Coverage-and-loop RED: `ff9bddda9bb7e49b566c5d7267f8b50b313c52f6`
- Coverage-and-loop RED tree: `c77a49e922b213ba801993f01ca4b96b36866201`
- Neutrality-and-install RED: `7da27cd61f8a64ba0dca9205b9d54ccb0bf6159c`
- Neutrality-and-install RED tree: `31a0dfaf43e4ee0f96a2e25c9367e02ed48292b6`
- Loop GREEN: `b3769d6e9fb55ab4e7fd455ea545230de5a4a429`
- Loop GREEN tree: `9e63885eae14870d72a39486d5131bd82162a4f0`
- Self-contained-path RED: `020ad57729e32bf698eca584a1194072eda3ec52`
- Self-contained-path RED tree: `ccc4f63724a90e19308f5909b5d7e396420e9158`
- Self-contained-path GREEN: `97ee55c2f0ecbc4a3c6883468332c9b770f6516b`
- Self-contained-path GREEN tree: `0eb52de1fe379d354512a4178f0a72090cd4980b`
- Admission-branch RED: `9c087595b9f636b456892292455326e688224e74`
- Admission-branch RED tree: `3eee37ac79c73100ae4f6ad2e182d96768727f8d`
- Final GREEN: `387716a31e8483d56fd5f1ce95cf97555c67ba82`
- Final GREEN tree: `9f3b870e01b15cb0e6a96f6f9b3f24996ebb6b21`
- Executable-surface guard: `0dd77db2790f6dfaad5ae760c9acb8577033d72a`
- Executable-surface-guard tree: `c7bb8270e4f9b2576002c0aa4a1f5ba50c03410e`
- Capture-contract RED: `c1c4ee68615eb74787b4d6d985f476164ace0491`
- Capture-contract RED tree: `db4ee9687da03206579b762a962cbc652a9631dd`
- Coverage-precedence RED: `dc9e17a50d9310e7b7fa71f9550397c2d18eb428`
- Coverage-precedence RED tree: `bc439fe37523432c3101e861d5e58d5698c2c014`
- Runnable-capture GREEN: `ca4052409b08bf719a17cf3aacd3578e9b18a819`
- Runnable-capture GREEN tree: `e24a801a04cab296e05295a9150bf7033f58abe7`

## What changed

The shipped `malleus-acolyte` skill now has a separate playbook for a project
that has source material but no accepted domain schema or semantic history. It
does not replace the existing standing orders for an established project.

The playbook gives a fresh adopter one ordered path:

1. retain exact source bytes and model only what they support;
2. choose only the Malleus level needed, and choose a domain-history profile
   explicitly when governed history is wanted. Schema-only or typed-graph-only
   adoption stops after structural compilation; steps 6 through 9 are the
   governed-history branch and require the profile;
3. inspect the optional `metrology`, `chronology`, and `research` packs before
   inventing project vocabulary, and extend a pack concept before extending
   root;
4. propose a domain ontology with instances and protocol machinery kept out,
   exposing every concrete Entity and Relation type as the eligible population
   surface;
5. run pack grounding or conformance where applicable and compile the exact
   LinkML source closure;
6. turn a document capture or structured source into the neutral population
   plan through an explicit source adapter, then use the two-axis capture census
   to inspect both block review and assertion formalisation, continue over source
   blocks still marked `UNTOUCHED`, and retain the fact that reviewed blocks can
   contain uncaptured assertions. Whole-reading coverage overrides the global
   smallest-slice rule for this capture task;
7. compile and prepare that plan, admit only a non-null
   `prepared.change_set` through one `KnowledgeChangeHistory` with
   `history.admit(change_set=prepared.change_set, ...)`, and retain a
   `NO_DOMAIN_CHANGE` preparation without calling admission;
8. reopen with `KnowledgeChangeHistory.reopen(...)`, replay, query, and trace
   accepted records back to retained evidence;
9. keep the loop in one working session by default, cap it at two additive
   revision rounds before it starts, and use only clustered typed gaps to
   justify a revision; and
10. stop when another addition would require invention.

For this path, a supplied current installation and exact input artifacts are the
closed working set. The section explicitly supersedes the older checkout probe
and adoption-guide pre-read. It forbids ambient home-directory, checkout,
network, and undeclared-document discovery, and requires an explicit failure
when a needed capability or artifact is absent.

The skill carries one marked, machine-parsed
`malleus.nascent-document-example/private-v0` JSON block. It shows the exact
closed reading, capture, attribution, assertion, optional time, formalisation,
gap, Entity, and Relation shapes needed by the current adapter, and lists all
six accepted gap kinds. Its neutral example is executed directly through
`adapt_document_assertions` in the conformance suite. The block says explicitly
that private-v0 is current input guidance, not a stable wire promise.

The exact grounding standing order from `design/KNOWLEDGE_PACKS.md` is carried
into the skill. The playbook also preserves the twelve generic rules extracted
from the retired producer brief: generated material remains proposed until
accepted; evaluation questions stay out of ontology construction and
population; source concepts, values, units, distinctions, and epistemic status
are not invented or collapsed; instances stay out of schema vocabulary;
protocol and query machinery stay outside the domain ontology; labels do not
smuggle assertions; normalization needs explicit evidence; unsupported source
material becomes typed gaps; and incomplete or `NO_DOMAIN_CHANGE` results do
not trigger a fallback.

## Executable surface named by the playbook

The installed commands are:

- `malleus-inquisitor install-skills --agent codex --project .`
- `malleus-inquisitor pack-grounding`
- `malleus-inquisitor pack-conformance`
- `malleus-compiler contract`

The playbook states that the command-line compiler stops at contract
compilation. It directs population and history work to the existing public
`malleus.compiler` facade and names `DOCUMENT_CAPTURE_GRAMMAR`,
`adapt_document_assertions`, `compile_population_plan`,
`prepare_population_change`, `KnowledgeChangeHistory`,
`trace_population_record`, and `compile_contract_revision`.

No public Python symbol, artifact grammar, or command was added in this piece.
The public deliverable is the installable skill procedure itself.

## Mechanical evidence

- The RED commit adds two tests. Both fail because the nascent-project section
  does not exist in either the source skill or an installed copy.
- The later RED guards add the complete population surface, both census axes,
  exact history calls and no-change branch, bounded loop, Codex install path,
  ordering, leakage constraints, and the closed installed-artifact boundary
  before the final GREEN.
- The two direct playbook tests pass after the final GREEN.
- The complete skill-installation and shipped-guidance slice passes 21 tests.
- The complete Inquisitor test module passes 104 tests.
- The content guard binds the model-neutral rules, real public command and
  function names, absence of model, fixture, answer, query, evaluation, brief,
  or paper specifics, and the ten-step order. It also checks that profile and
  pack choices precede ontology construction and that the fixed loop bounds
  precede revision.
- The installer test copies all shipped skills to a clean Codex project and
  proves the installed acolyte retains the playbook bytes.
- A direct executable guard resolves all named Python objects from
  `malleus.compiler.__all__`, verifies `KnowledgeChangeHistory.admit` and
  `KnowledgeChangeHistory.reopen`, exercises the Codex skill installer and both
  pack rites, and parses the documented compiler contract route.
- A second direct guard parses the JSON template from the installed skill,
  verifies every closed record shape and accepted gap kind, checks its reading
  digest, and passes it through the public document adapter to a deterministic
  plan and two-axis census.

## Non-claims

This piece does not generate an ontology or population, choose a project's
domain semantics, extract assertions, invent source mappings, add a population
CLI, judge vocabulary quality, evaluate query answers, admit Event records, or
stabilize a private artifact grammar. It does not prove that an arbitrary model
will follow the procedure. It publishes one source-independent operating
procedure over boundaries already implemented and tested by Core.
