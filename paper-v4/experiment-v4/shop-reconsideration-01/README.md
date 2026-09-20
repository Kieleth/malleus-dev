# The Shop staged reconsideration, bound for the paper

This cell prints nothing of its own. It binds the manuscript's Shop
reconsideration subsection to the frozen files the run left behind, so every
number the paper prints there is read from a file and not from a handover.

## The binding, before anything was written

**1. The exact claim this cell puts in the paper.** A fresh model session,
given new evidence about records it had written earlier, changed what the
evidence changed, kept what it did not, and said what it could not record. It
did so twice: once over three declared obligations, and once over five, the
second time on a graph whose ontology the author had grown by a recorded
additive revision with the rule layer re-bound and nothing earlier rewritten. A
second fresh session assessed every judgement, the author ratified both
records, and Core's review-coverage checker certified that the third boundary
reviewed every obligation.

**2. The smallest observation that supports or falsifies it, with its counts
and the layer it tests.**

| Observation | Count | Layer it tests |
| :-- | :-- | :-- |
| the assessor's judgements over the second boundary | correctly changed 2, correctly preserved 1, missed 0, spurious 0, over 3 obligations | one fresh assessor session, judging one review per obligation against ground truth |
| the assessor's judgements over the third boundary | correctly changed 1, correctly preserved 4, missed 0, spurious 0, over 5 obligations | the same, one fresh session for that boundary |
| every `SATISFIED` verdict in the run | 0 violations, and 764 compiled facts at the third boundary's single admission | the structural gate plus the two Prolog rules `NO_CONFLICTING_QUANTITY` and `NO_EMPTY_RECORD`, at admission, under the check contract the history required |
| the third boundary's completion result | complete, nothing missing, nothing stale, 1 pending correction and 4 unchanged over 5 reviews | `malleus.acquisition.check_review_coverage`, which reads the boundary and the reviews and nothing else |
| the second boundary's completion result | refused, `MALFORMED_INPUT` on `review.boundary_identity` | the same checker; the packet handed the producer the boundary's name where the checker requires its digest, so that run has no certificate as produced |
| the two ratifications | no judgement changed in either | the author, reading each record in full, bound to that record's digest |
| the recorded ontology revision | 2 classes added, 1 check contract re-bound, graph unchanged, ledger 38 events to 41 | replay on the pinned Core export, against the previously archived export |

Falsification would be a count that does not match the record, a certificate
that does not reproduce from the archived reviews, a digest in the manuscript
that no file carries, or a run of 60 normalised characters shared between the
manuscript and the chapter's text or the evidence packets.

**3. The artifacts reused.** Nothing is produced here. Every file below already
existed when this cell was written.

| Artifact | Path | sha256 |
| :-- | :-- | :-- |
| the durable record of the results | `handover/2026-09-18-shop-reconsideration-journal.md` | `47496fdbea76c633c74303171478eab9c53769d5d826d6174f4e623b2dedaa57` |
| table population, archive manifest | `private/shop-progressive-01/producer/stage-a/archive/2026-09-17T04:48:13Z/ARCHIVE.json` | `8bcff240afc98c35cea400649a1f706655bdd0d30407782fce9cc3f90c1286cd` |
| second boundary, archive manifest | `private/shop-progressive-01/producer/stage-b/archive/2026-09-17T14:37:05Z/ARCHIVE.json` | `ec2335eaf6382714b641f811e9e68623442696f2583515dddfb441528d5a998c` |
| third boundary, archive manifest | `private/shop-progressive-01/producer/stage-c/archive/2026-09-19T01:12:08Z/ARCHIVE.json` | `6d624d962bfd70cac92634b4e31a18f6dfd0b7e5b7d0783b4c567edad4052146` |
| third boundary, review-coverage certificate | `private/shop-progressive-01/producer/stage-c/review-coverage.json` | `e240d837cd2c6da3dc05a562724c530dc279a798eb7f724746dfd742e1557aec` |
| third boundary, replay verification | `private/shop-progressive-01/producer/stage-c/replay-verification.json` | `b8ef94776e318b6869fc54c8280673d78ded21cbd00ff994439e93759481915f` |
| the recorded ontology revision, receipt | `private/shop-progressive-01/producer/stage-c/revision-receipt.json` | `a286dbef69dfaddcd1aaadc5c0f2ffbd87a15ece141da1007fa85c5a001e4e81` |
| second boundary, assessor's record | `private/shop-progressive-01/assessment/stage-b-packet/review-record.json` | `d35ab5a9c7ec90157be62f4f1a1143afac00a79a8b8b607ad6b744980b92176b` |
| second boundary, ratified form | `private/shop-progressive-01/assessment/stage-b-packet/review-record-ratified.json` | `541130a46b54165b0507405cad22c8cfad6144f8e72c8ac75ccac8b256264de2` |
| third boundary, assessor's record | `private/shop-progressive-01/assessment/stage-c-packet/review-record.json` | `90723d8fb9f97e2aeb0c8b0e64c394fc82e6616cd034677bc6225fae378420c5` |
| third boundary, ratified form | `private/shop-progressive-01/assessment/stage-c-packet/review-record-ratified.json` | `c4d001108edc5773ad48478de6a6f8b827fa1af454102cbf4bb5dffef0ec8310` |
| author ratification, second boundary | `paper-v4/evaluation-v4/author-ratification-2026-09-17-shop-staged-review.md` | `552592661bae1b4d27eb581f6fdccc91d7348e9c51da88c5a911c2e658d00cbc` |
| author ratification, third boundary | `paper-v4/evaluation-v4/author-ratification-2026-09-18-shop-third-boundary.md` | `ff172ee78de718330c60f9e8f287fb28dd795695a9324fbd9ad11c5dc2238256` |

