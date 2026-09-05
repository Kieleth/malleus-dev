# RCA: the three points run-04's reviewer could not settle, 2026-09-05

Ordered by Luis at ratification (E-0135). Evidence: `private/paper-v4-v4-run-04/producer/work/document-population.json` (the capture and records), the frozen reading, `src/malleus/_contract_pipeline/document.py`, and the reviewer's record. Every count below was computed mechanically; the reading text is not quoted beyond what the analysis needs.

## 1. Claim statement digests were "unverifiable" at review

**What the reviewer saw.** Claim records carry `assertion_locator` and `statement_sha256` and no statement text. The review task allows the retained capture only to resolve a locator to a reading block, so the reviewer judged claim rows on the record's `name` plus the block.

**What is true.** All 104 records that carry a locator and a digest name an assertion in the capture, and in all 104 the digest equals the SHA-256 of that assertion's statement bytes. The digest is verifiable in one line from the retained capture, and every one of them is correct.

**Root cause, two layers.**
- Core: nothing checks the digest. `statement_sha256` appears in the research pack and nowhere in the document adapter or the population compiler. A producer that writes a wrong digest, or a digest of text that is not the located assertion, passes admission. Run-04's digests are right because Opus computed them; the protocol did not make it so.
- Review surface: the task restricts the retained capture to locator resolution. The located assertion's statement is reading text, already inside the allowed surface, so the restriction withholds nothing that needs withholding and blinds the reviewer to the one field that binds a claim to its words.

**Classification.** A Core gap (unverified digest) and a review-task defect (needless restriction). Not a producer fault.

**Fixes.**
- Core-12: in the document adapter, when a record's `assertion_locator` names an assertion of the same capture, refuse with a typed `DIGEST_MISMATCH` unless `statement_sha256` equals the digest of that assertion's statement bytes; aggregate all mismatches in one refusal. RED first on a one-record capture with a wrong digest.
- Review task, next cell: the reviewer may read the located assertion's statement through the retained capture, and judges a claim row on that statement and its block.

## 2. Twelve feature relations and five mechanism relations resolve to one block each

**What the reviewer saw.** `rel:cf:01` to `rel:cf:12` (CONCERNS_FEATURE) all derive from one assertion on the data-acquisition paragraph; `rel:mech:1` to `rel:mech:5` (CLAIM_CONCERNS) all derive from one assertion in the discussion opening.

**What is true.** Assertion `rel:069` on `page:2:block:002` is the sentence that points the reader to the Methods section for location details. It carries 36 formalization targets: `relation_type`, `source_id` and `target_id` for each of the twelve relations. It names no observation and no feature. Assertion `rel:062` on `page:2:block:007` is a sentence about maximum earthquake depth against a spreading-rate relationship; it carries 15 targets, the three fields of each of the five mechanism relations, and names no hypothesis. The pattern is wider than these seventeen: the capture's fan-out distribution has 306 assertions formalizing one record and a tail of hubs, the largest formalizing 47 distinct records (`rel:078`) and 23 (`rel:081`), both on one reference-list block.

**Root cause.** The derivation rule says every relation endpoint and every property must be named by a formalization target, and the adapter checks that the target record and path exist (UNKNOWN_FORMALIZATION_TARGET, UNDERIVED_FIELD). It does not check that the formalizing assertion's statement has anything to do with the value. Relations that are implicit in context, an observation about RC2 concerning RC2, have no verbatim sentence of their own; the honest options were a typed RELATION_ABSENT gap or an assertion on the sentence that actually names both endpoints. The producer satisfied the letter of the rule by hanging all such relations on one nearby sentence. The pairings are true on the reading, which is why the reviewer supported them; the evidence pointers are false.

**Classification.** Evidence mis-attribution through a hub assertion: a producer behaviour the rule permits and the gates cannot see. Not a hallucination; the facts hold. A protocol defect in the derivation rule's reach.

**Fixes.**
- Core-12, mechanical and additive: a derivation-locality census axis. For each relation, record whether the formalizing assertion's block is among the blocks that formalize at least one of its endpoints; report per capture the count of non-local relation derivations and the per-assertion fan-out (distinct records formalized), with the top hubs listed. No refusal at first; the number goes beside the census in the run result and the launch log. A profile may later refuse above a threshold.
- Skill: state that a relation's endpoints are formalized by an assertion whose statement names both endpoints, and that a relation the reading only implies is a RELATION_ABSENT gap, not a derivation from a neighbouring sentence.
- Review task: name derivation locality as a thing to check, so the reviewer's finding this time becomes a step next time.

## 3. One NOT_SUPPORTED disposition rests on the wrong block

**What the reviewer saw.** `claim:mechanism-magmatic-tectonic` carries `hypothesis_disposition: NOT_SUPPORTED`; its locator lands on the block that raises the possibility; the rejection sits later.

**What is true.** All six fields of that claim, including the disposition, derive from assertion `c:072` on `page:4:block:002`, modality HYPOTHESISED, whose statement is the sentence introducing the third possibility. The rejection is the next prose block, `page:4:block:003` (the reviewer's "two blocks later" counts a figure-panel block between). No assertion on the rejecting block formalizes the disposition. And this is systematic: all five `hypothesis_disposition` values in the capture derive from HYPOTHESISED assertions, that is, from the sentence that states each hypothesis, never from the sentence that disposes of it.

**Root cause.** Same rule gap as point 2, in its property form: a disposition is an evaluative value, and the assertion that formalizes it must be one that evaluates. The adapter checks that the target exists. The producer put every claim's disposition on the claim's own statement assertion, presumably because that assertion already carried the claim's other five fields.

**Classification.** Mis-derivation, not hallucination: the reviewer confirmed the disposition on the reading. The value is right and the evidence pointer is wrong, and the rule cannot tell.

**Fixes.**
- Core-12, typed and cheap: modality-disposition consistency. A `hypothesis_disposition` (and any field a pack marks as evaluative) must be formalized by at least one assertion whose modality is not HYPOTHESISED; refuse with a typed reason, aggregated, RED first. This is a pack-level declaration (which fields are evaluative) plus one adapter check.
- Skill: the disposition of a hypothesis is captured from the sentence that disposes of it.

## What is common to the three

The derivation rule binds every value to an assertion and every assertion to a block, and the adapter enforces the binding's existence, never its content. A digest that nobody recomputes, a hub sentence carrying thirty-six targets, and a disposition attached to the sentence it disposes of are three faces of one gap: the protocol proves that a pointer exists, and leaves what the pointer points at to review. Two of the three admit cheap mechanical checks (the digest, the modality of the formalizing assertion); the third admits a census axis now and a threshold later. None of the three changes a result of run-04: the review judged the rows on the reading and they hold. What changes is what the next cell's gates can see.

## Core-12 scope, proposed

1. `DIGEST_MISMATCH` in the document adapter, aggregated.
2. Modality-disposition consistency for pack-declared evaluative fields, aggregated.
3. Derivation-locality and fan-out as census axes, reported, not refused.
4. Skill sentences for 2 and 3; review-task sentences for 1 and 3.
5. RED first for each, ledger entry after Core-11's.
