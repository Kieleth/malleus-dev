# Intake: sample-neurosymbolic-framework-with-description-logics

Raw subagent findings, 2026-08-19. Opus subagent, evidence-first inspection of
shallow clone at commit 6b7b884889d6d9420fde097f21ebe8fe8d5327fb. Basis marks
(SOURCE_EXPLICIT / REVIEWER_INFERENCE / NOT_ESTABLISHED) preserved verbatim.
Ledger records derived from this file are in ../records/.

## Purpose

A CLI that automatically evolves a Python "query program" capable of answering
natural-language questions against a large biomedical OWL ontology (FMA, GO,
SNOMED CT, CL, HPO). A control harness starts from a degenerate seed program
that always answers "I don't know", evaluates it against hand-written gold Q&A
pairs using an LLM-as-a-judge, and repeatedly invokes the external coding agent
kiro-cli to rewrite the program until judged accuracy crosses a threshold. The
README frames this as producing "provably correct" answers by replacing LLM
reasoning with ontological reasoning (README.md:7, 38-40, 421-424).

## Headline findings

1. NO DL REASONER IS EVER INVOKED. Repo-wide grep for sync_reasoner, HermiT,
   Pellet, ELK, consistency, subsumption, satisfiability, entailment: zero code
   hits. owlready2 is a dependency but used only to load/count. The actual
   symbolic operation is BFS transitive closure over asserted subclass edges
   plus set intersection over asserted role triples in SQLite. (REVIEWER_INFERENCE)
2. "Provably correct" (README.md:7,40,423) is unsupported by any code. No proof
   object, entailment, or consistency check exists. (REVIEWER_INFERENCE)
3. "The LLM never sees the answer" (seed_program.py:4-5, docs/architecture.md:88)
   is false for the shipped final program: an LLM narrates the retrieved labels
   and is prompted to ADD pathophysiology/clinical significance beyond the
   retrieved set (iteration_4/query_program.py:292-313). (REVIEWER_INFERENCE)
4. The harness rule "core reasoning must use owlready2" (fixer.py:92) is
   prompt-stated and enforced by nothing; all four shipped evolved programs
   import only sqlite3+boto3, zero owlready2. Rule-in-prompt vs
   mechanism-in-code. (REVIEWER_INFERENCE)
5. Three non-ontological content leaks: LLM-authored broader_search_terms
   matched against labels; LIKE '%term%' label fallback; LLM narration of the
   result set. The concept SET is axiom-derived; the ANSWER is not. (REVIEWER_INFERENCE)
6. Sample result (100% on SNOMED, 4 iterations, $0.59) rests on 4 questions,
   threshold 0.95, LLM judge against hand-written encyclopedic prose that no
   OWL file asserts. Optimizes prose agreement, not ontological fidelity.
7. Artifact-integrity defect: per-iteration query_program.py is overwritten in
   place by the fixer, so iteration_N's stored program is the POST-fix program.
   iteration_3 and iteration_4 programs are byte-identical (sha256 6b0854c9...)
   despite a non-empty 12,235-byte changes.patch between them.
8. Schema mismatch: build_db.py emits labels/subclass/roles/equiv_* but every
   evolved program queries labels(concept_id,...)/subclass_of/relationships.
   The script that produced the sample run's index is not in the repository.

## Architecture (evidence: path:lines)

- Builder CLI / control harness — evolve loop: seed -> execute -> judge ->
  TASK.md -> kiro-cli fix -> repeat until accuracy >= threshold (default 0.8)
  or max_iterations (20). Ontology-agnostic. builder.py:111-496.
- Seed program — degenerate; loads OWL via owlready2, answers "I don't know".
  seed_program.py:11-30.
- Executor — runs evolving program as subprocess, scrapes last "Answer: " line.
  executor.py:19-93.
- Judge — LLM-as-a-judge, Bedrock Opus 4.6, VERDICT: CORRECT|INCORRECT.
  judge.py:20-128.
- Fixer — writes TASK.md, spawns kiro-cli --no-interactive --trust-all-tools
  over a PTY. fixer.py:37-190, 278-293.
- Run manager — per-iteration artifacts + run-level summary.json + REPORT.md.
  run_manager.py:37-140; builder.py:503-673.
- build_db.py — regex line-scanner over OWL functional syntax -> SQLite.
  Pure syntactic extraction. build_db.py:9-111.

## Position of the symbolic layer

ANSWER SOURCE, not gate. Sits between two LLM calls: LLM parses question to
structured query -> symbolic retrieval produces concept set -> LLM narrates.
No post-generation verification. Only rejection mechanisms: subprocess failure
and the LLM judge. Nothing rejects a statement for TBox inconsistency or a
failed subsumption test. Ontology is strictly read-only; nothing ever writes
to it, so admission-gating questions do not arise (mechanism absent).

## LLM layer

Judge: us.anthropic.claude-opus-4-6-v1 (Bedrock converse). Evolved programs:
us.anthropic.claude-sonnet-4-20250514-v1:0 (invoke_model). Fixer: kiro-cli,
model not pinned. Three roles: question decomposition, answer composition,
evaluation — the judge is the sole learning signal and headline metric.

## Key concepts

- Self-modifying program (SMP): program iteratively rewritten by a coding
  agent until it satisfies gold Q&A constraints. README.md:122-133.