Core coordinates. The repository's `main` at close-out is
`ff1c69315f68de949a223aedd3175e0319802807`. The third boundary ran against the
export `private/shop-progressive-01/runtime-d5d014ba`, Core
`d5d014ba1d7e3bfe906bc71dc93ded5657a3b424`, governance head `OVR-000464`, and
that export's `src/malleus` is the same 52 modules and the same digest as
`git archive d5d014ba1d7e3bfe906bc71dc93ded5657a3b424 src/malleus`. The table
population and the second boundary ran against the earlier export
`private/shop-progressive-01/runtime`, Core
`e7937b89917c8da7ee4a08acc22e99ad12b9985b`, governance head `OVR-000462`, and
they keep replaying against it. `src/malleus` is unchanged between `d5d014ba`
and `ff1c6931`.

The Core the paper gate imports for this cell is a separate coordinate, and on
2026-09-19 it moved to `d89a0c4718654249ad678eaff62e7b1daba30b6f`, the sealed
commit carrying the one-call atomic admission
`malleus.compiler.check_and_admit_population_plan`, governance head
`OVR-000468`. E-0436 is the standing rule: when Core changes, the paper's pin
moves to it, the cells re-run on it and the new fingerprints are the baseline.
That export is 53 modules,
`sha256:340196130e1820e9a4f9979223f40dcf6b8c1227d8805d812fd08ca529a3ed04`,
against `d5d014ba`'s 52 and
`sha256:f2fd444d09072c02575e64d6e918b30599b2ccb5823639188d76dabb72a3e73c`; the
one module added is `_contract_pipeline/admission.py`. Nothing this cell reads
moved with the pin. This cell produces no artifact: it reads frozen records,
so the move changes which Core the assertions import and no measured value.

Core capability reused, not written here:
`malleus.acquisition.check_review_coverage` for the completion certificate, and
`compose_contract_revision(check_contract_descriptors=...)` with the
`REBIND_CHECK_CONTRACT` change kind for the recorded revision.

**4. What this cell excludes, and therefore what its result may never be quoted
for.**

The counts are tallies of judgements. They are not a rate, a score, a
percentage or an accuracy, and eight judgements over two boundaries carry no
denominator that would make them one. Nothing here was run against a
hand-authored expected graph, so no comparison with the Small Shop's
adopter-authored fixtures may be drawn from it. Nothing here bears on models in
general: three producer sessions and two assessor sessions, one model, one
domain, one chapter. The table population is not a reviewed result; it is
`PARTIAL`, it carried no obligations, no assessor and no ratification, and it
appears only as the state the next two sessions inherited. The second
boundary's run has no completion certificate as produced, so that boundary's
counts may be quoted and its run may not be called mechanically complete. The
`SATISFIED` verdicts are the structural gate and two named domain rules; they
are not semantic correctness, not faithfulness to the source, and two rules are
not an oracle. The recorded revision is one additive revision with the rule
layer re-bound; it is not general ontology migration and not policy migration,
both of which Core's own status declares absent, and narrowing or removal
refuses with `NON_ADDITIVE_CHANGE`. The ratifications cover each record's
judgements and their counts; both binding files state that the
review-coverage certificate is recorded separately and is not ratified. One
modelling decision stands unresolved by evidence: whether the correction
relation should target the standing state record or the one it corrected.

## What the tests in this cell do

`test_shop_reconsideration.py` reads every number the manuscript's subsection
prints out of the frozen file that carries it, and refuses the manuscript if a
number, a digest or a named layer drifts from the record. It also refuses any
run of 60 normalised characters shared between the subsection and the chapter's
retained text or the three evidence packets, which is the rule that keeps the
chapter's prose out of this repository.

The evidence packets and the producer workspaces stay under `private/`. They
are available to the author for verification and they never enter git.

Run it alone, with the Core the gate pins first on the import path:

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=private/shop-progressive-01/runtime-d89a0c47/src \
    .venv/bin/python -m pytest -q -p no:cacheprovider -o pythonpath= \
    paper-v4/experiment-v4/shop-reconsideration-01/test_shop_reconsideration.py
```

The `-o pythonpath=` matters. This checkout's `src/malleus` carries seven
gitignored modules that no commit does, so a plain run imports more modules
than the pin has and the Core assertion refuses, correctly. Under the paper
gate the cell runs in the `d89a0c47` pinned group against a `git archive`
export of that commit, and that export and the private
`runtime-d89a0c47` export give the same 53 modules and the same digest.

Ledger entries: E-0433 to E-0483. Run report:
`private/shop-progressive-01/D0-REPORT.md`, addenda 1 to 18.
