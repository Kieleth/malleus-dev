# Malleus paper v4 run-14 source-grounded review record

Template. The row counts are substituted at freeze, from the frozen cell's own
query result, at the same time as `paper-v4/evaluation-v4/review-task-v4.template.md`.
No placeholder may survive instantiation.

Copy this file for the review and edit only the JSON block. `BLANK` and
`PRELIMINARY_COMPLETE` are not paper evidence; Luis must ratify.

Fill one `rows` entry per returned row, in order, zero-based: 190 for
CQ-01, 195 for CQ-02, 323 for CQ-03, 211 for
CQ-04, 919 in all. Cite reading block ids only. Write the reasons in
your own words and copy no source passage into this record.

Each `rationale` opens with the fixed tokens the task defines: `DIGEST_OK` or
`DIGEST_MISMATCH` where the record carries a statement digest, then, on a
`RELATION` row only, `DERIVATION_LOCAL` or `DERIVATION_NON_LOCAL`, and on a
`SUBJECT` or an `ENTITY` row only, one of `SUBJECT_IN_BLOCK`,
`SUBJECT_NOT_IN_BLOCK` or `NO_SUBJECT_IN_ROW`; then the reason in your own
words. The `rows` grammar is closed at four keys and the validator is frozen,
which is why every finding lives at the head of the text field.