- Degenerate seed: all capability demonstrably acquired through the loop.
- Ontology-agnostic harness: domain discovery delegated to the coding agent.
- LLM-as-a-judge accuracy: stop criterion and headline metric.
- Answer-line contract: last stdout line "Answer: " is the whole interface.
- "DL has no declarative query language": stated motivation for evolving an
  imperative program instead of a query string. README.md:207-213.
- SQLite ontology index: flattened asserted-axiom cache standing in for OWL.

## Resonances with autoresearch-et / malleus

- Typed KG: partial — SNOMED's typed role edges are used, but typing is
  inherited, nothing validated, role vocabulary comes from prompt examples.
- Ontology-gated writes: structurally absent (no writes exist).
- Bitemporal state: absent; linear per-iteration code versioning with
  provenance, plus the overwrite defect above.
- Grounded audit rationales: partial — every verdict has stored justification
  and stdout/stderr, but rationales are prose-vs-prose LLM narrative; no
  derivation trace to axioms (emitting ontology IDs is in fact forbidden,
  fixer.py:93-95).
- Closed research loop: STRONGEST resonance and the repo's real contribution.
  hypothesis(program) -> experiment(parallel eval) -> judge -> durable critique
  (TASK.md) -> automated repair -> re-eval, with stop criterion, budget bound,
  best-so-far tracking, cost accounting, auto REPORT.md. Trajectory 0% -> 0%
  -> 50% -> 100%. Caveat: closes on prose agreement, not ontological
  correctness.

## Maturity

Sample repo (MIT-0), 3,424 Python LOC, one shipped run over one ontology,
15 tests covering only executor string/subprocess handling, no library API.
Last commit 2026-05-12 ("tweak docs").

## Evidence digests (sha256, bytes)

README.md f1c49333a947faf5f46bac57ca0e55dfe216ba3000c7b289989473e28aa2032a 19016
docs/architecture.md bdeb27afd8cd28f0289c12fe660236d8f1fb60b1f263efe8ac680cda76f816f8 3559
ontology_qa_cli/seed_program.py 67961c0df5bdd643a23aaec54da3139858bd29c62ec51f81662dcbab2dcb9c21 1075
ontology_qa_cli/builder.py 5ebf907765472abbc458c962f1eb50d3b870cba7a2028e5371d348ddce0385ae 28720
ontology_qa_cli/judge.py 8ef9a0afd8768ce8ccf155737a1599ea110850987f1af0c335a3746ff6b37396 4216
ontology_qa_cli/fixer.py ff84c6bf15424719805d7bac875515cd3e3b2bb0c6f8311408df6aa4cc733749 10970
ontology_qa_cli/executor.py 37fbf635bb43a932d3e50d2abdef787d0f3a83f1f8427d12f54beff7c5b0ad07 2486
ontology_qa_cli/run_manager.py 6db16e261e98c981a1bfd744f973e092fd372131f4a5dd9495bc945b62532c4e 4851
ontology_qa_cli/config.py 6eecb5d73abb7c36f3a4697de8e92a577bb775ffbaeae00c0ecea9abc4464151 5831
ontology_qa_cli/query.py 0a321ab6683f50763895676b786ac445cd47028c2f95df0c9bd300230edfe537 5351
ontology_qa_cli/seed.py b479fbcfee17b396786a3e114abf42e4d7a0f3f58a3b1a4fb449f0eb77ca6899 753
ontology_qa_cli/ontology_stats.py 624002db823032edc7208360a2721d24f97667d37c871704bc7f7543c97aadbf 6204
build_db.py 4408f0f244b975f9a5ba6cdfc17999f5d4b10ec765846585a8fafb57f8484702 6711
ontology_config.yaml c6ba6efaa330c8ecc038cdd576c5f07d34e85737bcd0636389ef4a5c429022cc 17048
pyproject.toml 70c5a65be28f8dbf07d086da55df140fd677435c5b5064f14ba083417ee42a77 775
llm-costs.yaml 2e76fae20d296a995d9f942f9c9eb3912e2149f28de5e34b7315c41c8c8ee2c7 303
tests/test_executor.py 7f01036465bbb9deb72f3a2c9f053184a655b169f8cf316bb9d3d9cd53c51917 5533
assets/sample-run/REPORT.md 5df7e29898509cd084da9394c60efb5b3ca68916f09be0b600ce5cbb40a40d27 2333
assets/sample-run/summary.json 62ae4b9b1993de45179e90d295324f04cbde327f441f12e68dbf16095a851561 325
assets/sample-run/iteration_4/query_program.py 6b0854c9fcc42f7726d9ea68408e5dc067ba62450df781817e94b917b8b1602b 14251
assets/sample-run/iteration_3/query_program.py 6b0854c9fcc42f7726d9ea68408e5dc067ba62450df781817e94b917b8b1602b 14251
assets/sample-run/iteration_3/evaluation.json 61cd36db96bba8ddd61394f4f40c2b6ca424b3aa10d8176edabba0e8f896b10e 27138
assets/sample-run/iteration_4/evaluation.json 6fe18f954f6ded507440d97df1020cf2c32f8b7e077300965640b4b6f042f16c 60666
assets/sample-run/iteration_1/TASK.md ba346a4c6472787f93fbbc952e04655dd30cc491e47e08fea195562af18d20cc 13508
