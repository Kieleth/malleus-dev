# Malleus paper v4 run-09 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v3.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 210 for
CQ-01, 547 for CQ-02, 359 for CQ-03, 350 for
CQ-04, 1466 in all. Cite reading block ids only. Write the reasons in
your own words and copy no source passage into this record.

Each `rationale` opens with the fixed tokens the task defines: `DIGEST_OK` or
`DIGEST_MISMATCH` where the record carries a statement digest, then
`DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL`, then, on a `SUBJECT` or an
`ENTITY` row only, one of `SUBJECT_IN_BLOCK`, `SUBJECT_NOT_IN_BLOCK` or
`NO_SUBJECT_IN_ROW`; then the reason in your own words. The `rows` grammar is
closed at four keys and the validator is frozen, which is why every finding
lives at the head of the text field.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:88b69f6e80a3b9eac3a2c990178186df9c52fed3ced5c4e020162b0c202fa795",
    "review_input_manifest_sha256": "sha256:815c42b75268c684e632018123d9dfcf3280c407058518dc3b6fdf2e1cb833b5"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-09",
    "completed_at": "2026-09-05T06:50:01Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "CQ-01 asks four things: the observing system, the campaign, how many instruments went in, and how the data were acquired. All four are carried by named rows. The observing system is the instrument record at row 30, described as a network of ocean-bottom seismometers, on page:2:block:002. The campaign appears as four Campaign rows, rows 0 to 3; row 2 is the cruise itself and row 1 dates the passive experiment to two months of 2019 and ties it to that cruise, on page:6:block:002. The instrument count is carried with its value at rows 12 and 202, nineteen deployed, while rows 13 and 203 give the seventeen that returned usable data, each with a count scope saying which is which, so the two numbers cannot be confused. Acquisition is carried by row 199, which links the instrument network to the cruise on page:2:block:002, and is filled out by the recording duration at row 3 and the instrument spacing at row 108. The binding is type-only, so most of the rows are CO2 concentrations, segment geometry, isotherms, affiliations and software entries with no bearing on this question; that is over-return by the binding, not a failure to answer, and it leaves none of the four requested parts ambiguous. One method note on the subject axis: a SUBJECT row carries its subject's name in its own projection, but an ENTITY row carries the subject only as an identifier, so for those I resolved the identifier to a name through that same record's projection elsewhere in the query result, which is itself a bound material, and then looked for that name in the block. Two residuals for the ratifier: the observing system has no proper name in the source, so the row names it by instrument type and puts the network in a description slot; and the rows that project a counted record under the Observation type, rows 38 to 56 among them, repeat a quantity's name without its number, which would mislead anyone reading those rows without the counted projection of the same record.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:1:block:005",
        "page:10:block:043"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Campaign record campaign:microseismicity-study. The block its derivation reaches carries the setting paragraph's opening, which announces a microseismicity study on the equatorial Atlantic ridge, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects campaign:obs-experiment, with a temporal precision of month. That comes from the methods' opening, which dates the passive experiment to two months of 2019 and ties it to the cruise, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Campaign record campaign:smarties. The cited block holds the acknowledgement of the ship's company for the 2019 cruise, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:10:block:043",
            "page:10:block:044",
            "page:10:block:046",
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects campaign:smarties-recording, with a duration of ~21 days, a temporal precision of day. What the block reached carries is the results' recording duration and instrument spacing, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:all-mechanisms, with a count of 6. The derivation lands on the methods' selection thresholds for focal mechanisms and the count of new and total solutions they yield, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:identified-760, with a count of 760. The block its derivation reaches carries the methods' detection step, which gives the total registered in the phase database and the minimum number of instruments each kept event had to appear on, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:located-514, with a count of 514. That comes from the results' count of events located around the transform-ridge intersection, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rti, is named in that block.",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:location-categories, with a count of 4. The cited block holds the results' classification of locations into four quality categories, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:magnitude-groups, with a count of 3. What the block reached carries is the methods' split of the catalogue into three geographic groups and the b values found for them, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:mar-events, with a count of 317. The derivation lands on the second figure's own tally of events along the ridge profile, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The locator is the figure tally; a second derivation reaches the methods sentence that gives the same total for the ridge profile in prose, and both blocks are cited.",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:min-obs-per-event, with a count of 5. The block its derivation reaches carries the methods' detection step, which gives the total registered in the phase database and the minimum number of instruments each kept event had to appear on, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:new-mechanisms, with a count of 3. That comes from the methods' selection thresholds for focal mechanisms and the count of new and total solutions they yield, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:obs-deployed, with a count of 19. The cited block holds the results' acquisition sentence, which names the instrument network, its size, the cruise and the lengths of transform and ridge it covered, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, instrument:obs-network, is named in that block.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:obs-useful, with a count of 17. What the block reached carries is the results' automatic detection step and the number of instruments that gave usable data, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, instrument:obs-network, is named in that block.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:relocated-276, with a count of 276. The derivation lands on the methods' relocation settings and outcome, including the iterations, the separation limit, the events replaced and the per-profile totals, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:relocated-364, with a count of 364. The block its derivation reaches carries the methods' double-difference step, with the number of well-constrained events relocated and the residual, uncertainty and gap they satisfy, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:relocation-iterations, with a count of 5. That comes from the methods' relocation settings and outcome, including the iterations, the separation limit, the events replaced and the per-profile totals, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:romanche-events, with a count of 197. The cited block holds the second figure's own tally of events along the transform profile, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The locator is the figure tally; a second derivation reaches the methods sentence that gives the same total for the transform profile in prose, and both blocks are cited.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:subsections, with a count of 4. What the block reached carries is the setting paragraph's length for the studied ridge portion and its division into four named subsections, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:subset-360-size, with a count of 360. The derivation lands on the methods' velocity-model check, built on a sub-dataset selected by arrival count and station gap, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, dataset:subset-360, is named in that block.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:subset-45-size, with a count of 45. The block its derivation reaches carries the methods' forced-depth test, built on a subset of events from the deep band along one cross-section, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, dataset:subset-45, is named in that block.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:velest-iterations, with a count of 6. That comes from the methods' outcome of that check after a stated number of iterations, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:velocity-models, with a count of 5. The cited block holds the methods' construction of several 1-D P-wave models from the refraction profile and the depth to which that profile constrains velocity, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Dataset record dataset:earthquake-catalog. What the block reached carries is the data-availability sentence placing the event catalogue and the picked arrivals in a public repository, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Dataset record dataset:petdb. The derivation lands on the fifth figure's caption, which names the whole-rock database the compilation draws on, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:6:block:005",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects dataset:raw-seismic, with the location given for it. The block its derivation reaches carries the data-availability sentence pointing at the cruise website for the raw records and reports, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Dataset record dataset:refraction-profile. That comes from the results' use of an active-source refraction profile to pick the 1-D velocity model behind the travel times, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Dataset record dataset:subset-360. The cited block holds the methods' velocity-model check, built on a sub-dataset selected by arrival count and station gap, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Dataset record dataset:subset-45. What the block reached carries is the methods' forced-depth test, built on a subset of events from the deep band along one cross-section, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Dataset record dataset:supplementary-data-1. The derivation lands on the methods' compilation of whole-rock samples from the public database, restricted to the footprint of the instrument network, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:8:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Instrument record instrument:obs-network. The block its derivation reaches carries the results' acquisition sentence, which names the instrument network, its size, the cruise and the lengths of transform and ridge it covered, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:007",
            "page:5:block:004",
            "page:6:block:002",
            "page:8:block:003",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Method record method:double-difference. That comes from the results' pairing of a non-linear location algorithm with a subsequent double-difference relocation, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Method record method:first-motion. The cited block holds the methods' use of first-motion polarities from unfiltered vertical-component waveforms for the mechanisms, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Method record method:local-magnitude. What the block reached carries is the methods' local magnitude scale and its terms, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The description reproduces the formula as the text layer renders it and says so, so it claims no more than the block shows.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Method record method:nonlinear-location. The derivation lands on the results' pairing of a non-linear location algorithm with a subsequent double-difference relocation, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Method record method:oct-tree. The block its derivation reaches carries the methods' initial location step and the search algorithm it used, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:004"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Method record method:sta-lta. That comes from the results' automatic detection step and the number of instruments that gave usable data, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Method record method:wadati. The cited block holds the methods' Vp/Vs determination and the span of ratios tried in the sensitivity test, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:all-mechanisms. What the block reached carries is the methods' selection thresholds for focal mechanisms and the count of new and total solutions they yield, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:identified-760. The derivation lands on the methods' detection step, which gives the total registered in the phase database and the minimum number of instruments each kept event had to appear on, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:located-514. The block its derivation reaches carries the results' count of events located around the transform-ridge intersection, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rti, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:location-categories. That comes from the results' classification of locations into four quality categories, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:magnitude-groups. The cited block holds the methods' split of the catalogue into three geographic groups and the b values found for them, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:mar-events. What the block reached carries is the second figure's own tally of events along the ridge profile, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked. The locator is the figure tally; the second cited block states the same total in prose.",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:min-obs-per-event. The derivation lands on the methods' detection step, which gives the total registered in the phase database and the minimum number of instruments each kept event had to appear on, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:new-mechanisms. The block its derivation reaches carries the methods' selection thresholds for focal mechanisms and the count of new and total solutions they yield, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:obs-deployed. That comes from the results' acquisition sentence, which names the instrument network, its size, the cruise and the lengths of transform and ridge it covered, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, instrument:obs-network, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:obs-useful. The cited block holds the results' automatic detection step and the number of instruments that gave usable data, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, instrument:obs-network, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:relocated-276. What the block reached carries is the methods' relocation settings and outcome, including the iterations, the separation limit, the events replaced and the per-profile totals, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:relocated-364. The derivation lands on the methods' double-difference step, with the number of well-constrained events relocated and the residual, uncertainty and gap they satisfy, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:relocation-iterations. The block its derivation reaches carries the methods' relocation settings and outcome, including the iterations, the separation limit, the events replaced and the per-profile totals, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:romanche-events. That comes from the second figure's own tally of events along the transform profile, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked. The locator is the figure tally; the second cited block states the same total in prose.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:subsections. The cited block holds the setting paragraph's length for the studied ridge portion and its division into four named subsections, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:subset-360-size. What the block reached carries is the methods' velocity-model check, built on a sub-dataset selected by arrival count and station gap, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, dataset:subset-360, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:subset-45-size. The derivation lands on the methods' forced-depth test, built on a subset of events from the deep band along one cross-section, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, dataset:subset-45, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:velest-iterations. The block its derivation reaches carries the methods' outcome of that check after a stated number of iterations, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:velocity-models. That comes from the methods' construction of several 1-D P-wave models from the refraction profile and the depth to which that profile constrains velocity, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:abs:co2-primary, with a range of about 0.4 to 3 wt%. The cited block holds the abstract's summary of the geochemical syntheses, which puts an unusually large CO2 load in the primary melts and gives its range, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:abs:deep-eq-depth, with a range of 10 to 20 km. What the block reached carries is the abstract's headline result, earthquakes in the mantle beneath the ridge axis at depths far below the brittle-ductile boundary, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:b-value, with a value of 0.87. The derivation lands on the methods' catalogue statistics, the completeness magnitude and the b value, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:b-values-groups, with a range of 0.89 to 0.93. The block its derivation reaches carries the methods' split of the catalogue into three geographic groups and the b values found for them, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:bdb-at-ntd2, with a value of about 10 km. That comes from the discussion's reading of the microseismicity under the southern discontinuity as fixing the brittle-ductile boundary there, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:bdb, is named in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:bdb-isotherm-700, with a value of 700 \u00b0C with an uncertainty of 100 \u00b0C. The cited block holds the introduction's convention that the maximum earthquake depth, tied to a stated isotherm, defines the brittle-ductile boundary at slow ridges, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:bdb, is named in that block.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:bdb-isotherms-600-800, with a range of 600 to 800 \u00b0C. What the block reached carries is the discussion's first competing explanation, a very cold thick lithosphere that would push the boundary down to the depth of the corresponding isotherms, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:bdb, is named in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:bdb-shallow-offaxis, with an upper bound of 10 km. The derivation lands on the discussion's use of the shallow off-axis events west of the segment to argue the boundary stays shallow out to a young crustal age, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:bdb, is named in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:brittle-thickness-expected, with an upper bound of 10 km. The block its derivation reaches carries the results' spreading rate and the maximum earthquake depth and brittle thickness expected at that rate, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:brittle-thickness-ntds, with an upper bound of 10 km. That comes from the results' inference about how thick the brittle lithosphere is at the segment boundaries, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-ba-rc2, with a range of 0.7 to 4.6 wt%. The cited block holds the methods' pre-eruptive CO2 ranges from the two trace-element proxies, for both segments, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-ba-rc3, with a range of 0.06 to 0.8 wt%. What the block reached carries is the methods' pre-eruptive CO2 ranges from the two trace-element proxies, for both segments, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc3, is named in that block.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-ba90-rc2, with a range of 0.4 to 3 wt%. The derivation lands on the methods' primary-melt CO2 ranges from the two Fo90-corrected proxies, for both segments, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-ba90-rc3, with a range of 0.04 to 0.5 wt%. The block its derivation reaches carries the methods' primary-melt CO2 ranges from the two Fo90-corrected proxies, for both segments, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc3, is named in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-gas-loss, with a range of 80 to 90%. That comes from the discussion's account of CO2 solubility falling with pressure, so that most of the dissolved load has left the melt by the sea floor, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-preeruptive-rc2, with a range of 0.7 to 4.6 wt%. The cited block holds the results' pre-eruptive CO2 range for the segment after correcting for fractional crystallisation, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-rb-rc2, with a range of 0.9 to 4.3 wt%. What the block reached carries is the methods' pre-eruptive CO2 ranges from the two trace-element proxies, for both segments, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-rb-rc3, with a range of 0.07 to 1 wt%. The derivation lands on the methods' pre-eruptive CO2 ranges from the two trace-element proxies, for both segments, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc3, is named in that block.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-rb90-rc2, with a range of 0.5 to 2.8 wt%. The block its derivation reaches carries the methods' primary-melt CO2 ranges from the two Fo90-corrected proxies, for both segments, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-rb90-rc3, with a range of 0.05 to 0.7 wt%. That comes from the methods' primary-melt CO2 ranges from the two Fo90-corrected proxies, for both segments, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc3, is named in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-rc2-minimum, with a lower bound of 0.4 wt%. The cited block holds the methods' floor on primary-melt CO2 along the studied segment, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-rc2-primary, with a range of 0.4 to 3 wt%. What the block reached carries is the results' comparison of calculated melt CO2 between the segment carrying the deep earthquakes and the segment to its south, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:co2-rc3-primary, with a range of 0.04 to 0.7 wt%. The derivation lands on the results' comparison of calculated melt CO2 between the segment carrying the deep earthquakes and the segment to its south, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc3, is named in that block.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:cold-bdb-depth, with a value of about 20 km. The block its derivation reaches carries the discussion's first competing explanation, a very cold thick lithosphere that would push the boundary down to the depth of the corresponding isotherms, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:bdb, is named in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:cold-lithosphere-age, with a value of 45 Ma. That comes from the results' contrast between the expected southward shallowing of the boundary and the deep events actually seen beneath the segment axis, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:lithosphere, is named in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:criteria-met-fraction, with a value of about 78%. The cited block holds the methods' share of located events that satisfy at least two of those criteria, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:criterion-arrivals, with a lower bound of 8. What the block reached carries is the methods' three criteria for calling a location well constrained, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:criterion-gap, with an upper bound of 180\u00b0. The derivation lands on the methods' three criteria for calling a location well constrained, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:criterion-s-distance, with a value of 1.4. The block its derivation reaches carries the methods' three criteria for calling a location well constrained, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:crustal-age-13ma, with a value of about 1.3 Ma. That comes from the discussion's use of the shallow off-axis events west of the segment to argue the boundary stays shallow out to a young crustal age, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:crust, is named in that block. The block refers to the crust adjectivally, in naming a crustal age, rather than as a bare noun.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:crustal-thickness-west-flank, with a value of 5.4 km with an uncertainty of 0.3 km. The cited block holds the results' refraction-derived crustal thickness on the western flank, and what it implies about where the events sit, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:crust, is named in that block.",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:deep-eq-alignment, with a value of about 150\u00b0. What the block reached carries is the discussion's note that deep events under the segment axis lie along a direction matching the main axial normal faults instead of clustering, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:deep-eq-bsf-range, with a range of 10 to 19 km. The derivation lands on the sixth figure's caption, which states the depth range of the deep events under the ridge axis and reads them as degassing-driven, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:mar, is named in that block.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:deep-rc2-depth, with a range of about 10 to 20 km. The block its derivation reaches carries the results' three key depth observations along the four subsections, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:degassing-depth-window, with a range of 10 to 20 km. That comes from the discussion's expectation that melt keeps degassing on its way up and seeds earthquakes across a mantle depth window, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:mantle, is named in that block.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:depth-shift-uncertainty, with a value of about 2.6 km. The cited block holds the methods' depth-resolution test, where axial events stay in the same depth band and the shifts fall inside the average depth uncertainty, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:depth-uncertainty-limit, with an upper bound of 10 km. What the block reached carries is the methods' quality envelope for the located catalogue and its mean horizontal and vertical errors, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:dry-melting-depth, with a range of 60 to 70 km. The derivation lands on the introduction's two melting depths, the volatile-present onset and the start of extensive dry melting, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:equatorial-co2-average, with a value of about 2800 ppm. The block its derivation reaches carries the discussion's recall of earlier estimates of CO2 concentration across equatorial Atlantic segments, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:equatorial-atlantic, is named in that block.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:equatorial-co2-max, with a value of about 8799 ppm. That comes from the discussion's recall of earlier estimates of CO2 concentration across equatorial Atlantic segments, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:equatorial-atlantic, is named in that block.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:error-ellipsoid-confidence, with a value of 68%. The cited block holds the methods' description of the confidence ellipsoid the location code returns, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, software:nonlinloc-program, is named in that block.",
          "source_locators": [
            "page:7:block:005"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:expected-depth-slow, with an upper bound of 8 km. What the block reached carries is the introduction's thermally modelled expectation for maximum earthquake depth at slow and at ultraslow ridges, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:expected-depth-ultraslow, with an upper bound of 12 km. The derivation lands on the introduction's thermally modelled expectation for maximum earthquake depth at slow and at ultraslow ridges, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:expected-max-depth-here, with an upper bound of 10 km. The block its derivation reaches carries the results' spreading rate and the maximum earthquake depth and brittle thickness expected at that rate, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:fm-fault-plane-uncertainty, with an upper bound of 45\u00b0. That comes from the methods' selection thresholds for focal mechanisms and the count of new and total solutions they yield, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:fm-misfit, with an upper bound of 20%. The cited block holds the methods' selection thresholds for focal mechanisms and the count of new and total solutions they yield, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:fm-polarities, with a lower bound of 8. What the block reached carries is the methods' selection thresholds for focal mechanisms and the count of new and total solutions they yield, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:fm-probability, with a lower bound of 60%. The derivation lands on the methods' selection thresholds for focal mechanisms and the count of new and total solutions they yield, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:full-spreading-rate, with a value of about 32 mm/yr. The block its derivation reaches carries the results' spreading rate and the maximum earthquake depth and brittle thickness expected at that rate, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The block gives the rate without repeating that it is this study area; the surrounding results are about no other, and it is twice the half-rate the setting paragraph gives.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:hot-mantle-temperature, with a lower bound of 1100 \u00b0C. That comes from the discussion's conclusion that accretion at the segment is magmatic and the host mantle is hot, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:mantle, is named in that block.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:iceland-depths, with a lower bound of 10 km. The cited block holds the discussion's third competing explanation, drawing on magmatic-tectonic sequences elsewhere and the depths reported for them, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:instrument-spacing, with a value of about 30 km. What the block reached carries is the results' recording duration and instrument spacing, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002",
            "page:8:block:003"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:isotherm-750-line, with a value of 750 \u00b0C. The derivation lands on the fourth figure's caption, which identifies the isotherm drawn as a dashed line, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:isotherm-750, is named in that block.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:lithospheric-age-contours, with a value of 10 Ma. The block its derivation reaches carries the first figure's caption, which explains the lithospheric-age contours and their spacing, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:low-frequency-threshold, with a lower bound of 5 Hz. That comes from the discussion's spectral observation that some deep events lack energy above a threshold frequency, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:5:block:008"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:magnitude-completeness, with a value of 1.5. The cited block holds the methods' catalogue statistics, the completeness magnitude and the b value, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:mar-coverage, with a value of 120 km. What the block reached carries is the results' acquisition sentence, which names the instrument network, its size, the cruise and the lengths of transform and ridge it covered, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:mar, is named in that block.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:mar-half-spreading, with a value of 16 mm/yr. The derivation lands on the setting paragraph's half-spreading rate for the ridge here, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:mar, is named in that block.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:max-event-separation, with a value of 6 km. The block its derivation reaches carries the methods' relocation settings and outcome, including the iterations, the separation limit, the events replaced and the per-profile totals, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:mayotte-depths, with a lower bound of 30 km. That comes from the discussion's third competing explanation, drawing on magmatic-tectonic sequences elsewhere and the depths reported for them, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:mayotte, is named in that block.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:mean-horizontal-error, with a value of about 2.8 km. The cited block holds the methods' quality envelope for the located catalogue and its mean horizontal and vertical errors, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:mean-vertical-error, with a value of about 2.9 km. What the block reached carries is the methods' quality envelope for the located catalogue and its mean horizontal and vertical errors, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:median-valley-width, with a value of 10 km. The derivation lands on the tectonics paragraph's length, median-valley width and neo-volcanic ridge orientation for the northern segment, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:median-valley, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:melt-fraction-lab, with a value of about 1.1%. The block its derivation reaches carries the closing section's citation of the melt fraction and water content proposed to explain reflections at the lithosphere-asthenosphere boundary, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:lab, is named in that block.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:model1-velocity, with a lower bound of 7.2 km/s. That comes from the methods' remark that the fastest of the trial models puts an implausibly high P velocity at shallow depth for crust of that age, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, model:model-1, is named in that block.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:neovolcanic-orientation, with a value of 154\u00b0. The cited block holds the tectonics paragraph's length, median-valley width and neo-volcanic ridge orientation for the northern segment, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:neovolcanic-ridge, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:no-earthquakes-below-20, with a lower bound of 20 km. What the block reached carries is the discussion's note that nothing is seen below a certain depth under the segment axis, and the temperature offered as the reason, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:ntd1-length, with a value of about 35 km. The derivation lands on the tectonics paragraph's length, orientation and faulting for the first discontinuity, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:ntd1, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:ntd1-orientation, with a value of 76\u00b0. The block its derivation reaches carries the tectonics paragraph's length, orientation and faulting for the first discontinuity, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:ntd1, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:ntd2-deeper, with an upper bound of 10 km. That comes from the results' note that events under the southern discontinuity reach somewhat greater depth, as expected for a slow-slipping discontinuity, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:ntd2, is named in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:ntd2-depth, with a range of 4 to 10 km. The cited block holds the results' three key depth observations along the four subsections, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:ntd2, is named in that block.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:ntd2-depth-range, with an upper bound of 10 km. What the block reached carries is the results' statement of where the expected shallow depth range is actually observed, under the core complex and under the southern discontinuity, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:ntd2, is named in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:ntd2-offset, with a value of about 33 km. The derivation lands on the tectonics paragraph's offset, orientation and faulting for the second discontinuity, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:ntd2, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:ntd2-orientation, with a value of 110\u00b0. The block its derivation reaches carries the tectonics paragraph's offset, orientation and faulting for the second discontinuity, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:ntd2, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:occ-depth-range, with an upper bound of 6 km. That comes from the results' statement of where the expected shallow depth range is actually observed, under the core complex and under the southern discontinuity, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:occ, is named in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:offaxis-shallow-depth, with an upper bound of 6 km. The cited block holds the discussion's use of the shallow off-axis events west of the segment to argue the boundary stays shallow out to a young crustal age, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:offaxis-swarm-depth, with an upper bound of 10 km. What the block reached carries is the discussion's attribution of the shallow swarm-like activity west of the axis to off-axis magmatism, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:5:block:001"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:pore-pressure-trigger, with a range of 2 to 3 bars. The derivation lands on the discussion's appeal to the small pore-pressure rise known to be enough to trigger earthquakes, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:profile-halfwidth, with a value of 10 km. The block its derivation reaches carries the second figure's caption, which states the swath half-width used for the depth profiles, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:3:block:005"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:quality-a-uncertainty, with an upper bound of 5 km. That comes from the second figure's legend, which sets the uncertainty admitted by each location-quality class, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:3:block:004"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:quality-d-uncertainty, with a range of 5 to 10 km. The cited block holds the second figure's legend, which sets the uncertainty admitted by each location-quality class, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The legend puts class D above five and up to ten kilometres; the row carries the two bounds and claims nothing about which end is inclusive.",
          "source_locators": [
            "page:3:block:004"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:rc2-ba, with a lower bound of 89 ppm. What the block reached carries is the results' report that samples from the northern segment carry incompatible trace-element concentrations above stated thresholds, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:rc2-deep-earthquakes, with a range of 16 to 19 km. The derivation lands on the results' contrast between the expected southward shallowing of the boundary and the deep events actually seen beneath the segment axis, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:rc2-length, with a value of about 22 km. The block its derivation reaches carries the tectonics paragraph's length, median-valley width and neo-volcanic ridge orientation for the northern segment, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:rc2-rb, with a lower bound of 8 ppm. That comes from the results' report that samples from the northern segment carry incompatible trace-element concentrations above stated thresholds, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:rc3-length, with a value of 50 km. The cited block holds the tectonics paragraph's length and orientation for the southern segment, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc3, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:rc3-orientation, with a value of about 165\u00b0. What the block reached carries is the tectonics paragraph's length and orientation for the southern segment, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc3, is named in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:refraction-depth-range, with an upper bound of 60 km. The derivation lands on the methods' construction of several 1-D P-wave models from the refraction profile and the depth to which that profile constrains velocity, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:relocation-rms, with an upper bound of 0.25 s. The block its derivation reaches carries the methods' double-difference step, with the number of well-constrained events relocated and the residual, uncertainty and gap they satisfy, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:relocation-uncertainty, with a value of 2.1 km. That comes from the second figure's legend value for location uncertainty, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The locator is a bare legend value; the second cited block supplies the sentence that identifies it as the average horizontal uncertainty after relocation.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:relocation-uncertainty-limit, with an upper bound of 5 km. The cited block holds the methods' double-difference step, with the number of well-constrained events relocated and the residual, uncertainty and gap they satisfy, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:rms-limit, with an upper bound of 0.3 s. What the block reached carries is the methods' quality envelope for the located catalogue and its mean horizontal and vertical errors, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:romanche-chain-length, with a value of about 200 km. The derivation lands on the setting paragraph's placement of the study area on the ridge segment between the two transforms, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:mar-romanche-chain, is named in that block.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:romanche-coverage, with a value of 140 km. The block its derivation reaches carries the results' acquisition sentence, which names the instrument network, its size, the cruise and the lengths of transform and ridge it covered, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:romanche-tf, is named in that block.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:saturation-depth, with a value of about 25 km. That comes from the results' solubility calculation, which puts saturation and the onset of degassing at a stated pressure, depth and temperature, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:saturation-pressure, with a value of about 0.7 GPa. The cited block holds the results' solubility calculation, which puts saturation and the onset of degassing at a stated pressure, depth and temperature, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:saturation-temperature, with a value of 1250 \u00b0C. What the block reached carries is the results' solubility calculation, which puts saturation and the onset of degassing at a stated pressure, depth and temperature, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:shading-threshold, with a value of 10 km. The derivation lands on the third figure's caption, which sets the depth at which the shading of the sections changes, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:4:block:007"
          ]
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:shallow-rti-depth, with a range of 0 to 6 km. The block its derivation reaches carries the results' three key depth observations along the four subsections, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rti, is named in that block.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:solidus-anhydrous, with a value of about 1250 \u00b0C. That comes from the closing section's statement that volatiles lower the dry solidus so melt persists at sub-solidus temperatures at that boundary, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:asthenosphere, is named in that block. The subject reference resolves to a record named for the rock, which the block names, rather than to the layer its identifier suggests.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:solubility-calc-temperature, with a value of 1200 \u00b0C. The cited block holds the methods' solubility calculation and the parameters fed to it, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:studied-portion-length, with a value of about 120 km. What the block reached carries is the setting paragraph's length for the studied ridge portion and its division into four named subsections, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:subsection-length, with a range of 20 to 50 km. The derivation lands on the setting paragraph's length for the studied ridge portion and its division into four named subsections, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:subset-360-gap, with an upper bound of 180\u00b0. The block its derivation reaches carries the methods' velocity-model check, built on a sub-dataset selected by arrival count and station gap, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, dataset:subset-360, is named in that block.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:swir-highest-co2, with a value of 1.9 wt%. That comes from the discussion's citation of the largest melt CO2 content reported before this work, at the Southwest Indian Ridge, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:swir, is named in that block.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:temperature-10-20km, with a range of 1100 to 1200 \u00b0C. The cited block holds the discussion's thermal-model temperatures for the depth interval under the segment axis, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:temperature-below-20km, with a lower bound of 1200 \u00b0C. What the block reached carries is the discussion's note that nothing is seen below a certain depth under the segment axis, and the temperature offered as the reason, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:rc2, is named in that block.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:transect-halfwidth, with a value of 5 km. The derivation lands on the third figure's caption, which gives the swath half-width for the transects across the core complex, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:occ, is named in that block.",
          "source_locators": [
            "page:4:block:006"
          ]
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:velocity-perturbation, with a value of 0.1 km/s. The block its derivation reaches carries the methods' velocity perturbation test, applied uniformly at all depths, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:volatile-melting-depth, with a range of about 150 to 300 km. That comes from the introduction's two melting depths, the volatile-present onset and the start of extensive dry melting, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:vpvs-test-range, with a range of 1.5 to 2.5. The cited block holds the methods' Vp/Vs determination and the span of ratios tried in the sensitivity test, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:water-content-lab, with an upper bound of 332 ppm. What the block reached carries is the closing section's citation of the melt fraction and water content proposed to explain reflections at the lithosphere-asthenosphere boundary, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:lab, is named in that block.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:western-cluster-depth, with a range of about 2 to 6 km. The derivation lands on the results' western cluster with its shallow depths, used to argue the deep events are not a location artefact, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:axial-valley, is named in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:young-crust-age, with an upper bound of 7.5 Ma. The block its derivation reaches carries the methods' remark that the fastest of the trial models puts an implausibly high P velocity at shallow depth for crust of that age, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The subject the row attaches this to, feature:crust, is named in that block.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:brittany. That comes from the funding paragraph's list of the graduate-school project, the national programme and the regional council that funded the research, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:cnr-igag. The cited block holds the author affiliation footnote, which lists each institution with its city and country, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The name is the full affiliation string, city and country included, as the footnote gives it.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:erc. What the block reached carries is the funding paragraph's entry for the European Research Council grants, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:french-government. The derivation lands on the funding paragraph's list of the graduate-school project, the national programme and the regional council that funded the research, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:geo-ocean. The block its derivation reaches carries the author affiliation footnote, which lists each institution with its city and country, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The name is the full affiliation string, city and country included, as the footnote gives it.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:ipgp. That comes from the author affiliation footnote, which lists each institution with its city and country, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The name is the full affiliation string, city and country included, as the footnote gives it.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:isblue. The cited block holds the funding paragraph's list of the graduate-school project, the national programme and the regional council that funded the research, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 178,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:nsfc. What the block reached carries is the funding paragraph's entry for the Chinese national foundation grants to the first author, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 179,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:sio-hangzhou. The derivation lands on the author affiliation footnote, which lists each institution with its city and country, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The name is the full affiliation string, city and country included, as the footnote gives it.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 180,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:springer-nature. The block its derivation reaches carries the publisher's neutrality note in the back matter, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:11:block:004"
          ]
        },
        {
          "row_index": 181,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:tgir-fleet. That comes from the funding paragraph's statement that the cruise's shipping time came through the French oceanographic fleet infrastructure, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 182,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:unimore. The cited block holds the author affiliation footnote, which lists each institution with its city and country, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The name is the full affiliation string, city and country included, as the footnote gives it.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 183,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:zenodo. What the block reached carries is the data-availability sentence placing the event catalogue and the picked arrivals in a public repository, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The block names the repository the catalogue went into; whether that repository is well typed as an organisation is a modelling question, outside what is judged here.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 184,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the Organization record org:zjnsf. The derivation lands on the funding paragraph's entry for the Zhejiang provincial foundation grant, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 185,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects software:global-mapper, with the location given for it. The block its derivation reaches carries the code-availability entry for the structural-analysis package and where to obtain it, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 186,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the SoftwarePackage record software:gmt. That comes from the code-availability entry for the plotting toolbox, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. The block truncates the download location at a line break; the row asserts no location, so nothing rests on it.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 187,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects software:hash, with the location given for it, its version. The cited block holds the code-availability entry for the focal-mechanism package, with its version and download location, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 188,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects software:hypodd, with the location given for it, its version. What the block reached carries is the code-availability entry for the double-difference relocation program, with its version and download location, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 189,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the SoftwarePackage record software:hypodd-program. The derivation lands on the methods' double-difference step, with the number of well-constrained events relocated and the residual, uncertainty and gap they satisfy, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 190,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects software:nonlinloc, with the location given for it. The block its derivation reaches carries the code-availability entry for the location code and where to obtain it, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 191,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the SoftwarePackage record software:nonlinloc-program. That comes from the methods' initial location step and the search algorithm it used, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:7:block:004",
            "page:7:block:005"
          ]
        },
        {
          "row_index": 192,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects software:seisan, with the location given for it. The cited block holds the code-availability entry for the phase-picking software and where to obtain it, which is where the row comes from. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 193,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the SoftwarePackage record software:seisan-package. What the block reached carries is the methods' automatic detection step, run on the vertical components of the instruments that returned usable data, matching the row. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:002"
          ]
        },
        {
          "row_index": 194,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects software:velest, with the location given for it. The derivation lands on the code-availability entry for the 1-D velocity inversion program and where to obtain it, which states it. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 195,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects the SoftwarePackage record software:velest-program. The block its derivation reaches carries the methods' velocity-model check, built on a sub-dataset selected by arrival count and station gap, and that is what the row restates. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 196,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The record carries no assertion locator and no statement digest, so no digest comparison applies. The row projects software:zmap, with the location given for it. That comes from the code-availability entry for the catalogue-analysis software used for b-value and completeness, in the block the derivation lands on. The row attaches the record to nothing else, so the blocks that formalise it are the blocks it is judged on and locality holds by construction. The projection carries no subject reference at all. Several blocks formalise this record and every one of them is cited.",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 197,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The record carries no assertion locator and no statement digest, so no digest comparison applies. The row pairs campaign:smarties with org:tgir-fleet under FUNDED_BY. The cited block holds the funding paragraph's statement that the cruise's shipping time came through the French oceanographic fleet infrastructure, which is where the row comes from. The assertion that formalises the relation also formalises both endpoints, so the pointer rests where the pairing itself is stated. The block scopes the funding to the cruise shipping time; the row asserts only that a funding relation runs between these two, which the block does state.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 198,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The record carries no assertion locator and no statement digest, so no digest comparison applies. The row pairs dataset:earthquake-catalog with org:zenodo under DEPOSITED_IN. What the block reached carries is the data-availability sentence placing the event catalogue and the picked arrivals in a public repository, matching the row. The assertion that formalises the relation also formalises both endpoints, so the pointer rests where the pairing itself is stated.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 199,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The record carries no assertion locator and no statement digest, so no digest comparison applies. The row pairs instrument:obs-network with campaign:smarties under PART_OF_CAMPAIGN. The derivation lands on the results' acquisition sentence, which names the instrument network, its size, the cruise and the lengths of transform and ridge it covered, which states it. The assertion that formalises the relation also formalises both endpoints, so the pointer rests where the pairing itself is stated.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 200,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:subset-360-size, with a count of 360. The block its derivation reaches carries the methods' velocity-model check, built on a sub-dataset selected by arrival count and station gap, and that is what the row restates. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, dataset:subset-360, is named in that block.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 201,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:subset-45-size, with a count of 45. That comes from the methods' forced-depth test, built on a subset of events from the deep band along one cross-section, in the block the derivation lands on. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, dataset:subset-45, is named in that block.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 202,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:obs-deployed, with a count of 19. The cited block holds the results' acquisition sentence, which names the instrument network, its size, the cruise and the lengths of transform and ridge it covered, which is where the row comes from. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, instrument:obs-network, is named in that block.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 203,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects counted:obs-useful, with a count of 17. What the block reached carries is the results' automatic detection step and the number of instruments that gave usable data, matching the row. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, instrument:obs-network, is named in that block.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 204,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:subset-360-size. The derivation lands on the methods' velocity-model check, built on a sub-dataset selected by arrival count and station gap, which states it. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, dataset:subset-360, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 205,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:subset-45-size. The block its derivation reaches carries the methods' forced-depth test, built on a subset of events from the deep band along one cross-section, and that is what the row restates. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, dataset:subset-45, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 206,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:subset-360-gap, with an upper bound of 180\u00b0. That comes from the methods' velocity-model check, built on a sub-dataset selected by arrival count and station gap, in the block the derivation lands on. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, dataset:subset-360, is named in that block.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 207,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:obs-deployed. The cited block holds the results' acquisition sentence, which names the instrument network, its size, the cruise and the lengths of transform and ridge it covered, which is where the row comes from. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, instrument:obs-network, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 208,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects the Observation record counted:obs-useful. What the block reached carries is the results' automatic detection step and the number of instruments that gave usable data, matching the row. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, instrument:obs-network, is named in that block. This projection has no count slot, so the row names the quantity without carrying the number the same record carries under its counted type; nothing it does assert is left unbacked.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 209,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The SHA-256 of the located statement recomputes to the digest the record carries. The row projects obs:error-ellipsoid-confidence, with a value of 68%. The derivation lands on the methods' description of the confidence ellipsoid the location code returns, which states it. The record and the subject it points at are formalised in the same block, so the evidence pointer does not travel away from the pairing. The subject the row attaches this to, software:nonlinloc-program, is named in that block.",
          "source_locators": [
            "page:7:block:005"
          ]
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows name the subsection: the short ridge segment is returned as a record, relation rows place it among the four subsections of the studied ridge portion and south of the first non-transform discontinuity, and it is the subject of the observation rows that carry the deep event depths, so the first half of the question is answered directly. The second half is answered only in prose. Where the events sit relative to the ridge axis is carried inside the name and quantity-kind strings of observation records and never as a typed spatial relation: not one of the returned relations has an earthquake population as an endpoint, and none names a ridge axis at all, so a reader must parse a projected string to learn that the deep events lie beneath the axis rather than beside it. The same holds for their alignment direction. The returned set is also dominated by material outside the question, because the binding is type-only and expands every type in the question's set, so location-quality thresholds, velocity-model tests and melt chemistry arrive alongside the answer. Both halves are reachable from the rows; only one is reachable structurally.",
      "source_locators": [
        "page:1:block:005",
        "page:2:block:004",
        "page:2:block:006",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:009 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports as a calculated result what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:007 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:001 and page:5:block:002 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:001 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:006 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:002 and page:5:block:001 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:003 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:010 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:007 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:008 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 42,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The sentence begins at the end of page:3:block:001, where the absence of detachment-fault evidence is attached to the ten-kilometre-wide axial valley at the segment, and continues into page:4:block:001, which read alone appears to attach it to the segment as a whole. The row states it of the segment and drops that qualifier. The negative finding itself is in the reading."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:003 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:008 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:006 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 55,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The retained sentence starts mid-clause: the reading does not carry the subject that does the indicating, so what the block supports is that exhumed mantle is present and that a tectonic origin is supported, not the row's attribution of that support to the exhumed mantle. The demonstrative referent also sits outside the block, the naming of the subsection being in page:1:block:005."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports as a calculated result what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:007 reports as a calculated result what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:006 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:006 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:009 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:010 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:003 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:002 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:003 and page:6:block:005 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:003 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:002 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:004 and page:7:block:007 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:002 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:003 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 and page:6:block:002 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 and page:6:block:002 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:007 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:006 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:007 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:003 and page:7:block:007 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:004 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:010 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:004 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:003 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:003 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and page:2:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 101,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading attaches these inward dipping faults to the axial valley at the segment, the sentence starting at the end of page:3:block:001, whereas the row names them as bounding the segment. Their orientation and dip are supported; the narrower thing they bound is not."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:3:block:005",
            "page:5:block:005",
            "page:7:block:007",
            "page:7:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and page:5:block:009 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 and page:4:block:003 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 and page:4:block:003 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:002",
            "page:5:block:003",
            "page:5:block:006",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:002 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:003 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:3:block:003",
            "page:4:block:003",
            "page:4:block:004",
            "page:7:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:1:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:4:block:002",
            "page:5:block:001",
            "page:6:block:001",
            "page:7:block:009",
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:002 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and page:2:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and page:5:block:009 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:002 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:009 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 and page:4:block:003 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:007 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:010 and page:7:block:011 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:6:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:004 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:3:block:003",
            "page:4:block:002",
            "page:5:block:003",
            "page:5:block:009",
            "page:6:block:001",
            "page:7:block:012"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:005",
            "page:2:block:006",
            "page:2:block:007",
            "page:3:block:001",
            "page:3:block:005",
            "page:6:block:005",
            "page:7:block:007",
            "page:7:block:012",
            "page:8:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 and page:4:block:003 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:011 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 and page:3:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:2:block:004",
            "page:2:block:005",
            "page:3:block:001",
            "page:4:block:005",
            "page:4:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005",
            "page:2:block:007",
            "page:4:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:004 and page:2:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:4:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:001 and page:4:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005",
            "page:4:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:005 and page:4:block:006 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006",
            "page:8:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:006 and page:8:block:006 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:006 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:005 and page:8:block:007 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:005 and page:8:block:007 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and page:2:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:2:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:4:block:001",
            "page:4:block:003",
            "page:4:block:007",
            "page:5:block:002",
            "page:5:block:003",
            "page:5:block:004",
            "page:5:block:005",
            "page:5:block:006",
            "page:5:block:007",
            "page:6:block:005",
            "page:7:block:003",
            "page:7:block:010",
            "page:7:block:011",
            "page:8:block:001",
            "page:8:block:006",
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 151,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading attaches these inward dipping faults to the axial valley at the segment, the sentence starting at the end of page:3:block:001, whereas the row names them as bounding the segment. Their orientation and dip are supported; the narrower thing they bound is not."
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:5:block:004",
            "page:5:block:005",
            "page:5:block:006",
            "page:6:block:005",
            "page:8:block:006",
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:3:block:005",
            "page:5:block:005",
            "page:7:block:007",
            "page:7:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:003",
            "page:2:block:004",
            "page:2:block:006",
            "page:3:block:005",
            "page:4:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:001 and page:5:block:009 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010",
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:010 and page:7:block:011 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:011"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:011 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:2:block:004",
            "page:2:block:005",
            "page:3:block:001",
            "page:4:block:005",
            "page:4:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:003 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:002 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:003 and page:6:block:005 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:004 and page:7:block:007 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:003 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 and page:6:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 and page:6:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:007 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:006 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 178,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:007 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 179,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:003 and page:7:block:007 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 180,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 181,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 182,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:010 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 183,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 184,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 185,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 reports the concentration the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 186,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 187,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:002 reports the figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 188,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:002 reports the figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 189,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 190,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:004 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 191,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 192,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 193,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 194,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 195,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 196,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 197,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 198,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 199,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:003 reports the concentration the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 200,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 201,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 202,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 203,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 204,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 205,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 206,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 207,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 208,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 209,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports the age the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 210,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:008"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:008 reports the figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 211,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:008"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:008 reports the count the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 212,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:008"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:008 reports the orientation figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 213,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:008"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:008 reports the figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 214,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the age the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 215,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 and page:7:block:011 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 216,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:003 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 217,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:012 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 218,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 219,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 220,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:009 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 221,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:001 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 222,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:002 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 223,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 224,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 225,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:005 reports the figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 226,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:004 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 227,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:004 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 228,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 229,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:003 reports the orientation figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 230,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:003 reports the figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 231,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:003 reports the count the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 232,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:003 reports the figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 233,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:005 reports the rate the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 234,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 235,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:002 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 236,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002",
            "page:8:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:002 and the other cited blocks reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 237,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:010 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 238,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:2:block:007 reports the age the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 239,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:008 reports the frequency the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 240,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:002 reports the figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 241,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 242,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:005 reports the rate the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 243,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:007 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 244,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 245,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:001 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 246,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:001 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 247,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 248,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 249,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:009 reports the rate the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 250,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 251,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:007 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 252,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 253,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 254,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 255,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 256,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 257,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 258,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 259,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 260,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 261,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:001 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 262,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:003 reports the pressure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 263,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:005 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 264,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:004 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 265,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:004 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 266,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:004 reports the figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 267,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 268,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 269,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:004 reports the figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 270,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 271,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 272,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:6:block:003 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 273,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:006 reports the age the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 274,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:003 and page:7:block:007 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 275,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:006 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 276,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:001 reports the age the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 277,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 278,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 279,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:006 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 280,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:006 reports the pressure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 281,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:006 reports the temperature the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 282,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:4:block:007 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 283,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 284,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 285,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:007 reports the temperature the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 286,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 287,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 288,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:004 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 289,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 290,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 291,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:007 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 292,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:006 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose."
        },
        {
          "row_index": 293,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:010 reports the rate the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 294,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:002 reports the length, depth or thickness figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 295,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:7:block:002 reports the figure the row projects for the entity the record names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 296,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 297,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 298,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:009 reports the age the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries."
        },
        {
          "row_index": 299,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005",
            "page:2:block:007",
            "page:4:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 300,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 301,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and page:2:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 302,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:2:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:4:block:001",
            "page:4:block:003",
            "page:4:block:007",
            "page:5:block:002",
            "page:5:block:003",
            "page:5:block:004",
            "page:5:block:005",
            "page:5:block:006",
            "page:5:block:007",
            "page:6:block:005",
            "page:7:block:003",
            "page:7:block:010",
            "page:7:block:011",
            "page:8:block:001",
            "page:8:block:006",
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 303,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:5:block:004",
            "page:5:block:005",
            "page:5:block:006",
            "page:6:block:005",
            "page:8:block:006",
            "page:8:block:007"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 304,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 305,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 306,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 307,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:003",
            "page:2:block:004",
            "page:2:block:006",
            "page:3:block:005",
            "page:4:block:006"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 308,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:5:block:009 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 309,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:8:block:004 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 310,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:002",
            "page:2:block:005",
            "page:2:block:006",
            "page:2:block:007",
            "page:3:block:001",
            "page:3:block:005",
            "page:6:block:005",
            "page:7:block:007",
            "page:7:block:012",
            "page:8:block:002"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:001 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 311,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:3:block:001 and page:5:block:009 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 312,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 313,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:3:block:005",
            "page:5:block:005",
            "page:7:block:007",
            "page:7:block:009"
          ],
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The reading at page:1:block:005 and the other cited blocks introduces this feature under the name and description the row projects, and the projection carries nothing beyond that."
        },
        {
          "row_index": 314,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 describes the first non-transform discontinuity as characterised by a large set of faults with the strikes the source endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 315,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 describes the second non-transform discontinuity as having large areas affected by normal faults with the strikes the source endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 316,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 describes the first non-transform discontinuity as characterised by a large set of faults with the strikes the source endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 317,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 describes the second non-transform discontinuity as having large areas affected by normal faults with the strikes the source endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 318,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 says the core complex surface is heavily cut by normal faults with the strikes the target endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 319,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the ridge-transform-intersection segment is bounded on its eastern side by a westward dipping detachment fault, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 320,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The sentence carrying this bounding runs across a page break: its opening in page:3:block:001 attaches the bounding to the ten-kilometre-wide axial valley at the short ridge segment, and page:4:block:001 carries the rest. The row asserts the relation of the segment itself, so the qualifier that narrows it to the axial valley is missing. The fault orientation and the fact of a bounding are supported."
        },
        {
          "row_index": 321,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:004 places the cooled brittle lithosphere above the partially molten crust, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 322,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:004 places the cooled brittle lithosphere above the mantle, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 323,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 describes the first non-transform discontinuity as characterised by a large set of faults with the strikes the source endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 324,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the first non-transform discontinuity among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 325,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 describes the second non-transform discontinuity as having large areas affected by normal faults with the strikes the source endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 326,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the second non-transform discontinuity among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 327,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 says the core complex surface is heavily cut by normal faults with the strikes the target endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 328,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 places the oceanic core complex on the eastern side of the ridge-transform-intersection segment axis, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 329,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:007 places the oceanic core complex on the outside corner of the ridge, in figure-caption text, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 330,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the ridge-transform-intersection segment is bounded on its eastern side by a westward dipping detachment fault, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 331,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the ridge-transform-intersection segment among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 332,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The sentence carrying this bounding runs across a page break: its opening in page:3:block:001 attaches the bounding to the ten-kilometre-wide axial valley at the short ridge segment, and page:4:block:001 carries the rest. The row asserts the relation of the segment itself, so the qualifier that narrows it to the axial valley is missing. The fault orientation and the fact of a bounding are supported."
        },
        {
          "row_index": 333,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the short ridge segment among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 334,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 places the short ridge segment immediately south of the first non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 335,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 names the segment lying south of the second non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 336,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the studied ridge portion is offset by two non-transform discontinuities, the first of which it names, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 337,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the studied ridge portion is offset by two non-transform discontinuities, the second of which it names, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 338,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:3:block:002 places an extinct hydrothermal vent field on the eastern flank of the first non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 339,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 describes the first non-transform discontinuity as characterised by a large set of faults with the strikes the source endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 340,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 describes the second non-transform discontinuity as having large areas affected by normal faults with the strikes the source endpoint names, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 341,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 places the short ridge segment immediately south of the first non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 342,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 names the segment lying south of the second non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 343,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the studied ridge portion is offset by two non-transform discontinuities, the first of which it names, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 344,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the studied ridge portion is offset by two non-transform discontinuities, the second of which it names, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 345,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:3:block:002 places an extinct hydrothermal vent field on the eastern flank of the first non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 346,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the first non-transform discontinuity among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 347,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the second non-transform discontinuity among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 348,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 places the oceanic core complex on the eastern side of the ridge-transform-intersection segment axis, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 349,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the ridge-transform-intersection segment among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 350,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the short ridge segment among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 351,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:007 places the oceanic core complex on the outside corner of the ridge, in figure-caption text, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 352,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the first non-transform discontinuity among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 353,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the second non-transform discontinuity among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 354,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the first non-transform discontinuity among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 355,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the second non-transform discontinuity among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 356,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 places the oceanic core complex on the eastern side of the ridge-transform-intersection segment axis, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 357,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:007 places the oceanic core complex on the outside corner of the ridge, in figure-caption text, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 358,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 places the oceanic core complex on the eastern side of the ridge-transform-intersection segment axis, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 359,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:007 places the oceanic core complex on the outside corner of the ridge, in figure-caption text, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 360,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the ridge-transform-intersection segment is bounded on its eastern side by a westward dipping detachment fault, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 361,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The sentence carrying this bounding runs across a page break: its opening in page:3:block:001 attaches the bounding to the ten-kilometre-wide axial valley at the short ridge segment, and page:4:block:001 carries the rest. The row asserts the relation of the segment itself, so the qualifier that narrows it to the axial valley is missing. The fault orientation and the fact of a bounding are supported."
        },
        {
          "row_index": 362,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the ridge-transform-intersection segment is bounded on its eastern side by a westward dipping detachment fault, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 363,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the ridge-transform-intersection segment among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 364,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The sentence carrying this bounding runs across a page break: its opening in page:3:block:001 attaches the bounding to the ten-kilometre-wide axial valley at the short ridge segment, and page:4:block:001 carries the rest. The row asserts the relation of the segment itself, so the qualifier that narrows it to the axial valley is missing. The fault orientation and the fact of a bounding are supported."
        },
        {
          "row_index": 365,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the short ridge segment among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 366,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 places the short ridge segment immediately south of the first non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 367,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 names the segment lying south of the second non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 368,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the studied ridge portion is offset by two non-transform discontinuities, the first of which it names, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 369,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the studied ridge portion is offset by two non-transform discontinuities, the second of which it names, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 370,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:2:block:001 places the short ridge segment immediately south of the first non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 371,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 names the segment lying south of the second non-transform discontinuity, which is what the row's relation type and spatial qualifier reports and the extent of what it reports."
        },
        {
          "row_index": 372,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the studied ridge portion is offset by two non-transform discontinuities, the first of which it names, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 373,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 says the studied ridge portion is offset by two non-transform discontinuities, the second of which it names, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 374,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the ridge-transform-intersection segment among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 375,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The reading at page:1:block:005 lists the short ridge segment among the four subsections of the studied ridge portion, which is what the row's relation type reports and the extent of what it reports."
        },
        {
          "row_index": 376,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 377,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 378,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 379,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 380,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports as a calculated result what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 381,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:001 and page:5:block:002 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 382,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 383,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:001 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 384,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 385,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 386,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 387,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 388,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 389,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 390,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:002 and page:5:block:001 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 391,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:003 puts forward as a candidate explanation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 392,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 393,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:007 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 394,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 395,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 396,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 397,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 398,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 399,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 400,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The sentence begins at the end of page:3:block:001, where the absence of detachment-fault evidence is attached to the ten-kilometre-wide axial valley at the segment, and continues into page:4:block:001, which read alone appears to attach it to the segment as a whole. The row states it of the segment and drops that qualifier. The negative finding itself is in the reading."
        },
        {
          "row_index": 401,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 402,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 403,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 404,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 405,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 406,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 407,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 408,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports as a calculated result what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 409,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 410,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:010 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 411,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 412,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose. The subject record is formalized in the same block."
        },
        {
          "row_index": 413,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports as a calculated result what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 414,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 415,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:004 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 416,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:010 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 417,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:001 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 418,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 419,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 420,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:001",
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The sentence begins at the end of page:3:block:001, where the absence of detachment-fault evidence is attached to the ten-kilometre-wide axial valley at the segment, and continues into page:4:block:001, which read alone appears to attach it to the segment as a whole. The row states it of the segment and drops that qualifier. The negative finding itself is in the reading."
        },
        {
          "row_index": 421,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 422,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 423,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 424,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 425,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:003 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 426,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose. The subject record is formalized in the same block."
        },
        {
          "row_index": 427,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:007 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 428,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 records as a negative finding what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 429,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 asserts what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 430,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:003 and page:6:block:005 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 431,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:003 and page:6:block:005 gives this count and the scope the row projects for it, and the assertion the record locates recomputes to the digest it carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 432,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 433,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 434,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 435,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 436,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:003 and page:6:block:005 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 437,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 438,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:004 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 439,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 440,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 441,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 442,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 443,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 444,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 445,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 446,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 447,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 448,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 449,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 450,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 451,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 452,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 453,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 454,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports the age the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 455,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the age the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 456,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 and page:7:block:011 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 457,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:003 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 458,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:012 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose. The subject record is formalized in the same block."
        },
        {
          "row_index": 459,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 460,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 461,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 462,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 463,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:002 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 464,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:010 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose. The subject record is formalized in the same block."
        },
        {
          "row_index": 465,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 466,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:005 reports the rate the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 467,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 468,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 469,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 470,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 471,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:007 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 472,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 473,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 474,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 475,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 476,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 477,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 478,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 479,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 480,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 481,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:004 reports the figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 482,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 483,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 484,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:004 reports the figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 485,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 486,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 487,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 488,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 489,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 490,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 491,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 492,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 493,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:007 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 494,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:006 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose. The subject record is formalized in the same block."
        },
        {
          "row_index": 495,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 496,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 497,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:009 reports the age the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 498,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 499,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:004 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 500,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 501,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 502,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 503,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:010 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose. The subject record is formalized in the same block."
        },
        {
          "row_index": 504,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 505,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:6:block:001 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 506,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 507,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 508,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 509,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 510,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 511,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 512,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 513,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 514,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:006 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose. The subject record is formalized in the same block."
        },
        {
          "row_index": 515,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 516,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 517,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 518,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 519,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 520,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 521,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:006 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 522,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 523,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 524,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:8:block:007 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 525,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 526,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:005 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 527,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:4:block:003 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 528,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 529,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:007 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 530,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 531,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:004 reports the figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 532,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:006 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 533,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 534,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:004 reports the figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 535,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 536,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:001 reports the orientation figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 537,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:005 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 538,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:3:block:001 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 539,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:007 reports the temperature the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 540,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:003 and page:6:block:005 reports as an observation what the row's name reports, at the modality the row projects, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 541,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:004 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 542,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:7:block:012 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The supporting sentence is figure-caption or legend text inside that block rather than body prose. The subject record is formalized in the same block."
        },
        {
          "row_index": 543,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 544,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:1:block:005 reports the rate the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 545,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:5:block:009 reports the concentration the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        },
        {
          "row_index": 546,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The reading at page:2:block:002 reports the length, depth or thickness figure the row projects for the subject the row names, with the same bound, unit and qualification, and the located assertion recomputes to the digest the record carries. The subject record is formalized in the same block."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The question asks for the earthquake-depth range and the calculated primary-melt CO2 range of the central association, with units and estimate status. The returned rows carry both. The depth range beneath the RC2 axis appears as a measured observation with its unit and its subject, and again as the narrower range reported in the results and as the below-sea-floor range in the figure interpretation; the absence of events deeper than the upper bound is returned as its own negative observation. The calculated CO2 range of the primary melts along RC2 appears with its unit, marked calculated and estimated, both as the compared figure against the southern segment and as the two separate estimates from the Ba and Rb proxies, together with the minimum the authors draw from them, and the pre-eruptive figures are returned separately and labelled as such, so the two are not conflated. The depth and CO2 rows each carry a unit slot, a subject or a subject-bearing reference, and a modality, most of them a determination as well, saying whether the figure was measured, calculated, estimated or modelled; the handful of quantity rows elsewhere in the set that carry no unit are the dimensionless ones, such as the b values and the ratio tests. Between them these slots cover the four semantics the question asks for. The rows also bind both quantities to the same segment, and the claim rows that link the deep earthquakes to CO2 degassing are returned with the preferred-hypothesis marking, so the association the question calls central is present rather than left to inference. The set is much wider than the question needs, since the binding is type-only and returns every record of the case types, but breadth is not unresponsiveness: every requested part is directly addressed.",
      "source_locators": [
        "page:1:block:001",
        "page:2:block:004",
        "page:2:block:006",
        "page:5:block:005",
        "page:5:block:007",
        "page:7:block:012",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block presents it as a result of the measurements, which matches the row.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, axial valley, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, OCC termination, occurs in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block presents it as an expectation or a calculated result, which matches the row. The subject the row references, BDB, occurs in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a negative finding, which matches the row. The subject the row references, OBSs, occurs in that block.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the second cited block is where the authors call this their preferred possibility, which is what the row records. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, crust, occurs in that block.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block presents it as a result of the measurements, which matches the row. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:8:block:001"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as activity state of a fault; the block frames it as a negative finding, which matches the row. The subject the row references, detachment fault, occurs in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, Romanche TF, occurs in that block.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the same block also carries the authors turning this candidate down, which is what the row records. The subject the row references, lithosphere, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the same block also carries the authors turning this candidate down, which is what the row records. The subject the row references, lithosphere, occurs in that block.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the same block also carries the authors turning this candidate down, which is what the row records. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:4:block:002",
            "page:5:block:001"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the same block also carries the authors turning this candidate down, which is what the row records. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as accretion character of a ridge segment; the block states it plainly, which matches the row. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a negative finding, which matches the row. The block clips the last word of the phrase at its boundary, which does not change what is being claimed. The subject the row references, MAR, occurs in that block.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, OBSs, occurs in that block.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, LAB, occurs in that block.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, lithosphere, occurs in that block.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, BDB, occurs in that block.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, crust, occurs in that block.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:1:block:003"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:5:block:008"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a negative finding, which matches the row. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a negative finding, which matches the row. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a negative finding, which matches the row.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a negative finding, which matches the row. The subject the row references, MAR, occurs in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as origin of a ridge subsection; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:5:block:008"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, OCC dome, occurs in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, surface of this OCC, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, crust, occurs in that block.",
          "source_locators": [
            "page:5:block:001"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as accretion character of a ridge segment; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as origin of a ridge subsection; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as origin of a ridge segment; the block states it plainly, which matches the row. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as accretion character of a ridge segment; the block states it plainly, which matches the row. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block presents it as an expectation or a calculated result, which matches the row. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as accretion character of a ridge segment; the block states it plainly, which matches the row. The subject the row references, RC3, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block presents it as an expectation or a calculated result, which matches the row.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a hypothesis, which matches the row.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:5:block:002"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, LAB, occurs in that block.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:7:block:003"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject the row references, RTI, occurs in that block.",
          "source_locators": [
            "page:3:block:005"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the count this record carries and says what is being counted; the scope the row names is the one the prose gives. The subject the row references, RTI, occurs in that block.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the count this record carries and says what is being counted; the scope the row names is the one the prose gives. The subject the row references, OBSs, occurs in that block.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the count this record carries and says what is being counted; the scope the row names is the one the prose gives. The subject the row references, OBSs, occurs in that block.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the count this record carries and says what is being counted; the scope the row names is the one the prose gives. The subject the row references, 360-earthquakes sub-dataset, occurs in that block.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the count this record carries and says what is being counted; the scope the row names is the one the prose gives. The subject the row references, subset of 45 events, occurs in that block.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the count this record carries and says what is being counted; the scope the row names is the one the prose gives.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:6:block:005"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, and the remaining fields it carries (access_url) are borne out by the same prose.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:5:block:002"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:5:block:006",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 113,
          "source_support": "PARTIAL",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The blocks this row's derivation reaches name these melts as the primary melts of the segment and give the CO2 estimated for them, so the first half of the row's name holds. The qualifier that they are in equilibrium with their mantle source is not worded in either block; one of them speaks instead of equilibrium with an olivine composition, and the definition of a primary melt as being in equilibrium with the mantle source sits in a block this derivation does not reach.",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 114,
          "source_support": "PARTIAL",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The blocks this row's derivation reaches name these melts as the primary melts of the segment and give the CO2 estimated for them, so the first half of the row's name holds. The qualifier that they are in equilibrium with their mantle source is not worded in either block; one of them speaks instead of equilibrium with an olivine composition, and the definition of a primary melt as being in equilibrium with the mantle source sits in a block this derivation does not reach.",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block gives the magnitude scale by name, prints the formula the row's description reproduces, and defines the amplitude and the hypocentral distance that formula uses; the description also says openly that the formula is carried as the text layer renders it, which is what the block holds.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:7:block:004"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:6:block:003",
            "page:6:block:004"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports. The subject the row references, RTI, occurs in that block.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports. The subject the row references, OBSs, occurs in that block.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports. The subject the row references, OBSs, occurs in that block.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports. The subject the row references, 360-earthquakes sub-dataset, occurs in that block.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports. The subject the row references, subset of 45 events, occurs in that block.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as something measured.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records a numeric value without a unit slot and gives a single value; the row carries the same figures and presents them as a calculated figure.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states a numeric value without a unit slot and gives the two bounds of a range; the row carries the same figures and presents them as a calculated figure.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a length or depth in km and gives a single value; the row carries the same figures and presents them as a measurement. The subject the row references, BDB, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a temperature in \u00b0C and gives a value with its stated uncertainty; the row carries the same figures and presents them as a plain statement. The subject the row references, BDB, occurs in that block.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a temperature in \u00b0C and gives the two bounds of a range; the row carries the same figures and presents them inside a hypothesis it is putting forward. The subject the row references, BDB, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement. The subject the row references, BDB, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a calculated figure.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC3, occurs in that block.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC3, occurs in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records a concentration in % and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC3, occurs in that block.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC3, occurs in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a concentration in wt% and gives a lower bound; the row carries the same figures and presents them as an estimate. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject the row references, RC3, occurs in that block.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a length or depth in km and gives a single value; the row carries the same figures and presents them inside a hypothesis it is putting forward. The subject the row references, BDB, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out an age in Ma and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, lithosphere, occurs in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a dimensionless quantity in % and gives a single value; the row carries the same figures and presents them as a measurement.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records a count without a unit slot and gives a lower bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states an orientation or angular gap in \u00b0 and gives an upper bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives a numeric value without a unit slot and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries an age in Ma and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, crust, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a length or depth in km and gives a value with its stated uncertainty; the row carries the same figures and presents them as a measurement. The subject the row references, crust, occurs in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 178,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports an orientation or angular gap in \u00b0 and gives a single value; the row carries the same figures and presents them as a measurement. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 179,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a measurement. The subject the row references, MAR, occurs in that block.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 180,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a measurement. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 181,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 182,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries a length or depth in km and gives a single value; the row carries the same figures and presents them as a measurement.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 183,
          "source_support": "PARTIAL",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block opens mid-sentence, with a bare bound whose subject was left in the preceding block, so the ten-kilometre limit is there but nothing in this block says it is the depth uncertainty. The bound is supported; the identity of the quantity it bounds is not, on this block alone.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 184,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 185,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a concentration in ppm and gives a single value; the row carries the same figures and presents them as an estimate. The subject the row references, equatorial Atlantic Ocean, occurs in that block.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 186,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a concentration in ppm and gives a single value; the row carries the same figures and presents them as an estimate. The subject the row references, equatorial Atlantic Ocean, occurs in that block.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 187,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a dimensionless quantity in % and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, NonLinLoc, occurs in that block.",
          "source_locators": [
            "page:7:block:005"
          ]
        },
        {
          "row_index": 188,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a modelled figure.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 189,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a modelled figure.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 190,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a modelled figure.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 191,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records an orientation or angular gap in \u00b0 and gives an upper bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 192,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states a dimensionless quantity in % and gives an upper bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 193,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives a count without a unit slot and gives a lower bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 194,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries a dimensionless quantity in % and gives a lower bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 195,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a rate in mm/yr and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 196,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a temperature in \u00b0C and gives a lower bound; the row carries the same figures and presents them as a plain statement. The subject the row references, mantle, occurs in that block.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 197,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records a length or depth in km and gives a lower bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 198,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 199,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a temperature in \u00b0C and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, 750 \u00b0C isotherm, occurs in that block.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 200,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries an age in Ma and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 201,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a frequency in Hz and gives a lower bound; the row carries the same figures and presents them as a measurement.",
          "source_locators": [
            "page:5:block:008"
          ]
        },
        {
          "row_index": 202,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a numeric value without a unit slot and gives a single value; the row carries the same figures and presents them as a calculated figure.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 203,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, MAR, occurs in that block.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 204,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a rate in mm/yr and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, MAR, occurs in that block.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 205,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 206,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a length or depth in km and gives a lower bound; the row carries the same figures and presents them as a plain statement. The subject the row references, Mayotte Island, occurs in that block.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 207,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a length or depth in km and gives a single value; the row carries the same figures and presents them as a measurement. The block leaves whose values these are to a pronoun whose antecedent is in the preceding block; the quantity itself is named here.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 208,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a length or depth in km and gives a single value; the row carries the same figures and presents them as a measurement. The block leaves whose values these are to a pronoun whose antecedent is in the preceding block; the quantity itself is named here.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 209,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, median valley, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 210,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a concentration in % and gives a single value; the row carries the same figures and presents them as a modelled figure. The subject the row references, LAB, occurs in that block.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 211,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a rate in km/s and gives a lower bound; the row carries the same figures and presents them as a plain statement. The subject the row references, Model 1, occurs in that block.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 212,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries an orientation or angular gap in \u00b0 and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, neo-volcanic ridge, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 213,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a length or depth in km and gives a lower bound; the row carries the same figures and presents them inside a negative finding. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 214,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, NTD1, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 215,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records an orientation or angular gap in \u00b0 and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, NTD1, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 216,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement. The subject the row references, NTD2, occurs in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 217,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a measurement. The subject the row references, NTD2, occurs in that block.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 218,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement. The subject the row references, NTD2, occurs in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 219,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, NTD2, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 220,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports an orientation or angular gap in \u00b0 and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, NTD2, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 221,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement. The subject the row references, OCC, occurs in that block.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 222,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 223,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement.",
          "source_locators": [
            "page:5:block:001"
          ]
        },
        {
          "row_index": 224,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries a pressure in bars and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 225,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:3:block:005"
          ]
        },
        {
          "row_index": 226,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:3:block:004"
          ]
        },
        {
          "row_index": 227,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:3:block:004"
          ]
        },
        {
          "row_index": 228,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a dimensionless quantity in ppm and gives a lower bound; the row carries the same figures and presents them as a measurement. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 229,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a measurement. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 230,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 231,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a dimensionless quantity in ppm and gives a lower bound; the row carries the same figures and presents them as a measurement. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 232,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, RC3, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 233,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records an orientation or angular gap in \u00b0 and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, RC3, occurs in that block.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 234,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 235,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives an age in s and gives an upper bound; the row carries the same figures and presents them as a measurement.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 236,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries a length or depth in km and gives a single value; the row carries the same figures and presents them as a measurement. The located block gives the figure as a legend entry; the second cited block names it as the average horizontal uncertainty after relocation.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 237,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 238,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports an age in s and gives an upper bound; the row carries the same figures and presents them as a measurement. The block leaves whose values these are to a pronoun whose antecedent is in the preceding block; the quantity itself is named here.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 239,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, MAR segment, occurs in that block.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 240,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, Romanche TF, occurs in that block.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 241,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives a length or depth in km and gives a single value; the row carries the same figures and presents them as a modelled figure.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 242,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries a pressure in GPa and gives a single value; the row carries the same figures and presents them as a modelled figure.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 243,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a temperature in \u00b0C and gives a single value; the row carries the same figures and presents them as a modelled figure.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 244,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:4:block:007"
          ]
        },
        {
          "row_index": 245,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a measurement. The subject the row references, RTI, occurs in that block.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 246,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a temperature in \u00b0C and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, anhydrous peridotite, occurs in that block.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 247,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives a temperature in \u00b0C and gives a single value; the row carries the same figures and presents them as a modelled figure.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 248,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 249,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 250,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports an orientation or angular gap in \u00b0 and gives an upper bound; the row carries the same figures and presents them as a plain statement. The subject the row references, 360-earthquakes sub-dataset, occurs in that block.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 251,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a concentration in wt% and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, SWIR, occurs in that block.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 252,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a temperature in \u00b0C and gives the two bounds of a range; the row carries the same figures and presents them as a modelled figure. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 253,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a temperature in \u00b0C and gives a lower bound; the row carries the same figures and presents them as a modelled figure. The subject the row references, RC2, occurs in that block.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 254,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject the row references, OCC, occurs in that block.",
          "source_locators": [
            "page:4:block:006"
          ]
        },
        {
          "row_index": 255,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out a rate in km/s and gives a single value; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 256,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 257,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records a numeric value without a unit slot and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 258,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a concentration in ppm and gives an upper bound; the row carries the same figures and presents them as a calculated figure. The subject the row references, LAB, occurs in that block.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 259,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a measurement. The subject the row references, axial valley, occurs in that block.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 260,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries an age in Ma and gives an upper bound; the row carries the same figures and presents them as a plain statement. The subject the row references, crust, occurs in that block.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 261,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out this record under the name the row projects, and the remaining fields it carries (numerator_kind, denominator_kind, ratio_value, uncertainty) are borne out by the same prose.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 262,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports this record under the name the row projects, and the remaining fields it carries (numerator_kind, denominator_kind, ratio_value, uncertainty) are borne out by the same prose.",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 263,
          "source_support": "PARTIAL",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block gives this ratio and attributes it to the Wadati diagrams, exactly as the row's name does, but it gives the number as an approximation. The row carries the bare number and the Ratio projection has no slot for an approximation marker, so the row asserts the value more tightly than the prose does.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 264,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 265,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 266,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries this record under the name the row projects, and the remaining fields it carries (description) are borne out by the same prose.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 267,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 268,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 269,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 270,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 271,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, and the remaining fields it carries (sample_material) are borne out by the same prose.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 272,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries this record under the name the row projects, and the remaining fields it carries (sample_material) are borne out by the same prose.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 273,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The passage sets out this record under the name the row projects, and the remaining fields it carries (sample_material) are borne out by the same prose.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 274,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block reports this record under the name the row projects, and the remaining fields it carries (sample_material) are borne out by the same prose.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 275,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block records this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 276,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block states this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 277,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited prose gives this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 278,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The block carries this record under the name the row projects, which is the only field the row carries.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 279,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The block's sentence places the lithosphere over the crust, which is the relation and the spatial qualifier the row carries, and it names both endpoints. That sentence frames the ordering for fast- and intermediate-spreading ridges, a setting the row does not restate, but the ordering itself is what the row asserts.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 280,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same sentence places the lithosphere over the mantle beneath it, which is the relation and the qualifier the row carries, and both endpoints are named in it.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 281,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The block lists the subsections of the studied ridge portion and names this one among them, which is the part-of relation the row asserts; both endpoints and their descriptions are worded there.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 282,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The block's subdivision sentence names this segment as one of the four subsections of the studied portion, which is the relation the row asserts, and it words both endpoint descriptions.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 283,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The figure caption in the block ties these MORB samples to the segment they were taken along, which is the sampling relation the row asserts; the second cited block is where the samples are described as published analyses of mid-ocean ridge basalts.",
          "source_locators": [
            "page:6:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 284,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same caption ties the other set of MORB samples to its segment, giving the sampling relation the row asserts, with the sample material worded in the second cited block.",
          "source_locators": [
            "page:6:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 285,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL Same caption, same sampling relation, with this projection dropping the sample material; the caption names both endpoints.",
          "source_locators": [
            "page:6:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 286,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL Same caption again for the southern segment, with the sample material dropped from this projection; the relation and both endpoints are in the prose.",
          "source_locators": [
            "page:6:block:005",
            "page:5:block:004"
          ]
        },
        {
          "row_index": 287,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block presents it as an expectation or a calculated result, which matches the row. The subject record is formalised by the same block and its name, BDB, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:2:block:006",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 288,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, LAB, is written in that prose; the description the row gives for that subject is worded in page:5:block:010.",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ]
        },
        {
          "row_index": 289,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, BDB, is written in that prose; the description the row gives for that subject is worded there too.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 290,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, LAB, is written in that prose; the description the row gives for that subject is worded there too.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 291,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the second cited block is where the authors call this their preferred possibility, which is what the row records. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 292,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, crust, is written in that prose; the description the row gives for that subject is worded there too.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 293,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 294,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 295,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the same block also carries the authors turning this candidate down, which is what the row records. The subject record is formalised by the same block and its name, lithosphere, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 296,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the same block also carries the authors turning this candidate down, which is what the row records. The subject record is formalised by the same block and its name, lithosphere, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 297,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the same block also carries the authors turning this candidate down, which is what the row records. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:4:block:002",
            "page:5:block:001"
          ]
        },
        {
          "row_index": 298,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as candidate explanation for the deep earthquakes; the block frames it as a hypothesis, which matches the row; the same block also carries the authors turning this candidate down, which is what the row records. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 299,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, lithosphere, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:6:block:001",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 300,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, crust, is written in that prose; the description the row gives for that subject is worded in page:1:block:002.",
          "source_locators": [
            "page:4:block:002",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 301,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 302,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, crust, is written in that prose; the description the row gives for that subject is worded in page:1:block:002.",
          "source_locators": [
            "page:5:block:001",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 303,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block presents it as an expectation or a calculated result, which matches the row. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 304,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block presents it as a result of the measurements, which matches the row. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:8:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 305,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as accretion character of a ridge segment; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 306,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a negative finding, which matches the row. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:3:block:002",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 307,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block frames it as a negative finding, which matches the row. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:4:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 308,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:5:block:003",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 309,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as origin of a ridge segment; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 310,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as accretion character of a ridge segment; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 311,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the row types it as accretion character of a ridge segment; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, RC3, is written in that prose.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 312,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states the sentence this claim record formalises, and the row's wording adds nothing the prose does not carry; the block states it plainly, which matches the row. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:7:block:003",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 313,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives the count this record carries and says what is being counted; the scope the row names is the one the prose gives. The subject record is formalised by the same block and its name, 360-earthquakes sub-dataset, is written in that prose.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 314,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries the count this record carries and says what is being counted; the scope the row names is the one the prose gives. The subject record is formalised by the same block and its name, subset of 45 events, is written in that prose; the description the row gives for that subject is worded there too.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 315,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports. The subject record is formalised by the same block and its name, 360-earthquakes sub-dataset, is written in that prose.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 316,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports the count this record carries and says what is being counted; this projection drops the count slot and keeps the naming, which the block also supports. The subject record is formalised by the same block and its name, subset of 45 events, is written in that prose; the description the row gives for that subject is worded there too.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 317,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records an orientation or angular gap in \u00b0 and gives an upper bound; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, 360-earthquakes sub-dataset, is written in that prose.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 318,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a length or depth in km and gives a single value; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, BDB, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 319,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a temperature in \u00b0C and gives a value with its stated uncertainty; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, BDB, is written in that prose; the description the row gives for that subject is worded there too.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 320,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a temperature in \u00b0C and gives the two bounds of a range; the row carries the same figures and presents them inside a hypothesis it is putting forward. The subject record is formalised by the same block and its name, BDB, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 321,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, BDB, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 322,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a length or depth in km and gives a single value; the row carries the same figures and presents them inside a hypothesis it is putting forward. The subject record is formalised by the same block and its name, BDB, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 323,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a temperature in \u00b0C and gives a single value; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, 750 \u00b0C isotherm, is written in that prose.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 324,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a concentration in % and gives a single value; the row carries the same figures and presents them as a modelled figure. The subject record is formalised by the same block and its name, LAB, is written in that prose; the description the row gives for that subject is worded in page:5:block:010.",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ]
        },
        {
          "row_index": 325,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a concentration in ppm and gives an upper bound; the row carries the same figures and presents them as a calculated figure. The subject record is formalised by the same block and its name, LAB, is written in that prose; the description the row gives for that subject is worded in page:5:block:010.",
          "source_locators": [
            "page:6:block:001",
            "page:5:block:010"
          ]
        },
        {
          "row_index": 326,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries an age in Ma and gives a single value; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, lithosphere, is written in that prose; the description the row gives for that subject is worded in page:1:block:004.",
          "source_locators": [
            "page:2:block:006",
            "page:1:block:004"
          ]
        },
        {
          "row_index": 327,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out an age in Ma and gives a single value; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, crust, is written in that prose; the description the row gives for that subject is worded in page:1:block:002.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 328,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a length or depth in km and gives a value with its stated uncertainty; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, crust, is written in that prose; the description the row gives for that subject is worded in page:1:block:002.",
          "source_locators": [
            "page:2:block:006",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 329,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 330,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a temperature in \u00b0C and gives a lower bound; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, mantle, is written in that prose.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 331,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a temperature in \u00b0C and gives a single value; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, anhydrous peridotite, is written in that prose; the description the row gives for that subject is carried by the prose of the cited blocks.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 332,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries an age in Ma and gives an upper bound; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, crust, is written in that prose; the description the row gives for that subject is worded in page:1:block:002.",
          "source_locators": [
            "page:7:block:009",
            "page:1:block:002"
          ]
        },
        {
          "row_index": 333,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a rate in km/s and gives a lower bound; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, Model 1, is written in that prose; the description the row gives for that subject is carried by the prose of the cited blocks.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 334,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:8:block:006",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 335,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC3, is written in that prose.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 336,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:8:block:007",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 337,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC3, is written in that prose.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 338,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:5:block:006",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 339,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:8:block:006",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 340,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC3, is written in that prose.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 341,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:8:block:007",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 342,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC3, is written in that prose.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 343,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a concentration in wt% and gives a lower bound; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:8:block:007",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 344,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:5:block:005",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 345,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a concentration in wt% and gives the two bounds of a range; the row carries the same figures and presents them as an estimate. The subject record is formalised by the same block and its name, RC3, is written in that prose.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 346,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports an orientation or angular gap in \u00b0 and gives a single value; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:4:block:003",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 347,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 348,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a length or depth in km and gives a lower bound; the row carries the same figures and presents them inside a negative finding. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:5:block:007",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 349,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives a length or depth in km and gives an upper bound; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 350,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a dimensionless quantity in ppm and gives a lower bound; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:5:block:004",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 351,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a length or depth in km and gives the two bounds of a range; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:2:block:006",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 352,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 353,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block records a dimensionless quantity in ppm and gives a lower bound; the row carries the same figures and presents them as a measurement. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:5:block:004",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 354,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block states a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, RC3, is written in that prose.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 355,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited prose gives an orientation or angular gap in \u00b0 and gives a single value; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, RC3, is written in that prose.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 356,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block carries a length or depth in km and gives a single value; the row carries the same figures and presents them as a plain statement. The subject record is formalised by the same block and its name, MAR segment, is written in that prose; the description the row gives for that subject is worded there too.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 357,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The passage sets out a temperature in \u00b0C and gives the two bounds of a range; the row carries the same figures and presents them as a modelled figure. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:3:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 358,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block reports a temperature in \u00b0C and gives a lower bound; the row carries the same figures and presents them as a modelled figure. The subject record is formalised by the same block and its name, RC2, is written in that prose; the description the row gives for that subject is worded in page:1:block:005.",
          "source_locators": [
            "page:5:block:007",
            "page:1:block:005"
          ]
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows do reach the mechanism the question asks about and they do mark it as a hypothesis: one claim ties the deep mantle earthquakes to CO2 coming out of solution in the melt, carries a hypothesised modality, and is marked as the authors' preferred candidate, while the three rival explanations offered in the discussion carry the same modality and a not-supported disposition. Ascending melt, the volume change, the pressure increase, the extensional stress the mechanism needs, and the triggering of the earthquakes are all reachable in the returned rows, mostly inside one claim about the degassing step and one observation about how small a pore-pressure rise suffices. What keeps this short of fully responsive is that the epistemic status the question asks for is carried unevenly. The claim naming the pressure increase as the cause of the earthquakes observed beneath the segment is recorded as a plain statement with the authors' explicit first-person hedge dropped, and the claim spelling out volume change under extensional stress is likewise a plain statement; a reader taking the rows at face value sees the same mechanism at two different epistemic weights. Extensional stress is also present only inside the free text of a claim, not as anything the row structure marks on its own. The answer is there and it is findable, but the hypothesis framing the question insists on is not applied to the whole of the mechanism.",
      "source_locators": [
        "page:1:block:001",
        "page:3:block:001",
        "page:3:block:002",
        "page:3:block:003",
        "page:4:block:002",
        "page:5:block:001",
        "page:5:block:002",
        "page:5:block:003",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as an absence or a denial. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the cited blocks, the digest agrees, and the reading makes the point as a hypothesis. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading. The disposition marking this the authors' preferred explanation comes from a second assertion, in the block where they rank the four candidates.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as something measured. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:001"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as an absence or a denial. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a hypothesis. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. The disposition recording that this candidate is not supported comes from a second assertion in the same block, where the authors set it aside.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a hypothesis. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. The disposition recording that this candidate is not supported comes from a second assertion in the same block, where the authors argue the vent field is too far away to matter.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the cited blocks, the digest agrees, and the reading makes the point as a hypothesis. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading. The disposition recording that this candidate is not supported comes from an assertion in a later block, where the authors reject melt movement for these events.",
          "source_locators": [
            "page:4:block:002",
            "page:5:block:001"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a hypothesis. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. The disposition recording that this candidate is not supported comes from a second assertion in the same block, where the authors say the observations do not bear it out.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as an absence or a denial. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. The block breaks off before the last word of the sentence, and the row completes it in the only way the text allows.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:003"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:008"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as an absence or a denial. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as an absence or a denial. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as an absence or a denial. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as an absence or a denial. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:008"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:001"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:005"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 52,
          "source_support": "PARTIAL",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The block does carry the causal step this row records, but it carries it as something the authors put forward rather than assert: the sentence is framed in the first person as their suggestion, and the row drops that framing and labels the modality as plainly stated. The pressure increase, the degassing source and the place the earthquakes are seen are all in the block, so support is present but a qualifier the source insists on is missing.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. The block opens mid-sentence at the page break, so which subsection is meant is not resolvable inside it; the row is no more specific than the block, so it does not overreach.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as something calculated or modelled. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a hypothesis. Nothing in the claim goes beyond what is written there. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:002"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:7:block:003"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:005"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Count and scope both come from the sentence the locator names in the one cited block; the statement digest matches, and the reading states the tally as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The tally and what it ranges over are in the one cited block, the located assertion's digest agrees with the record, and the prose presents the number as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited blocks give the count and the population it counts, either as a figure or spelled out in words, and the digest of the located assertion recomputes to the record's value. The prose reports it as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Count and scope both come from the sentence the locator names in the one cited block; the statement digest matches, and the reading states the tally as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The tally and what it ranges over are in the one cited block, the located assertion's digest agrees with the record, and the prose presents the number as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited blocks give the count and the population it counts, either as a figure or spelled out in words, and the digest of the located assertion recomputes to the record's value. The prose reports it as something measured. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Count and scope both come from the sentence the locator names in the one cited block; the statement digest matches, and the reading states the tally as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The tally and what it ranges over are in the one cited block, the located assertion's digest agrees with the record, and the prose presents the number as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited blocks give the count and the population it counts, either as a figure or spelled out in words, and the digest of the located assertion recomputes to the record's value. The prose reports it as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Count and scope both come from the sentence the locator names in the cited blocks; the statement digest matches, and the reading states the tally as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The tally and what it ranges over are in the one cited block, the located assertion's digest agrees with the record, and the prose presents the number as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives the count and the population it counts, either as a figure or spelled out in words, and the digest of the located assertion recomputes to the record's value. The prose reports it as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Count and scope both come from the sentence the locator names in the one cited block; the statement digest matches, and the reading states the tally as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The tally and what it ranges over are in the cited blocks, the located assertion's digest agrees with the record, and the prose presents the number as something measured. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives the count and the population it counts, either as a figure or spelled out in words, and the digest of the located assertion recomputes to the record's value. The prose reports it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Count and scope both come from the sentence the locator names in the one cited block; the statement digest matches, and the reading states the tally as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The tally and what it ranges over are in the one cited block, the located assertion's digest agrees with the record, and the prose presents the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives the count and the population it counts, either as a figure or spelled out in words, and the digest of the located assertion recomputes to the record's value. The prose reports it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Count and scope both come from the sentence the locator names in the one cited block; the statement digest matches, and the reading states the tally as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block introduces the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the one cited block names it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the cited blocks, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the one cited block names it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block introduces the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the one cited block names it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the one cited block, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the cited blocks name it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:3:block:005",
            "page:5:block:005",
            "page:7:block:007",
            "page:7:block:009"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block introduces the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the one cited block names it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the one cited block, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the cited blocks name it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited blocks introduce the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:5:block:010",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the cited blocks name it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the one cited block, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:011"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the one cited block names it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited blocks introduce the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:002",
            "page:1:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:4:block:002",
            "page:5:block:001",
            "page:6:block:001",
            "page:7:block:009",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the cited blocks name it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the cited blocks, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:3:block:003",
            "page:4:block:002",
            "page:5:block:003",
            "page:5:block:009",
            "page:6:block:001",
            "page:7:block:012"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the cited blocks name it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:5:block:002",
            "page:5:block:003",
            "page:5:block:006",
            "page:5:block:010",
            "page:6:block:001"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited blocks introduce the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:5:block:006",
            "page:8:block:006"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the one cited block names it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the cited blocks, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the cited blocks name it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:5:block:005",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block introduces the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the one cited block names it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the one cited block, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the one cited block names it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block introduces the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the cited blocks name it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:6:block:003",
            "page:6:block:004"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Projected under the observation case, the row carries the quantity and its scope but no tally; the one cited block supports both and the statement digest matches, with the prose presenting it as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the one cited block and the located assertion's digest recomputes correctly. The prose frames it as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Projected under the observation case, the row carries the quantity and its scope but no tally; the cited blocks support both and the statement digest matches, with the prose presenting it as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the one cited block and the located assertion's digest recomputes correctly. The prose frames it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Projected under the observation case, the row carries the quantity and its scope but no tally; the one cited block supports both and the statement digest matches, with the prose presenting it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the cited blocks and the located assertion's digest recomputes correctly. The prose frames it as something measured. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Projected under the observation case, the row carries the quantity and its scope but no tally; the one cited block supports both and the statement digest matches, with the prose presenting it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:6:block:002"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the one cited block and the located assertion's digest recomputes correctly. The prose frames it as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Projected under the observation case, the row carries the quantity and its scope but no tally; the cited blocks support both and the statement digest matches, with the prose presenting it as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the cited blocks and the located assertion's digest recomputes correctly. The prose frames it as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Projected under the observation case, the row carries the quantity and its scope but no tally; the one cited block supports both and the statement digest matches, with the prose presenting it as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the one cited block and the located assertion's digest recomputes correctly. The prose frames it as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Projected under the observation case, the row carries the quantity and its scope but no tally; the one cited block supports both and the statement digest matches, with the prose presenting it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the cited blocks and the located assertion's digest recomputes correctly. The prose frames it as something measured. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Projected under the observation case, the row carries the quantity and its scope but no tally; the one cited block supports both and the statement digest matches, with the prose presenting it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the one cited block and the located assertion's digest recomputes correctly. The prose frames it as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Projected under the observation case, the row carries the quantity and its scope but no tally; the one cited block supports both and the statement digest matches, with the prose presenting it as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW This case projects the record without its count field, so what the row asserts is the quantity and its scope; both are in the one cited block and the located assertion's digest recomputes correctly. The prose frames it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Projected under the observation case, the row carries the quantity and its scope but no tally; the one cited block supports both and the statement digest matches, with the prose presenting it as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a hypothesis. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an upper limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an upper limit only the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and a lower limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a hypothesis. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and a lower limit only are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:008"
          ]
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes. That naming is adjectival rather than the bare noun, so the occurrence token records a reading of the prose rather than a literal word match.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the cited blocks, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in one of them, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 178,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 179,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 180,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an upper limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 181,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 182,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an approximate value are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 183,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 184,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:7:block:005"
          ]
        },
        {
          "row_index": 185,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an upper limit only the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 186,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an upper limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 187,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 188,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an upper limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 189,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an upper limit only the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 190,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and a lower limit only are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 191,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and a lower limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 192,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 193,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and a lower limit only the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 194,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and a lower limit only are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 195,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an approximate value come from the sentence in the cited blocks that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002",
            "page:8:block:003"
          ]
        },
        {
          "row_index": 196,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 197,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 198,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and a lower limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:008"
          ]
        },
        {
          "row_index": 199,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 200,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 201,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 202,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:7:block:007"
          ]
        },
        {
          "row_index": 203,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and a lower limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 204,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 205,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 206,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 207,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 208,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and a lower limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 209,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 210,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and a lower limit only are present as projected, the statement digest recomputes correctly, and the framing there is as an absence or a denial. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 211,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 212,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 213,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an upper limit only the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 214,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 215,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 216,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 217,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 218,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an upper limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 219,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 220,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an upper limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:5:block:001"
          ]
        },
        {
          "row_index": 221,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 222,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:3:block:005"
          ]
        },
        {
          "row_index": 223,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:3:block:004"
          ]
        },
        {
          "row_index": 224,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:3:block:004"
          ]
        },
        {
          "row_index": 225,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and a lower limit only the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 226,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 227,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 228,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and a lower limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 229,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 230,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an approximate value are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 231,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 232,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an upper limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 233,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited blocks give this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ]
        },
        {
          "row_index": 234,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an upper limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:006"
          ]
        },
        {
          "row_index": 235,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:001"
          ]
        },
        {
          "row_index": 236,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 237,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 238,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an approximate value are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 239,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 240,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 241,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:4:block:007"
          ]
        },
        {
          "row_index": 242,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 243,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 244,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 245,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 246,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 247,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 248,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 249,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 250,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and a lower limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 251,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:4:block:006"
          ]
        },
        {
          "row_index": 252,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 253,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 254,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL NO_SUBJECT_IN_ROW Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The projection carries no subject at all, so there is nothing to look for in the block on that axis. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 255,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an upper limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 256,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 257,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an upper limit only the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The row points at its subject by identifier only; the feature that identifier stands for is named in the same block, so the attachment holds on the reading.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 258,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the one cited block names it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 259,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The cited blocks introduce the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 260,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the cited blocks name it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:2:block:004",
            "page:2:block:006",
            "page:3:block:001",
            "page:3:block:002",
            "page:4:block:001",
            "page:4:block:003",
            "page:4:block:007",
            "page:5:block:002",
            "page:5:block:003",
            "page:5:block:004",
            "page:5:block:005",
            "page:5:block:006",
            "page:5:block:007",
            "page:6:block:005",
            "page:7:block:003",
            "page:7:block:010",
            "page:7:block:011",
            "page:8:block:001",
            "page:8:block:006",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 261,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the cited blocks, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001",
            "page:5:block:004",
            "page:5:block:005",
            "page:5:block:006",
            "page:6:block:005",
            "page:8:block:006",
            "page:8:block:007"
          ]
        },
        {
          "row_index": 262,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the one cited block names it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 263,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block introduces the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 264,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the one cited block names it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 265,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the one cited block, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 266,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the cited blocks name it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002",
            "page:3:block:005",
            "page:5:block:005",
            "page:7:block:007",
            "page:7:block:009"
          ]
        },
        {
          "row_index": 267,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The one cited block introduces the feature by that name, and the description repeats what is said about it there. No statement digest is carried by the record, so the digest token is omitted. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 268,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW The row projects only the feature's name and, where present, its description, and the one cited block names it in prose in those terms. The record carries no statement digest, so no digest token applies. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 269,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW Name and description are both drawn from prose in the one cited block, which is all this row asserts. With no assertion locator or statement digest on the record, the digest token does not apply. The projection carries no subject at all, so there is nothing to look for in the block on that axis.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 270,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL NO_SUBJECT_IN_ROW What the row claims is a named feature and its short description, and the cited blocks name it that way. This record carries no statement digest, hence no digest token. The projection carries no subject at all, so there is nothing to look for in them on that axis.",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:001"
          ]
        },
        {
          "row_index": 271,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The one cited block states the arrangement of the two features that this relation records, and every projected field of the relation derives from that one sentence. No statement digest is carried by a relation record, so the digest token is omitted; the endpoints are formalized in the same block.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 272,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL Relation type, its spatial qualifier where present, and both endpoint identifiers all derive from one sentence in the one cited block, which places the two features in that arrangement. A relation record carries no statement digest, so no digest token applies, and the block that formalizes the relation is also among the blocks that formalize its endpoints.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 273,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The one cited block states the arrangement of the two features that this relation records, and every projected field of the relation derives from that one sentence. No statement digest is carried by a relation record, so the digest token is omitted; the endpoints are formalized in the same block.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 274,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL Relation type, its spatial qualifier where present, and both endpoint identifiers all derive from one sentence in the one cited block, which places the two features in that arrangement. A relation record carries no statement digest, so no digest token applies, and the block that formalizes the relation is also among the blocks that formalize its endpoints.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 275,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The one cited block states the arrangement of the two features that this relation records, and every projected field of the relation derives from that one sentence. No statement digest is carried by a relation record, so the digest token is omitted; the endpoints are formalized in the same block.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 276,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL Relation type, its spatial qualifier where present, and both endpoint identifiers all derive from one sentence in the one cited block, which places the two features in that arrangement. A relation record carries no statement digest, so no digest token applies, and the block that formalizes the relation is also among the blocks that formalize its endpoints.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 277,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as an absence or a denial. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 278,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 279,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 280,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 281,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 282,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 283,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited blocks hold the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a hypothesis. The subject record projected beside it is named in one of them, so the attachment is visible on the reading and not only in the graph. The disposition marking this the authors' preferred explanation comes from a second assertion, in the block where they rank the four candidates.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ]
        },
        {
          "row_index": 284,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 285,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 286,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 287,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a hypothesis. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. The disposition recording that this candidate is not supported comes from a second assertion in the same block, where the authors set it aside.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 288,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a hypothesis. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. The disposition recording that this candidate is not supported comes from a second assertion in the same block, where the authors argue the vent field is too far away to matter.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 289,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the cited blocks; the digest recomputes to the value the record carries. Read there, the point is made as a hypothesis. The subject record projected beside it is named in one of them, so the attachment is visible on the reading and not only in the graph. The disposition recording that this candidate is not supported comes from an assertion in a later block, where the authors reject melt movement for these events.",
          "source_locators": [
            "page:4:block:002",
            "page:5:block:001"
          ]
        },
        {
          "row_index": 290,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a hypothesis. Nothing in the claim goes beyond what is written there. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. The disposition recording that this candidate is not supported comes from a second assertion in the same block, where the authors say the observations do not bear it out.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 291,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 292,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 293,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 294,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:001"
          ]
        },
        {
          "row_index": 295,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 296,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:001"
          ]
        },
        {
          "row_index": 297,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 298,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as an absence or a denial. Nothing in the claim goes beyond what is written there. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 299,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as an absence or a denial. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 300,
          "source_support": "PARTIAL",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Same reading as the entity row for this record, now with the ridge segment attached as subject: the block places the causal step inside an explicit first-person suggestion, and the row records it flatly with a stated modality. The mechanism and its location are supported; the epistemic framing the source gives it is not carried. The subject record projected beside it is named in the same block.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 301,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 302,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The claim traces to an assertion in the one cited block, the digest agrees, and the reading makes the point as a plain statement. Nothing in the claim goes beyond what is written there. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 303,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block holds the assertion the record points at, its digest recomputes correctly, and the prose puts the matter as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 304,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block carries the sentence this claim formalizes, and the recomputed digest of the located assertion matches the record, so the wording behind the claim is the wording in the reading. The block presents the point as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:7:block:003"
          ]
        },
        {
          "row_index": 305,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The fields of this claim derive from an assertion whose statement sits in the one cited block; the digest recomputes to the value the record carries. Read there, the point is made as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 306,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 307,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 308,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 309,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a hypothesis. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 310,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an upper limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 311,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a hypothesis. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 312,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 313,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 314,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an upper limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 315,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 316,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes. That naming is adjectival rather than the bare noun, so the occurrence token records a reading of the prose rather than a literal word match.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 317,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The cited blocks give this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something measured. The subject record projected beside it is named in one of them, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 318,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 319,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and a lower limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 320,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 321,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an upper limit only the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 322,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and a lower limit only are present as projected, the statement digest recomputes correctly, and the framing there is as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:7:block:009"
          ]
        },
        {
          "row_index": 323,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 324,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 325,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 326,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 327,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 328,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 329,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:006"
          ]
        },
        {
          "row_index": 330,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 331,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 332,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and a lower limit only are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:8:block:007"
          ]
        },
        {
          "row_index": 333,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 334,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 335,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an approximate value come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 336,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 337,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and a lower limit only the record projects; the located assertion's digest matches, and the reading frames the number as an absence or a denial. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 338,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an upper limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 339,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and a lower limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 340,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 341,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 342,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and a lower limit only are present as projected, the statement digest recomputes correctly, and the framing there is as something measured. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 343,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and an exact pair of bounds come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 344,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an approximate value are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 345,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an approximate value the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 346,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK Reading the one cited block, the quantity, its unit and an exact pair of bounds are present as projected, the statement digest recomputes correctly, and the framing there is as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 347,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The number, its unit and a lower limit only come from the sentence in the one cited block that the locator names; recomputing that assertion's digest reproduces the record's value, and the prose treats the figure as something calculated or modelled. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph. On the modality axis the record's own label and the label the capture puts on the same assertion are not the same word; I judged the prose, which bears the reading the record takes.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 348,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The quantity, its unit and an exact pair of bounds are all in the one cited block, and the digest of the located assertion recomputes to the value the record carries. The prose presents the figure as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 349,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK The one cited block gives this quantity with the unit and an exact pair of bounds the record projects; the located assertion's digest matches, and the reading frames the number as a plain statement. The subject record projected beside it is named in the same block, so the attachment is visible on the reading and not only in the graph.",
          "source_locators": [
            "page:2:block:001"
          ]
        }
      ]
    }
  ],
  "ratification": {
    "evaluator_kind": "HUMAN_AUTHOR",
    "actor_id": "actor:luis",
    "disposition": "PENDING",
    "completed_at": "",
    "notes": ""
  }
}
```

Each `rows` entry has this shape:

```
{
  "row_index": 0,
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "DIGEST_OK DERIVATION_LOCAL SUBJECT_IN_BLOCK one or two sentences in your own words"
}
```
