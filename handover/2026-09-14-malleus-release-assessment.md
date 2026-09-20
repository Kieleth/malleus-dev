# Shop milestone and Malleus release assessment

September 14 local date, inspected September 15 UTC. Prepared by Malleus Overlord
after Luis requested milestone documentation and consideration of a new release.
This authorizes coordination and a recommendation, not version selection,
project-document edits, a push, tag, package publication or experiment rebind.

## Recommendation

Publish the connected Shop warehouse result as an evidence-backed research
milestone first. Keep package version 0.14.0 for that publication and require
the exact repository checkout to reproduce the new example.

If Luis also wants the current Core functionality distributed as a package,
prepare a separate minor release, provisionally **0.15.0**. The justification is
the post-0.14.0 optional transition-rule capability, not the size of the Shop
example. A patch would suit a separately selected bug-fix-only cut, not all of
current main. Core independently recommends this same distinction.

No version or publication path has been selected by this assessment.

## The completed Shop result

Final Shop documentation commit:
`30ab66437087f93b4f3e7b13b4d19229d2f7fca2`, tree
`49cec9c321527dd3e0324b43954f5b6ace92b769`.
Executable GREEN: `557adf6f38e591fe22cb163fabc43e2be54c037e`, tree
`19b5e3856e29807253f6df20a48c9017cd4ff1b6`.
The final documentation changes only the warehouse README and Shop plan.

Table 1's 21 occurrences and Figure 14's 13 warehouse occurrences now share one
history and the same 17 enduring objects. X1 gains Scan, Store and Retrieve
between its existing Unpack and Pack occurrences. Y2 is scanned before Y1 even
though it was unpacked later. One recorded additive schema revision introduces
only the three activity values. The earlier 895,257 ledger bytes remain an
exact prefix; B's quantity correction, old records and payment explanation stay.

The result has 34 domain changes, 193 protocol events and 133 historical records.
History SHA-256:
`ae9bbf870fd928e96de9f62c54a43d05575929b2546bb1e4376ecc9b8191cc06`.
Full, reopened and maintained graph reads agree at the declared checkpoints.
Every new property traces to retained source. The 344-test isolated Shop and
transition selection includes the 12 warehouse cases; they are not additive.
This assessment read the receipts and checked Git identities, not reran that gate.

Sources: [warehouse explanation](../research/ontology_driven_kg_realization/experiments/small_shop/connected_story/warehouse/README.md),
[receipt](../research/ontology_driven_kg_realization/experiments/small_shop/connected_story/warehouse/receipt.json),
[validation](../research/ontology_driven_kg_realization/experiments/small_shop/connected_story/VALIDATION.md).

This demonstrates an adopter extending accepted knowledge without replacing
its prior history. It does not demonstrate automatic mapping, source truth,
causality, elapsed-time analysis, a real warehouse integration or an installed
Shop application. The chapter is trusted input by the author's experiment choice.
Whole-import rollback and interrupted-import resume are not implemented.

## Public API is not the same as the released package

Shop introduced no Core code. Nevertheless, its connected runner calls
`create_structural_history(transition_program=...)`. That optional keyword and
its enforced transition rules arrived after v0.14.0. The signature difference
and actual call were checked in Git and `connected_story/run.py`.

Therefore a publication must say **public API on the pinned repository revision**,
not imply that an unchanged installation of 0.14.0 runs this new example.
The Shop research modules are outside the current package build allowlist.
Installing a newer Core package would not itself install the Shop application.

## Actual runtime delta since v0.14.0

| Change | Evidence | Appropriate claim |
| :--- | :--- | :--- |
| Optional replacement restrictions, interpreted by admission and replay | `1385223eb274e63d98cc334d6dba6ecd54ed4007`; [result](2026-09-08-transition-admission-results.md) | New, explicitly selected functionality. Existing private-v0 programs retain their meaning. Not a universal domain policy or stable wire. |
| Authorization mapping/precedence moved into an identified packaged artifact | `a7c54fa8453b28616c37942a1411e464dd0622e2` | Refactoring with recorded preservation of policy/evaluation hashes. Not full replacement of standalone Assent. |
| Canonical JSON identity for that artifact | `92463f35d02e9320e4bb3d62326c3dd1c4fe9131` | Fixes checkout line-ending sensitivity, including the recorded Windows import failure. |

Only six `src/malleus` paths differ between the release and final Shop tip.
Root/domain ontology bytes and dependency versions do not change in this range.
The package allowlist adds the rule module and JSON artifact. Skill guidance
and project documentation also changed after release and need their own bounded
changelog descriptions. No general migration, automatic evaluation, new planner,
cross-language parity or consumer performance guarantee follows.

