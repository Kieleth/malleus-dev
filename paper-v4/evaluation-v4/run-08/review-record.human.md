# Malleus paper v4 run-08 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 5 for
CQ-01, 2 for CQ-02, 0 for CQ-03, 1 for
CQ-04, 8 in all. Cite reading block ids only. Write the reasons in
your own words and copy no source passage into this record.

Each `rationale` opens with the two fixed tokens the task defines, `DIGEST_OK`
or `DIGEST_MISMATCH` where the record carries a statement digest, then
`DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL`, then the reason in your own words.
The `rows` grammar is closed at four keys and the validator is frozen, which is
why both findings live at the head of the text field.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "HUMAN_RATIFIED",
  "inputs": {
    "review_protocol_sha256": "sha256:7cee52a7d6ea5018fe8443e621c72280b05c2bb5cc1e4a2eeaa27208665ed379",
    "review_input_manifest_sha256": "sha256:7925415a16e67ccefc2a48daf3cd1bf7679180233bee6a11f444e0f918515395"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-08",
    "completed_at": "2026-09-05T03:58:01Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows name the SMARTIES cruise, which is the campaign the question asks about, but they reach it only through a ship-time funding relation, never through the acquisition. The observing network and the number of instruments deployed appear nowhere in the rows, although the reading states both plainly at page:2:block:002 and page:6:block:002. The remaining four rows cover where the catalog was deposited and which packages were used to detect, locate and solve for focal mechanisms, which is processing rather than acquisition. One requested part is answered in substance, the rest is missing.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002",
        "page:10:block:044"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:10:block:044",
            "page:6:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation and its target organization are both formalized out of page:10:block:044, which is also among the blocks formalizing the campaign. No record in this row carries a statement digest, so no digest comparison applies. The block ties the fleet to the cost of the vessel time for that cruise, not to the cruise as a whole, and names other bodies as funders of the research; the row asserts a bare funding relation between campaign and organization and loses that scope."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "DERIVATION_LOCAL The relation and both endpoints are formalized out of the same block, page:8:block:008. These records carry no statement digest. The block records that the catalog and the arrival picks produced by the study were placed in the archive the row names as target, which is the relation, source and target the row asserts."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block, page:8:block:003, also formalizes the method and the software. Neither record type carries a statement digest. That block records that the study determined focal mechanisms with the package the row names, from the polarity picks the row's method describes, and page:8:block:010 supplies that package's version and address, the two extra attributes on the target."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block, page:7:block:004, also formalizes both endpoints. No statement digest is carried here. That block records that the study located its initial hypocenters with the search algorithm the row names, inside the program the row names, and page:8:block:010 supplies the address on the target."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010",
            "page:2:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block, page:6:block:002, also formalizes the target software, and the method's name is formalized out of page:2:block:002. These records carry no statement digest. page:6:block:002 records automatic detection of arrivals by the trigger algorithm the row names as source, inside the package it names as target; page:8:block:010 supplies that package's address, and page:2:block:002 carries the same method under the same name."
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "NOT_RESPONSIVE",
      "responsiveness_rationale": "Both rows report a ridge segment lying next to a non-transform discontinuity and nothing else. No earthquake population appears in either row, and no row relates any event to a ridge axis, so neither requested part is answered. The reading puts the deep microseismicity beneath the ridge axis of one named segment at page:2:block:004 and reports the observed depths there at page:2:block:006; the rows return two different segments with nothing that would pick out the one the question asks for.",
      "source_locators": [
        "page:2:block:004",
        "page:2:block:006"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block, page:2:block:001, also formalizes attributes of both endpoints, and page:1:block:005 formalizes their names and kinds. No statement digest is carried here. The subsection list and the sentence placing this segment immediately south of the first discontinuity support the adjacency, both feature kinds and the discontinuity's strike. The magmatic character is where support thins: the reading offers it as what the segment's valley width and volcanic ridge orientation suggest, while the row states it as a settled attribute."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block, page:1:block:005, also formalizes the names and kinds of both endpoints; the orientations come from page:2:block:001. No statement digest is present. The reading names the segment lying south of the second discontinuity, calls it magmatic and gives its orientation with no hedge, and gives the discontinuity's orientation, which covers every attribute the row carries."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "NOT_RESPONSIVE",
      "responsiveness_rationale": "The query returned no row for this question, so nothing in the result addresses either range, either unit or the estimate status. The reading carries both quantities: the observed depths of the deep earthquakes beneath the segment axis at page:2:block:006, and the calculated primary-melt CO2 range with its unit and its explicitly calculated status at page:5:block:005. An empty result cannot answer a question the reading answers.",
      "source_locators": [
        "page:2:block:006",
        "page:5:block:005"
      ],
      "rows": []
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "NOT_RESPONSIVE",
      "responsiveness_rationale": "The single row states that a segment is bounded by a detachment fault. It names no causal mechanism, no ascending melt, no degassing, no volume or pressure change, no extensional stress and no epistemic status, so it answers none of the question. The reading states the authors' preferred explanation at page:5:block:002 and the volume change acting under extensional stress to trigger the earthquakes at page:5:block:003, both offered as a suggestion rather than as settled fact.",
      "source_locators": [
        "page:5:block:002",
        "page:5:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The relation's block, page:1:block:005, also formalizes both endpoints; one target attribute comes from page:2:block:005. These record types carry no statement digest. The reading states without qualification that the segment is amagmatic and is bounded on its eastern side by a west-dipping detachment fault, which covers the relation, the segment and most of the fault's attributes. The inactive state is different in kind: the reading reaches it by inference from the lack of deep seismicity near the core-complex termination, and the row carries it as a settled attribute with the inference dropped."
        }
      ]
    }
  ],
  "ratification": {
    "evaluator_kind": "HUMAN_AUTHOR",
    "actor_id": "actor:luis",
    "disposition": "RATIFIED_AS_RECORDED",
    "completed_at": "2026-09-05T04:04:15Z",
    "notes": "Ratified as recorded. Decided by Luis in chat on 2026-09-05 after the overseer presented the four responsiveness verdicts, the support counts, the three PARTIAL rows (a hedge carried as settled in each), the vacuous digest check and the two review-surface debts. In the same decision Luis approved the four follow-ups of the v4.2 RCA: the subject element, entity-level and subject-following query cases, one skill sentence, and run-09 measured against run-04's local rows."
  }
}
```

Each `rows` entry has this shape:

```
{
  "row_index": 0,
  "source_support": "SUPPORTED | PARTIAL | UNSUPPORTED | NOT_EVALUABLE",
  "source_locators": ["page:2:block:004"],
  "rationale": "DIGEST_OK DERIVATION_LOCAL one or two sentences in your own words"
}
```