```json
{
  "schema": "malleus.paper-v4.source-grounded-review/v2",
  "status": "PRELIMINARY_COMPLETE",
  "inputs": {
    "review_protocol_sha256": "sha256:88b69f6e80a3b9eac3a2c990178186df9c52fed3ced5c4e020162b0c202fa795",
    "review_input_manifest_sha256": "sha256:c3c1215967133eea3cf4a2d349b0d09cdf05bc572a5a49c907b04a19b53d7af7"
  },
  "preliminary": {
    "evaluator_kind": "CLAUDE_PRELIMINARY",
    "actor_id": "actor:claude-preliminary-run-14",
    "completed_at": "2026-09-05T16:47:47Z"
  },
  "questions": [
    {
      "question_id": "CQ-01",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows do reach the question. The campaign is present as its own record, named and dated, the instrument type is present, a relation ties the campaign to the instruments it observed with, and a count record carries the number deployed with the acquisition sentence behind it. Two things keep this short of full responsiveness. The observation network itself is never a record: it survives only inside the free text of a count's scope and in the instrument-type record, so the part of the question asking which network produced the data is answered by inference rather than by a row. And the rows carry two instrument counts, the number deployed and the number that gave usable data, distinguished only by prose in a scope field, so the count the question asks for is not determinate from the row structure alone. The remainder of the returned rows, the reference list, the funders, the acknowledged individuals and the publication apparatus, bear on nothing the question asks.",
      "source_locators": [
        "page:2:block:002",
        "page:6:block:002"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:8:block:012",
            "page:8:block:013"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:8:block:014"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:8:block:015"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:8:block:016"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:8:block:017"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:001",
            "page:9:block:002"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited entry names the monograph series, its editors, the page span, the DOI and the year exactly as the row projects them, and an item contributed to an edited series is the chapter kind the row asserts.",
          "source_locators": [
            "page:9:block:003",
            "page:9:block:004"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:005"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:9:block:006"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:007"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:008"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:009"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:9:block:010"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:012"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:013"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Across the two cited blocks the entry gives the title, the monograph series, the page span, the DOI and the year the row projects, and the editors named beside the series carry the chapter reading of the work kind.",
          "source_locators": [
            "page:9:block:014",
            "page:9:block:015"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:9:block:016"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:017",
            "page:9:block:018"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:019"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:020",
            "page:9:block:021"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited entry gives the title, the abstracts volume it appeared in, the item number the row projects as a page range, the DOI and the year, and the venue named is a conference abstract collection, which is the projected kind.",
          "source_locators": [
            "page:9:block:022"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks together give the cruise name with its vessel, the year and the DOI as projected; naming a cruise and a research vessel rather than a venue supports the cruise work kind the row asserts.",
          "source_locators": [
            "page:9:block:023",
            "page:9:block:024"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:025",
            "page:9:block:026"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:028"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited entry states the title, the book it appeared in, the page span and the year as projected, and an item placed inside a named book with a publisher is the chapter kind the row shows.",
          "source_locators": [
            "page:9:block:029"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:030"
          ]
        },
        {
          "row_index": 26,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The cited entry states the title, the venue abbreviation, the page range, the DOI and the year as projected, but it carries no volume and does not present the venue as a journal, so the projected work kind is the one field the block leaves unsupported.",
          "source_locators": [
            "page:9:block:031"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:031",
            "page:9:block:032"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:9:block:033"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:034"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:035"
          ]
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:036"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:9:block:037",
            "page:9:block:038"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:039"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:040"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:041"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:9:block:042"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:043"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:044",
            "page:9:block:045"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:046",
            "page:9:block:047"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:9:block:048"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:049"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:050"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:9:block:051"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:9:block:052"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:9:block:053",
            "page:9:block:054"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:9:block:055"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:10:block:001",
            "page:9:block:056"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:10:block:002"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:10:block:003"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:10:block:004",
            "page:10:block:005"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:10:block:006",
            "page:10:block:007"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:10:block:008"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:10:block:009"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:10:block:010"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:10:block:011"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:10:block:012"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:10:block:013",
            "page:10:block:014"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:10:block:015"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:10:block:016"
          ]
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:10:block:017"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:10:block:018"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:10:block:019"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:10:block:020"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:10:block:021"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:10:block:023"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:10:block:024"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:10:block:025"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:10:block:026"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:10:block:027",
            "page:10:block:028"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:10:block:029"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:10:block:030"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks give the title, the year and the archive address the row projects as a DOI; the entry names no journal at all and points only at an open archive, which is the preprint kind the row asserts.",
          "source_locators": [
            "page:10:block:032",
            "page:10:block:033"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:10:block:034"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks state the title, the venue, the volume, the DOI and the year as the row shows them; the row projects no page range, so nothing is claimed that the entry, which gives none either, would have to carry.",
          "source_locators": [
            "page:10:block:035",
            "page:10:block:036"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows, the venue, the title, the page range, the year and the volume, is stated in the cited entry, and its periodical-article form supports the projected kind; the row asserts nothing further.",
          "source_locators": [
            "page:10:block:037"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The reference entry the witness derives from carries the venue, the title, the page range, the year and the volume just as the row projects them, and the entry's shape is that of an article in a periodical, which is the work kind projected. Nothing in the row runs past the entry.",
          "source_locators": [
            "page:10:block:038",
            "page:10:block:039"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Reading the cited entry alone gives the venue, the title, the page range, the year and the volume in the same form the row shows, and the entry is laid out as a periodical article, matching the projected kind. No projected field lacks support.",
          "source_locators": [
            "page:10:block:040"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row's fields, the venue, the title, the page range, the year and the volume, are all present in the cited reference entry, and the entry names a periodical with a volume and pages, which is what the projected work kind asserts.",
          "source_locators": [
            "page:10:block:041",
            "page:10:block:042"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks are the article's own title page, its running footer and its licence notice, and between them they state the title, the journal, the volume, the article number the row projects as a page range, the year, the DOI and the licence, each as projected.",
          "source_locators": [
            "page:10:block:045",
            "page:10:block:048",
            "page:11:block:003",
            "page:11:block:005",
            "page:11:block:006",
            "page:1:block:001",
            "page:1:block:006",
            "page:2:block:008",
            "page:3:block:006",
            "page:4:block:008",
            "page:5:block:011",
            "page:6:block:006",
            "page:7:block:013",
            "page:8:block:018",
            "page:9:block:056"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited data-availability block presents this deposit, the unprocessed recordings together with the reports of the voyage, as one item obtainable on request from a named site, which is the name the row projects and supports treating the item as data.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited methods block says the rock samples were compiled from this named database, and the figure caption cited beside it attributes the whole-rock analyses to it, which is exactly the name, the description and the database kind the row projects.",
          "source_locators": [
            "page:6:block:005",
            "page:8:block:005"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block states that the online version carries supplementary material and gives the address the row projects, so both the name and the kind rest on the block; the address is the article's own, which is what the block offers for reaching the material.",
          "source_locators": [
            "page:11:block:001"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks name the catalog and the picked arrivals as a deposit and give the repository address the row projects as a DOI, so the name, the address and the dataset kind are all stated.",
          "source_locators": [
            "page:8:block:008",
            "page:8:block:009"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited results block says an active-source wide-angle refraction profile supplied the velocity model used for the locations, and the figure caption cited beside it marks the profile in the study area; both the name and the description the row projects rest on that.",
          "source_locators": [
            "page:2:block:002",
            "page:3:block:004"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks name the cruise, date it to the year of the deployment, and say the instrument network that gathered the microseismicity was put out during it; one of them gives the two months, which is the month-level precision the row projects.",
          "source_locators": [
            "page:10:block:043",
            "page:2:block:002",
            "page:2:block:007",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited introduction block announces the microseismicity study of the ridge in the equatorial Atlantic whose results the paper presents, which is both the name and the description the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The abstract block cited says the seismological data were recorded by ocean-bottom seismometers and the results block gives the abbreviation the row projects as the name, so the name and the description both rest on cited prose.",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:002"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the results block naming the one-dimensional velocity model sought for the travel-time calculation states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the discussion block that applies a named CO2 solubility model to the melt states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:5:block:006"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the results blocks that report depth resolution tests and then rely on them states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:006"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the results block that relocates the hypocenters with a double-difference method states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the methods block that determines focal mechanisms from first-motion polarities states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:8:block:003"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the discussion block that corrects for fractional crystallization before computing CO2 states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:5:block:004"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the methods block that determines magnitudes on a local magnitude scale states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:8:block:002"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the results block that obtains hypocenters with a non-linear location algorithm states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the methods block that locates initial hypocenters with a non-linear oct-tree search states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:7:block:004"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the results and methods blocks that detect arrivals with a short-term/long-term average trigger states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the figure caption that takes the isotherms from a simulated thermal model states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:7:block:012"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects only a name, and the methods block that derives the Vp/Vs ratio from Wadati diagrams states it in those words; nothing else is asserted.",
          "source_locators": [
            "page:7:block:002"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW This name stands in the author line of the cited title-page block, which is all the row claims: a person bearing that name. Nothing further is projected.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a personal name and nothing else, and the cited byline block lists that person among the authors; the correspondence block cited beside it repeats the name.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:031"
          ]
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:031"
          ]
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:011"
          ]
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:022"
          ]
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:022"
          ]
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:027"
          ]
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:011"
          ]
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:031"
          ]
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:022"
          ]
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:022"
          ]
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:027"
          ]
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:011"
          ]
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:027"
          ]
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:031"
          ]
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:10:block:031"
          ]
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:027"
          ]
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:011"
          ]
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited reference block lists this person among the authors of that entry, in the surname-and-initials form the row projects, and a name in an author list is a person, which is the only other thing the row asserts.",
          "source_locators": [
            "page:9:block:027"
          ]
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited title-page block carries this person in the author list, so both the name and the personal agent type the row projects are stated there; the letter spacing the text layer left in the byline does not change what a reader takes the name to be.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW This name stands in the author line of the cited title-page block, which is all the row claims: a person bearing that name. Nothing further is projected.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a personal name and nothing else, and the cited byline block lists that person among the authors; the correspondence block cited beside it repeats the name.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited title-page block carries this person in the author list, so both the name and the personal agent type the row projects are stated there; the letter spacing the text layer left in the byline does not change what a reader takes the name to be.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW This name stands in the author line of the cited title-page block, which is all the row claims: a person bearing that name. Nothing further is projected.",
          "source_locators": [
            "page:11:block:002",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited acknowledgements block thanks this person by initial and surname, in the form the row projects, and thanking someone for discussions puts a person behind the name.",
          "source_locators": [
            "page:10:block:043"
          ]
        },
        {
          "row_index": 126,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The cited block opens with the surname alone: the initial the row projects belongs to the previous acknowledgements block, which this row does not cite, so the block supports the person but not the full name as shown.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited acknowledgements block names this person, initials and surname together as the row projects them, among those thanked for discussions.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited acknowledgements block names this person, initials and surname together as the row projects them, among those thanked for discussions.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited title-page block carries this person in the author list, so both the name and the personal agent type the row projects are stated there; the letter spacing the text layer left in the byline does not change what a reader takes the name to be.",
          "source_locators": [
            "page:11:block:002",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the funding block naming the regional council that supported the work through a named programme states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the affiliation footnote giving the institute, city and country the row projects as name and description states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the funding block naming the council that supported one author under a framework programme states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the funding block naming the national government and the programme under which it funded the work states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the funding block saying the cruise shipping time was paid through this fleet infrastructure states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the affiliation footnote giving the laboratory, its partner institutions, town and country states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the affiliation footnote naming the university, the institute and the city states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the funding block naming the project and spelling out what it is states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the funding block naming the national science foundation that partly funds one author states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the affiliation footnote naming the laboratory, the institute, the ministry and the city states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the publisher's note block, which names the publisher declaring neutrality states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:11:block:004"
          ]
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the affiliation footnote naming the department, the university and the city states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 142,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The cited data-availability block names the repository, so the name holds, but it presents it as a database that received the deposit and says nothing that makes it the organization the row's agent type asserts.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The row projects a body and an organizational agent type, and the funding block naming the provincial science foundation and its grant number states it; naming a funder or an institution in those roles is what an organization is.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows rests on the code-availability block, which names it, says what it was used for and gives the address the row projects.",
          "source_locators": [
            "page:8:block:010"
          ]
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows rests on the code-availability block spread over the two cited blocks, which names the toolbox with its major version, its use for graphing and the download address.",
          "source_locators": [
            "page:8:block:010",
            "page:8:block:011"
          ]
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows rests on the methods block that used it for focal mechanisms and the code-availability block that gives its version and address.",
          "source_locators": [
            "page:8:block:003",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows rests on the methods block that relocated events with it and the code-availability block that gives its version and address.",
          "source_locators": [
            "page:7:block:006",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows rests on the methods block that located the initial hypocenters with its oct-tree search and the code-availability block that gives its address.",
          "source_locators": [
            "page:7:block:004",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW Every field the row shows rests on the methods block that ran the trigger inside it and registered the events in its database, and the code-availability block that gives its address.",
          "source_locators": [
            "page:6:block:002",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The methods block cited says this program was used to search for a minimum one-dimensional velocity model, and the code-availability block cited beside it gives the address the row projects, so name, description and address all rest on cited prose.",
          "source_locators": [
            "page:6:block:004",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The magnitude block cited says the completeness and the b value were obtained with this software, and the code-availability block gives its address, which covers the name, the description and the locator the row shows.",
          "source_locators": [
            "page:8:block:002",
            "page:8:block:010"
          ]
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The block the relation derives from is also a block both endpoints derive from. It says the catalog and picked arrivals produced in this study were placed in the named repository, which is the deposit relation the row asserts, and it carries the modality as a plain statement.",
          "source_locators": [
            "page:8:block:008"
          ]
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block is one of the target reference's own blocks. That entry is the cruise's own citable record, naming the cruise and its vessel, which supports reading the cited work as the report of the campaign at the source end.",
          "source_locators": [
            "page:9:block:023"
          ]
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation and the target reference derive from the same block. The entry is a conference abstract whose title says it presents preliminary results of that cruise, so the work reports the campaign as the row asserts.",
          "source_locators": [
            "page:9:block:022"
          ]
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block is shared with both endpoints. It attributes the gathering of the microseismicity to a network of the instruments at the target end, working during the cruise at the source end, which is the observed-with link the row shows.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The author-contribution block the relation derives from is also one the target work derives from. It credits this author with developing the idea, which is the conceptualization role the row projects; the byline block cited beside it is what ties the initials in the contribution sentence to the named person.",
          "source_locators": [
            "page:10:block:045",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL Same shared block as the row above. It says this author supervised the acquisition, the processing and the interpretation, which is the supervision role projected, and the byline block resolves the initials to the name.",
          "source_locators": [
            "page:10:block:045",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The contribution block is shared with the target work and says this author wrote the paper, which is the drafting role the row projects; the byline block carries the initials-to-name step.",
          "source_locators": [
            "page:10:block:045",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The contribution block, shared with the target work, credits this author with analysing the results, which is the formal-analysis role shown; the byline block supplies the person behind the initials.",
          "source_locators": [
            "page:10:block:045",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same contribution block credits this author with processing the microseismicity data. The row projects an unnamed other role, and a stated contribution of that kind is what the block supports.",
          "source_locators": [
            "page:10:block:045",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The contribution block, shared with the target work, says this author wrote the paper, matching the drafting role; the initials are resolved by the cited byline block.",
          "source_locators": [
            "page:10:block:045",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The relation derives from the second author-contribution block, which is not among the blocks either endpoint derives from: the cruise is introduced in the results and methods and the person in the byline. On the reading the pairing still holds, because that block says the four named initials took part in the data collection during that cruise and the cited byline block is where those initials become names.",
          "source_locators": [
            "page:10:block:046",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The relation derives from the second author-contribution block, which is not among the blocks either endpoint derives from: the cruise is introduced in the results and methods and the person in the byline. On the reading the pairing still holds, because that block says the four named initials took part in the data collection during that cruise and the cited byline block is where those initials become names.",
          "source_locators": [
            "page:10:block:046",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The relation derives from the second author-contribution block, which is not among the blocks either endpoint derives from: the cruise is introduced in the results and methods and the person in the byline. On the reading the pairing still holds, because that block says the four named initials took part in the data collection during that cruise and the cited byline block is where those initials become names.",
          "source_locators": [
            "page:10:block:046",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The relation derives from the second author-contribution block, which is not among the blocks either endpoint derives from: the cruise is introduced in the results and methods and the person in the byline. On the reading the pairing still holds, because that block says the four named initials took part in the data collection during that cruise and the cited byline block is where those initials become names.",
          "source_locators": [
            "page:10:block:046",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from the title-page block, which both endpoints also derive from. That block carries the article title and the author list containing this person, which is the authorship link the row asserts and the plain statement modality it projects.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from the title-page block, which both endpoints also derive from. That block carries the article title and the author list containing this person, which is the authorship link the row asserts and the plain statement modality it projects.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from the title-page block, which both endpoints also derive from. That block carries the article title and the author list containing this person, which is the authorship link the row asserts and the plain statement modality it projects.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from the title-page block, which both endpoints also derive from. That block carries the article title and the author list containing this person, which is the authorship link the row asserts and the plain statement modality it projects.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from the title-page block, which both endpoints also derive from. That block carries the article title and the author list containing this person, which is the authorship link the row asserts and the plain statement modality it projects.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from the title-page block, which both endpoints also derive from. That block carries the article title and the author list containing this person, which is the authorship link the row asserts and the plain statement modality it projects.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from the title-page block, which both endpoints also derive from. That block carries the article title and the author list containing this person, which is the authorship link the row asserts and the plain statement modality it projects.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from the title-page block, which both endpoints also derive from. That block carries the article title and the author list containing this person, which is the authorship link the row asserts and the plain statement modality it projects.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The acknowledgements block the relation derives from is also the funder's own block. It says the shipping time for that cruise was funded through this fleet infrastructure, which supports the funding link at the grain the row states it.",
          "source_locators": [
            "page:10:block:044"
          ]
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The funding block is shared with the funder endpoint. It names the advanced grant agreement number the row projects and says it went to the author at the target end, whose initials the cited byline block resolves.",
          "source_locators": [
            "page:10:block:044",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same funding block names the council and the framework programme designation the row projects as the award identifier, and says the support went to that author; the byline block turns the initials into the name.",
          "source_locators": [
            "page:10:block:044",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The funding block, shared with the funder, says the named foundation partly funds the author at the target end and lists the grant number the row projects; the byline block carries the initials-to-name step.",
          "source_locators": [
            "page:10:block:044",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 178,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same block lists the second grant number under the same foundation and the same recipient, which is what this row projects.",
          "source_locators": [
            "page:10:block:044",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 179,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The funding block names the provincial foundation, its grant number and the author it funds, all as the row projects them, and it is one of the funder's own blocks.",
          "source_locators": [
            "page:10:block:044",
            "page:1:block:001"
          ]
        },
        {
          "row_index": 180,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block is one of the target reference's blocks. The entry is the software's own citable paper, which supports reading the work as the report of that program.",
          "source_locators": [
            "page:9:block:025"
          ]
        },
        {
          "row_index": 181,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation and the target reference share the block. The entry is the paper describing that seismicity package, so the reported-by link holds on the cited prose.",
          "source_locators": [
            "page:10:block:029"
          ]
        },
        {
          "row_index": 182,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record. The cruise the row names as subject is named in that block, and the block is about the network deployed on that cruise, so the count of instruments is a count of the cruise's own network rather than of something merely mentioned beside it. The second cited block repeats the network size.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 183,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The recomputed digest matches. The subject is the instrument type, and the block names it in both its long and short forms while stating how many of them yielded usable data, so the record is about the instruments themselves.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 184,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest matches the located statement. The subject is the velocity model, and the block says how many such models were built, so the count is a count of the subject and not of a neighbouring thing.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 185,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK Same record as the earlier row, projected here without its value. The digest matches, the cruise is named in the block, and what remains projected, that this is a count of the instruments in the deployed network, is what the block states.",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ]
        },
        {
          "row_index": 186,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest matches. The subject is the refraction profile, which the block names, and the block says the profile constrains velocity down to about the depth the row projects as an open upper bound in the unit shown, so the measurement is about the subject.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 187,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The same instrument count seen earlier without its value. The digest matches and the block names the instrument type while reporting how many were usable, so the record is about the subject.",
          "source_locators": [
            "page:2:block:002"
          ]
        },
        {
          "row_index": 188,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The velocity-model count again, projected without its value. The digest matches and the block states that models of that kind were built, which is what the record is about.",
          "source_locators": [
            "page:6:block:003"
          ]
        },
        {
          "row_index": 189,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest matches the located statement. The program named as subject appears in the block, and the block attributes the error ellipsoid and its confidence level to that program, so the value belongs to the subject.",
          "source_locators": [
            "page:7:block:005"
          ]
        }
      ]
    },
    {
      "question_id": "CQ-02",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "Both parts of the question are answered by rows, not by inference. The named subsection is present as its own ridge-segment record; the deep population is present as its own record; and a relation row ties the two, its derivation reaching the block that puts the deep microseismicity beneath that segment's ridge axis. Observation rows on the same population carry the depth interval, and a claim row gives the direction along which those events line up relative to the axial faults, so the position with respect to the axis is stated and not only implied. The neighbouring populations, the shallow events at the intersection, the normal-depth events at the southern discontinuity and the off-axis activity to the west, each carry their own relation to their own feature, so they sharpen the answer rather than blur it. One qualification, which does not change the label: there is no record for the ridge axis itself, so the relation reaches the segment and the axis appears in record names and in the derivation's own block rather than as an endpoint.",
      "source_locators": [
        "page:2:block:004",
        "page:2:block:006",
        "page:4:block:003"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this edifice as a volcano where comparable seismicity was seen, which carries both the name and the volcanic kind the row projects.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block introduces these bodies of melt and the role they play in separating brittle from ductile lithosphere, so the name and the melt-body kind both rest on it.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block describes the segment's valley by that name and gives its width, which supports the name and the axial-valley kind projected.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block spells out the boundary and its abbreviation, which is the name the row shows, and calls it a boundary, which is the kind.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this transform fault as one of the two bounding the segment that contains the study area, and places the study area in the segment's northern part beside the other one, from which the southern position in the description follows.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block opens on oceanic crust formed from mantle melt, which states the name and the layer kind the row projects.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the dipping fault of that kind bounding the RTI segment on its east.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks name this ocean region as the setting of the study and again in a figure caption.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ]
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block reports the extinct vent field on the flank of the first discontinuity, which is the name, the kind and the description the row shows.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this Icelandic peninsula, which supports the name and the landmass kind.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this ridge among the ultraslow-spreading ridges with deep mantle earthquakes, which is the name and the spreading-ridge kind.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited figure caption reports the inactive mound suggested by the dive observations, which is the name, the hydrothermal kind and the description projected.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block places the compared volcanic systems in this country, which is the name and the landmass kind.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this plate beneath which comparable reflections were seen, which is the name and the plate kind.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this ridge in the list of sites whose depth data were updated, which supports the name and the ridge kind.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks give the boundary in full and with its abbreviation, which is the name, and it is a boundary, which is the kind.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ]
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks speak of the brittle lithosphere and its thickness, which supports the name and the layer kind.",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005"
          ]
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this seamount as part of the northern ridge, which is the name and the edifice kind.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the mantle as the source of the melt forming the crust, which is the name and the layer kind.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block reports the enriched source near the transform invoked for the enriched basalts, which is the name, the kind and the description.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks name the ridge in full and give its abbreviation, which supports the name and the spreading-ridge kind.",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:007"
          ]
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The first cited block gives the long ridge segment between the two transforms and the second calls it a supersegment, which is the name and the segment kind.",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ]
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this island offshore which deeper events were observed, which is the name and the landmass kind.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks speak of the melt and its migration and saturation, which supports the name and the melt-body kind.",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ]
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The first cited block carries the label in the schematic and the second names the interface as expected, which supports the name and the boundary kind.",
          "source_locators": [
            "page:7:block:010",
            "page:7:block:011"
          ]
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the high-temperature shear zones to which transform-fault seismicity has been linked, which is the name and the shear-zone kind.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the oriented neo-volcanic ridge in the segment, which is the name and the volcanic kind.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the faults of that kind cutting the core-complex surface, which is the name and the fault kind.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block lists the four subsections and names the first discontinuity, and it defines the discontinuities as non-transform, which is the kind.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The same subsection list names the second discontinuity, and the block defines the discontinuities as non-transform.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block spells out the core complex and gives its abbreviation, which is the name, and states its kind.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 31,
          "source_support": "PARTIAL",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the massif and places it at a non-transform discontinuity, which supports the name and the location, but it says nothing volcanic about it, so the projected feature kind is the one field the block leaves unsupported.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this subsection as the RTI segment and gives the label the row projects, and it is a ridge segment there.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this subsection as a short ridge segment with the label the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names the segment south of the second discontinuity with the label the row projects.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block names this transform fault as one bounding the segment that contains the study area.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The two cited blocks spell out the intersection and give the abbreviation, and the second uses it as a reference position.",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:005"
          ]
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block reports peridotites observed on it, which is the name and the surface kind.",
          "source_locators": [
            "page:1:block:006"
          ]
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block spells out this ridge and gives its abbreviation while comparing it with the study area.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited figure caption names the cones shown in the segment, which is the name and the volcanic kind.",
          "source_locators": [
            "page:4:block:007"
          ]
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block reports the located events in the intersection region, which is the population the row names and the measured modality it projects.",
          "source_locators": [
            "page:2:block:003"
          ]
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited abstract block reports the deep events in the mantle along the ridge axis, which is the population the row names and its measured modality.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block describes the subset built for the fixed-depth test, its size, its depth span and the cross-section it lies along, which is the name and the description projected.",
          "source_locators": [
            "page:7:block:010"
          ]
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited figure block carries the ridge label and the event total for that profile, which is the population the row names and describes.",
          "source_locators": [
            "page:3:block:004"
          ]
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block reports the normal-depth events beneath the southern discontinuity, which is the population named and its measured modality.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block reports the shallow off-axis events west of the segment axis, which is the population named and its measured modality.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block reports the shallow events at the intersection corner beneath the core-complex dome, which is the population named and its measured modality.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited figure block carries the transform label and the event total for that profile, which is the population the row names and describes.",
          "source_locators": [
            "page:3:block:003"
          ]
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block describes the sub-dataset built for the velocity-model search, its size and its selection criteria, which is the name and the description.",
          "source_locators": [
            "page:6:block:004"
          ]
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "rationale": "NO_SUBJECT_IN_ROW The cited block reports the cluster on the western side of the valley, which is the population named and its measured modality.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The block that formalizes the relation is not one either endpoint derives from: both the faults and the valley are introduced in the earlier structural block, while the relation rests on the discussion of the segment axis. The reading still supports the pairing, because the cited discussion block says the valley floor is cut by ridge-parallel normal faults. Worth noting that the faults described there are the axis-parallel ones, while the block that introduces the fault record describes the set cutting the core-complex surface.",
          "source_locators": [
            "page:3:block:001",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation and both endpoints derive from the same block, which names the seamount as belonging to the northern ridge, which is the part-of link the row asserts.",
          "source_locators": [
            "page:8:block:004"
          ]
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block is shared with both endpoints and says the core complex's surface is heavily cut by normal faults, which is exactly the cutting relation projected.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The figure caption the relation derives from is also one both endpoints derive from, and it places the core complex on the outside corner of the ridge, which supports the containment the row asserts.",
          "source_locators": [
            "page:2:block:007"
          ]
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL One block carries the relation and both endpoints. It says the intersection segment is bounded on its east by the dipping fault, which is the bounding relation projected, and the same block gives that segment its label.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The relation derives from the structural block, while both endpoints derive from the earlier block that lists the subsections. The reading supports adjacency all the same: the cited structural block places the segment immediately south of the discontinuity, and the subsection list cited beside it puts them next to each other in order.",
          "source_locators": [
            "page:2:block:001",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation and both endpoints share the block, which names the segment as the one lying south of that discontinuity, which is the adjacency projected.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation derives from a block both endpoints also derive from, and it places the long ridge segment between two transform faults, one of them the target, which is the bounding relation shown.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The same shared block names the other bounding transform of that segment, which is what this row asserts.",
          "source_locators": [
            "page:1:block:005"
          ]
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block is one the vent-field endpoint derives from, and it puts the extinct field on the eastern flank of the discontinuity, which supports the containment projected.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 60,
          "source_support": "PARTIAL",
          "rationale": "DERIVATION_LOCAL The relation derives from the block the cluster itself derives from, which puts that cluster to the west of the valley and gives its shallow depths. Standing to one side of the valley is not the same as being contained by it, so the containment the row projects drops the qualifier the block carries; the measured modality and the pairing of the two features hold.",
          "source_locators": [
            "page:2:block:006",
            "page:2:block:001"
          ]
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The relation derives from the observations block, which is not one either endpoint derives from: the deep population comes from the abstract and the segment from the block that lists the subsections. On the reading the pairing is exact, because the cited observations block states that the deep microseismicity lies beneath the ridge axis of that segment, and the block cited beside it gives the segment its label.",
          "source_locators": [
            "page:2:block:004",
            "page:1:block:005"
          ]
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The relation derives from the methods block that reports the final split of the catalogue, which neither endpoint derives from. The reading supports it: that block says how many events ended up along the ridge, and the figure block cited beside it is where the same population and total are shown.",
          "source_locators": [
            "page:7:block:007",
            "page:3:block:004"
          ]
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation's block is shared with both endpoints and says the normal-depth events occur beneath the southern discontinuity, which is the lies-beneath relation projected.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_LOCAL The relation and both endpoints share the block, which puts the majority of shallow events on the outside corner of the intersection, so the containment the row asserts holds on the cited prose.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "rationale": "DERIVATION_NON_LOCAL The relation derives from the methods block reporting the final split, which neither endpoint derives from, while the population itself comes from the figure block. Both cited blocks agree that a set of events was located along the transform, which is the relation projected.",
          "source_locators": [
            "page:7:block:007",
            "page:3:block:003"
          ]
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is a spatial statement about where the ridge axis is moving to, and the core complex is one of its two terms, named twice in the cited sentence as the reference the axis moves relative to.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim predicates a southward shallowing of the boundary itself, so the subject is what the claim is about and not merely a place named in it.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim states a thickness of the brittle lithosphere at the segment boundaries, which is a property of the subject.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim follows the migrating melt and says it keeps degassing, so the melt is what the claim predicates of.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is a mechanism ending in earthquakes triggered in the mantle, which is a statement about how the mantle behaves and not only about where the events sit.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim says the fault is inactive, a property of the subject.",
          "source_locators": [
            "page:2:block:005"
          ]
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim attributes the enriched basalts to melting of that source, which makes the source a principal term of the claim.",
          "source_locators": [
            "page:5:block:005"
          ]
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim places the earthquakes in the mantle below a stated depth, which is a statement about the mantle hosting them.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is that hydrothermal circulation cools the lithosphere and deepens the boundary, so the lithosphere is what the cooling is predicated of; the block also frames it as a hypothesis, which matches the disposition the row projects.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the attributed claim concerns what volatiles do to the melt, which is the subject.",
          "source_locators": [
            "page:5:block:010"
          ]
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim says magmatism dominates crustal accretion at that segment, a property of the segment.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim concludes that the mantle beneath the segment axis is hot, which is about the mantle.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is that the carbon dioxide carried in the primitive melt will bear on whether melt is present at depth, so the melt is what the claim predicates of.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is about what could produce the melt observed at that boundary, which makes the boundary a principal term.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the background claim says the melt is focused beneath the ridge axis, which is about the melt.",
          "source_locators": [
            "page:1:block:002"
          ]
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim has melt freezing at the underside of the lithosphere and leaving it compositionally uneven, which predicates of the lithosphere.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim states that how the melts migrate is not understood, which is about the melts.",
          "source_locators": [
            "page:1:block:003"
          ]
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim ends in brittle failure in the ductile lower crust, which is a statement about the crust.",
          "source_locators": [
            "page:4:block:002"
          ]
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is that ascending melt resides, fractionates and evolves at those depths, all predicated of the melt.",
          "source_locators": [
            "page:6:block:001"
          ]
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the negative claim is that no active vents are seen on that segment's axis, a statement about the segment, and the block carries the negation the row's modality projects.",
          "source_locators": [
            "page:3:block:002"
          ]
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the negative claim bounds the depth of seismicity beneath that segment's axis, which is about the segment, and the block carries the negation.",
          "source_locators": [
            "page:5:block:007"
          ]
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the negative claim is that no current eruption is evidenced in the axial valley, which is about the valley, and the block states it as a negation.",
          "source_locators": [
            "page:4:block:003"
          ]
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the prior observation reports normal velocity ratios in that segment, a property of the segment.",
          "source_locators": [
            "page:7:block:003"
          ]
        },
        {
          "row_index": 89,
          "source_support": "PARTIAL",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim's predicate is that the event depths are not an artifact of location error, which is a statement about the earthquakes and about the reliability of their locations; the ridge enters only as the feature the events lie beneath, so the block supports the claim but not that the ridge is what the claim is about.",
          "source_locators": [
            "page:2:block:006"
          ]
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim reads the peridotites as showing exhumed mantle, which makes the mantle the thing the claim is about.",
          "source_locators": [
            "page:2:block:001"
          ]
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is that a small pressure rise from degassing of the ascending melt induces the events, so the melt is a principal term.",
          "source_locators": [
            "page:5:block:003"
          ]
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim says the segment is of magmatic origin, a property of the segment.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the negative claim says the segment shows no detachment faulting, which is about the segment, and the block carries the negation.",
          "source_locators": [
            "page:4:block:001"
          ]
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is a limitation: the record is a snapshot and the activity along the supersegment may vary over years. It predicates of the record as much as of the supersegment, but the varying activity it names belongs to the supersegment, so the subject is defensible on the cited block.",
          "source_locators": [
            "page:2:block:004"
          ]
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the prior observation links deep transform seismicity to semi-brittle deformation in those shear zones, which makes the shear zones the locus the claim is about.",
          "source_locators": [
            "page:1:block:004"
          ]
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim is general to ultraslow-spreading ridges and names this one as an example, so it does hold of the subject, though the subject is narrower than the claim.",
          "source_locators": [
            "page:5:block:009"
          ]
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the claim states what is not known about volatiles during melt migration, which is about the melt.",
          "source_locators": [
            "page:1:block:001"
          ]
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the preferred hypothesis ties the deep microseismicity to degassing, and that population is the subject; the block also marks it as the authors' preferred possibility, which is the disposition the row projects.",
          "source_locators": [
            "page:5:block:002"
          ]
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject is named in the block the derivation reaches. On aboutness, the rejected explanation is about those same deep earthquakes, and the block presents it as one explanation among several, which matches the disposition projected.",
          "source_locators": [
            "page:3:block:001"
          ]
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the observation gives the alignment of those deep events and compares it with the axial faults, so the population is what is being described."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the mechanism claim is stated of the deep mantle earthquakes themselves, which is the subject, and the block presents it as a suggestion, matching the hypothesised modality."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the figure caption interprets those deep events as a consequence of degassing, so the events are the subject of the interpretation."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the claim is that some of those deep events may be long-period, a property of the population."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the rejected possibility is about those deep earthquakes; the second cited block is where the authors give the reasons the possibility does not hold, which is the disposition the row projects."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the claim rules a mechanism out for the earthquakes, which is the subject; read on the cited block alone the demonstrative points outside it, so the population it refers to is narrower than the whole located set the subject record stands for."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the limitation says more earthquakes are needed to characterise their sources, which is about the earthquake set."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the conclusion is that those deep events are well constrained and not artifacts, a statement about the population."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the claim attributes the off-axis shallow activity to off-axis magmatism, so that population is what the claim is about."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the claim attributes the shallow events beneath the dome to rupture on normal faults, which is about that population."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the count is of the events making up that subset, so the quantity is a quantity of the subject."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the count is of earthquakes identified by the automatic detection, and the subject is the earthquake set they belong to."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the count is of the located earthquakes themselves, which is the subject; the second cited block repeats the same total."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the block states that the earthquake locations were sorted into that many categories; what is counted is the categories rather than the events, but the classification is of the subject's own locations, so the record is still about the subject."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the count is of the events on that profile, which is the population the subject record stands for."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the count is of the well-constrained events that were relocated, so the quantity belongs to the earthquake set; the program named in the same sentence is not the subject of the row."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the count is of the events on the transform profile, which is the subject population."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the count is of the earthquakes making up that sub-dataset, which is the subject."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the count is of the events that were well relocated and entered the final catalogue, which is the subject set."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the quantity is the CO2 content of the primary melts, so the melt is what the value belongs to, and the block marks it as indicated by geochemical analyses, matching the calculated modality."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the temperature is given for the condition at that boundary, which is the subject the value is attached to."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the block states the enrichment of the samples of that segment, so the concentration bound is a property of the segment's samples."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth is what the boundary would have under the cold-lithosphere explanation, so the value belongs to the subject, and the block presents it as one explanation, matching the hypothesised modality."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the isotherm is the one the boundary is defined by, which makes the value a property of the subject; the block also carries the uncertainty the row projects."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the block states the boundary depth beneath the southern discontinuity, which is the value the row attaches to the subject."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the block states how shallow the boundary stays off axis, which is a property of the subject."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the lower bound is on the primary melt CO2 along that segment, which the block attributes to the segment."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the pre-eruptive CO2 from barium for that segment, stated for the segment in the cited block."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the pre-eruptive CO2 from barium for the southern segment, stated for that segment."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the primary-melt CO2 from the barium proxy for that segment, given for it in the cited block."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the primary-melt CO2 from the barium proxy for the southern segment."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the block gives the calculated CO2 of the melts generated along that segment, so the value belongs to the melt, which is the subject."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the block gives the calculated CO2 for the southern segment, which is the subject."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the pre-eruptive CO2 from rubidium for that segment, stated for it."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the pre-eruptive CO2 from rubidium for the southern segment."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the primary-melt CO2 from the rubidium proxy for that segment."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the primary-melt CO2 from the rubidium proxy for the southern segment."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the isotherms are the ones the boundary would correspond to under the cold-lithosphere explanation, so they are given of the subject."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the length is the stretch of that ridge axis the network covered, a measure of the subject."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the length is the stretch of that transform the network covered, a measure of the subject."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the age is given of the crust of the western flank, which is the subject."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the thickness is given of the same crust, with the uncertainty the row projects; the second cited block repeats the figure for the crust beneath the segment."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth is where extensive dry melting starts, which the block attributes to upwelling mantle, so the value belongs to the subject."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the average is reported for segments in that ocean region, which is the subject."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the maximum is reported for the same region."
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the rate is the half-spreading rate of that ridge in the study area, a property of the subject."
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the temperature is that of the mantle in which the events occur, which is the subject."
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth bound is given for the seismicity in that country, so it belongs to the subject as its setting."
        },
        {
          "row_index": 148,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:5:block:010",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches, and the subject is named in one of the two blocks the derivations reach, though not in the block the located statement sits in. The temperature value itself is supported in both blocks, and the second does tie the boundary to that isotherm. What the reading does not support is the row's own description of the quantity as the isotherm drawn as a dashed black line: that line belongs to the other figure, whose caption does not mention the boundary, while the caption that does name the boundary draws it as a thick line. The projected description therefore joins two figures."
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the age is that of the cold lithosphere causing the edge effect, which is the subject."
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth bound is given for the seismicity offshore that island, so it belongs to the subject as its setting."
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the width is given of the valley itself, which is the subject."
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the melt fraction is the one proposed at the base of that boundary, so the value is attached to the subject."
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the modelled temperature is for the depth interval beneath the segment axis, and the block draws the conclusion about the mantle there, which is the subject."
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the length is given of that discontinuity, which is the subject."
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth is how far the earthquakes reach beneath that discontinuity, which characterises the subject's brittle thickness."
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the bound is the depth range observed beneath that discontinuity, again a property of the subject."
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the offset is given of that discontinuity, which is the subject."
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the bound is the depth range observed beneath the core complex, a property of the subject."
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the range is the pre-eruptive CO2 of those melts after fractional crystallization, so the value belongs to the melt."
        },
        {
          "row_index": 160,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the value is a plotting half-width for the depth profiles in a figure, not a property of the ridge. The cited caption supports the number and supports that one of the profiles runs along the ridge, but it does not support that the ridge is what the record is about; the quantity characterises how the figure was drawn."
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the block states the rubidium enrichment of the samples of that segment, so the bound is a property of the segment's samples."
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the length is given of that segment, which is the subject."
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the length is given of the southern segment, which is the subject."
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the pressure is the one at which the melt would saturate, so the value belongs to the melt, and the block attributes it to a solubility model, matching the modelled determination."
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the length is given of the long segment between the two transforms, which is the subject."
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the value is the highest melt CO2 previously reported, and the block attaches it to that ridge, which is the subject."
        },
        {
          "row_index": 167,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the value is the half-width within which events are plotted on two transects, a property of the figure rather than of the core complex. The caption supports the number and supports that the transects run along and across the complex, but not that the complex is what the record is about."
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth range is where volatile-bearing melting initiates, which the block places in the mantle, so the value belongs to the subject."
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the water content is the one proposed at the base of that boundary, so it is attached to the subject."
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the age bound is what counts as a young magmatically accreted crust, a property of the subject."
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same count as the earlier row, projected here without its value; the digest matches and the subset the count belongs to is the subject."
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same identification count without its value; the subject is the earthquake set the identified events belong to."
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same location count without its value, still a count of the subject's own events."
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same category count without its value; the categories are the ones the subject's locations were sorted into."
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same profile count without its value, a count of the subject population."
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same relocation count without its value; the events relocated are the subject's, and the program named in the block is not the subject."
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same transform profile count without its value."
        },
        {
          "row_index": 178,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same sub-dataset count without its value, a count of the earthquakes in the subject."
        },
        {
          "row_index": 179,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the same well-relocated count without its value, a count of the subject's events."
        },
        {
          "row_index": 180,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth range is that of the deep events reported in the abstract, which is the subject population."
        },
        {
          "row_index": 181,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the average depth uncertainty is a property of the located events, which is the subject set."
        },
        {
          "row_index": 182,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the average horizontal uncertainty after relocation is a property of the located events; the second cited block repeats it in the running text."
        },
        {
          "row_index": 183,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth range is that of the deep microseismicity beneath the segment axis, which is the subject population."
        },
        {
          "row_index": 184,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth interval is given of the deep events below the ridge, so it belongs to the subject; the block states it inside an interpretation, which is the modality the row projects."
        },
        {
          "row_index": 185,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth range is that of the deep events observed beneath the segment axis, a property of the subject."
        },
        {
          "row_index": 186,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth span is that of the events making up the fixed-depth test subset, which is the subject."
        },
        {
          "row_index": 187,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the frequency is the threshold above which energy is missing in some of those deep events, a property of the subject population."
        },
        {
          "row_index": 188,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth range is that of the normal-depth events beneath the southern discontinuity, which is the subject population."
        },
        {
          "row_index": 189,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth bound is that of the off-axis shallow activity, which is the subject."
        },
        {
          "row_index": 190,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth bound is that of the same off-axis activity as described in the discussion, and the block frames the reading as probable, matching the hypothesised modality."
        },
        {
          "row_index": 191,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the share is of the located earthquakes meeting the quality criteria, a property of the subject set."
        },
        {
          "row_index": 192,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth bound is that of the deep events still located when the velocities were perturbed, which is the subject population."
        },
        {
          "row_index": 193,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the depth range is that of the shallow events at the intersection, which is the subject population."
        },
        {
          "row_index": 194,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The digest recomputed from the located statement matches the record and the subject appears in the block the derivation reaches. On aboutness, the focal depths are those of the western cluster, which is the subject."
        }
      ]
    },
    {
      "question_id": "CQ-03",
      "question_responsiveness": "RESPONSIVE",
      "responsiveness_rationale": "The rows carry both halves the question asks for, and they carry them in projected fields rather than only in the prose behind them. The earthquake depth range is returned as an observation over the deep-earthquake set, with a lower and an upper bound, a length unit, and a measured modality and determination; the calculated primary-melt CO2 range is returned as an observation over the studied ridge segment, with bounds, a mass-fraction unit, a calculated modality and an estimated determination. Because every quantity row also carries the record it is a quantity of, the bounded quantity, the unit, the quantity subject and the observed-or-calculated status are all readable on single rows without inference. The set is heavily diluted by rows of unrelated types, chiefly reference entries, which the type-only binding admits, but that is precision rather than responsiveness: nothing the question asks for is missing from the rows, and the rows that carry it are individually unambiguous about which range belongs to which subject and which status it holds.",
      "source_locators": [
        "page:1:block:001",
        "page:2:block:004",
        "page:2:block:006",
        "page:5:block:005",
        "page:8:block:007"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:012",
            "page:8:block:013"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:014"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:015"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:016"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 4,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:017"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:001",
            "page:9:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:003",
            "page:9:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the page range, the year and the DOI in the form the row records, and its shape is that of a chapter in a monograph series. The row projects no subject."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:013"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:014",
            "page:9:block:015"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the page range, the year and the DOI exactly as the row projects them, and it is laid out as a chapter in a monograph series. The row projects no subject."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:016"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:017",
            "page:9:block:018"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:019"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:020",
            "page:9:block:021"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:022"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the page range, the year and the DOI exactly as the row projects them, and it is laid out as a conference abstract. The row projects no subject."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:023",
            "page:9:block:024"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the year and the DOI in the form the row records, and its shape is that of a work of the kind projected. The row projects no subject."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:025",
            "page:9:block:026"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:028"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:029"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the page range and the year as projected and is a chapter in a monograph series. The row projects no subject."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:030"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:031"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the page range, the year and the DOI in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:031",
            "page:9:block:032"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:033"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:034"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:035"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 31,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:036"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:037",
            "page:9:block:038"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:039"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:040"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:041"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:042"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:043"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:044",
            "page:9:block:045"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:046",
            "page:9:block:047"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:048"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:049"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:050"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:051"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:052"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:053",
            "page:9:block:054"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:9:block:055"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:001",
            "page:9:block:056"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:004",
            "page:10:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:006",
            "page:10:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:013",
            "page:10:block:014"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:015"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:016"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:017"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:018"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:019"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:020"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:021"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:023"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:024"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:025"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:026"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 69,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:027",
            "page:10:block:028"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the page range and the year as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:029"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:030"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:032",
            "page:10:block:033"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the year and the DOI in the cited reference entry match the projection, and the entry is a preprint. The row projects no subject."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:034"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:035",
            "page:10:block:036"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited block's reference entry states the title, the journal or container, the volume, the year and the DOI as projected and is a journal article. The row projects no subject."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:037"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The reference entry in the cited block carries the title, the journal or container, the volume, the page range and the year exactly as the row projects them, and it is laid out as a journal article. The row projects no subject."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:038",
            "page:10:block:039"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited reference gives the title, the journal or container, the volume, the page range and the year in the form the row records, and its shape is that of a journal article. The row projects no subject."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:040"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, the journal or container, the volume, the page range and the year in the cited reference entry match the projection, and the entry is a journal article. The row projects no subject."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:041",
            "page:10:block:042"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The row's the title, the journal or container, the volume, the page range and the year are all present in the cited reference entry, which is a journal article. The row projects no subject."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:045",
            "page:10:block:048",
            "page:11:block:003",
            "page:11:block:005",
            "page:11:block:006",
            "page:1:block:001",
            "page:1:block:006",
            "page:2:block:008",
            "page:3:block:006",
            "page:4:block:008",
            "page:5:block:011",
            "page:6:block:006",
            "page:7:block:013",
            "page:8:block:018",
            "page:9:block:056"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The title, DOI and article label come from the first block, the journal, volume, page and year from the running footers, and the licence from the licensing block, so every projected field is stated in the cited blocks. The row projects no subject."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The data-availability block says the raw seismic data and cruise reports are available on the cruise website, which supports the name and treating them as a dataset. The row projects no subject."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005",
            "page:8:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The methods block says the MORB samples were compiled from the PetDB database and the figure caption shows what it supplies for MORB whole rocks, which supports the name, the database kind and the description. The row projects no subject."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:11:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The additional-information block says the online version contains supplementary material at the article DOI, which is the name, the DOI and the kind projected. The row projects no subject."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:008",
            "page:8:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The data-availability blocks say the earthquake catalogue and picked arrivals were deposited in Zenodo and carry the deposit DOI across the block break. The row projects no subject."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Askja as a volcano in Iceland, which is the name and the volcanic-edifice kind the row projects. The row projects no subject."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces axial melt lenses at fast- and intermediate-spreading ridges, giving both the name and the melt-body kind. The row projects no subject."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes a median valley along the RC2 ridge segment, which carries the name and the axial-valley kind. The row projects no subject."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block defines the brittle-ductile boundary and its abbreviation, and treats it as a boundary within the lithosphere. The row projects no subject."
        },
        {
          "row_index": 88,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Chain as one of the two transform faults bounding the MAR segment, so the name and the fault kind hold, but nowhere in the reading is Chain said to be the southern of the two, and the row projects that as its description. The row projects no subject."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block treats oceanic crust as the layer formed from mantle melt at spreading centres, matching the name and the layer kind. The row projects no subject."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes a westward dipping detachment fault bounding the RTI segment, giving the name and the fault kind. The row projects no subject."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks place the study in the equatorial Atlantic Ocean and treat it as an ocean region. The row projects no subject."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field on the eastern flank of NTD1, which is the name, the kind and the description the row projects. The row projects no subject."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Fagradalsfjall as a peninsula in Iceland, supporting the name and a landmass classification. The row projects no subject."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Gakkel Ridge among ultraslow-spreading ridges, which gives both the name and the spreading-ridge kind. The row projects no subject."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure caption in the block reports an inactive hydrothermal mound seen on the Nautile dives, matching the name, the hydrothermal kind and the description. The row projects no subject."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block places Askja and Fagradalsfjall in Iceland, supporting the name and a landmass classification. The row projects no subject."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to reflections beneath the young Juan de Fuca plate, giving the name and the plate kind. The row projects no subject."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Knipovich Ridge as one of the ridges whose depth data were updated, supporting the name and the spreading-ridge kind. The row projects no subject."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks give the lithosphere-asthenosphere boundary and its abbreviation and treat it as a boundary surface. The row projects no subject."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks discuss the brittle lithosphere and its thickness, which supports the name and the layer kind. The row projects no subject."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Logachev Seamount of Knipovich Ridge; a seamount is a volcanic edifice, which is the kind projected. The row projects no subject."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block treats the mantle as the source of the melt beneath spreading centres, which supports the name and the layer kind. The row projects no subject."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block invokes an enriched mantle source near the Romanche transform to explain the enriched basalts, matching the name, the kind and the description. The row projects no subject."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks name the Mid-Atlantic Ridge and its abbreviation and treat it as the spreading ridge under study. The row projects no subject."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks refer to the MAR segment between the two transforms and later call it a supersegment, supporting the name and the ridge-segment kind. The row projects no subject."
        },
        {
          "row_index": 106,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to offshore Mayotte Island, supporting the name and a landmass classification. The row projects no subject."
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks discuss the melt and its behaviour beneath the ridge, supporting the name and the melt-body kind. The row projects no subject."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010",
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The schematic-figure blocks label the Moho and call it the expected Moho interface, which is the name and the boundary kind. The row projects no subject."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to high-temperature hydrated mylonite shear zones along transform faults, giving the name and the shear-zone kind. The row projects no subject."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an oriented neo-volcanic ridge in the RC2 valley, supporting the name and the volcanic-edifice kind. The row projects no subject."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes normal faults cutting the OCC surface, supporting the name and the fault kind. The row projects no subject."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the first non-transform discontinuity and names it NTD1. The row projects no subject."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the second non-transform discontinuity and names it NTD2. The row projects no subject."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces a prominent oceanic core complex and its abbreviation on the eastern side of the ridge axis. The row projects no subject."
        },
        {
          "row_index": 115,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block places the Rainbow massif at a non-transform discontinuity, which supports the name but says nothing about it being volcanic; the volcanic-edifice kind the row projects is not stated there. The row projects no subject."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the RTI segment RC1 and treats it as one of the ridge subsections. The row projects no subject."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names a short ridge segment RC2 among the four subsections. The row projects no subject."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ridge segment south of NTD2 as RC3. The row projects no subject."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Romanche transform fault as one of the two bounding transforms. The row projects no subject."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the eastern Romanche ridge-transform intersection and its abbreviation, and the figure caption repeats it. The row projects no subject."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports peridotites observed on the sea floor, which supports the name and treating the sea floor as a surface. The row projects no subject."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Southwest Indian Ridge and its abbreviation as a spreading ridge. The row projects no subject."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block marks volcanic cones on the RC2 map, supporting the name and the volcanic-edifice kind. The row projects no subject."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says a one-dimensional velocity model was sought to compute travel times, which is the name the row projects. The row projects no subject."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block applies a CO2 solubility model to the melt, which is the name projected. The row projects no subject."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks refer to the depth resolution tests carried out on the locations. The row projects no subject."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says the hypocentres were relocated with a double-difference location method. The row projects no subject."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says focal mechanisms were determined from P-phase first-motion polarities. The row projects no subject."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says the CO2 concentrations were computed after correcting for fractional crystallisation. The row projects no subject."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says magnitudes were determined on the local magnitude scale ML. The row projects no subject."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says a non-linear earthquake location algorithm produced the hypocentres. The row projects no subject."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the non-linear oct-tree search algorithm used for the initial locations. The row projects no subject."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name the short-term-average/long-term-average trigger algorithm used for detection. The row projects no subject."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block attributes the isotherms to a simulated thermal model. The row projects no subject."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says Wadati diagrams yielded the Vp/Vs ratio. The row projects no subject."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks give the CO2/Ba ratio with the same central value and the same uncertainty, and attribute it to undegassed MORBs and melt inclusions, which is what the row projects. The row projects no subject."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks give the CO2/Rb ratio with the same central value and the same uncertainty, and attribute it to undegassed MORBs and melt inclusions, which is what the row projects. The row projects no subject."
        },
        {
          "row_index": 138,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block does say the Wadati diagrams yield a Vp/Vs ratio used to estimate S-wave velocity in the inversion, but it gives that ratio as approximate, and the row projects a bare value with no uncertainty and no approximation marker. The row projects no subject."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block says regional basaltic rock samples and their geochemical analyses were synthesised, which is the name, the basalt kind and the description projected. The row projects no subject."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks report basalts observed on the sea floor and label them on the sample map. The row projects no subject."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to olivine melt inclusions used to define the global volatile trends. The row projects no subject."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says published geochemical analyses of MORB samples inside the network were compiled, and spells out mid-ocean ridge basalts. The row projects no subject."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006",
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks report peridotites observed on the sea floor and label them on the sample map. The row projects no subject."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports pillow basalts alongside peridotites on the sea floor at NTD1. The row projects no subject."
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block lists popping rocks among the plotted sample groups. The row projects no subject."
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block says regional basaltic rock samples and their geochemical analyses were synthesised, which is the name, the basalt kind and the description projected. The row projects no subject."
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks report basalts observed on the sea floor and label them on the sample map. The row projects no subject."
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to olivine melt inclusions used to define the global volatile trends. The row projects no subject."
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says published geochemical analyses of MORB samples inside the network were compiled, and spells out mid-ocean ridge basalts. The row projects no subject."
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006",
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks report peridotites observed on the sea floor and label them on the sample map. The row projects no subject."
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports pillow basalts alongside peridotites on the sea floor at NTD1. The row projects no subject."
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block lists popping rocks among the plotted sample groups. The row projects no subject."
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports the located earthquakes of this study, which is the set the row names and the measured modality it projects. The row projects no subject."
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block reports deep earthquakes in the mantle along the ridge axis as an observation of this study. The row projects no subject."
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the subset of events at 10 to 20 km along the cross-section whose depths were held fixed, matching the name and the description. The row projects no subject."
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-2 block carries the MAR label and the event total for that profile, which is the set the row names and describes. The row projects no subject."
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports normal-depth earthquakes beneath the southern NTD2 as one of the three key observations. The row projects no subject."
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports off-axis shallow microseismicity west of the RC2 axis. The row projects no subject."
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports the shallow earthquakes on the outside corner of the RTI as one of the three key observations. The row projects no subject."
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-2 block carries the transform label and the event total for that profile, which is the set the row names and describes. The row projects no subject."
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the sub-dataset assembled for the minimum-1-D velocity search, matching the name and the description. The row projects no subject."
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an earthquake cluster observed on the western side of the axial valley. The row projects no subject."
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block the relation is derived from says the axial valley floor is cut by ridge-parallel normal faults, which is exactly the pairing and the cutting relation projected; the endpoints are introduced a page earlier, so the relation's own block is not one of theirs."
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block names the Logachev Seamount of Knipovich Ridge, which states the part-whole pairing, and it is also the block that introduces both endpoints."
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block says the surface of the core complex is heavily cut by normal faults, which is the pairing and the cutting relation; that block also formalises the faults."
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The figure-caption block places the core complex on the outside corner of the ridge, which supports locating it in the ridge; the same block also formalises the ridge."
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block says the RTI segment is bounded to the east by a detachment fault, and it introduces both endpoints as well."
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block places segment RC2 immediately south of NTD1, which supports adjacency; both endpoints are introduced in the earlier segment-naming block, not in this one."
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block names RC3 as the ridge segment south of NTD2, which supports adjacency and also introduces both endpoints."
        },
        {
          "row_index": 170,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block places the MAR segment between the Romanche and Chain transforms, so the bounding pairing holds and the block also introduces both endpoints, but the row's target projection describes Chain as the southern of the two and the reading never says which of the pair is southern."
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block places the MAR segment between the Romanche and Chain transforms, which supports this bounding pairing, and it introduces both endpoints."
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The block puts the extinct vent field on the eastern flank of NTD1, which supports the containment pairing, and it also formalises the vent field."
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006",
            "page:2:block:001",
            "page:3:block:003"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block reports pillow basalts and peridotites present on the sea floor, which supports the hosting pairing; both endpoints are formalised in earlier blocks."
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006",
            "page:2:block:001",
            "page:3:block:003"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block reports pillow basalts and peridotites present on the sea floor, which supports the hosting pairing; both endpoints are formalised in earlier blocks."
        },
        {
          "row_index": 175,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The methods block says the MORB samples were compiled from the PetDB database, which is the reporting pairing, and that block also formalises the database."
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:6:block:005",
            "page:8:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The methods block says the MORB samples were compiled from the PetDB database, which is the reporting pairing, and that block also formalises the database."
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The block reports the earthquake cluster on the western side of the axial valley, which supports locating it in the valley, and it also formalises the cluster."
        },
        {
          "row_index": 178,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block states that the deep microseismicity lies beneath the ridge axis of segment RC2, which is the pairing projected; neither endpoint is formalised in that block."
        },
        {
          "row_index": 179,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:007",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block says events of that count were located along the ridge, which supports the pairing; the event set is formalised from the figure block and the ridge from the title and caption blocks, so not from this one."
        },
        {
          "row_index": 180,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block reports normal-depth earthquakes occurring beneath the southern NTD2, which is the pairing, and it also formalises the event set."
        },
        {
          "row_index": 181,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004",
            "page:3:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block puts the majority of shallow earthquakes on the outside corner of the RTI, which supports the pairing, and it also formalises the event set."
        },
        {
          "row_index": 182,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block says events of that count were located along the Romanche transform, which supports the pairing; neither endpoint is formalised in that block."
        },
        {
          "row_index": 183,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:10:block:045",
            "page:10:block:048",
            "page:11:block:003",
            "page:11:block:005",
            "page:11:block:006",
            "page:1:block:001",
            "page:1:block:006",
            "page:2:block:008",
            "page:3:block:006",
            "page:4:block:008",
            "page:5:block:011",
            "page:6:block:006",
            "page:7:block:013",
            "page:8:block:018",
            "page:9:block:056"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, the paper itself, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 184,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, OCC, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 185,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, BDB, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 186,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, lithosphere, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 187,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 188,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mantle, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 189,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, detachment fault, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 190,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mantle source, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 191,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, mantle, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 192,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, lithosphere, is named in that same block, so the claim is anchored to it there. The block goes on to set the idea aside, which is the disposition projected."
        },
        {
          "row_index": 193,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006",
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 194,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 195,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mantle, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 196,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 197,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, LAB, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 198,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:002",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 199,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, lithosphere, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 200,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:003",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 201,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, crust, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 202,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 203,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a negative finding, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 204,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a negative finding, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 205,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a negative finding, which matches the modality projected. The subject shown, median valley, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 206,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 207,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:006",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, Mid-Atlantic Ridge, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 208,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mantle, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 209,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:003",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 210,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 211,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a negative finding, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 212,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block does carry the limitation the row states and does name the supersegment, but what it qualifies is the microseismicity record, not the supersegment, so the block supports the claim without supporting that the record is about the subject shown"
        },
        {
          "row_index": 213,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mylonite shear zones, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 214,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, SWIR, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 215,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 216,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, depth resolution tests, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 217,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, 1-D velocity model, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 218,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:003",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, basalts, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 219,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:003",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, basalts, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 220,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there. The block also marks it as the authors' preferred explanation, which is the disposition projected."
        },
        {
          "row_index": 221,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there. The block goes on to set the idea aside, which is the disposition projected."
        },
        {
          "row_index": 222,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a measurement, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 223,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 224,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 225,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 226,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there. The block goes on to set the idea aside, which is the disposition projected."
        },
        {
          "row_index": 227,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 228,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 229,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 230,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, off-axis shallow microseismicity, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 231,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, shallow earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 232,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 5 the row projects, for 1-D P-wave velocity models constructed from the refraction profile. The subject shown, 1-D velocity model, is named in the same block."
        },
        {
          "row_index": 233,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 45 the row projects, for events at 10 to 20 km depth along cross-section cc'. The subject shown, subset, is named in the same block."
        },
        {
          "row_index": 234,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 760 the row projects, for earthquakes identified and registered into the SEISAN database. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 235,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a measurement. The block gives the count of 514 the row projects, for earthquakes located in the vicinity of the Romanche RTI region. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 236,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 4 the row projects, for categories the earthquake locations were classified into. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 237,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 317 the row projects, for events shown along the Mid-Atlantic Ridge profile. The subject shown, events, is named in the same block."
        },
        {
          "row_index": 238,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 364 the row projects, for well-constrained events for which double-difference relocations were determined. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 239,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 197 the row projects, for events shown along the Romanche transform fault profile. The subject shown, events, is named in the same block."
        },
        {
          "row_index": 240,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 360 the row projects, for earthquakes in the sub-dataset used with VELEST. The subject shown, sub-dataset, is named in the same block."
        },
        {
          "row_index": 241,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 276 the row projects, for events well relocated and used in the final catalog. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 242,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.4 to 3.0 wt% the row projects and frames it as a calculation. The block gives it as approximate, which the row carries. It is derived in the block, matching the status projected. The subject shown, melt, is named in the same block."
        },
        {
          "row_index": 243,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 1250 \u00b0C the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, LAB, is named in the same block."
        },
        {
          "row_index": 244,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 89 ppm the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 245,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 20 km the row projects and frames it as a hypothesis. The block gives it as approximate, which the row carries. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 246,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 700 \u00b0C the row projects and frames it as a plain statement. The block also gives the stated uncertainty the row carries. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 247,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 10 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 248,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 10 km the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 249,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 0.4 wt% the row projects and frames it as a calculation. The block gives it as a one-sided bound, which the row carries. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 250,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.7 to 4.6 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 251,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.06 to 0.8 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 252,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.4 to 3.0 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 253,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.04 to 0.5 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 254,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:005",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.4 to 3.0 wt% the row projects and frames it as a calculation. It is derived in the block, matching the status projected. The subject shown, melt, is named in the same block."
        },
        {
          "row_index": 255,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.04 to 0.7 wt% the row projects and frames it as a calculation. It is derived in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 256,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.9 to 4.3 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 257,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.07 to 1.0 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 258,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.5 to 2.8 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 259,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.05 to 0.7 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 260,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 600 to 800 \u00b0C the row projects and frames it as a hypothesis. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 261,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 120 km the row projects and frames it as a plain statement. The subject shown, Mid-Atlantic Ridge, is named in the same block."
        },
        {
          "row_index": 262,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 140 km the row projects and frames it as a plain statement. The subject shown, Romanche TF, is named in the same block."
        },
        {
          "row_index": 263,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 8 Ma the row projects and frames it as a plain statement. The subject shown, crust, is named in the same block."
        },
        {
          "row_index": 264,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 5.4 km the row projects and frames it as a plain statement. The block also gives the stated uncertainty the row carries. The subject shown, crust, is named in the same block."
        },
        {
          "row_index": 265,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 60 to 70 km the row projects and frames it as a plain statement. The subject shown, mantle, is named in the same block."
        },
        {
          "row_index": 266,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 2800 ppm the row projects and frames it as a calculation. The block gives it as approximate, which the row carries. It is estimated in the block, matching the status projected. The subject shown, equatorial Atlantic Ocean, is named in the same block."
        },
        {
          "row_index": 267,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 8799 ppm the row projects and frames it as a calculation. The block gives it as a one-sided bound, which the row carries. It is estimated in the block, matching the status projected. The subject shown, equatorial Atlantic Ocean, is named in the same block."
        },
        {
          "row_index": 268,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 16 mm/yr the row projects and frames it as a plain statement. The subject shown, Mid-Atlantic Ridge, is named in the same block."
        },
        {
          "row_index": 269,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 1100 \u00b0C the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, mantle, is named in the same block."
        },
        {
          "row_index": 270,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 10 km the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, Iceland, is named in the same block."
        },
        {
          "row_index": 271,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:5:block:010",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 750 \u00b0C the row projects and frames it as a plain statement. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 272,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 45 Ma the row projects and frames it as a plain statement. The subject shown, lithosphere, is named in the same block."
        },
        {
          "row_index": 273,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 30 km the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, Mayotte, is named in the same block."
        },
        {
          "row_index": 274,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 10 km the row projects and frames it as a plain statement. The subject shown, median valley, is named in the same block."
        },
        {
          "row_index": 275,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 1.1 % the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, LAB, is named in the same block."
        },
        {
          "row_index": 276,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 1100 to 1200 \u00b0C the row projects and frames it as a plain statement. It is modelled in the block, matching the status projected. The subject shown, mantle, is named in the same block."
        },
        {
          "row_index": 277,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 35 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, NTD1, is named in the same block."
        },
        {
          "row_index": 278,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 10 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, NTD2, is named in the same block."
        },
        {
          "row_index": 279,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 10 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, NTD2, is named in the same block."
        },
        {
          "row_index": 280,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 33 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, NTD2, is named in the same block."
        },
        {
          "row_index": 281,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 6 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, OCC, is named in the same block."
        },
        {
          "row_index": 282,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.7 to 4.6 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, melt, is named in the same block."
        },
        {
          "row_index": 283,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:007",
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the half-width the row projects with its unit, but it gives it as a plotting convention for the depth profiles of a figure; the ridge is named only as the line the profile follows, so the block does not support the ridge being what this measurement is about"
        },
        {
          "row_index": 284,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 8 ppm the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 285,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 22 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 286,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 50 km the row projects and frames it as a plain statement. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 287,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 0.7 GPa the row projects and frames it as a calculation. The block gives it as approximate, which the row carries. It is modelled in the block, matching the status projected. The subject shown, melt, is named in the same block."
        },
        {
          "row_index": 288,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 200 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, MAR supersegment, is named in the same block."
        },
        {
          "row_index": 289,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 1.9 wt% the row projects and frames it as a plain statement. The subject shown, SWIR, is named in the same block."
        },
        {
          "row_index": 290,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the transect half-width and unit the row projects, but as a plotting convention for two figure transects; the core complex is named only as what the transects run along and across, not as what the measurement is about"
        },
        {
          "row_index": 291,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 150 to 300 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, mantle, is named in the same block."
        },
        {
          "row_index": 292,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 332 ppm the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, LAB, is named in the same block."
        },
        {
          "row_index": 293,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 7.5 Ma the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, crust, is named in the same block."
        },
        {
          "row_index": 294,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, 1-D velocity model, is named in the same block."
        },
        {
          "row_index": 295,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, subset, is named in the same block."
        },
        {
          "row_index": 296,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 297,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a measurement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 298,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 299,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, events, is named in the same block."
        },
        {
          "row_index": 300,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 301,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, events, is named in the same block."
        },
        {
          "row_index": 302,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, sub-dataset, is named in the same block."
        },
        {
          "row_index": 303,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 304,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 10 to 20 km the row projects and frames it as a measurement. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 305,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 2.6 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 306,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 2.1 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 307,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 10 to 20 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 308,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 10 to 19 km the row projects and frames it as a hypothesis. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 309,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 16 to 19 km the row projects and frames it as a measurement. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 310,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 10 to 20 km the row projects and frames it as a plain statement. The subject shown, subset, is named in the same block."
        },
        {
          "row_index": 311,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 5 Hz the row projects and frames it as a hypothesis. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 312,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 4 to 10 km the row projects and frames it as a measurement. It is measured in the block, matching the status projected. The subject shown, normal-depth earthquakes, is named in the same block."
        },
        {
          "row_index": 313,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 6 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, off-axis shallow microseismicity, is named in the same block."
        },
        {
          "row_index": 314,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 10 km the row projects and frames it as a hypothesis. The block gives it as a one-sided bound, which the row carries. The subject shown, off-axis shallow microseismicity, is named in the same block."
        },
        {
          "row_index": 315,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 78 % the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 316,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 10 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 317,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0 to 6 km the row projects and frames it as a measurement. It is measured in the block, matching the status projected. The subject shown, shallow earthquakes, is named in the same block."
        },
        {
          "row_index": 318,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 2 to 6 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, earthquake cluster, is named in the same block."
        },
        {
          "row_index": 319,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion gives this ratio with the numerator, denominator, central value and uncertainty the row projects, framed as a calculation. The subject shown, MORB samples, is named in the same block."
        },
        {
          "row_index": 320,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion gives this ratio with the numerator, denominator, central value and uncertainty the row projects, framed as a calculation. The subject shown, MORB samples, is named in the same block."
        },
        {
          "row_index": 321,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion gives this ratio with the numerator, denominator, central value and uncertainty the row projects, framed as a calculation. The subject shown, MORB samples, is named in the same block."
        },
        {
          "row_index": 322,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion gives this ratio with the numerator, denominator, central value and uncertainty the row projects, framed as a calculation. The subject shown, MORB samples, is named in the same block."
        }
      ]
    },
    {
      "question_id": "CQ-04",
      "question_responsiveness": "PARTIAL",
      "responsiveness_rationale": "The rows do return the preferred mechanism and they mark its epistemic standing. A claim row states that the deep microseismicity beneath the segment is related to CO2 degassing from the ascending melt, carries a hypothesised modality, and is the only row in the set whose disposition is preferred, while the rival explanations carry the same modality with a not-supported disposition, so a reader can tell the preferred hypothesis from the rejected ones and can tell that none is offered as established fact. Rows also carry the ascending melt, the CO2 degassing, the volume change, the pressure increase and the triggering of the deep earthquakes. What no row carries in any projected field is the extensional stress state the reading makes a condition of that mechanism. The assertion the relevant row points to contains it, so it is reachable through the capture, but the claim as projected drops it, and a reader of the rows alone gets the mechanism without the stress condition it depends on. One requested part of the question is therefore addressed only behind the rows and not in them.",
      "source_locators": [
        "page:1:block:001",
        "page:5:block:002",
        "page:5:block:003",
        "page:7:block:012"
      ],
      "rows": [
        {
          "row_index": 0,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Askja as a volcano in Iceland, which is the name and the volcanic-edifice kind the row projects. The row projects no subject."
        },
        {
          "row_index": 1,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces axial melt lenses at fast- and intermediate-spreading ridges, giving both the name and the melt-body kind. The row projects no subject."
        },
        {
          "row_index": 2,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes a median valley along the RC2 ridge segment, which carries the name and the axial-valley kind. The row projects no subject."
        },
        {
          "row_index": 3,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block defines the brittle-ductile boundary and its abbreviation, and treats it as a boundary within the lithosphere. The row projects no subject."
        },
        {
          "row_index": 4,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Chain as one of the two transform faults bounding the MAR segment, so the name and the fault kind hold, but nowhere in the reading is Chain said to be the southern of the two, and the row projects that as its description. The row projects no subject."
        },
        {
          "row_index": 5,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block treats oceanic crust as the layer formed from mantle melt at spreading centres, matching the name and the layer kind. The row projects no subject."
        },
        {
          "row_index": 6,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes a westward dipping detachment fault bounding the RTI segment, giving the name and the fault kind. The row projects no subject."
        },
        {
          "row_index": 7,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks place the study in the equatorial Atlantic Ocean and treat it as an ocean region. The row projects no subject."
        },
        {
          "row_index": 8,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an extinct hydrothermal vent field on the eastern flank of NTD1, which is the name, the kind and the description the row projects. The row projects no subject."
        },
        {
          "row_index": 9,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Fagradalsfjall as a peninsula in Iceland, supporting the name and a landmass classification. The row projects no subject."
        },
        {
          "row_index": 10,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:009"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Gakkel Ridge among ultraslow-spreading ridges, which gives both the name and the spreading-ridge kind. The row projects no subject."
        },
        {
          "row_index": 11,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure caption in the block reports an inactive hydrothermal mound seen on the Nautile dives, matching the name, the hydrothermal kind and the description. The row projects no subject."
        },
        {
          "row_index": 12,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block places Askja and Fagradalsfjall in Iceland, supporting the name and a landmass classification. The row projects no subject."
        },
        {
          "row_index": 13,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to reflections beneath the young Juan de Fuca plate, giving the name and the plate kind. The row projects no subject."
        },
        {
          "row_index": 14,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names Knipovich Ridge as one of the ridges whose depth data were updated, supporting the name and the spreading-ridge kind. The row projects no subject."
        },
        {
          "row_index": 15,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks give the lithosphere-asthenosphere boundary and its abbreviation and treat it as a boundary surface. The row projects no subject."
        },
        {
          "row_index": 16,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks discuss the brittle lithosphere and its thickness, which supports the name and the layer kind. The row projects no subject."
        },
        {
          "row_index": 17,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Logachev Seamount of Knipovich Ridge; a seamount is a volcanic edifice, which is the kind projected. The row projects no subject."
        },
        {
          "row_index": 18,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block treats the mantle as the source of the melt beneath spreading centres, which supports the name and the layer kind. The row projects no subject."
        },
        {
          "row_index": 19,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block invokes an enriched mantle source near the Romanche transform to explain the enriched basalts, matching the name, the kind and the description. The row projects no subject."
        },
        {
          "row_index": 20,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks name the Mid-Atlantic Ridge and its abbreviation and treat it as the spreading ridge under study. The row projects no subject."
        },
        {
          "row_index": 21,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks refer to the MAR segment between the two transforms and later call it a supersegment, supporting the name and the ridge-segment kind. The row projects no subject."
        },
        {
          "row_index": 22,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to offshore Mayotte Island, supporting the name and a landmass classification. The row projects no subject."
        },
        {
          "row_index": 23,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The cited blocks discuss the melt and its behaviour beneath the ridge, supporting the name and the melt-body kind. The row projects no subject."
        },
        {
          "row_index": 24,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010",
            "page:7:block:011"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The schematic-figure blocks label the Moho and call it the expected Moho interface, which is the name and the boundary kind. The row projects no subject."
        },
        {
          "row_index": 25,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block refers to high-temperature hydrated mylonite shear zones along transform faults, giving the name and the shear-zone kind. The row projects no subject."
        },
        {
          "row_index": 26,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an oriented neo-volcanic ridge in the RC2 valley, supporting the name and the volcanic-edifice kind. The row projects no subject."
        },
        {
          "row_index": 27,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes normal faults cutting the OCC surface, supporting the name and the fault kind. The row projects no subject."
        },
        {
          "row_index": 28,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the first non-transform discontinuity and names it NTD1. The row projects no subject."
        },
        {
          "row_index": 29,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces the second non-transform discontinuity and names it NTD2. The row projects no subject."
        },
        {
          "row_index": 30,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block introduces a prominent oceanic core complex and its abbreviation on the eastern side of the ridge axis. The row projects no subject."
        },
        {
          "row_index": 31,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block places the Rainbow massif at a non-transform discontinuity, which supports the name but says nothing about it being volcanic; the volcanic-edifice kind the row projects is not stated there. The row projects no subject."
        },
        {
          "row_index": 32,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the RTI segment RC1 and treats it as one of the ridge subsections. The row projects no subject."
        },
        {
          "row_index": 33,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names a short ridge segment RC2 among the four subsections. The row projects no subject."
        },
        {
          "row_index": 34,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the ridge segment south of NTD2 as RC3. The row projects no subject."
        },
        {
          "row_index": 35,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Romanche transform fault as one of the two bounding transforms. The row projects no subject."
        },
        {
          "row_index": 36,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:005"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the eastern Romanche ridge-transform intersection and its abbreviation, and the figure caption repeats it. The row projects no subject."
        },
        {
          "row_index": 37,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports peridotites observed on the sea floor, which supports the name and treating the sea floor as a surface. The row projects no subject."
        },
        {
          "row_index": 38,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the Southwest Indian Ridge and its abbreviation as a spreading ridge. The row projects no subject."
        },
        {
          "row_index": 39,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:007"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block marks volcanic cones on the RC2 map, supporting the name and the volcanic-edifice kind. The row projects no subject."
        },
        {
          "row_index": 40,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says a one-dimensional velocity model was sought to compute travel times, which is the name the row projects. The row projects no subject."
        },
        {
          "row_index": 41,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block applies a CO2 solubility model to the melt, which is the name projected. The row projects no subject."
        },
        {
          "row_index": 42,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks refer to the depth resolution tests carried out on the locations. The row projects no subject."
        },
        {
          "row_index": 43,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says the hypocentres were relocated with a double-difference location method. The row projects no subject."
        },
        {
          "row_index": 44,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says focal mechanisms were determined from P-phase first-motion polarities. The row projects no subject."
        },
        {
          "row_index": 45,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says the CO2 concentrations were computed after correcting for fractional crystallisation. The row projects no subject."
        },
        {
          "row_index": 46,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says magnitudes were determined on the local magnitude scale ML. The row projects no subject."
        },
        {
          "row_index": 47,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says a non-linear earthquake location algorithm produced the hypocentres. The row projects no subject."
        },
        {
          "row_index": 48,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block names the non-linear oct-tree search algorithm used for the initial locations. The row projects no subject."
        },
        {
          "row_index": 49,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW Both cited blocks name the short-term-average/long-term-average trigger algorithm used for detection. The row projects no subject."
        },
        {
          "row_index": 50,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:012"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-caption block attributes the isotherms to a simulated thermal model. The row projects no subject."
        },
        {
          "row_index": 51,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:002"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block says Wadati diagrams yielded the Vp/Vs ratio. The row projects no subject."
        },
        {
          "row_index": 52,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports the located earthquakes of this study, which is the set the row names and the measured modality it projects. The row projects no subject."
        },
        {
          "row_index": 53,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The abstract block reports deep earthquakes in the mantle along the ridge axis as an observation of this study. The row projects no subject."
        },
        {
          "row_index": 54,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the subset of events at 10 to 20 km along the cross-section whose depths were held fixed, matching the name and the description. The row projects no subject."
        },
        {
          "row_index": 55,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-2 block carries the MAR label and the event total for that profile, which is the set the row names and describes. The row projects no subject."
        },
        {
          "row_index": 56,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports normal-depth earthquakes beneath the southern NTD2 as one of the three key observations. The row projects no subject."
        },
        {
          "row_index": 57,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports off-axis shallow microseismicity west of the RC2 axis. The row projects no subject."
        },
        {
          "row_index": 58,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports the shallow earthquakes on the outside corner of the RTI as one of the three key observations. The row projects no subject."
        },
        {
          "row_index": 59,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The figure-2 block carries the transform label and the event total for that profile, which is the set the row names and describes. The row projects no subject."
        },
        {
          "row_index": 60,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block describes the sub-dataset assembled for the minimum-1-D velocity search, matching the name and the description. The row projects no subject."
        },
        {
          "row_index": 61,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "NO_SUBJECT_IN_ROW The block reports an earthquake cluster observed on the western side of the axial valley. The row projects no subject."
        },
        {
          "row_index": 62,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:3:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block the relation is derived from says the axial valley floor is cut by ridge-parallel normal faults, which is exactly the pairing and the cutting relation projected; the endpoints are introduced a page earlier, so the relation's own block is not one of theirs."
        },
        {
          "row_index": 63,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:8:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block names the Logachev Seamount of Knipovich Ridge, which states the part-whole pairing, and it is also the block that introduces both endpoints."
        },
        {
          "row_index": 64,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_LOCAL The block says the surface of the core complex is heavily cut by normal faults, which is the pairing and the cutting relation; that block also formalises the faults."
        },
        {
          "row_index": 65,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DERIVATION_LOCAL The figure-caption block places the core complex on the outside corner of the ridge, which supports locating it in the ridge; the same block also formalises the ridge."
        },
        {
          "row_index": 66,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block says the RTI segment is bounded to the east by a detachment fault, and it introduces both endpoints as well."
        },
        {
          "row_index": 67,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block places segment RC2 immediately south of NTD1, which supports adjacency; both endpoints are introduced in the earlier segment-naming block, not in this one."
        },
        {
          "row_index": 68,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block names RC3 as the ridge segment south of NTD2, which supports adjacency and also introduces both endpoints."
        },
        {
          "row_index": 69,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block places the MAR segment between the Romanche and Chain transforms, so the bounding pairing holds and the block also introduces both endpoints, but the row's target projection describes Chain as the southern of the two and the reading never says which of the pair is southern."
        },
        {
          "row_index": 70,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block places the MAR segment between the Romanche and Chain transforms, which supports this bounding pairing, and it introduces both endpoints."
        },
        {
          "row_index": 71,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DERIVATION_LOCAL The block puts the extinct vent field on the eastern flank of NTD1, which supports the containment pairing, and it also formalises the vent field."
        },
        {
          "row_index": 72,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:2:block:006"
          ],
          "rationale": "DERIVATION_LOCAL The block reports the earthquake cluster on the western side of the axial valley, which supports locating it in the valley, and it also formalises the cluster."
        },
        {
          "row_index": 73,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block states that the deep microseismicity lies beneath the ridge axis of segment RC2, which is the pairing projected; neither endpoint is formalised in that block."
        },
        {
          "row_index": 74,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:007",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block says events of that count were located along the ridge, which supports the pairing; the event set is formalised from the figure block and the ridge from the title and caption blocks, so not from this one."
        },
        {
          "row_index": 75,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DERIVATION_LOCAL The block reports normal-depth earthquakes occurring beneath the southern NTD2, which is the pairing, and it also formalises the event set."
        },
        {
          "row_index": 76,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004",
            "page:3:block:005"
          ],
          "rationale": "DERIVATION_LOCAL The block puts the majority of shallow earthquakes on the outside corner of the RTI, which supports the pairing, and it also formalises the event set."
        },
        {
          "row_index": 77,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DERIVATION_NON_LOCAL The block says events of that count were located along the Romanche transform, which supports the pairing; neither endpoint is formalised in that block."
        },
        {
          "row_index": 78,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, OCC, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 79,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, BDB, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 80,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, lithosphere, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 81,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 82,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:5:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mantle, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 83,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, detachment fault, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 84,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mantle source, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 85,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, mantle, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 86,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, lithosphere, is named in that same block, so the claim is anchored to it there. The block goes on to set the idea aside, which is the disposition projected."
        },
        {
          "row_index": 87,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006",
            "page:5:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 88,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 89,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mantle, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 90,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 91,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, LAB, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 92,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:002",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 93,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, lithosphere, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 94,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:003",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 95,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, crust, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 96,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 97,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a negative finding, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 98,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a negative finding, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 99,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a negative finding, which matches the modality projected. The subject shown, median valley, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 100,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:7:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 101,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:006",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, Mid-Atlantic Ridge, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 102,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mantle, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 103,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:003",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 104,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 105,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a negative finding, which matches the modality projected. The subject shown, RC2, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 106,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block does carry the limitation the row states and does name the supersegment, but what it qualifies is the microseismicity record, not the supersegment, so the block supports the claim without supporting that the record is about the subject shown"
        },
        {
          "row_index": 107,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, mylonite shear zones, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 108,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, SWIR, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 109,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, melt, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 110,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, depth resolution tests, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 111,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, 1-D velocity model, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 112,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there. The block also marks it as the authors' preferred explanation, which is the disposition projected."
        },
        {
          "row_index": 113,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there. The block goes on to set the idea aside, which is the disposition projected."
        },
        {
          "row_index": 114,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a measurement, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 115,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 116,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 117,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 118,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:4:block:002",
            "page:4:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there. The block goes on to set the idea aside, which is the disposition projected."
        },
        {
          "row_index": 119,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 120,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 121,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:8:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a plain statement, which matches the modality projected. The subject shown, deep earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 122,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, off-axis shallow microseismicity, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 123,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The assertion the locator reaches is the sentence this claim summarises and the block frames it as a hypothesis, which matches the modality projected. The subject shown, shallow earthquakes, is named in that same block, so the claim is anchored to it there."
        },
        {
          "row_index": 124,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 5 the row projects, for 1-D P-wave velocity models constructed from the refraction profile. The subject shown, 1-D velocity model, is named in the same block."
        },
        {
          "row_index": 125,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 45 the row projects, for events at 10 to 20 km depth along cross-section cc'. The subject shown, subset, is named in the same block."
        },
        {
          "row_index": 126,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 760 the row projects, for earthquakes identified and registered into the SEISAN database. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 127,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a measurement. The block gives the count of 514 the row projects, for earthquakes located in the vicinity of the Romanche RTI region. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 128,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 4 the row projects, for categories the earthquake locations were classified into. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 129,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 317 the row projects, for events shown along the Mid-Atlantic Ridge profile. The subject shown, events, is named in the same block."
        },
        {
          "row_index": 130,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 364 the row projects, for well-constrained events for which double-difference relocations were determined. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 131,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 197 the row projects, for events shown along the Romanche transform fault profile. The subject shown, events, is named in the same block."
        },
        {
          "row_index": 132,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 360 the row projects, for earthquakes in the sub-dataset used with VELEST. The subject shown, sub-dataset, is named in the same block."
        },
        {
          "row_index": 133,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count of 276 the row projects, for events well relocated and used in the final catalog. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 134,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.4 to 3.0 wt% the row projects and frames it as a calculation. The block gives it as approximate, which the row carries. It is derived in the block, matching the status projected. The subject shown, melt, is named in the same block."
        },
        {
          "row_index": 135,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 1250 \u00b0C the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, LAB, is named in the same block."
        },
        {
          "row_index": 136,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 89 ppm the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 137,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 20 km the row projects and frames it as a hypothesis. The block gives it as approximate, which the row carries. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 138,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 700 \u00b0C the row projects and frames it as a plain statement. The block also gives the stated uncertainty the row carries. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 139,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 10 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 140,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 10 km the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 141,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 0.4 wt% the row projects and frames it as a calculation. The block gives it as a one-sided bound, which the row carries. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 142,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.7 to 4.6 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 143,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.06 to 0.8 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 144,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.4 to 3.0 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 145,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.04 to 0.5 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 146,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:005",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.4 to 3.0 wt% the row projects and frames it as a calculation. It is derived in the block, matching the status projected. The subject shown, melt, is named in the same block."
        },
        {
          "row_index": 147,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.04 to 0.7 wt% the row projects and frames it as a calculation. It is derived in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 148,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.9 to 4.3 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 149,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.07 to 1.0 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 150,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.5 to 2.8 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 151,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:8:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.05 to 0.7 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 152,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 600 to 800 \u00b0C the row projects and frames it as a hypothesis. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 153,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:002",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 120 km the row projects and frames it as a plain statement. The subject shown, Mid-Atlantic Ridge, is named in the same block."
        },
        {
          "row_index": 154,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 140 km the row projects and frames it as a plain statement. The subject shown, Romanche TF, is named in the same block."
        },
        {
          "row_index": 155,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 8 Ma the row projects and frames it as a plain statement. The subject shown, crust, is named in the same block."
        },
        {
          "row_index": 156,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:2:block:006",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 5.4 km the row projects and frames it as a plain statement. The block also gives the stated uncertainty the row carries. The subject shown, crust, is named in the same block."
        },
        {
          "row_index": 157,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 60 to 70 km the row projects and frames it as a plain statement. The subject shown, mantle, is named in the same block."
        },
        {
          "row_index": 158,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 2800 ppm the row projects and frames it as a calculation. The block gives it as approximate, which the row carries. It is estimated in the block, matching the status projected. The subject shown, equatorial Atlantic Ocean, is named in the same block."
        },
        {
          "row_index": 159,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:007",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 8799 ppm the row projects and frames it as a calculation. The block gives it as a one-sided bound, which the row carries. It is estimated in the block, matching the status projected. The subject shown, equatorial Atlantic Ocean, is named in the same block."
        },
        {
          "row_index": 160,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:1:block:005",
            "page:2:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 16 mm/yr the row projects and frames it as a plain statement. The subject shown, Mid-Atlantic Ridge, is named in the same block."
        },
        {
          "row_index": 161,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 1100 \u00b0C the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, mantle, is named in the same block."
        },
        {
          "row_index": 162,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 10 km the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, Iceland, is named in the same block."
        },
        {
          "row_index": 163,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:5:block:010",
            "page:7:block:011"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 750 \u00b0C the row projects and frames it as a plain statement. The subject shown, BDB, is named in the same block."
        },
        {
          "row_index": 164,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:004",
            "page:2:block:005",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 45 Ma the row projects and frames it as a plain statement. The subject shown, lithosphere, is named in the same block."
        },
        {
          "row_index": 165,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:4:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 30 km the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, Mayotte, is named in the same block."
        },
        {
          "row_index": 166,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 10 km the row projects and frames it as a plain statement. The subject shown, median valley, is named in the same block."
        },
        {
          "row_index": 167,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 1.1 % the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, LAB, is named in the same block."
        },
        {
          "row_index": 168,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 1100 to 1200 \u00b0C the row projects and frames it as a plain statement. It is modelled in the block, matching the status projected. The subject shown, mantle, is named in the same block."
        },
        {
          "row_index": 169,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 35 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, NTD1, is named in the same block."
        },
        {
          "row_index": 170,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 10 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, NTD2, is named in the same block."
        },
        {
          "row_index": 171,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 10 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, NTD2, is named in the same block."
        },
        {
          "row_index": 172,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 33 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, NTD2, is named in the same block."
        },
        {
          "row_index": 173,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 6 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, OCC, is named in the same block."
        },
        {
          "row_index": 174,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0.7 to 4.6 wt% the row projects and frames it as a calculation. It is estimated in the block, matching the status projected. The subject shown, melt, is named in the same block."
        },
        {
          "row_index": 175,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:007",
            "page:3:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the half-width the row projects with its unit, but it gives it as a plotting convention for the depth profiles of a figure; the ridge is named only as the line the profile follows, so the block does not support the ridge being what this measurement is about"
        },
        {
          "row_index": 176,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:5:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 8 ppm the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 177,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 22 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, RC2, is named in the same block."
        },
        {
          "row_index": 178,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 50 km the row projects and frames it as a plain statement. The subject shown, RC3, is named in the same block."
        },
        {
          "row_index": 179,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 0.7 GPa the row projects and frames it as a calculation. The block gives it as approximate, which the row carries. It is modelled in the block, matching the status projected. The subject shown, melt, is named in the same block."
        },
        {
          "row_index": 180,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:005",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 200 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, MAR supersegment, is named in the same block."
        },
        {
          "row_index": 181,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 1.9 wt% the row projects and frames it as a plain statement. The subject shown, SWIR, is named in the same block."
        },
        {
          "row_index": 182,
          "source_support": "PARTIAL",
          "source_locators": [
            "page:1:block:005",
            "page:4:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The block gives the transect half-width and unit the row projects, but as a plotting convention for two figure transects; the core complex is named only as what the transects run along and across, not as what the measurement is about"
        },
        {
          "row_index": 183,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 150 to 300 km the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, mantle, is named in the same block."
        },
        {
          "row_index": 184,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:010",
            "page:6:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 332 ppm the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, LAB, is named in the same block."
        },
        {
          "row_index": 185,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:002",
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 7.5 Ma the row projects and frames it as a plain statement. The block gives it as a one-sided bound, which the row carries. The subject shown, crust, is named in the same block."
        },
        {
          "row_index": 186,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:002",
            "page:6:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, 1-D velocity model, is named in the same block."
        },
        {
          "row_index": 187,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, subset, is named in the same block."
        },
        {
          "row_index": 188,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:002"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 189,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:6:block:005"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a measurement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 190,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 191,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, events, is named in the same block."
        },
        {
          "row_index": 192,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 193,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, events, is named in the same block."
        },
        {
          "row_index": 194,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:6:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, sub-dataset, is named in the same block."
        },
        {
          "row_index": 195,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion is where this count is stated and the block frames it as a plain statement. The block gives the count this record was drawn from. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 196,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 10 to 20 km the row projects and frames it as a measurement. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 197,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:009"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 2.6 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 198,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:3:block:004",
            "page:7:block:007"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 2.1 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 199,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 10 to 20 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 200,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:012"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 10 to 19 km the row projects and frames it as a hypothesis. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 201,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 16 to 19 km the row projects and frames it as a measurement. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 202,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 10 to 20 km the row projects and frames it as a plain statement. The subject shown, subset, is named in the same block."
        },
        {
          "row_index": 203,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:5:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 5 Hz the row projects and frames it as a hypothesis. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 204,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 4 to 10 km the row projects and frames it as a measurement. It is measured in the block, matching the status projected. The subject shown, normal-depth earthquakes, is named in the same block."
        },
        {
          "row_index": 205,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 6 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, off-axis shallow microseismicity, is named in the same block."
        },
        {
          "row_index": 206,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:3:block:001",
            "page:5:block:001"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the upper bound 10 km the row projects and frames it as a hypothesis. The block gives it as a one-sided bound, which the row carries. The subject shown, off-axis shallow microseismicity, is named in the same block."
        },
        {
          "row_index": 207,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:003",
            "page:7:block:008"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the value 78 % the row projects and frames it as a plain statement. The block gives it as approximate, which the row carries. The subject shown, earthquakes, is named in the same block."
        },
        {
          "row_index": 208,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:1:block:001",
            "page:7:block:010"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the lower bound 10 km the row projects and frames it as a measurement. The block gives it as a one-sided bound, which the row carries. It is measured in the block, matching the status projected. The subject shown, deep earthquakes, is named in the same block."
        },
        {
          "row_index": 209,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:004"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 0 to 6 km the row projects and frames it as a measurement. It is measured in the block, matching the status projected. The subject shown, shallow earthquakes, is named in the same block."
        },
        {
          "row_index": 210,
          "source_support": "SUPPORTED",
          "source_locators": [
            "page:2:block:006"
          ],
          "rationale": "DIGEST_OK SUBJECT_IN_BLOCK The located assertion states the range 2 to 6 km the row projects and frames it as a measurement. The block gives it as approximate, which the row carries. It is measured in the block, matching the status projected. The subject shown, earthquake cluster, is named in the same block."
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
  "rationale": "DIGEST_OK SUBJECT_IN_BLOCK one or two sentences in your own words"
}
```