The repository declares Semantic Versioning. The proposed minor version reflects
new optional functionality; it is a recommendation for this pre-1.0 project,
not a claim that SemVer mandates this exact version. [Specification](https://semver.org/spec/v2.0.0.html).

## Remote and local publication state

GitHub was read through its connector, without moving refs:

- Remote main is `6c73895981bc5ff4efdd6215090992685178ecc7`.
- Its [CI run 34681781560](https://github.com/Kieleth/malleus-dev/actions/runs/34681781560)
  completed successfully. That receipt predates the eight local Shop commits.
- Remote version refs include v0.14.0, annotated object
  `fcc969f9ade029db05890c88f591e2f84db04546`, with no later version ref returned.
- [Release run 34288358949](https://github.com/Kieleth/malleus-dev/actions/runs/34288358949)
  is successful at `e2b9e77912f9b36fdbfe2fca310548a789bffb4d`.
  The [retained release report](2026-09-08-core-release.md) records PyPI upload.
- A direct PyPI refresh was unavailable through the browsing tool; its generic
  cached page showed older content. It is not used to contradict the verified
  release workflow or claim a fresh package-index inventory.

Local main is final Shop tip 30ab6643, eight commits ahead of verified remote
main. Package metadata still says 0.14.0 and CHANGELOG's Unreleased section is
empty. There is no final release-candidate full/documentation/package receipt
for the proposed publication cut. The shared checkout also has unrelated
uncommitted Paper and Recon work, which must remain outside any selected commit.

## Cross-session responses and boundaries

| Owner session | Release relevance |
| :--- | :--- |
| Malleus Core | Recommends research milestone first; optional 0.15.0 for all current Core. Owns eventual README/docs/changelog promotion and package verification. No work was dispatched. |
| Malleus Core Shop | Documentation completed at 30ab6643. Its 13-path executable/evidence cut and two-path final documentation handoff remain Shop-owned. No new Core feature or push. |
| Draft lean Malleus arXiv paper (2) | Owns the completed Sol comparison and separately approved three-problem amendment, E-0383/master 1.5.42. Local uncommitted research work. Retains Core `c95dba7b86bb61487bda9a52458e1ea47cce20ab`; nothing needs package inclusion. |
| Malleus arXiv MultiDOC-RAG | Separate mixed-source/changing-domain research lane. Read-only astronomy-archive investigation, no implementation or newly selected Core pin. No release blocker. |
| Malleus Robotics | Research branch 7518bd17 plus uncommitted model-delivery work. Retains action/simulator Core `44541993f964674ac4cc994949e121f9de7387ba`; separate candidate pin `79ae2feff7fc59436ef405fd91fe5a38c8253394`. No package inclusion or Core defect. A model call reached response validation but not admission/controller; no new simulation. Its operational preflight is not release coverage. |
| Malleus-semantic-reentry | Committed, clean research proof; frozen Core `1385223eb274e63d98cc334d6dba6ecd54ed4007`. Its historical compatibility receipts do not certify current package bytes. Keep the research implementation outside the installed API and do not rebind it. No blocker under that exclusion. |

Malleus-code was also asked for its release boundary. Its detailed cross-thread
handoff encountered a destination-authorization refusal. This assessment does
not reproduce that withheld detail or retry its transfer. Explicit authorization
for that handoff remains a coordination dependency, not evidence of a package
defect. Do not describe the all-consumer handoff as complete.

## Proposed project-documentation cut, owned by Core

After approval, make a short README entry linking the warehouse milestone and
add its bounded result to the existing Small Shop walkthrough. Preserve the
earlier examples and receipts. Populate Unreleased with separate categories:
optional runtime functionality, authorization implementation change, Windows
fix, adopter guidance, and repository-local Shop evidence. Avoid describing the
Shop importer as installed or automatic. This proposal changes no file here.

Shop continues to own its source, ontology, mapping, importer and evidence docs.
Paper, Robotics, Re-entry and Code remain consumers; release assessment neither
moves their pins nor pauses their separately authorized work.

## Decisions and readiness

**Decision A:** approve project-level milestone documentation and eventual
publication of its exact committed repository coordinate, without a package bump.
A research tag, if selected, must not use the `v*` package-release trigger.

**Decision B, separate:** approve preparation of 0.15.0 for all current Core
changes. Then Core owns the existing exact-candidate full, docs, package,
clean-install and remote matrix gates, version/compatibility notes, and a
separately authorized push/tag/publication. This assessment starts none of them.
Do not run release work from the dirty shared checkout or absorb its edits.

The known empty supporting-claims-list mismatch between the two authorization
paths blocks claiming interchangeability. Core confirms it does not block this
bounded milestone or package cut when full replacement is expressly excluded.
Choosing that semantic contract remains separate work. No consumer has supplied
a new package defect from the warehouse milestone.

Readiness gaps are the author's publication decision, missing project-level
release notes/version selection, exact-candidate verification and publication.
They are not evidence that the existing Shop execution failed.

## Author approval: prepare 0.15.0, publication held

Luis answered "go" to the explicit question: "Do you approve instructing Core
to prepare 0.15.0 and run the release checks, with publishing held for your final
approval?" This selects the minor release preparation, superseding the earlier
unselected-version status. It does not authorize publication.

Core received the instruction to prepare the version, project documentation,
compatibility notes and exact isolated candidate, then run the existing release
checks. Local isolated preparation commits are part of this workflow. Shared
main movement, remote pushes, release tags, remote workflow dispatch and package
publication remain held. If remote CI needs a published candidate, that is an
explicit next approval dependency, not permission to bypass the hold.

Shop source/evidence paths, dirty Paper/Recon work and consumer pins remain
untouched. The authorization-claim-list semantic choice is excluded. Core must
return the candidate commit/tree, actual gate results, package identities and
precise remaining publication actions for final approval.
